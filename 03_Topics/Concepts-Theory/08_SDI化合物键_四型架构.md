---
title: SDI化合物键：四型架构与碳sp3杂化类比
tags:
  - sdi-bond
  - compound-bond
  - architecture
  - inest
  - hardware
  - emergence
  - neuromorphic
---

**对应专利**：[[专利P1_四型化合物键自演化架构]]
**对应论文**：[[paper1_iNEST_core_architecture]]

## 一、架构总览

SDI化合物键是iNEST的核心架构创新。每个SDI节点拥有4种键类型通道，类比碳的sp3杂化。

| 键型 | 极性 | 稳定性 | Ea | 功能 | 化学类比 |
|------|------|--------|-----|------|----------|
| E-L | 兴奋(+) | 长时程 | 0.85 | 固化骨架，长时记忆 | C-C共价键 |
| I-L | 抑制(-) | 长时程 | 0.85 | 侧抑制，稀疏维持 | 电负性原子 |
| E-S | 兴奋(+) | 短时程 | 0.15 | STDP学习通道 | 氢键/范德华力 |
| I-S | 抑制(-) | 短时程 | 0.15 | 修剪通道 | 瞬态排斥 |

## 二、键状态机（6条规则）

1. E-S → E-L（固化）：LTP计数 >= theta_LTP
2. I-S → 断开（修剪）：LTD计数 >= theta_LTD
3. 断开 → E-S（新建）：FEP梯度驱动
4. E-L → E-S（衰减）：T_decay未激活
5. I-L 保持不变
6. E-L → E-S（缩放）：全局E-L > 60%触发Turrigiano降级

## 三、五世代路线图

| Gen | 年份 | K | 生物类比 |
|-----|------|---|----------|
| Gen1 | 2027 | <=100 | C.elegans |
| Gen2 | 2029 | <=1000 | 章鱼神经节 |
| Gen3 | 2031 | <=10000 | 皮层锥体细胞 |
| Gen4 | 2033 | <=100000 | 小脑浦肯野 |
| Gen5 | 2035 | <=1M | 人脑连接度 |

## Related Notes
- [[STDP-FEP梯度下降统一映射]]
- [[三原理协同_FEP_STDP_最小作用量]]
- [[液态计算化学_MOC]]
- [[paper2_liquid_computing_chemistry]]
- [[专利组合总览]]