---
title: "【iNEST知识库】TCC_Naming_Convention_v2"
date: 2026-04-29 03:08:32
source: "????"
note_id: 1908472274210609864
note_type: plain_text
tags: []
source: getnote---

# 【iNEST知识库】TCC_Naming_Convention_v2

# TCC 原语库命名规范
# TCC Primitive Library Specification v2.0 (TCC-16)
#
# 最后更新：2026-04-20
# 状态：正式规范 v2.0（所有文档、代码、专利、论文统一遵循）
# 文件位置：00_KnowledgeBase_知识库/02_CST_核心理论著作/TCC_Naming_Convention_v2.md
# 前版本：TCC_Naming_Convention_v1.md（TCC-8，已废止）

provenance: external
---

## 一、TCC-16 完备原语集

$$\text{TCC-16} = \{\text{FUSE}, \text{PULL}, \text{CAST}, \text{SWAP}, \text{GEMM}, \text{FOLD}, \text{MAPS}, \text{SCAN}, \text{MOVE}, \text{LINK}, \text{TICK}\}$$

**TCC-16 = 11个原语的最小完备集**（4通信 + 4计算 + 1数据 + 2控制）

### 1.1 设计三原则

1. **代数完备性**：原语集构成计算完备的代数系统——任何可在分布式系统执行的计算均可由原语有限组合表达
2. **正交最小性**：任何一个原语都不能被其余原语在O(1)或O(log N)步内等价替代；否则降级为SDK库函数
3. **硬件可映射性**：每个原语对应一个物理上可独立实现的RTL IP核，面积不超过50K LUT等效门

### 1.2 命名规则

- 统一前缀：Python/API用`tcc.`，RTL/C用`tcc_`，常量引用全大写
- 名称：4个英文字母，可直接发音（如FUSE /fjuːz/，SCAN /skæn/）
- 语义：英文动词或可用作动词的名词
- 不与MPI/NCCL/CUDA/RISC-V现有关键字冲突

---

## 二、TCC-16 原语详表

| 类别 | 编号 | 原语 | 图标 | 语义定义 | MPI等价 | 最优拓扑 | Γst | ALU模式 |
|------|------|------|------|---------|---------|---------|-----|---------|
| **通信** | 1 | **tcc.FUSE** | ⊕ | AllReduce：所有节点贡献数据，全局归约，结果广播至所有节点。`y[*] = Reduce(x[0],...,x[N-1])` | MPI_Allreduce | Butterfly/Ring | ~1.0 | ADD |
| **通信** | 2 | **tcc.PULL** | ⇊ | AllGather：每个节点贡献一份数据，所有节点获得完整拼接。`y[*] = Concat(x[0],...,x[N-1])` | MPI_Allgather | Radial-tree | ~0.2 | PASS |
| **通信** | 3 | **tcc.CAST** | ⇈ | Broadcast：单一源节点数据复制到所有节点。`y[*] = x[root]` | MPI_Bcast | Optimal-tree | ~0.1 | PASS |
| **通信** | 4 | **tcc.SWAP** | ⥂ | AlltoAll：N个节点两两交换不同数据块（分布式矩阵转置）。`y[i][j] = x[j][i]` | MPI_Alltoall | Full Crossbar | ~0.0 | PASS |
| **计算** | 5 | **tcc.GEMM** | ⊗ | 矩阵乘加：`C = α·A×B + β·C`，支持INT4/INT8/FP16/BF16，可配置累加位宽 | cuBLAS GEMM | Local | 1.0 | MUL+ADD |
| **计算** | 6 | **tcc.FOLD** | ⊐ | 向量归约：`y = Reduce(x, op)`，op ∈ {SUM, MAX, MIN, ARGMAX, ARGMIN, PROD} | MPI_Reduce(local) | Ring/Tree | ~0.8 | ADD |
| **计算** | 7 | **tcc.MAPS** | ∘ | 逐元素映射：`y[i] = f(x[i])`，f可为算术、非线性激活、位操作、LUT查表、比较 | — | Local | 1.0 | MUL/ADD/LUT |
| **计算** | 8 | **tcc.SCAN** | ∫ | 前缀归约：`y[i] = Reduce(x[0],...,x[i], op)`，支持inclusive/exclusive，op ∈ {SUM, MAX, MIN, PROD} | MPI_Scan | Binary Tree | ~0.9 | ADD |
| **数据** | 9 | **tcc.MOVE** | → | 点对点传输：从节点src向节点dst发送数据，支持阻塞/非阻塞/带tag | MPI_Send+Recv | P2P | 0.0 | PASS |
| **控制** | 10 | **tcc.LINK** | ⥊ | SDI拓扑控制器：配置互连拓扑、同步屏障、状态查询。子命令：`.config(topo)` `.barrier()` `.status()` `.fence()` `.reset()` | MPI_Barrier | Meta | — | SDI |
| **控制** | 11 | **tcc.TICK** | ⏱ | 全局时间基准：分布式逻辑时钟/事件时间戳，为GALS异步系统提供因果序保证（Lamport 1978） | — | Meta | — | Counter |

