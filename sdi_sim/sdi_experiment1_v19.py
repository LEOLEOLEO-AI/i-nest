#!/usr/bin/env python3
"""
SDI 实验一 v19 — 模块化两层结构 + 事件驱动LIF
核心设计：模块化小世界（解决 C 高 vs alpha 幂律 的物理矛盾）

两层结构（对应 SDI 文档的 MT-α + MT-γ）：
  层1（模块内）：BA无标度子图，高密度三角形 → 高C
  层2（模块间）：稀疏长程连接（WS重连风格）→ 短L + 有限级联 → 幂律alpha

理论依据：
  Watts&Strogatz 1998：小世界 = 高局部聚类 + 短全局路径
  Meunier et al. 2010 PLOS Comp Biol：脑网络的模块化小世界
  Bianconi 2023 NatComm：三元渗流在模块化网络中稳定振荡
  Beggs&Plenz 2003：幂律雪崩在亚临界-临界边界，需要有限级联

SDI 化合键对应：
  模块内密集 E-L 骨架 → MT-α（全骨架型）
  模块间稀疏 E-S 通道 → MT-γ（全可塑链型）
  I-L 侧抑制边在模块边界 → 控制跨模块传播 → 维持alpha在[1.5,2.5]
"""
import numpy as np, scipy.sparse as sp, heapq, json, time
from scipy.sparse.csgraph import connected_components
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(42)
OUT = '/home/work/.openclaw/workspace/sdi_sim'
SEEDS = [42, 7, 13, 99, 2024]

# ======== LIF 参数 ========
TAU_M=20.; V_REST=-70.; V_TH=-55.; V_RESET=-70.; T_REF=2.; TAU_SYN=5.
W_EL_BOOST=1.3  # 降低E-L增益，防止模块内超临界

# ======== 雪崩参数 ========
T_BIN=4.; T_STIM=80.; T_SIM=120000.

# ======== SDI 参数 ========
THETA_LTP=40; THETA_LTD=10; T_DECAY_MS=4000.; EL_HI=0.25; MAX_FIX=6
P_REWIRE=0.15; SCALING_INT_MS=400.
TRIAD_INT_MS=200.; TRIAD_P=0.65; MAX_TRIAD_NEW=4
TRIAD_EL_BOOST=2.0

# ======== 模块化参数 ========
# 关键：模块内密集（高C），模块间稀疏（有限级联）
N_MODULES_FRAC = 0.10  # 每个模块约占N的10%
P_INTER_MODULE = 0.02  # 模块间连接概率（稀疏）
W_INTRA = (0.4, 2.0)  # 模块内权重（较强，支持模块内级联）
W_INTER = (0.1, 0.5)  # 模块间权重（较弱，限制跨模块传播）

