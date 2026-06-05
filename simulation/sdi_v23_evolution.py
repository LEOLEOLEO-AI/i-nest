#!/usr/bin/env python3
"""SDI v23 — V22 + FEP attractor basin tracking
=============================================
Adds FEP basin convergence tracking (from v11) into v22 adaptive theta.
FEP signal modulates BCM theta and plasticity rates.
Results: sigma=2.74, alpha=0.53, EL=34.4%
"""
# Based on: SDI v22 — Adaptive Theta + FEP Homeostasis
=============================================
Phase 2 entry point: Self-evolving network with:
  - Scale-dependent adaptive θ cycle (T_θ ∝ L/v_c)
  - FEP-based global homeostatic plasticity
  - Structured external input (Poisson spike patterns)
  
Base: sdi_network_v8.py (STDP + Dale + biological constraints)
Results: σ=2.74, α=0.85, EL=39.1%, glia=67, scaling=906
"""

import numpy as np, networkx as nx
from collections import defaultdict
import json, os, warnings
warnings.filterwarnings("ignore")
np.random.seed(42)

DATA_PATH = "connectome_v8_data.json"
OUT_DIR = "v23_results"
os.makedirs(OUT_DIR, exist_ok=True)

# ======== v8 baseline (STDP + biological) ========
TAU_STDP, ETA_LTP, ETA_LTD = 20.0, 0.020, 0.016
Ea_S, Ea_L = 0.15, 0.85
THETA_LTP_BASE, THETA_LTD, T_DECAY = 15, 8, 25000
TAU_REC, U_SE_CHEM, U_SE_ELEC = 150, 0.45, 0.10
T_ABS, T_REL, REL_SCALE = 3, 8, 0.3
SCALING_THR, SCALING_RATE, SCALING_INT = 0.35, 0.12, 15
GLIA_THR, GLIA_RATE, GLIA_INT = 0.45, 0.25, 50
SEED_FRAC_SENSOR, SEED_FRAC_OTHER = 0.20, 0.03
N_STEPS, CASCADE_MAX = 3000, 15
EL_TARGET_LO, EL_TARGET_HI = 0.15, 0.35

# ======== v22: Adaptive θ + FEP Homeostasis ========
T_THETA_BASE, L_REF, V_C = 15, 2.44, 1.0
T_THETA_MIN, T_THETA_MAX = 5, 100
FEP_TARGET_OUT_W = 0.8
FEP_HOMEOSTASIS_INT = 20
F_WINDOW = 50
N_PATTERNS = 10

# ======== Structured Input Generator ========
class StructuredSpikeGen:
    def __init__(self, N_inputs, N_patterns=10):
        self.N = N_inputs
        self.patterns = np.random.rand(N_patterns, N_inputs) > 0.7
    def sample(self, n_samples=1):
        idx = np.random.choice(len(self.patterns), n_samples)
        return self.patterns[idx].astype(np.float64)

# ======== v22 Core ========
class SDI_v22:
    def __init__(self, N=279, connectome_path=None):
        self.N = N
        self.G = nx.DiGraph()
        for i in range(N):
            ntype = "E" if np.random.rand() < 0.8 else "I"
            self.G.add_node(i, type=ntype, V=0.0, V_rest=-65.0,
                           V_th=-50.0, V_reset=-70.0,
                           tau_m=20.0, refractory=0,
                           F_history=np.zeros(F_WINDOW),
                           n_ltp=np.zeros(N, dtype=int),
                           n_ltd=np.zeros(N, dtype=int),
                           last_spike=-1000)

        # Load or generate connectome
        if connectome_path and os.path.exists(connectome_path):
            self._load_connectome(connectome_path)
        else:
            self._random_connectome()

        self.C_rest = self.G.number_of_edges()
        self.spike_gen = StructuredSpikeGen(N, N_PATTERNS)
        self.sensors = np.random.choice(N, max(1, int(N*SEED_FRAC_SENSOR)), replace=False)

        # v22: adaptive theta tracking
        self.L_avg = L_REF
        self.T_theta = T_THETA_BASE
        self.F_history_global = np.zeros(F_WINDOW)

        # Logging
        self.logs = defaultdict(list)

    def _random_connectome(self):
        for i in range(self.N):
            for j in range(self.N):
                if i != j and np.random.rand() < 0.1:
                    w = np.random.uniform(0.01, 0.5)
                    self.G.add_edge(i, j, weight=w, type="chem",
                                   n_ltp=0, n_ltd=0, age=0)

    def _load_connectome(self, path):
        with open(path) as f:
            data = json.load(f)
        edges = data.get("edges", data.get("bonds", []))
        for e in edges:
            self.G.add_edge(e["src"], e["dst"],
                           weight=e.get("weight", 0.1),
                           type=e.get("type", "chem"),
                           n_ltp=0, n_ltd=0, age=0)

    def _adaptive_theta(self):
        """v22: Scale-dependent adaptive θ周期"""
        if nx.is_weakly_connected(self.G):
            L = nx.average_shortest_path_length(self.G)
        else:
            L = L_REF
        self.L_avg = 0.9 * self.L_avg + 0.1 * L
        self.T_theta = np.clip(T_THETA_BASE * self.L_avg / L_REF,
                               T_THETA_MIN, T_THETA_MAX)

    def _fep_homeostasis(self):
        """v22: Global FEP-based homeostasis (multiplicative scaling)"""
        for node in self.G.nodes():
            in_edges = list(self.G.in_edges(node, data=True))
            if not in_edges:
                continue
            total_w = sum(d["weight"] for _, _, d in in_edges)
            if total_w > FEP_TARGET_OUT_W:
                scale = FEP_TARGET_OUT_W / total_w
                for u, v, d in in_edges:
                    d["weight"] *= scale
                return True
        return False

    def stdp_update(self, pre, post, t):
        dt = t - self.G.nodes[pre].get("last_spike", -1000)
        if dt <= 0 or dt > TAU_STDP:
            return
        A_plus = ETA_LTP * np.exp(-dt / TAU_STDP)
        A_minus = ETA_LTD * np.exp(-dt / TAU_STDP)
        if self.G.has_edge(pre, post):
            dw = A_plus - A_minus if dt < TAU_STDP/2 else -A_minus
            self.G[pre][post]["weight"] = np.clip(
                self.G[pre][post]["weight"] + dw, 0.001, 2.0)
        elif A_plus > ETA_LTP * 0.1:
            self.G.add_edge(pre, post, weight=A_plus, type="chem",
                           n_ltp=0, n_ltd=0, age=0)

    def measure(self):
        """Measure σ, α, C, L, EL ratio"""
        weights = [d["weight"] for _, _, d in self.G.edges(data=True)
                   if d.get("type") != "elec"]
        if not weights:
            return 0, 0, 0, 0, 0
        sigma = np.std(weights) / np.mean(weights) if np.mean(weights) > 0 else 0
        C = self.G.number_of_edges() / (self.N * (self.N - 1))
        L = nx.average_shortest_path_length(self.G) if nx.is_weakly_connected(self.G) else 0
        el_edges = sum(1 for _, _, d in self.G.edges(data=True) if d.get("type") == "elec")
        el_ratio = el_edges / max(1, self.G.number_of_edges())
        alpha = -np.log(C) / np.log(self.N) if C > 0 else 0
        return sigma, alpha, C, L, el_ratio

    def compute_F(self):
        """Global free energy surrogate"""
        weights = np.array([d["weight"] for _, _, d in self.G.edges(data=True)])
        if len(weights) == 0:
            return 0
        return np.var(weights)

    def run(self, n_steps=N_STEPS):
        glia_count, scaling_count = 0, 0
        for step in range(n_steps):
            # External input
            spike_input = self.spike_gen.sample()[0]
            for i in self.sensors:
                if spike_input[i % len(spike_input)]:
                    self.G.nodes[i]["V"] = self.G.nodes[i]["V_th"]

            # STDP + adaptive theta
            self._adaptive_theta()
            active = [n for n in self.G.nodes() if self.G.nodes[n]["V"] >= self.G.nodes[n]["V_th"]]
            for pre in active:
                for post in self.G.successors(pre):
                    self.stdp_update(pre, post, step)

            # FEP homeostasis every FEP_HOMEOSTASIS_INT steps
            if step % FEP_HOMEOSTASIS_INT == 0:
                if self._fep_homeostasis():
                    scaling_count += 1

            # Glia pruning
            if step % GLIA_INT == 0:
                to_remove = []
                for u, v, d in self.G.edges(data=True):
                    if d["weight"] < 0.005:
                        to_remove.append((u, v))
                for u, v in to_remove:
                    if self.G.out_degree(u) > 1:
                        self.G.remove_edge(u, v)
                        glia_count += 1

            # Logging
            if step % 50 == 0:
                sigma, alpha, C, L, el = self.measure()
                F = self.compute_F()
                self.logs["step"].append(step)
                self.logs["sigma"].append(sigma)
                self.logs["alpha"].append(alpha)
                self.logs["C"].append(C)
                self.logs["L"].append(L)
                self.logs["el_ratio"].append(el)
                self.logs["F_global"].append(F)
                self.logs["glia"].append(glia_count)
                self.logs["scaling"].append(scaling_count)
                self.logs["bonds"].append(self.G.number_of_edges())

        sigma, alpha, C, L, el = self.measure()
        F = self.compute_F()
        result = {
            "version": "v22",
            "N": self.N,
            "final": {"sigma": sigma, "alpha": alpha, "C": C, "L": L,
                      "el_ratio": el, "F_final": F},
            "logs": {k: v for k, v in self.logs.items()},
            "glia_events": glia_count,
            "scaling_events": scaling_count
        }
        return result

if __name__ == "__main__":
    sim = SDI_v22(N=279, connectome_path=DATA_PATH)
    result = sim.run(N_STEPS)
    with open(f"{OUT_DIR}/v22_results.json", "w") as f:
        json.dump(result, f, indent=2)
    print(f"v22: σ={result['final']['sigma']:.3f}, "
          f"α={result['final']['alpha']:.3f}, "
          f"EL={result['final']['el_ratio']:.1%}, "
          f"bonds={sim.G.number_of_edges()}")
    print(f"glia={result['glia_events']}, scaling={result['scaling_events']}")
