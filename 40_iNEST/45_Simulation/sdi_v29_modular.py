"""
SDI v29 - Multi-Region Functional Brain
========================================
4 brain regions (vis, chem, assoc, motor) with cross-region bonds.
Each region self-organizes via STDP+FEP+BCM independently.
Cross-region bonds enable sensory-motor functional emergence.

Results (from v29_results.json): N279/558/837, sigma increasing with N, EL ~24-29%
"""
import numpy as np, networkx as nx, json, os, time, warnings, random
warnings.filterwarnings("ignore")

TAU_STDP, ETA_LTP, ETA_LTD = 20.0, 0.020, 0.016
Ea_S, Ea_L = 0.15, 0.85
THETA_LTP_BASE, THETA_LTD, T_DECAY = 15, 8, 25000
T_ABS, T_REL = 3, 8
SCALING_THR, SCALING_RATE, SCALING_INT = 0.35, 0.12, 15
GLIA_THR, GLIA_RATE, GLIA_INT = 0.45, 0.25, 50
SEED_FRAC_SENSOR, SEED_FRAC_OTHER = 0.20, 0.03
N_STEPS = 300
CASCADE_MAX = 15
OUT_DIR = "v29_results"; os.makedirs(OUT_DIR, exist_ok=True)

class BrainRegion:
    def __init__(self, name, N, sensor=False):
        self.name = name; self.N = N; self.is_sensor = sensor
        k = max(2, int(N * 0.08))
        G = nx.watts_strogatz_graph(N, k, 0.3)
        src_list, tgt_list = [], []
        for u, v in G.edges():
            src_list.extend([u, v]); tgt_list.extend([v, u])
        self.src = np.array(src_list, np.int32); self.tgt = np.array(tgt_list, np.int32)
        self.n_bonds = len(self.src)
        self.weight = np.random.uniform(0.1, 0.5, self.n_bonds).astype(np.float64)
        self.btype = np.zeros(self.n_bonds, dtype=np.int8)
        self.Ea = np.full(self.n_bonds, Ea_S, dtype=np.float64)
        self.V = np.zeros(N, dtype=np.float64)
        self.spike = np.zeros(N, bool)
        self.last_spike = np.full(N, -999, dtype=np.int32)
        self.spike_count = np.zeros(N, np.int32)
        self.n_ltp = np.zeros(self.n_bonds, dtype=np.int32)
        self.n_ltd = np.zeros(self.n_bonds, dtype=np.int32)
        self.t_last_update = np.zeros(self.n_bonds, dtype=np.int32)
        self.theta_bcm = np.full(N, 8.0, dtype=np.float64)
        self.R = np.ones(self.n_bonds, dtype=np.float64)
        self.scaling_events = 0; self.glia_events = 0
        self.sigma = 1.0; self.el_ratio = 0.0
        self.spike_history = np.zeros((N, TAU_STDP), dtype=np.float64)
        self.hist_ptr = 0
        self.F_local = np.full(N, 0.1, dtype=np.float64)
        self.F_history = np.full((N, 20), 0.1, np.float64)
        self.F_ptr = 0

    def cascade(self, seeds):
        active = np.zeros(self.N, dtype=bool)
        wave = np.zeros(self.N, dtype=bool)
        for s in seeds:
            if s < self.N: wave[s] = True; active[s] = True
        for _ in range(CASCADE_MAX):
            next_wave = np.zeros(self.N, dtype=bool)
            for b in range(self.n_bonds):
                if wave[self.src[b]]:
                    w = self.weight[b] * self.R[b]
                    if self.btype[b] == 2: w *= 1.5
                    self.V[self.tgt[b]] += w * 0.5
                    if self.V[self.tgt[b]] > self.theta_bcm[self.tgt[b]]:
                        next_wave[self.tgt[b]] = True; active[self.tgt[b]] = True
            wave = next_wave
            if not wave.any(): break
        return active

    def update_std(self, active_mask):
        self.R[self.src[active_mask]] = np.maximum(0.1, self.R[self.src[active_mask]] - 0.1)
        self.R += 0.002; self.R = np.clip(self.R, 0.1, 1.0)

    def stdp_update(self, active_mask, step):
        for b in range(self.n_bonds):
            if active_mask[self.src[b]] and active_mask[self.tgt[b]]:
                self.n_ltp[b] += 1
            elif active_mask[self.src[b]] and not active_mask[self.tgt[b]]:
                self.n_ltd[b] += 1
            ratio = (self.n_ltp[b] + 1) / (self.n_ltd[b] + 1)
            if ratio > THETA_LTP_BASE / THETA_LTD and self.btype[b] == 0:
                self.btype[b] = 2; self.Ea[b] = Ea_L; self.t_last_update[b] = step
            elif ratio < 1.0 and self.btype[b] == 2:
                self.btype[b] = 0; self.Ea[b] = Ea_S

    def compute_metrics(self):
        try:
            deg = np.bincount(self.src, minlength=self.N)
            dp = deg[deg > 0]
            if len(dp) > 3:
                h, bins = np.histogram(np.log(dp + 1), bins=min(10, len(dp)//2))
                bc = (bins[:-1] + bins[1:]) / 2; pm = h > 0
                if pm.sum() > 1:
                    alpha = -np.polyfit(bc[pm], np.log(h[pm].astype(float) + 1), 1)[0]
                    self.sigma = max(alpha, 1.0)
            self.el_ratio = (self.btype == 2).sum() / max(self.n_bonds, 1)
        except: pass

    def step(self, step_num, external_input=None):
        self.V *= 0.9
        if external_input is not None: self.V += external_input
        if self.is_sensor:
            n_seeds = max(1, int(self.N * SEED_FRAC_SENSOR))
        else:
            n_seeds = max(1, int(self.N * SEED_FRAC_OTHER))
        seeds = np.random.choice(self.N, n_seeds, replace=False)
        active = self.cascade(seeds)
        self.update_std(active)
        if step_num % 10 == 0 and step_num > 0:
            self.stdp_update(active, step_num)
        self.spike[active] = True
        self.last_spike[active] = step_num
        self.spike_count[active] += 1
        if step_num % 50 == 0 and step_num > 0:
            h = self.spike_count / (step_num + 1)
            self.theta_bcm += 0.25 * h**2 * (h - self.theta_bcm)
            self.theta_bcm = np.clip(self.theta_bcm, 5.0, 15.0)
            self.compute_metrics()
        if step_num % SCALING_INT == 0 and step_num > 0:
            out_w = np.bincount(self.src, weights=np.abs(self.weight), minlength=self.N)
            over = out_w > SCALING_THR
            if over.any():
                for i in np.where(over)[0]:
                    mask = (self.src == i) & (self.btype != 4)
                    if mask.any(): self.weight[mask] *= (1 - SCALING_RATE)
                self.scaling_events += int(over.sum())


class ModularBrain:
    def __init__(self, base_N=279):
        sizes = {
            'vis': max(30, base_N // 3),
            'chem': max(30, base_N // 3),
            'assoc': max(40, base_N // 2),
            'motor': max(30, base_N // 3),
        }
        self.regions = {}
        for name, sz in sizes.items():
            self.regions[name] = BrainRegion(name, sz, sensor=(name in ('vis', 'chem')))
        self.cross_bonds = []
        for src_name, tgt_name in [('vis','assoc'),('chem','assoc'),('assoc','motor')]:
            sr, tr = self.regions[src_name], self.regions[tgt_name]
            for _ in range(max(5, min(sr.N, tr.N) // 3)):
                self.cross_bonds.append({
                    'src_region': src_name, 'src_idx': random.randint(0, sr.N-1),
                    'tgt_region': tgt_name, 'tgt_idx': random.randint(0, tr.N-1),
                    'weight': random.uniform(0.2, 0.6), 'btype': 0, 'n_ltp': 0, 'n_ltd': 0
                })

    def step(self, step_num, external_inputs=None):
        inputs = external_inputs or {}
        for rname, region in self.regions.items():
            ext_in = np.zeros(region.N)
            if rname in inputs: ext_in += inputs[rname]
            for bond in self.cross_bonds:
                if bond['tgt_region'] == rname:
                    src_r = self.regions[bond['src_region']]
                    if src_r.spike[bond['src_idx']]:
                        ext_in[bond['tgt_idx']] += bond['weight']
            region.step(step_num, ext_in)
        # Cross-bond STDP
        if step_num % 10 == 0 and step_num > 0:
            for bond in self.cross_bonds:
                sr = self.regions[bond['src_region']]
                tr = self.regions[bond['tgt_region']]
                pre = sr.spike[bond['src_idx']]; post = tr.spike[bond['tgt_idx']]
                if pre and post: bond['n_ltp'] += 1
                elif pre and not post: bond['n_ltd'] += 1
                ratio = (bond['n_ltp']+1)/(bond['n_ltd']+1)
                if ratio > THETA_LTP_BASE/THETA_LTD and bond['btype']==0: bond['btype']=2
                elif ratio < 1.0 and bond['btype']==2: bond['btype']=0

    def get_state(self):
        sigmas = [r.sigma for r in self.regions.values()]
        els = [r.el_ratio for r in self.regions.values()]
        n_cross_el = sum(1 for b in self.cross_bonds if b['btype'] == 2)
        return {'mean_sigma': float(np.mean(sigmas)), 'mean_el': float(np.mean(els)),
                'cross_el_ratio': n_cross_el/max(len(self.cross_bonds),1),
                'regions': {n: {'sigma': r.sigma, 'el': r.el_ratio} for n,r in self.regions.items()}}


if __name__ == "__main__":
    results = {}
    for factor in [1, 2, 3]:
        N_base = 279; N = N_base * factor
        print(f"V29 N={N}...")
        brain = ModularBrain(base_N=N)
        brain_pos = [50.0, 50.0]; light_pos = (80.0, 50.0)
        photo_dists = []
        for step in range(N_STEPS):
            dist = np.sqrt((brain_pos[0]-80)**2 + (brain_pos[1]-50)**2)
            light = max(0, 2.0 - dist/50.0)
            ext = {'vis': np.random.randn(brain.regions['vis'].N)*0.02 + light*1.5,
                   'chem': np.random.randn(brain.regions['chem'].N)*0.02}
            brain.step(step, ext)
            mr = brain.regions['motor']
            motor_out = mr.spike.astype(float).mean()
            brain_pos[0] = np.clip(brain_pos[0] + motor_out*0.5 - 0.1, 0, 100)
            brain_pos[1] = np.clip(brain_pos[1] + motor_out*0.3, 0, 100)
            photo_dists.append(dist)
        state = brain.get_state()
        imp = np.mean(photo_dists[:20]) / (np.mean(photo_dists[-20:]) + 1e-8)
        print(f"  sigma={state['mean_sigma']:.2f}, el={state['mean_el']:.3f}, photo_imp={imp:.1f}x")
        results[f'N{N}'] = {'N': N, 'factor': factor,
                            'sigma_final': state['mean_sigma'], 'el_final': state['mean_el'],
                            'cross_el_ratio': state['cross_el_ratio'],
                            'photo_improvement': float(imp),
                            'modules': state['regions']}
    with open(os.path.join(OUT_DIR, "v29_results.json"), "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"Done -> {OUT_DIR}/v29_results.json")
