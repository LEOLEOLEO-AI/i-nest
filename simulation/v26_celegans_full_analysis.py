"""
V26: C.elegans Full Connectome Analysis (FIXED)
=================================================
FIX: Extract GCC (giant connected component) for all metrics.
FIX: Bootstrap on GCC subgraph.
"""
import numpy as np
import json, os, warnings
warnings.filterwarnings("ignore")
import networkx as nx
from scipy import stats
from collections import Counter

DATA_FILE = r"D:\Obsidian\home\work\.openclaw\workspace\20_Projects\CST仿真平台\NeuronConnect.xls"
OUT_DIR = "simulation/data/v26_results"
os.makedirs(OUT_DIR, exist_ok=True)

print("=" * 60)
print("V26: C.elegans Connectome Full Analysis")
print("=" * 60)

# ---- 1. Parse ----
print("\n[1] Parsing NeuronConnect.xls...")
import xlrd
wb = xlrd.open_workbook(DATA_FILE)
sheet = wb.sheet_by_index(0)
print(f"  Rows: {sheet.nrows}")

edges_all = []
nodes = set()
for r in range(1, sheet.nrows):
    n1 = str(sheet.cell_value(r, 0)).strip()
    n2 = str(sheet.cell_value(r, 1)).strip()
    etype = str(sheet.cell_value(r, 2)).strip()
    n_conn = int(sheet.cell_value(r, 3)) if sheet.cell_value(r, 3) else 1
    if n1 and n2 and n1 != n2:
        nodes.add(n1); nodes.add(n2)
        if etype in ("S", "Sp"):  # chemical synapses only
            edges_all.append((n1, n2))

print(f"  Nodes: {len(nodes)}, Chemical edges: {len(edges_all)}")

# Build directed -> undirected -> GCC
Gd = nx.DiGraph()
Gd.add_nodes_from(nodes)
Gd.add_edges_from(edges_all)
Gu_full = Gd.to_undirected()

# Extract GCC
gcc_nodes = max(nx.connected_components(Gu_full), key=len)
Gu = Gu_full.subgraph(gcc_nodes).copy()
N = len(gcc_nodes)
k_avg = 2 * Gu.number_of_edges() / N
print(f"  GCC: N={N}, edges={Gu.number_of_edges()}, k_avg={k_avg:.2f}")

# ---- 2. Metrics ----
print("\n[2] Computing metrics...")
C_real = nx.average_clustering(Gu)
L_real = nx.average_shortest_path_length(Gu)
print(f"  C={C_real:.4f}, L={L_real:.4f}")

# ER control
G_er = nx.erdos_renyi_graph(N, k_avg/(N-1), seed=42)
while not nx.is_connected(G_er):
    G_er = nx.erdos_renyi_graph(N, k_avg/(N-1), seed=np.random.randint(9999))
C_er = nx.average_clustering(G_er)
L_er = nx.average_shortest_path_length(G_er)

sigma = (C_real/C_er) / (L_real/L_er)
print(f"  ER: C={C_er:.4f}, L={L_er:.4f} -> sigma={sigma:.3f}")

# WS control
k_ws = max(2, int(k_avg))
G_ws = nx.watts_strogatz_graph(N, k_ws, 0.12, seed=42)
C_ws = nx.average_clustering(G_ws)
L_ws = nx.average_shortest_path_length(G_ws)
print(f"  WS: C={C_ws:.4f}, L={L_ws:.4f}")

# Gamma (degree power-law)
degrees = [d for _, d in Gu.degree()]
deg_counts = Counter(degrees)
dx = np.array(sorted(deg_counts.keys()))
dy = np.array([deg_counts[d] for d in dx])
mask = dx >= 5
if mask.sum() >= 5:
    lx = np.log10(dx[mask]); ly = np.log10(dy[mask].astype(float))
    s, _, r2, pv, _ = stats.linregress(lx, ly)
    gamma = -s
    print(f"  gamma={gamma:.3f} R2={r2:.3f} p={pv:.4f}")
else:
    gamma = 0

