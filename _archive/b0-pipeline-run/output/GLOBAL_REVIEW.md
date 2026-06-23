# B0 v6 Global Review — Engineering Journal Simulated Peer Review
**Pipeline:** arxiv-survey | **Stage:** C4 | **Reviewer:** WILLOSCAR global-reviewer
**Date:** 2026-06-17

---

## Reviewer Recommendation: **MINOR REVISION** (Accept with minor changes)

---

## Overall Assessment

This is a **well-structured, evidence-rich scoping review** that makes a compelling case for a paradigm shift from node-centric to network-centric computing. The paper successfully bridges empirical measurements, formal modeling, and architectural proposals. Its strongest contribution is the **Data-Movement Dominance Law** and the **SDI architectural framework**, both of which are novel and well-supported.

---

## Section-by-Section Review

### Highlights (5 items)
**Score: 4/5** — Concise, measurable, specific. Item 5 ("six non-von-Neumann pathways") could be more precise about what "sustainable computing" means here.

### Abstract
**Score: 4/5** — Clear narrative arc. Could tighten the last sentence (currently editorializing). Suggest: "Tackling the 90% data-movement bottleneck, rather than iterating on the 10% computational component, offers the highest-leverage path toward sustainable intelligent computing."

### 1. Introduction
**Score: 4/5** — Strong hook (八十年/80 years). Appropriate scope declaration (scoping review, not systematic review). The mention of PRISMA-ScR compliance is excellent.

### 2. First Principles Decomposition
**Score: 5/5** — This is the paper's intellectual core. The formal statement of the Data-Movement Dominance Law is crisp and falsifiable. The multi-source evidence (Eyeriss, OPT-175B, HPCG, edge AI) provides convincing triangulation. Section 2.3's three implications are logically tight.

**Minor issue:** 畏=0.9 should be explicitly tied to the empirical sources. Currently reads as a derived claim without direct citation anchoring.

### 3. Four Computing Scenarios
**Score: 4/5** — Good breadth. Could benefit from a summary comparison table showing energy fractions across all four scenarios side-by-side.

### 4. Operator Space Convergence
**Score: 4/5** — The CORDIC-Weierstrass argument is elegant. The "鈮?0 primitives" bound is bold; consider adding a table enumerating them explicitly.

### 5. Data Movement Meta-Primitives
**Score: 5/5** — This is the strongest technical contribution. The 11-meta-primitive taxonomy with formal cost model is original and practically useful. The five canonical transformations (E/D/V/C/T) provide a clean optimization framework. This section alone could justify a separate architecture paper.

### 6. SDI Architecture
**Score: 4/5** — Clear and well-motivated. The four-component architecture (PIM, Primitive Scheduler, Protocol Adapter, Topology Compiler) is well-defined. 

**Missing:** No comparison with existing reconfigurable interconnects (e.g., Intel's EMIB, AMD's Infinity Fabric, NVIDIA's NVSwitch). A short comparison paragraph would strengthen credibility.

### 7. Liquid Unified Architecture
**Score: 3/5** — Ambitious but less grounded than preceding sections. The "six non-von-Neumann pathways" claim is broad. Reference [29] (in preparation) is a RED FLAG for a journal submission.

**Critical issue:** The dependency on unpublished work [29] must be resolved before submission. Either (a) publish [29] on arXiv with a permanent identifier, or (b) fully self-contain the argument within this paper.

### 8. Topological Center Computing
**Score: 3/5** — The formalization is a good start but feels incomplete. The sphere-packing bound is standard; the SDI-related theorems need more development. This section reads more like a research proposal than a review finding.

### 9. Outlook
**Score: 4/5** — Five concrete, falsifiable research agendas. Excellent fit for Engineering's "Outlook" convention. Each agenda is specific enough to be actionable.

### 10. Conclusion
**Score: 4/5** — Clear restatement. Could be slightly more forward-looking (what's the first experiment to run?).

---

## Quality Dimensions

| Dimension | Score | Notes |
|---|---|---|
| Novelty | 8/10 | SDI framework + 畏 law are novel; some sections retread known ground |
| Rigor | 7/10 | Strong empirical base; [29] dependency is a weakness |
| Clarity | 8/10 | Well-organized; some long paragraphs could be broken |
| Impact | 9/10 | Timely for "Sustainable Intelligent Computing" special issue |
| Completeness | 7/10 | Section 8 feels incomplete; missing comparison with existing fabrics |

---

## CRITICAL FIXES (Must address before submission)

1. **Resolve reference [29]:** Publish companion paper on arXiv OR remove dependency
2. **Section 6 comparison table:** Add 3-5 row comparison with NVSwitch, EMIB, Infinity Fabric
3. **畏=0.9 anchoring:** Add explicit citation to the measurements that support this boundary

## IMPORTANT IMPROVEMENTS (Should address)

4. **Section 8 development:** Expand formal treatment or narrow scope claim
5. **Vendor white paper alternatives:** Add peer-reviewed sources for [14,15,21,31,32] where possible
6. **Section 3 summary table:** Add comparative energy-fraction table across four scenarios
7. **SDN literature grounding:** Cite McKeown et al. 2008 (OpenFlow) in Section 6.1

## MINOR POLISH

8. Break paragraphs >15 lines for readability
9. Check all figure cross-references (currently says "See Fig. X" without numbers in some spots)
10. Verify Chinese abstract matches English abstract precisely

---

## Verdict

**This paper is close to submission-ready.** The intellectual core (Sections 2, 5, 6) is strong. The critical blocker is reference [29]. With the 3 critical fixes applied, this paper has a high probability of acceptance at Engineering's Sustainable Intelligent Computing special issue.
