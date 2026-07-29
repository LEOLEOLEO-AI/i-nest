"""Compute the structural CST component from the frozen C. elegans graph.

The script intentionally computes only Sc. Tc, Gamma_st and CST are refused
until a verified neuron-ID-by-time functional recording is supplied.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def edge_triplet(edge):
    if isinstance(edge, dict) and "value" in edge:
        return edge["value"]
    return edge


def directed_edges(data):
    edges = []
    for raw in data["edges_chem"]:
        triplet = edge_triplet(raw)
        if len(triplet) >= 2:
            source, target = int(triplet[0]), int(triplet[1])
            weight = float(triplet[2]) if len(triplet) > 2 else 1.0
            edges.append((source, target, weight))
    return edges


def directed_core_fraction(n, edges):
    indegree = [0] * n
    outdegree = [0] * n
    for source, target, _ in edges:
        outdegree[source] += 1
        indegree[target] += 1
    active = sum(1 for i in range(n) if indegree[i] > 0 and outdegree[i] > 0)
    return active / n if n else float("nan")


def path_efficiency(n, edges):
    adjacency = [[] for _ in range(n)]
    for source, target, _ in edges:
        adjacency[source].append(target)
    total = 0.0
    pairs = 0
    for source in range(n):
        distance = [-1] * n
        distance[source] = 0
        queue = [source]
        for node in queue:
            for target in adjacency[node]:
                if distance[target] < 0:
                    distance[target] = distance[node] + 1
                    queue.append(target)
        for target in range(n):
            if target != source and distance[target] > 0:
                total += 1.0 / distance[target]
                pairs += 1
    return total / pairs if pairs else float("nan")


def undirected_modularity_proxy(n, edges):
    # Deterministic component proxy: fraction of edges internal to weakly
    # connected components. It is explicitly not called Louvain modularity.
    adjacency = [[] for _ in range(n)]
    for source, target, _ in edges:
        adjacency[source].append(target)
        adjacency[target].append(source)
    component = [-1] * n
    count = 0
    for root in range(n):
        if component[root] >= 0:
            continue
        component[root] = count
        queue = [root]
        for node in queue:
            for target in adjacency[node]:
                if component[target] < 0:
                    component[target] = count
                    queue.append(target)
        count += 1
    internal = sum(1 for source, target, _ in edges if component[source] == component[target])
    return internal / len(edges) if edges else float("nan")


def reciprocal_cycle_fraction(n, edges):
    pairs = {(source, target) for source, target, _ in edges if source != target}
    reciprocal = sum(1 for source, target in pairs if (target, source) in pairs)
    return reciprocal / len(pairs) if pairs else float("nan")


def geometric_mean(values):
    if any(not math.isfinite(value) or value <= 0 for value in values):
        return float("nan")
    return math.prod(values) ** (1.0 / len(values))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--connectome", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    data = json.loads(args.connectome.read_text(encoding="utf-8"))
    n = int(data["N"])
    edges = directed_edges(data)
    components = {
        "kappa_0_directed_core_fraction": directed_core_fraction(n, edges),
        "kappa_1_directed_path_efficiency": path_efficiency(n, edges),
        "kappa_2_modularity_proxy_not_louvain": undirected_modularity_proxy(n, edges),
        "kappa_top_reciprocal_cycle_proxy": reciprocal_cycle_fraction(n, edges),
    }
    sc = geometric_mean(list(components.values()))
    result = {
        "protocol": "V-CST-00",
        "task": "V-CST-01",
        "status": "PARTIAL_Sc_ONLY",
        "evidence": "[推导] from [实测/引用] structural file; source provenance must be attached separately",
        "connectome": str(args.connectome),
        "connectome_sha256": sha256(args.connectome),
        "N": n,
        "directed_chemical_edge_records": len(edges),
        "components": components,
        "Sc": sc,
        "Tc": "NOT_EXECUTED",
        "Gamma_st": "NOT_EXECUTED",
        "alpha": "NOT_EXECUTED",
        "CST": "NOT_EXECUTED",
        "quality_gate": {
            "all_v2_1_components_implemented": False,
            "functional_time_series_verified": False,
            "louvain_kappa_2_verified": False,
            "biological_cst_claim_allowed": False,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

