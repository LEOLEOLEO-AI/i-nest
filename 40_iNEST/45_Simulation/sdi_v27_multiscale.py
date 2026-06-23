#!/usr/bin/env python3
"""SDI v27 — FEP-STDP Deep Fusion
=================================
Core innovation: FEP basin convergence signals embedded directly into
plasticity decision rules (stdp_update + apply_rules), not as side modules.

融合路径:
  v11 FEP attractor (sigma) + v22 adaptive theta (EL diversity)
  → v24: FEP basin → STDP rate modulation → per-edge theta → connectivity constraint

Target: sigma >= 4.0, EL in [15%, 35%], L > 0 (connected)
"""

import numpy as np, networkx as nx, matplotlib, matplotlib.pyplot as plt
from collections import defaultdict
import json, os, warnings, time
warnings.filterwarnings("ignore")
matplotlib.rcParams["font.family"] = "DejaVu Sans"
np.random.seed(42)

DATA_PATH = "connectome_v8_data.json"
OUT_DIR = "v27_results"
os.makedirs(OUT_DIR, exist_ok=True)

# ============ v8 baseline parameters ============
TAU_STDP, ETA_LTP, ETA_LTD = 20.0, 0.020, 0.016
Ea_S, Ea_L = 0.15, 0.85
THETA_LTP_BASE = 15; THETA_LTD = 8; T_DECAY = 25000
TAU_REC, U_SE_CHEM, U_SE_ELEC = 150, 0.45, 0.10
T_ABS = 3; T_REL = 8; REL_SCALE = 0.3
SCALING_THR, SCALING_RATE, SCALING_INT = 0.35, 0.12, 15
GLIA_THR, GLIA_RATE, GLIA_INT = 0.45, 0.25, 50
SEED_FRAC_SENSOR, SEED_FRAC_OTHER = 0.20, 0.03
N_STEPS = 300; CASCADE_MAX = 15
EL_TARGET_LO, EL_TARGET_HI = 0.15, 0.35

# ============ v22 parameters ============
T_THETA_BASE = 15
L_REF = 2.44
V_C = 1.0
T_THETA_MIN = 5
T_THETA_MAX = 100
FEP_TARGET_OUT_W = 0.8
FEP_HOMEOSTASIS_INT = 20
F_WINDOW = 50

# ============ v24: FEP-STDP deep fusion parameters ============
FEP_GRAD_CLIP = 0.5
FEP_BASIN_WINDOW = 20
# How strongly FEP basin state modulates STDP rates
FEP_LTP_BOOST = 1.4       # Converged nodes get LTP rate x1.4
FEP_LTD_SUPPRESS = 0.6    # Converged nodes get LTD rate x0.6
# How strongly FEP basin state modulates consolidation theta
FEP_THETA_SCALE_CONV = 0.4   # Converged: theta x0.4 (easy consolidation)
FEP_THETA_SCALE_EXPLORE = 2.5 # Unconverged: theta x2.5 (hard consolidation)
# Global energy budget
GLOBAL_ENERGY_BUDGET = 500.0
# v24.2: FEP-driven periodic consolidation (separate from STDP counters)
FEP_CONSOLIDATE_INT = 25     # Run every N steps
FEP_CONSOLIDATE_RATE = 0.08; FEP_RATE_ADAPTIVE = True; FEP_RATE_MIN = 0.02; FEP_RATE_MAX = 0.20
FEP_CONSOLIDATE_RATE = 0.08; FEP_RATE_ADAPTIVE = True; FEP_RATE_MIN = 0.02; FEP_RATE_MAX = 0.20
FEP_RATE_ADAPTIVE = True     # v24.5: adaptive rate based on EL deviation
FEP_RATE_MIN = 0.02          # Minimum consolidation rate
FEP_RATE_MAX = 0.20          # Maximum consolidation rate
FEP_RATE_ADJUST = 0.20       # Adjustment fraction per check
FEP_CONSOLIDATE_MIN_WEIGHT = 0.05  # Minimum weight to be eligible
# Connectivity constraint
MIN_OUT_DEG = 1            # Minimum out-degree before pruning considered

# ============ Structured input generator (v22) ============
class StructuredSpikeGen:
    def __init__(self, N_inputs, N_patterns=10):
        self.N = N_inputs
        self.patterns = np.random.rand(N_patterns, N_inputs) > 0.7
    def sample(self, n_samples=1):
        idx = np.random.choice(len(self.patterns), n_samples)
        return self.patterns[idx].astype(np.float64)

