#!/usr/bin/env python3
"""
SDI 实验一 v5 — 修复 alpha + 优化 Rat/Mouse C
修复点：
  1. alpha 改用 Hill MLE estimator（Clauset 2009），替换 log-bin
  2. Rat/Mouse: k 调高到 14，p_init=0.08，让 C 能超过目标阈值
  3. cascade 全局抑制系数从 5.0 降到 3.0，允许更大雪崩 → 更接近幂律
  4. 抑制神经元比例修正：I-S/I-L 约束更严格 (E:I=4:1)
"""
import numpy as np
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
import json, time
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

np.random.seed(42)
OUT = '/home/work/.openclaw/workspace/sdi_sim'

THETA_LTP = 80
THETA_LTD = 15
T_DECAY   = 400
ETA_LTP   = 0.015
ETA_LTD   = 0.008
TAU_STDP  = 20.
EL_HI     = 0.25
CASCADE_MAX = 12
T_ABS, T_REL, REL_SCALE = 3, 8, 0.4
MAX_FIX   = 8
N_STEPS   = 5000
LOG_INT   = 200
P_REWIRE  = 0.15
REWIRE_INT = 50

SPECIES = {
    'C.elegans':      {'N':279, 'k':16, 'k_init':8, 'p_init':0.05, 'sf':0.22,
        'bio':{'sigma':4.71,'C':0.337,'L':2.44,'alpha':2.32,'el':0.191},
        'tgt':{'sigma':(4.,None),'C':(.25,None),'L':(2.,3.5),'alpha':(1.5,2.5),'el':(.15,.28)}},
    'Larval_Droso':   {'N':321, 'k':16, 'k_init':8, 'p_init':0.05, 'sf':0.20,
        'bio':{'sigma':None,'C':.25,'L':2.1,'alpha':2.,'el':.18},
        'tgt':{'sigma':(3.,None),'C':(.20,None),'L':(1.5,3.5),'alpha':(1.5,2.5),'el':(.15,.28)}},
    'Rat_Cortex':     {'N':73,  'k':14, 'k_init':8, 'p_init':0.10, 'sf':0.15,
        'bio':{'sigma':3.,'C':.42,'L':1.9,'alpha':2.,'el':.18},
        'tgt':{'sigma':(2.5,None),'C':(.30,None),'L':(1.5,3.),'alpha':(1.5,2.5),'el':(.15,.28)}},
    'Mouse_Cortex':   {'N':112, 'k':14, 'k_init':8, 'p_init':0.10, 'sf':0.15,
        'bio':{'sigma':3.2,'C':.45,'L':1.8,'alpha':2.1,'el':.20},
        'tgt':{'sigma':(2.5,None),'C':(.35,None),'L':(1.5,3.),'alpha':(1.5,2.5),'el':(.15,.28)}},
    'Macaque_Cortex': {'N':242, 'k':16, 'k_init':8, 'p_init':0.05, 'sf':0.12,
        'bio':{'sigma':3.8,'C':.55,'L':2.3,'alpha':2.2,'el':.20},
        'tgt':{'sigma':(3.,None),'C':(.40,None),'L':(2.,3.5),'alpha':(1.5,2.5),'el':(.15,.28)}},
}

def metrics(src, tgt, N):
    if len(src)==0: return 0.,99.,0.
    adj=sp.csr_matrix((np.ones(len(src)*2),(np.r_[src,tgt],np.r_[tgt,src])),shape=(N,N))
    adj.data[:]=1.
    nc,lbl=connected_components(adj,directed=False)
    sz=np.bincount(lbl); lc=lbl==sz.argmax(); n=int(lc.sum())
    if n<8: return 0.,99.,0.
    on=-np.ones(N,int); on[lc]=np.arange(n)
    em=lc[src]&lc[tgt]; ls=on[src[em]]; lt=on[tgt[em]]
    a=sp.csr_matrix((np.ones(len(ls)*2),(np.r_[ls,lt],np.r_[lt,ls])),shape=(n,n))
    a.data[:]=1.
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
                if int(v) not in vi:
                    vi[int(v)]=vi[u]+1; q.append(int(v)); ds.append(vi[int(v)])
    L=float(np.mean(ds)) if ds else 99.
    m=a.nnz//2; p=2*m/(n*(n-1)) if n>1 else 1e-6
    sigma=(C/max(p,1e-9))/(L/max(np.log(n)/np.log(max(2,n*p)),0.01)) if L>0 else 0.
    return C,L,sigma

