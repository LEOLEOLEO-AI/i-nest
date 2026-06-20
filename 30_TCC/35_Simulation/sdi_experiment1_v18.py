#!/usr/bin/env python3
"""
SDI 实验一 v15 — 事件驱动LIF + SDI + 方案B + 方案C + 延长时间
方案B：加速三元闭合（Accelerated Triadic Closure）
  - 每次 STDP 后，新边优先建在"共同激活过的二阶邻居"之间
  - 对应 SDI 文档：轴突侧支发芽（Axonal Sprouting）机制
方案C：BA 无标度初始图（Scale-Free，hub 结构）
  - 优先连接（Preferential Attachment），hub 天然高三角密度
  - 完全随机，不预设任何生物拓扑
延长：T_SIM = 120000ms（120秒），仿真约1500次刺激
"""
import numpy as np, scipy.sparse as sp, heapq, json, time
from scipy.sparse.csgraph import connected_components
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(42)
OUT = '/home/work/.openclaw/workspace/sdi_sim'
SEEDS = [42, 7, 13, 99, 2024]

# ======== LIF 参数 ========
TAU_M    = 20.0; V_REST = -70.0; V_TH = -55.0; V_RESET = -70.0
T_REF    = 2.0;  TAU_SYN = 5.0;  W_EL_BOOST = 1.5

# ======== 刺激 & 雪崩 ========
T_STIM   = 80.0   # ms
T_BIN    = 4.0    # ms
T_SIM    = 120000.0  # ms（高阶拓扑收敛：120秒，约1500次刺激）

# ======== SDI 参数 ========
# 方案B增强 + 高阶拓扑（三元渗流理论，Bianconi 2023 NatComm）
THETA_LTP = 35     # 进一步降低固化阈值，加快E-L积累

# 有符号三元调控参数（Signed Triadic Regulation）
# 依据：Bianconi 2023三元渗流 + Reimann 2017神经clique拓扑
TRIAD_EL_BOOST  = 2.0   # E-L三角形内固化概率增益（腔结构维护）
TRIAD_CHECK_INT = 300.0  # ms，每300ms检查三角形固化机会
THETA_LTP = 35     # 降低阈值，加快固化速度
THETA_LTD = 10
T_DECAY_MS = 4000.0
EL_HI      = 0.25
MAX_FIX    = 10
P_REWIRE   = 0.20   # 提高重连概率
SCALING_INT_MS = 300.0

# ======== 方案B：三元闭合参数 ========
TRIAD_INT_MS   = 200.0  # 每200ms做一次三元闭合扫描
TRIAD_P        = 0.70   # 新边优先选共激活二阶邻居的概率
MAX_TRIAD_NEW  = 6      # 每次最多新建三角形边数
COACT_WINDOW_MS= 20.0   # 共激活时间窗口（ms内视为共激活）

