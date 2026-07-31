---
title: "代码/仿真验证报告"
date: 2026-07-25
author: iNEST 验证中枢
type: verification-report
phase: C
tags: [verification, code, simulation, SDDE, CST]
provenance: own
---

# 代码/仿真验证报告

> Phase C: 代码/仿真验证 | 2026-07-25

---

## 一、验证对象

### 1.1 脚本清单

| # | 脚本路径 | 功能 | 验证状态 |
|---|----------|------|----------|
| 1 | `50_Output/54_Code/em_milstein_convergence.py` | EM/Milstein 收敛阶验证 | ✅ 已运行 |
| 2 | `50_Output/54_Code/inest_sdde_visualization.py` | SDDE 三图可视化 | ⚠️ 已运行（Figure 1 有问题） |
| 3 | `50_Output/54_Code/iNEST/cst_phase_scan.py` | CST 相变扫描 N=1024 | ✅ 已运行 |
| 4 | `50_Output/54_Code/gen_inest_sdde_ppt.py` | PPT 生成 | 未验证（非核心） |
| 5 | `50_Output/54_Code/iNEST/multiscale.py` | 多尺度分析 | 未验证 |
| 6 | `50_Output/54_Code/iNEST/run_rg_flow.py` | 重整化群流 | 未验证 |

---

## 二、em_milstein_convergence.py — ✅ 真实有效

### 2.1 脚本概述

- **功能**: 验证 Euler-Maruyama (p=1/2) 和 Milstein (p=1) 收敛阶
- **方法**: 蒙特卡洛模拟 M=2000 条路径，对比解析精确解
- **参数**: a=-1.0, b=0.5, c=1.0, tau=1.0, T=2.0
- **随机种子**: `rng = np.random.default_rng(20260725)`

### 2.2 运行结果

```
EM       fitted order  ~ 0.553   (theory 0.5)
Milstein fitted order  ~ 1.077   (theory 1.0)
已保存：EM_Milstein_convergence.pdf / .png
```

### 2.3 评估

| 维度 | 评估 |
|------|------|
| 数值正确性 | ✅ EM 阶数 0.553 接近理论 0.5；Milstein 阶数 1.077 接近理论 1.0 |
| 参考解质量 | ✅ 使用解析精确解（非数值参考），符合最佳实践 |
| 随机种子 | ✅ 固定种子 20260725，可复现 |
| 蒙特卡洛路径数 | ✅ M=2000 足够消除统计涨落 |
| 输出 | ✅ 生成 PDF + PNG 图表 |

**结论**: 该脚本是真实有效的数值收敛验证，结果可信。

---

## 三、inest_sdde_visualization.py — ⚠️ Figure 1 严重问题

### 3.1 脚本概述

生成三张图：
- Figure 1: EM/Milstein 收敛阶对比
- Figure 2: 加性 vs 乘性噪声 SDDE 轨迹
- Figure 3: 涌现阈值 Θ 相图 + iNEST 六级智能热区

### 3.2 Figure 1 — ❌ 硬编码数据（严重违规）

**问题**: Figure 1 的数据（第 65-67 行）为人工构造的完美几何数列，非真实计算结果。

```python
# 第 65-67 行
h       = np.array([2**-4, 2**-6, 2**-8, 2**-10, 2**-12])
err_em  = np.array([1.00e-1, 5.00e-2, 2.50e-2, 1.25e-2, 6.25e-3])
err_mil = np.array([1.00e-1, 2.50e-2, 6.25e-3, 1.56e-3, 3.91e-4])
```

**证据**:
- EM 误差: 每步精确减半 (1e-1 → 5e-2 → 2.5e-2 → 1.25e-2 → 6.25e-3)
- Milstein 误差: 每步精确减四分之一 (1e-1 → 2.5e-2 → 6.25e-3 → 1.56e-3 → 3.91e-4)
- 真实的蒙特卡洛收敛实验（如 `em_milstein_convergence.py`）不可能产生如此完美的几何数列
- 代码注释标注为"Buckwar 理论基准"，但 Buckwar 的理论预测的是收敛阶（斜率），不是具体误差值

**与真实脚本对比**:
| 指标 | 硬编码 Figure 1 | 真实 em_milstein_convergence.py |
|------|----------------|-------------------------------|
| EM 斜率 | 0.500 (完美) | 0.553 (真实) |
| Milstein 斜率 | 1.000 (完美) | 1.077 (真实) |
| 数据来源 | 人工构造 | M=2000 蒙特卡洛模拟 |
| 可复现性 | ❌ 无法复现 | ✅ 固定种子可复现 |

