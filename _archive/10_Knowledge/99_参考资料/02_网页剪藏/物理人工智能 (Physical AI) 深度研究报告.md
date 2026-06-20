---
title: 物理人工智能 (Physical AI) 深度研究报告
source: https://zhuanlan.zhihu.com/p/1992326790232957691
author:
  - "[[码夫祥子​软件开发行业 从业人员]]"
published:
created: 2026-04-27
description: 物理人工智能 (Physical AI) 深度研究报告：从比特世界的认知到原子世界的重塑1. 绪论：物理人工智能的范式定义与认知跨越1.1 物理人工智能 (PAI) 的概念重构与多维定义物理人工智能（Physical AI，简称 PAI）并非…
tags:
  - clippings
---
## 物理人工智能 (Physical AI) 深度研究报告：从比特世界的认知到原子世界的重塑

## 1\. 绪论：物理人工智能的范式定义与认知跨越

### 1.1 物理人工智能 (PAI) 的概念重构与多维定义

物理人工智能（Physical AI，简称 PAI）并非单一技术的迭代，而是人工智能发展史上一次根本性的范式转移。它标志着 AI 从处理符号、文本和图像的“比特世界”（Bit World）向直接操纵物质、能量和实体的“原子世界”（Atom World）的跨越 1。

学术界对 PAI 的定义具有极高的严谨性。根据发表在《Nature Machine Intelligence》上的权威定义，PAI 是指“创建能够执行通常与智能生物相关的任务的物理系统的理论与实践” 3。这一定义的核心在于“物理系统”与“智能”的不可分割性。不同于传统的机器人学（Robotics），PAI 不仅仅是为机械躯体安装一个智能软件大脑，而是强调智能必须通过材料、机械结构、传感器和驱动器的深度融合来涌现。正如 Empa 机器人中心所指出的，PAI 是材料科学、机械工程、计算机科学、生物学和化学五大基础学科的交叉产物 3。

