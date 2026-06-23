# CST Phase Transition Scanner: N=1024
# ======================================
# Scans network parameters to identify critical phase transition
# thresholds where superlinear intelligence gain emerges.
# 
# Based on: CST simulation platform, 05_SDI技术路线仿真规划.md
# Key metrics: sigma, clustering, path length, structured efficiency

import math, random, json
from pathlib import Path
from collections import deque
from typing import List, Dict, Tuple

SEED = 42
random.seed(SEED)

def watts_strogatz(n, k, p):
    adj = [set() for _ in range(n)]
    rng = random.Random(SEED + int(p * 1000))
    for i in range(n):
        for j in range(1, k // 2 + 1):
            nb = (i + j) % n; adj[i].add(nb); adj[nb].add(i)
    for i in range(n):
        nbrs = sorted(adj[i])
        for j in range(1, k // 2 + 1):
            nb = (i + j) % n
            if nb in adj[i] and rng.random() < p:
                adj[i].discard(nb); adj[nb].discard(i)
                cands = [v for v in range(n) if v != i and v not in adj[i]]
                if cands: new = rng.choice(cands); adj[i].add(new); adj[new].add(i)
    return [sorted(list(s)) for s in adj]

def random_graph(n, k):
    rng = random.Random(SEED + 9999)
    p = k / max(n - 1, 1)
    adj = [set() for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < p: adj[i].add(j); adj[j].add(i)
    return [sorted(list(s)) for s in adj]

def clustering(adj):
    n = len(adj); total, cnt = 0.0, 0
    for i in range(n):
        nbrs = set(adj[i]); k = len(nbrs)
        if k < 2: continue
        tri = 0
        nlist = list(nbrs)
        for a in range(k):
            for b in range(a + 1, k):
                if nlist[b] in adj[nlist[a]]: tri += 1
        total += (2.0 * tri) / (k * (k - 1)); cnt += 1
    return total / max(cnt, 1)

def avg_path(adj):
    n = len(adj); total, reachable = 0, 0
    sample = min(n, 50)  # sample sources for speed at N=1024
    for src in range(0, n, max(1, n // sample)):
        dist = [-1] * n; q = deque([src]); dist[src] = 0
        while q:
            u = q.popleft()
            for v in adj[u]:
                if dist[v] == -1: dist[v] = dist[u] + 1; q.append(v)
        for v in range(n):
            if v != src and dist[v] > 0: total += dist[v]; reachable += 1
    return total / max(reachable, 1)

def global_eff(adj):
    n = len(adj); total, cnt = 0.0, 0
    sample = min(n, 30)
    for src in range(0, n, max(1, n // sample)):
        dist = [-1] * n; q = deque([src]); dist[src] = 0
        while q:
            u = q.popleft()
            for v in adj[u]:
                if dist[v] == -1: dist[v] = dist[u] + 1; q.append(v)
        for v in range(n):
            if v != src and dist[v] > 0: total += 1.0 / dist[v]; cnt += 1
    return total / max(cnt, 1)

def compute_sigma(adj, n, k):
    C = clustering(adj); L = avg_path(adj)
    adj_r = random_graph(n, k)
    Cr = clustering(adj_r); Lr = max(avg_path(adj_r), 0.001)
    if Cr == 0 or Lr == 0: return 0, C, L
    return (C / Cr) / (L / Lr), C, L

def scan(N=1024, K=16):
    """Scan p from 0.001 to 0.5 and track phase transition metrics."""
    print(f"CST Phase Transition Scan: N={N}, K={K}")
    print("=" * 70)
    print(f"{'p':>7} {'sigma':>8} {'C':>8} {'L':>7} {'E_glob':>8} {'S_eff':>8} {'d_sigma/dp':>10}")

    p_values = [0.001, 0.002, 0.003, 0.005, 0.008, 0.01, 0.015, 0.02, 0.03,
                0.04, 0.05, 0.06, 0.08, 0.10, 0.12, 0.15, 0.18, 0.20,
                0.22, 0.25, 0.28, 0.30, 0.35, 0.40, 0.45, 0.50]

    results = []
    prev_sigma = None
    phase_changes = []

    for p in p_values:
        adj = watts_strogatz(N, K, p)
        sigma, C, L = compute_sigma(adj, N, K)
        E = global_eff(adj)
        S_eff = C * E

        dsig_dp = ""
        if prev_sigma is not None and sigma > 0:
            dp = p - p_values[p_values.index(p) - 1]
            dsig = (sigma - prev_sigma) / dp
            dsig_dp = f"{dsig:.1f}"
            # Detect phase change: rapid sigma increase
            if dsig > 50:
                phase_changes.append((p, sigma, dsig))

        results.append({"p": p, "sigma": round(sigma, 2), "C": round(C, 4),
                       "L": round(L, 2), "E_glob": round(E, 4),
                       "S_eff": round(S_eff, 4)})
        print(f"{p:7.3f} {sigma:8.2f} {C:8.4f} {L:7.2f} {E:8.4f} {S_eff:8.4f} {dsig_dp:>10}")
        prev_sigma = sigma

    # ── Phase change analysis ──
    print(f"\nPhase Change Detection (d_sigma/dp > 50):")
    for p, sigma, dsig in phase_changes:
        print(f"  p={p:.3f}: sigma={sigma:.2f}, d_sigma/dp={dsig:.1f}")

    # ── Find sigma >= 4.0 threshold ──
    for r in results:
        if r["sigma"] >= 4.0:
            print(f"\nSigma >= 4.0 threshold: p={r['p']:.3f}, sigma={r['sigma']:.2f}, "
                  f"C={r['C']:.4f}, S_eff={r['S_eff']:.4f}")
            break

    # ── S_eff peak ──
    best = max(results, key=lambda r: r["S_eff"])
    print(f"S_eff peak: p={best['p']:.3f}, sigma={best['sigma']:.2f}, "
          f"S_eff={best['S_eff']:.4f}")

    # ── Compare to random baseline ──
    adj_r = random_graph(N, K)
    Cr = clustering(adj_r); Er = global_eff(adj_r)
    SE_r = Cr * Er
    print(f"\nRandom baseline: C_rand={Cr:.4f}, E_rand={Er:.4f}, S_eff_rand={SE_r:.4f}")
    for r in results[::5]:  # every 5th
        ratio = r["S_eff"] / SE_r if SE_r > 0 else 0
        print(f"  p={r['p']:.3f}: S_eff/S_eff_rand = {ratio:.2f}")

    return results

if __name__ == "__main__":
    results = scan(1024, 16)
    out = Path(r"C:\Users\LEO\Documents\Codex\2026-05-29\goal-inest")
    with open(out / "cst_phase_scan_N1024.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved to {out / 'cst_phase_scan_N1024.json'}")
