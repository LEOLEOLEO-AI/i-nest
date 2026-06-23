import sys, json
sys.path.insert(0, r"D:\iNEST\Write\Code\MNoB")
from memai.multiscale import RenormalizationGroup, rg_flow_to_cst

rg = RenormalizationGroup(n_coarse=256, k=16, p=0.05, seed=42)
flow = rg.compute_flow(steps=5)

print("RG Flow Results:")
print("="*70)
for i, s in enumerate(flow):
    fd = s.get("fractal_dim", "N/A")
    print(f"Step {i}: N={s['n']}, C={s['C']:.4f}, L={s['L']:.2f}, sigma={s['sigma']:.2f}, d_f={fd}")

cst_data = rg_flow_to_cst(flow)
print()
print("CST Mapping:")
for d in cst_data:
    print(f"  Level {d['level']}: N={d['n']}, CST={d['cst']:.4f}")

with open("rg_flow_results.json", "w") as f:
    json.dump({"flow": flow, "cst_mapping": cst_data}, f, indent=2, default=str)
print()
print("Saved to rg_flow_results.json")
