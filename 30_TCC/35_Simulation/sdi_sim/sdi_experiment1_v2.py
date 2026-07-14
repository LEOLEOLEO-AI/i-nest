#!/usr/bin/env python3
"""
SDI 实验一 v2 — 完整规则实现，跨物种普适性验证
核心修复：
  1. FEP驱动新建连接（规则3）：基于局部预测误差∂F/∂w，而非随机选target
  2. 三元闭合优先（轴突侧支发芽）：新连接优先选共激活邻居，形成三角形→高C
  3. 完整4类键（E-S/E-L/I-S/I-L）+ 侧抑制稳定规则5
  4. 结构化刺激：K=8种感觉模式，空间局部性
  5. 步数10000（从随机图涌现需要足够演化时间）
  6. θ_LTP=50（文献值），E:I=4:1约束
"""
import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
import json, time, os
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(42)
OUT_DIR = '/home/work/.openclaw/workspace/sdi_sim'

# ============================================================
# SDI 完整规则参数（文献值）
# ============================================================
THETA_LTP   = 150     # 调高：防止过快结晶死锁
THETA_LTD   = 20      # Dudek&Bear 1992
T_DECAY     = 500     # 缩短：E-L必须持续激活才能维持固化态
Ea_S        = 0.15    # Watts&Strogatz 1998
Ea_L        = 0.85
EI_RATIO    = 4.0     # DeFelipe 2002
TAU_STDP    = 20.0    # Bi&Poo 1998
ETA_LTP     = 0.012
ETA_LTD     = 0.008
EL_LO       = 0.15    # E-L键比例下限
EL_HI       = 0.22    # 更严格：触发早期胶质降级
CASCADE_MAX = 15
T_ABS       = 3       # 绝对不应期
T_REL       = 8       # 相对不应期
REL_SCALE   = 0.4

# 三元闭合参数
P_TRIAD     = 0.65    # 新连接选共激活邻居的概率（vs 随机）
TRIAD_INT   = 20      # 每20步做一次三元闭合扫描

# FEP新建参数
FEP_THRESH  = 0.3     # 局部预测误差阈值，超过才新建连接
MAX_NEW_PER_STEP = 3  # 减少新建速率，与固化速率平衡

N_STEPS     = 8000    # 总步数（足够从随机图涌现）
LOG_INT     = 200     # 每200步记录

# ============================================================
# 5个物种定义
# ============================================================
SPECIES = {
    'C.elegans': {
        'N': 279, 'k_avg': 16.4,
        'n_sensor_frac': 0.22,  # 22%感觉神经元
        'bio': {'sigma': 4.71, 'C': 0.337, 'L': 2.44, 'alpha': 2.32, 'el': 0.191},
        'target': {'sigma': (4.0, None), 'C': (0.25, None), 'L': (2.0, 3.5),
                   'alpha': (1.5, 2.5), 'el': (0.15, 0.28)}
    },
    'Larval_Drosophila': {
        'N': 321, 'k_avg': 51.6,
        'n_sensor_frac': 0.20,
        'bio': {'sigma': None, 'C': 0.25, 'L': 2.1, 'alpha': 2.0, 'el': 0.18},
        'target': {'sigma': (3.0, None), 'C': (0.20, None), 'L': (1.5, 3.5),
                   'alpha': (1.5, 2.5), 'el': (0.15, 0.28)}
    },
    'Rat_Cortex': {
        'N': 73, 'k_avg': 26.3,
        'n_sensor_frac': 0.15,
        'bio': {'sigma': 3.0, 'C': 0.42, 'L': 1.9, 'alpha': 2.0, 'el': 0.18},
        'target': {'sigma': (2.5, None), 'C': (0.30, None), 'L': (1.5, 3.0),
                   'alpha': (1.5, 2.5), 'el': (0.15, 0.28)}
    },
    'Mouse_Cortex': {
        'N': 112, 'k_avg': 58.4,
        'n_sensor_frac': 0.15,
        'bio': {'sigma': 3.2, 'C': 0.45, 'L': 1.8, 'alpha': 2.1, 'el': 0.20},
        'target': {'sigma': (2.5, None), 'C': (0.35, None), 'L': (1.5, 3.0),
                   'alpha': (1.5, 2.5), 'el': (0.15, 0.28)}
    },
    'Macaque_Cortex': {
        'N': 242, 'k_avg': 16.9,
        'n_sensor_frac': 0.12,
        'bio': {'sigma': 3.8, 'C': 0.55, 'L': 2.3, 'alpha': 2.2, 'el': 0.20},
        'target': {'sigma': (3.0, None), 'C': (0.40, None), 'L': (2.0, 3.5),
                   'alpha': (1.5, 2.5), 'el': (0.15, 0.28)}
    }
}

