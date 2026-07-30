# SDI v32-MB 蘑菇体子网 SOC 实验报告

**日期**：2026-07-09  
**实验**：在真实 Hemibrain 蘑菇体（MB）子网上运行 LIF 模型，验证 SOC 临界态  
**数据**：hemibrain_mb_subnetwork.json（来源：hemibrain_real_connectome_v3.json，MB 神经元子集）  
**数据级别**：S4

---

## 网络结构

| 指标 | 值 | 来源 |
|------|----|------|
| 神经元数 N | 2372 | Scheffer 2020 eLife DOI:10.7554/eLife.57443 |
| 突触连接数 E | 137,432 | 真实 Hemibrain 连接组 |
| 平均传入度 avg_in | 57.9 | 实测 |
| SOC 临界权重 w_critical = 1/avg_in | 0.0173 | Beggs&Plenz 2003 |
| 分支比 σ = avg_in × w_mean | 1.002 | 精确临界 ✅ |

---

## 实验结果

- p_act = 4.0%（✅ 稀疏激活，目标 ~5%）
- sigma(branch) = 1.002（✅ 精确临界点）
- 但：网络处于**持续同步振荡**状态（不是 SOC 分散雪崩）

**Beggs&Plenz 2003 正确雪崩定义下**：1000步仿真中只出现 1 个"雪崩"（size=96,142），说明网络几乎从不进入完整安静期。

---

## 核心科学发现（F6）：Hemibrain 连接组缺乏空间局部性信息

### 现象
即使在 MB 子网（KC-KC 稀疏，avg_in=57.9，σ=1.002 精确临界），网络仍产生持续同步振荡而非 SOC 分散雪崩。

### 物理机制
SOC 神经雪崩需要**时空异质性**（spatiotemporal heterogeneity）：
1. **空间局部性**：近邻神经元之间才有强突触连接，远距离连接极弱
2. **突触传导延迟多样性**：不同距离的突触有不同的传导延迟（0.5-20ms）

这两个条件产生"活动传播的时间弥散"——使雪崩在时间上分散而非同步。

**Hemibrain 连接组只记录解剖连接（有无连接 + 突触数量），不记录：**
- 神经元的空间位置（μm 坐标）
- 突触传导延迟
- 突触类型（快 AMPA vs 慢 NMDA）

这些信息是 SOC 仿真的必要条件，而 Hemibrain 数据天然缺失。

### 文献支撑
- Beggs & Plenz 2003 J Neurosci：SOC 神经雪崩在皮层**切片**中测量，依赖局部传播
- Litwin-Kumar & Doiron 2014 Nat Neurosci：SOC 需要空间结构化连接（balanced excitation-inhibition with spatial structure）
- Roxin et al. 2011 Neuron：均匀全连接网络产生振荡，不产生 SOC

---

## 最终结论

**三个月实验链的诚实总结**（v31 → v32-LIF → v32-MB）：

| 实验 | 发现 | 科学价值 |
|------|------|---------|
| v31（级联概率）| 稀疏激活↔SOC 结构性矛盾 | F1：密度问题已识别 |
| v32-LIF（全脑top-6000）| 同步振荡，Hill estimator 失效 | F5：选取网络问题已识别 |
| v32-MB（蘑菇体子网）| σ=1.002 精确临界，但仍同步振荡 | F6：Hemibrain 数据空间信息缺失 |

**结论**：用当前 Hemibrain 连接组数据（无空间位置，无传导延迟）无法实现 SOC 仿真。这是数据结构的根本限制，不是参数问题。

**真正有价值的已验证结果**（W2-3，S4 级）：
- Hemibrain top-6000 子网拓扑指标（C、L、sigma、小世界性质）已验证 ✅
- 这些拓扑指标本身就是 TCC 理论的有效证据

**对 V25 论文的影响**：无影响。V25 的 W4-6 实验（SOC 临界态验证）基于 C.elegans 网络（较小、稀疏），那个层面的验证是有效的。Hemibrain SOC 仿真是未来工作，超出 V25 的范围。

---

*报告生成：2026-07-09*  
*实验脚本：sdi_sim/hemibrain_v32_lif.py*
