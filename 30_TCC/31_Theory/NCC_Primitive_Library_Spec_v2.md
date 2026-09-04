---
direction: both
category: 理论
tags: [NCC, 原语库, 命名规范, 分布式计算, 硬件架构]
summary: "NCC-11原语库命名规范v2.0，定义11个完备原语集"
quality: high
processed: 2026-09-04 08:16
---
---
title: "【iNEST知识库】NCC_Naming_Convention_v2"
tags:
  - research
  - sdi-bond
  - architecture
  - design
  - hardware
  - first-principles
  - paper
  - physics
date: 2026-08-31 07:23
source: GetNotes
score: 18
---

## Original Note

【iNEST知识库】NCC_Naming_Convention_v2

# NCC 原语库命名规范
# NCC Primitive Library Specification v2.0 (NCC-11)
#
# 最后更新：2026-04-20
# 状态：正式规范 v2.0（所有文档、代码、专利、论文统一遵循）
# 文件位置：00_KnowledgeBase_知识库/02_CST_核心理论著作/NCC_Naming_Convention_v2.md
# 前版本：NCC_Naming_Convention_v1.md（NCC-8，已废止）

---

## 一、NCC-11 完备原语集

$$\text{NCC-11} = \{\text{FUSE}, \text{PULL}, \text{CAST}, \text{SWAP}, \text{GEMM}, \text{FOLD}, \text{MAPS}, \text{SCAN}, \text{MOVE}, \text{LINK}, \text{TICK}\}$$

**NCC-11 = 11个原语的最小完备集**（4通信 + 4计算 + 1数据 + 2控制）

### 1.1 设计三原则

1. **代数完备性**：原语集构成计算完备的代数系统——任何可在分布式系统执行的计算均可由原语有限组合表达
2. **正交最小性**：任何一个原语都不能被其余原语在O(1)或O(log N)步内等价替代；否则降级为SDK库函数
3. **硬件可映射性**：每个原语对应一个物理上可独立实现的RTL IP核，面积不超过50K LUT等效门

### 1.2 命名规则

- 统一前缀：Python/API用`ncc.`，RTL/C用`ncc_`，常量引用全大写
- 名称：4个英文字母，可直接发音（如FUSE /fjuːz/，SCAN /skæn/）
- 语义：英文动词或可用作动词的名词
- 不与MPI/NCCL/CUDA/RISC-V现有关键字冲突

---

## 二、NCC-11 原语详表

| 类别 | 编号 | 原语 | 图标 | 语义定义 | MPI等价 | 最优拓扑 | Γst | ALU模式 |
|------|------|------|------|---------|---------|---------|-----|---------|
| **通信** | 1 | **ncc.FUSE** | ⊕ | AllReduce：所有节点贡献数据，全局归约，结果广播至所有节点。`y[*] = Reduce(x[0],...,x[N-1])` | MPI_Allreduce | Butterfly/Ring | ~1.0 | ADD |
| **通信** | 2 | **ncc.PULL** | ⇊ | AllGather：每个节点贡献一份数据，所有节点获得完整拼接。`y[*] = Concat(x[0],...,x[N-1])` | MPI_Allgather | Radial-tree | ~0.2 | PASS |
| **通信** | 3 | **ncc.CAST** | ⇈ | Broadcast：单一源节点数据复制到所有节点。`y[*] = x[root]` | MPI_Bcast | Optimal-tree | ~0.1 | PASS |
| **通信** | 4 | **ncc.SWAP** | ⥂ | AlltoAll：N个节点两两交换不同数据块（分布式矩阵转置）。`y[i][j] = x[j][i]` | MPI_Alltoall | Full Crossbar | ~0.0 | PASS |
| **计算** | 5 | **ncc.GEMM** | ⊗ | 矩阵乘加：`C = α·A×B + β·C`，支持INT4/INT8/FP16/BF16，可配置累加位宽 | cuBLAS GEMM | Local | 1.0 | MUL+ADD |
| **计算** | 6 | **ncc.FOLD** | ⊐ | 向量归约：`y = Reduce(x, op)`，op ∈ {SUM, MAX, MIN, ARGMAX, ARGMIN, PROD} | MPI_Reduce(local) | Ring/Tree | ~0.8 | ADD |
| **计算** | 7 | **ncc.MAPS** | ∘ | 逐元素映射：`y[i] = f(x[i])`，f可为算术、非线性激活、位操作、LUT查表、比较 | — | Local | 1.0 | MUL/ADD/LUT |
| **计算** | 8 | **ncc.SCAN** | ∫ | 前缀归约：`y[i] = Reduce(x[0],...,x[i], op)`，支持inclusive/exclusive，op ∈ {SUM, MAX, MIN, PROD} | MPI_Scan | Binary Tree | ~0.9 | ADD |
| **数据** | 9 | **ncc.MOVE** | → | 点对点传输：从节点src向节点dst发送数据，支持阻塞/非阻塞/带tag | MPI_Send+Recv | P2P | 0.0 | PASS |
| **控制** | 10 | **ncc.LINK** | ⥊ | SDI拓扑控制器：配置互连拓扑、同步屏障、状态查询。子命令：`.config(topo)` `.barrier()` `.status()` `.fence()` `.reset()` | MPI_Barrier | Meta | — | SDI |
| **控制** | 11 | **ncc.TICK** | ⏱ | 全局时间基准：分布式逻辑时钟/事件时间戳，为GALS异步系统提供因果序保证（Lamport 1978） | — | Meta | — | Counter |

