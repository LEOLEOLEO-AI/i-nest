# iNEST 实验数据完整包 — 2026-06-04

## 产出清单

| 文件 | 内容 | 用途 |
|------|------|------|
| fig_cst_phase_transition_N1024.png | N=1024相变四面板图 | CST V25 Figure 4 |
| fig_sdi_experiments.png | 涌现+容错+吞吐 | P-Theory v2 Figure 3 |
| fig_rg_flow_mc.png | RG收敛+d_f+MC | CST RG Figure 2 |

---

## 一、CST N=1024 相变扫描

| sigma峰值 | 26.28 (p=0.060) |
| S_eff峰值 | 0.1651 |
| S_eff/Rand | 27.1x |
| 一阶相变 d_sigma/dp | 3000 (p=0.003) |
| sigma>=4.0 | p=0.001 |

---

## 二、SDI Exp 2-4

| Exp 2 并行吞吐 | N=128, 8并发零拥塞 |
| Exp 3 容错 hub15% | E/E0=0.965 |
| Exp 4 涌现阈值 | N=48, N=1024: 26.77x |

---

## 三、CST RG Monte Carlo

| RG不动点 | sigma=4.68 (step=2) |
| 分形维数 | d_f=2.06 (p=0.01) |
| MC稳定性 | CV=0.86% |

---

## 四、下一步

1. 将数据插入对应论文Section
2. 更新图表计数
3. 格式检查后投稿