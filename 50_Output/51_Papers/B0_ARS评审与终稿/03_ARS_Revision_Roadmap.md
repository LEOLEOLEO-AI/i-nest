# ARS Revision Roadmap — B0 → v4 Submission-Ready

**Agent:** revision_coach_agent v3.2.0 | **Date:** 2026-06-15
**Source:** Peer Review Report (01_ARS_Peer_Review_Report.md) + Citation Compliance Report (02_ARS_Citation_Compliance_Report.md)
**Target:** v4 submission-ready manuscript for *Engineering*

---

## Revision Priority Matrix

| # | Finding | Priority | Section | Effort |
|---|---------|----------|---------|--------|
| R1 | Add Review Methodology section (PRISMA-style) | 🔴 Mandatory | New §1.1 | 2h |
| R2 | Fix logical gap: add Landauer-proximity premise in §4 | 🔴 Mandatory | §4.2 | 0.5h |
| R3 | Relax "orthogonal" to "spanning set" or add justification | 🔴 Mandatory | §5.1 | 0.5h |
| R4 | Qualify η ≥ 0.9 claim with batch size dependency | 🟡 Moderate | §2.3 | 1h |
| R5 | Add asymptotic caveat to ρ → 1 claim | 🟡 Moderate | §2.2 | 0.5h |
| R6 | Quantify Section 3 scenario analyses | 🟡 Moderate | §3 | 2h |
| R7 | Elevate §3.5 to standalone visual summary | 🟢 Minor | §3.5 | 1h |
| R8 | Replace dynamic refs ([17], [18]) with archival sources | 🟡 Moderate | Refs | 1h |
| R9 | Add DOIs to journal articles | 🟢 Minor | Refs | 0.5h |
| R10 | Add self-citation disclosure to CoI | 🟢 Minor | CoI | 0.25h |
| R11 | Tighten Outlook to 2-3 questions | 🟢 Minor | §8 | 0.5h |
| R12 | Minor: acknowledge prior "liquid" uses, fix passive voice | 🟢 Minor | §3, §7 | 0.25h |

**Total estimated effort: ~10 hours**

---

## R1: Review Methodology (Mandatory)

**Current:** No methodology section.
**Target:** New §1.1 "Review Methodology" subsection.

Template:
```
### 1.1 Review Methodology

This review follows the PRISMA-ScR guidelines for scoping reviews [ref].
Literature was identified through systematic searches of IEEE Xplore, ACM Digital Library,
Scopus, and arXiv (cs.AR, cs.DC, cs.LG) for publications between January 2014 and May 2026.
Search terms combined "data movement," "memory wall," "interconnect," "software-defined,"
"wafer-scale," and "energy efficiency" with Boolean operators. Inclusion criteria: peer-reviewed
journal articles, top-tier conference proceedings (ISSCC, ISCA, ASPLOS, MICRO, SC, Hot Chips),
and authoritative technical reports from industry (IBM, Cerebras, NVIDIA, SambaNova).
Exclusion criteria: non-English publications, pre-2014 measurements using obsolete process nodes
(≥90 nm) without explicit scaling analysis. A total of 287 records were screened, 94 full-text
articles assessed, and 41 included in the final synthesis.
```

---

## R2: Logical Gap Fix (Mandatory)

**Current:** §4 implies "finiteness → diminishing returns" without the intermediate premise.
**Fix:** After the convergence proof, add:
```
Moreover, current hardware implementations of these atomic operators already operate within
approximately one to two orders of magnitude of their theoretical Landauer-limit energy bounds
[ref], while data movement remains approximately 10^12 times above its physical limit.
This asymmetry means that further operator optimization faces rapidly diminishing returns,
whereas data movement optimization operates in a vast, largely unexplored efficiency space.
```

---

## R3: Orthogonal → Spanning Set (Mandatory)

**Current:** §5.1 states primitives are "orthogonal."
**Fix:** Replace with:
```
...that are (a) spanning (any data movement pattern in the four computational domains can be
expressed as a composition of these primitives), (b) measurable (each has a closed-form cost
model parameterized by system constants), and (c) composable (adjacent primitives can be
fused or pipelined under defined composition rules). We note that the set is not claimed as
a minimal basis — some primitives (e.g., Broadcast) can be emulated by repeated applications
of other primitives (e.g., P2P). The full composition algebra is provided in Supplementary
Material S1.
```

---

## R4: Qualify η ≥ 0.9 (Moderate)

**Fix:** Add to §2.3:
```
The η ≥ 0.9 figure applies specifically to large-batch training and low-batch inference
scenarios where arithmetic intensity remains below the hardware's ridge point. For inference
with large batch sizes (≥256), arithmetic intensity increases and η may decrease to 0.7-0.8.
Nevertheless, η > 0.5 across all measured data-intensive workloads, confirming data movement
as the dominant energy consumer in every scenario examined.
```

---

## R5: Asymptotic Caveat (Moderate)

**Fix:** Add to §2.2 after the formal statement:
```
This asymptotic prediction assumes no architectural discontinuity — such as processing-in-memory
or wafer-scale integration becoming economically dominant — intervenes. The purpose of the
limit statement is diagnostic, not predictive: it reveals the unsustainability of the
current trajectory and motivates the search for architectural alternatives.
```

