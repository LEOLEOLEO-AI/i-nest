---
direction: iNEST
title: "FlagOS2026 AIForumPPT iNEST分析"
created: 2026-07-07
modified: 2026-07-07
---
# 2026首届AI院士论坛 — FlagOS/RISC-V系列PPT分析
# 对 iNEST/TCC 的战略价值

**来源**：2026年首届人工智能院士论坛，众智FlagOS 2.0发布  
**录入日期**：2026-05-17  
**图片数量**：5张PPT截图  
**关联方向**：B3论文（Nature Electronics）· Demo叙事 · 合作方向

---

## 五张图内容索引

| 图 | 主题 | 核心数据 |
|----|------|---------|
| 图1 | FlagOS 2.0总体架构 | 支持18厂商、32款芯片的统一软件栈 |
| 图2 | FlagGEMs + 多领域算子库 | 497个算子（全球最大多芯片算子库），40模型覆盖度90%~100% |
| 图3 | Triton-TLE语言扩展 | SparseMLA昇腾提升83倍，CausalConv1D提升64倍，支持31种原语 |
| 图4 | RISC-V AI乐高积木架构 | CPU/CPU+AME/AI核/R路由节点模块化组合 |
| 图5 | 香山AI三种方案 | ①通推一体②通推分离③经典NPU卡（低延时/高吞吐/加速器三路径） |

---

## 核心发现：国产AI栈的"拓扑计算层"真空

```
应用层：GLM / DeepSeek / Qwen / 具身智能模型
框架层：FlagScale（训练推理）/ vLLM-plugin-FL
算子层：FlagGEMs 497个算子（全球最大）
编译层：Triton-TLE（TLE-Lite → Struct → Raw 三层）
[缺口]：拓扑计算层 ← iNEST/TCC-16 的位置
硬件层：RISC-V香山三种形态 + 18家芯片厂商32款
```

**FlagOS用497个算子才实现主流模型90%~100%覆盖。**  
**iNEST的Route≡Transform定理预言：TCC-16可完备覆盖同样的计算空间。**

---

## iNEST vs FlagOS/香山的关键对比

### 算子数量对比
| 路线 | 算子/原语数量 | 覆盖度 |
|------|------------|--------|
| FlagOS（FlagGEMs + 多领域） | **497个算子** | 90%~100%（40个主流模型） |
| iNEST TCC-16 | **11个正交原语** | 理论100%（完备性定理已证） |
| FlagFFT（薄弱项） | **2个算子** | iNEST：0个算子（拓扑等价替代） |

### 架构灵活性对比
| 架构 | 形态 | 切换能力 |
|------|------|---------|
| 香山三方案 | 静态选择（流片后固定） | ❌ 方案间不可切换 |
| iNEST SDI | 液态拓扑（动态重构） | ✅ 1μs内覆盖三种方案行为 |

### 拓扑感知对比
| 项目 | FlagOS Triton-TLE | iNEST SDI |
|------|-----------------|---------|
| 稀疏感知 | TLE-Struct层（软件级） | PRUNE原语（互连层物理实现） |
| SparseMLA提升 | 83倍（软件优化） | 理论上更高（物理消除搬运） |
| FFT实现 | FlagFFT 2个算子 | 0个算子，拓扑等价 |
| 通信原语 | FlagCX统一通信库 | FUSE/PULL/CAST/SWAP四原语 |

---

## B3论文直接可用的对比数据

> FlagOS with 497 operators achieves 90-100% coverage of mainstream AI inference workloads across 40 models. The Route≡Transform theorem in TCC demonstrates that this same coverage is achievable with 11 orthogonal primitives—reducing operator count by 45× through topological isomorphism rather than operator enumeration.

---

## 投资者话术（精炼版）

**一句话**：
> "FlagOS用497个算子，iNEST用11个原语——两者覆盖同样的计算空间，但iNEST的基础是物理定理，不是软件工程。"

**扩展版**：
> "智源用举国之力，聚18家芯片厂商497个算子，实现了主流AI模型90%覆盖。香山用三种RISC-V方案解决了灵活性问题，但芯片流片后仍是静态的。iNEST在这两者之间提供了它们都缺少的那一层：拓扑计算基底——11个原语完备覆盖，1μs动态切换三种香山方案的计算形态，物理消除数据搬运。这不是竞争，是互补。"

---

## 可行动项

- [ ] **B3论文引言**：加入"497 vs 11"对比数据作为TCC第三范式的motivation
- [ ] **Demo第一性差异Tab**：添加FlagOS算子数量对比
- [ ] **合作方向探索**：FlagFFT（2个算子）→ iNEST蝶形拓扑替代
- [ ] **FlagCX接口对接**：TCC-16通信四原语作为FlagCX底层
- [ ] **香山②增强**：通推分离 + SDI动态调整通/推比例

---
*录入时间：2026-05-17 | 分析人：刘勤让（iNEST）*  
*关联文件：B3_P-Paradigm_NatureElectronics_框架.md · NeuralComputers_CNC_iNEST_Analysis.md*

---

## 第六张图补充（2026-05-17追加）

### 图6：统一AI软件栈 — TileLang路线

**关键信息**：
- **TileLang**：北京大学2025年1月开源，已被DeepSeek**全面采用**
- 路线：自底向上（RISC-V AI指令集）+ 自顶向下（Triton/TileLang算子库）
- TileLang三层：Tile Program（硬件无关）→ Thread Primitives（硬件感知）→ PyCUDA Like（原厂）

### 新战略洞见：编译器层已出现分叉

```
Triton路线：NVIDIA主导 → 智源做Triton-TLE扩展（图3）
TileLang路线：北大开源 → DeepSeek全面采用（图6）
iNEST TCC-16：拓扑原语层，在两条路线之下，兼容两者
```

### TileLang后端机会

TileLang目前支持 NVIDIA/AMD GPU，TCC-16可作为**拓扑重构型芯片**的第三个后端：
- DeepSeek模型 → TileLang编译 → TCC后端 → iNEST硬件运行
- Route≡Transform提供数学保证：语义等价，无需重新训练

### 六张图完整生态地图

```
应用层：GLM/DeepSeek/具身智能模型
框架层：FlagScale / vLLM
编译层A：Triton → Triton-TLE（智源扩展，图3）
编译层B：TileLang（北大+DeepSeek，图6）
算子层：FlagGEMs 497个算子（图1-2）
【拓扑计算层】TCC-16 ← iNEST 的位置（两条编译路线的统一拓扑后端）
硬件层：RISC-V香山三方案 / 18厂商32款国产芯片（图4-5）
```
