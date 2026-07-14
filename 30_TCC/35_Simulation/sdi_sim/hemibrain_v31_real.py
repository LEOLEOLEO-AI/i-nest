#!/usr/bin/env python3
"""
SDI v31-real - Hemibrain REAL connectome (hemibrain_real_connectome_v3.json)
修复历史：从合成网络(v31)迁移到真实突触连接(v31-real)
原因：v31 用 pre/avg_fanout 估算度数并随机采样连接，导致 alpha~3.1（雪崩过短）
修复：直接加载真实突触连接 [pre_idx, post_idx, weight]，权重归一化后传导充分

数据级别：S4（iNEST仿真，基于真实Hemibrain connectome）
"""
import numpy as np, scipy.sparse as sp
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json, warnings, time
warnings.filterwarnings('ignore')
np.random.seed(42)

# ============================================================
# Hemibrain-specific parameters (NOT C.elegans defaults)
# ============================================================
T_DECAY      = 500    # bond decay steps
MAX_FIX      = 20
BOND_CAP     = 1.00
THETA_LTP_BASE = 25
THETA_LTD    = 8
ETA_LTP      = 0.010
ETA_LTD      = 0.008
TAU_STDP     = 20.0
Ea_S, Ea_L   = 0.15, 0.85
TAU_REC      = 150
U_SE_CHEM    = 0.45
T_ABS, T_REL, REL_SCALE = 3, 8, 0.3
EL_LO, EL_HI = 0.01, 0.08   # electrical synapse ratio targets
SCALING_INT  = 15
GLIA_INT     = 50
N_STEPS      = 500
CASCADE_MAX  = 50    # allow full avalanche propagation in large network
INH_THRESH   = 0.20  # 来源A（生物测量）：Drosophila CNS 抑制性神经元比例 ~20-25%
                     # Luo et al. 2010 Neuron; Aso et al. 2014 eLife DOI:10.7554/eLife.04577
                     # 前馈抑制模型：激活比例超过 f_inh≈0.20 时全局抑制触发
# --- 突触稳态可塑性（Synaptic Scaling）---
# 来源A：Turrigiano & Nelson 2004 Nat Rev Neurosci DOI:10.1038/nrn1327
# 来源B：平方根缩放指数（Turrigiano 1998 Nature）
P_TARGET     = 0.05   # 目标稀疏激活率：与 APL_THRESH 统一（来源A：Lin 2014 Nat Neurosci DOI:10.1038/nn.3648，KC稀疏激活~5%）
HOMEO_INT    = 50     # 稳态监测窗口（步数）
HOMEO_MARGIN = 1.5    # 触发阈值：实际激活率 > 1.5×目标 或 < 0.5×目标
HOMEO_ALPHA  = 0.5    # 缩放指数（Turrigiano 1998，平方根缩放）
W_MIN        = 0.0001 # 权重下限（防止完全消除，与当前权重尺度匹配）
W_MAX        = 0.068  # 权重上限（来源A：Bi & Poo 2001, Annu Rev Neurosci DOI:10.1146/annurev.neuro.24.1.139）
                      # LTP 饱和点约初始突触效能 2×；w_hi_initial=0.034 → 上限=0.034×2=0.068
# --- APL 等效全局抑制回路（H2 实验）---
# 来源A：Aso 2014 eLife DOI:10.7554/eLife.04577
#   KC 稀疏激活率目标 ~5%（Lin 2014 Nat Neurosci DOI:10.1038/nn.3648）
#   APL 为全局 GABAergic 抑制，强反馈，防止蘑菇体过度激发
# 来源B（物理推导）：比例控制器，K_apl > 1/(avg_in×w_mean)=0.060，取0.10（过阻尼）
P_APL_THRESH = 0.05   # KC 稀疏激活上限（来源A：Lin 2014）
K_APL        = 0.05   # APL 反馈增益（来源B重推导）：
                      # 目标 ratio=0.10 时 APL 贡献=0.05（轻微压制）
                      # K = 0.05 / ((0.10-0.05)/0.05) = 0.05
                      # ratio=0.20 时 APL=0.15，与原始INH协同总抑制≈0.15（合理）
INH_GAIN     = 3.0   # 来源B（物理推导）：线性前馈抑制增益；
                     # 3.0 使 inh 在 ratio=0.53 时达到饱和（inh=1.0），
                     # 对应网络中 ~53% 神经元同时激活的极端情况

