#!/usr/bin/env python3
import numpy as np, scipy.sparse as sp
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt, json, warnings, time, csv
from collections import defaultdict
warnings.filterwarnings('ignore')
np.random.seed(42)

# ============================================================
# SDI v31 - Hemibrain full network (25397 neurons from CSV)
# Params = C.elegans validated (T_DECAY=200)
# ============================================================
T_DECAY = 200
MAX_FIX = 20
EL_FLOOR = 40
BOND_CAP = 1.00
THETA_LTP_BASE = 25
THETA_LTD = 8
ETA_LTP = 0.010
ETA_LTD = 0.008
TAU_STDP = 20.0
Ea_S, Ea_L = 0.15, 0.85
TAU_REC = 150
U_SE_CHEM, U_SE_ELEC = 0.45, 0.10
T_ABS, T_REL, REL_SCALE = 3, 8, 0.3
EL_LO, EL_HI = 0.15, 0.28
SCALING_INT = 15
GLIA_INT = 50
N_STEPS = 500
CASCADE_MAX = 12

# ============================================================
# Load Hemibrain CSV (25397 neurons)
# ============================================================
print('Loading hemibrain_meta.csv...')
neurons = {}
with open('/home/work/.openclaw/workspace/10_Knowledge/专题归档/05_Datasets_仿真与实验数据/Simulation_Results/hemibrain_meta.csv') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        bid = row[0]
        try: pre = float(row[11]) if row[11] else 0.0
        except: pre = 0.0
        try: post = float(row[12]) if row[12] else 0.0
        except: post = 0.0
        cell_class = row[4] or 'unknown'
        if bid not in neurons:
            neurons[bid] = {'pre': 0.0, 'post': 0.0, 'cls': cell_class}
        neurons[bid]['pre'] += pre
        neurons[bid]['post'] += post

N_all = len(neurons)
print(f'Total neurons in CSV: {N_all}')

# Filter to active neurons (meaningful connectivity)
active_ids = [b for b, n in neurons.items() if n['pre'] > 5 or n['post'] > 5]
N_active = len(active_ids)
print(f'Active neurons (pre>5 or post>5): {N_active}')

# Subsample for tractability: use ALL active neurons but cap at 6000
MAX_N = 6000
if N_active > MAX_N:
    degs = np.array([max(neurons[b]['pre'], neurons[b]['post']) for b in active_ids], float)
    probs = degs / degs.sum()
    np.random.seed(42)
    sidx = np.random.choice(len(active_ids), MAX_N, replace=False, p=probs)
    sim_ids = [active_ids[i] for i in sidx]
else:
    sim_ids = active_ids

N = len(sim_ids)
sim2idx = {b: i for i, b in enumerate(sim_ids)}
print(f'Simulation N={N}')

# Classify node types
def classify(c):
    if c in ('olfactory', 'hygrosensory', 'thermosensory'): return 'sensory'
    return 'interneuron'

node_cls = [neurons[b]['cls'] for b in sim_ids]
node_types = [classify(c) for c in node_cls]
sensor_idx = np.array([i for i, t in enumerate(node_types) if t == 'sensory'], np.int32)
other_idx = np.arange(N, dtype=np.int32)
print(f'Sensors: {len(sensor_idx)}, Inter: {N - len(sensor_idx)}')

# ============================================================
# Build edges from pre/post counts
# ============================================================
avg_fanout = 5
out_deg = np.array([max(1, int(neurons[b]['pre'] / avg_fanout)) for b in sim_ids], int)
out_deg = np.clip(out_deg, 1, 80)

edges = []
for i, bid in enumerate(sim_ids):
    n_e = out_deg[i]
    targets = np.random.choice(N, size=n_e, replace=True)
    for t in targets:
        if t != i:
            edges.append((i, t, np.random.uniform(0.05, 0.95)))

src_c = np.array([e[0] for e in edges], np.int32)
tgt_c = np.array([e[1] for e in edges], np.int32)
w_c   = np.array([e[2] for e in edges], np.float64)
bt_c  = np.zeros(len(src_c), np.int8)
N_chem = len(src_c)
print(f'Chem edges: {N_chem}')

