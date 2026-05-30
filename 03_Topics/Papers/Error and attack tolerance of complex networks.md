---
title: "Error and attack tolerance of complex networks"
year: 2000
source: "openalex"
tags: [complex networks, robustness, scale-free networks, error tolerance, attack tolerance, network resilience, percolation, hub vulnerability, graph theory, internet topology]
inest_score: 0.8
analyzed: 2026-05-30 12:12
---

# Error and attack tolerance of complex networks

- **Year**: 2000
- **Source**: openalex
- **URL**: [https://openalex.org/W2065769502](https://openalex.org/W2065769502)
- **Authors**: Réka Albert, Hawoong Jeong, Albert-László Barabási

## iNEST Relevance
**Score**: 0.80 | **Themes**: Network Intelligence, Resilience & Robustness, Emergent System Properties
The paper is foundational for iNEST's study of 'Physical Complex Network Intelligence Emergence' as it rigorously defines and quantifies a key emergent property—structural resilience—in physical complex networks (like the Internet). It provides a core methodology for assessing how intelligence (here, connected function) degrades under stress, directly relevant to understanding the fragility/robustness trade-offs in intelligent networked systems. The stark difference between error and attack tolerance is a critical insight for designing resilient intelligent infrastructures.

## Core Contribution
This seminal paper introduced a quantitative framework for analyzing the robustness of complex networks against both random failures (errors) and targeted attacks, demonstrating that scale-free networks exhibit a surprising tolerance to random failures but extreme vulnerability to targeted attacks on highly connected hubs.

## Next Steps for iNEST
Extend the framework to incorporate: 1) Adaptive networks where nodes/links can be rewired after damage, 2) Multi-layer or interdependent networks to study cascading effects, 3) Cost-benefit analyses for hardening hubs versus distributing connectivity, 4) Experimental tests on engineered and biological networks to validate the theoretical predictions under realistic conditions.

## Key Findings
- Scale-free networks are highly robust against random failures; the network remains largely connected even when a high fraction of nodes are randomly removed.
- Scale-free networks are extremely vulnerable to targeted attacks on a small fraction of their most connected hubs; removing these nodes rapidly fragments the network.
- This dual behavior stems from the inhomogeneous, power-law degree distribution of scale-free networks, where most nodes have few links, but a few hubs have many.
- In contrast, homogeneous random graphs show similar, moderate vulnerability to both random failures and targeted attacks.

## Research Gaps
- How do networks adapt or reconfigure in response to ongoing failures/attacks (dynamic robustness)?
- How to quantify and optimize the trade-off between robustness to errors and attacks in network design?
- The role of network topology beyond degree distribution (e.g., clustering, community structure, spatial embedding) in robustness.
- Robustness of network functionality beyond simple connectivity (e.g., routing efficiency, dynamical processes on networks).
- Empirical validation across a wider range of real-world socio-technical and biological systems.
