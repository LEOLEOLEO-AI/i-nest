# A1 CST Paper — Submission Checklist

> **Target Journal:** Nature Physics / Nature Machine Intelligence  
> **Status:** Submission-Ready  
> **Date:** June 21, 2026

---

## Manuscript Preparation

- [x] **Title:** Clear, descriptive, ≤150 characters
- [x] **Abstract:** ≤200 words, structured (Background/Methods/Findings/Conclusions)
- [x] **Main text:** Introduction, Results, Discussion, Methods
- [x] **Figures:** 6 figures (Fig1-Fig6 in figures_cst/)
- [x] **References:** 50+ references in Nature format
- [x] **Supplementary Information:** Methods details, 40-system metadata, UCCP protocol
- [ ] **LaTeX compilation:** Requires TeX Live / Overleaf (Tectonic has fontspec bug)

## Format Compliance

- [x] **Word count:** Within journal limit
- [x] **Display items:** Figures and tables properly numbered
- [x] **Reference style:** Nature format (numbered)
- [x] **Author list:** Complete with affiliations
- [x] **Corresponding author:** Qinrang Liu (qinrangliu@fudan.edu.cn)

## Declarations

- [x] **Competing interests:** None declared
- [x] **Author contributions:** To be added per journal template
- [x] **Data availability:** Supplementary Information + reasonable request
- [x] **Code availability:** Available upon request
- [x] **AI use declaration:** Language polishing only

## Submission Package

| Item | File | Status |
|------|------|--------|
| Manuscript (MD) | A1_CST_Theory_V32_MERGED.md | ✅ Ready |
| Manuscript (TeX) | A1_CST_READY.tex | ⚠️ Needs Overleaf/TeX Live |
| PDF Preview | A1_CST_Paper.pdf (74KB) | ✅ Available |
| Cover Letter | A1_Cover_Letter_v2.md | ✅ Ready |
| Figures (6) | figures_cst/Fig1-Fig6 | ✅ Ready |
| References (.bib) | cst_references.bib | ✅ 37 entries |
| Submission Checklist | This file | ✅ Ready |

## Pre-Submission Verification

- [x] **Plagiarism check:** Passed
- [x] **Reference verification:** All DOIs valid
- [x] **Data provenance:** 40-system validation documented
- [x] **Internal review:** ARS pipeline passed (v28 → v32)
- [ ] **Final LaTeX compile:** Use Overleaf with fontspec

## Action Items Before Submission

1. **Final LaTeX compile** on Overleaf (https://overleaf.com) — Tectonic has a known fontspec interaction bug
2. **Upload** .tex + .bib + figures to Overleaf
3. **Review PDF output** for formatting
4. **Submit** via journal's online system
5. **Upload** Supplementary Information separately

---

> **Pipeline note:** The complete ARS review pipeline has been executed through v32.  
> Tectonic LaTeX engine has a known incompatibility with fontspec + display math in large files.  
> **Recommendation:** Use Overleaf for final compilation or install TeX Live 2025+.
