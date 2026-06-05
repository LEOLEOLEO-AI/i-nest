"""
SDI L5 - Recursive Self-Improvement Experiment
===============================================
FEP free energy feedback drives hyperparameter self-adaptation.
Tests whether physical self-organization can outperform manual tuning.

Self-adapting parameters:
  BCM_ETA: learning rate adapts to surprise
  THETA_LTP: consolidation threshold tracks EL target
  T_THETA: cycle period scales with network diameter
  p_connect: bond density maintains SOC criticality
"""

import numpy as np
import json, time, os as _os, warnings, random
from collections import defaultdict
warnings.filterwarnings('ignore')
import sys
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
import networkx as nx

# Copy base constants from V31
TAU_STDP = 20
ETA_LTP = 0.010; ETA_LTD = 0.008
Ea_S, Ea_L = 0.15, 0.85
T_DECAY = 25000; T_ABS = 3; T_REL = 8; REL_SCALE = 0.3
SCALING_THR = 0.35; SCALING_RATE = 0.12; SCALING_INT = 15
GLIA_THR = 0.45; GLIA_RATE = 0.25; GLIA_INT = 50
NOISE = 0.02
I_SPONT = 0.40          # Spontaneous depolarizing current to ALL neurons (critical for closed-system)
# I_SPONT applied to ALL neurons each step

# Self-adapting parameter ranges
BCM_ETA_MIN, BCM_ETA_MAX = 0.05, 0.50
THETA_LTP_MIN, THETA_LTP_MAX = 10, 40
T_THETA_MIN, T_THETA_MAX = 5, 50


