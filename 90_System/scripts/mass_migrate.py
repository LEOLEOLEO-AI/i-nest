# -*- coding: utf-8 -*-
import shutil
from pathlib import Path

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")

TCC_KW = ["tcc", "topology", "wafer", "sdsow", "chiplet", "2.5d", "3dic",
          "pcie", "ccu", "sdi", "marvell", "interconnect", "packaging",
          "switch", "router", "network-on-chip", "noc", "cst_"]

INEST_KW = ["inest", "neuromorphic", "spiking", "synapse", "brain",
            "cognitive", "consciousness", "hnn", "fractal", "criticality",
            "complexity", "emergence", "neuron", "hamiltonian"]

def classify(name):
    n = name.lower()
    t = sum(1 for k in TCC_KW if k in n)
    i = sum(1 for k in INEST_KW if k in n)
    if t > i: return "tcc"
    if i > t: return "inest"
    return "ambig"

def get_subdir(cls, name):
    n = name.lower()
    for k, sub in [("theory", "31_Theory"), ("tech", "32_Tech"),
                   ("dev", "33_Dev"), ("project", "34_Projects"), ("sim", "35_Simulation")]:
        if k in n:
            return sub.replace("3", "4") if cls == "inest" else sub
    return "41_Theory" if cls == "inest" else "31_Theory"

# Ensure targets exist
for t in ["20_Processing/21_TCC", "20_Processing/22_iNEST"]:
    (VAULT / t).mkdir(parents=True, exist_ok=True)

for base in ["30_TCC", "40_iNEST"]:
    for sub in ["31_Theory", "32_Tech", "33_Dev", "34_Projects", "35_Simulation"]:
        (VAULT / base / sub).mkdir(parents=True, exist_ok=True)

SOURCES = [
    "10_Knowledge", "00_KnowledgeBase_知识库", "05_Fleeting", "MEMORY",
    "01_Concepts", "03_Projects", "20_Projects", "Projects",
    "TCC计算范式", "智能涌现范式",
    "iNEST_HW_Engineering", "iNEST_Sim_Research", "sdi_sim",
    "NCC_IP_Portfolio", "Inbox", "30_Outputs",
    "KB", "knowledge", "scripts", "灵感库",
]

stats = {"tcc": 0, "inest": 0, "ambig": 0}
errors = []

for src_name in SOURCES:
    src_dir = VAULT / src_name
    if not src_dir.exists():
        continue
    for f in list(src_dir.rglob("*.md")):
        try:
            rel = f.relative_to(src_dir)
            cls = classify(str(rel))
            sub = get_subdir(cls, str(rel))
            if cls == "tcc":
                dst_base = VAULT / "30_TCC" / sub
            elif cls == "inest":
                dst_base = VAULT / "40_iNEST" / sub
            else:
                dst_base = VAULT / "20_Processing" / "21_TCC"
            dst = dst_base / rel.parent if rel.parent != Path(".") else dst_base
            dst.mkdir(parents=True, exist_ok=True)
            tf = dst / f.name
            if not tf.exists():
                shutil.move(str(f), str(tf))
                stats[cls] += 1
        except Exception as e:
            errors.append(f"{src_name}/{rel}: {e}")

print(f"TCC: {stats['tcc']} | iNEST: {stats['inest']} | Ambiguous: {stats['ambig']}")
if errors:
    print(f"Errors: {len(errors)}")
    for e in errors[:10]:
        print(f"  {e}")

# Show remaining
for src_name in SOURCES:
    src_dir = VAULT / src_name
    if src_dir.exists():
        md = sum(1 for _ in src_dir.rglob("*.md"))
        if md > 0:
            print(f"REMAINS: {src_name} ({md} md)")
