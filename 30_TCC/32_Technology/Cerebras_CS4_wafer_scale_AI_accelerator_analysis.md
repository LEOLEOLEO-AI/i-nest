---
direction: both
category: 技术
tags: [chip, architecture, hardware, llm, infrastructure]
summary: "Cerebras CS-4晶圆级AI推理加速器，性能较上代提升6倍"
quality: high
processed: 2026-08-23 22:02
---
---
title: "Cerebras CS-4 深度解析：重塑AI推理极限的晶圆级性能怪兽"
tags:
  - chip
  - transformer
  - computing
  - llm
  - design
  - infrastructure
  - first-principles
  - semiconductor
  - physics
  - architecture
  - hardware
  - network
  - ai
date: 2026-08-23 21:00
source: GetNotes
score: 19
---

## Original Note

---
note_id: 1919287467866100712
title: "Cerebras CS-4 深度解析：重塑AI推理极限的晶圆级性能怪兽"
type: link
created: 2026-08-23 17:02:26
source: getnote
kb: 
---

# Cerebras CS-4 深度解析：重塑AI推理极限的晶圆级性能怪兽

### **🚀 CS-4 是什么级别的产品，核心定位是什么？**

CS-4 是**机架级AI加速器**，推理速度比顶级GPU快最高**30倍**。
- **发布方**：Cerebras Systems
- **定位**：面向超大规模数据中心与「Token工厂」的终极推理引擎
- **架构创新**：从底层计算、供电、散热到I/O通信全方位重构

### **🧠 单芯片和整机算力分别提升了多少？**

单芯片带宽翻倍，整机算力达上一代的**6倍**。

| 维度 | CS-3（WSE-3） | CS-4（WSE-3T） |
| :--- | :--- | :--- |
| 片上内存（SRAM） | 44GB | 44GB |
| 单芯片带宽 | 21PB/s | 43.2PB/s |
| 晶圆数量 | 1颗 | 3颗 |
| 系统总带宽 | 21PB/s | 129.6PB/s |
| AI峰值算力 | 125PFLOPs | 750PFLOPs |
- **核心频率**：从 1.4GHz 提升至 **2.8GHz**
- **实测性能**：GPT-OSS-120B 模型下，单用户生成速度超 **4,400 tokens/s**
- **能效提升**：每瓦吞吐量较上一代提升 **10倍**
  说白了，同样一度电，CS-4 能吐出的Token数量是上一代的10倍。

### **🎒 单芯片带宽翻倍靠什么技术实现？**

靠**0.5毫米极限供电**和**晶圆级背包架构**。
- **供电距离骤降**：传统GPU供电距离约50mm → CS-4 缩短至 **0.5mm**，几乎消除板级功率损耗
- **3D一体化封装**：电源转换、液冷、高速I/O、控制元件全部封装在晶圆后方
- **组件数量减少 50%**
- **部署效率提升**：集群部署时间从「数天」缩短至「几小时」

### **⚡ 三颗晶圆怎么连起来，延迟有多低？**

无交换机直连，晶圆间延迟仅**2微秒**。
- **单晶圆外部带宽**：2.4Tbps（翻倍）
- **整机I/O总带宽**：**7.2Tbps**
- **互联协议**：支持标准以太网 RoCE v2 RDMA
- **集群扩展能力**：可支持超 **50万亿参数** 的超大模型

### **🤝 CS-4 是单独用还是和其他芯片搭配？**

主打**异构分解推理**，专门做解码加速。
- **分工模式**：Prefill（上下文处理）由 AMD Instinct / AWS Trainium 等负责 → 低延迟网络移交 → CS-4 专攻 Token 生成
- **核心优势**：计算性价比极致平衡

### **📝 补充细节**
- 片上内存维持 44GB 不变，原因是受限于**单块晶圆最大物理面积**与 **5nm 工艺**
- 系统总带宽 129.6PB/s 是上一代的 **6.1倍**
- 「晶圆直连」无需额外网络交换机，是降低延迟的关键

---
*getnote | 2026-08-23 21:00*


---

## Related Notes

[[FPGA原型]]
[[iNEST-MOC]]
[[paper2_liquid_computing_chemistry]]
[[SDI化合物键_四型架构]]
[[paper1_iNEST_core_architecture]]
