"""Generate motor_idx for drosophila connectome and create V30 replacement"""
import json, numpy as np
from collections import Counter

# Load drosophila
with open(r"D:\Obsidian\phase1_workspace\drosophila_structured.json") as f:
    dro = json.load(f)

# Compute out-degree
out_deg = Counter()
for e in dro["edges_chem"]:
    out_deg[e[0]] += 1
for e in dro["edges_elec"]:
    out_deg[e[0]] += 1

# Select top 100 interneurons by out-degree as motor neurons
inter_idx = dro["inter_idx"]
ranked = sorted([(n, out_deg.get(n, 0)) for n in inter_idx], key=lambda x: -x[1])
motor_idx = sorted([n for n, _ in ranked[:100]])

# Update remaining interneurons
motor_set = set(motor_idx)
inter_remaining = [n for n in inter_idx if n not in motor_set]

print(f"motor_idx: {len(motor_idx)} nodes, out-degree range {ranked[99][1]}-{ranked[0][1]}")
print(f"inter_remaining: {len(inter_remaining)} nodes")
print(f"sensor_idx: {len(dro['sensor_idx'])} nodes")

# Save updated drosophila with motor_idx
dro["motor_idx"] = motor_idx
with open(r"D:\Obsidian\phase1_workspace\drosophila_structured.json", "w") as f:
    json.dump(dro, f)
print("Saved drosophila_structured.json with motor_idx")

# Now create V30 drosophila config: map drosophila subgraphs to brain regions
# vis: sensor[0:50] + inter[0:50]
# chem: sensor[50:100] + inter[50:100]  
# assoc: inter[100:250]
# motor: motor_idx[0:100]

sensors = dro["sensor_idx"]
inter_rem = inter_remaining

region_nodes = {
    "vis": sorted(sensors[:50] + inter_rem[:50]),
    "chem": sorted(sensors[50:100] + inter_rem[50:100]),
    "assoc": sorted(inter_rem[100:250]),
    "motor": sorted(motor_idx[:100]),
}

# Verify
for name, nodes in region_nodes.items():
    print(f"{name}: {len(nodes)} nodes, range [{min(nodes)}, {max(nodes)}]")

# Check overlap
all_nodes = []
for nodes in region_nodes.values():
    all_nodes.extend(nodes)
print(f"Total unique nodes across regions: {len(set(all_nodes))}")
print(f"Overlap check: {len(all_nodes)} vs {len(set(all_nodes))}")

# Build subgraph edges for each region
def extract_region_edges(all_chem, all_elec, node_set):
    """Extract edges where both src and tgt are in node_set"""
    ns = set(node_set)
    chem_out = []
    for e in all_chem:
        if e[0] in ns and e[1] in ns:
            chem_out.append(e)
    elec_out = []
    for e in all_elec:
        if e[0] in ns and e[1] in ns:
            elec_out.append(e)
    return chem_out, elec_out

region_data = {}
for name, nodes in region_nodes.items():
    chem_e, elec_e = extract_region_edges(dro["edges_chem"], dro["edges_elec"], nodes)
    # Remap node indices to 0..N-1
    node_map = {old: new for new, old in enumerate(nodes)}
    chem_remapped = [[node_map[e[0]], node_map[e[1]], e[2]] for e in chem_e]
    elec_remapped = [[node_map[e[0]], node_map[e[1]], e[2]] for e in elec_e]
    region_data[name] = {
        "N": len(nodes),
        "original_nodes": nodes,
        "edges_chem": chem_remapped,
        "edges_elec": elec_remapped,
    }
    print(f"{name}: {len(chem_remapped)} chem + {len(elec_remapped)} elec edges, N={len(nodes)}")

# Also extract cross-region edges for bonds
def extract_cross_edges(all_chem, all_elec, src_set, tgt_set):
    ss = set(src_set); ts = set(tgt_set)
    chem_out = []; elec_out = []
    for e in all_chem:
        if e[0] in ss and e[1] in ts:
            chem_out.append(e)
    for e in all_elec:
        if e[0] in ss and e[1] in ts:
            elec_out.append(e)
    return chem_out, elec_out

cross_bonds = {}
for (src_name, tgt_name) in [("vis","assoc"),("chem","assoc"),("assoc","motor"),("motor","assoc")]:
    chem_e, elec_e = extract_cross_edges(
        dro["edges_chem"], dro["edges_elec"],
        region_nodes[src_name], region_nodes[tgt_name])
    src_map = {old: new for new, old in enumerate(region_nodes[src_name])}
    tgt_map = {old: new for new, old in enumerate(region_nodes[tgt_name])}
    all_cross = []
    for e in chem_e + elec_e:
        all_cross.append([src_map[e[0]], tgt_map[e[1]], e[2]])
    cross_bonds[f"{src_name}_to_{tgt_name}"] = all_cross
    print(f"Cross {src_name}->{tgt_name}: {len(all_cross)} edges")

# Save V30 drosophila config
config = {
    "description": "V30 Drosophila connectome replacement config",
    "source": "hemibrain / flywire 800-node connectome",
    "regions": region_data,
    "cross_bonds": cross_bonds,
}
with open(r"D:\Obsidian\phase1_workspace\v30_drosophila_config.json", "w") as f:
    json.dump(config, f)
print("\nSaved v30_drosophila_config.json")