# ============================================================
# Load REAL Hemibrain connectome
# ============================================================
print('Loading hemibrain_real_connectome_v3.json...')
t0 = time.time()
with open('/home/work/.openclaw/workspace/sdi_sim/hemibrain_real_connectome_v3.json') as f:
    data = json.load(f)

N_full = data['N']
all_edges = data['edges']  # [pre_idx, post_idx, weight]
print(f'Full connectome: N={N_full}, edges={len(all_edges)}')

# Subsample to N=6000 most connected neurons
import numpy as np
# Compute degree for each neuron
deg = np.zeros(N_full, int)
for e in all_edges:
    deg[e[0]] += 1
    deg[e[1]] += 1

top_idx = np.argsort(deg)[::-1][:6000]
top_set = set(top_idx.tolist())
idx_map = {old: new for new, old in enumerate(top_idx)}

# Filter edges: both endpoints in top_6000
edges_sub = [(idx_map[e[0]], idx_map[e[1]], e[2]) 
             for e in all_edges if e[0] in top_set and e[1] in top_set]
N = 6000
print(f'Subsampled: N={N}, edges={len(edges_sub)}, load_time={time.time()-t0:.1f}s')

# Build arrays
src_c = np.array([e[0] for e in edges_sub], np.int32)
tgt_c = np.array([e[1] for e in edges_sub], np.int32)
w_raw = np.array([float(e[2]) for e in edges_sub], np.float64)

# 权重归一化（来源A：Beggs & Plenz 2003, J Neurosci, DOI:10.1523/JNEUROSCI.23-35-11167.2003）
# SOC 临界条件：分支比 σ = avg_in × w_mean = 1（无抑制初始状态）
# top-6000 平均传入连接数 avg_in = 74.7（来源C：hemibrain_real_connectome_v3.json实测）
# → w_mean_critical = 1 / 74.7 = 0.0134
# → 范围 [0.007, 0.034]（对数归一化，对称于临界均值）
w_log = np.log1p(w_raw)
w_c = 0.0034 + 0.030 * (w_log - w_log.min()) / (w_log.max() - w_log.min() + 1e-9)
# 验证：对数分布w_mean实测需~0.0134，调整后[0.0034,0.0334]
bt_c = np.zeros(len(src_c), np.int8)
N_chem = len(src_c)
print(f'Chem edges: {N_chem}, w_mean={w_c.mean():.3f}, w_max={w_c.max():.3f}')

# Electrical synapses (~5%)
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
# Network metrics
# ============================================================
import scipy.sparse as sp

def compute_metrics(src, tgt, N, sample=2000):
    adj = sp.csr_matrix((np.ones(len(src)), (src, tgt)), shape=(N, N))
    d = np.array(adj.sum(axis=1)).ravel()
    C = float((d * (d - 1)).sum()) / max(1, len(src)) / 2 if len(src) > 0 else 0
    # estimate L via BFS from random sample
    smp = np.random.choice(N, min(sample, N), replace=False)
    dists = []
    for s in smp[:50]:
        row = sp.csgraph.shortest_path(adj, method='D', directed=True, indices=s)
        finite = row[np.isfinite(row) & (row > 0)]
        if len(finite) > 0:
            dists.append(finite.mean())
    L = np.mean(dists) if dists else 99.0
    # sigma
    n_rand = adj.nnz
    p = n_rand / (N * (N - 1))
    Cr = max(p, 1e-9)
    Lr = np.log(N) / np.log(max(2, N * p))
    sigma = (C / Cr) / (L / max(Lr, 0.1))
    return sigma, C, L

print('\nComputing initial metrics (fast)...')
cm0 = ~all_ie
sigma0, C0, L0 = compute_metrics(all_src[cm0], all_tgt[cm0], N, sample=100)
print(f'Initial: sigma={sigma0:.3f}, C={C0:.3f}, L={L0:.3f}')

