#!/usr/bin/env python3
"""
SDI 实验一 v3 — 完整规则，向量化三元闭合，真正有效
核心修复：
  1. 三元闭合全向量化（A@A矩阵找共同邻居），每步都执行
  2. EL比例硬性胶质控制，E-L不会无限积累
  3. THETA_LTP=150，T_DECAY=300，避免结晶死锁
  4. 结构化刺激：8模式空间局部性
  5. N_STEPS=6000
"""
import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
import json, time
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(42)
OUT = '/home/work/.openclaw/workspace/sdi_sim'

# ======== 参数 ========
THETA_LTP    = 150
THETA_LTD    = 20
T_DECAY      = 300
Ea_S, Ea_L   = 0.15, 0.85
EI_RATIO     = 4.0
TAU_STDP     = 20.0
ETA_LTP      = 0.012
ETA_LTD      = 0.008
EL_LO, EL_HI = 0.15, 0.22
CASCADE_MAX  = 15
T_ABS, T_REL, REL_SCALE = 3, 8, 0.4
MAX_FIX      = 5       # 每步最多固化
MAX_NEW      = 6       # 每步最多新建
N_STEPS      = 6000
LOG_INT      = 200
GLIA_INT     = 30      # 每30步检查EL比例并降级

SPECIES = {
    'C.elegans':       {'N':279,  'k':16.4, 'sf':0.22,
        'bio':{'sigma':4.71,'C':0.337,'L':2.44,'alpha':2.32,'el':0.191},
        'tgt':{'sigma':(4.0,None),'C':(0.25,None),'L':(2.0,3.5),'alpha':(1.5,2.5),'el':(0.15,0.28)}},
    'Larval_Droso':    {'N':321,  'k':51.6, 'sf':0.20,
        'bio':{'sigma':None,'C':0.25,'L':2.1,'alpha':2.0,'el':0.18},
        'tgt':{'sigma':(3.0,None),'C':(0.20,None),'L':(1.5,3.5),'alpha':(1.5,2.5),'el':(0.15,0.28)}},
    'Rat_Cortex':      {'N':73,   'k':26.3, 'sf':0.15,
        'bio':{'sigma':3.0,'C':0.42,'L':1.9,'alpha':2.0,'el':0.18},
        'tgt':{'sigma':(2.5,None),'C':(0.30,None),'L':(1.5,3.0),'alpha':(1.5,2.5),'el':(0.15,0.28)}},
    'Mouse_Cortex':    {'N':112,  'k':58.4, 'sf':0.15,
        'bio':{'sigma':3.2,'C':0.45,'L':1.8,'alpha':2.1,'el':0.20},
        'tgt':{'sigma':(2.5,None),'C':(0.35,None),'L':(1.5,3.0),'alpha':(1.5,2.5),'el':(0.15,0.28)}},
    'Macaque_Cortex':  {'N':242,  'k':16.9, 'sf':0.12,
        'bio':{'sigma':3.8,'C':0.55,'L':2.3,'alpha':2.2,'el':0.20},
        'tgt':{'sigma':(3.0,None),'C':(0.40,None),'L':(2.0,3.5),'alpha':(1.5,2.5),'el':(0.15,0.28)}},
}

