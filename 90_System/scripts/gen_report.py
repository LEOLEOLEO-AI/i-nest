import json
from pathlib import Path

VAULT = Path(r"D:\Obsidian\vault")
data = json.loads((VAULT / "60_MOC" / "deepseek_analysis.json").read_text(encoding="utf-8"))

tcc_paper = [r for r in data["results"] if r.get("direction")=="TCC" and r.get("paper") in ("高","中")]
tcc_patent = [r for r in data["results"] if r.get("direction")=="TCC" and r.get("patent") in ("高","中")]
inest_paper = [r for r in data["results"] if r.get("direction")=="iNEST" and r.get("paper") in ("高","中")]
inest_patent = [r for r in data["results"] if r.get("direction")=="iNEST" and r.get("patent") in ("高","中")]

lines = []
lines.append("# DeepSeek V4 Pro 知识库分析报告")
lines.append("")
lines.append(f"分析篇数: {len(data['results'])} | TCC论文灵感: {len(tcc_paper)} | TCC专利灵感: {len(tcc_patent)} | iNEST论文灵感: {len(inest_paper)} | iNEST专利灵感: {len(inest_patent)}")
lines.append("")

for label, items in [("TCC 论文灵感", tcc_paper), ("TCC 专利灵感", tcc_patent),
                      ("iNEST 论文灵感", inest_paper), ("iNEST 专利灵感", inest_patent)]:
    lines.append(f"## {label} ({len(items)}篇)")
    lines.append("")
    for r in items[:25]:
        name = r.get("file", "?")
        d = r.get("direction", "?")
        pv = r.get("paper", "?")
        pt = r.get("patent", "?")
        sm = r.get("simulation", "?")
        cd = r.get("code", "?")
        lines.append(f"### {name}")
        lines.append(f"方向:{d} | 论文:{pv} | 专利:{pt} | 仿真:{sm} | 代码:{cd}")
        it = r.get("insight_tcc", "")
        ii = r.get("insight_inest", "")
        if it and it != "无直接关联":
            lines.append(f"- TCC: {it}")
        if ii and ii != "无直接关联":
            lines.append(f"- iNEST: {ii}")
        lines.append("")
    lines.append("")

report = "\n".join(lines)
(VAULT / "60_MOC" / "02_DeepSeek_Insights.md").write_text(report, encoding="utf-8")
print(f"Report saved: 60_MOC/02_DeepSeek_Insights.md")
print(f"TCC paper: {len(tcc_paper)}, TCC patent: {len(tcc_patent)}")
print(f"iNEST paper: {len(inest_paper)}, iNEST patent: {len(inest_patent)}")