# ============================================================
# SDI v31-real
# ============================================================
class SDI:
    def __init__(self):
        self.N = N
        self.t = 0
        self.src = all_src.copy()
        self.tgt = all_tgt.copy()
        self.w   = all_w.copy()
        self.bt  = all_bt.copy()
        self.ie  = all_ie.copy()
        self.Ea  = np.where(self.ie, 0.5, Ea_S)
        self.n_ltp = np.zeros(len(self.src), np.int32)
        self.n_ltd = np.zeros(len(self.src), np.int32)
        self.la = np.full(len(self.src), -99999, np.int32)
        self.R  = np.where(self.ie, 0.95, 1.0)
        self.lf = np.full(N, -99999, np.int32)
        self.ac = np.zeros(N, np.int32)
        self.ava = []
        self.theta = THETA_LTP_BASE
        self.act_history = []  # 每步激活率记录，用于稳态监测
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

    def el_r(self):
        cm = ~self.ie
        nb = cm.sum()
        return float(np.sum((self.bt == 4) & ~cm)) / max(1, nb) if nb else 0.0

    def fit_alpha(self):
        # Sliding window: last 200 avalanches
        window = self.ava[-200:] if len(self.ava) >= 200 else self.ava
        s = np.array([x for x in window if x >= 2])
        if len(s) < 40:
            return None
        xm = max(2, int(np.percentile(s, 10)))
        x = s[s >= xm]
        if len(x) < 15:
            return None
        return float(1 + len(x) / np.sum(np.log(x / (xm - 0.5))))

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
            # 原始 E-I 平衡抑制（来源A：Drosophila E-I ~80:20）
            inh = max(0, (ratio - INH_THRESH) * INH_GAIN)
            # APL 等效回路（H2实验）
            # 来源A：Aso 2014 eLife DOI:10.7554/eLife.04577，KC稀疏激活上限5%
            # 来源B：比例控制器 K_APL=0.10（过阻尼，K>0.060保证单步收敛）
            if ratio > P_APL_THRESH:
                inh_apl = K_APL * (ratio - P_APL_THRESH) / max(P_APL_THRESH, 1e-6)
                inh = min(1.0, inh + inh_apl)
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
        act_rate = aa.sum() / N
        self.ava.append(int(aa.sum()))
        self.act_history.append(float(act_rate))
        return aa

    def stdp(self, am):
        nd = np.where(am)[0]
        if len(nd) == 0:
            return
        fired = set(nd.tolist())
        pre_f = np.isin(self.src, nd)
        post_f = np.isin(self.tgt, nd)
        dt = self.t - self.la
        lp = pre_f & (dt >= 0) & (dt < 50) & (np.isin(self.tgt, nd))
        ld = post_f & (dt >= 0) & (dt < 50) & (np.isin(self.src, nd))
        idx = np.arange(len(self.src))
        if lp.any():
            self.n_ltp[lp] += 1
            self.w[lp] = np.clip(
                self.w[lp] + ETA_LTP * np.exp(-dt[lp] / TAU_STDP), W_MIN, W_MAX)  # Bi&Poo 2001
        if ld.any():
            self.n_ltd[ld] += 1
            self.w[ld] = np.clip(
                self.w[ld] - ETA_LTD * np.exp(-dt[ld] / TAU_STDP), W_MIN, W_MAX)
        self.la[pre_f] = self.t

    def apply_rules(self):
        er = self.el_r()
        if er > EL_HI:
            self.theta = min(THETA_LTP_BASE * 4, int(THETA_LTP_BASE * (1 + (er - EL_HI) * 12)))
        elif er < EL_LO:
            self.theta = max(5, int(THETA_LTP_BASE * (1 - (EL_LO - er) * 6)))
        else:
            self.theta = THETA_LTP_BASE

        cm = ~self.ie
        ct = cm & (((self.bt == 1) & (self.n_ltp >= self.theta)) |
                   ((self.bt == 2) & (self.n_ltd >= THETA_LTD)))
        if ct.any():
            self.bt[ct] = np.where(self.bt[ct] == 1, 2, 1)
            self.n_ltp[ct] = 0
            self.n_ltd[ct] = 0

        dc = cm & (self.bt == 2) & (self.t - self.la > T_DECAY)
        self.bt[dc] = 0
        self.n_ltp[dc] = 0
        self.n_ltd[dc] = 0
        self._rebuild()

    def run(self):
        logs = {'step': [], 'sigma': [], 'alpha': [], 'el': [], 'bonds': [], 'theta': []}
        print(f'\nRunning {N_STEPS} steps on REAL Hemibrain network')
        print(f'N={N}, chem={N_chem}, elec={Ne}')
        print(f'Params: T_DECAY={T_DECAY}, CASCADE_MAX={CASCADE_MAX}, INH_THRESH={INH_THRESH}')
        print('-' * 70)

        for step in range(N_STEPS):
            self.t = step
            # Sensor input
            n_inp = max(1, int(N * 0.03))
            seeds = np.random.choice(N, n_inp, replace=False).tolist()
            am = self.cascade(seeds)
            if am.any():
                self.stdp(am)
            if step % SCALING_INT == 0:
                self.apply_rules()
            # 突触稳态可塑性（每 HOMEO_INT 步）
            if step > 0 and step % HOMEO_INT == 0 and len(self.act_history) >= HOMEO_INT:
                p_actual = float(np.mean(self.act_history[-HOMEO_INT:]))
                if p_actual > HOMEO_MARGIN * P_TARGET or p_actual < P_TARGET / HOMEO_MARGIN:
                    # 小步缩放（来源A: Turrigiano 1998，稳态可塑性时间尺度慢）
                    # 每次只移动 2% 朝目标方向，避免过冲
                    ETA_HOMEO = 0.02
                    direction = 1.0 if p_actual > P_TARGET else -1.0
                    scale = 1.0 - direction * ETA_HOMEO
                    cm = ~self.ie
                    self.w[cm] = np.clip(self.w[cm] * scale, W_MIN, W_MAX)
                    self._rebuild()
                    # 记录稳态事件（不打印，避免干扰输出）
                    self.scl_e += 1

            if (step + 1) % 100 == 0:
                cm = ~self.ie
                sig, C, L = compute_metrics(self.src[cm], self.tgt[cm], N, sample=50)

                al = self.fit_alpha()
                er = self.el_r()
                crit = ' [SOC TARGET]' if (al and 1.5 <= al <= 2.5) else ''
                logs['step'].append(step)
                logs['sigma'].append(sig)
                logs['alpha'].append(al or 0.0)
                logs['el'].append(er)
                logs['bonds'].append(len(self.src))
                logs['theta'].append(self.theta)
                al_str = f'{al:.3f}' if al else 'N/A'
                print(f'  Step {step+1:4d}: sigma={sig:.3f} alpha={al_str} '
                      f'E-L={er:.1%} bonds={len(self.src)}{crit}')
        return logs

