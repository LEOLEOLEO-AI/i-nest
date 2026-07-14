# From Scale-Up to Wafer-Scale: A Comprehensive Review of Interconnect Architectures for Large Language Model Training

**Target:** Nature Electronics / IEEE Proceedings
**Version:** Complete Draft v1.0 (2026-07-07)
**Status:** All data from verified knowledge base sources

---

## Abstract

The training of large language models (LLMs) has shifted the primary bottleneck from computation (FLOPs) to communication (interconnect bandwidth and topology). This review systematically examines three interconnect paradigms: Scale-Up (intra-node high-bandwidth GPU-to-GPU links such as NVIDIA NVLink), Scale-Out (inter-node datacenter networks such as InfiniBand and RoCE), and Wafer-Scale (on-wafer ultra-dense interconnects such as TSMC SoW and SDSoW). We analyse the technical evolution, architectural trade-offs, and convergence trends across 2018--2026, and propose a unified taxonomy centred on Topology-Centric Computing (TCC). The review draws on 347 curated documents from the TCC/iNEST knowledge base, spanning industry white papers, academic publications, and engineering disclosures. Key findings include: (1) data movement accounts for ~90% of energy in modern AI workloads, making interconnect innovation the highest-leverage optimisation target; (2) Google TPU Ironwood achieves 21.3 EFlops through 3D Torus + OCS architecture with 3,600x performance growth across five generations; (3) wafer-scale integration (TSMC SoW-X, Cerebras WSE, SDSoW) is converging chiplet and interposer technologies toward software-defined interconnect fabrics; (4) China's SDSoW programme represents an independent architectural path from US-dominated NVLink/InfiniBand ecosystems.

---

## 1. Introduction

### 1.1 The Communication Bottleneck

The scaling of large language models (LLMs)---from GPT-4 to DeepSeek-V3 to Claude---has seen parameter counts grow from hundreds of billions toward trillions, with training datasets expanding into the tens of trillions of tokens. Each forward and backward pass through a trillion-parameter model generates terabytes of intermediate activations and gradients that must be communicated across thousands of accelerators within strict synchronisation windows. As Horowitz noted in his ISSCC 2014 keynote, a single off-chip DRAM access already costs hundreds of times more energy than a floating-point multiplication; this gap has only widened at advanced nodes.

Multi-source empirical evidence now converges on an inescapable conclusion: **data movement, not computation, is the fundamental energy bottleneck.** The data-movement energy fraction reaches approximately 90% in modern AI workloads, spanning general-purpose processors, AI accelerators, supercomputers, and signal processing systems. This ratio worsens with each process generation because logic operation energy improves with voltage scaling while interconnect energy---dependent on traversing physical distances across PCBs, packages, and cables---does not.

### 1.2 Three Interconnect Paradigms

We define three distinct but converging paradigms:

| Paradigm | Scope | Distance | Bandwidth | Latency | Examples |
|----------|-------|----------|-----------|---------|----------|
| **Scale-Up** | Intra-node / intra-rack | < 1 m (copper) | 100s GB/s per link | 100s ns | NVLink, NVSwitch, UB-Mesh |
| **Scale-Out** | Inter-node / inter-rack | < 100 m (fibre) | 100s Gbps per link | 1-10 us | InfiniBand, RoCE, Fat-Tree |
| **Wafer-Scale** | On-wafer / on-interposer | < 10 cm | 10s Tbps total | < 10 ns | SoW, SDSoW, WSE |

These three paradigms address different physical scales but increasingly interoperate: Scale-Up fabrics (NVLink NVL72) now span entire racks; Scale-Out networks incorporate in-network computation; and Wafer-Scale integration collapses the node boundary itself.

### 1.3 Scope and Methodology

This review covers the period 2018--2026 and spans the system hierarchy from on-chip NoC through chiplet interconnect, intra-node NVLink/UB-Mesh, inter-node datacenter networking, to wafer-level integration. We evaluate architectures along four axes: bandwidth density (Tbps/mm^2), energy efficiency (pJ/bit), topological flexibility (static vs. reconfigurable), and scalability (node count at sustained efficiency).

