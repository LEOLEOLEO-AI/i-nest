---
provenance: external
---

---
title: "Jim Keller与Tenstorrent的开源AI处理器战略：RISC-V架构与开放芯片生态"
date: 2025-09-14 03:06:34
source: "????"
note_id: 1887413063863406368
note_type: link
tags: [AI链接笔记, Jim Keller, RISC-V AI处理器, 开放芯片架构]
source: getnote---

# Jim Keller与Tenstorrent的开源AI处理器战略：RISC-V架构与开放芯片生态

### 🔹 核心人物与使命
- **Jim Keller**：芯片行业传奇人物，曾任职英特尔、AMD、特斯拉硬件部门高管，现领导Tenstorrent推动开源AI处理器创新
- **使命**：解决AI硬件"昂贵且封闭"的痛点，通过开源架构和模块化设计，让高性能AI计算更普及、可扩展

### 🔹 Open AI Tensix处理器技术解析

![Open AI Tensix处理器架构图](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd4dff0fc7a6de158ad27607ce31a3c1b?Expires=1785911748&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=8NCvo0QSZAcUcWkB%2Bls1WnWwwLY%3D&x-oss-process=image%2Fresize%2Cm_lfit%2Cw_720%2Ch_3240)
- **核心参数**：
  - 5个RISC-V CPU核心
  - 24 BFloat16 TFLOPS算力
  - 1.4TB/s SRAM带宽 + 1.4TB/s NOC带宽
- **开源特性**：
  - 开放Tenstorrent ISA规范
  - 提供高级模拟器与全套开源软件栈
  - 支持普通DRAM与以太网构建AI集群

### 🔹 Black Hole芯片与硬件产品矩阵
- **Black Hole芯片**（台积电6nm制程）：
  - 含140个张量处理器和RISC-V核心
  - 成本约8000万美元，支持GDDR6 DRAM
  - 采用多芯片组合方案：8芯片/板 × 4板/盒 = 32芯片/节点，提供1TB DRAM与16TB总带宽
- **已出货产品**：
  - Galaxy box服务器（可扩展AI训练集群）
  - 水冷quiet box（低噪音版本）
  - PCI Express加速卡
  - Eson TPU IP授权（已应用于LG电视芯片）

### 🔹 开放芯片生态战略
- **小芯片架构**：
  - 模块化设计CPU/内存控制器/AI计算单元
  - 兼容UCIe互连标准，支持独立迭代与组合
  - 推出"空芯片"（empty chip）方案，预集成基础IP，客户可快速植入自研模块
- **Open Chiplet Architecture计划**：
  - 开放互连协议/测试/加密等全套系统组件
  - 贡献IP至行业联盟，降低芯片设计门槛

### 🔹 AI训练集群方案

| 集群规模       | 组件构成                | 核心特性                  |
|----------------|-------------------------|---------------------------|
| 基础单元       | 9个Galaxy box           | 全冗余连接，单线缆故障不影响运行 |
| 标准训练集群   | 多个基础单元互联        | 统一管理界面，支持数百节点扩展 |
| 最大配置       | 2000+ Black Hole芯片    | 百万级RISC-V核心协同计算   |


<!-- orphan-cleanup: linked to MOC -->
## 来源回链

- [[TCC_Master_Index]]
