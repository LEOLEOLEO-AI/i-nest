# Codex 研究工具配置手册：TCC + iNEST

> 版本 2.1 | 2026-06-24 | 8 就绪

---

## 一、已安装核心工具

### TCC 拓扑计算管线

| 工具 | 版本 | 用途 |
|------|------|------|
| **networkx** | 3.4.2 | 网络拓扑构建、小世界/无标度模型、中心性分析 |
| **igraph** | 1.0 | 大规模图社区检测（Leiden）、motif 发现、百万节点级 |
| **PyTorch Geometric** | 2.7.0 | GNN 图预测、GraphSAGE/GCN/GAT、节点/边分类 |

### iNEST 神经形态管线

| 工具 | 版本 | 用途 |
|------|------|------|
| **brian2** | 2.9.0 | 生物神经元精细仿真（LIF/IZH）、STDP 可塑性 |
| **snntorch** | 0.9.4 | 脉冲神经网络训练、代理梯度、脉冲编码/解码 |
| **snngrow** | 1.0.0 | 字节跳动 SNN 生长训练：架构自动生长/剪枝 |
| **PySpike** | 0.8.0 | 脉冲序列同步分析：SPIKE-distance、ISI-distance（Cython 加速） |
| **reservoirpy** | 0.4.1 | 储备池计算、Echo State Network、涌现动力学 |

### 异步电路 / 芯片设计（TCC 硬件）

| 工具 | 类型 | 用途 |
|------|------|------|
| **Workcraft** | Java GUI | 异步电路建模/验证/综合（STG、Petri Net、MPSat 时序验证） |

---

## 二、安装状态

| 工具 | 状态 |
|------|------|
| **PySpike** | OK Cython 加速 |
| **MSVC 编译器** | OK VS 2022 BuildTools 14.44 |
| **SNAP** | 阻塞 — Python 绑定仅支持到 py39 |
| **NEST** | 阻塞 — 需 GSL + Boost |
| **Balsa** | 阻塞 — 需 MSYS2 |

---

## 三、工具导入验证

`
import networkx; import igraph; import torch_geometric
import brian2; import snntorch; import snngrow
import pyspike; import reservoirpy
print("8 tools OK")
`

---

预览: http://127.0.0.1:8900/home/work/.openclaw/workspace/90_System/指南/TCC_iNEST_工具配置手册.md
