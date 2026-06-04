# iNEST Three Core Papers Gap Analysis and Priority Actions
# =========================================================
# Date: 2026-06-04

## Paper 1: CST V25 FINAL

Status: Complete draft, 40-system validated, Spearman rho=0.976
Target: Nature / Science / Nature Machine Intelligence

Gaps:
1. SDI simulation data integration needed
2. CST N=1024 sigma scan figure missing
3. RG flow visualization missing
4. Cross-species connectome data from paper 52 not integrated

Priority: Run cst_phase_scan.py -> insert sigma scan figure

## Paper 2: P-Theory v2 (Meta-Topology + SDI-Bond)

Status: Complete draft, 8 sections, completeness theorem proven
Target: JMLR / NeurIPS / PRL

Gaps:
1. Computational validation of completeness theorem needed
2. CST connection not explicitly stated
3. Concrete engineering numbers from SDI exp1 not integrated
4. SDI experiments 2-4 results missing

Priority: Insert SDI_Simulation_Supplement.md as Section 4.3

## Paper 3: CST RG First-Principles Protocol

Status: Protocol/outline, not yet full paper
Target: PRL / Communications Physics

Gaps:
1. Full paper not written (outline only)
2. Monte Carlo simulations not executed
3. Literature meta-analysis not performed
4. multiscale.py RG flow data not connected

Priority: Expand into full PRL manuscript using CST_Axiomatization_Outline.md

## Immediate Actions (when Python env restored)

```powershell
python cst_phase_scan.py        # CST N=1024 scan for paper 1
python run_exps.py              # SDI exps 2-4 for paper 2
python multiscale.py            # RG flow for paper 3
```
