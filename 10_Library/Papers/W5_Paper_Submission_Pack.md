# W5 Paper Submission Pack + DVS Experiment Guide
# ==============================================

## Paper 52: Cross-Species CST Validation — Submission Checklist

Status: Draft complete (Obsidian V25 FINAL). Needs final polish.
Target: Physical Review Letters (primary), eLife (backup)

### Pre-submission checklist
- [ ] Insert SDI sigma scan data (N=192 sigma>=4.0, N=1024 S_eff=27x)
- [ ] Insert RG flow data (N=128->8, fixed point step 3-4)
- [ ] Update Spearman rho from 0.90 to 0.976 (V25 has this)
- [ ] Format for PRL: 3750 words max, 5 figures, 50 references
- [ ] Create PRL cover letter emphasizing:
  - First quantitative validation of von Neumann complexity threshold
  - 40-system cross-validation with natural constant thresholds
  - Direct engineering implications for AGI hardware roadmap
- [ ] Register on arXiv as preprint before journal submission

### Cover letter draft
"We submit 'From Compute to Complexity: A Physical Theory of Intelligence
Emergence' for consideration in Physical Review Letters. This paper presents
the first quantitative framework resolving von Neumann's 1948 complexity
threshold conjecture, with 40-system cross-validation (Spearman rho=0.976).
The theory predicts six universal intelligence thresholds at natural constants
and has been independently validated through SDI topology simulations (sigma
scan N=64-1024, RG flow analysis). We believe this work establishes the
physical foundations for a new paradigm of complexity-driven intelligence
emergence, with direct implications for next-generation AI hardware design."

## Paper P-Theory v2 — Submission Checklist

Status: Full draft + simulation supplement. Needs integration.
Target: JMLR / NeurIPS (ML+systems track)

### Pre-submission checklist
- [ ] Merge simulation supplement (P-Theory_v2_Simulation_Supplement.md) as Section 4.3
- [ ] Add explicit CST mapping (Section 4.3.2 from supplement)
- [ ] Add engineering parameter table (Section 4.3.3)
- [ ] Format for JMLR: double-column, 8-12 pages
- [ ] Register on arXiv

## Paper CST RG — Writing Checklist

Status: Protocol exists. Full paper needs writing.
Target: PRL / Communications Physics

### Writing plan
- Section 1-2: Merge from CST_Axiomatization_Outline.md
- Section 3: CST RG Protocol content (device physics derivation)
- Section 4: MC simulation validation (can use multiscale.py RG flow data)
- Section 5: Discussion + Landauer bound implications

## Haihe V3 Update Notes

Key additions from current work:
1. SDI sigma scan results: N=192 achieves sigma>=4.0, N=1024 achieves S_eff=27x
2. CST cross-species validation: Spearman rho=0.976 (updated from 0.90)
3. SDI simulation platform: 4 experiments complete, engineering parameters determined
4. Minimum SDI scale: N>=192 chiplets for adaptive intelligence emergence

## DVS Experiment Guide

Status: Code exists (D:\\iNEST\\Write\\Code\\MNoB\\scripts\\train_dvs.py). Needs:
1. Download real DVSGesture dataset (tonic library)
2. Run with 128x128 frames: python scripts/train_dvs.py --height 128 --width 128 --epochs 50
3. Expected: acc > 0.5 on real data (vs 0.17-0.33 on synthetic)
4. Output: loss/acc curves + confusion matrix

