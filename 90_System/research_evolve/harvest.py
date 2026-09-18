# -*- coding: utf-8 -*-
"""research_evolve.harvest — 从现有产出中收集"候选"，不新造数据。

关键立场：本模块**不生成**新想法，只把系统已经产出的东西收进候选池。
当前系统的病不是"想法太少"，而是每天生成 18 条建议却永不关闭。
所以这里只做收集 + 忠实还原字段（并修正已知的字段丢失 bug）。
"""
from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path

from .common import (
    VAULT,
    load_json,
    load_vocabulary,
    norm_title,
    parse_frontmatter,
    read_text,
)

META = VAULT / "99_Meta"
WIKI = VAULT / "wiki"
IDEA_DIR = VAULT / "60_MOC" / "灵感卡片"


def _mk(kind: str, title: str, source: str, detail: str = "",
        evidence: dict | None = None) -> dict | None:
    title = (title or "").strip()
    if len(title) < 4:
        return None
    return {"kind": kind, "title": title, "source": source,
            "detail": (detail or "").strip()[:600],
            "evidence": evidence or {}}


# ---------------------------------------------------------------- 假说
def harvest_hypotheses() -> list[dict]:
    """从 99_Meta/hypothesis_registry.json 收集未验证假说。"""
    data = load_json(META / "hypothesis_registry.json", default={}) or {}
    out = []
    for h in data.get("hypotheses", []) or []:
        status = str(h.get("status", "")).lower()
        if status in ("validated", "refuted", "done", "closed"):
            continue
        hid = h.get("id", "?")
        title = h.get("title", "")
        has_method = bool(h.get("test_method"))
        has_evidence = bool(h.get("evidence"))
        out.append(_mk(
            "hypothesis", f"{hid}: {title}",
            "99_Meta/hypothesis_registry.json",
            detail=" | ".join(x for x in [
                f"理由: {h.get('rationale','')}" if h.get("rationale") else "",
                f"验证方法: {h.get('test_method','')}" if has_method else "",
                f"来源桥: {h.get('source_bridge','')}" if h.get("source_bridge") else "",
            ] if x),
            evidence={
                "status": status,
                "has_test_method": has_method,
                "has_evidence": has_evidence,
                "evidence_text": str(h.get("evidence", ""))[:200],
                "created": str(h.get("created", "")),
            },
        ))
    return [c for c in out if c]


# ---------------------------------------------------------------- 进化队列
def harvest_evolution_queue() -> list[dict]:
    """从 99_Meta/evolution_queue.json 收集待办。

    修正 task_recommender.py 的两个 bug：
      * 它用 str(item)[:100] 打印原始 dict（报告里出现截断的 Python repr）；
      * 它把每条都硬编码成 MEDIUM，丢掉条目自身的真实 priority。
    """
    data = load_json(META / "evolution_queue.json", default={}) or {}
    items = data.get("items") or data.get("queue") or []
    out = []
    for it in items:
        if not isinstance(it, dict):
            continue
        # 注意: "superseded" 必须一并跳过。
        # consolidate_evolution_queue.py 把 51 条历史堆积标记为 superseded
        # （而非删除），若这里不排除，它们仍会被当作活跃候选重新收进来
        # ——实测发现 open 池里凭空多出 51 条 evolution_item 就是这个原因。
        status = str(it.get("status", "pending")).lower()
        if status in ("done", "closed", "resolved", "dismissed", "superseded"):
            continue
        iid = it.get("id", "?")
        title = it.get("title") or it.get("summary") or ""
        out.append(_mk(
            "evolution_item", f"{iid}: {title}",
            "99_Meta/evolution_queue.json",
            detail=str(it.get("detail") or it.get("description") or "")[:400],
            evidence={
                "priority": str(it.get("priority", "")),
                "type": str(it.get("type", "")),
                "status": status,
                "created": str(it.get("created") or it.get("date") or ""),
            },
        ))
    return [c for c in out if c]


# ---------------------------------------------------------------- 灵感卡
_NEXT_RE = re.compile(r"\*\*下一步\*\*[:：]\s*(.+)")
_INNOV_RE = re.compile(r"\*\*创新点\*\*[:：]\s*(.+)")
_HYP_RE = re.compile(r"\*\*假设关联\*\*[:：]\s*(.+)")


def harvest_ideas(limit: int = 400) -> list[dict]:
    """从 60_MOC/灵感卡片/ 收集灵感卡，取"标题即洞见"，并把下一步作为可执行性证据。"""
    if not IDEA_DIR.exists():
        return []
    files = sorted(IDEA_DIR.glob("*.md"),
                   key=lambda p: p.stat().st_mtime, reverse=True)[:limit]
    out = []
    for f in files:
        txt = read_text(f)
        fm, body = parse_frontmatter(txt)
        lines = [l.strip() for l in body.splitlines() if l.strip()]
        headline = next((l.lstrip("# ").strip() for l in lines if l.startswith("# ")), "")
        if not headline:
            continue
        nxt = (_NEXT_RE.search(body) or [None, ""])[1] if _NEXT_RE.search(body) else ""
        inn = (_INNOV_RE.search(body) or [None, ""])[1] if _INNOV_RE.search(body) else ""
        hyp = (_HYP_RE.search(body) or [None, ""])[1] if _HYP_RE.search(body) else ""
        src_link = fm.get("source", "")
        out.append(_mk(
            "idea", headline,
            f"60_MOC/灵感卡片/{f.name}",
            detail=" | ".join(x for x in [inn, nxt] if x),
            evidence={
                "source_ref": src_link,
                "hypothesis_link": hyp,
                "has_next_step": bool(nxt),
                "method": fm.get("method", ""),
                "card_date": fm.get("date", ""),
            },
        ))
    return [c for c in out if c]


