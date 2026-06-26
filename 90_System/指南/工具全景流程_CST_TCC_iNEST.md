# TCC + iNEST + CST 工具全景流程

> 8 工具 x 3 研究域 x 4 条标准链路 | 2026-06-24
> 预览: http://127.0.0.1:8900/home/work/.openclaw/workspace/90_System/指南/工具全景流程_CST_TCC_iNEST.md

---

## 一、三域定位

`
CST (仿真实验)    - 数值验证层：所有理论的计算机验证，仿真数据产出
TCC (拓扑计算)    - 硬件理论层：晶圆级网络拓扑、芯片互连架构  
iNEST (神经形态)  - 智能涌现层：脉冲神经网络、群体智能、储备池计算
`

---

## 二、工具-任务映射矩阵

| 研究任务 | networkx | igraph | PyG | brian2 | snntorch | snngrow | PySpike | reservoirpy |
|----------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **CST** 网络拓扑生成 | ★★★ | ★★ | | | | | | |
| **CST** 大规模图指标计算 | | ★★★ | | | | | | |
| **CST** 连接组数据分析 | ★★ | ★★★ | | | | | ★★ | |
| **CST** 仿真结果验证 | ★ | ★ | | | | | ★★★ | |
| **TCC** 晶圆网络建模 | ★★★ | ★★ | ★★ | | | | | |
| **TCC** 拓扑优化预测 | ★ | ★★ | ★★★ | | | | | |
| **TCC** 芯片互连 motif | | ★★★ | | | | | | |
| **iNEST** 神经元动力学 | | | | ★★★ | | | | |
| **iNEST** SNN 架构训练 | | | | | ★★★ | ★★★ | | |
| **iNEST** 群体涌现分析 | | | | | | | ★★ | ★★★ |
| **iNEST** 脉冲同步验证 | | | | | | | ★★★ | |
| **跨界** 生物-芯片拓扑对比 | ★★★ | ★★★ | ★★ | | | | | |

---

## 三、四条标准工具链路

### 链路 1：CST 仿真验证

`
任务: 验证 TCC/iNEST 理论模型的数值正确性

networkx  ------>  igraph  ------>  PySpike
 拓扑生成           图指标计算        脉冲同步验证

Step 1: G = nx.watts_strogatz_graph(n=1024, k=8, p=0.1)
Step 2: g = ig.Graph.from_networkx(G); g.community_leiden()
Step 3: pyspike.spike_sync(spike_trains)
`

### 链路 2：TCC 晶圆拓扑设计

`
任务: 设计并优化晶圆级芯片互连拓扑

networkx  ------>  igraph  ------>  PyG
 拓扑建模           深度分析          GNN 预测

Step 1: networkx 构建候选拓扑（小世界/无标度/随机）
Step 2: igraph 计算模块度 + motif 分布
Step 3: PyG GCN 模型预测拓扑重构性能
`

### 链路 3：iNEST 神经形态智能

`
任务: 从单神经元到群体涌现的完整仿真

brian2 -> snntorch -> snngrow -> PySpike -> reservoirpy
 精细       SNN        生长        脉冲        涌现
 模型       训练        剪枝        验证        分析

Step 1: brian2.NeuronGroup()       LIF 单神经元
Step 2: snntorch.spikegen.rate()   脉冲编码
Step 3: snngrow.grow_and_prune()   架构优化
Step 4: pyspike.isi_distance()     同步性验证
Step 5: reservoirpy.Reservoir()    涌现动力学
`

### 链路 4：跨界对比验证

`
任务: 生物连接组 <-> 芯片拓扑 mutual inspiration

生物数据  ------>  networkx+igraph  ------>  芯片设计
hemibrain         拓扑特征 + 交叉对比         晶圆优化

Step 1: nx.read_graphml("connectome.graphml")
Step 2: igraph 提取度分布/聚类系数/路径
Step 3: nx 生成芯片候选拓扑
Step 4: 对比 motif 分布 + 模块度
`

---

## 四、典型研究场景速查

| 场景 | 输入 | 工具链 | 输出 |
|------|------|--------|------|
| 新拓扑架构验证 | N, 参数集 | networkx -> igraph -> PyG | 拓扑性能报告 |
| 连接组数据分析 | .graphml | networkx -> igraph -> PySpike | 结构+脉冲报告 |
| SNN 架构搜索 | 任务规格 | brian2 -> snntorch -> snngrow | 最优 SNN 架构 |
| 涌现临界探测 | SNN 数据 | PySpike -> reservoirpy | 相变边界 |
| 芯片拓扑对比 | 2+ 方案 | networkx -> igraph | 对比决策报告 |
| 完整研究管线 | 研究假设 | 8 工具串联 | 论文级产出 |

---

## 五、Codex 一键触发词

| 触发词 | 执行的链路 |
|--------|-----------|
| CST 仿真验证 | 链路 1: networkx -> igraph -> PySpike |
| TCC 拓扑设计 | 链路 2: networkx -> igraph -> PyG |
| iNEST 神经全链路 | 链路 3: brian2 -> snntorch -> snngrow -> PySpike -> reservoirpy |
| 跨界对比 | 链路 4: 生物连接组 <-> 芯片拓扑 |
| 全栈研究 | 链路 1-4 串联 |
| 验证工具链 | 8 工具全部导入测试 |
