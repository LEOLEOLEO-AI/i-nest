"""
SDI 实验七 v2 — 修复参数版
修复：
  1. C.elegans connectome路径修复
  2. Rule4：初始k=12（高密度），min_e=1，P_PRUNE=0.08，更激进
  3. Rule2b：增大跨社区偏差 CROSS_COMM_BIAS=5.0
  4. N_STEPS=12000（更长演化）
对照设计：
  A: 四规则完整（Rule2b+Rule4）
  B: 关闭Rule4（验证Q差异）
  C: 旧Rule2（随机）对照
  D: C.elegans真实connectome
"""
import numpy as np, json, os, time, sys
import networkx as nx
from collections import defaultdict

BASE = '/vault/sdi_sim'
OUT  = os.path.join(BASE, 'exp7_v2_results.json')
CE_DATA = os.path.join(BASE, 'celegans_sim/connectome_v8_data.json')

# ── 参数 ─────────────────────────────────────────────────
N_STEPS   = 12000
LOG_INT   = 600
SEEDS     = [42, 7, 13]

# Rule1
THETA_LTP = 65; THETA_LTD = 15
ETA_LTP   = 0.012; ETA_LTD = 0.008

# Rule2b
REWIRE_INT        = 50
P_REWIRE          = 0.15
CROSS_COMM_BIAS   = 5.0   # ↑ 增强跨社区偏好

# Rule3
SCALING_INT   = 100
ACT_LO = 0.05; ACT_HI = 0.20

# Rule4（关键修复）
PRUNE_INT   = 100    # ↓ 更频繁
P_PRUNE     = 0.08   # ↑ 更激进
MIN_EDGES   = 1      # ↓ 最低保护
ACT_THR     = 0.03   # 活跃度阈值

# 网络：初始k=12（高密度，给Rule4空间修剪）
NETWORKS = {
    'WS_4rules':   {'N':300,'k':12,'p':0.1,'rule4':True, 'rule2b':True},
    'WS_no_rule4': {'N':300,'k':12,'p':0.1,'rule4':False,'rule2b':True},
    'WS_old_rule2':{'N':300,'k':12,'p':0.1,'rule4':True, 'rule2b':False},
    'CE_4rules':   {'N':279,'connectome':True,'rule4':True,'rule2b':True},
}

# ── 初始化 ───────────────────────────────────────────────

