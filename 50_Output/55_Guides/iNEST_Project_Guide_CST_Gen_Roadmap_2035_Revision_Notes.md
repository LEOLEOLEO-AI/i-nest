---
title: iNEST 项目指南修订说明：CST 与 Gen1–Gen5 时间节奏
status: review
revision_date: 2026-07-24
---

# 修订说明

## 依据材料
- CST v32：`50_Output/51_Papers/A1_ARS评审与终稿/A1_CST_Theory_V32_MERGED_CLEAN.md`
- 原始项目指南：`D:/Project/十五五/苏州实验室/iNEST_Project_Guide_v2.0_HYu(1)_YuchaoYang(1).docx`
- 智涌脑路线：`D:/iNEST/Write/Code/other/iNEST4.html`
- TCC 基线：`30_TCC/TCC_Knowledge_Base_Baseline_v2.0.md`

## 发现的问题
1. 原指南使用 TCC-11，与 TCC-16（R=6、T=6、C=4）冲突。
2. 原指南把 CST `>5.0`、`>8.0`、`>13.0` 当能力阈值，但 CST v32 的 `Sc,Tc` 归一化范围为 `(0,1]`，缺少标定依据。
3. 原指南使用 `10^6` 键、`CST>5.0`、良率/CV/能效等未经逐项验证的数字。
4. `iNEST4.html` 作为唯一代际路线基准，明确 2035 年为 Gen5 通用智能，2035+ 为 Gen6 超级智能理论探索。

## 修订结果
- 保留 CST v32 公式，分量范围与能力映射分离。
- 统一 TCC-16：R6/T6/C4。
- 完全采用 iNEST4.html 路线：Gen1=2027、Gen2=2029、Gen3=2031、Gen4=2033、Gen5=2035、Gen6=2035+；Gen5 对应 2035 年通用智能目标。
- 将 2035 Gen5 明确为通用智能能力目标，不写成已实现成果。
- 删除未经验证的硬指标，替换为验证方法和 `[待测]` 状态。
- Gen5 纳入 2035 年通用智能目标；Gen6 保留为 Gen5 之后的扩展探索。

## 必须执行的验证任务
`V-CST-01` 至 `V-CST-06`、`V-GEN-01`，详见修订版指南。

## 审批后动作
将验证任务同步到研发看板和 Home 主页，显示当前代际、下一里程碑、待测指标和证据状态。审批前不覆盖原始 DOCX，不把规划目标写入已完成成果。



