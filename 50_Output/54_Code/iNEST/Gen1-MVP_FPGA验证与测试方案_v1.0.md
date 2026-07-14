---
title: "Gen1-MVP智涌脑 FPGA验证与测试方案"
date: 2026-06-18
version: v1.0
status: Final
author: iNEST Engineering Team (天津大学/NDSC)
target_hardware: Xilinx VCK190 (Versal ACAP)
tags:
  - FPGA验证
  - 测试方案
  - Gen1-MVP
  - 自动化测试
  - 行为验证
  - CST验证
  - 性能评测
---

# Gen1-MVP智涌脑 FPGA验证与测试方案 v1.0

> **目标**：建立从模块级到系统级、从功能到性能、从仿真对标到行为涌现的完整验证体系。确保Gen1-MVP在2027 Q4交付时满足M0/M1里程碑的全部成功标准。

---

## 一、验证层次架构

```
Level 0: 单元测试 (Unit Test)         — 每个IP核独立验证
Level 1: 模块集成测试 (Integration)    — 模块间接口验证
Level 2: 子系统测试 (Sub-system)       — FEP+CST+SOC协同验证
Level 3: 全系统功能测试 (System)       — 完整的感知→行为链路
Level 4: 性能基准测试 (Performance)    — 延迟/吞吐/功耗/资源
Level 5: 仿真对标测试 (Fidelity)       — 硬件实测 vs 软件仿真
Level 6: 行为涌现测试 (Emergence)      — L1-L6智能跃迁验证
```

---

## 二、Level 0: 单元测试

### 2.1 IP核单元测试清单

| IP核 | 测试项 | 测试方法 | 通过标准 | 优先级 |
|------|--------|---------|---------|--------|
| `sdio_crossbar_4x4` | 单键连接/断裂 | cocotb + 波形检查 | 脉冲正确路由, 延迟<5ns | P0 |
| `sdio_crossbar_4x4` | AXI4-Lite读写 | cocotb寄存器测试 | 所有寄存器读写正确 | P0 |
| `sdio_crossbar_4x4` | 拓扑切换 | 写入→验证→断言 | 切换延迟<10μs | P0 |
| `sdio_crossbar_4x4` | 全连接压力测试 | 16键×100K脉冲 | 无丢包, 吞吐达标 | P1 |
| `sdio_bond_core_v24` | NCL握手协议 | 波形检查 (已通过) | 双轨握手正确 | ✅ |
| `sdio_bond_core_v24` | LTP/LTD计数 | 定向脉冲注入→计数验证 | 计数误差=0 | P0 |
| `sdio_bond_core_v24` | FEP增益调制 | fep_converged切换→增益变 | 增益切换<5ns | P1 |
| `pe_neuron_array` | 75神经元并行发放 | 随机脉冲注入→输出验证 | 无死锁, 发放率正确 | P0 |
| `pe_neuron_array` | Bond仲裁 | 多键同时输出→仲裁正确 | Round-robin公平性 | P1 |
| `fep_engine_top` | KL散度计算 | 已知分布→计算结果对比 | 误差<1% (vs Python参考) | P0 |
| `fep_engine_top` | 收敛检测 | 输入收敛序列→检测正确 | 检测延迟<3周期 | P1 |
| `cst_estimator` | S_c计算 | 已知拓扑→计算结果对比 | 误差<5% (vs CST-Meter) | P0 |
| `cst_estimator` | σ计算 | 已知图→σ值对比 | 误差<3% | P0 |
| `cst_estimator` | 相变检测 | CST序列→phase正确 | 检测准确率>95% | P1 |
| `stdp_bcm_accel` | BCM阈值更新 | 固定输入→阈值收敛验证 | 收敛值误差<2% | P1 |
| `soc_controller` | 缩放事件生成 | σ偏差→scale调整 | 反馈方向正确 | P1 |
| `adaptive_tau_ctrl` | 惊讶度→tau映射 | 输入sweep→tau输出 | 查表正确 | P1 |

### 2.2 单元测试自动化框架

