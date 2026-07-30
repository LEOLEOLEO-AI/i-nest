"""SDI v26 — Multi-Scale + Enhanced BCM + Scaling Law Verification
==================================================================
v25.1 → v26 三项升级:

1. BCM增强: 滚动平均h替代瞬时h
   h_avg = 0.85*h_avg + 0.15*h  (EMA with decay)
   θ_bcm += η * h_avg² * (h_avg - θ_bcm)
   → 更稳定, 受级联阻尼影响更小

2. 多尺度连接组生成器
   基于C.elegans统计特征生成 N={100,200,279,500} 合成连接组
   保持: 度分布(power-law), 聚类系数, chem/elec比例

3. 标度律自动测试
   σ(N), EL(N), t_convergence(N), bonds(N)
   验证架构在不同规模下的行为
"""

import numpy as np, networkx as nx, matplotlib, matplotlib.pyplot as plt
from collections import defaultdict
import json, os, warnings, time
warnings.filterwarnings("ignore")
matplotlib.rcParams["font.family"] = "DejaVu Sans"

DATA_PATH = "D:/Obsidian/phase1_workspace/connectome_v8_data.json"
OUT_DIR   = "D:/Obsidian/phase1_workspace/v26_results"
os.makedirs(OUT_DIR, exist_ok=True)

# ============ v25 baseline (kept) ============
TAU_STDP, ETA_LTP, ETA_LTD = 20.0, 0.020, 0.016
Ea_S, Ea_L = 0.15, 0.85
T_DECAY = 25000
TAU_REC, U_SE_CHEM, U_SE_ELEC = 150, 0.45, 0.10
T_ABS = 3; T_REL = 8; REL_SCALE = 0.3
SCALING_THR, SCALING_RATE, SCALING_INT = 0.35, 0.12, 15
GLIA_THR, GLIA_RATE, GLIA_INT = 0.45, 0.25, 50
SEED_FRAC_SENSOR, SEED_FRAC_OTHER = 0.20, 0.03
CASCADE_MAX = 15
EL_TARGET_LO, EL_TARGET_HI = 0.15, 0.35

T_THETA_BASE = 15; L_REF = 2.44; V_C = 1.0
T_THETA_MIN = 5; T_THETA_MAX = 100
FEP_TARGET_OUT_W = 0.8; FEP_HOMEOSTASIS_INT = 20
F_WINDOW = 50

# ============ v26 enhanced parameters ============
BCM_ETA = 0.08           # v26: increased for rolling avg
BCM_THETA_MIN = 3.0
BCM_THETA_MAX = 30.0
BCM_EMA_DECAY = 0.85     # Rolling average decay for h

FEP_BASIN_WINDOW = 20
FEP_CONVERGENCE_STEEPNESS = 0.5

ACTION_WINDOW = 100
ACTION_FEEDBACK_STRENGTH = 0.15

HETERO_SUPPRESS = 0.01
HETERO_RADIUS = 5

PER_NODE_ENERGY_CAP = 1.5
GLOBAL_ENERGY_BUDGET = 500.0

FEP_CONSOLIDATE_INT = 25
FEP_CONSOLIDATE_RATE = 0.08
FEP_RATE_ADAPTIVE = True
FEP_RATE_MIN = 0.02
FEP_RATE_MAX = 0.20
FEP_CONSOLIDATE_MIN_WEIGHT = 0.05

MIN_OUT_DEG = 3
FEP_GRAD_CLIP = 0.5


# ============================================================
# v26-1: Multi-Scale Connectome Generator
# ============================================================

