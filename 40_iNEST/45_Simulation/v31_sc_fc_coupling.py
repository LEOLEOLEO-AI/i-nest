#!/usr/bin/env python3
"""V31: C.elegans SC-FC coupling via graph heat kernel.
Heat kernel: K = exp(-t * L_norm) directly maps SC -> FC.
The diffusion time t controls spatial scale.
"""
import numpy as np, json, os, warnings, time
warnings.filterwarnings("ignore")
import networkx as nx
from scipy import stats
from scipy.linalg import expm
np.random.seed(42)

os.chdir(r"D:\Obsidian\home\work\.openclaw\workspace\simulation")
OUT_DIR = "data/v31_results"
os.makedirs(OUT_DIR, exist_ok=True)

print("=" * 60)
print("V31: C.elegans SC-FC via Graph Heat Kernel")
print("=" * 60)

# Load connectome
print("[1] Loading connectome...")
import xlrd
wb = xlrd.open_workbook(r"D:\Obsidian\home\work\.openclaw\workspace\20_Projects\CST仿真平台\NeuronConnect.xls")
sheet = wb.sheet_by_index(0)
edges, nodes_set = [], set()
for r in range(1, sheet.nrows):
    n1, n2 = str(sheet.cell_value(r, 0)).strip(), str(sheet.cell_value(r, 1)).strip()
    if n1 and n2 and n1 != n2 and str(sheet.cell_value(r, 2)).strip() in ("S", "Sp"):
        nodes_set.add(n1); nodes_set.add(n2); edges.append((n1, n2))
Gd = nx.DiGraph(); Gd.add_nodes_from(nodes_set); Gd.add_edges_from(edges)
Gu = Gd.to_undirected(); gcc = max(nx.connected_components(Gu), key=len)
G_real = Gu.subgraph(gcc).copy(); N = len(gcc)
nodes_list = sorted(G_real.nodes()); idx = {n: i for i, n in enumerate(nodes_list)}
A = np.zeros((N, N))
for u, v in G_real.edges(): A[idx[u], idx[v]] = 1.0; A[idx[v], idx[u]] = 1.0
print(f"  N={N}, E={G_real.number_of_edges()}")

# Structural metrics
k_avg = A.sum() / N
C_s = nx.average_clustering(G_real); L_s = nx.average_shortest_path_length(G_real)
G_er_s = nx.erdos_renyi_graph(N, k_avg/(N-1), seed=42)
for _ in range(100):
    if nx.is_connected(G_er_s): break
    G_er_s = nx.erdos_renyi_graph(N, k_avg/(N-1), seed=np.random.randint(99999))
C_er_s = nx.average_clustering(G_er_s); L_er_s = nx.average_shortest_path_length(G_er_s)
sigma_s = (C_s/C_er_s)/(L_s/L_er_s)
print(f"  Structural sigma={sigma_s:.3f}")

# ER control
A_er = np.zeros((N, N))
for u, v in G_er_s.edges():
    if u < N and v < N: A_er[u, v] = 1.0; A_er[v, u] = 1.0
te = int(A.sum()/2); ce = int(A_er.sum()/2)
if ce < te:
    pairs = [(i,j) for i in range(N) for j in range(i+1,N) if A_er[i,j]==0]
    for i,j in np.random.permutation(pairs)[:te-ce]: A_er[i,j]=1.0; A_er[j,i]=1.0

# Heat kernel
print("[2] Computing heat kernel FC...")
def heat_kernel_fc(A, t_values=[0.5, 1.0, 2.0, 5.0, 10.0]):
    """Compute FC as heat kernel of normalized graph Laplacian at multiple scales."""
    deg = A.sum(axis=1)
    deg[deg == 0] = 1
    D_inv_sqrt = np.diag(1.0 / np.sqrt(deg))
    L_norm = np.eye(N) - D_inv_sqrt @ A @ D_inv_sqrt
    results = {}
    for t in t_values:
        K = expm(-t * L_norm)
        np.fill_diagonal(K, 0)
        G_fc = None
        for thresh in [0.3, 0.5, 0.7]:
            fc_bin = (K > thresh).astype(float)
            np.fill_diagonal(fc_bin, 0)
            G_tmp = nx.from_numpy_array(fc_bin)
            if G_tmp.number_of_edges() > N and nx.is_connected(G_tmp):
                G_fc = G_tmp
                break
        if G_fc is None or G_fc.number_of_edges() <= N:
            results[t] = {"sigma_fc": 0, "C_fc": 0, "L_fc": 0, "E_fc": 0}
            continue
        C_fc = nx.average_clustering(G_fc); L_fc = nx.average_shortest_path_length(G_fc)
        E_fc = G_fc.number_of_edges(); k_fc = 2*E_fc/N
        G_er_fc = nx.erdos_renyi_graph(N, k_fc/(N-1), seed=42)
        for _ in range(50):
            if nx.is_connected(G_er_fc): break
            G_er_fc = nx.erdos_renyi_graph(N, k_fc/(N-1), seed=np.random.randint(99999))
        if nx.is_connected(G_er_fc):
            C_er_fc = nx.average_clustering(G_er_fc); L_er_fc = nx.average_shortest_path_length(G_er_fc)
            sigma_fc = (C_fc/C_er_fc)/(L_fc/L_er_fc) if C_er_fc > 0 else 0
        else: sigma_fc = 0
        results[t] = {"sigma_fc": round(float(sigma_fc),3), "C_fc": round(float(C_fc),4),
                      "L_fc": round(float(L_fc),4), "E_fc": E_fc}
    return results

