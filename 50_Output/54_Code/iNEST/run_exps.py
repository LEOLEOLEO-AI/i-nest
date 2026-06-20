# Experiments 2-4 runner
import sys, os, json, math, random
from pathlib import Path
from collections import deque

sys.path.insert(0, r"D:\iNEST\Write\Code\SDI")
from sdi_sim.topology import *

SEED = 42
random.seed(SEED)

def _random_adj(n, k, seed):
    rng = random.Random(seed)
    p = k / (n - 1) if n > 1 else 0
    adj = [set() for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < p:
                adj[i].add(j); adj[j].add(i)
    return [sorted(list(s)) for s in adj]

def _bfs_path(adj, src, dst):
    n = len(adj); visited = [-1]*n; q = deque([src]); visited[src] = src
    while q:
        u = q.popleft()
        if u == dst: break
        for v in adj[u]:
            if visited[v] == -1: visited[v] = u; q.append(v)
    if visited[dst] == -1: return None
    path = []; cur = dst
    while cur != src: path.append(cur); cur = visited[cur]
    path.append(src); path.reverse(); return path

def _throughput(adj, n_tasks):
    N = len(adj); nodes = list(range(N)); random.shuffle(nodes)
    pairs = []; used = set()
    for _ in range(n_tasks):
        for _ in range(10):
            s = random.choice(nodes); d = random.choice([n for n in nodes if n != s])
            if (s,d) not in used: used.add((s,d)); pairs.append((s,d)); break
    if not pairs: return 0.0
    active = []
    for s,d in pairs:
        p = _bfs_path(adj, s, d)
        if p: active.append(set(p))
    if not active: return 0.0
    eu = {}
    for ps in active:
        pl = list(ps)
        for i in range(len(pl)-1):
            e = tuple(sorted([pl[i], pl[i+1]]))
            eu[e] = eu.get(e, 0) + 1
    return sum(1 for v in eu.values() if v <= max(1,n_tasks//3)) / max(1,len(eu))

def _rm_edges(adj, frac):
    new_adj = [set(nbrs) for nbrs in adj]; n = len(adj)
    edges = [(i,j) for i in range(n) for j in new_adj[i] if i < j]
    random.shuffle(edges)
    for i,j in edges[:max(1,int(len(edges)*frac))]:
        new_adj[i].discard(j); new_adj[j].discard(i)
    return [sorted(list(s)) for s in new_adj]

def _rm_hubs(adj, frac):
    n = len(adj); degs = [(len(adj[i]),i) for i in range(n)]; degs.sort(reverse=True)
    rm = set(d[1] for d in degs[:max(1,int(n*frac))])
    result = [set() for _ in range(n)]
    for i in range(n):
        if i not in rm:
            for j in adj[i]:
                if j not in rm: result[i].add(j)
    return [sorted(list(s)) for s in result]

N, K = 128, 16
print("EXP 2: Parallel Task Throughput")
for name, gen in [("Random", lambda: _random_adj(N,K,SEED)), ("WS-0.05", lambda: watts_strogatz(N,K,0.05,SEED)), ("WS-0.10", lambda: watts_strogatz(N,K,0.10,SEED)), ("Clusters", lambda: functional_clusters(N,8,0.9,0.02,SEED))]:
    adj = gen(); C = clustering_coefficient(adj); L = avg_shortest_path(adj)
    sigma = small_world_sigma(adj, N, K); se = C / max(L, 0.001)
    tps = [_throughput(adj, t) for t in [1,2,4,8]]
    print(f"{name:>10}: C={C:.4f} L={L:.2f} sigma={sigma:.2f} SE={se:.4f}  tp={[round(t,3) for t in tps]}")

print("\nEXP 3: Fault Tolerance")
for name, gen in [("Random", lambda: _random_adj(N,K,SEED)), ("WS-0.05", lambda: watts_strogatz(N,K,0.05,SEED)), ("WS-0.10", lambda: watts_strogatz(N,K,0.10,SEED))]:
    adj = gen(); e0 = global_efficiency(adj)
    er = [round(global_efficiency(_rm_edges(adj,f))/e0,3) for f in [0.05,0.10,0.20,0.30]]
    eh = [round(global_efficiency(_rm_hubs(adj,f))/e0,3) for f in [0.02,0.05,0.10,0.15]]
    print(f"{name:>10}: E0={e0:.4f}  rand={er}  hubs={eh}")

print("\nEXP 4: Scale Threshold")
print(f"{'N':>6} {'p':>6} {'sigma':>7} {'C':>7} {'L':>6} {'SE':>7} {'vs_rand':>8}")
for N in [16,32,48,64,96,128,192,256,384,512,768,1024]:
    best_se, best = 0, None
    for p in [0.01,0.02,0.03,0.05,0.08,0.10,0.12,0.15,0.18,0.20,0.25]:
        adj = watts_strogatz(N, K, p, SEED)
        C = clustering_coefficient(adj); E = global_efficiency(adj); se = C * E
        if se > best_se:
            best_se = se; sigma = small_world_sigma(adj, N, K)
            se_r = clustering_coefficient(_random_adj(N,K,SEED+100)) * global_efficiency(_random_adj(N,K,SEED+100))
            best = (N, p, sigma, C, avg_shortest_path(adj), se, se_r)
    if best:
        Nv,pv,sv,Cv,Lv,sev,ser = best
        ratio = sev/ser if ser>0 else 0
        m = " ***" if ratio>1.5 else ""
        print(f"{Nv:>6} {pv:>6.3f} {sv:>7.2f} {Cv:>7.4f} {Lv:>6.2f} {sev:>7.4f} {ratio:>8.2f}{m}")
print("\nDone.")
