# TCC-SL：全 Switchless 方案的可行性、最新进展与落地建议

**Domain**: TCC
**Source**: 00_Inbox\04 Creating\晶上全 Switchless 方案及工程落地.md
**Compiled**: 2026-08-06

## Summary
我的判断是——**可以，而且对 TCC 而言 switchless 不是妥协，是范式回归。** 但前提是把这个词的含义钉死： **去掉的是"集中式高基数交换 ASIC"，不是"交换功能"。** 交换功能被拆散、下沉到每一个计算节点内部，成为节点自身 NoC 路由器的自然延伸。这里的数量级差异是决定性的：一颗 64 口 400G 的 InfiniBand 交换机售价四万美元以上、端到端延迟约 200 ns、功耗可达 1.7 kW；而节点内嵌的一个 radix ≤ 16 的微路由器，面积不到 2 mm²、延迟 20 ns 量 更值得您注意的是驱动这件事的物理转折点。清华 IIIS 冯胤骁与马恺声在 Switch-Less Dragonfly on Wafers 中给出了一张关键对照表：NVSwitch 128 lane×100G = 12.8 Tb/s，Tofino2 12.8 Tb/s，Rosetta 12.8 Tb/s；而计算芯片这边，Tesla DOJO D1 是 576 lane×112G SerDes = * 对您的理论框架而言，这一点还有更深的一层：**大脑里没有交换机。** 

## Keywords
NoC, SDI, TCC, chiplet, topology, wafer, 拓扑, 晶圆

---
*Auto-compiled by wiki_compiler.py*


## Related Concepts

[[Chiplet_Heterogeneous_Integration]]
[[Heterogeneous_Integration]]
[[Network_Topology_Design]]
[[Network_on_Chip]]
[[Neuromorphic_Computing]]
[[SDI_Bond]]
[[TCC]]
[[Wafer_Scale_Integration]]
[[Wafer_Scale_Neuromorphic]]
