# 研究任务确认队列 - 2026-08-17

> 这里只生成候选任务；批准前不会写入正式工作计划。

## RP-2026-07-19-2124106212ac
- 状态: `pending_review`
- 候选任务: V-NT-01：在统一 LIF 网络、固定数据集和固定随机种子下，建立 BPTT、局部 STDP/三因子规则与 e-prop 类规则的最小对照。验证方法：仿真。验收标准：每组具有版本、配置、输入数据、训练/测试指标、内存和运行时间记录。
- 来源: [[2026-07-20_NeuroTrain_fulltext_analysis]]
- 证据: [引用] 原始论文洞察文件，需人工核验后执行
- 确认方式: 将 JSON 中该条目的 `status` 改为 `approved`，再运行 `approve_research_tasks.py`。

## RP-2026-07-19-cbf3076a81e9
- 状态: `pending_review`
- 候选任务: V-NT-02：在 V-NT-01 的同一训练任务上替换 SDI/NoC 候选拓扑，比较学习更新的消息量、峰值链路负载和更新等待时间。验证方法：网络仿真。验收标准：拓扑以外变量固定，报告统计方法和原始运行日志。
- 来源: [[2026-07-20_NeuroTrain_fulltext_analysis]]
- 证据: [引用] 原始论文洞察文件，需人工核验后执行
- 确认方式: 将 JSON 中该条目的 `status` 改为 `approved`，再运行 `approve_research_tasks.py`。

## RP-2026-07-19-f3102a5d5604
- 状态: `pending_review`
- 候选任务: 可借鉴量子NoC的纠缠管理策略，探索经典NoC中自适应路由或资源分配的新思路
- 来源: [[2026-07-19_arXiv_Adaptive Entanglement Management in Quantum Multi-Core Archi]]
- 证据: [引用] 原始论文洞察文件，需人工核验后执行
- 确认方式: 将 JSON 中该条目的 `status` 改为 `approved`，再运行 `approve_research_tasks.py`。

