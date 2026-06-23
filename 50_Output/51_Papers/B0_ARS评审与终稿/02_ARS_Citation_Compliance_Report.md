# ARS Citation Compliance Report — B0

**Agent:** citation_compliance_agent v3.2.0 | **Target Format:** Vancouver (numbered, square brackets) | **Date:** 2026-06-15

---

## Audit Results

| Check | Status | Detail |
|-------|--------|--------|
| Orphan detection | ✅ PASS | All 41 references cited in text, all in-text citations in reference list |
| Reference range | ✅ PASS | [1]-[41] sequential, no gaps |
| DOI completeness | ⚠️ PARTIAL | 15/41 references include DOI. Conference proceedings (e.g., ISSCC, ISCA) often lack DOIs — acceptable. Recommend adding DOIs for journal articles where available. |
| Format consistency | ✅ PASS | Vancouver square-bracket style applied uniformly. Author-year format consistently Person et al. (Year) or [N]. |
| Self-citation disclosure | ⚠️ MISSING | No explicit self-citation statement. If any of [1]-[41] are by the authors, this must be disclosed in Conflict of Interest. |
| URL accessibility | ⚠️ UNVERIFIED | IBM Research Blog [17] and Cerebras press release [19] are dynamic URLs. Verify they resolve or replace with permanent identifiers. |
| Preprint handling | ✅ PASS | arXiv references (e.g., [11], [22]) correctly marked with arXiv ID. |
| Non-English sources | N/A | All references appear to be English-language publications. |
| Retraction check | ⚠️ UNVERIFIED | Recommend running all PMID/DOI through Retraction Watch database before submission. |

---

## Reference-By-Reference Check

| Ref | Type | Format OK? | DOI? | Notes |
|-----|------|------------|------|-------|
| [1] Horowitz ISSCC 2014 | Conference | ✅ | ❌ | IEEE Xplore likely has DOI |
| [2] Kuhn 1962 | Book | ✅ | ❌ | Classic — acceptable without DOI |
| [3] Stillmaker & Baas 2017 | Tech Report | ✅ | ❌ | UC Davis TR; verify availability |
| [4]-[8] | Journal/Conf | ✅ | Mixed | Standard format |
| [9] OPT-175B training log | Report | ⚠️ | ❌ | Consider citing NeurIPS 2022 paper instead |
| [10] Narayanan et al. 2021 | Conf (SC) | ✅ | ❌ | Check ACM DL for DOI |
| [11] Meta Llama 3 report | arXiv | ✅ | ✅ | Format correct |
| [12] HPCG benchmark | Standard | ✅ | N/A | Cite HPCG website or primary publication |
| [13] ExaNeSt project | Project | ⚠️ | ❌ | Verify primary publication exists |
| [14]-[16] Edge AI | Conf/Journal | ✅ | Mixed | — |
| [17] IBM Research Blog | Blog | ⚠️ | ❌ | Dynamic URL — archive or replace with NorthPole ISCA 2024 paper |
| [18] Cerebras WSE-3 | Press Release | ⚠️ | ❌ | Replace with Hot Chips 2024 presentation |
| [19]-[41] | Various | ✅ | Mixed | Format consistent |

---

## Priority Actions

| Priority | Action |
|----------|--------|
| 🔴 High | Replace blog/press-release refs ([17], [18]) with archival publications where available |
| 🟡 Medium | Add DOIs to journal articles (15 currently missing) |
| 🟡 Medium | Verify [3], [13] are accessible primary sources |
| 🟢 Low | Add self-citation disclosure to Conflict of Interest |
| 🟢 Low | Pre-submission retraction check via Retraction Watch |

