#!/usr/bin/env python3
"""V31-refined: SC-FC via C.elegans Neuron Classes (FIXED)."""
import numpy as np, json, os, warnings, time
warnings.filterwarnings("ignore")
import networkx as nx
from scipy import stats
np.random.seed(42)

os.chdir(r"D:\Obsidian\home\work\.openclaw\workspace\simulation")
OUT_DIR = "data/v31_results"
os.makedirs(OUT_DIR, exist_ok=True)

print("=" * 60)
print("V31-refined: SC-FC via C.elegans Neuron Classes")
print("=" * 60)

def classify_neuron(name):
    sensory = {"ADL","ADF","AFD","ALA","AQR","ASE","ASG","ASH","ASI","ASJ","ASK",
               "AUA","AWA","AWB","AWC","BAG","CEP","FLP","IL1","IL2","OLL","OLQ",
               "PDE","PHA","PHB","PHC","PLM","PLN","PQR","PVD","URX","URY",
               "ADE","ADF","ADL","AWA","AWB","AWC","AFD","ASH","ASI","ASJ","ASK"}
    motor = {"AS","DA","DB","DD","VA","VB","VC","VD"}
    if name[:3] in sensory or name[:2] in sensory: return "sensory"
    if name[:2] in motor: return "motor"
    return "interneuron"

print("[1] Loading connectome...")
import xlrd
wb = xlrd.open_workbook(r"D:\Obsidian\home\work\.openclaw\workspace\20_Projects\CST仿真平台\NeuronConnect.xls")
sheet = wb.sheet_by_index(0)
edges, node_types = [], {}
for r in range(1, sheet.nrows):
    n1, n2 = str(sheet.cell_value(r, 0)).strip(), str(sheet.cell_value(r, 1)).strip()
    etype = str(sheet.cell_value(r, 2)).strip()
    if n1 and n2 and n1 != n2 and etype in ("S", "Sp"):
        edges.append((n1, n2))
        for n in (n1, n2):
            if n not in node_types: node_types[n] = classify_neuron(n)

Gd = nx.DiGraph(); Gd.add_nodes_from(node_types); Gd.add_edges_from(edges)
Gu = Gd.to_undirected(); gcc = max(nx.connected_components(Gu), key=len)
G = Gu.subgraph(gcc).copy(); N = len(gcc)

from collections import Counter
type_counts = Counter(node_types[n] for n in gcc)
print(f"  N={N}, E={G.number_of_edges()}")
print(f"  Types: {dict(type_counts)}")

print("\n[2] Computing SC-FC via functional categories...")
nodes_list = sorted(G.nodes()); n2i = {n:i for i,n in enumerate(nodes_list)}
cat = np.array([node_types[n] for n in nodes_list])

within_e, between_e = 0, 0
within_possible, between_possible = 0, 0
cats = ["sensory","interneuron","motor"]
cat_pair_density = {}

for ci in cats:
    ni = np.where(cat == ci)[0]
    for cj in cats:
        nj = np.where(cat == cj)[0]
        if len(ni) == 0 or len(nj) == 0: continue
        if ci == cj:
            pp = len(ni) * (len(ni) - 1) // 2
            pa = sum(1 for x in ni for y in nj if x < y and G.has_edge(nodes_list[x], nodes_list[y]))
        else:
            pp = len(ni) * len(nj)
            pa = sum(1 for x in ni for y in nj if G.has_edge(nodes_list[x], nodes_list[y]))
        d = pa / max(1, pp)
        cat_pair_density[f"{ci[:3]}->{cj[:3]}"] = {"edges": pa, "possible": pp, "density": round(d, 4)}
        if ci == cj: within_e += pa; within_possible += pp
        else: between_e += pa; between_possible += pp