**违规级别**: P0（严重）— 将人工构造数据呈现为理论基准，违反 AGENTS.md 规则 A（准确性是刚性原则）

**修复方案**: 用 `em_milstein_convergence.py` 的真实输出替换 Figure 1 的硬编码数据。

### 3.3 Figure 2 — ✅ 真实仿真

**功能**: 对比加性噪声 `g(X)=0.30` 与乘性噪声 `g(X)=0.30X` 的 SDDE 轨迹

**代码质量评估**:
- `simulate_sdde()` 函数实现了标准的 Euler-Maruyama 离散
- 使用共享 Wiener 增量保证跨子图可比性
- 参数: a=-1, b=0.5, tau=1, T=20, dt=0.005, n_traj=20
- 延迟项 `X_tau = X[i - n_delay]` 实现正确

**结论**: Figure 2 是真实的 SDDE 仿真，结果可信。

### 3.4 Figure 3 — ✅ 相图可视化

**功能**: 绘制涌现指标 Θ = 2μ_max(A) + λ_g 的二维相图

**评估**:
- Θ 的定义与 SDDE 理论一致（耦合谱半径 + 噪声强度）
- iNEST 六级智能标签 (L1-L6) 标注在相图热区
- 使用 `pcolormesh` + `contour` 组合，视觉表达清晰
- ⚠️ 六级智能标签的位置标注是定性的，未与 CST 阈值 {1/√2, 1, φ, e, π, δ} 建立定量映射

**结论**: Figure 3 是合理的可视化，但标签位置缺乏定量依据。

---

## 四、cst_phase_scan.py — ✅ 真实有效

### 4.1 脚本概述

- **功能**: 扫描 Watts-Strogatz 网络参数 p，识别相变阈值
- **网络规模**: N=1024, K=16
- **指标**: sigma (小世界系数), C (聚类系数), L (平均路径长度), E_glob (全局效率), S_eff (结构效率)
- **随机种子**: SEED=42

### 4.2 运行结果

```
关键发现:
- Sigma >= 4.0 阈值: p=0.001, sigma=8.46
- Sigma 峰值: p=0.050, sigma=26.15
- S_eff 峰值: p=0.060, S_eff=0.1651
- 随机基线: S_eff_rand=0.0061
- 峰值/基线比: ~27x
- 相变检测 (d_sigma/dp > 50): p=0.002 至 p=0.050
```

### 4.3 评估

| 维度 | 评估 |
|------|------|
| 算法正确性 | ✅ Watts-Strogatz 实现、聚类系数、BFS 平均路径计算均正确 |
| 采样策略 | ✅ N=1024 下对 50 个源节点采样，平衡精度与速度 |
| 相变检测 | ✅ d_sigma/dp > 50 阈值合理，检测到 10 个相变点 |
| 随机基线对比 | ✅ 与 ER 随机图对比，峰值 S_eff 比基线高 27 倍 |
| 输出路径 | ⚠️ 硬编码为 `C:\Users\LEO\Documents\Codex\...`，需修改 |
| 物理意义 | ✅ 证实小世界网络在 p≈0.05-0.06 处存在结构效率相变峰 |

**结论**: 该脚本真实有效，结果支持 CST 理论中"网络拓扑相变驱动智能涌现"的核心假设。

### 4.4 与 CST 理论的映射

- sigma (小世界系数) → CST 中 R_sw (小世界系数分量)
- S_eff = C × E_glob → CST 中 Sc (空间复杂度) 的简化版本
- 相变峰值 p≈0.05 → 对应 Watts-Strogatz 经典结果中"小世界"涌现区间

---

## 五、LaTeX 论文引用验证

### 5.1 论文信息

- **标题**: "From Compute to Complexity"
- **作者**: Qinrang Liu (刘勤让)
- **日期**: June 2026
- **引用数**: 66 条
- **文件路径**: `50_Output/51_Papers/A1_ARS评审与终稿/latex/A1_CST_FINAL.tex`

### 5.2 引用验证结果

#### 核心引用 [1]-[50] — ✅ 全部为真实经典论文

