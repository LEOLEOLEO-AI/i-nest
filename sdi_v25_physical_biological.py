"""SDI v25 — Physical First Principles + Biological Mechanism Grounding
=====================================================================
v24.5 → v25 六项优化，每项对应明确的物理/生物原理：

1. BCM滑动阈值 (替换LTP/LTD硬比值≥3.0)
   物理: 稳态可塑性 — Bienenstock-Cooper-Munro (1982)
   生物: θ_m随突触后活动滑动, 防止LTP饱和/LTD抑郁
   实现: θ_bcm[i] += η*(h[i]² - θ_bcm[i]*h[i])

2. 分级FEP收敛 (替换二值yes/no)
   物理: 自由能盆地深度 → 收敛程度 = sigmoid(盆地停留/窗口)
   生物: 预测可靠性是连续谱, 非二元开关

3. 最小作用量反馈 (新机制)
   物理: dS/dt = σ×v_prop - ΣEa×|Δw|, dS/dt<0 → 效率提升→加固化
   生物: 代谢效率驱动突触稳态

4. 异突触竞争 (新机制)
   物理: 资源有限→胜者多占
   生物: 异突触可塑性(heterosynaptic LTD): 一个突触增强→邻近减弱

5. 每节点能量约束 (替换仅全局预算)
   物理: 单神经元轴突输送有物理上限
   生物: 代谢瓶颈, 突触缩放

6. 保留v24已验证机制：周期FEP固化 + 连通约束 + 动态σ + 自适应θ
=====================================================================
"""

import numpy as np, networkx as nx, matplotlib, matplotlib.pyplot as plt
from collections import defaultdict
import json, os, warnings, time
warnings.filterwarnings("ignore")
matplotlib.rcParams["font.family"] = "DejaVu Sans"
np.random.seed(42)

DATA_PATH = "D:/Obsidian/phase1_workspace/connectome_v8_data.json"
OUT_DIR   = "D:/Obsidian/phase1_workspace/v25_results"
os.makedirs(OUT_DIR, exist_ok=True)

# ============ v8 baseline (unchanged) ============
TAU_STDP, ETA_LTP, ETA_LTD = 20.0, 0.020, 0.016
Ea_S, Ea_L = 0.15, 0.85
T_DECAY = 25000
TAU_REC, U_SE_CHEM, U_SE_ELEC = 150, 0.45, 0.10
T_ABS = 3; T_REL = 8; REL_SCALE = 0.3
SCALING_THR, SCALING_RATE, SCALING_INT = 0.35, 0.12, 15
GLIA_THR, GLIA_RATE, GLIA_INT = 0.45, 0.25, 50
SEED_FRAC_SENSOR, SEED_FRAC_OTHER = 0.20, 0.03
N_STEPS = 500; CASCADE_MAX = 15
EL_TARGET_LO, EL_TARGET_HI = 0.15, 0.35

# ============ v22 parameters (unchanged) ============
T_THETA_BASE = 15
L_REF = 2.44
V_C = 1.0
T_THETA_MIN = 5
T_THETA_MAX = 100
FEP_TARGET_OUT_W = 0.8
FEP_HOMEOSTASIS_INT = 20
F_WINDOW = 50

# ============ v25: Physical + Biological Grounding ============
# --- BCM sliding threshold (replaces LTP/LTD ratio) ---
BCM_ETA = 0.05           # BCM threshold sliding rate
BCM_THETA_MIN = 3.0       # Minimum BCM threshold
BCM_THETA_MAX = 30.0      # Maximum BCM threshold

# --- Graded FEP convergence (sigmoid, not binary) ---
FEP_BASIN_WINDOW = 20
FEP_CONVERGENCE_STEEPNESS = 0.5  # Sigmoid steepness

# --- Minimum action feedback ---
ACTION_WINDOW = 100        # dS/dt sliding window
ACTION_FEEDBACK_STRENGTH = 0.15  # How much dS/dt affects consolidation rate

# --- Heterosynaptic competition ---
HETERO_SUPPRESS = 0.01    # 1% weight suppression on competing edges
HETERO_RADIUS = 5         # Number of competing edges affected

# --- Per-node energy constraint ---
PER_NODE_ENERGY_CAP = 1.5  # Max total outgoing weight per node
GLOBAL_ENERGY_BUDGET = 500.0

