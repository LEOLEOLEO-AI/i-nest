# SDI Simulator v22-v28

自演化 SDI（Self-Developing Intelligence）仿真程序，版本 v22 到 v28。

## 版本演进

| 版本 | 文件 | 主题 |
|------|------|------|
| v22 | `sdi_v22_evolution.py` | 基础自演化框架 |
| v23 | `sdi_v23_fusion.py` | 多策略融合 |
| v24 | `sdi_v24_fep_stdp_fusion.py` | FEP + STDP 融合 |
| v25 | `sdi_v25_physical_biological.py` | 物理-生物约束 |
| v26 | `sdi_v26_multiscale.py` | 多尺度建模 |
| v27 | `sdi_v27_multiscale.py` | 多尺度优化 |
| v28 | `sdi_v28_multiscale.py` | 多尺度 FPGA 估算 |

## 目录结构

- `sdi_v2*_*.py` — 各版本主仿真程序
- `sdi_network_v*.py` — 共享网络模块
- `_*.py` — 辅助脚本（构建/优化/修复）
- `fpga/` — FPGA 映射与资源估算
- `results/` — 各版本运行结果
- `collective_comm_naas/` — 集群通信仿真

## 文档

- `Idea_SDI_Simulator_v22_Strategy.md` — v22 策略文档
- `v22_SelfEvolution_Design.md` — 自演化设计文档
- `V29_Simulation_Advancement_Plan.md` — v29 规划
