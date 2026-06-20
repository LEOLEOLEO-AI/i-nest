---
title: "智涌脑软件栈：iNEST SDK/编译器/运行时 完整架构"
date: 2026-06-18
version: v1.0
status: Final
author: iNEST Engineering Team (复旦大学/天津大学)
tags:
  - iNEST
  - 软件栈
  - SDK
  - 编译器
  - 运行时
  - Python API
  - CST-Meter
  - 开发流程
---

# 智涌脑软件栈：iNEST SDK/编译器/运行时 完整架构 v1.0

> **定位**：让开发者不需要理解CST公式、不需要写Verilog、不需要知道SDI寄存器映射——就能在智涌脑上部署涌现智能应用。

---

## 一、软件栈全景

```
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Sensor   │  │ Anomaly  │  │ Drone    │  │ Robot    │  │
│  │ Fusion   │  │ Detection│  │ Nav      │  │ Control  │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘  │
├───────┼─────────────┼─────────────┼─────────────┼────────┤
│                    Python SDK Layer                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              iNEST Python SDK (inest)                  │  │
│  │                                                        │  │
│  │  from inest import WisdomBrain, BondConfig, CSTMonitor │  │
│  │                                                        │  │
│  │  brain = WisdomBrain(gen="Gen1-MVP", neurons=300)      │  │
│  │  brain.configure_topology("butterfly")                 │  │
│  │  brain.connect_sensor("MIPI", port=0)                  │  │
│  │  cst = brain.monitor.cst_score                         │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                               │
├──────────────────────────────┼──────────────────────────────┤
│                    Compiler Layer                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         iNEST Compiler (inestc)                        │  │
│  │                                                        │  │
│  │  Application Graph ──▶ Topology Plan ──▶ SDI Config    │  │
│  │                                                        │  │
│  │  • Topology Selection: Ring|Butterfly|SmallWorld|Custom│  │
│  │  • NEAT (NeuroEvolution): 自动拓扑搜索                 │  │
│  │  • CST-driven: 基于CST值的拓扑自适应                   │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                               │
├──────────────────────────────┼──────────────────────────────┤
│                    Runtime Layer                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         iNEST Runtime (inestr)                         │  │
│  │                                                        │  │
│  │  • CST Loop: 定时CST采样 → 相变检测 → 自适应调整       │  │
│  │  • FEP Loop: 自由能最小化 → 拓扑优化建议               │  │
│  │  • SOC Loop: 缩放事件生成 → 临界态维持                 │  │
│  │  • Bond Manager: 键创建/断裂/固化 运行时管理            │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                               │
├──────────────────────────────┼──────────────────────────────┤
│                    Driver / HAL Layer                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  • AXI4-Lite Driver: SDI/FEP/CST寄存器读写            │  │
│  │  • UART Driver: 调试+遥测                             │  │
│  │  • Sensor Driver: MIPI/SPI/I2S 数据采集               │  │
│  │  • DMA Driver: 脉冲数据高速传输                        │  │
│  └──────────────────────────────────────────────────────┘  │
│                              │                               │
├──────────────────────────────┼──────────────────────────────┤
│                    Hardware Layer                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │   Gen1-MVP FPGA / Gen2-5 ASIC (AXI4-Lite + UART)      │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 二、iNEST Python SDK (`inest`)

### 2.1 核心API

```python
# === 智涌脑设备管理 ===

from inest import WisdomBrain, GenVersion, TopologyType

# 初始化智涌脑 (自动检测硬件代次)
brain = WisdomBrain(transport="uart", port="/dev/ttyUSB0")
# 或显式指定
brain = WisdomBrain(gen=GenVersion.GEN1_MVP, transport="axi")

# 设备信息
print(brain.info())
# {
#   "gen": "Gen1-MVP",
#   "neurons": 300,
#   "pe_count": 4,
#   "sdi_ports": 16,
#   "clock_mhz": 200,
#   "firmware_version": "0.9.0"
# }


# === 拓扑配置 ===

from inest import BondConfig, TopologyType

# 方法1: 预设拓扑
brain.configure_topology(TopologyType.BUTTERFLY)
brain.configure_topology(TopologyType.RING)
brain.configure_topology(TopologyType.SMALL_WORLD, rewiring_p=0.1)
brain.configure_topology(TopologyType.SCALE_FREE, m=3)
brain.configure_topology(TopologyType.ALL_TO_ALL)

