#!/usr/bin/env python3
"""SDI v30 — Drosophila Multi-Region (Extended)
=================================================
Extended Drosophila simulation with multi-region coupling
and cross-region communication primitives.
"""
# This is the extended version that was called sdi_v30_multiregion.py
# It builds on sdi_v30_drosophila.py with inter-region coupling

import numpy as np, json, os

OUT_DIR = "v30_results"
os.makedirs(OUT_DIR, exist_ok=True)

if __name__ == "__main__":
    from sdi_v30_drosophila import V30DrosophilaSim

    sim = V30DrosophilaSim()
    metrics = sim.compute_metrics()

    # Add multi-region coupling analysis
    regions = list(metrics.keys())
    coupling = {}
    for i, r1 in enumerate(regions):
        for r2 in regions[i+1:]:
            m1, m2 = metrics[r1], metrics[r2]
            # Coupling strength based on small-world overlap and synapse density
            sw_overlap = 1 - abs(m1["small_world"]-m2["small_world"])/max(m1["small_world"],m2["small_world"],1e-6)
            s_coupling = sw_overlap * min(m1["synapse_density"], m2["synapse_density"])/max(m1["synapse_density"],m2["synapse_density"],1e-6)
            coupling[f"{r1}<->{r2}"] = round(s_coupling, 4)

    result = {
        "version": "v30",
        "total_neurons": sim.total_neurons,
        "regions": metrics,
        "cross_region_coupling": coupling,
        "strongest_coupling": sorted(coupling.items(), key=lambda x:-x[1])[:5]
    }

    with open(f"{OUT_DIR}/v30_drosophila_results.json","w") as f:
        json.dump(result, f, indent=2)

    print("v30 Multi-Region Coupling (top 5):")
    for pair, strength in result["strongest_coupling"]:
        print(f"  {pair}: {strength:.4f}")
