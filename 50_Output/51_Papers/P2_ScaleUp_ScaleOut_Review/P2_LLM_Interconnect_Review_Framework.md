# 大语言模型训练的Scale-Up与Scale-Out网络架构及晶圆级互连创新：综述框架

**目标期刊：** Nature Electronics / IEEE Proceedings / Engineering
**预计篇幅：** 8000-12000 词 + 8-12 张配图
**知识库素材基础：** 347 篇核心文档（3.5MB）
**状态：** 框架构建阶段（2026-07-07）

---

## 一、论文总纲

### 论文题目（候选）

1. **From Scale-Up to Wafer-Scale: A Comprehensive Review of Interconnect Architectures for Large Language Model Training**
2. **大语言模型训练的互连架构综述：从Scale-Up/Scale-Out到晶圆级集成**
3. **Beyond Bandwidth: Network Architecture Innovations for the LLM Era**

**推荐：** 候选 1（英文投稿 Nature Electronics）或候选 2（中文投稿 中国科学：信息科学）

---

### 核心论点

> LLM 训练的瓶颈已从计算（FLOPs）转移到通信（interconnect bandwidth & topology）。Scale-up（节点内高带宽互连）和 Scale-out（节点间大规模网络）构成了双层架构，而**晶圆级互连**正从晶圆级芯片向软件定义晶上系统（SDSoW）演进。本文系统综述这三种范式的技术路线、关键突破与融合趋势，提出以"拓扑中心计算"为统一框架的分类学体系。

---

## 二、章节大纲

### 第1章：引言 (1,200词)

**1.1 LLM 训练的 Scaling 挑战**
- GPT-4/Claude/DeepSeek 等模型的参数与数据规模增长趋势
- 计算 vs 通信的时间占比演变
- 数据移动能耗占比 ~90%（由 B0 论文结论支撑）

**1.2 互连架构的三种范式**
- Scale-Up：单节点/单机柜内 GPU-to-GPU 高带宽互连（NVLink, NVSwitch）
- Scale-Out：跨节点/跨机柜的数据中心网络（InfiniBand, RoCE, 胖树拓扑）
- Wafer-Scale：晶圆级/晶上系统内的超密互连（SoW, SDSoW, WSE）

**1.3 综述范围与方法论**
- 覆盖时间：2018-2026
- 统一评价框架：带宽密度 (Tbps/mm), 能效 (pJ/bit), 拓扑灵活性, 可扩展性

### 第2章：Scale-Up 互连 (1,500词)

**2.1 NVLink 技术代际演进**
- NVLink 1.0 → 5.0：带宽从 160GB/s 到 1.8TB/s
- NVSwitch 架构：从 6-GPU 到 72-GPU (NVL72) 全互连拓扑

**2.2 GB200 NVL72 的超节点互连方案**
- 5000 根 NVLink 铜缆，130TB/s 总带宽
- 机柜级设计（rack-scale liquid cooling + high-density interconnect）

**2.3 华为灵衢（UB-Mesh）超节点架构**
- UB-Mesh 设计理念：统一总线互连
- 与 NVLink 对比：拓扑灵活性 vs 带宽密度
- Hot Chips 2025 披露的技术细节

**2.4 Scale-Up 路线的局限与边界**
- 铜缆长度限制（~1m），光互连替代时机
- 超节点 vs 分布式训练的经济学

### 第3章：Scale-Out 网络 (1,500词)

**3.1 主流拓扑架构对比**
- Fat-Tree（胖树）：CLOS 三级架构
- Dragonfly/Dragonfly+：降低光缆成本
- Torus/3D-Torus：超算网络的启示

**3.2 InfiniBand vs RoCE**
- InfiniBand NDR (400Gbps) → XDR (800Gbps)
- RoCEv2 + 51.2T 交换机
- 实际部署数据：10万级 H100 集群分析

**3.3 集合通信优化**
- All-Reduce 的拓扑感知调度
- 网内归约 (In-Network Reduction/Sharp)

**3.4 Scale-Out 的瓶颈与未来**
- 跨机柜光缆延迟（us 级 vs 片内 ns 级）
- 并行策略对网络的不同需求

### 第4章：晶圆级互连 (2,000词)

**4.1 晶圆级计算的技术谱系**
- Cerebras WSE-1/2/3（2.6万亿晶体管）
- TSMC SoW / SoW-X（16 ASIC + 80 HBM4）
- Tesla Dojo D1 Chip + Training Tile

**4.2 晶圆级互连的技术挑战**
- 信号完整性、散热、供电
- 冗余设计与良率管理
- 3D 堆叠与混合键合（Hybrid Bonding）

**4.3 软件定义晶上系统（SDSoW）—— 中国方案**
- SDSoW 核心理念：软件定义互连 + 正交原语集 + 拓扑融合
- '十五五'战略布局（2026-2035）