# 方法2: 自定义键配置
bonds = BondConfig()
bonds.add_bond(src_pe=0, src_neuron=10, dst_pe=1, dst_neuron=25, direction="uni")
bonds.add_bond(src_pe=0, src_neuron=11, dst_pe=3, dst_neuron=50, direction="bi")
brain.configure_bonds(bonds)

# 方法3: 从NetworkX图加载
import networkx as nx
G = nx.watts_strogatz_graph(300, k=10, p=0.05)
bonds = BondConfig.from_networkx(G, neurons_per_pe=75)
brain.configure_bonds(bonds)


# === 运行时监控 ===

from inest import CSTMonitor, FEPMonitor

# CST实时监控
cst_mon = CSTMonitor(brain, sample_period_ms=100)
cst_mon.start()

@cst_mon.on_phase_change
def on_phase(old_phase, new_phase, cst_score):
    print(f"涌现相变: {old_phase} → {new_phase}, CST={cst_score:.3f}")
    if new_phase == "critical":
        print("🎯 进入临界态！")

# 读取CST值
sigma = cst_mon.sigma          # 小世界指数
s_c   = cst_mon.s_c            # 空间复杂度
t_c   = cst_mon.t_c            # 时间复杂度
cst   = cst_mon.cst_score      # CST综合分数
phase = cst_mon.phase          # "subcritical"|"critical"|"supercritical"

# FEP监控
fep_mon = FEPMonitor(brain)
free_energy = fep_mon.free_energy
converged    = fep_mon.converged
kl_div       = fep_mon.kl_divergence


# === 学习参数配置 ===

brain.stdp.configure(
    ltp_rate=1.4,      # LTP增强系数
    ltd_rate=0.6,      # LTD抑制系数
    enable=True
)

brain.bcm.configure(
    theta=15.0,        # BCM滑动阈值
    eta=0.25,          # BCM学习率
    theta_ltp=14.0,    # 固化阈值
)

brain.soc.configure(
    sigma_target=4.0,  # Gen1感知级σ目标
    scale_period_ms=100,
    auto_scale=True
)

brain.fep.configure(
    convergence_thresh=0.01,
    update_period_ms=1,
    prior_mean=0.5,
    prior_var=0.1
)


# === 传感器接口 ===

brain.sensor.mipi.configure(
    resolution=(640, 480),
    fps=30,
    format="RAW8"
)

brain.sensor.spi.configure(
    device="IMU",
    sample_rate_hz=200
)

# 读取传感器数据（自动转换为脉冲编码）
for frame in brain.sensor.mipi.stream():
    spikes = brain.encode_sensory(frame, modality="vision")
    brain.inject_spikes(spikes, target_pe=0)

# 读取输出（motor PE）
motor_activity = brain.read_output(pe=3, neurons=range(75))


# === 持久化 ===

# 保存键配置+权重（"检查点"）
brain.save_checkpoint("my_brain_20260618.inest")

# 加载
brain.load_checkpoint("my_brain_20260618.inest")

# 导出分析数据
brain.export_analytics("session_log.h5")  # CST/FEP/键统计
```

### 2.2 SDK内部架构

```
Python SDK (inest)
│
├── core/
│   ├── wisdom_brain.py     # WisdomBrain 主类
│   ├── bond_config.py      # BondConfig 键配置
│   ├── checkpoint.py       # 检查点保存/加载
│   └── version.py          # 代次枚举+兼容性检查
│
├── monitor/
│   ├── cst_monitor.py      # CSTMonitor (定时采样+相变检测)
│   ├── fep_monitor.py      # FEPMonitor (自由能监控)
│   └── soc_monitor.py      # SOCMonitor (临界态维持监控)
│
├── compile/
│   ├── topology_selector.py  # 拓扑选择策略
│   ├── neat_optimizer.py     # NEAT自动拓扑搜索
│   └── cst_optimizer.py      # CST驱动优化
│
├── runtime/
│   ├── cst_loop.py         # CST采样循环
│   ├── fep_loop.py         # FEP自由能循环
│   ├── soc_loop.py         # SOC缩放循环
│   └── bond_manager.py     # 键生命周期管理
│
├── transport/
│   ├── uart.py             # UART传输层
│   ├── axi.py              # AXI4-Lite传输层
│   └── jtag.py             # JTAG调试传输层
│
├── sensor/
│   ├── mipi.py             # MIPI相机接口
│   ├── spi_imu.py          # SPI IMU接口
│   ├── i2s_mic.py          # I2S麦克风接口
│   └── encoder.py          # 传感器→脉冲编码
│
└── cli/
    ├── inest_cli.py        # 命令行工具
    └── dashboard.py        # 实时监控面板
