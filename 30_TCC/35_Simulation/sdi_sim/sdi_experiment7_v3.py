"""
SDI 实验七 v3 — CE专属修复版
修复：
  1. CE权重归一化：max_w → 0.4，保证信号可传播
  2. 动态ACT_THR：低于全网中位活跃度×0.3才修剪（非固定值）
  3. min_edges按物种平均度自适应：max(2, avg_degree*0.3)
  4. BTW驱动激活：多点随机种子，确保稀疏网络能激活
  5. 社区标签每500步刷新（Rule2b定向性更及时）
  6. 对照组：WS_ER（低初始Q，Rule4效果更显著）

目标：
  CE: Q>0.3, σ>2.5，复现实验六水平
  WS_ER: 四规则Q vs 无Rule4Q 差异>0.4（类似实验四）
"""
import numpy as np, json, os, time
import networkx as nx
from collections import defaultdict

BASE = '/vault/sdi_sim'
OUT  = os.path.join(BASE, 'exp7_v3_results.json')
CE_DATA = os.path.join(BASE, 'celegans_sim/connectome_v8_data.json')

# ── 参数 ─────────────────────────────────────────────────
N_STEPS   = 10000
LOG_INT   = 500
SEEDS     = [42, 7, 13]

# Rule1 STDP
THETA_LTP = 40;   THETA_LTD = 20   # 无每步衰减；慢衰减每20步执行一次
DECAY_INT = 20    # ltp慢衰减间隔（步数）

# Rule2b
REWIRE_INT      = 50
P_REWIRE        = 0.12   # ↓ 略降，减少重连破坏EL键
CROSS_COMM_BIAS = 5.0
COMM_REFRESH    = 500   # 每500步刷新社区标签

# Rule3
SCALING_INT = 100
ACT_LO = 0.05; ACT_HI = 0.20

# Rule4
PRUNE_INT = 150
P_PRUNE   = 0.08
# min_edges和ACT_THR改为自适应（见run()里计算）

# 网络配置
NETWORKS = {
    # WS高密度（验证Rule4轨迹）
    'WS_4rules':   {'type':'ws','N':300,'k':12,'p':0.1,'rule4':True, 'rule2b':True},
    'WS_no_rule4': {'type':'ws','N':300,'k':12,'p':0.1,'rule4':False,'rule2b':True},
    # ER随机图（低初始Q，Rule4效果最大化，类实验四）
    'ER_4rules':   {'type':'er','N':300,'p_er':0.04,'rule4':True, 'rule2b':True},
    'ER_no_rule4': {'type':'er','N':300,'p_er':0.04,'rule4':False,'rule2b':True},
    # C.elegans真实connectome（核心修复目标）
    'CE_4rules':   {'type':'ce','rule4':True, 'rule2b':True},
    'CE_no_rule4': {'type':'ce','rule4':False,'rule2b':True},
}

# ── 网络初始化 ────────────────────────────────────────────

