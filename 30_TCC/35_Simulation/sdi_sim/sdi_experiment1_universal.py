#!/usr/bin/env python3
"""
SDI Experiment 1: Cross-Species Universal Validation
验证SDI化合键规则的跨物种普适性
随机初始网络 + 结构化外部刺激 -> 涌现小世界拓扑
"""
import numpy as np
import scipy.sparse as sp
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json, time, sys, os

np.random.seed(42)

# ============================================================
# Species definitions
# ============================================================
SPECIES = {
    'C.elegans': {
        'N': 279, 'k_avg': 16.4,
        'bio': {'sigma': 4.71, 'C': 0.337, 'L': 2.44, 'alpha': 2.32, 'el_ratio': 0.191},
        'target': {'sigma': (4.0, None), 'C': (0.30, None), 'L': (2.0, 3.5), 'alpha': (1.5, 2.5), 'el_ratio': (0.15, 0.28)}
    },
    'Larval_Drosophila': {
        'N': 321, 'k_avg': 51.6,
        'bio': {'sigma': None, 'C': None, 'L': None, 'alpha': None, 'el_ratio': None},
        'target': {'sigma': (3.0, None), 'C': (0.20, None), 'L': (2.0, 4.0), 'alpha': (1.5, 2.5), 'el_ratio': (0.15, 0.28)}
    },
    'Mouse_Cortex': {
        'N': 112, 'k_avg': 58.4,
        'bio': {'sigma': 3.2, 'C': 0.45, 'L': 1.8, 'alpha': 2.1, 'el_ratio': 0.20},
        'target': {'sigma': (2.5, None), 'C': (0.35, None), 'L': (1.5, 3.0), 'alpha': (1.5, 2.5), 'el_ratio': (0.15, 0.28)}
    },
    'Rat_Cortex': {
        'N': 73, 'k_avg': 26.3,
        'bio': {'sigma': 3.0, 'C': 0.42, 'L': 1.9, 'alpha': 2.0, 'el_ratio': 0.18},
        'target': {'sigma': (2.5, None), 'C': (0.30, None), 'L': (1.5, 3.0), 'alpha': (1.5, 2.5), 'el_ratio': (0.15, 0.28)}
    },
    'Macaque_Cortex': {
        'N': 242, 'k_avg': 16.9,
        'bio': {'sigma': 3.8, 'C': 0.55, 'L': 2.3, 'alpha': 2.2, 'el_ratio': 0.20},
        'target': {'sigma': (3.0, None), 'C': (0.40, None), 'L': (2.0, 3.5), 'alpha': (1.5, 2.5), 'el_ratio': (0.15, 0.28)}
    }
}

# ============================================================
# SDI v31 Hyperparameters (validated on C.elegans)
# ============================================================
T_DECAY         = 200
MAX_FIX         = 20
EL_FLOOR        = 40
BOND_CAP        = 1.00
THETA_LTP_BASE  = 25
THETA_LTD       = 8
ETA_LTP         = 0.010
ETA_LTD         = 0.008
TAU_STDP        = 20.0
Ea_S, Ea_L      = 0.15, 0.85
EL_LO, EL_HI   = 0.15, 0.28
TAU_REC         = 150
U_SE_CHEM       = 0.45
U_SE_ELEC       = 0.10
T_ABS, T_REL, REL_SCALE = 3, 8, 0.3
SCALING_INT     = 15
GLIA_INT        = 50
N_STEPS         = 1000
CASCADE_MAX     = 12
K_PATTERNS      = 8   # number of stimulus patterns
T_PATTERN       = 10  # steps per pattern

