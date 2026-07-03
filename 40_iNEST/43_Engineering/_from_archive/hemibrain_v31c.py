#!/usr/bin/env python3
import numpy as np
import scipy.sparse as sp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json, warnings, time
warnings.filterwarnings('ignore')
np.random.seed(42)

# ============================================================
# Params (v31 C.elegans-validated)
# ============================================================
T_DECAY, MAX_FIX, EL_FLOOR, BOND_CAP = 200, 20, 40, 1.00
THETA_LTP_BASE = 25; THETA_LTD = 8
TAU_STDP = 20.0; ETA_LTP = 0.010; ETA_LTD = 0.008
Ea_S, Ea_L = 0.15, 0.85
TAU_REC = 150; U_SE_CHEM = 0.45; U_SE_ELEC = 0.10
T_ABS, T_REL, REL_SCALE = 3, 8, 0.3
EL_LO, EL_HI = 0.15, 0.28
SCALING_INT = 15; GLIA_INT = 50; N_STEPS = 500
CASCADE_MAX = 12

# ============================================================
# Load Hemibrain CSV -> build synthetic edges
# ============================================================
print('Loading hemibrain CSV...')
import csv
neurons = {}
with open('/home/work/.openclaw/workspace/10_Knowledge/专题归档/05_Datasets_仿真与实验数据/Simulation_Results/hemibrain_meta.csv') as f:
    for row in csv.reader(f):
        if row[0] == 'body_id': continue
        bid = row[0]
        try: pre = float(row[11]) if row[11] else 0.0
        except: pre = 0.0
        try: post = float(row[12]) if row[12] else 0.0
        except: post = 0.0
        if bid not in neurons:
            neurons[bid] = {'pre': 0.0, 'post': 0.0, 'cls': row[4] or 'unk'}
        neurons[bid]['pre'] += pre
        neurons[bid]['post'] += post

# Subsample 2500 neurons proportional to degree
MAX_N = 2500
active_ids = [b for b, n in neurons.items() if n['pre'] > 5 or n['post'] > 5]
deg = np.array([max(neurons[b]['pre'], neurons[b]['post']) for b in active_ids], float)
probs = deg / deg.sum()
np.random.seed(42)
sidx = np.random.choice(len(active_ids), min(MAX_N, len(active_ids)), replace=False, p=probs)
sim_ids = [active_ids[i] for i in sidx]
N = len(sim_ids)
sim2idx = {b: i for i, b in enumerate(sim_ids)}
print(f'N={N} (from {len(active_ids)} active neurons)')

# Degree from CSV
avg_fanout = 5
out_deg = np.clip([max(1, int(neurons[b]['pre']/avg_fanout)) for b in sim_ids], 1, 60)
in_deg  = np.clip([max(1, int(neurons[b]['post']/avg_fanout)) for b in sim_ids], 1, 60)

# Build directed edges
edges = []
for i, b in enumerate(sim_ids):
    for t in np.random.choice(N, out_deg[i], replace=True):
        if t != i: edges.append((i, t))
src = np.array([e[0] for e in edges], np.int32)
tgt = np.array([e[1] for e in edges], np.int32)
w   = np.random.uniform(0.1, 0.7, len(src)).astype(np.float64)
bt  = np.zeros(len(src), np.int8)  # E-S
ie  = np.zeros(len(src), bool)
N_chem = len(src)
print(f'Chem edges: {N_chem}')

# Elec ~5%
Ne = int(N_chem * 0.05)
es = np.random.randint(0, N, Ne, np.int32)
et = np.random.randint(0, N, Ne, np.int32)
ew = np.full(Ne, 0.3, np.float64)
eb = np.full(Ne, 4, np.int8)
ee = np.full(Ne, True, bool)

all_src = np.concatenate([src, es]); all_tgt = np.concatenate([tgt, et])
all_w   = np.concatenate([w,   ew]); all_bt  = np.concatenate([bt,  eb])
all_ie  = np.concatenate([ie,  ee])

# Node types from CSV class
node_cls = [neurons[b]['cls'] for b in sim_ids]
sensor_idx = np.array([i for i, c in enumerate(node_cls)
                       if c in ('olfactory','hygrosensory','thermosensory')], np.int32)
other_idx  = np.arange(N, dtype=np.int32)
print(f'Sensors: {len(sensor_idx)}')

