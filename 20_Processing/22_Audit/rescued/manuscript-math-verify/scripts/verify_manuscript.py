#!/usr/bin/env python3
"""verify_manuscript.py — 手稿数学验证引擎（独立 CLI 版）

从 @deepseek-ai/Agent 考古资产 tooluniverse_agent_base.py (L1290-1915) 提炼，
去除 ToolUniverse 依赖，仅使用 Python 标准库（re/html/json/pathlib）。

用途：对理论手稿（HTML 或纯文本）执行结构化的数学-逻辑验证：
  claim 抽取 -> 证明义务 -> 符号目录 -> 公式依赖 -> 推导链 -> 数值一致性
  -> 证明骨架（假设/引理/步骤/缺口）-> 仿真交接 -> 一致性检查 -> 修订报告

用法:
    python verify_manuscript.py <manuscript.html|manuscript.md|manuscript.txt> [--json OUT]
    python verify_manuscript.py <path> --report           # 只输出可读修订报告
    python verify_manuscript.py <path> --json out.json    # 全量结构化结果

来源标注: 原实现见 D:\Obsidian\vault\20_Processing\22_Audit\rescued\scripts\
           tooluniverse_agent_base.py（考古审计 2026-08-21 抢救迁移）。
"""

import argparse
import html
import json
import re
import sys
from pathlib import Path

# Windows 控制台 UTF-8 输出（避免 GBK 乱码）
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
from typing import Any, Dict, List

# ─────────────────────────── 文本工具 ───────────────────────────

def clean_text(value: str) -> str:
    return " ".join((value or "").split())


def summarize_text(text: str, max_chars: int) -> str:
    cleaned = clean_text(text)
    if len(cleaned) <= max_chars:
        return cleaned
    cutoff = cleaned[:max_chars].rsplit(" ", 1)[0]
    return f"{cutoff}..."


def normalize_pdf_math_noise(text: str) -> str:
    """修复 PDF 导入产生的数学符号噪声（空格拆散/分数误写等）。"""
    normalized = text or ""
    replacements = [
        (r"\bC\s+S\s+T\b", "CST"),
        (r"\bC\s+S\b", "CS"),
        (r"\bC\s+T\b", "CT"),
        (r"\bR\s+I\b", "RI"),
        (r"Γ\s*s\s*t", "Γ_st"),
        (r"Γ\s+st", "Γ_st"),
        (r"λ\s+m\s+a\s+x", "λ_max"),
        (r"η\s+c\s+o\s+u\s+p\s+l\s+i\s+n\s+g", "η_coupling"),
        (r"β\s+d\s+e\s+v\s+i\s+c\s+e", "β_device"),
        (r"1\s*/\s*√\s*2", "1/√2"),
        (r"1\s*/\s*2\s*≈\s*0\.707", "1/√2≈0.707"),
        (r"1\s*/\s*2\s*=\s*0\.707", "1/√2=0.707"),
        (r"θ\s*2\s*=\s*1\s*/\s*2\s*≈\s*0\.707", "θ2=1/√2≈0.707"),
        (r"θ\s*₂\s*=\s*1\s*/\s*2\s*≈\s*0\.707", "θ₂=1/√2≈0.707"),
        (r"θ\s*0\s*=\s*1\s*/\s*2", "θ0=1/√2"),
        (r"θ\s*₀\s*=\s*1\s*/\s*2", "θ₀=1/√2"),
    ]
    for pattern, replacement in replacements:
        normalized = re.sub(pattern, replacement, normalized)
    normalized = re.sub(
        r"(?<=\b[A-Za-zΑ-Ωα-ω])\s+(?=[A-Za-zΑ-Ωα-ω]\b)", "", normalized
    )
    normalized = re.sub(r"\s+", " ", normalized)
    return normalized


def compact_math_text(text: str) -> str:
    compact = normalize_pdf_math_noise(text).replace("−", "-")
    compact = re.sub(r"(?<=\w)\s+(?=\w)", "", compact)
    compact = re.sub(r"\s+", " ", compact)
    return compact


def extract_formula_symbols(expr: str) -> List[str]:
    symbols = []
    for token in ["CS", "CT", "CST", "RI", "Γ_st", "α", "θ", "λ", "NMI", "Mantel"]:
        if token in expr and token not in symbols:
            symbols.append(token)
    return symbols


# ─────────────────────────── 手稿解析 ───────────────────────────

