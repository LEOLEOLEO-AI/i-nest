# SDI Compound-Bond Self-Evolving Network
## Physics-First Architecture for Intelligence Emergence

**Proposed Title**: Software-Defined Interconnect Bonds: A Physics-First Architecture
for Self-Organizing Intelligence via Free Energy Minimization

**Authors**: iNEST Research Group
**Target**: Nature Machine Intelligence / Science Advances
**Status**: Framework v0.1 | 2026-06-04 00:20

---

## 1. Paper Type & Positioning

- **Type**: Original Research Article
- **Core Contribution**: First unified framework integrating FEP, STDP, and Least Action
  Principle in a single self-organizing architecture. First simulation demonstration
  that critical-state intelligence structures emerge spontaneously from physics-first
  principles alone (no backpropagation, no labels, no central control).

### Differentiation from Existing Work

| Dimension | LNN/CfC | KAN | Transformer | **iNEST** |
|-----------|---------|-----|-------------|-----------|
| Learning | Supervised BPTT | Supervised BP | Supervised BP+Attn | **FEP self-org, unsupervised** |
| Activation | Hand-designed | B-spline designed | ReLU/GELU | **Evolved via variational free energy** |
| Topology | Fixed | Fixed | Fixed | **Self-evolving (consolidate/prune/create)** |
| Physics basis | None | None | None | **FEP + Least Action + STDP** |
| Power target | N/A | N/A | ~3MW | **20W (brain-level)** |

---

## 2. Paper Structure

### Ch1: Introduction - The Physics Ceiling of LLMs (~1500 words)

**1.1 Physical Limits of Current AI**
- GPT-4: ~3MW training vs brain 20W (150,000x gap)
- Transformer O(N^2) attention vs brain O(N) sparsity
- CST metric: GPT-4 ~0.06 vs human brain ~3.92 (65x gap)
- LLMs are "fossil-fuel intelligence" - fundamentally unsustainable

**1.2 Limitations of Alternatives**
- LNN/CfC (Liquid AI, 2024): O(1) inference but still BPTT-supervised
- KAN (Liu et al., 2024): Function-on-weight compression but activation still designed
- SNN+STDP: No global convergence mechanism, hard to scale
- Common problem: all "design" intelligence rather than "allow" it to emerge

**1.3 iNEST Core Proposition**
> If a neural network follows only physics-first principles (free energy
> minimization + least action) and biological plasticity rules (STDP + synaptic
> scaling), with no hand-designed objective function, labels, or architecture
> constraints - will intelligent structures emerge spontaneously?

**Answer (v28 simulation verification): YES.**

### Ch2: Theoretical Foundation - Three-Principle Unified Framework (~3000 words) [CORE]

**2.1 SDI Compound-Bond Architecture**
- 4 bond types (E-L/I-L/E-S/I-S) x N dynamic channels + 2 SYN interfaces
- Carbon sp^3 hybridization analogy: 4 valence bonds -> 4 bond types -> "organic" intelligence chemistry
- E-L (Excitatory-Long): Consolidation skeleton, long-term memory
- I-L (Inhibitory-Long): Lateral inhibition, sparsity maintenance
- E-S (Excitatory-Short): STDP learning channel, consolidation candidate
- I-S (Inhibitory-Short): Pruning channel, disconnection candidate
- 6-rule bond state machine drives type transitions

**2.2 STDP as Physical Realization of FEP Gradient Descent** [Key Math Innovation]

Variational free energy for node i:
    F_i = sum_j [ (y_hat_ij - y_ij)^2 + Ea_ij * w_ij^2 ]
          |---prediction error---|   |--complexity penalty--|

STDP weight update = -eta * dF_i/dw_ij

dF_i/dw_ij = -2(y_hat - y)*h_j + 2*Ea*w_ij

LTP (delta_t > 0): reduces prediction error -> -dF/dw > 0 -> w increases
LTD (delta_t < 0): reduces redundant complexity -> -dF/dw < 0 -> w decreases

**Key insight**: STDP is NOT a hand-designed rule - it is the NATURAL IMPLEMENTATION
of FEP gradient descent on memristive substrates.

**2.3 Three-Principle Temporal Coordination**

| Principle | Timescale | Driver | Implementation | Math Form |
|-----------|-----------|--------|----------------|-----------|
| STDP | ms | Spike timing delta_t | Per-bond weight | delta_w = eta*dF/dw |
| FEP | s | Prediction error + complexity | Consolidate/prune decisions | F_i local minima |
| Least Action | min-h | Integral of Ea*|dw|dt | Topology evolution path | delta_S/delta[G(t)]=0 |
| Synaptic Scaling | h-day | Global E/I balance | Skeleton depolymerization | E-L>60% triggers downgrade |

All four are necessary - removing any one breaks convergence (verified in v4-v28).

**2.4 Free Energy Landscape and Critical-State Attractor**

Dual feedback loops drive the system to criticality:
- Loop 1 (subcritical->critical): Too much E-L -> prediction error increases ->
  F increases -> T_decay triggers -> E-S increases -> plasticity restored -> F decreases
