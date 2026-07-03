# P-Paradigm 综述论文大纲 (Nature Electronics)
## Title: Liquid Hardware and the Topology-Centric Computing Paradigm: From Isomorphism Laws to Embodied AI
**Authors:** Qinrang Liu et al.
**Target Journal:** *Nature Electronics* (Perspective / Review)

### Abstract (核心叙事)
The stagnation of Moore's Law and the rigid Node-Centric (von Neumann) paradigm have led to severe "communication walls" and "dark silicon" effects in modern computing, particularly in SWaP-C constrained Embodied AI and complex systems (e.g., autonomous swarms, LEO satellites). This perspective introduces the **Topology-Centric Computing (TCC)** paradigm, enabled by Software-Defined Interconnects (SDI) and governed by fundamental **Isomorphism Laws**. By mathematically proving that diverse computational workflows—from radar signal processing (FFT) to large language model inference (AllReduce/AlltoAll)—share isomorphic topological substrates, we propose a transition from rigid silicon to **"Liquid Hardware."** We demonstrate how such architectures achieve "Silicon Neural Reuse," allowing physical interconnects to dynamically reconfigure at microsecond scales. We highlight the strategic advantage of this paradigm in closing the OODA (Observe-Orient-Decide-Act) loop, fundamentally redefining the substrate of future intelligent systems.

### 1. Introduction: The Crisis of Rigid Silicon
- The divergence of Signal Processing (FFT, spatial filtering) and Deep Learning (MatMul, AllReduce) architectures.
- The "Dark Silicon" tragedy in Embodied AI (e.g., satellites carrying redundant, mutually idle FPGA and GPU payloads).
- The biological inspiration: Neural Reuse (e.g., visual cortex repurposed for tactile processing in the blind).

### 2. The Topology-Centric Computing (TCC) Paradigm
- **Route and Transform Decomposition**: All distributed tensor computations factorize into 5 communication primitives ($\mathcal{R}$) and 4 operator primitives ($\mathcal{T}$).
- **The Isomorphism Laws (核心理论基石)**:
  - *Theorem 1 (FFT-AllReduce Isomorphism)*: The butterfly compute graph of the Fast Fourier Transform is topologically isomorphic to the optimal communication graph of the AllReduce primitive.
  - *Theorem 2 (Scatter-Gather Isomorphism)*: Multicast routing structures in spatial filtering map directly to parameter broadcasting in neural network inference.
  - *Theorem 3 (Torus-AlltoAll Isomorphism)*: The optimal routing for digital beamforming (DBF) weight updates maps to Mixture-of-Experts (MoE) token dispatch.

### 3. Liquid Hardware: SDI as the Flexible Ligament
- Microsecond-scale topological reconfiguration.
- Overcoming the von Neumann bottleneck by embedding computation within the interconnect fabric (Topology is Computation).

### 4. Use Case: Closing the OODA Loop in Space
- **The LEO Satellite / Autonomous Swarm Scenario**.
- **T0 (Observe/感知)**: SDI reconfigures 90% of the silicon into a streaming FFT pipeline. Radar range and resolution double, penetrating sea clutter.
- **T1 (Orient & Decide/决策)**: SDI instantaneously "melts" the FFT pipeline into an AllReduce tree and AlltoAll crossbar. The same silicon morphs into an LLM inference engine to assess threats and plan evasion.
- **T2 (Act/行动)**: Dynamic resource partitioning (e.g., 40% anti-jamming beamforming, 60% adversarial AI).

### 5. Conclusion: Redefining the Intelligent Substrate
- The shift from scaling transistors to scaling topological flexibility.
- The future of System of Systems (SoS) architectures relies on liquid, isomorphic substrates.


---
**Tags:** #NaaS #SDI
