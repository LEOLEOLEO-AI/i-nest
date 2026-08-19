---
type: research-task-proposal
status: pending_review
direction: iNEST
source_type: external-evidence
evidence_status: "[引用] 方法启迪已确认；结果待复现"
output_type: simulation-and-architecture
priority: P1
---

# iNEST 层次化模块架构：仿真与设计基线任务建议

## 证据来源

- [[2026-08-12_arXiv_The Neural Division of Labor Biologically-Inspired Modular A]]
- 外部论文提供模块隔离、功能分工与生物启发训练机制的参考，不构成团队原创结论。

## 已确认启迪

iNEST 应把层次化、模块性和功能分工纳入架构基线：以可组合模块承载局部表征、记忆、决策或调控功能；模块间采用可观测的事件与状态接口，避免无边界的全局耦合。

## 待审批任务

- 任务编号：V-iNEST-MOD-01
- 目标：建立模块化 SNN 与全局耦合 SNN 的最小可复现对照。
- 固定项：任务、数据集、随机种子、训练预算与评估协议。
- 变量：模块划分、模块间通信图、局部学习规则与全局耦合基线。
- 记录指标：[待测] 准确率/任务损失、抗扰动能力、模块间消息量、峰值通信负载、存储占用、运行时间。
- 验收：提交版本化配置、原始日志、绘图脚本和结论边界；不得使用未经验证的性能数字。

## 预期输出

- iNEST 层次化模块架构设计说明
- 一组可复现仿真配置与结果记录
- 论文和专利的候选论点，需在验证后另行确认

## 决策

当前状态为 pending_review。确认后才进入正式研发看板与任务计划。