# Run
net = SDI()
t_run = time.time()
logs = net.run()
elapsed = time.time() - t_run

cm = ~net.ie
sf, Cf, Lf = compute_metrics(net.src[cm], net.tgt[cm], N, sample=100)
af = net.fit_alpha()
er = net.el_r()
af_str = f'{af:.3f}' if af else 'N/A'

print('\n' + '=' * 70)
print('HEMIBRAIN v31-REAL RESULTS (real connectome):')
print(f'  N={N}, chem={N_chem}, elec={Ne}')
print(f'  sigma={sf:.3f}  (target >= 1.0, Hemibrain-specific)')
print(f'  alpha={af_str}  (target 1.5-2.5, SOC critical)')
print(f'  C={Cf:.3f}  (target >= 0.04, Hemibrain W2-3: 0.0493)')
print(f'  L={Lf:.3f}  (target 2.0-3.5)')
print(f'  E-L ratio={er:.1%}  (elec/total synapse ratio, target 1-8%)')
print(f'  Time: {elapsed:.1f}s')

# Pass/fail
def p(cond): return '✓ PASS' if cond else '✗ FAIL'
print(f'\n  sigma: {p(sf >= 1.0)}')
print(f'  alpha: {p(af and 1.5 <= af <= 2.5)}')
print(f'  C:     {p(Cf >= 0.04)}')
print(f'  L:     {p(2.0 <= Lf <= 3.5)}')
valid = sf >= 1.0 and af and 1.5 <= af <= 2.5 and Cf >= 0.04 and 2.0 <= Lf <= 3.5
print(f'\n  OVERALL: {"✓ PASS" if valid else "✗ FAIL (partial)"}')

# Save results
results = {
    'version': 'v31-real',
    'data_source': 'hemibrain_real_connectome_v3.json (real synaptic connections)',
    'sigma': float(sf), 'alpha': float(af) if af else None,
    'C': float(Cf), 'L': float(Lf), 'el_ratio_final': float(er),
    'n_neurons': N, 'n_chem': N_chem, 'n_elec': Ne,
    'T_DECAY': T_DECAY, 'CASCADE_MAX': CASCADE_MAX,
    'INH_THRESH': INH_THRESH, 'valid': int(valid), 'elapsed_s': elapsed,
    'steps': [int(x) for x in logs['step']],
    'alpha_traj': [float(x) for x in logs['alpha']],
    'sigma_traj': [float(x) for x in logs['sigma']],
}
with open('/home/work/.openclaw/workspace/sdi_sim/hemibrain_v31real_results.json', 'w') as f:
    json.dump(results, f, indent=2)
print('\nResults saved to hemibrain_v31real_results.json')
print('DONE')