**4.4 晶圆级光互连**
- 硅光子 interposer
- 光互连 vs 电互连的能效对比

### 第5章：Chiplet 间互连协议与标准 (1,200词)

**5.1 Chiplet 互连的协议生态**
- UCIe, BoW, NVLink-C2C, Infinity Fabric, EMIB

**5.2 基于 Chiplet 的异构集成**
- NoC-Chiplets：应用定义片上网络

**5.3 Chiplet 互连与 Scale-Up 的融合趋势**
- 从 Chiplet 到晶圆级：互连密度连续谱

### 第6章：拓扑中心计算 —— 统一框架与展望 (1,500词)

**6.1 范式转变**
- "以算为中心" → "以互连为中心"

**6.2 液态架构与软件定义互连（SDI）**
- SDI 三层模型

**6.3 互连架构的智能涌现视角（CST 框架）**

**6.4 未来路线图（2026-2040）**

### 第7章：结论 (500词)

---

## 三、材料基础（知识库现有素材 + 侧边栏链接）

### 核心参考文献列表（可点击打开）

以下链接格式为 `http://127.0.0.1:8900/` + 相对路径，在 Codex 侧边栏浏览器中可直接打开预览。

- [R01] NVIDIA Blackwell架构与NVLink互联深度解析
  → [50_Output/54_Code/TCC/进一步解读英伟达_Blackwell_架构、NVlink及GB200_超级芯片_深度学习_蓝海大脑GPU_InfoQ写作社区.md](http://127.0.0.1:8900/50_Output/54_Code/TCC/进一步解读英伟达_Blackwell_架构、NVlink及GB200_超级芯片_深度学习_蓝海大脑GPU_InfoQ写作社区.md)

- [R02] 英伟达GB200架构解析：互联架构和未来演进
  → [50_Output/54_Code/TCC/英伟达GB200架构解析1__互联架构和未来演进.md](http://127.0.0.1:8900/50_Output/54_Code/TCC/英伟达GB200架构解析1__互联架构和未来演进.md)

- [R03] GB200 NVL72全互联技术：铜缆方案或成为未来趋势
  → [30_TCC/32_Tech/英伟达GB200_NVL72全互联技术，铜缆方案或成为未来趋势？.md](http://127.0.0.1:8900/30_TCC/32_Tech/英伟达GB200_NVL72全互联技术，铜缆方案或成为未来趋势？.md)

- [R04] 华为灵衢(UB)技术与超节点架构详解
  → [30_TCC/32_Tech/华为灵衢(UB)技术与超节点架构详解.md](http://127.0.0.1:8900/30_TCC/32_Tech/华为灵衢(UB)技术与超节点架构详解.md)

- [R05] 华为UB-Mesh：革新大规模语言模型训练的数据中心网络架构
  → [50_Output/54_Code/TCC/UB-Mesh：革新大规模语言模型训练的数据中心网络架构.md](http://127.0.0.1:8900/50_Output/54_Code/TCC/UB-Mesh：革新大规模语言模型训练的数据中心网络架构.md)

- [R06] ODCC 2026超节点大会：AI基础设施Scale-up技术与未来趋势
  → [30_TCC/32_Tech/ODCC 2026超节点大会圆桌讨论：AI基础设施Scale-up技术与未来趋势.md](http://127.0.0.1:8900/30_TCC/32_Tech/ODCC%202026超节点大会圆桌讨论：AI基础设施Scale-up技术与未来趋势.md)

- [R07] 挑战Nvlink，华为推出互联技术，即将开源
  → [30_TCC/32_Tech/挑战Nvlink，华为推出互联技术，即将开源.md](http://127.0.0.1:8900/30_TCC/32_Tech/挑战Nvlink，华为推出互联技术，即将开源.md)

- [R08] 10万级H100集群：网络拓扑、InfiniBand与以太网对比分析
  → [30_TCC/32_Tech/10万级_H100_集群：能源、网络拓扑、以太网与_InfiniBand、可靠性、故障、检查点.md](http://127.0.0.1:8900/30_TCC/32_Tech/10万级_H100_集群：能源、网络拓扑、以太网与_InfiniBand、可靠性、故障、检查点.md)

- [R09] 超算网络中的主流拓扑架构
  → [30_TCC/32_Tech/超算网络中的主流拓扑架构.md](http://127.0.0.1:8900/30_TCC/32_Tech/超算网络中的主流拓扑架构.md)

- [R10] WSE SwarmX 网络架构优化方案
  → [30_TCC/32_Tech/WSE SwarmX 网络架构 优化方案.md](http://127.0.0.1:8900/30_TCC/32_Tech/WSE%20SwarmX%20网络架构%20优化方案.md)

- [R11] 晶圆级计算技术：从历史挑战到现代架构创新
  → [30_TCC/32_Tech/晶圆级计算技术：从历史挑战到现代架构创新.md](http://127.0.0.1:8900/30_TCC/32_Tech/晶圆级计算技术：从历史挑战到现代架构创新.md)

- [R12] 晶圆级芯片（WSC）技术深度分析：架构、集成与应用前景
  → [50_Output/54_Code/TCC/晶圆级芯片（WSC）技术深度分析：架构、集成与应用前景.md](http://127.0.0.1:8900/50_Output/54_Code/TCC/晶圆级芯片（WSC）技术深度分析：架构、集成与应用前景.md)

- [R13] 详解台积电「晶圆级系统」等技术革新
  → [30_TCC/32_Tech/详解台积电「晶圆级系统」等技术革新.md](http://127.0.0.1:8900/30_TCC/32_Tech/详解台积电「晶圆级系统」等技术革新.md)

- [R14] TSMC下一代晶圆级AI系统SoW-X：16颗ASIC+80颗HBM4+260Tb/s总片间带宽
  → [30_TCC/32_Tech/TSMC下一代晶圆级AI系统SoW-X：16颗_ASIC＋80颗HBM4＋260Tb_s总片间带宽.md](http://127.0.0.1:8900/30_TCC/32_Tech/TSMC下一代晶圆级AI系统SoW-X：16颗_ASIC＋80颗HBM4＋260Tb_s总片间带宽.md)

- [R15] Cerebras全球最大芯片WSE升级二代：一颗芯片等于一张晶圆
  → [30_TCC/32_Tech/Cerebras全球最大芯片WSE升级二代：一颗芯片等于一张晶圆.md](http://127.0.0.1:8900/30_TCC/32_Tech/Cerebras全球最大芯片WSE升级二代：一颗芯片等于一张晶圆.md)

- [R16] SDSoW+DeepSeek的'双子星'
  → [30_TCC/32_Tech/SDSoW+DeepSeek的'双子星'.md](http://127.0.0.1:8900/30_TCC/32_Tech/SDSoW+DeepSeek的'双子星'.md)

- [R17] 软件定义晶上系统（SDSoW）未来十年（2026-2035）发展战略规划
  → [30_TCC/32_Tech/软件定义晶上系统（SDSoW）未来十年（2026-2035）发展战略规划.md](http://127.0.0.1:8900/30_TCC/32_Tech/软件定义晶上系统（SDSoW）未来十年（2026-2035）发展战略规划.md)

- [R18] SDSoW'十五五'国家重大工程布局的建议
  → [30_TCC/32_Tech/SDSoW'十五五'国家重大工程布局的建议.md](http://127.0.0.1:8900/30_TCC/32_Tech/SDSoW'十五五'国家重大工程布局的建议.md)

- [R19] SDSoW：以系统级创新筑基，托举中国架构革命与生态突围
  → [50_Output/54_Code/TCC/SDSoW：以系统级创新筑基，托举中国架构革命与生态突围.md](http://127.0.0.1:8900/50_Output/54_Code/TCC/SDSoW：以系统级创新筑基，托举中国架构革命与生态突围.md)

- [R20] Chiplet互连协议思考
  → [30_TCC/32_Tech/Chiplet互连协议思考.md](http://127.0.0.1:8900/30_TCC/32_Tech/Chiplet互连协议思考.md)

- [R21] 基于Chiplet的集成架构综述：EDA视角
  → [50_Output/51_Papers/基于Chiplet的集成架构综述：EDA视角.md](http://127.0.0.1:8900/50_Output/51_Papers/基于Chiplet的集成架构综述：EDA视角.md)

- [R22] 美欧Chiplet技术发展深度研究
  → [30_TCC/32_Tech/美欧Chiplet技术发展深度研究：从战略布局到技术创新的全景分析.md](http://127.0.0.1:8900/30_TCC/32_Tech/美欧Chiplet技术发展深度研究：从战略布局到技术创新的全景分析.md)

- [R23] TCC-SDI：软件定义互连与拓扑中心计算范式
  → [50_Output/51_Papers/TCC_Software_Defined_Interconnect_拓扑中心计算范式.md](http://127.0.0.1:8900/50_Output/51_Papers/TCC_Software_Defined_Interconnect_拓扑中心计算范式.md)

- [R24] Complete Physical Topology Mapping for Collective Communication Primitives
  → [30_TCC/32_Tech/Complete Physical Topology Mapping for Collective Communication Primitives A CST-Optimal Framework for Network-Centric C.md](http://127.0.0.1:8900/30_TCC/32_Tech/Complete%20Physical%20Topology%20Mapping%20for%20Collective%20Communication%20Primitives%20A%20CST-Optimal%20Framework%20for%20Network-Centric%20C.md)

- [R25] 基于正交原语集与拓扑融合变换的网络复杂度计算方法及系统
  → [30_TCC/32_Tech/一种基于正交原语集与拓扑融合变换的网络复杂度计算方法及系统.md](http://127.0.0.1:8900/30_TCC/32_Tech/一种基于正交原语集与拓扑融合变换的网络复杂度计算方法及系统.md)

- [R26] 拓扑中心计算最小可行产品方案（海河实验室）
  → [30_TCC/32_Tech/海河实验室：拓扑中心计算最小可行产品方案.md](http://127.0.0.1:8900/30_TCC/32_Tech/海河实验室：拓扑中心计算最小可行产品方案.md)

- [R27] RISC-V 架构下 SDI 智算互联系统设计：面向 LLM 低延迟推理与训练
  → [30_TCC/32_Tech/RISC-V 架构下 SDI 智算互联系统设计：面向 LLM 低延迟推理与训练.md](http://127.0.0.1:8900/30_TCC/32_Tech/RISC-V%20架构下%20SDI%20智算互联系统设计：面向%20LLM%20低延迟推理与训练.md)

- [R28] B0 Engineering综述：从冯诺依曼到网络中心计算范式迁移
  → [50_Output/51_Papers/B0_ARS评审与终稿/B0_Engineering_v7_FINAL.md](http://127.0.0.1:8900/50_Output/51_Papers/B0_ARS评审与终稿/B0_Engineering_v7_FINAL.md)

- [R29] CST Intelligence Emergence Paper (V22 Engineering Format)
  → [50_Output/51_Papers/CST_Intelligence_Emergence_Paper_V22_Engineering_Format.md](http://127.0.0.1:8900/50_Output/51_Papers/CST_Intelligence_Emergence_Paper_V22_Engineering_Format.md)

- [R30] SDSoW Hardware Mapping
  → [30_TCC/35_Simulation/SDSoW_Hardware_Mapping.md](http://127.0.0.1:8900/30_TCC/35_Simulation/SDSoW_Hardware_Mapping.md)

---

## 四、撰写思路与推进路线

### Phase 1：材料消化与分类（1周）
- 按上述章节映射，逐篇阅读核心材料
- 提取关键技术参数表（带宽、延迟、功耗、规模、年份）
- 构建产品/技术对比矩阵

### Phase 2：关键数据采集与制图（1-2周）

**必备配图：**

| 编号 | 配图 | 数据来源 |
|------|------|----------|
| Fig.1 | Scale-Up/Scale-Out/Wafer-Scale 三种范式定位 | 第2-4章素材综合 |
| Fig.2 | NVLink 代际演进带宽增长曲线 | NVIDIA技术白皮书 |
| Fig.3 | GB200 NVL72 机柜级互连拓扑示意图 | GB200架构解析文档 |
| Fig.4 | InfiniBand vs RoCE 性能对比 | 10万级H100集群文档 |
| Fig.5 | TSMC SoW / Cerebras WSE / SDSoW 三方案对比 | 第4章素材 |
| Fig.6 | 从Chiplet到晶圆级：互连密度连续谱 | 第5+4章素材 |
| Fig.7 | SDI 三层架构：物理/协议/调度层 | TCC-SDI文档 |
| Fig.8 | 互连能效与智能涌现（CST）关系 | CST仿真数据 |

### Phase 3：初稿撰写（2-3周）
- 按 1-7 章顺序撰写
- 每章完成即跑 ARS 审查
- 并行收集/补充参考文献（Zotero管理）

### Phase 4：修订与投稿（1周）
- 全文章节互审 + 交叉引用检查
- 配图终版 + 图注校对
- Cover Letter + Highlights + 推荐审稿人

---

## 五、当前知识库缺口

| 缺口 | 重要度 | 获取途径 |
|------|--------|----------|
| NVLink 6.0 (Rubin) 最新参数 | 高 | NVIDIA GTC 2026 Keynote |
| Google TPU ICI 互连最新架构 | 高 | Google公开论文 |
| AMD Infinity Fabric 最新参数 | 中 | AMD技术白皮书 |
| 光互连部署数据 | 中 | OFC 2026会议论文 |
| Cerebras Condor Galaxy集群真实数据 | 中 | Cerebras客户案例 |
| 国内超节点最新进展 | 高 | 行业会议/论文 |

---

> **撰写负责人：** 刘勤让 (qinrangliu@fudan.edu.cn)
> **素材基础：** 347篇知识库文档
> **目标投稿：** 2026年9月前
> **协同关系：** 与B0(Engineering综述)、P1(TCC-SDI论文)、CST理论论文构成TCC研究体系
