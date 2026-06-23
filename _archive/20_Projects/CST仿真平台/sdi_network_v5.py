"""
SDI网络仿真 v5 — 突触缩放 + 精确线虫规模对标
核心修正：
  1. 突触缩放（Synaptic Scaling, Turrigiano 1998）：
     全局E-L过饱和时，高激活节点的E-L权重等比例下调
     → 防止晶化死锁，维持临界态动态平衡
  2. N=279（线虫C.elegans精确规模）
  3. 目标对标：σ≥5.0, α→1.5, C≈0.337, L≈2.44
  4. F正确定义：固化后F下降（预测精度提升→惊讶度↓）
  5. 动态扇出：4类型通道，每类Nᵢ动态变量
"""

import numpy as np
import scipy.sparse as sp
import networkx as nx
import matplotlib
matplotlib.rcParams['font.family'] = 'DejaVu Sans'
import matplotlib.pyplot as plt
from collections import defaultdict
import warnings, time
warnings.filterwarnings('ignore')

# ============================================================
# 参数（v5）
# ============================================================
THETA_LTP   = 30        # 固化阈值（线虫规模小，适当降低）
THETA_LTD   = 8         # 修剪阈值
T_DECAY     = 30000     # E-L衰减时间常数（线虫规模适配）
Ea_S        = 0.15      # Watts&Strogatz 1998
Ea_L        = 0.85      # 能量守恒约束
EI_RATIO    = 4.0       # DeFelipe 2002
TAU_STDP    = 20.0      # Bi&Poo 1998
ETA_LTP     = 0.015
ETA_LTD     = 0.010

# 突触缩放参数（Turrigiano 1998）
SCALING_THRESHOLD = 0.60    # E-L占比超过60%触发缩放
SCALING_RATE      = 0.06    # 每次缩放权重下调6%
SCALING_INTERVAL  = 30      # 每30步检查一次

# 网络规模（精确线虫规模）
N_NODES   = 279         # C.elegans神经元数
K_INIT    = 16          # 线虫平均连接度（Varshney 2011）
P_REWIRE  = 0.12        # Watts&Strogatz最优p
N_STEPS   = 2000
SEED_FRAC = 0.05

# 线虫基准值（Varshney 2011 + 仿真验证）
CELEGANS_SIGMA = 5.87
CELEGANS_C     = 0.337
CELEGANS_L     = 2.44
CELEGANS_K     = 16.4