def make_ws(N, k, p, rng):
    W = np.zeros((N,N), dtype=np.float32)
    for i in range(N):
        for d in range(1, k//2+1):
            j=(i+d)%N; w=rng.uniform(0.05,0.30)
            W[i,j]=W[j,i]=w
    for i in range(N):
        for d in range(1, k//2+1):
            if rng.random()<p:
                j=(i+d)%N; nj=rng.randint(0,N)
                if nj!=i and W[i,nj]==0:
                    W[i,nj]=W[i,j]; W[i,j]=0
    np.fill_diagonal(W,0); return W

def load_ce(rng):
    with open(CE_DATA) as f: d=json.load(f)
    N=d.get('N',279)
    W=np.zeros((N,N),dtype=np.float32)
    EL=np.zeros((N,N),dtype=bool)
    for row in d.get('chemical',[]):
        s,t,w = int(row[0]),int(row[1]),float(row[2])
        if s<N and t<N: W[s,t]=min(w/20.0,0.5)
    for row in d.get('electrical',[]):
        s,t = int(row[0]),int(row[1])
        if s<N and t<N:
            W[s,t]=W[t,s]=0.3; EL[s,t]=EL[t,s]=True
    return W,EL,N

# ── 指标 ─────────────────────────────────────────────────

def sigma(W,rng,ns=15):
    A=(W>0).astype(float); N=W.shape[0]; k=A.sum(1); km=k.mean()
    if km<2: return 1.0
    C=(A@A).diagonal()/(np.maximum(k*(k-1),1)); Cm=C.mean(); Cr=km/N
    nodes=rng.choice(N,min(ns,N),replace=False); Lv=[]
    for s in nodes:
        dist={s:0}; q=[s]
        while q:
            v=q.pop(0)
            for u in np.where(A[v]>0)[0]:
                if u not in dist: dist[u]=dist[v]+1; q.append(u)
        if len(dist)>1: Lv.append(np.mean(list(dist.values())))
    L=np.mean(Lv) if Lv else 1.0; Lr=np.log(N)/np.log(max(km,2))
    return float(np.clip((Cm/max(Cr,1e-6))/(L/max(Lr,1e-6)),0,20))

def Q_mod(W):
    try:
        G=nx.from_numpy_array(W)
        comms=list(nx.community.greedy_modularity_communities(G))
        return float(np.clip(nx.community.modularity(G,comms),0,1)),comms
    except: return 0.0,[]

def comm_labels(comms,N):
    L=np.zeros(N,dtype=int)
    for ci,c in enumerate(comms):
        for n in c:
            if n<N: L[n]=ci
    return L

def activate(W,rng,n=3):
    N=W.shape[0]; h=np.zeros(N,dtype=np.float32)
    h[rng.choice(N,n,replace=False)]=1.0
    for _ in range(4):
        h=np.tanh(W@h)
        if h.mean()>0.20:
            thr=np.percentile(h[h>0],70) if (h>0).any() else 0.5
            h[h<thr]=0
        h[h<0.05]=0
    return h.astype(np.float32)

# ── 规则 ─────────────────────────────────────────────────

def r1(W,EL,ltp,ltd,act,rng):
    a=(act>0.3).astype(np.int8); ia=(act<0.1).astype(np.int8)
    lev=np.outer(a,a).astype(np.int16); lev&=(W>0); np.fill_diagonal(lev,0)
    lde=np.outer(ia,a).astype(np.int16); lde&=(W>0)
    ltp+=lev; ltd+=lde
    nel=(ltp>=THETA_LTP)&~EL&(W>0); EL|=nel; W[nel]=np.minimum(W[nel]*2,1.0)
    pm=(ltd>=THETA_LTD)&~EL&(W>0); pm&=((W>0).sum(1)>MIN_EDGES)[:,None]
    if pm.any(): W[pm]=0; ltp[pm]=0; ltd[pm]=0
    np.fill_diagonal(W,0); return W,EL,ltp,ltd

def r2b(W,EL,ema,clbls,rng,directed=True):
    N=W.shape[0]; cands=np.argwhere((W>0)&~EL)
    if len(cands)==0: return W
    n=max(1,int(len(cands)*P_REWIRE*0.01))
    idx=rng.choice(len(cands),n,replace=False)
    for i,j in cands[idx]:
        if not directed:
            nj=rng.randint(0,N)
            if nj!=i and W[i,nj]==0: W[i,nj]=W[i,j]; W[i,j]=0
        else:
            wts=ema.copy()+0.01
            if clbls is not None:
                cross=(clbls!=clbls[i]).astype(float)
                wts*=(1+cross*(CROSS_COMM_BIAS-1))
            wts[i]=0; wts[W[i]>0]=0
            if wts.sum()<1e-8: continue
            wts/=wts.sum(); nj=rng.choice(N,p=wts)
            if W[i,nj]==0: W[i,nj]=W[i,j]; W[i,j]=0
    np.fill_diagonal(W,0); return W

def r3(W,ema):
    up=ema<ACT_LO; dn=ema>ACT_HI
    if up.any(): W[up,:]=np.minimum(W[up,:]*1.04,1.0)
    if dn.any(): W[dn,:]*=0.96
    np.fill_diagonal(W,0); return W

def r4(W,EL,ema,rng):
    N=W.shape[0]; deg=(W>0).sum(1)
    for i in np.where(deg>MIN_EDGES)[0]:
        edges=np.where((W[i]>0)&~EL[i])[0]
        for j in edges:
            if ema[j]<ACT_THR and rng.random()<P_PRUNE and deg[i]>MIN_EDGES:
                W[i,j]=0; deg[i]-=1
    return W

# ── 主仿真 ────────────────────────────────────────────────

def run(name,cfg,seed):
    rng=np.random.RandomState(seed)
    if cfg.get('connectome'):
        W,EL,N=load_ce(rng)
    else:
        N=cfg['N']; W=make_ws(N,cfg['k'],cfg['p'],rng)
        EL=np.zeros((N,N),dtype=bool)

    ltp=np.zeros((N,N),dtype=np.int16); ltd=ltp.copy()
    ema=np.zeros(N,dtype=np.float32); clbls=None
    log={'step':[],'sigma':[],'Q':[],'EL_ratio':[]}
    t0=time.time()

    for step in range(N_STEPS):
        act=activate(W,rng)
        ema=0.97*ema+0.03*act
        W,EL,ltp,ltd=r1(W,EL,ltp,ltd,act,rng)
        if step%REWIRE_INT==0:
            W=r2b(W,EL,ema,clbls,rng,directed=cfg.get('rule2b',True))
        if step%SCALING_INT==0: W=r3(W,ema)
        if cfg.get('rule4',True) and step%PRUNE_INT==0:
            W=r4(W,EL,ema,rng)
        if step%LOG_INT==0:
            s=sigma(W,rng); q,comms=Q_mod(W)
            if comms: clbls=comm_labels(comms,N)
            elr=EL.sum()/max((W>0).sum(),1)
            log['step'].append(step); log['sigma'].append(s)
            log['Q'].append(q); log['EL_ratio'].append(float(elr))
            edges=(W>0).sum()
            print(f"  {name} s={seed} t={step:5d}: σ={s:.2f} Q={q:.3f} "
                  f"EL={elr*100:.1f}% edges={edges} ({time.time()-t0:.0f}s)")

    fs=sigma(W,rng); fq,fc=Q_mod(W); felr=EL.sum()/max((W>0).sum(),1)
    return {'net':name,'seed':seed,'rule4':cfg.get('rule4',True),
            'rule2b':cfg.get('rule2b',True),
            'final':{'sigma':fs,'Q':fq,'EL_ratio':float(felr),
                     'edges':int((W>0).sum())},
            'log':log}

# ── 主程序 ────────────────────────────────────────────────

if __name__=='__main__':
    print("="*60)
    print("SDI 实验七 v2 — 参数修复版（k=12, min_e=1, P_PRUNE=0.08）")
    print("="*60)
    results=[]
    for name,cfg in NETWORKS.items():
        for seed in SEEDS:
            print(f"\n>>> {name} seed={seed}")
            results.append(run(name,cfg,seed))

    print("\n"+"="*60+"  汇总:")
    by=defaultdict(list)
    for r in results: by[r['net']].append(r)
    summary={}
    for net,rl in by.items():
        qs=[r['final']['Q'] for r in rl]; ss=[r['final']['sigma'] for r in rl]
        summary[net]={'Q_mean':float(np.mean(qs)),'Q_std':float(np.std(qs)),
                      'sigma_mean':float(np.mean(ss))}
        print(f"  {net}: Q={np.mean(qs):.3f}±{np.std(qs):.3f} σ={np.mean(ss):.2f}")
    q4=summary.get('WS_4rules',{}).get('Q_mean',0)
    q0=summary.get('WS_no_rule4',{}).get('Q_mean',0)
    print(f"\n★ Rule4效果: 四规则Q={q4:.3f}  无Rule4Q={q0:.3f}  差异={q4-q0:+.3f}x")
    json.dump({'results':results,'summary':summary},
              open(OUT,'w'),indent=2)
    print(f"✅ {OUT}")