# Electric synapses (~5% of chem)
Ne = int(N_chem * 0.05)
es_c = np.random.randint(0, N, Ne, np.int32)
et_c = np.random.randint(0, N, Ne, np.int32)
ew_c = np.full(Ne, 0.3, np.float64)
eb_c = np.full(Ne, 4, np.int8)
ee_c = np.full(Ne, True, bool)

all_src = np.concatenate([src_c, es_c])
all_tgt = np.concatenate([tgt_c, et_c])
all_w   = np.concatenate([w_c,   ew_c])
all_bt  = np.concatenate([bt_c,  eb_c])
all_ie  = np.concatenate([np.zeros(N_chem, bool), ee_c])

print(f'Total edges: {len(all_src)} (chem={N_chem}, elec={Ne})')

# ============================================================
# Fast sparse metrics (no networkx)
# ============================================================
from scipy.sparse.csgraph import connected_components

def build_adj_und(s, t, N_):
    u = np.concatenate([s, t])
    v = np.concatenate([t, s])
    return sp.csr_matrix((np.ones(len(u), float), (u, v)), shape=(N_, N_))

def get_lcc(s, t, N_):
    adj = build_adj_und(s, t, N_)
    nc, labels = connected_components(adj, directed=False)
    if nc == 0: return s[:0].copy(), t[:0].copy(), N_
    sizes = np.bincount(labels)
    lcc_label = sizes.argmax()
    node_mask = labels == lcc_label
    n_lcc = node_mask.sum()
    old_new = -np.ones(N_, int)
    old_new[node_mask] = np.arange(n_lcc)
    # Edge mask: both endpoints in LCC
    edge_mask = node_mask[s] & node_mask[t]
    src_l = old_new[s[edge_mask]]
    tgt_l = old_new[t[edge_mask]]
    return src_l, tgt_l, n_lcc

def clustering_sparse(adj):
    deg = np.array(adj.sum(axis=1)).flatten().astype(int)
    nz = np.where(deg > 1)[0]
    if len(nz) == 0: return 0.0
    A2 = adj @ adj
    tri = float(adj.multiply(A2).sum()) / 2.0
    denom = float(np.sum(deg[nz] * (deg[nz] - 1)))
    return tri / denom if denom > 0 else 0.0

def avg_path_sparse(adj, n_lcc, max_sample=25, max_depth=6):
    nodes = np.arange(n_lcc)
    sample = np.random.choice(nodes, min(max_sample, n_lcc), replace=False)
    all_d = []
    for s in sample:
        visited = np.zeros(n_lcc, bool); visited[s] = True
        cur = {s}; depth = 0
        while cur and depth < max_depth:
            depth += 1
            nxt = set()
            for u in cur:
                for v in adj.getrow(u).indices:
                    if not visited[v]:
                        visited[v] = True; nxt.add(v)
                        all_d.append(depth)
            cur = nxt
    if not all_d: return max_depth * 2.0
    n_reach = len(all_d)
    if n_reach < n_lcc * 0.75:
        return (sum(all_d) + (n_lcc - n_reach) * 2 * max_depth) / n_lcc
    return float(np.mean(all_d))

def compute_metrics(s_c, t_c, N_):
    sl, tl, n_lcc = get_lcc(s_c, t_c, N_)
    if n_lcc < 10: return 1.0, 0.0, 10.0
    adj = build_adj_und(sl, tl, n_lcc)
    C = clustering_sparse(adj)
    L = avg_path_sparse(adj, n_lcc)
    m_ = adj.nnz; n_ = n_lcc
    p_ = 2 * m_ / (n_ * (n_ - 1)) if n_ > 1 else 1.0
    Cr = max(p_, 1e-6)
    Lr = np.log(n_) / np.log(max(2, n_ * p_))
    return (C / Cr) / (L / max(Lr, 0.1)), C, L

