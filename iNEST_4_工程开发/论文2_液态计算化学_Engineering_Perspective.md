# 论文二：液态计算化学——软件定义互连作为可演化化合键

## Engineering Perspective 格式

> 目标期刊：Engineering (中国工程院院刊) / PNAS Perspective  
> 类型：Perspective / Review  
> iNEST Research Team, Tianjin University | 2026-06-03

---

## Title

**Liquid Computing Chemistry: Software-Defined Interconnects as Evolvable Chemical Bonds for Self-Organizing Intelligence**

## Article Type

Perspective (per *Engineering* journal format: visionary, forward-looking, 3000-5000 words, 3-4 figures)

---

## Structured Abstract

**Background**: Modern AI relies on static architectures and massive labeled datasets, fundamentally unlike biological intelligence which self-organizes through local physical interactions. **Concept**: We propose "Liquid Computing Chemistry"—a paradigm where neural network connections are treated as evolvable chemical bonds governed by activation energies, free energy minimization, and metaplasticity. **Core metaphor**: Synaptic states (short-term E-S vs. long-term E-L) are analogous to chemical bonds (weak van der Waals vs. strong covalent), with bond-type transitions driven by local free energy gradients rather than global optimization. **Implementation**: Software-Defined Interconnects (SDI) realize this metaphor through NULL Convention Logic asynchronous circuits on FPGA, enabling event-driven, clockless computation. **Validation**: Multi-scale simulations (N=279-1953) grounded in C.elegans connectomics demonstrate scale-invariant self-organization: small-world coefficient σ grows with network size while consolidation homeostasis EL locks at 28-31%. **Vision**: Domain-specific meta-topologies (visual cortex-like, olfactory bulb-like, etc.) could self-evolve into functional neural circuits through the same physical principles, yielding AI systems that are inherently interpretable, energy-efficient (μW-scale), and safe by construction—a green alternative to the megawatt-scale black-box large language models dominating AI today.

## Key Points

1. The SDI bond is to neural computing what the chemical bond is to molecular chemistry: a fundamental unit of structure that determines all higher-order properties.
2. Six physical/biological mechanisms drive bond evolution: FEP, BCM, minimum action, heterosynaptic competition, per-node energy constraint, periodic consolidation.
3. FPGA implementation via NCL async circuits achieves 200M spikes/s, 5ns latency, μW-scale power per bond.
4. Scale-invariance validated across 5 network sizes: bonds ∝ N^1.05, time ∝ N^1.40.
5. The paradigm requires zero labeled data, zero backpropagation, and zero global optimization.

---

## Full Outline

### 1. The Chemical Bond as Computational Primitive

1.1 **From Molecules to Minds**
   - Chemistry: bond type determines molecule properties → 10^7 known compounds from ~100 elements
   - Neuroscience: synapse type determines circuit function → 10^14 synapses from ~10^4 neuron types
   - Proposal: formalize the synapse as a "computational chemical bond"

1.2 **The Bond-Type Phase Space**
   ```
   E-S (Exploratory-Stable):   Ea = 0.15, high plasticity, low stability
   E-L (Established-Locked):   Ea = 0.85, low plasticity, high stability
   Gap junction (Electrical):   Ea = 0.50, fixed, bidirectional
   ```
   - Transition: E-S ↔ E-L governed by BCM threshold + FEP convergence
   - Analogy: van der Waals ↔ covalent bond, catalyzed by prediction success

1.3 **Bond Energy Landscape**
   - Each SDI bond has an activation energy profile
   - FEP gradient defines the energy landscape
   - System evolves toward minimum free energy configurations
   - Local minima = stable circuit motifs (memories)

### 2. Six Laws of Liquid Computing Chemistry

2.1 **Law 1: Free Energy Minimization** (Friston 2010)
   - Every bond minimizes F_local = prediction_error + λ × complexity
   - Converged nodes (F_local stable) → bonds consolidate
   - Unconverged nodes (F_local fluctuating) → bonds explore

2.2 **Law 2: Metaplasticity** (BCM 1982)
   - θ_bcm slides with post-synaptic activity history
   - Prevents saturation (runaway LTP) and depression (runaway LTD)
   - Surprise accelerates adaptation (noradrenaline analog)

2.3 **Law 3: Least Action** (Hamilton 1834)
   - dS/dt = efficiency_gain - topology_cost
   - dS/dt < 0 → system becoming more efficient → reward consolidation
   - dS/dt > 0 → cost exceeds benefit → slow consolidation