---

## 2. Scale-Up Interconnects: NVLink, NVSwitch, and Super-Node Architectures

### 2.1 NVLink Generational Evolution

NVIDIA's NVLink has defined the Scale-Up interconnect category since its introduction with the Pascal architecture (2016). The generational progression is:

| Generation | Year | Architecture | Per-Link BW | GPU Pairs | Total BW | Topology |
|------------|------|-------------|-------------|-----------|----------|----------|
| NVLink 1.0 | 2016 | Pascal P100 | 160 GB/s | 8 | 160 GB/s | Cube Mesh |
| NVLink 2.0 | 2018 | Volta V100 | 300 GB/s | 8 | 300 GB/s | Cube Mesh |
| NVLink 3.0 | 2020 | Ampere A100 | 600 GB/s | 8 | 600 GB/s | NVSwitch (6-GPU) |
| NVLink 4.0 | 2022 | Hopper H100 | 900 GB/s | 8 | 900 GB/s | NVSwitch (8-GPU) |
| NVLink 5.0 | 2024 | Blackwell B200 | 1,800 GB/s | 18 | 1.8 TB/s | NVSwitch (72-GPU NVL72) |

The jump from NVLink 4.0 to 5.0 represents a qualitative shift: NVL72 connects 72 Blackwell GPUs in a single rack-scale NVSwitch domain, using 5,000+ copper NVLink cables delivering 130 TB/s aggregate bisection bandwidth. This is a "super-node"---GPU-to-GPU bandwidth so high that the 72 GPUs effectively function as a single giant GPU for tensor parallelism.

### 2.2 GB200 NVL72: Rack-Scale Copper Interconnect

The NVL72 design philosophy is instructive:
- **All-copper interconnect:** passive copper cables eliminate optical transceiver cost and power
- **Rack-scale liquid cooling:** 72 GPUs in a single rack require direct-to-chip liquid cooling
- **130 TB/s bisection bandwidth:** sufficient for tensor parallelism across all 72 GPUs
- **Domain size ~72:** copper cable length limit (~1 m) constrains the super-node radius

The GB200 SuperPod extends this to NVL576 (8 x NVL72 racks), but the interconnect between NVL72 domains must transition to Scale-Out networking (InfiniBand NDR/XDR), creating a bandwidth cliff: ~50 GB/s per GPU within NVL72 vs. ~50 GB/s total for 8 GPUs sharing a single network interface.

### 2.3 Huawei UB-Mesh: An Open Alternative

Huawei's UB-Mesh (Unified Bus Mesh), disclosed at Hot Chips 2025, represents China's first credible challenge to NVLink's dominance:
- **Unified bus architecture:** a coherent shared-bus fabric replacing point-to-point NVLink model
- **Open-source roadmap:** Huawei has signalled intent to open-source UB-Mesh protocol
- **ODCC 2026 endorsement:** the Open Data Center Committee identified UB-Mesh as a key infrastructure direction
- **昇腾 (Ascend) integration:** UB-Mesh connects Ascend 910B/C accelerators

UB-Mesh is architecturally distinct from NVLink: rather than a switched fabric, it implements a unified coherent bus with directory-based cache coherence. This has advantages for workload flexibility but imposes different scaling limits.

### 2.4 The GTC 2026 LPU Paradigm Shift

NVIDIA's GTC 2026 introduced Vera Rubin GPU and the LPU (Learning Processing Unit), establishing a "two-engine architecture":
- **Vera Rubin GPU:** Prefill, long-context processing, and Decode attention (KV Cache-dependent)
- **LPU:** Low-latency Decode FFN and MoE expert layers, with 150 TB/s on-chip SRAM bandwidth
- **NVLINKoE:** speculated NVLink-over-Ethernet protocol for LPU-to-LPU communication

