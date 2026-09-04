---
direction: both
category: 项目
tags: [tcc, bp, 商业计划, 拓扑计算, 芯片]
summary: "拓扑芯智TCC芯片商业计划书，主打液态拓扑切换与训推一体"
quality: high
processed: 2026-09-04 08:15
---
---
title: "TCC BP"
tags:
  - tcc
  - chip
  - semiconductor
  - sdi-bond
  - architecture
  - network
  - emergence
  - design
  - infrastructure
  - cst
  - fpga
  - hardware
  - computing
  - criticality
date: 2026-08-31 07:23
source: GetNotes
score: 29
---

## Original Note

TCC BP

### 项目名称：拓扑芯智（TopoCore）——液态拓扑计算芯片

### BP结构（12页）

**第1页：封面**

- 拓扑芯智 TopoCore
- 一句话：让每颗芯片拥有"变形"能力——微秒级拓扑切换使能训推一体AI+信号处理

**第2页：痛点与机会**

- 痛点①：端侧AI芯片只能推理不能学习（智驾/无人机Corner Case无法本地适应）
- 痛点②：DBF处理器国内空白，全部依赖进口FPGA实现，功耗高、灵活性差
- 痛点③：星载计算需一星多能（推理+训练+信号+视频），当前无单芯片方案
- 市场：边缘AI 2026年300亿美元+、波束成形IC 2034年386亿美元、太空算力2034年186亿美元

**第3页：解决方案**

- TCC（Topology‑Centric Computing）范式：拓扑即计算
- 核心IP：Route‑Transform原语引擎 + SDI液态拓扑切换（τ ≤ 1 µs）
- 一颗芯片 = AI推理 + AI训练 + DBF波束成形 + FFT信号处理

**第4页：技术壁垒**

- 壁垒①：Route‑Transform完备性定理（学术护城河，无法绕过）
- 壁垒②：三代SDI芯片IP（SDI3210→SDI4820→SDI12850，10年积累）
- 壁垒③：液态三率指标体系（η/κ/τ/σ）定义产业标准

**第5页：产品路线图**

- Phase 1（2029）：TCC‑Edge PCIe模组（FPGA验证转产品），面向无人机/智驾
- Phase 2（2030）：TCC‑DBF ASIC（7nm），面向卫星通信相控阵/雷达
- Phase 3（2031）：TCC‑SDSoW晶上平台，面向DRBE/数字孪生

**第6页：商业模式**

- IP授权（给卫星制造商/雷达厂商）：年费 + 流片Royalty
- 模组销售（给Tier‑1域控/飞控厂商）：ASP ¥2000‑8000
- SaaS算力服务（星载/地面混合算力网络）

**第7页：市场定位与对标**

- vs 地平线J6：TCC能训练，J6不能
- vs Cerebras WSE：TCC 15W边缘级，WSE 25kW数据中心级
- vs 芯正微DBF：TCC是计算+拓扑一体，芯正微是纯射频前端
- 定位：**唯一同时覆盖AI训推+DBF的边缘级芯片**

**第8页：核心团队**

- CTO：iNEST理论创始人，网络时空协同复杂度/SDI芯片三代主导
- VP Engineering：SDSoW架构师
- VP Product：智驾/卫星行业15年+经验

**第9页：验证数据（来自先导项目）**

- η ≥ 80%（FPGA实测）
- κ ≥ 25×（AllReduce加速实测）
- τ ≤ 1 µs（拓扑切换实测）
- σ ≤ 5%（训推切换实测）
- 64阵元×16波束DBF实时演示

**第10页：财务预测**

- 2030年营收：¥1.2亿（模组500套×¥8000 + IP授权3家×¥3000万）
- 2032年营收：¥8亿（ASIC放量 + SaaS启动）
- 毛利率：IP授权90%+，模组60%+，ASIC芯片50%+

**第11页：融资需求**

- Pre‑A轮：¥5000万（2029 H1），用于12人团队+ASIC前端设计
- A轮：¥2亿（2030），用于7nm流片+量产准备
- B轮：¥5亿（2031），用于SDSoW平台+生态建设

**第12页：愿景**

- 从"算力堆砌智能"到"拓扑涌现智能"
- 让每一颗中国芯片都拥有"液态变形"的超能力
- 对标十年后：中国的Cerebras + 中国的DRBE = TopoCore

  


Tags: 
Source: knowledge

---

## Related Notes

[[NCL神经计算定律详解]]
[[自组织临界态SOC]]
[[FPGA原型]]
[[paper1_iNEST_core_architecture]]
[[CST计量仪]]
[[超非线性增益]]
[[SDI化合物键_四型架构]]
[[iNEST-MOC]]