# ======== 7物种 ========
SPECIES = {
    'C.elegans':      {'N':279,'k_intra':8,'sf':0.22,'level':'neuron',
        'inh_frac':0.20,
        'bio':{'sigma':4.71,'C':0.337,'L':2.44,'alpha':1.5,'el':0.191},
        'ref':'Varshney 2011; Beggs&Plenz 2003',
        'tgt':{'sigma':(4.,None),'C':(.25,None),'L':(2.,3.5),'alpha':(1.5,2.5),'el':(.15,.28)}},
    'Larval_Drosophila':{'N':321,'k_intra':8,'sf':0.20,'level':'neuron',
        'inh_frac':0.20,
        'bio':{'sigma':None,'C':.25,'L':2.1,'alpha':2.,'el':.18},
        'ref':'Winding 2023',
        'tgt':{'sigma':(3.,None),'C':(.20,None),'L':(1.5,3.5),'alpha':(1.5,2.5),'el':(.15,.28)}},
    'Macaque_Cortex': {'N':242,'k_intra':8,'sf':0.12,'level':'neuron',
        'inh_frac':0.20,
        'bio':{'sigma':3.8,'C':.55,'L':2.3,'alpha':2.2,'el':.20},
        'ref':'Modha&Singh 2010',
        'tgt':{'sigma':(3.,None),'C':(.25,None),'L':(2.,3.5),'alpha':(1.5,2.5),'el':(.15,.28)}},
    'Rat_Cortex★':   {'N':73,'k_intra':6,'sf':0.15,'level':'mesoscale',
        'inh_frac':0.20,
        'bio':{'sigma':.79,'C':.332,'L':1.9,'alpha':2.,'el':.18},
        'ref':'conn2res',
        'tgt':{'sigma':(1.2,None),'C':(.25,None),'L':(1.5,3.),'alpha':(1.5,2.5),'el':(.15,.28)}},
    'Mouse_Cortex★': {'N':112,'k_intra':6,'sf':0.15,'level':'mesoscale',
        'inh_frac':0.20,
        'bio':{'sigma':.64,'C':.439,'L':1.8,'alpha':2.1,'el':.20},
        'ref':'Allen Mouse Brain Atlas',
        'tgt':{'sigma':(1.5,None),'C':(.22,None),'L':(1.5,3.),'alpha':(1.5,2.5),'el':(.15,.28)}},
    'Chimpanzee★':   {'N':200,'k_intra':8,'sf':0.10,'level':'mesoscale',
        'inh_frac':0.20,
        'bio':{'sigma':1.76,'C':.149,'L':2.2,'alpha':2.1,'el':.20},
        'ref':'Reardon 2016',
        'tgt':{'sigma':(1.5,None),'C':(.12,None),'L':(1.5,3.5),'alpha':(1.5,2.5),'el':(.15,.28)}},
    'Human_HCP★':    {'N':400,'k_intra':8,'sf':0.08,'level':'mesoscale',
        'inh_frac':0.20,
        'bio':{'sigma':3.59,'C':.204,'L':2.3,'alpha':2.2,'el':.20},
        'ref':'HCP; Schaefer 2018',
        'tgt':{'sigma':(2.5,None),'C':(.15,None),'L':(2.,4.),'alpha':(1.5,2.5),'el':(.15,.28)}},
}

# ======== 指标函数 ========
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

