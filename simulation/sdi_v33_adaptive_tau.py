"""SDI V33 - Adaptive Tau: Surprise-Driven STDP Window
Based on Idea #7: LNN adaptive tau for SDI simulation.
Key innovation: STDP time window adapts per-neuron based on local surprise.
tau_i(t) = tau_base / (1 + alpha_tau * surprise_i(t))
surprise_i(t) = |F_local - mean(F_history)| / std(F_history)
"""
import numpy as np, json, os as _os, warnings, random, time
from collections import defaultdict
warnings.filterwarnings("ignore")
import networkx as nx

TAU_BASE = 20; ETA_LTP = 0.010; ETA_LTD = 0.008
Ea_S = 0.15; Ea_L = 0.85
THETA_LTP_BASE = 16; THETA_LTD = 8
T_DECAY = 25000; T_ABS = 3; T_REL = 8; REL_SCALE = 0.3
SCALING_THR = 0.35; SCALING_RATE = 0.12; SCALING_INT = 15
GLIA_THR = 0.45; GLIA_RATE = 0.25; GLIA_INT = 50
NOISE_LEVEL = 0.02; I_SPONT = 0.40

class TauConfig:
    def __init__(self, enabled=True, tau_base=20.0, alpha_tau=1.0,
                 tau_min=5.0, tau_max=50.0):
        self.enabled = enabled
        self.tau_base = tau_base
        self.alpha_tau = alpha_tau
        self.tau_min = tau_min
        self.tau_max = tau_max