> **TICK新增说明**：TCC采用GALS（全局异步局部同步）架构，无全局时钟。分布式时间基准是因果一致性的理论必须——由Lamport逻辑时钟理论（1978）严格证明。TICK仅需轻量计数器+消息戳机制（<500 LUT），是正确性基石，不可省略。

---

## 三、旧名 → 新名映射（历史对照）

| 旧名（v1.0 TCC-8） | 新名（v2.0 TCC-16） | 变更说明 |
|-------------------|-------------------|---------|
| NPC-AR | **tcc.FUSE** | 升级自v1.0，无变化 |
| NPC-AG | **tcc.PULL** | 升级自v1.0，无变化 |
| NPC-BC | **tcc.CAST** | 升级自v1.0，无变化 |
| NPC-AA（保留字→） | **tcc.SWAP** | v2.0正式升为核心原语（原TCC-9保留字） |
| NPC-RS（已废止） | 由`tcc.FUSE(mode=ring)`实现 | ReduceScatter通过LINK配置ring拓扑的FUSE |
| CPC-M/MAC | **tcc.GEMM** | 升级自v1.0，无变化 |
| CPC-R/RED | **tcc.FOLD** | 升级自v1.0，无变化 |
| CPC-EW | **tcc.MAPS** | 升级自v1.0，无变化；LUT功能并入MAPS |
| CPC-S（保留字→） | **tcc.SCAN** | v2.0正式升为核心原语（原TCC-9保留字） |
| CPC-T/CPC-LUT | **tcc.MAPS(func=lut)** | 合并入MAPS，不再单独列原语 |
| SDI-Ctrl | **tcc.LINK** | 升级自v1.0，无变化 |
| —（新增） | **tcc.MOVE** | v2.0新增：GALS架构P2P数据传输 |
| —（新增） | **tcc.TICK** | v2.0新增：分布式逻辑时钟 |

> **v1.0→v2.0变化**：TCC-8 → TCC-16，新增SWAP/SCAN（从保留字升为核心）+ MOVE + TICK；LOOK独立原语取消，功能合并入MAPS(func=lut)。

---

## 四、SDK层库函数（非硬件原语，由原语组合实现）

| SDK函数 | 组合实现 | 步数 |
|---------|---------|------|
| `tcc.sort(x, N)` | log²N轮{SWAP(butterfly)+MAPS(compare-swap)} | O(log²N) |
| `tcc.rand(seed, N)` | LINK.lfsr(seed)+CAST(seed)+MAPS(lfsr_step) | O(1) |
| `tcc.pack(x, fmt)` | MAPS(bit_shift\|mask\|concat) | O(1) |
| `tcc.scatter(x, root)` | CAST(x,root)+MAPS(select_chunk[rank]) | O(log N) |
| `tcc.reduce(x, root, op)` | FUSE(x,op)+MAPS(mask_if_not_root) | O(log N) |
| `tcc.rscat(x, op)` | FUSE(x,op)[LINK→ring, ReduceScatter模式] | O(N) |
| `tcc.gather(x, root)` | PULL(x)+MAPS(mask_if_not_root) | O(log N) |
| `tcc.transpose(A)` | SWAP(A) | O(N) |
| `tcc.fft(x, N)` | log₂N轮{LINK.config(butterfly_k)+MAPS(twiddle_mul)+FUSE(butterfly_add)} | O(log N) |
| `tcc.conv2d(x, w)` | im2col via MAPS+GEMM(x_col, w) | O(1) |
| `tcc.softmax(x)` | FOLD(x,MAX)+MAPS(exp(x-max))+FOLD(expx,SUM)+MAPS(expx/sum) | O(1) |
| `tcc.layernorm(x)` | FUSE(x,SUM)/N→μ; FUSE((x-μ)²,SUM)/N→σ²; MAPS((x-μ)/√(σ²+ε)·γ+β) | O(1) |
| `tcc.flash_attn(Q,K,V)` | 分块: GEMM(Q_i,K_j^T)+SCAN(running_max)+MAPS(exp)+SCAN(running_sum)+GEMM(P,V_j) | O(T/B) |

---

## 五、Python SDK 签名（PyiNEST-Lite）

