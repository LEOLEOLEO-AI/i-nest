from pathlib import Path
from docx import Document

src = Path(r"D:\Output\Genspark\自催化闭包与自催化网络：从化学网络理论到网络时空协同复杂度涌现智能的第一性原理(2).docx")
doc = Document(src)
lines = []
for p in doc.paragraphs:
    t = p.text.strip()
    if not t:
        lines.append("")
        continue
    s = p.style.name if p.style else ""
    if "Heading 1" in s:
        lines.append(f"# {t}")
    elif "Heading 2" in s:
        lines.append(f"## {t}")
    elif "Heading 3" in s:
        lines.append(f"### {t}")
    else:
        lines.append(t)

content = "\n\n".join(lines)

front = """---
title: "自催化闭包：从化学网络到智能涌现的第一性原理"
direction: iNEST
source: "Genspark"
date: 2026-07-12
tags: [inest, first-principles, autocatalytic, emergence]
---

# 自催化闭包：从化学网络到智能涌现的第一性原理

> 来源: Genspark 创新引擎 | 方向: iNEST | 导入日期: 2026-07-12

---

"""

full = front + content
dst = Path(r"D:\Obsidian\vault\40_iNEST\41_Theory\autocatalytic_closure_emergence.md")
dst.parent.mkdir(parents=True, exist_ok=True)
dst.write_text(full, encoding="utf-8")
print(f"Saved: {dst.stat().st_size/1024:.1f}KB")