# ======== 指标函数 ========
def metrics(src, tgt, N):
    if len(src) == 0: return 0.,99.,0.
    r = np.concatenate([src,tgt]); c = np.concatenate([tgt,src])
    adj = sp.csr_matrix((np.ones(len(r)),(r,c)),shape=(N,N)); adj.data[:]=1.
    nc,lbl = connected_components(adj,directed=False)
    sz = np.bincount(lbl); lc = lbl==sz.argmax(); n=int(lc.sum())
    if n<8: return 0.,99.,0.
    on = -np.ones(N,int); on[lc]=np.arange(n)
    em=lc[src]&lc[tgt]; ls=on[src[em]]; lt=on[tgt[em]]
    a=sp.csr_matrix((np.ones(len(ls)*2),(np.r_[ls,lt],np.r_[lt,ls])),shape=(n,n)); a.data[:]=1.
    deg=np.array(a.sum(1)).flatten()
    tri=np.array(a.multiply(a@a).sum(1)).flatten()/2.
    dm=deg*(deg-1); vm=dm>0
    C=float(np.mean(tri[vm]/dm[vm])) if vm.any() else 0.
    np.random.seed(0)
    samp=np.random.choice(n,min(40,n),replace=False); ds=[]
    for s in samp:
        vi={int(s):0}; q=[int(s)]; qi=0
        while qi<len(q) and len(vi)<min(120,n):
            u=q[qi]; qi+=1
            for v in a.getrow(u).indices:
                if int(v) not in vi: vi[int(v)]=vi[u]+1; q.append(int(v)); ds.append(vi[int(v)])
    L=float(np.mean(ds)) if ds else 99.
    m=a.nnz//2; p=2*m/(n*(n-1)) if n>1 else 1e-6
    Cr=max(p,1e-9); Lr=np.log(n)/np.log(max(2,n*p))
    sigma=(C/Cr)/(L/max(Lr,.01)) if L>0 else 0.
    return C,L,sigma

def alpha_fit(av):
    av=np.array(av); av=av[av>0]
    if len(av)<15: return None
    lc,be=np.histogram(np.log(av),bins=12)
    bc=(be[:-1]+be[1:])/2; v=lc>2
    if v.sum()<4: return None
    s=np.polyfit(bc[v],np.log(lc[v]+1),1)[0]
    return float(-s)