# --- FEP periodic consolidation (v24 proven, kept) ---
FEP_CONSOLIDATE_INT = 25
FEP_CONSOLIDATE_RATE = 0.08
FEP_RATE_ADAPTIVE = True
FEP_RATE_MIN = 0.02
FEP_RATE_MAX = 0.20
FEP_CONSOLIDATE_MIN_WEIGHT = 0.05

# --- Connectivity ---
MIN_OUT_DEG = 3

# --- FEP gradient ---
FEP_GRAD_CLIP = 0.5


# ============ Structured input (unchanged) ============
class StructuredSpikeGen:
    def __init__(self, N_inputs, N_patterns=10):
        self.N = N_inputs
        self.patterns = np.random.rand(N_patterns, N_inputs) > 0.7
    def sample(self, n_samples=1):
        idx = np.random.choice(len(self.patterns), n_samples)
        return self.patterns[idx].astype(np.float64)


# ============ SDI v25 Core ============
class SDI_v25:
    def __init__(self):
        t0 = time.time()
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
        self.last_fire = np.full(self.N, -1000)
        self.act_count = np.zeros(self.N)

        # v25: BCM sliding threshold per node
        self.theta_bcm = np.full(self.N, 8.0)  # BCM threshold per node
        self.bcm_eta = np.full(self.N, BCM_ETA)

        # v25: Graded FEP convergence
        self.F_local = np.zeros(self.N)
        self.F_basin_min = np.full(self.N, np.inf)
        self.F_basin_count = np.zeros(self.N, np.int32)
        self.F_convergence = np.zeros(self.N)  # v25: graded [0,1], not binary
        self.F_gradient = np.zeros(self.N)
        self.surprise_i = np.zeros(self.N)
        self.F_history = []

        # v25: Minimum action tracking
        self.action_cumulative = 0.0
        self.action_history = []
        self.efficiency_history = []
        self.cost_history = []
        self.prev_weights = None  # for delta-w computation

        # Edges: merge chem + elec
        chem = data["edges_chem"]
        chem_src = np.array([e[0] for e in chem], np.int32)
        chem_tgt = np.array([e[1] for e in chem], np.int32)
        chem_nbr = np.array([e[2] for e in chem], np.float64)
        chem_w = chem_nbr / max(chem_nbr.max(), 1.0)
        chem_type = np.zeros(len(chem), np.int8)

        elec = data["edges_elec"]
        e_src1 = np.array([e[0] for e in elec], np.int32)
        e_tgt1 = np.array([e[1] for e in elec], np.int32)
        e_src2 = e_tgt1.copy(); e_tgt2 = e_src1.copy()
        elec_src = np.concatenate([e_src1, e_src2])
        elec_tgt = np.concatenate([e_tgt1, e_tgt2])
        elec_w = np.full(len(elec_src), 0.3)
        elec_type = np.full(len(elec_src), 4, np.int8)

        N_chem, N_elec = len(chem_src), len(elec_src)
        self.src = np.concatenate([chem_src, elec_src])
        self.tgt = np.concatenate([chem_tgt, elec_tgt])
        self.weight = np.concatenate([chem_w, elec_w])
        self.btype = np.concatenate([chem_type, elec_type])
        self.is_elec = np.concatenate([np.zeros(N_chem,bool), np.ones(N_elec,bool)])

        # Edge state
        self.n_ltp = np.zeros(len(self.src), np.int32)
        self.n_ltd = np.zeros(len(self.src), np.int32)
        self.last_active = np.full(len(self.src), -99999, np.int32)
        self.Ea = np.where(self.is_elec, 0.5, Ea_S)
        self.R = np.where(self.is_elec, 0.95, 1.0)

        # Adjacency list
        self.adj = [[] for _ in range(self.N)]
        for j in range(len(self.src)):
            self.adj[int(self.src[j])].append(j)

        # Adaptive theta
        self.theta_ltp_current = T_THETA_BASE

        # Consolidation
        self.consolidate_rate = FEP_CONSOLIDATE_RATE

        # Metrics
        self.t = 0
        self.G = nx.DiGraph()
        self._rebuild()
        self.scaling_events = 0
        self.glia_events = 0
        self.avalanche_sizes = []

        self.structured_gen = StructuredSpikeGen(len(self.sensor_idx), N_patterns=10)

        print(f"v25 init: N={self.N} chem={len(chem)} elec={len(elec)} "
              f"(time {time.time()-t0:.1f}s)")
        print(f"  BCM sliding theta + Graded FEP + Min Action + Heterosynaptic + Per-Node Energy")

    def _rebuild(self):
        self.G.clear()
        self.G.add_nodes_from(range(self.N))
        w_thresh = 0.03
        active = self.weight > w_thresh
        for j in np.where(active)[0]:
            self.G.add_edge(int(self.src[j]), int(self.tgt[j]))
        if self.G.number_of_nodes() > 1 and not nx.is_weakly_connected(self.G):
            # v25.1: aggressive connectivity recovery — add back strongest weak edges
            weak = np.where(~active)[0]
            if len(weak) > 0:
                sorted_weak = weak[np.argsort(self.weight[weak])[::-1]]
                for j in sorted_weak[:min(200, len(sorted_weak))]:
                    self.G.add_edge(int(self.src[j]), int(self.tgt[j]))
                # If still disconnected, lower threshold further
                if not nx.is_weakly_connected(self.G):
                    very_weak = np.where(self.weight > 0.005)[0]
                    for j in very_weak:
                        self.G.add_edge(int(self.src[j]), int(self.tgt[j]))

    # ===== v25-1: BCM sliding threshold =====
    def bcm_update(self):
        """BCM rule: theta_bcm slides with post-synaptic activity squared
        theta_bcm[i] += eta * (h[i]^2 * (h[i] - theta_bcm[i]))
        FEP convergence slows the sliding rate
        
        Physical grounding: Bienenstock-Cooper-Munro (1982) theory of visual cortex plasticity
        Biological grounding: LTP/LTD threshold depends on history of post-synaptic activity
        """
        for i in range(self.N):
            # FEP convergence slows BCM adaptation (stable neurons have stable thresholds)
            eta_eff = self.bcm_eta[i] * (1.0 - 0.7 * self.F_convergence[i])
            # BCM update
            delta = eta_eff * self.h[i]**2 * (self.h[i] - self.theta_bcm[i])
            self.theta_bcm[i] = np.clip(self.theta_bcm[i] + delta, BCM_THETA_MIN, BCM_THETA_MAX)

    # ===== v25-2: Graded FEP convergence =====
    def fep_compute_energy(self):
        for i in range(self.N):
            out_edges = self.adj[i]
            if not out_edges:
                self.F_local[i] = 0.0; continue
            pe = 0.0; cp = 0.0; n_out = 0
            for j in out_edges:
                prediction = self.h[i] * self.weight[j]
                actual = self.h[self.tgt[j]]
                pe += (prediction - actual)**2
                cp += self.weight[j]**2
                n_out += 1
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
            # Gradient
            grad = 0.0; n_out = 0
            for j in self.adj[i]:
                prediction = self.h[i] * self.weight[j]
                actual = self.h[self.tgt[j]]
                grad += 2.0 * (prediction - actual) * self.weight[j]
                n_out += 1
            self.F_gradient[i] = np.clip(grad / max(n_out,1), -FEP_GRAD_CLIP, FEP_GRAD_CLIP)

            # v25: Graded convergence (sigmoid), not binary
            if self.F_local[i] < self.F_basin_min[i] * 0.99:
                self.F_basin_min[i] = self.F_local[i]
                self.F_basin_count[i] = 0
            else:
                self.F_basin_count[i] += 1
            # Sigmoid: convergence_degree ∈ [0, 1]
            x = (self.F_basin_count[i] - FEP_BASIN_WINDOW/2) / max(FEP_BASIN_WINDOW/4, 1)
            self.F_convergence[i] = 1.0 / (1.0 + np.exp(-FEP_CONVERGENCE_STEEPNESS * x))

    # ===== v25-3: Minimum action feedback =====
    def action_update(self, sigma_current: float):
        """Compute action S and dS/dt for feedback into consolidation rate
        S = integral [ sigma(t)*v_prop - sum(Ea_j * |dw_j|) ] dt
        dS/dt < 0: system becoming more efficient, reward consolidation
        dS/dt > 0: system cost exceeds benefit, slow consolidation
        
        Physical grounding: Principle of Least Action (Lagrangian mechanics)
        Biological grounding: Metabolic efficiency drives synaptic homeostasis
        """
        efficiency = sigma_current * 1.0  # v_prop = 1

        # Cost: sum of Ea * |delta_weight|
        cost = 0.0
        if self.prev_weights is not None:
            n_common = min(len(self.weight), len(self.prev_weights))
            for j in range(n_common):
                dw = abs(self.weight[j] - self.prev_weights[j])
                cost += self.Ea[j] * dw
        # Snapshot taken at end of step (handled in step())

        dS_dt = efficiency - cost
        self.action_cumulative += dS_dt
        self.action_history.append(dS_dt)
        self.efficiency_history.append(efficiency)
        self.cost_history.append(cost)

        # v25: dS/dt feedback into consolidation rate
        if len(self.action_history) > ACTION_WINDOW:
            recent_dS = np.mean(self.action_history[-ACTION_WINDOW:])
            # Normalize to [-1, 1] range for feedback
            dS_norm = np.clip(recent_dS / max(abs(recent_dS), 1e-8), -1, 1) if abs(recent_dS) > 1e-6 else 0
            # dS/dt < 0 (efficient) → increase rate; dS/dt > 0 (costly) → decrease
            adjustment = 1.0 - ACTION_FEEDBACK_STRENGTH * dS_norm
            adjustment = np.clip(adjustment, 0.7, 1.3)
            self.consolidate_rate *= adjustment
            self.consolidate_rate = np.clip(self.consolidate_rate, FEP_RATE_MIN, FEP_RATE_MAX)

    # ===== STDP with BCM threshold (v25) =====
    def stdp_update(self, active_mask):
        active_nodes = np.where(active_mask)[0]
        if len(active_nodes) == 0: return

        for pre in active_nodes:
            # FEP convergence modulates STDP rates (from v24, kept)
            fep_conv = self.F_convergence[pre]
            ltp_boost = 1.0 + 0.4 * fep_conv   # 1.0 → 1.4
            ltd_suppress = 1.0 - 0.4 * fep_conv # 1.0 → 0.6

            for j in self.adj[pre]:
                if self.is_elec[j]: continue
                post = self.tgt[j]
                if active_mask[post]:
                    self.n_ltp[j] += 1
                    self.n_ltd[j] = max(0, self.n_ltd[j] - 1)  # decay
                    dw = ETA_LTP * ltp_boost
                    self.weight[j] = np.clip(self.weight[j] + dw, 0.01, 3.0)
                else:
                    self.n_ltd[j] += 1
                    self.n_ltp[j] = max(0, self.n_ltp[j] - 1)  # decay
                    dw = -ETA_LTD * ltd_suppress
                    self.weight[j] = np.clip(self.weight[j] + dw, 0.01, 3.0)
                self.last_active[j] = self.t

    # ===== v25: BCM-based consolidation (replaces LTP/LTD ratio) =====
    def apply_rules(self):
        chem = ~self.is_elec

        # v25: BCM sliding threshold per source node determines consolidation
        # Each edge consolidates when n_ltp exceeds BCM threshold of source node
        for j in range(len(self.src)):
            if not chem[j]: continue
            src_node = int(self.src[j])
            theta_eff = self.theta_bcm[src_node]
            # FEP convergence modulates: converged → lower effective threshold
            theta_eff *= (1.0 - 0.5 * self.F_convergence[src_node])

            if self.btype[j] == 0 and self.n_ltp[j] >= theta_eff:
                self.btype[j] = 2  # E-S → E-L
                self.Ea[j] = Ea_L
                self.n_ltp[j] = max(0, self.n_ltp[j] - int(theta_eff))

                # v25-4: Heterosynaptic competition
                # When one edge consolidates, slightly suppress competing edges from same source
                competing = [k for k in self.adj[src_node]
                           if k != j and chem[k] and self.btype[k] == 0]
                n_compete = min(HETERO_RADIUS, len(competing))
                if n_compete > 0:
                    chosen = np.random.choice(competing, size=n_compete, replace=False)
                    for k in chosen:
                        self.weight[k] *= (1.0 - HETERO_SUPPRESS)
                        self.n_ltp[k] = max(0, self.n_ltp[k] - 1)

        # E-L → E-S (decay): long time inactive
        dec = chem & (self.btype==2) & (self.t - self.last_active > T_DECAY)
        if dec.any():
            self.btype[dec] = 0
            self.Ea[dec] = Ea_S

        # Connectivity-preserving pruning
        cut = chem & (self.weight < 0.01) & (self.t - self.last_active > 1500)
        if cut.any():
            keep = ~cut
            for j in np.where(cut)[0]:
                src_node = int(self.src[j])
                remaining_out = np.sum(keep & (self.src == src_node))
                if remaining_out < MIN_OUT_DEG:
                    cut[j] = False
            if cut.any():
                keep = ~cut
                self._apply_keep(keep)
                chem = ~self.is_elec

        # New E-S bonds
        deg = np.bincount(self.src[chem].astype(int), minlength=self.N)
        low = np.where(deg < 6)[0]
        if len(low) > 0:
            n_new = min(len(low)*2, 60)
            ns = np.random.choice(low, n_new)
            nt = np.random.randint(0, self.N, n_new)
            valid = ns != nt
            ns, nt = ns[valid], nt[valid]
            n_add = len(ns)
            if n_add > 0:
                exc = np.random.random(n_add) < 0.8
                new_len = len(self.src)
                self.src = np.concatenate([self.src, ns.astype(np.int32)])
                self.tgt = np.concatenate([self.tgt, nt.astype(np.int32)])
                self.btype = np.concatenate([self.btype, np.where(exc,0,1).astype(np.int8)])
                self.weight = np.concatenate([self.weight,
                    np.where(exc, np.random.uniform(0.1,0.4,n_add),
                             np.random.uniform(0.03,0.12,n_add))])
                self.n_ltp = np.concatenate([self.n_ltp, np.zeros(n_add, np.int32)])
                self.n_ltd = np.concatenate([self.n_ltd, np.zeros(n_add, np.int32)])
                self.last_active = np.concatenate([self.last_active,
                                                   np.full(n_add, self.t, np.int32)])
                self.Ea = np.concatenate([self.Ea, np.full(n_add, Ea_S)])
                self.R = np.concatenate([self.R, np.ones(n_add)])
                self.is_elec = np.concatenate([self.is_elec, np.zeros(n_add, bool)])
                for k in range(n_add):
                    self.adj[int(ns[k])].append(new_len + k)

    def _apply_keep(self, keep):
        for attr in ["src","tgt","btype","weight","n_ltp","n_ltd",
                     "last_active","Ea","R","is_elec"]:
            if hasattr(self, attr):
                arr = getattr(self, attr)
                setattr(self, attr, arr[keep])
        self.adj = [[] for _ in range(self.N)]
        for j in range(len(self.src)):
            self.adj[int(self.src[j])].append(j)

    # ===== Adaptive theta =====
    def compute_adaptive_theta(self):
        if self.G.number_of_nodes() < 2: return T_THETA_BASE
        try:
            if not nx.is_weakly_connected(self.G): return T_THETA_BASE
            L_current = nx.average_shortest_path_length(self.G)
            T_theta = int(T_THETA_BASE * (L_current / L_REF) / V_C)
            return max(T_THETA_MIN, min(T_theta, T_THETA_MAX))
        except: return T_THETA_BASE

    # ===== v25-5: Per-node energy constraint ===== 
    def per_node_energy_constraint(self):
        for i in range(self.N):
            out_mask = np.isin(np.arange(len(self.src)),
                               np.array(self.adj[i])) & (~self.is_elec)
            if not out_mask.any(): continue
            total_w = self.weight[out_mask].sum()
            if total_w > PER_NODE_ENERGY_CAP:
                scale = PER_NODE_ENERGY_CAP / total_w
                self.weight[out_mask] *= scale

    # ===== v25-6: FEP periodic consolidation (kept from v24) =====
    def fep_periodic_consolidate(self):
        # v25: adaptive rate based on EL deviation
        if FEP_RATE_ADAPTIVE:
            chem_all = ~self.is_elec
            el_current = np.sum((self.btype==2) & chem_all) / max(chem_all.sum(), 1)
            if el_current < EL_TARGET_LO:
                self.consolidate_rate = min(FEP_RATE_MAX, self.consolidate_rate * 1.2)
            elif el_current > EL_TARGET_HI:
                self.consolidate_rate = max(FEP_RATE_MIN, self.consolidate_rate * 0.7)
            elif el_current > 0.30:  # v25.1: soft cap as EL approaches 35%
                overshoot = (el_current - 0.30) / 0.05  # 0 at 30%, 1 at 35%
                factor = 1.0 - 0.4 * overshoot  # reduce rate by up to 40%
                self.consolidate_rate *= np.clip(factor, 0.6, 1.0)

        if self.t % FEP_CONSOLIDATE_INT != 0: return

        chem = ~self.is_elec
        # v25: use graded convergence, not binary
        converged_mask = self.F_convergence[self.src] > 0.5
        eligible = chem & (self.btype == 0) & converged_mask & (self.weight >= FEP_CONSOLIDATE_MIN_WEIGHT)
        n_eligible = eligible.sum()
        if n_eligible == 0: return

        n_convert = max(1, int(n_eligible * self.consolidate_rate))
        eligible_idx = np.where(eligible)[0]
        convert = np.random.choice(eligible_idx, size=min(n_convert, len(eligible_idx)), replace=False)
        self.btype[convert] = 2
        self.Ea[convert] = Ea_L
        return n_convert

    # ===== Global energy budget =====
    def energy_budget_check(self):
        total_energy = self.F_local.sum() + (self.Ea * self.weight**2).sum()
        if total_energy > GLOBAL_ENERGY_BUDGET:
            scale = GLOBAL_ENERGY_BUDGET / total_energy
            self.Ea *= (1.0 + scale) / 2.0
            self.Ea = np.clip(self.Ea, 0.005, Ea_L)

    # ===== Cascade =====
    def cascade(self, stim):
        seeds = np.where(stim > 0.2)[0]
        seeds = [s for s in seeds if (self.t - self.last_fire[s]) >= T_ABS]
        if not seeds:
            self.avalanche_sizes.append(0)
            return np.zeros(self.N, bool)
        active = np.zeros(self.N, bool)
        active[seeds] = True
        for s in seeds:
            self.last_fire[s] = self.t
            self.act_count[s] += 1

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
                    effective = self.h[src] * self.weight[j] * self.R[j]
                    if np.random.random() < effective:
                        active[tgt] = True
                        self.last_fire[tgt] = self.t
                        self.act_count[tgt] += 1
                        next_front.append(tgt)
            front = next_front
        self.avalanche_sizes.append(int(active.sum()))
        return active

    # ===== Synaptic scaling =====
    def synaptic_scaling(self):
        chem = ~self.is_elec
        nb = chem.sum()
        el_r = np.sum((self.btype==2) & chem) / max(1, nb)
        if el_r < SCALING_THR: return
        thr = np.percentile(self.act_count, 80)
        hot = np.where(self.act_count >= thr)[0]
        if len(hot) == 0: return
        sm = chem & (self.btype==2) & (np.isin(self.src, hot) | np.isin(self.tgt, hot))
        if sm.sum() == 0: return
        self.weight[sm] *= (1 - SCALING_RATE)
        deg = sm & (self.weight < 0.08)
        if deg.any():
            self.btype[deg] = 0
            self.Ea[deg] = Ea_S
        self.scaling_events += 1

    # ===== Glia modulation =====
    def glia_modulation(self):
        chem = ~self.is_elec
        nb = chem.sum()
        el_r = np.sum((self.btype==2) & chem) / max(1, nb)
        if el_r < GLIA_THR: return 0
        el_bonds = np.where(chem & (self.btype==2))[0]
        if len(el_bonds) == 0: return 0
        n_degrade = max(1, int(len(el_bonds) * GLIA_RATE))
        top_idx = el_bonds[np.argsort(self.weight[el_bonds])[::-1][:n_degrade]]
        self.btype[top_idx] = 0
        self.Ea[top_idx] = Ea_S
        self.n_ltp[top_idx] = 0
        self.glia_events += 1
        return n_degrade

    # ===== Dynamic sigma =====
    def metrics(self):
        self._rebuild()
        g = self.G
        if g.number_of_nodes() < 10: return 1.0, 0.0, 0.0, 0

        G_u = g.to_undirected()
        C = nx.average_clustering(G_u)
        try:
            L_val = nx.average_shortest_path_length(G_u)
        except nx.NetworkXError:
            L_val = 0.0

        N = g.number_of_nodes()
        M = g.number_of_edges()
        p = max(M / (N * (N - 1)), 1e-6)
        C_rand = p
        L_rand = np.log(N) / max(np.log(N * p), 1e-6)
        sigma = (C / max(C_rand, 1e-6)) / (L_val / max(L_rand, 1e-6)) if L_val > 0 else 0.0

        chem = ~self.is_elec
        el_ratio = np.sum((self.btype==2) & chem) / max(chem.sum(), 1)
        return sigma, C, L_val, el_ratio

    def compute_alpha(self):
        sizes = np.array(self.avalanche_sizes[-200:]) if len(self.avalanche_sizes) > 0 else np.array([0])
        sizes = sizes[sizes > 0]
        if len(sizes) < 10: return 99.0
        hist, bins = np.histogram(sizes, bins=min(20, len(set(sizes))))
        nonzero = hist > 0
        if np.sum(nonzero) < 3: return 99.0
        slope, _ = np.polyfit(np.log(bins[1:][nonzero]), np.log(hist[nonzero]), 1)
        return float(-slope)

    # ===== v25 Step =====
    def step(self):
        structured_spikes = self.structured_gen.sample(1)[0]
        stim = np.zeros(self.N)
        n_sensor = max(1, int(len(self.sensor_idx) * SEED_FRAC_SENSOR))
        spike_indices = np.where(structured_spikes > 0.3)[0]
        if len(spike_indices) > 0:
            driven = self.sensor_idx[spike_indices[:n_sensor]]
            stim[driven] = structured_spikes[spike_indices[:n_sensor]]
        random_sensors = np.random.choice(self.sensor_idx, size=n_sensor, replace=False)
        stim[random_sensors] = np.maximum(stim[random_sensors],
                                          np.random.uniform(0.2, 0.8, n_sensor))
        n_other = max(1, int(self.N * SEED_FRAC_OTHER))
        other_idx = np.random.choice(self.N, size=n_other, replace=False)
        stim[other_idx] = np.maximum(stim[other_idx], np.random.uniform(0.1, 0.3, n_other))
        refractory = (self.t - self.last_fire) < T_ABS
        stim[refractory] *= REL_SCALE

        active = self.cascade(stim)
        self.R = np.clip(self.R + 1.0/TAU_REC, 0.1, 1.0)
        active_edges = active[self.src] | active[self.tgt]
        self.R[active_edges] -= np.where(self.is_elec[active_edges], U_SE_ELEC, U_SE_CHEM)

        # v25: FEP energy (before plasticity)
        self.fep_compute_energy()
        self.fep_basin_update()

        # v25: STDP with BCM threshold
        self.stdp_update(active)

        # v25: BCM threshold slide
        if self.t % 5 == 0:
            self.bcm_update()

        # Adaptive theta
        if self.t % 10 == 0:
            self.theta_ltp_current = self.compute_adaptive_theta()

        # v25: BCM-based consolidation (replaces ratio check)
        self.apply_rules()

        # v25: FEP periodic consolidation
        self.fep_periodic_consolidate()

        # Periodic maintenance
        if self.t > 0 and self.t % SCALING_INT == 0:
            self.synaptic_scaling()
        if self.t > 0 and self.t % GLIA_INT == 0:
            self.glia_modulation()

        # v25: Per-node energy constraint
        if self.t > 0 and self.t % 20 == 0:
            self.per_node_energy_constraint()

        self.energy_budget_check()
        # v25: snapshot for next action computation
        self.prev_weights = self.weight.copy()
        self.t += 1

    # ===== v25 Run =====
    def run(self):
        print(f"\nv25 Physical+Biological Grounded: {N_STEPS} steps")
        print(f"  BCM sliding theta | Graded FEP convergence | Min action feedback")
        print(f"  Heterosynaptic competition | Per-node energy constraint")
        print("-"*72)

        sigma_history, el_history, f_history = [], [], []
        conv_history, bonds_history, action_history = [], [], []
        bcm_history = []

        for step_i in range(N_STEPS):
            self.step()

            if self.t % 20 == 0 or self.t < 5:
                sigma, C, L_val, el_ratio = self.metrics()
                F_mean = self.F_local.mean()
                conv_mean = self.F_convergence.mean()
                n_bonds = len(self.src)
                bcm_mean = self.theta_bcm.mean()

                # v25: action feedback
                self.action_update(sigma)

                sigma_history.append((self.t, sigma))
                el_history.append((self.t, el_ratio))
                f_history.append((self.t, F_mean))
                conv_history.append((self.t, conv_mean))
                bonds_history.append((self.t, n_bonds))
                action_history.append((self.t, self.action_cumulative))
                bcm_history.append((self.t, bcm_mean))

                dS_recent = np.mean(self.action_history[-10:]) if len(self.action_history) >= 10 else 0  # simplified
                print(f"  t={self.t:4d} theta={self.theta_ltp_current:2d} "
                      f"sigma={sigma:.3f} L={L_val:.3f} "
                      f"EL={el_ratio*100:5.1f}% F={F_mean:.4f} "
                      f"cv={conv_mean:.2f} bcm={bcm_mean:.1f} "
                      f"rate={self.consolidate_rate:.3f} bonds={n_bonds}")

        return sigma_history, el_history, f_history, conv_history, bonds_history, action_history, bcm_history

    def save_and_plot(self, sigma_hist, el_hist, f_hist, conv_hist, bonds_hist, action_hist, bcm_hist):
        fig, axes = plt.subplots(2, 4, figsize=(20, 10))
        ts = [x[0] for x in sigma_hist]

        ax = axes[0,0]; ax.plot(ts, [x[1] for x in sigma_hist], 'b-', lw=2)
        ax.axhline(4.0, color='g', ls='--', label='target=4.0'); ax.set_ylabel('sigma'); ax.legend(); ax.set_title('Small-World')

        ax = axes[0,1]; ax.plot(ts, [x[1]*100 for x in el_hist], 'r-', lw=2)
        ax.axhline(15, color='g', ls='--'); ax.axhline(35, color='g', ls='--')
        ax.set_ylabel('E-L %'); ax.set_title('Consolidation')

        ax = axes[0,2]; ax.plot(ts, [x[1] for x in f_hist], 'm-', lw=2)
        ax.set_ylabel('F'); ax.set_title('Free Energy')

        ax = axes[0,3]; ax.plot(ts, [x[1] for x in conv_hist], 'c-', lw=2)
        ax.set_ylabel('FEP convergence'); ax.set_title('Graded Convergence')

        ax = axes[1,0]; ax.plot(ts, [x[1] for x in bonds_hist], 'orange', lw=2)
        ax.set_ylabel('bonds'); ax.set_title('Active Bonds')

        ax = axes[1,1]; ax.plot(ts, [x[1] for x in bcm_hist], 'purple', lw=2)
        ax.set_ylabel('theta_bcm mean'); ax.set_title('BCM Threshold')

        ax = axes[1,2]; ax.plot(ts, [x[1] for x in action_hist], 'brown', lw=2)
        ax.set_ylabel('cumulative action'); ax.set_title('Min Action S(t)')

        # Text summary
        ax = axes[1,3]; ax.axis('off')
        final_s = sigma_hist[-1][1] if sigma_hist else 0
        final_el = el_hist[-1][1]*100 if el_hist else 0
        final_f = f_hist[-1][1] if f_hist else 0
        final_cv = conv_hist[-1][1] if conv_hist else 0
        final_bcm = bcm_hist[-1][1] if bcm_hist else 0
        txt = (f"v25 Physical+Biological\n\n"
               f"sigma = {final_s:.3f}\n"
               f"E-L   = {final_el:.1f}%\n"
               f"F     = {final_f:.4f}\n"
               f"FEPcv = {final_cv:.2f}\n"
               f"BCM   = {final_bcm:.1f}\n"
               f"Target: sigma>=4, EL 15-35%")
        ax.text(0.1, 0.5, txt, fontsize=10, family='monospace', va='center')

        plt.tight_layout()
        plt.savefig(f"{OUT_DIR}/sdi_v25_main.png", dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  Plot saved -> {OUT_DIR}/sdi_v25_main.png")

        results = {
            "version": "v25",
            "N": self.N,
            "sigma_final": final_s,
            "el_final_pct": final_el,
            "F_final": final_f,
            "FEP_convergence": final_cv,
            "BCM_theta_mean": final_bcm,
            "consolidate_rate_final": self.consolidate_rate,
            "glia_events": self.glia_events,
            "scaling_events": self.scaling_events,
        }
        with open(f"{OUT_DIR}/v25_results.json", "w") as f:
            json.dump(results, f, indent=2)
        print(f"  Results saved -> {OUT_DIR}/v25_results.json")


if __name__ == "__main__":
    sim = SDI_v25()
    s, e, f, c, b, a, bcm = sim.run()
    sim.save_and_plot(s, e, f, c, b, a, bcm)
    print("\nv25 complete.")