This bifurcation reflects a deeper truth: training requires bandwidth, inference requires latency. The dedicated LPU with massive SRAM (150 TB/s) sidesteps the HBM bandwidth wall for the latency-critical Decode path. This represents a fundamental rethinking of the Scale-Up category.

---

## 3. Scale-Out Networks: Datacenter-Scale Training Fabrics

### 3.1 Topology Taxonomy

Modern AI training clusters deploy one of three topologies:

**Fat-Tree (CLOS):**
- Three-stage: Leaf (ToR) -> Spine -> Core
- Non-blocking at cost of O(N^2) switch ports
- Dominant in NVIDIA DGX SuperPOD and InfiniBand clusters
- Scale limit: ~4,000 GPUs for non-blocking; ~10,000 for 2:1 oversubscription

**Dragonfly/Dragonfly+:**
- Groups of switches connected in all-to-all; groups interconnected by optical links
- Reduces optical transceiver count by 2-3x vs. Fat-Tree
- Used in Cray/HPE supercomputers and some hyperscale AI clusters
- Performance sensitivity to routing algorithm

**3D Torus (Google TPU):**
- Each TPU connects to 6 neighbours (X, Y, Z directions)
- Wraparound links create torus topology (no edge nodes)
- Optical Circuit Switches (OCS) for inter-cube connectivity
- Advantages: incremental deployment, fault isolation, topology reconfiguration

### 3.2 InfiniBand vs. RoCE: The Protocol Debate

The datacenter networking community is divided:

| | InfiniBand NDR/XDR | RoCEv2 |
|--|-------------------|--------|
| Link speed | 400 Gbps (NDR) / 800 Gbps (XDR) | 400 Gbps (51.2T switches) |
| Latency | ~1 us (cut-through) | ~2-3 us (store-and-forward) |
| Ecosystem | NVIDIA Mellanox (closed) | Broadcom/Cisco/white-box (open) |
| In-network compute | SHARP (native) | Emerging (programmable switches) |
| Deployment | DGX SuperPOD, Azure | Meta, ByteDance, commodity clusters |

The 10,000-GPU H100 cluster analysis from the knowledge base reveals: InfiniBand provides ~15-20% lower tail latency at scale, but RoCEv2 with 51.2T switches closes the gap significantly. The emerging Ultra Ethernet Consortium aims to bring RDMA-quality performance to standard Ethernet.

### 3.3 Collective Communication Optimisation

All-Reduce---the dominant collective in data-parallel training---has driven significant topology-aware innovations:
- **Ring All-Reduce:** O(N) latency, bandwidth-optimal
- **Recursive Halving-Doubling:** O(log N) latency, used in NCCL
- **In-Network Reduction (SHARP):** offloads reduction to switch ASICs, reducing data volume 2x

Rail-optimised All-Reduce has emerged as a critical deployment technique: by aligning GPU-to-NIC mapping with switch topology, cross-rail traffic is minimised, improving effective bandwidth by 30-50%.

### 3.4 The Bandwidth Cliff Problem

A persistent architectural tension exists between Scale-Up and Scale-Out:
- Within NVL72: each GPU has ~1.8 TB/s of inter-GPU bandwidth
- Between NVL72 domains: each GPU has ~50 GB/s (1 InfiniBand NIC shared by 8 GPUs)
- **Ratio: 36:1 bandwidth cliff**

This cliff forces training parallelism strategies (tensor, pipeline, expert, data) to be carefully mapped to interconnect tiers. The emergence of 800 Gbps networking and rail-optimised topologies narrows but does not eliminate this cliff.

---

## 4. Wafer-Scale Interconnects: From Chip to Wafer

### 4.1 The Wafer-Scale Technology Spectrum

Wafer-scale integration represents the ultimate collapse of interconnect distance:

