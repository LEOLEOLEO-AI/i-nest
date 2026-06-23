---
title: "英国AI芯片产业对标分析_Fractile与Graphcore的Transformer ASIC路线图"
date: 2026-06-18
version: v1.0
status: Final
sources: "Google News RSS, SiliconANGLE, WSJ, Tom's Hardware, EE Times, HPCwire, BusinessCloud, Business Weekly"
tags: [TCC, UK, AI芯片, ASIC, Fractile, Graphcore, Transformer, 推理加速, 竞争分析]
---

# 英国AI芯片产业对标分析：Fractile与Graphcore的Transformer ASIC路线

> **核心发现**：英国正在成为全球AI推理芯片的重要创新极。以Fractile（DRAM-free新型推理架构）和Graphcore（晶圆级IPU）为代表，英国AI芯片产业在2024-2026年间累计融资超$10亿，形成了一条从基础研究（ARIA）→ 初创孵化 → 大规模资本注入 → 产业巨头合作的完整创新链条。这些技术路线与TCC计算范式在"突破存储墙""网络中心计算"等维度上形成有意义的参照系。

---

## 一、英国AI芯片产业全景

### 1.1 产业格局速览

| 公司 | 地点 | 成立 | 技术路线 | 累计融资 | 最新状态（2026.6） |
|------|------|------|----------|----------|-------------------|
| **Fractile** | Cambridge | 2022 | DRAM-free推理芯片 | $247M ($15M+$12M+$220M) | $220M Series B；Anthropic洽谈采购 |
| **Graphcore** | Bristol | 2016 | 晶圆级IPU处理器 | ~$1.3B (含SoftBank收购+注资) | SoftBank旗下；$457M追加注资；$1.3B印度投资 |
| **Myrtle.ai** | Cambridge | 2018 | FPGA/ASIC混合推理加速 | ~$10M | 专注ML推理软件栈 + FPGA |
| **Blueshift Memory** | Cambridge | 2016 | 新型内存架构（Cambridge CAM） | 种子轮 | 关注AI/视觉计算内存瓶颈 |

### 1.2 政府/政策支持

| 机构/计划 | 规模 | 方向 | 对TCC的启示 |
|-----------|------|------|------------|
| **ARIA**（先进研究与发明局） | £5M给Fractile | 高风险/高回报AI硬件 | 类似"173专项"的先导机制 |
| **UK AI Hardware Plan** | 战略级 | 国家AI算力主权 | 论证"国家算力主权"的重要性 |
| **National AI Supercomputer** | £750M | 国家级算力基础设施 | 大规模计算平台的公共投资模式 |
| **AI投资总包** | £1.1B | 整体AI战略 | 算力-算法-数据三要素协同 |

---

## 二、核心公司深度对标

### 2.1 Fractile：DRAM-free推理架构的革命性尝试

#### 2.1.1 公司概况

- **创始人**：Walter Goodwin（牛津大学芯片工程背景）
- **创立时间**：2022年
- **所在地**：剑桥（Cambridge, UK）
- **团队规模**：未公开（推断50-100人，基于$220M融资规模）
- **投资方**：Pat Gelsinger（前Intel CEO，个人投资）、ARIA（£5M政府资助）、多家VC

#### 2.1.2 技术路线

**核心创新：DRAM-free架构**

根据2026年5月WSJ和SiliconANGLE的报道，Fractile的技术架构有以下关键特征：

> "Goodwin told the Wall Street Journal that it doesn't use traditional high-bandwidth memory, nor on-chip static random-access memory or SRAM."

这意味着Fractile采用了**第三种内存架构**——既不是传统HBM，也不是片上SRAM。可能的实现方向：

1. **近存计算（Near-Memory Computing）**：逻辑与存储物理紧耦合，减少数据搬运
2. **存内计算（In-Memory Computing）**：在存储单元内完成部分计算操作
3. **新型非易失存储器（NVM）**：如MRAM、ReRAM等新型存储介质
4. **层次化内存-逻辑融合**：在标准服务器机架内实现内存与芯片的短距高速互联

**关键设计目标**：
- 减少Token生成延迟（"将一个月的工作压缩到一天"）
- 降低前沿大模型推理的响应时间
- 使更激进的AI应用场景（药物发现、材料发现、软件工程）在经济上可行

