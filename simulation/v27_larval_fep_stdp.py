#!/usr/bin/env python3
"""V27: Drosophila Larval Connectome FEP-STDP Simulation. All real data."""
import numpy as np
import json, os, warnings, time
warnings.filterwarnings("ignore")
import networkx as nx
from scipy import stats
from collections import Counter, defaultdict
np.random.seed(42)

DATA_FILE = "connectome_larval_cns.json"
OUT_DIR = "data/v27_results"
os.makedirs(OUT_DIR, exist_ok=True)

print("=" * 60)
print("V27: Drosophila Larval FEP-STDP on Real Connectome")
print("=" * 60)

t0 = time.time()
with open(DATA_FILE) as f:
    raw = json.load(f)

nodes_all = raw["nodes"]
edges_chem = raw["edges_chem"]
N_full = len(nodes_all)
E_chem = len(edges_chem)
print(f"\n[1] Loaded: N={N_full}, chemical edges={E_chem}")

Gu_full = nx.Graph()
Gu_full.add_nodes_from(range(N_full))
weighted_edges = [(int(e[0]), int(e[1]), float(e[2])) for e in edges_chem]
Gu_full.add_weighted_edges_from(weighted_edges)

gcc_nodes = max(nx.connected_components(Gu_full), key=len)
Gu_gcc = Gu_full.subgraph(gcc_nodes).copy()
N_gcc = len(gcc_nodes)
E_gcc = Gu_gcc.number_of_edges()
k_avg = 2 * E_gcc / N_gcc
print(f"    GCC: N={N_gcc}, E={E_gcc}, k_avg={k_avg:.2f}")

# Static topology metrics
print("\n[2] Static topology metrics...")
C_real = nx.average_clustering(Gu_gcc)
L_real = nx.average_shortest_path_length(Gu_gcc)
eff_real = nx.global_efficiency(Gu_gcc)

G_er = nx.erdos_renyi_graph(N_gcc, k_avg/(N_gcc-1), seed=42)
for _ in range(100):
    if nx.is_connected(G_er): break
    G_er = nx.erdos_renyi_graph(N_gcc, k_avg/(N_gcc-1), seed=np.random.randint(99999))
C_er = nx.average_clustering(G_er)
L_er = nx.average_shortest_path_length(G_er)
sigma = (C_real/C_er) / (L_real/L_er)
print(f"    sigma={sigma:.3f}  C={C_real:.4f}  L={L_real:.4f}  eff={eff_real:.4f}")

degrees = [d for _, d in Gu_gcc.degree()]
er_deg = [d for _, d in G_er.degree()]
ks_d = stats.ks_2samp(degrees, er_deg)
clust_r = list(nx.clustering(Gu_gcc).values())
clust_e = list(nx.clustering(G_er).values())
ks_c = stats.ks_2samp(clust_r, clust_e)
print(f"    KS deg p={ks_d.pvalue:.2e}  KS clust p={ks_c.pvalue:.2e}")

# Degree power-law
deg_counts = Counter(degrees)
dx = np.array(sorted(deg_counts.keys()))
dy = np.array([deg_counts[d] for d in dx])
mask = (dx >= 5) & (dy > 0)
if mask.sum() >= 5:
    lx = np.log10(dx[mask]); ly = np.log10(dy[mask].astype(float))
    slope, _, r2, pv, _ = stats.linregress(lx, ly)
    gamma_exp = -slope
    print(f"    gamma={gamma_exp:.3f} R2={r2:.3f}")
else:
    gamma_exp = 0

# Avalanche statistics on full GCC
print("\n[3] Avalanche statistics...")
def avalanches(G, trials=100, steps=50):
    nodes_list = list(G.nodes())
    sizes = []
    for _ in range(trials):
        active = {np.random.choice(nodes_list)}
        visited = set(active)
        cs = 1
        for _ in range(steps):
            new_active = set()
            for node in active:
                nbs = list(G.neighbors(node))
                if nbs:
                    k = min(len(nbs), np.random.poisson(2))
                    for nb in np.random.choice(nbs, size=max(1,k), replace=False):
                        if nb not in visited and np.random.random() < 0.3:
                            new_active.add(nb)
                            visited.add(nb)
            if not new_active: break
            active = new_active
            cs += len(new_active)
        sizes.append(cs)
    return np.array(sizes)

