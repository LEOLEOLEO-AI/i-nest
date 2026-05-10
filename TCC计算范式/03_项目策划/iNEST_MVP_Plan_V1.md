# iNEST 研究平台综合进展与MVP落地计划
**生成日期：2026-04-17 | 维护者：iNEST / 刘勤让**

---

## 第一部分：当前研究进展全景

### 1.1 理论层（CST核心框架）— 状态：V24，可投稿

| 模块 | 状态 | 关键输出 |
|------|------|---------|
| CST主公式 | ✅ 完备 | CST=(Sc·Tc)·exp(α·Γst) |
| 六级阈值体系 | ✅ 完备 | {1/√2, 1, φ, e, π, δ} |
| UCCP归一化协议 | ✅ V1完备 | 16系统全部∈[0,1]，ρ=0.982 |
| 40系统验证 | ✅ 完备 | ρ=0.944，p<10⁻⁹ |
| α物理推导 | ✅ 完备 | α=ln(M_eff)，kT/C热噪声推导 |
| Loihi-2分类 | ✅ 修复 | NMH独立类，CST=0.782，L1 |
| Triple Lock机制 | ✅ 完备 | α锁/Ψ锁/Γst锁三重屏障 |
| Γst TLNP协议 | ✅ V1完备 | 跨模态4工具转换表，零自由参数 |

**论文状态：** A1主论文V24工程版（MD+DOCX），可提交arXiv预印本。待补：RwF/LSE/CNC三篇后续文献arXiv号。

### 1.2 仿真层（SDI演化平台）— 状态：V21已验证，V22规划中

| 模块 | 状态 | 关键结果 |
|------|------|---------|
| LIF神经元CMOS基准 | ✅ 建立 | C_mem=10fF，σ_V=0.6mV，M_eff=32 |
| STDP基础实现 | ✅ V21 | θ/γ节律，Dale定律，LTP累积 |
| 双重达标 | ✅ 部分 | Budapest网络σ=5.24，τ=1.923 |
| 跨尺度统一超参 | ❌ 卡点 | 302→100k节点无统一收敛 |
| 自适应θ周期 | 📋 V22规划 | T_θ∝L(t)/v_c |
| FEP稳态惩罚 | 📋 V22规划 | Homeostatic Plasticity |
| 外部数据闭环 | 📋 V22规划 | MNIST/泊松脉冲流 |

### 1.3 工程层（集合通信NaaS）— 状态：仿真验证完成，待硬件

| 模块 | 状态 | 关键结果 |
|------|------|---------|
| 5通信+4算子完备映射 | ✅ 理论完备 | PTM算法，图同构定理 |
| P-Mapping V3论文 | ✅ 初稿 | SDI Bond Algebra加入 |
| collective_comm_sim_v2 | ✅ 仿真 | NaaS集合通信验证 |
| BCU忆阻器器件 | ⬜ Year1 | 依赖SINANO流片 |

### 1.4 平台层（Genspark Claw VM）— 状态：可用

