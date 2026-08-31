# NCC 原语库 v1.0 最终版规范

**Domain**: TCC
**Source**: 00_Inbox\01_GetNotes\NCC 原语库 v1.0 最终版规范.md
**Compiled**: 2026-08-31

## Summary
title: "NCC 原语库 v1.0 最终版规范" date: 2026-08-31 07:23 Now I have comprehensive data to construct the definitive NCC Primitive Library reference document. Let me compile everything into a rigorous, complete specification. NCC 原语库的设计遵循三条第一性原理。其一，**代数完备性**：原语集必须构成一个计算完备的代数系统——任何可在分布式系统上执行的计算，都能在有限步内由原语组合表达。其二，**正交最小性**：任何一个原语都不能被其余原语在 O(1) 或 O(log N) 步内等价替代；否则该原语应降级为 SDK 库函数。其三，**硬件可映射性**：每个原语都对应一个物理上可独立实现的 RTL IP 核，面积不超 命名规则：统一前缀 `ncc.`，后接四个大写字母的英语动词助记符，全部可直接发音（如 FUSE 读作 /fjuːz/，SCAN 读作 /skæn/），避免缩写嵌

## Keywords
SDI, 互连, 拓扑

---
*Auto-compiled by wiki_compiler.py*


## Related Concepts

[[NCC_Primitive_Library]]
[[Network_Topology_Design]]
[[SDI_Bond]]
[[TCC]]
