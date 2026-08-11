---
direction: both
category: 资料
tags: [Dragonfly+, 组网架构, 超算, 智算, OCS, 胖树, 拓扑]
summary: "解析Dragonfly+及Group-Wise变体，对比胖树，探讨OCS演进"
quality: high
processed: 2026-08-11 12:05
---
---
title: "Dragonfly+与Group-Wise Dragonfly+超算智算组网架构深度解析"
tags:
  - infrastructure
  - network
  - architecture
  - computing
  - first-principles
  - design
  - semiconductor
  - hardware
  - chip
  - physics
date: 2026-08-06 21:00
source: GetNotes
score: 17
---

## Original Note

---
note_id: 1917614455698266792
title: "Dragonfly+与Group-Wise Dragonfly+超算智算组网架构深度解析"
type: link
created: 2026-08-05 16:13:52
source: getnote
kb: 
---

# Dragonfly+与Group-Wise Dragonfly+超算智算组网架构深度解析

### 🏗️ 超算智算网络为什么要做扁平化？

为了**降低时延和建设成本**，扁平化已成为万卡/10万卡规模组网的核心优化方向。
- **多平面胖树是主流**：以128端口交换机为例
  - 传统2层胖树 = **8,192** 个GPU接入（公式：r²/2）
  - 双平面胖树 = **16,384** 个GPU接入
  - 4平面胖树 = **32,768** 个GPU接入
- **超出两层多平面胖树上限后**，Dragonfly+ 及 Group-Wise Dragonfly+ 成为扁平化组网优选项。

### 📐 几种组网架构的扩展性差在哪？

组网规模直接由**交换机端口数 r** 决定，不同拓扑公式差异极大。

| 拓扑类型 | 组网规模公式 | 128端口交换机对应规模 |
| :--- | :--- | :--- |
| 2层胖树 | r²/2 | 8,192 |
| 3层胖树 | r³/4 | 524,288 |
| 传统Dragonfly+ | r⁴/16 | 16,777,216 |
| Group-Wise Dragonfly+ | r³/8 | 262,144 |
- **传统Dragonfly特点**：网络直径小、成本低
  - 短板1：全局链路稀疏 → 路由策略不佳易**严重拥堵**
  - 短板2：扩容需**重新布线规划** → 复杂度和管理难度高

### 🔍 Dragonfly+ 拓扑到底怎么搭？

Dragonfly+ 是**分层交换+直连**的结合体，组内胖树、组间全互联。
- **核心结构**：
  - 组内 = 标准 **CLOS结构（2层胖树）** → 保证本地高带宽
  - 组间 = 全局链路全互联 → 无需核心交换机（Super-Spine/Core）
- **三种组间互联模式**：
  - **(a) 最大规模型**：每组对之间仅1条全局链路 → 扩展性最强，组间带宽受限
    - 绕路（组A→组B→组C）需在组B内 **Down-Up绕行** → 路径长、占用组内带宽
  - **(b) 中等规模型（Group-Wise Dragonfly+）**：每个Spine到其他组各1条链路
    - 单平面：同号Spine之间1条链路；多平面：对应平面同号Spine之间1条链路
    - 优势 = 避免上下设备绕行 + 更简洁的**多路径均衡路由**
    - 代价 = 组网规模变小
  - **(c) 小规模型**：每个Spine到其他组有多条并行链路

### 🌍 业内有哪些实际组网案例？

Dragonfly/Dragonfly+ 在超算领域应用广泛，代表案例包括 **HPE Cray Slingshot、JUPITER、JUWELS**。

#### HPE Cray Slingshot 互联方案
- 采用**两级Dragonfly拓扑**，应用于Frontier、LUMI、Perlmutter等超算
- Slingshot11交换机 = **64个200G端口**
- 每组配置 = 32台交换机
  - 16端口 → 接端节点
  - 31端口 → 组内互连
  - 17端口 → 组间互连
- 最大规模：**545个组**（17×32+1），支持 **279,040个端节点**

#### JUPITER 超算（德国于利希研究中心）
- 欧洲首台Exascale级超算，2026年6月HPC Top500排名**第5位**
- 芯片：NVIDIA Grace Hopper 超级芯片
- 网络：NVIDIA Quantum InfiniBand，**Dragonfly+拓扑** + 自适应路由
- 组构成：共27个Group
  - 25个 = GPU集群（Booster cells）
  - 1个 = CPU集群（Cluster cells）
  - 1个 = 管理子系统（Admin cells）
- 单Group细节：
  - **240个节点**，分布在5个物理机架
  - 15台L1交换机 + 16台L2交换机
  - 每节点4个200G端口 → 分支线缆连L1的400G端口
  - 每台L2最多32条400G上行，至少26条用于跨组全局链路
- 总规模：**24,000个GPU**，推测采用 Group-Wise Dragonfly+ 优化结构

#### JUWELS Booster 超算
- 2026年6月HPC Top500排名**第58位**
- 936个计算节点，每节点4块NVIDIA A100 GPU
- 网络：Dragonfly+拓扑 **HDR-200 InfiniBand**
- 单Group = 48个节点，组内完整2层胖树（10叶+10脊）
- 组间：每对Group之间有**10条全局链路**（Group-Wise Dragonfly+结构）

### 🔮 蜻蜓拓扑+OCS是下一代方向吗？

AI集群进入十万卡级后，**蜻蜓拓扑+OCS** 正成为智算组网的重要演进路径。
- **蜻蜓拓扑（Dragonfly系列统称）优势**：
  - 减少交换机层级 → 缩短通信路径
  - 优化全局流量结构 → 降低成本与功耗、提升算力利用率
- **固有挑战**：
  - 稀疏模式：路由复杂、负载均衡难、收敛比大、**组间带宽瓶颈**、路径延迟差异大
  - 密集模式：全局链路多、**光纤管理难**、故障排查困难
- **英伟达2026 OFC披露方案**：
  - 用蜻蜓拓扑取代Fat-tree胖树
  - 引入 **CPO光电共封装交换机 + OCS全光交换** 分层协同
  - Scale-out（机柜间/集群内）：Spine可用OCS替代
  - Scale-across（跨集群/跨园区）：OCS为最优解
- **OCS替代电Spine的六大价值**：
  - 极致低时延 = 纯光路交换 + 无光电转换 + 跳数减少
  - 极致低功耗 = 消除光电转换损耗 → 降低**TCO（总体拥有成本）**
  - 无损高带宽 = 全光直连 + 无阻塞端到端大带宽
  - 算力弹性调度 → 提升集群利用率
  - 高扩展性 + 长生命周期 → 降低扩容成本
  - 高可用 + 简化运维 = 光路自动切换绕障 → 故障恢复快
- **未来趋势**：混合组网为主
  - 组内/集群内 = Fat-Tree
  - 组间/跨集群 = Dragonfly + OCS
  - 从"静态互联"向"**动态可重构光网络**"演进

### 📝 补充细节
- 文中"蜻蜓拓扑"是 Dragonfly、Dragonfly+、Group-Wise Dragonfly+ 三者的统称。
- Group-Wise Dragonfly+ 相比传统Dragonfly+，本质是用**规模换带宽和路由简洁性**。
- JUPITER的L2交换机多配1台，是为了匹配上行32条链路的需求。

---
*getnote | 2026-08-06 21:00*


---

## Related Notes

[[iNEST-MOC]]
[[FPGA原型]]
[[paper1_iNEST_core_architecture]]
[[SDI化合物键_四型架构]]
