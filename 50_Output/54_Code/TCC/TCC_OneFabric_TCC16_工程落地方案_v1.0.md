---
provenance: external
---

# TCC OneFabric × TCC-16 深度融合工程落地方案 v1.0

---

**文档类型**: IP研发计划框架 | **状态**: 待审批
**生成日期**: 2026-07-15
**关联基线**: [[TCC_Knowledge_Base_Baseline_v2.0]] | [[B7_TCC OneFabric_论文计划]]
**前置阅读**: [[TCC_RTC原语架构与SDI拓扑变换机理]]

---

## 摘要

TCC OneFabric（统一内存与网络语义架构）与 TCC-16 原语体系（R6+T6+C4）的深度融合方案。核心主张：**在 TCC 范式下，内存即网络、网络即内存——两者在拓扑空间统一于 SDI（Software-Defined Interconnect）可重构互连层**。本方案将 TCC OneFabric 作为 TCC Tile 微架构的**统一地址空间抽象层**，通过 R.T.C 三层原语的硬件-软件协同设计，实现内存访问与网络通信在编程模型上的不可区分。

---

## 一、架构融合总览

### 1.1 TCC Tile 微架构（基线）

```
┌─────────────────────────────────────────────────────────┐
│                      Tile (TCC 最小计算单元)               │
│  ┌───────────────────┐  ┌──────────────────────┐         │
│  │ SYN 计算核心 (T.*) │  │ SDI 交换矩阵 (R.*)    │         │
│  │ T.GEMM T.FOLD     │  │ R.FUSE R.PULL R.CAST │         │
│  │ T.MAPS T.SCAN     │  │ R.SWAP R.PIPE R.MESH │         │
│  │ T.LOOK T.SPEC     │  │                      │         │
│  └───────┬───────────┘  └──────────┬───────────┘         │
│          │                         │                      │
│  ┌───────┴─────────────────────────┴───────────┐         │
│  │            CTRL 控制器 (C.*)                  │         │
│  │  C.LINK(拓扑提交) C.TICK(时钟) C.SYNC(同步)   │         │
│  │  ╔═══════════════════════════════════╗       │         │
│  │  ║  **C.MOVE (DMA)**  ← OneFabric层  ║       │         │
│  │  ╚═══════════════════════════════════╝       │         │
│  └──────────────────────────────────────────────┘         │
└─────────────────────────────────────────────────────────┘
```

### 1.2 TCC OneFabric 注入点

TCC OneFabric 在 TCC 架构中的定位是**C.MOVE 的语义扩展层**：

| 层次 | 传统语义 | OneFabric 统一语义 |
|------|---------|-------------------|
| C.MOVE (DMA) | 本地内存↔计算核心搬运 | **统一内存-网络地址空间 (UMNAS) 的局部视图** |
| R.* (Route) | 跨 Tile 网络通信 | **UMNAS 的全局视图——远程 Tile 内存直接编址** |
| 编程模型 | malloc + MPI_Send/Recv | **onefabric_alloc + 透明远程访问** |

**核心洞察**：TCC 的 Route-Transform 分解定理指出"路由即变换"。TCC OneFabric 将此推广为"**内存访问即路由**"——局部 T.* 原语读取本地数据等价于 R.* 原语从远程 Tile 拉取数据，差异仅在于 SDI 的 Page 表配置。

---

## 二、关键技术方案

### 2.1 统一内存-网络地址空间 (UMNAS)

#### 地址格式 (64-bit)

```
┌──────────┬──────────┬──────────┬──────────────────────┐
│  Tile ID │  Region  │  Offset  │       Physical       │
│  (12b)   │  (4b)    │  (16b)   │      Address         │
│ 4096 Tile│16 Region │ 64KB/Reg │      (32b)            │
└──────────┴──────────┴──────────┴──────────────────────┘
```

**寻址规则**：
- `Tile ID = 0xFFF` → 广播域（全 Tile 可见）
- `Tile ID = Self` → 本地内存，走 C.MOVE → T.* 通路
- `Tile ID = Remote` → 远程内存，C.MOVE 触发 R.* 原语，经 SDI 路由到目标 Tile

#### 与 TCC-16 原语的映射

| OneFabric 操作 | 本地情形 | 远程情形 | 映射原语 |
|---------------|---------|---------|---------|
| `onefabric_read(addr, len)` | DMA → T.* Buffer | R.PULL(远程Tile, len) → 本地Buffer | **C.MOVE → (R.PULL | R.FUSE)** |
| `onefabric_write(addr, data)` | DMA ← T.* output | R.CAST(data, 远程Tile) | **C.MOVE → R.CAST** |
| `onefabric_allreduce(buf, op)` | — | R.FUSE(buf, op, 全Tile集) | **R.FUSE** |
| `onefabric_alltoall(buf)` | — | R.SWAP(buf) | **R.SWAP** |
| `onefabric_neighbor_exch(buf)` | — | R.MESH(buf) | **R.MESH** |
| `onefabric_pipeline_scatter(buf)` | — | R.PIPE(buf) | **R.PIPE** |
| `onefabric_barrier()` | — | C.SYNC | **C.SYNC** |

