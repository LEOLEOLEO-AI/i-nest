---
created: '2026-05-01T01:10:25+00:00'
evidence:
- stage-02/problem_tree.md
id: problem_decompose-rc-20260501-010756-7b872d
run_id: rc-20260501-010756-7b872d
stage: 02-problem_decompose
tags:
- problem_decompose
- stage-02
- run-rc-20260
title: 'Stage 02: Problem Decompose'
---

# Stage 02: Problem Decompose

# Route≡Transform: Research Decomposition
## Isomorphism Between Communication and Computation Primitives — NCC-11 Completeness and Minimality

---

## Source

**Research Goal Document**: *Route≡Transform: Formal Isomorphism between Communication Primitives and Computation Primitives on Reconfigurable Interconnect Fabrics for Topology-Centric Computing — Completeness and Minimality of the NCC-11 Primitive Set*
**Project**: iNEST-NCC-Research | **Draft Stage**: Stage 01 (unverified — benchmark names and SOTA claims are LLM-generated estimates pending literature verification)
**Decomposition Date**: 2025-07-14

> **Methodological Note**: The sub-questions below are ordered by *logical dependency*, not merely by importance. A failure or negative result in an earlier sub-question materially changes the scope and framing of all subsequent ones. Each sub-question is therefore both a research deliverable and a **decision gate**.

---

## Sub-questions

---

### SQ-1 — Algebraic Foundation: What Formal Structure Governs the Route≡Transform Correspondence?

**Full Statement**: What is the minimal algebraic structure (e.g., monoid, semiring, symmetric monoidal category, or Kleene algebra) that simultaneously captures both collective communication primitives (AllReduce, AllGather, Broadcast, AllToAll) and computation primitives (GEMM, Reduce, Scan, Map) as elements or morphisms, such that reconfigurable interconnect topology changes correspond to well-defined algebraic operations within that structure — and under what conditions does a non-trivial isomorphism between the communication sub-algebra and the computation sub-algebra exist?

**Motivation**: This is the foundational question. Without a precisely specified algebraic structure, "isomorphism" is a metaphor rather than a theorem. The choice of structure is non-obvious: if the correct structure is a symmetric monoidal category, the proof machinery differs entirely from a semiring treatment, and the notion of "completeness" (SQ-2) depends on what the algebra can express. Critically, the reconfigurability assumption — the paper's core differentiator from MPI algebraic specifications — must be encoded structurally here, not added as an afterthought.

**Key Sub-tasks**:
- Survey candidate algebraic structures: process algebras (CSP, CCS), Kleene algebras with tests, symmetric monoidal categories (string diagrams), commutative semirings, and dataflow algebra
- Identify which structures have existing completeness theorems that could be adapted (e.g., Kleene's theorem for regular languages as an analogy)
- Formally define the "reconfigurability operator" — the algebraic action corresponding to topology reconfiguration — and characterize when it induces an isomorphism between communication and computation sub-algebras
- Determine whether the isomorphism is strict (bijective homomorphism) or weaker (e.g., Morita equivalence, adjunction) — the answer determines what "Route≡Transform" actually claims

**Expected Output**: A formally stated **Isomorphism Candidate Theorem** with stated assumptions, even if the full proof is deferred to SQ-2. This theorem statement is the load-bearing structure for the entire paper.

**Dependency**: None — this is the root question.

**Estimated Effort**: Weeks 1–4 (per the 16-week plan)

---

### SQ-2 — Completeness and Minimality: Is NCC-11 a Functionally Complete and Irredundant Generating Set?

**Full Statement**: Given the algebraic structure established in SQ-1, is the NCC-11 primitive set (a) **complete** — meaning every distributed ML dataflow computation expressible over a reconfigurable interconnect can be represented as a finite composition of NCC-11 primitives — and (b) **minimal** — meaning no proper subset of NCC-11 is itself complete? If NCC-11 is not minimal, what is the smallest complete subset S ⊆ NCC-11, and what is |S|? If NCC-11 is not complete, what is the smallest extension that achieves completeness?

**Motivation**: This is the central technical contribution. The analogy to Boolean functional completeness (NAND sufficiency, Post's theorem for clone theory) is precise and productive: Post's lattice classifies all clones of Boolean functions by their closure properties, and an analogous classification for distributed dataflow primitives does not exist. The question has immediate engineering stakes — if NCC-11 contains redundant primitives, implementations are carrying unnecessary complexity; if it is incomplete, deployed NCC systems have silent expressiveness gaps.

**Key Sub-tasks**:
- **Completeness proof strategy**: Define the target class of computations (distributed ML dataflow graphs) formally as a language or category; attempt to show NCC-11 generates this class under composition. Likely approach: show that any dataflow graph node can be simulated by a bounded composition of NCC-11 primitives, using a normal-form argument
- **Minimality proof strategy**: For each primitive p ∈ NCC-11, attempt to express p as a com

... (truncated, see full artifact)
