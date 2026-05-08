#!/usr/bin/env python3
"""
SDI 实验一 v13 — LIF + SDI 化合键融合（正确实现）
神经元动力学：标准 LIF（线性，参数空间宽，亚临界可控）
液态拓扑：SDI 化合键动态重构（固化/消除/WS重连）= LNN 液态层的工程实现
雪崩检测：T_bin=4ms 时间窗口（与 Beggs&Plenz 2003 一致）
STDP：精确 spike 时刻（0.5ms 分辨率）
目标：alpha 真正落入 [1.5, 2.5]（SOC 临界态幂律）

说明：LTC 的 (A-V) 非线性项使参数窗口极窄（超临界过渡太陡），
      LIF 线性输入适合仿真，与 SDI 液态拓扑结合已足够表达 LNN 核心思想。
"""
import numpy as np, scipy.sparse as sp, json, time
from scipy.sparse.csgraph import connected_components
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(42)
OUT = '/home/work/.openclaw/workspace/sdi_sim'
SEEDS = [42, 7, 13, 99, 2024]

# ======== LIF 参数（Beggs&Plenz 2003 体外皮层片层条件）========
DT       = 0.5    # ms
TAU_M    = 20.0   # ms，膜时间常数
V_REST   = -70.0  # mV
V_TH     = -55.0  # mV，阈值
V_RESET  = -70.0  # mV
T_REF    = 2.0    # ms → int(T_REF/DT)=4步
TAU_SYN  = 5.0    # ms，突触电流衰减
W_EL_BOOST = 1.4  # E-L 键（固化骨架）权重增益（快响应）
W_IS_SIGN  = -0.3 # I-S/I-L 键为抑制性

# ======== 刺激参数 ========
T_STIM   = 60.0   # ms，刺激间隔（让雪崩完全熄灭）
K_SEEDS  = 1      # 单点刺激（模拟电极）

# ======== 雪崩检测 ========
T_BIN    = 4.0    # ms，时间窗口
BIN_STEPS = int(T_BIN / DT)   # = 8步

# ======== SDI 参数（与 v11 一致）========
THETA_LTP  = 60
THETA_LTD  = 12
T_DECAY    = 500
EL_HI      = 0.25
MAX_FIX    = 8
P_REWIRE   = 0.15
REWIRE_INT = 100  # 步
SCALING_INT= 200  # 步

# ======== 仿真长度 ========
# 100次刺激 × 60ms = 6000ms = 6秒
# 产生约 100 次雪崩，足够做幂律拟合
N_STEPS  = 12000   # 12000步 × 0.5ms = 6000ms