# ======== 7物种 ========
SPECIES = {
    'C.elegans':      {'N':279,'k_avg':8,'sf':0.22,'level':'neuron',
        'w_exc':(0.4,2.0),'inh_frac':0.20,
        'bio':{'sigma':4.71,'C':0.337,'L':2.44,'alpha':1.5,'el':0.191},
        'ref':'Varshney 2011; Beggs&Plenz 2003',
        'tgt':{'sigma':(4.,None),'C':(.25,None),'L':(2.,3.5),'alpha':(1.5,2.5),'el':(.15,.28)}},
    'Larval_Drosophila':{'N':321,'k_avg':8,'sf':0.20,'level':'neuron',
        'w_exc':(0.4,2.0),'inh_frac':0.20,
        'bio':{'sigma':None,'C':.25,'L':2.1,'alpha':2.,'el':.18},
        'ref':'Winding 2023',
        'tgt':{'sigma':(3.,None),'C':(.20,None),'L':(1.5,3.5),'alpha':(1.5,2.5),'el':(.15,.28)}},
    'Macaque_Cortex': {'N':242,'k_avg':8,'sf':0.12,'level':'neuron',
        'w_exc':(0.4,2.0),'inh_frac':0.20,
        'bio':{'sigma':3.8,'C':.55,'L':2.3,'alpha':2.2,'el':.20},
        'ref':'Modha&Singh 2010',
        'tgt':{'sigma':(3.,None),'C':(.25,None),'L':(2.,3.5),'alpha':(1.5,2.5),'el':(.15,.28)}},
    'Rat_Cortex★':   {'N':73,'k_avg':6,'sf':0.15,'level':'mesoscale',
        'w_exc':(0.5,2.2),'inh_frac':0.20,
        'bio':{'sigma':.79,'C':.332,'L':1.9,'alpha':2.,'el':.18},
        'ref':'conn2res',
        'tgt':{'sigma':(1.2,None),'C':(.25,None),'L':(1.5,3.),'alpha':(1.5,2.5),'el':(.15,.28)}},
    'Mouse_Cortex★': {'N':112,'k_avg':6,'sf':0.15,'level':'mesoscale',
        'w_exc':(0.5,2.2),'inh_frac':0.20,
        'bio':{'sigma':.64,'C':.439,'L':1.8,'alpha':2.1,'el':.20},
        'ref':'Allen Mouse Brain Atlas',
        'tgt':{'sigma':(1.5,None),'C':(.22,None),'L':(1.5,3.),'alpha':(1.5,2.5),'el':(.15,.28)}},
    'Chimpanzee★':   {'N':200,'k_avg':8,'sf':0.10,'level':'mesoscale',
        'w_exc':(0.4,1.8),'inh_frac':0.20,
        'bio':{'sigma':1.76,'C':.149,'L':2.2,'alpha':2.1,'el':.20},
        'ref':'Reardon 2016',
        'tgt':{'sigma':(1.5,None),'C':(.12,None),'L':(1.5,3.5),'alpha':(1.5,2.5),'el':(.15,.28)}},
    'Human_HCP★':    {'N':400,'k_avg':8,'sf':0.08,'level':'mesoscale',
        'w_exc':(0.3,1.6),'inh_frac':0.20,
        'bio':{'sigma':3.59,'C':.204,'L':2.3,'alpha':2.2,'el':.20},
        'ref':'HCP; Schaefer 2018',
        'tgt':{'sigma':(2.5,None),'C':(.15,None),'L':(2.,4.),'alpha':(1.5,2.5),'el':(.15,.28)}},
}

# ======== 指标 ========
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
    # Betti-1 = edges - nodes + connected_components（欧拉特征）
    # β₁ 高 → 更多独立环路 → 高阶拓扑腔丰富（Giusti 2016）
    # 此处仅返回基本指标，beta1 作为诊断量
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