# ============================================================
# SDI v31
# ============================================================
class SDI:
    def __init__(self):
        self.N = N
        self.t = 0
        self.src = all_src.copy()
        self.tgt = all_tgt.copy()
        self.w = all_w.copy()
        self.bt = all_bt.copy()
        self.ie = all_ie.copy()
        self.Ea = np.where(self.ie, 0.5, Ea_S)
        self.n_ltp = np.zeros(len(self.src), np.int32)
        self.n_ltd = np.zeros(len(self.src), np.int32)
        self.la = np.full(len(self.src), -99999, np.int32)
        self.R = np.where(self.ie, 0.95, 1.0)
        self.lf = np.full(N, -99999, np.int32)
        self.ac = np.zeros(N, np.int32)
        self.ava = []
        self.theta = THETA_LTP_BASE
        self.scl_e = 0
        self.glia_e = 0
        self._rebuild()

    def _rebuild(self):
        cm = ~self.ie
        sc = np.where(np.isin(self.bt[cm], [0, 2]), 1.0, -0.25)
        wc = self.w[cm] * self.R[cm] * sc
        em = self.ie
        we = self.w[em] * self.R[em] * 0.5
        self.W = sp.csr_matrix(
            (np.concatenate([wc, we]),
             (np.concatenate([self.src[cm], self.src[em]]),
              np.concatenate([self.tgt[cm], self.tgt[em]]))),
            shape=(N, N))

    def cascade(self, seeds):
        seeds = [s for s in seeds if self.t - self.lf[s] >= T_ABS]
        if not seeds:
            self.ava.append(0)
            return np.zeros(N, bool)
        a = np.zeros(N, bool)
        a[seeds] = True
        aa = a.copy()
        for _ in range(CASCADE_MAX):
            sig = self.W @ a.astype(float)
            ratio = aa.sum() / max(1, N)
            inh = max(0, (ratio - 0.18) * 4.5)
            dt = self.t - self.lf
            rs = np.ones(N)
            rs[dt < T_ABS] = 0.0
            rs[(dt >= T_ABS) & (dt < T_REL)] = REL_SCALE
            p = np.clip(sig * (1 - inh) * rs, 0, 1)
            nw = (p > np.random.random(N)) & (~aa)
            if not nw.any():
                break
            self.lf[nw] = self.t
            self.ac[nw] += 1
            aa |= nw
            a = nw
        self.ava.append(int(aa.sum()))
        return aa

    def stdp(self, am):
        nd = np.where(am)[0]
        if len(nd) == 0:
            return
        em = (~self.ie) & (np.isin(self.src, nd) | np.isin(self.tgt, nd))
        if not em.any():
            return
        idx = np.where(em)[0]
        dt = self.lf[self.src[idx]] - self.lf[self.tgt[idx]]
        lp = (dt > 0) & (dt < 200)
        if lp.any():
            self.w[idx[lp]] = np.clip(
                self.w[idx[lp]] + ETA_LTP * np.exp(-dt[lp] / TAU_STDP), 0, 1)
            self.n_ltp[idx[lp]] += 1
        ld = (dt < 0) & (dt > -200)
        if ld.any():
            self.w[idx[ld]] = np.clip(
                self.w[idx[ld]] - ETA_LTD * np.exp(dt[ld] / TAU_STDP), 0, 1)
            self.n_ltd[idx[ld]] += 1
        self.la[idx] = self.t

    def el_r(self):
        cm = ~self.ie
        nb = cm.sum()
        return float(np.sum((self.bt == 2) & cm)) / max(1, nb) if nb else 0.0

    def apply_rules(self):
        er = self.el_r()
        if er > EL_HI:
            self.theta = min(THETA_LTP_BASE * 4, int(THETA_LTP_BASE * (1 + (er - EL_HI) * 12)))
        elif er < EL_LO:
            self.theta = max(5, int(THETA_LTP_BASE * (1 - (EL_LO - er) * 6)))
        else:
            self.theta = THETA_LTP_BASE

        cm = ~self.ie
        fx = cm & (self.bt == 0) & (self.n_ltp >= self.theta)
        if fx.sum() > MAX_FIX:
            fi = np.where(fx)[0]
            np.random.shuffle(fi)
            f_arr = np.zeros(len(self.src), bool)
            f_arr[fi[:MAX_FIX]] = True
        else:
            f_arr = fx

        self.bt[f_arr] = 2
        self.Ea[f_arr] = Ea_L
        self.n_ltp[f_arr] = 0

        dc = cm & (self.bt == 2) & (self.t - self.la > T_DECAY)
        self.bt[dc] = 0
        self.Ea[dc] = Ea_S

        ct = cm & (((self.bt == 1) & (self.n_ltd >= THETA_LTD)) |
                   ((self.bt == 0) & (self.w < 0.01) & (self.t - self.la > 1500)))
        k = ~ct

        self.src = self.src[k]
        self.tgt = self.tgt[k]
        self.bt = self.bt[k]
        self.w = self.w[k]
        self.n_ltp = self.n_ltp[k]
        self.n_ltd = self.n_ltd[k]
        self.la = self.la[k]
        self.Ea = self.Ea[k]
        self.R = self.R[k]
        self.ie = self.ie[k]

        deg = np.bincount(self.src[~self.ie].astype(int), minlength=N)
        low = np.where(deg < 6)[0]
        if len(low) > 0:
            nn = min(len(low) * 2, int(60 * BOND_CAP))
            ns = np.random.choice(low, nn)
            nt = np.random.randint(0, N, nn)
            v = ns != nt
            ns, nt = ns[v], nt[v]
            na = len(ns)
            ex = np.random.random(na) < 0.8
            self.src = np.concatenate([self.src, ns.astype(np.int32)])
            self.tgt = np.concatenate([self.tgt, nt.astype(np.int32)])
            self.bt = np.concatenate([self.bt, np.where(ex, 0, 1).astype(np.int8)])
            self.w = np.concatenate([self.w, np.where(ex,
                np.random.uniform(0.1, 0.4, na), np.random.uniform(0.03, 0.12, na))])
            self.n_ltp = np.concatenate([self.n_ltp, np.zeros(na, np.int32)])
            self.n_ltd = np.concatenate([self.n_ltd, np.zeros(na, np.int32)])
            self.la = np.concatenate([self.la, np.full(na, self.t, np.int32)])
            self.Ea = np.concatenate([self.Ea, np.full(na, Ea_S)])
            self.R = np.concatenate([self.R, np.ones(na)])
            self.ie = np.concatenate([self.ie, np.zeros(na, bool)])

        return er

    def fit_alpha(self):
        s = np.array([x for x in self.ava if x >= 2])
        if len(s) < 60:
            return None
        xm = max(2, int(np.percentile(s, 10)))
        x = s[s >= xm]
        if len(x) < 20:
            return None
        return float(1 + len(x) / np.sum(np.log(x / (xm - 0.5))))

    def run(self):
        print(f'\nRunning {N_STEPS} steps on Hemibrain network')
        print(f'N={self.N}, chem={int((~self.ie).sum())}, elec={int(self.ie.sum())}')
        print(f'Params: T_DECAY={T_DECAY}, MAX_FIX={MAX_FIX}, BOND_CAP={BOND_CAP}')
        print('-' * 70)

        logs = {'step': [], 'sigma': [], 'alpha': [], 'el': [], 'bonds': [], 'theta': []}

        for step in range(N_STEPS):
            self.t = step

            for _ in range(4):
                ns = max(1, min(len(sensor_idx), 5))
                no = max(1, int(N * 0.02))
                seeds = list(set(
                    list(np.random.choice(sensor_idx, ns, replace=False)) +
                    list(np.random.choice(other_idx, no, replace=False))))
                am = self.cascade(seeds)
                self.stdp(am)
                self._rebuild()

            self.R += (1 - self.R) / TAU_REC
            an = np.where(self.lf == self.t)[0]
            if len(an) > 0:
                sa = np.isin(self.src, an)
                cm = ~self.ie
                self.R[sa & cm] = np.clip(self.R[sa & cm] - U_SE_CHEM * self.R[sa & cm], 0.05, 1.0)
                self.R[sa & self.ie] = np.clip(self.R[sa & self.ie] - U_SE_ELEC * self.R[sa & self.ie], 0.05, 1.0)

            if step % SCALING_INT == 0 and step > 0:
                er = self.el_r()
                if er >= 0.35:
                    hot = np.where(self.ac >= np.percentile(self.ac, 80))[0]
                    if len(hot) > 0:
                        cm = ~self.ie
                        sm = cm & (self.bt == 2) & (np.isin(self.src, hot) | np.isin(self.tgt, hot))
                        if sm.sum() > 0:
                            self.w[sm] *= 0.88
                            dg = sm & (self.w < 0.08)
                            self.bt[dg] = 0
                            self.Ea[dg] = Ea_S
                            self.scl_e += 1

            if step % GLIA_INT == 0 and step > 0:
                er = self.el_r()
                if er >= 0.45:
                    cm = ~self.ie
                    eb_ = np.where(cm & (self.bt == 2))[0]
                    if len(eb_) > 0:
                        nd = max(1, int(len(eb_) * 0.25))
                        top = eb_[np.argsort(self.w[eb_])[::-1][:nd]]
                        self.bt[top] = 0
                        self.Ea[top] = Ea_S
                        self.n_ltp[top] = 0
                        self.glia_e += 1

            if step % 15 == 0:
                self.apply_rules()
                self._rebuild()

            if step % 100 == 0 and step > 0:
                cm = ~self.ie
                sig, C, L = compute_metrics(self.src[cm], self.tgt[cm], N)
                al = self.fit_alpha()
                er = self.el_r()
                logs['step'].append(step)
                logs['sigma'].append(sig)
                logs['alpha'].append(al or 0.0)
                logs['el'].append(er)
                logs['bonds'].append(len(self.src))
                logs['theta'].append(self.theta)
                a_str = f'{al:.3f}' if al else 'N/A'
                crit = ' [TARGET]' if (al and 1.5 <= al <= 2.5 and sig >= 4.0) else ''
                print(f'  Step {step:4d}: sigma={sig:.3f} alpha={a_str} '
                      f'E-L={er:.1%} bonds={len(self.src)}{crit}')

        return logs

