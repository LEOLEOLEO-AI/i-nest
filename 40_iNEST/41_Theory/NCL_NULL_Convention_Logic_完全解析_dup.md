# NCL (NULL Convention Logic) 完全解析

> 独立参考文件 | 可随时索引查询  
> 维护日期：2026-06-03 | iNEST Research Team

---

## 一、什么是 NCL

**NULL Convention Logic** 是一种**无全局时钟的异步逻辑范式**，由 Karl Fant 和 Scott Brandt 于 1996 年系统化（美国专利 US5305463, *Theseus Logic*）。

### 核心思想

传统同步电路靠全局时钟协调一切：
```
时钟 ↑ → 所有寄存器同时采样 → 组合逻辑传播 → 时钟 ↑ → 重复
```

NCL 靠**数据本身**的到达/完成来协调：
```
DATA 到达 → 组合逻辑计算 → 完成检测 → DATA 消费 → NULL → 准备下一轮
```

**没有时钟，只有数据流。**

---

## 二、NCL 的四态编码（双轨 Dual-Rail）

传统逻辑用 1 bit = 1 wire (0 或 1)。NCL 用 **2 wires = 1 bit**：

```
DATA0  DATA1  含义
──────────────────
  0      0    NULL (无数据)
  1      0    DATA = 0
  0      1    DATA = 1
  1      1    INVALID (禁止)
```

这意味着每个信号有 **三种合法状态**：NULL、DATA0、DATA1。

### 为什么需要 NULL？

NULL 是"数据已被消费，管道空闲"的信号。在同步电路中，这是时钟沿做的事。在 NCL 中，NULL 从一个流水线级传播到下一级，形成**自定时流水线**。

---

## 三、NCL 流水线（四相握手）

```
Phase 1 (DATA): 输入 DATA → 组合逻辑计算 → 输出 DATA
Phase 2 (NULL): 输入 NULL → 组合逻辑复位  → 输出 NULL
Phase 3 (DATA): 输入 DATA → ...
Phase 4 (NULL): 输入 NULL → ...
```

### 与同步流水线的对比

| 特性 | 同步 (时钟) | NCL (异步) |
|------|-----------|-----------|
| 时序控制 | 全局时钟 | 本地握手 |
| 最慢路径 | 关键路径决定频率 | 每级独立, 快者快慢者慢 |
| 功耗 | 时钟树功耗 ~30% | 仅活动部分耗电 |
| EMI | 同步开关噪声 | 分布式, EMI 低 |
| 设计复杂度 | 低 | 高 |
| 吞吐 | 固定 | 自适应 (data-dependent) |

---

## 四、NCL 阈值门（关键电路原语）

### TH22 (Muller C-gate, 二输入C单元)

```
TH22: 两个输入都为 DATA  → 输出 DATA
      两个输入都为 NULL  → 输出 NULL
      其他               → 保持上一个状态 (迟滞)
```

这是 NCL 的**最基本单元**，实现了"等所有输入都到了再输出"的完成检测。

### THmn (m-of-n 阈值门)

```
TH34w2: 4 输入中 3 个为 DATA, 其中 1 个有权重 2 → 输出 DATA
```

### 在 SDI v24 中的应用

```
NCLRail: 双轨线的 Python 模型
  - data0, data1: 两个布尔信号
  - is_null: data0==False and data1==False
  - is_data: data0 XOR data1
  - value: 0 或 1 或 None (NULL)

NCLThresholdGate: 阈值门的 Python 模型
  - evaluate(inputs): data_count >= threshold → DATA, all null → NULL

NCLPipelineStage: 流水线级
  - 输入寄存器 → 组合逻辑 → 输出寄存器 → 完成检测
```

---

## 五、为什么 NCL 适合脉冲神经网络硬件

### 1. 天然匹配脉冲时序

脉冲到达时间不确定 → NCL 不依赖时钟 → 每个脉冲"到达即处理"

### 2. 事件驱动 = 低功耗

```
同步: 每 ns 都在耗电 (时钟一直在跑)
NCL:  只在脉冲到达时耗电
```

