---
provenance: own
---

# V-CST 执行状态

**日期**：2026-07-24  
**主库**：`D:\Obsidian\vault`  
**协议**：`V-CST-00_protocol.md`

## 已完成

- `V-CST-00` 协议已冻结：公式、证据分类、缺失值规则、质量门禁和 RG 假设已写入文件。
- 已确认线虫结构文件存在：`40_iNEST/45_Simulation/connectome_v8_data.json`。
- 该文件可读取节点、化学边、电突触边和节点类型，支持 V-CST-01 的结构输入审计。
- 已创建无生物学回退值的计算器 `calculate_sc.py`。
- 已创建功能数据审计器 `audit_celegans_data.py`。

## 未完成与原因

- `V-CST-01`：脚本已具备，但本次未产生正式结果文件。运行环境的 Python 虚拟环境指向不存在的 Python 3.11，系统 `py` 启动器也报告没有安装的 Python 解释器。
- `V-CST-02`：未执行。主库目前没有经确认的“神经元 ID × 时间”线虫原始活动时序。
- `V-CST-03`：未执行，因为缺少可匹配的功能时序。
- `Tc`、`Gamma_st`、`alpha` 和完整 `CST`：均为 `NOT_EXECUTED`，禁止用常数、随机数或旧实验结果填充。

## 恢复后的首要命令

在安装并确认 Python 3.11+ 后运行：

```powershell
$dir = 'D:\Obsidian\vault\40_iNEST\45_Simulation\v_cst_validation'
python "$dir\audit_celegans_data.py" --root 'D:\Obsidian\vault\40_iNEST\45_Simulation' --output "$dir\celegans_data_audit.json"
python "$dir\calculate_sc.py" --connectome 'D:\Obsidian\vault\40_iNEST\45_Simulation\connectome_v8_data.json' --output "$dir\v_cst_01_sc_result.json"
```

## 当前结论

本轮完成的是“可审计验证管线的建立”，不是 CST 生物学正确性的验证。只有 V-CST-01 产生可复现结果，并获得带神经元 ID 映射的真实功能数据后，才可继续 V-CST-02/V-CST-03。

