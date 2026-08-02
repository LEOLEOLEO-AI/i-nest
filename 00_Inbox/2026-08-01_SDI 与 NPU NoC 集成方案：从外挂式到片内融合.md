---
title: getnote_1917222390681866328_SDI 与 NPU NoC 集成方案：从外挂式到片内融合
tags:
  - semiconductor
  - fpga
  - architecture
  - tcc
  - design
  - network
  - hardware
  - chip
  - sdi-bond
  - cst
date: 2026-08-01 21:39
source: GetNotes
score: 25
---

## Original Note

---
note_id: 1917222390681866328
title: "SDI 与 NPU NoC 集成方案：从外挂式到片内融合"
type: plain_text
created: 2026-08-01 10:48:13
source: getnote
kb: 
---

# SDI 与 NPU NoC 集成方案：从外挂式到片内融合

# SDI 与 NPU NoC 集成方案：从外挂式到片内融合

## 一、集成的核心问题

SDI（Software-Defined Interconnect）与 NPU NoC 的集成，本质上要回答三个问题：
1. SDI 放在哪里——片内、片外、还是封装内？
2. SDI 和 NoC 是什么关系——替代、补充、还是分层？
3. 数据怎么流动——Tile → NoC → SDI → 外部，还是 Tile → SDI 直接走？

按渐进式三阶段展开：外挂式（Y1）→ Chiplet 级（Y2-Y3）→ 片内融合式（Y3+）。

---

## 二、三种集成模式总览

| 模式 | SDI 位置 | NPU 改动量 | 延迟量级 | 带宽效率 | 适用阶段 |
|------|---------|-----------|---------|---------|---------|
| 外挂式 | NPU 芯片外（FPGA/ASIC 板卡） | 零改动 | 100ns ~ 1μs（PCIe/SerDes 级） | 低 | Y1 原型验证 |
| Chiplet 级 | 封装内独立 Die | 小改动（增加 D2D 接口） | 1 ~ 10ns（封装内） | 中高 | Y2-Y3 产品化 |
| 片内融合式 | NPU 片内，与 NoC 融合 | 架构级改动 | < 1ns（片内） | 最高 | Y3+ 下一代架构 |

---

## 三、模式一：外挂式集成（FPGA 原型阶段）

### 架构

NPU 芯片内部走原有 NoC，通过 PCIe/高速 SerDes 连接到外部 SDI FPGA 板卡。SDI 只处理跨芯片流量，NPU 片内通信完全不动。

### 数据流

- NPU 内部通信：完全走 NPU 原有 NoC
- NPU → 外部：Tile → NPU NoC → DMA 引擎 → PCIe/SerDes → SDI 交换矩阵 → 外部端口
- 外部 → NPU：反向路径

### 关键设计点

- SDI 只处理跨芯片流量，NPU 零改动
- DMA 引擎是对接点，SDI 对 NPU 来说就是一个"智能网卡"
- 拓扑切换在 SDI 内部完成，NPU 无感知
- TCC-NCCL Plugin 做决策：片间流量才走 SDI

### 落地要点

- 优先用 NPU 已有的 PCIe Gen5 接口，不需要新增硬件
- 基于 NPU 现有的 DMA 驱动做扩展，增加 SDI 配置通道
- 先测清楚当前跨芯片通信的效率基线，再对比优化效果

---

## 四、模式二：Chiplet 级集成（ASIC 产品化阶段）

### 架构

SDI 作为独立 Die，通过 UCIe 3.0 或 BoW 与 NPU Die 封装在同一个 2.5D/3D 封装内。外部 I/O Die 也在封装内。

### 数据流

- NPU 片内通信：走 NPU NoC，部分流量可卸载到 SDI
- 跨 Die 通信：Tile → NPU NoC → D2D 接口 → SDI 交换矩阵 → 外部 / 其他 NPU Die
- SDI 加速的片内通信（可选）：Tile0 → NoC → D2D → SDI → D2D → NoC → Tile1（仅当 SDI 拓扑更优时走）

### 关键设计点

- D2D 接口选型：延迟敏感用 BoW（< 1ns），带宽敏感用 UCIe 3.0（~1.35 Tbps/mm）
- SDI Die 定位：拓扑加速芯片，提供 NPU NoC 做不到的动态重构
- 流量分流策略：小消息走 NoC（路径短），大消息/集合通信走 SDI（拓扑收益大）
- Page Commit 范围：SDI Die 内部 ~10ns 级，跨 Die 同步 ~100ns 级

### 落地要点

- SDI Die 面积控制在 NPU Die 的 1/5 ~ 1/3
- 先从 2.5D 中介层开始，3D 堆叠留到下一代
- 多 Die 封装良率 = 各 Die 良率乘积，需要良率风险评估

---

## 五、模式三：片内融合式集成（下一代架构）

### 设计理念：SDI 即 NoC

SDI 不再是外挂的交换矩阵，而是直接替代了传统 NoC——每个 Tile 旁边就是一个 SDI 交换单元，所有 Tile 间通信都走 SDI。没有两套网络的问题，拓扑切换是常态，TopoColor 虚通道并行多拓扑。

### 分布式 SDI 交换单元（SE）微架构

5×5 交换单元（4 个方向 + 本地 Tile 端口），内部四级流水线：

1. **IB 输入缓冲**：接收 flit，按虚通道分队列（1 拍）
2. **RC 路由计算**：根据 TopoColor 查表决定输出端口（1 拍）
3. **SA 交叉开关分配**：仲裁多输入对同一输出的竞争（1 拍）
4. **OB 输出缓冲**：发送前缓冲，对接下一跳（1 拍）

总延迟 4 拍（~2ns @ 2GHz）。32×32 Mesh 对角线 64 跳，最坏延迟 ~128ns，与片内 SRAM 访问同量级。