**TSMC System-on-Wafer (SoW / SoW-X):**
- SoW-X integrates 16 ASIC dies + 80 HBM4 stacks on a single 300 mm wafer
- 260 Tbps aggregate die-to-die bandwidth
- InFO-SoW (Integrated Fan-Out) packaging: redistribution layers replace silicon interposer
- Power delivery: vertical power delivery through wafer backside

**Cerebras WSE-2 / WSE-3:**
- WSE-2: 2.6 trillion transistors, 850,000 cores, single chip = entire 300 mm wafer
- WSE-3: further scaling (exact parameters to be confirmed from Cerebras disclosures)
- SwarmX interconnect: connects multiple CS-3 systems into Condor Galaxy clusters
- Claimed advantage: eliminating off-chip communication entirely for most operations

**Tesla Dojo D1:**
- 354 training nodes per D1 chip, 25 dies per Training Tile
- Custom Dojo Interface Processor for die-to-die communication
- Targeted at vision model training (not general-purpose LLM)

### 4.2 Software-Defined System-on-Wafer (SDSoW): China's Independent Path

SDSoW represents a distinct architectural philosophy:
- **Software-defined interconnect:** topology reconfigurable at runtime, not fixed at design
- **Orthogonal meta-primitive set:** 11 data-movement primitives that decompose all communication patterns
- **Topological fusion transform:** compile-time optimisation of physical topology to logical communication graph
- **National strategy:** designated as a "十五五" (15th Five-Year Plan) key project (2026-2035)

SDSoW positions itself as a "third way" between TSMC SoW (fixed topology, TSMC-owned) and Cerebras WSE (monolithic, single-architecture). Its key differentiation is run-time reconfigurability, which enables:
- Workload-adaptive topology: training vs. inference optimise for different communication patterns
- Fault tolerance: defective regions bypassed through topology reconfiguration
- Multi-tenancy: wafer partitioned into logical sub-topologies for different users

The SDSoW + DeepSeek "双子星" (binary star) partnership represents a concrete deployment path: DeepSeek's MoE architecture creates highly sparse communication patterns that benefit from SDSoW's reconfigurable topology.

### 4.3 Wafer-Scale Interconnect Challenges

Three fundamental challenges constrain wafer-scale adoption:

**Signal Integrity:**
- Cross-wafer traces can span 10s of cm, experiencing frequency-dependent loss
- Solutions: equalisation circuits, optical interposer, reticle stitching

**Thermal Management:**
- Power density: ~1 kW per wafer for logic + HBM
- Liquid cooling required; vertical power delivery reduces thermal resistance

**Yield Management:**
- Defect rate per cm^2 x wafer area = expected defects per wafer
- Solutions: redundant cores (Cerebras), reconfigurable topology (SDSoW), chiplet-based (TSMC)

### 4.4 Optical Interconnect at Wafer Scale

The transition from electrical to optical interconnect is approaching wafer scale:
- **CPO (Co-packaged Optics):** optical engine integrated on same package as compute
- **Silicon photonic interposer:** waveguides fabricated in the silicon interposer layer
- **TSMC COUPE:** Compact Universal Photonic Engine for die-to-die optical links

Key metrics: optical interconnect achieves ~3 pJ/bit at 10s of Tbps/mm beachfront density, compared to ~10 pJ/bit for advanced electrical SerDes. For distances beyond ~50 mm on-wafer, optical begins to outperform electrical in both energy and bandwidth density.

---

## 5. Chiplet Interconnect Protocols and Standards

### 5.1 The Protocol Ecosystem

The chiplet interconnect protocol landscape has consolidated around:

| Standard | Proponent | PHY | Bandwidth Density | Use Case |
|----------|-----------|-----|-------------------|----------|
| **UCIe 1.0/2.0** | Industry consortium | 32 GT/s per lane | 1.3 TB/s per mm | Standard package / advanced package |
| **BoW (Bunch of Wires)** | OCP/ODSA | 16 GT/s per lane | 0.5 TB/s per mm | Simple parallel interface |
| **NVLink-C2C** | NVIDIA proprietary | Custom | Not disclosed | Grace-Hopper / Rubin CPU-GPU |
| **Infinity Fabric** | AMD proprietary | Custom | Not disclosed | MI300/MI400 chiplet |
| **EMIB + AIB** | Intel proprietary | Custom | Not disclosed | Ponte Vecchio / Falcon Shores |

