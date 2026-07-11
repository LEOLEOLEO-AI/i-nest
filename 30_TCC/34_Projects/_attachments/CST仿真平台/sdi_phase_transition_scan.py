"""
SDI网络相变下确界扫描实验
目标：找到出现幂律临界相变（α→1.5）的最小节点数 N_min

方法：
  固定所有参数（k_ratio=k/N, p=0.12, 四原理规则），
  扫描 N = [10, 20, 30, 50, 80, 100, 150, 200, 279, 400, 600, 1000]
  对每个N：
    1. 初始化WS小世界（k = max(4, int(N*k_ratio))）
    2. 运行1000步（四原理+突触缩放）
    3. 记录：σ, α, C, L, E-L占比
    4. 判断是否达到临界态（α∈[1.2,2.5] AND σ≥3.0）

下确界判据：
  N_min = 使得α∈[1.2,2.5] AND σ≥3.0 的最小N
  （线虫N=279是生物学下确界，仿真找工程下确界）

文献参照：
  Beggs&Plenz 2003：皮层切片~60-100神经元就能观测到幂律
  Petermann et al 2009：~100神经元可见神经雪崩
  Haldeman&Beggs 2005：理论预测N_min≈50-100（有限尺寸效应）
"""

import numpy as np
import scipy.sparse as sp
import networkx as nx
import matplotlib
matplotlib.rcParams['font.family'] = 'DejaVu Sans'
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from collections import defaultdict
import warnings, time
warnings.filterwarnings('ignore')

# ============================================================
# 固定参数（与v5一致，文献确认值）
# ============================================================
K_RATIO     = 16.4 / 279   # 线虫k/N比（Varshney 2011）
P_REWIRE    = 0.12
THETA_LTP   = 30
THETA_LTD   = 8
T_DECAY     = 30000
Ea_S, Ea_L  = 0.15, 0.85
EI_RATIO    = 4.0
TAU_STDP    = 20.0
ETA_LTP, ETA_LTD = 0.015, 0.010
SCALING_THR = 0.60
SCALING_RATE= 0.06
SCALING_INT = 30
N_STEPS     = 1200          # 每个规模运行步数
SEED_FRAC   = 0.08          # 种子比例（提高到8%，让大雪崩有机会出现）
CASCADE_MAX = 15            # 增大级联深度

# 扫描的节点数列表
N_SCAN = [10, 20, 30, 50, 80, 100, 150, 200, 279, 400, 600, 1000]

# 临界态判据
ALPHA_LO, ALPHA_HI = 1.2, 2.5   # 允许范围（有限尺寸效应，允许稍宽）
SIGMA_MIN = 3.0

