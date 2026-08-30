---
direction: iNEST
category: 技术
tags: [memristor, neuromorphic, self-organization, SNN, hardware]
summary: "基于忆阻器动力学与自组织网络，梳理iNEST落地方案"
quality: high
processed: 2026-08-30 18:45
---
---
title: "iNEST落地方案"
tags:
  - paper
  - hardware
  - self-organization
  - stdp
  - top-journal
  - neuroscience
  - chip
  - research
  - architecture
  - first-principles
  - semiconductor
  - sdi-bond
  - learning-rule
  - criticality
  - free-energy
  - design
  - fep
  - fpga
  - memristor
  - physics
  - network
  - emergence
  - neural
date: 2026-08-29 22:20
source: GetNotes
score: 60
---

## Original Note

---
note_id: 1919837915170618808
title: "iNEST落地方案"
type: plain_text
created: 2026-08-29 15:26:30
source: getnote
kb: 
---

# iNEST落地方案

# 沿"非线性动力学器件 → 类生物物理神经网络 → 智能涌现"路径的系统性梳理与iNEST落地方案

## 一 · 周芃博士这条技术路线的本质与iNEST的映射

周芃在UCSC蔡少棠、Jason Eshraghian、Wei D. Lu联合团队的博士工作（MEMprop，*IEEE JETCAS* 2022）把握住了一个关键点：**RRAM/忆阻器的高阶动力学不是"非理想性"，而是计算资源本身**。他把两颗Knowm忆阻器加一个电容组成的MIF神经元（Memristive Integrate-and-Fire）直接写进SPICE微分方程，用前向Euler展开成可微计算图，让BPTT穿透器件的物理演化——这与iNEST"物理网络的时空协同复杂度超过阈值时涌现智能"的第一性原理在方法论上同源：**都主张让物理演化本身成为计算，而不是把物理层抽象为非理想性再去补偿**[[原论文](https://arxiv.org/abs/2206.12992)]。

对iNEST而言，可以直接沿用的三条设计准则：

一· 器件层：把非易失/易失忆阻器的开关动力学、阈值切换、离子漂移作为神经元/突触的天然物理实现，而不是数字LIF的载体。

二· 网络层：BPTT+STDP+E/I平衡+BMC等局部规则组成"多尺度自组织栈"，让全局动力学从局部规则中涌现。

三· 系统层：以晶圆级/面板级异构异质集成撑起物理神经元数量与拓扑维度，用SDI在其上做动态可塑的连接编排。

---

## 二 · 与周芃工作平行或后续的关键学术成果

### 2.1 全忆阻SNN与动力学神经元（与MEMprop同一谱系）


| 工作                                                                                                                                                                                   | 核心贡献                                   | 对iNEST的价值  |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------- | ---------- |
| Wang Z. et al., *Nat. Electron.* 2018（Wei Lu组）"Fully memristive neural networks for pattern classification with unsupervised learning"                                               | 8×8全忆阻SNN，扩散型忆阻器做LIF神经元＋非易失做突触，STDP无监督 | 全忆阻SNN的原型  |
| Duan Q. et al., *Nat. Commun.* 2020"Spiking neurons with spatiotemporal dynamics and gain modulation for monolithically integrated memristive neural networks"                       | 单片集成三元件神经元（R+M+C），具时空动力学与增益调制          | 神经元最小工程配方  |
| Kiani F. et al., *Sci. Adv.* 2021 (Qiangfei Xia/Yang JJ) "A fully hardware-based memristive multilayer neural network"                                                               | 全硬件多层忆阻器神经网络，梯度可部分离线计算                 | 硬件多层实现     |
| Shi X. et al. (MIND 2025, 皇后大学Belfast) "Memristive dynamical spiking neural networks with spatiotemporal heterogeneity" [[PDF](https://pure.qub.ac.uk/files/654150277/MIND2025.pdf)] | MEMprop的直接后继，把时空异质性作为可训练变量             | 异质性=表征容量   |
| Wan W. et al., *Nature* 2022 "NeuRRAM: 48 CIM cores, 3M RRAM" [[Nature](https://www.nature.com/articles/s41586-022-04992-8)]                                                         | 双向电压驱动的CIM核，MNIST/CIFAR/语音/图像重建全通用     | 大规模异构任务基准  |
| Yao P. et al. (吴华强), *Nature* 2020 "Fully hardware-implemented memristor CNN" [[PubMed](https://pubmed.ncbi.nlm.nih.gov/31996818/)]                                                  | 八颗2048-cell阵列，混合训练达到软件相当精度             | 大规模阵列一致性方案 |
| Yu R. et al., *Nat. Commun.* 2025 "A full-stack memristor-based CIM system" [[Nature](https://www.nature.com/articles/s41467-025-57183-0)]                                           | 多芯片可编排，支持多种AI数据流                       | 系统级"栈"参考   |


### 2.2 自组织液态网络（与iNEST"液态硬件"最贴合）

蔡少棠"边缘混沌（Edge of Chaos）"理论在物理器件上得到验证的两条主线：

**纳米线网络（NWN）**——Sydney大学Kuncic组、Polimi/INRiM的Milano组：

- Hochstetter J. et al., *Nat. Commun.* 2021 "Avalanches and edge-of-chaos learning in neuromorphic nanowire networks"——证明自组织银纳米线网络在临界态附近学习性能最佳，出现类神经雪崩（幂律）[[Nature](https://www.nature.com/articles/s41467-021-24260-z)]。
- Milano G. et al., *Nat. Commun.* 2022（引用549次）"In materia reservoir computing with a fully memristive architecture based on self-organized nanowire networks"——完全在材料内做储备池计算。
- Milano G. et al., *Nat. Commun.* 2025 "Self-organizing neuromorphic nanowire networks as stochastic dynamical systems"[[Nature](https://www.nature.com/articles/s41467-025-58741-2)]。

这一路线正是iNEST"物理液态网络"的现成实验证据：**局部STDP-like规则 + 网络自组织拓扑 → 全局临界动力学 → 高计算表达力**。

**光电/有机in-materia计算**：

- Cui H. et al., *Nat. Commun.* 2025 "A bioinspired in-materia analog photoelectronic reservoir computing system"[[Nature](https://www.nature.com/articles/s41467-025-56899-3)]。
- Ferrarese Lupi F. et al., *Adv. Mater.* 2025 "Neuromorphic light-responsive organic matter for in-materia computing"[[Wiley](https://advanced.onlinelibrary.wiley.com/doi/10.1002/adma.202501813)]。
- *Nature Reviews* 2025 "Training of physical neural networks"综述——PNN训练算法全景。

### 2.3 晶圆级/大规模异质集成（iNEST工程载体的最新参考）


| 工作                                                                                                                                                                                                         | 关键指标             | 借鉴点             |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------- | --------------- |
| Choi S. et al., *Nat. Commun.* 2025 "Wafer-scale fabrication of memristive passive crossbar circuits for brain-scale neuromorphic computing"[[Nature](https://www.nature.com/articles/s41467-025-63831-2)] | 无源交叉阵列晶圆级工艺，脑级密度 | 无源密度基线          |
| DGIST 2025新型晶圆级忆阻器集成技术[[TechXplore](https://techxplore.com/news/2025-11-memristor-wafer-technology-paves-brain.html)]                                                                                      | 可扩展手动交叉阵列晶圆工艺    | 工艺可行性           |
| Schranghamer T. F. et al., *Nat. Commun.* 2025 "Large-scale crossbar arrays based on three-terminal MoS₂ memtransistors"[[Nature](https://www.nature.com/articles/s41467-025-64536-2)]                     | 2D三端器件替代1T1R     | 器件密度与调控能力       |
| An Y. S. et al. 2025 "Monolithic 3D integrated TiOₓ memristor"（*Nano Energy*）                                                                                                                              | 单片3D、缓解sneak电流   | 3D堆叠垂直集成        |
| Cerebras WSE-3                                                                                                                                                                                             | 46,225 mm²、900k核 | 晶圆级封装/供电/散热工程范式 |


### 2.4 局部学习规则与涌现（EI平衡、BMC类）

- Barzon G. et al., *Phys. Rev. Lett.* 2025 "Excitation-Inhibition Balance Controls Information Encoding in Neural Populations"——**证明信息在临界稳定边缘（E/I平衡处）达到最大**[[APS](https://link.aps.org/doi/10.1103/PhysRevLett.134.068403)]。这是iNEST"E/I平衡→涌现智能"的关键理论支撑。
- Serrano-Gotarredona T. et al. "STDP and STDP Variations with Memristors"经典综述——所有主流STDP波形与忆阻器实现的映射表。
- Zhou W. et al., *Neural Networks* 2023 "Forgetting-memristor-based STDP learning circuit"——含遗忘动力学的STDP电路。
- Karamimanesh M. et al., *Sci. Rep.* 2026 "A fully-CMOS spiking LIF neuron for on-chip STDP-like learning"[[Nature](https://www.nature.com/articles/s41598-026-55364-5)]。

### 2.5 连续时间/液态动力学的算法层

- Hasani R. et al. (MIT/Liquid AI) "Liquid Time-constant Networks" AAAI 2021、"Closed-form continuous-time neural networks" *Nat. Mach. Intell.* 2022——**连续时间RNN的理论骨架**，与忆阻器MIF神经元的连续时间动力学天然同构，可直接作为iNEST算法层的正统模型。
- Predictive Coding / FEP：Friston系列——为iNEST的"最小自由能+最小作用量"提供数学形式。

---

## 三 · 开源代码 · 仿真工具 · 验证环境（可以立即拉下来跑）

### 3.1 器件与阵列层仿真


| 工具                                            | 仓库                              | 能力                                                                | iNEST用途      |
| --------------------------------------------- | ------------------------------- | ----------------------------------------------------------------- | ------------ |
| **snnTorch**                                  | github.com/jeshraghian/snntorch | Eshraghian团队维护，PyTorch原生，支持surrogate gradient、BPTT，MEMprop范式的直接工具 | 神经元级/网络级差分训练 |
| **MemTorch**                                  | github.com/coreylammie/MemTorch | 大规模忆阻DL仿真，注入器件非理想性；PyTorch直插                                      | 器件—网络协同仿真    |
| **IBM AIHWKit**                               | github.com/IBM/aihwkit          | RPU tile仿真，混合精度AIMC，脉冲编程模型                                        | 训练/推理精度评估    |
| **NeuroSim V1.5 / DNN+NeuroSim**              | github.com/neurosim             | 电路级面积/功耗/延迟基准，PyTorch接口                                           | 芯片PPA基准      |
| **NeuroPack**                                 | Prodromakis组开源                  | 脉冲SNN仿真，权重更新时纳入器件动力学                                              | SNN局部规则实验    |
| **PySpice仿真SNN in-situ学习** *Electronics* 2024 |                                 | SPICE内在训练                                                         | SPICE级RTL验证  |


### 3.2 神经形态硬件与验证平台


| 平台                                             | 属性              | 用途                    |
| ---------------------------------------------- | --------------- | --------------------- |
| Intel Loihi 2 + Lava框架                         | 128核异步脉冲、开源Lava | STDP/E-I平衡等规则的数字侧原型验证 |
| BrainScaleS-2（海德堡）                             | 混合信号加速仿真        | 亚阈值模拟神经元验证            |
| SpiNNaker 2                                    | 大规模脉冲仿真机        | 网络级涌现行为压力测试           |
| Prophesee EVK + DVS128 Gesture                 | 事件相机数据          | 具身感知输入端               |
| PyNN / Nengo / Norse / BindsNET / SpikingJelly | 通用SNN前端         | 算法—硬件协同               |
| NanoWireNetworkPy（Kuncic组）                     | NWN模拟           | 液态网络临界性研究             |
| **NEST 3.x**（同名巧合，但正是标准E/I仿真器）                 | 大规模生物级SNN       | E/I平衡、BMC、临界性验证       |


### 3.3 数据集与任务基准

- 静态：MNIST / FashionMNIST / CIFAR-10。
- 神经形态：DVS128 Gesture、N-MNIST、N-Caltech101、SHD（听觉脉冲）。
- 具身：Habitat 3.0、Isaac Sim、Genesis（连续控制/OODA闭环）。
- 涌现指标：Fisher信息、幂律指数、临界性κ、Lempel-Ziv复杂度、φ*（IIT）。

---

## 四 · iNEST"晶圆级/面板级异构异质集成 + SDI液态网络"可行性方案

### 4.1 总体架构（三层+一环）

```
┌──────────────────────────────────────────────────────────┐
│  L3 具身闭环层：OODA + 最小自由能/最小作用量 + STDP        │
│      (Habitat/Isaac Sim 闭环 + 真实机器人)                │
├──────────────────────────────────────────────────────────┤
│  L2 SDI 动态可塑连接层（Software-Defined Interconnect）    │
│      光互连/CoWoS-L/UCIe/硅光波导 + FPGA控面 + 路由表      │
├──────────────────────────────────────────────────────────┤
│  L1 物理神经元/突触阵列层（Wafer/Panel 异质异构）           │
│      RRAM+PCM+FeFET+MoS2+纳米线自组织片 + 3D堆叠          │
└──────────────────────────────────────────────────────────┘
              ↑↓  局部规则闭环（STDP/EI/BMC）  ↑↓
```

### 4.2 L1 · 器件与阵列（工程可行性）

一· 主力器件矩阵，采用"三型互补"：

　　（一）非易失突触——TaOₓ/HfOₓ RRAM（1T1R，可承接吴华强、Wei Lu的成熟工艺），承担连接权重；

　　（二）易失神经元——扩散型Ag/SiOₓ阈值切换器件或Mott绝缘体（NbO₂/VO₂），承担MIF/Neuristor动力学；

　　（三）三端调制——MoS₂ memtransistor（Schranghamer 2025）承担增益调制/E-I开关。

二· 集成路径：

　　（一）先落地"晶圆级Chiplet+3D堆叠"，参考DGIST 2025与Choi 2025的无源晶圆工艺，把RRAM作为BEOL集成在CMOS基底之上；

　　（二）"晶矩（Reticle-scale tile）+ UCIe/D2D 互联"作过渡形态，规避良率瓶颈；

　　（三）终极形态："面板级"通过Fan-out Panel-Level Packaging（FOPLP）扩展到>晶圆面积，参考Cerebras的供电/散热范式，但把核心从数字SLA核换成模拟忆阻单元。

三· 单Tile规格建议（一期原型）：

　　（一）单Tile 512×512 1T1R RRAM，功能密度 ≈ 60 Mcell/mm²；

　　（二）每Tile集成 ≈ 4k易失神经元器件；

　　（三）Tile内BEOL布置纳米线自组织"液态子池"以引入天然复杂动力学（Milano 2022范式）。

### 4.3 L2 · SDI动态可塑连接（iNEST最核心的差异化）

**SDI = Software-Defined Interconnect**，把互连从ASIC硬布线升级为可编程矩阵。工程实现三选一或叠加：

一· **硅光交换阵列**（Lightmatter/Ayar Labs范式）——微环谐振/MZI矩阵，λ和相位可控，10ps量级重构，实现"物理波长复用"的多路复用突触。

二· **FPGA/CGRA可编程路由片**贴附在晶圆边缘——控制面用OpenROAD/RapidStream的思路生成路由表，数据面走UCIe D2D。

三· **BEOL可编程通路** = 用RRAM本身做交叉点开关的"网络中的网络"（Network-of-Networks），把连接权重和连接拓扑都放到同一物理层。

**动态可塑的三级时间尺度**：

　　（一）ns级：忆阻器件电导演化（STDP）；

　　（二）μs~ms级：SDI局部路由重配（相当于"突触发芽/剪枝"）；

　　（三）s级以上：拓扑级重构（等效"神经发生"），由L3的自由能目标驱动。

### 4.4 L3 · 局部规则栈驱动全局涌现

在同一物理网络上叠加四类规则，通过FPGA控面并行推送：

一· **STDP + 遗忘**（Serrano-Gotarredona、Zhou 2023）→ 无监督表征。

二· **E/I平衡**（Barzon 2025的Physical Review Letters结论：临界稳定边缘信息最大）→ 通过MoS₂三端器件按80:20调制。

三· **BMC（Balanced/Meta-plasticity/Homeostasis）** → 长时程gain scaling，防止爆发/沉默。

四· **梯度回填**（MEMprop、Shi 2025）→ 稀疏、低频、用于关键任务微调，不覆盖局部涌现。

上层用**Free Energy Principle**统一目标：Loss = 感知预测误差 + 动作代价 + 复杂度项（KL），对应"最小自由能+最小作用量"。

### 4.5 分阶段落地路线（24个月节奏）


| 阶段                        | 时间      | 目标                                                           | 交付物                            |
| ------------------------- | ------- | ------------------------------------------------------------ | ------------------------------ |
| 阶段一 · 仿真验证                | M0–M6   | 用snnTorch + AIHWKit + NeuroSim复现MEMprop，扩展到E/I+STDP+SDI路由    | 完整可微仿真栈+iNEST-Sim v0.1         |
| 阶段二 · 单Tile流片             | M6–M15  | 65nm/28nm CMOS + BEOL RRAM，512×512 1T1R + Mott神经元 + 边缘FPGA控面 | iNEST-Tile v1，跑DVS128、SHD      |
| 阶段三 · 多Tile Chiplet + SDI | M12–M20 | 4–16 Tile通过UCIe/硅光互连，动态路由                                    | iNEST-WSI v1，具身闭环Habitat/Isaac |
| 阶段四 · 面板级异构异质集成           | M18–M24 | FOPLP面板级+3D堆叠+纳米线液态子池                                        | iNEST-Panel v1，感知/反应/适应智能等级验证  |


### 4.6 智能等级评定的物理可测指标

对应用户"六等级"（感知/反应/适应/创造/通用/超级），在iNEST硬件上建议如下可观测量：

- **感知**：Fisher信息 & 稀疏度；
- **反应**：闭环延迟、能效（TOPS/W下的脉冲率）；
- **适应**：在线STDP导致的分布漂移下的鲁棒性；
- **创造**：网络在临界态下的Lempel-Ziv复杂度与幂律指数κ；
- **通用**：跨任务迁移的表征距离（CKA）；
- **超级**：整合信息φ*（IIT）与自由能下降速率的联合曲线。

---

## 五 · 需要重点关注的若干"低垂果实"

一· **直接扩MEMprop为E/I异质版本**——Shi 2025已给出方向，把E/I比、时间常数、E_rest/E_reset全部作为可学习参数，能立刻在MNIST/DVS128以上取得非线性提升，同时天然映射到晶圆异质工艺的器件差异。

二· **NWN液态子池嵌入CIM Tile**——Milano组的自组织银纳米线膜可用低温工艺沉积到CMOS BEOL上，作为一个"物理储备池"接入交叉阵列，等价于给每个Tile内置一个"临界态"引擎，规避Cortex-like拓扑难以规则化生长的难题。

三· **硅光SDI + UCIe混合互连**——不要求全片硅光，采用"电中近程 + 光远程"的分层SDI，可以在24个月内成型。

四· **仿真链闭环**——推荐iNEST内部把 snnTorch（算法可微）→ AIHWKit（器件非理想）→ NeuroSim（PPA）→ Lava（Loihi 2数字对照）串成同一Docker流水线，作为项目"数字孪生"，保证从算法到晶圆的一致性。

---

## 六 · 结语

周芃的MEMprop在方法论上完成了一次关键跃迁——**让物理动力学进入梯度计算图**；蔡少棠的"边缘混沌"给出了智能涌现的复杂性判据；Milano/Kuncic的自组织纳米线给出了"液态"的物理原型；晶圆级/面板级异构异质集成与SDI给出了工程可行的载体。**iNEST在此之上真正独特的贡献，是把这四条本来相互孤立的路径缝合为一个可运行的技术栈**：以物理网络的时空复杂度为第一性原理，以局部规则栈生成全局动力学，以晶圆/面板级集成撑起物理规模，以SDI承载动态可塑——这是当前学术界尚未有人系统闭合的、可以直接申报"具身物理智能"重大专项的完整命题。

如果需要，我可以下一步为您（一）搭出iNEST-Sim v0.1的可运行代码骨架（snnTorch+AIHWKit+NeuroSim联合仿真），（二）撰写"晶圆级异构异质集成+SDI液态网络"重点研发计划的正式项目建议书折子（中文半角、按您指定格式），或（三）生成一份用于院士汇报的16:9演示。

---
*getnote | 2026-08-29 22:20*


---

## Related Notes

[[SDI化合物键_四型架构]]
[[paper1_iNEST_core_architecture]]
[[iNEST-MOC]]
[[Papers-MOC]]
[[变分自由能F]]
[[STDP-FEP梯度下降统一映射]]
[[自组织临界态SOC]]
[[FPGA原型]]