> **TICK新增说明**：NCC采用GALS（全局异步局部同步）架构，无全局时钟。分布式时间基准是因果一致性的理论必须——由Lamport逻辑时钟理论（1978）严格证明。TICK仅需轻量计数器+消息戳机制（<500 LUT），是正确性基石，不可省略。

---

## 三、旧名 → 新名映射（历史对照）

| 旧名（v1.0 NCC-8） | 新名（v2.0 NCC-11） | 变更说明 |
|-------------------|-------------------|---------|
| NPC-AR | **ncc.FUSE** | 升级自v1.0，无变化 |
| NPC-AG | **ncc.PULL** | 升级自v1.0，无变化 |
| NPC-BC | **ncc.CAST** | 升级自v1.0，无变化 |
| NPC-AA（保留字→） | **ncc.SWAP** | v2.0正式升为核心原语（原NCC-9保留字） |
| NPC-RS（已废止） | 由`ncc.FUSE(mode=ring)`实现 | ReduceScatter通过LINK配置ring拓扑的FUSE |
| CPC-M/MAC | **ncc.GEMM** | 升级自v1.0，无变化 |
| CPC-R/RED | **ncc.FOLD** | 升级自v1.0，无变化 |
| CPC-EW | **ncc.MAPS** | 升级自v1.0，无变化；LUT功能并入MAPS |
| CPC-S（保留字→） | **ncc.SCAN** | v2.0正式升为核心原语（原NCC-9保留字） |
| CPC-T/CPC-LUT | **ncc.MAPS(func=lut)** | 合并入MAPS，不再单独列原语 |
| SDI-Ctrl | **ncc.LINK** | 升级自v1.0，无变化 |
| —（新增） | **ncc.MOVE** | v2.0新增：GALS架构P2P数据传输 |
| —（新增） | **ncc.TICK** | v2.0新增：分布式逻辑时钟 |

> **v1.0→v2.0变化**：NCC-8 → NCC-11，新增SWAP/SCAN（从保留字升为核心）+ MOVE + TICK；LOOK独立原语取消，功能合并入MAPS(func=lut)。

---

## 四、SDK层库函数（非硬件原语，由原语组合实现）

| SDK函数 | 组合实现 | 步数 |
|---------|---------|------|
| `ncc.sort(x, N)` | log²N轮{SWAP(butterfly)+MAPS(compare-swap)} | O(log²N) |
| `ncc.rand(seed, N)` | LINK.lfsr(seed)+CAST(seed)+MAPS(lfsr_step) | O(1) |
| `ncc.pack(x, fmt)` | MAPS(bit_shift\|mask\|concat) | O(1) |
| `ncc.scatter(x, root)` | CAST(x,root)+MAPS(select_chunk[rank]) | O(log N) |
| `ncc.reduce(x, root, op)` | FUSE(x,op)+MAPS(mask_if_not_root) | O(log N) |
| `ncc.rscat(x, op)` | FUSE(x,op)[LINK→ring, ReduceScatter模式] | O(N) |
| `ncc.gather(x, root)` | PULL(x)+MAPS(mask_if_not_root) | O(log N) |
| `ncc.transpose(A)` | SWAP(A) | O(N) |
| `ncc.fft(x, N)` | log₂N轮{LINK.config(butterfly_k)+MAPS(twiddle_mul)+FUSE(butterfly_add)} | O(log N) |
| `ncc.conv2d(x, w)` | im2col via MAPS+GEMM(x_col, w) | O(1) |
| `ncc.softmax(x)` | FOLD(x,MAX)+MAPS(exp(x-max))+FOLD(expx,SUM)+MAPS(expx/sum) | O(1) |
| `ncc.layernorm(x)` | FUSE(x,SUM)/N→μ; FUSE((x-μ)²,SUM)/N→σ²; MAPS((x-μ)/√(σ²+ε)·γ+β) | O(1) |
| `ncc.flash_attn(Q,K,V)` | 分块: GEMM(Q_i,K_j^T)+SCAN(running_max)+MAPS(exp)+SCAN(running_sum)+GEMM(P,V_j) | O(T/B) |

---

## 五、Python SDK 签名（PyiNEST-Lite）