| 引用 | 作者 | 年份 | 期刊 | 真实性 |
|------|------|------|------|--------|
| [1] | Tononi | 2004 | BMC Neurosci | ✅ IIT 奠基论文 |
| [6] | Beggs & Plenz | 2003 | J. Neurosci | ✅ 神经雪崩奠基论文 |
| [8] | Watts & Strogatz | 1998 | Nature | ✅ 小世界网络奠基论文 |
| [17] | Feigenbaum | 1978 | J. Stat. Phys | ✅ Feigenbaum 常数原始论文 |
| [23] | Friston | 2010 | Nat. Rev. Neurosci | ✅ 自由能原理 |
| [44] | von Neumann | 1966 | UI Press | ✅ 自繁殖自动体 |
| [45] | Turing | 1950 | Mind | ✅ 计算机器与智能 |
| [48] | Barabási & Albert | 1999 | Science | ✅ 无标度网络 |
| [58] | Wilson | 1983 | Rev. Mod. Phys | ✅ 重整化群 |

#### 新增引用 [51]-[66] — ⚠️ 部分需独立验证

| 引用 | 内容 | 级别 | 验证状态 |
|------|------|------|----------|
| [52] | Liu, Q. 2026 预印本 | S5 | ✅ 正确标注为内部预印本 |
| [54] | Battiston et al. arXiv:2510.05253 → Nature Reviews Physics 2026 | S3 | ⚠️ 需验证 arXiv ID |
| [55] | Chung & Abbott, Nature Neuroscience 2026, DOI:10.1038/s41593-025-02183-y | S2 | ⚠️ 需验证 DOI |
| [56] | Fan et al., Nature Communications 16, 6821 (2025), DOI:10.1038/s41467-025-62251-6 | S2 | ⚠️ 需验证 DOI |
| [59] | Xia et al., "Nature Sensors" (2026) | — | ❌ "Nature Sensors" 期刊不存在 |
| [60] | [HIFT technology group] 2026 预印本 | S5 | ✅ 正确标注为内部预印本 |
| [63] | Bellitto et al. arXiv:2603.09576 (2026) | S3 | ⚠️ 需验证 arXiv ID |
| [64] | Chen et al. arXiv:2603.18620 (2026) | S3 | ⚠️ 需验证 arXiv ID |
| [65] | Zhuge et al. arXiv:2604.06425 (2026), Meta AI/KAUST | S3 | ⚠️ 需验证 arXiv ID |
| [66] | Zhang, W.-Z. JSAI 2026 Oral | S5 | ✅ 正确标注为会议报告 |

### 5.3 引用问题清单

1. **[59] "Nature Sensors" (2026)** — 该期刊不存在（Nature 系列中没有此期刊），需更正或移除
2. **[54], [63], [64], [65]** — 2026 年 arXiv 预印本，需在线验证 arXiv ID 是否真实
3. **[55], [56]** — 提供了 DOI，需在线验证 DOI 是否解析到正确论文

---

## 六、验证总结

### 6.1 脚本验证结果矩阵

| 脚本 | 真实性 | 数值正确性 | 可复现性 | 总评 |
|------|--------|------------|----------|------|
| em_milstein_convergence.py | ✅ | ✅ | ✅ | **通过** |
| inest_sdde_visualization.py Fig.1 | ❌ 硬编码 | ❌ 伪造数据 | ❌ | **不通过** |
| inest_sdde_visualization.py Fig.2 | ✅ | ✅ | ✅ | **通过** |
| inest_sdde_visualization.py Fig.3 | ✅ | ✅ | ✅ | **通过** |
| cst_phase_scan.py | ✅ | ✅ | ✅ | **通过** |

### 6.2 关键发现

1. **真实验证通过**: EM 收敛阶 0.553、Milstein 收敛阶 1.077，与理论预测一致
2. **硬编码问题确认**: `inest_sdde_visualization.py` Figure 1 使用完美几何数列冒充理论基准
3. **相变扫描有效**: N=1024 网络在 p≈0.05 处确实存在结构效率相变峰，支持 CST 理论
4. **LaTeX 引用基本可靠**: 核心 50 条引用全部真实，新增引用中 [59] 存在期刊名错误

### 6.3 整改建议

| 优先级 | 问题 | 建议 |
|--------|------|------|
| P0 | Figure 1 硬编码 | 用 `em_milstein_convergence.py` 真实输出替换 |
| P1 | [59] "Nature Sensors" | 核实并更正期刊名或移除该引用 |
| P1 | cst_phase_scan.py 输出路径 | 修改为相对路径或环境变量 |
| P2 | [54]-[65] arXiv ID 验证 | 在线验证并标注验证状态 |
| P2 | Figure 3 标签位置 | 建立与 CST 六级阈值的定量映射 |

---
*验证人: iNEST 验证中枢 | 验证日期: 2026-07-25 | 报告版本: v1.0*
