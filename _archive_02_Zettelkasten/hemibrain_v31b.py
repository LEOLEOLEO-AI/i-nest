#!/usr/bin/env python3
import numpy as np
import scipy.sparse as sp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collections import defaultdict
import json, warnings, time
warnings.filterwarnings('ignore')
np.random.seed(42)

# ============================================================
# Params (v31 C.elegans-validated)
# ============================================================
T_DECAY           = 200
MAX_FIX_PER_CALL  = 20
EL_FIX_THETA_FLOOR= 40
BOND_CAP_FACTOR   = 1.00
THETA_LTP_BASE    = 25
THETA_LTD         = 8
TAU_STDP          = 20.0
ETA_LTP           = 0.010
ETA_LTD           = 0.008
Ea_S, Ea_L        = 0.15, 0.85
TAU_REC           = 150
U_SE_CHEM         = 0.45
U_SE_ELEC         = 0.10
T_ABS, T_REL, REL_SCALE = 3, 8, 0.3
EL_TARGET_LO, EL_TARGET_HI = 0.15, 0.28
SCALING_THR, SCALING_RATE, SCALING_INT = 0.35, 0.12, 15
GLIA_THR, GLIA_RATE, GLIA_INT = 0.45, 0.25, 50
N_STEPS           = 500
CASCADE_MAX       = 15

# ============================================================
# Load Hemibrain CSV
# ============================================================
print('Loading hemibrain metadata...')
import csv
neurons = {}
with open('/home/work/.openclaw/workspace/10_Knowledge/专题归档/05_Datasets_仿真与实验数据/Simulation_Results/hemibrain_meta.csv') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        body_id = row[0]
        try: pre  = float(row[11]) if row[11] else 0.0
        except: pre  = 0.0
        try: post = float(row[12]) if row[12] else 0.0
        except: post = 0.0
        cell_class = row[4] or 'unknown'
        ntype = row[2] or 'unknown'
        if body_id not in neurons:
            neurons[body_id] = {'pre': 0.0, 'post': 0.0, 'class': cell_class, 'name': ntype}
        neurons[body_id]['pre']  += pre
        neurons[body_id]['post'] += post

def classify_neuron(cls):
    if cls in ('olfactory','hygrosensory','thermosensory'): return 'sensory'
    return 'interneuron'

body_ids = list(neurons.keys())
N_raw = len(body_ids)
body2idx = {b: i for i, b in enumerate(body_ids)}

# Build edge list from CSV degree data (config model)
print('Building synthetic connectome from CSV degrees...')
active = {bid: i for bid, i in body2idx.items()
          if neurons[bid]['pre'] > 5 or neurons[bid]['post'] > 5}
active_ids = list(active.keys())
N_active = len(active_ids)
print(f'Active neurons: {N_active}')

# Subsample to 5000 for tractable simulation
MAX_N = 5000
if N_active > MAX_N:
    degrees = np.array([max(neurons[bid]['pre'], neurons[bid]['post'])
                        for bid in active_ids], dtype=float)
    probs = degrees / degrees.sum()
    np.random.seed(42)
    sampled = np.random.choice(len(active_ids), MAX_N, replace=False, p=probs)
    sim_ids = [active_ids[i] for i in sampled]
else:
    sim_ids = active_ids

N_sim = len(sim_ids)
idx2sim = {i: bid for i, bid in enumerate(sim_ids)}
sim2idx = {bid: i for i, bid in enumerate(sim_ids)}
print(f'Simulating N={N_sim}')

# Degree sequence from pre/post counts
avg_fanout = 5
out_deg = np.clip([max(1, int(neurons[bid]['pre'] / avg_fanout)) for bid in sim_ids], 1, 80)
in_deg  = np.clip([max(1, int(neurons[bid]['post'] / avg_fanout)) for bid in sim_ids], 1, 80)

# Build edges (directed, will symmetrize for undirected metrics)
edges_src, edges_tgt = [], []
total_out = out_deg.sum()
for i, bid in enumerate(sim_ids):
    n_e = out_deg[i]
    targets = np.random.choice(N_sim, size=n_e, replace=True)
    for t in targets:
        if t != i:
            edges_src.append(i)
            edges_tgt.append(t)