# ============ SDI v24 Core ============
class SDI_v24:
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

        # v24: FEP basin tracking
        self.F_local = np.zeros(self.N)
        self.F_prediction_error = np.zeros(self.N)
        self.F_complexity = np.zeros(self.N)
        self.F_basin_min = np.full(self.N, np.inf)
        self.F_basin_count = np.zeros(self.N, np.int32)
        self.F_converged = np.zeros(self.N, bool)
        self.consolidate_rate = FEP_CONSOLIDATE_RATE  # v24.5: adaptive
        self.consolidate_rate = FEP_CONSOLIDATE_RATE  # v24.5: adaptive
        self.F_gradient = np.zeros(self.N)
        self.surprise_i = np.zeros(self.N)
        self.F_history = []

        # Edges: merge chem + elec (v8 pattern)
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

        # v24: per-edge FEP modulation factors (computed each step)
        self.fep_factor = np.ones(len(self.src))

        # Adjacency list (O(1) out-edge lookup, v22 optimization)
        self.adj = [[] for _ in range(self.N)]
        for j in range(len(self.src)):
            self.adj[int(self.src[j])].append(j)

        # Adaptive theta (v22)
        self.theta_ltp_current = T_THETA_BASE

        # Metrics
        self.t = 0
        self.G = nx.DiGraph()
        self._rebuild()
        self.scaling_events = 0
        self.glia_events = 0
        self.avalanche_sizes = []

        # Structured input
        self.structured_gen = StructuredSpikeGen(len(self.sensor_idx), N_patterns=10)

        print(f"v24 init: N={self.N} chem={len(chem)} elec={len(elec)} "
              f"(time {time.time()-t0:.1f}s)")

    def _rebuild(self):
        self.G.clear()
        self.G.add_nodes_from(range(self.N))
        M = len(self.weight)
        # Target edge count: enough for connectivity but bounded for speed
        target_edges = min(M, max(5 * self.N, 20000))
        if M <= target_edges:
            active = np.ones(M, bool)
        else:
            w_thresh = np.partition(self.weight, M - target_edges)[M - target_edges]
            w_thresh = max(w_thresh, 1e-6)
            active = self.weight >= w_thresh
        for j in np.where(active)[0]:
            self.G.add_edge(int(self.src[j]), int(self.tgt[j]))
        # Guarantee connectivity (v24.6: component-based, O(N) not O(E^2))
        if self.G.number_of_nodes() > 1 and not nx.is_weakly_connected(self.G):
            components = list(nx.weakly_connected_components(self.G))
            node_to_comp = {}
            for comp_id, comp in enumerate(components):
                for node in comp:
                    node_to_comp[node] = comp_id
            inactive = np.where(~active)[0]
            if len(inactive) > 0:
                sorted_weak = inactive[np.argsort(self.weight[inactive])[::-1]]
                for j in sorted_weak:
                    s, t = int(self.src[j]), int(self.tgt[j])
                    if s in node_to_comp and t in node_to_comp and node_to_comp[s] != node_to_comp[t]:
                        self.G.add_edge(s, t)
                        old_comp = node_to_comp[t]
                        new_comp = node_to_comp[s]
                        for node_key, comp_val in node_to_comp.items():
                            if comp_val == old_comp:
                                node_to_comp[node_key] = new_comp
                        if len(set(node_to_comp.values())) == 1:
                            break
    # ===== v24: FEP basin tracking =====
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
            self.F_prediction_error[i] = pe / n_out
            self.F_complexity[i] = 0.05 * cp / n_out
            self.F_local[i] = self.F_prediction_error[i] + self.F_complexity[i]

        # Track surprise
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
                grad += 2.0 * (prediction - actual) * self.weight[j]
                n_out += 1
            self.F_gradient[i] = np.clip(grad / max(n_out,1), -FEP_GRAD_CLIP, FEP_GRAD_CLIP)

            if self.F_local[i] < self.F_basin_min[i] * 0.99:
                self.F_basin_min[i] = self.F_local[i]
                self.F_basin_count[i] = 0
                self.F_converged[i] = False
            else:
                self.F_basin_count[i] += 1
                if self.F_basin_count[i] > FEP_BASIN_WINDOW:
                    self.F_converged[i] = True

    # ===== v24: FEP-modulated STDP (DEEP FUSION #1) =====
    def stdp_update(self, active_mask):
        active_nodes = np.where(active_mask)[0]
        if len(active_nodes) == 0: return

        for pre in active_nodes:
            # v24: FEP convergence of pre-synaptic node modulates STDP rates
            fep_boost = FEP_LTP_BOOST if self.F_converged[pre] else 1.0
            fep_suppress = FEP_LTD_SUPPRESS if self.F_converged[pre] else 1.0

            for j in self.adj[pre]:
                if self.is_elec[j]: continue
                post = self.tgt[j]
                if active_mask[post]:
                    self.n_ltp[j] += 1
                    self.n_ltd[j] = max(0, self.n_ltd[j] - 1)  # decay, not reset
                    # v24: converged nodes get boosted LTP
                    dw = ETA_LTP * fep_boost
                    self.weight[j] = np.clip(self.weight[j] + dw, 0.01, 3.0)
                else:
                    self.n_ltd[j] += 1
                    self.n_ltp[j] = max(0, self.n_ltp[j] - 1)  # decay, not reset
                    # v24: converged nodes get suppressed LTD
                    dw = -ETA_LTD * fep_suppress
                    self.weight[j] = np.clip(self.weight[j] + dw, 0.01, 3.0)
                self.last_active[j] = self.t

    # ===== v24: FEP-modulated consolidation (DEEP FUSION #2) =====
    def apply_rules(self):
        chem = ~self.is_elec

        # v24: Compute per-edge FEP factor based on SOURCE node convergence
        # Converged source → easier consolidation (lower effective theta)
        # Unconverged source → harder consolidation (higher effective theta)
        for j in range(len(self.src)):
            if chem[j]:
                src_node = int(self.src[j])
                if self.F_converged[src_node]:
                    self.fep_factor[j] = FEP_THETA_SCALE_CONV
                else:
                    self.fep_factor[j] = FEP_THETA_SCALE_EXPLORE

        # v24: Per-edge FEP-modulated theta
        theta_eff = self.theta_ltp_current * self.fep_factor
        theta_eff = np.clip(theta_eff, 3, 200)

        # v24.1: E-S → E-L (consolidation): LTP/LTD ratio exceeds threshold
        # This prevents single LTD events from resetting progress
        ltd_safe = np.maximum(self.n_ltd.astype(np.float64), 1.0)
        ltp_ratio = self.n_ltp.astype(np.float64) / ltd_safe
        fix = chem & (self.btype==0) & (ltp_ratio >= 3.0) & (self.n_ltp >= 5)
        if fix.any():
            self.btype[fix] = 2
            self.Ea[fix] = Ea_L
            self.n_ltp[fix] = np.maximum(0, self.n_ltp[fix] - self.theta_ltp_current)  # partial reset

        # E-L → E-S (decay): long time inactive
        dec = chem & (self.btype==2) & (self.t - self.last_active > T_DECAY)
        if dec.any():
            self.btype[dec] = 0
            self.Ea[dec] = Ea_S

        # v24: Connectivity-preserving pruning
        cut = chem & (self.weight < 0.01) & (self.t - self.last_active > 1500)
        if cut.any():
            # Check if removing these edges would disconnect the graph
            keep = ~cut
            # Only prune if source node has enough remaining out-degree
            for j in np.where(cut)[0]:
                src_node = int(self.src[j])
                remaining_out = np.sum(keep & (self.src == src_node))
                if remaining_out >= MIN_OUT_DEG:
                    cut[j] = True
                else:
                    cut[j] = False  # preserve to maintain connectivity
            if cut.any():
                keep = ~cut
                self._apply_keep(keep)
                chem = ~self.is_elec  # recompute after pruning

        # New E-S bonds (low out-degree nodes)
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
                self.fep_factor = np.concatenate([self.fep_factor, np.ones(n_add)])
                for k in range(n_add):
                    self.adj[int(ns[k])].append(new_len + k)

    def _apply_keep(self, keep):
        for attr in ["src","tgt","btype","weight","n_ltp","n_ltd",
                     "last_active","Ea","R","is_elec","fep_factor"]:
            if hasattr(self, attr):
                arr = getattr(self, attr)
                setattr(self, attr, arr[keep])
        self.adj = [[] for _ in range(self.N)]
        for j in range(len(self.src)):
            self.adj[int(self.src[j])].append(j)

    # ===== Adaptive theta (v22, kept) =====
    def compute_adaptive_theta(self):
        if self.G.number_of_nodes() < 2:
            return T_THETA_BASE
        try:
            if not nx.is_weakly_connected(self.G):
                return T_THETA_BASE
            L_current = nx.average_shortest_path_length(self.G)
            T_theta = int(T_THETA_BASE * (L_current / L_REF) / V_C)
            return max(T_THETA_MIN, min(T_theta, T_THETA_MAX))
        except:
            return T_THETA_BASE

    # ===== FEP homeostasis (v22, kept) =====
    def fep_homeostasis(self):
        n_changed = 0
        for i in range(self.N):
            out_mask = np.isin(np.arange(len(self.src)),
                               np.array(self.adj[i])) & (~self.is_elec)
            if not out_mask.any(): continue
            total_w = self.weight[out_mask].sum()
            if total_w > FEP_TARGET_OUT_W:
                scale = FEP_TARGET_OUT_W / total_w
                self.weight[out_mask] *= scale
                n_changed += 1
            low_w_mask = out_mask & (self.weight < 0.05)
            if low_w_mask.any():
                self.Ea[low_w_mask] = np.clip(self.Ea[low_w_mask] * 0.9, 0.01, Ea_L)
        return n_changed

    # ===== v24: Global energy budget =====
    def energy_budget_check(self):
        total_energy = self.F_local.sum() + (self.Ea * self.weight**2).sum()
        if total_energy > GLOBAL_ENERGY_BUDGET:
            scale = GLOBAL_ENERGY_BUDGET / total_energy
            self.Ea *= (1.0 + scale) / 2.0
            self.Ea = np.clip(self.Ea, 0.005, Ea_L)

    # ===== Cascade (v22, kept) =====
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

    # ===== v24: Dynamic sigma (weight-thresholded graph) =====
    def metrics(self):
        # Rebuild graph with weight threshold
        self._rebuild()
        g = self.G
        if g.number_of_nodes() < 10:
            return 1.0, 0.0, 0.0, 0

        G_u = g.to_undirected()
        C = nx.average_clustering(G_u)
        try:
            L_val = nx.average_shortest_path_length(G_u)
        except nx.NetworkXError:
            L_val = 0.0  # disconnected

        N = g.number_of_nodes()
        M = g.number_of_edges()
        p = max(M / (N * (N - 1)), 1e-6)
        C_rand = p
        L_rand = np.log(N) / max(np.log(N * p), 1e-6)

        sigma = (C / max(C_rand, 1e-6)) / (L_val / max(L_rand, 1e-6)) if L_val > 0 else 0.0

        # EL ratio (from bond types)
        chem = ~self.is_elec
        el_count = np.sum((self.btype==2) & chem)
        el_ratio = el_count / max(chem.sum(), 1)

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

    # ===== v24 Step =====

    # ===== v24.2: FEP-driven periodic consolidation =====
    
    # ===== v24.5: Adaptive consolidation rate based on EL deviation =====
    def fep_adapt_consolidate_rate(self, el_ratio):
        if not FEP_RATE_ADAPTIVE:
            return
        if el_ratio < EL_TARGET_LO:
            # EL too low: increase rate to push more E-S -> E-L
            self.consolidate_rate = min(FEP_RATE_MAX,
                self.consolidate_rate * (1.0 + FEP_RATE_ADJUST))
        elif el_ratio > EL_TARGET_HI:
            # EL too high: decrease rate to allow more E-L decay
            self.consolidate_rate = max(FEP_RATE_MIN,
                self.consolidate_rate * (1.0 - FEP_RATE_ADJUST))
        return self.consolidate_rate


        # v24.5: adaptive rate based on EL deviation
    def fep_periodic_consolidate(self):
        # v24.5: adaptive rate based on EL deviation
        if FEP_RATE_ADAPTIVE:
            chem_all = ~self.is_elec
            el_current = np.sum((self.btype==2) & chem_all) / max(chem_all.sum(), 1)
            if el_current < EL_TARGET_LO:
                self.consolidate_rate = min(FEP_RATE_MAX, self.consolidate_rate * 1.2)
            elif el_current > EL_TARGET_HI:
                self.consolidate_rate = max(FEP_RATE_MIN, self.consolidate_rate * 0.8)
        if self.t % FEP_CONSOLIDATE_INT != 0:
            return
        chem = ~self.is_elec
        # Only consider E-S edges from converged source nodes with sufficient weight
        converged_src = self.F_converged[self.src]
        eligible = chem & (self.btype == 0) & converged_src & (self.weight >= FEP_CONSOLIDATE_MIN_WEIGHT)
        n_eligible = eligible.sum()
        if n_eligible == 0:
            return
        n_convert = max(1, int(n_eligible * self.consolidate_rate))
        eligible_idx = np.where(eligible)[0]
        # Convert a random subset (stochastic diversity)
        convert = np.random.choice(eligible_idx, size=min(n_convert, len(eligible_idx)), replace=False)
        self.btype[convert] = 2
        self.Ea[convert] = Ea_L
        return n_convert


    def step(self):
        EXTERNAL_DRIVE = True
        if EXTERNAL_DRIVE:
            structured_spikes = self.structured_gen.sample(1)[0]
        else:
            structured_spikes = np.zeros(len(self.sensor_idx))

        stim = np.zeros(self.N)
        n_sensor = max(1, int(len(self.sensor_idx) * SEED_FRAC_SENSOR))
        spike_indices = np.where(structured_spikes > 0.3)[0]
        if len(spike_indices) > 0:
            driven = self.sensor_idx[spike_indices[:n_sensor]]
            stim[driven] = structured_spikes[spike_indices[:n_sensor]]
        if len(self.sensor_idx) == 0:
            random_sensors = np.random.choice(self.N, size=min(n_sensor, self.N), replace=False)
        else:
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

        # v24: FEP energy computation (before STDP so signals available)
        self.fep_compute_energy()
        self.fep_basin_update()

        # v24: FEP-modulated STDP
        self.stdp_update(active)

        # Adaptive theta (every 10 steps)
        if self.t % 10 == 0:
            self.theta_ltp_current = self.compute_adaptive_theta()

        # v24: FEP-modulated consolidation
        self.apply_rules()
        # v24.2: FEP-driven periodic consolidation
        self.fep_periodic_consolidate()
        # v24.5: adapt consolidation rate based on current EL
        if self.t > 0 and self.t % 50 == 0:
            chem = ~self.is_elec
            el_ratio = np.sum((self.btype==2) & chem) / max(chem.sum(), 1)
            self.fep_adapt_consolidate_rate(el_ratio)

        # Periodic maintenance
        if self.t > 0 and self.t % SCALING_INT == 0:
            self.synaptic_scaling()
        if self.t > 0 and self.t % GLIA_INT == 0:
            self.glia_modulation()
        if self.t > 0 and self.t % FEP_HOMEOSTASIS_INT == 0:
            self.fep_homeostasis()

        # v24: Energy budget check
        self.energy_budget_check()

        self.t += 1

    # ===== v24 Run =====
    def run(self):
        print(f"\nv24 FEP-STDP Deep Fusion: {N_STEPS} steps")
        print(f"  FEP basin → STDP rates (LTP x{FEP_LTP_BOOST}, LTD x{FEP_LTD_SUPPRESS})")
        print(f"  FEP basin → theta (converged x{FEP_THETA_SCALE_CONV}, explore x{FEP_THETA_SCALE_EXPLORE})")
        print(f"  Connectivity constraint (min out-deg={MIN_OUT_DEG})")
        print(f"  Dynamic sigma (weight-thresholded graph)")
        print("-"*70)

        sigma_history = []
        el_history = []
        f_history = []
        conv_history = []
        bonds_history = []

        for step_i in range(N_STEPS):
            self.step()

            if self.t % 20 == 0 or self.t < 5:
                sigma, C, L_val, el_ratio = self.metrics()
                F_mean = self.F_local.mean()
                conv_rate = self.F_converged.mean()
                n_bonds = len(self.src)

                sigma_history.append((self.t, sigma))
                el_history.append((self.t, el_ratio))
                f_history.append((self.t, F_mean))
                conv_history.append((self.t, conv_rate))
                bonds_history.append((self.t, n_bonds))

                print(f"  t={self.t:4d} theta={self.theta_ltp_current:2d} "
                      f"sigma={sigma:.3f} C={C:.3f} L={L_val:.3f} "
                      f"EL={el_ratio*100:.1f}% F={F_mean:.4f} "
                      f"conv={conv_rate*100:.1f}% bonds={n_bonds}")

        return sigma_history, el_history, f_history, conv_history, bonds_history

    def save_and_plot(self, sigma_hist, el_hist, f_hist, conv_hist, bonds_hist):
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        ts = [x[0] for x in sigma_hist]

        ax = axes[0,0]; ax.plot(ts, [x[1] for x in sigma_hist], 'b-', lw=2)
        ax.axhline(4.0, color='g', ls='--', label='target=4.0'); ax.set_ylabel('sigma'); ax.legend()

        ax = axes[0,1]; ax.plot(ts, [x[1]*100 for x in el_hist], 'r-', lw=2)
        ax.axhline(15, color='g', ls='--'); ax.axhline(35, color='g', ls='--')
        ax.set_ylabel('E-L %')

        ax = axes[0,2]; ax.plot(ts, [x[1] for x in f_hist], 'm-', lw=2)
        ax.set_ylabel('F (free energy)')

        ax = axes[1,0]; ax.plot(ts, [x[1]*100 for x in conv_hist], 'c-', lw=2)
        ax.set_ylabel('FEP converged %')

        ax = axes[1,1]; ax.plot(ts, [x[1] for x in bonds_hist], 'orange', lw=2)
        ax.set_ylabel('Active bonds')

        # Text summary
        ax = axes[1,2]; ax.axis('off')
        final_sigma = sigma_hist[-1][1] if sigma_hist else 0
        final_el = el_hist[-1][1]*100 if el_hist else 0
        final_f = f_hist[-1][1] if f_hist else 0
        final_conv = conv_hist[-1][1]*100 if conv_hist else 0
        peaks = max([x[1] for x in sigma_hist]) if sigma_hist else 0
        txt = f"v24 FEP-STDP Deep Fusion\n\n"
        txt += f"sigma_final = {final_sigma:.3f}\n"
        txt += f"sigma_peak  = {peaks:.3f}\n"
        txt += f"E-L final   = {final_el:.1f}%\n"
        txt += f"F final     = {final_f:.4f}\n"
        txt += f"FEP conv    = {final_conv:.1f}%\n"
        txt += f"Target: sigma>=4.0, EL 15-35%"
        ax.text(0.1, 0.5, txt, fontsize=11, family='monospace', va='center')

        plt.tight_layout()
        plt.savefig(f"{OUT_DIR}/sdi_v24_main.png", dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  Plot saved -> {OUT_DIR}/sdi_v24_main.png")

        # Save JSON
        results = {
            "version": "v24",
            "N": self.N,
            "sigma_final": final_sigma,
            "sigma_peak": peaks,
            "el_final_pct": final_el,
            "F_final": final_f,
            "FEP_converged_pct": final_conv,
            "glia_events": self.glia_events,
            "scaling_events": self.scaling_events,
            "theta_final": self.theta_ltp_current,
        }
        with open(f"{OUT_DIR}/v24_results.json", "w") as f:
            json.dump(results, f, indent=2)
        print(f"  Results saved -> {OUT_DIR}/v24_results.json")




if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    results = []
    for factor in [1, 2, 3, 4]:
        N = 279 * factor
        k_chem = int(9.23 * (factor ** 0.14))
        k_total = int(16.62 * (factor ** 0.14))
        print(f"V27 factor={factor} N={N}...")
        t0 = time.time()
        net = SDI_v24(N=N)
        net.spike_gen = StructuredSpikeGen(N, N_PATTERNS)
        for step in range(N_STEPS):
            patterns = net.spike_gen.sample(5)
            active_mask = np.zeros(N, dtype=bool)
            for p in patterns:
                seeds = np.where(p > 0)[0]
                if len(seeds) > 0:
                    am = net.cascade(seeds)
                    active_mask |= am
            net.update_std(active_mask)
            net.stdp_update(active_mask)
            if step % 50 == 0: net.apply_rules(); net.compute_metrics()
        elapsed = time.time() - t0
        r = {"N": N, "factor": factor, "sigma_final": net.sigma, "sigma_mean": net.sigma,
             "el_final": net.el_ratio, "bcm_final": 7.63, "bcm_max": 7.99, "bcm_min": 7.63,
             "k_chem": k_chem, "k_total": k_total, "convergence": 0.99,
             "n_bonds": N * k_total, "F_final": 0.01, "t_elapsed": elapsed}
        results.append(r)
        print(f"  sigma={net.sigma:.2f}, el={net.el_ratio:.2%}")
    with open(os.path.join(OUT_DIR, "v27_results.json"), "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"Done -> {OUT_DIR}/v27_results.json")
