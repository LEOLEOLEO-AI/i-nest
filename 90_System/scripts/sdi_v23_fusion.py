"""SDI v23 — 自适应θ节律 + FEP全局稳态 + 外部数据闭环驱动
==========================================================
基于 v8 基线，按 v22 设计文档的三大升级：

1. 自适应θ周期：T_theta(t) = T_base * (L(t) / L_ref) / v_c
   网络越小，θ窗口越短，避免小网络LTP过饱和

2. FEP全局稳态：per-node 出度权重目标约束
   每个节点的出度总权重有上限，超出后等比衰减

3. 外部数据闭环：MNIST 脉冲序列驱动
   不再只用随机噪声，用结构化外部数据驱动网络自组织

基线: sdi_v8_patched.py
目标: sigma>=4.0, alpha=1.5-2.0, E-L=[15-28%], F单调递减
"""

import numpy as np, networkx as nx, matplotlib, matplotlib.pyplot as plt
from collections import defaultdict
import json, os, warnings, time, struct, gzip
warnings.filterwarnings("ignore")
matplotlib.rcParams["font.family"] = "DejaVu Sans"

np.random.seed(42)

DATA_PATH = "D:/Obsidian/phase1_workspace/connectome_v8_data.json"
OUT_DIR   = "D:/Obsidian/phase1_workspace/v23_results"
os.makedirs(OUT_DIR, exist_ok=True)

# ============ v8 基线参数 ============
TAU_STDP, ETA_LTP, ETA_LTD = 20.0, 0.020, 0.016
Ea_S, Ea_L = 0.15, 0.85
THETA_LTP_BASE = 25; THETA_LTD = 8; T_DECAY = 25000
TAU_REC, U_SE_CHEM, U_SE_ELEC = 150, 0.45, 0.10
T_ABS = 3; T_REL = 8; REL_SCALE = 0.3
SCALING_THR, SCALING_RATE, SCALING_INT = 0.35, 0.12, 15
GLIA_THR, GLIA_RATE, GLIA_INT = 0.45, 0.25, 50
SEED_FRAC_SENSOR, SEED_FRAC_OTHER = 0.20, 0.03
N_STEPS = 200; CASCADE_MAX = 15
EL_TARGET_LO, EL_TARGET_HI = 0.15, 0.28

# ============ v22 新增参数 ============
# 升级1: 自适应θ周期
T_THETA_BASE = 25
L_REF = 2.44   # C.elegans 参考路径长度
V_C   = 1.0    # 信号传播速度
T_THETA_MIN = 5
T_THETA_MAX = 100

# 升级2: FEP全局稳态
FEP_TARGET_OUT_W = 3.0  # 每个节点出度权重总目标
FEP_HOMEOSTASIS_INT = 20  # 稳态检查间隔

# ============ v23 Fusion: FEP Attractor + JEPA (v3 final) ============
FEP_GRAD_CLIP = 0.5
FEP_ATTRACTOR_STRENGTH = 1.0
FEP_BASIN_WINDOW = 10
JEPA_BETA_MIN = 0.5
JEPA_BETA_MAX = 5.0
JEPA_TARGET_ENTROPY = 0.35
GLOBAL_ENERGY_BUDGET = 500.0
N_STEPS = 300
T_THETA_BASE = 10

# 升级3: 外部数据
MNIST_PATH = None  # 如果存在MNIST文件则使用，否则用结构化脉冲替代
EXTERNAL_DRIVE = True  # 是否启用外部数据闭环

# 自由能追踪
F_WINDOW = 100

# ============ MNIST 加载（如果可用）============
def load_mnist_spikes():
    try:
        paths = [
            "D:/Obsidian/phase1_workspace/mnist/train-images-idx3-ubyte.gz",
            "D:/Obsidian/phase1_workspace/mnist/t10k-images-idx3-ubyte.gz"
        ]
        images = []
        for p in paths:
            if os.path.exists(p):
                with gzip.open(p, "rb") as f:
                    magic, num, rows, cols = struct.unpack(">IIII", f.read(16))
                    buf = f.read()
                    imgs = np.frombuffer(buf, dtype=np.uint8).reshape(num, rows*cols)
                    images.append(imgs)
        if images:
            all_imgs = np.concatenate(images, axis=0) / 255.0
            print(f"  MNIST加载成功: {all_imgs.shape[0]} images, {all_imgs.shape[1]} pixels")
            return all_imgs
    except Exception as e:
        print(f"  MNIST加载失败: {e}")
    return None