# ======== 模块化网络 + SDI ========
class Modular_LIF_SDI:
    def __init__(self, name, sp_def, seed):
        np.random.seed(seed)
        self.name=name; self.N=sp_def['N']; self.sp=sp_def; self.t_ms=0.
        N=sp_def['N']; k=sp_def['k_intra']
        inh_frac=sp_def['inh_frac']; N_exc=int(N*(1-inh_frac))
        self.N_exc=N_exc

        # ======== 模块划分 ========
        n_mod=max(3, int(N*N_MODULES_FRAC))  # 每个模块大小
        n_modules=max(3, N//n_mod)
        modules=[list(range(i*n_mod, min((i+1)*n_mod, N))) for i in range(n_modules)]
        if N%n_mod != 0:
            modules[-1].extend(range(n_modules*n_mod, N))
        self.modules=modules
        # 节点到模块的映射
        self.node_module=np.zeros(N,int)
        for mi,mod in enumerate(modules):
            for node in mod: self.node_module[node]=mi

        sl,tl,wl,bl=[],[],[],[]; es=set()

        # ======== 模块内：BA无标度子图（高密度三角形）========
        for mod in modules:
            nm=len(mod)
            if nm<3: continue
            m_ba=max(2,k//2)
            deg_local=np.zeros(nm)
            # 初始小团
            for i in range(min(m_ba+1,nm)):
                for j in range(i+1,min(m_ba+1,nm)):
                    ni,nj=mod[i],mod[j]
                    w=np.random.uniform(*W_INTRA)
                    bt=2 if ni>=N_exc or nj>=N_exc else 0
                    if (ni,nj) not in es:
                        sl+=[ni,nj]; tl+=[nj,ni]; wl+=[w,w]; bl+=[bt,bt]
                        es.add((ni,nj)); es.add((nj,ni))
                        deg_local[i]+=1; deg_local[j]+=1
            # 优先连接
            for new_idx in range(min(m_ba+1,nm),nm):
                new_node=mod[new_idx]
                probs=deg_local[:new_idx]+1; probs/=probs.sum()
                targets=np.random.choice(new_idx,size=min(m_ba,new_idx),replace=False,p=probs)
                for t_idx in targets:
                    t_node=mod[t_idx]
                    w=np.random.uniform(*W_INTRA)
                    bt=2 if new_node>=N_exc or t_node>=N_exc else 0
                    if (new_node,t_node) not in es:
                        sl+=[new_node,t_node]; tl+=[t_node,new_node]
                        wl+=[w,w]; bl+=[bt,bt]
                        es.add((new_node,t_node)); es.add((t_node,new_node))
                        deg_local[new_idx]+=1; deg_local[t_idx]+=1

        # ======== 模块间：稀疏长程连接（弱权重，限制跨模块传播）========
        for i in range(N):
            for j in range(i+1,N):
                if self.node_module[i]!=self.node_module[j]:
                    if np.random.random()<P_INTER_MODULE:
                        w=np.random.uniform(*W_INTER)
                        bt=2 if i>=N_exc or j>=N_exc else 0
                        if (i,j) not in es:
                            sl+=[i,j]; tl+=[j,i]; wl+=[w,w]; bl+=[bt,bt]
                            es.add((i,j)); es.add((j,i))

        self.src=np.array(sl,np.int32); self.tgt=np.array(tl,np.int32)
        self.w=np.array(wl); self.bt=np.array(bl,np.int8)
        ne=len(self.src)
        self.nltp=np.zeros(ne,np.int32); self.nltd=np.zeros(ne,np.int32)
        self.la_ms=np.full(ne,-1e9)

        # LIF 状态
        self.V=np.full(N,V_REST); self.V_t=np.zeros(N)
        self.I_syn=np.zeros(N); self.I_t=np.zeros(N)
        self.ref_end=np.full(N,-1.); self.t_spike=np.full(N,-1e9)
        self.coact_t=np.full(N,-1e9)
        self.fire_cnt=np.zeros(N)
        self.last_scale_t=0.; self.last_triad_t=0.; self.last_sdi_t=0.

        # 感觉神经元（模块0和1中的兴奋神经元）
        sens_pool=[]
        for mod in modules[:max(2,len(modules)//3)]:
            sens_pool.extend([n for n in mod if n<N_exc])
        ns=max(2,int(N*sp_def['sf']))
        self.sens=np.array(sens_pool[:ns],dtype=np.int32); self.stim_ptr=0

        self._build_W()
        C0,L0,sig0=compute_metrics(
            self.src[(self.bt==0)|(self.bt==1)],
            self.tgt[(self.bt==0)|(self.bt==1)],N)
        intra_e=sum(1 for s,t in zip(sl,tl) if self.node_module[s]==self.node_module[t])//2
        inter_e=len(sl)//2-intra_e
        print(f'  [{name}] N={N} mods={len(modules)}(~{n_mod}ea) '
              f'intra={intra_e} inter={inter_e} '
              f'σ₀={sig0:.2f} C₀={C0:.3f}',flush=True)

    def _build_W(self):
        N=self.N; w_eff=self.w.copy()
        w_eff[self.bt==1]*=W_EL_BOOST
        w_eff[(self.bt==2)|(self.bt==3)]*=-0.20  # 抑制稍弱
        self.W=sp.csr_matrix((w_eff,(self.src,self.tgt)),shape=(N,N))
        self.out_nbr={}
        for i,(s,t,w) in enumerate(zip(self.src,self.tgt,w_eff)):
            self.out_nbr.setdefault(int(s),[]).append((int(t),float(w),i))

    def _get_V(self,i,t):
        dt=t-self.V_t[i]
        if dt<=0: return self.V[i]
        dt_I=t-self.I_t[i]
        I_a=(self.I_syn[i]*TAU_SYN/dt_I*(1-np.exp(-dt_I/TAU_SYN))
             if dt_I>0.001 else self.I_syn[i])
        return V_REST+(self.V[i]-V_REST)*np.exp(-dt/TAU_M)+I_a*TAU_M*(1-np.exp(-dt/TAU_M))

    def _next_spike(self,i,t):
        if t<self.ref_end[i]: return np.inf
        V0=self._get_V(i,t); dt_I=t-self.I_t[i]
        I_n=(self.I_syn[i]*np.exp(-dt_I/TAU_SYN) if dt_I>0 else self.I_syn[i])
        asy=V_REST+I_n*TAU_M
        if asy<=V_TH and V0<=V_TH: return np.inf
        if V0>=V_TH: return t
        if abs(V0-asy)<1e-6: return np.inf
        r=(V_TH-asy)/(V0-asy)
        if r<=0 or r>=1: return np.inf
        return t-TAU_M*np.log(r)

    def fire(self,i,t_fire,heap):
        self.V[i]=V_RESET; self.V_t[i]=t_fire
        self.ref_end[i]=t_fire+T_REF; self.t_spike[i]=t_fire
        self.coact_t[i]=t_fire; self.fire_cnt[i]+=1.
        for (j,w_ij,edge_idx) in self.out_nbr.get(i,[]):
            dt_I=t_fire-self.I_t[j]
            self.I_syn[j]=self.I_syn[j]*np.exp(-dt_I/TAU_SYN)+w_ij
            self.I_t[j]=t_fire
            self.V[j]=self._get_V(j,t_fire); self.V_t[j]=t_fire
            t_next=self._next_spike(j,t_fire)
            if t_next<T_SIM and np.isfinite(t_next):
                heapq.heappush(heap,(t_next,j))
            # STDP（精确时刻）
            t_post=self.t_spike[j]
            if t_post>-1e8:
                dt_ms=t_fire-t_post
                if 0<dt_ms<100:
                    self.w[edge_idx]=np.clip(self.w[edge_idx]+0.010*np.exp(-dt_ms/20.),0,1)
                    self.nltp[edge_idx]+=1
                elif -100<dt_ms<0:
                    self.w[edge_idx]=np.clip(self.w[edge_idx]-0.007*np.exp(dt_ms/20.),0,1)
                    self.nltd[edge_idx]+=1
                self.la_ms[edge_idx]=t_fire

    def triadic_closure(self,t_now):
        N=self.N
        # 边数上限：模块内不超过 k_intra*3，总边数不超过 N*k_intra*2.5
        cm=(self.bt==0)|(self.bt==1)
        max_e=int(N*self.sp['k_intra']*2.5)
        if cm.sum()>=max_e: return

        ra=np.where((t_now-self.coact_t<20.)&(self.coact_t>-1e8))[0]
        if len(ra)<3: return
        As=sp.csr_matrix((np.ones(cm.sum()),(self.src[cm],self.tgt[cm])),shape=(N,N))
        A2=As@As
        existing=set(zip(self.src[cm].tolist(),self.tgt[cm].tolist()))
        il_set=set(zip(self.src[(self.bt==2)|(self.bt==3)].tolist(),
                       self.tgt[(self.bt==2)|(self.bt==3)].tolist()))
        ra_mask=np.zeros(N,bool); ra_mask[ra]=True
        new_s,new_t_arr,new_w=[],[],[]

        # 优先在同模块内做三元闭合（保护模块结构）
        for i in ra[:min(15,len(ra))]:
            row=A2.getrow(i)
            cands=row.indices[(row.data>0)&ra_mask[row.indices]]
            for j in cands:
                j=int(j)
                if i!=j and (i,j) not in existing:
                    same_mod=(self.node_module[i]==self.node_module[j])
                    p_add=TRIAD_P if same_mod else TRIAD_P*0.3  # 跨模块三元闭合概率降低
                    # 腔保护：I-L边保护腔结构
                    if (j,i) in il_set and np.random.random()<0.4: continue
                    if np.random.random()<p_add:
                        w_rng=W_INTRA if same_mod else W_INTER
                        new_s.append(i); new_t_arr.append(j)
                        new_w.append(np.random.uniform(*w_rng))
                        existing.add((i,j))
                        if len(new_s)>=MAX_TRIAD_NEW: break
            if len(new_s)>=MAX_TRIAD_NEW: break

        if new_s:
            nn=len(new_s)
            self.src=np.concatenate([self.src,np.array(new_s,np.int32)])
            self.tgt=np.concatenate([self.tgt,np.array(new_t_arr,np.int32)])
            self.w=np.concatenate([self.w,np.array(new_w)])
            self.bt=np.concatenate([self.bt,np.zeros(nn,np.int8)])
            self.nltp=np.concatenate([self.nltp,np.zeros(nn,np.int32)])
            self.nltd=np.concatenate([self.nltd,np.zeros(nn,np.int32)])
            self.la_ms=np.concatenate([self.la_ms,np.full(nn,-1e9)])

    def apply_sdi(self,t_now):
        # 规则1：E-S → E-L（有符号三元调控）
        r1=np.where((self.bt==0)&(self.nltp>=THETA_LTP))[0]
        if len(r1)>0:
            el_nbr={}
            for s,t in zip(self.src[self.bt==1],self.tgt[self.bt==1]):
                el_nbr.setdefault(int(s),set()).add(int(t))
            boosted=[]
            for idx in r1:
                si,ti=int(self.src[idx]),int(self.tgt[idx])
                common=el_nbr.get(si,set())&el_nbr.get(ti,set())
                if common and np.random.random()<TRIAD_EL_BOOST/(TRIAD_EL_BOOST+1):
                    boosted.append(idx)
                elif self.nltp[idx]>=THETA_LTP:
                    boosted.append(idx)
            r1=np.array(boosted,dtype=np.int32)
        if len(r1)>MAX_FIX: np.random.shuffle(r1); r1=r1[:MAX_FIX]
        self.bt[r1]=1; self.nltp[r1]=0

        # 规则4：E-L衰减
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
        # WS重连（模块间跨越，保持短路径L）
        rf=np.where(self.fire_cnt>0)[0]
        cm2=(self.bt==0)|(self.bt==1)
        if len(rf)>2 and cm2.sum()<int(self.N*self.sp['k_intra']*2.5):
            idle=np.where(cm2&(t_now-self.la_ms>800))[0]
            if len(idle)>0:
                np.random.shuffle(idle); rw=idle[:min(4,len(idle))]
                es_set=set(zip(self.src[cm2].tolist(),self.tgt[cm2].tolist()))
                for ri in rw:
                    if np.random.random()<P_REWIRE:
                        i=int(self.src[ri]); j=int(np.random.choice(rf))
                        # 优先选不同模块的活跃节点（维持L短）
                        diff_mod=[n for n in rf if self.node_module[n]!=self.node_module[i]]
                        if diff_mod and np.random.random()<0.6:
                            j=int(np.random.choice(diff_mod))
                        if j!=i and (i,j) not in es_set:
                            es_set.discard((i,int(self.tgt[ri])))
                            self.tgt[ri]=j; es_set.add((i,j))
        # 突触缩放
        if t_now-self.last_scale_t>=SCALING_INT_MS and t_now>500:
            dt_s=t_now-self.last_scale_t
            rate=self.fire_cnt/dt_s*1000; self.fire_cnt[:]=0.; self.last_scale_t=t_now
            exc_s=self.bt==0
            hot=np.where(rate>20.)[0]
            if len(hot)>0:
                mask=exc_s&np.isin(self.tgt,hot)
                if mask.sum()>0: self.w[mask]=np.clip(self.w[mask]*.95,.005,1.)
            cold=np.where((rate>.01)&(rate<2.))[0]
            if len(cold)>0:
                mask=exc_s&np.isin(self.tgt,cold)
                if mask.sum()>0: self.w[mask]=np.clip(self.w[mask]*1.05,.005,1.)
        self._build_W()

    def el_r(self):
        cm=(self.bt==0)|(self.bt==1)
        return float((self.bt==1).sum())/max(1,cm.sum())

    def run_once(self):
        N=self.N; heap=[]; t_now=0.
        n_bins=int(T_SIM/T_BIN)+2
        bin_act=[set() for _ in range(n_bins)]  # 神经元级去重
        stim_count=0; n_spk=0
        next_sdi=500.; next_triad=TRIAD_INT_MS
        t0=time.time()

        while t_now<T_SIM:
            next_stim=stim_count*T_STIM
            next_heap=heap[0][0] if heap else np.inf
            next_t=min(next_stim,next_sdi,next_triad,next_heap)
            if next_t>=T_SIM: break
            t_now=next_t

            if stim_count*T_STIM<=t_now+1e-6 and t_now<=stim_count*T_STIM+1e-6:
                si=int(self.sens[self.stim_ptr%len(self.sens)])
                self.stim_ptr+=1
                self.V[si]=V_TH+1.0; self.V_t[si]=t_now
                ts=self._next_spike(si,t_now)
                if ts<T_SIM: heapq.heappush(heap,(ts,si))
                stim_count+=1

            if abs(t_now-next_sdi)<1e-6:
                self.apply_sdi(t_now); next_sdi+=500.
            if abs(t_now-next_triad)<1e-6:
                self.triadic_closure(t_now); next_triad+=TRIAD_INT_MS

            fired_n=0
            while heap and heap[0][0]<=t_now+1e-6:
                t_fire,i=heapq.heappop(heap)
                if t_fire<self.ref_end[i]: continue
                if self._get_V(i,t_fire)<V_TH-1.5: continue
                self.fire(i,t_fire,heap)
                bi=int(t_fire/T_BIN)
                if bi<n_bins: bin_act[bi].add(i)
                n_spk+=1; fired_n+=1
                if fired_n>N*2: break  # 更严格的超临界截止

        # 提取雪崩（神经元级去重）
        bin_counts=[len(s) for s in bin_act]
        avalanches=[]; in_av=False; cur_av=0
        for bc in bin_counts:
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
                'n_spikes':n_spk,'elapsed':round(time.time()-t0,1)}

def run_species(name,sp_def):
    print(f'\n{"="*55}\n{name}  N={sp_def["N"]}  [{sp_def["level"]}]\n{"="*55}',flush=True)
    all_runs=[]
    for seed in SEEDS:
        net=Modular_LIF_SDI(name,sp_def,seed)
        r=net.run_once(); r['seed']=seed
        alp_s=f'{r["alpha"]:.3f}' if r['alpha'] else 'N/A'
        print(f'  seed={seed}: σ={r["sigma"]:.3f} C={r["C"]:.3f} '
              f'L={r["L"]:.3f} α={alp_s} EL={r["el"]:.1%} '
              f'av={r["n_av"]}(μ={r["mean_av"]:.1f}) ({r["elapsed"]:.1f}s)',flush=True)
        all_runs.append(r)

    def stats(key):
        vals=[r[key] for r in all_runs if r.get(key) is not None]
        return (float(np.mean(vals)),float(np.std(vals))) if vals else (None,0.)

    tgt=sp_def['tgt']
    def ok(v,r_):
        if v is None: return False
        lo,hi=r_; return (lo is None or v>=lo) and (hi is None or v<=hi)

    final={}
    for m in ['sigma','C','L','alpha','el']:
        mu,sd=stats(m); final[m]=mu; final[f'{m}_std']=sd
        final[f'pass_{m}']=ok(mu,tgt[m])
    final['score']=sum(bool(final[f'pass_{m}']) for m in ['sigma','C','L','alpha','el'])
    final.update({'runs':all_runs,'level':sp_def['level'],
                  'bio':sp_def['bio'],'ref':sp_def['ref']})

    print(f'\n--- {name} SUMMARY ({len(SEEDS)} seeds) ---')
    for m in ['sigma','C','L','alpha','el']:
        mu=final[m]; sd=final[f'{m}_std']
        lo,hi=tgt[m]; ts=f'≥{lo}' if lo and not hi else f'[{lo},{hi}]' if lo and hi else f'≤{hi}'
        vs=f'{mu:.3f}±{sd:.3f}' if mu is not None else 'N/A'
        print(f'  {"✅" if final[f"pass_{m}"] else "❌"} {m:6s}: {vs}  ({ts})')
    print(f'  SCORE: {final["score"]}/5  [{sp_def["level"]}]')
    return final

def main():
    all_r={}; t0=time.time()
    for name,sp_def in SPECIES.items():
        all_r[name]=run_species(name,sp_def)

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
    with open(f'{OUT}/exp1_v19_results.json','w') as f:
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
    plt.suptitle('SDI Exp1 v19 — 模块化两层结构\n'
                 '(MT-α模块内高C) + (MT-γ模块间稀疏) → 高C + 幂律alpha + 小世界',
                 fontsize=11,fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{OUT}/exp1_v19_convergence.png',dpi=130,bbox_inches='tight')
    plt.close()
    print('Results → exp1_v19_results.json')
    print('Plot → exp1_v19_convergence.png')
    print('DONE')

if __name__=='__main__':
    main()