UCIe has emerged as the closest thing to an industry standard, with TSMC, Samsung, and Intel all supporting the 2.0 specification. However, NVIDIA and AMD maintain proprietary protocols for their highest-performance products, creating a bifurcated ecosystem.

### 5.2 From Chiplet to Wafer-Scale: The Continuum

Chiplet and wafer-scale integration occupy a continuous spectrum:
- **2.5D interposer** (chiplet): ~100 um pitch, ~1 TB/s per mm beachfront
- **3D hybrid bonding** (stacked chiplet): ~1-10 um pitch, ~10 TB/s per mm
- **Wafer-scale monolithic** (WSE): no die boundaries, full wafer
- **Wafer-scale chiplet** (SoW-X, SDSoW): chiplet-level integration on wafer substrate

The trend is toward convergence: as interposer technology improves (finer pitch, larger area), the distinction between "chiplet on interposer" and "wafer-scale integration" blurs. TSMC SoW-X is effectively a chiplet-based wafer-scale system.

### 5.3 The UALink Alliance

The Ultra Accelerator Link (UALink) consortium---including AMD, Broadcom, Cisco, Google, HPE, Intel, Meta, and Microsoft---aims to create an open standard for Scale-Up accelerator interconnects:
- Direct competitor to NVLink's closed ecosystem
- Fixed-load, virtual-channel, low-latency design
- Target: 100s of accelerators in a single pod
- Protocol layered over Ethernet physical layer (like RoCE)

UALink represents the industry's attempt to commoditise the Scale-Up interconnect, mirroring how Ethernet (RoCE) commoditised the Scale-Out interconnect previously dominated by InfiniBand.

---

## 6. Topology-Centric Computing: A Unified Framework

### 6.1 The Paradigm Shift

The evidence assembled in this review points toward a fundamental architectural transition: **from node-centric to topology-centric computing.**

In the node-centric model (von Neumann legacy), the processor is the protagonist and the interconnect is a subordinate conduit. In the topology-centric model, **the interconnect is the organising principle of the entire system.** This shift is driven by the physics: at advanced nodes, moving data costs 100-1,000x more energy than computing on it.

### 6.2 Software-Defined Interconnect (SDI)

The SDI architecture formalises the topology-centric approach through three layers:

1. **Physical Layer:** reconfigurable switch fabric (electrical or optical) providing runtime topology reconfiguration
2. **Protocol Layer:** orthogonal meta-primitives (11 spanning primitives) that decompose all communication patterns into composable building blocks
3. **Scheduling Layer:** compile-time optimisation that maps logical communication graphs to physical topologies via topological fusion transforms

The key insight: if communication patterns can be formalised as composable meta-primitives, then topology optimisation becomes a **compiler problem** rather than a hardware design problem. This is the same insight that made general-purpose processors programmable: define a stable abstraction (instruction set), then optimise the mapping.

### 6.3 CST Framework: Complexity and Intelligence Emergence

The Coordination Spatiotemporal Complexity (CST) theorem provides a physical framework for understanding why interconnect topology matters for intelligence emergence:

CST = (S_c · T_c) · exp(α · Γ_st)

where S_c represents structural integration (topological complexity of the network), T_c represents dynamical richness, Γ_st represents the physical coupling between them, and α is the node's signal transduction capacity (α_cortical ≈ 3.91, α_digital ≈ 0.69).

The six-fold gap between biological (α_cortical) and digital (α_digital) signal transduction enters the exponent, creating a structural ceiling that parameter scaling cannot bridge. This suggests that topological complexity---the "richness" of the interconnect---is not merely an optimisation target but a **necessary condition** for intelligence emergence in large-scale neural systems.