src = np.array(edges_src, np.int32)
tgt = np.array(edges_tgt, np.int32)
w   = np.random.uniform(0.1, 0.8, len(src)).astype(np.float64)
btype = np.zeros(len(src), np.int8)  # E-S
is_elec = np.zeros(len(src), bool)
N_chem = len(src)
print(f'Chem edges: {N_chem}')

# Electric synapses (~5%)
N_elec = int(N_chem * 0.05)
e_src = np.random.randint(0, N_sim, N_elec, dtype=np.int32)
e_tgt = np.random.randint(0, N_sim, N_elec, dtype=np.int32)
e_w   = np.full(N_elec, 0.3, np.float64)
e_btype = np.full(N_elec, 4, np.int8)
e_is_elec = np.full(N_elec, True)

# Node types
node_types = {i: classify_neuron(neurons[idx2sim[i]]['class']) for i in range(N_sim)}
sensor_idx = np.array([i for i, t in node_types.items() if t == 'sensory'], np.int32)
other_idx  = np.arange(N_sim, dtype=np.int32)

# ============================================================
# Fast SDI v31
# ============================================================
class SDI_v31:
    def __init__(self, N, src, tgt, w, btype, is_elec, sensor_idx, other_idx):
        self.N = N
        self.src = src.astype(np.int32)
        self.tgt = tgt.astype(np.int32)
        self.weight = w.astype(np.float64)
        self.btype = btype.astype(np.int8)
        self.is_elec = is_elec.astype(bool)
        self.sensor_idx = sensor_idx
        self.other_idx  = other_idx
        self.Ea = np.where(self.is_elec, 0.5, Ea_S)
        self.n_ltp = np.zeros(len(self.src), np.int32)
        self.n_ltd = np.zeros(len(self.src), np.int32)
        self.last_active = np.full(len(self.src), -99999, np.int32)
        self.R = np.where(self.is_elec, 0.95, 1.0)
        self.t_fire = np.full(self.N, -99999.0)
        self.last_fire = np.full(self.N, -99999, np.int32)
        self.act_count = np.zeros(self.N, np.int32)
        self.avalanche_sizes = []
        self.t = 0
        self.scaling_events = 0
        self.glia_events = 0
        self.theta_ltp_current = THETA_LTP_BASE
        self._build_W()

    def _build_W(self):
        chem_mask = ~self.is_elec
        sign_chem = np.where(np.isin(self.btype[chem_mask], [0, 2]), 1.0, -0.25)
        w_chem = self.weight[chem_mask] * self.R[chem_mask] * sign_chem
        elec_mask = self.is_elec
        w_elec = self.weight[elec_mask] * self.R[elec_mask] * 0.5
        all_w = np.concatenate([w_chem, w_elec])
        all_src = np.concatenate([self.src[chem_mask], self.src[elec_mask]])
        all_tgt = np.concatenate([self.tgt[chem_mask], self.tgt[elec_mask]])
        self.W = sp.csr_matrix((all_w, (all_src, all_tgt)), shape=(self.N, self.N))

    def cascade(self, seeds):
        seeds = [s for s in seeds if (self.t - self.last_fire[s]) >= T_ABS]
        if not seeds:
            self.avalanche_sizes.append(0)
            return np.zeros(self.N, bool)
        active = np.zeros(self.N, bool)
        active[seeds] = True
        all_a = active.copy()
        for step in range(CASCADE_MAX):
            signal = self.W @ active.astype(float)
            ratio = all_a.sum() / max(1, self.N)
            inh = max(0, (ratio - 0.18) * 4.5)
            dt_f = self.t - self.last_fire
            ref_s = np.ones(self.N)
            ref_s[dt_f < T_ABS] = 0.0
            ref_s[(dt_f >= T_ABS) & (dt_f < T_REL)] = REL_SCALE
            prob = np.clip(signal * (1 - inh) * ref_s, 0, 1)
            new = (prob > np.random.random(self.N)) & (~all_a)
            if not new.any():
                break
            self.last_fire[new] = self.t + step
            self.act_count[new] += 1
            all_a |= new
            active = new
        self.avalanche_sizes.append(int(all_a.sum()))
        return all_a

    def stdp(self, am):
        nodes = np.where(am)[0]
        if len(nodes) == 0:
            return
        em = (~self.is_elec) & (np.isin(self.src, nodes) | np.isin(self.tgt, nodes))
        if not em.any():
            return
        idx = np.where(em)[0]
        dt = self.last_fire[self.src[idx]] - self.last_fire[self.tgt[idx]]
        ltp = (dt > 0) & (dt < 200)
        if ltp.any():
            self.weight[idx[ltp]] = np.clip(
                self.weight[idx[ltp]] + ETA_LTP * np.exp(-dt[ltp] / TAU_STDP), 0, 1)
            self.n_ltp[idx[ltp]] += 1
        ltd = (dt < 0) & (dt > -200)
        if ltd.any():
            self.weight[idx[ltd]] = np.clip(
                self.weight[idx[ltd]] - ETA_LTD * np.exp(dt[ltd] / TAU_STDP), 0, 1)
            self.n_ltd[idx[ltd]] += 1
        self.last_active[idx] = self.t

    def _el_ratio(self):
        chem = ~self.is_elec
        nb = chem.sum()
        if nb == 0: return 0.0
        return float(np.sum((self.btype == 2) & chem)) / nb

    def apply_rules(self):
        el_r = self._el_ratio()
        if el_r > EL_TARGET_HI:
            self.theta_ltp_current = min(THETA_LTP_BASE * 4,
                int(THETA_LTP_BASE * (1 + (el_r - EL_TARGET_HI) * 12)))
        elif el_r < EL_TARGET_LO:
            self.theta_ltp_current = max(5,
                int(THETA_LTP_BASE * (1 - (EL_TARGET_LO - el_r) * 6)))
        else:
            self.theta_ltp_current = THETA_LTP_BASE

        chem = ~self.is_elec
        # E-S -> E-L
        fixable = chem & (self.btype == 0) & (self.n_ltp >= self.theta_ltp_current)
        fix_count = fixable.sum()
        if fix_count > MAX_FIX_PER_CALL:
            fi = np.where(fixable)[0]
            np.random.shuffle(fi)
            fix = np.zeros(len(self.src), bool)
            fix[fi[:MAX_FIX_PER_CALL]] = True
        else:
            fix = fixable
        self.btype[fix] = 2
        self.Ea[fix] = Ea_L
        self.n_ltp[fix] = 0

        # E-L -> E-S decay
        dec = chem & (self.btype == 2) & (self.t - self.last_active > T_DECAY)
        self.btype[dec] = 0
        self.Ea[dec] = Ea_S

        # Prune
        cut = chem & (((self.btype == 1) & (self.n_ltd >= THETA_LTD)) |
                      ((self.btype == 0) & (self.weight < 0.01) &
                       (self.t - self.last_active > 1500)))
        keep = ~cut
        for attr in ('src','tgt','btype','weight','n_ltp','n_ltd',
                     'last_active','Ea','R','is_elec'):
            arr = getattr(self, attr)
            setattr(self, attr, arr[keep])

        # New bonds
        deg = np.bincount(self.src[~self.is_elec].astype(int), minlength=self.N)
        low = np.where(deg < 6)[0]
        if len(low) > 0:
            n_new = min(len(low)*2, int(60 * BOND_CAP_FACTOR))
            ns = np.random.choice(low, n_new)
            nt = np.random.randint(0, self.N, n_new)
            v = ns != nt
            ns, nt = ns[v], nt[v]
            n_add = len(ns)
            exc = np.random.random(n_add) < 0.8
            for attr, val in [
                ('src', np.concatenate([self.src, ns.astype(np.int32)])),
                ('tgt', np.concatenate([self.tgt, nt.astype(np.int32)])),
                ('btype', np.concatenate([self.btype, np.where(exc, 0, 1).astype(np.int8)])),
                ('weight', np.concatenate([self.weight,
                    np.where(exc, np.random.uniform(0.1, 0.4, n_add),
                             np.random.uniform(0.03, 0.12, n_add))])),
                ('n_ltp', np.concatenate([self.n_ltp, np.zeros(n_add, np.int32)])),
                ('n_ltd', np.concatenate([self.n_ltd, np.zeros(n_add, np.int32)])),
                ('last_active', np.concatenate([self.last_active, np.full(n_add, self.t, np.int32)])),
                ('Ea', np.concatenate([self.Ea, np.full(n_add, Ea_S)])),
                ('R', np.concatenate([self.R, np.ones(n_add)])),
                ('is_elec', np.concatenate([self.is_elec, np.zeros(n_add, bool)])),
            ]:
                setattr(self, attr, val)
        return el_r

    def compute_sigma_fast(self):
        import networkx as nx
        # Build undirected graph from chem edges
        chem = ~self.is_elec
        G = nx.Graph()
        for s, t in zip(self.src[chem].tolist(), self.tgt[chem].tolist()):
            G.add_edge(s, t)
        if G.number_of_nodes() < 3:
            return 1.0, 0.0, 0.0
        if not nx.is_connected(G):
            G = G.subgraph(max(nx.connected_components(G), key=len)).copy()
        n = G.number_of_nodes()
        m = G.number_of_edges()
        # Clustering
        C = nx.average_clustering(G)
        # Path length
        try:
            L = nx.average_shortest_path_length(G)
        except:
            L = 5.0
        # Small-worldness
        p = 2 * m / (n * (n - 1)) if n > 1 else 1
        Cr = max(p, 1e-6)
        Lr = np.log(n) / np.log(max(2, n * p))
        sigma = (C / Cr) / (L / max(Lr, 0.1))
        return sigma, C, L

    def fit_powerlaw(self):
        s = np.array([x for x in self.avalanche_sizes if x >= 2])
        if len(s) < 60:
            return None
        xm = max(2, int(np.percentile(s, 10)))
        x = s[s >= xm]
        if len(x) < 20:
            return None
        return float(1 + len(x) / np.sum(np.log(x / (xm - 0.5))))

    def run(self):
        print(f'\nRunning {N_STEPS} steps, N={self.N}')
        print(f'Chem edges={int((~self.is_elec).sum())}, elec={int(self.is_elec.sum())}')
        print(f'Params: T_DECAY={T_DECAY}, MAX_FIX={MAX_FIX_PER_CALL}, '
              f'BOND_CAP={BOND_CAP_FACTOR}')
        print('-' * 60)
        logs = {'step': [], 'sigma': [], 'alpha': [], 'el_ratio': [],
                'theta': [], 'bonds': []}

        for step in range(N_STEPS):
            self.t = step
            for _ in range(5):
                ns = max(1, min(len(self.sensor_idx), 3))
                no = max(1, int(self.N * 0.03))
                seeds = list(set(
                    list(np.random.choice(self.sensor_idx, ns, replace=False).tolist()) +
                    list(np.random.choice(self.other_idx, no, replace=False).tolist())
                ))
                am = self.cascade(seeds)
                self.stdp(am)
                self._build_W()
            # STD resource
            self.R += (1.0 - self.R) / TAU_REC
            active_nodes = np.where(self.last_fire == self.t)[0]
            if len(active_nodes) > 0:
                sa = np.isin(self.src, active_nodes)
                chem_a = sa & (~self.is_elec)
                self.R[chem_a] = np.clip(self.R[chem_a] - U_SE_CHEM * self.R[chem_a], 0.05, 1.0)
                elec_a = sa & self.is_elec
                self.R[elec_a] = np.clip(self.R[elec_a] - U_SE_ELEC * self.R[elec_a], 0.05, 1.0)

            if step % SCALING_INT == 0 and step > 0:
                chem = ~self.is_elec
                el_r = np.sum((self.btype == 2) & chem) / max(1, chem.sum())
                if el_r >= SCALING_THR:
                    thr = np.percentile(self.act_count, 80)
                    hot = np.where(self.act_count >= thr)[0]
                    if len(hot) > 0:
                        sm = chem & (self.btype == 2) & (np.isin(self.src, hot) | np.isin(self.tgt, hot))
                        if sm.sum() > 0:
                            self.weight[sm] *= (1 - SCALING_RATE)
                            deg = sm & (self.weight < 0.08)
                            self.btype[deg] = 0
                            self.Ea[deg] = Ea_S
                            self.scaling_events += 1

            if step % GLIA_INT == 0 and step > 0:
                chem = ~self.is_elec
                el_r = np.sum((self.btype == 2) & chem) / max(1, chem.sum())
                if el_r >= GLIA_THR:
                    el_bonds = np.where(chem & (self.btype == 2))[0]
                    if len(el_bonds) > 0:
                        n_deg = max(1, int(len(el_bonds) * GLIA_RATE))
                        top = el_bonds[np.argsort(self.weight[el_bonds])[::-1][:n_deg]]
                        self.btype[top] = 0
                        self.Ea[top] = Ea_S
                        self.n_ltp[top] = 0
                        self.glia_events += 1

            if step % 15 == 0:
                self.apply_rules()
                self._build_W()

            if step % 50 == 0:
                sig, C, L = self.compute_sigma_fast()
                alpha = self.fit_powerlaw()
                el_r = self._el_ratio()
                logs['step'].append(step)
                logs['sigma'].append(sig)
                logs['alpha'].append(alpha or 0)
                logs['el_ratio'].append(el_r)
                logs['theta'].append(self.theta_ltp_current)
                logs['bonds'].append(len(self.src))
                a_str = f'{alpha:.3f}' if alpha else 'N/A'
                print(f'  Step {step:4d}: sigma={sig:.3f} alpha={a_str} '
                      f'E-L={el_r:.1%} bonds={len(self.src)}')

        return logs

