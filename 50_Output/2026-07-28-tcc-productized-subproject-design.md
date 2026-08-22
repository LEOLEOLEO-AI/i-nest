---
provenance: own
---

# TCC 产品化子工程（`tcc`）设计说明

> 面向后续长期维护：在 `cim-design` 仓库内新建一个“产品化子工程”作为主力代码归宿，顶层包名为 `tcc`。DRBE 与推理（infer）作为两个 workload 共享同一套 TCC 核心层（L1/L2/L3 + RTC + metrics）。

## 1. 目标与范围

### 1.1 目标（必须达成）

- 在仓库内新增 **产品化子工程**：`src/tcc/`，作为后续主力开发与维护入口。
- 保持现有 DRBE MVP 主链体验不丢：仍支持一键运行 `IQ 回放 → FFT → DBF → 拓扑页切换 → 指标输出`。
- 固化 TCC 核心层边界：将 **L1/L2/L3、RTC 原语、指标体系（含 `τ_commit/τ_apply/τ_resume`）** 抽到 `tcc/core`，供不同 workload 复用。
- 建立 workload 分层：`tcc/workloads/drbe` 与 `tcc/workloads/infer` 分别承载 DRBE 与推理相关实现，互不相互依赖（只能依赖 `tcc/core`）。
- 术语一致性：工程中统一使用 **算粒（compute grain）/存粒（storage grain）**。

### 1.2 非目标（本轮明确不做）

- 不在本次结构化过程中引入连续弛豫 L3（路径 B）实现；仅保留可替换的接口位。
- 不试图一次性删除或完全重写旧的平铺目录代码；旧结构转入 legacy 管理。
- 不引入复杂的构建/发布流水线（CI/CD、wheel 发布等）；仅做产品化目录与可安装包的基础设施。

## 2. 现状与问题

当前仓库已具备 DRBE MVP 的模块化骨架（如 `rtc_primitives/`、`l1_clusters/`、`l2_liquid_topology/`、`l3_solver/`、`metrics/`、`topology_pages/`、`task_templates/` 等），但仍存在产品化维护痛点：

- **模块边界不硬**：平铺目录容易在后续扩展推理/更多 IP 时产生循环依赖与命名漂移。
- **产品代码与实验脚本容易混杂**：会导致“能跑但不可维护”，难以稳定扩展与测试。
- **workload 扩展路径不清晰**：DRBE 与推理未来会共享 L1/L2/L3，但各自需要独立的簇库、页库与 pipeline。

因此本次选择在仓库内新建产品化子工程，通过结构约束把上述问题“系统性消除”。

## 3. 总体架构

### 3.1 核心原则

- **Core / Workloads 分离**：`tcc/core` 只放“通用框架能力”，`tcc/workloads/*` 放“具体任务域实现”。
- **Workload 只依赖 Core**：任何 workload 代码不得 import 另一个 workload。
- **Legacy 只读**：旧结构保留用于对照与回溯，但后续新增功能只进入 `src/tcc`。
- **可解释优先**：L3（路径 A）在产品化子工程中以“规则调度 + 可解释成本分解”为 baseline；连续弛豫后续只替换求解器，不改变外部接口。

### 3.2 包命名与定位

- 顶层包：`tcc`（长期主工程名）
- DRBE：`tcc.workloads.drbe`
- 推理：`tcc.workloads.infer`（先建骨架，占位，不在本轮实现推理功能）

## 4. 目标目录结构

### 4.1 顶层结构（仓库内）

```
.
├── src/
│   └── tcc/
│       ├── __init__.py
│       ├── core/
│       └── workloads/
├── tests/
├── scripts/
└── main.py
```

约束：
- `src/tcc`：产品代码唯一归宿。
- `tests`：优先为 `src/tcc` 提供单元/集成测试。
- `scripts`：一次性实验/分析脚本目录；**产品代码不得 import `scripts`**。
- 根 `main.py`：兼容入口，内部调用 `tcc.workloads.drbe.app.run_mvp()`，不再承载核心逻辑。

### 4.2 `tcc/core` 结构

```
tcc/core/
├── types.py                 # 共享类型：CandidatePlan/CostBreakdown/SolverDecision 等
├── rtc/                     # R/T/C 原语定义
├── config/                  # 配置加载与默认配置
├── l1/                      # L1：复合单元簇抽象（算粒/存粒/互连能力画像）
├── l2/                      # L2：液态拓扑（切页执行器 + 事件结构 + τ 指标钩子）
├── l3/                      # L3：决策框架（路径A规则调度为 baseline）
└── metrics/                 # 指标体系（含 τ_commit/τ_apply/τ_resume）
```

说明：
- `types.py`：跨层共享结构，确保 L3 输出可直接驱动 L2，且主流程可稳定序列化/打印。
- `l3/` 内部区分“候选生成、成本模型、求解入口”三块职责，但对外保持一个稳定入口（例如 `optimize()`）。
- `metrics/` 与 `l2/` 的关系：`l2` 生成结构化事件，`metrics` 负责记录、汇总、统计，为 L3 提供 `switch_stats` 输入。

### 4.3 `tcc/workloads` 结构

#### 4.3.1 DRBE