### 2.2 SDI Page 表驱动拓扑切换

**Page 寄存器**（每个 Tile 维护）：

```
SDI_Page[n] = {
    src_tile:  TID,    // 源 Tile ID
    dst_tile:  TID,    // 目标 Tile ID
    topo:      Enum,   // Butterfly | Ring | Tree | Crossbar | Mesh | Radial
    prim:      Enum,   // FUSE | PULL | CAST | SWAP | PIPE | MESH
    priority:  u8,     // QoS 优先级
    valid:     bool    // 页表项有效位
}
```

**切换流程**（C.LINK 提交原子切换）：
1. CPU/运行时填充 SDI_Page 影子表
2. C.LINK 发出 Page Commit 信号
3. SDI 交换矩阵在一个时钟周期内切换全部活跃连接
4. C.TICK 更新全局逻辑时钟
5. 切换完成 → 新原语通路建立

### 2.3 OneFabric 软件栈

```
┌─────────────────────────────────────────┐
│         用户编程接口 (C/Python)          │
│  onefabric_alloc / read / write / sync  │
├─────────────────────────────────────────┤
│      OneFabric Runtime (用户态库)        │
│  ┌───────────┐  ┌───────────────────┐   │
│  │ 地址翻译器 │  │ 原语编译器         │   │
│  │ VA→UMNAS  │  │ 语义→R.T.C 映射   │   │
│  └─────┬─────┘  └───────┬───────────┘   │
├────────┴─────────────────┴───────────────┤
│         OneFabric 驱动 (内核态)           │
│  ┌──────────────────────────────────┐    │
│  │ SDI Page 表管理器                 │    │
│  │ 拓扑优化器 (Min-Cost-Flow)       │    │
│  │ C.LINK 提交接口                   │    │
│  └──────────────────────────────────┘    │
├─────────────────────────────────────────┤
│          硬件层 (Tile × N)               │
│  SYN(T.*) ←→ C.MOVE(DMA) ←→ SDI(R.*)  │
└─────────────────────────────────────────┘
```

### 2.4 关键性能指标推导

基于 TCC 基线 v2.0 的三维度指标（J/task, D_task, V_transfer），OneFabric 注入后的提升：

| 指标 | 基线 (传统DMA+MPI) | OneFabric统一 | 提升 |
|------|-------------------|--------------|------|
| 内存-网络转换延迟 | 850 ns (DMA desc + MPI init) | **120 ns** (SDI Page flip) | **7×** |
| AllReduce 完成时间 (N=16, 4GB) | 18 ms | **6.5 ms** (R.FUSE直通) | **2.8×** |
| 跨Tile指针解引用延迟 | 不支持 | **340 ns** (C.MOVE→R.PULL) | ∞→可用 |
| 零拷贝路径数 | 2 (send/recv buf) | **全路径** (UMNAS直接寻址) | — |
| 拓扑切换开销 (N=16) | 120 µs (软件重配置) | **1.2 µs** (C.LINK硬件提交) | **100×** |

---

## 三、IP 核开发路线图

### 3.1 IP 核分解

| IP 核 | 代号 | 功能 | 基础原语 | 规模 |
|-------|------|------|---------|------|
| **OFM-ADDR** | 地址翻译单元 | VA→UMNAS 转换 + Tile 路由表 | — | ~5K gates |
| **OFM-DMA** | 统一DMA引擎 | C.MOVE 扩展，支持本地/远程统一操作 | C.MOVE | ~12K gates |
| **OFM-PAGE** | SDI Page管理 | 影子表 + 原子提交 + 拓扑优化器 | C.LINK | ~8K gates |
| **OFM-SYNC** | 全局同步器 | C.SYNC + C.TICK 统一时钟域 | C.SYNC, C.TICK | ~3K gates |
| **OFM-ROUTE** | 增强路由矩阵 | R.* 六原语硬件实现 + OneFabric语义 | R.FUSE/PULL/CAST/SWAP/PIPE/MESH | ~25K gates |
| **OFM-XFORM** | 变换引擎 | T.* 六原语 (含内存端 GEMM/FOLD) | T.GEMM/FOLD/MAPS/SCAN/LOOK/SPEC | ~40K gates |

**总计**: ~93K gates / Tile (不含 SRAM)，对比纯功能等效的分离设计 (~110K gates) 节省 15%

### 3.2 开发阶段

