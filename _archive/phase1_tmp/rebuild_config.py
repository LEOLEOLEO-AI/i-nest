"""Rebuild drosophila config with higher motor region density"""
import json, networkx as nx, numpy as np, random
random.seed(42); np.random.seed(42)

with open(r"D:\Obsidian\phase1_workspace\drosophila_structured.json") as f:
    dro = json.load(f)

sensors = dro["sensor_idx"]
motor_set = set(dro["motor_idx"])
inter_rem = [n for n in dro["inter_idx"] if n not in motor_set]

region_nodes = {
    "vis": sorted(sensors[:50] + inter_rem[:50]),
    "chem": sorted(sensors[50:100] + inter_rem[50:100]),
    "assoc": sorted(inter_rem[100:250]),
    "motor": sorted(dro["motor_idx"][:100]),
}

G_full = nx.DiGraph()
for e in dro["edges_chem"]:
    G_full.add_edge(e[0], e[1], weight=e[2], type='chem')
for e in dro["edges_elec"]:
    G_full.add_edge(e[0], e[1], weight=e[2], type='elec')
    G_full.add_edge(e[1], e[0], weight=e[2], type='elec')

def extract_and_fix(name, nodes, G_full, target_k=8):
    ns = set(nodes)
    chem_edges = []; elec_edges = []
    for u, v, d in G_full.edges(data=True):
        if u in ns and v in ns:
            if d['type'] == 'chem':
                chem_edges.append([u, v, d['weight']])
            else:
                elec_edges.append([u, v, d['weight']])

    # Connectivity fix
    G_sub = nx.Graph()
    for e in chem_edges: G_sub.add_edge(e[0], e[1])
    for e in elec_edges: G_sub.add_edge(e[0], e[1])
    comps = list(nx.connected_components(G_sub))
    gc = max(comps, key=len) if comps else set()
    if len(comps) > 1:
        gc_list = list(gc)
        for comp in comps:
            if comp == gc: continue
            bridge_src = random.choice(list(comp))
            bridge_tgt = random.choice(gc_list)
            chem_edges.append([bridge_src, bridge_tgt, 0.5])
            chem_edges.append([bridge_tgt, bridge_src, 0.5])

    # Boost to target mean degree
    out_deg = {}
    for e in chem_edges: out_deg[e[0]] = out_deg.get(e[0], 0) + 1
    for e in elec_edges: out_deg[e[0]] = out_deg.get(e[0], 0) + 1
    current_k = (len(chem_edges) + len(elec_edges)) / len(nodes)
    if current_k < target_k:
        n_extra = int((target_k - current_k) * len(nodes))
        node_list = list(ns)
        for _ in range(n_extra):
            s = random.choice(node_list)
            t = random.choice([n for n in node_list if n != s])
            chem_edges.append([s, t, random.uniform(0.2, 0.5)])

    # Remap
    node_map = {old: new for new, old in enumerate(nodes)}
    chem_r = [[node_map[e[0]], node_map[e[1]], e[2]] for e in chem_edges]
    elec_r = [[node_map[e[0]], node_map[e[1]], e[2]] for e in elec_edges]
    k_final = (len(chem_r) + len(elec_r)) / len(nodes)
    print(f"  {name}: {len(chem_r)} chem + {len(elec_r)} elec, k_avg={k_final:.1f}")
    return {"N": len(nodes), "original_nodes": nodes, "edges_chem": chem_r, "edges_elec": elec_r}

region_data = {}
for name, nodes in region_nodes.items():
    tk = 8 if name in ("motor", "assoc") else 7
    region_data[name] = extract_and_fix(name, nodes, G_full, target_k=tk)

# Cross bonds: densely connect key pathways
def make_cross(src_n, tgt_n, min_edges=250):
    edges = []
    for _ in range(min_edges):
        s = random.randint(0, src_n-1); t = random.randint(0, tgt_n-1)
        edges.append([s, t, random.uniform(0.1, 0.5)])
    return edges

cross_bonds = {}
# Use biological edges where available, supplement with artificial
for sn, tn, min_e in [("vis","assoc",300),("chem","assoc",300),("assoc","motor",350),("motor","assoc",200)]:
    ss = set(region_nodes[sn]); ts = set(region_nodes[tn])
    bio = []
    for u, v, d in G_full.edges(data=True):
        if u in ss and v in ts:
            bio.append([u, v, d['weight']])
    src_map = {old: new for new, old in enumerate(region_nodes[sn])}
    tgt_map = {old: new for new, old in enumerate(region_nodes[tn])}
    all_e = [[src_map[e[0]], tgt_map[e[1]], e[2]] for e in bio]
    # Supplement
    src_n = region_nodes[sn]['N']; tgt_n = region_nodes[tn]['N']
    if len(all_e) < min_e:
        for _ in range(min_e - len(all_e)):
            all_e.append([random.randint(0,src_n-1), random.randint(0,tgt_n-1), random.uniform(0.1,0.5)])
    cross_bonds[f"{sn}_to_{tn}"] = all_e
    print(f"Cross {sn}->{tn}: {len(all_e)} edges (bio={len(bio)})")

config = {"description": "V30 Drosophila config v3 - density-boosted", "regions": region_data, "cross_bonds": cross_bonds}
with open(r"D:\Obsidian\phase1_workspace\v30_drosophila_config.json", "w") as f:
    json.dump(config, f)
print("Saved v3 config")
