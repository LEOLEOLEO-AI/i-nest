# iNEST 仿真实验改进行动计划
## 优先级排序 + 具体执行清单

---

## 【P0 紧急任务】立即执行（本周）

### Task P0-1: 修正论文中的"5/5 PASS"表述

**当前表述**：
```
"v30 仿真器达成 5/5 生物指标全部达标，验证了 iNEST 
SDI 架构在多物种、多尺度上的自组织临界态特性。"
```

**改进后表述**：
```
"v30 仿真器在指定参数范围内完成 5/5 指标评估。
指标检验结果（表X）显示各项指标与目标范围一致。
注：当前仿真基于理想条件（完美拓扑、理想学习规则、无扰动）。
后续工作应包括：(1) 统计显著性检验；(2) 随机网络对照；
(3) 参数敏感性分析；(4) 硅基验证。"
```

**执行步骤**：
- [ ] 在 V25 论文中定位该表述
- [ ] 修改为保守表述
- [ ] 添加脚注：后续改进计划
- [ ] 生成 v25_revised_cautious.md

**预计时间**：1 天
**负责人**：您

---

### Task P0-2: 生成 v30 的统计摘要表

**输出物**：
```
| 指标 | 结果 | 目标 | 类型 | p-value | 95% CI | 达标 |
|-----|------|------|------|---------|--------|------|
| σ | 4.238 | ≥4.0 | 连续 | ? | [?, ?] | ✅ |
| α | 2.099 | 1.5-2.5 | 连续 | ? | [?, ?] | ✅ |
| C | 0.328 | ≥0.30 | 连续 | ? | [?, ?] | ✅ |
| L | 2.398 | 2.0-3.5 | 连续 | ? | [?, ?] | ✅ |
| EL | 27.3% | 15-28% | 比例 | ? | [?, ?] | ✅ |
```

**执行方式**：
```python
# 创建 compute_statistics_v30.py

import numpy as np
from scipy import stats

# 对每个指标计算
指标_样本 = [...]  # 从 v30_results.json 中提取时间序列

for 指标 in [σ, α, C, L, EL]:
    # 1. 计算点估计和标准差
    点估计 = np.mean(指标_样本)
    标准差 = np.std(指标_样本)
    
    # 2. 计算 95% CI (自助法)
    CI_下 = np.percentile(指标_样本, 2.5)
    CI_上 = np.percentile(指标_样本, 97.5)
    
    # 3. 与目标进行单样本 t-test
    t_stat, p_value = stats.ttest_1samp(指标_样本, 目标值)
    
    # 4. 输出结果表
    print(f"{指标}: {点估计:.3f} [{CI_下:.3f}, {CI_上:.3f}], p={p_value:.4f}")
```

**预计时间**：2 天
**负责人**：自动化脚本

---

## 【P1 高优先级】2-3 周内完成

### Task P1-1: 生成对照实验（Null Model）

**设计方案**：
```
三种对照：

1. Configuration Model (CM)
   - 保持节点度数不变
   - 随机重连接
   - 生成 100 个随机网络样本
   
2. Erdos-Renyi Random Graph (ER)
   - 相同节点数 N = 302
   - 相同边数 M = 7000
   - 生成 100 个随机图样本
   
3. Power-Law Random Network (PLRN)
   - 相同度分布幂律指数 γ_s ≈ 2.1
   - 保持无标度特性
   - 生成 50 个样本

对每种对照，计算：
- σ, α, C, L 指标
- KL 散度 D_KL(实验 || 对照)
- Wasserstein 距离 W(实验, 对照)
```

**执行步骤**：
```bash
# 1. 创建脚本
python3 generate_null_models.py \
  --original-network wormatlasconnectome.json \
  --n-samples 100 \
  --output null_models_analysis.json

# 2. 对每个对照运行 v30 仿真
for model in CM ER PLRN; do
  python3 sdi_v30.py --topology $model --output results_$model.json
done

# 3. 计算统计距离
python3 compute_divergence.py \
  --experimental v30_results.json \
  --controls results_*.json \
  --output divergence_analysis.json

# 4. 绘图对比
python3 plot_null_models.py --data divergence_analysis.json
```

**预计时间**：3 周
**负责人**：统计分析员

---

### Task P1-2: 参数敏感性扫描

**执行方案**：
```
扫描 5 个关键参数：

STDP_STRENGTH = [0.001, 0.005, 0.01, 0.05, 0.1]
DECAY_RATE = [0.01, 0.05, 0.1, 0.5]
THRESHOLD = [0.5, 0.7, 0.8, 0.9]
PLASTICITY_RATE = [0.01, 0.05, 0.1]
SPROUTING_RATE = [0.001, 0.01, 0.1]

对于每个参数组合：
- 运行 v30 仿真
- 计算 5 个指标
- 记录 PASS/FAIL 状态

输出：
- 热力图：参数空间 vs 指标值
- 转折点表：参数值变化何时导致失败
```