- Loop 2 (supercritical->critical): Too much E-S -> complexity increases ->
  F increases -> theta_LTP triggers consolidation -> E-L increases -> skeleton stable -> F decreases
- **Equilibrium = Critical State = F global minimum = SOC = Optimal physical state for intelligence emergence**

### Ch3: Simulation Validation - C. elegans to Multi-Scale Emergence (~2500 words)

**3.1 Platform Design**
- Real connectome mode: C. elegans (N=279) x N scaling (x2,x3,x4,x7)
- Synthetic connectome mode: degree scaling k(N)=k0*N^epsilon, epsilon=0.14
- SDI_v28: STDP + FEP + BCM sliding threshold + surprise coupling + degree scaling correction

**3.2 Key Results (v28, 5 scales)**
- N=279: sigma=5.00, EL=29.1%, BCM=7.0, k=6.8, bonds=5101, time=17.6s\n- N=558: sigma=9.14, EL=28.4%, BCM=7.0, k=6.9, bonds=10334, time=26.4s\n- N=837: sigma=11.81, EL=29.2%, BCM=7.1, k=12.9, bonds=15695, time=49.9s\n- N=1116: sigma=14.26, EL=29.7%, BCM=7.1, k=13.2, bonds=21314, time=150.2s\n- N=1953: sigma=19.45, EL=31.0%, BCM=7.0, k=14.1, bonds=39106, time=207.8s\n
**3.3 Scaling Law Verification**
- bonds proportional to N^1.02: linear sparse scaling (matches biological brains)
- time proportional to N^1.22: near-linear scalable (far better than Transformer O(N^2))
- sigma increases with scale: scale-friendly (unlike traditional methods)

**3.4 Emergence Verification**
- Power-law avalanche P(S) proportional to S^(-alpha), alpha in [1.5, 2.5]
- Small-world sigma >= 4.0
- E-L ratio 15-35% golden zone
- BCM sliding threshold adaptive convergence
- F_total monotonically decreasing to plateau
- NO external labels, NO central control, NO backpropagation

### Ch4: FPGA Hardware Mapping [Patent-Dense] (~1500 words)

**4.1 SDIO-Bond Core Architecture**
- SDI node -> FPGA logic blocks (LUT+FF)
- Compound-bond channels -> software-defined routing
- SYN synaptic neuron -> memristor crossbar / DSP core
- 4 bond types -> 4 independent physical channels

**4.2 Asynchronous Spike-Driven Mechanism**
- No global clock, event-driven (AER protocol)
- Spike timing encoding: precise timing IS information
- Isomorphic to biological neural coding

**4.3 Resource Estimates**
- Gen1 (K<=100): Single FPGA, ~10K LUT
- Gen3 (K<=10000): FPGA cluster + SDI switch
- Gen5 (K<=1M): Wafer-scale integration

### Ch5: Discussion & Outlook (~1000 words)

**5.1 Quantitative Comparison**
- Energy efficiency target: brain 20W vs LLM 3MW (150,000x)
- Learning: self-organization vs supervised BP
- Interpretability: every bond has physical meaning

**5.2 Intelligence Emergence Brain Roadmap**
- Gen1 (2027): C. elegans level, K<=100, edge anomaly detection
- Gen2 (2029): Octopus ganglion, K<=1000, autonomous navigation
- Gen3 (2031): Cortical pyramidal, K<=10000, multimodal perception
- Gen4 (2033): Cerebellar Purkinje, K<=100000, motor control
- Gen5 (2035): Human brain connectivity, K<=1M, general intelligence emergence

---

## 3. Patent Protection List (8 items)

| ID | Patent Name | Core Protection | Priority |
|----|-------------|-----------------|----------|
| P1 | 4-Type Compound-Bond Self-Evolving Architecture | 4 types x N channels + 2 SYN + state machine | *** |
| P2 | FEP-Driven Self-Organizing Bond Management | Local free energy + consolidate/prune decisions | *** |
| P3 | STDP-FEP Unified Gradient Descent Mapping | STDP = -eta*dF/dw mathematical relation | *** |
| P4 | Three-Principle SOC Convergence Method | Multi-timescale synergy + dual feedback loops | ** |
| P5 | BCM + Surprise Coupling Fast Adaptation | theta_BCM adaptive + surprise factor | ** |
| P6 | Degree Scaling Law Multi-Scale Extension | k(N)=k0*N^epsilon, epsilon=0.14 | ** |
| P7 | SDI-SYN Heterogeneous Interface Protocol | Q1/Q2 dual-path + multi-type SYN | * |
| P8 | Async Spike-Driven Event Processor | Clockless AER + local rule parallelism | * |

---

## 4. Writing Progress

- [x] Overall framework and structure
- [x] Patent list
- [ ] Ch2 complete mathematical derivation
- [ ] Synthetic vs real connectome comparison experiments
- [ ] External data closed-loop (MNIST->spike->functional emergence)
- [ ] FPGA prototype verification
- [ ] Nature MI LaTeX manuscript preparation
- [ ] Patent application drafting (P1-P3 priority)

---

*Created: {ts} | iNEST Research Group*
