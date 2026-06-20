# iNEST 论文与专利清单更新 — 2026-06-04
# =========================================
# 本次更新内容：
#   1. CST RG论文(#29) — 新完成v0.5初稿，填入D组D6/D7位
#   2. P-Theory v2 — 更新至含SDI Section 4.3计算验证数据
#   3. CST V25 FINAL — 更新至含SDI Section 5.1计算验证数据
#   4. 新增专利方向：SDI拓扑涌现阈值检测 + RG重整化群分析方法
#   5. DVS真实数据实验基线结果

---

## 一、论文清单更新

### A组（CST基础理论）— 更新

| 编号 | 变更 | 说明 |
|------|------|------|
| A1 | 状态更新 | CST V25 FINAL 已插入 SDI Section 5.1（计算验证），完整性 92%→95% |
| A11 | 状态保持 | 英文统一理论论文，与A1互补 |

### B组（SDI-CC 互连体系）— 更新

| 编号 | 变更 | 说明 |
|------|------|------|
| B1 (P-Theory) | 状态更新 | 已插入 Section 4.3（SDI-Bond计算验证），含Exp 2/3/4实际数据，完整性 87%→92% |

### D组（技术专项）— 新论文填入

| 编号 | 原状态 | 新状态 | 标题 |
|------|--------|--------|------|
| D6 | 待撰写 | 🟢 v0.5初稿 | 复杂网络RG变换严格数学理论 → **CST RG: Renormalization Group Analysis of Small-World Topology Emergence** |
| D7 | 待撰写 | 🟢 v0.5初稿 | RG不动点与CST最优态对应定理 → 已并入D6（RG fixed point at σ=4.97, CST Level I） |

**D6/D7 新论文关键数据**：
- N=1024一阶相变：dσ/dp=2,998 at p=0.003
- RG flow固定点：σ=4.97，分形维数d_f=1.29
- 涌现阈值：N=48，S_eff/Rand=1.89x
- N=1024优势：S_eff/Rand=26.77x
- 文件：`goal-inest/CST_RG_Paper_Draft_v0.5.md`
- 目标：Physical Review Letters / Communications Physics

---

## 二、专利清单更新 — 新增方向

### P1（中期跟进）— 新增3项

| 编号 | 标题 | 来源 | 优先级 |
|------|------|------|--------|
| P1-5 | **一种基于RG重整化群的小世界网络涌现阈值检测方法** | CST RG paper + Exp 4 (N=48涌现阈值) | 高 |
| P1-6 | **一种面向容错芯片互联的SDI拓扑参数优化方法** | Exp 3 (p=0.10最优) + Exp 2 (并行吞吐) | 高 |
| P1-7 | **一种基于帧累积的DVS事件流忆阻器交叉阵列处理方法** | DVS loader + CrossbarClassifier | 中 |

### 新增专利详情

**P1-5: RG重整化群涌现阈值检测方法**
- 技术问题：现有网络拓扑分析无法定量判定涌现发生的最小规模
- 发明方案：基于degree-coarse-graining的RG flow，计算S_eff/Rand比值，
  当比值突破1.5x时判定为涌现阈值
- 技术效果：在N=48处准确检测到涌现（S_eff/Rand=1.89x），
  分形维数d_f=1.29，RG固定点σ=4.97
- 对应论文：D6/D7 (CST RG)
- 对应项目：海河实验室+NSFC

**P1-6: SDI拓扑参数优化方法**
- 技术问题：现有芯粒互联拓扑无法兼顾结构效率与容错性
- 发明方案：以S_eff=C×E_glob为优化目标，p=0.10为最优重连概率，
  在15% hub攻击下E/E₀=0.945，同时保持S_eff高7.3倍
- 技术效果：128并发任务零拥塞，30%边损失后E/E₀=0.883
- 对应论文：B1 (P-Theory v2 Section 4.3)
- 对应项目：海河实验室SDI芯粒设计

**P1-7: DVS事件流忆阻器交叉阵列处理方法**
- 技术问题：DVS事件流数据无法直接输入忆阻器交叉阵列
- 发明方案：基于.npy预处理的帧累积方法，支持DVSGesture
  11类手势识别，252样本数据加载管线
- 技术效果：MLP基线19.6%（单帧），线性基线17.6%
- 对应项目：memai仿真平台

---

## 三、DVS实验基线结果（补充证据）

| 方法 | 准确率 | 说明 |
|------|--------|------|
| 随机基线 | 9.1% | 11类均匀分布 |
| CrossbarClassifier (4-bit, sign-only) | 5.9% | 不收敛，sign更新在电导范围内振荡 |
| 线性softmax分类器 | 17.6% | 单帧信息不足以区分手势 |
| 2层MLP (64 hidden) | 19.6% | 非线性改善有限，时序信息完全丢失 |

**结论**：单帧累积丢失DVS全部时序信息，准确率上限约20%。
要突破此上限需要：
1. 多帧时序处理（SNN/LNN）
2. 全栈FEP+STDP仿真（非sign-only crossbar）
3. 忆阻器电导范围扩大或差分对权重复用

---

## 四、后续计划整合

### 论文投递（本周）
1. A1 (CST V25) → Nature Machine Intelligence（SDI数据已插入）
2. B1 (P-Theory v2) → JMLR / NeurIPS（Section 4.3已更新）
3. D6/D7 (CST RG) → PRL（v0.5待完善至v1.0）

### 专利交底（2周内）
4. P1-5 (RG涌现阈值) — 从CST_RG_Paper_Draft_v0.5.md提取技术方案
5. P1-6 (SDI拓扑优化) — 从SDI_Simulation_Report_v2.md提取实验数据
6. P1-7 (DVS忆阻器处理) — 从更新后的dvs.py提取方法流程

### 实验补强（1个月内）
7. DVS多帧时序处理（替换单帧累积）
8. 全栈FEP+STDP仿真接入DVS数据
9. 更新D6/D7论文至v1.0（补充RG理论推导 + Monte Carlo验证）
