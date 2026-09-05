# 关于NCCL通信

**Domain**: TCC
**Source**: 00_Inbox\01_GetNotes\关于NCCL通信.md
**Compiled**: 2026-09-05

## Summary
date: 2026-08-31 07:23 现在我有了所有关键原始文献。下面为6期播客逐一展开。 AllReduce蝴蝶算法的学术谱系可以追溯到三个里程碑。 第一个里程碑是1966年Cooley和Tukey发表的FFT快速傅里叶变换算法（Math. Comput. 1965），其中的蝴蝶运算图成为后续所有递归分治通信结构的数学原型。1988年Leighton在经典教材《Introduction to Parallel Algorithms and Architectures》（Morgan Kaufmann）中正式将蝴蝶网络定义为多级互连拓扑，证明N个 第二个里程碑是Rabenseifner在2004年ICCS会议上发表的"Optimization of Collective Reduction Operations"（cited 302），提出了Recursive Halving-Doubling算法——将AllReduce分解为ReduceScatter（递归向量减半+距离加倍）+ AllGather（递归距离减半+向量加倍），每一阶段恰好利

## Keywords
SDI, interconnect, 互连, 拓扑

---
*Auto-compiled by wiki_compiler.py*


## Related Concepts

[[Network_Topology_Design]]
[[SDI_Bond]]
[[TCC]]
