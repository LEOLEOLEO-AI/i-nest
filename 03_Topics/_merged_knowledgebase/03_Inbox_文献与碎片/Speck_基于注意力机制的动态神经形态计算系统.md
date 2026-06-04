# Speck：基于注意力机制的动态神经形态计算系统

- **类型**: link
- **时间**: 2025-08-23 06:19:05
- **标签**: AI链接笔记, 神经形态计算, 动态SNN, 注意力机制
- **来源**: https://www.nature.com/articles/s41467-024-47811-6

## 内容

Speck 脉冲神经网络芯片是一款创新型的感算一体神经形态芯片，其技术优势显著，在低功耗、高性能、架构设计和应用适配等多个维度展现出独特价值。

1.  **低功耗特性**
    
    -   **静态功耗极低**：处理器静态功耗仅为 0.42mW，在无输入时几乎不消耗运行能量，这使得 Speck 在边缘计算场景中优势突出，可长时间稳定运行，降低能源成本。例如在智能安防的监控设备中，可在长时间待机状态下保持极低能耗。
        
    -   **运行功耗低**：运行单个样本时，实时功率最低能达到 0.70mW。在处理动态视觉任务时，其功耗相比传统 AI 芯片大幅降低，如在手势识别任务中，能耗仅为传统 GPU 的几十分之一甚至更低，极大地提高了能源利用效率。
        
2.  **高性能表现**
    
    -   **计算速度快**：系统处理单个脉冲的延迟仅为 3.36μs，能快速处理输入的事件流，实现实时响应。在智能机器人的避障应用中，可迅速感知周围环境变化并做出反应，保障机器人的安全运行。
        
    -   **准确率高**：在多个事件基准数据集上，如 DVS128 Gesture、DVS128 Gait-day 等，部署动态 SNNs 时展现出高准确率。以 Gesture 数据集为例，传统 SNN 准确率为 81.0%，而 Speck 上的动态 SNN 提升至 90.0%，有效提升了任务处理的可靠性。
        
3.  **独特架构设计**
    
    -   **完全异步架构**：采用完全异步设计，计算能力依赖输入数据，无需全局或局部时钟信号，避免了时钟空翻带来的冗余功耗。这种架构使芯片能根据输入动态调整计算资源，在有输入时迅速响应，无输入时进入低功耗状态。
        
    -   **感算一体集成**：集成 128×128 像素的 DVS 和异步脉冲神经网络芯片，实现感算一体。DVS 可在视觉场景亮度变化时异步、稀疏地生成事件流，芯片能直接对这些事件流进行处理，减少数据传输延迟和功耗，提高系统整体效率。
        
    -   **灵活可扩展架构**：包含 9 个 SNN 核心，每个核心可独立、异步工作，通过中央事件路由器可灵活配置事件路由。这种架构设计方便根据任务需求扩展芯片规模，提高计算能力，以适应不同复杂程度的任务。
        
4.  **算法协同优化**
    
    -   **解决动态不平衡问题**：揭示了 SNNs 中存在的 “动态不平衡” 现象，并设计基于注意力的动态框架。该框架可根据输入重要性调节 SNNs 的脉冲响应，使网络更专注于重要信息，提高处理效率和准确率。
        
    -   **软件工具链支持**：提供完整的软件工具链，包括数据管理、模型仿真、宿主管理等功能。借助这些工具，工程师可高效地将 SNN 算法部署到芯片上，加速应用开发过程，降低开发成本。
        

🔋 **动态计算的挑战与解决方案**

-   **传统AI瓶颈**：资源与能源限制制约边缘设备部署，类脑计算（神经形态计算）通过模拟人脑神经元突触计算，以低功耗（如人脑仅20W）为潜在解决方案。
    
-   **动态计算定义**：无输入时能耗最低，输入变化时能耗显著变化，但传统脉冲神经网络（SNN）存在“动态失衡”——不同输入激活的子网络规模相似，导致能耗差异小，削弱动态计算优势。
    