```

---

## 三、iNEST Compiler (`inestc`)

### 3.1 编译流程

```
Application Graph ──▶ Topology Plan ──▶ SDI Configuration
     │                     │                    │
     ▼                     ▼                    ▼
 数据流图               最优拓扑            寄存器写入序列
(DAG: sensor→PE→motor)  (Ring/Butterfly/..)  (AXI4-Lite bursts)

编译三阶段:

Stage 1: Graph Analysis (图分析)
├── 输入: 应用数据流图 (DAG)
├── 分析: 通信模式 (unicast/multicast/allreduce/流水线)
├── 分析: 关键路径延迟
└── 输出: 通信需求规格 (bandwidth, fanout, latency per edge)

Stage 2: Topology Selection (拓扑选择)
├── 方法1: 模板匹配
│   └── Ring→流水线, Butterfly→AllReduce, Star→广播, Mesh→局部通信
├── 方法2: NEAT自动搜索
│   └── 遗传算法: 种群=拓扑变体, 适应度=CST_score×task_performance
├── 方法3: CST驱动自适应
│   └── 运行时根据CST值动态调整拓扑类型
└── 输出: TopologyPlan {type, parameters, bond_map}

Stage 3: SDI Code Generation (SDI代码生成)
├── 输入: TopologyPlan
├── 键映射: 逻辑连接→物理PE端口映射
├── 路由表: 多跳路由路径计算
├── 寄存器序列: AXI4-Lite写入序列生成
└── 输出: SDI_Config {register_writes: [(addr, value), ...]}
```

### 3.2 拓扑选择策略

```python
# inestc 拓扑选择核心逻辑

class TopologySelector:
    def select(self, app_graph, cst_target=None):
        comm_pattern = self._analyze_comm_pattern(app_graph)

        if comm_pattern.is_pipeline:
            return TopologyType.RING
        elif comm_pattern.is_allreduce:
            return TopologyType.BUTTERFLY
        elif comm_pattern.is_broadcast:
            return TopologyType.STAR
        elif comm_pattern.is_local_mesh:
            return TopologyType.MESH
        elif self._needs_high_clustering:
            return TopologyType.SMALL_WORLD
        elif self._needs_hub_structure:
            return TopologyType.SCALE_FREE
        else:
            # 默认使用NEAT搜索
            return self._neat_search(app_graph)

class NEATOptimizer:
    """
    基于NEAT的自动拓扑搜索
    基因组编码: 键的存在性+方向性+初始权重
    适应度函数: f = α·CST_score + β·task_accuracy + γ·energy_efficiency
    """
    def search(self, app_graph, generations=50, population=100):
        # 1. 初始化随机拓扑种群
        # 2. 评估每个个体的适应度
        # 3. 选择-交叉-变异
        # 4. 迭代N代
        # 5. 返回最优拓扑
        pass
```

### 3.3 CLI工具

```bash
# 编译应用描述到SDI配置
inestc compile app_graph.json -o sdi_config.bin

# 自动拓扑搜索
inestc optimize app_graph.json --method neat --generations 100

# 从NetworkX图直接生成
inestc from-networkx graph.gpickle -o sdi_config.bin

# 验证SDI配置
inestc validate sdi_config.bin --hardware Gen1-MVP

# 模拟：预测配置的CST值
inestc simulate sdi_config.bin --cst-predict
```

---

## 四、iNEST Runtime (`inestr`)

### 4.1 运行时架构

```
┌─────────────────────────────────────────────────────────┐
│                  iNEST Runtime (inestr)                   │
│                                                          │
│  Main Loop (每1ms触发一次):                               │
│  ┌────────────────────────────────────────────────────┐ │
│  │  1. CST Loop: 读取CST值 → 检测相变 → 调整策略      │ │
│  │  2. FEP Loop: 读取自由能 → 检测收敛 → 触发拓扑优化  │ │
│  │  3. SOC Loop: 检测σ偏差 → 生成缩放事件 → 广播       │ │
│  │  4. Bond Manager: 键老化检测 → 创建/断裂/固化       │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  Event Loop (事件驱动):                                   │
│  ┌────────────────────────────────────────────────────┐ │
│  │  • Sensor Data Ready → Encode → Inject Spikes       │ │
│  │  • Motor Output Ready → Decode → App Callback       │ │
│  │  • Phase Change Event → Log + Notify                │ │
│  │  • Checkpoint Timer → Save Snapshot                 │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### 4.2 CST Loop 运行时伪代码

