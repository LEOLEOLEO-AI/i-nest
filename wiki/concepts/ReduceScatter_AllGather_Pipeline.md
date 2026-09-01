---
title: "ReduceScatter_AllGather_Pipeline"
type: concept
domain: TCC
created: 2026-09-02
auto: true
---

# ReduceScatter_AllGather_Pipeline

**Domain**: TCC
**First mentioned**: auto-extracted
**Last updated**: 2026-09-02

## Definition
A two-stage collective communication structure where ReduceScatter performs partial reductions across distributed vectors and AllGather assembles the final reduced result across all nodes. This decomposition is central to efficient AllReduce implementation on topology-centric interconnects, directly influencing latency and bandwidth trade-offs.

## Context
Auto-extracted concept from raw material compilation.

## Related Work

[[3D_Vertical_Interconnect]]
[[Advanced_Packaging_for_Space]]
[[BurstInterleaving]]
[[CXL_Deployment_Transition]]
[[Chiplet_Based_Trusted_Hardware]]
[[Chiplet_Heterogeneous_Stacking]]
[[Memory_Wall]]
[[Network_Topology_Design]]
[[P_Paradigm]]
[[TCC]]

## Sources
- See wiki/articles/ for source article summaries

## Open Questions
- *(Explore connections to other concepts)*