```python
# test_sdio_crossbar.py — cocotb单元测试示例

import cocotb
from cocotb.triggers import Timer, RisingEdge
from cocotb.clock import Clock

@cocotb.test()
async def test_single_bond_route(dut):
    """测试单键脉冲路由"""
    # 初始化
    clock = Clock(dut.clk, 5, units="ns")  # 200MHz
    cocotb.start_soon(clock.start())

    dut.rst_n.value = 0
    await Timer(20, units="ns")
    dut.rst_n.value = 1

    # 配置键: PE0_port0 → PE1_port0
    await axi_write(dut, addr=0x10, value=0x0001_0041)  # src=0,dst=1,en=1
    await axi_write(dut, addr=0x00, value=0x0000_0001)  # enable

    # 发送测试脉冲
    dut.spike_in.value = 0x0001  # PE0_port0 = 1
    await Timer(5, units="ns")

    # 验证路由
    assert dut.spike_out.value == 0x0001_0000, f"路由错误: {dut.spike_out.value}"


@cocotb.test()
async def test_topology_switch_timing(dut):
    """测试拓扑切换延迟 (目标<10μs)"""
    # 配置初始拓扑
    await configure_topology(dut, "ring")

    # 记录切换开始时间
    start_time = cocotb.utils.get_sim_time(units="ns")
    await configure_topology(dut, "butterfly")

    # 等待切换完成
    await RisingEdge(dut.sdi_ready)
    switch_time = cocotb.utils.get_sim_time(units="ns") - start_time

    assert switch_time < 10_000, f"切换延迟{switch_time}ns > 10μs目标"
```

---

## 三、Level 1-2: 集成与子系统测试

### 3.1 集成测试清单

| 测试 | 集成模块 | 验证点 | 方法 |
|------|---------|--------|------|
| INT-01 | PE → Crossbar → PE | 跨PE脉冲路由正确性 | 4 PE同时发送, 验证路由 |
| INT-02 | PE → FEP Engine | FEP数据采集完整性 | 300神经元收敛→FEP读取 |
| INT-03 | PE → CST Estimator | CST数据采集完整性 | 运行100ms→CST值稳定 |
| INT-04 | FEP → SOC → PE | 闭环: FEP收敛→SOC缩放→PE响应 | 注入惊讶度变化→scale响应 |
| INT-05 | CST → SOC → PE | 闭环: σ偏差→缩放→σ恢复 | 人为降低连接→SOC恢复 |
| INT-06 | Sensor I/F → PE | 真实传感器→脉冲编码→PE注入 | MIPI帧→PE0脉冲流 |

### 3.2 子系统协同验证

```python
# test_fep_cst_soc_closed_loop.py

def test_fep_convergence_triggers_soc():
    """验证FEP收敛→SOC缩放→PE响应闭环"""
    brain = connect_to_fpga()

    # 1. 初始状态: FEP未收敛
    assert brain.fep.converged == False

    # 2. 运行直到FEP收敛
    brain.run_until(lambda: brain.fep.converged, timeout_s=10)

    # 3. 验证SOC收到FEP收敛信号
    assert brain.soc.scale_factor != 1.0, "SOC应调整缩放因子"

    # 4. 验证PE响应缩放
    pe0_spike_rate_before = brain.pe[0].spike_rate
    brain.wait(1.0)  # 等待SOC生效
    pe0_spike_rate_after = brain.pe[0].spike_rate
    assert pe0_spike_rate_after != pe0_spike_rate_before


def test_cst_sigma_deviation_triggers_soc_recovery():
    """验证σ偏差→SOC恢复闭环"""
    brain = connect_to_fpga()
    brain.soc.configure(sigma_target=4.0, auto_scale=True)

    # 基线
    sigma_0 = brain.cst.sigma

    # 人为降低连接密度 (减少键数)
    brain.bond_manager.prune_bonds(ratio=0.5)
    brain.wait(0.5)
    sigma_1 = brain.cst.sigma
    assert sigma_1 < sigma_0, "剪枝应降低σ"

    # 等待SOC自动恢复
    brain.wait(5.0)  # SOC周期100ms, 50次迭代
    sigma_2 = brain.cst.sigma

    # 验证恢复趋势
    assert sigma_2 > sigma_1, f"SOC应恢复σ: {sigma_1}→{sigma_2}"
```

---

## 四、Level 3: 全系统功能测试

### 4.1 端到端感知→行为链路

