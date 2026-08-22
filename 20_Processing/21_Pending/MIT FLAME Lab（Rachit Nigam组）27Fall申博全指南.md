---
title: "MIT FLAME Lab（Rachit Nigam组）27Fall申博全指南"
tags:
  - fpga
  - transformer
  - llm
  - chip
  - semiconductor
  - computing
  - hardware
  - ai
  - infrastructure
date: 2026-08-15 21:00
source: GetNotes
score: 13
---

## Original Note

---
note_id: 1918522023089461424
title: "MIT FLAME Lab（Rachit Nigam组）27Fall申博全指南"
type: link
created: 2026-08-15 11:01:10
source: getnote
kb: 
---

# MIT FLAME Lab（Rachit Nigam组）27Fall申博全指南

### 👤 这位导师是谁，背景有多硬？

Rachit Nigam是**MIT EECS新聘助理教授**，2026年1月刚入职。
- **现任职务**：MIT EECS助理教授 + Douglas Ross Career Development Professor + MIT CSAIL成员 + FLAME Lab负责人。
- **教育经历**：UMass Amherst 计算机本科 → Cornell University CS博士。
- **业界经历**：Jane Street 低延迟团队 + Facebook Reality Labs 芯片设计。
- **博士奖项**：
  - 2025年 **SIGPLAN John C. Reynolds Doctoral Dissertation Award**
  - 2026年 ACM Doctoral Dissertation Award Honorable Mention
  - 2026年 Cornell CS Outstanding Dissertation Award

### 🔬 这个组到底在研究什么？

用**编程语言+编译器**解决硬件设计的效率和正确性问题。
说白了，就是在芯片造出来之前，靠软件方法提前把设计bug和性能问题揪出来，让AI专用硬件做得更快更稳。
- **硬件编程语言**
  - 代表项目 **Filament**：把「时间」放进类型系统 → 编译阶段就能发现流水线组合错误
  - 已影响 Google XLS、Jane Street Hardcaml
- **硬件编译器与加速器设计**
  - 代表项目 **Calyx**：把 C++/Halide/PyTorch 高层程序转成高效硬件电路
  - 已被 **LLVM CIRCT** 采用
- **AI与专用硬件加速器**：聚焦新语言+编译工具，降低专用加速器的设计、优化、部署门槛
- **形式化方法 × 硬件验证**
  - 代表工作 **Dahlia**：把底层硬件约束嵌入高层语言
  - 提前检查资源冲突、时序错误、性能问题

### ⭐ 为什么这个新PI组特别值得关注？

**2026年刚启动**，方向成熟但团队还在早期建设。
- **窗口期优势**：新PI招人需求大，研究方向已成型
- **赛道卡位**：直击AI算力底层瓶颈，不做模型应用，做未来AI芯片的设计/编译/验证
- **跨领域价值**：同时连接 PL、Compiler、Architecture，底层能力迁移性强

### 🎯 什么样的学生背景最匹配？

CS/ECE/计算机工程/数字IC/体系结构等**偏硬件底层**背景最对口。

| 匹配度 | 相关经历 |
| :--- | :--- |
| 高匹配 | LLVM/MLIR/CIRCT、Compiler、Verilog/SystemVerilog、FPGA、HLS、AI Accelerator、NPU、Formal Verification、软硬件协同 |
| 需转方向 | CUDA、LLM推理加速、模型量化（需关联到编译/硬件抽象/加速器设计） |
- **注意边界**：只做过CUDA、LLM推理或模型量化 ≠ 直接匹配，申请时要讲清解决了什么编译/体系结构/硬件抽象/验证问题。

### 💡 不同背景怎么准备申请材料？

核心是**突出科研问题与个人贡献**，不要只列技能。
- **本科直博**
  - 不要只写「会Verilog」「做过FPGA」
  - 要讲清：设计了什么模块 → 系统瓶颈在哪 → 为什么这样改编译/硬件 → 性能提升多少 → 本人负责哪部分
  - 有 LLVM/MLIR、RTL、HLS、形式化验证项目经验，即使无顶会也可用完整项目+代码+推荐信证明潜力
- **硕士申博**
  - Compiler/PL方向：重点讲语言设计、IR、优化Pass、静态分析、类型系统解决了什么问题
  - Architecture/FPGA方向：突出性能、资源利用率、时序、软硬件协同
  - 做CUDA/LLM Serving/模型量化的同学：要说明研究如何连接到 Compiler、Hardware Abstraction、Accelerator Design，不能只停留在AI模型部署

### 📧 怎么投递申请？

走**MIT EECS统一申请通道**，不是单独向导师申名额。
- 导师邮箱：rnigam@mit.edu
- 导师主页：https://people.csail.mit.edu/rachit/
- 录取流程：先证明与MIT EECS整体PL/Systems/Architecture方向匹配 → 录取后再确定导师匹配

### 📝 补充细节
- FLAME Lab全称 = Foundations of Languages and Machines Lab
- 适合申请方向：Programming Languages、Compiler、Computer Architecture、AI Accelerator、FPGA、EDA
- 27Fall申请是该组正式招生的第一个完整申请季

---
*getnote | 2026-08-15 21:00*


---

## Related Notes

[[iNEST-MOC]]
[[SDI化合物键_四型架构]]
[[FPGA原型]]
[[paper2_liquid_computing_chemistry]]