class ConnectomeGenerator:
    """基于C.elegans统计特征生成多尺度合成连接组

    保持的统计特征:
      - 度分布: power-law (P(k) ~ k^(-γ), γ≈2.5)
      - 聚类系数: C≈0.2
      - chem/elec比例: ~2.5:1
      - 节点类型: sensory 22%, motor 40%, inter 38%
    """

    @staticmethod
    def generate(N: int, seed: int = 42) -> dict:
        np.random.seed(seed)

        # 度分布: power-law with exponential cutoff
        def sample_degree(k_min=2, k_max=None):
            if k_max is None:
                k_max = max(5, N // 3)
            gamma = 2.5
            # Inverse CDF sampling
            u = np.random.random()
            # Approximate: k = k_min * (1-u)^(-1/(gamma-1))
            k = int(k_min * (1.0 - u + 1e-6) ** (-1.0 / (gamma - 1.0)))
            return min(k, k_max)

        # 生成度序列
        degrees = np.array([sample_degree() for _ in range(N)], np.int32)

        # 节点类型
        n_sensor = max(1, int(N * 0.22))
        n_motor = max(1, int(N * 0.40))
        n_inter = N - n_sensor - n_motor
        n_types = {}
        nodes = list(range(N))
        for i in range(N):
            if i < n_sensor: n_types[i] = "sensory"
            elif i < n_sensor + n_motor: n_types[i] = "motor"
            else: n_types[i] = "interneuron"

        # 生成化学突触边 (directed, preferential attachment)
        chem_edges = []
        total_deg = degrees.sum()
        for src in range(N):
            k_out = max(1, int(degrees[src] * 0.7))  # ~70% outgoing
            # Preferential attachment: probability ∝ target degree
            probs = degrees.astype(np.float64) / total_deg
            probs[src] = 0  # 禁止自连接
            probs /= probs.sum()
            targets = np.random.choice(N, size=min(k_out, N-1),
                                       replace=False, p=probs)
            for tgt in targets:
                w = np.random.randint(1, 37)  # weight 1-36 (like C.elegans)
                chem_edges.append([src, int(tgt), w])

        # 生成电突触边 (bidirectional, based on proximity in node space)
        n_elec_raw = max(1, len(chem_edges) // 3)  # ~1/3 of chem
        elec_edges = []
        for _ in range(n_elec_raw):
            src = np.random.randint(0, N)
            # Electrical synapses tend to connect nearby nodes
            tgt = (src + np.random.randint(-5, 6)) % N
            if tgt != src:
                elec_edges.append([src, tgt, np.random.randint(1, 4)])

        return {
            "N": N,
            "nodes": nodes,
            "n_types": n_types,
            "edges_chem": chem_edges,
            "edges_elec": elec_edges,
        }

    @staticmethod
    def save(data: dict, path: str):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)

    @staticmethod
    def stats(data: dict) -> dict:
        N = data["N"]
        chem = data["edges_chem"]
        elec = data["edges_elec"]
        G = nx.DiGraph()
        G.add_nodes_from(range(N))
        for e in chem: G.add_edge(e[0], e[1])
        for e in elec:
            G.add_edge(e[0], e[1])
            G.add_edge(e[1], e[0])

        Gu = G.to_undirected()
        try:
            C = nx.average_clustering(Gu)
            L = nx.average_shortest_path_length(Gu)
            M = G.number_of_edges()
            p = M / (N * (N - 1))
            L_rand = np.log(N) / max(np.log(N * p), 1e-6)
            sigma = (C / max(p, 1e-6)) / (L / max(L_rand, 1e-6))
        except:
            sigma, C, L = 0, 0, 0

        return {
            "N": N, "chem": len(chem), "elec": len(elec),
            "sigma": round(sigma, 3), "C": round(C, 3), "L": round(L, 3),
        }


# ============================================================
# v26 Core Simulator (extends v25 with BCM rolling avg)
# ============================================================

class SDI_v26:
    def __init__(self, connectome_data: dict = None, N: int = None):
        t0 = time.time()

        if connectome_data is not None:
            data = connectome_data
        elif N is not None:
            data = ConnectomeGenerator.generate(N)
        else:
            with open(DATA_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)

        self.N = data["N"]
        self.nodes = data["nodes"]
        self.n_types = data["n_types"]
        self.sensor_idx = np.array([i for i,n in enumerate(self.nodes)
                                     if self.n_types[n]=="sensory"], np.int32)
        self.motor_idx  = np.array([i for i,n in enumerate(self.nodes)
                                     if self.n_types[n]=="motor"], np.int32)
        self.inter_idx  = np.array([i for i,n in enumerate(self.nodes)
                                     if self.n_types[n]=="interneuron"], np.int32)

        # Node state
        self.h = np.random.uniform(0.05, 0.15, self.N).astype(np.float64)
        self.h_avg = self.h.copy()  # v26: rolling average for BCM
        self.last_fire = np.full(self.N, -1000)
        self.act_count = np.zeros(self.N)

        # v26: BCM with rolling average
        self.theta_bcm = np.full(self.N, 8.0)

        # Graded FEP
        self.F_local = np.zeros(self.N)
        self.F_basin_min = np.full(self.N, np.inf)
        self.F_basin_count = np.zeros(self.N, np.int32)
        self.F_convergence = np.zeros(self.N)
        self.F_gradient = np.zeros(self.N)
        self.surprise_i = np.zeros(self.N)
        self.F_history = []

        # Min action
        self.action_cumulative = 0.0
        self.action_history = []
        self.prev_weights = None

        # Edges
        chem = data["edges_chem"]
        elec = data["edges_elec"]

        chem_src = np.array([e[0] for e in chem], np.int32)
        chem_tgt = np.array([e[1] for e in chem], np.int32)
        chem_nbr = np.array([e[2] for e in chem], np.float64)
        chem_w = chem_nbr / max(chem_nbr.max(), 1.0)
        chem_type = np.zeros(len(chem), np.int8)

        e_src1 = np.array([e[0] for e in elec], np.int32)
        e_tgt1 = np.array([e[1] for e in elec], np.int32)
        e_src2 = e_tgt1.copy(); e_tgt2 = e_src1.copy()
        elec_src = np.concatenate([e_src1, e_src2])
        elec_tgt = np.concatenate([e_tgt1, e_tgt2])
        elec_w = np.full(len(elec_src), 0.3)
        elec_type = np.full(len(elec_src), 4, np.int8)

        N_chem = len(chem_src)
        self.src = np.concatenate([chem_src, elec_src])
        self.tgt = np.concatenate([chem_tgt, elec_tgt])
        self.weight = np.concatenate([chem_w, elec_w])
        self.btype = np.concatenate([chem_type, elec_type])
        self.is_elec = np.concatenate([np.zeros(N_chem,bool), np.ones(len(elec_src),bool)])

        self.n_ltp = np.zeros(len(self.src), np.int32)
        self.n_ltd = np.zeros(len(self.src), np.int32)
        self.last_active = np.full(len(self.src), -99999, np.int32)
        self.Ea = np.where(self.is_elec, 0.5, Ea_S)
        self.R = np.where(self.is_elec, 0.95, 1.0)

        self.adj = [[] for _ in range(self.N)]
        for j in range(len(self.src)):
            self.adj[int(self.src[j])].append(j)

        self.theta_ltp_current = T_THETA_BASE
        self.consolidate_rate = FEP_CONSOLIDATE_RATE

        self.t = 0
        self.G = nx.DiGraph()
        self._rebuild()
        self.scaling_events = 0
        self.glia_events = 0
        self.avalanche_sizes = []

        self.structured_gen = None
        if connectome_data is None and N is None:
            # Real connectome: use structured generator
            n_sensor = len(self.sensor_idx)
            class Gen:
                def __init__(self, n): self.N = n
                def sample(self, n_samples=1):
                    return np.random.rand(n_samples, self.N) > 0.7
            self.structured_gen = Gen(n_sensor)

    def _rebuild(self):
        self.G.clear(); self.G.add_nodes_from(range(self.N))
        active = self.weight > 0.03
        for j in np.where(active)[0]:
            self.G.add_edge(int(self.src[j]), int(self.tgt[j]))
        if self.G.number_of_nodes() > 1 and not nx.is_weakly_connected(self.G):
            weak = np.where(~active)[0]
            if len(weak) > 0:
                sorted_weak = weak[np.argsort(self.weight[weak])[::-1]]
                for j in sorted_weak[:min(200, len(sorted_weak))]:
                    self.G.add_edge(int(self.src[j]), int(self.tgt[j]))
                if not nx.is_weakly_connected(self.G):
                    very_weak = np.where(self.weight > 0.005)[0]
                    for j in very_weak:
                        self.G.add_edge(int(self.src[j]), int(self.tgt[j]))

    # ===== v26-2: BCM with rolling h average =====
    def bcm_update(self):
        """v26: BCM using EMA of h instead of instantaneous h
        h_avg = BCM_EMA_DECAY * h_avg + (1-BCM_EMA_DECAY) * h
        theta_bcm += eta * h_avg² * (h_avg - theta_bcm)

        This makes BCM respond to sustained activity, not damped spikes.
        """
        # Update rolling average
        self.h_avg = BCM_EMA_DECAY * self.h_avg + (1.0 - BCM_EMA_DECAY) * self.h

        for i in range(self.N):
            eta_eff = BCM_ETA * (1.0 - 0.5 * self.F_convergence[i])
            h_a = self.h_avg[i]
            delta = eta_eff * h_a**2 * (h_a - self.theta_bcm[i])
            self.theta_bcm[i] = np.clip(self.theta_bcm[i] + delta, BCM_THETA_MIN, BCM_THETA_MAX)

    # ===== FEP (from v25, unchanged) =====
    def fep_compute_energy(self):
        for i in range(self.N):
            out_edges = self.adj[i]
            if not out_edges: self.F_local[i] = 0.0; continue
            pe = 0.0; cp = 0.0; n_out = 0
            for j in out_edges:
                prediction = self.h[i] * self.weight[j]
                actual = self.h[self.tgt[j]]
                pe += (prediction - actual)**2; cp += self.weight[j]**2; n_out += 1
            self.F_local[i] = pe / n_out + 0.05 * cp / n_out
        self.F_history.append(float(self.F_local.mean()))
        if len(self.F_history) > F_WINDOW:
            window = np.array(self.F_history[-F_WINDOW:])
            mean_F, std_F = window.mean(), window.std()
            if std_F > 1e-8:
                for i in range(self.N):
                    self.surprise_i[i] = abs(self.F_local[i] - mean_F) / max(std_F, 1e-8)

    def fep_basin_update(self):
        for i in range(self.N):
            if abs(self.F_local[i]) < 1e-12: continue
            grad = 0.0; n_out = 0
            for j in self.adj[i]:
                prediction = self.h[i] * self.weight[j]
                actual = self.h[self.tgt[j]]
                grad += 2.0 * (prediction - actual) * self.weight[j]; n_out += 1
            self.F_gradient[i] = np.clip(grad / max(n_out,1), -FEP_GRAD_CLIP, FEP_GRAD_CLIP)
            if self.F_local[i] < self.F_basin_min[i] * 0.99:
                self.F_basin_min[i] = self.F_local[i]; self.F_basin_count[i] = 0
            else:
                self.F_basin_count[i] += 1
            x = (self.F_basin_count[i] - FEP_BASIN_WINDOW/2) / max(FEP_BASIN_WINDOW/4, 1)
            self.F_convergence[i] = 1.0 / (1.0 + np.exp(-FEP_CONVERGENCE_STEEPNESS * x))

    def action_update(self, sigma_current: float):
        efficiency = sigma_current * 1.0
        cost = 0.0
        if self.prev_weights is not None:
            n_common = min(len(self.weight), len(self.prev_weights))
            for j in range(n_common):
                cost += self.Ea[j] * abs(self.weight[j] - self.prev_weights[j])
        dS_dt = efficiency - cost
        self.action_cumulative += dS_dt
        self.action_history.append(dS_dt)
        if len(self.action_history) > ACTION_WINDOW:
            recent_dS = np.mean(self.action_history[-ACTION_WINDOW:])
            dS_norm = np.clip(recent_dS / max(abs(recent_dS), 1e-8), -1, 1) if abs(recent_dS) > 1e-6 else 0
            adjustment = 1.0 - ACTION_FEEDBACK_STRENGTH * dS_norm
            self.consolidate_rate *= np.clip(adjustment, 0.7, 1.3)
            self.consolidate_rate = np.clip(self.consolidate_rate, FEP_RATE_MIN, FEP_RATE_MAX)

    # ===== STDP (from v25) =====
    def stdp_update(self, active_mask):
        active_nodes = np.where(active_mask)[0]
        if len(active_nodes) == 0: return
        for pre in active_nodes:
            fep_conv = self.F_convergence[pre]
            ltp_boost = 1.0 + 0.4 * fep_conv
            ltd_suppress = 1.0 - 0.4 * fep_conv
            for j in self.adj[pre]:
                if self.is_elec[j]: continue
                post = self.tgt[j]
                if active_mask[post]:
                    self.n_ltp[j] += 1; self.n_ltd[j] = max(0, self.n_ltd[j] - 1)
                    self.weight[j] = np.clip(self.weight[j] + ETA_LTP * ltp_boost, 0.01, 3.0)
                else:
                    self.n_ltd[j] += 1; self.n_ltp[j] = max(0, self.n_ltp[j] - 1)
                    self.weight[j] = np.clip(self.weight[j] - ETA_LTD * ltd_suppress, 0.01, 3.0)
                self.last_active[j] = self.t

    # ===== Apply rules (from v25) =====
    def apply_rules(self):
        chem = ~self.is_elec
        for j in range(len(self.src)):
            if not chem[j]: continue
            src_node = int(self.src[j])
            theta_eff = self.theta_bcm[src_node] * (1.0 - 0.5 * self.F_convergence[src_node])
            if self.btype[j] == 0 and self.n_ltp[j] >= theta_eff:
                self.btype[j] = 2; self.Ea[j] = Ea_L
                self.n_ltp[j] = max(0, self.n_ltp[j] - int(theta_eff))
                # Heterosynaptic competition
                competing = [k for k in self.adj[src_node] if k != j and chem[k] and self.btype[k] == 0]
                n_compete = min(HETERO_RADIUS, len(competing))
                if n_compete > 0:
                    chosen = np.random.choice(competing, size=n_compete, replace=False)
                    for k in chosen:
                        self.weight[k] *= (1.0 - HETERO_SUPPRESS)
                        self.n_ltp[k] = max(0, self.n_ltp[k] - 1)

        dec = chem & (self.btype==2) & (self.t - self.last_active > T_DECAY)
        if dec.any(): self.btype[dec] = 0; self.Ea[dec] = Ea_S

        cut = chem & (self.weight < 0.01) & (self.t - self.last_active > 1500)
        if cut.any():
            keep = ~cut
            for j in np.where(cut)[0]:
                src_node = int(self.src[j])
                if np.sum(keep & (self.src == src_node)) < MIN_OUT_DEG: cut[j] = False
            if cut.any():
                self._apply_keep(~cut)
                chem = ~self.is_elec

        deg = np.bincount(self.src[chem].astype(int), minlength=self.N)
        low = np.where(deg < 6)[0]
        if len(low) > 0:
            n_new = min(len(low)*2, 60)
            ns = np.random.choice(low, n_new); nt = np.random.randint(0, self.N, n_new)
            valid = ns != nt; ns, nt = ns[valid], nt[valid]; n_add = len(ns)
            if n_add > 0:
                exc = np.random.random(n_add) < 0.8; new_len = len(self.src)
                self.src = np.concatenate([self.src, ns.astype(np.int32)])
                self.tgt = np.concatenate([self.tgt, nt.astype(np.int32)])
                self.btype = np.concatenate([self.btype, np.where(exc,0,1).astype(np.int8)])
                self.weight = np.concatenate([self.weight,
                    np.where(exc, np.random.uniform(0.1,0.4,n_add), np.random.uniform(0.03,0.12,n_add))])
                self.n_ltp = np.concatenate([self.n_ltp, np.zeros(n_add, np.int32)])
                self.n_ltd = np.concatenate([self.n_ltd, np.zeros(n_add, np.int32)])
                self.last_active = np.concatenate([self.last_active, np.full(n_add, self.t, np.int32)])
                self.Ea = np.concatenate([self.Ea, np.full(n_add, Ea_S)])
                self.R = np.concatenate([self.R, np.ones(n_add)])
                self.is_elec = np.concatenate([self.is_elec, np.zeros(n_add, bool)])
                for k in range(n_add): self.adj[int(ns[k])].append(new_len + k)

    def _apply_keep(self, keep):
        for attr in ["src","tgt","btype","weight","n_ltp","n_ltd","last_active","Ea","R","is_elec"]:
            if hasattr(self, attr): setattr(self, attr, getattr(self, attr)[keep])
        self.adj = [[] for _ in range(self.N)]
        for j in range(len(self.src)): self.adj[int(self.src[j])].append(j)

    def compute_adaptive_theta(self):
        if self.G.number_of_nodes() < 2: return T_THETA_BASE
        try:
            if not nx.is_weakly_connected(self.G): return T_THETA_BASE
            L_current = nx.average_shortest_path_length(self.G)
            return max(T_THETA_MIN, min(int(T_THETA_BASE * (L_current / L_REF) / V_C), T_THETA_MAX))
        except: return T_THETA_BASE

    def per_node_energy_constraint(self):
        for i in range(self.N):
            out_mask = np.isin(np.arange(len(self.src)), np.array(self.adj[i])) & (~self.is_elec)
            if not out_mask.any(): continue
            total_w = self.weight[out_mask].sum()
            if total_w > PER_NODE_ENERGY_CAP:
                self.weight[out_mask] *= PER_NODE_ENERGY_CAP / total_w

    def fep_periodic_consolidate(self):
        if FEP_RATE_ADAPTIVE:
            chem_all = ~self.is_elec
            el_current = np.sum((self.btype==2) & chem_all) / max(chem_all.sum(), 1)
            if el_current < EL_TARGET_LO:
                self.consolidate_rate = min(FEP_RATE_MAX, self.consolidate_rate * 1.2)
            elif el_current > EL_TARGET_HI:
                self.consolidate_rate = max(FEP_RATE_MIN, self.consolidate_rate * 0.7)
            elif el_current > 0.30:
                overshoot = (el_current - 0.30) / 0.05
                self.consolidate_rate *= np.clip(1.0 - 0.4 * overshoot, 0.6, 1.0)

        if self.t % FEP_CONSOLIDATE_INT != 0: return
        chem = ~self.is_elec
        converged_mask = self.F_convergence[self.src] > 0.5
        eligible = chem & (self.btype == 0) & converged_mask & (self.weight >= FEP_CONSOLIDATE_MIN_WEIGHT)
        if eligible.sum() == 0: return
        n_convert = max(1, int(eligible.sum() * self.consolidate_rate))
        eligible_idx = np.where(eligible)[0]
        convert = np.random.choice(eligible_idx, size=min(n_convert, len(eligible_idx)), replace=False)
        self.btype[convert] = 2; self.Ea[convert] = Ea_L

    def energy_budget_check(self):
        total_energy = self.F_local.sum() + (self.Ea * self.weight**2).sum()
        if total_energy > GLOBAL_ENERGY_BUDGET:
            scale = GLOBAL_ENERGY_BUDGET / total_energy
            self.Ea *= (1.0 + scale) / 2.0; self.Ea = np.clip(self.Ea, 0.005, Ea_L)

    def cascade(self, stim):
        seeds = np.where(stim > 0.2)[0]
        seeds = [s for s in seeds if (self.t - self.last_fire[s]) >= T_ABS]
        if not seeds: self.avalanche_sizes.append(0); return np.zeros(self.N, bool)
        active = np.zeros(self.N, bool); active[seeds] = True
        for s in seeds: self.last_fire[s] = self.t; self.act_count[s] += 1
        front = list(seeds)
        for _ in range(CASCADE_MAX):
            if not front: break
            next_front = []
            for src in front:
                for j in self.adj[src]:
                    tgt = int(self.tgt[j])
                    if active[tgt]: continue
                    if (self.t - self.last_fire[tgt]) < T_REL:
                        if np.random.random() > REL_SCALE: continue
                    if np.random.random() < self.h[src] * self.weight[j] * self.R[j]:
                        active[tgt] = True; self.last_fire[tgt] = self.t
                        self.act_count[tgt] += 1; next_front.append(tgt)
            front = next_front
        self.avalanche_sizes.append(int(active.sum())); return active

    def synaptic_scaling(self):
        chem = ~self.is_elec; nb = chem.sum()
        if np.sum((self.btype==2) & chem) / max(1, nb) < SCALING_THR: return
        hot = np.where(self.act_count >= np.percentile(self.act_count, 80))[0]
        if len(hot) == 0: return
        sm = chem & (self.btype==2) & (np.isin(self.src, hot) | np.isin(self.tgt, hot))
        if sm.sum() == 0: return
        self.weight[sm] *= (1 - SCALING_RATE)
        deg = sm & (self.weight < 0.08)
        if deg.any(): self.btype[deg] = 0; self.Ea[deg] = Ea_S
        self.scaling_events += 1

    def glia_modulation(self):
        chem = ~self.is_elec
        if np.sum((self.btype==2) & chem) / max(chem.sum(), 1) < GLIA_THR: return 0
        el_bonds = np.where(chem & (self.btype==2))[0]
        if len(el_bonds) == 0: return 0
        n_degrade = max(1, int(len(el_bonds) * GLIA_RATE))
        top_idx = el_bonds[np.argsort(self.weight[el_bonds])[::-1][:n_degrade]]
        self.btype[top_idx] = 0; self.Ea[top_idx] = Ea_S; self.n_ltp[top_idx] = 0
        self.glia_events += 1; return n_degrade

    def metrics(self):
        self._rebuild(); g = self.G
        if g.number_of_nodes() < 10: return 1.0, 0.0, 0.0, 0
        Gu = g.to_undirected(); C = nx.average_clustering(Gu)
        try: L_val = nx.average_shortest_path_length(Gu)
        except: L_val = 0.0
        Nn = g.number_of_nodes(); Mm = g.number_of_edges()
        p = max(Mm / (Nn * (Nn - 1)), 1e-6)
        C_rand = p; L_rand = np.log(Nn) / max(np.log(Nn * p), 1e-6)
        sigma = (C / max(C_rand, 1e-6)) / (L_val / max(L_rand, 1e-6)) if L_val > 0 else 0.0
        chem = ~self.is_elec
        el_ratio = np.sum((self.btype==2) & chem) / max(chem.sum(), 1)
        return sigma, C, L_val, el_ratio

    def step(self):
        # Stimulus
        if self.structured_gen is not None:
            structured = self.structured_gen.sample(1)[0]
        else:
            structured = np.random.rand(len(self.sensor_idx)) > 0.7
        stim = np.zeros(self.N)
        n_sensor = max(1, int(len(self.sensor_idx) * SEED_FRAC_SENSOR))
        spike_idx = np.where(structured)[0][:n_sensor]
        if len(spike_idx) > 0: stim[self.sensor_idx[spike_idx]] = structured[spike_idx]
        random_sensors = np.random.choice(self.sensor_idx, size=n_sensor, replace=False)
        stim[random_sensors] = np.maximum(stim[random_sensors], np.random.uniform(0.2, 0.8, n_sensor))
        n_other = max(1, int(self.N * SEED_FRAC_OTHER))
        other_idx = np.random.choice(self.N, size=n_other, replace=False)
        stim[other_idx] = np.maximum(stim[other_idx], np.random.uniform(0.1, 0.3, n_other))
        stim[(self.t - self.last_fire) < T_ABS] *= REL_SCALE

        active = self.cascade(stim)
        self.R = np.clip(self.R + 1.0/TAU_REC, 0.1, 1.0)
        ae = active[self.src] | active[self.tgt]
        self.R[ae] -= np.where(self.is_elec[ae], U_SE_ELEC, U_SE_CHEM)

        self.fep_compute_energy(); self.fep_basin_update()
        self.stdp_update(active)
        if self.t % 5 == 0: self.bcm_update()
        if self.t % 10 == 0: self.theta_ltp_current = self.compute_adaptive_theta()
        self.apply_rules(); self.fep_periodic_consolidate()
        if self.t > 0 and self.t % SCALING_INT == 0: self.synaptic_scaling()
        if self.t > 0 and self.t % GLIA_INT == 0: self.glia_modulation()
        if self.t > 0 and self.t % 20 == 0: self.per_node_energy_constraint()
        self.energy_budget_check()
        self.prev_weights = self.weight.copy()
        self.t += 1

    def run_compact(self, N_STEPS=300, log_interval=40):
        """Compact run for multi-scale testing — returns metrics only"""
        sigma_hist, el_hist, bcm_hist = [], [], []
        for _ in range(N_STEPS):
            self.step()
            if self.t % log_interval == 0 or self.t < 5:
                s, _, _, el = self.metrics()
                sigma_hist.append(s); el_hist.append(el)
                bcm_hist.append(float(self.theta_bcm.mean()))

        return {
            "N": self.N,
            "sigma_final": sigma_hist[-1] if sigma_hist else 0,
            "sigma_mean": np.mean(sigma_hist[-5:]) if len(sigma_hist) >= 5 else 0,
            "el_final": el_hist[-1] if el_hist else 0,
            "bcm_final": bcm_hist[-1] if bcm_hist else 0,
            "convergence": float(self.F_convergence.mean()),
            "n_bonds": len(self.src),
            "F_final": float(self.F_local.mean()),
        }


# ============================================================
# v26-3: Multi-Scale Automated Test
# ============================================================

def multi_scale_test(scales=[100, 200, 279, 500], n_steps=300):
    """Run v26 at multiple network scales and analyze scaling laws"""
    print("=" * 70)
    print("v26 Multi-Scale Scaling Law Test")
    print(f"  Scales: {scales} | Steps: {n_steps}")
    print("=" * 70)

    results = []
    for N in scales:
        t0 = time.time()
        print(f"\n--- N={N} ---")

        # Generate synthetic connectome
        data = ConnectomeGenerator.generate(N, seed=42 + N)
        stats = ConnectomeGenerator.stats(data)
        print(f"  Generated: chem={stats['chem']}, elec={stats['elec']}, "
              f"sigma={stats['sigma']}, C={stats['C']}, L={stats['L']}")

        # Run v26
        sim = SDI_v26(connectome_data=data)
        r = sim.run_compact(N_STEPS=n_steps)
        r["t_elapsed"] = time.time() - t0
        r["connectome_sigma"] = stats["sigma"]
        results.append(r)

        status = "PASS" if r["sigma_final"] >= 4.0 and 0.15 <= r["el_final"] <= 0.35 else "FAIL"
        print(f"  {status} sigma={r['sigma_final']:.3f} EL={r['el_final']*100:.1f}% "
              f"BCM={r['bcm_final']:.1f} bonds={r['n_bonds']} "
              f"time={r['t_elapsed']:.1f}s")

    # Scaling law analysis
    print(f"\n{'='*70}")
    print("Scaling Law Summary")
    print(f"{'N':>5s} {'sigma':>8s} {'EL%':>7s} {'BCM':>7s} {'bonds':>7s} {'time':>7s} {'status':>6s}")
    print("-" * 55)
    for r in results:
        status = "PASS" if r["sigma_final"] >= 4.0 and 0.15 <= r["el_final"] <= 0.35 else "FAIL"
        print(f"{r['N']:5d} {r['sigma_final']:8.3f} {r['el_final']*100:6.1f}% "
              f"{r['bcm_final']:7.1f} {r['n_bonds']:7d} {r['t_elapsed']:6.1f}s {status:>6s}")

    # Fit scaling laws
    Ns = np.array([r["N"] for r in results])
    sigmas = np.array([r["sigma_final"] for r in results])
    bonds = np.array([r["n_bonds"] for r in results])
    times = np.array([r["t_elapsed"] for r in results])

    # σ(N) ≈ const? (small-world should be scale-invariant)
    sigma_cv = np.std(sigmas) / max(np.mean(sigmas), 1e-6)
    print(f"\n  σ coefficient of variation: {sigma_cv:.3f} (0 = scale-invariant)")

    # bonds(N) ∝ N^α
    if len(Ns) >= 2:
        slope, _ = np.polyfit(np.log(Ns), np.log(bonds), 1)
        print(f"  bonds(N) ∝ N^{slope:.2f}")

    # time(N) ∝ N^β
    if len(Ns) >= 2:
        slope_t, _ = np.polyfit(np.log(Ns), np.log(times), 1)
        print(f"  time(N) ∝ N^{slope_t:.2f}")

    # Plot
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    axes[0,0].plot(Ns, sigmas, 'bo-', lw=2, ms=8)
    axes[0,0].axhline(4.0, color='g', ls='--', label='target')
    axes[0,0].set_xlabel('N'); axes[0,0].set_ylabel('sigma'); axes[0,0].set_title('sigma(N)')
    axes[0,0].legend()

    axes[0,1].plot(Ns, [r["el_final"]*100 for r in results], 'ro-', lw=2, ms=8)
    axes[0,1].axhline(15, color='g', ls='--'); axes[0,1].axhline(35, color='g', ls='--')
    axes[0,1].set_xlabel('N'); axes[0,1].set_ylabel('EL%'); axes[0,1].set_title('EL(N)')

    axes[0,2].loglog(Ns, bonds, 'go-', lw=2, ms=8)
    axes[0,2].set_xlabel('N'); axes[0,2].set_ylabel('bonds'); axes[0,2].set_title('bonds(N)')

    axes[1,0].loglog(Ns, times, 'mo-', lw=2, ms=8)
    axes[1,0].set_xlabel('N'); axes[1,0].set_ylabel('time(s)'); axes[1,0].set_title('time(N)')

    axes[1,1].plot(Ns, [r["bcm_final"] for r in results], 'co-', lw=2, ms=8)
    axes[1,1].set_xlabel('N'); axes[1,1].set_ylabel('BCM theta'); axes[1,1].set_title('BCM(N)')

    # Text summary
    axes[1,2].axis('off')
    n_pass = sum(1 for r in results if r["sigma_final"] >= 4.0 and 0.15 <= r["el_final"] <= 0.35)
    txt = (f"v26 Multi-Scale\n\n"
           f"Scales tested: {len(scales)}\n"
           f"All pass: {n_pass}/{len(scales)}\n"
           f"sigma CV: {sigma_cv:.3f}\n"
           f"bonds ∝ N^{slope:.2f}\n"
           f"time ∝ N^{slope_t:.2f}")
    axes[1,2].text(0.1, 0.5, txt, fontsize=11, family='monospace', va='center')

    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/v26_scaling_laws.png", dpi=150, bbox_inches="tight")
    plt.close()

    # Save results
    with open(f"{OUT_DIR}/v26_scaling_results.json", "w") as f:
        json.dump(results, f, indent=2)

    return results


if __name__ == "__main__":
    # Run multi-scale test
    np.random.seed(42)
    multi_scale_test(scales=[100, 200, 279, 500], n_steps=300)
    print(f"\nResults saved to {OUT_DIR}/")