# ======== SDI 网络 ========
class SDI:
    def __init__(self, name, sp):
        self.name=name; self.N=sp['N']; self.sp=sp; self.t=0
        N=self.N
        ns=max(3,int(N*sp['sf']))
        self.sens=np.arange(ns)
        # 8种感觉模式（空间局部）
        K=8; spk=max(2,ns//K)
        self.pats=[]
        for k in range(K):
            ps=list(range(k*spk,min((k+1)*spk,ns)))
            if N>ns:
                po=np.random.choice(np.arange(ns,N),min(4,N-ns),replace=False).tolist()
            else: po=[]
            self.pats.append(ps+po)
        self.cp=0; self.pc=0

        # 初始图
        p=sp['k']/(N-1)
        sl,tl,wl,bl=[],[],[],[]
        for i in range(N):
            for j in range(i+1,N):
                if np.random.random()<p:
                    w=np.random.uniform(.05,.3)
                    exc=np.random.random()<.8
                    bt=0 if exc else 2
                    sl.append(i);tl.append(j);wl.append(w);bl.append(bt)
                    if np.random.random()<.3:
                        sl.append(j);tl.append(i);wl.append(w*.7);bl.append(bt)
        self.src=np.array(sl,np.int32); self.tgt=np.array(tl,np.int32)
        self.w=np.array(wl); self.bt=np.array(bl,np.int8)
        ne=len(self.src)
        self.nltp=np.zeros(ne,np.int32); self.nltd=np.zeros(ne,np.int32)
        self.la=np.full(ne,-99999,np.int32); self.lf=np.full(N,-99999,np.int32)
        self._rb()
        print(f'  [{name}] N={N} edges={ne} sens={ns}',flush=True)

    def _rb(self):
        N=self.N; exc=(self.bt==0)|(self.bt==1)
        we=np.where(exc,self.w,-0.25*self.w)
        self.W=sp.csr_matrix((we,(self.src,self.tgt)),shape=(N,N))

    def stim(self):
        T=12
        if self.pc>=T:
            self.pc=0
            self.cp=(self.cp+1)%len(self.pats) if np.random.random()>.05 else np.random.randint(len(self.pats))
        self.pc+=1
        seeds=list(self.pats[self.cp])
        spont=np.random.choice(self.N,max(1,int(self.N*.01)),replace=False).tolist()
        return list(set(seeds+spont))

    def cascade(self,seeds):
        N=self.N
        seeds=[s for s in seeds if self.t-self.lf[s]>=T_ABS]
        if not seeds: return np.zeros(N,bool),0
        act=np.zeros(N,bool); act[seeds]=True; aa=act.copy()
        self.lf[seeds]=self.t
        for _ in range(CASCADE_MAX):
            sig=self.W@act.astype(float)
            inh=max(0,(aa.sum()/N-.20)*5.)
            dt=self.t-self.lf; rs=np.ones(N)
            rs[dt<T_ABS]=0.; rs[(dt>=T_ABS)&(dt<T_REL)]=REL_SCALE
            p=np.clip(sig*(1-inh)*rs,0,1)
            nf=(p>np.random.random(N))&(~aa)
            if not nf.any(): break
            self.lf[nf]=self.t; aa|=nf; act=nf
        return aa,int(aa.sum())

    def stdp(self,am):
        fi=np.where(am)[0]
        if not len(fi): return
        em=(self.bt<=2)&(np.isin(self.src,fi)|np.isin(self.tgt,fi))
        if not em.any(): return
        idx=np.where(em)[0]
        dt=self.lf[self.src[idx]]-self.lf[self.tgt[idx]]
        lp=(dt>0)&(dt<200)
        if lp.any():
            self.w[idx[lp]]=np.clip(self.w[idx[lp]]+ETA_LTP*np.exp(-dt[lp]/TAU_STDP),0,1)
            self.nltp[idx[lp]]+=1
        ld=(dt<0)&(dt>-200)
        if ld.any():
            self.w[idx[ld]]=np.clip(self.w[idx[ld]]-ETA_LTD*np.exp(dt[ld]/TAU_STDP),0,1)
            self.nltd[idx[ld]]+=1
        self.la[em]=self.t

    def rules(self,am):
        N=self.N
        # 规则1：E-S→E-L（固化，限速）
        r1=np.where((self.bt==0)&(self.nltp>=THETA_LTP))[0]
        if len(r1)>MAX_FIX:
            np.random.shuffle(r1); r1=r1[:MAX_FIX]
        self.bt[r1]=1; self.nltp[r1]=0

        # 规则4：E-L→E-S（衰减）
        self.bt[(self.bt==1)&(self.t-self.la>T_DECAY)]=0

        # 胶质控制：EL比例超标→降级最旧E-L键
        cm=(self.bt==0)|(self.bt==1)
        el_r=float((self.bt==1).sum())/max(1,cm.sum())
        if el_r>EL_HI and self.t%GLIA_INT==0:
            el_idx=np.where(self.bt==1)[0]
            n_degrade=max(3,len(el_idx)//8)
            stale=el_idx[np.argsort(self.la[el_idx])[:n_degrade]]
            self.bt[stale]=0; self.nltp[stale]=0

        # 规则2：I-S消除
        kill=(self.bt==2)&(self.nltd>=THETA_LTD)
        kill|=(self.bt==2)&(self.w<0.015)&(self.t-self.la>400)
        keep=~kill
        self.src=self.src[keep]; self.tgt=self.tgt[keep]
        self.w=self.w[keep]; self.bt=self.bt[keep]
        self.nltp=self.nltp[keep]; self.nltd=self.nltd[keep]
        self.la=self.la[keep]

        # ======================================================
        # 规则3：三元闭合（向量化核心）+ FEP新建
        # ======================================================
        am_arr=np.where(am)[0]
        if len(am_arr)==0: return

        # 构建当前邻接矩阵（二值化）
        cm2=(self.bt==0)|(self.bt==1)
        if cm2.sum()==0: return
        As=sp.csr_matrix((np.ones(cm2.sum()),(self.src[cm2],self.tgt[cm2])),shape=(N,N))

        # 激活向量
        am_vec=np.zeros(N); am_vec[am_arr]=1.

        # 三元闭合：A→B→C中，A与C有共同激活邻居B
        # A2[i,j] = A和j的共同邻居数
        A2=As@As  # N×N，A2[i,j]=i和j的共同邻居数

        # 找：(i,j)不存在边，但A2[i,j]>0，且j在am_arr中
        existing=sp.csr_matrix((np.ones(cm2.sum()),(self.src[cm2],self.tgt[cm2])),shape=(N,N))
        existing.data[:]=1.

        # 候选：am_arr中的节点j，与低度节点i有共同邻居
        deg=np.array(As.sum(1)).flatten()
        low_mask=deg<max(2,deg.mean()*0.6)

        # 对am_arr中的节点，找有共同邻居但无直连的低度源节点
        am_col=sp.csr_matrix((np.ones(len(am_arr)),(np.zeros(len(am_arr),int),am_arr)),shape=(1,N))
        shared=(As@am_col.T).T  # 1×N → 每个节点与am_arr中某节点的共同邻居数
        shared_arr=np.array(shared.todense()).flatten()

        new_s,new_t=[],[]
        existing_set=set(zip(self.src[cm2].tolist(),self.tgt[cm2].tolist()))

        # 找候选对：低度节点 i 与 am_arr 中节点 j 有共同邻居
        low_nodes=np.where(low_mask)[0]
        if len(low_nodes)>0:
            # 对每个低度节点i，找A2[i,j]>0且j∈am_arr且无现有边的j
            for i in low_nodes[:min(20,len(low_nodes))]:
                row=A2.getrow(i)
                cands=row.indices[row.data>0]  # 有共同邻居的节点
                cands_am=np.intersect1d(cands,am_arr)  # 且在激活集中
                for j in cands_am:
                    j=int(j)
                    if i!=j and (i,j) not in existing_set:
                        new_s.append(i); new_t.append(j)
                        existing_set.add((i,j))
                        if len(new_s)>=MAX_NEW: break
                if len(new_s)>=MAX_NEW: break

        # 不够MAX_NEW时，FEP补充：低度节点连接高活跃节点
        if len(new_s)<MAX_NEW:
            act_score=np.zeros(N); act_score[am_arr]=1.
            for i in low_nodes[:MAX_NEW-len(new_s)]:
                j=int(am_arr[np.random.randint(len(am_arr))])
                if i!=j and (i,j) not in existing_set:
                    new_s.append(i); new_t.append(j)
                    existing_set.add((i,j))

        if new_s:
            nn=len(new_s)
            self.src=np.concatenate([self.src,np.array(new_s,np.int32)])
            self.tgt=np.concatenate([self.tgt,np.array(new_t,np.int32)])
            self.w=np.concatenate([self.w,np.random.uniform(.05,.15,nn)])
            self.bt=np.concatenate([self.bt,np.zeros(nn,np.int8)])
            self.nltp=np.concatenate([self.nltp,np.zeros(nn,np.int32)])
            self.nltd=np.concatenate([self.nltd,np.zeros(nn,np.int32)])
            self.la=np.concatenate([self.la,np.full(nn,self.t,np.int32)])

        self._rb()

    def el_r(self):
        cm=(self.bt==0)|(self.bt==1)
        return float((self.bt==1).sum())/max(1,cm.sum())

    def run(self):
        logs={'step':[],'sigma':[],'C':[],'L':[],'alpha':[],'el':[],'ne':[]}
        avs=[]; t0=time.time()
        for step in range(N_STEPS):
            self.t=step
            seeds=self.stim()
            am,av=self.cascade(seeds)
            if av>0: avs.append(av)
            self.stdp(am)
            self.rules(am)

            if step%LOG_INT==0 and step>0:
                cm=(self.bt==0)|(self.bt==1)
                C,L,sig=metrics(self.src[cm],self.tgt[cm],self.N)
                alp=alpha_fit(avs[-200:])
                el=self.el_r()
                logs['step'].append(step); logs['sigma'].append(round(sig,3))
                logs['C'].append(round(C,4)); logs['L'].append(round(L,3))
                logs['alpha'].append(round(alp,3) if alp else None)
                logs['el'].append(round(el,4)); logs['ne'].append(int(cm.sum()))
                as_='N/A' if alp is None else f'{alp:.3f}'
                print(f'  {step:5d}: σ={sig:.3f} C={C:.3f} L={L:.3f} '
                      f'α={as_} EL={el:.1%} e={cm.sum()}',flush=True)

        cm=(self.bt==0)|(self.bt==1)
        C,L,sig=metrics(self.src[cm],self.tgt[cm],self.N)
        alp=alpha_fit(avs[-500:]); el=self.el_r()
        tgt=self.sp['tgt']
        def ok(v,r):
            if v is None: return False
            lo,hi=r
            return (lo is None or v>=lo) and (hi is None or v<=hi)
        res={'sigma':sig,'C':C,'L':L,'alpha':alp,'el':el,
             'pass_sigma':ok(sig,tgt['sigma']),'pass_C':ok(C,tgt['C']),
             'pass_L':ok(L,tgt['L']),'pass_alpha':ok(alp,tgt['alpha']),
             'pass_el':ok(el,tgt['el']),'elapsed':round(time.time()-t0,1),'logs':logs}
        res['score']=sum(res[k] for k in ['pass_sigma','pass_C','pass_L','pass_alpha','pass_el'])
        print(f'\n--- {self.name} FINAL ({res["elapsed"]:.1f}s) ---')
        for m,v,r,ok_ in [('sigma',sig,tgt['sigma'],res['pass_sigma']),
                           ('C',C,tgt['C'],res['pass_C']),
                           ('L',L,tgt['L'],res['pass_L']),
                           ('alpha',alp,tgt['alpha'],res['pass_alpha']),
                           ('EL',el,tgt['el'],res['pass_el'])]:
            vs=f'{v:.3f}' if v is not None else 'N/A'
            print(f'  {"✅" if ok_ else "❌"} {m}={vs}  target={r}')
        print(f'  SCORE: {res["score"]}/5')
        return res

def main():
    all_r={}; t0=time.time()
    for name,sp in SPECIES.items():
        print(f'\n{"="*55}\nSPECIES: {name}  N={sp["N"]}\n{"="*55}',flush=True)
        net=SDI(name,sp); all_r[name]=net.run()

    print(f'\n{"="*55}\nALL DONE  {time.time()-t0:.1f}s\n{"="*55}')
    for n,r in all_r.items():
        print(f'  {n}: {r["score"]}/5  σ={r["sigma"]:.2f} C={r["C"]:.3f} '
              f'L={r["L"]:.2f} α={r["alpha"]} EL={r["el"]:.1%}')

    save={n:{k:v for k,v in r.items() if k!='logs'} for n,r in all_r.items()}
    for n,r in all_r.items(): save[n]['logs']=r['logs']
    with open(f'{OUT}/exp1_v3_results.json','w') as f: json.dump(save,f,indent=2)

    # 收敛曲线
    fig,axes=plt.subplots(5,5,figsize=(22,18))
    mkeys=[('sigma','sigma','blue'),('C','C','green'),('L','L','orange'),
           ('alpha','alpha','red'),('el','EL ratio','purple')]
    for row,(name,r) in enumerate(all_r.items()):
        lg=r['logs']; bio=SPECIES[name]['bio']; tg=SPECIES[name]['tgt']
        for col,(mk,ml,col_) in enumerate(mkeys):
            ax=axes[row][col]
            vs=[(s,v) for s,v in zip(lg['step'],lg[mk]) if v is not None]
            if vs:
                xs,ys=zip(*vs); ax.plot(xs,ys,color=col_,lw=1.8)
            lo,hi=tg[mk]
            if lo: ax.axhline(lo,color='g',ls='--',lw=1,alpha=.7)
            if hi: ax.axhline(hi,color='r',ls='--',lw=1,alpha=.7)
            bv=bio.get(mk)
            if bv: ax.axhline(bv,color='k',ls=':',lw=1.5)
            ok_=r[f'pass_{mk}']
            ax.set_title(f'{name[:8]}\n{ml}',fontsize=7,
                         color='darkgreen' if ok_ else 'darkred')
            ax.tick_params(labelsize=6); ax.grid(alpha=.3)
    plt.suptitle('SDI Exp1 v3 — Full Rules + Vectorized Triadic Closure',
                 fontsize=11,fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{OUT}/exp1_v3_convergence.png',dpi=130,bbox_inches='tight')
    plt.close(); print('Plot saved. DONE')

if __name__=='__main__':
    main()