# ---------------------------------------------------------------- 跨域桥
# 兼容两种输出格式：
#   旧: ### SDI_Plastic_Interconnect (Strength: 1212)
#   新: ### SDI_Plastic_Interconnect (Strength: 1212 · Coverage: 0.6103)
# 教训: 我改写了 cross_domain_insight.py 的报告格式，却没同步更新这里的解析，
# 结果下一轮"收集 跨域桥: 0 条"——改输出格式必须同时改解析方。
_BRIDGE_RE = re.compile(
    r"^###\s+(\S+)\s+\(Strength:\s*(\d+)(?:\s*·\s*Coverage:\s*([\d.]+))?\s*\)\s*$",
    re.M,
)


def harvest_bridges() -> list[dict]:
    """从 wiki/cross_domain_insights.md 收集 TCC×iNEST 桥。

    注意（实测缺陷）：该文件的 Strength 值并不能反映相关性——旧生成器取的是
    按字母序排在最前的概念，因此 6 条顶级桥反复列着同样的
    [[1024_Card_SuperNode]] / [[2_5D_3D_HeterogeneousIntegration]] / [[2_5D_Interposer]]。
    该生成器已于 2026-09-18 改为术语特异性排序；这里保留原值但打上
    quality_flag，交由评分层降权。
    """
    p = WIKI / "cross_domain_insights.md"
    if not p.exists():
        return []
    txt = read_text(p)
    out = []
    for m in _BRIDGE_RE.finditer(txt):
        name, strength, coverage = m.group(1), m.group(2), m.group(3)
        ev = {"strength": int(strength),
              "quality_flag": "strength-is-corpus-frequency-not-relevance"}
        if coverage is not None:
            ev["coverage"] = float(coverage)
        out.append(_mk(
            "bridge", f"跨域桥 {name}",
            "wiki/cross_domain_insights.md",
            detail=f"Strength={strength}" + (f" · Coverage={coverage}" if coverage else ""),
            evidence=ev,
        ))
    return [c for c in out if c]


# ---------------------------------------------------------------- 概念债（聚合为一条）
_TITLE_LIKE_RE = re.compile(r"[\u4e00-\u9fff]|：|，|（")


def concept_debt() -> dict:
    """统计 wiki 概念层的"债"，聚合成单条候选（而不是 1850 条噪声）。

    实测口径：读取每个概念文件的前 400 字符判断 auto 标记与标题特征。
    """
    cdir = WIKI / "concepts"
    if not cdir.exists():
        return {}
    total = auto_stub = title_like = 0
    for f in cdir.glob("*.md"):
        total += 1
        head = read_text(f)[:400]
        if "auto: true" in head:
            auto_stub += 1
        stem = f.stem
        if _TITLE_LIKE_RE.search(stem) or len(stem) > 25:
            title_like += 1
    orphan_reported = 0
    hp = WIKI / "health.md"
    if hp.exists():
        m = re.search(r"Orphan Concepts\*\*:\s*(\d+)", read_text(hp))
        if m:
            orphan_reported = int(m.group(1))
    return {
        "total": total,
        "auto_stub": auto_stub,
        "title_like": title_like,
        "orphan_reported": orphan_reported,
        "orphan_source": "wiki/health.md (生成器自报)",
    }


# ---------------------------------------------------------------- 新来源检测（冻结守卫用）
NOISE_DIRS = {"_attachments_knowledge", "_digests", "getnote_external", "inbox_overflow"}


def new_source_activity(days: int = 2) -> dict:
    """检测是否有真正的新来源材料进入（用于"无新来源则冻结新增概念"）。

    只统计 00_Inbox 与 20_Processing 下的 .md，排除附件/摘要等噪声目录。
    """
    cutoff = datetime.now().timestamp() - days * 86400
    counts = {}
    newest = ""
    for root_rel in ("00_Inbox", "20_Processing", "raw"):
        root = VAULT / root_rel
        if not root.exists():
            counts[root_rel] = 0
            continue
        n = 0
        for f in root.rglob("*.md"):
            if any(part in NOISE_DIRS for part in f.parts):
                continue
            try:
                mt = f.stat().st_mtime
            except Exception:
                continue
            if mt >= cutoff:
                n += 1
                if mt > (datetime.fromisoformat(newest).timestamp() if newest else 0):
                    newest = datetime.fromtimestamp(mt).isoformat()
        counts[root_rel] = n
    return {"counts": counts, "total": sum(counts.values()),
            "newest": newest, "window_days": days}