class AdaptiveBrainRegion:
    """Single brain region with adaptive tau mechanism."""

    def __init__(self, name, N, p_connect=0.08, tau_cfg=None):
        self.name = name; self.N = N
        self.tau_cfg = tau_cfg or TauConfig()
        k = max(2, int(N * p_connect))
        G = nx.watts_strogatz_graph(N, k, 0.3)
        edges = list(G.edges())
        src_list, tgt_list = [], []
        for u, v in edges:
            if random.random() < 0.5:
                src_list.append(u); tgt_list.append(v)
            else:
                src_list.append(v); tgt_list.append(u)
        self.src = np.array(src_list, np.int32)
        self.tgt = np.array(tgt_list, np.int32)
        self.n_bonds = len(self.src)
        self.weight = np.random.uniform(0.1, 0.5, self.n_bonds).astype(np.float64)
        self.btype = np.zeros(self.n_bonds, dtype=np.int8)
        self.Ea = np.full(self.n_bonds, Ea_S, dtype=np.float64)
        self.V = np.zeros(N, dtype=np.float64)
        self.spike = np.zeros(N, bool)
        max_tau = int(self.tau_cfg.tau_max * 2)
        self.spike_history = np.zeros((N, max_tau), dtype=np.float64)
        self.hist_ptr = 0
        self.last_spike = np.full(N, -999, dtype=np.int32)
        self.spike_count = np.zeros(N, np.int32)
        self.n_ltp = np.zeros(self.n_bonds, dtype=np.int32)
        self.n_ltd = np.zeros(self.n_bonds, dtype=np.int32)
        self.t_last_update = np.zeros(self.n_bonds, dtype=np.int32)
        self.F_local = np.full(N, 0.1, dtype=np.float64)
        self.F_history = np.full((N, 20), 0.1, np.float64)
        self.F_ptr = 0
        self.basin_count = np.zeros(N, np.int32)
        self.theta_bcm = np.full(N, 4.0, dtype=np.float64)
        self.BCM_ETA = 0.25
        self.R = np.ones(self.n_bonds, dtype=np.float64)
        self.scaling_events = 0; self.glia_events = 0
        self.sigma = 1.0; self.alpha = 1.0
        self.C = 0.0; self.L = 0.0
        self.el_ratio = 0.0; self.k_avg = 0.0; self.F_mean = 0.0
        self.tau_per_neuron = np.full(N, self.tau_cfg.tau_base, dtype=np.float64)
        self.surprise_per_neuron = np.zeros(N, dtype=np.float64)
        self.tau_history = []

    def _compute_surprise(self):
        fm = self.F_history.mean(axis=1)
        fs = self.F_history.std(axis=1) + 1e-8
        self.surprise_per_neuron = np.abs(self.F_local - fm) / fs

    def _update_tau(self):
        if not self.tau_cfg.enabled:
            self.tau_per_neuron.fill(self.tau_cfg.tau_base)
            return
        self._compute_surprise()
        s = np.clip(self.surprise_per_neuron, 0, 10)
        self.tau_per_neuron = self.tau_cfg.tau_base / (1.0 + self.tau_cfg.alpha_tau * s)
        self.tau_per_neuron = np.clip(self.tau_per_neuron,
                                       self.tau_cfg.tau_min,
                                       self.tau_cfg.tau_max)

    def _get_tau_for_bond(self, b):
        if self.tau_cfg.enabled:
            return int(self.tau_per_neuron[self.src[b]])
        return int(self.tau_cfg.tau_base)

    def step(self, step_num, external_input=None):
        N = self.N
        in_ref = (step_num - self.last_spike) < T_ABS
        in_rel = (step_num - self.last_spike) < (T_ABS + T_REL)
        self.V *= 0.9; self.V += I_SPONT
        if external_input is not None:
            self.V += external_input

        active = self.spike.copy()
        for b in range(self.n_bonds):
            if active[self.src[b]] and not in_ref[self.tgt[b]]:
                w = self.weight[b] * self.R[b]
                if self.btype[b] == 2: w *= 1.5
                rf = REL_SCALE if in_rel[self.tgt[b]] else 1.0
                self.V[self.tgt[b]] += w * rf

        threshold = self.theta_bcm
        supra = self.V > threshold
        supra &= ~in_ref
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

        if step_num % 10 == 0 and step_num > 0: self._stdp_update(step_num)
        if step_num % 20 == 0:
            self._fep_update(step_num)
            self._update_tau()
        if step_num % 50 == 0 and step_num > 0: self._bcm_update(step_num)
        if step_num % SCALING_INT == 0 and step_num > 0: self._scaling_check()
        if step_num % GLIA_INT == 0 and step_num > 0: self._glia_check()

        if step_num % 100 == 0:
            el_mask = (self.btype == 2) & (self.t_last_update < step_num - T_DECAY)
            self.btype[el_mask] = 0
            self.Ea[el_mask] = Ea_S
            self.weight[el_mask] *= 0.5

        max_hist = self.spike_history.shape[1]
        self.spike_history[:, self.hist_ptr % max_hist] = self.spike.astype(np.float64)
        self.hist_ptr += 1

        if step_num % 50 == 0 and step_num > 0:
            self._compute_metrics()
            self.tau_history.append({
                "step": step_num,
                "tau_mean": float(self.tau_per_neuron.mean()),
                "tau_std": float(self.tau_per_neuron.std()),
                "surprise_mean": float(self.surprise_per_neuron.mean())
            })

    def _stdp_update(self, step):
        max_hist = self.spike_history.shape[1]
        for b in range(self.n_bonds):
            if self.btype[b] == 4: continue
            tau_b = self._get_tau_for_bond(b)
            window = min(tau_b, max_hist // 2)
            ptr = self.hist_ptr % max_hist
            if ptr >= window:
                pre = self.spike_history[self.src[b], ptr-window:ptr]
                post = self.spike_history[self.tgt[b], ptr-window:ptr]
            else:
                pre = np.concatenate([
                    self.spike_history[self.src[b], ptr-window:],
                    self.spike_history[self.src[b], :ptr]])
                post = np.concatenate([
                    self.spike_history[self.tgt[b], ptr-window:],
                    self.spike_history[self.tgt[b], :ptr]])
            pre_t = np.where(pre > 0)[0]
            post_t = np.where(post > 0)[0]
            if len(pre_t) == 0 or len(post_t) == 0: continue
            half = window // 2
            dt = post_t[:, None] - pre_t[None, :]
            dt_s = dt - half
            ltp = np.sum((dt_s > 0) & (dt_s <= half))
            ltd = np.sum((dt_s < 0) & (dt_s >= -half))
            self.n_ltp[b] += ltp; self.n_ltd[b] += ltd
            ratio = (self.n_ltp[b] + 1) / (self.n_ltd[b] + 1)
            if ratio > THETA_LTP_BASE / THETA_LTD and self.btype[b] == 0:
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
            fm = self.F_history.mean(axis=1)
            fs = self.F_history.std(axis=1) + 1e-8
            in_b = np.abs(self.F_local - fm) < fs
            self.basin_count[in_b] += 1
            self.basin_count[~in_b] = 0

    def _bcm_update(self, step):
        h = self.spike_count / (step + 1)
        s = np.abs(self.F_local - self.F_history.mean(axis=1))
        s = s / (self.F_history.std(axis=1) + 1e-8)
        eta = self.BCM_ETA * (1 + 0.8 * np.tanh(s))
        self.theta_bcm += eta * h**2 * (h - self.theta_bcm)
        silent = h < 0.005; self.theta_bcm[silent] *= 0.95
        self.theta_bcm = np.clip(self.theta_bcm, 2.0, 15.0)

    def _scaling_check(self):
        out_w = np.bincount(self.src, weights=np.abs(self.weight), minlength=self.N)
        over = out_w > SCALING_THR * self.N * 0.08 * 0.5
        if over.any():
            for b in range(self.n_bonds):
                if over[self.src[b]]:
                    self.weight[b] *= (1 - SCALING_RATE)
            self.scaling_events += 1

    def _glia_check(self):
        spike_max = max(self.spike_count.max(), 1)
        dead = (self.spike_count / (spike_max + 1e-8)) < 0.01
        if dead.sum() > self.N * GLIA_THR:
            for b in range(self.n_bonds):
                if dead[self.src[b]] or dead[self.tgt[b]]:
                    self.weight[b] *= (1 + GLIA_RATE * random.random())
            self.glia_events += 1

    def _compute_metrics(self):
        self.k_avg = float(len(np.where(self.btype == 2)[0]) / max(self.n_bonds, 1))
        e_mask = self.btype == 2; l_mask = self.btype == 0
        self.el_ratio = float((e_mask.sum() + 1) / (l_mask.sum() + 1))
        self.C = float(np.mean(self.weight))
        self.L = float(np.std(self.weight))
        self.alpha = float(self.C / (self.L + 1e-8))
        self.sigma = float(self.alpha * self.k_avg)
        self.F_mean = float(self.F_local.mean())

    def get_state(self):
        return {
            "name": self.name, "N": self.N, "n_bonds": self.n_bonds,
            "sigma": float(self.sigma), "alpha": float(self.alpha),
            "C": float(self.C), "L": float(self.L),
            "el_ratio": float(self.el_ratio), "k_avg": float(self.k_avg),
            "F_mean": float(self.F_mean),
            "n_ltp_total": int(self.n_ltp.sum()),
            "n_ltd_total": int(self.n_ltd.sum()),
            "scaling_events": int(self.scaling_events),
            "glia_events": int(self.glia_events),
            "tau_mean": float(self.tau_per_neuron.mean()),
            "tau_std": float(self.tau_per_neuron.std()),
            "surprise_mean": float(self.surprise_per_neuron.mean())
        }


def run_experiment(name, N, n_steps, tau_cfg, external_pattern=None, seed=42):
    """Run a single experiment and collect metrics."""
    random.seed(seed); np.random.seed(seed)
    region = AdaptiveBrainRegion(name, N, p_connect=0.08, tau_cfg=tau_cfg)
    sigma_traj, el_traj, tau_traj = [], [], []
    for step in range(n_steps):
        ext = None
        if external_pattern == "random":
            ext = np.random.randn(N) * NOISE_LEVEL * 3
        elif external_pattern == "pulsed":
            if step % 50 < 10:
                ext = np.ones(N) * 0.5 + np.random.randn(N) * NOISE_LEVEL
        region.step(step, ext)
        if step % 20 == 0:
            sigma_traj.append(float(region.sigma))
            el_traj.append(float(region.el_ratio))
            tau_traj.append(float(region.tau_per_neuron.mean()))
    final = region.get_state()
    final["sigma_traj"] = sigma_traj
    final["el_traj"] = el_traj
    final["tau_traj"] = tau_traj
    final["tau_history"] = region.tau_history
    return final


if __name__ == "__main__":
    _os.makedirs("simulation/data/v33_results", exist_ok=True)
    N = 60; n_steps = 1500

    configs = {
        "V33-A_baseline": {
            "tau_cfg": TauConfig(enabled=False, tau_base=20.0),
            "label": "Fixed tau=20 (baseline)",
            "ext": "random"
        },
        "V33-B_adaptive": {
            "tau_cfg": TauConfig(enabled=True, tau_base=20.0, alpha_tau=1.0),
            "label": "Adaptive tau (alpha=1.0)",
            "ext": "random"
        },
        "V33-C_adaptive_BCM": {
            "tau_cfg": TauConfig(enabled=True, tau_base=20.0, alpha_tau=1.0),
            "label": "Adaptive tau + BCM + pulsed",
            "ext": "pulsed"
        },
    }

    all_results = {}
    print("=" * 60)
    print("SDI V33 - Adaptive Tau: Surprise-Driven STDP Window")
    print("=" * 60)
    t_start = time.time()

    for exp_id, cfg in configs.items():
        print()
        print("--- " + cfg["label"] + " ---")
        result = run_experiment(exp_id, N, n_steps, cfg["tau_cfg"],
                                external_pattern=cfg["ext"], seed=42)
        all_results[exp_id] = result
        print("  Final sigma: " + str(round(result["sigma"], 3)))
        print("  Final E-L ratio: " + str(round(result["el_ratio"], 3)))
        print("  Final tau mean: " + str(round(result["tau_mean"], 2)))
        print("  Surprise mean: " + str(round(result["surprise_mean"], 3)))
        print("  LTP/LTD: " + str(result["n_ltp_total"]) + " / " + str(result["n_ltd_total"]))

    # V33-D: Alpha sweep
    print()
    print("--- V33-D: Alpha Tau Parameter Sweep ---")
    alphas = [0.2, 0.5, 1.0, 2.0, 5.0]
    sweep_results = {}
    for alpha in alphas:
        tau_cfg = TauConfig(enabled=True, tau_base=20.0, alpha_tau=alpha)
        result = run_experiment("sweep_a" + str(alpha), N, 800,
                                tau_cfg, external_pattern="random", seed=42)
        key = "alpha_" + str(alpha)
        sweep_results[key] = {
            "sigma": float(result["sigma"]),
            "el_ratio": float(result["el_ratio"]),
            "tau_mean": float(result["tau_mean"]),
            "surprise_mean": float(result["surprise_mean"])
        }
        print("  alpha=" + str(alpha) + ": sigma=" + str(round(result["sigma"], 3)) +
              ", el_ratio=" + str(round(result["el_ratio"], 3)) +
              ", tau_mean=" + str(round(result["tau_mean"], 2)))
    all_results["V33-D_sweep"] = sweep_results

    elapsed = time.time() - t_start

    # Save clean results
    clean = {}
    for k, v in all_results.items():
        if k == "V33-D_sweep":
            clean[k] = v
        else:
            clean[k] = {kk: vv for kk, vv in v.items()
                        if kk not in ("sigma_traj", "el_traj", "tau_traj", "tau_history")}

    out_path = "simulation/data/v33_results/v33_adaptive_tau_results.json"
    with open(out_path, "w") as f:
        json.dump(clean, f, indent=2, default=str)

    # Summary
    print()
    print("=" * 60)
    print("V33 Adaptive Tau - FINAL SUMMARY (" + str(round(elapsed, 1)) + "s)")
    print("=" * 60)
    print()
    print("Condition          | sigma | E-L ratio | tau mean")
    print("-" * 55)
    for exp_id in ["V33-A_baseline", "V33-B_adaptive", "V33-C_adaptive_BCM"]:
        r = all_results[exp_id]
        print(exp_id.ljust(20) + "| " + str(round(r["sigma"], 3)).rjust(6) +
              "| " + str(round(r["el_ratio"], 3)).rjust(10) +
              "| " + str(round(r["tau_mean"], 2)).rjust(9))
    print()
    print("Alpha sweep results:")
    for alpha in alphas:
        r = sweep_results["alpha_" + str(alpha)]
        print("  alpha=" + str(alpha) + ": sigma=" + str(round(r["sigma"], 3)) +
              ", el_ratio=" + str(round(r["el_ratio"], 3)))
    print()
    print("Results saved: " + out_path)
    print("=" * 60)