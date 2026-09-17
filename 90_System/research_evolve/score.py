# -*- coding: utf-8 -*-
"""research_evolve.score — 可审计的评分与自动裁决。

两条不可越界的纪律：
  1. **自动只能"否决垃圾"，不能"采纳想法"。**
     计划里写明"拍板在您"。所以自动裁决仅覆盖：越界（命中排除词）、
     重复（已否决过的换皮复现）、久挂不可执行。分数达门槛的候选只被
     *标注建议采纳*，仍留在人的裁决队列里。
  2. **每个分数都要能解释。**
     返回 reasons 列表，逐维写明依据与命中词，禁止黑箱总分
     （对照 AGENTS.md 0.1：结论必须可追溯）。
"""
from __future__ import annotations

import re

from .common import EVIDENCE_LABELS, load_vocabulary, norm_title

_WORD_RE = re.compile(r"[A-Za-z][A-Za-z0-9\-/]{2,}")
_CJK_RE = re.compile(r"[\u4e00-\u9fff]{2,}")


def _terms_in(text: str, vocab: list[str]) -> list[str]:
    """返回在 text 中命中的词表项（英文按词边界，中文按子串）。"""
    low = (text or "").lower()
    hits = []
    for term in vocab:
        t = term.strip()
        if not t:
            continue
        if re.search(r"[\u4e00-\u9fff]", t):
            if t in text:
                hits.append(t)
        else:
            # 词边界匹配：interconnect 不应命中 interconnected（AGENTS.md 6.3 的历史教训）
            if re.search(r"(?<![A-Za-z0-9])" + re.escape(t.lower()) + r"(?![A-Za-z0-9])", low):
                hits.append(t)
    return hits


def scope_check(text: str) -> dict:
    """领域越界检查：命中排除词且无领域词 -> 越界。"""
    vocab = load_vocabulary()
    tcc_hits = _terms_in(text, vocab["tcc"])
    inest_hits = _terms_in(text, vocab["inest"])
    excl_hits = _terms_in(text, vocab["exclusions"])
    in_domain = bool(tcc_hits or inest_hits)
    return {
        "tcc_hits": tcc_hits,
        "inest_hits": inest_hits,
        "exclusion_hits": excl_hits,
        "in_domain": in_domain,
        "excluded": bool(excl_hits) and not in_domain,
    }


def score_candidate(cand: dict, cfg: dict) -> dict:
    """给单条候选打分。返回 score/reasons/flags，全部可审计。"""
    rec = cand.get("record", cand)
    title = rec.get("title", "")
    detail = rec.get("detail", "") or ""
    ev = rec.get("evidence", {}) or {}
    text = f"{title} {detail}"

    sc = scope_check(text)
    reasons: list[str] = []
    flags: list[str] = []

    # ---- framework_fit
    fw_hits = sc["tcc_hits"] + sc["inest_hits"]
    if fw_hits:
        framework_fit = min(1.0, 0.45 + 0.18 * len(fw_hits))
        reasons.append(f"框架契合: 命中 {len(fw_hits)} 个词表项 {fw_hits[:4]}")
    else:
        framework_fit = 0.0
        reasons.append("框架契合: 未命中 TCC/iNEST 词表")
        flags.append("off-framework")

    # ---- testability
    has_method = bool(ev.get("has_test_method")) or bool(ev.get("has_next_step"))
    method_words = ("baseline", "metric", "reproduce", "seed", "对比", "基线", "复现", "仿真",
                    "实验", "验证", "评估", "指标", "acceptance")
    method_hits = [w for w in method_words if w.lower() in text.lower()]
    if has_method and method_hits:
        testability = 0.95
        reasons.append(f"可验证性: 有验证方法且含判据词 {method_hits[:3]}")
    elif has_method:
        testability = 0.7
        reasons.append("可验证性: 有验证方法但未给判据/基线")
        flags.append("no-acceptance-criterion")
    elif method_hits:
        testability = 0.45
        reasons.append(f"可验证性: 仅有方法词 {method_hits[:3]}，无明确步骤")
        flags.append("vague-method")
    else:
        testability = 0.0
        reasons.append("可验证性: 无验证方法")
        flags.append("not-testable")

    # ---- evidence_ready
    has_src = bool(ev.get("has_evidence")) or bool(ev.get("source_ref")) or bool(
        ev.get("evidence_text"))
    if has_src:
        evidence_ready = 0.9
        reasons.append("证据就绪: 有来源/证据字段")
    else:
        evidence_ready = 0.15
        reasons.append("证据就绪: 无来源，属未落地构思")
        flags.append("no-source")

    # ---- bridge_value（仅跨域桥）
    bridge_value = 0.0
    if rec.get("kind") == "bridge":
        strength = float(ev.get("strength", 0) or 0)
        bridge_value = min(1.0, strength / 1200.0)
        if ev.get("quality_flag"):
            bridge_value *= 0.4
            flags.append("bridge-strength-unreliable")
            reasons.append("桥价值: Strength 疑为字母序伪相关，已降权至 40%")
        else:
            reasons.append(f"桥价值: Strength={int(strength)}")
    else:
        bridge_value = 0.5   # 非桥类不参与该项，取中性值以免系统性低估

    w = cfg.get("weights", {})
    score = (w.get("framework_fit", 0.34) * framework_fit
             + w.get("testability", 0.28) * testability
             + w.get("evidence_ready", 0.22) * evidence_ready
             + w.get("bridge_value", 0.16) * bridge_value)

    # 越界直接清零（AGENTS.md 6.1 排除词命中即拒）
    if sc["excluded"]:
        score = 0.0
        reasons.append(f"领域越界: 命中排除词 {sc['exclusion_hits'][:4]} 且无 TCC/iNEST 领域词")
    # 噪音桥（强度极低）清零
    if rec.get("kind") == "bridge" and float(ev.get("strength", 0) or 0) < 10:
        score = 0.0
        reasons.append("桥价值: Strength<10，判定为噪声关联")

    return {
        "score": round(score, 4),
        "reasons": reasons,
        "flags": sorted(set(flags)),
        "scope": sc,
    }


def auto_verdict(rec: dict, scored: dict, cfg: dict, dup_of_rejected: bool) -> tuple[str, str] | None:
    """返回 (verdict, reason) 表示应当自动关闭；返回 None 表示留给人裁决。

    注意：这里**永远不会**返回 "accepted" 或 "adopted"——采纳只能由人给。
    """
    sc = scored.get("scope", {})
    flags = set(scored.get("flags", []))

    if sc.get("excluded"):
        return ("rejected",
                f"领域越界：命中排除词 {sc['exclusion_hits'][:3]}（AGENTS.md 6.1 排除规则）")

    if dup_of_rejected:
        return ("superseded", "与已否决候选同义（规范化标题命中否决记忆），避免重复讨论")

    seen = int(rec.get("seen_count", 1))
    defer_min = int(cfg.get("defer_min_seen", 3))
    if (seen >= defer_min
            and "not-testable" in flags
            and "no-source" in flags):
        return ("deferred",
                f"已出现 {seen} 次仍无来源且无验证方法，暂缓（保留以备出现新材料）")

    if rec.get("kind") == "bridge" and "bridge-strength-unreliable" in flags \
            and float(scored.get("score", 0)) < 0.25:
        return ("rejected", "跨域桥 Strength 疑为字母序伪相关且得分过低，判为生成器噪声")

    return None
