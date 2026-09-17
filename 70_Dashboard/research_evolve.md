# 科研自进化闭环报告

> 第 **1** 轮 · 2026-09-18 00:13 · 由 `research_evolve.evolve` 生成（每次运行一轮，一轮一次提交）

## 一、闭环四数（判定"进化"还是"空转"的唯一依据）

| 指标 | 本轮 | 上轮 | Δ | 含义 |
|---|---|---|---|---|
| 新增候选 opened | 138 | — | — | 本轮新进来的问题 |
| 关闭候选 closed | 5 | — | — | **已给出裁决并出队** |
| 升级 escalated | 56 | — | — | 久挂未裁决，需拍板 |
| 门禁违规 | 0 | — | — | 引用/证据标签/正本改动 |
| 当前 open 总数 | 133 | — | — | 待办池水位 |

> ✅ 本轮关闭 **5** 条，构成一次真正的进化轮（进化 = 变异 + **选择** + 留存；旧系统只有变异与留存）。

## 二、冻结守卫（无新论文则不许长概念）

- 近 **2** 天新来源材料：**15** 篇 （00_Inbox=15, 20_Processing=0, raw=0）
- 判定：**允许增量编译**
- 依据：有新来源 15 篇，允许增量编译
- 状态文件：`90_System/research_evolve/state/freeze.json`

## 三、待您裁决（7 条，最高优先在前）

### C-00005 · 🔺升级 score=0.884 · hypothesis · 挂起 25 天 · 见 1 次

**H5: TCC×iNEST: SDI软件定义互连可实现类突触可塑性拓扑重构**

- 详情：理由: 将STDP权重更新规则映射到NoC路由表更新，实现互连拓扑按负载自适应调整 | 验证方法: 在sdi_network仿真框架中对比固定拓扑vs可塑拓扑的吞吐/延迟 | 来源桥: SDI_Plastic_Interconnect
- 来源：`99_Meta/hypothesis_registry.json`
- 框架契合: 命中 6 个词表项 ['TCC', '拓扑重构', '软件定义互连', 'SDI']
- 可验证性: 有验证方法且含判据词 ['对比', '仿真', '验证']
- 证据就绪: 有来源/证据字段
- 裁决：`python -m research_evolve.evolve --decide C-00005 accepted|rejected|deferred "理由"`

### C-00007 · 🔺升级 score=0.8806 · hypothesis · 挂起 25 天 · 见 1 次

**H7: TCC×iNEST: NoC路由算法为事件驱动spike包重设计可降低延迟一个数量级**

- 详情：理由: spike稀疏性+异步性使传统同步流水线浪费严重，event-driven路由可大幅提升效率 | 验证方法: 在仿真中实现async路由协议，对比packet latency分布 | 来源桥: NoC_Spiking_Routing
- 来源：`99_Meta/hypothesis_registry.json`
- 框架契合: 命中 3 个词表项 ['TCC', 'NoC', 'iNEST']
- 可验证性: 有验证方法且含判据词 ['对比', '仿真', '验证']
- 证据就绪: 有来源/证据字段
- 裁决：`python -m research_evolve.evolve --decide C-00007 accepted|rejected|deferred "理由"`

### C-00117 · 🔺升级 score=0.8806 · idea · 挂起 23 天 · 见 1 次

**MTIA 300将通信拓扑提升为一等计算资源：计算/通信双平面分离+近内存归约，让通信不打断计算，实现3.9倍通信性能提升，印证拓扑本身是计算能力维度，而非开销。**

- 详情：在晶圆级SDSoW上增设独立的集合通信物理平面：边缘布置通信引擎（ME）近HBM，将AllReduce/归约下沉到内存旁路；NoC采用双平面路由，使计算流与通信流完全重叠，可扩展至百万神经元实时仿真。 | [ ] 设计TCC晶圆级双平面NoC仿真，对比单平面Mesh的AllReduce延迟与计算吞吐。
- 来源：`60_MOC/灵感卡片/20260826_MTIA300_communication_offloading_TCC_insights.md`
- 框架契合: 命中 3 个词表项 ['TCC', 'SDSoW', 'NoC']
- 可验证性: 有验证方法且含判据词 ['对比', '仿真']
- 证据就绪: 有来源/证据字段
- 裁决：`python -m research_evolve.evolve --decide C-00117 accepted|rejected|deferred "理由"`

### C-00010 · 🔺升级 score=0.8806 · hypothesis · 挂起 20 天 · 见 1 次

**H10: TCC×iNEST: 脑连接组拓扑模式可启发晶圆级NoC最优拓扑设计**

- 详情：理由: 大脑的小世界/模块化拓扑是亿年优化的结果，直接移植到芯片设计 | 验证方法: 用连接组数据生成NoC拓扑，vs mesh/torus对比性能 | 来源桥: Topology_Brain_Connectome
- 来源：`99_Meta/hypothesis_registry.json`
- 框架契合: 命中 3 个词表项 ['TCC', 'NoC', 'iNEST']
- 可验证性: 有验证方法且含判据词 ['对比', '验证']
- 证据就绪: 有来源/证据字段
- 裁决：`python -m research_evolve.evolve --decide C-00010 accepted|rejected|deferred "理由"`

### C-00109 · 🔺升级 score=0.8806 · idea · 挂起 19 天 · 见 1 次

**网络局部motif结构（如三节点连接模式）直接决定全局动力学稳定性与任务适配性，说明拓扑本身即计算资源，而非仅参数规模。**