# ============================================================
# RUN
# ============================================================
t0 = time.time()
print('=' * 60)
print('SDI v31 on Hemibrain connectome (5000 neuron synthetic network)')
print('=' * 60)

# Combined edge arrays
all_src = np.concatenate([src, e_src])
all_tgt = np.concatenate([tgt, e_tgt])
all_w   = np.concatenate([w,   e_w])
all_btype = np.concatenate([btype, e_btype])
all_is_elec = np.concatenate([is_elec, e_is_elec])

net = SDI_v31(N_sim, all_src, all_tgt, all_w, all_btype, all_is_elec,
              sensor_idx, other_idx)
print(f'Network: N={N_sim}, chem={int((~net.is_elec).sum())}, elec={int(net.is_elec.sum())}')

sig0, C0, L0 = net.compute_sigma_fast()
print(f'Initial: sigma={sig0:.3f}, C={C0:.3f}, L={L0:.3f}')

logs = net.run()

# Final
sf, Cf, Lf = net.compute_sigma_fast()
af = net.fit_powerlaw()
el_f = net._el_ratio()

print('\n' + '=' * 60)
print('HEMIBRAIN v31 RESULTS:')
print(f'  sigma={sf:.3f}  (target >= 4.0)')
print(f'  alpha={af:.3f if af else None}  (target 1.5-2.5)')
print(f'  C={Cf:.3f}  (target >= 0.30)')
print(f'  L={Lf:.3f}  (target 2.0-3.5)')
print(f'  E-L={el_f:.1%}  (target 15-28%)')
print(f'  Glia={net.glia_events}, Scaling={net.scaling_events}')
print(f'  Time: {time.time()-t0:.1f}s')

