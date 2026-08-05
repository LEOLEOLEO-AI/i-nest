---
title: "RTC原语与元拓扑的映射关系"
type: article-summary
domain: TCC
created: 2026-08-04
auto: true
---
# RTC原语与元拓扑的映射关系

**Domain**: TCC
**Source**: 00_Inbox\04 Creating\RTC原语与元拓扑的映射关系.md
**Compiled**: 2026-08-04

## Summary
这样一来，六类骨架不再是另立门户，而是**六条 R 原语的实现空间**；元拓扑库的完备性也有了严格定义——**库对 6 条 R 原语实现全覆盖，每条原语提供 ≥ 1 种骨架、关键原语（R.FUSE、R.SWAP）提供 ≥ 2 种骨架变体供寻优选择**。「1 套库」的说法由此站得住脚，而且比「10 套」有力得多。 另外三条衔接关系一并厘清，写进方案后整个体系就自洽了：其一，**C.LINK 就是国际引领指标的承载原语**——「≤ 1 μs 原子重构」的准确表述是「C.LINK 页面提交时延 ≤ 1 μs」，指标与原语一一对应，可追溯、可测量；其二，**R ∘ T 的融合执行就是「拓扑近似等价于计算」（Route ≈ Transform）的工程体现**——R.FUSE 与 T.FOLD 在归约树上合并执行，数

## Keywords
拓扑

---
*Auto-compiled by wiki_compiler.py*


## Related Concepts

[[Network_Topology_Design]]
[[TCC]]