```
tcc/workloads/drbe/
├── app.py                   # DRBE MVP 编排入口：run_mvp()
├── pages/                   # FFTPage/DBFPage/PageManager 及 DRBE 页库
├── io/                      # IQ 回放等输入输出适配器
└── pipeline/                # FFT/DBF pipeline runtime（调用任务模板/算粒簇）
```

#### 4.3.2 推理（占位骨架）

```
tcc/workloads/infer/
├── app.py
├── pages/
└── pipeline/
```

说明：
- `infer` 本轮不实现功能，只建立目录与最小可 import 的骨架，避免后续加入推理时再次改造顶层结构。

## 5. 兼容与迁移策略

### 5.1 两阶段迁移（不中断可跑）

**阶段 1：建立产品化骨架 + 迁入 DRBE MVP 必需代码**
- 新增 `pyproject.toml`（或最小化配置文件）以支持 `src/` 布局的 import。
- 建立 `src/tcc/core` 与 `src/tcc/workloads/drbe` 目录与 `__init__.py`。
- 将当前 DRBE MVP 主链（IQ 回放、FFT/DBF pipeline、页管理、切页执行、指标、L3 baseline）按职责迁入新结构。
- 修改根 `main.py`：变成兼容入口，内部调用新子工程的 `run_mvp()`。
- 目标：迁移后 `python main.py` 仍可跑通，并输出同等或更丰富的结构化结果。

**阶段 2：旧结构进入 legacy 只读**
- 保留旧目录与旧文件用于对照与回溯，但明确规则：**后续所有新功能只进 `src/tcc`**。
- 如确有外部脚本依赖旧路径，可将旧模块改为薄转发（re-export），例如旧 `l3_solver/relaxation_solver.py` 只转调 `tcc.core.l3.*`，不再包含业务逻辑。
- 逐步将测试迁移到 `tests/` 下的新路径（围绕 `tcc`）。

### 5.2 Legacy 约束（硬规则）

- Legacy 目录（当前平铺模块）不再新增功能、不再扩展接口。
- 允许：
  - 修复阻塞性 bug（若影响 `main.py` 兼容）
  - 薄转发以保持兼容
  - 添加“弃用说明”与迁移提示

## 6. L3（路径 A）在新工程中的定位

### 6.1 L3 输入输出契约（核心稳定点）

L3 输出必须包含：
- `selected_page`
- `selected_clusters`
- `placement`
- `score`（总评分）
- `cost_breakdown`（至少：compute/route/io/reconfig/energy 五项）
- `reconfig_estimate`（`τ_commit/τ_apply/τ_resume` 的估计值）
- `reason`（可解释理由列表）

这样主流程可以做到：
- “为什么选这个页/映射/切换方案”
- “估计的重构代价是多少”
- “实际事件测得的 τ 指标是多少”
- “估计与实际偏差如何”

### 6.2 L3 内部职责拆分（可替换位）

L3 内部建议拆分为三类模块（文件名可在实施计划中细化）：
- 候选生成（规则）：生成 keep/switch/reuse_shared 三类候选方案
- 成本模型：对候选方案打分并输出分解
- 求解入口：枚举候选 → 打分 → 选择最优 → 组装 `SolverDecision`

后续升级路径 B（连续弛豫）时，仅替换“求解入口”的选择策略或新增一个 solver 实现，不改变上层接口与数据结构。

## 7. 配置与运行入口

### 7.1 配置来源

继续支持仓库现有 `config.yaml`，并在 `tcc/core/config` 中提供默认配置（用于未来拆分与复用）。优先级建议：

1. 显式传入配置路径
2. 仓库根 `config.yaml`
3. `tcc/core/config/default.yaml`

### 7.2 运行入口

至少支持两种：
- `python main.py`：兼容入口（默认运行 DRBE MVP）
- `python -m tcc`：产品化入口（后续扩展为选择不同 workload）

## 8. 测试与验收标准

### 8.1 最小验收标准（结构化后必须满足）

- `python -m pytest tests -v` 全绿（针对 `tcc` 新子工程）。
- `python main.py` 可跑通并输出：
  - L3 决策结构（含 `cost_breakdown`、`reconfig_estimate`、`reason`）
  - L2 切页事件结构（含 `τ_commit/τ_apply/τ_resume`）
  - FFT/DBF 结果形状或摘要（用于 sanity check）

### 8.2 推荐新增的关键测试（方向）

- `test_cost_model.py`：成本分解单调性与切页代价项存在性
- `test_mapping_solver.py`：候选方案生成与策略标记
- `test_l3_l2_integration.py`：L3 决策驱动 L2 切页事件且事件包含 τ 三元组
- `test_main_integration.py`：主流程返回/打印结构完整且可解释

## 9. 风险与对策

- **一次性迁移引入 import 混乱**：通过分阶段迁移、保持 `main.py` 兼容入口来降低风险；每迁一步跑核心集成测试。
- **workload 间耦合反弹**：通过硬规则（workload 只依赖 core）与目录结构约束，将耦合问题前置暴露。
- **推理加入时架构再次大改**：提前建立 `workloads/infer` 骨架与 core 抽象接口，后续仅新增推理簇/页/pipeline。



<!-- orphan-cleanup: no MOC found, tagged -->