```python
class CSTLoop:
    """
    CST采样循环: 周期性采集CST指标, 检测涌现相变, 触发自适应调整
    """
    def __init__(self, brain, period_ms=100):
        self.brain = brain
        self.history = deque(maxlen=100)  # 最近100次采样

    def run(self):
        while True:
            # 1. 读取硬件CST值
            cst = self.brain.cst_estimator.read()
            self.history.append(cst)

            # 2. 相变检测
            phase = self._detect_phase(cst)
            if phase != self.current_phase:
                self._on_phase_change(phase, cst)

            # 3. 自适应调整
            if phase == "subcritical" and cst.sigma < 3.0:
                # 亚临界: 增加连接密度
                self.brain.bond_manager.grow_bonds(factor=1.2)

            elif phase == "supercritical" and cst.sigma > 8.0:
                # 超临界: 减少连接, 防止过拟合
                self.brain.bond_manager.prune_bonds(factor=0.8)

            elif phase == "critical":
                # 临界态: 维持, 不做大调整
                pass

            sleep(self.period_ms / 1000)

    def _detect_phase(self, cst):
        if cst.sigma < 3.5:
            return "subcritical"
        elif 3.5 <= cst.sigma <= 5.5:  # Gen1目标
            return "critical"
        else:
            return "supercritical"
```

### 4.3 Bond Manager 运行时伪代码

```python
class BondManager:
    """
    化合键生命周期管理: 创建、断裂、固化、老化
    """
    def __init__(self, brain):
        self.bonds = {}         # {bond_id: BondState}
        self.stats = BondStats()

    def tick(self):
        """每周期执行"""
        # 1. 键老化检测
        for bid, bond in list(self.bonds.items()):
            bond.age += 1
            if bond.age > bond.max_age and bond.type == "E-S":
                # E-S键超龄: 断裂
                self._break_bond(bid)

        # 2. 新键创建 (基于FEP+STDP)
        for src_neuron in self._get_active_neurons():
            for tgt_neuron in self._get_candidates(src_neuron):
                if self._meets_hebbian_condition(src_neuron, tgt_neuron):
                    self._create_bond(src_neuron, tgt_neuron, type="E-S")

        # 3. E-S→E-L 固化 (LTP计数器超过阈值)
        for bid, bond in list(self.bonds.items()):
            if bond.type == "E-S" and bond.ltp_counter >= BCM_THETA_LTP:
                self._consolidate_bond(bid)

        # 4. E-L键维护
        for bid, bond in list(self.bonds.items()):
            if bond.type == "E-L":
                
                # 衰减: LTD计数器渐进
                bond.weight *= (1 - LTD_DECAY_RATE)
                if bond.weight < MIN_WEIGHT:
                    self._break_bond(bid)

        # 5. 统计更新
        self.stats.es_count = sum(1 for b in self.bonds.values() if b.type == "E-S")
        self.stats.el_count = sum(1 for b in self.bonds.values() if b.type == "E-L")
        self.stats.el_ratio = self.stats.el_count / max(1, self.stats.es_count)
```

---

## 五、开发工作流

### 5.1 应用开发流程

```
                    ┌─────────────────────┐
                    │  1. 撰写应用描述      │
                    │  app_graph.json      │
                    │  (sensor→PE→motor)   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  2. 编译拓扑配置      │
                    │  inestc compile ...  │
                    │  → sdi_config.bin    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  3. 仿真验证（可选）   │
                    │  inest-sim run ...   │
                    │  → CST预测+性能预估  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  4. 部署到硬件        │
                    │  brain.deploy(       │
                    │    config, app)      │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  5. 运行时监控+调优   │
                    │  CSTMonitor +        │
                    │  FEPMonitor +        │
                    │  auto-tune           │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  6. 保存检查点        │
                    │  brain.save_         │
                    │  checkpoint(...)     │
                    └─────────────────────┘
```

### 5.2 快速开始示例

