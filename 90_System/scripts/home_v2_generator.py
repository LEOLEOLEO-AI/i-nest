#!/usr/bin/env python3
"""Generate a readable, evidence-aware research home page."""
import json
import subprocess
from datetime import datetime
from pathlib import Path

VAULT = Path(r"D:\Obsidian\vault")

def count(folder):
    path = VAULT / folder
    return len(list(path.rglob("*.md"))) if path.exists() else 0

def load_json(path, default):
    try:
        return json.loads((VAULT / path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return default

def git_count():
    try:
        result = subprocess.run(["git", "-C", str(VAULT), "status", "--porcelain"], capture_output=True, text=True, timeout=20)
        return len([line for line in result.stdout.splitlines() if line.strip()])
    except Exception:
        return -1

def link(path, label=None):
    return f"[[{path}|{label or Path(path).stem}]]"

def generate():
    today = datetime.now().strftime("%Y-%m-%d")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    state = load_json("99_Meta/research_state.json", {})
    review = load_json("99_Meta/knowledge_compile_state.json", {"items": []})
    proposals = load_json("99_Meta/research_task_proposals.json", {"items": []})
    vault = state.get("vault", {})
    pending = [item for item in proposals.get("items", []) if item.get("status") == "pending_review" and not item.get("title", "").lower().startswith("review for relevance")]
    review_items = review.get("items", [])[:8]
    lines = ["---", "cssclass: research-home", "type: research-control-center", f"updated: {today}", "---", "", "# TCC · iNEST 研发中枢", "", f"> 更新时间：{now}  |  Git 未提交：{git_count()}  |  外部洞察：待确认 {len(review_items)} 条", "", "## 今日总览", "", "| 维度 | 当前数量 | 入口 |", "|---|---:|---|"]
    lines += [f"| 知识库 Markdown | {vault.get('total_md', count('')):,} | {link('60_MOC/00_Processing_Pending_Review', '健康与待复核')} |", f"| TCC 知识 | {vault.get('tcc_30', count('30_TCC')):,} | {link('30_TCC/TCC_Master_Index', 'TCC 总索引')} |", f"| iNEST 知识 | {vault.get('inest_40', count('40_iNEST')):,} | {link('40_iNEST/iNEST_Master_Index', 'iNEST 总索引')} |", f"| Processing | {vault.get('processing_20', count('20_Processing')):,} | {link('20_Processing', '处理中')} |", f"| 论文/专利/代码/指南 | {vault.get('output_50', count('50_Output')):,} | {link('50_Output', '成果区')} |", "", "## 研发主线", "", "| 方向 | 理论攻关 | 技术研究 | 工程落地 | 成果出口 |", "|---|---|---|---|---|", f"| TCC | {link('30_TCC/31_Theory', '拓扑中心计算与 R/T/C 基线')} | {link('30_TCC/32_Technology', 'SDI / Chiplet / OneFabric')} | {link('30_TCC/33_Engineering', 'RTL / CST / 原型')} | {link('50_Output/51_Papers/00_Paper_Versions_Index', '论文版本总表')} |", f"| iNEST | {link('40_iNEST/41_Theory', '复杂网络与涌现智能')} | {link('40_iNEST/42_Technology', 'SNN / 器件 / 学习规则')} | {link('40_iNEST/43_Engineering', '仿真与工程实现')} | {link('50_Output/51_Papers/00_Paper_Versions_Index', '论文版本总表')} |", "", "## 外部知识编译待确认", "", "> 这些条目是外部资料的处理结果，不是团队原创成果；确认前不会进入正式任务计划或成果统计。", ""]
    if review_items:
        lines += ["| 条目 | 方向 | 证据 | 下一步 |", "|---|---|---|---|"]
        for index, item in enumerate(review_items, 1):
            title = item.get("title", "未命名")[:70]
            action = "；".join(item.get("candidate_actions", []))[:100] or "人工确认具体行动"
            lines.append(f"| {index}. {title} | {item.get('track', '待判定')} | {item.get('evidence_status', '待核验')} | {action} |")
    else:
        lines.append("当前没有形成可确认的具体外部洞察。")
    lines += ["", f"- 每日编译报告：{link(f'60_MOC/12_Knowledge_Review_{today}', today)}", f"- 待确认任务：{link('60_MOC/05_Task_Review', '研究任务确认队列')}", "- 批准入口：运行 approve_research_tasks.py 后再进入正式计划。", "", "## 任务推进规则", "", "1. 外部材料先进入 processed，不得直接计入论文、专利和工程成果。", "2. 你确认后才改为 accepted，并生成正式任务。", "3. 指标必须标注 [实测]、[仿真]、[引用]、[推导] 或 [待测]。", "4. 仿真程序、数据和结果集保留在本地，不因整理而删除。", "", f"*由 home_v2_generator.py 自动生成 · {now}*", ""]
    (VAULT / "Home.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"[OK] Home.md generated: {len(lines)} lines")

if __name__ == "__main__":
    generate()
