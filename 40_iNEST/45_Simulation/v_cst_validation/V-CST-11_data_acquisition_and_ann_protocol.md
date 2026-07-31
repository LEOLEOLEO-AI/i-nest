---
provenance: external
---

# V-CST-11 数据获取与 ANN 复算协议

**状态**：执行规范草案，2026-07-24  
**前置协议**：[V-CST-00](V-CST-00_protocol.md)  
**目标**：为不同物种与人工神经网络取得可复现的结构、动态和结构-功能耦合输入；不以论文摘要、二手汇总表或模型代理值冒充原始数据。

## 1. 先区分“论文结论”与“可计算数据”

顶刊论文优先用于三件事：确定数据集版本、定义分析协议、提供独立的比较结论。论文中报告的单个指标不能替代原始图、原始神经元时序或 ANN 激活日志。

| 证据等级 | 可用于 | 不可用于 |
|---|---|---|
| A：版本化原始结构+功能数据 | 完整 `Sc`、`Tc`、`Gamma_st` 和重复性 | 无 |
| B：原始结构，功能数据可公开取得但尚未完成 ID 映射 | `Sc`；`Tc/Gamma_st` 的待执行计划 | 完整 CST 结论 |
| C：同行评审论文报告的汇总量 | 独立标定、外部比较、先验范围 | 计算个体/模型的 CST |
| D：综述、手工表、代理数或随机仿真 | 假设生成、历史对照 | 生物或 ANN CST 验证 |

当前 `Simulation_Results/ann_data.csv` 和 `ann_real_results.json` 归为 **D**：包含手工/代理的 `Sc`、`Tc`、`Gamma_st`、`alpha`，没有冻结的权重文件、输入数据、激活日志和运行哈希。它们不得进入 V-CST 的统计检验。

## 2. CST V2.1 所需的最小数据合同

| 分量 | 最小原始输入 | 输出 | 不可接受替代 |
|---|---|---|---|
| `kappa_0` | 有向结构边、节点 ID | 有向 D-core/层级指标 | 无向化后未声明的图 |
| `kappa_1` | 有向边与权重/距离规则 | 有向路径效率 | 只引用论文平均路径长度 |
| `kappa_2` | 可重复结构图 | 固定分辨率和随机重启的 Louvain 模块度 | 连通分量或贪婪模块度代理 |
| `kappa_top` | 有向图/高阶关系 | 明确的有向循环或持久同调统计 | 人工指定常数 |
| `tau_0` | 节点×时间的原始活动矩阵 | DFA/Hurst 和记忆时间尺度 | 模型架构名称或参数量 |
| `tau_1` | 同一时序矩阵 | 跨节点 Hurst-复杂度同步 | 静态 FC 单值 |
| `tau_2` | 足够长的时序与采样率 | MFDFA 奇异谱宽度 | 单次相关系数 |
| `tau_top` | 阈值与 bin 规则已固定的事件/激活序列 | 雪崩幂律与替代分布比较 | 随机 avalanche 或仅线性拟合 R² |
| `Gamma_st` | 同 ID 的结构矩阵与功能/复杂度矩阵 | `NMI(M_struct,M_func_CS)*sign(Mantel_r_CS)` | 结构与功能来自不同对象/脑区的拼接 |
| `alpha` | 预先定义的节点可分辨状态数或器件测量 | 独立标定与不确定性 | 为使 CST 命中阈值而回填 |

## 3. 物种数据优先级与官方下载入口

所有下载文件都应放入未纳入 Git 的数据区，并配套一个 `.md` 元数据文件（数据集名、URL、版本、许可证、下载日期、SHA-256、对象、ID 映射覆盖率）。JSON/二进制数据本身不提交 Git。

