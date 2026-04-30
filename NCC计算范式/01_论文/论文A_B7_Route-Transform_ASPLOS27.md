# 论文A（B7）：Route≡Transform 理论核心论文
# Paper A (B7): Route≡Transform: A Unified Algebraic Theory
# 目标：ASPLOS 2027 September cycle | 截止：2026年9月9日
# 状态：📋 框架完成，T1任务展开中

---

## 基本信息

| 项目 | 内容 |
|------|------|
| **标题** | Route≡Transform: A Unified Algebraic Theory of Communication and Computation Primitives for Network-Centric Computing |
| **目标会议** | ASPLOS 2027（September cycle） |
| **投稿截止** | 2026年9月9日 |
| **论文类型** | 理论+实验验证，~14页正文（双栏ACM格式）|
| **配套专利** | P1（方法类权利要求1,2）+ P3（FFT同构）|
| **先投专利** | P1必须在本文arXiv上线前完成CNIPA申请 |

---

## Abstract（草稿）

We present a unified algebraic framework that proves communication primitives (AllReduce, AllGather, Broadcast, AlltoAll) and computation primitives (GEMM, Reduce, Map, Scan) are structurally isomorphic operations on a reconfigurable interconnect topology. We formalize this as the Route≡Transform theorem: for any distributed computation expressible as a sequence of communication and computation steps, there exists an equivalent sequence of topology reconfigurations on a single reconfigurable datapath that produces identical results. We define NCC-11, a minimal complete primitive set of 11 orthogonal operations, and prove its completeness (any Turing-computable distributed function is expressible) and minimality (removing any primitive causes at least one target workload to degrade by Ω(N)). We demonstrate three corollaries with profound hardware implications: (1) an N-point FFT is exactly k=log₂N topology reconfigurations of a butterfly pattern, requiring zero dedicated FFT hardware; (2) Mixture-of-Experts token dispatch is a single AlltoAll, topologically equivalent to a distributed matrix transpose; (3) CFAR sliding-window detection is a prefix scan, equivalent to a linear-chain topology with stateful forwarding. We validate these results on a 4-node FPGA prototype (Xilinx VCK190), demonstrating 1024-point FFT in 800 ns via topology reconfiguration, Gemma-4 E2B inference at 5.2 tokens/s, and ≤1 μs cross-scene switching between LLM inference, video detection, and radar DBF.

---

## 论文结构（~14页）

| 章节 | 内容 | 篇幅 | 任务 | 状态 |
|------|------|------|------|------|
| §1 Introduction | Horowitz能耗数据；通信-计算二元分离历史；核心thesis | 1.5页 | T1-5 | ⬜ |
| §2 Background | Horowitz Energy Wall；SHARP/Cerebras/Active Networks对比；缺失的统一 | 1.5页 | T1-5 | ⬜ |
| §3 Theory | **核心**：4定理体系（分解/同构/完备/最小性） | 3页 | **T1-1~4** | 🔴进行中 |
| §4 NCC-11 Spec | 11原语形式化语义、接口、复杂度（表格形式） | 1.5页 | T1-2 | 🟡待 |
| §5 Hardware | VCK190平台、11 IP核资源占用、SDI控制器实现 | 2页 | T2-8 | ⬜待硬件 |
| §6 Evaluation | FFT 800ns、Gemma-4 5.2tok/s、切换<1μs、扩展分析 | 3页 | T2-9 | ⬜待数据 |
| §7 Related Work | PIM/Dataflow/In-Network/Active Networks分类对比 | 0.5页 | T1-5 | ⬜ |
| §8 Discussion | 拓扑选择复杂度；Route→Protocol逆映射；量子扩展 | 0.5页 | T1-5 | ⬜ |
| §9 Conclusion | — | 0.5页 | — | ⬜ |

---

## 核心证明任务清单（T1展开）

### §3.2 定理1——分解定理

**目标**：证明任意分布式计算C = T_m∘R_m∘…∘T_1∘R_1

**证明路径**：
1. 定义分布式计算的数据流图（DFG）：边=Route（数据搬运），节点=Transform（计算）
2. 拓扑排序给出交替序列（经典图论结果）
3. 指出与Valiant BSP的关系：BSP是计算模型层，本定理在硬件原语层并给出最小集
- [ ] **T1-0** 写出严格形式化的定义（分布式计算D的DFG表示）

### §3.3 定理2——同构定理（最关键）

**Lemma 2a（FFT-Butterfly同构）**：
- 构造：写出N=8点Cooley-Tukey蝶形的邻接矩阵A_FFT（8×8）
- 构造：写出N=8节点超立方体维度有序AllReduce的通信图邻接矩阵A_AR（8×8）
- 证明：A_FFT[i,j]=1 ⟺ A_AR[i,j]=1（直接矩阵比对）
- 泛化：基-r FFT对应广义超立方体H_k^(r)
- [ ] **T1-1** 计算N=8的两个邻接矩阵，完成直接比对证明