# ============================================================
# 轻量SDI网络（单次扫描用）
# ============================================================
class SDI_scan:
    def __init__(self, N):
        self.N = N
        self.t = 0
        k = max(4, min(int(N * K_RATIO), N-1))
        if k % 2 != 0: k += 1
        G = nx.watts_strogatz_graph(N, k, P_REWIRE, seed=42)
        edges = list(G.edges())
        M = len(edges)

        self.src  = np.array([e[0] for e in edges], np.int32)
        self.tgt  = np.array([e[1] for e in edges], np.int32)
        exc = np.random.random(M) < EI_RATIO/(EI_RATIO+1)
        self.btype = np.where(exc,0,1).astype(np.int8)
        self.weight= np.where(exc,np.random.uniform(0.3,0.7,M),
                              np.random.uniform(0.05,0.2,M))
        self.n_ltp = np.zeros(M,np.int32)
        self.n_ltd = np.zeros(M,np.int32)
        self.last_active = np.full(M,-99999,np.int32)
        self.Ea    = np.full(M,Ea_S)
        self.t_fire= np.full(N,-99999.0)
        self.act_count = np.zeros(N,np.int32)
        self.avalanche_sizes = []
        self._rebuild()

    def _rebuild(self):
        sign = np.where(np.isin(self.btype,[0,2]),1.0,-0.25)
        self.W = sp.csr_matrix(
            (self.weight*sign,(self.src.astype(int),self.tgt.astype(int))),
            shape=(self.N,self.N))

    def cascade(self, seeds):
        active = np.zeros(self.N,bool); active[seeds]=True
        self.t_fire[seeds]=float(self.t)
        all_a = active.copy()
        for step in range(CASCADE_MAX):
            sig = self.W @ active.astype(float)
            inh = max(0,(all_a.sum()/self.N-0.25)*3.5)
            prob= np.clip(sig*(1-inh),0,1)
            new = (prob>np.random.random(self.N))&(~all_a)
            if not new.any(): break
            self.t_fire[new]=float(self.t+step)
            self.act_count[new]+=1; all_a|=new; active=new
        self.avalanche_sizes.append(int(all_a.sum()))
        return all_a

    def stdp(self, am):
        nodes=np.where(am)[0]
        em=np.isin(self.src,nodes)|np.isin(self.tgt,nodes)
        if not em.any(): return
        idx=np.where(em)[0]
        dt=self.t_fire[self.src[idx]]-self.t_fire[self.tgt[idx]]
        ltp=(dt>0)&(dt<200)
        if ltp.any():
            self.weight[idx[ltp]]=np.clip(
                self.weight[idx[ltp]]+ETA_LTP*np.exp(-dt[ltp]/TAU_STDP),0,1)
            self.n_ltp[idx[ltp]]+=1
        ltd=(dt<0)&(dt>-200)
        if ltd.any():
            self.weight[idx[ltd]]=np.clip(
                self.weight[idx[ltd]]-ETA_LTD*np.exp(dt[ltd]/TAU_STDP),0,1)
            self.n_ltd[idx[ltd]]+=1
        self.last_active[idx]=self.t

    def synaptic_scaling(self):
        el_mask=self.btype==2
        if el_mask.sum()/max(1,len(self.btype))<SCALING_THR: return
        thr=np.percentile(self.act_count,80)
        hot=np.where(self.act_count>=thr)[0]
        if len(hot)==0: return
        sm=el_mask&(np.isin(self.src,hot)|np.isin(self.tgt,hot))
        self.weight[sm]*=(1-SCALING_RATE)
        deg=self.btype[sm&(self.weight<0.15)]; self.btype[sm&(self.weight<0.15)]=0
        self.Ea[sm&(self.weight<0.15)]=Ea_S

    def apply_rules(self):
        fix=(self.btype==0)&(self.n_ltp>=THETA_LTP)
        self.btype[fix]=2; self.Ea[fix]=Ea_L; self.n_ltp[fix]=0
        dec=(self.btype==2)&(self.t-self.last_active>T_DECAY)
        self.btype[dec]=0; self.Ea[dec]=Ea_S
        cut=((self.btype==1)&(self.n_ltd>=THETA_LTD))|\
            ((self.btype==0)&(self.weight<0.015)&(self.t-self.last_active>2000))
        keep=~cut
        self.src=self.src[keep]; self.tgt=self.tgt[keep]
        self.btype=self.btype[keep]; self.weight=self.weight[keep]
        self.n_ltp=self.n_ltp[keep]; self.n_ltd=self.n_ltd[keep]
        self.last_active=self.last_active[keep]; self.Ea=self.Ea[keep]
        deg=np.bincount(self.src,minlength=self.N)+\
            np.bincount(self.tgt,minlength=self.N)
        low=np.where(deg<max(2,int(self.N*K_RATIO)//2))[0]
        if len(low)>0:
            n_new=min(len(low)*2,50)
            ns=np.random.choice(low,n_new); nt=np.random.randint(0,self.N,n_new)
            v=ns!=nt; ns,nt=ns[v],nt[v]
            exc=np.random.random(len(ns))<EI_RATIO/(EI_RATIO+1)
            self.src=np.concatenate([self.src,ns])
            self.tgt=np.concatenate([self.tgt,nt])
            self.btype=np.concatenate([self.btype,np.where(exc,0,1).astype(np.int8)])
            self.weight=np.concatenate([self.weight,np.where(exc,
                np.random.uniform(0.1,0.4,len(ns)),
                np.random.uniform(0.03,0.15,len(ns)))])
            self.n_ltp=np.concatenate([self.n_ltp,np.zeros(len(ns),np.int32)])
            self.n_ltd=np.concatenate([self.n_ltd,np.zeros(len(ns),np.int32)])
            self.last_active=np.concatenate([self.last_active,
                                             np.full(len(ns),self.t,np.int32)])
            self.Ea=np.concatenate([self.Ea,np.full(len(ns),Ea_S)])

    def run(self):
        for step in range(N_STEPS):
            self.t=step
            for _ in range(5):
                n_s=max(1,int(self.N*SEED_FRAC))
                seeds=np.random.choice(self.N,n_s,replace=False)
                am=self.cascade(seeds); self.stdp(am)
            if step%SCALING_INT==0 and step>0: self.synaptic_scaling()
            if step%20==0: self.apply_rules(); self._rebuild()

    def metrics(self):
        # σ
        G=nx.Graph(); G.add_nodes_from(range(self.N))
        for s,t in zip(self.src.tolist(),self.tgt.tolist()): G.add_edge(s,t)
        if not nx.is_connected(G):
            G=G.subgraph(max(nx.connected_components(G),key=len)).copy()
        n=G.number_of_nodes()
        if n<6: return 1.0,None,0.0,0.0,0.0
        C=nx.average_clustering(G)
        try:
            L=nx.average_shortest_path_length(G)
        except:
            L=5.0
        m=G.number_of_edges(); p=2*m/(n*(n-1))
        Cr=max(p,1e-6); Lr=np.log(n)/np.log(max(2,n*p))
        sigma=(C/Cr)/(L/max(Lr,0.1))
        # α
        s=np.array(self.avalanche_sizes); s=s[s>=2]
        alpha=None
        if len(s)>=30:
            xm=max(2,int(np.percentile(s,15))); x=s[s>=xm]
            if len(x)>=10:
                alpha=float(1+len(x)/np.sum(np.log(x/(xm-0.5))))
        el=np.sum(self.btype==2)/max(1,len(self.btype))
        return sigma,alpha,C,L,el

# ============================================================
# 主扫描
# ============================================================
def run_scan():
    results = []
    print("="*70)
    print("SDI网络相变下确界扫描")
    print(f"N扫描: {N_SCAN}")
    print(f"判据: α∈[{ALPHA_LO},{ALPHA_HI}] AND σ≥{SIGMA_MIN}")
    print(f"线虫下确界: N=279 (Varshney 2011)")
    print("="*70)

    for N in N_SCAN:
        t0=time.time()
        np.random.seed(42)  # 固定随机种子保证可重复
        net=SDI_scan(N)
        k_actual=2*len(net.src)/N
        net.run()
        sigma,alpha,C,L,el=net.metrics()
        dt=time.time()-t0

        critical = (alpha is not None and
                    ALPHA_LO<=alpha<=ALPHA_HI and sigma>=SIGMA_MIN)
        sw_ok = sigma >= SIGMA_MIN

        a_str=f"{alpha:.3f}" if alpha else "None"
        flag = "🎯临界!" if critical else ("✓小世界" if sw_ok else "×")
        print(f"  N={N:5d}: σ={sigma:.3f} α={a_str:7s} "
              f"C={C:.3f} L={L:.3f} E-L={el:.1%} "
              f"k_avg={k_actual:.1f} [{dt:.1f}s] {flag}")

        results.append(dict(N=N, sigma=sigma, alpha=alpha,
                            C=C, L=L, el=el, critical=critical,
                            sw_ok=sw_ok, k_avg=k_actual, time=dt))

    return results

# ============================================================
# 绘图
# ============================================================
def plot_scan(results):
    Ns     = [r['N'] for r in results]
    sigmas = [r['sigma'] for r in results]
    alphas = [r['alpha'] if r['alpha'] else np.nan for r in results]
    Cs     = [r['C'] for r in results]
    Ls     = [r['L'] for r in results]
    els    = [r['el']*100 for r in results]
    crits  = [r['critical'] for r in results]
    sws    = [r['sw_ok'] for r in results]

    fig = plt.figure(figsize=(18,11))
    gs  = gridspec.GridSpec(2,3,figure=fig,hspace=0.38,wspace=0.32)
    fig.suptitle(
        'SDI Network Phase Transition Scan — Finding N_min (Lower Bound)\n'
        f'Fixed params: k/N={K_RATIO:.4f}(C.elegans ratio), p={P_REWIRE}, '
        f'θ_LTP={THETA_LTP}, θ_LTD={THETA_LTD}, Scaling={SCALING_THR:.0%}\n'
        f'Critical criterion: α∈[{ALPHA_LO},{ALPHA_HI}] AND σ≥{SIGMA_MIN}',
        fontsize=11,fontweight='bold')

    # 图1: σ vs N
    ax=fig.add_subplot(gs[0,0])
    colors=['green' if c else ('orange' if s else 'red')
            for c,s in zip(crits,sws)]
    ax.scatter(Ns,sigmas,c=colors,s=80,zorder=5)
    ax.plot(Ns,sigmas,'gray',lw=1,alpha=0.5)
    ax.axhline(SIGMA_MIN,color='orange',ls='--',lw=1.5,label=f'σ_min={SIGMA_MIN}')
    ax.axhline(5.87,color='green',ls=':',lw=1.5,label='C.elegans σ=5.87')
    ax.axvline(279,color='blue',ls='--',lw=1.5,alpha=0.7,label='C.elegans N=279')
    ax.set_xscale('log'); ax.set_xlabel('N (nodes, log scale)')
    ax.set_ylabel('σ (small-world coefficient)')
    ax.set_title('Small-World σ vs N')
    ax.legend(fontsize=7); ax.grid(True,alpha=0.3)

    # 图2: α vs N（幂律指数，临界态核心指标）
    ax=fig.add_subplot(gs[0,1])
    valid_N  = [N for N,a in zip(Ns,alphas) if not np.isnan(a)]
    valid_a  = [a for a in alphas if not np.isnan(a)]
    valid_col= [colors[i] for i,a in enumerate(alphas) if not np.isnan(a)]
    if valid_N:
        ax.scatter(valid_N,valid_a,c=valid_col,s=80,zorder=5)
        ax.plot(valid_N,valid_a,'gray',lw=1,alpha=0.5)
    ax.fill_between([min(Ns),max(Ns)],[ALPHA_LO]*2,[ALPHA_HI]*2,
                    alpha=0.15,color='green',label=f'Critical zone [{ALPHA_LO},{ALPHA_HI}]')
    ax.axhline(1.5,color='green',ls='--',lw=2,label='Beggs&Plenz α=1.5')
    ax.axvline(279,color='blue',ls='--',lw=1.5,alpha=0.7,label='C.elegans N=279')
    ax.set_xscale('log'); ax.set_xlabel('N (nodes, log scale)')
    ax.set_ylabel('Power-law exponent α')
    ax.set_title('Avalanche α vs N\n(α→1.5 = critical state)')
    ax.legend(fontsize=7); ax.grid(True,alpha=0.3)

    # 图3: C和L vs N
    ax=fig.add_subplot(gs[0,2])
    ax.semilogx(Ns,Cs,'b-o',ms=5,lw=1.5,label='C (clustering)')
    ax.semilogx(Ns,[l/10 for l in Ls],'r-s',ms=5,lw=1.5,label='L/10 (path length)')
    ax.axhline(0.337,color='blue',ls='--',lw=1,label='C.elegans C=0.337')
    ax.axhline(0.244,color='red',ls='--',lw=1,label='C.elegans L/10=0.244')
    ax.axvline(279,color='blue',ls='--',lw=1.5,alpha=0.7)
    ax.set_xlabel('N (nodes, log scale)')
    ax.set_ylabel('C  /  L/10')
    ax.set_title('Clustering C & Path Length L vs N')
    ax.legend(fontsize=7); ax.grid(True,alpha=0.3)

    # 图4: E-L骨架占比 vs N
    ax=fig.add_subplot(gs[1,0])
    ax.semilogx(Ns,els,'purple',lw=2,marker='o',ms=5)
    ax.axhline(60,color='red',ls='--',lw=1.5,label='Scaling trigger 60%')
    ax.axvline(279,color='blue',ls='--',lw=1.5,alpha=0.7,label='C.elegans N=279')
    ax.set_xlabel('N (nodes, log scale)')
    ax.set_ylabel('E-L bond ratio (%)')
    ax.set_title('Backbone Consolidation vs N\n(saturation = crystallization risk)')
    ax.legend(fontsize=7); ax.grid(True,alpha=0.3)

    # 图5: 相变相图（σ vs α，每个N一个点）
    ax=fig.add_subplot(gs[1,1])
    for i,(N,sigma,alpha) in enumerate(zip(Ns,sigmas,alphas)):
        if np.isnan(alpha): continue
        c = 'green' if crits[i] else ('orange' if sws[i] else 'red')
        ax.scatter(sigma,alpha,c=c,s=100,zorder=5)
        ax.annotate(f'N={N}',xy=(sigma,alpha),fontsize=6,
                    xytext=(2,2),textcoords='offset points')
    ax.fill_between([SIGMA_MIN,max(sigmas)+2],[ALPHA_LO]*2,[ALPHA_HI]*2,
                    alpha=0.15,color='green',label='Critical zone')
    ax.axvline(SIGMA_MIN,color='orange',ls='--',lw=1.5,label=f'σ≥{SIGMA_MIN}')
    ax.axhline(1.5,color='green',ls='--',lw=1.5,label='α=1.5')
    ax.set_xlabel('σ (small-world)'); ax.set_ylabel('α (power-law)')
    ax.set_title('Phase Diagram: σ vs α\n(green zone = critical state)')
    ax.legend(fontsize=7); ax.grid(True,alpha=0.3)

    # 图6: 结论摘要
    ax=fig.add_subplot(gs[1,2]); ax.axis('off')

    # 找下确界
    n_min_crit = next((r['N'] for r in results if r['critical']), None)
    n_min_sw   = next((r['N'] for r in results if r['sw_ok']), None)

    rows=[
        ('PHASE TRANSITION LOWER BOUND','black',11,True),
        ('','white',5,False),
        ('Criterion: α∈[1.2,2.5] AND σ≥3.0','gray',8,False),
        ('','white',4,False),
        (f'N_min (critical) = {n_min_crit if n_min_crit else "Not found"}',
         'green' if n_min_crit else 'red',10,True),
        (f'N_min (small-world only) = {n_min_sw if n_min_sw else "Not found"}',
         'orange',9,False),
        (f'C.elegans lower bound = 279','blue',9,False),
        ('','white',5,False),
        ('Per-N Results:','black',9,True),
    ]
    for r in results:
        a_s = f"{r['alpha']:.2f}" if r['alpha'] else "N/A"
        status = "🎯" if r['critical'] else ("✓" if r['sw_ok'] else "×")
        rows.append((f"  N={r['N']:4d}: σ={r['sigma']:.2f} α={a_s:5s} {status}",
                     'green' if r['critical'] else ('orange' if r['sw_ok'] else 'gray'),
                     8, False))
    rows += [
        ('','white',5,False),
        ('Literature reference:','black',9,True),
        ('Beggs&Plenz 2003: N~60-100 in vitro','gray',7,False),
        ('Petermann 2009: N~100 in vivo','gray',7,False),
        ('Haldeman&Beggs 2005: N_min≈50-100 theory','gray',7,False),
    ]

    y=0.98
    for txt,col,fs,bold in rows:
        ax.text(0.02,y,txt,transform=ax.transAxes,fontsize=fs,color=col,
                fontweight='bold' if bold else 'normal',va='top')
        y-=max(0.032,fs*0.004)

    out='/home/work/.openclaw/workspace/sdi_sim/sdi_phase_scan.png'
    plt.savefig(out,dpi=150,bbox_inches='tight')
    plt.close()
    print(f"\n✅ 相变扫描图: {out}")
    return out

# ============================================================
if __name__=='__main__':
    import os; os.makedirs('/home/work/.openclaw/workspace/sdi_sim',exist_ok=True)
    t_all=time.time()
    results=run_scan()

    # 找下确界
    n_min_crit=[r['N'] for r in results if r['critical']]
    n_min_sw  =[r['N'] for r in results if r['sw_ok']]
    print("\n"+"="*70)
    print("下确界结论:")
    print(f"  小世界(σ≥3.0)下确界: N_min = {min(n_min_sw) if n_min_sw else '未找到'}")
    print(f"  临界态(α+σ)下确界:   N_min = {min(n_min_crit) if n_min_crit else '未找到'}")
    print(f"  线虫生物学下确界:     N = 279 (Varshney 2011)")
    print(f"  总扫描耗时: {time.time()-t_all:.1f}s")

    plot_scan(results)