```
测试场景: 光趋性 (phototaxis)
┌─────────────────────────────────────────────────────────────┐
│  Step 1: 传感器输入                                         │
│  MIPI相机 → 亮度编码 → 脉冲注入PE0 (视觉区)                  │
│                                                              │
│  Step 2: 感知处理                                           │
│  PE0 (75N) → Crossbar → PE2 (75N 联合皮层)                  │
│  视觉脉冲在网络中传播+整合                                    │
│                                                              │
│  Step 3: 决策                                               │
│  PE2 → Crossbar → PE3 (75N 运动区)                          │
│  联合皮层输出驱动运动神经元                                    │
│                                                              │
│  Step 4: 行为输出                                           │
│  PE3 脉冲解码 → 运动指令 (左转/右转/前进)                     │
│                                                              │
│  验证指标: 光趋性>80% (对标V29仿真81.1%)                      │
└─────────────────────────────────────────────────────────────┘
```

### 4.2 功能测试清单

| 测试 | 场景 | 输入 | 预期输出 | 对标仿真 |
|------|------|------|---------|---------|
| **FUNC-01** | 光趋性 | 单光源, 4方向 | 趋光>80% | V29: 81.1% |
| **FUNC-02** | 化趋性 | 化学梯度 | 趋化>75% | V29: 78.6% |
| **FUNC-03** | 模式补全 | 部分遮挡图案 | 完整识别>95% | V29: 100% |
| **FUNC-04** | 避障 | 障碍物出现 | 转向>85% | L6: 避障5.5x |
| **FUNC-05** | 多模融合 | 视觉+IMU同时输入 | 正确联合决策 | V30: 多脑区 |
| **FUNC-06** | 在线学习 | 新刺激类型 | 自适应>50次暴露 | V9: FEP收敛 |
| **FUNC-07** | 键自组织 | 初始随机拓扑 | σ→≥2.0 (MVP) | V8-V28 |
| **FUNC-08** | 涌现检测 | 运行中CST监控 | 相变事件记录 | CST Estimator |

---

## 五、Level 4: 性能基准测试

### 5.1 性能KPIs

| KPI | 目标 (MVP) | 目标 (Gen1) | 测量方法 | 优先级 |
|-----|-----------|------------|---------|--------|
| **σ (小世界指数)** | ≥2.0 | ≥4.0 | CST Estimator读取 | P0 |
| **EL (E-L比)** | ≥15% | ≥15% | Bond Stats寄存器 | P0 |
| **拓扑切换延迟** | <10μs | <1μs | ILA波形测量 | P0 |
| **脉冲路由延迟** | <5ns | <5ns | ILA波形测量 | P0 |
| **FEP更新频率** | >1kHz | >10kHz | 定时器计数 | P0 |
| **CST估算延迟** | <1ms | <100μs | 定时器计数 | P1 |
| **功耗/神经元** | <1mW | <1mW | 电流探头 | P1 |
| **最大脉冲吞吐** | >10M spikes/s | >40M spikes/s | 计数器 | P1 |
| **自由能收敛时间** | <10s | <1s | FEP监控 | P2 |
| **FPGA资源利用率** | <75% LUT | — | Vivado报告 | P0 |

### 5.2 性能基准测试自动化

```python
# perf_benchmark.py

def benchmark_topology_switch():
    """测试拓扑切换延迟"""
    brain = connect_to_fpga()
    results = []

    for topo in ["ring", "butterfly", "star", "all_to_all"]:
        for _ in range(100):  # 100次测试
            t_start = brain.get_hw_timestamp()
            brain.configure_topology(topo)
            brain.wait_ready()
            t_end = brain.get_hw_timestamp()
            results.append(t_end - t_start)

    return {
        "mean_ns": np.mean(results),
        "p99_ns": np.percentile(results, 99),
        "max_ns": np.max(results),
        "pass": np.max(results) < 10_000  # <10μs
    }


def benchmark_cst_estimation():
    """测试CST估算延迟"""
    brain = connect_to_fpga()
    brain.cst.configure(continuous_mode=True, update_period=1)  # 最快

    results = []
    for _ in range(1000):
        t_start = brain.get_hw_timestamp()
        cst = brain.cst.read()
        results.append(brain.get_hw_timestamp() - t_start)
        time.sleep(0.001)

    return {
        "mean_us": np.mean(results) / 1000,
        "p99_us": np.percentile(results, 99) / 1000,
        "pass": np.mean(results) / 1000 < 1000  # <1ms
    }


def benchmark_power():
    """功耗测量 (需要外部电流探头)"""
    brain = connect_to_fpga()

    # 空闲功耗
    brain.idle()
    p_idle = measure_power()

    # 全负载功耗 (所有PE满负荷发放)
    brain.stress_test(duration_s=10)
    p_load = measure_power()

    return {
        "p_idle_mw": p_idle,
        "p_load_mw": p_load,
        "p_per_neuron_uw": (p_load / 300) * 1000,
        "pass": (p_load / 300) < 1.0  # <1mW/neuron
    }
```

