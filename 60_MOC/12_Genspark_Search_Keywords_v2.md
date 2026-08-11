---
title: "Genspark 检索关键词更新指令 v2"
date: 2026-08-11
tags: [genspark, keyword, tcc, inest, pipeline]
status: pending-confirm
---

# Genspark 检索关键词更新指令 v2

> 此文档用于同步更新 Genspark 侧的文献检索配置。请将以下指令发给 Genspark（clawcomputer）。

---

## 指令内容（可直接粘贴给 Genspark）

请更新你的每日文献检索关键词配置，严格执行以下规则：

### 1. TCC 方向（拓扑中心计算）
- **必须使用**：topological center computing / topology-centric computing / topological computing / topology-based computing / topology as a computing primitive
- **叠加工程语境**：network-on-chip (NoC) / chiplet / wafer-scale integration / interconnect / routing / reconfigurable network
- **严禁使用**：trusted / trust / security / tee / sgx / confidential / 可信计算 等任何安全、可信计算方向关键词
- 注意：TCC = Topological Center Computing，**不是** Trusted Computing Cloud

### 2. iNEST 方向（复杂网络涌现智能）
- **只检索**：complex network emergence / emergent intelligence / collective intelligence / criticality / self-organized criticality / higher-order interaction / simplicial complex / phase transition / bifurcation / edge of chaos / reservoir computing / spiking neural network / neuromorphic / integrated information / causal emergence

### 3. 硬性排除词（命中即丢弃，不写入知识库）
security, attack, threat, intrusion, malware, ransomware, false data injection, networked control, adversarial, trusted, trust, tee, sgx, confidential, blockchain, differential privacy, federated learning, privacy, cyber, cryptography, authentication, anomaly detection, intrusion detection, denial of service

### 4. 判定要求
- 对每篇候选论文：标题/摘要中出现任一排除词 → 直接丢弃
- 单词匹配用完整词（如 interconnect 不匹配 interconnected）
- 只输出与 TCC 拓扑中心计算或 iNEST 复杂网络涌现智能明确相关的论文

---
*2026-08-11 由 Codex 生成，等待用户确认后发给 Genspark*