fc_real = heat_kernel_fc(A)
fc_er = heat_kernel_fc(A_er)

for t in sorted(fc_real):
    print(f"  t={t:.1f}: FC sigma real={fc_real[t]['sigma_fc']:.3f} ER={fc_er[t]['sigma_fc']:.3f}")

# Best scale: where FC sigma is maximally different from ER
best_t = max(fc_real.keys(), key=lambda t: fc_real[t]['sigma_fc'])
best_sigma_fc = fc_real[best_t]['sigma_fc']
best_sigma_er = fc_er[best_t]['sigma_fc']

# SC-FC coupling at best scale
print(f"\n[3] SC-FC coupling at t={best_t}...")
K_real = expm(-best_t * (np.eye(N) - np.diag(1/np.sqrt(A.sum(axis=1))) @ A @ np.diag(1/np.sqrt(A.sum(axis=1)))))
np.fill_diagonal(K_real, 0)
K_er_mat = expm(-best_t * (np.eye(N) - np.diag(1/np.sqrt(A_er.sum(axis=1))) @ A_er @ np.diag(1/np.sqrt(A_er.sum(axis=1)))))
np.fill_diagonal(K_er_mat, 0)

def scfc(A_sc, K_mat):
    triu = np.triu_indices_from(A_sc, k=1)
    sc = A_sc[triu]; fc_v = K_mat[triu]
    mask = sc > 0
    if mask.sum() < 10: return 0, 1
    r, p = stats.pearsonr(sc[mask], fc_v[mask])
    return r, p

r_r, p_r = scfc(A, K_real)
r_e, p_e = scfc(A_er, K_er_mat)
print(f"  SC-FC r: real={r_r:.4f} (p={p_r:.2e}), ER={r_e:.4f} (p={p_e:.2e})")

# Mean FC strength (excluding structural edges vs on them)
triu = np.triu_indices_from(A, k=1)
sc_on = A[triu] > 0; sc_off = ~sc_on
fc_on = K_real[triu][sc_on]; fc_off = K_real[triu][sc_off]
print(f"  FC on SC edges: {np.mean(fc_on):.6f} vs off: {np.mean(fc_off):.6f}")
print(f"  Ratio on/off: {np.mean(fc_on)/max(1e-10,np.mean(fc_off)):.2f}x")

# Compose
v31 = {
    "version": "V31", "title": "C.elegans SC-FC via Graph Heat Kernel",
    "date": "2026-06-19", "data": "Varshney 2011",
    "method": "Heat kernel exp(-t*L_norm) of normalized graph Laplacian",
    "structural": {"N":N,"E":int(G_real.number_of_edges()),"k_avg":round(float(k_avg),2),
                   "sigma_s":round(float(sigma_s),3),"C_s":round(float(C_s),4),"L_s":round(float(L_s),4)},
    "functional": {
        "best_t": best_t,
        "sigma_fc_real": round(float(best_sigma_fc),3),
        "sigma_fc_er": round(float(best_sigma_er),3),
        "fc_by_scale": {str(t): {"real_sigma": fc_real[t]['sigma_fc'], "er_sigma": fc_er[t]['sigma_fc']} for t in sorted(fc_real)},
    },
    "sc_fc_coupling": {
        "r_real": round(float(r_r),4), "p_real": float(p_r),
        "r_er": round(float(r_e),4), "p_er": float(p_e),
        "fc_on_sc": round(float(np.mean(fc_on)),6),
        "fc_off_sc": round(float(np.mean(fc_off)),6),
        "on_off_ratio": round(float(np.mean(fc_on)/max(1e-10,np.mean(fc_off))),2),
    },
    "conclusion": f"SC->FC via heat kernel at t={best_t}: sigma_fc={best_sigma_fc:.1f} vs ER={best_sigma_er:.1f}. SC-FC r={r_r:.3f}."
}

with open(os.path.join(OUT_DIR, "v31_results.json"), "w") as f:
    json.dump(v31, f, indent=2)

print("\n" + "="*60)
print("V31 COMPLETE")
print("="*60)
print(f"  SC sigma={sigma_s:.1f} -> FC sigma={best_sigma_fc:.1f} (t={best_t})")
print(f"  SC-FC r={r_r:.3f} (p={p_r:.2e})")
print(f"  FC on/off SC edges: {np.mean(fc_on)/max(1e-10,np.mean(fc_off)):.2f}x")
print(f"  Saved: data/v31_results/v31_results.json")
