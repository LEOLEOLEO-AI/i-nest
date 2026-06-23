#!/usr/bin/env python3
"""V30: Scale Emergence Threshold Scan.
N=16 -> 1024 chiplet scale scan.
Identify minimum N where small-world + power-law emergence appears.
Uses SDI generator (WS model) validated in V29.
"""
import numpy as np, json, os, warnings, time
warnings.filterwarnings("ignore")
import networkx as nx
from scipy import stats
from collections import Counter

np.random.seed(42)
os.chdir(r"D:\Obsidian\home\work\.openclaw\workspace\simulation")
OUT_DIR = "data/v30_results"
os.makedirs(OUT_DIR, exist_ok=True)

print("=" * 60)
print("V30: Scale Emergence Threshold Scan (N=16 -> 1024)")
print("=" * 60)

SCALES = [16, 32, 64, 128, 256, 512, 1024]
K_PER_SCALE = {16:4, 32:8, 64:10, 128:14, 256:20, 512:28, 1024:40}

results = []

for N in SCALES:
    k = K_PER_SCALE[N]
    print(f"\n[N={N}, k={k}] ", end="", flush=True)
    t0 = time.time()
    
    # Scan beta for small-world emergence
    best_sigma = 0
    best_params = None
    emergence_detected = False
    phase = "random"  # "random" | "small_world" | "scale_free_like"
    
    beta_scan = []
    for beta in np.linspace(0.01, 0.5, 30):
        G = nx.watts_strogatz_graph(N, k, beta)
        if not nx.is_connected(G):
            continue
        
        C = nx.average_clustering(G)
        L = nx.average_shortest_path_length(G)
        
        # ER baseline
        G_er = nx.erdos_renyi_graph(N, k/(N-1), seed=42)
        for _ in range(100):
            if nx.is_connected(G_er): break
            G_er = nx.erdos_renyi_graph(N, k/(N-1), seed=np.random.randint(99999))
        C_er = nx.average_clustering(G_er)
        L_er = nx.average_shortest_path_length(G_er)
        sigma = (C/C_er)/(L_er) if C_er > 0 else 1.0
        
        beta_scan.append((beta, sigma, C, L))
        
        if sigma > best_sigma:
            best_sigma = sigma
            best_params = {"beta": beta, "sigma": sigma, "C": C, "L": L, "k": k}
    
    # Classify phase
    if best_sigma < 1.5:
        phase = "random"
    elif best_sigma < 4.0:
        phase = "transition"
        emergence_detected = True
    else:
        phase = "small_world"
        emergence_detected = True
    
    # Degree distribution
    if best_params:
        G_best = nx.watts_strogatz_graph(N, k, best_params["beta"])
        while not nx.is_connected(G_best):
            G_best = nx.watts_strogatz_graph(N, k, best_params["beta"])
        
        degrees = [d for _, d in G_best.degree()]
        deg_counts = Counter(degrees)
        dx = np.array(sorted(deg_counts.keys()))
        dy = np.array([deg_counts[d] for d in dx])
        dmask = (dx >= 3) & (dy > 0)
        if dmask.sum() >= 5:
            lx = np.log10(dx[dmask].astype(float))
            ly = np.log10(dy[dmask].astype(float))
            slope, _, r2, _, _ = stats.linregress(lx, ly)
            gamma_deg = -slope
        else:
            gamma_deg, r2 = 0, 0
        
        # Efficiency
        eff = nx.global_efficiency(G_best)
        mod = nx.algorithms.community.modularity(G_best, 
              nx.algorithms.community.greedy_modularity_communities(G_best))
    else:
        gamma_deg, r2, eff, mod = 0, 0, 0, 0
    
    elapsed = time.time() - t0
    r = {
        "N": N, "k": k,
        "best_beta": round(best_params["beta"], 4) if best_params else 0,
        "sigma_max": round(best_sigma, 3),
        "C": round(best_params["C"], 4) if best_params else 0,
        "L": round(best_params["L"], 4) if best_params else 0,
        "gamma_degree": round(gamma_deg, 3),
        "gamma_R2": round(r2, 3),
        "efficiency": round(eff, 4),
        "modularity": round(mod, 4),
        "phase": phase,
        "emergence": emergence_detected,
        "time_s": round(elapsed, 1),
    }
    results.append(r)
    print(f"sigma={best_sigma:.2f} phase={phase} ({elapsed:.1f}s)")

# Emergence threshold analysis
print("\n" + "=" * 60)
print("EMERGENCE PHASE DIAGRAM")
print("=" * 60)
print(f"{'N':>6s} {'k':>4s} {'sigma':>8s} {'C':>8s} {'L':>8s} {'phase':<15s} {'emerged':>8s}")
print("-" * 60)
for r in results:
    print(f"{r['N']:>6d} {r['k']:>4d} {r['sigma_max']:>8.3f} {r['C']:>8.4f} {r['L']:>8.4f} {r['phase']:<15s} {str(r['emergence']):>8s}")

# Find emergence threshold
threshold_N = None
for r in results:
    if r["emergence"]:
        threshold_N = r["N"]
        break

# Scale law: sigma ~ N^beta
Ns = np.array([r["N"] for r in results])
sigmas = np.array([r["sigma_max"] for r in results])
lx = np.log10(Ns)
ly = np.log10(sigmas)
slope, intercept, r2, p, _ = stats.linregress(lx, ly)

print(f"\n  Emergence threshold: N >= {threshold_N}")
print(f"  sigma ~ N^{slope:.3f} (R2={r2:.3f}, p={p:.4f})")
print(f"  At N=1024: sigma_pred = {10**(slope*np.log10(1024)+intercept):.1f}")

# Compile
v30_results = {
    "version": "V30",
    "title": "Scale Emergence Threshold Scan",
    "date": "2026-06-19",
    "scales": results,
    "emergence_threshold_N": threshold_N,
    "scaling_law": {
        "sigma_vs_N_slope": round(slope, 3),
        "sigma_vs_N_intercept": round(intercept, 3),
        "R2": round(r2, 3),
        "p_value": round(float(p), 6),
    },
    "conclusion": (
        f"Small-world emergence at N={threshold_N}. "
        f"sigma ~ N^{slope:.3f} (R2={r2:.3f}). "
        f"Minimum viable chiplet array: N>={threshold_N}."
    )
}

with open(os.path.join(OUT_DIR, "v30_results.json"), "w") as f:
    json.dump(v30_results, f, indent=2)

print(f"\nV30 COMPLETE. Saved: {os.path.join(OUT_DIR, 'v30_results.json')}")
