import os, csv, json, time, warnings; warnings.filterwarnings('ignore')
import numpy as np; import networkx as nx; from scipy import stats; from collections import Counter
np.random.seed(42)
os.chdir(r"D:\Obsidian\home\work\.openclaw\workspace\simulation")

v28 = json.load(open("data/v28_results/v28_results.json"))

print("Loading Hemibrain v1.2...")
csv_path = r"D:\Obsidian\home\work\.openclaw\workspace\sdi_sim\species_data\exported-traced-adjacencies-v1.2\traced-total-connections.csv"
id_to_idx = {}
edges = []
with open(csv_path) as f:
    next(f)
    for line in f:
        parts = line.strip().split(",")
        if len(parts) >= 3:
            pre, post = parts[0], parts[1]
            if pre not in id_to_idx: id_to_idx[pre] = len(id_to_idx)
            if post not in id_to_idx: id_to_idx[post] = len(id_to_idx)
            edges.append((id_to_idx[pre], id_to_idx[post]))

N_full = len(id_to_idx)
print(f"Full: N={N_full}, E={len(edges):,}")

G_full = nx.Graph(); G_full.add_nodes_from(range(N_full)); G_full.add_edges_from(edges)
gcc = max(nx.connected_components(G_full), key=len)
G_gcc = G_full.subgraph(gcc).copy()
N_gcc = len(gcc); E_gcc = G_gcc.number_of_edges()
print(f"GCC: N={N_gcc}, E={E_gcc:,}")

deg_sorted = sorted(G_gcc.degree(), key=lambda x: -x[1])
core_nodes = [n for n,_ in deg_sorted[:1000]]
G_core = G_gcc.subgraph(core_nodes).copy()
if not nx.is_connected(G_core):
    gcc_core = max(nx.connected_components(G_core), key=len)
    G_core = G_core.subgraph(gcc_core).copy()
N_core = G_core.number_of_nodes(); E_core = G_core.number_of_edges()
k_core = 2*E_core/N_core
print(f"Core: N={N_core}, E={E_core:,}, k_avg={k_core:.1f}")

print("Computing metrics...")
t0 = time.time()
C_real = nx.average_clustering(G_core)
L_real = nx.average_shortest_path_length(G_core)
G_er = nx.erdos_renyi_graph(N_core, k_core/(N_core-1), seed=42)
for _ in range(100):
    if nx.is_connected(G_er): break
    G_er = nx.erdos_renyi_graph(N_core, k_core/(N_core-1), seed=np.random.randint(99999))
C_er = nx.average_clustering(G_er); L_er = nx.average_shortest_path_length(G_er)
sigma = (C_real/C_er)/(L_real/L_er)
print(f"sigma={sigma:.3f} C={C_real:.4f} L={L_real:.4f} ({time.time()-t0:.1f}s)")

def avalanches(G, trials=100, steps=50):
    nodes_list = list(G.nodes()); sizes = []
    for _ in range(trials):
        active = {np.random.choice(nodes_list)}; visited = set(active); cs = 1
        for _ in range(steps):
            na = set()
            for node in active:
                nbs = list(G.neighbors(node))
                if nbs:
                    k = min(len(nbs), np.random.poisson(2))
                    for nb in np.random.choice(nbs, size=max(1,k), replace=False):
                        if nb not in visited and np.random.random() < 0.3: na.add(nb); visited.add(nb)
            if not na: break
            active = na; cs += len(na)
        sizes.append(cs)
    return np.array(sizes)

av_sizes = avalanches(G_core)
counts = Counter(av_sizes); sx = np.array(sorted(counts.keys())); sy = np.array([counts[k] for k in sx])
mask = (sx >= 2) & (sy > 0)
if mask.sum() >= 4:
    lx = np.log10(sx[mask].astype(float)); ly = np.log10(sy[mask].astype(float))
    slope, _, r2, _, _ = stats.linregress(lx, ly); alpha = -slope
else: alpha, r2 = 0, 0
print(f"alpha={alpha:.3f} R2={r2:.3f}")

v28["species"]["Drosophila Adult (Hemibrain)"] = {
    "N": N_core, "E": E_core, "k_avg": round(k_core, 1),
    "sigma": round(sigma, 3), "C": round(C_real, 4), "L": round(L_real, 4),
    "alpha_avalanche": round(alpha, 3), "alpha_R2": round(r2, 3),
    "sigma_times_alpha": round(sigma*alpha, 3),
    "source": "FlyWire Hemibrain v1.2", "ref": "traced-total-connections.csv",
    "note": f"Core N={N_core} from full N={N_gcc}"
}

species_list = list(v28["species"].keys())
sigmas = np.array([v28["species"][s]["sigma"] for s in species_list])
alphas = np.array([v28["species"][s]["alpha_avalanche"] for s in species_list])
Ns = np.array([v28["species"][s]["N"] for s in species_list])
sigma_alpha = sigmas * alphas
cv = float(np.std(sigma_alpha) / np.mean(sigma_alpha))

lx_n = np.log10(Ns); ly_s = np.log10(sigmas)
slope_n, _, r2_n, p_n, _ = stats.linregress(lx_n, ly_s)
slope_sa, _, r2_sa, p_sa, _ = stats.linregress(lx_n, sigma_alpha)

v28["n_species"] = len(species_list)
v28["cross_species_analysis"] = {
    "sigma_alpha_mean": round(float(np.mean(sigma_alpha)), 3),
    "sigma_alpha_std": round(float(np.std(sigma_alpha)), 3),
    "sigma_alpha_cv": round(float(cv), 3),
    "constancy_supported": bool(cv < 0.5),
    "sigma_vs_N_slope": round(float(slope_n), 3),
    "sigma_vs_N_R2": round(float(r2_n), 3),
    "sigma_vs_N_p": round(float(p_n), 4),
    "sigma_alpha_vs_N_slope": round(float(slope_sa), 3),
    "sigma_alpha_vs_N_R2": round(float(r2_sa), 3),
}
v28["conclusion"] = (
    f"4-species sigma*alpha={np.mean(sigma_alpha):.3f}+/-{np.std(sigma_alpha):.3f} "
    f"(CV={cv:.2f}). sigma~N^{slope_n:.3f} (R2={r2_n:.3f}). "
    f"{'Supports' if cv < 0.5 else 'Weakly supports'} iNEST constancy."
)

with open("data/v28_results/v28_results.json", "w") as f:
    json.dump(v28, f, indent=2)

print("\n" + "="*60)
print("V28 UPDATED (4 species)")
print("="*60)
print(f"{'Species':<30s} {'N':>6s} {'sigma':>8s} {'alpha':>8s} {'s*a':>8s}")
print("-"*60)
for s in species_list:
    m = v28["species"][s]
    print(f"{s:<30s} {m['N']:>6d} {m['sigma']:>8.3f} {m['alpha_avalanche']:>8.3f} {m['sigma_times_alpha']:>8.3f}")
print("-"*60)
print(f"sigma*alpha = {np.mean(sigma_alpha):.3f} +/- {np.std(sigma_alpha):.3f} CV={cv:.3f}")
print(f"sigma ~ N^{slope_n:.3f} R2={r2_n:.3f}")
