---
title: "wafer-scale逻辑架构技术：AI与高性能计算的突破方案"
source: "https://www.ll.mit.edu/partner-us/available-technologies/active-wafer-scale-reconfigurable-logic-fabric-ai-and-high"
created: 2026-03-06
note_id: "1903519449996180808"
tags:
  - "AI链接笔记"
  - "晶圆级集成"
  - "异构芯片封装"
  - "AI计算架构"
  - "get-笔记"
  - "AI研究"
---

# wafer-scale逻辑架构技术：AI与高性能计算的突破方案

## 摘要

### **📌 技术核心概述**  该技术通过**焊料凸点**、**无掩模可重构布线**、**硅通孔(TSV)** 和**分层互连**等技术，将多个裸片芯片键合并重新布线到单个晶圆上，形成具有集成冷却功能的高带宽、容错逻辑架构，专为**AI和高性能计算**设计。  ### **🚩 行业痛点与技术背景

## 正文

This technology bonds and reroutes multiple bare-die chips on a single wafer by using solder bumps, maskless reconfigurable wiring, through-silicon vias, and layered interconnects to form a high-bandwidth, defect-tolerant logic fabric with integrated cooling for AI and high-performance computing.



High-performance computing and AI workloads place unprecedented demands on on-chip communication bandwidth and latency, driving a shift toward tightly integrated multichip assemblies. Traditional printed circuit board (PCB) and interposer-based packaging architectures struggle to keep pace with the data rates required by deep learning inference and signal processing workloads, which require chip-to-chip interconnects approaching the density and speed of on-chip wiring. As the sizes of integrated circuit (IC) features shrink and heterogeneous accelerators become commonplace, the gap between die-to-die and intra-die communication grows, creating bottlenecks that throttle system-level throughput and efficiency.

Conventional approaches rely on discrete chip packaging with relatively coarse-pitch solder balls or wire bonds, resulting in long interconnect paths, high parasitic capacitance, and limited routing density. Large reticle stitching techniques for monolithic dies introduce manufacturing complexity and low yields, making wafer-scale integration impractical. Existing interposer solutions provide modest improvements but still suffer from thermal hotspots caused by uneven power distribution and limited cooling pathways. Moreover, the lack of fine-grained defect mitigation and reconfigurability means that single-point failures can render entire modules unusable, driving up costs and reducing system reliability.

### Technology Description

An active–passive wafer-scale logic fabric integrates hundreds of bare-die chips into a single, monolithic device by combining a solder-compatible under-bump metal (UBM) layer with μ-bump flip-chip bonding to heterogeneous ICs and a base interposer or PCB substrate. Multiple passive routing layers, implemented with transistor-based switches or routing chiplets, can be masklessly reconfigured to bypass defects discovered during wafer-scale testing. Through-silicon vias link the fabric's opposing surfaces, while hierarchical interconnect pitches use distinct solder or metal alloys to optimize signal integrity at each integration level. Integrated cooling structures — such as micro-channels and micro-jets—are embedded directly into the wafer, and the fabrication flow merges EX4 deep-ultraviolet (DUV) lithography for active device layers with large-field i-line reticles and stitching for interconnects up to 88 mm², rounded out by laser direct-write (LDW) or contact lithography to complete full-die circuitization.

This approach is differentiated by its ability to provide chip-like wiring density across a heterogeneous multichip assembly, delivering higher bandwidth and lower latency than achievable by traditional packaging. Maskless reconfiguration of passive routing layers enables yield enhancement and defect tolerance at wafer scale. The use of multiple melt-temperature interconnects permits hierarchical assembly steps without reflow interference, while embedded cooling ensures thermal management at high power densities. Unifying active device fabrication, reconfigurable routing, heterogeneous chiplet integration, and advanced thermal solutions in a single wafer platform creates a scalable, fault-tolerant substrate ideally suited for AI and high-performance embedded computing.

### Benefits

*   Monolithic-scale performance by seamlessly tiling known-good chips into a single wafer-scale device
*   Ultra-high bandwidth and low-latency "chip-like" interconnects between heterogeneous chiplets
*   Maskless, transistor-based reconfiguration of passive routing layers to bypass defects and boost yield
*   Hierarchical interconnect pitches and multi-melt-temperature solder alloys for optimized 2D/3D integration
*   Integrated micro-channel and micro-jet cooling structures for efficient thermal management
*   Reduced connectivity loss and power consumption compared to conventional board-level packaging
*   Flexible multilevel lithography (EX4 DUV, i-line stitching, LDW) enabling full-wafer circuitization and cost-effective manufacturing

### Potential Use Cases

*   Neural network training accelerators
*   AI inference servers
*   Data-center reconfigurable field-programmable fate arrays
*   Real-time image processors
*   Autonomous vehicle computers

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 08:55*