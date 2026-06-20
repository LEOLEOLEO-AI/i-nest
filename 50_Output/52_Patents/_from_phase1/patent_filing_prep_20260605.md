# iNEST Patent Priority Filing — Preparation Package
**Date**: 2026-06-05 | **Status**: Ready for attorney consultation

---

## Priority Patents (Filing: Q3 2026, CN/US/PCT)

### P1: 4-Type Compound-Bond Architecture [PRIORITY ★★★]

**Technical Field**: Neuromorphic computing hardware architecture

**Core Claims**:
1. A neural network interconnect architecture comprising four independent physical bond types (E, L, S, C) with N dynamically configurable channels per type
2. Two SYN interfaces (input/output) for external system integration
3. A finite state machine controlling bond type transitions based on Hebbian learning signals (LTP/LTD)
4. Each bond type implemented as an independent physical channel with dedicated conductance control

**Novelty**:
- Existing neuromorphic interconnects (Loihi, TrueNorth) use homogeneous synaptic channels
- The 4-type architecture enables simultaneous heterogeneous plasticity regimes
- Physical separation of bond types prevents cross-interference during learning

**Supporting Data**:
- SDI simulation results (v22-v30): EL ratio convergence to 15-35% golden zone
- CST validation: 40-system Spearman ρ=0.976
- Multi-region V30: pattern memory 100%, phototaxis PI=0.811

### P2: FEP-Driven Autonomous Bond Management [PRIORITY ★★★]

**Technical Field**: Self-organizing neural network plasticity

**Core Claims**:
1. A method for autonomous synapse management wherein each node computes a local free energy F_i = Σ[(pred_err)² + Ea·w²]
2. Decisions to consolidate (strengthen), prune (weaken), or create new synaptic connections based on F_i local minima detection
3. The F_i computation is purely local (no global optimization or backpropagation)

**Novelty**:
- Existing plasticity rules (STDP, BCM) modify existing weights but don''t autonomously create/prune connections
- FEP provides a principled, local, energy-based criterion for structural plasticity
- No supervised signal or reward function required

**Supporting Data**:
- V29 functional emergence: phototaxis PI=1.000, chemotaxis CI=1.000 at N=558 — purely FEP-driven, no reward
- V30 multi-region: cross-region bonds autonomously formed via FEP

### P3: STDP-FEP Gradient Descent Mapping [PRIORITY ★★★]

**Technical Field**: Mathematical mapping between biological and optimization-based learning

**Core Claims**:
1. A formal proof that STDP weight updates (Δw_STDP) are equivalent to gradient descent on the FEP free energy: Δw_STDP = -η · ∂F/∂w
2. LTP (long-term potentiation) corresponds to reducing prediction error (∂F_pred/∂w)
3. LTD (long-term depression) corresponds to reducing complexity cost (∂F_complex/∂w)

**Novelty**:
- Unifies two historically separate learning paradigms (Hebbian/STDP and optimization/backprop)
- Provides theoretical justification for local learning in neuromorphic hardware without backpropagation
- Enables formal convergence analysis of STDP through gradient descent theory

**Supporting Data**:
- V25-V30 simulation results showing convergence of F_local and EL ratio
- Mathematical derivation in A1 CST Theory paper §3.1.1

---

## Pre-Filing Action Items

### Immediate (This Week)
- [ ] Schedule meeting with patent attorney (recommended: Linda Liu & Partners or Liu Shen & Associates)
- [ ] Prepare Chinese-language technical disclosure documents for P1-P3
- [ ] Finalize English abstract translations for PCT filing

### Week 2
- [ ] Prior art search results from attorney
- [ ] Detailed claims drafting session
- [ ] Review and finalize invention disclosure forms

### Week 3-4
- [ ] File CN provisional applications (secures priority date)
- [ ] Begin US/PCT translation
- [ ] Academic publication embargo: DO NOT publish A1 CST Theory before provisional filing

---

## Academic Publication Coordination

**CRITICAL**: The A1 CST Theory paper (V27_FINAL, ready for submission) MUST NOT be submitted to any journal or preprint server before P1-P3 provisional patents are filed.

| Patent | Related Paper | Filing Before Publication? |
|--------|-------------|---------------------------|
| P1 (4-Type Bond) | A1 CST Theory | ✅ Must file first |
| P2 (FEP Management) | A1 CST Theory §3.1.1 | ✅ Must file first |
| P3 (STDP-FEP Mapping) | A1 CST Theory §Theory | ✅ Must file first |
| P4 (SOC Convergence) | A1 CST Theory | ⚠️ Q4 2026 |
| P5 (BCM+Surprise) | Future paper | ⚠️ Q4 2026 |

---

## Estimated Timeline

| Milestone | Target Date | Dependency |
|-----------|------------|------------|
| Attorney consultation | June 10, 2026 | — |
| Prior art search complete | June 20, 2026 | Attorney engaged |
| CN provisional filed | June 30, 2026 | Claims drafted |
| A1 paper submitted | July 1, 2026 | CN provisional filed |
| PCT application filed | September 30, 2026 | CN provisional + translation |
| US non-provisional | December 31, 2026 | PCT filing |