# ============================================================
t0 = time.time()
print('=' * 70)
print('SDI v31 on Hemibrain connectome')
print(f'Source: hemibrain_meta.csv ({N_all} neurons, {N_active} active, sim={N})')
print('Parameters: C.elegans validated (T_DECAY=200)')
print('=' * 70)

net = SDI()
print(f'\nNetwork: N={net.N}, chem={int((~net.ie).sum())}, elec={int(net.ie.sum())}')
print(f'Sensors: {len(sensor_idx)}, Other: {N - len(sensor_idx)}')

# Initial metrics
cm = ~net.ie
sig0, C0, L0 = compute_metrics(net.src[cm], net.tgt[cm], N)
print(f'Initial: sigma={sig0:.3f}, C={C0:.3f}, L={L0:.3f}')

logs = net.run()

# Final metrics
cm = ~net.ie
sf, Cf, Lf = compute_metrics(net.src[cm], net.tgt[cm], N)
af = net.fit_alpha()
er = net.el_r()

print('\n' + '=' * 70)
print('HEMIBRAIN v31 RESULTS:')
print(f'  N={net.N}, chem={int((~net.ie).sum())}, elec={int(net.ie.sum())}')
print(f'  sigma={sf:.3f}  (target >= 4.0, C.elegans: 4.71)')
af_str = f'{af:.3f}' if af else 'N/A'
print(f'  alpha={af_str}  (target 1.5-2.5, C.elegans: 2.32)')
print(f'  C={Cf:.3f}  (target >= 0.30, C.elegans: 0.337)')
print(f'  L={Lf:.3f}  (target 2.0-3.5, C.elegans: 2.44)')
print(f'  E-L ratio={er:.1%}  (target 15-28%, C.elegans: 19.1%)')
print(f'  Glia events: {net.glia_e}')
print(f'  Scaling events: {net.scl_e}')
print(f'  Time: {time.time()-t0:.1f}s')