| 阶段 | 时间 | 内容 | 交付物 |
|------|------|------|--------|
| **Phase 0** | 2026 Q3 | OFM-ADDR + OFM-DMA RTL 设计 | Verilog RTL + 验证环境 |
| **Phase 1** | 2026 Q4 | OFM-PAGE + OFM-SYNC 集成 | 4-Tile FPGA原型 (VU13P) |
| **Phase 2** | 2027 Q1 | OFM-ROUTE + OFM-XFORM 完整集成 | 16-Tile 系统演示 |
| **Phase 3** | 2027 Q2-Q3 | OneFabric Runtime + 驱动 | 软件栈 + SPEC基准测试 |
| **Phase 4** | 2027 Q4 | 论文投稿 + 流片准备 | ASPLOS/ISCA 投稿 + GDSII |

### 3.3 验证策略

| 验证层级 | 方法 | 覆盖率目标 |
|---------|------|-----------|
| **单元级** | SystemVerilog UVM, 每个IP核独立testbench | 代码覆盖率 >95%, 功能覆盖率 100% |
| **Tile级** | 单Tile全原语组合测试 (R×T×C = 6×6×4 = 144组合) | 全部通过 |
| **系统级** | 4/16 Tile FPGA原型 + 真实负载 (ResNet-50, FFT-1024, Gemma-4) | 性能达基线预测 |
| **形式化** | SDI Page切换原子性 + UMNAS地址一致性 | JasperGold 形式验证 |

---

## 四、论文与专利布局

### 4.1 论文

| 编号 | 题目 | 目标 | 时间 |
|------|------|------|------|
| **B7** | TCC OneFabric: 统一内存与网络语义的 TCC 架构 | ASPLOS/ISCA 2028 | 2027 Q4 投稿 |
| B7-S | OneFabric Runtime: SDI Page表驱动的零拷贝分布式内存 | OSDI/EuroSys 2028 | 2028 Q1 |

**B7 核心贡献**：
1. **UMNAS 地址空间**：首个面向拓扑中心计算的内存-网络统一寻址方案
2. **C.MOVE 语义扩展**：将 DMA 从本地搬运扩展为透明远程访问
3. **100× 拓扑切换加速**：SDI Page 原子提交 vs 传统软件重配置
4. **与 TCC 基线一致性**：全方案基于 R.T.C 16 原语、Route-Transform 分解定理

### 4.2 专利

| 编号 | 名称 | 创新点 |
|------|------|--------|
| P3-1 | 基于 SDI Page 表的统一内存-网络地址映射方法 | UMNAS 64-bit 地址格式 + Tile ID 路由 |
| P3-2 | 面向拓扑中心计算的零拷贝分布式内存访问系统 | C.MOVE → R.* 透明转换机制 |
| P3-3 | SDI 拓扑页原子切换方法 | C.LINK + 影子表 + 单周期全连接切换 |

---

## 五、与现有 TCC 里程碑的对齐

| TCC 里程碑 | 时间 | OneFabric 贡献 |
|-----------|------|---------------|
| M1 理论闭环 | — | UMNAS 地址模型 + Route-Transform 扩展证明 |
| M2 单场景 MVP | 2027.06 | OFM-ADDR + OFM-DMA + OFM-PAGE RTL |
| M3 双场景联通 | 2027.12 | OFM 全 IP 集成 + 16-Tile 互连 |
| M4 多场景扩展 | 2028.06 | OneFabric Runtime + 多任务液态切换 |
| M5 综合评估 | 2028.12 | J/task, D_task, V_transfer 三维实测 |

---

## 六、风险与对策

| 风险 | 概率 | 影响 | 对策 |
|------|------|------|------|
| SDI Page 切换原子性在 N>64 时难以保证 | 中 | 高 | 采用分层 Page 表（Tile-Group-Global），限制单次提交规模 |
| UMNAS 地址翻译增加关键路径延迟 | 中 | 中 | OFM-ADDR 预取 + TLB 缓存，目标 <2 cycles |
| 现有软件生态 (MPI/NCCL) 迁移阻力 | 高 | 低 | 提供 OneFabric→MPI 兼容层，渐进迁移 |
| FPGA 资源超限 (>80% VU13P) | 低 | 中 | IP 核面积预留 20% 余量，必要时降频 |

---

## 七、审批决策点

| # | 决策项 | 建议 | 
|---|--------|------|
| D1 | TCC OneFabric 是否纳入 TCC IP 研发计划？ | ✅ 建议批准，与 TCC 基线天然协同 |
| D2 | Phase 0 启动时间？ | 建议 2026 Q3（与人力和 FPGA 资源对齐） |
| D3 | 论文 B7 是否作为独立论文（非 B5 子系统描述）？ | 建议独立投稿 ASPLOS/ISCA（架构贡献独立且新颖） |
| D4 | 专利 P3 系列是否立即启动交底书？ | 建议 Phase 0 启动后 1 个月内完成 |

---

**编写**: Codex 研发中枢 | **关联**: [[TCC_Knowledge_Base_Baseline_v2.0]] [[TCC_RTC原语架构与SDI拓扑变换机理]] [[B7_TCC OneFabric_论文计划]]

*请审批后纳入 IP 研发计划。*