工业界对 PAI 的理解则更侧重于其应用价值与交互能力。AWS 将 PAI 定义为一个集成了感知、理解、推理和学习的软硬件系统，其核心目标是与物理世界进行交互 1。这里的关键区别在于“推理与物理后果的耦合”。传统的 AI 模型（如 ChatGPT）可以推理出“如何倒一杯咖啡”的步骤描述，但 PAI 模型必须首先定位咖啡的物理坐标，理解液体的流体动力学特性，规划机械臂的轨迹，并实时调整抓握力以防止杯子滑落或破碎 1。这种能力被称为“ [具身智能](https://zhida.zhihu.com/search?content_id=268703924&content_type=Article&match_order=1&q=%E5%85%B7%E8%BA%AB%E6%99%BA%E8%83%BD&zhida_source=entity) ”（Embodied Intelligence），但在 PAI 的语境下，它更强调“工程实现的计算化”——即不仅仅是哲学上的具身，而是通过工程系统（如机器人、自动驾驶汽车）在物理实体中实现计算智能 4。

### 1.2 具身智能与物理人工智能的辩证关系

尽管“具身智能”（Embodied AI）与 PAI 常被混用，但二者在学术光谱上存在细微差别。具身智能是一个源自认知科学和生物学的广泛概念，它主张认知不仅仅是大脑的产物，而是身体、环境与大脑动态交互的结果 4。在 AI 研究中，具身智能的研究对象可以包括仿真环境（Simulation）中的虚拟代理（Virtual Agents）。

相比之下，物理人工智能（PAI）是具身智能在现实物理世界中的严格实现。它排除了纯虚拟的仿真代理，专注于那些必须面对现实世界物理法则（如重力、摩擦力、接触动力学）挑战的实体系统 4。XenonStack 的研究指出，PAI 的独特之处在于其“具身性”（Embodiment）——即通过机械运动、环境感知和自适应决策的结合，填补了感知、认知与行动之间的鸿沟 5。简而言之，具身智能提供了理论基础，而物理人工智能则是其在工程上的终极表达。

### 1.3 破解莫拉维克悖论：进化的启示

PAI 的核心挑战在于解决著名的“莫拉维克悖论”（Moravec's Paradox）。该悖论指出：让计算机在智力测试、下棋或逻辑推理方面达到成人水平相对容易，但在感知能力和移动能力（如一岁婴儿般的行走和抓取）方面达到人类水平却极其困难 6。

这一悖论的生物学解释在于进化的时间尺度。人类的高级推理能力（如抽象思维、数学）仅进化了数万年，因此其生物学实现相对简单且“浅层”，易于被逆向工程和算法化。然而，人类的感知运动能力（Sensorimotor Skills）——如在复杂地形行走、识别物体、手眼协调——是经过数亿年自然选择优化的结果。这些能力根植于深层的无意识神经回路中，极其高效且鲁棒，但难以通过传统的符号逻辑或规则编程来复制 6。

PAI 的发展正是为了攻克这一堡垒。通过引入神经网络、深度强化学习（Deep RL）以及模仿人类神经系统的神经 [形态计算](https://zhida.zhihu.com/search?content_id=268703924&content_type=Article&match_order=1&q=%E5%BD%A2%E6%80%81%E8%AE%A1%E7%AE%97&zhida_source=entity) （Neuromorphic Computing），PAI 试图在机器中重建这种经过亿万年进化的感知运动智能。正如 XPENG AI Day 所强调的，当数字世界的算法进化（大模型）与物理世界的能源革命（新能源与电驱）相遇时，PAI 使得机器能够从“各种各样的任务”向“通用物理任务”进化，这正是对生物进化历程的一种技术重演 2。

---

## 2\. 演进史：从规则束缚到通用智能的觉醒

PAI 的发展并非一蹴而就，而是经历了从刚性自动化到柔性感知，再到通用认知的三个关键阶段。这一过程反映了人类对“机器智能”理解的不断深化。

### 2.1 规则基机器人 (Rule-based Robotics)：工业自动化的序章 (1960s - 2000s)

物理自动化的历史可以追溯到 1960 年代，以 Unimate 机械臂为代表。这一时期的机器人被称为“规则基机器人”。其核心特征是“确定性”与“结构化”。

- 技术逻辑： 工程师需要显式地编写每一条运动指令（如“移动到坐标 X,Y,Z”）。系统的运行依赖于预定义的规则和极其精确的物理模型。
- 局限性： 这种系统缺乏对环境的感知与适应能力。它们必须在严格控制的结构化环境（如汽车流水线）中工作，一旦环境发生微小变化（如零件位置偏移 1 厘米），机器人就会失败。正如世界经济论坛报告所述，这些机器人虽然具备惊人的速度和精度，但本质上是“盲目”的执行机构，不具备智能 7。
- 历史地位： 这一阶段解决了“重复劳动”的问题，但未能触及“智能”的本质。

### 2.2 训练基机器人 (Training-based Robotics)：感知的引入与学习的萌芽 (2000s - 2020)

随着计算机视觉和机器学习的发展，机器人开始具备初步的感知能力，进入“训练基机器人”时代。

- 技术突破： 统计机器学习（Statistical AI）开始取代符号 AI。SLAM（同步定位与地图构建）技术的成熟使移动机器人（如扫地机器人、AGV）能够在未知环境中导航。波士顿动力（Boston Dynamics）的机器人通过复杂的控制理论和动力学模型展示了卓越的运动能力，但其核心仍高度依赖人工设计的控制器。
- 深度学习的介入： 2015 年左右，深度强化学习（Deep RL）的兴起让研究者开始尝试让机器人通过“试错”来学习技能。然而，物理世界的试错成本极高，数据采集效率低下。因此，这一阶段过度依赖仿真（Simulation）技术，试图通过 Sim-to-Real（仿真到现实）迁移来解决数据匮乏问题 7。

### 2.3 上下文感知机器人 (Context-based Robotics)：大模型驱动的通用智能 (2021 - 至今)

ChatGPT 和 Transformer 架构的爆发，将 PAI 推向了“上下文感知”的新纪元。

- 核心特征： 这一代机器人不再仅仅执行特定任务，而是能够通过大模型理解复杂的自然语言指令、感知环境语义，并进行常识推理（Common Sense Reasoning）。
- 技术跃迁： 视觉-语言-动作（VLA）模型的出现，打破了感知、认知与行动的界限。机器人不再需要针对每个任务单独编程，而是可以通过观察互联网海量视频数据学习通用的物理常识。例如，Google 的 RT-2 和 NVIDIA 的 GR00T 项目展示了机器人如何将图像和语言转化为具体的机械动作，实现了从“专用工具”向“通用代理”的质变 9。这标志着 PAI 正式进入了能够处理非结构化环境、理解人类意图的“物理智能”阶段。

---

## 3\. 核心原理与架构：构建物理智能的“三位一体”

物理人工智能的实现依赖于三个核心维度的深度融合：作为身体的形态计算、作为大脑的基础模型，以及连接虚拟与现实的仿真进化。

### 3.1 形态计算 (Morphological Computation)：身体即算法

在传统机器人学中，控制算法被视为智能的唯一载体，而机械结构仅仅是执行器。PAI 颠覆了这一观点，引入了“形态计算”理论，认为机器人的物理身体本身就是计算过程的一部分。

### 3.1.1 计算卸载 (Computational Offloading)

形态计算的核心思想是利用物理系统的自然动力学特性来替代复杂的中央控制算法。这种机制被称为“计算卸载”。

- 原理解析： 传统的刚性机器人抓取一个形状复杂的物体（如一个软柿子）需要极其复杂的力反馈控制和精确的路径规划，以防止物体损坏。而在 PAI 中，通过使用柔性材料（如硅胶手指），机器人在接触物体时，材料会自然地发生形变以适应物体表面。这种形变过程本身就是在“计算”最佳的抓取形状，而不需要中央处理器进行任何几何计算 11。
- 能效优势： 这种利用物理特性（如弹性、阻尼、摩擦）来处理信息的方式，极大地降低了对算力和电力的需求，同时提高了系统的响应速度和鲁棒性。正如生物利用肌腱的弹性来储存能量从而实现高效奔跑一样，PAI 系统通过形态计算实现了“更少的代码，更多的智能” 12。

### 3.1.2 软体机器人技术的材料基础

形态计算的物理载体是软体机器人（Soft Robotics）。这需要材料科学的深度参与。

- 关键材料：
- 弹性体 (Elastomers)： 如硅胶和橡胶，提供柔顺性和被动适应性，是构建柔性执行器的基础 13。
- 水凝胶 (Hydrogels)： 具有高度生物相容性和可调节的含水量，常用于模拟生物组织或作为离子导电介质，实现感知功能 15。
- 形状记忆合金 (SMA)： 在热或电刺激下可发生相变从而产生动作，充当人工肌肉。
- 电活性聚合物 (EAP)： 在电场作用下改变形状，被称为“人造肌肉”，具有响应速度快、变形量大的特点 13。
- 制造工艺： 3D 打印技术（如嵌入式 3D 打印）使得在软体材料中直接集成传感器和电路成为可能，从而实现了“感知-执行”一体化的结构设计 15。

### 3.2 认知引擎：视觉-语言-动作 (VLA) 模型

如果说形态计算赋予了 PAI 适应性的身体，那么 VLA 模型则赋予了它通用的认知大脑。VLA 模型代表了机器人学习领域的最高水平。

### 3.2.1 VLA 架构的技术解构

传统的机器人控制通常是分模块的：感知模块识别物体，规划模块计算路径，控制模块驱动电机。VLA 模型通过 End-to-End（端到端）的 Transformer 架构将这些步骤统一起来。

- 输入模态： VLA 接收多模态输入，包括 RGB 图像（视觉）、自然语言指令（文本）以及机器人的本体感受数据（关节角度、速度） 9。
- 动作的 Token 化 (Action Tokenization)： 这是 VLA 最具革命性的创新。在 Transformer 模型中，文本被处理为 Token。VLA 将机器人的物理动作（如“手腕旋转 5 度”、“抓手闭合”）也离散化为 Token。这意味着，在模型眼中，输出一段莎士比亚的诗句和输出一段机械臂抓取苹果的指令在数学上是等价的——都是序列预测问题 9。
- 三塔架构 (Three-Tower Architecture)： 典型的 VLA（如 RT-2）采用三塔结构：视觉编码器（如 ViT）处理图像，语言编码器（如 LLM）处理指令，本体感知编码器处理状态。这三股信息流在共享的 Transformer 主干中融合，最终输出动作 Token 9。

### 3.2.2 世界模型与想象力

先进的 PAI 系统不仅能反应，还能预测。XPENG VLA 2.0 和 NVIDIA GR00T 等系统集成了“世界模型”（World Model）。

- 预测与推理： 世界模型允许机器人在执行动作之前，在“脑海”中模拟物理世界的演变。例如，如果机器人想要拿起一个玻璃杯，世界模型可以预测“如果用力过大，杯子会碎”。这种能力使 PAI 具备了处理长尾场景（罕见、突发情况）的能力，因为它可以通过内在的模拟来预演后果，而不仅仅依赖记忆中的训练数据 2。

### 3.3 从仿真到现实 (Sim-to-Real)：进化的加速器

由于真实世界的物理数据采集成本极高且危险，PAI 的训练高度依赖仿真环境。

### 3.3.1 DrEureka 与自动化领域随机化

如何保证仿真中训练的策略在现实中有效？这是 Sim-to-Real 的核心难题。

- DrEureka 算法： 这是一个利用 LLM 自动化设计 Sim-to-Real 流程的突破性技术。在过去，工程师需要手动调整仿真参数（如摩擦系数、重力加速度）来匹配现实。DrEureka 利用 LLM 编写奖励函数（Reward Function），并自动配置领域随机化（Domain Randomization）参数。它生成的策略在四足机器人瑜伽球平衡等高难度任务中，表现优于人类专家设计的策略 18。
- 机制： LLM 根据任务描述和物理模拟反馈，不断迭代奖励函数代码，通过在仿真中引入大量的随机扰动（如地面湿滑度变化、电机扭矩波动），训练出具有极强鲁棒性的策略，从而无缝迁移到现实世界。

### 3.3.2 合成数据工厂

NVIDIA 的 Isaac Lab 和 GR00T-Mimic 展示了数据生成的工业化。通过少量的真实人类演示，系统可以生成数百万条合成轨迹。这些合成数据不仅包含了动作，还通过 NVIDIA Cosmos Transfer 等工具增强了视觉逼真度，使得训练数据在规模上达到了“互联网级别”，从而能够训练出通用的基础模型 21。

---

## 4\. 硬件实现：解构 PAI 的解剖学

PAI 系统的硬件不仅仅是机械组件的堆叠，而是按照仿生学原理构建的精密系统，涵盖了驱动（肌肉）、感知（皮肤与神经）和计算（边缘大脑）。

### 4.1 驱动系统：寻找完美的“人造肌肉”

驱动器决定了机器人的力量、速度和能效。目前主要有三种技术路线：

| 驱动技术 | 代表平台/技术 | 优势 | 劣势 | 适用场景 |
| --- | --- | --- | --- | --- |
| 电驱系统 (Electric) | Tesla Optimus, Unitree G1 | 精度高，控制成熟，供应链完善，维护成本低 | 功率密度较低，刚性较大，难以实现极高的爆发力 | 通用制造，家庭服务，移动操作 22 |
| 液压系统 (Hydraulics) | Sanctuary Phoenix | 功率密度极高，体积小力量大，响应速度快，耐冲击 | 易泄漏，维护复杂，成本高，噪音大 | 精细工业操作，需要大力矩的小空间场景 24 |
| 人工肌肉 (Artificial Muscle) | HASEL, 磁性聚合物 | 仿生特性，柔顺性好，自愈合，能量密度高 | 技术尚在实验室阶段，控制非线性强，耐久性待验证 | 未来软体机器人，医疗康复，微型机器人 26 |

- 液压技术的微型化突破： Sanctuary AI 使得液压技术焕发新生。他们研发的微型液压阀比工业标准快 50 倍，且成本降低 6 倍。这种微型液压系统使得 Phoenix 机器人的手部在保持人类尺寸的同时，具备了远超电驱系统的力量和灵巧度，能够完成穿针引线等精细动作 24。
- HASEL 执行器： 这是一种液压放大自愈静电致动器，结合了软体机器人的柔顺性和电机的高频响应。它通过电场驱动液体介质，模拟肌肉的收缩。最新的 HASEL 设计不仅成本降低，还具备自愈功能（电击穿后可恢复），是未来 PAI 驱动的重要方向 26。
- 磁性人工肌肉： UNIST 开发的新型磁性聚合物材料，能够举起自身重量 4000 倍的物体，并通过磁场编程改变刚度（从橡胶态到硬塑料态），这种“变刚度”特性是实现多功能操作的关键 29。

### 4.2 神经形态感知：赋予机器“痛觉”

触觉是机器人与物理世界安全交互的最后一道防线。

- [神经形态电子皮肤](https://zhida.zhihu.com/search?content_id=268703924&content_type=Article&match_order=1&q=%E7%A5%9E%E7%BB%8F%E5%BD%A2%E6%80%81%E7%94%B5%E5%AD%90%E7%9A%AE%E8%82%A4&zhida_source=entity) (Neuromorphic E-Skin)： 传统的触觉传感器只传输压力数值。中国研究团队开发的 NRE-skin 模拟了生物神经系统的“脉冲编码”机制。它将压力、纹理等信息编码为脉冲信号（Spikes）。更具革命性的是，它集成了“痛觉感知”——当外界刺激超过阈值时，皮肤会直接触发局部的反射弧 (Reflex Arc)，指令执行器回缩，这一过程无需经过中央大脑处理。这种仿生反射机制极大地提高了机器人的反应速度（毫秒级）和自我保护能力 30。
- 多模态融合皮肤： 剑桥大学和 UCL 研发的离子导电水凝胶皮肤，利用电阻抗断层扫描（EIT）技术，无需复杂的布线即可在单一材料上同时感知压力、温度和湿度，并通过机器学习解析极其微细的触觉模式 33。

### 4.3 边缘计算：大脑的本地化

PAI 必须在本地（Edge）进行实时推理，依赖云端会导致致命的延迟。

- 神经形态芯片 (Neuromorphic Chips)： 为了解决能耗问题，Intel Loihi 2 和 BrainChip Akida 等神经形态芯片模仿大脑的“事件驱动”机制（Event-driven）。它们只在检测到变化（Spike）时才消耗能量，这使得在边缘端运行复杂的 SNN（脉冲神经网络）成为可能，能效比传统 GPU 高出数个数量级 35。
- VLA 的边缘部署： NVIDIA Jetson Thor 和 T4000 模块专为人形机器人设计，提供高达 800 TOPS 的算力，旨在本地运行 7B 参数以上的 VLA 模型。LiteVLA 等轻量化模型架构通过 4-bit 量化技术，使得在资源受限的嵌入式设备（如 Raspberry Pi）上运行 [视觉-语言-动作模型](https://zhida.zhihu.com/search?content_id=268703924&content_type=Article&match_order=1&q=%E8%A7%86%E8%A7%89-%E8%AF%AD%E8%A8%80-%E5%8A%A8%E4%BD%9C%E6%A8%A1%E5%9E%8B&zhida_source=entity) 成为可能，虽然这伴随着精度和推理速度的权衡 37。

---

## 5\. 全球 PAI 平台深度对标与技术路线分析

当前，PAI 领域呈现出百花齐放的态势，各家科技巨头和初创公司选择了截然不同的技术路线。以下是对主流平台的深度技术对标。

### 5.1 平台参数与架构对比表

| 平台名称 | 开发商 | 核心驱动技术 | 智能/模型架构 | 关键特性 | 目标场景 |
| --- | --- | --- | --- | --- | --- |
| Optimus Gen 3 | Tesla | 电驱 (行星滚柱丝杠) | 端到端神经网络 (FSD迁移) | 22 DoF 灵巧手，汽车级供应链，可制造性强 | 大规模制造，通用劳动力 |
| Figure 02 | Figure AI | 电驱 | OpenAI VLA 模型 (语音-语音推理) | 强大的语义理解与推理，一体化外骨骼设计 | 工厂物流 (BMW)，家庭服务 |
| Phoenix | Sanctuary | 微型液压 + 电驱 | Carbon AI + 触觉反馈 | 超高灵巧度，仿生手部动作，极高功率密度 | 精细工业操作，遥操作数据采集 |
| G1 Ultimate | Unitree | 高扭矩电驱 | UnifoLM 机器人大模型 | 43 DoF (含腰部/手)，360° LiDAR，极高性价比 | 教育科研，通用服务，大规模部署 |
| Neo | 1X | 肌腱驱动 (Tendon) | EVE 具身智能 + 专用 LLM | 本质安全 (软体/无夹点)，静音，类人柔顺运动 | 家庭伴侣，家务劳动 |
| Digit v4 | Agility | 电驱 (反向膝关节) | 混合控制 (RL + 经典) | 物流优化设计，高稳定性，已商业化 | 仓储物流，搬运 |

### 5.2 典型技术路线深度解析

### 5.2.1 Tesla Optimus：可制造性优先的工业主义

Tesla 的核心逻辑是“量产”。Optimus Gen 3 没有追求液压的极致性能或软体的极致安全，而是选择了最为成熟、供应链最完善的电驱方案。其行星滚柱丝杠执行器经过了 2000 万次的循环测试，确保了工业级的耐用性。Tesla 最大的护城河在于其数据闭环——利用百万辆 Tesla 汽车收集的视觉数据和 FSD 芯片的算力，Optimus 能够快速迭代其视觉感知算法。其手部设计从 11 个自由度增加到 22 个，正是为了适应工厂中复杂工具的操作 22。

### 5.2.2 Figure 02：硅基智能的物理化身

Figure 02 代表了“软件定义硬件”的极致。通过与 OpenAI 的深度合作，Figure 02 的“大脑”直接接入了最先进的 VLM。这使得它在理解模糊指令（如“把桌上能吃的东西给我”）方面具有压倒性优势。Figure 02 还是首个在机身集成 VLM 进行常识推理的商用机器人，其计算单元的推理能力是前代的 3 倍，电池容量增加了 50% 以支持高强度的 AI 运算 41。

### 5.2.3 Sanctuary Phoenix：液压技术的文艺复兴

Sanctuary AI 走了一条独特的路。他们认为，要实现人类手部的灵巧度（In-hand Manipulation），电机的体积和重量太大。因此，他们复兴了液压技术，利用精密制造的微型阀门实现了惊人的功率密度。Phoenix 的手可以同时完成抓取、调整姿态、按压等精细动作，这在纯电驱手中极难实现。这代表了 PAI 对“物理极致”的追求 24。

### 5.2.4 1X Neo：家庭场景的生物力学解

1X Neo 是为进入人类客厅而设计的。为了彻底解决“夹伤人”的安全隐患，Neo 放弃了刚性传动，采用了肌腱驱动系统，并覆盖了软体外壳。这种设计模仿了人类肌肉和肌腱的运作方式，具有天然的柔顺性（Compliance）。即使机器人失控撞击人体，其软体结构也能吸收能量，确保安全。此外，Neo 采用了“具身思维链”技术，使其能够处理长程家务任务 44。

---

## 6\. 挑战与瓶颈：物理世界的硬约束

尽管 PAI 展现了无限前景，但在大规模普及之前，必须跨越数道物理与工程的鸿沟。

### 6.1 能源鸿沟 (The Energy Gap)：算力与动力的双重饥渴

PAI 面临着严峻的能源挑战。

- 续航短板： 目前主流人形机器人的续航普遍在 2-4 小时（如 Unitree G1, Figure 02），只有 Tesla Optimus 声称能达到 8 小时以上，但这通常是在理想工况下。液压系统（如 Atlas）的续航更是捉襟见肘（<1小时）。
- 能耗结构： 机器人的能耗由致动能耗和计算能耗组成。随着 VLA 模型越来越大，边缘计算的能耗占比显著上升。研究显示，要替代美国制造业和仓储业 50% 的工时，人形机器人每年将消耗 270 亿千瓦时的电力，这是巨大的能源负担 46。
- 效率悖论： 为了提高智能，需要更大的模型，从而消耗更多电力，导致电池更重，进而需要更强的电机来驱动，形成恶性循环。解决之道在于神经形态计算（降低计算能耗）和高能量密度固态电池的突破。

### 6.2 安全性标准：从隔离到共存

当机器人走出工厂围栏进入家庭，现有的安全标准（如 ISO 10218）已不再适用。

- ISO 13482 与 IEC 63310 的冲突： ISO 13482 是现行的个人护理机器人安全标准，侧重于风险评估和物理隔离。而 2025 年发布的 IEC 63310 标准则更侧重于智能家居环境下的功能性能和互联互通 48。
- 被动安全 vs. 主动安全： 传统的安全策略是“监测到人即停止”。但在家庭中，机器人需要与人频繁接触。未来的安全标准将转向功率和力限制 (PFL)，以及依赖神经形态皮肤实现的反射式安全——即在碰撞发生的毫秒级瞬间，机器人能像生物一样通过脊髓反射自动收缩，从而从物理层面消除伤害 32。

### 6.3 幻觉与物理现实 (Hallucinations per Watt-hour)

生成式 AI（VLA）固有的“幻觉”问题在物理世界中是不可接受的。ChatGPT 说错话可能只是一个尴尬的回答，但机器人产生“幻觉”动作（如将宠物的尾巴识别为绳子并拉扯）可能导致物理伤害。如何在边缘设备有限的算力（Watt-hour）下，抑制大模型的幻觉，保证物理操作的确定性，是当前研究的热点。量化技术（Quantization）虽然能降低能耗，但也增加了精度损失的风险 50。

---

## 7\. 未来趋势：生物融合与自主经济的黎明

### 7.1 生物混合机器人 (Bio-hybrid Robotics)：生命的工程化

PAI 的终极演进方向可能是超越硅基，走向碳基融合。

- 活体驱动与感知： 科学家正在探索利用活体组织构建机器人。例如，利用对光敏感的肌肉组织驱动的生物混合机器人，或者利用真菌（菌丝体）网络作为机器人的传感器和控制器。真菌能够感知光、热和化学信号，并产生电位脉冲驱动机器人运动，展示了惊人的环境适应力 51。
- 自愈系统： 受到生物自愈能力的启发，未来的 PAI 将具备自我修复功能。东京大学开发的附着活体皮肤的机器人脸已经展示了这种潜力，这种皮肤不仅逼真，还能在受损后自我愈合 52。

### 7.2 神经形态计算的全面普及

为了解决能源效率问题，PAI 将全面拥抱神经形态计算。随着 Intel Loihi 2、BrainChip Akida 等芯片在 2025 年的成熟，基于脉冲神经网络（SNN）的控制系统将成为主流。这将使得机器人在感知和控制层面上实现类似生物大脑的“稀疏计算”和“事件驱动”，从而将能耗降低数个数量级，为全天候续航奠定基础 35。

### 7.3 自主经济 (The Autonomous Economy) 的崛起

PAI 的成熟将催生全新的“自主经济”。

- 从工具到劳动力： 随着 Unitree G1 等机器人将硬件成本降至 1.6 万美元，机器人的 ROI（投资回报率）将发生质变。它们将不再昂贵的实验品，而是廉价的通用劳动力。
- 技能的通证化： 在自主经济中，机器人的物理技能（如“做回锅肉”、“修水管”）将像软件 APP 一样被封装、交易和下载。VLA 模型使得这种技能的跨机型迁移成为可能，从而形成一个庞大的物理技能应用商店 1。

---

## 8\. 结语

物理人工智能（Physical AI）正在重写人与机器、数字与物理的关系。通过将 AI 的认知能力注入由先进材料和仿生结构构成的躯体中，我们正在创造一种全新的物种。从形态计算的智慧身体，到 VLA 模型的通用大脑，再到神经形态皮肤的敏锐感知，PAI 正在系统性地破解莫拉维克悖论。

尽管能源、安全和伦理挑战依然严峻，但随着技术迭代的加速，PAI 必将走出实验室，成为工业 4.0 的基石，家庭生活的伴侣，乃至人类探索星辰大海的先驱。这不仅是技术的胜利，更是人类对“智能”本质理解的升华——智能，终将具身于形，作用于物。

### 引用的著作

1. Physical AI: Building the Next Foundation in Autonomous Intelligence - AWS, 访问时间为 一月 6, 2026， [aws.amazon.com/blogs/sp](https://link.zhihu.com/?target=https%3A//aws.amazon.com/blogs/spatial/physical-ai-building-the-next-foundation-in-autonomous-intelligence/)
2. XPENG Shares Achievements in Physical AI Emergence: Unveils XPENG VLA 2.0, Robotaxi, Next-Gen IRON, and Flying Car, 访问时间为 一月 6, 2026， [xpeng.com/news/019a56f5](https://link.zhihu.com/?target=https%3A//www.xpeng.com/news/019a56f54fe99a2a0a8d8a0282e402b7)
3. Sustainability Robotics - Physical AI - Empa, 访问时间为 一月 6, 2026， [empa.ch/web/s799/pai](https://link.zhihu.com/?target=https%3A//www.empa.ch/web/s799/pai)
4. Physical Artificial Intelligence for Powering the Next Revolution in Robotics, 访问时间为 一月 6, 2026， [asmedigitalcollection.asme.org](https://link.zhihu.com/?target=https%3A//asmedigitalcollection.asme.org/computingengineering/article/25/12/120809/1225298/Physical-Artificial-Intelligence-for-Powering-the)
5. Physical AI explained: Everything you need to know - XenonStack, 访问时间为 一月 6, 2026， [xenonstack.com/blog/phy](https://link.zhihu.com/?target=https%3A//www.xenonstack.com/blog/physical-ai)
6. Moravec's paradox - Wikipedia, 访问时间为 一月 6, 2026， [en.wikipedia.org/wiki/M](https://link.zhihu.com/?target=https%3A//en.wikipedia.org/wiki/Moravec%2527s_paradox)
7. What is physical AI -- and how is it changing manufacturing? - The World Economic Forum, 访问时间为 一月 6, 2026， [weforum.org/stories/202](https://link.zhihu.com/?target=https%3A//www.weforum.org/stories/2025/09/what-is-physical-ai-changing-manufacturing/)
8. When Did AI Agents Become A Thing? The History & Evolution Of Agentic AI - Mindset AI, 访问时间为 一月 6, 2026， [mindset.ai/blogs/how-ha](https://link.zhihu.com/?target=https%3A//www.mindset.ai/blogs/how-have-ai-agents-evolved-over-time)
9. VLA Models: Vision-Language-Action for Robotics (2025) | RoboCloud Hub, 访问时间为 一月 6, 2026， [robocloud-dashboard.vercel.app](https://link.zhihu.com/?target=https%3A//robocloud-dashboard.vercel.app/learn/blog/vla-models-robotics-2025)
10. NVIDIA Releases New Physical AI Models as Global Partners Unveil Next-Generation Robots, 访问时间为 一月 6, 2026， [nvidianews.nvidia.com/n](https://link.zhihu.com/?target=https%3A//nvidianews.nvidia.com/news/nvidia-releases-new-physical-ai-models-as-global-partners-unveil-next-generation-robots)
11. Morphological computation | Robotics and Bioinspired Systems Class Notes - Fiveable, 访问时间为 一月 6, 2026， [fiveable.me/robotics-bi](https://link.zhihu.com/?target=https%3A//fiveable.me/robotics-bioinspired-systems/unit-8/morphological-computation/study-guide/Dav1bpfnVqZ34T5P)
12. Morphological Computation in Robots with MHTECHIN: Unlocking the Power of Body-Environment Interaction, 访问时间为 一月 6, 2026， [mhtechin.com/support/mo](https://link.zhihu.com/?target=https%3A//www.mhtechin.com/support/morphological-computation-in-robots-with-mhtechin-unlocking-the-power-of-body-environment-interaction/)
13. Soft Robotics: Engineering Flexible Automation for Complex Environments - MDPI, 访问时间为 一月 6, 2026， [mdpi.com/2673-4591/92/1](https://link.zhihu.com/?target=https%3A//www.mdpi.com/2673-4591/92/1/65)
14. Soft Robotics vs. Hard Robotics – Comparative Insights and Analysis - SoftGripping, 访问时间为 一月 6, 2026， [soft-gripping.com/disco](https://link.zhihu.com/?target=https%3A//soft-gripping.com/discover/soft-robotics-vs-hard-robotics/)
15. Artificial muscle flexes in multiple directions, offering a path to soft, wiggly robots | MIT News, 访问时间为 一月 6, 2026， [news.mit.edu/2025/artif](https://link.zhihu.com/?target=https%3A//news.mit.edu/2025/artificial-muscle-flexes-multiple-directions-offering-path-soft-wiggly-robots-0317)
16. Vision Language Action Models in Robotic Manipulation: A Systematic Review - arXiv, 访问时间为 一月 6, 2026， [arxiv.org/html/2507.106](https://link.zhihu.com/?target=https%3A//arxiv.org/html/2507.10672v1)
17. NVIDIA Isaac GR00T N1.6 - A Foundation Model for Generalist Robots. - GitHub, 访问时间为 一月 6, 2026， [github.com/NVIDIA/Isaac](https://link.zhihu.com/?target=https%3A//github.com/NVIDIA/Isaac-GR00T)
18. DrEureka: Revolutionizing Robot Training with LLMs | by Elmo | Antaeus AR | Medium, 访问时间为 一月 6, 2026， [medium.com/antaeus-ar/d](https://link.zhihu.com/?target=https%3A//medium.com/antaeus-ar/dreureka-revolutionizing-robot-training-with-llms-331f2742c725)
19. \[Literature Review\] DrEureka: Language Model Guided Sim-To-Real Transfer, 访问时间为 一月 6, 2026， [themoonlight.io/en/revi](https://link.zhihu.com/?target=https%3A//www.themoonlight.io/en/review/dreureka-language-model-guided-sim-to-real-transfer)
20. Language Model Guided Sim-To-Real Transfer - DrEureka, 访问时间为 一月 6, 2026， [eureka-research.github.io](https://link.zhihu.com/?target=https%3A//eureka-research.github.io/dr-eureka/)
21. Building a Synthetic Motion Generation Pipeline for Humanoid Robot Learning | NVIDIA Technical Blog, 访问时间为 一月 6, 2026， [developer.nvidia.com/bl](https://link.zhihu.com/?target=https%3A//developer.nvidia.com/blog/building-a-synthetic-motion-generation-pipeline-for-humanoid-robot-learning/)
22. Elon Musk's Optimus Gen 3: A Technical Breakdown of the 2025 AI Revolution - Capitaly.vc, 访问时间为 一月 6, 2026， [capitaly.vc/blog/elon-m](https://link.zhihu.com/?target=https%3A//www.capitaly.vc/blog/elon-musks-optimus-gen-3-a-technical-breakdown-of-the-2025-ai-revolution)
23. Unitree G1 - Roboworks, 访问时间为 一月 6, 2026， [roboworks.net/store/p/u](https://link.zhihu.com/?target=https%3A//www.roboworks.net/store/p/unitree-g1-humanoid-robot)
24. Sanctuary AI Achieves In-hand Manipulation - YouTube, 访问时间为 一月 6, 2026， [youtube.com/watch?](https://link.zhihu.com/?target=https%3A//www.youtube.com/watch%3Fv%3DO73vVHbSX1s)
25. Sanctuary AI Demonstrates In-Hand Manipulation Capabilities for Improved General Purpose Robot Dexterity, 访问时间为 一月 6, 2026， [sanctuary.ai/blog/sanct](https://link.zhihu.com/?target=https%3A//www.sanctuary.ai/blog/sanctuary-ai-demonstrates-in-hand-manipulation-capabilities-for-improved-general-purpose-robot-dexterity)
26. HASEL Actuators Activated with a Multi-Channel Low-Cost High Voltage Power Supply, 访问时间为 一月 6, 2026， [mdpi.com/2076-0825/14/1](https://link.zhihu.com/?target=https%3A//www.mdpi.com/2076-0825/14/12/601)
27. HASEL Actuators Activated with a Multi-Channel Low-Cost High Voltage Power Supply, 访问时间为 一月 6, 2026， [ResearchGate - Temporarily Unavailable](https://link.zhihu.com/?target=https%3A//www.researchgate.net/publication/398461161_HASEL_Actuators_Activated_with_a_Multi-Channel_Low-Cost_High_Voltage_Power_Supply)
28. Remarkable robotic hand can now manipulate the objects that it's holding - New Atlas, 访问时间为 一月 6, 2026， [newatlas.com/robotics/s](https://link.zhihu.com/?target=https%3A//newatlas.com/robotics/sanctuary-ai-in-hand-manipulation/)
29. This New Artificial Muscle Could Let Humanoid Robots Lift 4,000 Times Their Own Weight, 访问时间为 一月 6, 2026， [zmescience.com/science/](https://link.zhihu.com/?target=https%3A//www.zmescience.com/science/news-science/this-new-artificial-muscle-could-let-humanoid-robots-lift-4000-times-their-own-weight/)
30. China Unveils 'Electronic Skin' That Gives Robots Human-Like Reflexes - eWeek, 访问时间为 一月 6, 2026， [eweek.com/news/china-ro](https://link.zhihu.com/?target=https%3A//www.eweek.com/news/china-robots-electronic-skin-human-like-reflexes/)
31. China develops neuromorphic e-skin that lets humanoid robots sense pain and react, 访问时间为 一月 6, 2026， [oodaloop.com/briefs/tec](https://link.zhihu.com/?target=https%3A//oodaloop.com/briefs/technology/china-develops-neuromorphic-e-skin-that-lets-humanoid-robots-sense-pain-and-react/)
32. A neuromorphic robotic electronic skin with active pain and injury perception - PNAS, 访问时间为 一月 6, 2026， [Just a moment...](https://link.zhihu.com/?target=https%3A//www.pnas.org/doi/10.1073/pnas.2520922122)
33. Improved electronic skin gives robots the human touch | UCL News, 访问时间为 一月 6, 2026， [ucl.ac.uk/news/2025/jun](https://link.zhihu.com/?target=https%3A//www.ucl.ac.uk/news/2025/jun/improved-electronic-skin-gives-robots-human-touch)
34. Single-material electronic skin gives robots the human touch - University of Cambridge, 访问时间为 一月 6, 2026， [cam.ac.uk/stories/robot](https://link.zhihu.com/?target=https%3A//www.cam.ac.uk/stories/robotic-skin)
35. Neuromorphic Computing Market Share, Size & Growth 2025-2035 - Metatech Insights, 访问时间为 一月 6, 2026， [metatechinsights.com/in](https://link.zhihu.com/?target=https%3A//www.metatechinsights.com/industry-insights/neuromorphic-computing-market-3255)
36. Top Neuromorphic Chips in 2025: BrainChip Akida, Intel Loihi & IBM TrueNorth - ElProCus, 访问时间为 一月 6, 2026， [elprocus.com/top-neurom](https://link.zhihu.com/?target=https%3A//www.elprocus.com/top-neuromorphic-chips-in-2025/)
37. Accelerate AI Inference for Edge and Robotics with NVIDIA Jetson T4000 and NVIDIA JetPack 7.1, 访问时间为 一月 6, 2026， [developer.nvidia.com/bl](https://link.zhihu.com/?target=https%3A//developer.nvidia.com/blog/accelerate-ai-inference-for-edge-and-robotics-with-nvidia-jetson-t4000-and-nvidia-jetpack-7-1/)
38. Lite VLA: Efficient Vision-Language-Action Control on CPU-Bound Edge Robots - arXiv, 访问时间为 一月 6, 2026， [arxiv.org/html/2511.056](https://link.zhihu.com/?target=https%3A//arxiv.org/html/2511.05642v1)
39. Elon Musk teases Tesla Optimus Gen 3 capabilities: 'So many improvements' - Teslarati, 访问时间为 一月 6, 2026， [teslarati.com/elon-musk](https://link.zhihu.com/?target=https%3A//www.teslarati.com/elon-musk-teases-tesla-optimus-gen-3-capabilities-so-many-improvements/)
40. A Complete Review Of Tesla's Optimus Robot - Brian D. Colwell, 访问时间为 一月 6, 2026， [briandcolwell.com/a-com](https://link.zhihu.com/?target=https%3A//briandcolwell.com/a-complete-review-of-teslas-optimus-robot/)
41. Figure 02 - Humanoid robot guide, 访问时间为 一月 6, 2026， [humanoid.guide/product/](https://link.zhihu.com/?target=https%3A//humanoid.guide/product/figure-02/)
42. Figure 02 humanoid robot is ready to get to work - The Robot Report, 访问时间为 一月 6, 2026， [therobotreport.com/figu](https://link.zhihu.com/?target=https%3A//www.therobotreport.com/figure-02-humanoid-robot-is-ready-to-get-to-work/)
43. Figure unveils Figure 02, its second-generation humanoid, setting new standards in AI and robotics - PR Newswire, 访问时间为 一月 6, 2026， [Figure unveils Figure 02, its second-generation humanoid, setting new standards in AI and robotics](https://link.zhihu.com/?target=https%3A//www.prnewswire.com/news-releases/figure-unveils-figure-02-its-second-generation-humanoid-setting-new-standards-in-ai-and-robotics-302214889.html)
44. NEO Home Robot | Order Today - 1X.tech, 访问时间为 一月 6, 2026， [1x.tech/discover/neo-ho](https://link.zhihu.com/?target=https%3A//www.1x.tech/discover/neo-home-robot)
45. 1X built its latest humanoid NEO Gamma to better fit into the home - The Robot Report, 访问时间为 一月 6, 2026， [therobotreport.com/1x-b](https://link.zhihu.com/?target=https%3A//www.therobotreport.com/1x-built-humanoid-neo-gamma-better-fit-home/)
46. Green Robotics: Energy Consumption & Sustainability Stats - PatentPC, 访问时间为 一月 6, 2026， [patentpc.com/blog/green](https://link.zhihu.com/?target=https%3A//patentpc.com/blog/green-robotics-energy-consumption-sustainability-stats)
47. The Energy Diet of Humanoid Robots - Mobius Market Research, 访问时间为 一月 6, 2026， [research.mobiusriskgroup.com](https://link.zhihu.com/?target=https%3A//research.mobiusriskgroup.com/p/the-energy-diet-of-humanoid-robots)
48. IEC 63310 vs Western Standards: The New Frontier in Personal Care Robotics - Saphira AI, 访问时间为 一月 6, 2026， [saphira.ai/blog/iec-633](https://link.zhihu.com/?target=https%3A//www.saphira.ai/blog/iec-63310-vs-western-standards)
49. What Is ANSI/A3 R15.06-2025 / ANSI/A3 R15.06-3-2025? - The ANSI Blog, 访问时间为 一月 6, 2026， [blog.ansi.org/ansi/ansi](https://link.zhihu.com/?target=https%3A//blog.ansi.org/ansi/ansi-a3-r15-06-2025-robot-safety/)
50. Generative AI at the Edge: Challenges and Opportunities - ACM Queue, 访问时间为 一月 6, 2026， [queue.acm.org/detail.cf](https://link.zhihu.com/?target=https%3A//queue.acm.org/detail.cfm%3Fid%3D3733702)
51. Robots are gaining new capabilities thanks to plants and fungi - Science News, 访问时间为 一月 6, 2026， [sciencenews.org/article](https://link.zhihu.com/?target=https%3A//www.sciencenews.org/article/plant-fungi-robots-pop-culture-scifi)
52. Biohybrid Robots Break New Ground: Where Biology Meets Robotics | RoboticsTomorrow, 访问时间为 一月 6, 2026， [roboticstomorrow.com/ne](https://link.zhihu.com/?target=https%3A//www.roboticstomorrow.com/news/2025/04/28/biohybrid-robots-break-new-ground-where-biology-meets-robotics/24649/)

编辑于 2026-01-07 20:10・北京