#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""灵感引擎 v4 — 纯 LLM 深度分析（无规则兜底）

每天对最近文章做 LLM 深度分析:
  核心洞察 / 假设关联 / 新研究想法 / 下一步行动 / 概念关联
LLM 不可用时明确报错（不降级为关键词规则）。
"""
import json, os, re, sys, time
from datetime import datetime, timedelta
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).parent))
import llm_client

VAULT = Path(r"D:\Obsidian\vault")
META = VAULT / "99_Meta"
OUTPUT_DIR = VAULT / "60_MOC" / "灵感卡片"
STATE_FILE = META / "inspiration_state.json"
SCAN_DIRS = [VAULT / "30_TCC", VAULT / "40_iNEST"]
LOOKBACK_DAYS = 5
MAX_PER_RUN = 6


def load_state():
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except:
        return {"analyzed": {}}


def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def get_hypotheses():
    try:
        d = json.loads((META / "hypothesis_registry.json").read_text(encoding="utf-8"))
        return d.get("hypotheses", [])
    except:
        return []


def analyze_article(filepath, hyps):
    """LLM 深度分析，返回 dict 或 None(失败)"""
    txt = filepath.read_text(encoding="utf-8", errors="ignore")[:4000]
    hyp_summary = "\n".join(
        f"- {h['id']}: {h['title']} [{h['status']}]" for h in hyps
    )
    prompt = (
        "你是TCC(拓扑中心计算)×iNEST(涌现智能)的科研助手，用户正在这两个方向做研究。\n"
        "请深度分析以下研究笔记，给出真正有用的研究洞察，不要泛泛而谈。\n\n"
        "## 用户的研究假设库:\n" + hyp_summary + "\n\n"
        "## 待分析的文章:\n" + txt + "\n\n"
        "## 严格返回JSON(不要任何多余文本):\n"
        '{\n'
        '  "core_insight": "这篇文章最核心的一个洞察，必须具体(80字内)",\n'
        '  "relevance": "与哪个假设最相关？给出假设ID并说明理由(60字内)",\n'
        '  "new_idea": "基于这篇文章，你能想到什么具体的、可执行的创新点或实验设计？(100字内)",\n'
        '  "action": "下一步具体行动(一条可执行的task，40字内)",\n'
        '  "tags": ["3-5个标签"],\n'
        '  "connects_to": ["2-4个相关wiki概念"]\n'
        '}'
    )
    return llm_client.call_json(prompt, max_tokens=1200)


def write_card(filepath, analysis):
    stem = filepath.stem[:50]
    card = []
    card.append("---")
    card.append(f"title: 灵感·{stem}")
    card.append(f'source: "[[{filepath.stem}]]"')
    card.append(f"date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    card.append("type: inspiration-card")
    card.append("method: llm")
    card.append("---")
    card.append("")
    card.append(f"# {analysis.get('core_insight', '-')}")
    card.append("")
    if analysis.get("relevance"):
        card.append(f"**假设关联**: {analysis['relevance']}")
        card.append("")
    if analysis.get("new_idea"):
        card.append(f"> **创新点**: {analysis['new_idea']}")
        card.append("")
    if analysis.get("action"):
        card.append(f"**下一步**: [ ] {analysis['action']}")
        card.append("")
    tags = analysis.get("tags") or []
    if tags:
        card.append("**标签**: " + " · ".join(f"[[{t}]]" for t in tags[:6]))
        card.append("")
    card.append("---")
    card.append(f"*来源: [[{filepath.stem}]] | LLM 深度分析*")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    outfile = OUTPUT_DIR / f"{datetime.now().strftime('%Y%m%d')}_{stem}.md"
    outfile.write_text("\n".join(card), encoding="utf-8")
    return outfile


def main():
    state = load_state()
    hyps = get_hypotheses()
    cutoff = datetime.now() - timedelta(days=LOOKBACK_DAYS)

    candidates = []
    for scan_dir in SCAN_DIRS:
        if not scan_dir.exists():
            continue
        for f in sorted(scan_dir.rglob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True):
            rel = str(f.relative_to(VAULT))
            if rel in state.get("analyzed", {}):
                continue
            if datetime.fromtimestamp(f.stat().st_mtime) < cutoff:
                continue
            if f.stat().st_size < 200:
                continue
            candidates.append(f)
            if len(candidates) >= MAX_PER_RUN:
                break
        if len(candidates) >= MAX_PER_RUN:
            break

    if not candidates:
        print("[inspiration_engine] 无新文章需要分析")
        return

    print(f"[inspiration_engine] {len(candidates)} 篇待分析")

    ok = 0
    fail = 0
    for f in candidates:
        rel = str(f.relative_to(VAULT))
        print(f"  分析: {f.name[:45]}...", flush=True)
        analysis = analyze_article(f, hyps)
        if not analysis or "core_insight" not in analysis:
            print(f"    ❌ LLM分析失败, 跳过 (LLM不可用或返回异常)")
            state.setdefault("analyzed", {})[rel] = {"date": datetime.now().isoformat(), "error": True}
            fail += 1
            continue
        card = write_card(f, analysis)
        state.setdefault("analyzed", {})[rel] = {
            "date": datetime.now().isoformat(), "card": card.name, "method": "llm",
        }
        print(f"    ✅ {card.name}")
        ok += 1
        time.sleep(1)

    save_state(state)
    print(f"[inspiration_engine] 完成: {ok} 成功 / {fail} 失败")
    if fail and ok == 0:
        print("  ⚠️ 全部失败: 检查 LLM 连接 (llm_client.py 自测: python llm_client.py)")


if __name__ == "__main__":
    main()