2.4 **Law 4: Resource Competition** (Heterosynaptic)
   - When one bond strengthens, neighbors weaken
   - Creates sparse, efficient representations
   - Analogous to competitive inhibition in enzyme kinetics

2.5 **Law 5: Metabolic Constraint** (per-node energy cap)
   - Each neuron has finite axonal transport capacity
   - Total outgoing weight bounded → prevents hub neurons
   - Analogous to cellular ATP budget

2.6 **Law 6: Periodic Consolidation** (protein synthesis windows)
   - Consolidation occurs in discrete time windows
   - Rate adapts based on global consolidation fraction
   - Analogous to sleep-dependent memory consolidation

### 3. Implementation: From Theory to Silicon

3.1 **SDI Bond Core Architecture**
   - NCL dual-rail encoding: DATA0/DATA1/NULL
   - Four-phase handshake pipeline
   - FEP-modulated STDP state machine
   - BCM threshold comparator
   - Completion detection circuit

3.2 **FPGA Resource Profile**
   - VCK190: 279 nodes OK (38.9% LUT, 13.6% DSP)
   - Max capacity: 341 nodes per chip
   - Power: ~53mW for C.elegans-scale
   - Latency: 5ns per spike
   - Throughput: 200M spikes/s

3.3 **Scaling Beyond Single Chip**
   - Multi-chip: AI Engine mesh interconnect
   - ASIC path: 10-100× density improvement
   - Estimated ASIC capacity: ~10^4 nodes at 28nm, ~10^5 at 7nm

### 4. Domain-Specific Meta-Topologies

4.1 **The Meta-Topology Hypothesis**
   - Different brain regions have different canonical circuit motifs
   - Visual cortex: orientation columns, feedforward hierarchy
   - Olfactory bulb: odor-specific glomeruli, lateral inhibition
   - Hippocampus: recurrent collaterals, pattern completion
   - Cerebellum: parallel fibers, Purkinje cell convergence

4.2 **Bond-Type Differentiation by Region**
   - Sensory regions: high E-S → high plasticity → fast adaptation
   - Motor regions: high E-L → high stability → reliable execution
   - Association regions: balanced E-S/E-L → flexible integration

4.3 **Application Domains**
   - Intelligence computing: ultra-low-power edge AI (drones, wearables)
   - Signal processing: adaptive filtering, anomaly detection
   - High-performance computing: graph processing, sparse matrix operations

### 5. Toward Functional Emergence

5.1 **Current State**: Network features validated (σ, EL, scaling laws)
5.2 **Next Phase**: Functional emergence
   - Phototaxis: virtual C.elegans navigating light gradient
   - Foraging: reward-modulated bond consolidation
   - Classification: unsupervised clustering through bond competition
   - Sequence learning: temporal credit assignment via eligibility traces
5.3 **The AGI Hypothesis**: If all six laws operate simultaneously on sufficiently rich meta-topologies, general intelligence may emerge as a natural consequence of physical self-organization—not as a programmed capability.

### 6. A Green, Safe, and Equitable AI Paradigm

6.1 **Energy**: μW-scale edge deployment vs. MW-scale data centers
6.2 **Data**: Zero-shot, unsupervised, physically-grounded
6.3 **Safety**: Inherently interpretable (every bond has physical meaning)
6.4 **Equity**: FPGA-deployable → accessible to institutions without GPU clusters

---

## Figures

| Figure | Content | Status |
|--------|---------|--------|
| Fig 1 | SDI Bond Type Phase Diagram (E-S ↔ E-L energy landscape) | Needs creation |
| Fig 2 | Six Laws Schematic (circular layout with dependencies) | Needs creation |
| Fig 3 | Multi-Scale Validation (σ(N), EL(N), bonds(N) panels) | v28 data ready |
| Fig 4 | NCL Async Pipeline vs. Synchronous Clock Tree | Needs creation |

---

## References (Key)

1. Friston K (2010) The free-energy principle: a unified brain theory? *Nat Rev Neurosci*
2. Bienenstock EL, Cooper LN, Munro PW (1982) Theory for the development of neuron selectivity. *J Neurosci*
3. Watts DJ, Strogatz SH (1998) Collective dynamics of small-world networks. *Nature*
4. Fant KM, Brandt SA (1996) NULL Convention Logic. *Proc ASSC*
5. Hasani R et al. (2022) Liquid neural networks. *Science Robotics*
6. Laughlin SB, Sejnowski TJ (2003) Communication in neuronal networks. *Science*
7. Holtmaat A, Svoboda K (2009) Experience-dependent structural synaptic plasticity. *Nat Rev Neurosci*

---

*论文2框架 | iNEST Research Team | 2026-06-03*