results = {
    'sigma': sf, 'alpha': af, 'C': Cf, 'L': Lf,
    'el_ratio_final': el_f,
    'n_chem_final': int((~net.is_elec).sum()),
    'n_elec': int(net.is_elec.sum()),
    'n_neurons': N_sim,
    'scaling_events': net.scaling_events,
    'glia_events': net.glia_events,
    'T_DECAY': T_DECAY, 'MAX_FIX_PER_CALL': MAX_FIX_PER_CALL,
    'EL_FIX_THETA_FLOOR': EL_FIX_THETA_FLOOR,
    'BOND_CAP_FACTOR': BOND_CAP_FACTOR,
    'steps': logs['step'], 'sigma_traj': logs['sigma'],
    'alpha_traj': logs['alpha'], 'el_ratio_traj': logs['el_ratio'],
    'theta_traj': logs['theta'],
}
out = '/home/work/.openclaw/workspace/sdi_sim/hemibrain_v31_results.json'
with open(out, 'w') as f:
    json.dump(results, f, indent=2)
print(f'Saved: {out}')

# Plot
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
st = logs['step']
ax = axes[0,0]
ax.plot(st, logs['sigma'], 'b-o', ms=3, lw=1.5)
ax.axhline(4.0, color='green', ls='--', lw=2, label='target >= 4.0')
ax.set_title('Small-Worldness sigma'); ax.legend(); ax.grid(True, alpha=0.3)

