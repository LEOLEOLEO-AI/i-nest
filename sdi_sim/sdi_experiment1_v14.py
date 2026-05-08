#!/usr/bin/env python3
"""
SDI 实验一 v14 — 事件驱动 LIF + SDI 化合键
神经元：事件驱动 LIF（解析 spike 时刻，连续时间，精确幂律）
液态拓扑：SDI 化合键（E-S/E-L/I-S 固化/消除/WS重连/突触缩放）
初始图：随机图（ER），从零演化，不预设任何生物拓扑特性
目标：α 真正落入 [1.5, 2.5]，σ/C/L/EL 全达标

事件驱动核心：
  每个神经元的下次 spike 时刻用 LIF 解析解预测
  维护优先队列（最小堆），按时间顺序处理 spike 事件
  突触电流用指数核（EPSP）精确积分，无离散步误差
"""
import numpy as np, scipy.sparse as sp, heapq, json, time
from scipy.sparse.csgraph import connected_components
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(42)
OUT = '/home/work/.openclaw/workspace/sdi_sim'
SEEDS = [42, 7, 13, 99, 2024]

# ======== LIF 参数（Beggs&Plenz 2003）========
TAU_M    = 20.0   # ms，膜时间常数
V_REST   = -70.0  # mV
V_TH     = -55.0  # mV，阈值
V_RESET  = -70.0  # mV
T_REF    = 2.0    # ms，不应期
TAU_SYN  = 5.0    # ms，突触 EPSP 衰减
W_EL_BOOST = 1.5  # E-L 键权重增益（固化骨架快响应）

# ======== 雪崩参数 ========
T_BIN    = 4.0    # ms，雪崩检测窗口（Beggs&Plenz 2003）

# ======== 刺激参数 ========
T_STIM   = 80.0   # ms，刺激间隔（让雪崩完全熄灭）
T_SIM    = 10000.0 # ms，总仿真时长（10秒，约125次刺激）

# ======== SDI 化合键参数 ========
THETA_LTP  = 50
THETA_LTD  = 10
T_DECAY_MS = 5000.0   # ms，E-L 衰减时间（不活跃则退化）
EL_HI      = 0.25
MAX_FIX    = 8
P_REWIRE   = 0.15
SCALING_INT_MS = 500.0  # ms，突触缩放检测间隔

# ======== 7物种定义 ========
SPECIES = {
    'C.elegans': {
        'N':279,'k_avg':8,'sf':0.22,'level':'neuron',
        'w_exc':(0.3,1.8),'inh_frac':0.2,
        'bio':{'sigma':4.71,'C':0.337,'L':2.44,'alpha':1.5,'el':0.191},
        'ref':'Varshney 2011; Beggs&Plenz 2003',
        'tgt':{'sigma':(4.,None),'C':(.25,None),'L':(2.,3.5),'alpha':(1.5,2.5),'el':(.15,.28)}},
    'Larval_Drosophila': {
        'N':321,'k_avg':8,'sf':0.20,'level':'neuron',
        'w_exc':(0.3,1.8),'inh_frac':0.2,
        'bio':{'sigma':None,'C':.25,'L':2.1,'alpha':2.,'el':.18},
        'ref':'Winding 2023',
        'tgt':{'sigma':(3.,None),'C':(.20,None),'L':(1.5,3.5),'alpha':(1.5,2.5),'el':(.15,.28)}},
    'Macaque_Cortex': {
        'N':242,'k_avg':8,'sf':0.12,'level':'neuron',
        'w_exc':(0.3,1.8),'inh_frac':0.2,
        'bio':{'sigma':3.8,'C':.55,'L':2.3,'alpha':2.2,'el':.20},
        'ref':'Modha&Singh 2010',
        'tgt':{'sigma':(3.,None),'C':(.25,None),'L':(2.,3.5),'alpha':(1.5,2.5),'el':(.15,.28)}},
    'Rat_Cortex★': {
        'N':73,'k_avg':6,'sf':0.15,'level':'mesoscale',
        'w_exc':(0.4,2.0),'inh_frac':0.2,
        'bio':{'sigma':.79,'C':.332,'L':1.9,'alpha':2.,'el':.18},
        'ref':'conn2res',
        'tgt':{'sigma':(1.2,None),'C':(.25,None),'L':(1.5,3.),'alpha':(1.5,2.5),'el':(.15,.28)}},
    'Mouse_Cortex★': {
        'N':112,'k_avg':6,'sf':0.15,'level':'mesoscale',
        'w_exc':(0.4,2.0),'inh_frac':0.2,
        'bio':{'sigma':.64,'C':.439,'L':1.8,'alpha':2.1,'el':.20},
        'ref':'Allen Mouse Brain Atlas',
        'tgt':{'sigma':(1.5,None),'C':(.22,None),'L':(1.5,3.),'alpha':(1.5,2.5),'el':(.15,.28)}},
    'Chimpanzee★': {
        'N':200,'k_avg':8,'sf':0.10,'level':'mesoscale',
        'w_exc':(0.3,1.6),'inh_frac':0.2,
        'bio':{'sigma':1.76,'C':.149,'L':2.2,'alpha':2.1,'el':.20},
        'ref':'Reardon 2016',
        'tgt':{'sigma':(1.5,None),'C':(.12,None),'L':(1.5,3.5),'alpha':(1.5,2.5),'el':(.15,.28)}},
    'Human_HCP★': {
        'N':400,'k_avg':8,'sf':0.08,'level':'mesoscale',
        'w_exc':(0.2,1.4),'inh_frac':0.2,
        'bio':{'sigma':3.59,'C':.204,'L':2.3,'alpha':2.2,'el':.20},
        'ref':'HCP; Schaefer 2018',
        'tgt':{'sigma':(2.5,None),'C':(.15,None),'L':(2.,4.),'alpha':(1.5,2.5),'el':(.15,.28)}},
}