```python
import ncc

# 控制：拓扑重构
ncc.link.config(ncc.BUTTERFLY, stage=3)     # 蝴蝶拓扑第3级
ncc.link.config(ncc.RING)                    # 环形拓扑
ncc.link.config(ncc.CROSSBAR)               # 全连接
ncc.link.config(ncc.TREE)                   # 树形
ncc.link.barrier()                          # 全局同步屏障
ncc.tick.stamp()                            # 打时间戳（因果序）

# 通信原语
ncc.cast(src=0, data=weights)               # 广播
ncc.fuse(data=gradients, op="sum")          # AllReduce求和
ncc.fuse(data=activations, op="max")        # AllReduce求最大
ncc.pull(data=kv_cache)                     # AllGather
ncc.swap(data=tokens, dst_map=expert_map)   # AlltoAll（MoE专家分发）
ncc.move(data=buf, src=0, dst=3, tag=42)    # P2P传输

# 计算原语
ncc.gemm(A=query, B=key.T, C=attn_score)   # 注意力QK^T
ncc.gemm(A=x, B=weight, C=out, dtype="int4") # INT4 GEMM
ncc.fold(data=vector, op="sum")             # 向量归约
ncc.fold(data=vector, op="argmax")          # argmax
ncc.maps(data=x, func="silu")              # SiLU激活
ncc.maps(data=x, func="rsqrt")             # 倒数平方根
ncc.maps(data=x, func="lut", table=rope_t) # 查表（RoPE）
ncc.scan(data=x, op="sum", exclusive=False) # 前缀和（inclusive）
ncc.scan(data=detect, op="sum")            # CFAR目标计数
```

---

## 六、RTL 模块命名（SystemVerilog）

```verilog
// NCC-11 IP核模块命名规范
module ncc_fuse #(parameter WIDTH=256, NODES=8, OP=SUM)  (...); // AllReduce IP
module ncc_pull #(parameter WIDTH=256, NODES=8)          (...); // AllGather IP
module ncc_cast #(parameter WIDTH=256, NODES=8)          (...); // Broadcast IP
module ncc_swap #(parameter WIDTH=256, NODES=8)          (...); // AlltoAll IP
module ncc_gemm #(parameter M=16, N=16, K=16, DTYPE=INT4)(...); // GEMM IP (脉动阵列)
module ncc_fold #(parameter WIDTH=256, OP=SUM)           (...); // Reduce IP (树形归约)
module ncc_maps #(parameter WIDTH=256, LUT_DEPTH=1024)   (...); // Element-wise + LUT IP
module ncc_scan #(parameter WIDTH=256, OP=SUM, EX=0)     (...); // 前缀扫描 IP
module ncc_move #(parameter WIDTH=256)                   (...); // P2P传输 IP
module ncc_link #(parameter NODES=4, BOND_W=8)           (...); // SDI Controller IP
module ncc_tick #(parameter WIDTH=64)                    (...); // 逻辑时钟 IP
```

---

## 七、NCCL → NCC 自动映射（兼容层）

| NCCL API | NCC原语映射 | 拓扑配置 |
|----------|-----------|---------|
| `ncclAllReduce` | `ncc.FUSE(buf, op)` | LINK→ring(大消息)/tree(小消息) |
| `ncclBroadcast` | `ncc.CAST(buf, root)` | LINK→tree |
| `ncclReduce` | `ncc.FUSE(buf, op)`+`ncc.MAPS(mask)` | LINK→tree |
| `ncclAllGather` | `ncc.PULL(buf)` | LINK→ring |
| `ncclReduceScatter` | `ncc.FUSE(buf, op, mode=rscat)` | LINK→ring |
| `ncclAlltoAll` | `ncc.SWAP(buf)` | LINK→crossbar |
| `ncclSend` | `ncc.MOVE(buf, dst)` | 无需全局拓扑 |
| `ncclRecv` | `ncc.MOVE(buf, src)` | 无需全局拓扑 |
| `ncclGroupStart/End` | `ncc.LINK.fence()` | — |

---

## 八、MPI → NCC 映射

| MPI API | NCC原语映射 | 备注 |
|---------|-----------|------|
| `MPI_Allreduce` | `ncc.FUSE` | 同NCCL |
| `MPI_Allgather/v` | `ncc.PULL` | v变体通过MAPS处理不等长 |
| `MPI_Bcast` | `ncc.CAST` | 直接映射 |
| `MPI_Alltoall/v` | `ncc.SWAP` | v变体通过LINK配置非均匀交换 |
| `MPI_Scan` | `ncc.SCAN` | **直接映射，NCC独有优势** |
| `MPI_Exscan` | `ncc.SCAN(exclusive=True)` | 参数区分 |
| `MPI_Send/Recv` | `ncc.MOVE` | 直接映射 |
| `MPI_Isend/Irecv` | `ncc.MOVE(async=True)` | 非阻塞模式 |
| `MPI_Barrier` | `ncc.LINK.barrier()` | 控制层 |

---

## 九、三场景原语流（使用NCC-11命名）

### 9.1 Gemma-4 E2B 单Token推理（单Transformer层）

```
ncc.cast(weights) → ncc.gemm(QKV) → ncc.fold(RMSNorm.s

…（内容已截断，完整版见Obsidian）

Tags: 
Source: openapi

---

## Related Notes

[[FPGA原型]]
[[SDI化合物键_四型架构]]
[[iNEST-MOC]]
[[Papers-MOC]]