# ============================================================
# SDI v31 (compact, fast)
# ============================================================
class SDI:
    def __init__(self):
        self.N = N; self.t = 0
        self.src = all_src; self.tgt = all_tgt
        self.w = all_w; self.bt = all_bt; self.ie = all_ie
        self.Ea = np.where(self.ie, 0.5, Ea_S)
        self.n_ltp = np.zeros(len(self.src), np.int32)
        self.n_ltd = np.zeros(len(self.src), np.int32)
        self.la = np.full(len(self.src), -99999, np.int32)
        self.R = np.where(self.ie, 0.95, 1.0)
        self.lf = np.full(N, -99999, np.int32)
        self.ac = np.zeros(N, np.int32)
        self.ava = []
        self.theta = THETA_LTP_BASE
        self.scl_e = 0; self.glia_e = 0
        self._rebuild()

    def _rebuild(self):
        cm = ~self.ie
        sc = np.where(np.isin(self.bt[cm], [0,2]), 1.0, -0.25)
        wc = self.w[cm] * self.R[cm] * sc
        em = self.ie; we = self.w[em] * self.R[em] * 0.5
        self.W = sp.csr_matrix((np.concatenate([wc,we]),
                                (np.concatenate([self.src[cm],self.src[em]]),
                                 np.concatenate([self.tgt[cm],self.tgt[em]]))),
                                shape=(N, N))

    def cascade(self, seeds):
        seeds = [s for s in seeds if self.t - self.lf[s] >= T_ABS]
        if not seeds: self.ava.append(0); return
        a = np.zeros(N, bool); a[seeds] = True; aa = a.copy()
        for _ in range(CASCADE_MAX):
            sig = self.W @ a.astype(float)
            r = aa.sum() / max(1, N)
            inh = max(0, (r - 0.18) * 4.5)
            dt = self.t - self.lf
            rs = np.ones(N); rs[dt < T_ABS] = 0.0
            rs[(dt >= T_ABS) & (dt < T_REL)] = REL_SCALE
            p = np.clip(sig*(1-inh)*rs, 0, 1)
            nw = (p > np.random.random(N)) & (~aa)
            if not nw.any(): break
            self.lf[nw] = self.t; self.ac[nw] += 1; aa |= nw; a = nw
        self.ava.append(int(aa.sum()))

    def stdp(self, am):
        nd = np.where(am)[0]
        if len(nd) == 0: return
        em = (~self.ie) & (np.isin(self.src, nd) | np.isin(self.tgt, nd))
        if not em.any(): return
        idx = np.where(em)[0]
        dt = self.lf[self.src[idx]] - self.lf[self.tgt[idx]]
        lp = (dt > 0) & (dt < 200)
        if lp.any():
            self.w[idx[lp]] = np.clip(self.w[idx[lp]]+ETA_LTP*np.exp(-dt[lp]/TAU_STDP), 0, 1)
            self.n_ltp[idx[lp]] += 1
        ld = (dt < 0) & (dt > -200)
        if ld.any():
            self.w[idx[ld]] = np.clip(self.w[idx[ld]]-ETA_LTD*np.exp(dt[ld]/TAU_STDP), 0, 1)
            self.n_ltd[idx[ld]] += 1
        self.la[idx] = self.t

    def el_r(self):
        cm = ~self.ie; nb = cm.sum()
        return float(np.sum((self.bt == 2)&cm))/max(1, nb) if nb else 0.0

    def apply_rules(self):
        er = self.el_r()
        if er > EL_HI: self.theta = min(100, int(THETA_LTP_BASE*(1+(er-EL_HI)*12)))
        elif er < EL_LO: self.theta = max(5, int(THETA_LTP_BASE*(1-(EL_LO-er)*6)))
        else: self.theta = THETA_LTP_BASE
        cm = ~self.ie
        fx = cm & (self.bt == 0) & (self.n_ltp >= self.theta)
        if fx.sum() > MAX_FIX:
            fi = np.where(fx)[0]; np.random.shuffle(fi)
            f = np.zeros(len(self.src), bool); f[fi[:MAX_FIX]] = True
        else: f = fx
        self.bt[f] = 2; self.Ea[f] = Ea_L; self.n_ltp[f] = 0
        dc = cm & (self.bt == 2) & (self.t - self.la > T_DECAY)
        self.bt[dc] = 0; self.Ea[dc] = Ea_S
        ct = cm & (((self.bt==1)&(self.n_ltd>=THETA_LTD))|
                   ((self.bt==0)&(self.w<0.01)&(self.t-self.la>1500)))
        k = ~ct
        for a_ in ('src','tgt','bt','w','n_ltp','n_ltd','la','Ea','R','ie'):
            setattr(self, a_, getattr(self, a_)[k])
        # New bonds
        deg = np.bincount(self.src[~self.ie].astype(int), minlength=N)
        low = np.where(deg < 6)[0]
        if len(low) > 0:
            nn = min(len(low)*2, int(60*BOND_CAP))
            ns = np.random.choice(low, nn); nt = np.random.randint(0, N, nn)
            v = ns != nt; ns, nt = ns[v], nt[v]; na = len(ns)
            ex = np.random.random(na) < 0.8
            for a_, val in [('src',np.concatenate([self.src, ns])),
                            ('tgt',np.concatenate([self.tgt, nt])),
                            ('bt',np.concatenate([self.bt, np.where(ex,0,1)])),
                            ('w',np.concatenate([self.w, np.where(ex,
                                np.random.uniform(0.1,0.4,na),
                                np.random.uniform(0.03,0.12,na))])),
                            ('n_ltp',np.concatenate([self.n_ltp, np.zeros(na,np.int32)])),
                            ('n_ltd',np.concatenate([self.n_ltd, np.zeros(na,np.int32)])),
                            ('la',np.concatenate([self.la, np.full(na,self.t,np.int32)])),
                            ('Ea',np.concatenate([self.Ea, np.full(na,Ea_S)])),
                            ('R',np.concatenate([self.R, np.ones(na)])),
                            ('ie',np.concatenate([self.ie, np.zeros(na,bool)]))]:
                setattr(self, a_, val)
        return er

    def compute_metrics(self):
        cm = ~self.ie
        G_edges = [(int(s),int(t)) for s,t in zip(self.src[cm],self.tgt[cm])]
        # Build nx only for the largest connected component
        import networkx as nx
        G = nx.Graph(); G.add_edges_from(G_edges)
        if G.number_of_nodes() < 3: return 1.0, 0.0, 0.0
        if not nx.is_connected(G):
            G = G.subgraph(max(nx.connected_components(G), key=len)).copy()
        n_ = G.number_of_nodes(); m_ = G.number_of_edges()
        C = nx.average_clustering(G)
        try: L = nx.average_shortest_path_length(G)
        except: L = 5.0
        p_ = 2*m_/(n_*(n_-1)) if n_ > 1 else 1
        Cr = max(p_, 1e-6)
        Lr = np.log(n_) / np.log(max(2, n_*p_))
        return (C/Cr)/(L/max(Lr,0.1)), C, L

    def fit_alpha(self):
        s = np.array([x for x in self.ava if x >= 2])
        if len(s) < 60: return None
        xm = max(2, int(np.percentile(s, 10)))
        x = s[s >= xm]
        if len(x) < 20: return None
        return float(1 + len(x) / np.sum(np.log(x/(xm-0.5))))

    def run(self):
        print(f'Starting {N_STEPS} steps, N={N}')
        logs = {'step':[],'sigma':[],'alpha':[],'el':[],'theta':[]}
        for step in range(N_STEPS):
            self.t = step
            for _ in range(5):
                ns = max(1, min(len(sensor_idx), 3))
                no = max(1, int(N * 0.03))
                seeds = list(set(list(np.random.choice(sensor_idx,ns,replace=False)) +
                                 list(np.random.choice(other_idx,no,replace=False))))
                self.cascade(seeds); self.stdp(seeds); self._rebuild()
            self.R += (1-self.R)/TAU_REC
            an = np.where(self.lf == self.t)[0]
            if len(an) > 0:
                sa = np.isin(self.src, an)
                cm = ~self.ie; ca = sa & cm; ea = sa & self.ie
                self.R[ca] = np.clip(self.R[ca]-U_SE_CHEM*self.R[ca], 0.05, 1.0)
                self.R[ea] = np.clip(self.R[ea]-U_SE_ELEC*self.R[ea], 0.05, 1.0)
            if step % SCALING_INT == 0 and step > 0:
                er = self.el_r()
                if er >= 0.35:
                    hot = np.where(self.ac >= np.percentile(self.ac, 80))[0]
                    if len(hot) > 0:
                        cm = ~self.ie
                        sm = cm & (self.bt==2) & (np.isin(self.src,hot)|np.isin(self.tgt,hot))
                        if sm.sum() > 0:
                            self.w[sm] *= 0.88
                            dg = sm & (self.w < 0.08); self.bt[dg] = 0; self.Ea[dg] = Ea_S
                            self.scl_e += 1
            if step % GLIA_INT == 0 and step > 0:
                er = self.el_r()
                if er >= 0.45:
                    cm = ~self.ie
                    eb = np.where(cm & (self.bt==2))[0]
                    if len(eb) > 0:
                        nd = max(1, int(len(eb)*0.25))
                        top = eb[np.argsort(self.w[eb])[::-1][:nd]]
                        self.bt[top] = 0; self.Ea[top] = Ea_S; self.n_ltp[top] = 0
                        self.glia_e += 1
            if step % 15 == 0:
                self.apply_rules(); self._rebuild()
            if step % 50 == 0:
                sig, C, L = self.compute_metrics()
                al = self.fit_alpha()
                er = self.el_r()
                logs['step'].append(step); logs['sigma'].append(sig)
                logs['alpha'].append(al or 0); logs['el'].append(er)
                logs['theta'].append(self.theta)
                print(f'  step {step}: sigma={sig:.3f} alpha=str(al) '
                      f'EL={er:.1%} bonds={len(self.src)}')
        return logs

