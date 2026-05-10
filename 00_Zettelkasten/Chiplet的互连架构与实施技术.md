# Chiplet的互连架构与实施技术

> 笔记本: 我的剪贴板  
> 创建时间: 2024-12-07  

---

原文链接: [https://mp.weixin.qq.com/s/lwvd-BGGKTE31ztgd-mE_Q](https://mp.weixin.qq.com/s/lwvd-BGGKTE31ztgd-mE_Q)


**引言**

Chiplet 技术代表着半导体设计的重要转变，通过将复杂的片上系统 (SoC) 分解为较小的模块化组件。这种方法提供了更大的灵活性和可扩展性，但成功的关键在于连接这些组件的互连架构。本文探讨 Chiplet 互连技术的主要方面和实施挑战[1]。


**互连基础**

互连在 Chiplet 架构中起着关键连接作用，包括多层连接。根据 Arm 公司系统架构师兼研究员 Rob Dimond 的说法，这包括单个 Chiplet 内的片上网络 (NoC)、各种内部互连，以及促进 Chiplet 之间数据传输的通用 Chiplet 互连快速通道 (UCIe)。互连架构必须高效处理内部数据移动和外部通信。
互连的物理实现通常依赖于导线，尽管未来的发展可能在封装之间和内部都采用光学互连。这些导线并不统一 - 在直径、密度、绝缘和材料成分上都有所不同，每种特性都会影响性能。导线的数量和特性直接影响设计决策和实施策略。


图 1：Alphawave 的多标准 I/O Chiplet，展示AlphaCHIP1600-IO 架构，具有 D2D UCIe PHY 层、流协议控制器以及用于以太网和 PCIe 连接的各种接口控制器。


**分区和架构考虑**

成功实施 Chiplet 需要仔细考虑分区策略。基本挑战在于理解如何有效地分散计算和数据流。这包括分析目标应用的要求，并确定在多个 Chiplet 之间划分功能的最佳方式。
例如，在 GPU 密集型应用中，现代语言模型的规模常常超过单个 GPU 的能力，需要在多个 Chiplet 之间进行分布式处理。这在保持数据一致性和管理 Chiplet 间通信带宽方面带来了额外的挑战。
汽车行业是 Chiplet 分区的特别有趣的案例。西门子数字工业软件的 David Fritz 解释了汽车制造商如何探索基于 Chiplet 的解决方案，通过改变系统中使用的 Chiplet 数量来提供不同性能层级。


**实施挑战与解决方案**
在实施基于 Chiplet 的系统时，必须解决几个关键挑战：

**1. 物理接口设计：**芯片间连接通常采用高速但相对窄的接口。这些连接必须采用数据包化方式，类似于通信协议，而不是传统的片上总线。这种方法允许在管理物理约束的同时进行高效的数据传输。
**2. 内存管理：**内存映射架构在 Chiplet 系统中变得极为重要。Arteris 的 Ashley Stevens 强调了在细粒度和粗粒度内存映射之间取得平衡的重要性。虽然细粒度映射可以均匀分布访问，但可能由于 Chiplet 间通信延迟而引入延迟问题。
**3. 测试和验证：**Chiplet 系统在测试和验证方面带来了新的挑战。Alphawave Semi 的 Letizia Giuliano 指出了开发新测试方法的必要性，特别是对于运行速度达到 32Gbps 及以上的高速接口。这包括在 PHY 层内开发特定的测试结构和实施全面的调试功能。


**未来方向和标准化**

行业正在推动 Chiplet 接口的标准化，包括 AMBA CHI、UCIe 和 BoW 等几个竞争协议。虽然英特尔、AMD、NVIDIA 和苹果等主要公司已经在实施 Chiplet 设计，但这些主要是专有解决方案。发展真正的商业 Chiplet 市场需要进一步的标准化和协作。
行业联盟正在形成以应对这些挑战。欧洲的 imec 汽车 Chiplet 计划 (ACP) 和日本的汽车 SoC 研究联盟 (ASRA) 正在致力于标准化架构方法和物理实现。这些努力的重点是创建可以在不同性能层级和应用中使用的可扩展解决方案。
实现完整的 Chiplet 生态系统需要在标准化和互操作性方面继续努力。正如 Keysight 的 Chun-Ting "Tim" Wang Lee 所指出的，确保不同 Chiplet 标准能够无缝协作仍然是行业面临的重大挑战。这种互操作性对于实现 Chiplet 技术的全部潜力和实现真正的即插即用 Chiplet 市场很重要。


**参考文献**
[1] Mutschler, "Chiplets make progress using interconnects as glue," Semiconductor Engineering, Oct. 31, 2024. [Online]. Available: https://semiengineering.com/chiplets-make-progress-using-interconnects-as-glue/ [Accessed: Dec. 1, 2024]


**END**


**软件申请**


我们欢迎化合物/硅基光电子芯片的研究人员和工程师申请体验免费版PIC Studio软件。无论是研究还是商业应用，PIC Studio都可提升您的工作效能。


点击左下角"阅读原文"马上申请


**欢迎转载**


转载请注明出处，请勿修改内容和删除作者信息！


**关注我们**

***关于我们：***
*深圳逍遥科技有限公司（Latitude Design Automation Inc.）是一家专注于半导体芯片设计自动化（EDA）的高科技软件公司。我们自主开发特色工艺芯片设计和仿真软件，提供成熟的设计解决方案如PIC Studio、MEMS Studio和Meta Studio，分别针对光电芯片、微机电系统、超透镜的设计与仿真。我们提供特色工艺的半导体芯片集成电路版图、IP和PDK工程服务，广泛服务于光通讯、光计算、光量子通信和微纳光子器件领域的头部客户。逍遥科技与国内外晶圆代工厂及硅光/MEMS中试线合作，推动特色工艺半导体产业链发展，致力于为客户提供前沿技术与服务。*
http://www.latitudeda.com/

（点击上方名片关注我们，发现更多精彩内容）

---
**Tags:** [[Chiplet]]
