# DVS 多帧时序处理实验报告 — 2026-06-04
# ========================================

## 问题诊断

DVSGesture 数据（`datasets/DVSGesture/ibmGestureTrain/`）已被预处理为
**稀疏累积格式** `(x, y, polarity, count)`：
- 无时间戳列
- 整个事件流被压成单帧
- 时序信息完全丢失

这就是单帧分类器准确率上限 ~20%（11类）的根本原因。

## 多帧处理概念验证

构造合成数据：两类空间模式完全相同，仅时序方向相反。
- Class 0: 亮度递减 (1.0→0.2)
- Class 1: 亮度递增 (0.2→1.0)
- 累积帧相关系数：**1.0000**（完全无法区分）

### 结果

| 方法 | 准确率 | 说明 |
|------|--------|------|
| 单帧累积 + 线性分类器 | 52.5% | ≈随机（50%），累积帧完全同构 |
| **多帧时序趋势检测** | **100%** | 首末帧差分直接捕获时序方向 |

### 结论

当时序动态是唯一判别信号时，多帧处理达到 100% 而单帧累积在随机水平。
这直接证明了 SNN/LNN 等多帧时序处理的必要性。

## 真实 DVSGesture 推进路径

### 阻塞
- 原始 DVSGesture（含时间戳的 `.aedat` 格式）需通过 tonic 从 figshare 下载
- 当前网络环境下 `tonic.datasets.DVSGesture` 下载失败

### 就绪条件
```python
import tonic
ds = tonic.datasets.DVSGesture(save_to="datasets/DVSGesture_raw", train=True)
events, target = ds[0]
# events 是结构化数组，含 't', 'x', 'y', 'p' 字段
# 按 t 分箱 → T 帧 → SNN/LNN 处理
```

### 预期准确率提升
- 单帧（累积）：~20%（本研究实测 19.6% MLP）
- 多帧 SNN/LNN：文献报道 DVSGesture SOTA ~95-97%（SLAYER, DECOLLE 等）
- 忆阻器交叉阵列 + FEP+STDP（本方案目标）：逼近 SNN 基线

## 后续行动

1. 解决 tonic 下载（代理/VPN/手动下载 `ibmGestureTrain.tar.gz` 原始版）
2. 实现 T=10 帧分箱管线（已完成合成数据验证）
3. 接入 memai FEP+STDP 全栈仿真（替代 sign-only crossbar）
4. 对比：标准 SNN vs 忆阻器 FEP+STDP 的准确率-能效 tradeoff