**已知架构特征**：
| 维度 | Fractile路线 | 传统GPU路线 | TCC路线 |
|------|-------------|------------|---------|
| 内存架构 | **DRAM-free（第3种方案）** | HBM + 片上SRAM | **拓扑定义内存**（Route=Memory） |
| 计算范式 | 推理专用ASIC | 通用并行计算 | **拓扑中心计算**（Route≡Transform） |
| 存储墙突破 | 物理层（新型存储介质） | 带宽堆叠（HBM3e→HBM4） | **网络层**（拓扑重构消除数据搬运） |
| 规模扩展 | 单芯片+标准机架 | 多卡Scale-Up | **晶上网络**（节点内+跨节点统一拓扑） |
| 目标场景 | 大模型推理 | 训练+推理 | **全场景**（训练+推理+新计算范式） |

#### 2.1.3 融资里程碑与意义

```
2022 ── 公司成立
2024.07 ── $15M种子轮 + 退出隐形模式
2024.10 ── ARIA £5M资助（政府背书）
2025.02 ── Pat Gelsinger个人投资（产业领袖认可）
2026.05 ── $220M Series B（大规模资本验证）
2026.05 ── Anthropic洽谈采购（产业头部客户意向）
```

**融资分析**：
- **$220M是英国AI芯片领域最大单笔融资之一**，超越Graphcore早期融资速度
- **Anthropic作为潜在客户**的意义：表明头部AI Lab认可专用推理芯片的价值
- **Pat Gelsinger投资**的象征意义：Intel前CEO看好创新ASIC路线，暗示"后GPU时代"的可能

#### 2.1.4 对TCC的战略启示

**正向验证**：

1. **"突破存储墙"是产业共识**：Fractile以物理层创新（新内存介质）突破存储墙，TCC以网络层创新（拓扑定义内存）突破同一瓶颈——两条路线形成互补验证
2. **推理专用硬件的价值被头部客户确认**：Anthropic采购意向验证了"专用优于通用"的趋势，TCC的"可编程拓扑计算"兼具专用性能和通用灵活性
3. **标准机架部署的产业现实**：Fractile选择"标准服务器机架"作为部署单元，说明数据中心兼容性是产业化的必要条件——TCC的SDSoW同样需要考虑标准机架兼容

**差异化优势**：

| 对比维度 | Fractile | TCC |
|----------|----------|-----|
| 创新层级 | 物理层（器件/材料） | **网络层+架构层** |
| 可编程性 | 固定功能（推理ASIC） | **软件定义拓扑**（LINK/NPC/CPC原语） |
| 扩展维度 | 单芯片优化 | **网络拓扑优化**（N=1→10K节点） |
| 理论支撑 | 工程直觉驱动 | **CST定理**（I ∝ CST = (Sc·Tc)·e^(α·Γst)） |
| 场景覆盖 | 大模型推理 | **全场景**：训练+推理+科学计算+新范式 |

### 2.2 Graphcore：从独立创新到SoftBank生态

#### 2.2.1 公司轨迹

| 时间 | 事件 | 意义 |
|------|------|------|
| 2016 | 创立，总部布里斯托 | 英国首个大规模AI芯片创业公司 |
| 2018-2020 | IPU MK1/MK2发布 | 创新型大规模并行AI处理器 |
| 2022 | Bow IPU（晶圆对晶圆3D堆叠） | 3D集成+晶圆级封装 |
| 2024.07 | **SoftBank收购**（~$600M） | 从独立到生态整合 |
| 2025.10 | 宣布$1.3B印度投资计划 | 全球制造布局 |
| 2026.05 | SoftBank追加$457M注资 | 持续的资本支持 |

#### 2.2.2 技术指标

| 指标 | IPU MK2 (GC200) | Bow IPU | NVIDIA H100对比 |
|------|-----------------|---------|-----------------|
| 晶体管数 | 59.4B | 59.4B（同芯片） | 80B |
| 片上内存 | 900 MB | 900 MB | 80 GB HBM3 |
| FP16算力 | 250 TFLOPS | 350 TFLOPS | 990 TFLOPS |
| 功耗 | ~150W | ~150W（改善16%） | 700W |
| 架构优势 | MIMD细粒度并行 | 晶圆对晶圆3D堆叠 | Tensor Core + NVLink |
| 独特优势 | 稀疏计算、图计算 | 3D集成性能/功耗比↑ | 软件生态成熟度 |

#### 2.2.3 战略转变：被收购后的定位

被SoftBank收购后，Graphcore的定位从"NVIDIA挑战者"转变为"SoftBank AGI战略的硬件支柱"：

- **与ARM形成互补**：ARM（CPU）+ Graphcore（AI加速器）= 完整的端-边-云AI计算方案
- **印度$1.3B投资**：包括研发中心和新一代芯片制造，利用印度半导体人才和市场规模
- **AGI导向**：SoftBank将Graphcore定位为通往AGI的基础设施