# ============================================================
# Fast metrics (numpy/scipy only)
# ============================================================
def compute_metrics_fast(src_c, tgt_c, N, avalanches, max_bfs=40, max_depth=5):
    """Compute sigma, C, L, alpha, el_ratio using only numpy/scipy."""
    # Build undirected adjacency
    u_src = np.concatenate([src_c, tgt_c])
    u_tgt = np.concatenate([tgt_c, src_c])
    adj = sp.csr_matrix((np.ones(len(u_src), float), (u_src, u_tgt)), shape=(N, N))

    # Connected components via BFS
    visited = np.zeros(N, bool)
    components = []
    for start in range(N):
        if visited[start]: continue
        comp = [start]; visited[start] = True; qi = 0
        while qi < len(comp):
            u = comp[qi]; qi += 1
            for v in adj.getrow(u).indices:
                if not visited[v]:
                    visited[v] = True; comp.append(v)
        components.append(comp)
    largest_cc = max(components, key=len)
    cc_nodes = np.array(largest_cc)
    cc_map = {n: i for i, n in enumerate(cc_nodes)}
    cc_n = len(cc_nodes)

    if cc_n < 3:
        return 1.0, 0.0, 5.0, None

    # Subgraph adjacency
    cc_idx = np.array(cc_nodes)
    cc_adj = adj.tocsr()[cc_idx][:, cc_idx]

    # Clustering coefficient via A^3 trace
    A = cc_adj.astype(float)
    deg = np.array(A.sum(axis=1)).flatten()
    nz_mask = deg > 1
    if nz_mask.sum() > 0:
        A2 = A @ A
        tri_mat = A.multiply(A2)
        tri = float(tri_mat.sum()) / 2.0
        denom = float(np.sum(deg[nz_mask] * (deg[nz_mask] - 1)))
        C = tri / denom if denom > 0 else 0.0
    else:
        C = 0.0

    # Average path length via BFS sampling
    sample = np.random.choice(cc_n, min(max_bfs, cc_n), replace=False)
    all_depths = []
    A_csr = cc_adj.tocsr()
    for s in sample:
        visited_bfs = np.zeros(cc_n, bool); visited_bfs[s] = True
        current = [s]; depth = 0
        while current and depth < max_depth:
            depth += 1; nxt = []
            for u in current:
                for v in A_csr.getrow(u).indices:
                    if not visited_bfs[v]:
                        visited_bfs[v] = True; nxt.append(v)
                        all_depths.append(depth)
            current = nxt
    if all_depths:
        n_reached = len(all_depths)
        if n_reached < cc_n * 0.6:
            total = sum(all_depths) + (cc_n - n_reached) * 2 * max_depth
            L = total / cc_n
        else:
            L = float(np.mean(all_depths))
    else:
        L = max_depth * 2.0

    # Small-worldness sigma
    m = int(cc_adj.nnz)
    p = 2.0 * m / (cc_n * (cc_n - 1)) if cc_n > 1 else 1.0
    Cr = max(p, 1e-6)
    Lr = np.log(cc_n) / np.log(max(2, cc_n * p))
    sigma = (C / Cr) / (L / max(Lr, 0.1)) if L > 0 else 0.0

    # Power-law alpha from avalanche sizes
    s_arr = np.array([x for x in avalanches if x >= 2])
    alpha = None
    if len(s_arr) >= 60:
        xm = max(2, int(np.percentile(s_arr, 10)))
        x = s_arr[s_arr >= xm]
        if len(x) >= 20:
            alpha = float(1 + len(x) / np.sum(np.log(x / (xm - 0.5))))

    return sigma, C, L, alpha