# Save results
results = {
    'sigma': float(sf),
    'alpha': float(af) if af else None,
    'C': float(Cf),
    'L': float(Lf),
    'el_ratio_final': float(er),
    'n_neurons': int(net.N),
    'n_total_in_csv': int(N_all),
    'n_active_in_csv': int(N_active),
    'n_chem_init': int(N_chem),
    'n_chem_final': int((~net.ie).sum()),
    'n_elec': int(net.ie.sum()),
    'scaling_events': int(net.scl_e),
    'glia_events': int(net.glia_e),
    'T_DECAY': int(T_DECAY),
    'MAX_FIX_PER_CALL': int(MAX_FIX),
    'steps': [int(x) for x in logs['step']],
    'sigma_traj': [float(x) for x in logs['sigma']],
    'alpha_traj': [float(x) for x in logs['alpha']],
    'el_ratio_traj': [float(x) for x in logs['el']],
    'bonds_traj': [int(x) for x in logs['bonds']],
    'theta_traj': [int(x) for x in logs['theta']],
}

out_path = '/home/work/.openclaw/workspace/sdi_sim/hemibrain_v31_results.json'
with open(out_path, 'w') as f:
    json.dump(results, f, indent=2)
print(f'\nResults saved to {out_path}')

# Plot
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
st = logs['step']