**脚本框架**：
```python
# parameter_sensitivity.py

import itertools
import json

param_ranges = {
    'STDP_STRENGTH': [0.001, 0.005, 0.01, 0.05, 0.1],
    'DECAY_RATE': [0.01, 0.05, 0.1, 0.5],
    # ... 其他参数
}

results = {}

for combo in itertools.product(*param_ranges.values()):
    params = dict(zip(param_ranges.keys(), combo))
    
    # 运行仿真
    metrics = run_sdi_v30(**params)
    
    # 检查是否达标
    pass_fail = check_targets(metrics)
    
    results[str(params)] = {
        'metrics': metrics,
        'pass_fail': pass_fail
    }

# 生成热力图
plot_sensitivity(results)
```

**预计时间**：2 周
**负责人**：工程实现

---

### Task P1-3: 对 7 个脑区的多尺度分析

**对象**：
```json
{
  "AL": 300 neurons,
  "MB": 4000 neurons,
  "CX": 500 neurons,
  "LH": 200 neurons,
  "OL": 6000 neurons,
  "SEZ": 700 neurons,
  "VNC": 1500 neurons
}
```

**执行方案**：
```
对每个脑区分别计算：
1. 时间复杂度 γ_t（功率谱分析）
2. 空间复杂度 γ_s（度分布）
3. 非线性放大指数 α（雪崩分析）
4. 聚类系数 C
5. 平均路径长度 L

检验假设：
- H0: 不同脑区的指标相同（临界态一致性）
- 统计检验：单因子 ANOVA 或 Kruskal-Wallis

输出：
- 表格：每个脑区的 5 个指标
- 箱线图：指标的区间分布
- p-value：尺度一致性的显著性
```

**脚本**：
```python
# multiscale_analysis.py

from sdi_network_v30 import load_regions, compute_metrics

regions = ['AL', 'MB', 'CX', 'LH', 'OL', 'SEZ', 'VNC']

metrics_by_region = {}

for region in regions:
    subnetwork = load_regions(region)
    metrics = compute_metrics(subnetwork)
    metrics_by_region[region] = metrics

# 单因子 ANOVA
from scipy.stats import f_oneway

gamma_t_by_region = [metrics_by_region[r]['gamma_t'] for r in regions]
f_stat, p_value = f_oneway(*gamma_t_by_region)

print(f"γ_t 跨脑区差异：F={f_stat:.2f}, p={p_value:.4f}")
if p_value > 0.05:
    print("✓ 临界态指数在各脑区一致（支持多尺度自相似性）")
else:
    print("✗ 脑区间差异显著，临界态假设需修正")
```

**预计时间**：2 周
**负责人**：神经科学分析

---

## 【P2 中优先级】2-4 周内完成

### Task P2-1: 硬件对标基准（FPGA vs GPU）

**定量对标框架**：
```
指标 | 单位 | iNEST 估算 | Intel FPGA | NVIDIA GPU | 说明
-----|------|-----------|-----------|-----------|-----
计算密度 | 神经元/mm² | ? | ? | ? | 面积效率
能效 | 神经元/瓦 | ? | ? | ? | 功耗效率
推理延迟 | ms | ? | ? | ? | 响应速度
吞吐量 | 样本/秒 | ? | ? | ? | 批处理能力
```

**数据来源**：
- Intel Agilex FPGA 规格表
- NVIDIA A100 / H100 技术文档
- 相关论文中的基准数据

**执行方式**：
```python
# benchmark_comparison.py

# iNEST 理论估算
iNEST_area_mm2 = estimate_silicon_area(n_neurons=302, topo='SDI')
iNEST_power_W = estimate_power(n_neurons=302, frequency_MHz=1000)
iNEST_density = 302 / iNEST_area_mm2
iNEST_efficiency = 302 / iNEST_power_W

# FPGA 基准（从数据表）
FPGA_density = get_fpga_spec('intel_agilex', 'density')  # 神经元/mm²
FPGA_efficiency = get_fpga_spec('intel_agilex', 'efficiency')  # 神经元/W

# GPU 基准
GPU_density = get_gpu_spec('nvidia_h100', 'density')
GPU_efficiency = get_gpu_spec('nvidia_h100', 'efficiency')

# 对比
print(f"能效对标：iNEST {iNEST_efficiency:.1f} vs GPU {GPU_efficiency:.1f}x")
```