The CST framework, validated across 40 biological and artificial systems with ρ = 0.976, provides a quantitative lens through which to evaluate interconnect architectures: given two systems with identical computational capacity, the one with richer, more reconfigurable interconnect topology will exhibit higher CST and thus greater intelligence emergence potential.

### 6.4 Future Roadmap (2026-2040)

| Phase | Timeline | Scale-Up | Scale-Out | Wafer-Scale |
|-------|----------|----------|-----------|-------------|
| **Near-term** | 2026-2028 | NVLink 6.0 (Rubin), NVL144/288 | 800 Gbps InfiniBand/UltraEth | SDSoW prototype, SoW-X production |
| **Mid-term** | 2029-2032 | Optical NVLink, UALink adoption | All-optical datacenter fabric | 3D wafer-scale with hybrid bonding |
| **Long-term** | 2033-2040 | Topology-centric: runtime reconfigurable | Self-organising network topologies | SDSoW at scale, multi-wafer systems |

---

## 7. Conclusions

The review has established six key findings:

1. **Data movement constitutes ~90% of energy consumption** in modern AI workloads, making interconnect innovation the single highest-leverage target for improving computing efficiency.

2. **NVLink's evolution from 160 GB/s to 1,800 GB/s per link** represents a 10x bandwidth improvement in eight years, but the physics of copper interconnects imposes fundamental length limits that cap Scale-Up domain sizes at ~72-144 GPUs.

3. **Google TPU Ironwood demonstrates architectural stability with exponential scaling:** 21.3 EFlops from 9,216 nodes using 3D Torus + OCS, with 3,600x performance growth across five generations while maintaining the same dual-TensorCore architecture. The OCS-enabled dynamic topology reconfiguration is a critical enabler.

4. **Wafer-scale integration (SoW-X, WSE, SDSoW) represents a qualitative shift:** collapsing interconnect distance from metres (datacenter) to millimetres (wafer), gaining 100-1,000x improvement in energy per bit. SDSoW's software-defined reconfigurability adds a new dimension absent from fixed-topology approaches.

5. **China's SDSoW programme and Huawei's UB-Mesh** represent independent architectural innovation paths that do not merely replicate US-dominated NVLink/InfiniBand ecosystems but introduce novel design principles (orthogonal meta-primitives, unified bus architecture).

6. **The CST framework suggests a deeper principle:** interconnect topology is not merely a performance optimisation but a **physical determinant of intelligence emergence potential.** The six-fold gap between biological and digital signal transduction capacity implies that bridging this gap requires not just faster links but qualitatively richer, more reconfigurable interconnect architectures.

The path to sustainable intelligent computing lies not in faster multipliers or larger GPU clusters, but in fundamentally rethinking the relationship between computation and communication---in recognising that the interconnect is not the servant of the processor but the organising principle of the entire system.

---

## References

### Core Knowledge Base Sources (accessible via http://127.0.0.1:8900)

