"""Audit C. elegans structural and functional inputs for V-CST.

This script reports provenance and schema only. It never fabricates missing
functional time series and never treats derived result tables as activity data.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ACTIVITY_HINTS = ("activity", "calcium", "fluorescence", "timeseries", "time_series", "functional")
STRUCTURAL_HINTS = ("connectome", "neuronconnect", "edge", "adjacency", "herm")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def classify(path: Path) -> str:
    name = path.name.lower()
    if any(token in name for token in ACTIVITY_HINTS):
        return "activity_candidate"
    if any(token in name for token in STRUCTURAL_HINTS):
        return "structural_candidate"
    return "other"


def inspect_json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {"json": False}
    if isinstance(value, dict):
        return {"json": True, "root": "object", "keys": sorted(value.keys())}
    return {"json": True, "root": type(value).__name__}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    records = []
    for path in sorted(args.root.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in {".json", ".csv", ".tsv", ".npy", ".npz", ".mat", ".h5", ".hdf5", ".xls", ".xlsx"}:
            continue
        record = {
            "path": str(path),
            "size_bytes": path.stat().st_size,
            "sha256": sha256(path),
            "classification": classify(path),
        }
        if path.suffix.lower() == ".json":
            record.update(inspect_json(path))
        records.append(record)

    activity = [record for record in records if record["classification"] == "activity_candidate"]
    structural = [record for record in records if record["classification"] == "structural_candidate"]
    result = {
        "protocol": "V-CST-00",
        "task": "V-CST-01/V-CST-02 input audit",
        "root": str(args.root),
        "records": records,
        "summary": {
            "structural_candidates": len(structural),
            "activity_name_candidates": len(activity),
            "raw_neuron_id_by_time_series_verified": False,
            "Tc_status": "NOT_EXECUTED",
            "Gamma_st_status": "NOT_EXECUTED",
            "CST_status": "NOT_EXECUTED",
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