within_d = within_e / max(1, within_possible)
between_d = between_e / max(1, between_possible)
enrich = within_d / max(1e-10, between_d)
print(f"  Within-cat: {within_e}/{within_possible} ({within_d:.4f})")
print(f"  Between-cat: {between_e}/{between_possible} ({between_d:.4f})")
print(f"  Enrichment: {enrich:.1f}x")

print("\n  Category pairs:")
for k, v in sorted(cat_pair_density.items()):
    print(f"    {k}: {v['edges']:>4d}/{v['possible']:>5d} ({v['density']:.4f})")

print("\n[3] Permutation test (1000x)...")
G_mat = np.zeros((N,N))
for u,v in G.edges(): G_mat[n2i[u],n2i[v]]=1; G_mat[n2i[v],n2i[u]]=1
real_frac = within_e / max(1, within_e + between_e)

perm_fracs = []
for _ in range(1000):
    cp = cat[np.random.permutation(N)]
    pw = sum(1 for i in range(N) for j in range(i+1,N) if G_mat[i,j]>0 and cp[i]==cp[j])
    pb = sum(1 for i in range(N) for j in range(i+1,N) if G_mat[i,j]>0 and cp[i]!=cp[j])
    perm_fracs.append(pw / max(1, pw + pb))
perm_fracs = np.array(perm_fracs)
p_val = float((perm_fracs >= real_frac).mean())
print(f"  Real: {real_frac:.4f}  Perm: {perm_fracs.mean():.4f}+/-{perm_fracs.std():.4f}  p={p_val:.4f}")

print("\n[4] Modularity...")
m = G.number_of_edges()
comm = [{i for i in range(N) if cat[i]==c} for c in cats]
Q = 0
for c_set in comm:
    for i in c_set:
        ki = G.degree(nodes_list[i])
        for j in c_set:
            if i < j:
                aij = 1 if G.has_edge(nodes_list[i],nodes_list[j]) else 0
                Q += aij - ki * G.degree(nodes_list[j]) / (2*m)
Q /= (2*m)
print(f"  Q = {Q:.4f}")

# ER comparison
G_er = nx.erdos_renyi_graph(N, 2*m/(N*(N-1)), seed=42)
er_w = sum(1 for i in range(N) for j in range(i+1,N) if G_er.has_edge(i,j) and cat[i]==cat[j])
er_b = sum(1 for i in range(N) for j in range(i+1,N) if G_er.has_edge(i,j) and cat[i]!=cat[j])
er_frac = er_w / max(1, er_w + er_b)
print(f"  ER within-cat frac: {er_frac:.4f} (real: {real_frac:.4f}, diff: {real_frac-er_frac:+.4f})")

v31 = {
    "version": "V31-refined", "title": "SC-FC via Biological Neuron Classes",
    "date": "2026-06-19", "data": "Varshney 2011 + C.elegans naming",
    "neuron_types": {k: int(v) for k,v in type_counts.items()},
    "sc_fc": {
        "within_density": round(float(within_d),4),
        "between_density": round(float(between_d),4),
        "enrichment": round(float(enrich),1),
        "within_frac": round(float(real_frac),4),
        "er_within_frac": round(float(er_frac),4),
        "permutation_p": round(p_val,4),
        "modularity_Q": round(float(Q),4),
    },
    "category_pairs": cat_pair_density,
    "conclusion": (
        f"SC edges enriched {enrich:.0f}x within functional categories. "
        f"Permutation p={p_val:.4f} {'**' if p_val<0.01 else '*' if p_val<0.05 else 'ns'}. "
        f"Q={Q:.3f}. "
        f"Real fraction={real_frac:.3f} vs ER={er_frac:.3f}."
    )
}

with open(os.path.join(OUT_DIR, "v31_results.json"), "w") as f:
    json.dump(v31, f, indent=2)

print("\n" + "="*60)
print("V31-REFINED")
print("="*60)
print(f"  Enrichment: {enrich:.0f}x within-category")
print(f"  p = {p_val:.4f}  Q = {Q:.3f}")
print(f"  {v31['conclusion']}")
