"""
SDI网络仿真 v2 - 动态扇出 + 多步级联激活
修正：
  1. 每类型通道物理连线数Nᵢ动态变量（非固定4条）
  2. 多步级联激活（真实神经雪崩传播）
  3. 全局抑制反馈（防超临界）
  4. θ_LTD降为10（加速修剪，向α→1.5收敛）

文献参数：
  θ_LTP=50 (Frey&Morris 1997)
  θ_LTD=10 (修正值，加速稀疏修剪)
  T_decay=1e5, Ea_S=0.15, Ea_L=0.85
  E:I=4:1 (DeFelipe 2002)
  α_target=1.5 (Beggs&Plenz 2003)
"""

import numpy as np
import networkx as nx
import matplotlib
matplotlib.rcParams['font.family'] = 'DejaVu Sans'
import matplotlib.pyplot as plt
from collections import defaultdict
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# 确认参数
# ============================================================
THETA_LTP   = 50
THETA_LTD   = 10        # v2修正：从20降到10，加速修剪
T_DECAY     = 100000
Ea_S        = 0.15
Ea_L        = 0.85
EI_RATIO    = 4.0
ALPHA_TARGET = 1.5
K_BRANCH    = 0.05      # E-S侧支发芽系数
W_THRESHOLD = 0.5       # E-L权重分裂阈值
K_MAX       = 50        # 单节点最大扇出（Gen1仿真限制）

BOND_EL = 'E-L'
BOND_IL = 'I-L'
BOND_ES = 'E-S'
BOND_IS = 'I-S'

# ============================================================
# 化合键（支持多条同类型并行）
# ============================================================
class Bond:
    _id = 0
    def __init__(self, src, tgt, bond_type):
        self.bid = Bond._id; Bond._id += 1
        self.src = src
        self.tgt = tgt
        self.type = bond_type
        self.weight = (np.random.uniform(0.3, 0.7) * EI_RATIO/(EI_RATIO+1)
                       if bond_type in (BOND_EL, BOND_ES)
                       else np.random.uniform(0.05, 0.2))
        self.n_ltp = 0
        self.n_ltd = 0
        self.last_active = 0
        self.Ea = Ea_L if bond_type in (BOND_EL, BOND_IL) else Ea_S