---

## 六、Level 5: 仿真对标测试 (Fidelity)

### 6.1 软件仿真 vs 硬件实测 对标矩阵

| 指标 | 软件仿真 (V8-V28) | 硬件实测目标 | 允许偏差 | 对标方法 |
|------|------------------|------------|---------|---------|
| σ (小世界) | 4.0 (无标度) | 3.5-4.5 | ±12.5% | CST-Meter vs CST Estimator |
| EL (E-L比) | 自稳定 | 15%-25% | — | Bond矩阵统计 vs 仿真记录 |
| 自由能趋势 | 单调递减 (V9) | 单调递减 | 趋势一致 | FEP Engine vs V9结果 |
| 发放率 | 仿真值 | 仿真值±20% | ±20% | PE stats vs 仿真 |
| 收敛时间 | V8-V28稳定 | 硬件自稳定时间 | 可比范围 | SOC收敛 vs 仿真收敛 |
| 雪崩规模分布 | 幂律 (V11) | 幂律α≈1.5 | ±0.2 | 硬件雪崩数据 vs 仿真 |

### 6.2 对标验证流程

```
1. 取已完成的仿真结果 (如V28: σ=4.0, 无标度拓扑)
2. 以相同初始条件配置硬件
   - 相同拓扑类型
   - 相同初始键数/连接密度
   - 相同STDP/BCM/FEP参数
3. 运行硬件N秒, 采集全部CST/FEP/键统计数据
4. 将硬件数据转换为仿真可读格式 (HDF5)
5. 使用CST-Meter统一分析软硬件数据
6. 计算偏差矩阵: |HW - SIM| / SIM
7. 判定: 关键指标偏差<20% → 对标通过
```

---

## 七、Level 6: 行为涌现测试 (M0/M1里程碑)

### 7.1 M0里程碑测试 (2027 Q3)

| 测试项 | 成功标准 | 验证方法 |
|--------|---------|---------|
| **M0.1** | σ≥2.0 (MVP目标) | CST Estimator连续10次采样均值 |
| **M0.2** | EL≥15% (键生成/断裂比) | Bond Stats 100ms窗口统计 |
| **M0.3** | FEP自由能单调递减 | FEP Engine 10s趋势分析 |
| **M0.4** | 拓扑切换延迟<10μs | ILA 100次测量p99 |
| **M0.5** | 无死锁运行>1小时 | 持续运行+定时心跳检测 |

### 7.2 M1里程碑测试 (2027 Q4)

| 测试项 | 成功标准 | 验证方法 |
|--------|---------|---------|
| **M1.1** | σ≥4.0 (Gen1感知级目标) | 同M0.1 |
| **M1.2** | 光趋性>80% (对标V29: 81.1%) | FUNC-01: 4方向×100次试验 |
| **M1.3** | 化趋性>75% (对标V29: 78.6%) | FUNC-02: 梯度场×100次 |
| **M1.4** | 模式补全>95% (对标V29: 100%) | FUNC-03: 10图案×每个50次 |
| **M1.5** | 24小时稳定性运行 | 持续运行+每小时CST快照 |
| **M1.6** | 功耗<5W (FPGA) / <1W (ASIC预测) | 电流探头测量 |

### 7.3 行为涌现演示方案

```
Demo 1: 线虫级光趋性 (30秒)
├── 展示: 4方向光源 → 智涌脑实时决策方向
├── 可视化: CST实时曲线 (展示从亚临界→临界的过程)
└── 对标: V29仿真81.1%光趋性

Demo 2: 拓扑自组织 (60秒)
├── 展示: 初始随机拓扑 → 20s自组织 → 无标度拓扑 (σ从1.5→4.0)
├── 可视化: 键矩阵热力图变化动画
└── 对标: V8-V28仿真

Demo 3: 自由能收敛 (15秒)
├── 展示: FEP Engine输出 → 自由能从2.0单调降至0.1
├── 可视化: F vs t 实时曲线
└── 对标: V9仿真

Demo 4: 涌现相变检测 (持续)
├── 展示: CST Estimator在线检测相变
├── 可视化: 相态指示灯 (蓝=亚临界, 绿=临界, 红=超临界)
└── 对标: CST-Meter离线分析
```

---

## 八、测试基础设施

### 8.1 测试平台架构