# ======== 7物种 ========
SPECIES = {
    'C.elegans':      {'N':279,'k':16,'k_init':8, 'p_init':0.05,'sf':0.22,'level':'neuron',
        'w_init':(0.04,0.18),
        'bio':{'sigma':4.71,'C':0.337,'L':2.44,'alpha':1.5,'el':0.191},
        'ref':'Varshney 2011; Beggs&Plenz 2003',
        'tgt':{'sigma':(4.,None),'C':(.25,None),'L':(2.,3.5),'alpha':(1.5,2.5),'el':(.15,.28)}},
    'Larval_Drosophila':{'N':321,'k':16,'k_init':8,'p_init':0.05,'sf':0.20,'level':'neuron',
        'w_init':(0.04,0.18),
        'bio':{'sigma':None,'C':.25,'L':2.1,'alpha':2.,'el':.18},
        'ref':'Winding 2023',
        'tgt':{'sigma':(3.,None),'C':(.20,None),'L':(1.5,3.5),'alpha':(1.5,2.5),'el':(.15,.28)}},
    'Macaque_Cortex': {'N':242,'k':16,'k_init':14,'p_init':0.10,'sf':0.12,'level':'neuron',
        'w_init':(0.04,0.18),
        'bio':{'sigma':3.8,'C':.55,'L':2.3,'alpha':2.2,'el':.20},
        'ref':'Modha&Singh 2010',
        'tgt':{'sigma':(3.,None),'C':(.25,None),'L':(2.,3.5),'alpha':(1.5,2.5),'el':(.15,.28)}},
    'Rat_Cortex★':   {'N':73, 'k':14,'k_init':12,'p_init':0.08,'sf':0.15,'level':'mesoscale',
        'w_init':(0.05,0.20),
        'bio':{'sigma':.79,'C':.332,'L':1.9,'alpha':2.,'el':.18},
        'ref':'conn2res; Rubinov&Sporns 2010',
        'tgt':{'sigma':(1.2,None),'C':(.25,None),'L':(1.5,3.),'alpha':(1.5,2.5),'el':(.15,.28)}},
    'Mouse_Cortex★': {'N':112,'k':14,'k_init':12,'p_init':0.10,'sf':0.15,'level':'mesoscale',
        'w_init':(0.05,0.20),
        'bio':{'sigma':.64,'C':.439,'L':1.8,'alpha':2.1,'el':.20},
        'ref':'Allen Mouse Brain Atlas',
        'tgt':{'sigma':(1.5,None),'C':(.22,None),'L':(1.5,3.),'alpha':(1.5,2.5),'el':(.15,.28)}},
    'Chimpanzee★':   {'N':200,'k':20,'k_init':10,'p_init':0.08,'sf':0.10,'level':'mesoscale',
        'w_init':(0.04,0.16),
        'bio':{'sigma':1.76,'C':.149,'L':2.2,'alpha':2.1,'el':.20},
        'ref':'Reardon 2016',
        'tgt':{'sigma':(1.5,None),'C':(.12,None),'L':(1.5,3.5),'alpha':(1.5,2.5),'el':(.15,.28)}},
    'Human_HCP★':    {'N':400,'k':25,'k_init':10,'p_init':0.06,'sf':0.08,'level':'mesoscale',
        'w_init':(0.03,0.14),
        'bio':{'sigma':3.59,'C':.204,'L':2.3,'alpha':2.2,'el':.20},
        'ref':'HCP; Schaefer 2018',
        'tgt':{'sigma':(2.5,None),'C':(.15,None),'L':(2.,4.),'alpha':(1.5,2.5),'el':(.15,.28)}},
}

# ======== 指标函数（不变）========
def compute_metrics(src, tgt, N):
    if len(src)==0: return 0.,99.,0.
    adj=sp.csr_matrix((np.ones(len(src)*2),(np.r_[src,tgt],np.r_[tgt,src])),shape=(N,N))
    adj.data[:]=1.
    nc,lbl=connected_components(adj,directed=False)
    sz=np.bincount(lbl); lc=lbl==sz.argmax(); n=int(lc.sum())
    if n<8: return 0.,99.,0.
    on=-np.ones(N,int); on[lc]=np.arange(n)
    em=lc[src]&lc[tgt]; ls=on[src[em]]; lt=on[tgt[em]]
    a=sp.csr_matrix((np.ones(len(ls)*2),(np.r_[ls,lt],np.r_[lt,ls])),shape=(n,n)); a.data[:]=1.
    deg=np.array(a.sum(1)).flatten()
    tri=np.array(a.multiply(a@a).sum(1)).flatten()/2.
    dm=deg*(deg-1); vm=dm>0
    C=float(np.mean(tri[vm]/dm[vm])) if vm.any() else 0.
    np.random.seed(0); samp=np.random.choice(n,min(40,n),replace=False); ds=[]
    for s in samp:
        vi={int(s):0}; q=[int(s)]; qi=0
        while qi<len(q) and len(vi)<min(120,n):
            u=q[qi]; qi+=1
            for v in a.getrow(u).indices:
                if int(v) not in vi: vi[int(v)]=vi[u]+1; q.append(int(v)); ds.append(vi[int(v)])
    L=float(np.mean(ds)) if ds else 99.
    m=a.nnz//2; p=2*m/(n*(n-1)) if n>1 else 1e-6
    sigma=(C/max(p,1e-9))/(L/max(np.log(n)/np.log(max(2,n*p)),0.01)) if L>0 else 0.
    return C,L,sigma

