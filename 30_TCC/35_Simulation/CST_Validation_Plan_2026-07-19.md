---
provenance: external
---

# CST 仿真验证计划 — 2026-07-19

## 证据边界

本计划只把可追溯结果写入论文。性能数字必须标记为 `[实测]`、`[仿真]`、`[引用]`、`[推导]` 或 `[待测]`，并绑定验证编号。

## 本地数据盘点

- `[待核验]` Hemibrain connectome：`30_TCC/35_Simulation/sdi_sim/hemibrain_real_connectome_v3.json`。文件头标注 `N=46297`、`n_edges=1640361`，这些是文件内容字段，不代表已完成来源核验。
- `[待核验]` C. elegans connectome：`30_TCC/35_Simulation/celegans_sim/connectome_v8_data.json`。
- `[待核验]` Larval CNS、Allen mouse、macaque 和多版本仿真结果已存在于 `40_iNEST/45_Simulation/`。
- `fetch_hemibrain_v3.py` 中包含硬编码访问令牌；禁止继续使用或提交该令牌。后续下载必须改用环境变量，并记录数据集版本、查询条件、下载时间和 SHA-256。

## 分阶段验证

### V-CST-01：数据完整性

方法：读取 JSON schema，检查节点 ID、边端点范围、重复边、权重非负性，并计算 SHA-256。

验收：零个非法端点；重复边处理规则明确；数据来源和版本写入 manifest；未通过前不得称为真实 connectome 验证。

### V-CST-02：零模型基线

方法：同一节点数、度分布和随机种子下，对比真实 connectome、度保持随机化和 Erdős–Rényi/小世界基线。

验收：所有模型使用同一指标定义、同一采样次数和同一置信区间方法；指标数值标记 `[仿真]`。

### V-CST-03：LIF/SNN 动力学复现

方法：固定时间步、阈值、突触延迟、输入协议和随机种子，复现现有 Hemibrain 与 C. elegans 脚本。

验收：日志包含配置快照、代码版本、输入 SHA-256、输出文件和异常信息；没有配置就不接受结果。

### V-CST-04：CST 相变/临界性扫描

方法：只扫描预先声明的耦合参数或控制参数，输出 avalanche、同步、模块度和任务性能的原始轨迹。

验收：报告扫描范围、步长、边界处理、重复实验和 null model；任何阈值结论必须绑定原始数据和验证编号。

### V-CST-05：跨生物网络泛化

方法：在 C. elegans、Drosophila/Hemibrain 和哺乳动物连接组上执行同一分析协议。

验收：区分“跨数据集复现”与“机制成立”；不能用单一网络结果声称普适性。

## TRAE + Genspark 协同策略

- Codex：唯一任务编排者、证据账本维护者、脚本和结果入口维护者。
- TRAE：只做单文件调试、可视化和交互式代码检查；提交改动前运行对应 `V-CST-*` 检查。
- Genspark：做假设对抗、论文/方法对比和图表叙事审查；输入必须来自带来源的 brief，不直接改正式结果。
- Obsidian：保存 brief、配置、原始结果、报告和人工确认状态；不把聊天结论当实验事实。

协同交换格式：每次任务都提交 `question`、`input_files`、`input_sha256`、`config`、`expected_output`、`verification_id`、`status` 七个字段。

## 下一步顺序

1. 完成 `V-CST-01` 数据 manifest 和来源核验。
2. 选一个小规模 C. elegans 子集完成 `V-CST-02` 和 `V-CST-03`。
3. 再扩展到 Hemibrain，最后做跨数据集比较。
4. 只有通过前三步，才把结果写入论文 Section 4/5。


<!-- orphan-cleanup: linked to MOC -->
## 来源回链

- [[TCC_Master_Index]]
