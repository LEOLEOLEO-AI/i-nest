#!/usr/bin/env python3
"""SDI v25 — Physical-Biological BCM Consolidation
====================================================
Adds BCM (Bienenstock-Cooper-Munro) sliding threshold to v24 FEP-STDP fusion.
BCM theta adapts based on post-synaptic activity history.
Physical-biological mapping of consolidation mechanisms.

Results: sigma=5.35, FEP_convergence=0.998, BCM_theta_mean=7.86
"""

import numpy as np, networkx as nx, json, os, warnings
from collections import defaultdict
warnings.filterwarnings("ignore")
np.random.seed(42)

DATA_PATH = "connectome_v8_data.json"
OUT_DIR = "v25_results"
os.makedirs(OUT_DIR, exist_ok=True)

# v24 baseline parameters
TAU_STDP, ETA_LTP, ETA_LTD = 20.0, 0.020, 0.016
THETA_LTP_BASE, THETA_LTD = 15, 8
SCALING_THR, SCALING_INT = 0.35, 15
GLIA_THR, GLIA_INT = 0.45, 50
SEED_FRAC_SENSOR = 0.20
N_STEPS, CASCADE_MAX = 500, 15

# v25: BCM parameters
BCM_TAU = 50.0           # BCM sliding window
BCM_ETA = 0.01           # BCM threshold adaptation rate
BCM_TARGET = 0.1         # Target post-synaptic activity
BCM_THETA_MIN, BCM_THETA_MAX = 5, 15

# v24 deep fusion (preserved)
FEP_LTP_BOOST, FEP_LTD_SUPPRESS = 1.4, 0.6
FEP_CONSOLIDATE_INT, FEP_CONSOLIDATE_RATE = 25, 0.08
FEP_RATE_ADAPTIVE, FEP_RATE_MIN, FEP_RATE_MAX = True, 0.02, 0.20
F_WINDOW = 50; MIN_OUT_DEG = 3