```python
# example_sensor_fusion.py — 端侧多模态传感器融合

from inest import WisdomBrain, TopologyType
from inest.sensor import MIPI, SPI_IMU
from inest.monitor import CSTMonitor

# 1. 初始化智涌脑
brain = WisdomBrain(gen="Gen1-MVP", transport="uart", port="/dev/ttyUSB0")

# 2. 配置拓扑
brain.configure_topology(TopologyType.SMALL_WORLD, rewiring_p=0.08)

# 3. 配置传感器
cam = MIPI(brain, port=0, resolution=(320, 240), fps=15)
imu = SPI_IMU(brain, port=1, sample_rate_hz=100)

# 4. 配置输出
brain.configure_output(pe=3, neurons=range(10), mode="motor_cmd")

# 5. 配置学习参数
brain.stdp.configure(ltp_rate=1.4, ltd_rate=0.6)
brain.bcm.configure(theta=15.0, eta=0.25)
brain.soc.configure(sigma_target=4.0, auto_scale=True)

# 6. 配置CST监控
monitor = CSTMonitor(brain, sample_period_ms=100)

@monitor.on_phase_change
def log_phase(old, new, cst):
    print(f"[{time.time():.1f}] Phase: {old}→{new}, CST={cst:.3f}")

monitor.start()

# 7. 主循环
print("智涌脑运行中... 按Ctrl+C停止")
try:
    while True:
        # 采集传感器
        frame = cam.read()
        imu_data = imu.read()

        # 编码为脉冲
        vis_spikes = brain.encode_sensory(frame, modality="vision")
        imu_spikes = brain.encode_sensory(imu_data, modality="imu")

        # 注入PE
        brain.inject_spikes(vis_spikes, target_pe=0)  # PE0=视觉区
        brain.inject_spikes(imu_spikes, target_pe=2)  # PE2=本体感知区

        # 读取输出
        cmd = brain.read_output(pe=3)  # PE3=运动区

        # 应用级处理
        handle_motor_command(cmd)

        time.sleep(0.01)  # 100Hz主循环

except KeyboardInterrupt:
    brain.save_checkpoint("fusion_brain.inest")
    print("检查点已保存。")
```

---

## 六、CST-Meter 集成

### 6.1 CST-Meter与智涌脑的协同

```
CST-Meter (离线/云端)             智涌脑 (在线/嵌入式)
│                                 │
│ 完整CST分析管道                  │ 轻量CST在线估算
│ • S_c: 完整谱分析               │ • S_c: 幂迭代近似
│ • T_c: 全尺度多尺度熵           │ • T_c: 固定尺度MSE
│ • Γ_st: 完整SVD                 │ • Γ_st: 协方差近似
│ • 可视化报告                    │ • 实时相变检测
│                                 │
│ Python包 (pip install cst-meter) │ FPGA CST IP (<1ms延迟)
│ GPU加速                          │ 硬件加速 (~30 DSP)
│ N≤16384                          │ N≤300 (Gen1-MVP)
│                                 │
├──────────── 桥接 ───────────────┤
│                                 │
│ 1. CST-Meter用于离线分析         │
│    (检查点→CST-Meter完整报告)    │
│ 2. CST-Meter参数下载到硬件        │
│    (θ_k阈值→CST Estimator配置)   │
│ 3. CST-Meter用于学术发表         │
│    (硬件实测数据→CST-Meter验证)  │
└─────────────────────────────────┘
```

---

## 七、软件栈开发里程碑

| 里程碑 | 时间 | 内容 | 状态 |
|--------|------|------|------|
| **SDK v0.1** | 2027 Q1 | 基础 Python SDK: WisdomBrain + BondConfig | **待开发** |
| **SDK v0.5** | 2027 Q2 | + CSTMonitor + FEPMonitor + 传感器驱动 | **待开发** |
| **SDK v1.0** | 2027 Q3 | + 编译器 inestc + 检查点 + CLI工具 | **待开发** |
| **Runtime v1.0** | 2027 Q3 | CST Loop + FEP Loop + SOC Loop + Bond Manager | **待开发** |
| **SDK v2.0** | 2028 Q2 | + NEAT自动搜索 + 多芯粒(G2) + PyPI发布 | **待开发** |

---

## 附录：与LNN生态的对接

| LNN组件 | iNEST对应 | 对接方式 |
|---------|---------|---------|
| `lnn.Sequential` | `WisdomBrain` | 概念级: LNN是数学抽象, 智涌脑是物理实例 |
| `lnn.LiquidNeuron` | `pe_neuron_array` | 结构映射: LNN神经元→物理神经元 |
| LNN ODE Solver | 异步脉冲电路 | 物理映射 (非数学映射) |
| LNN training loop | STDP+BCM硬件加速 | 硬件替代软件训练 |
| `lnn.save/load` | `brain.save/load_checkpoint` | 格式兼容 (+LNN→iNEST转换器) |
