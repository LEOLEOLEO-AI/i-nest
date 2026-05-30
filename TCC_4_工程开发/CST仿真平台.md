---
title: CST仿真平台
tags:
- criticality
- emergence
- large-language-model
- neuron
- neuroscience
- paper
- simulation
- survey
- synapse
- topology
---
**CST网络时空协同复杂度仿真平台**  
iNEST研究团队 · 天津大学微电子学院  
版本：v1.0 | 日期：2026-03-25

---

## 文件夹结构

### 📄 核心文档
| 文件 | 说明 |
|------|------|
| `CST仿真平台科学依据.md` | **总纲**：11章，20条参考文献，全部参数的生物学依据 |
| `CST仿真平台_C.elegans相变复现报告_v1.docx` | **正式报告**：七章Word文档，含四大关键发现和论文引用句 |

### 🧪 仿真代码（Python）
| 文件 | 说明 | 关键结果 |
|------|------|---------|
| `sdi_network_v2.py` | 动态扇出+级联激活 | σ=2.65，τ=11.35（E-L过固化问题暴露） |
| `sdi_network_v3.py` | NumPy向量化+三原理显式计算 | 速度×100，F定义问题暴露 |
| `sdi_network_v4.py` | 修正FEP定义 | 晶化死锁问题暴露（E-L=99%） |
| `sdi_network_v5.py` | +突触缩放（Turrigiano 1998） | σ=6.32，**首超线虫基准** |
| `sdi_network_v6.py` | +STD突触疲劳+不应期+E-L比例约束 | τ=2.89，**大幅收敛** |
| **`sdi_network_v8.py`** | **真实Connectome+有向图+三类神经元+电突触+胶质细胞** | **τ=2.28 ✓，初始σ=4.71** |
| `sdi_phase_transition_scan.py` | N扫描实验（N=10~1000） | **工程下确界N_min=80** |
| `build_report.py` | 生成Word报告的Python脚本 | — |

### 📊 真实生物数据
| 文件 | 说明 |
|------|------|
| `NeuronConnect.xls` | C.elegans完整神经连接图谱（WormAtlas，Varshney 2011，518KB） |
| `connectome_v8_data.json` | 从XLS提取的结构化数据（节点/边/类型，v8直接读取） |

### 🖼️ 仿真结果图
| 文件 | 说明 |
|------|------|
| `sdi_v5_celegans.png` | v5结果：σ首超线虫基准 |
| `sdi_v6_celegans_replication.png` | v6结果：STD引入后τ=2.89 |
| `sdi_v7_alpha_convergence.png` | v7结果：WS模型极限 |
| `sdi_v8_real_connectome.png` | **v8结果：真实connectome，τ=2.28** |
| `sdi_phase_scan.png` | **相变扫描：N_min=80下确界图** |
| `real_connectome_final.png` | 真实connectome拓扑分析图 |
| `critical_emergence_final.png` | 临界态涌现验证图 |

### 📚 知识库文档（01-13）
| 文件 | 内容 |
|------|------|
| `01_文献综述_临界态与超线性增益.md` | Beggs&Plenz, Shew等核心文献 |
| `02_文献综述_大模型涌现能力.md` | LLM涌现与阈值理论 |
| `03_文献综述_工程系统互连增益.md` | 工程佐证 |
| `04_仿真验证_线虫connectome.md` | 真实数据仿真结果（σ=5.87复现） |
| `05_SDI技术路线仿真规划.md` | 四阶段仿真规划 |
| `06_引用模板_答辩与论文.md` | 标准引用格式 |
| `07_核心定义_超非线性增益与智能视角.md` | IE三元指标（J/task） |
| `08_技术路线宣言.md` | iNEST核心命题表述 |
| `09_战略报告提纲_决策层.md` | 决策层报告SCQA结构 |
| `10_SDA物理架构_物理第一性智能涌现.md` | 三层架构+STDP/FEP/最小作用量 |
| `11_SDI节点接口规范与化合键定义.md` | E-L/I-L/E-S/I-S参数全表，动态扇出 |
| `12_三原理协同_FEP_最小作用量_STDP.md` | 三原理物理推导 |
| `13_知识框架总图_SDI化合键到临界态涌现.md` | 知识总纲（理论链条图） |

---

## 快速复现

```bash
# 环境准备
pip install numpy scipy networkx matplotlib python-docx xlrd openpyxl

# 1. 运行最新版仿真（真实connectome，N=279）
cd CST仿真平台
python3 sdi_network_v8.py

# 2. 运行相变下确界扫描
python3 sdi_phase_transition_scan.py

# 3. 生成正式报告
python3 build_report.py
```

---

## 核心结果速览

| 实验 | 关键结论 |
|------|---------|
| **C.elegans复现** | σ=6.31（超基准5.87）；真实初始σ=4.71（误差20%） |
| **幂律收敛** | α: 15.7(v5)→2.89(v6)→2.28(v8)，首进有限尺寸预期区间 |
| **相变下确界** | N_min=80（工程），N=279（生物，线虫） |
| **α外推预测** | N=10⁶（Gen1）时τ≈1.52→1.5（SOC临界态） |
| **τ=1.5的意义** | 分支过程临界点解析解，智能涌现可直接测量的充要判据 |

---

## 引用

如在论文或报告中使用本仿真平台的结果，请引用：

> iNEST Research Team, Tianjin University. (2026). *CST Simulation Platform for Intelligence Emergence: Replicating C.elegans Neural Phase Transition*. Internal Report v1.0.

核心数据来源请同时引用：
- Varshney et al. (2011). PLOS Comp Biol. DOI:10.1371/journal.pcbi.1001066
- Beggs & Plenz (2003). J. Neurosci. DOI:10.1523/JNEUROSCI.23-35-11167.2003

## Related Notes

- [[iNEST 机构 — 全景导航 (Map of Content)]]
- [[夏强飞一天2篇Nature大子刊：感存算一体，忆阻器阵列模拟计算]]
- [[你的大脑如何“连线”？科学家在纳米尺度研究神经网络]]