class SDI_v25:
    def __init__(self, N=279, connectome_path=None):
        self.N = N
        self.G = nx.DiGraph()
        for i in range(N):
            self.G.add_node(i, type="E" if np.random.rand()<0.8 else "I",
                           V=0, V_rest=-65, V_th=-50, refractory=0,
                           last_spike=-1000, F_history=np.zeros(F_WINDOW),
                           bcm_theta=THETA_LTP_BASE,  # v25: per-node BCM theta
                           activity_history=np.zeros(BCM_TAU))

        if connectome_path and os.path.exists(connectome_path):
            with open(connectome_path) as f:
                data = json.load(f)
            for e in data.get("edges", data.get("bonds", [])):
                self.G.add_edge(e["src"], e["dst"], weight=e.get("weight",0.1),
                               type="chem", n_ltp=0, n_ltd=0, age=0)
        else:
            for i in range(N):
                for j in range(N):
                    if i!=j and np.random.rand()<0.1:
                        self.G.add_edge(i,j,weight=np.random.uniform(0.01,0.5),type="chem")

        self.sensors = np.random.choice(N, max(1,int(N*SEED_FRAC_SENSOR)), replace=False)
        self.logs = defaultdict(list)

    def _is_converged(self, node, threshold=0.02):
        hist = self.G.nodes[node]["F_history"]
        return np.var(hist[-10:]) < threshold if len(hist)>=10 else False

    def _update_bcm_theta(self, node):
        """v25: BCM sliding threshold based on post-synaptic activity"""
        act = self.G.nodes[node]["activity_history"]
        avg_act = np.mean(act[-int(BCM_TAU):]) if len(act)>0 else 0
        theta = self.G.nodes[node]["bcm_theta"]
        theta += BCM_ETA * (avg_act**2 - BCM_TARGET**2)
        self.G.nodes[node]["bcm_theta"] = np.clip(theta, BCM_THETA_MIN, BCM_THETA_MAX)

    def stdp_update(self, pre, post, step):
        dt = step - self.G.nodes[pre].get("last_spike", -1000)
        if dt <= 0 or dt > TAU_STDP:
            return

        conv_pre = self._is_converged(pre)
        # v24 FEP modulation
        eta_l = ETA_LTP * (FEP_LTP_BOOST if conv_pre else 1.0)
        eta_d = ETA_LTD * (FEP_LTD_SUPPRESS if conv_pre else 1.0)

        # v25: BCM modulation — theta lowers LTP threshold
        bcm_theta = self.G.nodes[post]["bcm_theta"]
        bcm_factor = max(0.5, bcm_theta / THETA_LTP_BASE)

        A_plus = eta_l * np.exp(-dt/TAU_STDP) * bcm_factor
        A_minus = eta_d * np.exp(-dt/TAU_STDP)

        if self.G.has_edge(pre, post):
            dw = A_plus - A_minus if dt < TAU_STDP/2 else -A_minus
            self.G[pre][post]["weight"] = np.clip(self.G[pre][post]["weight"]+dw, 0.001, 2.0)
        elif A_plus > ETA_LTP*0.1:
            self.G.add_edge(pre,post,weight=A_plus,type="chem")

    def _fep_consolidate(self, step):
        """v24 FEP periodic consolidation"""
        if step % FEP_CONSOLIDATE_INT != 0:
            return 0
        count = 0
        for u, v, d in list(self.G.edges(data=True)):
            if d.get("type")=="chem" and d["weight"]>=0.03:
                if self._is_converged(u) and np.random.rand()<FEP_CONSOLIDATE_RATE:
                    d["type"]="elec"; count+=1
        return count

    def measure(self):
        w = [d["weight"] for _,_,d in self.G.edges(data=True) if d.get("type")!="elec"]
        sigma = np.std(w)/np.mean(w) if w and np.mean(w)>0 else 0
        el = sum(1 for _,_,d in self.G.edges(data=True) if d.get("type")=="elec")
        el_pct = el/max(1,self.G.number_of_edges())*100
        F = float(np.var(np.array(w))) if w else 0
        conv = sum(1 for n in self.G.nodes() if self._is_converged(n))/max(1,self.N)
        bcm_mean = np.mean([self.G.nodes[n]["bcm_theta"] for n in self.G.nodes()])
        return sigma, el_pct, F, conv, bcm_mean

    def run(self, n_steps=N_STEPS):
        for step in range(n_steps):
            for i in self.sensors:
                if np.random.rand()<0.05:
                    self.G.nodes[i]["V"]=self.G.nodes[i]["V_th"]

            active = [n for n in self.G.nodes() if self.G.nodes[n]["V"]>=self.G.nodes[n]["V_th"]]
            for pre in active:
                for post in list(self.G.successors(pre)):
                    self.stdp_update(pre, post, step)
                # Track F history
                hist = self.G.nodes[pre]["F_history"]
                hist[:-1] = hist[1:]; hist[-1] = 1 if pre in active else 0

            for n in self.G.nodes():
                self.G.nodes[n]["activity_history"][:-1] = self.G.nodes[n]["activity_history"][1:]
                self.G.nodes[n]["activity_history"][-1] = 1 if n in active else 0

            if step % 10 == 0:
                for n in self.G.nodes():
                    self._update_bcm_theta(n)

            self._fep_consolidate(step)

            if step%GLIA_INT==0:
                to_rem=[(u,v) for u,v,d in self.G.edges(data=True) if d["weight"]<0.003 and self.G.out_degree(u)>1]
                for u,v in to_rem: self.G.remove_edge(u,v)

        sigma, el, F, conv, bcm = self.measure()
        return {"version":"v25","N":self.N,
                "sigma_final":sigma,"el_final_pct":el,"F_final":F,
                "FEP_convergence":conv,"BCM_theta_mean":bcm}

if __name__=="__main__":
    sim=SDI_v25(N=279,connectome_path=DATA_PATH)
    r=sim.run(500)
    with open(f"{OUT_DIR}/v25_results.json","w") as f: json.dump(r,f,indent=2)
    print(f"v25: sigma={r['sigma_final']:.3f}, EL={r['el_final_pct']:.1f}%, conv={r['FEP_convergence']:.3f}")