# ============================================================
# RUN
# ============================================================
t0 = time.time()
print('='*60)
print('SDI v31 on Hemibrain (2500 neuron synthetic network)')
print('='*60)
net = SDI()
print(f'N={net.N}, chem={int((~net.ie).sum())}, elec={int(net.ie.sum())}')
logs = net.run()
sf, Cf, Lf = net.compute_metrics()
af = net.fit_alpha()
er = net.el_r()
print(f'\n=== HEMIBRAIN v31 FINAL ===')
print(f'sigma={sf:.3f}  alpha={af if af else None}')
print(f'C={Cf:.3f}  L={Lf:.3f}  EL={er:.1%}')
print(f'Glia={net.glia_e}  Scaling={net.scl_e}')
print(f'Time: {time.time()-t0:.1f}s')

# Save
r = {'sigma':sf,'alpha':af,'C':Cf,'L':Lf,'el_ratio_final':er,
     'n_neurons':N,'n_chem_final':int((~net.ie).sum()),
     'scaling_events':net.scl_e,'glia_events':net.glia_e,
     'steps':logs['step'],'sigma_traj':logs['sigma'],
     'alpha_traj':logs['alpha'],'el_ratio_traj':logs['el']}
with open('/home/work/.openclaw/workspace/sdi_sim/hemibrain_v31_results.json','w') as f:
    json.dump(r, f, indent=2)