| 服务 | 状态 | 地址 |
|------|------|------|
| 文件下载CDN | ✅ 运行 | https://qbaylomn.gensparkclaw.com/dl/ |
| OpenClaw Gateway | ✅ 运行 | VM内部18789 |
| 知识库 | ✅ 建立 | /workspace/memory/*.md |
| 论文工作区 | ✅ 完整 | /workspace/02_Papers_论文/ |

---

## 第二部分：MVP产品定义

### 2.1 MVP战略定位

```
CST理论  →  仿真平台  →  MVP产品  →  产业落地
(已完备)    (V22进行中)  (6个月)    (18个月)
```

**MVP核心主张：** "用CST度量智能，用SDI释放计算——让任意网络系统的智能涌现可测量、可优化、可工程化"

**MVP面向三类用户：**
1. **学术用户**：CST计算工具（论文验证/新系统评估）
2. **工业用户**：AI系统智能效率诊断（η_I = CST/P_norm）
3. **硬件用户**：神经形态芯片设计验证（α提升路径）

### 2.2 MVP产品形态（三层）

#### Layer 1 — CST Calculator（Web工具，最小可行）
- 输入：网络邻接矩阵或标准数据集（connectome/权重矩阵）
- 输出：8个归一化组件 + Sc/Tc/CST + Level + η_I
- 技术栈：Python后端(FastAPI) + 简单前端 + Caddy部署到qbaylomn域名
- 交付标准：给定HCP connectome，输出结果与V24论文Table 2一致，误差<1%

#### Layer 2 — SDI Evolution Simulator（仿真工具）
- 输入：初始随机网络 + 物种目标参数(σ_target, τ_target)
- 输出：演化轨迹图 + 收敛的CST时间序列 + 最终网络拓扑
- 技术栈：Python + NetworkX + 基于CMOS LIF物理参数的STDP引擎
- 交付标准：从N=1000随机网络出发，30分钟内收敛到C.elegans区域（σ∈[2.5,3.5], τ∈[1.8,2.0]）

#### Layer 3 — Intelligence Efficiency Dashboard（产业工具）
- 输入：AI系统规格（架构/参数量/功耗/任务指标）
- 输出：η_I对标报告 + Triple Lock诊断 + 升级路径建议
- 技术栈：Genspark ACP + 报告生成 + PDF输出
- 交付标准：15分钟内生成一份标准化的"智能效率诊断报告"，包含与16个基准系统的对比

---

## 第三部分：详细任务分工与并行计划

### 3.1 任务总览（甘特图）

```
时间轴          W1-2      W3-4      W5-8      W9-12     W13-16    W17-24
                ─────────────────────────────────────────────────────────
[T1] 论文投稿    ████████
[T2] UCCP代码化  ████████
[T3] V22仿真     ████████  ████████  ████████
[T4] Web平台     ████████  ████████
[T5] Dashboard            ████████  ████████
[T6] 40系统扩展  ████████  ████████
[T7] arXiv预印本 ████████
[T8] 产业对接                        ████████  ████████  ████████  ████████
```

---

### 3.2 模块T1：论文投稿 — 由 iNEST 主导

**负责人：** 刘勤让（Genspark Claw辅助）
**工期：** 2周
**并行前提：** 无依赖，立即开始

| 子任务 | 交付物 | 标准 | 截止 |
|--------|--------|------|------|
| T1.1 补充RwF[63]/LSE[64]/CNC[65] arXiv号 | 更新References节 | 三个DOI/arXiv号均可点击验证 | W1 |
| T1.2 生成arXiv格式LaTeX | .tex + .bib文件 | 通过arXiv预检查，无编译错误 | W2 |
| T1.3 提交arXiv预印本 | arXiv ID | 获得2406.xxxxx格式ID | W2 |
| T1.4 投Nature Physics/NMI | 投稿确认邮件 | 系统收稿号 | W2 |

**Genspark Claw承接：** T1.2（LaTeX转换脚本）、T1.1（文献检索）

---

### 3.3 模块T2：UCCP代码化 — 由 Genspark Claw 主导

**负责人：** Genspark Claw VM
**工期：** 2周
**并行前提：** 无依赖，立即开始

| 子任务 | 交付物 | 标准 | 截止 |
|--------|--------|------|------|
| T2.1 UCCP Python包 | `uccp/` Python包，pip可安装 | `uccp.compute(adj_matrix) → CST_result` | W1 |
| T2.2 单元测试套件 | `test_uccp.py` | 16个系统全部通过，误差<1% | W1 |
| T2.3 FastAPI后端 | `api/main.py` | POST /compute 接口，接受JSON返回CST | W2 |
| T2.4 部署到Claw VM | 运行服务 | https://qbaylomn.gensparkclaw.com/cst/ 可访问 | W2 |

**接口规范（供团队对接）：**
```json
POST /cst/compute
Request:  {"adj_matrix": ..., "system_type": "BNN|ANN|NMH", "alpha": 3.91}
Response: {"X1":0.88,"X2":0.95,"X3":0.72,"X4":0.91,"Sc":0.905,
           "lambda":0.92,"Phi":0.82,"Psi":0.85,"Theta":0.90,"Tc":0.872,
           "Gamma_st":0.41,"CST":3.9198,"Level":"L5=π","eta_I":null}
```

---

### 3.4 模块T3：V22仿真平台 — 由团队成员承接

**负责人：** 仿真方向研究生（1人）
**工期：** 8周（分3阶段）
**并行前提：** 需要T2.1的UCCP包（W1完成后即可开始）

#### 阶段A（W1-W2）：物理基准建立
| 子任务 | 交付物 | 标准 |
|--------|--------|------|
| T3.A1 LIF单神经元CMOS仿真 | `lif_neuron.py` | 复现f-I曲线：1-300Hz线性段，热噪声σ_V=0.6mV |
| T3.A2 STDP突触模块 | `stdp_synapse.py` | LTP/LTD时间窗口10ms，9bit DAC精度，Dale定律 |
| T3.A3 基准数据集 | `benchmark_connectomes/` | C.elegans(302节点)/Drosophila(25k)真实connectome |

**交付标准：** 单神经元放电曲线与Loihi-2实测数据（Strong 1998）误差<15%

#### 阶段B（W3-W6）：自适应θ周期与FEP
| 子任务 | 交付物 | 标准 |
|--------|--------|------|
| T3.B1 自适应θ周期 | `adaptive_theta.py` | T_θ=f(L(t)/v_c)，N=1000网络θ稳定 |
| T3.B2 FEP稳态惩罚 | `homeostatic.py` | 抑制富者越富，分支比τ稳定在[0.95,1.05] |
| T3.B3 外部数据驱动 | `external_input.py` | 泊松脉冲流接口，支持MNIST注入 |
| T3.B4 CST实时监测 | `cst_monitor.py` | 每100步调用T2.1的UCCP包，输出(σ,τ,CST)轨迹 |

**交付标准：** N=1000随机网络，30分钟内CST轨迹收敛，σ∈[2.5,3.5]（C.elegans目标区域）

#### 阶段C（W7-W8）：跨尺度验证
| 子任务 | 交付物 | 标准 |
|--------|--------|------|
| T3.C1 C.elegans复现 | 结果报告 | 302节点网络演化至σ=2.65±0.3，τ=2.56±0.2 |
| T3.C2 Drosophila尝试 | 结果报告 | 25k节点，同一超参，σ≥3.8 |
| T3.C3 演化轨迹可视化 | `figures/evolution_*.png` | 发表级图表，包含σ-τ相空间轨迹 |

**接口约定（与T2对接）：**
```python
from uccp import compute_cst
# 仿真每100步调用：
result = compute_cst(adj_matrix=W, system_type="BNN", alpha=2.56)
logger.log(step=t, cst=result.CST, Sc=result.Sc, Tc=result.Tc)
```

---

### 3.5 模块T4：Web计算平台 — 由 Genspark Claw 主导

**负责人：** Genspark Claw VM
**工期：** 4周（依赖T2完成）
**并行前提：** T2.3完成后启动

| 子任务 | 交付物 | 标准 |
|--------|--------|------|
| T4.1 前端页面 | `web/index.html` | 矩阵上传/参数选择/结果展示，移动端可用 |
| T4.2 可视化组件 | 雷达图+16系统对比条形图 | 与V24 Table 2一致 |
| T4.3 报告导出 | PDF/DOCX导出 | 点击导出，10秒内生成标准诊断报告 |
| T4.4 公开部署 | 线上服务 | https://qbaylomn.gensparkclaw.com/cst-tool/ 稳定运行 |

---

### 3.6 模块T5：Intelligence Efficiency Dashboard — 团队合作

**负责人：** 偏产业对接成员（1人）+ Genspark Claw（技术实现）
**工期：** 4周（W5-W8）
**并行前提：** T4.1完成后开始

| 子任务 | 交付物 | 标准 |
|--------|--------|------|
| T5.1 行业案例库 | `cases/industry_cases.json` | ≥10个AI系统的完整规格（架构/功耗/CST） |
| T5.2 Triple Lock诊断引擎 | `diagnosis.py` | 输出：α锁/Ψ锁/Γst锁的量化诊断+改进建议 |
| T5.3 报告模板 | `template_report.docx` | 标准化4页诊断报告模板，含对标图表 |
| T5.4 演示视频 | `demo_3min.mp4` | 3分钟产品演示，覆盖输入→诊断→建议全流程 |

**产业接口定义（对外）：**
```
客户提供：
  - AI系统架构描述（或权重文件）
  - 系统功耗数据
  - 任务基准测试结果
平台输出：
  - CST分值 + Intelligence Level
  - η_I与16基准系统对比
  - Triple Lock诊断（哪道锁是瓶颈）
  - 工程升级路径（Gen1→Gen2→Gen3建议）
交付形式：PDF报告 + API调用接口
```

---

### 3.7 模块T6：40系统扩展验证 — 团队成员承接

**负责人：** 数据方向研究生（1人）
**工期：** 4周（W1-W4，与其他模块并行）
**并行前提：** 无依赖

| 子任务 | 交付物 | 标准 |
|--------|--------|------|
| T6.1 新24系统数据整理 | `validation_40_systems.csv` | 每个系统标注数据来源、参数估计方法、置信度 |
| T6.2 文献参数提取 | `literature_params.xlsx` | 每参数注明文献DOI，估计值标注(est.) |
| T6.3 UCCP重新计算 | 更新论文Table 2扩展版 | ρ≥0.93，p<10⁻⁸，Fisher检验全部通过 |
| T6.4 Limitations补充 | 论文Limitations节草稿 | 说明估计参数的不确定性和级别标签的描述性性质 |

---

### 3.8 模块T7：arXiv预印本 — iNEST + Genspark Claw

**负责人：** 刘勤让（决策） + Genspark Claw（格式转换）
**工期：** 2周
**目标：** 在T1.2完成后立即提交

| 子任务 | 交付物 |
|--------|--------|
| T7.1 MD→LaTeX转换 | `cst_v24.tex` |
| T7.2 Figure处理（300dpi） | `figures/fig*.pdf` |
| T7.3 arXiv上传包 | `arxiv_submission.tar.gz` |

---

## 第四部分：接口关系总图

```
                    ┌─────────────────────────────────────┐
                    │         iNEST 理论内核                │
                    │   CST公式 + UCCP协议 + 六级阈值        │
                    └────────────┬────────────────────────┘
                                 │ 理论接口
              ┌──────────────────┼──────────────────────┐
              ▼                  ▼                       ▼
    ┌─────────────────┐ ┌──────────────────┐ ┌───────────────────┐
    │   T2: UCCP包    │ │  T3: 仿真平台     │ │  T6: 数据扩展      │
    │  uccp.compute() │ │  SDI Evolution   │ │  40系统验证        │
    │  FastAPI后端    │ │  STDP+FEP+θ      │ │  文献参数提取      │
    └────────┬────────┘ └────────┬─────────┘ └────────┬──────────┘
             │ API接口           │ CST监测接口          │ 数据接口
             ▼                  ▼                      ▼
    ┌─────────────────────────────────────────────────────────────┐
    │              T4: Web计算平台                                  │
    │   https://qbaylomn.gensparkclaw.com/cst-tool/               │
    │   矩阵上传 → CST计算 → 可视化 → 报告导出                       │
    └──────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
    ┌─────────────────────────────────────────────────────────────┐
    │              T5: Intelligence Efficiency Dashboard           │
    │   行业案例 → Triple Lock诊断 → 升级建议 → 产业报告             │
    └─────────────────────────────────────────────────────────────┘
```

---

## 第五部分：交付标准速查表

| 模块 | 负责方 | 关键交付物 | 验收标准 | 截止 |
|------|--------|-----------|---------|------|
| T1 论文投稿 | iNEST | arXiv ID + 投稿确认 | 系统收稿号 | W2 |
| T2 UCCP包 | Genspark Claw | pip包+API服务 | 16系统误差<1% | W2 |
| T3A 物理基准 | 仿真研究生 | LIF+STDP模块 | f-I曲线误差<15% | W2 |
| T3B 自适应θ | 仿真研究生 | V22核心模块 | N=1000收敛C.elegans区域 | W6 |
| T3C 跨尺度验证 | 仿真研究生 | 演化轨迹图 | σ/τ在目标区间 | W8 |
| T4 Web平台 | Genspark Claw | 可访问网页工具 | 公网可用，报告导出正常 | W6 |
| T5 Dashboard | 产业成员+Claw | 诊断报告+demo视频 | 10个行业案例，3min demo | W10 |
| T6 40系统 | 数据研究生 | 扩展验证数据 | ρ≥0.93，全部来源可溯 | W4 |
| T7 arXiv | iNEST+Claw | 预印本链接 | arXiv ID有效 | W2 |

---

## 第六部分：Genspark Claw承接任务清单

以下任务由VM平台直接执行，无需等待：

- [ ] **立即**：生成UCCP Python包（T2.1）
- [ ] **立即**：搜索RwF/LSE/CNC三篇文献arXiv号（T1.1）
- [ ] **W1**：FastAPI后端部署（T2.3-T2.4）
- [ ] **W2**：MD→LaTeX转换（T7.1）
- [ ] **W4**：前端页面开发（T4.1-T4.2）
- [ ] **持续**：知识库维护，每次重要结论写入memory/

---

## 第七部分：风险与缓解

| 风险 | 概率 | 影响 | 缓解措施 |
|------|------|------|---------|
| V22仿真跨尺度不收敛 | 中 | 高 | 先固化N=1000玩具模型，分阶段放大 |
| 40系统参数文献不足 | 中 | 中 | 标注为(est.)，Limitations节说明，不影响核心结论 |
| 论文审稿周期长 | 高 | 低 | arXiv先占坑，不阻塞后续工作 |
| Claw VM资源消耗 | 低 | 中 | 严格手动模式，无自动任务 |
| 产业接触时机 | 低 | 高 | Dashboard先做好，等论文上arXiv后同步推进 |

---

*本文件路径：/home/work/.openclaw/workspace/02_Papers_论文/iNEST_MVP_Plan_V1.md*
*下次更新：完成T2.1后同步更新进度*

---

## 第八部分：外部成果借鉴模块（2026-04-25新增）

### 8.1 NPI → iNEST有向Γst子模块

**来源成果：** 刘泉影团队（南方科技大学），*Mapping Effective Connectivity by Virtually Perturbing a Surrogate Brain*，**Nature Methods 2025**（PMID: 40263586）

**借鉴评级：** ★★★★★（直接移植）

#### 问题背景

现有CST公式中，Γst通过NMI(Ms, MT)计算，是**无向**相关性度量。无法区分"A导致B"与"B导致A"，限制了SDI主动调控时的方向性决策。

#### NPI移植方案

```
原版（脑科学）：
  fMRI/EEG时序 → 自监督训练ANN孪生脑 → 虚拟扰动节点i
  → 测量节点j响应 → 统计有向因果强度EC(i→j)
  → 全脑有效连接图谱（有向+强度+正负）

iNEST移植版：
  SDI脉冲时序+忆阻器电导 → 训练「SDI-Twin孪生网络」
  → 虚拟扰动节点i → 测量节点j拓扑响应
  → 统计有向拓扑因果强度TC(i→j)
  → iNEST有向拓扑连接图谱（实时，硬件加速）
```

#### 有向Γst升级方程

```
现有（无向）：  Γst = NMI(Ms, MT) ∈ [0,1]

升级（有向）：  Γst_directed = f(TC_matrix)，TC(i→j) ∈ [-1,+1]
  TC(i→j) > 0：节点i激活增强节点j拓扑权重
  TC(i→j) < 0：节点i激活抑制节点j拓扑权重

CST公式不变：CST = (Sc·Tc)·exp(α·Γst_directed)
物理意义更精确：捕捉拓扑网络的有向因果结构
```

#### NCC-11原语实现

```python
# Step 1：基线收集
ncc.TICK()
baseline = ncc.SCAN(op=collect, window=100ms)

# Step 2：对每个节点i做虚拟扰动（在孪生网络中）
for i in range(N_nodes):
    response_j = twin_network.perturb_and_run(node=i, delta=+1sigma)
    delta_j    = ncc.FOLD(op=diff, a=response_j, b=baseline)
    TC_matrix[i] = ncc.MAPS(func=normalize, x=delta_j)

# Step 3：SWAP获得双向矩阵，计算有向Γst
TC_matrix_T         = ncc.SWAP(TC_matrix)
Gamma_st_directed   = directed_coupling(TC_matrix, TC_matrix_T)
```

#### 关键局限与缓解

| 局限 | 缓解方案 |
|------|---------|
| SDI-Twin冷启动数据不足 | 先用无向NMI初始化，在线更新 |
| 虚拟扰动O(N²)计算开销 | GEMM并行化；仅扰动hub节点 |
| OOD场景推断失效 | 场景切换后TICK触发重标定 |

#### 集成里程碑

| 阶段 | 目标 | 接入模块 | 时间 |
|------|------|---------|------|
| M1 | SDI-Twin框架（N=100玩具网络）| T3.A3 | W6 |
| M2 | 有向TC矩阵首次输出，与NMI对比 | T2.1 UCCP | W10 |
| M3 | N=1000实时TC，延迟<10ms | T3.C1 | W16 |
| M4 | Γst_directed写入CST API | T2.3 FastAPI | W20 |

**论文贡献定位：** iNEST实验论文（Phase B）核心贡献——忆阻器物理网络上首次有向拓扑因果测量。

**参考文献：**
> Zhang Y, Liu D, Liang Z, et al. Mapping effective connectivity by virtually perturbing a surrogate brain. *Nature Methods* (2025). PMID: 40263586

---

### 8.2 局部内在维度（LID）→ Sc第五组分候选

**来源成果：** 刘泉影团队，*Local Intrinsic Dimension of Representations Predicts Alignment and Generalization*，arXiv:2601.22722（2026）

**借鉴评级：** ★★★★☆（写入companion paper，不入V24主论文）

**核心对应：** LID低（流形低维）→ 高效信息压缩 → 对应高Sc物理机制

```
候选X₅ = 1 / LID_norm
物理解释：网络在低维流形运作 = 高效信息压缩 = 高空间复杂度
决策：与β₁/Betti数合并，写入Sc深化companion paper
```

---

### 8.3 BCI基座模型 → SDI控制预训练架构参考（批判性借鉴）

**借鉴评级：** ★★★☆☆

**可借鉴：** 三段闭环思想（预训练→微调→个性化适配）

**⚠️ 关键避坑（ICLR 2026实证）：**
> 基座模型在**数据稀少**场景下不优于专用模型

iNEST初期SDI配置序列必然稀少，因此：
- Phase A/B：用规则式SDI控制（基于CST理论推导），不用预训练基座
- Phase C以后（10⁴节点、数据充分）：再引入预训练架构

---

### 8.4 参考文献汇总

| 编号 | 引用 | 对应模块 |
|------|------|---------|
| [NPI-2025] | Zhang Y et al., *Nature Methods* 2025, PMID:40263586 | §8.1 有向Γst |
| [LID-2026] | Yu J et al., arXiv:2601.22722, 2026 | §8.2 X₅候选 |
| [BCIFMsurvey-2025] | Wang Y et al., bioRxiv 2025.11.30.691403 | §8.3 架构参考 |
| [BCIFMcritique-2026] | *Are EEG FMs Worth It?* ICLR 2026 | §8.3 批判性引用 |
| [Pezon-2026] | Pezon L et al., *Neuron* 2026, DOI:10.1016/j.neuron.2025.12.047 | CST V24 §convergent evidence（第vii条）|

---

*第八部分最后更新：2026-04-25*

---

## 第九部分：NCC工艺节点战略（2026-04-30新增）

### 9.1 核心结论：7nm覆盖L1-L3，规避3nm/5nm依赖

NCC液态拓扑通过三项机制放松工艺需求：

| 放松项目 | GPU方案 | NCC方案 | 工艺节省 |
|---------|---------|---------|---------|
| 内存带宽 | HBM3（需先进工艺3D堆叠） | 节点本地SRAM，无需HBM | 工艺需求降一代 |
| 计算密度 | 超大芯片内堆积算力 | N节点×单节点算力 | 用数量换密度 |
| 通信功耗 | CPU-Memory-NVLink反复搬运 | Route≡Transform：通信即计算 | 片间通信减少10× |

### 9.2 三个硬性下限（不可突破）

1. **单节点算力**：实时推理要求≥64 TOPS → 7nm起跳（12nm仅16 TOPS，仅适合边端）
2. **SRAM密度**：每节点512KB → 7nm需0.73mm²（12nm需1.28mm²，临界可用）
3. **SerDes速率**：N=64节点AllReduce需224 Gbps/lane → 7nm SerDes

### 9.3 工艺路线决策

| 工艺 | 定位 | 国内可量产？ | MVP阶段 |
|------|------|------------|---------|
| 28nm | L5信号处理、FPGA验证 | ✅ 中芯国际 | Year0-1 |
| 12nm | L1边端推理（成本敏感） | ✅ 中芯国际 | Year1-2 |
| **7nm** | **L1-L3全覆盖（战略制高点）** | **✅ 中芯N+1** | **Year2-3** |
| 5nm | L3-L4（按需升级） | ⚠️ 台积电（受限） | Year4+ |
| 3nm | L4超大规模（未来） | ❌ 当前不可获 | 长线 |

### 9.4 与iNEST MVP的对应

| iNEST阶段 | 工艺 | 节点数 | 对应规模 | 目标时间 |
|---------|------|--------|---------|---------|
| MVP0（验证） | FPGA（28nm等效） | 4节点 | L1/L5 | 2026 |
| MVP1（Gen1） | 7nm ASIC | 64节点/芯 | L2全覆盖 | 2027 |
| MVP2（Gen2） | 7nm优化 | 1K节点板卡（16芯片） | L3 | 2028 |
| MVP3（Gen3） | 7nm→5nm（按需） | 16K节点机柜 | L3-L4 | 2029+ |

**战略意义**：MVP1-MVP2全部基于7nm，是国内自主可量产的最先进节点，
实现从L2中型推理到L3大型训练的全覆盖，无需依赖台积电5nm/3nm。