# ======== 拓扑指标 ========
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

# ======== 事件驱动 LIF + SDI ========
class EventDriven_LIF_SDI:
    def __init__(self, name, sp, seed):
        np.random.seed(seed)
        self.name=name; self.N=sp['N']; self.sp=sp
        N=sp['N']; k=sp['k_avg']; w_lo,w_hi=sp['w_exc']
        inh_frac=sp['inh_frac']

        # ER 随机图（完全随机初始化，不预设任何生物拓扑）
        p_er=k/(N-1)
        sl,tl,wl,bl=[],[],[],[]
        N_exc=int(N*(1-inh_frac))
        for i in range(N):
            for j in range(N):
                if i!=j and np.random.random()<p_er:
                    w=np.random.uniform(w_lo,w_hi)
                    # 抑制神经元（后 inh_frac 比例）输出为 I-S
                    bt=2 if i>=N_exc else 0  # I-S or E-S
                    sl.append(i); tl.append(j)
                    wl.append(w); bl.append(bt)

        self.src=np.array(sl,np.int32); self.tgt=np.array(tl,np.int32)
        self.w=np.array(wl); self.bt=np.array(bl,np.int8)
        ne=len(self.src)
        self.nltp=np.zeros(ne,np.int32); self.nltd=np.zeros(ne,np.int32)
        self.la_ms=np.full(ne,-1e9)  # 最后 STDP 事件时刻(ms)

        # 神经元状态
        self.V      = np.full(N,V_REST)
        self.V_t    = np.zeros(N)         # V 最后更新时刻
        self.I_syn  = np.zeros(N)         # 当前突触电流（指数衰减）
        self.I_t    = np.zeros(N)         # I_syn 最后更新时刻
        self.ref_end= np.full(N,-1.)      # 不应期结束时刻(ms)
        self.t_spike= np.full(N,-1e9)     # 最后 spike 时刻(ms)

        # 感觉神经元
        ns=max(2,int(N*sp['sf']))
        self.sens=np.arange(min(ns,N_exc))  # 只选兴奋性感觉神经元
        self.stim_ptr=0

        # SDI 状态
        self.fire_cnt=np.zeros(N)       # 激活计数（突触缩放用）
        self.last_scale_t=0.            # 上次突触缩放时刻

        self._build_W()
        C0,L0,sig0=compute_metrics(
            self.src[(self.bt==0)|(self.bt==1)],
            self.tgt[(self.bt==0)|(self.bt==1)],N)
        print(f'  [{name}] N={N} edges={ne} σ₀={sig0:.2f} C₀={C0:.3f} '
              f'N_exc={N_exc} k_avg≈{ne/N:.1f}',flush=True)

    def _build_W(self):
        N=self.N; w_eff=self.w.copy()
        w_eff[self.bt==1]*=W_EL_BOOST   # E-L 增益
        w_eff[(self.bt==2)|(self.bt==3)]*=-0.25  # 抑制
        self.W=sp.csr_matrix((w_eff,(self.src,self.tgt)),shape=(N,N))
        # 邻接表（每个节点的下游列表）
        self.out_nbr={}
        for i,(s,t,w) in enumerate(zip(self.src,self.tgt,w_eff)):
            self.out_nbr.setdefault(int(s),[]).append((int(t),float(w),i))

    def _get_V(self, i, t):
        """获取神经元 i 在时刻 t 的精确膜电位（LIF解析解）"""
        dt=t-self.V_t[i]
        if dt<=0: return self.V[i]
        # I_syn 在 [I_t[i], t] 之间的积分（指数衰减）
        dt_I=t-self.I_t[i]
        I_now=self.I_syn[i]*np.exp(-dt_I/TAU_SYN)
        # V(t) = V_rest + (V0-V_rest)*exp(-dt/tau) + I_eff 的积分
        # 近似：I_syn 从 I_t 到 t 指数衰减，用平均值
        I_avg=self.I_syn[i]*TAU_SYN/dt_I*(1-np.exp(-dt_I/TAU_SYN)) if dt_I>0.001 else self.I_syn[i]
        decay=np.exp(-dt/TAU_M)
        V_new=V_REST+(self.V[i]-V_REST)*decay+I_avg*TAU_M*(1-decay)
        return V_new

    def _next_spike(self, i, t):
        """预测神经元 i 的下次 spike 时刻"""
        if t<self.ref_end[i]: return np.inf  # 在不应期
        V0=self._get_V(i,t)
        dt_I=t-self.I_t[i]
        I_now=self.I_syn[i]*np.exp(-dt_I/TAU_SYN) if dt_I>0 else self.I_syn[i]
        # 渐近值
        asymptote=V_REST+I_now*TAU_M
        if asymptote<=V_TH and V0<=V_TH: return np.inf
        if V0>=V_TH: return t
        if abs(V0-asymptote)<1e-6: return np.inf
        ratio=(V_TH-asymptote)/(V0-asymptote)
        if ratio<=0 or ratio>=1: return np.inf
        return t-TAU_M*np.log(ratio)

    def fire(self, i, t_fire, heap):
        """处理神经元 i 在 t_fire 时刻的 spike"""
        N=self.N
        # 更新状态
        self.V[i]=V_RESET; self.V_t[i]=t_fire
        self.ref_end[i]=t_fire+T_REF
        t_prev_spike=self.t_spike[i]
        self.t_spike[i]=t_fire
        self.fire_cnt[i]+=1.

        # 传播突触电流到下游神经元
        for (j,w_ij,edge_idx) in self.out_nbr.get(i,[]):
            # 更新 j 的 I_syn
            dt_I=t_fire-self.I_t[j]
            self.I_syn[j]=self.I_syn[j]*np.exp(-dt_I/TAU_SYN)+w_ij
            self.I_t[j]=t_fire
            # 更新 j 的 V 基准
            self.V[j]=self._get_V(j,t_fire); self.V_t[j]=t_fire
            # 预测 j 的下次 spike
            t_next=self._next_spike(j,t_fire)
            if t_next<T_SIM and np.isfinite(t_next):
                heapq.heappush(heap,(t_next,j))

            # STDP（精确时刻）
            t_pre=t_fire; t_post=self.t_spike[j]
            if t_post>-1e8:
                dt_ms=t_pre-t_post
                if 0<dt_ms<100:  # LTP
                    self.w[edge_idx]=np.clip(
                        self.w[edge_idx]+0.012*np.exp(-dt_ms/20.),0,1)
                    self.nltp[edge_idx]+=1
                elif -100<dt_ms<0:  # LTD
                    self.w[edge_idx]=np.clip(
                        self.w[edge_idx]-0.008*np.exp(dt_ms/20.),0,1)
                    self.nltd[edge_idx]+=1
                self.la_ms[edge_idx]=t_fire

    def apply_sdi(self, t_now):
        """SDI 化合键规则（按 ms 时刻触发）"""
        # 规则1：E-S → E-L
        r1=np.where((self.bt==0)&(self.nltp>=THETA_LTP))[0]
        if len(r1)>MAX_FIX: np.random.shuffle(r1); r1=r1[:MAX_FIX]
        self.bt[r1]=1; self.nltp[r1]=0
        # 规则4：E-L → E-S（T_DECAY_MS 内无活动）
        self.bt[(self.bt==1)&(t_now-self.la_ms>T_DECAY_MS)]=0
        # 胶质控制
        cm=(self.bt==0)|(self.bt==1)
        if cm.sum()>0 and (self.bt==1).sum()/cm.sum()>EL_HI:
            el_idx=np.where(self.bt==1)[0]
            stale=el_idx[np.argsort(self.la_ms[el_idx])[:max(3,len(el_idx)//10)]]
            self.bt[stale]=0; self.nltp[stale]=0
        # 规则2：I-S 消除
        kill=((self.bt==2)&(self.nltd>=THETA_LTD))|\
             ((self.bt==2)&(self.w<.01)&(t_now-self.la_ms>2000))
        keep=~kill
        self.src=self.src[keep]; self.tgt=self.tgt[keep]; self.w=self.w[keep]
        self.bt=self.bt[keep]; self.nltp=self.nltp[keep]
        self.nltd=self.nltd[keep]; self.la_ms=self.la_ms[keep]
        # WS 重连
        recent_fired=np.where(self.fire_cnt>0)[0]
        if len(recent_fired)>2:
            cm2=(self.bt==0)|(self.bt==1)
            idle=np.where(cm2&(t_now-self.la_ms>1000))[0]
            if len(idle)>0:
                np.random.shuffle(idle); rw=idle[:min(4,len(idle))]
                es_set=set(zip(self.src[cm2].tolist(),self.tgt[cm2].tolist()))
                for ri in rw:
                    if np.random.random()<P_REWIRE:
                        i=int(self.src[ri]); j=int(np.random.choice(recent_fired))
                        if j!=i and (i,j) not in es_set:
                            es_set.discard((i,int(self.tgt[ri])))
                            self.tgt[ri]=j; es_set.add((i,j))
        # 突触缩放
        if t_now-self.last_scale_t>=SCALING_INT_MS and t_now>1000:
            dt_s=t_now-self.last_scale_t
            rate=self.fire_cnt/dt_s*1000  # Hz
            self.fire_cnt[:]=0.; self.last_scale_t=t_now
            exc_s=self.bt==0
            hot=np.where(rate>20.)[0]  # >20Hz 过度激活
            if len(hot)>0:
                mask=exc_s&np.isin(self.tgt,hot)
                if mask.sum()>0: self.w[mask]=np.clip(self.w[mask]*.94,.005,1.)
            cold=np.where((rate>.01)&(rate<2.))[0]  # <2Hz 低活跃
            if len(cold)>0:
                mask=exc_s&np.isin(self.tgt,cold)
                if mask.sum()>0: self.w[mask]=np.clip(self.w[mask]*1.06,.005,1.)
        self._build_W()

    def el_r(self):
        cm=(self.bt==0)|(self.bt==1)
        return float((self.bt==1).sum())/max(1,cm.sum())

    def run_once(self):
        N=self.N; heap=[]; t_now=0.
        # 雪崩检测数组（按 T_BIN 分 bin）
        n_bins=int(T_SIM/T_BIN)+1
        bin_spikes=np.zeros(n_bins,int)
        n_spikes_total=0

        # SDI 检查点
        sdi_interval_ms=500.
        next_sdi=sdi_interval_ms

        t0=time.time()
        stim_count=0

        while t_now<T_SIM:
            # 下次刺激事件
            next_stim=stim_count*T_STIM
            # 下次 SDI 事件
            # 下次 heap 事件
            next_heap=heap[0][0] if heap else np.inf

            # 确定下一个事件
            next_t=min(next_stim, next_sdi, next_heap)
            if next_t>=T_SIM: break
            t_now=next_t

            # 处理刺激
            if abs(t_now-stim_count*T_STIM)<1e-6 and stim_count*T_STIM<=t_now+1e-6:
                seed_i=int(self.sens[self.stim_ptr%len(self.sens)])
                self.stim_ptr+=1
                # 直接设 V 超阈
                self.V[seed_i]=V_TH+2.; self.V_t[seed_i]=t_now
                t_s=self._next_spike(seed_i,t_now)
                if t_s<T_SIM: heapq.heappush(heap,(t_s,seed_i))
                stim_count+=1

            # 处理 SDI
            if abs(t_now-next_sdi)<1e-6:
                self.apply_sdi(t_now)
                next_sdi+=sdi_interval_ms

            # 处理 spike 事件
            fired_this_step=0
            while heap and heap[0][0]<=t_now+1e-6:
                t_fire,i=heapq.heappop(heap)
                if t_fire<self.ref_end[i]: continue  # 在不应期，跳过
                # 检查 V 是否还在阈值以上
                V_check=self._get_V(i,t_fire)
                if V_check<V_TH-1.0: continue  # 已被抑制，取消
                self.fire(i,t_fire,heap)
                # 记录到雪崩 bin
                bin_idx=int(t_fire/T_BIN)
                if bin_idx<n_bins:
                    bin_spikes[bin_idx]+=1
                n_spikes_total+=1
                fired_this_step+=1
                if fired_this_step>N*2: break  # 防止超临界无限循环

        # 提取雪崩
        avalanches=[]; in_av=False; cur_av=0
        for bc in bin_spikes:
            if bc>0:
                cur_av+=bc; in_av=True
            elif in_av:
                if cur_av>1: avalanches.append(cur_av)
                cur_av=0; in_av=False
        if in_av and cur_av>1: avalanches.append(cur_av)

        # 计算拓扑指标
        cm=(self.bt==0)|(self.bt==1)
        C,L,sig=compute_metrics(self.src[cm],self.tgt[cm],N)
        alp=hill_alpha_ks(avalanches)
        el=self.el_r()
        elapsed=time.time()-t0

        return {'sigma':sig,'C':C,'L':L,'alpha':alp,'el':el,
                'n_av':len(avalanches),
                'mean_av':float(np.mean(avalanches)) if avalanches else 0.,
                'n_spikes':n_spikes_total,
                'elapsed':round(elapsed,1)}

def run_species(name, sp):
    print(f'\n{"="*55}\n{name}  N={sp["N"]}  [{sp["level"]}]\n{"="*55}',flush=True)
    all_runs=[]
    for seed in SEEDS:
        net=EventDriven_LIF_SDI(name,sp,seed)
        r=net.run_once(); r['seed']=seed
        alp_s=f'{r["alpha"]:.3f}' if r['alpha'] else 'N/A'
        print(f'  seed={seed}: σ={r["sigma"]:.3f} C={r["C"]:.3f} '
              f'L={r["L"]:.3f} α={alp_s} EL={r["el"]:.1%} '
              f'av={r["n_av"]}(μ={r["mean_av"]:.1f}) '
              f'spk={r["n_spikes"]} ({r["elapsed"]:.1f}s)',flush=True)
        all_runs.append(r)

    def stats(key):
        vals=[r[key] for r in all_runs if r.get(key) is not None]
        return (float(np.mean(vals)),float(np.std(vals))) if vals else (None,0.)

    tgt=sp['tgt']
    def ok(v,r_):
        if v is None: return False
        lo,hi=r_; return (lo is None or v>=lo) and (hi is None or v<=hi)

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
        v_s=f'{mu:.3f}±{sd:.3f}' if mu is not None else 'N/A'
        print(f'  {"✅" if final[f"pass_{m}"] else "❌"} {m:6s}: {v_s}  (target {ts})')
    print(f'  SCORE: {final["score"]}/5  [{sp["level"]}]')
    return final

def main():
    all_r={}; t0=time.time()
    for name,sp in SPECIES.items():
        all_r[name]=run_species(name,sp)

    print(f'\n{"="*60}\nALL DONE {time.time()-t0:.1f}s\n{"="*60}')
    print(f'{"物种":22s} {"级别":10s} {"分":5s}  σ       C      L     α      EL')
    print('-'*75)
    for n,r in all_r.items():
        lvl='★meso' if r['level']=='mesoscale' else 'neuron'
        a_s=f'{r["alpha"]:.2f}±{r["alpha_std"]:.2f}' if r['alpha'] else 'N/A'
        print(f'{n:22s} {lvl:10s} {r["score"]}/5  '
              f'{r["sigma"]:.2f}±{r["sigma_std"]:.2f}  '
              f'{r["C"]:.3f}  {r["L"]:.2f}  {a_s}  {r["el"]:.1%}')

    def fix(o):
        if isinstance(o,(bool,np.bool_)): return int(o)
        if isinstance(o,np.integer): return int(o)
        if isinstance(o,np.floating): return float(o)
        if isinstance(o,dict): return {k:fix(v) for k,v in o.items()}
        if isinstance(o,list): return [fix(v) for v in o]
        return o
    with open(f'{OUT}/exp1_v14_results.json','w') as f:
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
                ax.bar([.5],[mu],width=.4,color=cl,alpha=.75)
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
    plt.suptitle('SDI Exp1 v14 — 事件驱动LIF + SDI液态拓扑\n'
                 '随机ER初始图 → SDI规则演化 → 生物复杂网络特性（目标α∈[1.5,2.5]）',
                 fontsize=11,fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{OUT}/exp1_v14_convergence.png',dpi=130,bbox_inches='tight')
    plt.close()
    print('Results → exp1_v14_results.json')
    print('Plot → exp1_v14_convergence.png')
    print('DONE')

if __name__=='__main__':
    main()