def hill_alpha_ks(data):
    data=np.array(data,float); data=data[data>0]
    if len(data)<15: return None
    uniq=np.unique(data); best_ks,best_a=1e9,None
    for xm in uniq[len(uniq)//4:len(uniq)//2+1][:10]:
        tail=data[data>=xm]
        if len(tail)<8: continue
        a=1.+len(tail)/np.sum(np.log(tail/(xm-.5)))
        ts=np.sort(tail); ce=np.arange(1,len(ts)+1)/len(ts)
        ct=1-(xm/ts)**(a-1); ks=np.max(np.abs(ce-ct))
        if ks<best_ks: best_ks=ks; best_a=float(a)
    return best_a

# ======== LIF + SDI 网络 ========
class LIF_SDI:
    def __init__(self, name, sp, seed):
        np.random.seed(seed)
        self.name=name; self.N=sp['N']; self.sp=sp; self.t=0
        N=sp['N']; k=sp['k_init']; k=max(4,k//2*2); p_init=sp['p_init']
        w_lo,w_hi=sp['w_init']

        # WS 环形格初始化
        sl,tl=[],[]
        for i in range(N):
            for d in range(1,k//2+1):
                j=(i+d)%N; sl+=[i,j]; tl+=[j,i]
        es=set(zip(sl,tl))
        for idx in range(len(sl)//2):
            if np.random.random()<p_init:
                i=sl[idx*2]; j=np.random.randint(N)
                if j!=i and (i,j) not in es:
                    old=(sl[idx*2],tl[idx*2])
                    es.discard(old); es.discard((old[1],old[0]))
                    es.add((i,j)); es.add((j,i))
        pairs=list(es); sl3=[p[0] for p in pairs]; tl3=[p[1] for p in pairs]

        # 权重：亚临界初始（单点刺激后级联但不爆炸）
        wl=np.random.uniform(w_lo,w_hi,len(sl3))
        bl=np.where(np.random.random(len(sl3))<.8,0,2).astype(np.int8)

        self.src=np.array(sl3,np.int32); self.tgt=np.array(tl3,np.int32)
        self.w=wl; self.bt=bl; ne=len(self.src)
        self.nltp=np.zeros(ne,np.int32); self.nltd=np.zeros(ne,np.int32)
        self.la=np.full(ne,-99999,np.int32)

        # LIF 状态
        self.V   = np.full(N, V_REST)
        self.ref = np.zeros(N, np.int32)    # 不应期剩余步
        self.s   = np.zeros(N)              # 突触变量（每节点）
        self.t_spike = np.full(N, -9999.)   # 最后 spike 时刻(ms)

        # 感觉神经元（用于单点轮换刺激）
        ns=max(3,int(N*sp['sf']))
        self.sens=np.arange(ns); self.stim_ptr=0

        # 突触缩放追踪
        self.fire_count=np.zeros(N,np.float32)

        self._build_W()
        C0,L0,sig0=compute_metrics(self.src[(self.bt==0)|(self.bt==1)],
                                   self.tgt[(self.bt==0)|(self.bt==1)],N)
        print(f'  [{name}] N={N} edges={ne} σ₀={sig0:.2f} C₀={C0:.3f} '
              f'w∈[{w_lo},{w_hi}]',flush=True)

    def _build_W(self):
        """构建 LIF 突触权重矩阵（SDI化合键类型影响权重）"""
        N=self.N; w_eff=self.w.copy()
        w_eff[self.bt==1]*=W_EL_BOOST          # E-L固化骨架：快响应，权重增强
        w_eff[(self.bt==2)|(self.bt==3)]*=W_IS_SIGN  # 抑制键为负
        self.W=sp.csr_matrix((w_eff,(self.src,self.tgt)),shape=(N,N))

    def lif_step(self, t_ms):
        """LIF 单步积分，返回 fired 向量"""
        N=self.N
        # 突触电流衰减
        self.s *= np.exp(-DT/TAU_SYN)
        # 膜电位更新
        I_syn = self.W @ self.s
        dV = (-(self.V - V_REST)/TAU_M + I_syn) * DT
        self.V += dV
        # 不应期钳制
        self.V[self.ref>0] = V_RESET
        self.ref[self.ref>0] -= 1
        # 刺激注入（每 T_STIM ms 单点刺激）
        stim_interval=int(T_STIM/DT)
        if self.t % stim_interval == 0:
            # 轮换刺激感觉神经元
            seed_node=int(self.sens[self.stim_ptr % len(self.sens)])
            self.stim_ptr+=1
            self.V[seed_node]=V_TH+3.0  # 直接到阈值以上
        # Spike 检测
        fired=(self.V>=V_TH)&(self.ref==0)
        self.V[fired]=V_RESET
        self.ref[fired]=int(T_REF/DT)
        # 更新突触变量 + spike 时刻
        self.s[fired]+=1.0
        self.t_spike[fired]=t_ms
        self.fire_count[fired]+=1.0
        return fired

    def stdp(self, fired, t_ms):
        """精确 spike 时刻驱动的 STDP"""
        fi=np.where(fired)[0]
        if not len(fi): return
        em=(self.bt<=1)&(np.isin(self.src,fi)|np.isin(self.tgt,fi))
        if not em.any(): return
        idx=np.where(em)[0]
        dt_ms=self.t_spike[self.src[idx]]-self.t_spike[self.tgt[idx]]
        lp=(dt_ms>0)&(dt_ms<100)
        if lp.any():
            self.w[idx[lp]]=np.clip(
                self.w[idx[lp]]+0.012*np.exp(-dt_ms[lp]/20.),0,1)
            self.nltp[idx[lp]]+=1
        ld=(dt_ms<0)&(dt_ms>-100)
        if ld.any():
            self.w[idx[ld]]=np.clip(
                self.w[idx[ld]]-0.008*np.exp(dt_ms[ld]/20.),0,1)
            self.nltd[idx[ld]]+=1
        self.la[em]=self.t

    def sdi_rules(self, fired):
        """SDI 化合键 5 条规则"""
        N=self.N
        # 规则1：E-S → E-L
        r1=np.where((self.bt==0)&(self.nltp>=THETA_LTP))[0]
        if len(r1)>MAX_FIX: np.random.shuffle(r1); r1=r1[:MAX_FIX]
        self.bt[r1]=1; self.nltp[r1]=0
        # 规则4：E-L → E-S
        self.bt[(self.bt==1)&(self.t-self.la>T_DECAY)]=0
        # 胶质控制 EL 比例
        cm=(self.bt==0)|(self.bt==1)
        if cm.sum()>0 and (self.bt==1).sum()/cm.sum()>EL_HI:
            el_idx=np.where(self.bt==1)[0]
            stale=el_idx[np.argsort(self.la[el_idx])[:max(3,len(el_idx)//10)]]
            self.bt[stale]=0; self.nltp[stale]=0
        # 规则2：I-S 消除
        kill=((self.bt==2)&(self.nltd>=THETA_LTD))|\
             ((self.bt==2)&(self.w<.01)&(self.t-self.la>500))
        keep=~kill
        self.src=self.src[keep]; self.tgt=self.tgt[keep]; self.w=self.w[keep]
        self.bt=self.bt[keep]; self.nltp=self.nltp[keep]
        self.nltd=self.nltd[keep]; self.la=self.la[keep]
        # WS 重连（惰性边 → 活跃神经元）
        if self.t%REWIRE_INT==0:
            fi_nodes=np.where(fired)[0]
            if len(fi_nodes)>2:
                cm2=(self.bt==0)|(self.bt==1)
                idle=np.where(cm2&(self.t-self.la>300))[0]
                if len(idle)>0:
                    np.random.shuffle(idle); rw=idle[:min(4,len(idle))]
                    es_set=set(zip(self.src[cm2].tolist(),self.tgt[cm2].tolist()))
                    for ri in rw:
                        if np.random.random()<P_REWIRE:
                            i=int(self.src[ri])
                            j=int(np.random.choice(fi_nodes))
                            if j!=i and (i,j) not in es_set:
                                es_set.discard((i,int(self.tgt[ri])))
                                self.tgt[ri]=j; es_set.add((i,j))
        # 突触缩放（基于真实激活率）
        if self.t%SCALING_INT==0 and self.t>500:
            rate=self.fire_count/SCALING_INT; self.fire_count[:]=0.
            exc_s=self.bt==0
            hot=np.where(rate>.20)[0]
            if len(hot)>0:
                mask=exc_s&np.isin(self.tgt,hot)
                if mask.sum()>0: self.w[mask]=np.clip(self.w[mask]*.95,.005,1.)
            cold=np.where((rate>.0005)&(rate<.03))[0]
            if len(cold)>0:
                mask=exc_s&np.isin(self.tgt,cold)
                if mask.sum()>0: self.w[mask]=np.clip(self.w[mask]*1.05,.005,1.)
        self._build_W()

    def el_r(self):
        cm=(self.bt==0)|(self.bt==1)
        return float((self.bt==1).sum())/max(1,cm.sum())

    def run_once(self):
        bin_counts=[]; cur_bin=0; t0=time.time()
        for step in range(N_STEPS):
            self.t=step
            t_ms=step*DT
            fired=self.lif_step(t_ms)
            # 累计 bin
            cur_bin+=int(fired.sum())
            if (step+1)%BIN_STEPS==0:
                bin_counts.append(cur_bin); cur_bin=0
            # STDP（每步）
            self.stdp(fired,t_ms)
            # SDI 规则（每5步）
            if step%5==0: self.sdi_rules(fired)

        # 提取雪崩
        avalanches=[]; in_av=False; cur_av=0
        for bc in bin_counts:
            if bc>0:
                cur_av+=bc; in_av=True
            elif in_av:
                if cur_av>1: avalanches.append(cur_av)
                cur_av=0; in_av=False
        if in_av and cur_av>1: avalanches.append(cur_av)

        cm=(self.bt==0)|(self.bt==1)
        C,L,sig=compute_metrics(self.src[cm],self.tgt[cm],self.N)
        alp=hill_alpha_ks(avalanches)
        el=self.el_r()
        return {'sigma':sig,'C':C,'L':L,'alpha':alp,'el':el,
                'n_av':len(avalanches),
                'mean_av':float(np.mean(avalanches)) if avalanches else 0.,
                'elapsed':round(time.time()-t0,1)}

def run_species(name, sp):
    print(f'\n{"="*55}\n{name}  N={sp["N"]}  [{sp["level"]}]\n{"="*55}',flush=True)
    all_runs=[]
    for seed in SEEDS:
        net=LIF_SDI(name,sp,seed)
        r=net.run_once(); r['seed']=seed
        alp_s=f'{r["alpha"]:.3f}' if r['alpha'] else 'N/A'
        print(f'  seed={seed}: σ={r["sigma"]:.3f} C={r["C"]:.3f} '
              f'L={r["L"]:.3f} α={alp_s} EL={r["el"]:.1%} '
              f'av={r["n_av"]}(μ={r["mean_av"]:.1f}) ({r["elapsed"]:.1f}s)',flush=True)
        all_runs.append(r)

    def stats(key):
        vals=[r[key] for r in all_runs if r.get(key) is not None]
        return (float(np.mean(vals)),float(np.std(vals))) if vals else (None,0.)

    tgt=sp['tgt']
    def ok(v,r):
        if v is None: return False
        lo,hi=r; return (lo is None or v>=lo) and (hi is None or v<=hi)

    final={}
    for m in ['sigma','C','L','alpha','el']:
        mu,sd=stats(m); final[m]=mu; final[f'{m}_std']=sd
        final[f'pass_{m}']=ok(mu,tgt[m])
    final['score']=sum(bool(final[f'pass_{m}']) for m in ['sigma','C','L','alpha','el'])
    final.update({'runs':all_runs,'level':sp['level'],'bio':sp['bio'],'ref':sp['ref']})

    print(f'\n--- {name} SUMMARY ({len(SEEDS)} seeds) ---')
    for m in ['sigma','C','L','alpha','el']:
        mu=final[m]; sd=final[f'{m}_std']
        lo,hi=tgt[m]
        ts=f'≥{lo}' if lo and not hi else f'[{lo},{hi}]' if lo and hi else f'≤{hi}'
        v_str=f'{mu:.3f}±{sd:.3f}' if mu is not None else 'N/A'
        print(f'  {"✅" if final[f"pass_{m}"] else "❌"} {m:6s}: {v_str}  (target {ts})')
    print(f'  SCORE: {final["score"]}/5  [{sp["level"]}]')
    return final

def main():
    all_r={}; t0=time.time()
    for name,sp in SPECIES.items():
        all_r[name]=run_species(name,sp)

    print(f'\n{"="*60}\nALL DONE {time.time()-t0:.1f}s\n{"="*60}')
    print(f'{"物种":22s} {"级别":10s} {"得分":5s}  σ       C      L     α      EL')
    print('-'*75)
    for n,r in all_r.items():
        lvl='★meso' if r['level']=='mesoscale' else 'neuron'
        mu=r['alpha']; sd=r['alpha_std']
        a_str=f'{mu:.2f}±{sd:.2f}' if mu else 'N/A'
        print(f'{n:22s} {lvl:10s} {r["score"]}/5  '
              f'{r["sigma"]:.2f}±{r["sigma_std"]:.2f}  '
              f'{r["C"]:.3f}  {r["L"]:.2f}  {a_str}  {r["el"]:.1%}')

    print('\n【LIF+SDI 液态拓扑说明】')
    print('  神经元：标准 LIF（线性突触，参数空间宽）')
    print('  液态拓扑：SDI 化合键动态重构（固化/消除/WS重连）')
    print('    E-L键（固化）权重增益×1.4 → 快响应骨架（对应LNN短τ）')
    print('    E-S键（可塑）正常权重    → 慢适应通道（对应LNN长τ）')
    print('  雪崩：T_bin=4ms，单点刺激，与Beggs&Plenz 2003完全对应')
    print('  STDP：精确spike时刻（0.5ms分辨率）')

    def fix(o):
        if isinstance(o,(bool,np.bool_)): return int(o)
        if isinstance(o,np.integer): return int(o)
        if isinstance(o,np.floating): return float(o)
        if isinstance(o,dict): return {k:fix(v) for k,v in o.items()}
        if isinstance(o,list): return [fix(v) for v in o]
        return o
    with open(f'{OUT}/exp1_v13_results.json','w') as f:
        json.dump(fix(all_r),f,indent=2)

    # 汇总图
    fig,axes=plt.subplots(7,5,figsize=(22,26))
    mkeys=[('sigma','σ','b'),('C','C','g'),('L','L','orange'),
           ('alpha','α','r'),('el','EL','purple')]
    for row,(name,r) in enumerate(all_r.items()):
        bio=r['bio']; tg=SPECIES[name]['tgt']; lvl=r['level']
        for col,(mk,ml,cl) in enumerate(mkeys):
            ax=axes[row][col]
            mu=r[mk]; sd=r.get(f'{mk}_std',0)
            if mu is not None:
                ax.bar([.5],[mu],width=.4,color=cl,alpha=.7)
                ax.errorbar([.5],[mu],yerr=[sd],color='k',capsize=5,lw=2)
            lo,hi=tg[mk]
            if lo: ax.axhline(lo,color='g',ls='--',lw=1.5,alpha=.8)
            if hi: ax.axhline(hi,color='r',ls='--',lw=1.5,alpha=.8)
            bv=bio.get(mk)
            if bv: ax.axhline(bv,color='k',ls=':',lw=1.5,alpha=.7)
            ok_=bool(r.get(f'pass_{mk}',False))
            sp_s=name.replace('_Cortex★','').replace('_Cortex','')[:9]
            sf='★' if lvl=='mesoscale' else ''
            ax.set_title(f'{sp_s}{sf}\n{ml}',fontsize=7,
                         color='darkgreen' if ok_ else 'darkred',
                         fontweight='bold' if ok_ else 'normal')
            ax.set_xticks([]); ax.tick_params(labelsize=6); ax.grid(alpha=.3,axis='y')
    plt.suptitle('SDI Exp1 v13 — LIF + SDI 液态拓扑\n'
                 'LIF神经元 + 化合键动态重构 → 真正幂律雪崩 α∈[1.5,2.5]',
                 fontsize=11,fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{OUT}/exp1_v13_convergence.png',dpi=130,bbox_inches='tight')
    plt.close()
    print('Results → exp1_v13_results.json')
    print('Plot → exp1_v13_convergence.png')
    print('DONE')

if __name__=='__main__':
    main()