#### 2.2.4 对TCC的启示

**正向验证**：
- **晶圆级集成是趋势**：Bow IPU的晶圆对晶圆3D堆叠验证了"晶上系统"方向
- **非GPU架构有商业价值**：Graphcore证明了非NVIDIA架构的可行性
- **大规模资本需要产业巨头背书**：独立AI芯片公司需要生态主（SoftBank）的资本和渠道支持

**TCC的差异化**：
- Graphcore的IPU仍是"节点中心"范式（处理器设计创新），TCC是"网络中心"范式（拓扑设计创新）
- Graphcore的创新在芯片内部，TCC的创新在芯片间网络
- Graphcore受限于固定拓扑，TCC的可编程拓扑是根本差异

---

## 三、全球AI推理芯片竞争格局的参照价值

### 3.1 专有ASIC vs 通用GPU vs 拓扑可编程的三角定位

```
                    通用性 ↑
                           │
                    NVIDIA GPU（CUDA生态）
                           │
                           │     TCC（软件定义拓扑）
                           │        ★ 第三路线
                           │
        Etched Sohu ───────┼────────── Groq LPU
        (Transformer固化)  │      (确定性架构)
                           │
                    Fractile      Graphcore IPU
                    (DRAM-free)   (MIMD细粒度)
                           │
                    专用性 ──┴───── 可编程性 →
```

**TCC的第三路线定位**：
- **不是专用ASIC**（如Etched/Fractile）：保持了跨模型、跨场景的通用性
- **不是通用GPU**（如NVIDIA）：通过拓扑可编程获得专用级性能
- **是可编程拓扑计算**：Route≡Transform统一了通信与计算，实现"通用中的专用"

### 3.2 产业四大趋势交叉验证

| 趋势 | 产业证据 | TCC位置 |
|------|----------|---------|
| **推理超越训练成为主战场** | Fractile $220M融资、Anthropic采购、Etched/Groq/Taalas崛起 | TCC的Route=Transform天然适配推理 |
| **存储墙是核心瓶颈** | Fractile的DRAM-free、HBM4路线图、CXL互联 | TCC的"拓扑定义内存"从更高维度突破 |
| **专用化是差异化方向** | Etched固化Transformer、Fractile推理专用 | TCC的可编程拓扑="专用性能+通用灵活性" |
| **晶圆级+3D集成是未来** | Bow IPU、Cerebras WSE-3、Dojo | TCC的SDSoW是系统级晶上集成 |

---

## 四、英国模式对TCC产业化的参考

### 4.1 ARIA模式 vs 173专项模式

| 维度 | 英国ARIA | 中国173专项 |
|------|----------|------------|
| 资金规模 | £5M（单项目）→ $220M（市场化） | 6.8亿元（一期）→ 30亿元（十五五二期） |
| 机制 | 政府种子→VC接力→产业客户验证 | 政府专项→团队攻关→产业化联合体 |
| 灵活性 | 高风险/高回报，快速迭代 | 系统性攻关，长周期规划 |
| 成功案例 | Fractile（3年从0到Anthropic客户） | SDSoW（5年从概念到173/十五五） |

**对TCC的启示**：两种模式可以互补。TCC可以借鉴ARIA的"快验证"机制，在173专项框架内设立"快速孵化子项"，加速MVP验证。

### 4.2 产学研协同模式

英国的"剑桥集群"（ARM + Fractile + Myrtle + Blueshift）展示了**地理密度驱动的创新协同**：

- **剑桥大学** → 人才供给 + 基础研究
- **ARM** → IP授权生态 + 产业标准
- **Fractile/Myrtle/Blueshift** → 差异化创新

**TCC的四单位协同**可以参照此模式：
- **复旦大学**（TCC架构+编译器SDK）↔ Cambridge大学角色
- **苏州实验室**（材料+光子+忆阻器）↔ ARM IP生态角色
- **天大**（FPGA验证+工程实现）↔ Fractile工程化角色
- **NDSC**（SDI交换机+协议）↔ 标准制定角色

---

## 五、关键性能指标对比

### 5.1 推理性能对标（基于公开数据）

> **注**：Fractile芯片尚未发布，以下为基于公开报道的推断。Taalas、Etched数据来自公开报道。