- 详情：设计SDI动态motif重配置实验：在晶圆级NoC上在线切换Level1/Level3 motif富集区域，验证同一硬件在不同任务下通过拓扑重构获得性能提升。 | [ ] 构建NoC仿真器，比较静态拓扑与动态motif重配置在噪声识别和连续控制任务上的增益。
- 来源：`60_MOC/灵感卡片/20260829_TCC_iNEST_Systematic_Evidence_Review.md`
- 框架契合: 命中 3 个词表项 ['拓扑重构', 'SDI', 'NoC']
- 可验证性: 有验证方法且含判据词 ['仿真', '实验', '验证']
- 证据就绪: 有来源/证据字段
- 裁决：`python -m research_evolve.evolve --decide C-00109 accepted|rejected|deferred "理由"`

### C-00106 · 🔺升级 score=0.8806 · idea · 挂起 19 天 · 见 1 次

**Hala Point通过1152颗Loihi 2芯片集成11.5亿神经元，验证了多芯片异步SNN系统可扩展性，且能效优于数据中心AI加速器，但尚未达到单die晶圆级集成。**

- 详情：借鉴Loihi的片上学习引擎和事件驱动通信，在TCC的SDSoW中设计Spike流感知的NoC路由，并用忆阻器crossbar替代数字突触，实现晶圆级SNN存算一体加速，可测试MNIST能效。 | [ ] 调研Loihi 2和Lava架构，对比SDSoW的NoC设计，制定SNN加速器原型方案。
- 来源：`60_MOC/灵感卡片/20260830_Hala_Point：英特尔打造全球最大“类脑”计算系统.md`
- 框架契合: 命中 3 个词表项 ['TCC', 'SDSoW', 'NoC']
- 可验证性: 有验证方法且含判据词 ['对比', '验证']
- 证据就绪: 有来源/证据字段
- 裁决：`python -m research_evolve.evolve --decide C-00106 accepted|rejected|deferred "理由"`

### C-00100 · 🔺升级 score=0.8806 · idea · 挂起 18 天 · 见 1 次

**三个元拓扑(P2/星/环)与五种SDI-bond操作构成完备生成集，可产生所有通信原语拓扑并分形扩展；最优拓扑满足最小作用量变分原理。**

- 详情：以六种通信原语的流量模式为约束，用SDI-bond图代数搜索最小化网络作用量的晶圆级NoC拓扑，并在Mesh/环/树/星拓扑上对比延迟与能耗。 | [ ] 实现SDI-bond图代数库，枚举三基元组合生成六种通信原语拓扑，验证完备性。
- 来源：`60_MOC/灵感卡片/20260831_P-Theory_v2_MetaTopology_SDI_Bond_Draft.md`
- 框架契合: 命中 3 个词表项 ['元拓扑', 'SDI', 'NoC']
- 可验证性: 有验证方法且含判据词 ['对比', '验证']
- 证据就绪: 有来源/证据字段
- 裁决：`python -m research_evolve.evolve --decide C-00100 accepted|rejected|deferred "理由"`

## 四、本轮关闭 5 条（含原因，永不复活）

- `C-00133` **跨域桥 Chiplet_Heterogeneous_Neuromorphic** → **rejected**（跨域桥 Strength 疑为字母序伪相关且得分过低，判为生成器噪声）
- `C-00135` **跨域桥 WaferScale_Neuromorphic** → **rejected**（跨域桥 Strength 疑为字母序伪相关且得分过低，判为生成器噪声）
- `C-00136` **跨域桥 3DIC_Neural_Stacking** → **rejected**（跨域桥 Strength 疑为字母序伪相关且得分过低，判为生成器噪声）
- `C-00137` **跨域桥 Topology_Brain_Connectome** → **rejected**（跨域桥 Strength 疑为字母序伪相关且得分过低，判为生成器噪声）
- `C-00138` **跨域桥 Memory_Wall_Neuromorphic_Solution** → **rejected**（跨域桥 Strength 疑为字母序伪相关且得分过低，判为生成器噪声）

## 五、门禁（新增违规 0 · 存量债 942 · 本轮消除 0）

扫描 182 个交付草稿文件。**只有基线之外的新违规才判失败**——门禁是回归检测器，不是把存量债每天重报一遍（那会退化成第二个"每天 18 条建议"）。

| 类型 | 总数 | 其中新增 |
|---|---|---|
| unlabeled-number | 636 | 0 |
| citation-unregistered | 306 | 0 |


> 收敛方式：人工复核后运行 `python -m research_evolve.gates --update-baseline` 接受当前存量为债。

## 六、概念层负债（实测口径）

- 概念文件总数：**6123**
- 带 `auto: true` 自动占位：**5940** （97.0%）
- 文件名近似文章标题：**3184** （52.0%）
- 孤儿概念（自报）：**1850** — 来源 `wiki/health.md (生成器自报)`

> 说明：孤儿数取自生成器自报，未在本轮重算（重算 6000+ 文件全库链接成本高，且 `wiki_grow.py` 的 `Knowledge Graph Density` 是按概念**数量**分档的伪造指标，不可用于判断图质量）。

---

*本报告由 `research_evolve` 生成：每轮一次运行、一次提交，所有计数均来自本轮实际扫描，扫描口径与阈值见 `90_System/research_evolve/config.yaml`，候选与裁决的完整记忆见 `90_System/research_evolve/state/registry.json`。*