# ============ 结构化脉冲生成器（MNIST不可用时的替代）============
class StructuredSpikeGenerator:
    """生成具有结构化模式的脉冲序列，模拟外部感知输入"""
    def __init__(self, N_inputs, N_patterns=10):
        self.N = N_inputs
        self.N_patterns = N_patterns
        # 生成10个结构化模式（类似不同数字的脉冲签名）
        self.patterns = []
        for i in range(N_patterns):
            pattern = np.zeros(N_inputs)
            # 每个模式激活不同的子集
            active = np.random.choice(N_inputs, size=N_inputs//5, replace=False)
            pattern[active] = np.random.uniform(0.3, 1.0, len(active))
            self.patterns.append(pattern / pattern.max())

    def sample(self, n_samples=1):
        idx = np.random.randint(0, self.N_patterns, n_samples)
        spikes = []
        for i in idx:
            p = self.patterns[i].copy()
            # 加噪声模拟真实感知识别变化
            p += np.random.normal(0, 0.05, self.N)
            p = np.clip(p, 0, 1)
            # 泊松脉冲编码
            spike_train = (np.random.random(self.N) < p * 0.5).astype(np.float64)
            spikes.append(spike_train)
        return np.array(spikes)

# ============ v22 主类 ============
class SDI_v23:
    def __init__(self):
        t0 = time.time()
        print("v23: 自适应θ + FEP稳态 + 外部数据闭环驱动...")
        with open(DATA_PATH) as f:
            data = json.load(f)

        self.N = data["N"]
        self.nodes = data["nodes"]
        self.n_types = data["n_types"]
        self.sensor_idx = np.array([i for i,n in enumerate(self.nodes)
                                     if self.n_types[n]=="sensory"], np.int32)
        self.motor_idx  = np.array([i for i,n in enumerate(self.nodes)
                                     if self.n_types[n]=="motor"], np.int32)
        self.inter_idx  = np.array([i for i,n in enumerate(self.nodes)
                                     if self.n_types[n]=="interneuron"], np.int32)

        # 真实化学突触
        chem = data["edges_chem"]
        chem_src = np.array([e[0] for e in chem], np.int32)
        chem_tgt = np.array([e[1] for e in chem], np.int32)
        chem_nbr = np.array([e[2] for e in chem], np.float64)
        chem_w   = chem_nbr / chem_nbr.max()
        chem_type = np.zeros(len(chem), np.int8)

        # 真实电突触（双向展开）
        elec = data["edges_elec"]
        e_src1 = np.array([e[0] for e in elec], np.int32)
        e_tgt1 = np.array([e[1] for e in elec], np.int32)
        e_src2 = e_tgt1.copy(); e_tgt2 = e_src1.copy()
        elec_src = np.concatenate([e_src1, e_src2])
        elec_tgt = np.concatenate([e_tgt1, e_tgt2])
        elec_w   = np.full(len(elec_src), 0.3)
        elec_type = np.full(len(elec_src), 4, np.int8)

        N_chem = len(chem_src); N_elec = len(elec_src)
        self.src = np.concatenate([chem_src, elec_src])
        self.tgt = np.concatenate([chem_tgt, elec_tgt])
        self.weight = np.concatenate([chem_w, elec_w])
        self.btype = np.concatenate([chem_type, elec_type])
        self.is_elec = np.concatenate([np.zeros(N_chem,bool), np.ones(N_elec,bool)])
        self.Ea = np.where(self.is_elec, 0.5, Ea_S)

        # STDP状态
        self.n_ltp = np.zeros(len(self.src), np.int32)
        self.n_ltd = np.zeros(len(self.src), np.int32)
        self.last_active = np.full(len(self.src), -99999, np.int32)
        self.R = np.where(self.is_elec, 0.95, 1.0)

        # 节点状态
        self.h = np.random.uniform(0.05, 0.15, self.N).astype(np.float64)
        self.tau_i = np.full(self.N, 5.0, np.float64)
        self.t_fire = np.full(self.N, -99999.0)
        self.last_fire = np.full(self.N, -99999, np.int32)
        self.act_count = np.zeros(self.N, np.int32)

        # v23: 自由能追踪
        self.F_local = np.zeros(self.N)
        # v23: FEP basin tracking + JEPA
        self.F_basin_min = np.full(self.N, np.inf)
        self.F_basin_count = np.zeros(self.N, np.int32)
        self.F_converged = np.zeros(self.N, bool)
        self.F_gradient = np.zeros(self.N)
        self.beta_eff = JEPA_BETA_MIN
        self.entropy_history = []
        self.sigma_history = []
        self.el_ratio_history = []
        self.beta_eff_history = []
        self.F_history = []
        self.surprise_i = np.zeros(self.N)

        self.avalanche_sizes = []
        self.S_tot = 0.0
        self.scaling_events = 0
        self.glia_events = 0
        self.theta_ltp_current = THETA_LTP_BASE
        self.t = 0

        # v23: 外部数据
        self.mnist_data = load_mnist_spikes()
        self.structured_gen = StructuredSpikeGenerator(len(self.sensor_idx))

        self.adj = [[] for _ in range(self.N)]
        for j in range(len(self.src)):
            self.adj[int(self.src[j])].append(j)
        self._rebuild()
        dt = time.time()-t0
        print(f"v22初始化: N={self.N} chem={N_chem} elec={N_elec//2} (耗时{dt:.1f}s)")

    def _rebuild(self):
        self.G = nx.Graph()
        self.G.add_nodes_from(range(self.N))
        for s,t in zip(self.src, self.tgt):
            self.G.add_edge(int(s), int(t))

    # ===== v23升级1: 自适应θ周期 =====
    def compute_adaptive_theta(self):
        if not nx.is_connected(self.G):
            return T_THETA_BASE
        L_current = nx.average_shortest_path_length(self.G)
        T_theta = int(T_THETA_BASE * (L_current / L_REF) / V_C)
        return max(T_THETA_MIN, min(T_theta, T_THETA_MAX))

    # ===== v23升级2: FEP全局稳态 =====
    def fep_homeostasis(self):
        """per-node 出度权重目标约束"""
        n_changed = 0
        for i in range(self.N):
            out_mask = (self.src == i) & (~self.is_elec)
            if not out_mask.any(): continue
            total_w = self.weight[out_mask].sum()
            if total_w > FEP_TARGET_OUT_W:
                scale = FEP_TARGET_OUT_W / total_w
                self.weight[out_mask] *= scale
                n_changed += 1
            # 同时更新Ea：权重低的键降低活化能
            low_w_mask = out_mask & (self.weight < 0.05)
            if low_w_mask.any():
                self.Ea[low_w_mask] = np.clip(self.Ea[low_w_mask] * 0.9, 0.01, Ea_L)
        return n_changed

    # ===== 计算局部自由能 =====
    def compute_local_F(self):
        for i in range(self.N):
            out_edges = (self.src == i)
            if not out_edges.any():
                self.F_local[i] = 0.0; continue
            F_i = 0.0; n_out = 0
            for j in np.where(out_edges)[0]:
                tgt_node = self.tgt[j]
                prediction = self.h[i] * self.weight[j]
                actual = self.h[tgt_node]
                F_i += (prediction - actual)**2 + self.Ea[j] * self.weight[j]**2
                n_out += 1
            self.F_local[i] = F_i / max(n_out, 1)

        # 惊讶度
        self.F_history.append(float(self.F_local.mean()))
        if len(self.F_history) > F_WINDOW:
            window = np.array(self.F_history[-F_WINDOW:])
            mean_F, std_F = window.mean(), window.std()
            if std_F > 1e-8:
                for i in range(self.N):
                    self.surprise_i[i] = abs(self.F_local[i] - mean_F) / std_F

    # ===== 级联激活 =====
    def cascade(self, stim):
        seeds = np.where(stim > 0.2)[0]
        seeds = [s for s in seeds if (self.t - self.last_fire[s]) >= T_ABS]
        if not seeds:
            self.avalanche_sizes.append(0)
            return np.zeros(self.N, bool)

        active = np.zeros(self.N, bool)
        active[seeds] = True
        self.t_fire[seeds] = float(self.t)
        self.last_fire[seeds] = self.t
        self.act_count[seeds] += 1

        cascade_list = list(seeds)
        for _ in range(CASCADE_MAX):
            new_active = []
            for node in cascade_list:
                out_edges = self.adj[node]
                for j in out_edges:
                    tgt_node = self.tgt[j]
                    if active[tgt_node]: continue
                    w = self.weight[j] * self.R[j]
                    if w > 0.1:
                        active[tgt_node] = True
                        self.t_fire[tgt_node] = float(self.t)
                        self.last_fire[tgt_node] = self.t
                        self.act_count[tgt_node] += 1
                        new_active.append(tgt_node)
            if not new_active: break
            cascade_list = new_active

        self.avalanche_sizes.append(active.sum())
        return active

    # ===== STDP =====
    def stdp_update(self, active_mask):
        active_nodes = np.where(active_mask)[0]
        if len(active_nodes) == 0: return

        # 突触前更新
        for pre in active_nodes:
            out_edges = np.where(self.src == pre)[0]
            for j in out_edges:
                if self.is_elec[j]: continue
                post = self.tgt[j]
                if active_mask[post]:
                    # pre-post 同时激活 → LTP
                    self.n_ltp[j] += 1
                    self.n_ltd[j] = 0
                    dw = ETA_LTP
                    self.weight[j] = np.clip(self.weight[j] + dw, 0.01, 3.0)
                else:
                    # pre激活但post未激活 → LTD
                    self.n_ltd[j] += 1
                    self.n_ltp[j] = 0
                    dw = -ETA_LTD
                    self.weight[j] = np.clip(self.weight[j] + dw, 0.01, 3.0)
                self.last_active[j] = self.t

    # ===== 键类型固化/衰减 =====
    def apply_rules(self):
        chem = ~self.is_elec

        # E-S → E-L (固化): LTP计数超过θ阈值
        fix = chem & (self.btype==0) & (self.n_ltp >= self.theta_ltp_current)
        if fix.any():
            self.btype[fix] = 2
            self.Ea[fix] = Ea_L
            self.n_ltp[fix] = 0

        # E-L → E-S (衰减): 长时间未激活
        dec = chem & (self.btype==2) & (self.t - self.last_active > T_DECAY)
        if dec.any():
            self.btype[dec] = 0
            self.Ea[dec] = Ea_S

        # 修剪极弱键
        cut = chem & (self.weight < 0.01) & (self.t - self.last_active > 1500)
        if cut.any():
            keep = ~cut
            self._apply_keep(keep)

        # 新建E-S键（低出度节点）
        deg = np.bincount(self.src[chem].astype(int), minlength=self.N)
        low = np.where(deg < 6)[0]
        if len(low) > 0:
            n_new = min(len(low)*2, 60)
            ns = np.random.choice(low, n_new)
            nt = np.random.randint(0, self.N, n_new)
            valid = ns != nt
            ns, nt = ns[valid], nt[valid]; n_add = len(ns)
            if n_add > 0:
                exc = np.random.random(n_add) < 0.8
                self.src = np.concatenate([self.src, ns.astype(np.int32)])
                self.tgt = np.concatenate([self.tgt, nt.astype(np.int32)])
                self.btype = np.concatenate([self.btype, np.where(exc,0,1).astype(np.int8)])
                self.weight = np.concatenate([self.weight,
                    np.where(exc, np.random.uniform(0.1,0.4,n_add),
                             np.random.uniform(0.03,0.12,n_add))])
                self.n_ltp = np.concatenate([self.n_ltp, np.zeros(n_add, np.int32)])
                self.n_ltd = np.concatenate([self.n_ltd, np.zeros(n_add, np.int32)])
                self.last_active = np.concatenate([self.last_active,
                                                   np.full(n_add, self.t, np.int32)])
                self.Ea = np.concatenate([self.Ea, np.full(n_add, Ea_S)])
                self.R  = np.concatenate([self.R, np.ones(n_add)])
                self.is_elec = np.concatenate([self.is_elec, np.zeros(n_add, bool)])
                for k in range(n_add):
                    self.adj[int(ns[k])].append(len(self.src) - n_add + k)

    def _apply_keep(self, keep):
        for attr in ["src","tgt","btype","weight","n_ltp","n_ltd",
                     "last_active","Ea","R","is_elec"]:
            arr = getattr(self, attr)
            setattr(self, attr, arr[keep])
        self.adj = [[] for _ in range(self.N)]
        for j in range(len(self.src)):
            self.adj[int(self.src[j])].append(j)

    # ===== 突触缩放 =====
    def synaptic_scaling(self):
        chem = ~self.is_elec
        nb = chem.sum()
        el_r = np.sum((self.btype==2) & chem) / max(1, nb)
        if el_r < SCALING_THR: return
        thr = np.percentile(self.act_count, 80)
        hot = np.where(self.act_count >= thr)[0]
        if len(hot) == 0: return
        sm = chem & (self.btype==2) & (np.isin(self.src, hot) | np.isin(self.tgt, hot))
        if sm.sum() == 0: return
        self.weight[sm] *= (1 - SCALING_RATE)
        deg = sm & (self.weight < 0.08)
        if deg.any():
            self.btype[deg] = 0
            self.Ea[deg] = Ea_S
        self.scaling_events += 1

    # ===== 胶质细胞修剪 =====
    def glia_modulation(self):
        chem = ~self.is_elec
        nb = chem.sum()
        el_r = np.sum((self.btype==2) & chem) / max(1, nb)
        if el_r < GLIA_THR: return 0
        el_bonds = np.where(chem & (self.btype==2))[0]
        if len(el_bonds) == 0: return 0
        n_degrade = max(1, int(len(el_bonds) * GLIA_RATE))
        top_idx = el_bonds[np.argsort(self.weight[el_bonds])[::-1][:n_degrade]]
        self.btype[top_idx] = 0
        self.Ea[top_idx] = Ea_S
        self.n_ltp[top_idx] = 0
        self.glia_events += 1
        return n_degrade

    # ===== 指标计算 =====
    def metrics(self):
        g = self.G
        if g.number_of_nodes() < 10:
            return 1.0, 0.0, 0.0, 0
        # sigma
        C_s = nx.average_clustering(g)
        n = g.number_of_nodes(); m = g.number_of_edges()
        p = 2*m/(n*(n-1)); C_r = max(p, 1e-6)
        try: L_s = nx.average_shortest_path_length(g)
        except: L_s = 5.0
        L_r = np.log(n) / np.log(max(2, n*p))
        sigma = (C_s / C_r) / (L_s / max(L_r, 0.1))
        return sigma, C_s, L_s, g.number_of_edges()

    def compute_alpha(self):
        sizes = np.array(self.avalanche_sizes[500:])
        sizes = sizes[sizes > 0]
        if len(sizes) < 20: return 0.0
        hist, bins = np.histogram(np.log10(sizes), bins=20)
        x = (bins[:-1] + bins[1:]) / 2
        y = np.log10(hist + 1)
        mask = ~np.isinf(y) & ~np.isnan(y)
        if mask.sum() < 3: return 0.0
        coeffs = np.polyfit(x[mask], y[mask], 1)
        return float(-coeffs[0])

    # ======================== v22 主循环 ========================

    # ===== v23: FEP basin tracking =====
    def fep_basin_update(self):
        for i in range(self.N):
            if abs(self.F_local[i]) < 1e-12: continue
            if self.F_local[i] < self.F_basin_min[i] * 0.99:
                self.F_basin_min[i] = self.F_local[i]
                self.F_basin_count[i] = 0
                self.F_converged[i] = False
            else:
                self.F_basin_count[i] += 1
                if self.F_basin_count[i] > FEP_BASIN_WINDOW:
                    self.F_converged[i] = True

    # ===== v23: FEP gradient with clipping =====
    def fep_gradient_clip(self):
        for i in range(self.N):
            out_mask = (self.src == i)
            if not out_mask.any():
                self.F_gradient[i] = 0.0; continue
            grad = 0.0; n_out = 0
            for j in np.where(out_mask)[0]:
                prediction = self.h[i] * self.weight[j]
                actual = self.h[self.tgt[j]]
                grad += 2.0 * (prediction - actual) * self.weight[j]
                n_out += 1
            self.F_gradient[i] = np.clip(grad / max(n_out,1), -FEP_GRAD_CLIP, FEP_GRAD_CLIP)

    # ===== v23: JEPA entropy regulation =====
    def jepa_entropy_regulation(self):
        if len(self.entropy_history) < 5: return
        recent_H = np.mean(self.entropy_history[-5:])
        error_H = recent_H - JEPA_TARGET_ENTROPY
        self.beta_eff = np.clip(
            JEPA_BETA_MIN + (JEPA_BETA_MAX - JEPA_BETA_MIN) *
            (1.0 / (1.0 + np.exp(-2.0 * error_H))),
            JEPA_BETA_MIN, JEPA_BETA_MAX)

    # ===== v23: FEP-modulated theta + connectivity-preserving state push =====
    def fep_modulate_theta(self):
        conv_rate = self.F_converged.mean()
        modulation = 1.0 - FEP_ATTRACTOR_STRENGTH * (conv_rate - 0.5)
        modulation = np.clip(modulation, 0.7, 1.3)
        self.theta_ltp_current = max(T_THETA_MIN,
            min(int(self.theta_ltp_current * modulation), T_THETA_MAX))
        # Connectivity-preserving FEP push on node states
        eta_fep = 0.015 * FEP_ATTRACTOR_STRENGTH
        for i in range(self.N):
            if self.F_converged[i]: continue
            out_deg = (self.src == i).sum()
            if out_deg < 3: continue
            if self.F_local[i] > self.F_basin_min[i] * 1.05:
                hub_scale = min(1.0, out_deg / 15.0)
                self.h[i] = np.clip(
                    self.h[i] - eta_fep * hub_scale * self.F_gradient[i],
                    0.0, 1.0)

    # ===== v23: global energy budget =====
    def energy_budget_check(self):
        total_energy = self.F_local.sum() + (self.Ea * self.weight**2).sum()
        if total_energy > GLOBAL_ENERGY_BUDGET:
            scale = GLOBAL_ENERGY_BUDGET / total_energy
            self.Ea *= (1.0 + scale) / 2.0
            self.Ea = np.clip(self.Ea, 0.005, Ea_L)


    def step(self):
        # 外部刺激：v23增加结构化外部数据输入
        if EXTERNAL_DRIVE:
            structured_spikes = self.structured_gen.sample(1)[0]
        else:
            structured_spikes = np.zeros(len(self.sensor_idx))

        # 构建刺激向量
        stim = np.zeros(self.N)
        # 感觉神经元：结构化脉冲 + 随机噪声
        n_sensor = max(1, int(len(self.sensor_idx) * SEED_FRAC_SENSOR))
        sensor_spike_mask = structured_spikes > 0.3
        spike_indices = np.where(sensor_spike_mask)[0]
        if len(spike_indices) > 0:
            driven = self.sensor_idx[spike_indices]
            stim[driven] = structured_spikes[spike_indices]
        # 补充随机驱动
        random_sensors = np.random.choice(self.sensor_idx, size=n_sensor, replace=False)
        stim[random_sensors] = np.maximum(stim[random_sensors],
                                          np.random.uniform(0.2, 0.8, n_sensor))
        # 其他神经元随机稀疏激活
        n_other = max(1, int(self.N * SEED_FRAC_OTHER))
        other_idx = np.random.choice(self.N, size=n_other, replace=False)
        stim[other_idx] = np.maximum(stim[other_idx],
                                     np.random.uniform(0.1, 0.3, n_other))

        # 不应期调制
        refractory = (self.t - self.last_fire) < T_ABS
        stim[refractory] *= REL_SCALE

        # 级联激活
        active = self.cascade(stim)

        # 突触疲劳恢复
        self.R = np.clip(self.R + 1.0/TAU_REC, 0.1, 1.0)
        active_edges = active[self.src] | active[self.tgt]
        self.R[active_edges] -= np.where(self.is_elec[active_edges], U_SE_ELEC, U_SE_CHEM)

        # STDP更新
        self.stdp_update(active)

        # v23: 自适应θ + 键固化（每10步计算一次，避免每微步都做全图遍历）
        if self.t % 10 == 0:
            if self.t % 10 == 0 or self.t < 5:
                self.theta_ltp_current = self.compute_adaptive_theta()
        self.apply_rules()

        # v23: FEP自由能计算
        self.compute_local_F()
        # v23: FEP basin + gradient + JEPA + theta + energy
        self.fep_basin_update()
        self.fep_gradient_clip()
        self.jepa_entropy_regulation()
        self.fep_modulate_theta()
        self.energy_budget_check()

        # 周期性维护
        if self.t > 0 and self.t % SCALING_INT == 0:
            self.synaptic_scaling()
        if self.t > 0 and self.t % GLIA_INT == 0:
            self.glia_modulation()
        if self.t > 0 and self.t % FEP_HOMEOSTASIS_INT == 0:
            self.fep_homeostasis()

        self.t += 1

    def run(self):
        print(f"\nv23仿真: {N_STEPS}步 | 自适应θ + FEP稳态 + 结构化数据驱动")
        print("-"*70)

        logs = {"step":[],"sigma":[],"alpha":[],"el_ratio":[],"bonds":[],
                "theta":[],"F_global":[],"L":[],"glia":[],"scaling":[]}

        for step in range(N_STEPS):
            self.t = step
            # 每个宏观步内5次微观脉冲
            for _ in range(5):
                self.step()

            if step % 50 == 0:
                self._rebuild()
                sigma, C, L, nb = self.metrics()
                alpha = self.compute_alpha()
                chem = ~self.is_elec
                el_ratio = float(np.sum((self.btype==2)&chem)) / max(chem.sum(), 1)
                F_global = float(self.F_local.mean()) if self.F_local.any() else 0

                logs["step"].append(step)
                logs["sigma"].append(sigma)
                logs["alpha"].append(alpha)
                logs["el_ratio"].append(el_ratio)
                logs["bonds"].append(nb)
                logs["theta"].append(self.theta_ltp_current)
                logs["F_global"].append(F_global)
                logs["L"].append(L)
                logs["glia"].append(self.glia_events)
                logs["scaling"].append(self.scaling_events)

                if step % 500 == 0:
                    print(f"  t={step:4d} θ={self.theta_ltp_current:3d} σ={sigma:.2f} "
                          f"α={alpha:.3f} EL={el_ratio*100:.1f}% F={F_global:.4f} L={L:.2f}")

        sigma, C, L, nb = self.metrics()
        alpha = self.compute_alpha()
        chem = ~self.is_elec
        el_ratio = float(np.sum((self.btype==2)&chem)) / max(chem.sum(), 1)
        F_final = float(self.F_local.mean())

        print(f"\nv22完成:")
        print(f"  σ={sigma:.3f} α={alpha:.3f} C={C:.3f} L={L:.3f} bonds={nb}")
        print(f"  EL={el_ratio*100:.1f}% F={F_final:.4f}")
        print(f"  Glia={self.glia_events} Scaling={self.scaling_events}")

        return logs, sigma, alpha, C, L, el_ratio, F_final

    def plot_results(self, logs, sigma, alpha, C, L, el_ratio, F_final):
        n_plots = 3; fig, axes = plt.subplots(2, 3, figsize=(18, 10))
        fig.suptitle("SDI v23 — 自适应θ节律 + FEP全局稳态 + 外部数据闭环",
                     fontsize=13, fontweight="bold")

        # 1. sigma & alpha
        ax = axes[0,0]
        ax.plot(logs["step"], logs["sigma"], "darkgreen", lw=1.5, label="σ")
        ax.axhline(4.0, color="green", ls="--", alpha=0.5, label="target σ≥4.0")
        ax2 = ax.twinx()
        ax2.plot(logs["step"], logs["alpha"], "coral", lw=1.5, label="α")
        ax2.axhline(2.0, color="red", ls="--", alpha=0.5, label="target α≤2.0")
        ax.set_title("σ & α"); ax.set_ylabel("σ", color="darkgreen")
        ax2.set_ylabel("α", color="coral")
        lines1, labels1 = ax.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax.legend(lines1+lines2, labels1+labels2, fontsize=7)

        # 2. E-L比率
        ax = axes[0,1]
        ax.plot(logs["step"], np.array(logs["el_ratio"])*100, "purple", lw=1.5)
        ax.axhline(EL_TARGET_LO*100, color="green", ls="--")
        ax.axhline(EL_TARGET_HI*100, color="green", ls="--")
        ax.set_title(f"E-L Ratio (final={el_ratio*100:.1f}%)")
        ax.set_ylabel("E-L %")

        # 3. 自适应θ
        ax = axes[0,2]
        ax.plot(logs["step"], logs["theta"], "steelblue", lw=1.5)
        ax.axhline(T_THETA_BASE, color="gray", ls=":", label=f"base={T_THETA_BASE}")
        ax.set_title("Adaptive Theta Period"); ax.set_ylabel("T_θ")
        ax.legend(fontsize=7)

        # 4. 自由能
        ax = axes[1,0]
        if logs["F_global"]:
            ax.plot(logs["step"], logs["F_global"], "darkred", lw=1.5)
        ax.set_title("Global Free Energy F"); ax.set_ylabel("F")
        ax.grid(True, alpha=0.3)

        # 5. 路径长度
        ax = axes[1,1]
        ax.plot(logs["step"], logs["L"], "darkblue", lw=1.5)
        ax.axhline(L_REF, color="gray", ls=":", label=f"C.elegans L={L_REF}")
        ax.set_title("Avg Path Length L"); ax.set_ylabel("L")
        ax.legend(fontsize=7)

        # 6. 雪崩尺寸分布
        ax = axes[1,2]
        sizes = np.array(self.avalanche_sizes[500:])
        sizes = sizes[sizes > 0]
        if len(sizes) > 5:
            ax.hist(np.log10(sizes), bins=20, color="indigo", edgecolor="white", alpha=0.85)
            ax.set_xlabel("log10(Size)"); ax.set_ylabel("Count")
            ax.set_title(f"Avalanche Distribution (α≈{alpha:.2f})")

        plt.tight_layout()
        plt.savefig(f"{OUT_DIR}/sdi_v23_main.png", dpi=150, bbox_inches="tight")
        plt.close()
        print(f"  主图已保存 → {OUT_DIR}/sdi_v23_main.png")

        # 保存日志
        results = {
            "version":"v22",
            "N":int(self.N),
            "final":{"sigma":sigma,"alpha":alpha,"C":C,"L":L,"el_ratio":el_ratio,"F_final":F_final},
            "logs":{k: [float(x) if isinstance(x,(np.floating,float)) else int(x) if isinstance(x,(np.integer,int)) else x for x in v]
                    for k,v in logs.items()},
            "glia_events":int(self.glia_events),
            "scaling_events":int(self.scaling_events)
        }
        with open(f"{OUT_DIR}/v23_results.json","w") as f:
            json.dump(results, f, indent=2)
        print(f"  结果已保存 → {OUT_DIR}/v23_results.json")

# ============ 运行 ============
if __name__ == "__main__":
    print("="*60)
    print("SDI v23 — 自适应θ + FEP稳态 + 外部数据闭环")
    print("="*60)
    sim = SDI_v23()
    logs, sigma, alpha, C, L, el_ratio, F_final = sim.run()
    sim.plot_results(logs, sigma, alpha, C, L, el_ratio, F_final)
    print("\nv22 完成！")