```python
import tcc

# 控制：拓扑重构
tcc.link.config(tcc.BUTTERFLY, stage=3)     # 蝴蝶拓扑第3级
tcc.link.config(tcc.RING)                    # 环形拓扑
tcc.link.config(tcc.CROSSBAR)               # 全连接
tcc.link.config(tcc.TREE)                   # 树形
tcc.link.barrier()                          # 全局同步屏障
tcc.tick.stamp()                            # 打时间戳（因果序）

# 通信原语
tcc.cast(src=0, data=weights)               # 广播
tcc.fuse(data=gradients, op="sum")          # AllReduce求和
tcc.fuse(data=activations, op="max")        # AllReduce求最大
tcc.pull(data=kv_cache)                     # AllGather
tcc.swap(data=tokens, dst_map=expert_map)   # AlltoAll（MoE专家分发）
tcc.move(data=buf, src=0, dst=3, tag=42)    # P2P传输

# 计算原语
tcc.gemm(A=query, B=key.T, C=attn_score)   # 注意力QK^T
tcc.gemm(A=x, B=weight, C=out, dtype="int4") # INT4 GEMM
tcc.fold(data=vector, op="sum")             # 向量归约
tcc.fold(data=vector, op="argmax")          # argmax
tcc.maps(data=x, func="silu")              # SiLU激活
tcc.maps(data=x, func="rsqrt")             # 倒数平方根
tcc.maps(data=x, func="lut", table=rope_t) # 查表（RoPE）
tcc.scan(data=x, op="sum", exclusive=False) # 前缀和（inclusive）
tcc.scan(data=detect, op="sum")            # CFAR目标计数
```

---

## 六、RTL 模块命名（SystemVerilog）

```verilog
// TCC-16 IP核模块命名规范
module tcc_fuse #(parameter WIDTH=256, NODES=8, OP=SUM)  (...); // AllReduce IP
module tcc_pull #(parameter WIDTH=256, NODES=8)          (...); // AllGather IP
module tcc_cast #(parameter WIDTH=256, NODES=8)          (...); // Broadcast IP
module tcc_swap #(parameter WIDTH=256, NODES=8)          (...); // AlltoAll IP
module tcc_gemm #(parameter M=16, N=16, K=16, DTYPE=INT4)(...); // GEMM IP (脉动阵列)
module tcc_fold #(parameter WIDTH=256, OP=SUM)           (...); // Reduce IP (树形归约)
module tcc_maps #(parameter WIDTH=256, LUT_DEPTH=1024)   (...); // Element-wise + LUT IP
module tcc_scan #(parameter WIDTH=256, OP=SUM, EX=0)     (...); // 前缀扫描 IP
module tcc_move #(parameter WIDTH=256)                   (...); // P2P传输 IP
module tcc_link #(parameter NODES=4, BOND_W=8)           (...); // SDI Controller IP
module tcc_tick #(parameter WIDTH=64)                    (...); // 逻辑时钟 IP
```

---

## 七、NCCL → TCC 自动映射（兼容层）

| NCCL API | TCC原语映射 | 拓扑配置 |
|----------|-----------|---------|
| `ncclAllReduce` | `tcc.FUSE(buf, op)` | LINK→ring(大消息)/tree(小消息) |
| `ncclBroadcast` | `tcc.CAST(buf, root)` | LINK→tree |
| `ncclReduce` | `tcc.FUSE(buf, op)`+`tcc.MAPS(mask)` | LINK→tree |
| `ncclAllGather` | `tcc.PULL(buf)` | LINK→ring |
| `ncclReduceScatter` | `tcc.FUSE(buf, op, mode=rscat)` | LINK→ring |
| `ncclAlltoAll` | `tcc.SWAP(buf)` | LINK→crossbar |
| `ncclSend` | `tcc.MOVE(buf, dst)` | 无需全局拓扑 |
| `ncclRecv` | `tcc.MOVE(buf, src)` | 无需全局拓扑 |
| `ncclGroupStart/End` | `tcc.LINK.fence()` | — |

---

## 八、MPI → TCC 映射

| MPI API | TCC原语映射 | 备注 |
|---------|-----------|------|
| `MPI_Allreduce` | `tcc.FUSE` | 同NCCL |
| `MPI_Allgather/v` | `tcc.PULL` | v变体通过MAPS处理不等长 |
| `MPI_Bcast` | `tcc.CAST` | 直接映射 |
| `MPI_Alltoall/v` | `tcc.SWAP` | v变体通过LINK配置非均匀交换 |
| `MPI_Scan` | `tcc.SCAN` | **直接映射，TCC独有优势** |
| `MPI_Exscan` | `tcc.SCAN(exclusive=True)` | 参数区分 |
| `MPI_Send/Recv` | `tcc.MOVE` | 直接映射 |
| `MPI_Isend/Irecv` | `tcc.MOVE(async=True)` | 非阻塞模式 |
| `MPI_Barrier` | `tcc.LINK.barrier()` | 控制层 |

---

## 九、三场景原语流（使用TCC-16命名）

### 9.1 Gemma-4 E2B 单Token推理（单Transformer层）

```
tcc.cast(weights) → tcc.gemm(QKV) → tcc.fold(RMSNorm.s

…（内容已截断，完整版见Obsidian）


<!-- orphan-cleanup: no MOC found, tagged -->