-   **创新方案**：提出注意力驱动的动态框架，通过优化膜电位调节脉冲响应，实现输入依赖的能耗差异化。
    

🧠 **Speck神经形态芯片设计**

-   **核心特性**：6.1mm×4.9mm的感知-计算一体化SoC，集成128×128 DVS摄像头与全异步神经形态处理器，静态功耗仅**0.42 mW**，单样本处理延迟\*\*<0.1 ms\*\*，实时功耗低至**0.70 mW**。
    
-   **架构亮点**：
    
    -   **全异步逻辑**：无全局时钟，仅在输入事件触发时激活计算，闲置时接近零功耗。
        
    -   **事件驱动卷积**：基于地址事件表示（AER）的异步卷积处理，单脉冲延迟**3.36 μs**。
        
    -   **模块化SNN核心**：9个独立异步SNN核心，支持动态路由与并行计算（图2g）。
        

📊 **动态SNN算法框架**

-   **注意力机制**：通过时间/通道维度的注意力优化膜电位（公式： \(\mathbf{U} \leftarrow \mathbf{W}_\tau(\theta,\mathbf{U}) \odot \mathbf{U}\) ），缓解时空不变性导致的动态失衡。
    
-   **两种策略**：
    
    -   **精炼（AR）**：调整特征图权重增强关键信息；
        
    -   **掩码（AM）**：直接过滤冗余输入事件（图3c）。
        
-   **实验验证**：在Gesture/Gait数据集上，动态SNN较传统SNN降低**60%脉冲发放率**，同时提升精度\*\*+9.0%\*\*（图4f）。
    

⚡ **系统性能对比**

| 平台  | 模型  | 精度（%） | 功耗（mW） | 延迟（ms） |
| --- | --- | --- | --- | --- |
| GPU | Vanilla SNN | 92.1 | 30079 | 35.2 |
| Speck | Vanilla SNN | 91.8 | 3.8 | 0.09 |
| Speck | Dynamic SNN | 92.5 | 0.70 | 0.08 |
| _表：Speck与GPU在事件驱动动作识别任务上的性能对比（Gesture数据集）_ |     |     |     |     |

📈 **应用场景与未来方向**

-   **目标场景**：移动设备、物联网、智能家居等低功耗实时场景（图2f），支持动态视觉任务如步态识别、手势控制。
    
-   **未来优化**：扩展网络类型支持、引入混合精度计算，平衡能效与任务复杂度。
    

### 关键图表解析

图1：神经形态计算与传统计算的动态特性对比

-   **a**：脉冲神经元（突触累积）vs 人工神经元（乘加运算）；
    
-   **b**：SNN动态失衡现象（不同输入激活相似规模子网络）；
    
-   **c**：注意力框架通过时空调节实现差异化响应。
    

图2：Speck芯片设计细节

-   **d**：Speck物理原型（含DVS摄像头）；
    
-   **g**：全异步架构（事件路由+SNN核心）；
    
-   **i**：异步事件驱动卷积流程（地址映射+动态权重访问）。
    

图4：动态SNN性能与脉冲活动分析

-   **b/e**：AR策略提升精度（+5%）并降低脉冲发放率（-30%）；
    
-   **f**：动态SNN的NSFR（网络脉冲发放率）随输入显著变化，缓解动态失衡。

## 原文

Introduction
------------