# ============================================================
# SDI Network (species-generic)
# ============================================================
class SDINetwork:
    def __init__(self, N, k_avg, species_name):
        self.N = N
        self.t = 0
        self.species = species_name
        self.theta = THETA_LTP_BASE
        self.scl_e = 0; self.glia_e = 0
        self.ava = []

        # ---- Random Erdos-Renyi initialization (NO connectome!) ----
        p_er = min(0.99, k_avg / (N - 1))
        n_edges = int(p_er * N * (N - 1))
        print(f'  [init] {species_name}: N={N}, k_avg={k_avg:.1f}, p_er={p_er:.4f}, n_edges~{n_edges}')

        # Generate random directed edges
        rng = np.random.default_rng(42 + hash(species_name) % 1000)
        src_list, tgt_list = [], []
        for i in range(N):
            targets = rng.integers(0, N, size=max(1, int(k_avg)))
            for t in targets:
                if t != i:
                    src_list.append(i); tgt_list.append(int(t))
        # Deduplicate
        pairs = set(zip(src_list, tgt_list))
        src_arr = np.array([p[0] for p in pairs], np.int32)
        tgt_arr = np.array([p[1] for p in pairs], np.int32)
        ne = len(src_arr)
        w_arr = rng.uniform(0.05, 0.3, ne).astype(np.float64)
        bt_arr = np.zeros(ne, np.int8)   # all E-S initially
        ie_arr = np.zeros(ne, bool)

        # Electric synapses ~5%
        n_elec = max(1, int(ne * 0.05))
        e_src = rng.integers(0, N, n_elec, dtype=np.int32)
        e_tgt = rng.integers(0, N, n_elec, dtype=np.int32)
        e_w   = np.full(n_elec, 0.3, np.float64)
        e_bt  = np.full(n_elec, 4, np.int8)
        e_ie  = np.full(n_elec, True, bool)

        self.src = np.concatenate([src_arr, e_src])
        self.tgt = np.concatenate([tgt_arr, e_tgt])
        self.w   = np.concatenate([w_arr, e_w])
        self.bt  = np.concatenate([bt_arr, e_bt])
        self.ie  = np.concatenate([ie_arr, e_ie])

        self.Ea = np.where(self.ie, 0.5, Ea_S)
        self.n_ltp = np.zeros(len(self.src), np.int32)
        self.n_ltd = np.zeros(len(self.src), np.int32)
        self.la = np.full(len(self.src), -99999, np.int32)
        self.R = np.where(self.ie, 0.95, 1.0)
        self.lf = np.full(N, -99999, np.int32)
        self.ac = np.zeros(N, np.int32)

        # ---- Stimulus patterns ----
        # 20% of nodes are "sensory"
        n_sensory = max(1, int(N * 0.20))
        all_idx = np.arange(N)
        rng2 = np.random.default_rng(99 + hash(species_name) % 1000)
        # K_PATTERNS non-overlapping subsets of sensory pool
        sensory_pool = rng2.choice(N, n_sensory, replace=False)
        pat_size = max(1, n_sensory // K_PATTERNS)
        self.patterns = []
        for k in range(K_PATTERNS):
            start_i = k * pat_size
            end_i = min(start_i + pat_size, n_sensory)
            self.patterns.append(sensory_pool[start_i:end_i])
        self.other_idx = np.arange(N, dtype=np.int32)
        self.current_pattern = 0
        self.pattern_step = 0

        self._rebuild()
        print(f'  [init] chem={int((~self.ie).sum())} elec={int(self.ie.sum())}')

    def _rebuild(self):
        cm = ~self.ie
        sc = np.where(np.isin(self.bt[cm], [0, 2]), 1.0, -0.25)
        wc = self.w[cm] * self.R[cm] * sc
        em = self.ie; we = self.w[em] * self.R[em] * 0.5
        self.W = sp.csr_matrix(
            (np.concatenate([wc, we]),
             (np.concatenate([self.src[cm], self.src[em]]),
              np.concatenate([self.tgt[cm], self.tgt[em]]))),
            shape=(self.N, self.N))

    def _get_seeds(self):
        """Structured stimulus: cycle through K_PATTERNS patterns."""
        pat = self.patterns[self.current_pattern % K_PATTERNS]
        self.pattern_step += 1
        if self.pattern_step >= T_PATTERN:
            self.pattern_step = 0
            # 10% chance of random jump, else sequential
            if np.random.random() < 0.10:
                self.current_pattern = np.random.randint(0, K_PATTERNS)
            else:
                self.current_pattern = (self.current_pattern + 1) % K_PATTERNS
        # Add small background noise (5% random nodes)
        n_noise = max(1, int(self.N * 0.05))
        noise = np.random.choice(self.other_idx, n_noise, replace=False).tolist()
        seeds = list(set(pat.tolist() + noise))
        return seeds

    def cascade(self, seeds):
        seeds = [s for s in seeds if self.t - self.lf[s] >= T_ABS]
        if not seeds: self.ava.append(0); return np.zeros(self.N, bool)
        a = np.zeros(self.N, bool); a[seeds] = True; aa = a.copy()
        for _ in range(CASCADE_MAX):
            sig = self.W @ a.astype(float)
            ratio = aa.sum() / max(1, self.N); inh = max(0, (ratio - 0.18) * 4.5)
            dt = self.t - self.lf; rs = np.ones(self.N)
            rs[dt < T_ABS] = 0.0; rs[(dt >= T_ABS) & (dt < T_REL)] = REL_SCALE
            p = np.clip(sig * (1 - inh) * rs, 0, 1)
            nw = (p > np.random.random(self.N)) & (~aa)
            if not nw.any(): break
            self.lf[nw] = self.t; self.ac[nw] += 1; aa |= nw; a = nw
        self.ava.append(int(aa.sum()))
        return aa

    def stdp(self, am):
        nd = np.where(am)[0]
        if len(nd) == 0: return
        em = (~self.ie) & (np.isin(self.src, nd) | np.isin(self.tgt, nd))
        if not em.any(): return
        idx = np.where(em)[0]
        dt = self.lf[self.src[idx]] - self.lf[self.tgt[idx]]
        lp = (dt > 0) & (dt < 200)
        if lp.any():
            self.w[idx[lp]] = np.clip(self.w[idx[lp]] + ETA_LTP * np.exp(-dt[lp] / TAU_STDP), 0, 1)
            self.n_ltp[idx[lp]] += 1
        ld = (dt < 0) & (dt > -200)
        if ld.any():
            self.w[idx[ld]] = np.clip(self.w[idx[ld]] - ETA_LTD * np.exp(dt[ld] / TAU_STDP), 0, 1)
            self.n_ltd[idx[ld]] += 1
        self.la[idx] = self.t

    def el_r(self):
        cm = ~self.ie; nb = cm.sum()
        return float(np.sum((self.bt == 2) & cm)) / max(1, nb)

    def apply_rules(self):
        er = self.el_r()
        if er > EL_HI: self.theta = min(100, int(THETA_LTP_BASE * (1 + (er - EL_HI) * 12)))
        elif er < EL_LO: self.theta = max(5, int(THETA_LTP_BASE * (1 - (EL_LO - er) * 6)))
        else: self.theta = THETA_LTP_BASE
        cm = ~self.ie
        fx = cm & (self.bt == 0) & (self.n_ltp >= self.theta)
        if fx.sum() > MAX_FIX:
            fi = np.where(fx)[0]; np.random.shuffle(fi)
            f = np.zeros(len(self.src), bool); f[fi[:MAX_FIX]] = True
        else:
            f = fx
        self.bt[f] = 2; self.Ea[f] = Ea_L; self.n_ltp[f] = 0
        dc = cm & (self.bt == 2) & (self.t - self.la > T_DECAY)
        self.bt[dc] = 0; self.Ea[dc] = Ea_S
        ct = cm & (((self.bt == 1) & (self.n_ltd >= THETA_LTD)) |
                   ((self.bt == 0) & (self.w < 0.01) & (self.t - self.la > 1500)))
        k = ~ct
        for a_ in ('src','tgt','bt','w','n_ltp','n_ltd','la','Ea','R','ie'):
            setattr(self, a_, getattr(self, a_)[k])
        # Sprouting
        deg = np.bincount(self.src[~self.ie].astype(int), minlength=self.N)
        low = np.where(deg < 6)[0]
        if len(low) > 0:
            nn = min(len(low) * 2, int(60 * BOND_CAP))
            ns = np.random.choice(low, nn); nt = np.random.randint(0, self.N, nn)
            v = ns != nt; ns, nt = ns[v], nt[v]; na = len(ns)
            ex = np.random.random(na) < 0.8
            for a_, val in [
                ('src', np.concatenate([self.src, ns.astype(np.int32)])),
                ('tgt', np.concatenate([self.tgt, nt.astype(np.int32)])),
                ('bt', np.concatenate([self.bt, np.where(ex, 0, 1).astype(np.int8)])),
                ('w', np.concatenate([self.w, np.where(ex,
                    np.random.uniform(0.1, 0.4, na), np.random.uniform(0.03, 0.12, na))])),
                ('n_ltp', np.concatenate([self.n_ltp, np.zeros(na, np.int32)])),
                ('n_ltd', np.concatenate([self.n_ltd, np.zeros(na, np.int32)])),
                ('la', np.concatenate([self.la, np.full(na, self.t, np.int32)])),
                ('Ea', np.concatenate([self.Ea, np.full(na, Ea_S)])),
                ('R', np.concatenate([self.R, np.ones(na)])),
                ('ie', np.concatenate([self.ie, np.zeros(na, bool)]))]:
                setattr(self, a_, val)
        return er

    def run(self):
        logs = {'step': [], 'sigma': [], 'C': [], 'L': [], 'alpha': [], 'el_ratio': []}
        for step in range(N_STEPS):
            self.t = step
            seeds = self._get_seeds()
            for _ in range(3):
                am = self.cascade(seeds); self.stdp(am)
            self._rebuild()
            self.R += (1 - self.R) / TAU_REC
            an = np.where(self.lf == self.t)[0]
            if len(an) > 0:
                sa = np.isin(self.src, an); cm = ~self.ie
                self.R[sa & cm] = np.clip(self.R[sa & cm] - U_SE_CHEM * self.R[sa & cm], 0.05, 1.0)
                self.R[sa & self.ie] = np.clip(self.R[sa & self.ie] - U_SE_ELEC * self.R[sa & self.ie], 0.05, 1.0)
            if step % SCALING_INT == 0 and step > 0:
                er = self.el_r()
                if er >= 0.35:
                    hot = np.where(self.ac >= np.percentile(self.ac, 80))[0]
                    if len(hot) > 0:
                        cm = ~self.ie; sm = cm & (self.bt == 2) & (np.isin(self.src, hot) | np.isin(self.tgt, hot))
                        if sm.sum() > 0:
                            self.w[sm] *= 0.88; dg = sm & (self.w < 0.08)
                            self.bt[dg] = 0; self.Ea[dg] = Ea_S; self.scl_e += 1
            if step % GLIA_INT == 0 and step > 0:
                er = self.el_r()
                if er >= 0.45:
                    cm = ~self.ie; eb_ = np.where(cm & (self.bt == 2))[0]
                    if len(eb_) > 0:
                        nd = max(1, int(len(eb_) * 0.25))
                        top = eb_[np.argsort(self.w[eb_])[::-1][:nd]]
                        self.bt[top] = 0; self.Ea[top] = Ea_S; self.n_ltp[top] = 0; self.glia_e += 1
            if step % 15 == 0:
                self.apply_rules(); self._rebuild()
            if step % 100 == 0:
                cm = ~self.ie; er = self.el_r()
                sig, C, L, al = compute_metrics_fast(
                    self.src[cm], self.tgt[cm], self.N, list(self.ava), max_bfs=30, max_depth=5)
                logs['step'].append(step); logs['sigma'].append(sig)
                logs['C'].append(C); logs['L'].append(L)
                logs['alpha'].append(al or 0); logs['el_ratio'].append(er)
                a_str = '%.3f' % al if al else 'N/A'
                print(f'  step {step:4d}: sigma={sig:.3f} C={C:.3f} L={L:.3f} alpha={a_str} EL={er:.1%}')
                sys.stdout.flush()
        return logs


# ============================================================
# MAIN: Run all species
# ============================================================
def check_pass(val, lo, hi):
    if val is None: return False
    if lo is not None and val < lo: return False
    if hi is not None and val > hi: return False
    return True

all_results = {}
t0_total = time.time()

for sp_name, sp_info in SPECIES.items():
    print('\n' + '='*60)
    print(f'SPECIES: {sp_name}  (N={sp_info["N"]}, k_avg={sp_info["k_avg"]})')
    print('='*60)
    t0 = time.time()
    net = SDINetwork(sp_info['N'], sp_info['k_avg'], sp_name)
    logs = net.run()

    # Final metrics
    cm = ~net.ie; er = net.el_r()
    sf, Cf, Lf, af = compute_metrics_fast(
        net.src[cm], net.tgt[cm], net.N, list(net.ava), max_bfs=40, max_depth=5)

    target = sp_info['target']
    passes = {
        'sigma': check_pass(sf, *target['sigma']),
        'C':     check_pass(Cf, *target['C']),
        'L':     check_pass(Lf, *target['L']),
        'alpha': check_pass(af, *target['alpha']),
        'el_ratio': check_pass(er, *target['el_ratio'])
    }
    n_pass = sum(passes.values())

    print(f'\n--- {sp_name} FINAL ({time.time()-t0:.1f}s) ---')
    print(f'  sigma={sf:.3f}  PASS={passes["sigma"]}  (target>={target["sigma"][0]})')
    print(f'  C={Cf:.3f}  PASS={passes["C"]}  (target>={target["C"][0]})')
    print(f'  L={Lf:.3f}  PASS={passes["L"]}  (target {target["L"]})')
    a_s = '%.3f' % af if af else 'N/A'
    print(f'  alpha={a_s}  PASS={passes["alpha"]}  (target {target["alpha"]})')
    print(f'  EL={er:.1%}  PASS={passes["el_ratio"]}  (target {target["el_ratio"]})')
    print(f'  SCORE: {n_pass}/5')

    all_results[sp_name] = {
        'N': sp_info['N'], 'k_avg': sp_info['k_avg'],
        'sigma': sf, 'C': Cf, 'L': Lf, 'alpha': af, 'el_ratio': er,
        'passes': passes, 'score': n_pass,
        'logs': logs, 'time': time.time() - t0
    }
    sys.stdout.flush()

print('\n' + '='*60)
print(f'ALL SPECIES DONE. Total time: {time.time()-t0_total:.1f}s')
print('='*60)
for sp_name, r in all_results.items():
    print(f'  {sp_name}: {r["score"]}/5')

# ============================================================
# Save results
# ============================================================
save_results = {}
for sp, r in all_results.items():
    save_results[sp] = {k: v for k, v in r.items() if k != 'logs'}
    save_results[sp]['logs'] = r['logs']

with open('/home/work/.openclaw/workspace/sdi_sim/experiment1_results.json', 'w') as f:
    json.dump(save_results, f, indent=2, default=lambda x: None if x is None else x)
print('Results saved.')

# ============================================================
# Plot: 5 species x 5 metrics convergence
# ============================================================
metrics = ['sigma', 'C', 'L', 'alpha', 'el_ratio']
metric_labels = ['sigma (small-worldness)', 'C (clustering)', 'L (path length)',
                 'alpha (power-law)', 'E-L ratio']
target_lines = {
    'sigma': {'lo': 4.0, 'hi': None},
    'C': {'lo': 0.30, 'hi': None},
    'L': {'lo': 2.0, 'hi': 3.5},
    'alpha': {'lo': 1.5, 'hi': 2.5},
    'el_ratio': {'lo': 0.15, 'hi': 0.28}
}
colors = {'C.elegans': 'blue', 'Larval_Drosophila': 'orange',
          'Mouse_Cortex': 'green', 'Rat_Cortex': 'red', 'Macaque_Cortex': 'purple'}

fig, axes = plt.subplots(5, 5, figsize=(20, 20))
fig.suptitle('SDI Experiment 1: Cross-Species Universal Validation\n'
             'Random Init → Structured Stimuli → Emergent Small-World Topology',
             fontsize=14, fontweight='bold')

for i, metric in enumerate(metrics):
    for j, (sp_name, r) in enumerate(all_results.items()):
        ax = axes[i][j]
        logs = r['logs']
        st = logs['step']
        vals = logs[metric]
        ax.plot(st, vals, color=colors[sp_name], lw=2, marker='o', ms=4)

        # Target lines
        tl = target_lines[metric]
        if tl['lo'] is not None:
            ax.axhline(tl['lo'], color='green', ls='--', lw=1.5, alpha=0.7, label='target lo')
        if tl['hi'] is not None:
            ax.axhline(tl['hi'], color='red', ls='--', lw=1.5, alpha=0.7, label='target hi')

        # Bio reference
        bio_val = SPECIES[sp_name]['bio'].get(metric)
        if bio_val is not None:
            ax.axhline(bio_val, color='gray', ls=':', lw=1.5, alpha=0.8)

        passed = r['passes'].get(metric, False)
        title = f'{sp_name[:12]}\n{metric_labels[i][:18]}'
        ax.set_title(title, fontsize=7, color='darkgreen' if passed else 'darkred')
        ax.grid(True, alpha=0.3); ax.tick_params(labelsize=6)
        if i == 4:
            final_val = vals[-1] if vals else 0
            ax.set_xlabel(f'Steps (final={final_val:.2f})', fontsize=6)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('/home/work/.openclaw/workspace/sdi_sim/experiment1_convergence.png', dpi=120, bbox_inches='tight')
plt.close()
print('Plot saved: experiment1_convergence.png')
print('DONE')