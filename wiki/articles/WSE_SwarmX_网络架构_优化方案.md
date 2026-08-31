# WSE SwarmX 网络架构 优化方案

**Domain**: TCC
**Source**: 00_Inbox\01_GetNotes\WSE SwarmX 网络架构 优化方案.md
**Compiled**: 2026-09-01

## Summary
title: "WSE SwarmX 网络架构 优化方案" date: 2026-08-31 07:23 Now I have gathered comprehensive information. Let me compile the thorough analysis. Cerebras 的网络架构由两个层级构成，其设计哲学可用 John Kim 在 ISCA 2008 提出的 Dragonfly 分层思想来理解——**片内互连（Intra-Wafer Fabric）**与**片间互连（Inter-Wafer SwarmX）**各自解决不同尺度的通信问题。 **片内层（WSE-3 On-Wafer Fabric）**：84 个 die 通过跨 scribe-line 高层金属布线实现全晶圆均匀 2D Mesh 拓扑。每个算核仅 0.05 mm²，内含 5 端口路由器（上下左右 + 本地），32-bit 双向端口，单周期跳转延迟。关键特性包括：24 条可配置静态路由"颜色"通道（colors），每条颜色独立缓冲、互不阻塞、时分复用于同一物理链路；硬件原

## Keywords
SDI, chiplet, wafer, 互连, 封装, 拓扑, 晶圆

---
*Auto-compiled by wiki_compiler.py*


## Related Concepts

[[Chiplet]]
[[Chiplet_Heterogeneous_Integration]]
[[Interconnect_Routing]]
[[Network_Topology_Design]]
[[SDI_Bond]]
[[TCC]]
[[Wafer_Scale_Integration]]
[[Wafer_Scale_Neuromorphic]]
