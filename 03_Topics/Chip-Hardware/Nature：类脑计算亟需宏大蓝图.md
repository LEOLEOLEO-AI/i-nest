---
title: Nature：类脑计算亟需宏大蓝图
tags:
- brain
- chip
- chip-hardware
- chiplet
- deep-learning
- dynamics
- neural-networks
- neuron
- neuroscience
- paper
---
> 笔记本: 微信  
> 创建时间: 2022-05-19  

---

# Nature：类脑计算亟需宏大蓝图

          

                                      原创
                                                      
                                      A. Mehonic等
                                  
                                      
                        
              [
                集智俱乐部              ](#)
              
            
            *2022-05-19 20:00*
            *发表于北京*

          

          
                                                    

          
                    
                                        

          
                    

          
                              
                                        
                    
                    
          
          

            


**导语**


**与日俱增的算力需求下，现代计算系统能耗也越来越高，很难作为可持续的平台支持人工智能技术的未来发展。这一能源问题很大程度上源于传统数字计算系统采用经典冯·诺依曼结构，即数据处理和存储需要在不同地方进行；而在人脑中，数据处理和存储在同一个区域完成，且大规模并行。生物学的灵感启发了类脑计算，神经形态系统可以处理非结构化数据、完成图像识别、对噪声和不确定数据集进行分类、并参与建构更优的学习和推断系统，有望从根本上改变处理信号和数据的方式，无论是在能源效率方面，还是在处理现实世界的不确定性方面。然而，目前对神经形态计算的关注和投资远远落后于数字人工智能和量子技术，该如何发挥神经形态计算的潜力？近期发表于 *Nature *的文章认为，类脑计算亟需一幅宏大蓝图。**
 
**研究领****域：类脑计算，神经科学，人工智能******


****

A. Mehonic & A. J. Kenyon **| 作者**
任卡娜** | **翻译
JawDrin** | 审校**
邓一雪** | **编辑


论文题目：
Brain-inspired computing needs a master plan
论文链接：
https://www.nature.com/articles/s41586-021-04362-w


### 


**摘要**


类脑计算（Brain-inspired Computing，或译作“脑启发计算”）向我们描绘了一幅美好的愿景：按照根本不同的方式以极高的能源利用效率处理信息，并且能够处理人类正在增速产生的越来越多的非结构化与噪声数据。要想实现这样的愿景，我们亟需一张宏图，在资金、研究重点等方面提供支持，将不同的研究团体协调地聚集在一起。昨天，我们在数字技术上如此走过；今天，在量子技术上一如既往；那么明天，在类脑计算上所做的是否也应如此？


### 


**背景**


现代计算系统能耗过高，不能作为可持续的平台支持日益应用广泛的人工智能技术的发展。我们仅仅关注了速度、准确度、每秒并行操作数等功能，而忽略了可持续性，特别是在基于云的系统（Cloud-based Systems）的例子中。瞬间获取信息的习惯让我们忘记了实现这些功能的计算机系统会带来怎样的能源和环境消耗。例如，每次谷歌搜索都有数据中心的支持，而这样一个数据中心每年大约使用200太瓦时（terawatt）的能量，预计到2030年能耗还将增加一个数量级[1]。无独有偶，在高端人工智能系统中，以DeepMind引以为傲的、能够在复杂策略游戏中击败人类专家的 AlphaGo 和 AlphaGo Zero 为例，它们需要数千个并行处理单元，每个单元的功率大约200瓦，远超人脑的约20瓦[2]。

尽管并非所有数据密集型运算都用得上人工智能和深度学习，我们仍然需要担心应用越来越广的深度学习所带来的环境成本。此外，我们还应考虑包括物联网（Internat of Things, IoT）和自主机器人代理（Autonomous Robotic Agents）等不需计算密集型深度学习算法的应用，减少其能耗。若能耗需求过高，需要接入无数设备来运行的物联网也就无从谈起。分析表明，激增的算力需求远超摩尔定律（Moore's Law）带来的提升，算力需求翻倍现在只需要两个月（图1a）[3]。通过智能架构和软硬件协同设计的结合，我们正在取得越来越显著的进步。以NVIDA的图形处理器（Graphics Processing Units, GPU）为例，其性能自2012年已经提高了317倍，远超摩尔定律的预言（图1b），尽管与此同时，处理器能耗从25W增长到320W。研究与开发阶段不凡的性能提升（图1b，红色部分）昭示着我们可以做得更好[4-5]。但遗憾的是，单靠传统的计算解决方案无法满足长期需求。当想到大多复杂深度学习模型惊人的高训练成本时，这种遗憾尤其明显（图1c）。因此，我们需要新的出路。


图1：算力需求迅速增长。(a) 展示了在过去的40年中计算能力需求的增长，算力统计单位是petaFLOPS days：直到2012年，计算能力需求每24个月就翻一番，仍然是符合摩尔定律的增速；然而最近已经缩短到大约每2个月。不同颜色表示不同的应用领域[3]。(b) 展示了过去五年中人工智能硬件效率的提高：最先进的解决方案使计算效率提高了300多倍，研究和开发的解决方案有望进一步改进[22-24]。(c) 则展示了自2011年以来人工智能模型培训成本与日俱增[25]。

**能源问题很大程度上源于数字计算系统处理数据和储存数据是在不同地方，也就是支撑数字计算系统的经典冯·诺依曼结构**（von Neumann Architecture），这种结构决定了处理器要在移动数据上花费大部分的时间和能源。幸而生物学所带来的灵感给我们指了一条新的出路——在同一个区域完成储存与处理，以一种完全不同的方式编码信息，或者直接对信号进行操作，并采用大规模并行，这将在方框1中展开论述。其实，能源利用的高效和高级功能的行使可以兼得——我们的大脑就是明证。当然，关于我们的大脑如何做到兼得这二者，还有太多需要探索的奥秘。我们的目标并非仅仅简单模仿生物系统，而是要向过去几十年中神经科学与计算神经科学的重大进展当中找到出路。我们对大脑的了解已足以用来激发灵感。


### 


**生物学的启示**


在生物学中，数据存储并非独立于数据处理，比如人脑——主要是神经元和突触——以大规模并行和适应性的结构行使这两种功能。人脑平均包含1011个神经元和1015个突触，消耗大约20瓦功率；而一个相同大小的人工神经网络的数字模拟消耗7900千瓦[6]。这六个数量级的差距无疑是对我们的挑战。大脑直接以极高的效率处理噪声信号；这与传统计算机系统中时间和能源消耗巨大的信号-数据转换和高精度计算形成鲜明对比，即使是最强大的数字超级计算机对于大脑也是望尘莫及。因此，类脑计算系统（另译作神经形态计算）**有望从根本上改变我们处理信号和数据的方式，无论是在能源效率方面，还是在处理现实世界的不确定性方面。**

当然，这个想法的产生在科学发展历程中也是有迹可循的。“神经形态”（neuromorphic）一词描述的是模仿生物神经系统部分功能的设备和系统，在20世纪80年代末由加州理工学院的卡弗·米德（Carver Mead）创造[7-8]。灵感来自于过去几十年的工作，将神经系统建模为等效电路[9]，并构建模拟电子设备和系统，以提供类似的功能。


**方框1**


**当我们在说神经形态系统时，**
**我们在说什么？**

大脑带来的灵感使我们能以与现有传统计算系统完全不同的方式处理信息。不同的类脑计算平台（或神经形态计算平台）使用迥异于冯·诺依曼计算机的方法组合：模拟数据处理（Analogue Data Processing）、异步通信（Asychronous Communication）、大规模并行处理（Massively Parallel Processing, MPP）或者脉冲版的深度残差网络（Spiking Deep Residual Network, Spiking ResNet）等等。

神经形态四个字，涵盖了至少三个普遍的研究群体，可根据他们的研究目标进行区分：模拟神经功能（大脑逆向工程）、模拟神经网络（开发新计算方法）和设计新型电子设备。

（1）模拟神经功能

神经形态工程学研究的是大脑如何用突触、神经元这样的生物性结构的物理属性来完成“计算”。类脑工程师们利用模拟电子的物理原理模拟生物神经元和突触的功能，来定义处理音频、视频或智能传感器等行使功能所需要的基本操作，比如载体隧道（Carrier Tunneling）、硅浮栅上的荷电保持能力（Charge Retention）以及各种设备或材料属性对各种场呈指数增长的依赖性。更详细的信息可以在引文[41]中找到。

（2）模拟神经网络

类脑计算从生物学角度寻求新的数据处理方法，这也可以被理解为神经形态系统的计算科学。这个方向的研究着眼于模拟生物神经网络的结构和运作（结构或运作），也就是像大脑一样，在同一个区域完成储存与处理；或者采用基于电压尖峰来模拟生物系统动作电位这样完全不同的计算方法。

（3）设计新型电子设备

当然，巧妇难为无米之炊。我们需要支撑实现仿生功能所需的设备和材料。最近发展的可定制特性的电子和光子元件，能够帮助我们模仿突触和神经元等生物结构。这些神经形态工具提供的激动人心的新技术可以扩展神经形态工程和计算的能力。

在这些新元件中，最重要的是忆阻器：其电阻值是其历史阻值的函数。忆阻器复杂的动态电反应意味着它可以被用于数字记忆元件、人工突触中的可变权重、认知处理元件、光学传感器和模拟生物神经元的设备[42]等等。它们可能具备真正树突的部分功能[43]，而它们的动态反应也可以产生类似于大脑的振荡行为，在混沌边缘运行[44-45]。它们可能与单个系统中的生物神经元联系在一起[46]。它们只需很少能量便可完成这些功能。

数据漫谈。我们使用“数据”一词来描述编码在模拟信号或传感器的物理响应中的信息，或者更为标准的纯理论运算中的的数字信息。言及大脑“处理数据”，我们描述的是一套完整的信号处理任务，但是不依赖于传统意义上的信号数字化。想象一下类脑计算系统在从模拟信号处理到处理超大规模数据库这样不同的层次上运行：在前一种情况下，我们可以从一开始就避免生成大数据集；在后一种情况中，我们可以尽可能避免冯·诺伊曼模型的影响来大幅提高处理效率。我们的确有充分的理由来解释，为什么在许多场景中需要使用数字化的方式表示信号：高精确度、可靠性和确定性。然而，在晶体管物理学中发现，数字化抽象剔除了大量信息，而只追求最小的、量子化的信息：一个比特。在这样的过程中，我们付出了巨大的能源成本来用效率换取可靠性。由于人工智能的应用在本质上仍是概率的（probabilistic），因此我们必须考虑这种用效率换取可靠性是否有意义。由传统冯·诺伊曼计算机执行支撑人工智能应用的计算任务是非常计算密集的，也因此是能耗巨大的。然而，使用基于峰值（spike-based）的信号模拟或混合系统或许能够以高能效的方式执行类似任务。因此，人工智能系统的进步和新设备的出现，重新点燃人们对神经形态计算的兴趣。这些新设备提供了新的令人兴奋的方式来模拟生物神经系统的一些能力，详见方框1。

“神经形态”的定义各有千秋。一言蔽之，**这是一个关于硬件的故事：类脑芯片旨在整合和利用大脑的各种有用特征**，包括内存计算（in-memory computing，或译作“存算一体化”）、基于尖峰的信息处理（spike-based information processing）、细粒度并行性（fine-grained parallelism）、能够弹性应对噪声和随机性的信号处理、适应性、硬件学习、异步通信（asynchronous communication）和模拟处理（analogue processing）。尽管这其中需要具备多少才能被归类为神经形态尚无定论，但这显然是一种不同于主流计算系统上所实现的人工智能。然而，我们不应迷失在术语中，而应关注方法能否行之有效。

目前的神经形态技术方法仍然在解构与建构的两极之间上下求索：解构试图逆向拆解大脑结构和功能之间的深奥联系，建构则尽力从我们对于大脑有限的认识中寻找灵感。漫漫解构之路上，也许最重要的是人类脑计划（Human Brain Project, HBP），这个高调而野心勃勃的十年计划，自2013年起由欧盟开始资助。人类脑计划采用两个现有的类脑计算平台，并将进一步开发开放可访问的类脑计算平台，也就是曼彻斯特大学的 SpiNNaker 和海德堡大学的 BrainScaleS。这两个平台都实现了高度复杂的大脑结构硅模型来帮助我们更好地理解生物大脑的运作。而建构同样是筚路蓝缕，许多团队使用类脑计算的方法来增强数字或模拟电子设备的性能。图2总结了现有神经形态芯片范畴，根据在分析-合成和技术平台中不同的位置将其划分为四类。对我们来说更重要的是意识到，神经形态工程不仅仅是高级认知系统，在认知能力有限的小型边缘设备中它能同时提供能量、速度和安全方面的收益（起码可通过消除与云持续通信的需求来实现）。


图2. 类脑芯片的图景。主流的类脑芯片根据其在解构-建构（分析-合成）研究中扮演的不同角色和技术平台的不同，分为四类：模拟生物系统或类脑计算应用可以二分，进一步通过实现方式将这两类再细分为基于新架构的数字CMOS（Complementary Metal Oxide Semiconductor，互补金属氧化物半导体）实现（如数字模拟峰值而非电压模拟），或使用模拟电路实现。无论落在哪一个部分，这些类脑芯片至少具备右侧列出的部分特性，这使它们有别于传统的CMOS芯片。右上角标注a表示搭载忆阻器。

类脑芯片相关参考资料[26-40]：
- 
Neurogrid：Benjamin, B. V. et al. Neurogrid: a mixed-analog–digital multichip system for large-scale neural simulations. Proc. IEEE 102, 699–716 (2014).
- 
BrainSclaseS：Schmitt, S. et al. Neuromorphic hardware in the loop: training a deep spiking network on the BrainScaleS wafer-scale system. In 2017 Intl Joint Conf. Neural Networks (IJCNN) https://doi.org/10.1109/ijcnn.2017.7966125 (IEEE, 2017).
- 
MNIFAT：Lichtsteiner, P., Posch, C. & Delbruck, T. A 128 × 128 120 dB 15 μs latency asynchronous temporal contrast vision sensor. IEEE J. Solid-State Circuits 43, 566–576 (2008).
- 
DYNAP：Moradi, S., Qiao, N., Stefanini, F. & Indiveri, G. A scalable multicore architecture with heterogeneous memory structures for dynamic neuromorphic asynchronous processors (DYNAPs). IEEE Trans. Biomed. Circuits Syst. 12, 106–122 (2018).
- 
DYNAP-SEL：Thakur, C. S. et al. Large-scale neuromorphic spiking array processors: a quest to mimic the brain. Front. Neurosci. 12, 891 (2018).
- 
ROLLS：Qiao, N. et al. A reconfigurable on-line learning spiking neuromorphic processor comprising 256 neurons and 128K synapses. Front. Neurosci. 9, 141 (2015).
- 
Spirit：Valentian, A. et al. in 2019 IEEE Intl Electron Devices Meeting (IEDM) 14.3.1–14.3.4 https://doi.org/10.1109/IEDM19573.2019.8993431 (IEEE, 2019).
- 
ReASOn：Resistive Array of Synapses with ONline Learning (ReASOn) Developed by NeuRAM3 Project https://cordis.europa.eu/project/id/687299/reporting (2021).
- 
DeepSouth：Wang, R. et al. Neuromorphic hardware architecture using the neural engineering framework for pattern recognition. IEEE Trans. Biomed. Circuits Syst. 11, 574–584 (2017).
- 
SpiNNaker：Furber, S. B., Galluppi, F., Temple, S. & Plana, L. A. The SpiNNaker Project. Proc. IEEE 102, 652–665 (2014). An example of a large-scale neuromorphic system as a model for the brain.
- 
IBM TrueNorth：Merolla, P. A. et al. A million spiking-neuron integrated circuit with a scalable communication network and interface. Science 345, 668–673 (2014).
- 
Intel Loihi：Davies, M. et al. Loihi: a neuromorphic manycore processor with on-chip learning. IEEE Micro 38, 82–99 (2018).
- 
Tianjic：Pei, J. et al. Towards artificial general intelligence with hybrid Tianjic chip architecture. Nature 572, 106–111 (2019).
- 
ODIN：Frenkel, C., Lefebvre, M., Legat, J.-D. & Bol, D. A 0.086-mm2 12.7-pJ/SOP 64k-synapse 256-neuron online-learning digital spiking neuromorphic processor in 28-nm CMOS. IEEE Trans. Biomed. Circuits Syst. 13, 145–158 (2018).
- 
Intel SNN chip：Chen, G. K., Kumar, R., Sumbul, H. E., Knag, P. C. & Krishnamurthy, R. K. A 4096-neuron 1M-synapse 3.8-pJ/SOP spiking neural network with on-chip STDP learning and sparse weights in 10-nm FinFET CMOS. IEEE J. Solid-State Circuits 54, 992–1002 (2019).


### 


**前景展望**


我们之意不是神经形态系统会（或应该）取代传统计算平台。相反，**精密计算就应该保留数字计算，神经形态系统则可以处理非结构化数据、完成图像识别、对噪声和不确定数据集进行分类、并参与建构更优的学习和推断系统**。比如在自主和物联网系统的例子中，它们可以比传统方法节省更多能源。而量子计算也是未来图景的一部分。尽管根据最乐观的估计，量子计算系统的实际应用尚需时日，但它一定会彻底改变许多计算任务。然而，物联网智能传感器、边缘计算设备或自主机器人系统使用不依赖云计算的量子计算是不可能的。因为仍需能够处理不确定和噪声数据的低功率计算元件。读者不妨想象一下**数字系统、类脑系统和量子系统三方协作，各司其职、扬长避短的未来图景，那会是什么样的？**

类脑计算是一个大跨度的交叉学科，正如半导体微电子学的发展依赖于包括固体物理学、电子工程学、计算机科学和材料科学在内的许多不同学科那样。物理学家、化学家、工程师、计算机科学家、生物学家和神经科学家都需要参与到其发展进程中。道阻且长，哪怕是让来自不同学科的研究人员互相理解专业术语就已足够困难。本研究即是明证。作为联系了计算机科学（特别是人工智能）和神经科学（最初是计算神经科学）的研究，身处“同一个房间”里的人们花费了大量的时间和精力，来确保每个人都以相同的方式理解术语和概念。毕竟当今最先进的人工智能系统中，许多概念——尽管不需要完全仿生——仍然得追溯到20世纪70年代和80年代的神经科学领域。我们必须张开双臂去拥抱其他学科，尤其是认识到在人工智能或神经科学方面取得的许多进展都是在不同的学科帮助下共同推动的，像是材料科学、纳米技术或电子工程的创新。还有如意识到传统的CMOS技术可能不是有效地实现类脑算法的最佳结构，因此需要全面创新。尽早参与和实现学科交流与交叉，可以避免在已经探索失败的方向重蹈覆辙或是竹篮打水一场空。

此外，我们不应忽视在系统层面整合新神经形态技术的挑战。除了开发类脑算法和工具，更紧迫的问题是如何用功能等效的神经形态替代方案取代现有的主流人工智能系统。这进一步强调了对类脑计算的集大成的需要。

尽管有上述潜力，目前尚没有类脑技术商用的成功案例可以参考。现有的系统和平台主要是研究工具，量子计算亦是如此，且是一个更长期的愿景。但是这样的现状不该成为延误类脑计算发展的障碍，解决低功耗计算系统的需求也迫在眉睫。不过我们已经非常接近于实现这一目标，因为所有附加功能都来自于类脑计算这种截然不同的计算方法。商业体系也将必然诞生。


### 


**把握机遇**


若神经形态计算是必须的，那将如何实现？技术要求首当其冲。将不同研究团体聚集在一起虽是必要但不充分，还需要激励、机遇和基础设施。与其他社群相比，神经形态社群完全不同，缺乏对量子计算的关注，也不了解半导体行业的大局。全球各地的项目也已开始收集必要的专业知识，且势头正紧。对神经形态研究的投资远不及数字人工智能或量子技术（方框2）。考虑到数字半导体技术的成熟，上述现象便不足以为奇，但却是一个错失的良机。诚然，有不少中等规模神经形态研究研究和开发投资的例子，如IBM人工智能硬件中心的一系列脑启发研究（像前文图2中提到的TrueNorth芯片）、Intel公司Loihi处理器的开发、以及美国的脑计划（Brain Initiative Project），但目前的投资远远低于其应得的水平，毕竟这样的技术有可能颠覆数字人工智能。

神经形态社群正在蓬勃发展、不断壮大，但也难免缺乏一个共同的关注点。尽管会议、专题讨论会和期刊不断地总结更新着人们对这一领域的认识，神经形态与类脑领域终究大业未竟，比如说服资助机构和政府认识到这一领域的重要性。

在神经形态与类脑领域采取大动作也已时机成熟。**国家层面而言，政府应当打通产学研三方，创建以任务为导向的研究中心，推进神经形态技术的发展**。这招在量子技术和纳米技术等领域屡试不爽，美国国家纳米技术计划（National Nanotechnology Initiative）就是绝佳的例子[10]。这样的研究中心可以是实体机构也可以是虚拟机构，但必须把不同领域最优秀的研究人员聚集在一起。这些人需要采用异于传统信息技术的新方法（在传统信息技术中，材料、设备、电路、系统、算法和应用程序等每一个抽象概念都需要不同社群的支持）。我们需要对整个社群进行全面而同步的设计。譬如电子工程师仅仅在设计系统之前咨询计算神经科学家是不够的，工程师和神经科学家的通力合作应该贯穿在整个过程中，以确保尽可能充分地将各自领域的原理集成到硬件和更多工作当中。凡此种种足见：跨学科的合作创造是第一要务！因此研究中心应积极招徕广大的研究人员。

具备了物质和经济基础，一支有合作自觉的研究者队伍更是关键。电子工程师很少接触神经科学的想法，反之亦然。电子工程师和物理学家可能对神经元和突触的生物学特点具备一定常识，但不太可能了解前沿的计算神经科学。**一个值得参考的做法是设立硕士课程和博士培训项目来培养神经形态工程师**。英国研究理事会赞助了博士培养中心（Centres for Doctoral Training, CDTs），其重点项目支持需要重点关注的领域。CDT可以是独立机构，也可以是合作机构。通过建立跨机构的互补性团队，各机构在交叉领域进行合作大有裨益。这样的项目往往又与产业界密切合作，以常规博士培养项目望尘莫及的方式培养出高素质的研究人员。这当然是新兴的神经形态工程社群所值得借鉴的经验，从而促进社群间的互动，也能够从中诞生下一代的研究人员和研究领导者。首创的案例有：格罗宁根大学认知系统和材料研究项目[11]、慕尼黑工业大学的神经工程硕士项目[12]、苏黎世联邦理工学院的神经形态工程模拟电路设计课程[13]、斯坦福大学的大规模神经模型[14]以及塞维利亚微电子学院（Microelectrónica de Sevilla）的视觉神经形态系统的发展课程[15]等等。路漫漫其修远兮。

在国家之间也亟需这样的合作，正如在研究领域一样，**不分国界的最优秀人群之间的合作才是最成功的**。在神经形态计算这样的跨学科研究中，这是至关重要的，因此国际研究网络和项目无疑要发挥作用。早期的例子包括专注于神经形态计算技术的欧洲神经技术联盟（European Neurotech consortium）[16]，以及德累斯顿大学的汇集了材料、设备和算法领域的许多最优秀研究者的Chua忆阻器中心（Chua Memristor Centre）[17]。同样，宁可一思进，莫在一思停。

那么**如何吸引到政府的支持**呢？政府承诺高能效的生物启发计算，是推动大规模节能减排的一部分。这不仅可以解决气候变化问题，还将加速孵育更多围绕大数据、物联网、医疗保健分析、药物和疫苗研发建模以及机器人等新兴低碳产业。如果现有行业依赖于更大规模的传统数字数据分析，将会增加能源成本同时表现出次优性能。相反，我们可以创造良性循环，在这个循环中，大大减少知识技术的碳足迹，这些技术还将推动下一代颠覆性的产业，与此同时又为一系列新兴神经形态产业创造环境。

如果这条路听起来怎么都像画大饼，不妨看看量子技术领域的成功经验。依托于国家量子技术计划（National Quantum Technologies Programme），英国政府迄今为止已经为一系列量子计划投入了大约10亿英镑，催生出的研究中心汇集了工业界和学术界，将量子科学转化为针对传感器和计量、成像、通信和计算的技术。一个独立的、软硬件俱全的国家量子计算中心（National Quantum Computing Centre）就建立在这些中心和其他研究人员的工作之上，正在开发通用量子计算机。中国已经建立了价值数十亿美元的中国量子信息科学国家实验室，美国也在2018年委托进行了量子信息科学国家战略概述（National Strategic Overview for Quantum Information Science）[18]，并开展了一项为期5年、投入12亿美元来支持一系列国家量子研究中心的计划[19]。得益于这些国家财政支持与政策红利，全球掀起了一股创立量子技术公司的热潮。一项分析发现，2017和2018年，相关私营公司的融资已经达到4.5亿美元[20]——政策的有力引导作用可见一斑。尽管神经形态计算技术比量子技术更成熟，也尽管它有可能在更短时间内颠覆现有的人工智能技术，但对于神经形态计算的这种支持仍并不存在。神经形态计算可以说是未来计算三大方向中的“灰姑娘”。

最后，谈谈COVID-19大流行可能对本研究观点带来的影响。这场危机如何加速了世界运作方式的改变，各位有目共睹：例如，更多人居家办公。尽管减少通勤和旅行带来直接的好处，如部分研究认为，疫情带来的全球二氧化碳减排可能高达17%[21]，但新的工作方式自有其代价。减少通勤和旅行带来的减排能在多大程度上被数据中心的增排所抵消？本质上，新冠疫情进一步强调了开发神经形态计算系统等低碳计算技术的必要性。


**方框2**


**人工智能融资前景**

得益于见长的数据处理需求以及支持现有计算和内存密集型算法的硬件开发，数字人工智能领域的投资正在蓬勃发展。英国政府在2018年4月宣布，除了既定的研究委员会资助，另外投入9.5亿英镑支持数字人工智能行业发展。法国政府则宣布，2018-2022年将在人工智能领域投资18亿欧元[47]。德国承诺从2018-2025年投资30亿欧元。日本在2017年投资26万亿日元。美国政府在2020年对民用人工智能技术的资助为9.73亿美元[48]。另外，由于非人工智能项目经常被夹带发表在分析中，美国军方的人工智能资助数据较难获得。据估计，中国在民用和军用人工智能领域投资将高达80亿美元，北京附近建设一个21亿美元的人工智能研究园区[49]。欧盟委员会承诺在2018年至2050年期间投资15亿美元[50]。当然相较商业投资，这些不可谓多也。保守估计，美国在2019年对人工智能公司的商业投资高达195亿美元[51]。到2023年，全球商业投资预计将达到980亿美元左右[52]。如果我们当前的硬件系统无法支撑有创新潜能的神经形态算法和架构，就应考虑这样的投资金额存在风险。如果神经形态技术能够像它们所承诺的那样提供效率节约和性能提升，那么聪明的投资者就会在押注数字系统的同时，押注新技术和架构。

由于神经形态技术目前仍然缺乏关注和政府层面的重视，因此其研究资金林林总总，基本是项目层面而非战略层面的。虽然已有乐观估计，比如全球类脑芯片市场将从2021年的2270万美元增长到2026年的5506亿美元[53]，但目前的结论仍然是：神经形态系统的投资远远落后于数字人工智能或量子技术。


图3. 数字人工智能技术近期全球公共研究资金的比较。上图数据以2021年汇率的美元等值表示，单位百万美元。部分国家研究资金以年为单位计算（例如UKRI承诺的2020年资金），部分则没有特定的期限（例如英国人工智能领域的协议），另外还有多年计划。上图展示了数字技术领域公共资金的规模，但是更高效的神经形态与类脑技术的发展势必威胁现有的人工智能研究投资生态。


### 


**结语**


关于如何发挥好神经形态的潜力，行文至此，已经了然：通过建立卓越研究中心，为合作研究提供有针对性的支持；提供灵活的资助机制以实现快速进展；提供与产业界密切合作的机制，引入商业资金并孵化新的产业和企业，尤其参考量子技术的发展；为下一代神经形态研究人员和领导者制定培训方案；以上，更快、更广地推行。

类脑计算有望改变实现人工智能的途径，在技术进步和需求增长的时代背景下，良机已至，既需勇敢的思考，又要勇敢的倡议者支持这些思考。我们会抓住机遇吗？


**参考文献**


- 
Jones, N. How to stop data centres from gobbling up the world’s electricity. Nature https://doi.org/10.1038/d41586-018-06610-y (12 September 2018).
- 
Wu, K. J. Google’s new AI is a master of games, but how does it compare to the human mind? Smithsonian https://www.smithsonianmag.com/innovation/google-ai-deepminds-alphazero-games-chess-and-go-180970981/ (10 December 2018).
- 
Amodei, D. & Hernandez, D. AI and compute. OpenAI Blog https://openai.com/blog/ai-and-compute/ (16 May 2018).
- 
Venkatesan, R. et al. in 2019 IEEE Hot Chips 31 Symp. (HCS) https://doi.org/10.1109/HOTCHIPS.2019.8875657 (IEEE, 2019).
- 
Venkatesan, R. et al. in 2019 IEEE/ACM Intl Conf. Computer-Aided Design (ICCAD) https://doi.org/10.1109/ICCAD45719.2019.8942127 (IEEE, 2019).
- 
Wong, T. M. et al. 1014. Report no. RJ10502 (ALM1211-004) (IBM, 2012). The power consumption of this simulation of the brain puts that of conventional digital systems into context.
- 
Mead, C. Analog VLSI and Neural Systems (Addison-Wesley, 1989).
- 
Mead, C. A. Author Correction: How we created neuromorphic engineering. Nat. Electron. 3, 579–579 (2020).
- 
Hodgkin, A. L. & Huxley, A. F. A quantitative description of membrane current and its application to conduction and excitation in nerve. J. Physiol. 117, 500–544 (1952). More complex models followed, but this seminal work remains the clearest and an excellent starting point, developing equivalent electrical circuits and circuit models for the neural membrane.
- 
National Nanotechnology Initiative. US National Nanotechnology Initiative https://www.nano.gov (National Nanotechnology Coordination Office, accessed 18 August 2021).
- 
About Groningen Cognitive Systems and Materials. University of Groningen https://www.rug.nl/research/fse/cognitive-systems-and-materials/about/ (accessed 9 November 2020).
- 
Degree programs: Neuroengineering. Technical University of Munich https://www.tum.de/en/studies/degree-programs/detail/detail/StudyCourse/neuroengineering-master-of-science-msc/ (accessed 18 August 2021).
- 
Course catalogue: 227-1033-00L Neuromorphic Engineering I. ETH Zürich http://www.vvz.ethz.ch/Vorlesungsverzeichnis/lerneinheit.view?lerneinheitId=132789&semkez=2019W&ansicht=KATALOGDATEN&lang=en (accessed 9 November 2020).
- 
Brains in Silicon. http://web.stanford.edu/group/brainsinsilicon/ (accessed 16 March 2022).
- 
Neuromorphs. Instituto de Microelectrónica de Sevilla http://www2.imse-cnm.csic.es/neuromorphs (accessed 9 November 2020).
- 
Neurotech. https://neurotechai.eu (accessed 18 August 2021).
- 
Chua Memristor Center: Members. Technische Universität Dresden https://cmc-dresden.org/members (accessed 9 November 2020).
- 
Subcommittee on Quantum Information Science. National Strategic Overview for Quantum Information Science. https://web.archive.org/web/20201109201659/https://www.whitehouse.gov/wp-content/uploads/2018/09/National-Strategic-Overview-for-Quantum-Information-Science.pdf (US Government, 2018; accessed 17 March 2022).
- 
Smith-Goodson, P. Quantum USA vs. quantum China: the world’s most important technology race. Forbes https://www.forbes.com/sites/moorinsights/2019/10/10/quantum-usa-vs-quantum-china-the-worlds-most-important-technology-race/#371aad5172de (10 October 2019).
- 
Gibney, E. Quantum gold rush: the private funding pouring into quantum start-ups. Nature https://doi.org/10.1038/d41586-019-02935-4 (2 October 2019).
- 
Le Quéré, C. et al. Temporary reduction in daily global CO2 emissions during the COVID-19 forced confinement. Nat. Clim. Change 10, 647–653 (2020).
- 
Gokmen, T. &  Vlasov, Y. Acceleration of deep neural network training with resistive cross-point devices: design considerations. Front. Neurosci. 1010.3389/fnins.2016.00333 (2016).
- 
Marinella, M. J. et al. Multiscale co-design analysis of energy latency area and accuracy of a ReRAM analog neural training accelerator. IEEE J. Emerg. Selected Topics Circuits Systems 8, 86–101 (2018).
- 
Chang, H.-Y. et al. AI hardware acceleration with analog memory: microarchitectures for low energy at high speed. IBM J. Res. Dev. 63, 8:1–8:14 (2019).
- 
ARK Invest. Big Ideas 2021 https://research.ark-invest.com/hubfs/1_Download_Files_ARK-Invest/White_Papers/ARK–Invest_BigIdeas_2021.pdf (ARK Investment Management, 2021; accessed 27 April 2021).
- 
Benjamin, B. V. et al. Neurogrid: a mixed-analog–digital multichip system for large-scale neural simulations. Proc. IEEE 102, 699–716 (2014).
- 
Schmitt, S. et al. Neuromorphic hardware in the loop: training a deep spiking network on the BrainScaleS wafer-scale system. In 2017 Intl Joint Conf. Neural Networks (IJCNN) https://doi.org/10.1109/ijcnn.2017.7966125 (IEEE, 2017).
- 
Lichtsteiner, P., Posch, C. & Delbruck, T. A 128 × 128 120 dB 15 μs latency asynchronous temporal contrast vision sensor. IEEE J. Solid-State Circuits 43, 566–576 (2008).
- 
Moradi, S., Qiao, N., Stefanini, F. & Indiveri, G. A scalable multicore architecture with heterogeneous memory structures for dynamic neuromorphic asynchronous processors (DYNAPs). IEEE Trans. Biomed. Circuits Syst. 12, 106–122 (2018).
- 
Thakur, C. S. et al. Large-scale neuromorphic spiking array processors: a quest to mimic the brain. Front. Neurosci. 12, 891 (2018).
- 
Qiao, N. et al. A reconfigurable on-line learning spiking neuromorphic processor comprising 256 neurons and 128K synapses. Front. Neurosci. 9, 141 (2015).
- 
Valentian, A. et al. in 2019 IEEE Intl Electron Devices Meeting (IEDM) 14.3.1–14.3.4 https://doi.org/10.1109/IEDM19573.2019.8993431 (IEEE, 2019).
- 
Resistive Array of Synapses with ONline Learning (ReASOn) Developed by NeuRAM3 Project https://cordis.europa.eu/project/id/687299/reporting (2021).
- 
Wang, R. et al. Neuromorphic hardware architecture using the neural engineering framework for pattern recognition. IEEE Trans. Biomed. Circuits Syst. 11, 574–584 (2017).
- 
Furber, S. B., Galluppi, F., Temple, S. & Plana, L. A. The SpiNNaker Project. Proc. IEEE 102, 652–665 (2014). An example of a large-scale neuromorphic system as a model for the brain.
- 
Merolla, P. A. et al. A million spiking-neuron integrated circuit with a scalable communication network and interface. Science 345, 668–673 (2014).
- 
Davies, M. et al. Loihi: a neuromorphic manycore processor with on-chip learning. IEEE Micro 38, 82–99 (2018).
- 
Pei, J. et al. Towards artificial general intelligence with hybrid Tianjic chip architecture. Nature 572, 106–111 (2019).
- 
Frenkel, C., Lefebvre, M., Legat, J.-D. & Bol, D. A 0.086-mm2 12.7-pJ/SOP 64k-synapse 256-neuron online-learning digital spiking neuromorphic processor in 28-nm CMOS. IEEE Trans. Biomed. Circuits Syst. 13, 145–158 (2018).
- 
Chen, G. K., Kumar, R., Sumbul, H. E., Knag, P. C. & Krishnamurthy, R. K. A 4096-neuron 1M-synapse 3.8-pJ/SOP spiking neural network with on-chip STDP learning and sparse weights in 10-nm FinFET CMOS. IEEE J. Solid-State Circuits 54, 992–1002 (2019).
- 
Indiveri, G. et al. Neuromorphic silicon neuron circuits. Front. Neurosci. 5, 73 (2011).
- 
Mehonic, A. et al. Memristors—from in‐memory computing, deep learning acceleration, and spiking neural networks to the future of neuromorphic and bio‐inspired computing. Adv. Intell Syst. 2, 2000085 (2020). A review of the promise of memristors across a range of applications, including spike-based neuromorphic systems.
- 
Li, X. et al. Power-efficient neural network with artificial dendrites. Nat. Nanotechnol. 15, 776–782 (2020).
- 
Chua, L. Memristor, Hodgkin–Huxley, and edge of chaos. Nanotechnology 24, 383001 (2013)
- 
Kumar, S., Strachan, J. P. & Williams, R. S. Chaotic dynamics in nanoscale NbO2 Mott memristors for analogue computing. Nature 548, 318–321 (2017).
- 
Serb, A. et al. Memristive synapses connect brain and silicon spiking neurons. Sci Rep. 10, 2590 (2020).
- 
Rosemain, M. & Rose, M. France to spend $1.8 billion on AI to compete with U.S., China. Reuters https://www.reuters.com/article/us-france-tech-idUSKBN1H51XP (29 March 2018).
- 
Castellanos, S. Executives say $1 billion for AI research isn’t enough. Wall Street J. https://www.wsj.com/articles/executives-say-1-billion-for-ai-research-isnt-enough-11568153863 (10 September 2019).
- 
Larson, C. China’s AI imperative. Science 359, 628–630 (2018).
- 
European Commission. A European approach to artificial intelligence. https://ec.europa.eu/digital-single-market/en/artificial-intelligence (accessed 9 November 2020).
- 
Artificial intelligence (AI) funding investment in the United States from 2011 to 2019. Statista https://www.statista.com/statistics/672712/ai-funding-united-states (accessed 9 November 2020).
- 
Worldwide artificial intelligence spending guide. IDC Trackers https://www.idc.com/getdoc.jsp?containerId=IDC_P33198 (accessed 9 November 2020).
- 
Markets and Markets.com. Neuromorphic Computing Market https://www.marketsandmarkets.com/Market-Reports/neuromorphic-chip-market-227703024.html?gclid=CjwKCAjwlcaRBhBYEiwAK341jS3mzHf9nSlOEcj3MxSj27HVewqXDR2v4TlsZYaH1RWC4qdM0fKdlxoC3NYQAvD_BwE. (accessed 17 March 2022).


（参考文献可**上下滑动**查看）


**神经动力学模型读书会**


随着电生理学、网络建模、机器学习、统计物理、类脑计算等多种技术方法的发展，我们对大脑神经元相互作用机理与连接机制，对意识、语言、情绪、记忆、社交等功能的认识逐渐深入，大脑复杂系统的谜底正在被揭开。为了促进神经科学、系统科学、计算机科学等领域研究者的交流合作，我们发起了【[神经动力学模型读书会](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247603702&idx=1&sn=155301af87026492ed1591e0bb7e8c81&chksm=e8960f7bdfe1866ddd8d76d5c419528f5b28bd8b69386d97eac1ec11c9ea7c3cad94453d9c2e&scene=21#wechat_redirect)】。

集智俱乐部读书会是面向广大科研工作者的系列论文研读活动，其目的是共同深入学习探讨某个科学议题，激发科研灵感，促进科研合作。【[神经动力学模型读书会](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247603702&idx=1&sn=155301af87026492ed1591e0bb7e8c81&chksm=e8960f7bdfe1866ddd8d76d5c419528f5b28bd8b69386d97eac1ec11c9ea7c3cad94453d9c2e&scene=21#wechat_redirect)】由集智俱乐部和天桥脑科学研究院联合发起，已于3月19日开始，每周六下午14:00-16:00（或每周五晚上19:00-21:00，根据实际情况调整）进行，预计持续10-12周。期间将围绕神经网络多尺度建模及其在脑疾病、脑认知方面的应用进行研讨。

[ ](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247603702&idx=1&sn=155301af87026492ed1591e0bb7e8c81&chksm=e8960f7bdfe1866ddd8d76d5c419528f5b28bd8b69386d97eac1ec11c9ea7c3cad94453d9c2e&scene=21#wechat_redirect)


详情请见：
**[神经动力学模型读书会启动：整合计算神经科学的多学科方法](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247603702&idx=1&sn=155301af87026492ed1591e0bb7e8c81&chksm=e8960f7bdfe1866ddd8d76d5c419528f5b28bd8b69386d97eac1ec11c9ea7c3cad94453d9c2e&scene=21#wechat_redirect)**


**推荐阅读**
- 
[类脑计算前沿：基于有机电化学网络的生物信号分类](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247578273&idx=2&sn=749ad588e878c26f15fa001b6dadae91&chksm=e896e82cdfe1613a8e5cae9694ad090262da58892c0393815434f1e649e3ed0cc0f551aa3876&scene=21#wechat_redirect)
- 
[网络神经科学前沿：大脑如何在局部和全局高效处理信息？](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247565303&idx=1&sn=390493ed2f4d0d62c5424939c9d75617&chksm=e896a57adfe12c6c35563e1a2ece3eac63fc76b9b1f3798265898defa1c2d03d3c374116558a&scene=21#wechat_redirect)
- 
[李飞飞团队：如何制造更聪明的人工智能？让人工生命在复杂环境中进化](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247586008&idx=1&sn=a001a32c5c7c203663f095827bc4d004&chksm=e896ca55dfe14343953c8dc37d976bdd753d8c8bbbb4abb7e34ea7318864b884db9dceeb9bd0&scene=21#wechat_redirect)
- 
[《张江·复杂科学前沿27讲》完整上线！](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247576923&idx=2&sn=57f0d320812c01ff6f5ea97c09fc9623&chksm=e896f7d6dfe17ec038e8d238dae313119fca8c62aabd4730896bc99398db981dd5d9d3e0b927&scene=21#wechat_redirect)
- 
[成为集智VIP，解锁全站课程／读书会](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247555842&idx=1&sn=383e07df94e429aa66628a22471b37dc&chksm=e897418fdfe0c899169c672f35d92217a17a558ea929f85aef402b1ec074ed2e1176472a3cc7&scene=21#wechat_redirect)
- 
[**加入集智，一起复杂！**********](http://mp.weixin.qq.com/s?__biz=MzIzMjQyNzQ5MA==&mid=2247617062&idx=1&sn=e963acb6885ea3b26d32e91c12eae076&chksm=e89650abdfe1d9bddf82c71e612a15bc4393d0a61cde39d325b01b3099247145c98b492c37b8&scene=21#wechat_redirect)


**点击“阅读原文”，报名读书会**
          

          

          


           
                                
                    
        
                        
                
        
        

        

        
        


[阅读原文](#)

              
    

    

    
    

      

        
        

        
        

   
     
                 喜欢此内容的人还喜欢                 
              
   
      
       
         
           GAN之父Ian Goodfellow离职苹果：不想重返办公室工作                             
           
             GAN之父Ian Goodfellow离职苹果：不想重返办公室工作                                   
           
             ...                                               
         
           
             机器之心                      
                                          
                                      
                                 
             
               
不看的原因                                         
                                                                    
- 内容质量低                                    
- 不看此公众号                                                                                                   
       
      
       
         
           谷歌I/O四大更新：科技本质不是硬件和软件，而是知识与计算                             
           
             谷歌I/O四大更新：科技本质不是硬件和软件，而是知识与计算                                   
           
             ...                                               
         
           
             硅星人                      
                                          
                                      
                                 
             
               
不看的原因                                         
                                                                    
- 内容质量低                                    
- 不看此公众号                                                                                                   
       
      
       
         
           号称最强深度学习笔记本电脑，雷蛇与Lambda公司推出，售价超2万                             
           
             号称最强深度学习笔记本电脑，雷蛇与Lambda公司推出，售价超2万                                   
           
             ...                                               
         
           
             机器之心                      
                                          
                                      
                                 
             
               
不看的原因                                         
                                                                    
- 内容质量低                                    
- 不看此公众号                                                                                                   
             
        
        


      
    

    
    

      

        

          
          
微信扫一扫关注该公众号

---
**Tags:** [[BrainInspired]] [[SDSoW]] [[Chiplet]]