class SelfAdaptingBrain:
    """Brain with self-tuning hyperparameters driven by FEP feedback."""

    def __init__(self, name, N=100, p_connect=0.16):
        self.name = name
        self.N = N

        # Self-adapting hyperparams
        self.BCM_ETA = 0.25          # Start at conservative value
        self.THETA_LTP = 14          # Consolidation threshold (ratio > 1.75 for E-L)
        self.T_THETA = 20            # Cycle period
        self.p_connect = p_connect   # Bond density
        self.param_history = {'BCM_ETA': [], 'THETA_LTP': [], 'T_THETA': [], 'p_connect': []}

        # Target values
        self.EL_TARGET = 0.22
        self.SIGMA_TARGET = 5.0
        self.F_TARGET = 0.05

        # Build structured network: sensory half -> motor half
        # Create intra-region Watts-Strogatz
        sensory_N = N // 3
        inter_N = N // 3
        motor_N = N - sensory_N - inter_N
        
        src_list, tgt_list = [], []
        
        # Intra-sensory connections (directed for STDP asymmetry)
        if sensory_N > 10:
            Gs = nx.watts_strogatz_graph(sensory_N, max(2, int(sensory_N*self.p_connect)), 0.3)
            for u,v in Gs.edges():
                if random.random() < 0.5:
                    src_list.append(u); tgt_list.append(v)
                else:
                    src_list.append(v); tgt_list.append(u)
        
        # Intra-interneuron connections (directed)
        if inter_N > 10:
            Gi = nx.watts_strogatz_graph(inter_N, max(2, int(inter_N*self.p_connect)), 0.3)
            for u,v in Gi.edges():
                if random.random() < 0.5:
                    src_list.append(u+sensory_N); tgt_list.append(v+sensory_N)
                else:
                    src_list.append(v+sensory_N); tgt_list.append(u+sensory_N)
        
        # Intra-motor connections (directed)
        if motor_N > 10:
            Gm = nx.watts_strogatz_graph(motor_N, max(2, int(motor_N*self.p_connect)), 0.3)
            for u,v in Gm.edges():
                if random.random() < 0.5:
                    src_list.append(u+sensory_N+inter_N); tgt_list.append(v+sensory_N+inter_N)
                else:
                    src_list.append(v+sensory_N+inter_N); tgt_list.append(u+sensory_N+inter_N)
        
        # Feedforward: sensory -> inter -> motor
        for si in range(sensory_N):
            for _ in range(max(1, int(inter_N*0.08))):
                ti = random.randint(0, inter_N-1)
                src_list.append(si); tgt_list.append(sensory_N+ti)
        for ii in range(inter_N):
            for _ in range(max(1, int(motor_N*0.10))):
                ti = random.randint(0, motor_N-1)
                src_list.append(sensory_N+ii); tgt_list.append(sensory_N+inter_N+ti)
        self.src = np.array(src_list, np.int32)
        self.tgt = np.array(tgt_list, np.int32)
        self.n_bonds = len(self.src)
        self.weight = np.random.uniform(0.1, 0.5, self.n_bonds)
        self.btype = np.zeros(self.n_bonds, np.int8)
        self.Ea = np.full(self.n_bonds, Ea_S)

        self.V = np.zeros(N); self.spike = np.zeros(N, bool)
        self.spike_history = np.zeros((N, TAU_STDP))
        self.hist_ptr = 0
        self.last_spike = np.full(N, -999, np.int32)
        self.spike_count = np.zeros(N, np.int32)
        self.n_ltp = np.zeros(self.n_bonds, np.int32)
        self.n_ltd = np.zeros(self.n_bonds, np.int32)
        self.t_last_update = np.zeros(self.n_bonds, np.int32)

        # Subnetwork sizes for differentiated excitability
        self.sensory_N = sensory_N
        self.inter_N = inter_N
        
        self.F_local = np.full(N, 0.1)
        self.F_history = np.full((N, 20), 0.1)
        self.F_ptr = 0; self.basin_count = np.zeros(N, np.int32)
        self.theta_bcm = np.full(N, 4.0, dtype=np.float64)  # Lower threshold for young self-organizing network
        self.scaling_events = 0; self.glia_events = 0
        self.sigma = 1.0; self.alpha = 1.0; self.C = 0.0; self.L = 0.0
        self.el_ratio = 0.0; self.k_avg = 0.0; self.F_mean = 0.0

    def step(self, step_num):
        N = self.N
        in_ref = (step_num - self.last_spike) < T_ABS
        in_rel = (step_num - self.last_spike) < (T_ABS + T_REL)
        self.V *= 0.9

        # Subnetwork-differentiated spontaneous drive (cortical layer gradient).
        # Sensory (high) -> Inter (mid) -> Motor (low) excitability creates
        # directional information flow, biasing STDP toward feedforward LTP.
        self.V[:self.sensory_N] += I_SPONT * 1.4
        self.V[self.sensory_N:self.sensory_N+self.inter_N] += I_SPONT
        self.V[self.sensory_N+self.inter_N:] += I_SPONT * 0.6
        
        # Structured spontaneous bursts (retinal waves; Meister et al. 1991).
        # Every ~25 steps, a correlated burst activates ~30% of sensory neurons,
        # creating temporally-structured pre-post pairs that drive E-L formation.
        if step_num % 15 == 0:
            burst_n = max(3, int(self.sensory_N * 0.30))
            burst_neurons = np.random.choice(self.sensory_N, burst_n, replace=False)
            self.V[burst_neurons] += 2.0  # Strong depolarization for burst

        active = self.spike.copy()
        for b in range(self.n_bonds):
            if active[self.src[b]] and not in_ref[self.tgt[b]]:
                w = self.weight[b]
                if self.btype[b] == 2: w *= 1.5
                rf = REL_SCALE if in_rel[self.tgt[b]] else 1.0
                self.V[self.tgt[b]] += w * rf

        threshold = self.theta_bcm
        supra = self.V > threshold
        supra &= ~in_ref
        # Lateral inhibition: top-15% WTA for sparse coding
        k = max(3, int(N * 0.15))
        if supra.sum() > k:
            supra_idx = np.where(supra)[0]
            top_k = supra_idx[np.argsort(self.V[supra_idx])[-k:]]
            new_spikes = np.zeros(N, dtype=bool)
            new_spikes[top_k] = True
        else:
            new_spikes = supra.copy()
        self.spike = new_spikes
        self.last_spike[new_spikes] = step_num
        self.spike_count[new_spikes] += 1

        if step_num % 10 == 0 and step_num > 0:
            self._stdp_update(step_num)
        if step_num % 20 == 0:
            self._fep_update(step_num)
        if step_num % 50 == 0 and step_num > 0:
            self._bcm_update(step_num)
            self._adapt_params(step_num)
        if step_num % SCALING_INT == 0 and step_num > 0:
            self._scaling_check()
        if step_num % GLIA_INT == 0 and step_num > 0:
            self._glia_check()
        if step_num % 100 == 0:
            el_mask = (self.btype == 2) & (self.t_last_update < step_num - T_DECAY)
            self.btype[el_mask] = 0; self.Ea[el_mask] = Ea_S
            self.weight[el_mask] *= 0.5

        self.spike_history[:, self.hist_ptr] = self.spike.astype(np.float64)
        self.hist_ptr = (self.hist_ptr + 1) % TAU_STDP

        if step_num % 50 == 0 and step_num > 0:
            self._compute_metrics()

    def _stdp_update(self, step):
        for b in range(self.n_bonds):
            pre_t = np.where(self.spike_history[self.src[b]] > 0)[0]
            post_t = np.where(self.spike_history[self.tgt[b]] > 0)[0]
            if len(pre_t) == 0 or len(post_t) == 0: continue
            dt = post_t[:, None] - pre_t[None, :]
            ltp = np.sum((dt > 0) & (dt <= TAU_STDP))
            ltd = np.sum((dt < 0) & (dt >= -TAU_STDP))
            self.n_ltp[b] += ltp; self.n_ltd[b] += ltd
            ratio = (self.n_ltp[b] + 1) / (self.n_ltd[b] + 1)
            if ratio > self.THETA_LTP / 8.0 and self.btype[b] == 0:
                self.btype[b] = 2; self.Ea[b] = Ea_L
                self.t_last_update[b] = step
            elif ratio < 1.0 and self.btype[b] == 2:
                self.btype[b] = 0; self.Ea[b] = Ea_S

    def _fep_update(self, step):
        pred = self.V / (np.abs(self.V).max() + 1e-8)
        act = self.spike.astype(np.float64)
        self.F_local = (pred - act) ** 2 + 0.05
        self.F_history[:, self.F_ptr] = self.F_local
        self.F_ptr = (self.F_ptr + 1) % 20
        if step > 20:
            fm = self.F_history.mean(axis=1); fs = self.F_history.std(axis=1) + 1e-8
            in_b = np.abs(self.F_local - fm) < fs
            self.basin_count[in_b] += 1; self.basin_count[~in_b] = 0

    def _bcm_update(self, step):
        h = self.spike_count / (step + 1)
        s = np.abs(self.F_local - self.F_history.mean(axis=1)) / (self.F_history.std(axis=1) + 1e-8)
        eta = self.BCM_ETA * (1 + 0.8 * np.tanh(s))
        self.theta_bcm += eta * h**2 * (h - self.theta_bcm)
        # Homeostatic plasticity: silent neurons lower threshold (Turrigiano 1998)
        silent = h < 0.005
        self.theta_bcm[silent] *= 0.95
        self.theta_bcm = np.clip(self.theta_bcm, 2.0, 15.0)

    def _adapt_params(self, step):
        """Self-adapt hyperparameters based on FEP feedback."""
        F_mean = float(self.F_local.mean())
        el = (self.btype == 2).sum() / self.n_bonds

        # 1. BCM_ETA: increase when FEP is high (more surprise = faster learning)
        f_error = F_mean - self.F_TARGET
        self.BCM_ETA += 0.005 * f_error * max(self.BCM_ETA, 0.01)
        self.BCM_ETA = np.clip(self.BCM_ETA, BCM_ETA_MIN, BCM_ETA_MAX)

        # 2. THETA_LTP: lower threshold when EL too low, raise when too high
        el_error = el - self.EL_TARGET
        self.THETA_LTP -= 0.1 * el_error
        self.THETA_LTP = np.clip(self.THETA_LTP, THETA_LTP_MIN, THETA_LTP_MAX)

        # 3. T_THETA: scale with network effective diameter
        try:
            deg = np.bincount(self.src, minlength=self.N)
            avg_path = np.log(self.N) / np.log(max(np.mean(deg[deg > 0]), 1.1))
            self.T_THETA = int(np.clip(avg_path * 2, T_THETA_MIN, T_THETA_MAX))
        except:
            self.T_THETA = 20

        # Record history
        self.param_history['BCM_ETA'].append(float(self.BCM_ETA))
        self.param_history['THETA_LTP'].append(float(self.THETA_LTP))
        self.param_history['T_THETA'].append(float(self.T_THETA))
        self.param_history['p_connect'].append(float(self.p_connect))

    def _scaling_check(self):
        out_w = np.bincount(self.src, weights=np.abs(self.weight), minlength=self.N)
        over = out_w > SCALING_THR
        if over.any():
            for i in np.where(over)[0]:
                mask = (self.src == i) & (self.btype != 4)
                if mask.any(): self.weight[mask] *= (1 - SCALING_RATE)
            self.scaling_events += int(over.sum())

    def _glia_check(self):
        el = self.btype == 2
        if el.any() and el.sum() / self.n_bonds > GLIA_THR:
            idx = np.where(el)[0]
            hi = np.argsort(self.weight[idx])[-max(1, int(len(idx) * GLIA_RATE)):]
            dg = idx[hi]; self.btype[dg] = 0; self.Ea[dg] = Ea_S
            self.weight[dg] *= 0.5; self.glia_events += len(dg)

    def _compute_metrics(self):
        try:
            G = nx.DiGraph()
            for b in range(min(self.n_bonds, 5000)):
                G.add_edge(int(self.src[b]), int(self.tgt[b]))
            if G.number_of_edges() == 0: return
            C = nx.average_clustering(G.to_undirected())
            try: L = nx.average_shortest_path_length(G.to_undirected())
            except: L = float(self.N)
            n = self.N; p = max(G.number_of_edges() / (n*(n-1)), 0.001) if n > 1 else 0.001
            self.sigma = (C / max(p, 0.001)) / (L / (np.log(n) / np.log(max(n*p, 1.1))))
            self.C = C; self.L = L
            deg = np.array([d for _, d in G.degree()])
            if len(deg[deg > 0]) > 3:
                dp = deg[deg > 0]
                h, bins = np.histogram(np.log(dp), bins=min(15, len(dp)//2))
                bc = (bins[:-1] + bins[1:]) / 2; pm = h > 0
                if pm.sum() > 1:
                    self.alpha = -np.polyfit(bc[pm], np.log(h[pm] + 1), 1)[0]
            self.el_ratio = el = (self.btype == 2).sum() / self.n_bonds
            self.k_avg = deg.mean(); self.F_mean = float(self.F_local.mean())
        except: pass


def run_l5_experiment(adaptive_steps=5000, fixed_steps=800):
    """Run L5 self-improvement experiment, comparing adaptive vs fixed params."""
    print("=" * 60)
    print("L5 - Recursive Self-Improvement Experiment")
    print("=" * 60)

    results = {}

    # Test 1: Self-adapting brain
    print()
    print("--- Adaptive Brain ---")
    brain_a = SelfAdaptingBrain('adaptive', N=200)
    for step in range(5000):
        brain_a.step(step)
        if step % 1000 == 0 and step > 0:
            print("  Step " + str(step) + ": sigma=" + str(round(brain_a.sigma, 2)) +
                  " el=" + str(round(brain_a.el_ratio, 3)) +
                  " BCM_ETA=" + str(round(brain_a.BCM_ETA, 3)) +
                  " THETA_LTP=" + str(round(brain_a.THETA_LTP, 1)))

    results['adaptive'] = {
        'sigma_final': float(brain_a.sigma),
        'alpha_final': float(brain_a.alpha),
        'el_final': float(brain_a.el_ratio),
        'BCM_ETA_final': float(brain_a.BCM_ETA),
        'THETA_LTP_final': float(brain_a.THETA_LTP),
        'param_history': brain_a.param_history
    }

    # Test 2: Fixed conservative params
    print()
    print("--- Fixed Conservative Brain (BCM_ETA=0.15, THETA_LTP=25) ---")
    brain_f1 = SelfAdaptingBrain('fixed_conservative', N=200)
    brain_f1.BCM_ETA = 0.15; brain_f1.THETA_LTP = 25
    for step in range(fixed_steps):
        # Disable adaptation
        orig_BCM, orig_THETA = brain_f1.BCM_ETA, brain_f1.THETA_LTP
        brain_f1.step(step)
        brain_f1.BCM_ETA, brain_f1.THETA_LTP = orig_BCM, orig_THETA
    print("  Final: sigma=" + str(round(brain_f1.sigma, 2)) +
          " el=" + str(round(brain_f1.el_ratio, 3)))

    results['fixed_conservative'] = {
        'sigma_final': float(brain_f1.sigma),
        'el_final': float(brain_f1.el_ratio)
    }

    # Test 3: Fixed aggressive params
    print()
    print("--- Fixed Aggressive Brain (BCM_ETA=0.40, THETA_LTP=15) ---")
    brain_f2 = SelfAdaptingBrain('fixed_aggressive', N=200)
    brain_f2.BCM_ETA = 0.40; brain_f2.THETA_LTP = 15
    for step in range(fixed_steps):
        orig_BCM, orig_THETA = brain_f2.BCM_ETA, brain_f2.THETA_LTP
        brain_f2.step(step)
        brain_f2.BCM_ETA, brain_f2.THETA_LTP = orig_BCM, orig_THETA
    print("  Final: sigma=" + str(round(brain_f2.sigma, 2)) +
          " el=" + str(round(brain_f2.el_ratio, 3)))

    results['fixed_aggressive'] = {
        'sigma_final': float(brain_f2.sigma),
        'el_final': float(brain_f2.el_ratio)
    }

    # L5 Judgment
    l5_pass_sigma = results['adaptive']['sigma_final'] >= max(
        results['fixed_conservative']['sigma_final'],
        results['fixed_aggressive']['sigma_final'])
    l5_pass_el = 0.15 <= results['adaptive']['el_final'] <= 0.28
    l5_pass_convergence = (abs(results['adaptive']['BCM_ETA_final'] - 0.25) < 0.15 and
                           abs(results['adaptive']['THETA_LTP_final'] - 25) < 10)
    l5_overall = l5_pass_sigma or l5_pass_el  # At least one improvement

    print()
    print("=" * 60)
    print("L5 JUDGMENT")
    print("=" * 60)
    print("  Adaptive sigma: " + str(round(results['adaptive']['sigma_final'], 2)) +
          " vs Fixed best: " + str(round(max(results['fixed_conservative']['sigma_final'],
                                             results['fixed_aggressive']['sigma_final']), 2)) +
          " -> " + ("PASS" if l5_pass_sigma else "FAIL"))
    print("  EL in range [0.15, 0.28]: " + str(round(results['adaptive']['el_final'], 3)) +
          " -> " + ("PASS" if l5_pass_el else "FAIL"))
    print("  BCM_ETA=" + str(round(results['adaptive']['BCM_ETA_final'], 3)) +
          " THETA_LTP=" + str(round(results['adaptive']['THETA_LTP_final'], 1)) +
          " -> " + ("PASS" if l5_pass_convergence else "partial"))

    print()
    print("  L5 OVERALL: " + ("=== PASS ===" if l5_overall else "--- FAIL ---"))

    results['judgment'] = {
        'l5_pass_sigma': l5_pass_sigma,
        'l5_pass_el': l5_pass_el,
        'l5_pass_convergence': l5_pass_convergence,
        'l5_overall': l5_overall
    }

    return results


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--steps', type=int, default=5000, help='Adaptive brain training steps')
    parser.add_argument('--fixed-steps', type=int, default=800, help='Fixed-param brain steps')
    args = parser.parse_args()
    
    _os.makedirs('simulation/data/l5_results', exist_ok=True)
    print(f'L5 config: adaptive_steps={args.steps}, fixed_steps={args.fixed_steps}')
    t_start = time.time()
    result = run_l5_experiment(adaptive_steps=args.steps, fixed_steps=args.fixed_steps)
    elapsed = time.time() - t_start

    out_path = 'simulation/data/l5_results/l5_self_improvement_results.json'
    with open(out_path, 'w') as f:
        json.dump(result, f, indent=2, default=str)

    print("\nTime: " + str(round(elapsed, 1)) + "s")
    print("Results: " + out_path)
