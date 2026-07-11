#!/usr/bin/env python3
"""SDI v23 — FEP-STDP Parameter Fusion (Transitional)
======================================================
Attempt to fuse FEP signals into STDP parameters directly.
Result: Proved parameter fusion insufficient → led to v24 deep fusion.
σ=2.74, α=0.53, EL=34.4%, short run (250 steps)
"""

import numpy as np, networkx as nx, json, os, warnings
from collections import defaultdict
warnings.filterwarnings("ignore")
np.random.seed(42)

DATA_PATH = "connectome_v8_data.json"
OUT_DIR = "v23_results"
os.makedirs(OUT_DIR, exist_ok=True)

TAU_STDP, ETA_LTP, ETA_LTD = 20.0, 0.020, 0.016
Ea_S, Ea_L = 0.15, 0.85
THETA_LTP_BASE, THETA_LTD, T_DECAY = 15, 8, 25000
TAU_REC, U_SE_CHEM, U_SE_ELEC = 150, 0.45, 0.10
T_THETA_BASE, L_REF, V_C = 15, 2.44, 1.0
T_THETA_MIN, T_THETA_MAX = 5, 100
SCALING_THR, SCALING_RATE, SCALING_INT = 0.35, 0.12, 15
GLIA_THR, GLIA_RATE, GLIA_INT = 0.45, 0.25, 50
SEED_FRAC_SENSOR = 0.20
N_STEPS = 250; CASCADE_MAX = 15

# v23: FEP parameter modulation (proved insufficient)
FEP_MOD_ETA = True      # Modulate LTP/LTD rates by FEP
FEP_ETA_SCALE = 1.5      # FEP-converged nodes get x1.5 LTP rate

class SDI_v23:
    def __init__(self, N=279, connectome_path=None):
        self.N = N
        self.G = nx.DiGraph()
        for i in range(N):
            ntype = "E" if np.random.rand() < 0.8 else "I"
            self.G.add_node(i, type=ntype, V=0, V_rest=-65, V_th=-50,
                           refractory=0, last_spike=-1000, F_history=[])

        if connectome_path and os.path.exists(connectome_path):
            with open(connectome_path) as f:
                data = json.load(f)
            edges = data.get("edges", data.get("bonds", []))
            for e in edges:
                self.G.add_edge(e["src"], e["dst"],
                               weight=e.get("weight",0.1), type="chem",
                               n_ltp=0, n_ltd=0, age=0)
        else:
            for i in range(N):
                for j in range(N):
                    if i != j and np.random.rand() < 0.1:
                        self.G.add_edge(i, j, weight=np.random.uniform(0.01,0.5),
                                       type="chem", n_ltp=0, n_ltd=0, age=0)

        self.sensors = np.random.choice(N, max(1,int(N*SEED_FRAC_SENSOR)), replace=False)
        self.L_avg, self.T_theta = L_REF, T_THETA_BASE
        self.logs = defaultdict(list)

    def _adaptive_theta(self):
        if nx.is_weakly_connected(self.G):
            L = nx.average_shortest_path_length(self.G)
        else:
            L = L_REF
        self.L_avg = 0.9*self.L_avg + 0.1*L
        self.T_theta = np.clip(T_THETA_BASE*self.L_avg/L_REF, T_THETA_MIN, T_THETA_MAX)

    def _node_F_convergence(self, node):
        """Simple FEP convergence check: low variance in recent activity"""
        hist = self.G.nodes[node].get("F_history", [])
        if len(hist) < 5:
            return False
        return np.var(hist[-10:]) < 0.01 if len(hist)>=10 else False

    def stdp_update(self, pre, post, t):
        dt = t - self.G.nodes[pre].get("last_spike", -1000)
        if dt <= 0 or dt > TAU_STDP:
            return

        # v23: FEP-modulated learning rates
        fep_conv = self._node_F_convergence(pre)
        eta_l = ETA_LTP * (FEP_ETA_SCALE if fep_conv else 1.0)
        eta_d = ETA_LTD * (1.0/FEP_ETA_SCALE if fep_conv else 1.0)

        A_plus = eta_l * np.exp(-dt/TAU_STDP)
        A_minus = eta_d * np.exp(-dt/TAU_STDP)

        if self.G.has_edge(pre, post):
            dw = A_plus - A_minus if dt < TAU_STDP/2 else -A_minus
            self.G[pre][post]["weight"] = np.clip(self.G[pre][post]["weight"]+dw, 0.001, 2.0)
        elif A_plus > ETA_LTP*0.1:
            self.G.add_edge(pre, post, weight=A_plus, type="chem", n_ltp=0, n_ltd=0, age=0)

    def measure(self):
        weights = [d["weight"] for _,_,d in self.G.edges(data=True)]
        sigma = np.std(weights)/np.mean(weights) if weights and np.mean(weights)>0 else 0
        C = self.G.number_of_edges()/(self.N*(self.N-1))
        L = nx.average_shortest_path_length(self.G) if nx.is_weakly_connected(self.G) else 0
        el = sum(1 for _,_,d in self.G.edges(data=True) if d.get("type")=="elec")/max(1,self.G.number_of_edges())
        alpha = -np.log(C)/np.log(self.N) if C>0 else 0
        return sigma, alpha, C, L, el

    def compute_F(self):
        w = np.array([d["weight"] for _,_,d in self.G.edges(data=True)])
        return np.var(w) if len(w)>0 else 0

    def run(self, n_steps=N_STEPS):
        glia_count, scaling_count = 0, 0
        for step in range(n_steps):
            self._adaptive_theta()
            # Random Poisson input
            for i in self.sensors:
                if np.random.rand() < 0.05:
                    self.G.nodes[i]["V"] = self.G.nodes[i]["V_th"]

            active = [n for n in self.G.nodes() if self.G.nodes[n]["V"]>=self.G.nodes[n]["V_th"]]
            for pre in active:
                for post in list(self.G.successors(pre)):
                    self.stdp_update(pre, post, step)

            if step % GLIA_INT == 0:
                to_rem = [(u,v) for u,v,d in self.G.edges(data=True) if d["weight"]<0.005 and self.G.out_degree(u)>1]
                for u,v in to_rem:
                    self.G.remove_edge(u,v); glia_count+=1

            if step % 50 == 0:
                sigma, alpha, C, L, el = self.measure()
                F = self.compute_F()
                self.logs["step"].append(step); self.logs["sigma"].append(sigma)
                self.logs["alpha"].append(alpha); self.logs["el_ratio"].append(el)
                self.logs["F_global"].append(F); self.logs["L"].append(L)
                self.logs["bonds"].append(self.G.number_of_edges())
                self.logs["glia"].append(glia_count); self.logs["scaling"].append(scaling_count)
                self.logs["theta"].append(int(self.T_theta))

        sigma, alpha, C, L, el = self.measure()
        return {"version":"v23","N":self.N,
                "final":{"sigma":sigma,"alpha":alpha,"C":C,"L":L,"el_ratio":el,"F_final":self.compute_F()},
                "logs":{k:v for k,v in self.logs.items()},
                "glia_events":glia_count,"scaling_events":scaling_count}

if __name__ == "__main__":
    sim = SDI_v23(N=279, connectome_path=DATA_PATH)
    r = sim.run(250)
    with open(f"{OUT_DIR}/v23_results.json","w") as f:
        json.dump(r, f, indent=2)
    print(f"v23: sigma={r['final']['sigma']:.3f}, alpha={r['final']['alpha']:.3f}, EL={r['final']['el_ratio']:.1%}")