def make_ws(N, k, p, rng):
    W = np.zeros((N,N), dtype=np.float32)
    for i in range(N):
        for d in range(1, k//2+1):
            j=(i+d)%N; W[i,j]=W[j,i]=rng.uniform(0.1, 0.35)
    for i in range(N):
        for d in range(1, k//2+1):
            if rng.random()<p:
                j=(i+d)%N; nj=rng.randint(0,N)
                if nj!=i and W[i,nj]==0:
                    W[i,nj]=W[i,j]; W[i,j]=0
    np.fill_diagonal(W,0); return W

def make_er(N, p, rng):
    """ER随机图——低初始Q，给Rule4最大发挥空间"""
    W = np.zeros((N,N), dtype=np.float32)
    for i in range(N):
        for j in range(i+1,N):
            if rng.random()<p:
                w=rng.uniform(0.1,0.35)
                W[i,j]=W[j,i]=w
    np.fill_diagonal(W,0); return W

def load_ce(rng):
    """修复版CE加载：字段名edges_chem/edges_elec，权重归一化到[0.1,0.4]"""
    with open(CE_DATA) as f: d=json.load(f)
    N=d.get('N',279)
    W=np.zeros((N,N),dtype=np.float32)
    EL=np.zeros((N,N),dtype=bool)

    # 化学突触 — 字段名 edges_chem，格式 [src, dst, weight]
    chem = [(int(r[0]),int(r[1]),float(r[2])) for r in d.get('edges_chem',[])]
    if chem:
        max_w = max(w for _,_,w in chem)
        for s,t,w in chem:
            if s<N and t<N:
                W[s,t] = 0.1 + 0.3*(w/max_w)   # 归一化到 [0.1, 0.4]

    # 电突触 — 字段名 edges_elec，双向，标记EL
    for row in d.get('edges_elec',[]):
        s,t=int(row[0]),int(row[1])
        if s<N and t<N:
            W[s,t]=W[t,s]=0.25
            EL[s,t]=EL[t,s]=True

    avg_deg=(W>0).sum(1).mean()
    print(f"  CE loaded: N={N}, chem={len(chem)}, "
          f"elec={len(d.get('edges_elec',[]))}, avg_deg={avg_deg:.1f}, "
          f"w=[{W[W>0].min():.3f},{W[W>0].max():.3f}]")
    return W, EL, N

# ── 指标计算 ─────────────────────────────────────────────

def compute_sigma(W, rng, ns=15):
    A=(W>0).astype(float); N=W.shape[0]; k=A.sum(1); km=k.mean()
    if km<1.5: return 1.0
    C=(A@A).diagonal()/(np.maximum(k*(k-1),1)); Cm=C.mean(); Cr=max(km/N,1e-6)
    nodes=rng.choice(N,min(ns,N),replace=False); Lv=[]
    for s in nodes:
        dist={s:0}; q=[s]
        while q:
            v=q.pop(0)
            for u in np.where(A[v]>0)[0]:
                if u not in dist: dist[u]=dist[v]+1; q.append(u)
        if len(dist)>1: Lv.append(np.mean(list(dist.values())))
    L=np.mean(Lv) if Lv else 1.0; Lr=np.log(N)/np.log(max(km,2))
    return float(np.clip((Cm/Cr)/(L/max(Lr,1e-6)),0,20))

def compute_Q(W):
    try:
        G=nx.from_numpy_array(W)
        if G.number_of_edges()==0: return 0.0,[]
        comms=list(nx.community.greedy_modularity_communities(G))
        return float(np.clip(nx.community.modularity(G,comms),0,1)),comms
    except: return 0.0,[]

def comm_labels(comms, N):
    L=np.zeros(N,dtype=int)
    for ci,c in enumerate(comms):
        for n in c:
            if n<N: L[n]=ci
    return L

# ── BTW驱动激活（适配稀疏网络）────────────────────────────

def activate_btw(W, rng, n_seeds=5, n_steps=5):
    """
    BTW驱动：适量种子 + 多步传播
    种子数控制在N//20以内，避免过度激活导致EL=100%
    """
    N=W.shape[0]; h=np.zeros(N,dtype=np.float32)
    # 激活约12%节点，产生足够co-activation供STDP积累
    frac = 0.12
    n_seeds = max(5, int(W.shape[0] * frac))
    seeds = rng.choice(W.shape[0], n_seeds, replace=False)
    h[seeds] = rng.uniform(0.5, 1.0, n_seeds)
    for _ in range(n_steps):
        h = np.tanh(W @ h)
        if h.max() > 0:
            thr = np.percentile(h[h>0.05], 70) if (h>0.05).sum()>5 else 0.05
            h[h<thr] = 0
    return h.astype(np.float32)

# ── 四条规则 ─────────────────────────────────────────────

def rule1_stdp(W, EL, ltp, ltd, act, rng):
    a=(act>0.30).astype(np.int8); ia=(act<0.08).astype(np.int8)  # ↑激活阈值提高
    lev=np.outer(a,a).astype(np.int16); lev&=(W>0); np.fill_diagonal(lev,0)
    lde=np.outer(ia,a).astype(np.int16); lde&=(W>0)
    ltp+=lev; ltd+=lde
    # E-L固化
    nel=(ltp>=THETA_LTP)&~EL&(W>0)
    EL|=nel; W[nel]=np.minimum(W[nel]*1.5, 1.0)
    # E-S消除：弱连接且LTD积累
    pm=(ltd>=THETA_LTD)&~EL&(W>0)
    if pm.any(): W[pm]=0; ltp[pm]=0; ltd[pm]=0
    np.fill_diagonal(W,0)
    return W, EL, ltp, ltd

def rule2b(W, EL, ema, clbls, rng, directed, min_edges):
    N=W.shape[0]; cands=np.argwhere((W>0)&~EL)
    if len(cands)==0: return W
    n=max(1,int(len(cands)*P_REWIRE*0.01))
    for i,j in cands[rng.choice(len(cands),n,replace=False)]:
        if not directed:
            nj=rng.randint(0,N)
            if nj!=i and W[i,nj]==0: W[i,nj]=W[i,j]; W[i,j]=0
        else:
            wts=ema.copy()+0.01
            if clbls is not None:
                wts*=(1+(clbls!=clbls[i]).astype(float)*(CROSS_COMM_BIAS-1))
            wts[i]=0; wts[W[i]>0]=0
            if wts.sum()<1e-8: continue
            wts/=wts.sum(); nj=rng.choice(N,p=wts)
            if W[i,nj]==0: W[i,nj]=W[i,j]; W[i,j]=0
    np.fill_diagonal(W,0); return W

def rule3(W, ema):
    up=ema<ACT_LO; dn=ema>ACT_HI
    if up.any(): W[up,:]=np.minimum(W[up,:]*1.04,1.0)
    if dn.any(): W[dn,:]*=0.96
    np.fill_diagonal(W,0); return W

def rule4_adaptive(W, EL, ema, rng, min_edges, act_thr_rel=0.3):
    """
    自适应Rule4：
    - min_edges 按物种自适应
    - ACT_THR = 活跃度中位数 × act_thr_rel（相对阈值）
    """
    N=W.shape[0]; deg=(W>0).sum(1)
    act_med = np.median(ema[ema>0]) if (ema>0).any() else 0.01
    act_thr = act_med * act_thr_rel   # 动态阈值
    for i in np.where(deg>min_edges)[0]:
        edges=np.where((W[i]>0)&~EL[i])[0]
        for j in edges:
            if ema[j]<act_thr and rng.random()<P_PRUNE and deg[i]>min_edges:
                W[i,j]=0; deg[i]-=1
    return W

# ── 主仿真 ────────────────────────────────────────────────

def run(name, cfg, seed):
    rng = np.random.RandomState(seed)
    EL  = None

    if cfg['type']=='ce':
        W, EL, N = load_ce(rng)
    elif cfg['type']=='er':
        N=cfg['N']; W=make_er(N,cfg['p_er'],rng)
        EL=np.zeros((N,N),dtype=bool)
    else:
        N=cfg['N']; W=make_ws(N,cfg['k'],cfg['p'],rng)
        EL=np.zeros((N,N),dtype=bool)

    # 自适应参数
    avg_deg = (W>0).sum(1).mean()
    min_edges = max(2, int(avg_deg*0.3))
    print(f"  [{name}] N={N}, avg_deg={avg_deg:.1f}, min_edges={min_edges}")

    ltp=np.zeros((N,N),dtype=np.int16); ltd=ltp.copy()
    ema=np.zeros(N,dtype=np.float32); clbls=None
    log={'step':[],'sigma':[],'Q':[],'EL_ratio':[],'edges':[]}
    t0=time.time()

    for step in range(N_STEPS):
        # 激活（CE用BTW多点驱动）
        if cfg['type']=='ce':
            act = activate_btw(W, rng, n_seeds=8, n_steps=6)
        else:
            act = activate_btw(W, rng, n_seeds=4, n_steps=4)

        ema = 0.97*ema + 0.03*act

        # Rule1
        W, EL, ltp, ltd = rule1_stdp(W, EL, ltp, ltd, act, rng)
        # ltp慢衰减（每DECAY_INT步 -1，防无限累积）
        if step % DECAY_INT == 0:
            ltp = np.maximum(ltp - 1, 0)

        # Rule2b（社区标签定期刷新）
        if step % REWIRE_INT == 0:
            W = rule2b(W, EL, ema, clbls, rng,
                       directed=cfg.get('rule2b',True), min_edges=min_edges)

        # Rule3
        if step % SCALING_INT == 0:
            W = rule3(W, ema)

        # Rule4（自适应）
        if cfg.get('rule4',True) and step % PRUNE_INT == 0:
            W = rule4_adaptive(W, EL, ema, rng, min_edges)

        # 刷新社区标签（Rule2b定向性）
        if step % COMM_REFRESH == 0:
            _,comms = compute_Q(W)
            if comms: clbls = comm_labels(comms, N)

        # 记录
        if step % LOG_INT == 0:
            s = compute_sigma(W, rng)
            q,_ = compute_Q(W)
            elr = EL.sum()/max((W>0).sum(),1)
            edges = int((W>0).sum())
            log['step'].append(step)
            log['sigma'].append(s); log['Q'].append(q)
            log['EL_ratio'].append(float(elr)); log['edges'].append(edges)
            print(f"  {name} s={seed} t={step:5d}: σ={s:.2f} Q={q:.3f} "
                  f"EL={elr*100:.1f}% edges={edges} ({time.time()-t0:.0f}s)")

    fs=compute_sigma(W,rng); fq,_=compute_Q(W)
    felr=EL.sum()/max((W>0).sum(),1)
    return {
        'net':name,'seed':seed,
        'rule4':cfg.get('rule4',True),'rule2b':cfg.get('rule2b',True),
        'type':cfg['type'],
        'final':{'sigma':fs,'Q':fq,'EL_ratio':float(felr),'edges':int((W>0).sum())},
        'log':log,
    }

# ── 主程序 ────────────────────────────────────────────────

if __name__=='__main__':
    print("="*65)
    print("SDI 实验七 v3 — CE专属修复版")
    print("  ✦ 动态ACT_THR（相对中位数）")
    print("  ✦ CE权重归一化到[0.1,0.4]")
    print("  ✦ BTW多点驱动激活")
    print("  ✦ 社区标签500步刷新")
    print("  ✦ ER对照组（低初始Q，Rule4效果最大化）")
    print("="*65)

    results=[]
    for name,cfg in NETWORKS.items():
        for seed in SEEDS:
            print(f"\n>>> {name}  seed={seed}")
            results.append(run(name,cfg,seed))

    # 汇总
    print("\n"+"="*65)
    by=defaultdict(list)
    for r in results: by[r['net']].append(r)
    summary={}
    for net,rl in by.items():
        qs=[r['final']['Q'] for r in rl]
        ss=[r['final']['sigma'] for r in rl]
        es=[r['final']['EL_ratio'] for r in rl]
        summary[net]={
            'Q_mean':float(np.mean(qs)),'Q_std':float(np.std(qs)),
            'sigma_mean':float(np.mean(ss)),'EL_mean':float(np.mean(es)),
        }
        print(f"  {net}: Q={np.mean(qs):.3f}±{np.std(qs):.3f} "
              f"σ={np.mean(ss):.2f} EL={np.mean(es)*100:.1f}%")

    # 关键对比
    print("\n★ 关键对比（Rule4效果）:")
    for pair in [('WS_4rules','WS_no_rule4'),('ER_4rules','ER_no_rule4'),
                 ('CE_4rules','CE_no_rule4')]:
        q4=summary.get(pair[0],{}).get('Q_mean',0)
        q0=summary.get(pair[1],{}).get('Q_mean',0)
        ratio=q4/max(q0,0.001)
        print(f"  {pair[0][:10]} vs {pair[1][:10]}: "
              f"Q={q4:.3f} vs Q={q0:.3f}  比值={ratio:.2f}×")

    json.dump({'results':results,'summary':summary},
              open(OUT,'w'),indent=2)
    print(f"\n✅ 保存: {OUT}")