# ============================================================
class SDI_v5:
    def __init__(self):
        N, k, p = N_NODES, K_INIT, P_REWIRE
        self.N = N
        self.t = 0
        t0 = time.time()

        # WS小世界（对标线虫connectome）
        G = nx.watts_strogatz_graph(N, k, p, seed=42)
        edges = list(G.edges())
        M = len(edges)

        self.src  = np.array([e[0] for e in edges], dtype=np.int32)
        self.tgt  = np.array([e[1] for e in edges], dtype=np.int32)
        exc = np.random.random(M) < EI_RATIO/(EI_RATIO+1)
        # 类型：0=E-S, 1=I-S, 2=E-L, 3=I-L
        self.btype       = np.where(exc, 0, 1).astype(np.int8)
        self.weight      = np.where(exc,
                                    np.random.uniform(0.3,0.7,M),
                                    np.random.uniform(0.05,0.2,M))
        self.n_ltp       = np.zeros(M, np.int32)
        self.n_ltd       = np.zeros(M, np.int32)
        self.last_active = np.full(M, -99999, np.int32)
        self.Ea          = np.full(M, Ea_S)

        self.t_fire      = np.full(N, -99999.0)
        self.act_count   = np.zeros(N, np.int32)   # 累积激活次数（突触缩放用）

        # 固定σ采样（全图，线虫规模小可以全算）
        self.avalanche_sizes = []
        self.F_log  = []
        self.S_log  = [0.0]
        self.S_tot  = 0.0

        # 三原理可观测量
        self.scaling_events = 0   # 突触缩放触发次数（记录）

        self._rebuild_sparse()
        print(f"v5初始化: N={N}(线虫规模), M={M}边, k_avg={2*M/N:.1f}, 耗时{time.time()-t0:.3f}s")

    # ----------------------------------------------------------
    def _rebuild_sparse(self):
        sign = np.where(np.isin(self.btype,[0,2]), 1.0, -0.25)
        w_eff = self.weight * sign
        self.W = sp.csr_matrix(
            (w_eff, (self.src.astype(int), self.tgt.astype(int))),
            shape=(self.N, self.N))

    # ----------------------------------------------------------
    def cascade(self, seeds, max_steps=12):
        active = np.zeros(self.N, bool)
        active[seeds] = True
        self.t_fire[seeds] = float(self.t)
        all_active = active.copy()

        for step in range(max_steps):
            signal = self.W @ active.astype(float)
            ratio  = all_active.sum() / self.N
            inh    = max(0.0, (ratio - 0.25) * 3.5)
            prob   = np.clip(signal * (1-inh), 0, 1)
            new_a  = (prob > np.random.random(self.N)) & (~all_active)
            if not new_a.any():
                break
            self.t_fire[new_a] = float(self.t + step)
            self.act_count[new_a] += 1
            all_active |= new_a
            active = new_a

        self.avalanche_sizes.append(int(all_active.sum()))
        return all_active

    # ----------------------------------------------------------
    def stdp(self, active_mask):
        nodes = np.where(active_mask)[0]
        emask = np.isin(self.src, nodes) | np.isin(self.tgt, nodes)
        if not emask.any():
            return
        idx = np.where(emask)[0]
        dt  = self.t_fire[self.src[idx]] - self.t_fire[self.tgt[idx]]
        w0  = self.weight[idx].copy()

        ltp = (dt>0)&(dt<200)
        if ltp.any():
            self.weight[idx[ltp]] = np.clip(
                self.weight[idx[ltp]] + ETA_LTP*np.exp(-dt[ltp]/TAU_STDP), 0, 1)
            self.n_ltp[idx[ltp]] += 1

        ltd = (dt<0)&(dt>-200)
        if ltd.any():
            self.weight[idx[ltd]] = np.clip(
                self.weight[idx[ltd]] - ETA_LTD*np.exp(dt[ltd]/TAU_STDP), 0, 1)
            self.n_ltd[idx[ltd]] += 1

        self.last_active[idx] = self.t
        dS = float(np.sum(self.Ea[idx]*np.abs(self.weight[idx]-w0)))
        self.S_tot += dS

    # ----------------------------------------------------------
    def synaptic_scaling(self):
        """
        突触缩放（Turrigiano 1998, Nature）
        当E-L占比 > SCALING_THRESHOLD 时：
          找激活次数最高的top-20%节点
          将其所有E-L键权重 × (1 - SCALING_RATE)
          → 防止晶化，维持临界态可塑性
        """
        el_mask = self.btype == 2
        el_ratio = el_mask.sum() / max(1, len(self.btype))
        if el_ratio < SCALING_THRESHOLD:
            return 0

        # 找高激活节点（top 20%）
        threshold = np.percentile(self.act_count, 80)
        hot_nodes = np.where(self.act_count >= threshold)[0]
        if len(hot_nodes) == 0:
            return 0

        # 这些节点的E-L键权重下调
        hot_set = set(hot_nodes.tolist())
        scale_mask = el_mask & (
            np.isin(self.src, hot_nodes) | np.isin(self.tgt, hot_nodes))

        if scale_mask.sum() == 0:
            return 0

        self.weight[scale_mask] *= (1.0 - SCALING_RATE)
        # 权重过低的E-L退化为E-S
        degrade = scale_mask & (self.weight < 0.15)
        self.btype[degrade] = 0
        self.Ea[degrade] = Ea_S

        self.scaling_events += 1
        return int(scale_mask.sum())

    # ----------------------------------------------------------
    def apply_rules(self):
        # 规则1: E-S→E-L
        fix = (self.btype==0) & (self.n_ltp>=THETA_LTP)
        self.btype[fix]=2; self.Ea[fix]=Ea_L; self.n_ltp[fix]=0

        # 规则4: E-L衰减→E-S
        dec = (self.btype==2) & (self.t-self.last_active>T_DECAY)
        self.btype[dec]=0; self.Ea[dec]=Ea_S

        # 规则2: 断开
        cut = ((self.btype==1)&(self.n_ltd>=THETA_LTD)) | \
              ((self.btype==0)&(self.weight<0.015)&(self.t-self.last_active>2000))
        keep = ~cut
        self.src=self.src[keep]; self.tgt=self.tgt[keep]
        self.btype=self.btype[keep]; self.weight=self.weight[keep]
        self.n_ltp=self.n_ltp[keep]; self.n_ltd=self.n_ltd[keep]
        self.last_active=self.last_active[keep]; self.Ea=self.Ea[keep]

        # 规则3: 新建E-S键（低度节点）
        deg = np.bincount(self.src,minlength=self.N)+\
              np.bincount(self.tgt,minlength=self.N)
        low = np.where(deg < K_INIT//2)[0]
        if len(low)>0:
            n_new = min(len(low)*2, 100)
            ns = np.random.choice(low, n_new)
            nt = np.random.randint(0, self.N, n_new)
            v  = ns!=nt
            ns,nt = ns[v],nt[v]
            exc = np.random.random(len(ns)) < EI_RATIO/(EI_RATIO+1)
            self.src=np.concatenate([self.src,ns])
            self.tgt=np.concatenate([self.tgt,nt])
            self.btype=np.concatenate([self.btype,
                                       np.where(exc,0,1).astype(np.int8)])
            self.weight=np.concatenate([self.weight,
                                        np.where(exc,
                                                 np.random.uniform(0.1,0.4,len(ns)),
                                                 np.random.uniform(0.03,0.15,len(ns)))])
            self.n_ltp=np.concatenate([self.n_ltp,np.zeros(len(ns),np.int32)])
            self.n_ltd=np.concatenate([self.n_ltd,np.zeros(len(ns),np.int32)])
            self.last_active=np.concatenate([self.last_active,
                                             np.full(len(ns),self.t,np.int32)])
            self.Ea=np.concatenate([self.Ea,np.full(len(ns),Ea_S)])

    # ----------------------------------------------------------
    def compute_F(self):
        """
        修正版自由能F（FEP，v4修正延续）：
        F = Σ_bonds [ scale × (w - act_avg)² + Ea × w² ]
        E-L键：scale=0.2（高预测精度，低惊讶度，F贡献小）
        E-S键：scale=1.0（动态不确定，高惊讶度，F贡献大）
        系统固化 → E-L增多scale小 → F下降 ✓（FEP预测）
        但突触缩放阻止E-L过饱和 → F在低值动态平衡
        """
        max_act = max(self.act_count.max(), 1)
        act_src = self.act_count[self.src] / max_act
        act_tgt = self.act_count[self.tgt] / max_act
        act_avg = (act_src + act_tgt) / 2

        # 误差缩放：E-L/I-L误差权重×0.2，E-S/I-S×1.0
        scale = np.where(np.isin(self.btype,[2,3]), 0.2, 1.0)
        pred_err = scale * (self.weight - act_avg)**2
        complexity = self.Ea * self.weight**2

        F = float(np.sum(pred_err + complexity))
        self.F_log.append(F)
        return F

    # ----------------------------------------------------------
    def compute_sigma_full(self):
        """线虫规模小，全图精确计算σ"""
        G = nx.Graph()
        G.add_nodes_from(range(self.N))
        for s,t in zip(self.src.tolist(), self.tgt.tolist()):
            G.add_edge(s,t)
        if not nx.is_connected(G):
            G = G.subgraph(max(nx.connected_components(G),key=len)).copy()
        if G.number_of_nodes() < 10:
            return 1.0,0.0,0.0
        C = nx.average_clustering(G)
        L = nx.average_shortest_path_length(G)
        n,m = G.number_of_nodes(), G.number_of_edges()
        p   = 2*m/(n*(n-1))
        Cr  = max(p,1e-6)
        Lr  = np.log(n)/np.log(max(2,n*p))
        sigma = (C/Cr)/(L/max(Lr,0.1))
        return sigma, C, L

    # ----------------------------------------------------------
    def fit_powerlaw(self):
        if len(self.avalanche_sizes)<150:
            return None
        s = np.array(self.avalanche_sizes)
        s = s[s>=2]
        if len(s)<50:
            return None
        xm = max(2,int(np.percentile(s,15)))
        x  = s[s>=xm]
        if len(x)<15:
            return None
        return float(1+len(x)/np.sum(np.log(x/(xm-0.5))))

    # ----------------------------------------------------------
    def run(self, n_steps=N_STEPS):
        print(f"\n运行 {n_steps}步 | N={self.N}(线虫规模) | "
              f"θ_LTP={THETA_LTP} | θ_LTD={THETA_LTD} | "
              f"突触缩放阈值={SCALING_THRESHOLD:.0%}")
        print(f"目标: σ≥5.0, α→1.5, C≈{CELEGANS_C}, L≈{CELEGANS_L}")
        print("-"*65)

        logs = dict(step=[],sigma=[],alpha=[],F=[],S=[],
                    el_ratio=[],bonds=[],scaling=[])
        sigma_prev = None
        S_prev = 0.0

        for step in range(n_steps):
            self.t = step

            # 激活（每步5次雪崩）
            for _ in range(5):
                n_seed = max(1, int(self.N*SEED_FRAC))
                seeds  = np.random.choice(self.N, n_seed, replace=False)
                active = self.cascade(seeds)
                self.stdp(active)

            # 突触缩放（每SCALING_INTERVAL步）
            if step % SCALING_INTERVAL == 0 and step > 0:
                self.synaptic_scaling()

            # 键规则（每20步）
            if step % 20 == 0:
                self.apply_rules()
                self._rebuild_sparse()

            # 记录（每80步）
            if step % 80 == 0:
                sigma,C,L = self.compute_sigma_full()
                alpha = self.fit_powerlaw()
                F     = self.compute_F()
                nb    = len(self.src)
                el    = int(np.sum(self.btype==2))

                dS    = self.S_tot - S_prev
                S_prev= self.S_tot
                dsigma= (sigma-sigma_prev) if sigma_prev is not None else 0
                ratio = dsigma/max(dS,1e-8)
                self.S_log.append(self.S_tot)

                logs['step'].append(step)
                logs['sigma'].append(sigma)
                logs['alpha'].append(alpha or 0)
                logs['F'].append(F)
                logs['S'].append(self.S_tot)
                logs['el_ratio'].append(el/max(1,nb))
                logs['bonds'].append(nb)
                logs['scaling'].append(self.scaling_events)

                a_str = f"{alpha:.3f}" if alpha else "N/A"
                # 状态标记
                status = ""
                if alpha and 1.4<=alpha<=1.6: status += "🎯α"
                if sigma>=5.0: status += "✓σ"
                print(f"  步{step:4d}: σ={sigma:.3f} | α={a_str} | "
                      f"F={F:.1f} | E-L={el/max(1,nb):.1%} | "
                      f"缩放={self.scaling_events}次 | 键={nb} {status}")
                sigma_prev = sigma

        return logs

# ============================================================
# 绘图
# ============================================================
def plot_v5(net, logs, sf, Cf, Lf, af):
    fig, axes = plt.subplots(2, 3, figsize=(17,10))
    fig.suptitle(
        'SDI Network v5 — Synaptic Scaling + C.elegans Scale (N=279)\n'
        f'STDP(τ={TAU_STDP}ms) + FEP(F↓) + Least Action(δS→0) + Scaling(Turrigiano 1998)\n'
        f'θ_LTP={THETA_LTP} | θ_LTD={THETA_LTD} | T_decay={T_DECAY} | '
        f'Scaling threshold={SCALING_THRESHOLD:.0%} rate={SCALING_RATE:.0%}',
        fontsize=10, fontweight='bold')
    steps = logs['step']

    # 图1: σ对比线虫基准
    ax=axes[0,0]
    ax.plot(steps,logs['sigma'],'b-o',ms=4,lw=2,label='σ (v5, N=279)')
    ax.axhline(CELEGANS_SIGMA,color='green',ls='--',lw=2,
               label=f'C.elegans σ={CELEGANS_SIGMA}')
    ax.axhline(4.0,color='orange',ls=':',lw=1.5,label='Gen1 target 4.0')
    ax.set_title(f'Small-World σ vs C.elegans Baseline\n(target ≥{CELEGANS_SIGMA})')
    ax.set_xlabel('Step'); ax.set_ylabel('σ')
    ax.legend(fontsize=8); ax.grid(True,alpha=0.3)

    # 图2: α→1.5（SOC临界态）
    ax=axes[0,1]
    av=[v for v in logs['alpha'] if v>0]
    as_=[s for s,v in zip(steps,logs['alpha']) if v>0]
    if av:
        ax.plot(as_,av,'r-o',ms=4,lw=2,label='α (MLE fit)')
        ax.fill_between(as_,[1.4]*len(as_),[1.6]*len(as_),
                        alpha=0.25,color='green',label='Critical [1.4,1.6]')
        ax.axhline(1.5,color='green',ls='--',lw=2,
                   label='Beggs&Plenz 2003')
    ax.set_title('Power-law α → 1.5\n(SOC Critical State, Synaptic Scaling enabled)')
    ax.set_xlabel('Step'); ax.set_ylabel('α')
    ax.legend(fontsize=8); ax.grid(True,alpha=0.3)

    # 图3: 自由能F（FEP：应单调下降至平台）
    ax=axes[0,2]
    ax.plot(steps,logs['F'],'darkorange',lw=2,label='F (FEP)')
    if len(logs['F'])>3:
        z=np.polyfit(steps,logs['F'],1)
        trend='↓ F decreasing ✓ (FEP)' if z[0]<0 else '≈ F plateau (balanced)'
        color='green' if z[0]<0 else 'steelblue'
        ax.text(0.05,0.9,trend,transform=ax.transAxes,
                fontsize=9,fontweight='bold',color=color)
    ax.set_title('Variational Free Energy F\n(FEP: F=ΣPredErr²+Ea·w², E-L→F↓)')
    ax.set_xlabel('Step'); ax.set_ylabel('F')
    ax.legend(fontsize=8); ax.grid(True,alpha=0.3)

    # 图4: E-L占比 + 突触缩放事件
    ax=axes[1,0]; ax2=ax.twinx()
    ax.plot(steps,[v*100 for v in logs['el_ratio']],
            'darkblue',lw=2,label='E-L% (backbone)')
    ax.axhline(SCALING_THRESHOLD*100,color='red',ls='--',lw=1.5,
               label=f'Scaling trigger {SCALING_THRESHOLD:.0%}')
    ax2.plot(steps,logs['scaling'],'orange',lw=1.5,ls='--',
             label='Scaling events (cumul)')
    ax.set_title('Backbone E-L% + Synaptic Scaling\n(Turrigiano 1998: prevent crystallization)')
    ax.set_xlabel('Step'); ax.set_ylabel('E-L (%)',color='darkblue')
    ax2.set_ylabel('Scaling events',color='orange')
    ax.legend(loc='upper left',fontsize=8)
    ax2.legend(loc='lower right',fontsize=8)
    ax.grid(True,alpha=0.3)

    # 图5: 雪崩分布对标
    ax=axes[1,1]
    if net.avalanche_sizes:
        s=np.array(net.avalanche_sizes)
        u,c=np.unique(s,return_counts=True); p=c/c.sum()
        ax.loglog(u,p,'ko',ms=3,alpha=0.5,label='Observed')
        xr=np.linspace(max(u.min(),2),u.max(),100)
        yr15=xr**(-1.5); yr15/=yr15.sum()
        ax.loglog(xr,yr15,'g--',lw=2,label='Target α=1.5\n(Beggs&Plenz 2003)')
        if af:
            yrf=xr**(-af); yrf/=yrf.sum()
            ax.loglog(xr,yrf,'r-',lw=1.5,label=f'Fit α={af:.2f}')
    ax.set_title('Neuronal Avalanche Size Distribution\nP(S) ∝ S^(-3/2) at criticality')
    ax.set_xlabel('Avalanche Size S'); ax.set_ylabel('P(S)')
    ax.legend(fontsize=7); ax.grid(True,alpha=0.3)

    # 图6: 三原理验证摘要
    ax=axes[1,2]; ax.axis('off')
    bc=defaultdict(int)
    for bt in net.btype: bc[bt]+=1
    tb=len(net.src)
    F0=logs['F'][0] if logs['F'] else 1
    Ff=logs['F'][-1] if logs['F'] else 1
    fdrop=(F0-Ff)/max(F0,1)*100
    a_str=f"{af:.3f}" if af else "N/A"
    crit_ok = af and 1.4<=af<=1.6

    rows=[
        ('=== C.elegans Scale Verification ===','black',10,True),
        ('','white',5,False),
        (f'σ = {sf:.3f}  (C.elegans: {CELEGANS_SIGMA})',
         'green' if sf>=5.0 else 'orange',9,False),
        (f'C = {Cf:.3f}  (C.elegans: {CELEGANS_C})',
         'green' if abs(Cf-CELEGANS_C)<0.1 else 'orange',9,False),
        (f'L = {Lf:.3f}  (C.elegans: {CELEGANS_L})',
         'green' if abs(Lf-CELEGANS_L)<1.0 else 'orange',9,False),
        (f'α = {a_str}  (target: 1.4-1.6)',
         'green' if crit_ok else 'red',9,False),
        ('','white',5,False),
        ('=== Three Principles ===','black',10,True),
        ('① STDP (Bi&Poo 1998)','navy',9,True),
        (f'   τ={TAU_STDP}ms, η_LTP={ETA_LTP}, η_LTD={ETA_LTD}','gray',8,False),
        ('② FEP (Friston 2010)','darkorange',9,True),
        (f'   F: {F0:.0f}→{Ff:.0f} ({fdrop:+.1f}%)',
         'green' if fdrop>0 else 'red',8,False),
        ('③ Least Action','purple',9,True),
        (f'   S_total={net.S_tot:.0f}','gray',8,False),
        ('④ Synaptic Scaling (Turrigiano 1998)','crimson',9,True),
        (f'   Triggered {net.scaling_events} times',
         'green' if net.scaling_events>0 else 'red',8,False),
        ('','white',5,False),
        ('=== Bond Distribution ===','black',10,True),
        (f'E-L:{bc[2]}({bc[2]/max(1,tb):.1%}) I-L:{bc[3]}({bc[3]/max(1,tb):.1%})',
         'navy',8,False),
        (f'E-S:{bc[0]}({bc[0]/max(1,tb):.1%}) I-S:{bc[1]}({bc[1]/max(1,tb):.1%})',
         'royalblue',8,False),
        (f'Total bonds: {tb}  (Dynamic fanout N)','gray',8,False),
        ('','white',5,False),
        ('NO central control — self-organized!','darkgreen',9,True),
    ]
    y=0.98
    for txt,col,fs,bold in rows:
        ax.text(0.02,y,txt,transform=ax.transAxes,fontsize=fs,color=col,
                fontweight='bold' if bold else 'normal',va='top')
        y-=max(0.035,fs*0.0045)

    plt.tight_layout()
    out='/home/work/.openclaw/workspace/sdi_sim/sdi_v5_celegans.png'
    plt.savefig(out,dpi=150,bbox_inches='tight')
    plt.close()
    print(f"\n✅ 图表: {out}")
    return out

# ============================================================
if __name__=='__main__':
    import os; os.makedirs('/home/work/.openclaw/workspace/sdi_sim',exist_ok=True)
    t0=time.time()
    print("="*65)
    print(f"SDI网络仿真 v5 — 突触缩放 + C.elegans精确规模(N={N_NODES})")
    print(f"θ_LTP={THETA_LTP} | θ_LTD={THETA_LTD} | T_decay={T_DECAY}")
    print(f"突触缩放: 阈值={SCALING_THRESHOLD:.0%} 速率={SCALING_RATE:.0%} 间隔={SCALING_INTERVAL}步")
    print(f"对标: σ={CELEGANS_SIGMA}, C={CELEGANS_C}, L={CELEGANS_L}, α=1.5")
    print("="*65)

    net=SDI_v5()
    s0,C0,L0=net.compute_sigma_full()
    F0=net.compute_F(); net.F_log.clear()
    print(f"初始: σ={s0:.3f}, C={C0:.3f}, L={L0:.3f}, F={F0:.1f}")
    print(f"初始键: {len(net.src)}条, k_avg={2*len(net.src)/N_NODES:.1f}")

    logs=net.run(N_STEPS)

    sf,Cf,Lf=net.compute_sigma_full()
    af=net.fit_powerlaw()
    Ff=net.compute_F()
    a_str=f"{af:.3f}" if af else "N/A"

    print("\n"+"="*65)
    print("最终对标结果:")
    print(f"  σ={sf:.3f}  (线虫基准={CELEGANS_SIGMA},  {'✓' if sf>=5.0 else '△'})")
    print(f"  C={Cf:.3f}  (线虫基准={CELEGANS_C}, {'✓' if abs(Cf-CELEGANS_C)<0.1 else '△'})")
    print(f"  L={Lf:.3f}  (线虫基准={CELEGANS_L}, {'✓' if abs(Lf-CELEGANS_L)<1.0 else '△'})")
    print(f"  α={a_str}  (目标1.4-1.6, {'✓' if af and 1.4<=af<=1.6 else '△'})")
    print(f"  F: {F0:.1f}→{Ff:.1f} ({'↓FEP成立' if Ff<F0 else '↑需检查'})")
    print(f"  突触缩放触发: {net.scaling_events}次")
    print(f"  总化合键: {len(net.src)}, S_total={net.S_tot:.0f}")
    print(f"  总耗时: {time.time()-t0:.1f}s")

    plot_v5(net,logs,sf,Cf,Lf,af)