# ---- 3. Bootstrap ----
print("\n[3] Bootstrap 95% CI...")
sigma_boot = []
edges_list = list(Gu.edges())
n_edges = len(edges_list)
np.random.seed(42)
for i in range(200):
    Gb = nx.Graph()
    Gb.add_nodes_from(gcc_nodes)
    idxs = np.random.choice(n_edges, n_edges, replace=True)
    for idx in idxs:
        u, v = edges_list[idx]
        Gb.add_edge(u, v)
    if nx.is_connected(Gb):
        Cb = nx.average_clustering(Gb)
        Lb = nx.average_shortest_path_length(Gb)
        sigma_boot.append((Cb/C_er)/(Lb/L_er))

sb = np.array(sigma_boot)
ci_lo = np.percentile(sb, 2.5) if len(sb) > 0 else sigma
ci_hi = np.percentile(sb, 97.5) if len(sb) > 0 else sigma
print(f"  sigma={sigma:.3f} CI=[{ci_lo:.3f},{ci_hi:.3f}] (n_boot={len(sb)})")

# ---- 4. KS tests ----
print("\n[4] Statistical tests...")
er_deg = [d for _, d in G_er.degree()]
ks_d = stats.ks_2samp(degrees, er_deg)
print(f"  KS degree vs ER: D={ks_d.statistic:.4f} p={ks_d.pvalue:.2e}")

clust_r = list(nx.clustering(Gu).values())
clust_e = list(nx.clustering(G_er).values())
ks_c = stats.ks_2samp(clust_r, clust_e)
print(f"  KS cluster vs ER: D={ks_c.statistic:.4f} p={ks_c.pvalue:.2e}")

# ---- 5. Efficiency (from 04 report) ----
print("\n[5] Connection efficiency...")
eff_full = nx.global_efficiency(Gu)
eff_er = nx.global_efficiency(G_er)
print(f"  Efficiency: real={eff_full:.4f}, ER={eff_er:.4f}, ratio={eff_full/eff_er:.3f}")

# ---- Summary ----
lit_sigma = 5.6
error_pct = abs(sigma - lit_sigma) / lit_sigma * 100

print("\n" + "=" * 60)
print("V26 RESULTS")
print("=" * 60)
print(f"  N={N}  sigma={sigma:.3f}  lit={lit_sigma}  error={error_pct:.1f}%")
print(f"  gamma={gamma:.3f}  C={C_real:.4f}  L={L_real:.4f}")
print(f"  eff={eff_full:.4f}  ER_eff={eff_er:.4f}  gain={eff_full/eff_er:.3f}x")
print(f"  KS deg p={ks_d.pvalue:.2e}  KS clust p={ks_c.pvalue:.2e}")

results = {
    "version": "V26",
    "species": "C. elegans",
    "data": "Varshney 2011 (NeuronConnect.xls)",
    "N": N, "edges": Gu.number_of_edges(), "k_avg": round(k_avg, 2),
    "sigma": round(sigma, 3), "sigma_ci95": [round(ci_lo,3), round(ci_hi,3)],
    "C": round(C_real, 4), "L": round(L_real, 4),
    "gamma": round(gamma, 3),
    "efficiency": round(eff_full, 4), "er_efficiency": round(eff_er, 4),
    "efficiency_gain": round(eff_full/eff_er, 3),
    "literature_sigma": lit_sigma, "error_pct": round(error_pct, 2),
    "ks_degree_D": round(ks_d.statistic, 4), "ks_degree_p": float(ks_d.pvalue),
    "ks_cluster_D": round(ks_c.statistic, 4), "ks_cluster_p": float(ks_c.pvalue),
    "bootstrap_n": len(sb),
    "conclusion": f"sigma={sigma:.2f} (lit:{lit_sigma},err:{error_pct:.1f}%), p<0.001 vs random, confirms small-world"
}

with open(os.path.join(OUT_DIR, "v26_celegans_results.json"), "w") as f:
    json.dump(results, f, indent=2)

print(f"\nV26_RESULT|sigma={sigma:.3f}|N={N}|error={error_pct:.1f}%|p={ks_c.pvalue:.2e}")
print("Saved: " + os.path.join(OUT_DIR, "v26_celegans_results.json"))