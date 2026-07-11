# SDI 研究缩略语对照表

> 维护者：iNEST 实验室  
> 最后更新：2026-05-08

---

## 一、核心范式与架构

| 缩略语 | 全称 | 中文 | 说明 |
|--------|------|------|------|
| **TCC** | Topology-Centric Computing | 拓扑中心计算 | iNEST新一代计算范式，以网络拓扑的自组织临界态为核心，而非算力堆砌 |
| **SDI** | Software-Defined Interconnect | 软件定义互连 | 元拓扑递归分形形成高阶复杂拓扑的化合键；既能形成复杂高阶拓扑，也能形成自演化类神经物理网络 |
| **SDSoW** | Software-Defined System on Web | 软件定义网络系统 | 大规模、高密度、可塑的物理连线资源，为硅基网络提供"液态重构"与"时空演化"能力 |
| **SOC** | Self-Organized Criticality | 自组织临界性 | 复杂系统自发演化到临界态的机制；大道至简的核心"一"；Bak-Tang-Wiesenfeld 1987 |

---

## 二、网络拓扑指标

| 缩略语/符号 | 全称 | 中文 | 说明 |
|------------|------|------|------|
| **σ** | Small-world coefficient | 小世界系数 | σ = (C/C_rand) / (L/L_rand)；σ>1表示小世界特性；生物神经网络典型值3-10 |
| **C** | Clustering coefficient | 聚类系数 | 节点邻居间的连接比例；衡量局部团簇密度 |
| **L** | Average path length | 平均路径长度 | 任意两节点间最短路径的均值；衡量全局连通效率 |
| **α (alpha)** | Power-law exponent | 幂律指数 | 雪崩大小分布P(s)∝s^(-α)的指数；SOC临界态典型值1.5-2.5（神经元级）或2.0-4.5（脑区级）|
| **Q** | Modularity coefficient | 模块化系数 | Q>0.3表示有显著模块化结构；衡量社区结构强度 |
| **EL / E-L ratio** | Established-Long-term bond ratio | 长期固化键比例 | 突触中已固化为长期增强状态的比例；目标区间15%-28% |

---

## 三、SDI 规则体系

| 缩略语 | 全称 | 中文 | 说明 |
|--------|------|------|------|
| **STDP** | Spike-Timing Dependent Plasticity | 脉冲时序依赖可塑性 | Hebbian学习规则；pre早于post→LTP（增强），post早于pre→LTD（抑制）|
| **LTP** | Long-Term Potentiation | 长期增强 | 突触权重持续增强；STDP的正向结果；Bliss & Lømo 1973 |
| **LTD** | Long-Term Depression | 长期抑制 | 突触权重持续减弱；STDP的负向结果 |
| **WS重连** | Watts-Strogatz Rewiring | WS随机重连 | 将空闲突触以概率P_REWIRE重连到活跃节点；维持小世界拓扑 |
| **突触缩放** | Synaptic Scaling / Homeostatic Plasticity | 突触稳态可塑性 | 节点激活率过高→下调入突触权重；过低→上调；防止网络过激或沉寂；Turrigiano 1998 |
| **竞争性修剪** | Activity-Dependent Pruning | 活动依赖性修剪 | "use it or lose it"——长期沉默的突触以概率P_PRUNE删除；驱动模块化涌现；Bhatt 2009 |

---

## 四、SDI 参数表（v13 FINAL 锁定值）

| 参数 | 值 | 含义 |
|------|----|------|
| THETA_LTP | 65 | LTP累积阈值——突触累积65次LTP事件后固化为长期键 |
| THETA_LTD | 15 | LTD累积阈值——突触累积15次LTD事件后进入消除候选 |
| ETA_LTP | 0.012 | LTP权重增量步长 |
| ETA_LTD | 0.008 | LTD权重减量步长 |
| TAU_STDP | 20 | STDP时间窗口（步） |
| CASCADE_MAX | 10 | 单次级联最大传播深度 |
| T_ABS | 3 | 绝对不应期（步） |
| T_REL | 8 | 相对不应期（步） |
| T_DECAY | 400 | 长期键自然衰减时间常数 |
| P_REWIRE | 0.15 | WS重连概率 |
| REWIRE_INT | 50 | WS重连执行间隔（步） |
| SCALING_INT | 100 | 突触缩放执行间隔（步） |
| EL_HI | 0.25 | 长期键比例上限（超过则强制回收） |

---

## 五、神经回路组件（实验二嗅觉子环路）

| 缩略语 | 全称 | 中文 | 说明 |
|--------|------|------|------|
| **ORN** | Olfactory Receptor Neuron | 嗅觉感受神经元 | 嗅觉通路第一层；接收气味分子直接刺激；Hemibrain中N=33 |
| **PN** | Projection Neuron | 投射神经元 | 嗅觉通路第二层（ALPN/mPN等）；将ORN信号投射到蘑菇体；Hemibrain中N=124 |
| **KC** | Kenyon Cell | 肯扬细胞 | 蘑菇体主体细胞；稀疏编码核心；生物实测激活率<10%；Hemibrain中N=1099 |
| **APL** | All-neurons Projection Lateral neuron | 全投射侧向神经元 | 蘑菇体全局抑制性中间神经元；维持KC稀疏编码的WTA机制；Hemibrain中N=19 |
| **MBON** | Mushroom Body Output Neuron | 蘑菇体输出神经元 | 嗅觉通路末端；将KC编码转化为行为决策信号；Hemibrain中N=76 |
| **DAN** | Dopaminergic neuron | 多巴胺神经元 | 奖惩信号调制；负责蘑菇体的强化学习 |
| **WTA** | Winner-Takes-All | 赢者通吃 | 竞争性抑制机制；APL通过WTA维持KC稀疏激活 |

---

## 六、数据集与文献缩写

| 缩略语 | 全称 | 说明 |
|--------|------|------|
| **Hemibrain** | Hemibrain v1.2.1 | 果蝇半脑连接组；N=46297神经元；1.64M突触；Xu et al. 2020 |
| **HCP** | Human Connectome Project | 人类连接组计划；Human_HCP★使用Schaefer 2018 atlas N=400脑区 |
| **WS图** | Watts-Strogatz random graph | WS随机图；小世界网络的标准生成模型；Watts&Strogatz 1998 |
| **ER图** | Erdős–Rényi random graph | ER随机图；完全随机连接模型；用于实验三基线对照 |
| **BA图** | Barabási–Albert scale-free graph | BA无标度图；优先连接生成；用于实验三基线对照 |
| **Hill MLE** | Hill Maximum Likelihood Estimator | Hill最大似然估计；用于幂律指数α的估计；Clauset 2009 |
| **LCC** | Largest Connected Component | 最大连通分量；提取子网络时取LCC保证连通性 |

---

## 七、实验编号对照

| 实验 | 文件 | 核心内容 |
|------|------|----------|
| 实验一 v13 FINAL | `sdi_experiment1_v13.py` | 10物种×5种子拓扑普适性验证（已锁定） |
| 实验二 | `sdi_experiment2_olfactory.py` | Hemibrain嗅觉子环路功能验证 |
| 实验三 | `sdi_experiment3_emergence.py` | 零先验自演化——σ涌现验证 |
| 实验四 | `sdi_experiment4_modularity.py` | 竞争性修剪——Q模块化涌现验证 |
