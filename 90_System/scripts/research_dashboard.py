#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
research_dashboard.py v2 — 创新导航引擎
不是状态报表，而是回答三个问题：
  1. 我今天该做什么？
  2. 我的假设离发表还有多远？
  3. 本周最值得投入的创新方向是什么？
"""
import json, re, sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
VAULT = Path(r"D:\Obsidian\vault")
META = VAULT / "99_Meta"
OUT = VAULT / "60_MOC" / "科研中台.md"
NOW = datetime.now()
TODAY = NOW.strftime("%Y-%m-%d")

STATUS_MAP = {
    "proven": ("✅", "已证", "写论文！"),
    "under_investigation": ("🔍", "验证中", "补充实验证据"),
    "proposed": ("💡", "待启动", "设计验证方案"),
}

def read_json(p):
    try: return json.loads(Path(p).read_text(encoding="utf-8"))
    except: return None

def read_text(p):
    try: return Path(p).read_text(encoding="utf-8", errors="ignore")
    except: return ""

# ── 数据采集 ──────────────────────────────────────────────
evolog = read_json(META / "self_evolve_log.json") or []
hyps = (read_json(META / "hypothesis_registry.json") or {}).get("hypotheses", [])
health_txt = read_text(META / "vault_health.md")
bridge_txt = read_text(VAULT / "wiki" / "cross_domain_insights.md")
scan = read_json(META / "concept_scan.json") or {}

latest_h = evolog[-1].get("steps", {}).get("health", {}) if evolog else {}
recent_health = [e["steps"]["health"] for e in evolog if e.get("steps", {}).get("health")][-7:]

bridges = []
for m in re.finditer(r"### (\S+)\s*\(Strength: (\d+)\)\s*\n(.+?)\n", bridge_txt):
    bridges.append({"name": m.group(1), "strength": int(m.group(2)), "desc": m.group(3).strip()})
bridges.sort(key=lambda x: -x["strength"])

gaps = re.findall(r"×(\d+)\) `\[\[(.+?)\]\]`", health_txt)
cpt_dir = VAULT / "wiki" / "concepts"
concept_gaps = []
for count_str, name in gaps[:20]:
    count = int(count_str)
    f = cpt_dir / f"{name}.md"
    if f.exists():
        txt = f.read_text(encoding="utf-8", errors="ignore")
        is_stub = len(txt) < 300 or "占位概念" in txt
    else:
        is_stub = True
    concept_gaps.append({"name": name, "count": count, "needs_work": is_stub})

sim_scripts = list((VAULT / "90_System" / "scripts").glob("sdi_network_v*.py"))
latest_sim = max(sim_scripts, key=lambda p: p.stat().st_mtime).stem if sim_scripts else "无"

# ── 行动推导 ──────────────────────────────────────────────
actions = []

for h in hyps:
    st = h.get("status", "")
    hid = h.get("id", "")
    title = h.get("title", "")
    icon, label, next_step = STATUS_MAP.get(st, ("?", st, ""))
    
    if st == "proven":
        actions.append({
            "priority": 1, "time": "30min",
            "what": f"**{hid} 已证明 → 写论文！**",
            "why": f"{title} · 这是你最强的理论基础",
            "how": f"打开 `50_Output/51_Papers/` 创建论文大纲，以 {hid} 为核心论点",
        })
    elif st == "proposed" and h.get("source_bridge"):
        src = h.get("source_bridge", "")
        b = next((x for x in bridges if x["name"] == src), None)
        strength = b["strength"] if b else 0
        test = h.get("test_method", "")
        if test and strength > 100:
            actions.append({
                "priority": 2 if strength > 300 else 3,
                "time": "2-4h" if "仿真" in test.lower() else "30min",
                "what": f"**{hid}: {title[:60]}**",
                "why": f"来自跨域桥接 {src} (强度{strength}) | {next_step}",
                "how": test,
            })

top_gaps = [g for g in concept_gaps if g["needs_work"]][:3]
if top_gaps:
    gap_names = ", ".join(f"[[{g['name']}]]" for g in top_gaps[:3])
    actions.append({
        "priority": 2, "time": "15min/个",
        "what": f"补全高频概念定义: {gap_names}",
        "why": f"被引 {', '.join('×'+str(g['count']) for g in top_gaps)} 但仍是空壳，阻塞假设推进",
        "how": "打开 wiki/concepts/ 对应文件，写50字定义 + 2-3个关键引用",
    })

actions.sort(key=lambda a: a["priority"])

# ── 输出生成 ──────────────────────────────────────────────
L = []
L.append("---")
L.append("title: 创新导航")
L.append(f"updated: {TODAY}")
L.append("type: navigation")
L.append("---")
L.append("")
L.append("# 🧭 创新导航")
L.append("")
L.append(f"> **{NOW.strftime('%Y-%m-%d %H:%M')}** · 不是报表，是你的研究GPS")
L.append("")

# ═══ 今日行动 ════════════════════════════════════════════
L.append("## ⚡ 今天该做什么")
L.append("")
if actions:
    for i, a in enumerate(actions[:5], 1):
        icon = ["🥇","🥈","🥉","4️⃣","5️⃣"][i-1]
        L.append(f"### {icon} {a['what']}")
        L.append("")
        L.append(f"- **为什么**: {a['why']}")
        L.append(f"- **怎么做**: {a['how']}")
        L.append(f"- **预计时间**: {a['time']}")
        L.append("")
else:
    L.append("*暂无行动建议，检查假设注册表和跨域桥接。*")
    L.append("")

# ═══ 假设进展 ════════════════════════════════════════════
L.append("## 🔬 假设进展")
L.append("")
L.append("| ID | 假设 | 状态 | 下一步 | 发表潜力 |")
L.append("|-----|------|------|--------|----------|")

for h in hyps:
    st = h.get("status", "")
    hid = h.get("id", "?")
    title = h.get("title", "?")
    short = title[:55] + "..." if len(title) > 55 else title
    icon, label, next_s = STATUS_MAP.get(st, ("❓", st, "?"))
    
    potential = "—"
    if st == "proven":
        potential = "🔥 立即写论文"
    elif st == "under_investigation":
        potential = "⚡ 补充实验"
    elif st == "proposed":
        src = h.get("source_bridge", "")
        b = next((x for x in bridges if x["name"] == src), None)
        if b and b["strength"] > 400:
            potential = "⭐⭐ 高优先"
        elif b and b["strength"] > 100:
            potential = "⭐ 中等"
        else:
            potential = "💭 观察"
    
    L.append(f"| {hid} | {short} | {icon} {label} | {next_s} | {potential} |")

L.append("")

# ═══ 最高价值创新方向 ════════════════════════════════════
L.append("## 💡 本周最有价值的创新方向")
L.append("")
if bridges:
    for i, b in enumerate(bridges[:3]):
        icon = ["🥇", "🥈", "🥉"][i]
        name_pretty = b["name"].replace("_", " ")
        related = [h for h in hyps if h.get("source_bridge") == b["name"]]
        hyp_ref = f" → {related[0]['id']}" if related else ""
        
        L.append(f"### {icon} {name_pretty} (强度 {b['strength']}){hyp_ref}")
        L.append("")
        L.append(f"> {b['desc'][:120]}")
        L.append("")
        if related:
            h = related[0]
            L.append(f"- **验证方法**: {h.get('test_method', '待定')}")
            L.append(f"- **已有基础**: {h.get('evidence', '—')}")
            L.append(f"- **下一步**: {STATUS_MAP.get(h.get('status',''), ('','',''))[2]}")
        L.append("")
else:
    L.append("*无桥接数据。*")
    L.append("")

# ═══ 概念缺口 ════════════════════════════════════════════
L.append("## 📝 概念路障（每补一个，假设前进一步）")
L.append("")
gap_reasons = {
    "advanced packaging": "H6 Chiplet 忆阻器前置",
    "heterogeneous integration": "H6/H9 核心",
    "catastrophic forgetting": "H2 涌现挑战",
    "memristor device": "H6 硬件基础",
    "intelligence emergence": "iNEST 理论基石",
    "scaling laws": "晶上系统评估工具",
    "soc": "H2 缩写",
    "HebbianLimitCycleLearning": "学习规则×动力学",
    "Neuromorphic_Substrate": "所有 iNEST 载体",
    "EventDrivenAttention": "H7 认知基础",
}
if concept_gaps:
    L.append("| 概念 | 被引 | 关联 |")
    L.append("|------|------|------|")
    for g in concept_gaps[:8]:
        reason = gap_reasons.get(g["name"], "")
        L.append(f"| [[{g['name']}]] | ×{g['count']} | {reason} |")
    L.append("")

# ═══ 基础设施 ════════════════════════════════════════════
L.append("---")
L.append("")
L.append("<details><summary>🛠 基础设施状态</summary>")
L.append("")
L.append(f"- 仿真框架: {'✅ ' + latest_sim if sim_scripts else '❌'}")
L.append("- LLM: ✅ deepseek-v4-pro (本地代理)")
L.append("- arXiv: ⚠️ 429 (需VPN)")
L.append("- Git: ✅ bat+Start-Process")
L.append("")
L.append("</details>")
L.append("")
L.append("---")
L.append(f"*创新导航引擎 v2 · {NOW.isoformat()}*")

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(L), encoding="utf-8")
print(f"[innovation_navigator] 写入: {OUT}")