ax = axes[0,1]
av = [v for v in logs['alpha'] if v > 0]
as_ = [s for s, v in zip(st, logs['alpha']) if v > 0]
if av:
    ax.plot(as_, av, 'r-o', ms=3, lw=2)
    ax.fill_between(as_, [1.5]*len(as_), [2.5]*len(as_), alpha=0.2, color='green')
ax.axhline(1.5, color='green', ls='--', lw=2, label='BP target [1.5,2.5]')
ax.set_title('Power-law alpha'); ax.legend(); ax.grid(True, alpha=0.3)

ax = axes[1,0]
ax.plot(st, [v*100 for v in logs['el_ratio']], 'darkblue', lw=2)
ax.axhline(15, color='green', ls='--', lw=1.5, label='15%')
ax.axhline(28, color='red',   ls='--', lw=1.5, label='28%')
ax.set_title('E-L Chemical Synapse Ratio'); ax.set_ylabel('%'); ax.legend(); ax.grid(True, alpha=0.3)

ax = axes[1,1]
ax.axis('off')
a_str = f'{af:.3f}' if af else 'N/A'
target_map = [
    ('sigma', sf, 4.0, None, '>='),
    ('alpha', af if af else 0, 1.5, 2.5, 'range'),
    ('C', Cf, 0.30, None, '>='),
    ('L', Lf, 2.0, 3.5, 'range'),
    ('EL', el_f*100, 15, 28, '%'),
]

