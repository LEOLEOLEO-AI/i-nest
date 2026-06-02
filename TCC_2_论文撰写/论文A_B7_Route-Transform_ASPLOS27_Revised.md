---
title: 'Paper A (B7): Route≡Transform: A Unified Algebraic Theory of Communication and Computation Primitives for Topology-Centric Computing'
tags:
- large-language-model
- transformer
---
# 目标：ASPLOS 2027 September cycle | 截止：2026年9月9日

---

## Abstract

We present a unified algebraic framework demonstrating that communication primitives (e.g., AllReduce, AllGather) and computation primitives (e.g., GEMM, Reduce) are structurally isomorphic on a reconfigurable interconnect topology. We formalize this as the **Route≡Transform theorem**: for any distributed computation expressible as a sequence of dataflow operations, there exists an equivalent sequence of spatial topology reconfigurations on a single datapath that produces identical results without explicit memory-to-memory data movement. 

Based on this theorem, we define **TCC-11** (Network-Centric Computing 11), a minimal and complete primitive set of 11 orthogonal operations. We mathematically prove its completeness (Turing-computability for distributed functions) and minimality (removing any primitive degrades target workload performance by $\Omega(N)$). We demonstrate three corollaries with profound hardware-software co-design implications: (1) An N-point FFT is structurally isomorphic to $k=\log_2N$ reconfigurations of a butterfly network, eliminating the need for dedicated addressing hardware; (2) Mixture-of-Experts (MoE) token dispatch is a sparse AlltoAll, topologically equivalent to a distributed matrix transpose; (3) CFAR sliding-window detection is a prefix scan, isomorphic to a stateful linear-chain topology. 

We validate these theoretical results on a 4-node FPGA prototype (Xilinx VCK190) and a cycle-accurate simulator scaled to 1024 nodes. The prototype achieves a 1024-point FFT in 800 ns, Gemma-4 E2B inference at 5.2 tokens/s, and ultra-fast cross-domain switching ($\le 1 \mu s$) between LLM inference and radar DBF. Scalability analysis shows TCC maintains $\ge 99\%$ functional utilization at $N=1024$, overcoming the communication bottlenecks inherent in traditional GPU clusters.

---

## §1 Introduction
(Expanded) Highlights the Horowitz Energy Wall, explaining how data movement costs 10x-100x more energy than computation. Introduces the core thesis: routing *is* computing if the topology aligns perfectly with the dataflow graph.

## §2 Background
Contrasts TCC with existing paradigms: SHARP (In-Network Computing), Cerebras (Wafer-Scale), and Active Networks. Identifies the missing link: a unified algebraic abstraction that maps both networking and computing to a single set of primitives.

## §3 Theory: The Route≡Transform Framework

### 3.1 DFG to Topology Compilation (Compiler IR)
To bridge high-level frameworks (e.g., PyTorch) to TCC-11, we introduce a compiler IR where Dataflow Graphs (DFG) are mapped to Spatial Topology States. Nodes in DFG map to ALU primitives (FUSE, GEMM), while edges map strictly to routing configurations (LINK, PRUNE).

### 3.2 Theorem 1: Decomposition
**Theorem:** Any distributed computation $C = T_m \circ R_m \circ \dots \circ T_1 \circ R_1$ can be decomposed into an alternating sequence of spatial compute nodes and topology links.

### 3.3 Theorem 2: Structural Isomorphism (The Core)
**Lemma 2a (FFT-Butterfly Isomorphism)**:
We prove that the Cooley-Tukey butterfly addressing logic is mathematically equivalent to a hypercube AllReduce routing matrix $A_{AR}$. 
$$N\text{-point FFT} = k\cdot\text{LINK} + k\cdot\frac{N}{2}\cdot\text{GEMM(complex)} + k\cdot\frac{N}{2}\cdot\text{FUSE}$$
*Revision Note: We clarify that while ALUs (GEMM) perform the complex multiplication, the FFT addressing and memory movement are entirely replaced by the LINK routing, requiring zero dedicated FFT data-shuffling hardware.*

**Lemma 2b (AlltoAll-Transpose)**:
SWAP semantics $y[i][j]=x[j][i]$ are strictly isomorphic to matrix transpose.

**Lemma 2c (Scan-Pipeline)**:
Blelloch's up-sweep/down-sweep algorithm is topologically equivalent to a bidirectional linear-chain routing with stateful forwarding (SCAN primitive).

### 3.4 Theorem 3: Completeness
We prove TCC-11 covers 7 major workloads: Transformer (dense), CNN, FFT, SpMV, DBF, MoE, and GNN.
*   **SpMV**: FOLD_S + MOVE + PACK.
*   **MoE**: SWAP + GEMM + FUSE_S.
*   **GNN**: PULL_S + GEMM + PACK.

### 3.5 Theorem 4: Minimality (Lower Bounds)
**Lemma 4a**: Simulating SWAP without it requires $\Omega(N)$ steps using the other 10 primitives, proving its orthogonality.
**Lemma 4b**: Removing SCAN degrades CFAR sliding-window from $O(1)$ pipeline to $\Omega(N)$ sequential steps.
**Lemma 4c**: Removing MOVE degrades sparse P2P memory access to $\Omega(N)$ global exchanges.

### 3.6 Theorem T (Sparse Topology Extension)
For sparse graphs $G=(V,E)$ with density $\rho$, there exists a topology compression mapping $\phi: G \to G'$ where $|V'| \le \rho|V|$, preserving Route≡Transform isomorphism with a theoretical lower bound of $H(task)/\log_2 C$.

## §4 TCC-11 Specification
Formal definition of the 11 primitives: {LINK, PRUNE, PACK, SWAP, MOVE, PULL, CAST, GEMM, FUSE, FOLD, SCAN}.

## §5 Hardware Implementation
Implemented on Xilinx VCK190. Discusses the SDI controller, context switching ($\le 1 \mu s$), and provides a Horowitz-based energy model showing a 40% reduction in pJ/bit by eliminating off-chip SRAM/HBM round-trips during intermediate routing.

## §6 Evaluation
*   **Methodology**: 4-node FPGA prototype + Cycle-accurate Simulator for scale-out ($N=16 \dots 1024$). Baseline: Nvidia A100 cluster modeled via Megatron-LM communication traces.
*   **Performance**: FFT in 800ns; Gemma-4 at 5.2 tok/s.
*   **Scalability (T-Scale Theorem Validation)**: TCC maintains $\eta(N) \approx 99\%$ utilization at $N=1024$, whereas the A100 baseline drops to $\sim 60\%$ due to communication bubbles ($s_{GPU} \approx 40\%$).

## §7 Related Work & §8 Conclusion
(Omitted for brevity in this draft)

## Related Notes

- [[Anthropic用“AI显微镜”扒开Claude“大脑结构”，揭示语言模型行为背后机制]]
- [[GNN图神经网络，非结构化数据分析利器！]]
- [[Nature重磅：物理神经网络训练革命突破！]]
