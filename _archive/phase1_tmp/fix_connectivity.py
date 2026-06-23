"""Fix drosophila region connectivity and regenerate config"""
import json, networkx as nx, numpy as np, random

random.seed(42); np.random.seed(42)

with open(r"D:\Obsidian\phase1_workspace\drosophila_structured.json") as f:
    dro = json.load(f)

# Node sets
sensors = dro["sensor_idx"]
motor_set = set(dro["motor_idx"])
inter_rem = [n for n in dro["inter_idx"] if n not in motor_set]

region_nodes = {
    "vis": sorted(sensors[:50] + inter_rem[:50]),
    "chem": sorted(sensors[50:100] + inter_rem[50:100]),
    "assoc": sorted(inter_rem[100:250]),
    "motor": sorted(dro["motor_idx"][:100]),
}

# Build full graph for reference
G_full = nx.DiGraph()
for e in dro["edges_chem"]:
    G_full.add_edge(e[0], e[1], weight=e[2], type='chem')
for e in dro["edges_elec"]:
    G_full.add_edge(e[0], e[1], weight=e[2], type='elec')
    G_full.add_edge(e[1], e[0], weight=e[2], type='elec')

def extract_and_fix_region(name, nodes, G_full, min_edges_per_node=3):
    """Extract subgraph edges and add supplemental to ensure connectivity + density"""
    ns = set(nodes)
    chem_edges = []; elec_edges = []
    for u, v, d in G_full.edges(data=True):
        if u in ns and v in ns:
            if d['type'] == 'chem':
                chem_edges.append([u, v, d['weight']])
            else:
                elec_edges.append([u, v, d['weight']])

    # Check connectivity
    G_sub = nx.Graph()
    for e in chem_edges: G_sub.add_edge(e[0], e[1])
    for e in elec_edges: G_sub.add_edge(e[0], e[1])
    comps = list(nx.connected_components(G_sub))
    gc = max(comps, key=len) if comps else set()

    n_added = 0
    if len(comps) > 1:
        print(f"  {name}: fixing {len(comps)} components, giant={len(gc)}/{len(ns)}")
        # Connect each small component to giant component
        gc_list = list(gc)
        for comp in comps:
            if comp == gc: continue
            bridge_src = random.choice(list(comp))
            bridge_tgt = random.choice(gc_list)
            w = random.uniform(0.3, 0.6)
            chem_edges.append([bridge_src, bridge_tgt, w])
            chem_edges.append([bridge_tgt, bridge_src, w])  # bidirectional
            n_added += 2

    # Ensure minimum out-degree per node
    out_deg = {}
    for e in chem_edges: out_deg[e[0]] = out_deg.get(e[0], 0) + 1
    for e in elec_edges: out_deg[e[0]] = out_deg.get(e[0], 0) + 1

    for node in ns:
        deg = out_deg.get(node, 0)
        if deg < min_edges_per_node:
            candidates = [n for n in ns if n != node]
            for _ in range(min_edges_per_node - deg):
                tgt = random.choice(candidates)
                w = random.uniform(0.1, 0.3)
                chem_edges.append([node, tgt, w])
                n_added += 1

    # Remap to 0..N-1
    node_map = {old: new for new, old in enumerate(nodes)}
    chem_r = [[node_map[e[0]], node_map[e[1]], e[2]] for e in chem_edges]
    elec_r = [[node_map[e[0]], node_map[e[1]], e[2]] for e in elec_edges]

    # Verify
    G_check = nx.Graph()
    for e in chem_r: G_check.add_edge(e[0], e[1])
    for e in elec_r: G_check.add_edge(e[0], e[1])
    if not nx.is_connected(G_check):
        print(f"  WARNING: {name} still disconnected!")

    k_avg = (len(chem_r) + len(elec_r)) / len(nodes)
    print(f"  {name}: {len(chem_r)} chem + {len(elec_r)} elec, k_avg={k_avg:.1f}, added={n_added}")

    return {
        "N": len(nodes), "original_nodes": nodes,
        "edges_chem": chem_r, "edges_elec": elec_r,
    }

# Extract and fix all regions
region_data = {}
for name, nodes in region_nodes.items():
    region_data[name] = extract_and_fix_region(name, nodes, G_full, min_edges_per_node=4)

# Cross-region bonds: use biological edges + supplement if sparse
def extract_cross(src_name, tgt_name, src_nodes, tgt_nodes, G_full, min_cross=50):
    ss = set(src_nodes); ts = set(tgt_nodes)
    edges = []
    for u, v, d in G_full.edges(data=True):
        if u in ss and v in ts:
            edges.append([u, v, d['weight']])

    n_added = 0
    if len(edges) < min_cross:
        src_list = list(ss); tgt_list = list(ts)
        for _ in range(min_cross - len(edges)):
            s = random.choice(src_list)
            t = random.choice(tgt_list)
            edges.append([s, t, random.uniform(0.05, 0.2)])
            n_added += 1

    src_map = {old: new for new, old in enumerate(src_nodes)}
    tgt_map = {old: new for new, old in enumerate(tgt_nodes)}
    remapped = [[src_map[e[0]], tgt_map[e[1]], e[2]] for e in edges]
    print(f"Cross {src_name}->{tgt_name}: {len(remapped)} edges (bio={len(remapped)-n_added}, supp={n_added})")
    return remapped

cross_bonds = {}
for sn, tn in [("vis","assoc"),("chem","assoc"),("assoc","motor"),("motor","assoc")]:
    cross_bonds[f"{sn}_to_{tn}"] = extract_cross(sn, tn, region_nodes[sn], region_nodes[tn], G_full)

config = {
    "description": "V30 Drosophila connectome config v2 - connectivity-fixed",
    "source": "hemibrain/flywire 800-node connectome",
    "regions": region_data,
    "cross_bonds": cross_bonds,
}
with open(r"D:\Obsidian\phase1_workspace\v30_drosophila_config.json", "w") as f:
    json.dump(config, f)
print("\nSaved v30_drosophila_config.json v2")