# Plot
fig, axes = plt.subplots(2,2, figsize=(12,9))
st = logs['step']
axes[0,0].plot(st, logs['sigma'], 'b-o', ms=3)
axes[0,0].axhline(4.0, color='green', ls='--', lw=2, label='target>=4.0')
axes[0,0].set_title('sigma'); axes[0,0].legend(); axes[0,0].grid(alpha=0.3)
av = [(s,a) for s,a in zip(st,logs['alpha']) if a > 0]
if av: axes[0,1].plot(*zip(*av), 'r-o', ms=3)
axes[0,1].axhline(1.5, color='green', ls='--', lw=2, label='[1.5,2.5]')
axes[0,1].set_title('alpha'); axes[0,1].legend(); axes[0,1].grid(alpha=0.3)
axes[1,0].plot(st, [v*100 for v in logs['el']], 'darkblue', lw=2)
axes[1,0].axhline(15, color='green', ls='--', lw=1.5, label='15%')
axes[1,0].axhline(28, color='red',   ls='--', lw=1.5, label='28%')
axes[1,0].set_title('E-L Ratio'); axes[1,0].set_ylabel('%'); axes[1,0].legend(); axes[1,0].grid(alpha=0.3)
ax = axes[1,1]; ax.axis('off')
a_s = '%.3f' % af if af else 'N/A'
def p(c): return 'PASS' if c else 'FAIL'
ax.text(0.05, 0.95, 'HEMIBRAIN v31 RESULTS', transform=ax.transAxes,
        fontsize=13, fontweight='bold', va='top')
ax.text(0.05, 0.88, 'N=%d neurons (synthetic from hemibrain_meta.csv)' % N,
        transform=ax.transAxes, fontsize=9, va='top')
ax.text(0.05, 0.80, 'sigma = %.3f  >= 4.0 -> %s' % (sf, p(sf>=4.0)),
        transform=ax.transAxes, fontsize=9, va='top')
ax.text(0.05, 0.74, 'alpha = %s  [1.5,2.5] -> %s' % (a_s, p(af and 1.5<=af<=2.5)),
        transform=ax.transAxes, fontsize=9, va='top')
ax.text(0.05, 0.68, 'C      = %.3f  >= 0.30 -> %s' % (Cf, p(Cf>=0.30)),
        transform=ax.transAxes, fontsize=9, va='top')
ax.text(0.05, 0.62, 'L      = %.3f  [2.0,3.5] -> %s' % (Lf, p(2.0<=Lf<=3.5)),
        transform=ax.transAxes, fontsize=9, va='top')
ax.text(0.05, 0.56, 'E-L    = %.1f%%  [15%%,28%%] -> %s' % (er*100, p(0.15<=er<=0.28)),
        transform=ax.transAxes, fontsize=9, va='top')
valid = sf>=4.0 and af and 1.5<=af<=2.5 and Cf>=0.30
ax.text(0.05, 0.46, 'C.elegans params VALID at larger scale' if valid
        else 'Params need ADJUSTMENT at larger scale',
        transform=ax.transAxes, fontsize=11,
        color='darkgreen' if valid else 'darkred', fontweight='bold', va='top')
plt.tight_layout()
plt.savefig('/home/work/.openclaw/workspace/sdi_sim/hemibrain_v31_results.png', dpi=150)
print('Plot saved. DONE')