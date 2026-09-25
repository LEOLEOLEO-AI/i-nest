# Cross-Domain Insights

**Generated**: 2026-09-25

> **口径说明（2026-09-18 修订）**：以下每条桥的匹配概念按**术语特异性**
> （逆文档频率式）排序，不再按概念目录的字母序取前几个——旧实现因此让
> 每条桥都反复列出相同的字母序靠前概念。
> `Strength` = 两侧匹配概念数的较小者，是**语料频次量级**而非相关性度量
> （高频词如 topology/interconnect 会把它推高），故同时给出 `Coverage`
> （占本域概念比例）与 top 概念的特异性得分，供复核。

## Active Bridges (7)

### Chiplet_Heterogeneous_Neuromorphic (Strength: 53 · Coverage: 0.7705)
Chiplet-based heterogeneous integration enables combining CMOS logic with memristor crossbar arrays for neuromorphic acceleration.
- 匹配规模：TCC 94 个 / iNEST 53 个
- TCC concepts（按特异性）: [[AI_Application_Scenario_Reconstruction]], [[AI_Industrial_Ecosystem]], [[Allreduce_Latency_MVP]]
- iNEST concepts（按特异性）: [[AutonomousAdaptation]], [[Complexity_Emergence]], [[Complexity_Emergence_Engineering]]
- 排序依据: term-specificity-weighted (非字母序)

### WaferScale_Neuromorphic (Strength: 52 · Coverage: 0.7623)
Wafer-scale integration could enable massive-scale neuromorphic chips with millions of neurons on a single die.
- 匹配规模：TCC 93 个 / iNEST 52 个
- TCC concepts（按特异性）: [[Cerebras_WSE]], [[Chiplet_Interconnect_Topology]], [[Chiplet_Wafer_Interconnect_Abstraction]]
- iNEST concepts（按特异性）: [[MacroscopicDescriptor]], [[InNetwork_Neuromorphic_Fabric]], [[AutonomousAdaptation]]
- 排序依据: term-specificity-weighted (非字母序)

### NoC_Spiking_Routing (Strength: 44 · Coverage: 0.6967)
NoC routing algorithms could be redesigned for event-driven spike packet delivery, reducing latency by orders of magnitude.
- 匹配规模：TCC 85 个 / iNEST 44 个
- TCC concepts（按特异性）: [[Soft_NoC]], [[SDI_NoC_Fabric]], [[Speedster7t_2D_NoC]]
- iNEST concepts（按特异性）: [[SpikingNeuralNetwork]], [[iNEST_Interconnect]], [[iNEST_Neuromorphic_Integration]]
- 排序依据: term-specificity-weighted (非字母序)

### SDI_Plastic_Interconnect (Strength: 43 · Coverage: 0.7818)
SDI's software-defined interconnect could implement plastic (reconfigurable) network topologies inspired by synaptic plasticity.
- 匹配规模：TCC 105 个 / iNEST 43 个
- TCC concepts（按特异性）: [[Chiplet_Interconnect_Topology]], [[SDI_Bond]], [[SDI_NoC_Fabric]]
- iNEST concepts（按特异性）: [[Contested_Priors_Mechanism]], [[SDI_STDP]], [[STDP_iNEST]]
- 排序依据: term-specificity-weighted (非字母序)

### 3DIC_Neural_Stacking (Strength: 3 · Coverage: 0.0545)
3D-IC stacking mimics cortical columnar architecture, enabling dense neural processing layers.
- 匹配规模：TCC 46 个 / iNEST 3 个
- TCC concepts（按特异性）: [[3D_IC_Stacking]], [[AI_Industrial_Ecosystem]], [[Allreduce_Latency_MVP]]
- iNEST concepts（按特异性）: [[DelayBased_Reservoir]], [[Intelligence_Emergence]], [[Memristive_Reservoir]]
- 排序依据: term-specificity-weighted (非字母序)

### Topology_Brain_Connectome (Strength: 1 · Coverage: 0.0182)
Brain connectome topology patterns can inspire optimal NoC topologies for wafer-scale AI chips.
- 匹配规模：TCC 110 个 / iNEST 1 个
- TCC concepts（按特异性）: [[Alpha_Computation_Consistency]], [[Alpha_Consistency_Problem]], [[AvalancheBranchingRatio]]
- iNEST concepts（按特异性）: [[InNetworkNeuromorphicSimulation]]
- 排序依据: term-specificity-weighted (非字母序)

### Memory_Wall_Neuromorphic_Solution (Strength: 1 · Coverage: 0.0182)
Neuromorphic in-memory computing is a potential solution to the wafer-scale memory wall problem.
- 匹配规模：TCC 5 个 / iNEST 1 个
- TCC concepts（按特异性）: [[Memory_Bandwidth_Density]], [[Cerebras_WSE]], [[Memory_Wall]]
- iNEST concepts（按特异性）: [[Memristor]]
- 排序依据: term-specificity-weighted (非字母序)

## Cross-Domain Papers (1)
- 深度思考_拓扑中心计算原语体系的改进方向 (cross-score: 4)

## Suggested Research Directions
- **Chiplet_Heterogeneous_Neuromorphic**: Chiplet-based heterogeneous integration enables combining CMOS logic with memristor crossbar arrays for neuromorphic acceleration.
- **WaferScale_Neuromorphic**: Wafer-scale integration could enable massive-scale neuromorphic chips with millions of neurons on a single die.
- **NoC_Spiking_Routing**: NoC routing algorithms could be redesigned for event-driven spike packet delivery, reducing latency by orders of magnitude.