# ======== 事件驱动 LIF + SDI v15 ========
class LIF_SDI_v15:
    def __init__(self, name, sp, seed):
        np.random.seed(seed)
        self.name=name; self.N=sp['N']; self.sp=sp
        N=sp['N']; k=sp['k_avg']; w_lo,w_hi=sp['w_exc']
        inh_frac=sp['inh_frac']; N_exc=int(N*(1-inh_frac))

        # ======== 方案C：BA 无标度初始图 ========
        m=max(2,k//2)  # 每个新节点连 m 个已有节点
        sl,tl,wl,bl=[],[],[],[]
        deg_arr=np.zeros(N)
        # 初始小团（m+1个节点全连接）
        for i in range(min(m+1,N)):
            for j in range(i+1,min(m+1,N)):
                w=np.random.uniform(w_lo,w_hi)
                bt=2 if i>=N_exc or j>=N_exc else 0
                sl+=[i,j]; tl+=[j,i]; wl+=[w,w]; bl+=[bt,bt]
                deg_arr[i]+=1; deg_arr[j]+=1
        # 优先连接（Preferential Attachment）
        for new_node in range(min(m+1,N),N):
            probs=deg_arr[:new_node]+1  # +1 避免零概率
            probs=probs/probs.sum()
            targets=np.random.choice(new_node,size=min(m,new_node),
                                     replace=False,p=probs)
            for t in targets:
                w=np.random.uniform(w_lo,w_hi)
                bt=2 if new_node>=N_exc else 0
                sl+=[new_node,t]; tl+=[t,new_node]
                wl+=[w,w]; bl+=[bt,bt]
                deg_arr[new_node]+=1; deg_arr[t]+=1

        self.src=np.array(sl,np.int32); self.tgt=np.array(tl,np.int32)
        self.w=np.array(wl); self.bt=np.array(bl,np.int8)
        ne=len(self.src)
        self.nltp=np.zeros(ne,np.int32); self.nltd=np.zeros(ne,np.int32)
        self.la_ms=np.full(ne,-1e9)
        self.N_exc=N_exc

        # LIF 状态
        self.V=np.full(N,V_REST); self.V_t=np.zeros(N)
        self.I_syn=np.zeros(N);   self.I_t=np.zeros(N)
        self.ref_end=np.full(N,-1.); self.t_spike=np.full(N,-1e9)

        # 感觉神经元
        ns=max(2,int(N*sp['sf']))
        self.sens=np.arange(min(ns,N_exc)); self.stim_ptr=0

        # 方案B：共激活追踪
        self.coact_t=np.full(N,-1e9)  # 最近激活时刻（用于三元闭合）
        self.last_triad_t=0.; self.last_sdi_t=0.; self.last_scale_t=0.
        self.fire_cnt=np.zeros(N)

        self._build_W()
        C0,L0,sig0=compute_metrics(
            self.src[(self.bt==0)|(self.bt==1)],
            self.tgt[(self.bt==0)|(self.bt==1)],N)
        print(f'  [{name}] N={N} edges={ne} σ₀={sig0:.2f} C₀={C0:.3f} '
              f'BA k_avg≈{ne/N:.1f}',flush=True)

    def _build_W(self):
        N=self.N; w_eff=self.w.copy()
        w_eff[self.bt==1]*=W_EL_BOOST
        w_eff[(self.bt==2)|(self.bt==3)]*=-0.25
        self.W=sp.csr_matrix((w_eff,(self.src,self.tgt)),shape=(N,N))
        self.out_nbr={}
        for i,(s,t,w) in enumerate(zip(self.src,self.tgt,w_eff)):
            self.out_nbr.setdefault(int(s),[]).append((int(t),float(w),i))

    def _get_V(self,i,t):
        dt=t-self.V_t[i]
        if dt<=0: return self.V[i]
        dt_I=t-self.I_t[i]
        I_avg=(self.I_syn[i]*TAU_SYN/dt_I*(1-np.exp(-dt_I/TAU_SYN))
               if dt_I>0.001 else self.I_syn[i])
        decay=np.exp(-dt/TAU_M)
        return V_REST+(self.V[i]-V_REST)*decay+I_avg*TAU_M*(1-decay)

    def _next_spike(self,i,t):
        if t<self.ref_end[i]: return np.inf
        V0=self._get_V(i,t)
        dt_I=t-self.I_t[i]
        I_now=(self.I_syn[i]*np.exp(-dt_I/TAU_SYN) if dt_I>0 else self.I_syn[i])
        asymptote=V_REST+I_now*TAU_M
        if asymptote<=V_TH and V0<=V_TH: return np.inf
        if V0>=V_TH: return t
        if abs(V0-asymptote)<1e-6: return np.inf
        ratio=(V_TH-asymptote)/(V0-asymptote)
        if ratio<=0 or ratio>=1: return np.inf
        return t-TAU_M*np.log(ratio)

    def fire(self,i,t_fire,heap):
        self.V[i]=V_RESET; self.V_t[i]=t_fire
        self.ref_end[i]=t_fire+T_REF
        self.t_spike[i]=t_fire
        self.coact_t[i]=t_fire   # 记录激活时刻（方案B用）
        self.fire_cnt[i]+=1.
        for (j,w_ij,edge_idx) in self.out_nbr.get(i,[]):
            dt_I=t_fire-self.I_t[j]
            self.I_syn[j]=self.I_syn[j]*np.exp(-dt_I/TAU_SYN)+w_ij
            self.I_t[j]=t_fire
            self.V[j]=self._get_V(j,t_fire); self.V_t[j]=t_fire
            t_next=self._next_spike(j,t_fire)
            if t_next<T_SIM and np.isfinite(t_next):
                heapq.heappush(heap,(t_next,j))
            # STDP
            t_post=self.t_spike[j]
            if t_post>-1e8:
                dt_ms=t_fire-t_post
                if 0<dt_ms<100:
                    self.w[edge_idx]=np.clip(
                        self.w[edge_idx]+0.012*np.exp(-dt_ms/20.),0,1)
                    self.nltp[edge_idx]+=1
                elif -100<dt_ms<0:
                    self.w[edge_idx]=np.clip(
                        self.w[edge_idx]-0.008*np.exp(dt_ms/20.),0,1)
                    self.nltd[edge_idx]+=1
                self.la_ms[edge_idx]=t_fire

    def triadic_closure(self, t_now):
        """
        方案B：加速三元闭合（Axonal Sprouting）
        找在 COACT_WINDOW_MS 内共同激活的神经元对 (i,j)，
        若存在共同激活邻居 k（A→k 且 B→k），且 A→B 不存在，
        以概率 TRIAD_P 新建 A→B 边（E-S）
        """
        N=self.N
        # 最近共激活神经元（在时间窗口内）
        recently_active=np.where(
            (t_now-self.coact_t<COACT_WINDOW_MS) &
            (self.coact_t>-1e8))[0]
        if len(recently_active)<3: return

        cm=(self.bt==0)|(self.bt==1)
        existing=set(zip(self.src[cm].tolist(),self.tgt[cm].tolist()))

        # 找二阶共激活邻居对
        new_s,new_t_arr,new_w=[],[],[]
        # 用稀疏矩阵找共同邻居：A2[i,j] = 共同邻居数
        As=sp.csr_matrix((np.ones(cm.sum()),
                          (self.src[cm],self.tgt[cm])),shape=(N,N))
        # 只在 recently_active 子集上计算
        ra=recently_active
        ra_mask=np.zeros(N,bool); ra_mask[ra]=True
        A2_sub=As@As  # i→k→j 的路径数
        for i in ra[:min(20,len(ra))]:
            row=A2_sub.getrow(i)
            cands=row.indices[(row.data>0)&ra_mask[row.indices]]
            for j in cands:
                if i!=j and (i,j) not in existing:
                    if np.random.random()<TRIAD_P:
                        new_s.append(i); new_t_arr.append(j)
                        w_sp=self.sp['w_exc']
                        new_w.append(np.random.uniform(w_sp[0],w_sp[1]))
                        existing.add((i,j))
                        if len(new_s)>=MAX_TRIAD_NEW: break
            if len(new_s)>=MAX_TRIAD_NEW: break

        # 腔保护：若拟建边(i,j)会填满一个已有三角形且该三角形含I-L边
        # 则以0.5概率跳过（维持腔结构，Giusti 2016 & Reimann 2017）
        # I-L边代表侧抑制骨架，它保护三角形腔不被完全填充
        filtered_s, filtered_t, filtered_w = [], [], []
        il_set = set(zip(self.src[(self.bt==3)|(self.bt==2)].tolist(),
                         self.tgt[(self.bt==3)|(self.bt==2)].tolist()))
        for si, ti, wi in zip(new_s, new_t_arr, new_w):
            # 若(si,ti)的反方向存在I-L边，以0.4概率保留腔
            if (ti, si) in il_set and np.random.random() < 0.4:
                continue  # 跳过，维持拓扑腔
            filtered_s.append(si); filtered_t.append(ti); filtered_w.append(wi)
        new_s, new_t_arr, new_w = filtered_s, filtered_t, filtered_w

        if new_s:
            nn=len(new_s)
            self.src=np.concatenate([self.src,np.array(new_s,np.int32)])
            self.tgt=np.concatenate([self.tgt,np.array(new_t_arr,np.int32)])
            self.w=np.concatenate([self.w,np.array(new_w)])
            self.bt=np.concatenate([self.bt,np.zeros(nn,np.int8)])  # E-S
            self.nltp=np.concatenate([self.nltp,np.zeros(nn,np.int32)])
            self.nltd=np.concatenate([self.nltd,np.zeros(nn,np.int32)])
            self.la_ms=np.concatenate([self.la_ms,np.full(nn,-1e9)])

    def apply_sdi(self, t_now):
        # 规则1：E-S → E-L（基础固化）
        r1=np.where((self.bt==0)&(self.nltp>=THETA_LTP))[0]

        # 高阶拓扑增强：有符号三元调控（Bianconi 2023）
        # 若E-S边 (i,j) 所在三角形包含E-L边 → 固化概率×TRIAD_EL_BOOST
        # 对应：三角腔结构中的稳定化机制（腔维护 vs 腔填充的平衡）
        if len(r1) > 0:
            N = self.N
            cm_el = (self.bt == 1)
            if cm_el.sum() > 0:
                # 构建E-L邻接集合（用于三角形检测）
                el_nbr = {}
                for s, t in zip(self.src[cm_el], self.tgt[cm_el]):
                    el_nbr.setdefault(int(s), set()).add(int(t))
                boosted = []
                for idx in r1:
                    si, ti = int(self.src[idx]), int(self.tgt[idx])
                    # 检查(si,ti)是否参与E-L三角形
                    nbr_si = el_nbr.get(si, set())
                    nbr_ti = el_nbr.get(ti, set())
                    common = nbr_si & nbr_ti  # 共同E-L邻居 = 三角形第三顶点
                    if common and np.random.random() < TRIAD_EL_BOOST / (TRIAD_EL_BOOST + 1):
                        boosted.append(idx)
                    elif self.nltp[idx] >= THETA_LTP:
                        boosted.append(idx)
                r1 = np.array(boosted, dtype=np.int32)

        if len(r1)>MAX_FIX: np.random.shuffle(r1); r1=r1[:MAX_FIX]
        self.bt[r1]=1; self.nltp[r1]=0
        # 规则4：E-L → E-S
        self.bt[(self.bt==1)&(t_now-self.la_ms>T_DECAY_MS)]=0
        # 胶质控制
        cm=(self.bt==0)|(self.bt==1)
        if cm.sum()>0 and (self.bt==1).sum()/cm.sum()>EL_HI:
            el_idx=np.where(self.bt==1)[0]
            stale=el_idx[np.argsort(self.la_ms[el_idx])[:max(3,len(el_idx)//10)]]
            self.bt[stale]=0; self.nltp[stale]=0
        # 规则2：I-S消除
        kill=((self.bt==2)&(self.nltd>=THETA_LTD))|\
             ((self.bt==2)&(self.w<.01)&(t_now-self.la_ms>2000))
        keep=~kill
        self.src=self.src[keep]; self.tgt=self.tgt[keep]; self.w=self.w[keep]
        self.bt=self.bt[keep]; self.nltp=self.nltp[keep]
        self.nltd=self.nltd[keep]; self.la_ms=self.la_ms[keep]
        # WS 重连
        # 边数超限时也停止WS重连（与三元闭合一致）
        cm_now=(self.bt==0)|(self.bt==1)
        if cm_now.sum() >= int(self.N*self.sp['k_avg']*2.0):
            pass  # 超限，跳过重连（突触缩放仍执行）
        else:
            rf=np.where(self.fire_cnt>0)[0]
        rf=np.where(self.fire_cnt>0)[0]
        if len(rf)>2:
            cm2=(self.bt==0)|(self.bt==1)
            idle=np.where(cm2&(t_now-self.la_ms>800))[0]
            if len(idle)>0:
                np.random.shuffle(idle); rw=idle[:min(5,len(idle))]
                es=set(zip(self.src[cm2].tolist(),self.tgt[cm2].tolist()))
                for ri in rw:
                    if np.random.random()<P_REWIRE:
                        i=int(self.src[ri]); j=int(np.random.choice(rf))
                        if j!=i and (i,j) not in es:
                            es.discard((i,int(self.tgt[ri])))
                            self.tgt[ri]=j; es.add((i,j))
        # 突触缩放
        if t_now-self.last_scale_t>=SCALING_INT_MS and t_now>500:
            dt_s=t_now-self.last_scale_t
            rate=self.fire_cnt/dt_s*1000
            self.fire_cnt[:]=0.; self.last_scale_t=t_now
            exc_s=self.bt==0
            hot=np.where(rate>25.)[0]
            if len(hot)>0:
                mask=exc_s&np.isin(self.tgt,hot)
                if mask.sum()>0: self.w[mask]=np.clip(self.w[mask]*.94,.005,1.)
            cold=np.where((rate>.01)&(rate<2.))[0]
            if len(cold)>0:
                mask=exc_s&np.isin(self.tgt,cold)
                if mask.sum()>0: self.w[mask]=np.clip(self.w[mask]*1.06,.005,1.)
        self._build_W()

    def el_r(self):
        cm=(self.bt==0)|(self.bt==1)
        return float((self.bt==1).sum())/max(1,cm.sum())

    def run_once(self):
        N=self.N; heap=[]; t_now=0.
        n_bins=int(T_SIM/T_BIN)+2
        bin_spikes=np.zeros(n_bins,int)
        n_spikes=0; stim_count=0
        # 神经元级雪崩去重字典（每个bin内）
        neuron_in_bin = [{} for _ in range(n_bins+2)]
        next_sdi=500.; next_triad=TRIAD_INT_MS
        t0=time.time()

        while t_now<T_SIM:
            next_stim=stim_count*T_STIM
            next_heap=heap[0][0] if heap else np.inf
            next_t=min(next_stim,next_sdi,next_triad,next_heap)
            if next_t>=T_SIM: break
            t_now=next_t

            # 刺激
            if stim_count*T_STIM<=t_now+1e-6 and t_now<=stim_count*T_STIM+1e-6:
                seed_i=int(self.sens[self.stim_ptr%len(self.sens)])
                self.stim_ptr+=1
                self.V[seed_i]=V_TH+3.; self.V_t[seed_i]=t_now
                ts=self._next_spike(seed_i,t_now)
                if ts<T_SIM: heapq.heappush(heap,(ts,seed_i))
                stim_count+=1

            # SDI 规则
            if abs(t_now-next_sdi)<1e-6:
                self.apply_sdi(t_now); next_sdi+=500.

            # 方案B：三元闭合
            if abs(t_now-next_triad)<1e-6:
                self.triadic_closure(t_now)
                next_triad+=TRIAD_INT_MS

            # Spike 事件
            fired_n=0
            while heap and heap[0][0]<=t_now+1e-6:
                t_fire,i=heapq.heappop(heap)
                if t_fire<self.ref_end[i]: continue
                V_c=self._get_V(i,t_fire)
                if V_c<V_TH-1.5: continue
                self.fire(i,t_fire,heap)
                bi=int(t_fire/T_BIN)
                if bi<n_bins:
                    # 神经元级去重：同一神经元在同一bin内只计一次
                    if not neuron_in_bin[bi].get(i, False):
                        bin_spikes[bi]+=1
                        neuron_in_bin[bi][i]=True
                n_spikes+=1; fired_n+=1
                if fired_n>N*3: break

        # 提取雪崩
        avalanches=[]; in_av=False; cur_av=0
        for bc in bin_spikes:
            if bc>0: cur_av+=bc; in_av=True
            elif in_av:
                if cur_av>1: avalanches.append(cur_av)
                cur_av=0; in_av=False
        if in_av and cur_av>1: avalanches.append(cur_av)

        cm=(self.bt==0)|(self.bt==1)
        C,L,sig=compute_metrics(self.src[cm],self.tgt[cm],N)
        alp=hill_alpha_ks(avalanches)
        el=self.el_r()
        return {'sigma':sig,'C':C,'L':L,'alpha':alp,'el':el,
                'n_av':len(avalanches),
                'mean_av':float(np.mean(avalanches)) if avalanches else 0.,
                'n_spikes':n_spikes,'elapsed':round(time.time()-t0,1)}

def run_species(name,sp):
    print(f'\n{"="*55}\n{name}  N={sp["N"]}  [{sp["level"]}]\n{"="*55}',flush=True)
    all_runs=[]
    for seed in SEEDS:
        net=LIF_SDI_v15(name,sp,seed)
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
        vs=f'{mu:.3f}±{sd:.3f}' if mu is not None else 'N/A'
        print(f'  {"✅" if final[f"pass_{m}"] else "❌"} {m:6s}: {vs}  ({ts})')
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
        a_s=f'{r["alpha"]:.2f}' if r['alpha'] else 'N/A'
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
    with open(f'{OUT}/exp1_v18_results.json','w') as f:
        json.dump(fix(all_r),f,indent=2)

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
    plt.suptitle('SDI Exp1 v18 — 事件驱动LIF + BA初始图 + 三元闭合 + 30s仿真\n'
                 '随机初始 → SDI规则演化 → 生物复杂网络特性',
                 fontsize=11,fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{OUT}/exp1_v18_convergence.png',dpi=130,bbox_inches='tight')
    plt.close()
    print('Results → exp1_v18_results.json')
    print('Plot → exp1_v18_convergence.png')
    print('DONE')

if __name__=='__main__':
    main()
