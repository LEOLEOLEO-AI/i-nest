# -*- coding: utf-8 -*-
"""toolchain_demo.py — 8 tools auto-chained demo
Run: python toolchain_demo.py
Codex trigger: "toolchain demo"
"""
import numpy as np, time, json, os
print("=" * 60)
print("  TCC + iNEST + CST Toolchain Demo")
print("=" * 60)
OUT = "D:/Obsidian/home/work/.openclaw/workspace/99_Meta/toolchain_demo_output"
os.makedirs(OUT, exist_ok=True)
results = {}

# Step 1: networkx
t0 = time.time()
import networkx as nx
G_ws = nx.watts_strogatz_graph(n=1000, k=8, p=0.1)
results["nx"] = {
    "ws_clustering": float(nx.average_clustering(G_ws)),
    "ws_pathlen": float(nx.average_shortest_path_length(G_ws)),
    "sec": round(time.time()-t0, 2)
}
print(f"[1/8] networkx: clustering={results['nx']['ws_clustering']:.3f}, path_len={results['nx']['ws_pathlen']:.2f}")

# Step 2: igraph (networkx -> igraph)
t0 = time.time()
import igraph as ig
g_ws = ig.Graph.from_networkx(G_ws)
results["igraph"] = {
    "modularity": g_ws.community_leiden().modularity,
    "communities": len(g_ws.community_leiden()),
    "sec": round(time.time()-t0, 2)
}
print(f"[2/8] igraph: modularity={results['igraph']['modularity']:.3f}, communities={results['igraph']['communities']}")

# Step 3: PyG (networkx -> PyG)
t0 = time.time()
import torch, torch_geometric
from torch_geometric.data import Data
from torch_geometric.nn import GCNConv
edge_index = torch.tensor(list(G_ws.edges())).t().contiguous()
x = torch.ones((G_ws.number_of_nodes(), 16))
data = Data(x=x, edge_index=edge_index)
class GCN(torch.nn.Module):
    def __init__(self): super().__init__(); self.c1 = GCNConv(16, 32); self.c2 = GCNConv(32, 1)
    def forward(self, d): return self.c2(self.c1(d.x, d.edge_index).relu(), d.edge_index)
model = GCN(); model.eval()
with torch.no_grad(): pred = model(data)
results["pyg"] = {"mean": float(pred.mean()), "std": float(pred.std()), "sec": round(time.time()-t0, 2)}
print(f"[3/8] PyG: GNN mean={results['pyg']['mean']:.4f}")

# Step 4: brian2
t0 = time.time()
from brian2 import *
start_scope()
Nn = 500
eqs = """
dv/dt = (0.04*v**2 + 5*v + 140 - u + I)/ms : 1
du/dt = a*(b*v - u)/ms                         : 1
a                                               : 1
b                                               : 1
c                                               : 1
d                                               : 1
I                                               : 1
"""
G = NeuronGroup(Nn, eqs, threshold='v>=30', reset='v=c; u+=d', method='euler')
G.a = 0.02; G.b = 0.2; G.c = -65; G.d = 8; G.I = 10; G.v = -65; G.u = G.b*G.v
sm = SpikeMonitor(G); run(100*ms)
active = int(sum(sm.count > 0))
results["brian2"] = {"neurons": Nn, "fired": active, "total_spikes": int(sum(sm.count)), "sec": round(time.time()-t0, 2)}
print(f"[4/8] brian2: {Nn} neurons, {active} fired, {results['brian2']['total_spikes']} spikes")

# Step 5: snntorch (brian2 -> snntorch)
t0 = time.time()
spike_array = np.zeros((Nn, 100))
for i, ta in sm.spike_trains().items():
    for t in ta:
        bi = int(t/ms)
        if bi < 100: spike_array[i, bi] = 1
import snntorch as snn
from snntorch import spikegen
spike_tensor = torch.from_numpy(spike_array).float()
rate_enc = spikegen.rate(spike_tensor[:100, :], time_var_input=True)
results["snntorch"] = {"rate": float(rate_enc.mean()), "sec": round(time.time()-t0, 2)}
print(f"[5/8] snntorch: spike_rate={results['snntorch']['rate']:.3f}")

# Step 6: snngrow
t0 = time.time()
from snngrow.base import SpikeTensor
# snngrow: byte-level spike tensor optimization (ByteDance SNN toolkit)
st_data = torch.randint(0, 2, (100, 500, 10), dtype=torch.bool)
st = SpikeTensor(st_data)
results["snngrow"] = {"shape": str(tuple(st_data.shape)), "sparsity": float(st_data.float().mean()), "sec": round(time.time()-t0, 2)}
print(f"[6/8] snngrow: SpikeTensor {results['snngrow']['shape']} sparsity={results['snngrow']['sparsity']:.2%}")

# Step 7: PySpike (brian2 -> PySpike)
t0 = time.time()
import pyspike as spk
pts = []
for ta in list(sm.spike_trains().values())[:100]:
    pts.append(spk.SpikeTrain(ta/ms, [0, 100]))
if len(pts) >= 2:
    isi = spk.isi_distance(pts[0], pts[1])
    sd = spk.spike_distance(pts[0], pts[1])
    ss = spk.spike_sync(pts[:50])
else: isi = sd = ss = 0
results["pyspike"] = {"isi": round(isi,4), "spike_dist": round(sd,4), "sync": round(ss,4), "sec": round(time.time()-t0, 2)}
print(f"[7/8] PySpike: ISI={isi:.4f}, SpikeDist={sd:.4f}, Sync={ss:.4f}")

# Step 8: reservoirpy (snngrow -> reservoirpy)
t0 = time.time()
import reservoirpy as rpy
res = rpy.nodes.Reservoir(500, sr=0.9, lr=0.5, input_scaling=0.1)
ro = rpy.nodes.Ridge(ridge=1e-6, output_dim=1)
mrp = res >> ro
X = np.random.randn(10, 500)
Y = np.random.randn(10, 1)
mrp.fit(X, Y)
rpo = mrp.run(X)
results["reservoirpy"] = {"out_mean": float(np.mean(rpo)), "out_std": float(np.std(rpo)), "sec": round(time.time()-t0, 2)}
print(f"[8/8] reservoirpy: output_mean={results['reservoirpy']['out_mean']:.4f}")

# Summary
total = sum(v["sec"] for v in results.values())
results["_total_sec"] = round(total, 1)
with open(OUT+"/results.json", "w") as f: json.dump(results, f, indent=2, default=str)
print()
print("=" * 60)
print(f"  8/8 tools auto-chained | Total: {results['_total_sec']}s")
print(f"  Results: {OUT}/results.json")
print("=" * 60)