def fit_power_law(sizes):
    counts = Counter(sizes)
    sx = np.array(sorted(counts.keys()))
    sy = np.array([counts[k] for k in sx])
    mask = (sx >= 2) & (sy > 0)
    if mask.sum() >= 4:
        lx = np.log10(sx[mask].astype(float))
        ly = np.log10(sy[mask].astype(float))
        slope, _, r2, pv, _ = stats.linregress(lx, ly)
        return -slope, r2, pv
    return 0, 0, 1

avr = avalanches(Gu_gcc)
ave = avalanches(G_er)
ar, r2r, pr = fit_power_law(avr)
ae, r2e, pe = fit_power_law(ave)
print(f"    Real: mean={avr.mean():.1f}  max={avr.max()}  alpha={ar:.3f}  R2={r2r:.3f}")
print(f"    ER:   mean={ave.mean():.1f}  max={ave.max()}  alpha={ae:.3f}  R2={r2e:.3f}")

# FEP-STDP on core subnetwork
print("\n[4] FEP-STDP on core subnetwork...")
deg_sorted = sorted(Gu_gcc.degree(), key=lambda x: -x[1])
core_size = min(300, N_gcc)
core_nodes = [n for n, _ in deg_sorted[:core_size]]
Gu_core = Gu_gcc.subgraph(core_nodes).copy()
if not nx.is_connected(Gu_core):
    gcc_core = max(nx.connected_components(Gu_core), key=len)
    Gu_core = Gu_core.subgraph(gcc_core).copy()
    core_nodes = list(Gu_core.nodes())
N_core = len(core_nodes)
E_core = Gu_core.number_of_edges()
node_map = {old: new for new, old in enumerate(core_nodes)}
print(f"    Core: N={N_core}, E={E_core}")

adj_real = defaultdict(list)
for u, v, w in Gu_core.edges(data="weight", default=1.0):
    i, j = node_map[u], node_map[v]
    wn = min(w / 10.0, 1.0)
    adj_real[i].append((j, wn))
    adj_real[j].append((i, wn))

p_er2 = 2 * E_core / (N_core * (N_core - 1))
G_er_core = nx.erdos_renyi_graph(N_core, p_er2, seed=42)
adj_er2 = defaultdict(list)
for u, v in G_er_core.edges():
    adj_er2[u].append((v, 1.0))
    adj_er2[v].append((u, 1.0))

def run_fep(adj, name=""):
    N_use = N_core
    w = {}
    for i in range(N_use):
        for j, _ in adj.get(i, []):
            if j > i:
                wi = 0.05 if np.random.random() < 0.8 else 0.03
                w[(i,j)] = wi
                w[(j,i)] = wi
    v = np.random.randn(N_use) * 0.1
    spike_times = {i: [] for i in range(N_use)}
    Fs = []
    avs = []
    sigma_hist = []

    for t_step in range(200):
        I_ext = np.random.poisson(0.5, N_use) * 0.2
        I_syn = np.zeros(N_use)
        for i in range(N_use):
            for j, _ in adj.get(i, []):
                I_syn[i] += w.get((j,i), 0) * np.tanh(v[j])
        dv = (-v + I_syn + I_ext) / 10.0
        v += dv * 0.1
        spikes = np.where(v > 1.5)[0]
        v[spikes] = 0.0
        for si in spikes:
            spike_times[si].append(t_step)

        for (pre, post) in list(w.keys()):
            if spike_times[pre] and spike_times[post]:
                dt_st = spike_times[post][-1] - spike_times[pre][-1]
                if dt_st > 0:
                    dw = 0.005 * np.exp(-dt_st / 20.0)
                elif dt_st < 0:
                    dw = -0.0025 * np.exp(dt_st / 20.0)
                else:
                    dw = 0
                w[(pre,post)] += dw * 0.1

        Fs.append(np.mean((v - I_ext)**2) + 0.01 * sum(abs(wi) for wi in w.values()) / max(1, len(w)))
        if len(spikes) > 0:
            avs.append(len(spikes))

        if t_step % 20 == 0 and len(spikes) > 0:
            Gw = nx.Graph()
            Gw.add_nodes_from(range(N_use))
            for (i,j), wij in w.items():
                if abs(wij) > 0.001: Gw.add_edge(i, j)
            if Gw.number_of_edges() > N_use and nx.is_connected(Gw):
                Cw = nx.average_clustering(Gw)
                Lw = nx.average_shortest_path_length(Gw)
                sw = (Cw/C_er) / (Lw/L_er) if C_er > 0 else 1.0
                sigma_hist.append((t_step, sw))

    G_final = nx.Graph()
    G_final.add_nodes_from(range(N_use))
    for (i,j), wij in w.items():
        if abs(wij) > 0.001: G_final.add_edge(i, j)

    return {
        "N": N_use,
        "F_final": Fs[-1] if Fs else 0,
        "F_mean": float(np.mean(Fs[-50:])) if Fs else 0,
        "sigma_final": sigma_hist[-1][1] if sigma_hist else 0,
        "sigma_mean": float(np.mean([s[1] for s in sigma_hist])) if sigma_hist else 0,
        "n_avalanches": len(avs),
        "avalanche_mean": float(np.mean(avs)) if avs else 0,
        "avalanche_max": int(max(avs)) if avs else 0,
    }

