# iNEST 课题组科研数据管理与存取规范 (Data Management Standard)

> **知识库说明**：本规范定义了课题组在理论验证、仿真编程、论文撰写过程中，产生的所有核心数据（CSV, JSON, 图表等）的**统一存储、提取与校验规则**。以确保科研数据的可追溯性、版本一致性及跨脚本自动对齐。

## 一、 核心数据集存放位置 (Single Source of Truth)

为了避免“散落各处、版本冲突”，所有经过清洗、校验的最终版实验与仿真数据，**必须集中存放在专用的数据仓库目录中**：
```text
/home/work/.openclaw/workspace/00_KnowledgeBase_知识库/05_Datasets_仿真与实验数据/
├── BNN_Connectomes/      # 生物神经网络连接组原始数据 (C.elegans, Drosophila等)
├── ANN_ComputeGraphs/    # 人工神经网络计算流图提取数据 (ResNet, Transformer等)
├── Simulation_Results/   # 各版本仿真输出结果 (如 cst_v21_results.json)
└── Paper_Figures_Data/   # 专用于论文作图的清洗后汇总数据 (如 V22_Engineering_PlotData.csv)
```

## 二、 数据持久化与版本控制规则

### 1. 数据格式双规制
- **结构化机器可读（首选）**：仿真和计算的中间/最终结果，一律使用 `.json` 保存（如 `v22_cst_metrics.json`）。JSON支持复杂的嵌套结构（如分别记录 $S_c, T_c, \Gamma_{st}, RI$ 以及关联的拓扑类型）。
- **学术表格与绘图提取**：用于论文作图或LaTeX表格生成的数据，统一导出为平铺的 `.csv` 格式，确保第三方绘图软件（如Origin, Matlab, PGFPlots）可无缝导入。

### 2. 严禁覆盖，后缀定版
严禁使用诸如 `latest_results.csv` 这种命名覆盖历史数据。
- 命名必须包含**版本号**或**日期戳**（例如：`cst_results_v21_20260326.json`）。
- 被主编或编辑确认采纳的最终版本，必须加上 `_FINAL` 后缀，并设为只读（例如：`v22_cst_30samples_FINAL.csv`）。

## 三、 代码中的“防错提取”方法论 (Robust Data Access)

在所有用于绘图、对比验证的 Python 脚本中，**必须遵循以下数据加载范式**，防止因路径变更导致代码崩溃或加载错数据：

```python
import os
import json
import pandas as pd

def load_validated_cst_data(target_version="v22"):
    """
    统一的防错数据加载器。优先从知识库的标准化目录中寻找对应版本的数据。
    """
    base_dir = "/home/work/.openclaw/workspace/00_KnowledgeBase_知识库/05_Datasets_仿真与实验数据/Simulation_Results/"
    
    # 1. 寻找带有 FINAL 标记的最高优先级数据
    final_file = os.path.join(base_dir, f"cst_results_{target_version}_FINAL.json")
    if os.path.exists(final_file):
        with open(final_file, 'r') as f:
            return json.load(f)
            
    # 2. 如果没有 FINAL 版本，寻找该版本的最新仿真快照
    # (通过时间戳或文件搜索逻辑...)
    
    raise FileNotFoundError(f"未找到 {target_version} 的校验版数据，请检查数据仓库。")
```

## 四、 跨语言/跨系统对齐规则

为了确保在不同脚本（如生成论文表格的脚本、画图的脚本、做RI对比验证的脚本）中读取到的参数意义绝对一致，JSON/CSV的键名（Keys）必须遵守全局字典：
- **物种/模型名称**：`"ID"` 或 `"Name"` (如 "C.elegans", "ResNet-50")
- **空间复杂度**：`"Sc"` 或 `"Sigma"` (必须统一保留至少3位小数)
- **时间复杂度**：`"Tc"` 或 `"Tau"`
- **时空耦合度**：`"Gamma_st"` (对于ANN，需硬编码并附带注释解释其为0的物理原因)
- **智能等级/类型**：`"Level"` (如 "L0", "L1")，`"Type"` (如 "Reaction", "General")

所有新接入的数据，必须通过一个统一的 `data_validator.py` 脚本校验键名规范与数值域（如 $\tau$ 是否在临界域内），校验通过后方可存入 `05_Datasets_仿真与实验数据` 目录。