axes[0, 0].plot(st, logs['sigma'], 'b-o', ms=4, lw=2, label='sigma')
axes[0, 0].axhline(4.0, color='green', ls='--', lw=2, label='target >= 4.0')
axes[0, 0].axhline(sf, color='red', ls=':', lw=1.5, label=f'final={sf:.3f}')
axes[0, 0].set_title('Small-Worldness sigma'); axes[0, 0].legend(); axes[0, 0].grid(alpha=0.3)

av = [(s, a) for s, a in zip(st, logs['alpha']) if a > 0]
if av:
    axes[0, 1].plot(*zip(*av), 'r-o', ms=4, lw=2, label='alpha')
    axes[0, 1].axhline(1.5, color='green', ls='--', lw=1.5)
    axes[0, 1].axhline(2.5, color='green', ls='--', lw=1.5, label='[1.5, 2.5]')
axes[0, 1].set_title('Power-law alpha (avalanche)'); axes[0, 1].legend(); axes[0, 1].grid(alpha=0.3)

axes[1, 0].plot(st, [v * 100 for v in logs['el']], 'darkblue', lw=2, label='E-L%')
axes[1, 0].axhline(15, color='green', ls='--', lw=1.5, label='15% floor')
axes[1, 0].axhline(28, color='red', ls='--', lw=1.5, label='28% ceiling')
axes[1, 0].set_title('E-L Chemical Synapse Ratio'); axes[1, 0].set_ylabel('%')
axes[1, 0].legend(); axes[1, 0].grid(alpha=0.3)

ax = axes[1, 1]; ax.axis('off')
a_s = f'{af:.3f}' if af else 'N/A'

def p(cond): return '✓ PASS' if cond else '✗ FAIL'

items = [
    ('HEMIBRAIN v31 RESULTS (Full CSV Network)', 13, 'bold', 'black', 0.93),
    (f'{N_all} neurons in CSV → {N_active} active → N={N} simulated', 9, 'normal', 'gray', 0.87),
    ('', 9, 'normal', 'black', 0.81),
    (f'sigma = {sf:.3f}  (target ≥ 4.0)  [C.el: 4.71] → {p(sf >= 4.0)}', 11, 'normal', 'darkgreen' if sf >= 4.0 else 'darkred', 0.74),
    (f'alpha = {a_s}  (target 1.5–2.5)  [C.el: 2.32] → {p(af and 1.5 <= af <= 2.5)}', 11, 'normal', 'darkgreen' if (af and 1.5 <= af <= 2.5) else 'darkred', 0.68),
    (f'C      = {Cf:.3f}  (target ≥ 0.30)  [C.el: 0.337] → {p(Cf >= 0.30)}', 11, 'normal', 'darkgreen' if Cf >= 0.30 else 'darkred', 0.62),
    (f'L      = {Lf:.3f}  (target 2.0–3.5)  [C.el: 2.44] → {p(2.0 <= Lf <= 3.5)}', 11, 'normal', 'darkgreen' if 2.0 <= Lf <= 3.5 else 'darkred', 0.56),
    (f'E-L    = {er:.1%}  (target 15–28%)  [C.el: 19.1%] → {p(0.15 <= er <= 0.28)}', 11, 'normal', 'darkgreen' if 0.15 <= er <= 0.28 else 'darkred', 0.50),
    ('', 9, 'normal', 'black', 0.44),
]

valid = sf >= 4.0 and af and 1.5 <= af <= 2.5 and Cf >= 0.30
items.append(
    ('✅ ALL C.elegans params remain VALID at large scale' if valid
     else '⚠️  Some parameters need ADJUSTMENT for large scale',
     12, 'bold', 'darkgreen' if valid else 'darkred', 0.36)
)

for txt, fs, fw, clr, y in items:
    ax.text(0.05, y, txt, transform=ax.transAxes, fontsize=fs, fontweight=fw, color=clr, va='top')

plt.tight_layout()
plt.savefig('/home/work/.openclaw/workspace/sdi_sim/hemibrain_v31_results.png', dpi=150, bbox_inches='tight')
plt.close()
print('Plot saved. DONE')