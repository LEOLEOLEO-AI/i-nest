---
title: "Hot Chips 2026 深度解读：AI芯片从通用加速走向专用拆解"
tags:
  - chip
  - design
  - network
  - semiconductor
  - hardware
  - architecture
date: 2026-09-04 21:00
source: GetNotes
score: 29
---

## Original Note

---
note_id: 1920393473485895904
title: "Hot Chips 2026 深度解读：AI芯片从通用加速走向专用拆解"
type: link
created: 2026-09-04 15:09:54
source: getnote
kb: 
---

# Hot Chips 2026 深度解读：AI芯片从通用加速走向专用拆解

### 🏆 本届大会的核心背景是什么？

**内存成本已占AI机架70%**，成为全场设计的**核心约束**。
- **时间地点**：2026年8月23-25日，斯坦福大学。
- **发布来源**：Jason's Chips，2026年9月2日。
- **覆盖领域**：内存、CPU、GPU、网络、定制加速器。
---
### 💾 内存技术有哪六条路线在竞争？

**计算必须走向数据**，全行业已独立收敛到同一方向。

| 路线 | 代表厂商/方案 | 核心亮点 |
| :--- | :--- | :--- |
| HBM基座集成逻辑 | 三星 | 基座变计算单元，zHBM降70%功耗 |
| HBM封装演进 | SK海力士 | 终点都是混合键合，工艺优势不持久 |
| 3D DRAM | d-Matrix Raptor | 100 TB/s带宽 = HBM4的5倍 |
| 高带宽闪存HBF | OXMIQ/PRAXMATI | 容量是HBM的8-16倍，带宽差25倍 |
| 存内计算PIM | 三星LPDDR5X-PIM | 内部带宽 = 外部接口的8倍 |
| 近内存计算 | XCENA MX1 | CXL设备+3072 RISC-V核，吞吐提3.35x |
- **HBM本质**：靠**2048条I/O线**（DDR5仅64条）的并行度堆带宽，代价是3倍硅片面积 + 散热难。
- **HBF适用**：低batch小规模部署、MoE专家并行。
- **量产节奏**：所有方案都需**2-4年**，近期内存紧张无法缓解。
  说白了，搬数据比算数据更费钱，所以把计算器搬到数据旁边，已经是全行业共识。
---
### 🖥️ Agent时代CPU路线分歧有多大？

**十年来最大分歧**，没人知道Agent瓶颈到底在哪。
- **NVIDIA Vera**：88核Arm，**空间多线程**，主打极致单线程延迟。
- **Intel Diamond Rapids**：256核 + 1.28GB LLC，主打极致并发吞吐。
- **Arm AGI**：136核Neoverse V3，TSMC N3P，**300W标准化功率包络**，Meta是首个客户。
- **Fujitsu MONAKA**：144核Arm，<30%硅片用2nm，超低电压功耗减半。
- **核心变化**：服务器CPU十年趋同的格局，被Agent工作负载彻底打破。
---
### 🎮 GPU机架竞争格局怎么变了？

**机架取代芯片成为产品单位**，吞吐量-交互性曲线是新记分牌。
- **NVIDIA Rubin NVL72**：
  - 低交互侧 2x 吞吐/MW，高交互侧 **30x**（DeepSeek Agent基准）。
  - 平台化组合 = Rubin + Groq LPX + Vera + BlueField-4 + Spectrum-X。
  - 自适应稀疏 = NVFP4 + 稀疏注意力，软件优化嵌入硬件。
- **AMD Helios（MI455X）**：
  - 31TB HBM4 > NVIDIA 21TB，43 TB/s scale-out > 28.8。
  - 差距：NVLink专有协议 vs UALink通用以太网，尾延迟未公布。
- **Intel Crescent Island**：
  - 反常规：无HBM、风冷、PCIe scale-up、480GB LPDDR5X。
  - 专为prefill设计，与SRAM-based decode搭配做拆解式推理。
- **格局**：NVIDIA包揽整条曲线，AMD攻中段，Intel独占prefill角落。
---
### 🌐 网络技术出现了哪四层分化？

**组件密度上升，但每端口内容在缩减**。
- **新维度**：scale-up（机架内）、scale-out（机架间）、scale-across（数据中心间）、scale-in（GPU与服务间）。
- **Broadcom Thor Ultra**：800G NIC，UEC标准化修复三大问题。
- **NVIDIA BlueField-4**：Grace CPU + ConnectX-9，7.2 Tb/s per tray，**5级KV cache层级**。
- **Spectrum-X多平面**：每GPU 8个薄端口连8个独立平面，扩展到512K GPU，单故障仅损1/8带宽。
- **受益方向**：光模块走量，switch和NIC芯片是直接受益者。
---
### ⚡ ASIC与推理初创收敛到什么方向？

**架构争论已结束**，竞争转向制造、软件和资本。
- **Cerebras CS-4**：3片WSE-3 Turbo，750 PFLOPS，**带宽是Rubin的6000倍**，容量是1/160。
- **SambaNova SN50**：Decode专用，MBU达44-51%（GPU仅5-25%）。
- **Google TPU v8**：训练/推理拆成两块芯片，8i用BoardFly拓扑，7跳 vs 旧16跳。
- **OpenAI Jalapeño**：
  - 9个月tapeout，极小团队，AI辅助设计。
  - 216GB HBM4 @ 15.4 TB/s，700W。
  - vs GB300：**1.7x tokens/kW**，延迟低3.6倍。
  - 首片到服务ChatGPT仅10周。
- **收敛方向**：大SRAM、低hop拓扑、decode specialization。
---
### 📌 大会四大核心结论是什么？

四条趋势共同指向AI芯片的范式转移。

#### 1) 内存溢价正在被侵蚀

HBM-class产品约**90%毛利率**（10倍加价），6条创新路线同时争夺租金。
- 近期内存紧张不变，但中期溢价空间会被压缩。

#### 2) 推理正在被拆解

Prefill（计算密集）和decode（带宽密集）拆分，各用专用硬件。
- Intel做prefill，SambaNova/Groq等做decode，NVIDIA在平台内产品化拆分。

#### 3) AI正在吞噬芯片设计

OpenAI Jalapeño的**设计方式**比芯片本身更重要：极小团队 + AI辅助 = 9个月tapeout。
- 设计人才壁垒被压缩，护城河剩下制造准入、软件生态、客户关系和fab。

#### 4) 领先制程只留给逻辑
- Fujitsu MONAKA：<30%硅片用2nm，SRAM和I/O留5nm。
- AMD MI455X：计算用N2，其余用N3P。
- 结论：先进晶圆需求增速远低于晶体管数量增速，**封装和键合工具链**结构性看涨。
---
### 📝 补充细节
- **内存结论的分量**：5种不同路线、来自5个不同角落，独立收敛到"计算走向数据"，说明方向已确定，资本将随之流动。
- **Arm AGI的特殊性**：这是Arm首次自己做芯片，而非只授权IP。
- **HBF的成本细节**：需要SLC而非TLC（3倍die per bit）+ HBM式堆叠，NAND消耗倍数达9x。

---
*getnote | 2026-09-04 21:00*


---

## Related Notes

[[iNEST-MOC]]
[[FPGA原型]]
[[SDI化合物键_四型架构]]
[[paper1_iNEST_core_architecture]]
