# -*- coding: utf-8 -*-
"""Process 10_Inbox: classify by keyword + move to TCC/iNEST"""

import shutil, re
from pathlib import Path
from datetime import datetime

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
INBOX = VAULT / "10_Inbox"

TCC_KW = ["tcc","wafer","sdsow","晶圆","chiplet","互联","pcie","存算一体","算力",
          "交换","路由","封装","2.5d","3dic","ccu","微纳电子","先进计算",
          "拓扑中心","晶上","并行计算","数据中心","noc","sdi","交换机"]
INEST_KW = ["inest","神经","类脑","涌现","意识","大脑","brain","脉冲","spiking",
            "突触","synapse","神经元","neuromorphic","认知","cognitive",
            "复杂度","complexity","临界","分形","fractal","介观","liquid","pnn"]

def classify(filename, content):
    text = (filename + " " + content[:1000]).lower()
    t = sum(1 for kw in TCC_KW if kw in text)
    i = sum(1 for kw in INEST_KW if kw in text)
    if t > i: return "TCC"
    if i > t: return "iNEST"
    return "TCC"  # default

processed = 0
skipped = 0

for f in list(INBOX.rglob("*.md")):
    try:
        content = f.read_text(encoding="utf-8", errors="ignore")
    except:
        continue
    
    # Skip stubs and dedup markers
    if len(content) < 100 or "可能重复" in content:
        skipped += 1
        continue
    
    cls = classify(f.name, content)
    
    if cls == "TCC":
        dst = VAULT / "30_TCC" / "32_Tech" / f.name
    else:
        dst = VAULT / "40_iNEST" / "42_Tech" / f.name
    
    if dst.exists():
        # Add suffix
        dst = dst.with_name(f"{dst.stem}_inbox{dst.suffix}")
    
    shutil.move(str(f), str(dst))
    processed += 1

# Clean empty dirs
for d in sorted(INBOX.rglob("*"), reverse=True):
    if d.is_dir() and not list(d.iterdir()):
        d.rmdir()

print(f"[{datetime.now().strftime('%H:%M:%S')}] Inbox processed: {processed} moved, {skipped} skipped")
print(f"TCC: 30_TCC/32_Tech, iNEST: 40_iNEST/42_Tech")