脑皮层功耗 ~20W → 事件驱动是关键。NCL 在硅上实现类似机制。

### 3. 自适应流水线深度

```
级联传播: 信号传播深度可变 (0-15 层)
同步: 按最深路径预留时间 → 浅传播时浪费
NCL: 浅传播时自动更快 → 平均吞吐更高
```

### 4. 低 EMI

同步电路在时钟沿同时翻转 → 巨大 di/dt → 电磁干扰  
NCL 各模块独立翻转 → 分布均匀 → EMI 低 20-40dB

---

## 六、NCL → FPGA 映射策略

### 问题：FPGA 是为同步设计的

FPGA 内置了专用时钟网络、DSP、BRAM——都是同步接口。

### 解决方案：门控时钟等效

```
NCL 的"自定时"在 FPGA 上的实现:

1. 顶层模块仍有时钟 (clk_equiv = 200MHz)
2. 各 NCL 流水线级用 clk_equiv 采样本地握手信号
3. 当且仅当 "输入 DATA 且 输出被消费为 NULL" 时, 本级才工作

等价于: 每个流水线级有自己的门控时钟, 由数据流自动开关
```

Vivado 支持 `gated_clock` 约束和 `CLOCK_DEDICATED_ROUTE=FALSE` 来模拟 NCL 行为。

---

## 七、NCL 的局限性

| 局限 | 说明 | 缓解 |
|------|------|------|
| 面积开销 | 双轨编码 = 2× wiring | 仅数据路径, 控制路径仍用单轨 |
| 设计复杂度 | 握手协议的验证困难 | 用 Python 行为级先验证 |
| 工具链 | EDA 工具为同步优化 | Xilinx UG901 支持异步约束 |
| 测试 | 无时钟 → 扫描链困难 | 插入观察点, 用流水线暂停 |

---

## 八、在 SDI v24/v28 架构中的映射

```
Python 仿真层:
  NCLRail           → 双轨脉冲信号
  NCLThresholdGate  → 突触输入的完成检测
  NCLPipelineStage  → FEP 自由能计算流水线 (4 级)

Verilog RTL 层:
  sdio_bond_core_v24.v:
    pre_data0, pre_data1    → NCL 输入双轨
    post_data0, post_data1  → NCL 输出双轨
    done                    → 完成检测信号 (pre_valid XOR post_valid)

FPGA 物理层:
  VCK190:
    进位链 (CARRY4)     → 可变延迟线 (tau 控制器)
    LUTRAM              → 盆地最小值存储
    DSP48               → FEP 调制乘法
    BRAM                → 惊讶度历史
```

---

## 九、与传统神经形态芯片的比较

| 芯片 | 时钟策略 | 与 NCL 的关系 |
|------|---------|-------------|
| Intel Loihi 2 | 异步设计 + 同步 mesh | 片上异步核, 核间同步 mesh |
| IBM TrueNorth | 同步 (1kHz 慢时钟) | 用低时钟模拟异步 |
| SynSense DYNAP-SE2 | 完全异步 | 最接近原始 NCL 哲学 |
| **SDI v24 (本文)** | **NCL 异步流水线** | 直接在 FPGA 上实现 NCL |

### 核心差异

Loihi/TrueNorth 使用**固定神经元模型** (LIF, Izhikevich)。  
SDI 使用**自由能驱动的自演化突触**——没有固定的神经元动力学，只有 FEP 最小化的目标函数。  
NCL 是实现这种自演化硬件的**天然匹配范式**。

---

## 十、参考资料

- Fant & Brandt 1996. "NULL Convention Logic: A Complete And Consistent Logic For Asynchronous Digital Circuit Synthesis." *Proc Intl Conf Application Specific Systems*
- Smith & Di 2009. "Designing Asynchronous Circuits using NULL Convention Logic." *Synthesis Lectures on Digital Circuits*
- Sparsø & Furber 2001. "Principles of Asynchronous Circuit Design"
- Xilinx UG901: Vivado Synthesis Guide (gated clock, async constraints)

---

*独立参考文件 | iNEST Research Team | 2026-06-03*