Resource and energy constraints are the major restrictions to deploying traditional AI methods, especially in real-world edge platforms. A promising solution with an attractive low-power feature is neuromorphic computing, which is partially inspired by the human brain that runs even more complex and larger neural networks with a total energy need of just 20 W[1](https://www.nature.com/articles/s41467-024-47811-6#ref-CR1 "Roy, K., Jaiswal, A. & Panda, P. Towards spike-based machine intelligence with neuromorphic computing. Nature 575, 607–617 (2019)."),[2](https://www.nature.com/articles/s41467-024-47811-6#ref-CR2 "Schuman, C. D. et al. Opportunities for neuromorphic computing algorithms and applications. Nat. Comput. Sci. 2, 10–19 (2022)."),[3](https://www.nature.com/articles/s41467-024-47811-6#ref-CR3 "Bartolozzi, C., Indiveri, G. & Donati, E. Embodied neuromorphic intelligence. Nat. Commun. 13, 1024 (2022)."),[4](https://www.nature.com/articles/s41467-024-47811-6#ref-CR4 "Mehonic, A. & Kenyon, A. J. Brain-inspired computing needs a master plan. Nature 604, 255–260 (2022)."). By abstracting the computations in the human brain at the neuron and synapse level, existing neuromorphic platforms, such as the classic BrainScales[5](https://www.nature.com/articles/s41467-024-47811-6#ref-CR5 "Schemmel, J. et al. A wafer-scale neuromorphic hardware system for large-scale neural modeling. In 2010 IEEE International Symposium on Circuits and Systems (ISCAS) 1947–1950 (IEEE, 2010)."), SpiNNaker[6](https://www.nature.com/articles/s41467-024-47811-6#ref-CR6 "Painkras, E. et al. Spinnaker: a 1-w 18-core system-on-chip for massively-parallel neural network simulation. IEEE J. Solid-State Circuits 48, 1943–1953 (2013)."), Neurogrid[7](https://www.nature.com/articles/s41467-024-47811-6#ref-CR7 "Benjamin, B. V. et al. Neurogrid: a mixed-analog-digital multichip system for large-scale neural simulations. Proc. IEEE 102, 699–716 (2014)."), TrueNorth[8](https://www.nature.com/articles/s41467-024-47811-6#ref-CR8 "Merolla, P. A. et al. A million spiking-neuron integrated circuit with a scalable communication network and interface. Science 345, 668–673 (2014)."), and the most recent Darwin[9](https://www.nature.com/articles/s41467-024-47811-6#ref-CR9 "Shen, J. et al. Darwin: a neuromorphic hardware co-processor based on spiking neural networks. Sci. China Inf. Sci. 59, 1–5 (2016)."), Loihi[10](https://www.nature.com/articles/s41467-024-47811-6#ref-CR10 "Davies, M. et al. Loihi: a neuromorphic manycore processor with on-chip learning. IEEE Micro 38, 82–99 (2018)."), Tianjic[11](https://www.nature.com/articles/s41467-024-47811-6#ref-CR11 "Pei, J. et al. Towards artificial general intelligence with hybrid Tianjin chip architecture. Nature 572, 106–111 (2019)."), have demonstrated impressive energy efficiency via spike-based communication and computing. However, whether this level of abstraction[2](https://www.nature.com/articles/s41467-024-47811-6#ref-CR2 "Schuman, C. D. et al. Opportunities for neuromorphic computing algorithms and applications. Nat. Comput. Sci. 2, 10–19 (2022)."),[12](https://www.nature.com/articles/s41467-024-47811-6#ref-CR12 "Potok, T. et al. Neuromorphic computing, architectures, models, and applications. A beyond-CMOS approach to future computing, June 29-July 1, 2016. USDOE Office of Science (SC) (United States). Advanced Scientific Computing Research (ASCR). (Oak Ridge, TN, 2016)."),[13](https://www.nature.com/articles/s41467-024-47811-6#ref-CR13 "Li, G. et al. Brain inspired computing: a systematic survey and future trends. Preprint at TechRxiv 
                  https://doi.org/10.36227/techrxiv.21837027.v1
                  
                 (2023).") is the most suitable approach for emulating the efficient computation of the brain, and the role that high-level stereo brain mechanisms can play in neuromorphic chips, are challenges that must be addressed at this stage”.

An important function of the

---
**Tags:** #BrainInspired #SDSoW