| 优先级 | 物种/范围 | 结构数据入口 | 功能数据入口 | 可先完成的任务 | 主要限制 |
|---|---|---|---|---|---|
| P0 | *C. elegans* 全脑 | [WormWiring](https://www.wormwiring.org/), [Varshney 2011 DOI](https://doi.org/10.1371/journal.pcbi.1001066) | [Kato et al. 2015 DOI](https://doi.org/10.1016/j.cell.2015.09.034), [NeuroPAL 数据与资源](https://www.nature.com/articles/s41586-020-2975-2) | `V-CST-01`；拿到 ID 时序后 `02/03/05/10` | 结构与功能通常不是同一只动物；必须报告跨个体配准 |
| P1 | 斑马鱼幼体全脑 | [Zebrafish Brain Browser](https://zebrafishbrain.org/), [mapzebrain](https://mapzebrain.org/) | [Zebrafish Brain Browser](https://zebrafishbrain.org/), [Ahrens et al. Nature 2013 DOI](https://doi.org/10.1038/nature12166) | 功能 `Tc`、区域级 `Gamma_st`、状态对照 | 完整突触级结构与同一动物时序通常不同时具备 |
| P2 | 果蝇 | [FlyWire](https://flywire.ai/), [Hemibrain NeuPrint](https://neuprint.janelia.org/) | [Virtual Fly Brain](https://www.virtualflybrain.org/), [FlyLight](https://flweb.janelia.org/)；按实验检索原始钙成像 | `Sc`；匹配脑区后 `Tc/Gamma_st` | 成人全脑同步功能数据稀缺；不能把行为论文补成活动矩阵 |
| P3 | 小鼠 V1 局部皮层 | [MICrONS Explorer](https://www.microns-explorer.org/), [MICrONS NDA access](https://github.com/cajal/microns-nda-access) | [MICrONS Explorer](https://www.microns-explorer.org/), [Allen Brain Observatory](https://observatory.brain-map.org/visualcoding) | 局部 SC-FC、RG 粗粒化、交叉会话重复性 | MICrONS 为局部皮层而非全脑；原始数据体量大，先取已配对的边表和活动特征 |
| P4 | 小鼠全脑区域级 | [Allen Connectivity Atlas](https://connectivity.brain-map.org/), [Allen CCF](https://atlas.brain-map.org/) | [Allen Brain Observatory](https://observatory.brain-map.org/) | 区域级 `Sc/Tc` 与状态比较 | 注射追踪和钙成像对象不相同；需将推论写为群体/图谱级 |
| P5 | 人类区域级 | [HCP ConnectomeDB](https://www.humanconnectome.org/study/hcp-young-adult/data-releases), [HCP pipelines](https://github.com/Washington-University/HCPpipelines) | 同一 HCP release 的 rfMRI | 区域级 `Sc/Tc/Gamma_st`、重复性 | 不是单神经元；结构与功能应在同一被试、同一 atlas 上配对 |
| P6 | 猕猴区域级 | [PRIME-DE](https://fcon_1000.projects.nitrc.org/indi/PRIME/), [CoCoMac](https://cocomac.g-node.org/) | [PRIME-DE](https://fcon_1000.projects.nitrc.org/indi/PRIME/) | 区域级 SC-FC 与跨物种外推 | 追踪结构与 fMRI 常来自不同队列 |

### 3.1 P0 线虫的立即获取清单

1. 固定 `connectome_v8_data.json` 的 SHA-256，并补充其 Varshney/WormWiring 的版本来源与边类型解释。
2. 从 Kato 2015 的数据发布页、作者实验室或其关联数据仓库取得：`traces`、采样率、神经元 ID/NeuroPAL 映射、行为状态、去卷积/去趋势说明。
3. 只在 ID 映射覆盖预注册阈值后运行 V-CST-02/03。建议门槛为：结构图节点中至少 70% 可映射，且映射节点承载至少 70% 的化学边权；此为 **[待注册]** 方法门槛，不是生物学结论。
4. 若公开数据只有影像而无 ID，先完成图像分割、NeuroPAL 配准和人工抽样核验；未配准数据不能计算 `Gamma_st`。

## 4. 现有 ANN→CST 映射：已找到，但须版本化重建

历史映射位于：

- `50_Output/51_Papers/A1_CST_Theory_V31_ARS_REVISED.md` 的 Methods / UCCP；
- `20_Processing/_attachments_knowledge/.../Simulation_Results/ann_data.csv`；
- `20_Processing/_attachments_knowledge/.../Simulation_Results/ann_real_results.json`。

V31 的 ANN 数据提取思想为：

| V31 量 | 原定义 | 应从哪里实测 |
|---|---|---|
| `Sc` | 架构图的连通、层级/核心、Louvain 模块度、小世界 | checkpoint 配置 + `torch.fx`/模型图 + 参数张量形状 |
| `lambda_eff` | 层间活跃单元传播比 | 固定输入批次的逐层激活张量 |
| `Phi` | 跨层表示同步，ANN 用 CKA | 同一 token/样本、同一 checkpoint 的层表示 |
| `Psi` | 批间激活相关矩阵的时间/批次波动 | 固定数据集分块的多批次激活相关矩阵 |
| `Theta` | 层自相关衰减时间常数的熵 | 序列位置或任务流上的逐层激活时序 |
| `Gamma_st` | 结构社区与激活相关社区 NMI，乘结构/功能 Mantel 符号 | 架构图社区 + 激活 FC/复杂度图社区 |
| `alpha` | 二值数字 ANN 为 `ln(2)` 的旧假设 | 若保留，标记 `[推导/待验证]`；不能说是已实测节点状态数 |

### 4.1 与 CST V2.1 的兼容性门禁

V31 的 `Rsw/λeff/Φ/Ψ/Θ` 与 V2.1 的 `κ0/κ1/κ2/κtop/τ0/τ1/τ2/τtop` **不是同一公式**。因此：

- V31 只能作为“ANN 的结构图和激活日志如何取数”的历史方法；
- 新实验以 V2.1 输出为主，V31 输出仅作为探索性附录；
- `CKA` 可作为 ANN 的功能相似性矩阵候选，但必须明确它是 `M_func_CS` 的构造规则，不等同于生物 PLV；
- `tau_top` 不能从普通 Transformer 的单次前向自动声称为生物雪崩。应先作事件化规则、替代分布检验并以 `NOT_APPLICABLE` 作为允许结果；
- 数字 ANN 的 `alpha=ln(2)` 是设备层假设，不应根据 CST 阈值反推其正确性。对 GPU/TPU 推理，应另报告数值精度、量化位宽、激活离散化和训练/推理状态。

## 5. ANN 的可复算采集流程

### 5.1 首批模型：只选开放权重、可本地运行的模型

建议基准组：`ResNet-50`、`ViT-B/16`、`BERT-base`、`GPT-2 small`、`Mamba-130M`。每个模型建立一份实验清单：模型库版本、精确 revision/commit、权重 SHA-256、tokenizer/预处理版本、硬件、随机种子、数据集 revision、许可证。

| 步骤 | 数据产物 | V2.1 分量 |
|---|---|---|
| 导出模型图 | `nodes.parquet`、`edges.parquet`、有向权重/形状表 | `kappa_0/1/2/top` |
| 固定 3 个独立输入集和 3 个随机种子 | 输入清单与样本 ID | 重复性门禁 |
| 记录每层激活 | 分层张量摘要或分块存储的激活矩阵 | `tau_0/1/2`、功能图 |
| 构建功能复杂度图 | CKA、相关、Hurst/多分形、事件化图的定义和结果 | `Gamma_st`、`tau_top` |
| 构建结构社区 | 有向/加权图、Louvain 多重重启 | `kappa_2`、`Gamma_st` |
| 匹配结构与功能 | 相同节点集的社区标签与距离矩阵 | `Gamma_st` |
| 空模型 | 度/强度保持、层级保持、激活时间置换 | 所有主张的零假设 |

`节点` 的定义必须预注册：计算图算子、注意力头、MLP 通道、神经元，四种图不能混合比较。建议先按“注意力头/MLP block”建立宏观节点图，随后做通道级敏感性分析。

### 5.2 ANN 不能使用的捷径

- 只从 `config.json` 的层数、参数量估算 `Sc`；
- 仅用单条提示词、单批激活计算 `Tc`；
- 将训练轮数、token 数或损失曲线直接称为神经动力学；
- 以闭源模型排行榜/行为测试替代内部结构与激活数据；
- 用理论 `alpha` 调到目标 CST 阈值；
- 以同一模型产生的 benchmark 成绩作为独立“能力标签”。

## 6. 论文优先的参数补全原则

| 参数类别 | 优先文献/数据 | 用法 |
|---|---|---|
| 神经活动临界性/分支比 | [Beggs & Plenz 2003](https://doi.org/10.1523/JNEUROSCI.23-35-11167.2003), [Wilting & Priesemann 2018](https://doi.org/10.1038/s41467-018-04725-4) | 预注册雪崩与替代分布分析，不直接抄其数值 |
| SC-FC 对齐 | [Honey et al. 2009](https://doi.org/10.1073/pnas.0811168106), [Arnatkeviciute et al. 2022](https://doi.org/10.1038/s41467-022-30023-3) | 确定结构/功能矩阵对齐、空模型和跨尺度解释 |
| 线虫全脑时序 | [Kato et al. 2015](https://doi.org/10.1016/j.cell.2015.09.034), [Gordus et al. 2015](https://doi.org/10.1016/j.cell.2015.04.030) | 确定神经元 ID、行为状态和时间窗口；下载其原始或关联仓库数据 |
| ANN 表示相似性 | [Kornblith et al. 2019](https://doi.org/10.48550/arXiv.1905.00414), [Raghu et al. 2021](https://proceedings.mlr.press/v139/raghu21a.html) | 将 CKA 明确为功能图构造方法，而非 CST 已验证成分 |
| 多尺度神经动力学 | [Murray et al. 2014](https://doi.org/10.1038/nn.3862) | 时间常数的估计窗口、可靠性报告与区域差异参照 |

## 7. 执行顺序和交付物

1. **V-CST-12**：线虫数据登记与 ID 映射审计，输出 `dataset_manifest.md`、哈希、覆盖率和许可。
2. **V-CST-13**：线虫 V2.1 `Sc` 正式实现：有向图、Louvain、多重空模型、Bootstrap CI。
3. **V-CST-14**：线虫真实时序 `Tc`，包括 DFA/MFDFA/雪崩替代分布检验。
4. **V-CST-15**：线虫 `Gamma_st` 及错配/时间置换消融。
5. **V-CST-16**：ANN 开放权重遥测基准，先选一个 ResNet 和一个 GPT-2；只报告组件，不给智能等级标签。
6. **V-CST-17**：MICrONS 局部 SC-FC 与 RG 粗粒化。只有这一阶段完成，才讨论局部皮层和全脑尺度关系。
7. **V-CST-18**：跨物种预注册外推与竞争模型比较。

## 8. 当前判定

- `[实测]` 当前主库有可读线虫结构图和部分果蝇/猕猴结构文件。
- `[待测]` 线虫真实活动时序、ANN 权重与激活日志的 V2.1 计算。
- `[引用]` 顶刊论文可以给出方法依据和独立比较范围。
- `[仿真]` 历史 V9-V39 与 ANN 代理表可用于软件验证或假设生成，但不作为 CST 理论成立的证据。