def p(cond): return 'PASS' if cond else 'FAIL'
_valid = (sf >= 4.0 and af and 1.5 <= af <= 2.5 and Cf >= 0.30)
ae = af and 1.5 <= af <= 2.5
lines = [
    'HEMIBRAIN v31 RESULTS',
    'N=%d neurons (synthetic from hemibrain_meta.csv)' % N_sim,
    '',
    'sigma = %.3f  >= 4.0  [C.elegans: 4.71]  -> %s' % (sf, p(sf >= 4.0)),
    'alpha = %s  [1.5,2.5]  [C.elegans: 2.32]  -> %s' % (a_str, p(ae)),
    'C      = %.3f  >= 0.30  [C.elegans: 0.337]  -> %s' % (Cf, p(Cf >= 0.30)),
    'L      = %.3f  [2.0,3.5] [C.elegans: 2.44]  -> %s' % (Lf, p(2.0 <= Lf <= 3.5)),
    'E-L    = %.1f%%  [15%%,28%%] [C.elegans: 19.1%%] -> %s' % (el_f * 100, p(0.15 <= el_f <= 0.28)),
    '',
    'C.elegans params remain VALID at larger scale' if _valid else 'Some params need ADJUSTMENT for larger scale',
]

y = 0.95
for txt in lines:
    if 'PASS' in txt or 'VALID' in txt:
        color = 'darkgreen'
    elif 'FAIL' in txt or 'ADJUST' in txt:
        color = 'darkred'
    else:
        color = 'black'
    fs = 11 if ('VALID' in txt or 'ADJUST' in txt) else 9
    ax.text(0.05, y, txt, transform=ax.transAxes, fontsize=fs, color=color, va='top')
    y -= 0.055

plt.tight_layout()
plt.savefig('/home/work/.openclaw/workspace/sdi_sim/hemibrain_v31_results.png', dpi=150, bbox_inches='tight')
plt.close()
print('Plot saved.')
print('DONE')