# ============================================================
# SDI网络（动态扇出）
# ============================================================
class SDI_Network_v2:
    def __init__(self, n_nodes=200, p_initial=0.12, k_init=6):
        self.n = n_nodes
        self.t = 0
        # bonds: list of Bond（允许同(i,j)多条，不同类型）
        self.bonds = []
        self.avalanche_sizes = []
        self.t_fire = np.full(n_nodes, -9999, dtype=float)

        # 初始化WS小世界
        G = nx.watts_strogatz_graph(n_nodes, k_init, p_initial, seed=42)
        for i, j in G.edges():
            btype = BOND_ES if np.random.random() < EI_RATIO/(EI_RATIO+1) else BOND_IS
            self.bonds.append(Bond(i, j, btype))
        print(f"初始化: {n_nodes}节点, {len(self.bonds)}条化合键, "
              f"平均扇出k≈{2*len(self.bonds)/n_nodes:.1f}")

    # ----------------------------------------------------------
    # 邻接查询
    # ----------------------------------------------------------
    def _out_bonds(self, src):
        return [b for b in self.bonds if b.src == src]

    def _in_bonds(self, tgt):
        return [b for b in self.bonds if b.tgt == tgt]

    def _degree(self, node):
        return sum(1 for b in self.bonds if b.src == node or b.tgt == node)

    # ----------------------------------------------------------
    # STDP更新（Bi&Poo 1998，τ=20ms）
    # ----------------------------------------------------------
    def _stdp(self, bond):
        dt = self.t_fire[bond.src] - self.t_fire[bond.tgt]
        tau = 20.0
        if abs(dt) < 200:  # 时间窗口200步
            if dt > 0:     # 前→后，LTP
                dw = 0.012 * np.exp(-dt/tau)
                bond.weight = min(1.0, bond.weight + dw)
                bond.n_ltp += 1
            elif dt < 0:   # 后→前，LTD
                dw = 0.008 * np.exp(dt/tau)
                bond.weight = max(0.0, bond.weight - dw)
                bond.n_ltd += 1
        bond.last_active = self.t

    # ----------------------------------------------------------
    # 多步级联激活（真实神经雪崩）
    # ----------------------------------------------------------
    def _cascade(self, seed_nodes, max_steps=10):
        """
        模拟雪崩传播：每步激活节点向邻居传播，直到无新激活
        全局抑制反馈：激活比例超过30%时触发I-L抑制，防超临界
        """
        active = set(seed_nodes)
        all_active = set(seed_nodes)
        for s in seed_nodes:
            self.t_fire[s] = self.t

        for step in range(max_steps):
            new_active = set()
            total_active_ratio = len(all_active) / self.n

            # 全局抑制反馈（防超临界）
            global_inhibition = max(0, total_active_ratio - 0.3) * 2.0

            for i in list(active):
                for b in self._out_bonds(i):
                    if b.tgt in all_active:
                        continue
                    self._stdp(b)
                    if b.type in (BOND_EL, BOND_ES):
                        prob = b.weight * (1 - global_inhibition)
                    else:  # I键
                        prob = -b.weight * 0.3
                    if np.random.random() < max(0, prob):
                        new_active.add(b.tgt)
                        self.t_fire[b.tgt] = self.t + step

            if not new_active:
                break
            active = new_active
            all_active |= new_active

        avalanche_size = len(all_active)
        self.avalanche_sizes.append(avalanche_size)
        return avalanche_size

    # ----------------------------------------------------------
    # 动态扇出：轴突侧支发芽
    # ----------------------------------------------------------
    def _sprouting(self):
        """
        高权重E-L键发芽出新E-S分支
        对应生物轴突侧支发芽（axonal sprouting）
        """
        new_bonds = []
        node_degree = defaultdict(int)
        for b in self.bonds:
            node_degree[b.src] += 1
            node_degree[b.tgt] += 1

        for b in list(self.bonds):
            if b.type == BOND_EL and b.weight > W_THRESHOLD:
                if node_degree[b.src] < K_MAX:
                    # 发芽：建立新E-S键到随机邻居
                    candidates = [j for j in range(self.n)
                                  if j != b.src and j != b.tgt
                                  and node_degree[b.src] < K_MAX]
                    if candidates and np.random.random() < K_BRANCH:
                        j = np.random.choice(candidates)
                        new_b = Bond(b.src, j, BOND_ES)
                        new_b.weight = b.weight * 0.3  # 发芽初始权重
                        new_bonds.append(new_b)
                        node_degree[b.src] += 1
        self.bonds.extend(new_bonds)
        return len(new_bonds)

    # ----------------------------------------------------------
    # 化合键状态转换规则
    # ----------------------------------------------------------
    def _apply_rules(self):
        remove_ids = set()
        for b in self.bonds:
            # 规则1: E-S → E-L（固化）
            if b.type == BOND_ES and b.n_ltp >= THETA_LTP:
                b.type = BOND_EL
                b.Ea = Ea_L
                b.n_ltp = 0

            # 规则2: I-S → 断开（修剪）
            elif b.type == BOND_IS and b.n_ltd >= THETA_LTD:
                remove_ids.add(b.bid)

            # 规则3: 低权重E-S → 断开
            elif b.type == BOND_ES and b.weight < 0.05:
                if self.t - b.last_active > 1000:
                    remove_ids.add(b.bid)

            # 规则4: E-L衰减 → E-S
            elif b.type == BOND_EL and self.t - b.last_active > T_DECAY:
                b.type = BOND_ES
                b.Ea = Ea_S

            # 规则5: I-L保持（不衰减）

        self.bonds = [b for b in self.bonds if b.bid not in remove_ids]

        # 规则3补充: 新建E-S键（低度节点FEP驱动）
        node_degree = defaultdict(int)
        for b in self.bonds:
            node_degree[b.src] += 1
        for i in range(self.n):
            if node_degree[i] < 3 and np.random.random() < Ea_S:
                j = np.random.randint(0, self.n)
                if j != i:
                    self.bonds.append(Bond(i, j, BOND_ES))

    # ----------------------------------------------------------
    # 扇出统计
    # ----------------------------------------------------------
    def fanout_stats(self):
        out_deg = defaultdict(lambda: defaultdict(int))
        for b in self.bonds:
            out_deg[b.src][b.type] += 1
        all_k = [sum(d.values()) for d in out_deg.values()]
        if not all_k:
            return 0, 0, 0
        return np.mean(all_k), np.max(all_k), np.percentile(all_k, 95)

    # ----------------------------------------------------------
    # σ计算
    # ----------------------------------------------------------
    def compute_sigma(self):
        G = nx.Graph()
        G.add_nodes_from(range(self.n))
        for b in self.bonds:
            G.add_edge(b.src, b.tgt)
        if not nx.is_connected(G):
            G = G.subgraph(max(nx.connected_components(G), key=len)).copy()
        if G.number_of_nodes() < 10:
            return 1.0, 0.0, float('inf')
        C = nx.average_clustering(G)
        L = nx.average_shortest_path_length(G)
        n, m = G.number_of_nodes(), G.number_of_edges()
        p = 2*m / (n*(n-1))
        C_r = p
        L_r = np.log(n) / np.log(max(2, n*p))
        sigma = (C/max(C_r,1e-6)) / (L/max(L_r,1e-6))
        return sigma, C, L

    # ----------------------------------------------------------
    # 幂律拟合
    # ----------------------------------------------------------
    def fit_powerlaw(self):
        if len(self.avalanche_sizes) < 100:
            return None
        s = np.array(self.avalanche_sizes)
        s = s[s >= 2]
        if len(s) < 30:
            return None
        x_min = max(2, np.percentile(s, 20))
        x = s[s >= x_min]
        if len(x) < 10:
            return None
        return 1 + len(x) / np.sum(np.log(x/(x_min-0.5)))

    # ----------------------------------------------------------
    # 主循环
    # ----------------------------------------------------------
    def run(self, n_steps=800):
        print(f"\n运行 {n_steps} 步（多步级联激活 + 动态扇出）")
        logs = dict(step=[], sigma=[], alpha=[], bonds=[], el_ratio=[],
                    k_mean=[], k_max=[])

        for step in range(n_steps):
            self.t = step
            # 激活仿真（每步3次雪崩）
            for _ in range(3):
                seeds = np.random.choice(self.n, max(1, self.n//20), replace=False)
                self._cascade(seeds)

            # 键规则（每10步）
            if step % 10 == 0:
                self._apply_rules()

            # 侧支发芽（每50步）
            if step % 50 == 0:
                n_new = self._sprouting()

            # 记录
            if step % 40 == 0:
                sigma, C, L = self.compute_sigma()
                alpha = self.fit_powerlaw()
                nb = len(self.bonds)
                el = sum(1 for b in self.bonds if b.type == BOND_EL)
                k_mean, k_max, _ = self.fanout_stats()

                logs['step'].append(step)
                logs['sigma'].append(sigma)
                logs['alpha'].append(alpha or 0)
                logs['bonds'].append(nb)
                logs['el_ratio'].append(el/max(1,nb))
                logs['k_mean'].append(k_mean)
                logs['k_max'].append(k_max)

                a_str = f"{alpha:.3f}" if alpha else "N/A"
                print(f"  步{step:4d}: σ={sigma:.3f} | α={a_str} | "
                      f"键={nb} | E-L={el/max(1,nb):.1%} | "
                      f"k_mean={k_mean:.1f} | k_max={k_max}")

        return logs

# ============================================================
# 绘图
# ============================================================
def plot_results(net, logs, sigma_f, C_f, L_f, alpha_f):
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    fig.suptitle(
        'SDI Network v2 - Dynamic Fanout + Cascade Activation\n'
        f'theta_LTP={THETA_LTP}, theta_LTD={THETA_LTD}, '
        f'Ea_S={Ea_S}, Ea_L={Ea_L}, K_MAX={K_MAX}, N={net.n} nodes',
        fontsize=11, fontweight='bold')

    steps = logs['step']

    # 1. σ演化
    ax = axes[0,0]
    ax.plot(steps, logs['sigma'], 'b-o', ms=3, label='σ')
    ax.axhline(5.87, color='green', ls='--', lw=1.5, label='C.elegans 5.87')
    ax.axhline(4.0,  color='orange', ls='--', lw=1.5, label='Gen1 target 4.0')
    ax.set_title('Small-World σ Evolution')
    ax.set_xlabel('Step'); ax.set_ylabel('σ')
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    # 2. 幂律α演化
    ax = axes[0,1]
    alpha_vals = [v for v in logs['alpha'] if v > 0]
    alpha_steps = [s for s,v in zip(steps, logs['alpha']) if v > 0]
    if alpha_vals:
        ax.plot(alpha_steps, alpha_vals, 'r-o', ms=3, label='α')
        ax.fill_between(alpha_steps, [1.4]*len(alpha_steps), [1.6]*len(alpha_steps),
                        alpha=0.2, color='green', label='Target [1.4,1.6]')
        ax.axhline(1.5, color='green', ls='--', lw=1.5)
    ax.set_title('Avalanche Power-law α')
    ax.set_xlabel('Step'); ax.set_ylabel('α')
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    # 3. 动态扇出k_mean / k_max
    ax = axes[0,2]
    ax.plot(steps, logs['k_mean'], 'purple', lw=2, label='k_mean')
    ax.plot(steps, logs['k_max'],  'purple', lw=1, ls='--', label='k_max')
    ax.axhline(16.4, color='green', ls=':', lw=1.5, label='C.elegans k=16.4')
    ax.set_title('Dynamic Fanout Evolution\n(N-type channels, not fixed 4)')
    ax.set_xlabel('Step'); ax.set_ylabel('Fanout k')
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    # 4. E-L骨架固化进度
    ax = axes[1,0]
    ax.plot(steps, [v*100 for v in logs['el_ratio']], 'darkblue', lw=2)
    ax.set_title('Backbone Consolidation (E-L %)')
    ax.set_xlabel('Step'); ax.set_ylabel('E-L Ratio (%)')
    ax.grid(True, alpha=0.3)

    # 5. 雪崩分布
    ax = axes[1,1]
    if net.avalanche_sizes:
        s = np.array(net.avalanche_sizes)
        u, c = np.unique(s, return_counts=True)
        p = c / c.sum()
        ax.loglog(u, p, 'ko', ms=3, alpha=0.6, label='Observed')
        if alpha_f:
            xr = np.linspace(u.min(), u.max(), 50)
            yr = xr**(-alpha_f); yr /= yr.sum()
            ax.loglog(xr, yr, 'r--', lw=2, label=f'Fit α={alpha_f:.2f}')
            ax.loglog(xr, xr**(-1.5)/np.sum(xr**(-1.5)),
                      'g--', lw=1.5, label='Target α=1.5')
    ax.set_title('Avalanche Size Distribution')
    ax.set_xlabel('S'); ax.set_ylabel('P(S)')
    ax.legend(fontsize=8); ax.grid(True, alpha=0.3)

    # 6. 摘要
    ax = axes[1,2]
    ax.axis('off')
    bond_type_count = defaultdict(int)
    for b in net.bonds:
        bond_type_count[b.type] += 1
    total_b = sum(bond_type_count.values())
    k_mean_f, k_max_f, k95_f = net.fanout_stats()
    alpha_str = f"{alpha_f:.3f}" if alpha_f else "N/A"

    lines = [
        ('=== FINAL STATE ===',   'black', 11, True),
        ('',                       'black', 8,  False),
        (f'σ = {sigma_f:.3f}',    'green' if sigma_f>=4 else 'orange', 10, True),
        (f'  (target ≥4.0, C.elegans 5.87)', 'gray', 8, False),
        (f'α = {alpha_str}',
         'green' if alpha_f and 1.4<=alpha_f<=1.6 else 'orange', 10, True),
        (f'  (target 1.4-1.6)',   'gray', 8, False),
        (f'C = {C_f:.3f}  L = {L_f:.3f}', 'steelblue', 9, False),
        ('',                       'black', 8, False),
        ('=== FANOUT (Dynamic N) ===', 'black', 10, True),
        (f'k_mean = {k_mean_f:.1f}', 'navy', 9, False),
        (f'k_max  = {k_max_f}',    'navy', 9, False),
        (f'k_95th = {k95_f:.1f}', 'navy', 9, False),
        ('',                       'black', 8, False),
        ('=== BOND DISTRIBUTION ===', 'black', 10, True),
        (f'E-L: {bond_type_count[BOND_EL]} ({bond_type_count[BOND_EL]/max(1,total_b):.1%})',
         'navy', 9, False),
        (f'I-L: {bond_type_count[BOND_IL]} ({bond_type_count[BOND_IL]/max(1,total_b):.1%})',
         'darkred', 9, False),
        (f'E-S: {bond_type_count[BOND_ES]} ({bond_type_count[BOND_ES]/max(1,total_b):.1%})',
         'royalblue', 9, False),
        (f'I-S: {bond_type_count[BOND_IS]} ({bond_type_count[BOND_IS]/max(1,total_b):.1%})',
         'crimson', 9, False),
    ]
    y = 0.97
    for txt, col, fs, bold in lines:
        ax.text(0.02, y, txt, transform=ax.transAxes,
                fontsize=fs, color=col,
                fontweight='bold' if bold else 'normal', va='top')
        y -= 0.055

    plt.tight_layout()
    out = '/home/work/.openclaw/workspace/sdi_sim/sdi_v2_dynamic_fanout.png'
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\n✅ 图表保存: {out}")
    return out

# ============================================================
# 主程序
# ============================================================
if __name__ == '__main__':
    import os; os.makedirs('/home/work/.openclaw/workspace/sdi_sim', exist_ok=True)

    print("="*60)
    print("SDI网络仿真 v2 — 动态扇出 + 多步级联激活")
    print(f"θ_LTP={THETA_LTP} | θ_LTD={THETA_LTD} | T_decay={T_DECAY}")
    print(f"Ea_S={Ea_S} | Ea_L={Ea_L} | E:I={EI_RATIO}:1 | K_MAX={K_MAX}")
    print("="*60)

    net = SDI_Network_v2(n_nodes=200, p_initial=0.12, k_init=6)
    sigma0, C0, L0 = net.compute_sigma()
    print(f"初始: σ={sigma0:.3f}, C={C0:.3f}, L={L0:.3f}")

    logs = net.run(n_steps=800)

    sigma_f, C_f, L_f = net.compute_sigma()
    alpha_f = net.fit_powerlaw()
    k_mean_f, k_max_f, _ = net.fanout_stats()

    alpha_str = f"{alpha_f:.3f}" if alpha_f else "N/A"
    print("\n" + "="*60)
    print("最终结果:")
    print(f"  σ={sigma_f:.3f}  C={C_f:.3f}  L={L_f:.3f}")
    print(f"  α={alpha_str}  (目标1.4-1.6)")
    print(f"  k_mean={k_mean_f:.1f}  k_max={k_max_f}  (动态扇出)")
    print(f"  总化合键={len(net.bonds)}")

    out = plot_results(net, logs, sigma_f, C_f, L_f, alpha_f)
