# NCC能效提升计算

**Domain**: TCC
**Source**: 00_Inbox\01_GetNotes\NCC能效提升计算.md
**Compiled**: 2026-09-01

## Summary
date: 2026-08-31 07:23 Now I have all the data needed. Let me construct a rigorous, quantitative analysis. 根据我们的前期分析，Phase 1 在 VCK190 FPGA 上运行 Gemma-4 E2B（INT4，~2.3B 有效参数，MoE 激活 ~2.3B）的性能基线是： 这个起点之所以"低"，根源在于 FPGA 的三重能量税：查找表（LUT）实现逻辑比 ASIC 标准单元高 ~10-14× 能耗（Kuon & Rose, FPGA 2007），布线通过可编程互连矩阵引入 ~5-8× 额外电容，时钟分配网络全片常开（blanket clock tree）造成大量动态功耗浪费。 根据 Horowitz 2014 ISSCC 经典数据（45nm基准），以及工艺节点缩放的经验规律：

## Keywords
SDI, chiplet, 互连, 拓扑, 晶圆

---
*Auto-compiled by wiki_compiler.py*


## Related Concepts

[[Blanket_Clock_Tree]]
[[Chiplet]]
[[Chiplet_Heterogeneous_Integration]]
[[Interconnect_Routing]]
[[MoE_Routing]]
[[Network_Topology_Design]]
[[SDI_Bond]]
[[TCC]]
[[Wafer_Scale_Integration]]