**Lemma 2b（AlltoAll-Transpose）**：
- SWAP语义：y[i][j]=x[j][i] 就是转置的定义，直接同构
- [ ] 0.5天可完成

**Lemma 2c（Scan-Pipeline）**：
- Blelloch上扫描-下扫描算法在线性链拓扑上的数据流等价性
- [ ] 参考Blelloch 1990，改写为NCC拓扑语言

### §3.4 定理3——完备性

**目标**：对7类工作负载构造性证明原语覆盖

| 工作负载 | 原语分解 | 完成状态 |
|---------|---------|---------|
| Transformer推理 | 见三场景原语流（NCC_Naming_Convention_v2.md §9.1） | ✅已有 |
| CNN推理 | 见三场景原语流（§9.3 YOLO） | ✅已有 |
| FFT | 见§9.2 | ✅已有 |
| SpMV | FOLD_S(稀疏归约) + MOVE(P2P取数) + PACK(拓扑压缩)三步构成; 稀疏度由PRUNE降低带宽开销 | ⬜待写完整分解 |
| DBF | 已在B7素材中 | ✅已有 |
| MoE训练 | SWAP(令牌分发,等价转置) + GEMM(专家计算) + FUSE_S(稀疏汇聚梯度); PRUNE删去非激活专家对应链路 | ⬜待写 |
| GNN | PULL_S(稀疏邻居聚合,只关连进节点) + GEMM(特征变换) + PACK(图结构压缩); 稀疏拓扑适配是GNN的天然场景 | ⬜待写 |

- [ ] **T1-2** 补充SpMV/MoE训练/GNN的原语分解，整理覆盖矩阵

---

### ✨ §3.6 稀疏拓扑扩展定理（新增，2026-04-30）

**动机**：GNN/稀疏Transformer/MoE是当前最重要工作负载，它们的访存模式是**不规则稀疏**的。Route≡Transform在稀疏图上是否成立？需要形式化证明。

**定理 T（稀疏同构）**——候选表述：

> 设 G=(V,E) 为任意稀疏图，稀疏度 = 1 - ρ（ρ为边激活率）。
> 存在拓扑压缩映射 φ: G → G'，G'为紧凑子拓扑，|V'| = K，K ≤ ρ|V|。
> 在G'上，Route≡Transform成立（类同稠密情形的定理1—3）。
> 压缩的信息损失下界：H(任务) / log₂(单链路容量)。

**证明路径**：
1. **PRUNE正确性**：断开mask=0的链路不影响剩余计算语义（任何被删除的边在原计算中贡献为零）。
2. **PACK同构性**：ID映射 φ 是单射，保持激活边的相对顺序，因此G'的操作等价G上对应子图的操作。
3. **下界严格性**：任于信息熵，不可压缩到 K < H(任务)/log₂C 而不损失语义。

**对GNN的应用**：
- 图的邻接矩阵即稀疏拓扑掩码，PRUNE直接由图结构驱动
- PULL_S等价于在图的邻接表上做稀疏聚合（Message Passing的硬件原语实现）
- 拓扑压缩比 = 图的平均度 / N ≈ ρ（稀疏图的 ρ 通常 < 0.01）

- [ ] **T1-4（新）** 写出定理T的完整证明（利用上述证明路径，预估0.5天）

### §3.5 定理4——最小性（下界论证）

**SWAP不可替代**：
- 目标：证明去除SWAP后，MoE token dispatch退化Ω(N)×
- 论证：SWAP完成O(N²)全交换数据量；{FUSE,PULL,CAST}的单步输出数据量均为O(N)；因此模拟一次SWAP至少需要Ω(N)步
- [ ] **T1-3a** 写出形式化下界证明

**SCAN不可替代**：
- 目标：证明去除SCAN后，CFAR sliding-window退化Ω(N)×
- 论证：SCAN的有序部分结果语义（y[i]依赖x[0..i]的有序前缀）无法由无序的FOLD/FUSE在o(N)步内产生
- [ ] **T1-3b** 写出形式化下界证明

**MOVE不可替代**：
- 目标：证明去除MOVE后，sparse P2P退化Ω(N)×
- 论证：用SWAP模拟MOVE需要启动全局N×N交换，而MOVE仅需O(1)数据量
- [ ] **T1-3c** 写出形式化下界证明

---

## 投稿准备清单

- [ ] 确认ASPLOS'27 Sep cycle的页数限制和格式（通常14页，double-blind）
- [ ] LaTeX模板：ACM SIGPLAN LaTeX template
- [ ] 附录：NCC-11完整规范表格（可放Appendix）
- [ ] 图表预算：预计8-10个图（FFT同构图、三场景原语流图、覆盖矩阵、性能对比图）
- [ ] arXiv预印本：在P1 CNIPA申请日之后发布
