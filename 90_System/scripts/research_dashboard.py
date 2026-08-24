#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
research_dashboard.py — 科研中台看板生成器
每日自动生成 Obsidian 页面，集中展示：
  待审批提案 / 假设状态 / 跨域灵感 / 知识摄入趋势 / 概念缺口

用法: python research_dashboard.py
输出: 60_MOC/科研中台.md
"""
import json, os, re, sys
from datetime import datetime, timedelta
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
VAULT = Path(r"D:\Obsidian\vault")
META = VAULT / "99_Meta"
OUT = VAULT / "60_MOC" / "科研中台.md"
NOW = datetime.now()
TODAY = NOW.strftime("%Y-%m-%d")


def read_json(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception:
        return None


def read_text(p):
    try:
        return Path(p).read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""


def build():
    lines = []
    lines.append("---")
    lines.append("title: 科研中台")
    lines.append(f"updated: {TODAY}")
    lines.append("type: dashboard")
    lines.append("auto: research_dashboard.py")
    lines.append("---")
    lines.append("")
    lines.append("# 🔬 科研中台")
    lines.append("")
    lines.append(f"> **{TODAY}** · 自动生成于 {NOW.strftime('%H:%M')} · 审批后请勾选 ☑️")
    lines.append("")

    # ── 1. 自进化健康 ──────────────────────────────────────────
    evolog = read_json(META / "self_evolve_log.json") or []
    if evolog:
        latest = evolog[-1]
        h = latest.get("steps", {}).get("health", {})
        lines.append("## 📊 知识库健康")
        lines.append("")
        lines.append(f"| 指标 | 数值 | 来源日期 |")
        lines.append(f"|------|------|----------|")
        lines.append(f"| 笔记总数 | **{h.get('total_notes','?')}** | {h.get('date','?')} |")
        lines.append(f"| 断链 | **{h.get('broken_links','?')}** | |")
        lines.append(f"| 孤儿 | **{h.get('orphan_notes','?')}** | |")
        lines.append(f"| 缺FM | **{h.get('missing_frontmatter','?')}** | |")
        lines.append("")

        # 趋势 sparkline (近7天)
        recent = [e for e in evolog if e.get("steps", {}).get("health")]
        if len(recent) >= 2:
            lines.append("| 日期 | 笔记 | 断链 | 孤儿 | 缺FM |")
            lines.append("|------|------|------|------|------|")
            for e in recent[-7:]:
                hh = e["steps"]["health"]
                d = hh.get("date", "?")
                lines.append(f"| {d} | {hh.get('total_notes','?')} | {hh.get('broken_links','?')} | {hh.get('orphan_notes','?')} | {hh.get('missing_frontmatter','?')} |")
            lines.append("")

    # ── 2. 待审批提案 ──────────────────────────────────────────
    prop_dir = META / "evolution_proposals"
    if prop_dir.exists():
        props = sorted(prop_dir.glob("*.md"), reverse=True)[:3]
        if props:
            lines.append("## 📋 规则修订提案")
            lines.append("")
            for p in props:
                txt = read_text(p)
                approved = "✅" if "✅" in txt else "⏳"
                date_tag = p.stem
                # 提取 P0/P1 计数
                p0_count = txt.count("**P0")
                p1_count = txt.count("**P1")
                lines.append(f"- {approved} [[{p.stem}]] ({date_tag}) — P0:{p0_count} P1:{p1_count}")
            lines.append("")
            latest_prop = read_text(props[0])
            if "✅" not in latest_prop:
                lines.append(f"> ⚠️ 最新提案 [{props[0].stem}] 尚未审批，请在文件中勾选 ✅")
                lines.append("")

    # ── 3. 假设注册表 ──────────────────────────────────────────
    hyp = read_json(META / "hypothesis_registry.json")
    if hyp and hyp.get("hypotheses"):
        lines.append("## 🧬 研究假设")
        lines.append("")
        lines.append("| ID | 假设 | 状态 | 证据 |")
        lines.append("|-----|------|------|------|")
        status_icon = {"proven": "✅ 已证", "under_investigation": "🔍 验证中", "proposed": "💡 待启动"}
        for h in hyp["hypotheses"]:
            st = h.get("status", "?")
            icon = status_icon.get(st, st)
            title = h.get("title", "?")
            ev = h.get("evidence", "") or "—"
            lines.append(f"| {h.get('id','?')} | {title} | {icon} | {ev} |")
        lines.append("")

    # ── 4. 跨域桥接（研究灵感） ────────────────────────────────
    bridge_file = VAULT / "wiki" / "cross_domain_insights.md"
    bt = read_text(bridge_file)
    bridges = []
    for m in re.finditer(r"### (\S+)\s*\(Strength: (\d+)\)\s*\n(.+?)\n", bt):
        bridges.append({"name": m.group(1), "strength": int(m.group(2)), "desc": m.group(3).strip()})
    if bridges:
        lines.append("## 💡 跨域桥接（按强度排序）")
        lines.append("")
        lines.append("| 桥接 | 强度 | 描述 |")
        lines.append("|------|------|------|")
        for b in sorted(bridges, key=lambda x: -x["strength"])[:7]:
            name = b["name"].replace("_", " ")
            lines.append(f"| {name} | **{b['strength']}** | {b['desc'][:80]} |")
        lines.append("")

    # ── 5. 概念缺口 Top10 ────────────────────────────────────
    health_md = read_text(META / "vault_health.md")
    gaps = re.findall(r"×(\d+)\) `\[\[(.+?)\]\]`", health_md)
    if gaps:
        lines.append("## 🔗 高频缺失概念 Top 10")
        lines.append("")
        lines.append("> 被引用最多但尚无定义的概念——优先人工补全定义")
        lines.append("")
        lines.append("| 引用次数 | 概念 | 状态 |")
        lines.append("|----------|------|------|")
        cpt_dir = VAULT / "wiki" / "concepts"
        for count, name in gaps[:10]:
            stub_exists = (cpt_dir / f"{name}.md").exists()
            has_content = False
            if stub_exists:
                stub_text = read_text(cpt_dir / f"{name}.md")
                has_content = len(stub_text) > 300 and "占位概念" not in stub_text
            status = "📝 有内容" if has_content else ("🫥 占位stub" if stub_exists else "❌ 不存在")
            lines.append(f"| ×{count} | [[{name}]] | {status} |")
        lines.append("")

    # ── 6. 快速操作 ──────────────────────────────────────────
    lines.append("---")
    lines.append("")
    lines.append("## ⚡ 快速操作")
    lines.append("")
    lines.append("- 审批提案 → 打开 `99_Meta/evolution_proposals/` 中最新文件，在 P0/P1 行后加 ✅")
    lines.append("- 补概念定义 → 打开 `wiki/concepts/` 中的 stub，替换 `> 由 self_evolve 自动生成` 为真实定义")
    lines.append("- 手动触发自进化 → 终端执行 `python D:\\Obsidian\\vault\\90_System\\scripts\\self_evolve.py`")
    lines.append("- 检查同步健康 → 终端执行 `powershell -File D:\\Obsidian\\scripts\\check_sync_health.ps1`")
    lines.append("")
    lines.append("---")
    lines.append(f"*由 research_dashboard.py 自动生成 · {NOW.isoformat()}*")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"[research_dashboard] 写入: {OUT}")


if __name__ == "__main__":
    build()