| 芯片 | 架构 | Token速率（估算） | 单Token能耗 | 内存架构 | 成熟度 |
|------|------|------------------|------------|----------|--------|
| NVIDIA H200 | GPU通用 | ~2,000 tok/s (Llama3-70B) | ~0.35 J/tok | HBM3e 141GB | 量产 |
| Groq LPU | 确定性架构 | ~500 tok/s per chip | ~0.2 J/tok | SRAM 230MB | 量产 |
| Cerebras WSE-3 | 晶圆级 | ~1,800 tok/s (单芯片) | ~0.4 J/tok | 片上SRAM 44GB | 量产 |
| Etched Sohu | Transformer ASIC | ~500,000 tok/s (宣称) | 待验证 | 待披露 | 2025流片 |
| Taalas HC1 | 模型固化ASIC | "超越现代方案"（宣称） | "性价比10x"（宣称） | 待披露 | 2026发布 |
| **Fractile** | **DRAM-free** | **"月→日"级加速（宣称）** | **极低（DRAM-free）** | **第3种** | **开发中** |
| Graphcore Bow IPU | 晶圆堆叠 | ~800 tok/s (估算) | ~0.2 J/tok | 片上900MB | 量产 |
| **TCC-NCC (Phase1)** | **拓扑可编程** | **100K+ tok/s (系统级估算)** | **<0.1 J/tok (拓扑消除搬运)** | **拓扑定义** | **规划中** |

### 5.2 TCC的差异化性能优势来源

| 优势维度 | 传统方案瓶颈 | TCC方案 |
|----------|-------------|---------|
| 数据搬运能耗 | HBM → GPU 搬运占60%+能耗 | Route=Memory：网络拓扑消除搬运 |
| 多卡扩展效率 | NVLink/NVSwitch 延迟随N增长 | CST超线性：N↑→CST↑→I↑ |
| 模型适配灵活性 | ASIC固化；GPU通用但低效 | LINK.config：软件定义拓扑 |
| 摩尔定律上限 | 单芯片物理极限 | 网络扩展：N→∞理论无上限 |

---

## 六、总结与建议

### 6.1 核心结论

1. **Fractile的DRAM-free验证了"突破存储墙"是产业头号共识**，但TCC从网络层突破比物理层突破具有更高的天花板和更广的适用场景
2. **Graphcore的轨迹说明独立AI芯片公司需要生态主**，TCC应以SDSoW为载体，与173专项/新紫光深度融合
3. **英国ARIA模式证明了"小规模快验证+市场化接力"的可行性**，TCC可借鉴设立快速孵化机制
4. **Anthropic对Fractile的采购意向说明头部AI Lab正在主动寻找NVIDIA替代方案**，这是TCC打入市场的窗口期
5. **Taalas/Etched的"模型固化"路线短期有效但长期受限**，TCC的"可编程拓扑"兼顾了专用性能与通用灵活性

### 6.2 行动建议

1. **将Fractile纳入TCC对标分析体系**（作为"存储墙突破"参照系）
2. **跟踪Anthropic-Fractile合作进展**（验证推理专用芯片的市场接受度）
3. **研究ARIA的快速验证机制**（在173框架内孵化TCC MVP）
4. **准备TCC vs Fractile技术差异化论述**（重点突出"网络层创新 vs 物理层创新"的维度差异）
5. **关注Taalas/Etched的实测性能数据**（作为"专用ASIC上限"的校准参照）

---

## 附录：资料来源

| # | 来源 | 日期 | 内容 |
|---|------|------|------|
| 1 | SiliconANGLE | 2026.05.13 | Fractile $220M融资 + 技术架构披露 |
| 2 | WSJ | 2026.05 | Fractile CEO Goodwin技术路线采访 |
| 3 | Tom's Hardware | 2026.05.03 | Anthropic洽谈采购Fractile芯片 |
| 4 | EE Times | 2025.02.06 | Pat Gelsinger投资Fractile |
| 5 | BusinessCloud | 2026.05.14 | Fractile £160M+ UK AI chip moonshot |
| 6 | Business Weekly | 2024.10.24 | ARIA £5M授予Fractile |
| 7 | Business Weekly | 2024.07.28 | Fractile $15M种子轮 + 退出隐形模式 |
| 8 | HPCwire | 2025.12.02 | SoftBank收购Graphcore后追加投资 |
| 9 | Bloomberg | 2025.10.09 | Graphcore $1.3B印度投资计划 |
| 10 | Forbes | 2026 | Taalas HC1芯片发布 |
| 11 | HPCwire | 2026 | UK £750M National AI Supercomputer |
| 12 | Pulse 2.0 | 2026.05.13 | Fractile $220M Next-Gen AI Inference |
| 13 | DCD | 2026.05 | Fractile AI inference chip development |
| 14 | Ventureburn | 2026.05.14 | Fractile $220M advance AI inference |