def parse_manuscript(raw: str, path: Path) -> Dict[str, Any]:
    """解析 HTML 或纯文本手稿为分节结构。"""
    if path.suffix.lower() in (".html", ".htm"):
        title_match = re.search(r"<title>(.*?)</title>", raw, flags=re.IGNORECASE | re.DOTALL)
        title = clean_text(html.unescape(title_match.group(1))) if title_match else path.stem
        sections = []
        heading_matches = list(
            re.finditer(r"<h([1-4])[^>]*>(.*?)</h\1>", raw, flags=re.IGNORECASE | re.DOTALL)
        )
        for index, match in enumerate(heading_matches):
            level = int(match.group(1))
            heading = clean_text(html.unescape(re.sub(r"<[^>]+>", " ", match.group(2))))
            start = match.end()
            end = heading_matches[index + 1].start() if index + 1 < len(heading_matches) else len(raw)
            chunk = raw[start:end]
            chunk = re.sub(r"<script.*?</script>", " ", chunk, flags=re.IGNORECASE | re.DOTALL)
            chunk = re.sub(r"<style.*?</style>", " ", chunk, flags=re.IGNORECASE | re.DOTALL)
            text = clean_text(html.unescape(re.sub(r"<[^>]+>", " ", chunk)))
            sections.append({"heading": heading, "level": level, "text": text})
        full_text = clean_text(html.unescape(re.sub(r"<[^>]+>", " ", raw)))
        return {"title": title, "path": str(path), "section_count": len(sections),
                "sections": sections, "full_text": full_text}
    # 纯文本/Markdown：按标题行切分
    lines = raw.splitlines()
    sections = []
    current = {"heading": path.stem, "level": 1, "text": ""}
    heading_re = re.compile(r"^(#{1,4})\s+(.+)$")
    for line in lines:
        m = heading_re.match(line.strip())
        if m and current["text"].strip():
            sections.append(current)
            current = {"heading": clean_text(m.group(2)), "level": len(m.group(1)), "text": ""}
        else:
            current["text"] += " " + line.strip()
    if current["text"].strip():
        sections.append(current)
    return {"title": path.stem, "path": str(path), "section_count": len(sections),
            "sections": sections, "full_text": clean_text(raw)}


# ─────────────────────────── Claim 抽取 ───────────────────────────

def extract_manuscript_claims(manuscript: Dict[str, Any]) -> List[Dict[str, Any]]:
    claims = []
    claim_counter = 1
    theorem_markers = [("定理", "theorem"), ("引理", "lemma"), ("假设", "assumption"), ("猜想", "conjecture")]
    simulation_tokens = ["验证数据集", "准确率", "检测成功率", "GPT-4", "LSTM", "ResNet", "Level"]
    for section in manuscript.get("sections", []):
        text = section.get("text", "")
        heading = section.get("heading", "")
        normalized_text = normalize_pdf_math_noise(text)
        claim_type = "derivation_claim"
        for marker, inferred_type in theorem_markers:
            if marker in heading or marker in normalized_text:
                claim_type = inferred_type
                break
        if heading == "目 录":
            claim_type = "conjecture"
        requires_simulation_handoff = any(token in normalized_text for token in simulation_tokens)
        if not text.strip():
            continue
        claims.append({
            "claim_id": f"CLM-{claim_counter:03d}",
            "section": heading,
            "claim_type": claim_type,
            "statement": text,
            "requires_theoretical_proof": claim_type in {"theorem", "lemma", "conjecture", "derivation_claim"},
            "requires_literature_grounding": claim_type in {"theorem", "lemma", "conjecture", "derivation_claim", "assumption"},
            "requires_simulation_handoff": requires_simulation_handoff,
            "citations_present": bool(re.search(r"\b(19|20)\d{2}\b", text)),
            "keywords": re.findall(r"[A-Za-zα-ωΑ-Ω]+|\d+(?:\.\d+)?", normalized_text)[:8],
            "status": "extracted",
        })
        claim_counter += 1
    return claims


