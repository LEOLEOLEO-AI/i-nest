# ARS Citation Compliance Report — A1 CST Theory

**Agent:** citation_compliance_agent v3.2.0 | **Target Format:** Vancouver (numbered, square brackets) | **Date:** 2026-06-19

---

## Audit Results

| Check | Status | Detail |
|-------|--------|--------|
| Orphan detection | PASS | All 61 references cited in text, all in-text citations correspond to reference list entries |
| Reference range | PASS | [1]-[61] sequential, no gaps |
| DOI completeness | PARTIAL | 28/61 references include DOI. Classic books ([2], [43], [44]) and preprints ([31], [33], [35]-[37]) acceptable without DOI. Recommend adding DOIs for journal articles where missing. |
| Format consistency | PASS | Vancouver square-bracket style applied uniformly. Author-year format consistently "Person et al. (Year)" or [N]. |
| Self-citation disclosure | MISSING | No explicit self-citation statement. If any of [1]-[61] are by the authors, this must be disclosed in Conflict of Interest. |
| URL accessibility | UNVERIFIED | arXiv preprints ([31], [33], [35]-[37]) should be verified for latest versions before submission. |
| Preprint handling | PASS | arXiv references correctly marked with arXiv ID. |
| Non-English sources | N/A | All references appear to be English-language publications. |
| Retraction check | UNVERIFIED | Recommend running all PMID/DOI through Retraction Watch database before submission. |

---

## Reference-By-Reference Spot Check

| Ref | Type | Format OK? | DOI? | Notes |
|-----|------|------------|------|-------|
| [1] Hoel 2017 Entropy | Journal | YES | YES | Correct |
| [2] Sporns 2010 | Book | YES | NO | Classic — acceptable without DOI |
| [3] Bassett & Sporns 2017 | Journal | YES | YES | Correct |
| [4] Tononi et al. 2016 | Journal | YES | YES | Correct |
| [5] Barrett & Mediano 2019 | Journal | YES | YES | Correct |
| [6] Beggs & Plenz 2003 | Journal | YES | YES | Correct |
| [7] Shew et al. 2009 | Journal | YES | YES | Correct |
| [8] Watts & Strogatz 1998 | Journal | YES | YES | Correct |
| [11] Varshney et al. 2011 | Journal | YES | YES | Key C. elegans reference |
| [19] White et al. 1986 | Journal | YES | YES | Classic C. elegans connectome |
| [20] Scheffer et al. 2020 | Journal | YES | YES | Drosophila connectome reference |
| [25] Van Essen et al. 2013 | Journal | YES | YES | HCP reference |
| [30] Brown et al. 2020 | Conference | YES | NO | GPT-3 NeurIPS paper; verify DOI |
| [31] Kaplan et al. 2020 | arXiv | YES | YES | Scaling laws — verify latest version |
| [42] Low et al. 2012 | Declaration | YES | NO | Cambridge Declaration — unique source, acceptable |
| [43] Hebb 1949 | Book | YES | NO | Classic — acceptable without DOI |
| [44] von Neumann 1966 | Book | YES | NO | Classic — acceptable without DOI |
| [45] Turing 1936 | Journal | YES | NO | Classic — acceptable |
| [51]-[61] | Various | YES | Mixed | New v20 additions — verify all |

---

## Priority Actions

| Priority | Action |
|----------|--------|
| HIGH | Add self-citation disclosure to Conflict of Interest section |
| MEDIUM | Add DOIs to journal articles currently missing them (estimate ~15) |
| MEDIUM | Verify arXiv preprints [31], [33], [35]-[37] are latest versions |
| LOW | Pre-submission retraction check via Retraction Watch |
| LOW | Verify [42] Cambridge Declaration is citable as academic reference |
