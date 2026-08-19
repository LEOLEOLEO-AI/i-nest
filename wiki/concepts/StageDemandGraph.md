---
title: "StageDemandGraph"
type: concept
domain: TCC
created: 2026-08-05
auto: true
---
# StageDemandGraph

**Domain**: TCC
**First mentioned**: auto-extracted
**Last updated**: 2026-08-04

## Definition
A per-inference-stage subgraph Gs=(Vs,Es,ws) ⊆ Gphys, where s ∈ {Prefill, Decode, MoE, KV-migration}, with edge weights ws representing routing frequency or communication bandwidth for that stage. Enables stage-specific communication optimization by mapping each inference phase's unique traffic pattern onto the physical topology.

## Context
Auto-extracted concept from raw material compilation.

## Related Work

[[AdiabaticMultimodeBend]]
[[BisectionBandwidthBound]]
[[BisectionBandwidthMetric]]
[[ChipletRoutingFabric]]
[[ChipletWaferInterconnectScaling]]
[[Chiplet_Heterogeneous_Integration]]
[[Chiplet_Integration_Route]]
[[Chiplet_Interconnect]]
[[Chiplet_Interconnect_Topology]]
[[DataMovementMinimization]]
[[DirectConnect_Topology]]
[[Heterogeneous_Integration]]
[[Interconnect_Routing]]
[[Memory_Wall]]
[[MoE_Routing]]
[[Network_Topology_Design]]
[[TCC]]

## Sources
- See wiki/articles/ for source article summaries

## Open Questions
- *(Explore connections to other concepts)*
