# -*- coding: utf-8 -*-
"""灵感引擎 v3：LLM 分析 + 规则分析兜底

优先 LLM(多级回退)，LLM 不可用时用规则分析：
  1. 提取文章关键词
  2. 与假设库关键词匹配(自动打分)
  3. 与概念图谱交叉引用
  4. 产出结构化灵感卡片
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
MAX_PER_RUN = 8

# 规则分析用关键词库（TCC × iNEST 领域词）
TCC_KEYWORDS = ["chiplet", "noC", "interconnect", "wafer", "3d", "topology",
                "routing", "torus", "mesh", "photonic", "sdi", "tsv", "memory wall",
                "cache", "reconfig", "scalab", "bandwidth", "latency", "packaging",
                "cxl", "chip", "architecture"]
INEST_KEYWORDS = ["neuromorphic", "spike", "snn", "plasticity", "stdp", "synapse",
                  "memristor", "emergence", "critical", "reservoir", "brain",
                  "cortex", "neuron", "connectome", "learning", "attention",
                  "hebbian", "oscillat", "chaos", "consciousness", "cognition"]


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


def llm_analyze(filepath, hyps):
    """LLM 深度分析（多级回退）"""
    txt = filepath.read_text(encoding="utf-8", errors="ignore")[:3000]
    hyp_summary = "\n".join(f"- {h['id']}: {h['title']}" for h in hyps)
    prompt = (
        "你是TCC(拓扑中心计算)×iNEST(涌现智能)研究助手。分析以下笔记产出灵感卡片。\n\n"
        "## 研究假设库:\n" + hyp_summary + "\n\n"
        "## 文章:\n" + txt + "\n\n"
        "## 严格返回JSON(无多余文本):\n"
        '{"core_insight":"最核心洞察(50字内)","relevance":"最相关假设ID+理由",'
        '"new_idea":"新研究想法(80字内)","action":"下一步行动(30字内)",'
        '"tags":["标签"],"connects_to":["概念"]}'
    )
    result = llm_client.call(prompt)
    if not result:
        return None
    try:
        m = re.search(r'\{.*\}', result, re.DOTALL)
        if m:
            return json.loads(m.group())
    except:
        pass
    return {"core_insight": result[:200], "relevance": "", "new_idea": "",
            "action": "", "tags": [], "connects_to": []}


def rule_analyze(filepath, hyps):
    """规则分析兜底（无LLM时）"""
    txt = filepath.read_text(encoding="utf-8", errors="ignore")
    low = txt.lower()

    tcc_hits = [k for k in TCC_KEYWORDS if k in low]
    inest_hits = [k for k in INEST_KEYWORDS if k in low]

    # 匹配假设
    best_hyp, best_score = None, 0
    for h in hyps:
        title = h.get("title", "").lower()
        score = sum(1 for k in tcc_hits[:5] + inest_hits[:5] if k in title)
        if score > best_score:
            best_score, best_hyp = score, h.get("id")

    # 方向判定
    direction = "TCC×iNEST" if tcc_hits and inest_hits else ("TCC" if tcc_hits else ("iNEST" if inest_hits else "通用"))

    return {
        "core_insight": f"文章涉及 {direction} 方向"
                        f"（{'、'.join(tcc_hits[:3])} × {'、'.join(inest_hits[:3])}）",
        "relevance": f"{best_hyp}: 关键词重叠{best_score}个" if best_hyp else "暂无直接假设关联",
        "new_idea": "",
        "action": "人工审阅这篇文章，判断是否值得深入",
        "tags": tcc_hits[:3] + inest_hits[:3],
        "connects_to": list(set(tcc_hits[:3] + inest_hits[:3])),
    }


def write_card(filepath, analysis, used_llm):
    stem = filepath.stem[:50]
    card = []
    card.append("---")
    card.append(f"title: 灵感·{stem}")
    card.append(f'source: "[[{filepath.stem}]]"')
    card.append(f"date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    card.append("type: inspiration-card")
    card.append(f"method: {'llm' if used_llm else 'rule'}")
    card.append("---")
    card.append("")
    card.append(f"# {analysis.get('core_insight', '-')}")
    card.append("")
    if analysis.get("relevance"):
        card.append(f"**关联**: {analysis['relevance']}")
        card.append("")
    if analysis.get("new_idea"):
        card.append(f"> **新想法**: {analysis['new_idea']}")
        card.append("")
    if analysis.get("action"):
        card.append(f"**下一步**: [ ] {analysis['action']}")
        card.append("")
    tags = analysis.get("tags") or analysis.get("connects_to") or []
    if tags:
        card.append("**标签**: " + " | ".join(f"[[{t}]]" for t in tags[:6]))
    card.append("")
    card.append("---")
    card.append(f"*来源: [[{filepath.stem}]] | {'LLM分析' if used_llm else '规则分析(LLM不可用)'}*")

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
        print("[inspiration_engine] 无新文章")
        return

    print(f"[inspiration_engine] {len(candidates)} 篇待分析")
    analyzed = 0
    for f in candidates:
        rel = str(f.relative_to(VAULT))
        result = llm_analyze(f, hyps)
        used_llm = result is not None
        if not result:
            result = rule_analyze(f, hyps)
        card = write_card(f, result, used_llm)
        state.setdefault("analyzed", {})[rel] = {
            "date": datetime.now().isoformat(), "card": card.name,
            "method": "llm" if used_llm else "rule",
        }
        analyzed += 1
        print(f"  {'🟢LLM' if used_llm else '🟡规则'} {f.name[:40]} -> {card.name}")
        time.sleep(0.5)

    save_state(state)
    print(f"[inspiration_engine] 完成 {analyzed} 篇")


if __name__ == "__main__":
    main()