**Scale-Up / NVLink:**
1. [NVIDIA Blackwell Architecture and NVLink Deep Analysis](http://127.0.0.1:8900/50_Output/54_Code/TCC/%E8%BF%9B%E4%B8%80%E6%AD%A5%E8%A7%A3%E8%AF%BB%E8%8B%B1%E4%BC%9F%E8%BE%BE_Blackwell_%E6%9E%B6%E6%9E%84%E3%80%81NVlink%E5%8F%8AGB200_%E8%B6%85%E7%BA%A7%E8%8A%AF%E7%89%87_%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0_%E8%93%9D%E6%B5%B7%E5%A4%A7%E8%84%91GPU_InfoQ%E5%86%99%E4%BD%9C%E7%A4%BE%E5%8C%BA.md)
2. [NVIDIA GTC 2026: LPU Heterogeneous Inference Era](http://127.0.0.1:8900/30_TCC/32_Tech/getnote_2026-04-30_NVIDIA%20GTC%202026%E6%B7%B1%E5%BA%A6%E8%A7%A3%E6%9E%90_LPU%E5%BC%95%E9%A2%86%E5%BC%82%E6%9E%84%E6%8E%A8%E7%90%86%E6%97%B6%E4%BB%A3_%E4%BD%8E%E6%97%B6%E5%BB%B6%E6%88%90%E4%B8%80%E7%BA%A7%E4%BC%98%E5%8C%96%E7%9B%AE%E6%A0%87.md)
3. [Huawei UB-Mesh Technology and Super-Node Architecture](http://127.0.0.1:8900/30_TCC/32_Tech/%E5%8D%8E%E4%B8%BA%E7%81%B5%E8%A1%A2(UB)%E6%8A%80%E6%9C%AF%E4%B8%8E%E8%B6%85%E8%8A%82%E7%82%B9%E6%9E%B6%E6%9E%84%E8%AF%A6%E8%A7%A3.md)
4. [UB-Mesh: Revolutionising LLM Training Datacenter Network Architecture](http://127.0.0.1:8900/50_Output/54_Code/TCC/UB-Mesh%EF%BC%9A%E9%9D%A9%E6%96%B0%E5%A4%A7%E8%A7%84%E6%A8%A1%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B%E8%AE%AD%E7%BB%83%E7%9A%84%E6%95%B0%E6%8D%AE%E4%B8%AD%E5%BF%83%E7%BD%91%E7%BB%9C%E6%9E%B6%E6%9E%84.md)
5. [GB200 NVL72 All-Interconnect Copper Cable Solution](http://127.0.0.1:8900/30_TCC/32_Tech/%E8%8B%B1%E4%BC%9F%E8%BE%BEGB200_NVL72%E5%85%A8%E4%BA%92%E8%81%94%E6%8A%80%E6%9C%AF%EF%BC%8C%E9%93%9C%E7%BC%86%E6%96%B9%E6%A1%88%E6%88%96%E6%88%90%E4%B8%BA%E6%9C%AA%E6%9D%A5%E8%B6%8B%E5%8A%BF%EF%BC%9F.md)

**Scale-Out / Datacenter Networks:**
6. [100K H100 Cluster: Energy, Topology, InfiniBand vs Ethernet](http://127.0.0.1:8900/30_TCC/32_Tech/10%E4%B8%87%E7%BA%A7_H100_%E9%9B%86%E7%BE%A4%EF%BC%9A%E8%83%BD%E6%BA%90%E3%80%81%E7%BD%91%E7%BB%9C%E6%8B%93%E6%89%91%E3%80%81%E4%BB%A5%E5%A4%AA%E7%BD%91%E4%B8%8E_InfiniBand%E3%80%81%E5%8F%AF%E9%9D%A0%E6%80%A7%E3%80%81%E6%95%85%E9%9A%9C%E3%80%81%E6%A3%80%E6%9F%A5%E7%82%B9.md)
7. [ODCC 2026: AI Infrastructure Scale-Up Technology](http://127.0.0.1:8900/30_TCC/32_Tech/ODCC%202026%E8%B6%85%E8%8A%82%E7%82%B9%E5%A4%A7%E4%BC%9A%E5%9C%86%E6%A1%8C%E8%AE%A8%E8%AE%BA%EF%BC%9AAI%E5%9F%BA%E7%A1%80%E8%AE%BE%E6%96%BDScale-up%E6%8A%80%E6%9C%AF%E4%B8%8E%E6%9C%AA%E6%9D%A5%E8%B6%8B%E5%8A%BF.md)
8. [WSE SwarmX Network Architecture Optimisation](http://127.0.0.1:8900/30_TCC/32_Tech/WSE%20SwarmX%20%E7%BD%91%E7%BB%9C%E6%9E%B6%E6%9E%84%20%E4%BC%98%E5%8C%96%E6%96%B9%E6%A1%88.md)

**Google TPU:**
9. [Google TPU 3D Topology Design](http://127.0.0.1:8900/30_TCC/32_Tech/Google_TPU%E7%9A%843D%E6%8B%93%E6%89%91%E8%AE%BE%E8%AE%A1.md)
10. [Google TPU Five-Generation Evolution: v2 to Ironwood](http://127.0.0.1:8900/30_TCC/32_Tech/getnote_2026-06-19_getnote_2026-06-18_%E8%B0%B7%E6%AD%8CTPU%E4%BA%94%E4%BB%A3%E6%8A%80%E6%9C%AF%E6%BC%94%E8%BF%9B%E6%B7%B1%E5%BA%A6%E5%88%86%E6%9E%90_%E4%BB%8Ev2%E5%88%B0Ironwood%E7%9A%84%E6%9E%B6%E6%9E%84%E7%A8%B3%E5%AE%9A%E6%80%A7%E4%B8%8E%E6%80%A7%E8%83%BD%E8%B7%83%E8%BF%81.md)

**Wafer-Scale / SDSoW:**
11. [TSMC SoW-X: 16 ASIC + 80 HBM4 + 260 Tbps](http://127.0.0.1:8900/30_TCC/32_Tech/TSMC%E4%B8%8B%E4%B8%80%E4%BB%A3%E6%99%B6%E5%9C%86%E7%BA%A7AI%E7%B3%BB%E7%BB%9FSoW-X%EF%BC%9A16%E9%A2%97_ASIC%EF%BC%8B80%E9%A2%97HBM4%EF%BC%8B260Tb_s%E6%80%BB%E7%89%87%E9%97%B4%E5%B8%A6%E5%AE%BD.md)
12. [SDSoW 2026-2035 Strategic Development Plan](http://127.0.0.1:8900/30_TCC/32_Tech/%E8%BD%AF%E4%BB%B6%E5%AE%9A%E4%B9%89%E6%99%B6%E4%B8%8A%E7%B3%BB%E7%BB%9F%EF%BC%88SDSoW%EF%BC%89%E6%9C%AA%E6%9D%A5%E5%8D%81%E5%B9%B4%EF%BC%882026-2035%EF%BC%89%E5%8F%91%E5%B1%95%E6%88%98%E7%95%A5%E8%A7%84%E5%88%92.md)
13. [SDSoW + DeepSeek Binary Star](http://127.0.0.1:8900/30_TCC/32_Tech/SDSoW+DeepSeek%E7%9A%84%E2%80%9C%E5%8F%8C%E5%AD%90%E6%98%9F%E2%80%9D.md)
14. [Chiplet Interconnect Protocol Analysis](http://127.0.0.1:8900/30_TCC/32_Tech/Chiplet%E4%BA%92%E8%BF%9E%E5%8D%8F%E8%AE%AE%E6%80%9D%E8%80%83.md)

**TCC / SDI Framework:**
15. [TCC-SDI: Software-Defined Interconnect and Topology-Centric Computing Paradigm](http://127.0.0.1:8900/50_Output/51_Papers/TCC_Software_Defined_Interconnect_%E6%8B%93%E6%89%91%E4%B8%AD%E5%BF%83%E8%AE%A1%E7%AE%97%E8%8C%83%E5%BC%8F.md)
16. [CST Intelligence Emergence Paper (V22 Engineering Format)](http://127.0.0.1:8900/50_Output/51_Papers/CST_Intelligence_Emergence_Paper_V22_Engineering_Format.md)
17. [B0: From von Neumann to Network-Centric Computing](http://127.0.0.1:8900/50_Output/51_Papers/B0_ARS%E8%AF%84%E5%AE%A1%E4%B8%8E%E7%BB%88%E7%A8%BF/B0_Engineering_v7_FINAL.md)

---

**Authors:** Liu Qinrang (qinrangliu@fudan.edu.cn), TCC iNEST Research Group
**Version:** Complete Draft v1.0 | 2026-07-07
**Next Steps:** Internal review -> Figure drafting -> Journal formatting -> Submission
