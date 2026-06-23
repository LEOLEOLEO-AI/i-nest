# ARS Peer Review Report — B0 Engineering Submission

**Framework:** academic-research-skills v3.2.0 — 5-Dimension Scoring | **Date:** 2026-06-15
**Paper:** B0 — "From von Neumann to Network-Centric: A First-Principles Review of the Computing Paradigm Migration toward Sustainable Intelligent Computing"
**Target:** *Engineering* Special Issue on Sustainable Intelligent Computing

---

## Reviewer Panel

| Role | Perspective | Focus |
|------|-------------|-------|
| **EIC** | Editor-in-Chief | Overall contribution, special issue fit, impact |
| **R1** | Computer Architecture | Technical accuracy, prior work coverage |
| **R2** | Sustainable Computing | Energy quantification, sustainability claims |
| **R3** | Complex Systems | Conceptual coherence, interdisciplinary rigor |
| **DA** | Devil's Advocate | Logical fallacies, overclaims, counter-arguments |

---

## Five-Dimension Scoring

| Dimension | Weight | Score | Notes |
|-----------|--------|-------|-------|
| Originality | 20% | **8/10** | "Data-Movement Dominance Law" formal statement is novel. Meta-primitive taxonomy is genuinely useful. "Orthogonal" claim needs mathematical justification or should be relaxed to "spanning set." |
| Methodological Rigor | 25% | **6/10** | ⚠️ Lacks explicit Review Methodology section (PRISMA-style search strategy, inclusion/exclusion criteria). This is standard for *Engineering* Reviews and must be added. |
| Evidence Sufficiency | 25% | **8/10** | Five measurement regimes cited with specific numbers. Section 3 scenario analyses are qualitative — would benefit from quantified case studies with energy breakdown percentages. |
| Argument Coherence | 15% | **9/10** | Strong red thread: problem → diagnosis → formal law → solution → outlook. Each section builds on the previous. The DMD Law in Section 2 is an effective pivot. |
| Writing Quality | 15% | **8/10** | Clear, confident English. Active voice throughout. Minor: two instances of passive construction in Section 3; one dangling reference. |
| **Weighted Total** | **100%** | **7.7/10** | **Major Revision** recommended |

---

## Detailed Findings

### Section 1 — Introduction

- **R1 (Strengths):** Effective framing of three walls unified as "Data Movement Wall." Kuhn paradigm shift reference adds intellectual depth.
- **DA (Concern):** The claim "90% of energy is wasted on data movement" appears three times before Section 2 provides systematic evidence. Repetition weakens impact. **Fix:** State once in Abstract, defer full evidence to Section 2.
- **R1 (Minor):** [1] is ISSCC 2014 presentation. Consider also citing Horowitz, IEEE Micro 2015 for broader accessibility.

### Section 2 — The Data-Movement Dominance Law

- **R1, R2 (Strengths):** Formal statement (2.2) is the paper's strongest intellectual contribution. The inequality chain is elegant and verifiable.
- **R2 (Moderate):** The claim "η ≥ 0.9 for AI workloads" needs qualification. For high-batch-size inference, arithmetic intensity increases and η may be lower (e.g., 0.7-0.8). Add a paragraph on η range and batch size dependency.
- **DA (Moderate):** "ρ → 1 as N → ∞" assumes current architectural assumptions hold indefinitely. This is a strong asymptotic claim. **Fix:** Add caveat: "under the assumption that no architectural discontinuity (e.g., processing-in-memory becoming dominant) intervenes."

### Section 3 — Data Movement Anatomy

- **R1, R3 (Strengths):** Four-scenario taxonomy is well-chosen and comprehensive.
- **R2 (Minor):** Section 3.1 would benefit from a concrete example — e.g., a SPEC CPU2017 benchmark breakdown showing L1/L2/L3/DRAM energy proportions.
- **R3 (Recommended):** Section 3.5 (Cross-Scenario Synthesis) should be a standalone visual summary (table or figure) mapping η values across all four scenarios.

### Section 4 — Operator Space Convergence

- **R1 (Strengths):** Finite atomic operator proof (4.1) and universality argument (4.2) are rigorous and well-referenced.
- **DA (Moderate ⚠):** Logical gap between "operators are finite" and "ergo, optimizing operators has diminishing returns." Finiteness does not logically imply optimization is impossible — only that the space is bounded. **Fix:** Add the missing premise: "Current hardware implementations of these operators are already within an order of magnitude of their Landauer-limit energy bounds."

### Section 5 — Meta-Primitives

- **R1, R3 (Strengths):** 11 meta-primitives in three categories are genuinely useful. Cost model (5.2) provides computability.
- **R1 (Moderate):** Claim that primitives are "orthogonal" needs proof. Some primitives are compositional (Broadcast = repeated P2P). **Fix:** Either provide orthogonality proof, or relax to "spanning set" terminology with explicit composition rules.

### Section 6 — Software-Defined Interconnect

- **R1 (Strengths):** SDI architecture (6.2) and benefit threshold (6.3) are well-specified.
- **R2 (Minor):** Section 6.4 (Wafer-Scale) needs ballpark quantitative estimates. Even order-of-magnitude estimates strengthen the argument significantly.

### Section 7 — Liquid Architecture

- **R3 (Strengths):** Unification of six pathways (7.3) is conceptually elegant.
- **DA (Minor):** "Liquid" metaphor has prior uses (DARPA programs). **Fix:** Acknowledge prior uses and differentiate the specific meaning here. *(Note: the Genspark脱敏 strategy already addresses this — ensure this distinction is explicit in the paper.)*

### Section 8 — Outlook

- **EIC (Minor):** Too ambitious — reads like a grant proposal's future work. **Fix:** Tighten to 2-3 most important questions; move remaining to Supplementary.

---

## Editorial Decision

**Verdict: Major Revision**

The paper makes a clear, original contribution to "Sustainable Intelligent Computing." The DMD Law formal statement and 11 meta-primitives are the strongest elements. Three mandatory changes:

1. **Add Review Methodology section** (PRISMA-style: search strategy, databases, inclusion/exclusion criteria) — standard for *Engineering* Reviews.
2. **Fix logical gap in Section 4** — add missing premise about Landauer proximity of current operators.
3. **Relax "orthogonal" to "spanning set" or prove orthogonality** — Section 5.

**Resubmission encouraged within 4 weeks.**