### 面积估算（5×5 SE，4 TopoColor，64bit 数据）

| 组件 | 等效门数 | 占比 |
|------|---------|------|
| 5×5 Crossbar | ~15k | 25% |
| 输入缓冲（5端口×4VC×16flit） | ~20k | 33% |
| 路由表 | ~2k | 3% |
| 仲裁器 + 控制逻辑 | ~8k | 13% |
| Page 缓存（8 Page） | ~5k | 8% |
| 其他 | ~10k | 18% |
| **合计** | **~60k 门/SE** | 100% |

SE 面积约为 NPU Tile 的 1% ~ 2%，完全可接受。

---

## 六、TopoColor 虚通道机制

### TopoColor vs 传统 VC

| 维度 | 传统 NoC 虚通道 | TopoColor |
|------|---------------|-----------|
| 目的 | 死锁避免 + QoS | 多拓扑并行 |
| 路由 | 所有 VC 走同一拓扑 | 每个 Color 走不同拓扑 |
| 数量 | 通常 2-4 个 | 4-8 个 |
| 调度 | VC 间公平调度 | Color 间按权重调度 |

### 信用量流控

每个 Color 有独立的 credit 计数器，链路级管理，每跳独立。某个 Color 的 credit 用完只停发该 Color，不影响其他 Color。

### Color 间调度策略

- 轮询调度：公平，实现最简单
- 加权轮询：按权重分配带宽，适合流量不均衡场景
- 优先级调度：控制流走高优先级 Color，注意饥饿问题

推荐：数据通路用加权轮询，控制通路用高优先级 Color。权重可通过 Page 配置动态调整。

### Color 数量选择

推荐起步用 4 个 Color：
- Color 0：AllReduce / Butterfly（规约类）
- Color 1：Pipeline / Ring（流水类）
- Color 2：Mesh / 点对点（通用类）
- Color 3：控制 / 高优先级（C 原语、同步信号）

---

## 七、死锁预防与活锁避免

### 死锁预防策略

**策略一：拓扑级死锁预防（最有效）**
- TCC 拓扑是预编译的，Page 编译阶段就做死锁验证
- Tree/Butterfly：天然无环，无死锁
- Ring：用 2 个 VC 打破环
- Mesh/Torus：维序路由 + 逃逸 VC
- 运行时不需要死锁检测，按预编译配置跑

**策略二：Color 间隔离**
- 每个 Color 有独立缓冲和 credit，一个 Color 死锁不影响其他 Color
- 高优先级控制 Color 可做死锁恢复通道

**策略三：逃逸通道（Escape VC）**
- 预留专用逃逸虚通道
- 检测到潜在死锁（flit 等待超时）就移到逃逸 VC
- 逃逸 VC 采用无死锁路由策略

### 活锁避免

- TCC 拓扑确定、路由固定，活锁风险低
- 防止优先级反转：老化机制（等待越久优先级越高）+ 最大等待时间保证

### 死锁检测与恢复（最后防线）

- 检测：监控 flit 等待时间，超时触发死锁检测，向上游回溯等待环
- 恢复：软复位（只复位死锁 Color）→ 丢包重传 → 全局复位

---

## 八、Page Commit 硬件实现

### 双缓冲配置寄存器

每个 SE 有 Active（当前运行）和 Shadow（待切换）两组配置寄存器。新 Page 提前加载到 Shadow，C.LINK 信号到来时一拍切换。切换完成后 Active 和 Shadow 角色互换。

### 全局同步信号树

C.LINK 通过 H 树/鱼骨结构的低偏斜时钟树分发到所有 SE。1024 SE 规模下，偏斜控制在 5% 时钟周期以内（< 25ps @ 2GHz）。

### 排空确认的硬件实现

尾标记 + 全局 AND 树：
1. C.SYNC 后停止注入新 flit
2. 最后一个 flit 带 EOT 标记
3. 每个 SE 所有端口发完且收完 EOT → 发出排空完成信号
4. 所有 SE 的排空完成信号通过硬件 AND 树归约
5. AND 输出为 1 → 全局排空完成，可安全切换

AND 树延迟 O(log N)：1024 SE 需要 10 级与门，~5ns。加上排空传输时间，总排空时间几十纳秒量级。

---

## 九、技术演进路径与退出条件

```
Y1: 外挂式（FPGA）
  │  验证：概念可行，性能收益明确
  ▼
Y2: Chiplet 级（ASIC Die）
  │  验证：产品化可行，成本可控
  ▼
Y3: 片内融合式（下一代 NPU 架构）
```

**外挂式 → Chiplet 级退出条件**：
1. 至少 3 个场景性能提升 > 30%
2. 市场需求明确
3. D2D 接口方案成熟

**Chiplet 级 → 片内融合退出条件**：
1. SDI Die 面积 < NPU 的 20%
2. 片内通信优化收益 > 20%
3. 工具链成熟

---

## 十、与 NPU NoC 团队对接清单

**硬件对接**：NoC 拓扑结构、数据位宽/频率/flit 格式、流控机制、Tile 端口数量、DMA 引擎接口、配置总线类型、时钟树结构

**软件对接**：驱动架构（用户态/内核态）、DMA 编程接口、性能计数器访问方式、编译器后端接口（MLIR/XLA/自研）、集合通信库实现方式

**性能对接**：典型模型通信模式分析、当前 NoC 利用率瓶颈、跨芯片通信效率基线、性能分析工具使用方法


---
*getnote | 2026-08-01 21:39*


---

## Related Notes

[[FPGA原型]]
[[paper1_iNEST_core_architecture]]
[[iNEST-MOC]]
[[NCL神经计算定律详解]]
[[CST计量仪]]
[[超非线性增益]]
[[SDI化合物键_四型架构]]