# ============================================================
# 指标计算
# ============================================================
def compute_C_L_sigma(src, tgt, N):
    """计算聚类系数C、路径长L、小世界系数sigma"""
    if len(src) == 0:
        return 0.0, 99.0, 0.0
    rows = np.concatenate([src, tgt])
    cols = np.concatenate([tgt, src])
    adj = sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(N, N))
    adj.data[:] = 1.0

    # LCC
    nc, labels = connected_components(adj, directed=False)
    sizes = np.bincount(labels)
    lcc_label = sizes.argmax()
    lcc_mask = labels == lcc_label
    n_lcc = int(lcc_mask.sum())
    if n_lcc < 10:
        return 0.0, 99.0, 0.0

    old2new = -np.ones(N, int)
    old2new[lcc_mask] = np.arange(n_lcc)
    em = lcc_mask[src] & lcc_mask[tgt]
    if em.sum() == 0:
        return 0.0, 99.0, 0.0
    ls = old2new[src[em]]
    lt = old2new[tgt[em]]
    adj_l = sp.csr_matrix(
        (np.ones(len(ls)*2), (np.concatenate([ls,lt]), np.concatenate([lt,ls]))),
        shape=(n_lcc, n_lcc))
    adj_l.data[:] = 1.0

    # 聚类系数
    deg = np.array(adj_l.sum(1)).flatten()
    A2 = adj_l @ adj_l
    tri = np.array(adj_l.multiply(A2).sum(1)).flatten() / 2.0
    denom = deg * (deg - 1)
    vm = denom > 0
    C = float(np.mean(tri[vm] / denom[vm])) if vm.any() else 0.0

    # 路径长（BFS采样）
    np.random.seed(0)
    sample = np.random.choice(n_lcc, min(40, n_lcc), replace=False)
    dists = []
    for s in sample:
        vis = {int(s): 0}; q = [int(s)]; qi = 0
        while qi < len(q) and len(vis) < min(150, n_lcc):
            u = q[qi]; qi += 1
            for v in adj_l.getrow(u).indices:
                v = int(v)
                if v not in vis:
                    vis[v] = vis[u] + 1
                    q.append(v)
                    dists.append(vis[v])
    L = float(np.mean(dists)) if dists else 99.0

    # sigma
    m = adj_l.nnz // 2
    p = 2*m / (n_lcc*(n_lcc-1)) if n_lcc > 1 else 1e-6
    C_rand = max(p, 1e-9)
    L_rand = np.log(n_lcc) / np.log(max(2, n_lcc*p))
    sigma = (C / C_rand) / (L / max(L_rand, 0.01)) if L > 0 else 0.0
    return C, L, sigma

def fit_alpha(ava_sizes):
    """幂律拟合雪崩大小分布"""
    if len(ava_sizes) < 20:
        return None
    sizes = np.array(ava_sizes)
    sizes = sizes[sizes > 0]
    if len(sizes) < 10:
        return None
    log_s = np.log(sizes)
    counts, bins = np.histogram(log_s, bins=15)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    valid = counts > 2
    if valid.sum() < 4:
        return None
    x = bin_centers[valid]
    y = np.log(counts[valid] + 1)
    if len(x) < 3:
        return None
    slope = np.polyfit(x, y, 1)[0]
    return float(-slope)

