#!/usr/bin/env python3
"""Compile external pipeline notes into a review-only research queue."""
import json
import os
import re
from datetime import datetime
from pathlib import Path

from openai import OpenAI

VAULT = Path(r"D:\Obsidian\vault")
INBOX = VAULT / "00_Inbox" / "_pipeline_insights"
MOC = VAULT / "60_MOC"
META = VAULT / "99_Meta"
GENERIC_ACTIONS = {"review for relevance to tcc/inest.", "review for relevance to tcc/inest", "none", "n/a", "无", "暂无"}
MIN_RELEVANCE = 2

def frontmatter(text):
    if not text.startswith("---"):
        return {}
    match = re.search(r"^---\s*\n(.*?)\n---", text, re.MULTILINE | re.DOTALL)
    if not match:
        return {}
    values = {}
    for line in match.group(1).splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            values[key.strip()] = value.strip().strip('"')
    return values

def section(text, heading):
    match = re.search(rf"^##\s+{re.escape(heading)}\s*$", text, re.MULTILINE)
    if not match:
        return ""
    tail = text[match.end():]
    next_heading = re.search(r"^##\s+", tail, re.MULTILINE)
    return tail[: next_heading.start() if next_heading else None].strip()

def bullets(text):
    return [re.sub(r"^[-*]\s+", "", line).strip() for line in text.splitlines() if re.match(r"^[-*]\s+", line.strip())]

def clean(value, limit=420):
    value = re.sub(r"[*_]+", "", value or "")
    return re.sub(r"\s+", " ", value).strip()[:limit]

def deep_analysis(text, title, track):
    """Return a bounded research-use analysis; never invent performance data."""
    key = os.environ.get("DEEPSEEK_API_KEY", "")
    if not key:
        return {}
    prompt = f"""你是 TCC 与 iNEST 科研知识编译器。仅基于给定摘要，输出 JSON。
论文：{title}
当前方向：{track}
摘要：{section(text, 'Abstract')[:5000]}

字段：
direction: TCC / iNEST / both / reject
research_value: high / medium / low
tcc_insight: 对拓扑中心计算的具体启发，没有则写无直接关联
inest_insight: 对复杂网络涌现智能的具体启发，没有则写无直接关联
candidate_action: 一项可验证、可审批的论文/仿真/代码/专利候选动作；没有则写无
evidence_status: 只能是 [引用] 待人工核验
禁止：杜撰性能数值、把外部论文说成团队原创、直接生成已批准任务。"""
    try:
        client = OpenAI(api_key=key, base_url=os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1"))
        response = client.chat.completions.create(
            model=os.environ.get("DEEPSEEK_MODEL", "deepseek-v4-pro"),
            messages=[{"role": "user", "content": prompt}], temperature=0.1, max_tokens=700, timeout=90,
        )
        match = re.search(r"\{[\s\S]*\}", response.choices[0].message.content)
        return json.loads(match.group()) if match else {}
    except Exception as exc:
        print(f"[WARN] DeepSeek analysis skipped: {exc}")
        return {}

def compile_notes(use_llm=False):
    today = datetime.now().strftime("%Y-%m-%d")
    previous = {}
    state_path = META / "knowledge_compile_state.json"
    try:
        previous = {item.get("file"): item for item in json.loads(state_path.read_text(encoding="utf-8")).get("items", [])}
    except (OSError, json.JSONDecodeError):
        pass
    candidates = []
    for path in sorted(INBOX.glob(f"{today}_*.md"), reverse=True):
        text = path.read_text(encoding="utf-8", errors="replace")
        fm = frontmatter(text)
        try:
            relevance = int(fm.get("relevance", "0"))
        except ValueError:
            relevance = 0
        if relevance < MIN_RELEVANCE:
            continue
        actions = [a for a in bullets(section(text, "Actionable")) if a.lower() not in GENERIC_ACTIONS]
        tcc = clean(section(text, "TCC Insights"))
        inest = clean(section(text, "iNEST Insights"))
        if not actions and not tcc and not inest:
            continue
        analysis = deep_analysis(text, fm.get("title", path.stem), fm.get("track", "unclassified")) if use_llm else {}
        if analysis.get("direction") == "reject" or analysis.get("research_value") == "low":
            continue
        action = analysis.get("candidate_action", "")
        if action and action != "无":
            actions = [action, *actions]
        file_key = str(path.relative_to(VAULT)).replace("\\", "/")
        item = {"title": fm.get("title", path.stem), "source": fm.get("source", "unknown"), "url": fm.get("url", ""), "track": analysis.get("direction", fm.get("track", "unclassified")), "relevance": relevance, "file": file_key, "tcc_insight": analysis.get("tcc_insight", tcc) or "无直接关联或待确认。", "inest_insight": analysis.get("inest_insight", inest) or "无直接关联或待确认。", "candidate_actions": actions[:5], "knowledge_state": "processed", "evidence_status": analysis.get("evidence_status", "[引用] 待人工核验"), "provenance": "external", "user_decision": "pending", "analysis_mode": "deepseek-v4-pro" if analysis else "metadata-only"}
        prior = previous.get(file_key, {})
        if prior.get("user_decision") not in (None, "", "pending"):
            for key in ("knowledge_state", "evidence_status", "user_decision", "tcc_insight", "inest_insight", "candidate_actions"):
                if prior.get(key):
                    item[key] = prior[key]
            item["analysis_mode"] = "user-confirmed"
        candidates.append(item)
    return today, candidates

def write_outputs(today, candidates):
    MOC.mkdir(parents=True, exist_ok=True)
    META.mkdir(parents=True, exist_ok=True)
    payload = {"schema": "knowledge-compiler-review-v1", "generated": datetime.now().isoformat(timespec="seconds"), "status": "pending_user_review", "items": candidates}
    (META / "knowledge_compile_state.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["---", "type: knowledge-review", "status: pending_user_review", f"date: {today}", f"items: {len(candidates)}", "---", "", f"# 每日知识编译待确认 · {today}", "", "> 外部资料只在本页形成候选洞察，不计入团队论文、专利或已完成成果。确认后再进入正式任务计划。", ""]
    if not candidates:
        lines.append("今日没有形成可审阅的具体洞察。")
    for index, item in enumerate(candidates, 1):
        lines.extend([f"## K-{today}-{index:02d} · {item['title']}", f"- 来源：{item['source']}  | 方向：{item['track']}  | 相关度：{item['relevance']}", f"- 原文：[[{Path(item['file']).stem}]]", f"- 状态：{item['knowledge_state']}  | 证据：{item['evidence_status']}  | 决策：{item['user_decision']}", f"- TCC 启迪：{item['tcc_insight']}", f"- iNEST 启迪：{item['inest_insight']}", "- 候选行动：" + ("；".join(item["candidate_actions"]) if item["candidate_actions"] else "待人工提出具体行动"), "- 输出去向：待确认后选择论文 / 专利 / 仿真 / 核心代码 / 项目指南。", ""])
    output = MOC / f"12_Knowledge_Review_{today}.md"
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--analyze", action="store_true", help="Use DeepSeek V4 Pro for high-value notes only")
    args = parser.parse_args()
    day, items = compile_notes(use_llm=args.analyze)
    output = write_outputs(day, items)
    print(f"[OK] compiled={len(items)} output={output}")