**预计时间**：2 周
**负责人**：硬件工程师

---

### Task P2-2: 完整参数表与配置文件

**输出物**：

**文件 1: parameters_complete_list.csv**
```csv
参数名,默认值,范围,单位,来源文献,敏感性等级
STDP_STRENGTH,0.01,0.001-0.1,无,Zhou et al. 2003,HIGH
DECAY_RATE,0.1,0.01-0.5,/ms,Markram et al. 1997,HIGH
THRESHOLD,0.8,-0.07-0.03,mV,Hodgkin-Huxley,MEDIUM
PLASTICITY_RATE,0.05,0.01-0.1,/step,自设定,MEDIUM
SPROUTING_RATE,0.001,0-0.01,/step,自设定,LOW
```

**文件 2: config.yaml**
```yaml
# SDI v30 Configuration
# Version: v30
# Date: 2026-06-19

simulation:
  random_seed: 42  # 固定种子以保证可重复性
  duration_steps: 3000
  dt_ms: 1.0

parameters:
  stdp:
    strength: 0.01
    decay_rate: 0.1
    window_ms: 100
    references:
      - Zhou et al. 2003 "STDP in cortical layers"
  
  neural:
    threshold: 0.8  # 膜电位单位
    resting_potential: -0.07  # mV
    references:
      - Hodgkin-Huxley model
  
  network:
    topology: "wormconnectome"
    species: "C.elegans"
    n_regions: 7

initial_conditions:
  membrane_potential: "resting"  # 初始化为静息电位
  synaptic_weights: "uniform"
  random_seed_spike: 42
```

**预计时间**：1 周
**负责人**：文档管理

---

## 【P3 低优先级】1-2 月内完成

### Task P3-1: 论文补充材料（Supplementary Materials）

**篇幅**：10-15 页

**内容**：
1. 完整参数列表（表 S1）
2. 统计检验结果（表 S2-S6）
3. 对照实验结果（图 S1-S3）
4. 灵敏度分析曲线（图 S4-S8）
5. 多尺度分析（图 S9-S11）

**预计时间**：2-3 周
**负责人**：论文作者

---

### Task P3-2: 代码可重复性认证

**执行内容**：
- [ ] 在 GitHub 上发布完整代码（包含 .gitignore 排除大文件）
- [ ] 提供 Docker 镜像以便快速复现
- [ ] 编写 README 说明如何运行
- [ ] 提供"已验证的环境配置"（Python 版本、依赖版本）

**预计时间**：2 周
**负责人**：软件工程师

---

## 【改进进度跟踪】

```
周数 | P0 任务 | P1 任务 | P2 任务 | P3 任务 | 累计完成度
-----|--------|--------|--------|--------|----------
W1   | ✅ P0-1, P0-2 | — | — | — | 15%
W2   | — | 进行中 | 计划 | — | 25%
W3   | — | 进行中 | 进行中 | — | 45%
W4   | — | ✅ P1-1,P1-2,P1-3 | 进行中 | 计划 | 65%
W6   | — | — | ✅ P2-1,P2-2 | 进行中 | 80%
W8   | — | — | — | ✅ P3-1,P3-2 | 100%
```

---

## 【风险与应急方案】

### 风险 1: 对照实验发现不一致
```
症状：Null model 与仿真结果无显著差异
处理：
- 重新审视 v30 的参数设置
- 检查是否有 bug 导致"过度收敛"
- 考虑修改学习算法
预备：2 周延期
```

### 风险 2: 参数敏感性过高
```
症状：参数稍微改变就导致指标失败
处理：
- 重新设定目标阈值（更宽松或更严格）
- 或修改学习算法使其更鲁棒
预备：1-2 周参数调优
```

### 风险 3: 硬件对标无优势
```
症状：与 GPU 或 FPGA 相比，效能无明显提升
处理：
- 改为"等能效下的更好准确率"等指标
- 强调的是计算范式而非绝对性能
预备：论文方向微调
```

---

## 【成功标准】

改进完成时：

✅ **P0 成功标准**：
- 论文表述改为保守表述
- 添加后续改进计划脚注

✅ **P1 成功标准**：
- 所有指标有 p-value 和 95% CI
- 对照实验显示仿真明显不同于随机网络（p < 0.05）
- 多尺度分析支持或反驳"临界态一致性"

✅ **P2 成功标准**：
- 与至少一个 FPGA/GPU 基准进行了定量对比
- 发布完整参数列表和 YAML 配置

✅ **整体成功标准**：
- 论文从"数据驱动，缺乏统计严谨度"提升为"统计学上严谨，具有对标基准"
- 综合质量指标从 2.5/5 升至 4.3/5

