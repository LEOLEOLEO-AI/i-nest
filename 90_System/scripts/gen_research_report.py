import json
from pathlib import Path

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
data = json.loads((VAULT / "60_MOC" / "deep_research_analysis.json").read_text(encoding="utf-8"))

lines = []
lines.append("# 🧠 TCC + iNEST 知识库深度洞察报告")
lines.append("")
lines.append(f"> DeepSeek V4 Pro 分析 | {data['timestamp']}")
lines.append(f"> 分析核心科研文档: {sum(1 for r in data['results'] if 'error' not in r and 'type' in r)} 篇")
lines.append("")

# Collect all claims, methods, data, gaps
all_claims = []
all_methods = []
all_data = []
all_gaps = []
all_steps = []

for r in data["results"]:
    if "error" in r:
        continue
    for c in r.get("theoretical_claims", []):
        all_claims.append({"claim": c.get("claim",""), "evidence": c.get("evidence",""), 
                          "confidence": c.get("confidence",""), "file": r.get("filename","")})
    for m in r.get("technical_methods", []):
        all_methods.append(m)
    for d in r.get("key_data", []):
        all_data.append(d)
    for g in r.get("gaps", []):
        all_gaps.append(g)
    for s in r.get("next_steps", []):
        all_steps.append(s)

# === Report body ===
lines.append("## 一、理论突破")
lines.append("")

for c in all_claims[:20]:
    conf_emoji = {"高": "🔴", "中": "🟡", "低": "⚪"}.get(c["confidence"], "⚪")
    lines.append(f"### {conf_emoji} {c['claim'][:100]}")
    lines.append(f"- **证据**: {c['evidence'][:200]}")
    lines.append(f"- **来源**: {c['file'][:80]}")
    lines.append("")

lines.append("## 二、技术方法积累")
lines.append("")
lines.append("| 方法 | 成熟度 |")
lines.append("|------|--------|")
for m in all_methods[:15]:
    mat = m.get("maturity", "?")
    lines.append(f"| {m.get('method','?')[:60]} | {mat} |")
lines.append("")

lines.append("## 三、客观数据沉淀")
lines.append("")
lines.append("| 数据点 | 数值 | 来源 |")
lines.append("|--------|------|------|")
for d in all_data[:20]:
    lines.append(f"| {d.get('point','?')[:50]} | {d.get('value','?')[:40]} | {d.get('source','?')[:30]} |")
lines.append("")

lines.append("## 四、知识空白（待攻克的学术问题）")
lines.append("")
for g in all_gaps[:15]:
    lines.append(f"- [ ] {g}")
lines.append("")

lines.append("## 五、下一步研究建议")
lines.append("")
for s in all_steps[:15]:
    lines.append(f"- {s}")
lines.append("")

lines.append("## 六、逐文件分析结果")
lines.append("")
for r in data["results"]:
    if "error" in r:
        lines.append(f"### ⚠️ {r.get('file','?').split('/')[-1][:60]}")
        lines.append(f"*解析错误: {r['error'][:100]}*")
    else:
        lines.append(f"### {r.get('filename','?')[:60]}")
        lines.append(f"- 方向: {r.get('direction','?')} | 类型: {r.get('type','?')}")
        lines.append(f"- 摘要: {r.get('summary','')[:200]}")
    lines.append("")

lines.append("---")
lines.append(f"> 此报告基于知识库中原始研究文档的DeepSeek深度分析生成，可反哺知识库持续迭代。")

report = "\n".join(lines)
(VAULT / "60_MOC" / "02_Research_Insights.md").write_text(report, encoding="utf-8")
print(f"Report: 60_MOC/02_Research_Insights.md ({len(lines)} lines)")
print(f"Claims: {len(all_claims)}, Methods: {len(all_methods)}, Data: {len(all_data)}")
print(f"Gaps: {len(all_gaps)}, Next steps: {len(all_steps)}")