print("    Running FEP-STDP on REAL larval topology...")
t1 = time.time()
rf = run_fep(adj_real, "real")
print(f"    Done in {time.time()-t1:.1f}s, F={rf['F_final']:.6f}, sigma={rf['sigma_final']:.3f}")

print("    Running FEP-STDP on ER control...")
t1 = time.time()
ef = run_fep(adj_er2, "er")
print(f"    Done in {time.time()-t1:.1f}s, F={ef['F_final']:.6f}, sigma={ef['sigma_final']:.3f}")

# Compile results
print("\n[5] Compiling results...")
v27_results = {
    "version": "V27",
    "species": "Drosophila melanogaster (larva)",
    "data": "Winding et al. 2023, Science (connectome_larval_cns.json)",
    "date": "2026-06-19",
    "full_connectome": {
        "N_total": N_full, "E_chemical": E_chem,
        "N_gcc": N_gcc, "E_gcc": E_gcc,
        "k_avg": round(k_avg, 2),
        "density": round(2*E_gcc/(N_gcc*(N_gcc-1)), 6),
    },
    "static_topology": {
        "sigma": round(sigma, 3),
        "C_real": round(C_real, 4), "L_real": round(L_real, 4),
        "C_er": round(C_er, 4), "L_er": round(L_er, 4),
        "gamma": round(gamma_exp, 3),
        "efficiency": round(eff_real, 4),
        "efficiency_er": round(nx.global_efficiency(G_er), 4),
        "ks_degree_p": float(ks_d.pvalue),
        "ks_cluster_p": float(ks_c.pvalue),
    },
    "fep_stdp": {"real": rf, "er": ef},
    "avalanche": {
        "real_mean": float(avr.mean()), "real_max": int(avr.max()),
        "real_alpha": round(ar, 3), "real_R2": round(r2r, 3),
        "er_mean": float(ave.mean()), "er_max": int(ave.max()),
        "er_alpha": round(ae, 3), "er_R2": round(r2e, 3),
    },
    "conclusion": (
        f"Larval sigma={sigma:.2f}, KS clust p={ks_c.pvalue:.2e}. "
        f"FEP real F={rf['F_final']:.4f} vs ER F={ef['F_final']:.4f}. "
        f"Avalanche alpha_real={ar:.2f} vs alpha_er={ae:.2f}."
    )
}

with open(os.path.join(OUT_DIR, "v27_results.json"), "w") as f:
    json.dump(v27_results, f, indent=2, default=str)

print("\n" + "=" * 60)
print("V27 COMPLETE")
print("=" * 60)
print(f"  sigma={sigma:.3f}  C={C_real:.4f}  L={L_real:.4f}")
print(f"  KS_clust_p={ks_c.pvalue:.2e}")
print(f"  FEP real: F={rf['F_final']:.6f} sigma={rf['sigma_final']:.3f}")
print(f"  FEP ER:   F={ef['F_final']:.6f} sigma={ef['sigma_final']:.3f}")
print(f"  Avalanche real alpha={ar:.3f} R2={r2r:.3f}")
print(f"  Avalanche ER   alpha={ae:.3f} R2={r2e:.3f}")
print(f"  Total time: {time.time()-t0:.1f}s")
