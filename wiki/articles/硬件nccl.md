# 硬件nccl

**Domain**: TCC
**Source**: 00_Inbox\01_GetNotes\硬件nccl.md
**Compiled**: 2026-09-07

## Summary
date: 2026-08-31 07:23 下面给你一套基于 SDI（软件定义互联）、在晶元/晶圆级网络上直接用硬件实现 Allreduce / Alltoall 的完整方案：从硬件架构、物理映射、到性能/效能/工程收益，全部对齐你要的「底层硬做、软件只配不控、直接物理映射」思路。 一、总体思路：把集合通信「做进晶元网络硬件」 \- Allreduce、Alltoall 不再靠 CPU/GPU/驱动/协议栈跑，而是作为「硬件原语」固化在晶元级 NoC/Die-to-Die 互连里； \- SDI 只负责：拓扑重构、资源分配、映射编排，不做流控、路由、调度、负载均衡；

## Keywords
NoC, SDI, iNEST, interconnect, wafer, 互连, 拓扑, 晶圆, 芯粒

---
*Auto-compiled by wiki_compiler.py*


## Related Concepts

[[Chiplet_Heterogeneous_Integration]]
[[Network_Topology_Design]]
[[Network_on_Chip]]
[[NoC]]
[[SDI_Bond]]
[[TCC]]
[[Wafer_Scale_Integration]]
[[iNEST]]
[[拓扑重构]]