```
┌─────────────────────────────────────────────────────────────┐
│                    测试平台 (Test Bench)                      │
│                                                              │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐               │
│  │ Host PC  │   │ VCK190   │   │ 示波器    │               │
│  │          │   │ (DUT)    │   │ (Keysight)│               │
│  │ • Python │◄──┤ UART     ├──►│ • 延迟测量│               │
│  │ • cocotb │   │          │   │ • 功耗测量│               │
│  │ • CST-   │   │ ┌──────┐ │   │ • 波形捕获│               │
│  │   Meter  │   │ │iNEST │ │   └──────────┘               │
│  │ • 日志   │   │ │Gen1  │ │                               │
│  │          │   │ │MVP   │ │   ┌──────────┐               │
│  │          │   │ └──────┘ │   │ 信号发生器│               │
│  │          │   │          │   │          │               │
│  │          │◄──┤ JTAG     │   │ • 传感器 │               │
│  │          │──►│ (ILA)    │   │   模拟   │               │
│  └──────────┘   └──────────┘   └──────────┘               │
│                                                              │
│  自动化测试流水线:                                            │
│  Python Orchestrator → Vivado ILA → UART → 数据采集         │
│                          ↓                                   │
│                    CST-Meter 离线分析                         │
│                          ↓                                   │
│                    测试报告生成 (HTML/PDF)                    │
└─────────────────────────────────────────────────────────────┘
```

### 8.2 测试设备清单

| 设备 | 用途 | 型号 | 数量 |
|------|------|------|------|
| FPGA开发板 | DUT | Xilinx VCK190 | 2 |
| 高速示波器 | 时序/延迟测量 | Keysight MSOX6004A | 1 |
| 电流探头 | 功耗测量 | Keysight N7020A | 1 |
| 信号发生器 | 传感器模拟 | Rigol DG4162 | 1 |
| MIPI摄像头 | 真实传感器输入 | Raspberry Pi Camera v3 | 2 |
| IMU模块 | 真实传感器输入 | ICM-20948 | 1 |
| Host PC | 控制+分析 | 工作站 (64GB RAM) | 1 |

---

## 九、开发与验证时间线

```
2026 Q3:  ┌─ Bond Core v24 强化验证 ◄── 已完成IP验证
          ├─ Crossbar RTL + 单元测试
          └─ Python验证框架搭建 (cocotb)

2026 Q4:  ├─ PE Neuron Array RTL + 单元测试
          ├─ FEP Engine RTL + 单元测试
          └─ 集成测试 INT-01 (PE→Crossbar→PE)

2027 Q1:  ├─ CST Estimator RTL + 单元测试
          ├─ SOC/STDP/BCM RTL
          ├─ 全系统集成仿真 (Level 3)
          └─ 子系统闭环验证 (Level 2)

2027 Q2:  ├─ Vivado综合+布局布线迭代
          ├─ 时序收敛 (200MHz)
          ├─ 片上调试 (ILA)
          └─ Level 4 性能基准测试

2027 Q3:  ├─ 仿真对标测试 (Level 5)
          ├─ M0里程碑测试 ⚠️ 关键节点
          └─ 迭代修复+重新综合

2027 Q4:  ├─ 行为涌现测试 (Level 6)
          ├─ M1里程碑测试 ⚠️ 交付节点
          ├─ Demo视频录制
          └─ Gen1 ASIC 28nm流片启动
```

---

## 附录：测试报告模板

```markdown
# Gen1-MVP 测试报告 — M0里程碑

**日期**: 2027-XX-XX
**硬件**: Xilinx VCK190, 位流版本 vX.X
**测试工程师**: XXX

## M0.1: σ ≥ 2.0
- 测试方法: CST Estimator 连续10次采样
- 结果: [σ₁, σ₂, ..., σ₁₀]
- 均值: X.XX
- 判定: ✅ PASS / ❌ FAIL

## M0.2: EL ≥ 15%
- 测试方法: Bond Stats 100ms窗口统计
- E-S键数: XXX, E-L键数: XXX
- EL比: XX.X%
- 判定: ✅ PASS / ❌ FAIL

## M0.3: FEP自由能单调递减
- 测试方法: FEP Engine 10s趋势
- 起始F: X.XX, 结束F: X.XX
- 趋势: 递减/非递减
- 判定: ✅ PASS / ❌ FAIL

... (其他M0项)

## 总结
- 通过项: X/5
- M0判定: ✅ PASS / ❌ FAIL
- 备注: XXX
```