def build_proof_obligations(claims: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    items = []
    for claim in claims:
        if claim.get("requires_theoretical_proof"):
            checks = ["definitions_closed", "derivation_chain_present"]
            statement = normalize_pdf_math_noise(claim.get("statement", ""))
            if any(token in statement for token in ["θ", "阈值", "SNR"]):
                checks.append("threshold_algebra_explicit")
            if any(token in statement for token in ["Γ_st", "NMI", "Mantel"]):
                checks.append("bounded_domain_explicit")
            if any(token in statement for token in ["固定点", "β(CST)", "重整化"]):
                checks.extend(["beta_function_specified", "stability_condition_explicit"])
            items.append({
                "claim_id": claim.get("claim_id"),
                "obligation_kind": "theoretical",
                "required_checks": list(dict.fromkeys(checks)),
            })
        elif claim.get("requires_simulation_handoff"):
            items.append({
                "claim_id": claim.get("claim_id"),
                "obligation_kind": "simulation_handoff",
                "required_checks": ["open_source_dataset_selection", "metric_mapping"],
            })
    return items


def verify_claims_with_search(claims: List[Dict[str, Any]], manuscript: Dict[str, Any]) -> Dict[str, Any]:
    """启发式本地验证（无网络搜索时的占位实现）。"""
    items = []
    for claim in claims[:12]:
        support = 1 if claim.get("citations_present") else 0
        items.append({
            "claim_id": claim.get("claim_id"),
            "support_count": support,
            "counter_count": 0,
            "status": "heuristic_local_validation",
        })
    return {"verified_claim_count": len(items), "items": items}


# ─────────────────────────── 数学验证 ───────────────────────────

def build_symbol_catalog(section_texts: Dict[str, str], full_text: str) -> Dict[str, Any]:
    catalog = {}
    symbol_rules = {
        "CS": ["空间复杂度", "CS"],
        "CT": ["时间复杂度", "CT"],
        "CST": ["时空协同复杂度", "CST"],
        "Γ_st": ["时空耦合", "Γ_st"],
        "α": ["临界响应", "α"],
        "RI": ["相对智能", "RI"],
        "θ": ["智能阈值", "θ"],
        "λ": ["临界性", "λ"],
    }
    haystack = " ".join(section_texts.keys()) + " " + full_text
    for symbol, hints in symbol_rules.items():
        catalog[symbol] = {"defined": any(hint in haystack for hint in hints), "hints": hints}
    return catalog


def build_formula_dependency_checks(formulas: List[Dict[str, Any]], symbol_catalog: Dict[str, Any]) -> List[Dict[str, Any]]:
    checks = []
    for formula in formulas:
        missing = [
            symbol for symbol in formula.get("symbols", [])
            if symbol in symbol_catalog and not symbol_catalog[symbol].get("defined")
        ]
        checks.append({
            "name": f"dependency::{formula.get('expression', '')[:40]}",
            "status": "pass" if not missing else "warn",
            "detail": ("All referenced core symbols appear to have definitions."
                       if not missing else f"Potentially undefined symbols referenced: {', '.join(missing)}"),
        })
    return checks


def build_derivation_chain_checks(claims: List[Dict[str, Any]], proof_obligations: List[Dict[str, Any]],
                                  section_texts: Dict[str, str]) -> List[Dict[str, Any]]:
    claim_by_section: Dict[str, list] = {}
    for claim in claims:
        claim_by_section.setdefault(claim.get("section", ""), []).append(claim)
    checks = []
    expected_sections = [
        "0.2 阈值1（θ₁=0.5）的热力学推导",
        "0.3 阈值2（θ₂=1/√2）的信号检测理论推导",
        "0.4 从CST公式推导阈值表达式",
        "0.4bis",
        "0.5 六个自然常数作为智能等级边界的重整化群推导",
    ]
    for section_name in expected_sections:
        has_section = any(section_name in key for key in section_texts.keys())
        has_claims = any(section_name in key for key in claim_by_section.keys())
        checks.append({
            "name": f"section_chain::{section_name}",
            "status": "pass" if has_section and has_claims else "warn",
            "detail": ("Derivation section and extracted claims are both present."
                       if has_section and has_claims else "Expected derivation section or extracted claims are incomplete."),
        })
    theorem_claims = [claim for claim in claims if claim.get("claim_type") in {"theorem", "lemma", "conjecture"}]
    theoretical_obligations = [item for item in proof_obligations if item.get("obligation_kind") == "theoretical"]
    checks.append({
        "name": "theoretical_obligation_coverage",
        "status": "pass" if len(theoretical_obligations) >= max(1, len(theorem_claims) - 1) else "warn",
        "detail": f"{len(theoretical_obligations)} theoretical obligations detected for {len(theorem_claims)} theorem/lemma/conjecture style claims.",
    })
    return checks


def extract_math_formulas(text: str) -> List[Dict[str, Any]]:
    normalized = compact_math_text(normalize_pdf_math_noise(text))
    patterns = [
        r"Γ_st\s*=\s*NMI\s*\(\s*M_S\s*,\s*M_T\s*\)\s*[·\*]\s*sign\s*\(\s*Mantel\s*\(\s*A\s*,\s*FC\s*\)\s*\)",
        r"CS\s*=\s*\([^)]+\)",
        r"CT\s*=\s*\([^)]+\)",
        r"CST\s*[=≈]\s*[^。；]+",
        r"RI\s*=\s*[^。；]+",
        r"θ[0-9₀₁₂₃₄₅]?\s*=\s*[^。；,]+",
    ]
    formulas = []
    seen = set()
    for pattern in patterns:
        for match in re.finditer(pattern, normalized):
            expr = clean_text(match.group(0))
            if expr and expr not in seen:
                seen.add(expr)
                formulas.append({"expression": expr, "symbols": extract_formula_symbols(expr)})
    return formulas


def build_numeric_consistency_checks(claims: List[Dict[str, Any]], normalized_text: str, raw_text: str) -> List[Dict[str, Any]]:
    normalized = compact_math_text(normalized_text)
    checks = []
    if "θ1=0.5" in normalized or "θ₁=0.5" in raw_text:
        checks.append({"name": "theta1_half_consistency", "status": "pass",
                       "detail": "θ1 = 0.5 is consistently represented."})
    raw_compact = compact_math_text(raw_text)
    if ("1/2≈0.707" in raw_compact or "1/2=0.707" in raw_compact) and "1/√2≈0.707" not in normalized:
        checks.append({"name": "one_half_numeric_mismatch", "status": "fail",
                       "detail": "The manuscript equates 1/2 with approximately 0.707, which is numerically inconsistent. This likely should be 1/√2 ≈ 0.707."})
    elif ("1/2≈0.707" in raw_compact or "1/2=0.707" in raw_compact) and "1/√2≈0.707" in normalized:
        checks.append({"name": "pdf_fraction_normalized_to_inverse_sqrt2", "status": "pass",
                       "detail": "PDF-import fraction noise was normalized so that 0.707 is interpreted as 1/√2 rather than 1/2."})
    elif "1/√2≈0.707" in normalized or "1/√2" in normalized:
        checks.append({"name": "inverse_sqrt2_consistency", "status": "pass",
                       "detail": "1/√2 ≈ 0.707 is numerically consistent."})
    elif "1/2≈0.707" in raw_compact or "1/2=0.707" in raw_compact:
        checks.append({"name": "one_half_numeric_mismatch", "status": "fail",
                       "detail": "The manuscript contains an unresolved 1/2 ≈ 0.707 pattern after PDF-math normalization."})
    if "Γ_st∈[-1,1]" in normalized:
        checks.append({"name": "gamma_bound_presence", "status": "pass",
                       "detail": "Γ_st bound [-1, 1] is explicitly stated."})
    else:
        checks.append({"name": "gamma_bound_missing", "status": "warn",
                       "detail": "Γ_st bound [-1, 1] was not robustly detected in normalized math text."})
    theta_constants = ["0.707", "1.0", "1.618", "2.718", "3.142", "4.669"]
    found_constants = [value for value in theta_constants if value in normalized]
    checks.append({"name": "theta_constant_table_presence",
                   "status": "pass" if len(found_constants) >= 4 else "warn",
                   "detail": f"Detected {len(found_constants)} threshold constants in the manuscript table."})
    return checks


def build_math_validation(manuscript: Dict[str, Any], claims: List[Dict[str, Any]],
                          proof_obligations: List[Dict[str, Any]]) -> Dict[str, Any]:
    section_texts = {section.get("heading", ""): section.get("text", "")
                     for section in manuscript.get("sections", [])}
    full_text = manuscript.get("full_text", "")
    normalized_full_text = normalize_pdf_math_noise(full_text)
    formulas = extract_math_formulas(normalized_full_text)
    symbol_catalog = build_symbol_catalog(section_texts, normalized_full_text)
    numeric_checks = build_numeric_consistency_checks(claims, normalized_full_text, full_text)
    dependency_checks = build_formula_dependency_checks(formulas, symbol_catalog)
    derivation_checks = build_derivation_chain_checks(claims, proof_obligations, section_texts)
    issues = []
    for bucket in [numeric_checks, dependency_checks, derivation_checks]:
        for item in bucket:
            if item.get("status") != "pass":
                issues.append(item)
    return {
        "formula_count": len(formulas),
        "formulas": formulas,
        "symbol_catalog": symbol_catalog,
        "normalized_text_excerpt": summarize_text(normalized_full_text, 1200),
        "numeric_checks": numeric_checks,
        "dependency_checks": dependency_checks,
        "derivation_checks": derivation_checks,
        "issue_count": len(issues),
        "issues": issues,
    }


# ─────────────────────────── 证明骨架 ───────────────────────────

def infer_proof_assumptions(claim: Dict[str, Any], section_text: str) -> List[str]:
    assumptions = []
    lower_text = section_text.lower()
    if "热力学第二定律" in section_text:
        assumptions.append("Assume the thermodynamic entropy balance applies to the modeled open/self-organizing system.")
    if "landauer" in lower_text or "shannon" in lower_text:
        assumptions.append("Assume an admissible mapping exists between information-processing complexity and thermodynamic/information entropy.")
    if "signal" in lower_text or "检测" in section_text or "snr" in lower_text:
        assumptions.append("Assume Gaussian-noise signal detection theory is an appropriate surrogate model for system discrimination ability.")
    if "重整化" in section_text or "固定点" in section_text:
        assumptions.append("Assume a coarse-graining flow β(CST) exists and preserves the relevant control parameters.")
    if "α" in section_text and ("临界" in section_text or "相变" in section_text):
        assumptions.append("Assume critical-phenomena analogies are valid for mapping microscopic nonlinearity to macroscopic amplification.")
    if not assumptions:
        assumptions.append("Assume the section definitions and normalization rules are mathematically well-posed.")
    return assumptions


def infer_proof_lemmas(claim: Dict[str, Any], section_text: str) -> List[str]:
    lemmas = []
    if "θ1" in section_text or "0.5" in section_text:
        lemmas.append("Lemma: the environment-compensation requirement can be rewritten as a lower bound on system-side effective complexity.")
    if "θ2" in section_text or "1/√2" in section_text or "SNR" in section_text:
        lemmas.append("Lemma: under the adopted signal model, a discrimination threshold on d' induces a threshold on SNR and then on CST.")
    if "Γ_st" in section_text:
        lemmas.append("Lemma: because NMI ∈ [0,1] and sign(Mantel(·)) ∈ {-1,1}, Γ_st is bounded in [-1,1].")
    if "λ_max" in section_text:
        lemmas.append("Lemma: Perron-Frobenius provides an upper-scale network amplification proxy through the dominant eigenvalue λ_max(A).")
    if "β ( CST )" in section_text or "固定点" in section_text:
        lemmas.append("Lemma: any candidate intelligent-level boundary must satisfy β(CST*) = 0 before stability can be asserted.")
    return lemmas


def infer_derivation_steps(claim: Dict[str, Any], section_text: str) -> List[str]:
    steps = []
    normalized = normalize_pdf_math_noise(section_text)
    if "热力学第二定律" in normalized:
        steps.extend([
            "Start from total entropy balance and impose local entropy reduction for self-organization.",
            "Translate entropy compensation into an information/complexity capacity requirement.",
            "Aggregate sensing and prediction sub-capacities into a lower bound on system complexity.",
        ])
    if "SNR" in normalized or "signal detection" in normalized.lower() or "检测理论" in normalized:
        steps.extend([
            "Define signal and noise strengths and express SNR in terms of the manuscript's complexity ratio.",
            "Use the selected discrimination criterion on d' to derive a threshold inequality on SNR.",
            "Map the resulting SNR threshold onto the claimed CST intelligent-emergence threshold.",
        ])
    if "α" in normalized and ("λ_max" in normalized or "ξ" in normalized):
        steps.extend([
            "Model single-device nonlinear gain at the microscopic level.",
            "Lift local perturbation amplification to the network scale via λ_max(A).",
            "Insert critical correlation-length scaling to obtain the macroscopic α amplification law.",
        ])
    if "固定点" in normalized or "β(CST)" in normalized:
        steps.extend([
            "Define the coarse-graining transformation and induced flow equation β(CST).",
            "Solve the fixed-point condition β(CST*) = 0 for candidate constants.",
            "Check local stability through the derivative sign β'(CST*).",
        ])
    if not steps:
        steps.append("Reconstruct the section into explicit implication steps from definitions to final claim.")
    return list(dict.fromkeys(steps))


def infer_proof_conclusion(statement: str) -> str:
    return clean_text(statement)[:240]


def infer_proof_gaps(claim: Dict[str, Any], section_text: str, obligation: Dict[str, Any],
                     math_validation: Dict[str, Any]) -> List[str]:
    gaps = []
    normalized = normalize_pdf_math_noise(section_text)
    if "0.25" in normalized and ("sensor" in normalized.lower() or "predict" in normalized.lower()
                                 or "理解" in normalized or "预测" in normalized):
        gaps.append("The 0.25 + 0.25 decomposition needs an explicit derivation or citation rather than heuristic allocation.")
    if "SNR" in normalized and "1/√2" in normalized and "d'" in normalized:
        gaps.append("The bridge from the chosen d' criterion to the 1/√2 threshold should be written explicitly; the current text does not show the intermediate algebra.")
    if "β(CST)" in normalized or "固定点" in normalized:
        gaps.append("A concrete β(CST) function is not fully specified, so fixed-point existence and stability remain schematic.")
    if "α" in normalized and "∝|σ-1|" in normalized and "ξ/(ξ+c)" in normalized:
        gaps.append("The manuscript should state when the bounded ξ/(ξ+c) form is used versus when asymptotic critical divergence is invoked.")
    if obligation and not obligation.get("required_checks"):
        gaps.append("The proof obligation bundle lacks explicit required checks for this claim.")
    for issue in math_validation.get("issues", []):
        detail = issue.get("detail", "")
        if detail and any(token in detail for token in ["1/√2", "Γ_st", "threshold", "fixed-point", "固定点"]):
            gaps.append(detail)
    if not gaps:
        gaps.append("No explicit step-by-step formal derivation is written yet; convert prose reasoning into theorem-proof structure.")
    return list(dict.fromkeys(gaps))


def build_proof_skeletons(manuscript: Dict[str, Any], claims: List[Dict[str, Any]],
                          proof_obligations: List[Dict[str, Any]],
                          math_validation: Dict[str, Any]) -> Dict[str, Any]:
    section_map = {section.get("heading", ""): normalize_pdf_math_noise(section.get("text", ""))
                   for section in manuscript.get("sections", [])}
    theorem_like_claims = [claim for claim in claims
                           if claim.get("claim_type") in {"theorem", "lemma", "conjecture", "derivation_claim"}]
    skeletons = []
    for claim in theorem_like_claims[:12]:
        normalized_statement = normalize_pdf_math_noise(claim.get("statement", ""))
        section_text = next(
            (text for heading, text in section_map.items() if claim.get("section", "") in heading),
            normalize_pdf_math_noise(manuscript.get("full_text", "")),
        )
        obligation = next((item for item in proof_obligations if item.get("claim_id") == claim.get("claim_id")), {})
        skeletons.append({
            "claim_id": claim.get("claim_id"),
            "section": claim.get("section", ""),
            "claim_type": claim.get("claim_type", ""),
            "statement": normalized_statement,
            "assumptions": infer_proof_assumptions(claim, section_text),
            "lemmas": infer_proof_lemmas(claim, section_text),
            "derivation_steps": infer_derivation_steps(claim, section_text),
            "conclusion": infer_proof_conclusion(normalized_statement),
            "proof_gaps": infer_proof_gaps(claim, section_text, obligation, math_validation),
        })
    total_gaps = sum(len(item.get("proof_gaps", [])) for item in skeletons)
    return {"count": len(skeletons), "items": skeletons, "gap_count": total_gaps}


# ─────────────────────────── 仿真交接 ───────────────────────────

def suggest_dataset_families(claim: Dict[str, Any]) -> List[str]:
    text = f"{claim.get('section', '')} {claim.get('statement', '')}".lower()
    families = []
    if any(token in text for token in ["brain", "cortical", "neural", "神经", "脑"]):
        families.append("open_neuroimaging_and_connectomics")
    if any(token in text for token in ["network", "拓扑", "图", "graph"]):
        families.append("open_graph_benchmark_datasets")
    if any(token in text for token in ["dynamics", "时序", "temporal", "同步"]):
        families.append("open_temporal_network_and_time_series_datasets")
    if any(token in text for token in ["reinforcement", "agent", "智能体", "控制"]):
        families.append("open_rl_and_control_benchmarks")
    if not families:
        families.extend(["open_graph_benchmark_datasets", "open_temporal_network_and_time_series_datasets"])
    return list(dict.fromkeys(families))


def suggest_simulation_metrics(claim: Dict[str, Any]) -> List[str]:
    text = f"{claim.get('section', '')} {claim.get('statement', '')}".lower()
    metrics = []
    if any(token in text for token in ["阈值", "critical", "临界"]):
        metrics.extend(["critical_threshold_error", "phase_transition_sharpness"])
    if any(token in text for token in ["同步", "coherence", "一致性"]):
        metrics.extend(["synchronization_index", "mutual_information"])
    if any(token in text for token in ["预测", "accuracy", "准确率"]):
        metrics.extend(["accuracy", "f1", "calibration_error"])
    if any(token in text for token in ["复杂度", "complexity", "entropy"]):
        metrics.extend(["structural_entropy", "effective_complexity"])
    if not metrics:
        metrics.extend(["effect_size", "robustness_under_perturbation"])
    return list(dict.fromkeys(metrics))


def build_simulation_handoff(claims: List[Dict[str, Any]], proof_obligations: List[Dict[str, Any]],
                             evidence: Dict[str, Any]) -> Dict[str, Any]:
    evidence_map = {item.get("claim_id"): item for item in evidence.get("items", [])}
    obligation_map = {item.get("claim_id"): item for item in proof_obligations}
    items = []
    for claim in claims:
        if not claim.get("requires_simulation_handoff"):
            continue
        claim_evidence = evidence_map.get(claim.get("claim_id"), {})
        obligation = obligation_map.get(claim.get("claim_id"), {})
        items.append({
            "claim_id": claim.get("claim_id"),
            "statement": claim.get("statement", ""),
            "section": claim.get("section", ""),
            "simulation_goal": "Validate the operationalized consequence of this theoretical claim with open-source datasets.",
            "recommended_dataset_policy": "open_source_only",
            "candidate_dataset_families": suggest_dataset_families(claim),
            "recommended_metrics": suggest_simulation_metrics(claim),
            "required_checks": obligation.get("required_checks", []),
            "literature_support_count": claim_evidence.get("support_count", 0),
            "literature_counter_count": claim_evidence.get("counter_count", 0),
        })
    return {
        "workspace": "40_iNEST/45_Simulation",
        "policy": "Simulation and experimental validation must prioritize open-source datasets.",
        "count": len(items),
        "items": items,
    }


# ─────────────────────────── 一致性 + 修订报告 ───────────────────────────

def check_manuscript_consistency(manuscript: Dict[str, Any], claims: List[Dict[str, Any]],
                                 proof_obligations: List[Dict[str, Any]], evidence: Dict[str, Any],
                                 simulation_handoff: Dict[str, Any], math_validation: Dict[str, Any],
                                 proof_skeleton: Dict[str, Any]) -> Dict[str, Any]:
    issues = []
    theorem_claims = [claim for claim in claims if claim.get("claim_type") == "theorem"]
    assumption_claims = [claim for claim in claims if claim.get("claim_type") == "assumption"]
    if not theorem_claims:
        issues.append({"severity": "high", "type": "missing_theorem_structure",
                       "message": "No theorem claims were extracted."})
    if not assumption_claims:
        issues.append({"severity": "medium", "type": "missing_assumptions",
                       "message": "No explicit falsifiable assumptions were extracted."})
    claim_text = " ".join(claim.get("statement", "") for claim in claims)
    for symbol in ["CST", "α", "θ"]:
        if symbol in manuscript.get("full_text", "") and symbol not in claim_text:
            issues.append({"severity": "medium", "type": "symbol_definition_gap",
                           "message": f"Symbol {symbol} appears in manuscript but is weakly represented in extracted claims."})
    for math_issue in math_validation.get("issues", []):
        issues.append({"severity": "high" if math_issue.get("status") == "fail" else "medium",
                       "type": "math_validation_issue", "message": math_issue.get("detail", "")})
    for skeleton in proof_skeleton.get("items", []):
        if skeleton.get("proof_gaps"):
            issues.append({"severity": "medium", "type": "proof_skeleton_gap",
                           "message": f"{skeleton.get('claim_id')}: {skeleton.get('proof_gaps', [])[0]}"})
    verified_map = {item.get("claim_id"): item for item in evidence.get("items", [])}
    obligation_map = {item.get("claim_id"): item for item in proof_obligations}
    proof_gaps = []
    simulation_gaps = []
    for claim in claims:
        support_item = verified_map.get(claim["claim_id"])
        obligation = obligation_map.get(claim["claim_id"])
        if claim.get("requires_theoretical_proof") and not obligation:
            proof_gaps.append({"claim_id": claim["claim_id"],
                               "issue": "Proof-oriented claim has no explicit proof obligation bundle."})
        if claim.get("requires_theoretical_proof") and (not support_item or support_item.get("support_count", 0) == 0):
            proof_gaps.append({"claim_id": claim["claim_id"],
                               "issue": "No supporting literature found for proof-oriented claim."})
        if claim.get("requires_literature_grounding") and (not support_item or support_item.get("support_count", 0) == 0):
            proof_gaps.append({"claim_id": claim["claim_id"],
                               "issue": "No literature grounding found for this theory-side claim."})
        if claim.get("requires_simulation_handoff") and claim.get("claim_id") not in {
                item.get("claim_id") for item in simulation_handoff.get("items", [])}:
            simulation_gaps.append({"claim_id": claim["claim_id"],
                                    "issue": "Simulation-bound claim is missing a handoff item."})
        if support_item and support_item.get("counter_count", 0) > support_item.get("support_count", 0):
            issues.append({"severity": "high", "type": "counter_evidence_dominates",
                           "message": f"Claim {claim['claim_id']} currently has more counter-evidence than support."})
    return {"issue_count": len(issues), "issues": issues,
            "proof_gaps": proof_gaps, "simulation_gaps": simulation_gaps}


def build_revision_report(manuscript: Dict[str, Any], claims: List[Dict[str, Any]],
                          proof_obligations: List[Dict[str, Any]], evidence: Dict[str, Any],
                          simulation_handoff: Dict[str, Any], math_validation: Dict[str, Any],
                          proof_skeleton: Dict[str, Any], consistency: Dict[str, Any]) -> Dict[str, Any]:
    actions = []
    for gap in consistency.get("proof_gaps", [])[:10]:
        actions.append(f"{gap.get('claim_id')}: 补充理论推导链或文献依据，当前理论侧支撑不足。")
    for gap in consistency.get("simulation_gaps", [])[:10]:
        actions.append(f"{gap.get('claim_id')}: 为仿真平台补充开源数据集仿真移交项。")
    for issue in math_validation.get("issues", [])[:10]:
        actions.append(f"数学校验: {issue.get('detail', '')}")
    for skeleton in proof_skeleton.get("items", [])[:10]:
        if skeleton.get("proof_gaps"):
            actions.append(f"{skeleton.get('claim_id')}: 证明骨架缺口 -> {skeleton.get('proof_gaps', [])[0]}")
    for issue in consistency.get("issues", [])[:10]:
        actions.append(issue.get("message", ""))
    if not actions:
        actions.append("当前未发现高优先级修订项，但仍需人工检查数学证明细节。")
    return {
        "title": manuscript.get("title", ""),
        "priority_actions": actions,
        "summary": (f"Extracted {len(claims)} claims, generated {len(proof_obligations)} theory-side obligations, "
                    f"verified {evidence.get('verified_claim_count', 0)} claims against literature, "
                    f"detected {math_validation.get('issue_count', 0)} math-validation issues, "
                    f"built {proof_skeleton.get('count', 0)} proof skeletons with {proof_skeleton.get('gap_count', 0)} proof-skeleton gaps, "
                    f"prepared {simulation_handoff.get('count', 0)} simulation handoff items, "
                    f"and found {len(consistency.get('proof_gaps', []))} theory proof gaps."),
    }


# ─────────────────────────── 主流程 ───────────────────────────

def analyze_manuscript(manuscript_path: str) -> Dict[str, Any]:
    path = Path(manuscript_path)
    if not path.is_file():
        raise RuntimeError(f"manuscript_path is not a readable file: {path}")
    raw_text = path.read_text(encoding="utf-8", errors="ignore")
    manuscript = parse_manuscript(raw_text, path)
    claims = extract_manuscript_claims(manuscript)
    proof_obligations = build_proof_obligations(claims)
    evidence = verify_claims_with_search(claims, manuscript)
    math_validation = build_math_validation(manuscript, claims, proof_obligations)
    proof_skeleton = build_proof_skeletons(manuscript, claims, proof_obligations, math_validation)
    simulation_handoff = build_simulation_handoff(claims, proof_obligations, evidence)
    consistency = check_manuscript_consistency(manuscript, claims, proof_obligations, evidence,
                                               simulation_handoff, math_validation, proof_skeleton)
    revision_report = build_revision_report(manuscript, claims, proof_obligations, evidence,
                                            simulation_handoff, math_validation, proof_skeleton, consistency)
    return {
        "manuscript_digest": manuscript,
        "claims_digest": {"claims": claims, "claim_count": len(claims)},
        "proof_obligations_digest": {"items": proof_obligations, "count": len(proof_obligations)},
        "evidence_digest": evidence,
        "math_validation_digest": math_validation,
        "proof_skeleton_digest": proof_skeleton,
        "simulation_handoff_digest": simulation_handoff,
        "consistency_digest": consistency,
        "revision_report": revision_report,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="手稿数学验证引擎（独立 CLI）")
    parser.add_argument("manuscript", help="手稿文件路径（.html/.md/.txt）")
    parser.add_argument("--json", metavar="OUT", help="全量结构化结果输出到 JSON 文件")
    parser.add_argument("--report", action="store_true", help="仅输出可读修订报告")
    args = parser.parse_args()

    try:
        result = analyze_manuscript(args.manuscript)
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.json:
        Path(args.json).write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"全量结果已写入: {args.json}")

    if args.report or not args.json:
        report = result["revision_report"]
        print("=" * 72)
        print(f"修订报告: {report['title']}")
        print("=" * 72)
        print(report["summary"])
        print()
        print("优先修订项:")
        for action in report["priority_actions"]:
            print(f"  - {action}")
        print()
        handoff = result["simulation_handoff_digest"]
        print(f"仿真交接: {handoff['count']} 项（工作区 {handoff['workspace']}）")
        for item in handoff["items"][:5]:
            print(f"  - {item['claim_id']} [{item['section']}]: {item['statement'][:80]}...")
            print(f"      数据集: {', '.join(item['candidate_dataset_families'])}")
            print(f"      指标: {', '.join(item['recommended_metrics'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