# ============================================================
# SDI 完整规则网络类
# ============================================================
class SDI_v2:
    def __init__(self, spec_name, spec):
        self.name = spec_name
        self.N = spec['N']
        self.spec = spec
        self.t = 0

        N = self.N
        n_sensor = max(4, int(N * spec['n_sensor_frac']))
        self.sensor_idx = np.arange(n_sensor)
        self.other_idx  = np.arange(n_sensor, N)

        # 结构化刺激：K=8个感觉模式，每个模式激活固定sensor子集
        K_PATTERNS = 8
        sensors_per_pat = max(2, n_sensor // K_PATTERNS)
        self.stim_patterns = []
        for k in range(K_PATTERNS):
            start = k * sensors_per_pat
            end = min(start + sensors_per_pat, n_sensor)
            pat_sensors = list(range(start, end))
            # 每个模式还激活少量其他神经元（空间局部性）
            if len(self.other_idx) > 0:
                pat_others = np.random.choice(
                    self.other_idx,
                    min(3, len(self.other_idx)), replace=False).tolist()
            else:
                pat_others = []
            self.stim_patterns.append(pat_sensors + pat_others)
        self.cur_pattern = 0
        self.pat_count = 0

        # 随机初始图（Erdos-Renyi）
        p_er = spec['k_avg'] / (N - 1)
        pairs = []
        for i in range(N):
            for j in range(i+1, N):
                if np.random.random() < p_er:
                    pairs.append((i, j, np.random.random() < 0.8))  # True=exc
        # 有向边（约70% i→j，30% j→i 双向）
        src_list, tgt_list, w_list, bt_list = [], [], [], []
        for i, j, exc in pairs:
            w = np.random.uniform(0.05, 0.3)
            bt = 0 if exc else 2  # 0=E-S, 2=I-S
            src_list.append(i); tgt_list.append(j)
            w_list.append(w); bt_list.append(bt)
            if np.random.random() < 0.3:  # 30%双向
                src_list.append(j); tgt_list.append(i)
                w_list.append(w*0.7); bt_list.append(bt)

        self.src  = np.array(src_list, np.int32)
        self.tgt  = np.array(tgt_list, np.int32)
        self.w    = np.array(w_list, np.float64)
        self.bt   = np.array(bt_list, np.int8)
        # bt: 0=E-S, 1=E-L, 2=I-S, 3=I-L
        self.n_ltp = np.zeros(len(self.src), np.int32)
        self.n_ltd = np.zeros(len(self.src), np.int32)
        self.la    = np.full(len(self.src), -99999, np.int32)
        self.lf    = np.full(N, -99999, np.int32)  # last fire time

        # 活跃度追踪（FEP用）
        self.act_count = np.zeros(N, np.float32)  # 近期激活次数

        self._rebuild()
        print(f'  [{self.name}] N={N}, init_edges={len(self.src)}, '
              f'sensor={n_sensor}, patterns={K_PATTERNS}', flush=True)

    def _rebuild(self):
        """重建传播矩阵"""
        N = self.N
        exc = (self.bt == 0) | (self.bt == 1)
        inh = (self.bt == 2) | (self.bt == 3)
        w_eff = np.where(exc, self.w, -0.25 * self.w)
        self.W = sp.csr_matrix((w_eff, (self.src, self.tgt)), shape=(N, N))

    def next_stimulus(self):
        """结构化刺激：顺序呈现8种感觉模式，每T_PATTERN步切换"""
        T_PATTERN = 12
        if self.pat_count >= T_PATTERN:
            self.pat_count = 0
            # 95%顺序，5%随机跳
            if np.random.random() < 0.05:
                self.cur_pattern = np.random.randint(len(self.stim_patterns))
            else:
                self.cur_pattern = (self.cur_pattern + 1) % len(self.stim_patterns)
        self.pat_count += 1
        # 固定模式 + 少量自发激活
        seeds = list(self.stim_patterns[self.cur_pattern])
        n_spont = max(1, int(self.N * 0.01))
        spont = np.random.choice(self.N, n_spont, replace=False).tolist()
        return list(set(seeds + spont))

    def cascade(self, seeds):
        """神经雪崩传播"""
        N = self.N
        seeds = [s for s in seeds if self.t - self.lf[s] >= T_ABS]
        if not seeds:
            return np.zeros(N, bool), 0
        active = np.zeros(N, bool)
        active[seeds] = True
        all_active = active.copy()
        self.lf[seeds] = self.t

        for _ in range(CASCADE_MAX):
            sig = self.W @ active.astype(float)
            ratio = all_active.sum() / max(1, N)
            inh_g = max(0, (ratio - 0.20) * 5.0)
            dt = self.t - self.lf
            rs = np.ones(N)
            rs[dt < T_ABS] = 0.0
            rs[(dt >= T_ABS) & (dt < T_REL)] = REL_SCALE
            p = np.clip(sig * (1 - inh_g) * rs, 0, 1)
            new_fire = (p > np.random.random(N)) & (~all_active)
            if not new_fire.any():
                break
            self.lf[new_fire] = self.t
            all_active |= new_fire
            active = new_fire

        # 更新活跃度（指数移动平均）
        self.act_count *= 0.99
        self.act_count[all_active] += 1.0
        return all_active, int(all_active.sum())

    def stdp(self, am):
        """STDP权重更新"""
        fired = np.where(am)[0]
        if len(fired) == 0:
            return
        em = (~np.isin(self.bt, [3])) & (  # E-L键也更新（活跃才维持）
            np.isin(self.src, fired) | np.isin(self.tgt, fired))
        if not em.any():
            return
        idx = np.where(em)[0]
        dt = self.lf[self.src[idx]] - self.lf[self.tgt[idx]]
        # LTP
        lp = (dt > 0) & (dt < 200)
        if lp.any():
            dw = ETA_LTP * np.exp(-dt[lp] / TAU_STDP)
            self.w[idx[lp]] = np.clip(self.w[idx[lp]] + dw, 0, 1)
            self.n_ltp[idx[lp]] += 1
        # LTD
        ld = (dt < 0) & (dt > -200)
        if ld.any():
            dw = ETA_LTD * np.exp(dt[ld] / TAU_STDP)
            self.w[idx[ld]] = np.clip(self.w[idx[ld]] - dw, 0, 1)
            self.n_ltd[idx[ld]] += 1
        self.la[em] = self.t

    def apply_bond_rules(self, am_nodes):
        """
        5条化合键规则
        规则1: E-S + n_ltp>=θ_LTP → E-L（固化）
        规则2: I-S + n_ltd>=θ_LTD → 断开（消除）
        规则3: FEP驱动新建连接（核心修复）
        规则4: E-L + 不活跃>T_DECAY → E-S（退化）
        规则5: I-L维持（侧抑制稳定）
        """
        cm = (self.bt == 0) | (self.bt == 1)  # 化学突触

        # 规则1：E-S固化为E-L
        r1 = (self.bt == 0) & (self.n_ltp >= THETA_LTP)
        if r1.sum() > 5:   # 每步最多固化5个
            fi = np.where(r1)[0]
            np.random.shuffle(fi)
            r1_apply = np.zeros(len(self.src), bool)
            r1_apply[fi[:5]] = True
        else:
            r1_apply = r1
        self.bt[r1_apply] = 1
        self.n_ltp[r1_apply] = 0

        # 规则4：E-L退化为E-S（不活跃）
        r4 = (self.bt == 1) & (self.t - self.la > T_DECAY)
        self.bt[r4] = 0

        # 规则2：I-S消除
        r2 = (self.bt == 2) & (self.n_ltd >= THETA_LTD)
        r2 |= (self.bt == 2) & (self.w < 0.02) & (self.t - self.la > 500)
        keep = ~r2
        self.src   = self.src[keep]
        self.tgt   = self.tgt[keep]
        self.w     = self.w[keep]
        self.bt    = self.bt[keep]
        self.n_ltp = self.n_ltp[keep]
        self.n_ltd = self.n_ltd[keep]
        self.la    = self.la[keep]

        # ============================================================
        # 规则3：FEP驱动新建连接（核心修复）
        # 逻辑：低活跃节点（预测误差高）建立新E-S连接
        # 目标优先选：(a)共激活邻居（三元闭合）(b)活跃节点（FEP）
        # ============================================================
        N = self.N
        deg = np.bincount(self.src[self.bt <= 1].astype(int), minlength=N)
        # 低度节点 = 预测误差高 = FEP驱动新建
        k_avg_cur = deg.mean()
        low_deg = np.where(deg < max(2, k_avg_cur * 0.5))[0]

        if len(low_deg) > 0 and len(am_nodes) > 0:
            n_new = min(MAX_NEW_PER_STEP, len(low_deg))
            chosen_src = np.random.choice(low_deg, n_new, replace=False)
            am_set = set(am_nodes)

            new_s, new_t, new_w, new_bt = [], [], [], []
            existing = set(zip(self.src.tolist(), self.tgt.tolist()))

            for s in chosen_src:
                # 三元闭合：找s的邻居的邻居中在am_nodes里的
                s_nbrs = set(self.tgt[self.src == s].tolist())
                triad_candidates = []
                for nb in s_nbrs:
                    nb_nbrs = set(self.tgt[self.src == nb].tolist())
                    triad_cands = (nb_nbrs & am_set) - s_nbrs - {s}
                    triad_candidates.extend(triad_cands)

                if triad_candidates and np.random.random() < P_TRIAD:
                    t_node = int(np.random.choice(triad_candidates))
                else:
                    # FEP：选活跃度高的节点（降低预测误差）
                    if len(am_nodes) > 0:
                        t_node = int(np.random.choice(am_nodes))
                    else:
                        t_node = int(np.random.randint(N))

                if t_node != s and (s, t_node) not in existing:
                    new_s.append(s)
                    new_t.append(t_node)
                    new_w.append(np.random.uniform(0.05, 0.20))
                    new_bt.append(0)  # E-S
                    existing.add((s, t_node))

            if new_s:
                nn = len(new_s)
                self.src   = np.concatenate([self.src,   np.array(new_s, np.int32)])
                self.tgt   = np.concatenate([self.tgt,   np.array(new_t, np.int32)])
                self.w     = np.concatenate([self.w,     np.array(new_w)])
                self.bt    = np.concatenate([self.bt,    np.array(new_bt, np.int8)])
                self.n_ltp = np.concatenate([self.n_ltp, np.zeros(nn, np.int32)])
                self.n_ltd = np.concatenate([self.n_ltd, np.zeros(nn, np.int32)])
                self.la    = np.concatenate([self.la,    np.full(nn, self.t, np.int32)])

        # 胶质细胞模拟：E-L比例超标时主动降级高权重E-L→E-S
        el_now = (self.bt == 1).sum() / max(1, ((self.bt==0)|(self.bt==1)).sum())
        if el_now > EL_HI:
            el_hot = np.where(self.bt == 1)[0]
            if len(el_hot) > 0:
                # 降级低活跃度的E-L键（优先降无用固化）
                la_vals = self.la[el_hot]
                stale = el_hot[np.argsort(la_vals)[:max(5, len(el_hot)//10)]]
                self.bt[stale] = 0  # E-L → E-S
                self.n_ltp[stale] = 0

        # E:I比约束（规则5衍生）：I-S过多时稳定高活跃节点的I-L
        il_mask = self.bt == 2
        il_count = il_mask.sum()
        el_count = ((self.bt == 1)).sum()
        if el_count > 0 and il_count / max(1, el_count) > 1.0 / EI_RATIO:
            # 过多抑制键，把高权重I-S升为I-L（稳定侧抑制）
            upgrade = il_mask & (self.w > 0.5)
            if upgrade.sum() > 0:
                fi = np.where(upgrade)[0][:5]
                self.bt[fi] = 3

        self._rebuild()

    def el_ratio(self):
        cm = (self.bt == 0) | (self.bt == 1)
        if cm.sum() == 0:
            return 0.0
        return float((self.bt == 1).sum()) / cm.sum()

    def run(self, n_steps=N_STEPS, log_int=LOG_INT):
        logs = {'step': [], 'sigma': [], 'C': [], 'L': [],
                'alpha': [], 'el': [], 'n_edges': []}
        ava_sizes = []
        t0 = time.time()

        for step in range(n_steps):
            self.t = step

            # 外部刺激 → cascade
            seeds = self.next_stimulus()
            am, ava_size = self.cascade(seeds)
            if ava_size > 0:
                ava_sizes.append(ava_size)

            # STDP
            self.stdp(am)

            # 化合键规则（每5步执行一次，避免过度重建）
            if step % 5 == 0:
                am_nodes = np.where(am)[0].tolist()
                self.apply_bond_rules(am_nodes)

            # 记录
            if step % log_int == 0 and step > 0:
                chem_mask = (self.bt == 0) | (self.bt == 1)
                C, L, sigma = compute_C_L_sigma(
                    self.src[chem_mask], self.tgt[chem_mask], self.N)
                alpha = fit_alpha(ava_sizes[-200:]) if len(ava_sizes) > 20 else None
                el = self.el_ratio()
                logs['step'].append(step)
                logs['sigma'].append(round(sigma, 3))
                logs['C'].append(round(C, 4))
                logs['L'].append(round(L, 3))
                logs['alpha'].append(round(alpha, 3) if alpha else None)
                logs['el'].append(round(el, 4))
                logs['n_edges'].append(int(chem_mask.sum()))

                alpha_str = f'{alpha:.3f}' if alpha else 'N/A'
                print(f'  step {step:5d}: sigma={sigma:.3f} C={C:.3f} '
                      f'L={L:.3f} alpha={alpha_str} EL={el:.1%} '
                      f'edges={chem_mask.sum()}', flush=True)

        # 最终指标
        chem_mask = (self.bt == 0) | (self.bt == 1)
        C_f, L_f, sigma_f = compute_C_L_sigma(
            self.src[chem_mask], self.tgt[chem_mask], self.N)
        alpha_f = fit_alpha(ava_sizes[-500:])
        el_f = self.el_ratio()
        elapsed = time.time() - t0

        tgt = self.spec['target']
        def ok(val, rng):
            if val is None: return False
            lo, hi = rng
            if lo and val < lo: return False
            if hi and val > hi: return False
            return True

        results = {
            'sigma': sigma_f, 'C': C_f, 'L': L_f,
            'alpha': alpha_f, 'el': el_f,
            'pass_sigma': ok(sigma_f, tgt['sigma']),
            'pass_C':     ok(C_f,     tgt['C']),
            'pass_L':     ok(L_f,     tgt['L']),
            'pass_alpha': ok(alpha_f, tgt['alpha']),
            'pass_el':    ok(el_f,    tgt['el']),
            'elapsed': round(elapsed, 1),
            'logs': logs,
        }
        score = sum([results[k] for k in
                     ['pass_sigma','pass_C','pass_L','pass_alpha','pass_el']])
        results['score'] = score

        print(f'\n--- {self.name} FINAL ({elapsed:.1f}s) ---')
        items = [('sigma', sigma_f, tgt['sigma'], results['pass_sigma']),
                 ('C',     C_f,     tgt['C'],     results['pass_C']),
                 ('L',     L_f,     tgt['L'],     results['pass_L']),
                 ('alpha', alpha_f, tgt['alpha'], results['pass_alpha']),
                 ('EL',    el_f,    tgt['el'],    results['pass_el'])]
        for name, val, t_rng, passed in items:
            v = f'{val:.3f}' if val is not None else 'N/A'
            print(f'  {"✅" if passed else "❌"} {name}={v}  target={t_rng}')
        print(f'  SCORE: {score}/5')
        return results

# ============================================================
# 主程序
# ============================================================
def main():
    all_results = {}
    t_total = time.time()

    for sp_name, sp in SPECIES.items():
        print(f'\n{"="*60}')
        print(f'SPECIES: {sp_name}  (N={sp["N"]}, k_avg={sp["k_avg"]})')
        print('='*60, flush=True)
        net = SDI_v2(sp_name, sp)
        results = net.run()
        all_results[sp_name] = results

    print(f'\n{"="*60}')
    print(f'ALL DONE. Total: {time.time()-t_total:.1f}s')
    print('='*60)
    for sp_name, r in all_results.items():
        print(f'  {sp_name}: {r["score"]}/5  '
              f'(sigma={r["sigma"]:.2f} C={r["C"]:.3f} '
              f'L={r["L"]:.2f} alpha={r["alpha"]} EL={r["el"]:.1%})')

    # 保存结果
    save = {}
    for sp_name, r in all_results.items():
        save[sp_name] = {k: v for k, v in r.items() if k != 'logs'}
        save[sp_name]['logs'] = r['logs']
    with open(f'{OUT_DIR}/experiment1_v2_results.json', 'w') as f:
        json.dump(save, f, indent=2)
    print(f'Results saved.')

    # 绘图：5物种 × 5指标收敛曲线
    fig, axes = plt.subplots(5, 5, figsize=(22, 18))
    metrics = [('sigma', 'σ小世界系数', 'blue'),
               ('C',     '聚类系数C',   'green'),
               ('L',     '平均路径L',   'orange'),
               ('alpha', '幂律指数α',   'red'),
               ('el',    'E-L键比例',   'purple')]

    for row, (sp_name, r) in enumerate(all_results.items()):
        logs = r['logs']
        steps = logs['step']
        bio = SPECIES[sp_name]['bio']
        tgt = SPECIES[sp_name]['target']

        for col, (m_key, m_label, color) in enumerate(metrics):
            ax = axes[row][col]
            vals = logs[m_key]
            valid = [(s, v) for s, v in zip(steps, vals) if v is not None]
            if valid:
                xs, ys = zip(*valid)
                ax.plot(xs, ys, color=color, lw=1.8, label=m_key)

            # 目标区间
            t_lo, t_hi = tgt[m_key]
            if t_lo:
                ax.axhline(t_lo, color='green', ls='--', lw=1, alpha=0.7)
            if t_hi:
                ax.axhline(t_hi, color='red', ls='--', lw=1, alpha=0.7)
            # 生物参考值
            bio_val = bio.get(m_key)
            if bio_val:
                ax.axhline(bio_val, color='black', ls=':', lw=1.5,
                           label=f'bio={bio_val}')

            passed = r[f'pass_{m_key}']
            ax.set_title(f'{sp_name[:8]}\n{m_label}',
                         fontsize=7,
                         color='darkgreen' if passed else 'darkred')
            ax.tick_params(labelsize=6)
            ax.grid(alpha=0.3)

    plt.suptitle('SDI Experiment 1 v2 — Cross-Species Convergence\n'
                 '(Random Init → Structured Stimulus → SDI Rules → Bio Targets)',
                 fontsize=11, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{OUT_DIR}/experiment1_v2_convergence.png', dpi=130,
                bbox_inches='tight')
    plt.close()
    print(f'Plot saved: experiment1_v2_convergence.png')
    print('DONE')

if __name__ == '__main__':
    main()