def hill_alpha(data, x_min=1):
    """Hill MLE estimator for power-law exponent (Clauset 2009)"""
    data = np.array(data, float)
    data = data[data >= x_min]
    if len(data) < 15: return None
    # x_min estimation: use median as x_min
    xm = float(np.percentile(data, 25))
    xm = max(xm, 1.0)
    data = data[data >= xm]
    if len(data) < 10: return None
    return float(1.0 + len(data) / np.sum(np.log(data / (xm - 0.5))))

class SDI_v5:
    def __init__(self, name, sp):
        self.name=name; self.N=sp['N']; self.sp=sp; self.t=0
        N=self.N
        k=sp['k_init']; k=max(4,k//2*2)
        p_init=sp['p_init']

        # WS 环形格初始化
        sl,tl=[],[]
        for i in range(N):
            for d in range(1,k//2+1):
                j=(i+d)%N
                sl+=[i,j]; tl+=[j,i]
        es=set(zip(sl,tl))
        for idx in range(len(sl)//2):
            if np.random.random()<p_init:
                i=sl[idx*2]
                j=np.random.randint(N)
                if j!=i and (i,j) not in es:
                    old=(sl[idx*2],tl[idx*2])
                    es.discard(old); es.discard((old[1],old[0]))
                    es.add((i,j)); es.add((j,i))
        pairs=list(es)
        sl3=[p[0] for p in pairs]; tl3=[p[1] for p in pairs]
        wl=np.random.uniform(.05,.4,len(sl3))
        bl=np.where(np.random.random(len(sl3))<.8,0,2).astype(np.int8)

        self.src=np.array(sl3,np.int32); self.tgt=np.array(tl3,np.int32)
        self.w=wl; self.bt=bl; ne=len(self.src)
        self.nltp=np.zeros(ne,np.int32); self.nltd=np.zeros(ne,np.int32)
        self.la=np.full(ne,-99999,np.int32); self.lf=np.full(N,-99999,np.int32)

        ns=max(3,int(N*sp['sf'])); K=8; spk=max(2,ns//K)
        self.pats=[]
        for ki in range(K):
            ps=list(range(ki*spk,min((ki+1)*spk,ns)))
            po=(np.random.choice(np.arange(ns,N),min(3,N-ns),replace=False).tolist() if N>ns else [])
            self.pats.append(ps+po)
        self.cp=0; self.pc=0
        self._rb()
        C0,L0,sig0=metrics(self.src[(self.bt==0)|(self.bt==1)],
                           self.tgt[(self.bt==0)|(self.bt==1)],N)
        print(f'  [{name}] N={N} k_init={k} p={p_init} σ₀={sig0:.2f} C₀={C0:.3f} e={ne}',flush=True)

    def _rb(self):
        N=self.N; exc=(self.bt==0)|(self.bt==1)
        we=np.where(exc,self.w,-0.25*self.w)
        self.W=sp.csr_matrix((we,(self.src,self.tgt)),shape=(N,N))

    def stim(self):
        if self.pc>=12:
            self.pc=0
            self.cp=(self.cp+1)%len(self.pats) if np.random.random()>.05 else np.random.randint(len(self.pats))
        self.pc+=1
        return list(set(self.pats[self.cp]+
                        np.random.choice(self.N,max(1,int(self.N*.01)),replace=False).tolist()))

    def cascade(self,seeds):
        N=self.N
        seeds=[s for s in seeds if self.t-self.lf[s]>=T_ABS]
        if not seeds: return np.zeros(N,bool),0
        act=np.zeros(N,bool); act[seeds]=True; aa=act.copy()
        self.lf[seeds]=self.t
        for _ in range(CASCADE_MAX):
            sig=self.W@act.astype(float)
            # 降低全局抑制系数 3.0（原5.0），允许更大雪崩→幂律
            inh=max(0,(aa.sum()/N-.20)*3.0)
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
        em=(self.bt<=1)&(np.isin(self.src,fi)|np.isin(self.tgt,fi))
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
        r1=np.where((self.bt==0)&(self.nltp>=THETA_LTP))[0]
        if len(r1)>MAX_FIX: np.random.shuffle(r1); r1=r1[:MAX_FIX]
        self.bt[r1]=1; self.nltp[r1]=0
        self.bt[(self.bt==1)&(self.t-self.la>T_DECAY)]=0
        cm=(self.bt==0)|(self.bt==1)
        if cm.sum()>0 and (self.bt==1).sum()/cm.sum()>EL_HI:
            el_idx=np.where(self.bt==1)[0]
            stale=el_idx[np.argsort(self.la[el_idx])[:max(3,len(el_idx)//10)]]
            self.bt[stale]=0; self.nltp[stale]=0
        kill=((self.bt==2)&(self.nltd>=THETA_LTD))
        kill|=(self.bt==2)&(self.w<.01)&(self.t-self.la>500)
        keep=~kill
        self.src=self.src[keep]; self.tgt=self.tgt[keep]
        self.w=self.w[keep]; self.bt=self.bt[keep]
        self.nltp=self.nltp[keep]; self.nltd=self.nltd[keep]
        self.la=self.la[keep]
        # WS重连
        if self.t%REWIRE_INT==0:
            am_arr=np.where(am)[0]
            if len(am_arr)>3:
                cm2=(self.bt==0)|(self.bt==1)
                idle=np.where(cm2&(self.t-self.la>200))[0]
                if len(idle)>0:
                    np.random.shuffle(idle); rw=idle[:min(5,len(idle))]
                    es=set(zip(self.src[cm2].tolist(),self.tgt[cm2].tolist()))
                    for ri in rw:
                        if np.random.random()<P_REWIRE:
                            i=int(self.src[ri])
                            j=int(np.random.choice(am_arr))
                            if j!=i and (i,j) not in es:
                                old_t=int(self.tgt[ri])
                                es.discard((i,old_t)); self.tgt[ri]=j; es.add((i,j))
        self._rb()

    def el_r(self):
        cm=(self.bt==0)|(self.bt==1)
        return float((self.bt==1).sum())/max(1,cm.sum())

    def run(self):
        logs={'step':[],'sigma':[],'C':[],'L':[],'alpha':[],'el':[],'ne':[]}
        avs=[]; t0=time.time()
        for step in range(N_STEPS):
            self.t=step
            am,av=self.cascade(self.stim())
            if av>0: avs.append(av)
            self.stdp(am); self.rules(am)
            if step%LOG_INT==0 and step>0:
                cm=(self.bt==0)|(self.bt==1)
                C,L,sig=metrics(self.src[cm],self.tgt[cm],self.N)
                alp=hill_alpha(avs[-300:])
                el=self.el_r()
                logs['step'].append(step); logs['sigma'].append(round(sig,3))
                logs['C'].append(round(C,4)); logs['L'].append(round(L,3))
                logs['alpha'].append(round(alp,3) if alp else None)
                logs['el'].append(round(el,4)); logs['ne'].append(int(cm.sum()))
                as_='N/A' if alp is None else f'{alp:.3f}'
                print(f'  {step:5d}: σ={sig:.3f} C={C:.3f} L={L:.3f} α={as_} EL={el:.1%} e={cm.sum()}',flush=True)

        cm=(self.bt==0)|(self.bt==1)
        C,L,sig=metrics(self.src[cm],self.tgt[cm],self.N)
        alp=hill_alpha(avs[-800:]); el=self.el_r()
        tg=self.sp['tgt']
        def ok(v,r):
            if v is None: return False
            lo,hi=r
            return (lo is None or v>=lo) and (hi is None or v<=hi)
        res={'sigma':sig,'C':C,'L':L,'alpha':alp,'el':el,
             'pass_sigma':ok(sig,tg['sigma']),'pass_C':ok(C,tg['C']),
             'pass_L':ok(L,tg['L']),'pass_alpha':ok(alp,tg['alpha']),
             'pass_el':ok(el,tg['el']),'elapsed':round(time.time()-t0,1),'logs':logs}
        res['score']=sum(bool(res[k]) for k in ['pass_sigma','pass_C','pass_L','pass_alpha','pass_el'])
        print(f'\n--- {self.name} ({res["elapsed"]:.1f}s) ---')
        for m,v,r_,ok_ in [('sigma',sig,tg['sigma'],res['pass_sigma']),
                            ('C',C,tg['C'],res['pass_C']),
                            ('L',L,tg['L'],res['pass_L']),
                            ('alpha',alp,tg['alpha'],res['pass_alpha']),
                            ('EL',el,tg['el'],res['pass_el'])]:
            vs=f'{v:.3f}' if v is not None else 'N/A'
            print(f'  {"✅" if ok_ else "❌"} {m}={vs}  {r_}')
        print(f'  SCORE: {res["score"]}/5')
        return res

def main():
    all_r={}; t0=time.time()
    for name,sp in SPECIES.items():
        print(f'\n{"="*55}\n{name}  N={sp["N"]}\n{"="*55}',flush=True)
        all_r[name]=SDI_v5(name,sp).run()
    print(f'\n{"="*55}\nALL DONE {time.time()-t0:.1f}s\n{"="*55}')
    for n,r in all_r.items():
        print(f'  {n}: {r["score"]}/5  σ={r["sigma"]:.2f} C={r["C"]:.3f} '
              f'L={r["L"]:.2f} α={r["alpha"]} EL={r["el"]:.1%}')

    # 保存（转换 bool 为 int 避免 JSON 问题）
    def fix(o):
        if isinstance(o,bool): return int(o)
        if isinstance(o,dict): return {k:fix(v) for k,v in o.items()}
        if isinstance(o,list): return [fix(v) for v in o]
        return o
    with open(f'{OUT}/exp1_v5_results.json','w') as f:
        json.dump(fix({n:{k:v for k,v in r.items()} for n,r in all_r.items()}),f,indent=2)

    # 汇总收敛图
    fig,axes=plt.subplots(5,5,figsize=(22,18))
    mkeys=[('sigma','sigma','b'),('C','C','g'),('L','L','orange'),
           ('alpha','alpha','r'),('el','EL','purple')]
    for row,(name,r) in enumerate(all_r.items()):
        lg=r['logs']; bio=SPECIES[name]['bio']; tg=SPECIES[name]['tgt']
        for col,(mk,ml,cl) in enumerate(mkeys):
            ax=axes[row][col]
            vs=[(s,v) for s,v in zip(lg['step'],lg[mk]) if v is not None]
            if vs:
                xs,ys=zip(*vs)
                ax.plot(xs,ys,color=cl,lw=2,label=ml)
            lo,hi=tg[mk]
            if lo: ax.axhline(lo,color='g',ls='--',lw=1.2,alpha=.8,label='target_lo')
            if hi: ax.axhline(hi,color='r',ls='--',lw=1.2,alpha=.8,label='target_hi')
            bv=bio.get(mk)
            if bv: ax.axhline(bv,color='k',ls=':',lw=1.5,alpha=.7,label=f'bio={bv}')
            ok_=bool(r.get(f'pass_{mk}',False))
            ax.set_title(f'{name[:9]}\n{ml}',fontsize=7,
                         color='darkgreen' if ok_ else 'darkred',fontweight='bold' if ok_ else 'normal')
            ax.tick_params(labelsize=6); ax.grid(alpha=.3)

    plt.suptitle('SDI Experiment 1 v5\nCross-Species: Random Init (WS Ring Lattice) → SDI Rules → Bio Targets',
                 fontsize=11,fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{OUT}/exp1_v5_convergence.png',dpi=130,bbox_inches='tight')
    plt.close()
    print('Plot saved: exp1_v5_convergence.png')
    print('DONE')

if __name__=='__main__':
    main()
