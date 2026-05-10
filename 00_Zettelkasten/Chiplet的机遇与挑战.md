# Chiplet的机遇与挑战

> 笔记本: 微信  
> 创建时间: 2020-10-06  

---

速读摘要
随着IC制造工艺的升级，芯片性能和功耗方面的成本效益变得越来越低。2架构通过在不同的处理节点中组合多个处理器核心芯片(7纳米工艺)，IO芯片(14纳米工艺)和内存芯片来构建chiplet。10在3个芯片代工厂的6个工艺节点中集成了die，从而有效地证明了芯片技术在不同代工厂之间的互操作性。它证明了chiplet技术在构建高科技工艺和具有高IO性能的芯片方面的可行性。由zGlue开发和制造的芯片(例如蓝牙，物联网和WiFi)是基于ADI，Dialog，Macronix和Vishay等30多家公司的近100个芯片开发的。
原文约 9908  字   |  图片 10 张  |  建议阅读 20 分钟  |  [评价反馈](https://static.app.yinxiang.com/embedded-web/clipper/#/Evaluating?d=2020-10-06&nu=1f2b6f8b-0fec-4559-86e8-e40c93193e56&fr=myyxbj&ud=1bb10ab&v=2&sig=7AC1A11C7FAABD8D57C7B925C134D433)

 


##  Chiplet的机遇与挑战 

 半导体行业观察 **


来源：本文来自electronics，作者:Tao Li, Jie Hou, Jinli Yan, Rulin Liu, Hui Yang, Zhigang Sun,谢谢。

经过几十年的快速发展，大规模集成电路已经成为信息技术的核心。IC制造工艺随着摩尔定律的发展而不断发展，如今7纳米工艺已进入生产阶段，5纳米和3纳米工艺也在稳步推进。工艺节点的每一次突破都伴随着性能提升和功耗下降。但是，随着IC制造工艺的复杂性急剧增加，流片成本也大大增加。例如，用于构建新的GPU， CPU或SoC的设计成本为3000万，这给很多领域的芯片设计带来了巨大挑战 。

摩尔定律和Dennard定律的放缓和停滞加剧了这个问题。具体而言，摩尔定律自2000年以来就有放缓的迹象。到2008年，芯片实际性能与摩尔定律的要求之间的差距增加了15倍。Dennard定律在2007年开始显著放缓，并在2012年几乎消失。随着IC制造工艺的升级，芯片性能和功耗方面的成本效益变得越来越低。半导体行业和学术界普遍认为，后摩尔时代将很快到来，这意味着长期研究会更多地集中在摩尔技术领域，以及半导体行业的各个层面的规模化过程，比如设计，器件，架构和封装工艺，甚至去探索beyond CMOS 的新器件以维持功率，性能和面积以及成本（PPAC）的调整。

随着摩尔定律框架下集成技术的进一步发展，基于芯片的设计技术已经从三个方面解决了上述问题。

首先，chiplet试图将多个模块化芯片（模块化芯片的主要形式是die）集成到单个封装中，以通过内部互连技术开发专用的异构芯片。该解决方案有效地解决了规模化，开发成本和周期问题；

其次，借助2.5D、3D和其他先进的封装技术，chiplet可实现高性能的多芯片片上互连，从而改善了芯片系统的集成度以及性能和功耗的优化；

最后，模块化集成不仅有效地加快了开发速度，而且降低了开发成本和门槛。因此，当芯片的研究集中在算法和核心技术上时，整体创新水平和能力也会大幅提高。

与传统的单片集成方法相比，chiplet在许多方面都具有优势和潜力。然而，chiplet的成熟和广泛应用仍面临许多挑战。

首先，统一接口和标准对于异构集成系统至关重要。各种异构芯片的互连接口和标准的设计在技术和市场竞争方面难以平衡性能和灵活性；

其次，chiplet的核心封装技术在性能，功耗，成本等方面面临挑战；

第三，chiplet要解决的关键问题是支持芯片设计和电子设计自动化（EDA）工具链，以及生态系统是否完整和可持续；

目前，chiplet已成功应用于半导体行业，尤其是在具有高端技术和研究能力的公司。HBM存储器是chiplet早期成功应用的典型代表。从那时起，在FPGA相关领域，英特尔公司推出了基于chiplet技术的Agilex现场可编程门阵列（FPGA）产品。这些产品使用3D封装技术来实现异构芯片集成。

在高性能CPU芯片领域，AMD推出了Zen 2架构，该架构将IO组件和处理器内核分离为多个chiplet（使用7 nm，14 nm和其他工艺），以进一步按需集成。
在互联网领域，英特尔（以前是Barefoot）的Tofino2芯片具有12.8 T的交换能力，而这也是通过chiplet实现的。它将逻辑开关芯片与高速SerDes芯片集成在一起。最近，学术界，加利福尼亚大学，佐治亚理工学院和欧洲研究机构都开始研究与chiplet相关的问题，包括互连接口，封装和应用方面。

以上这些研究主要集中在独立产品或自身技术上。而在由DARPA（美国国防部高级研究计划局）于2017年发起的CHIPS计划（通用异构集成和IP重用策略）则试图将chiplet推向战略统一和生态建设的水平。在DARPA的计划中，chiplet所涉及的芯片具有不同的功能，这些芯片来自不同的公司，具有不同的工艺节点，半导体材料以及信号类型（例如，波，电子，光子，甚至是微机电系统）。因此，chiplet技术旨在支持打造全新生态和应用系统的宏伟计划。

尽管chiplet技术引起了广泛的关注，但有关chiplet的文献仍然很少，但我们迫切需要这些文献的信息。在本文中，我们详细分析了关于chiplet的现有研究和应用，并提出了未来的发展趋势。我们希望我们的所作的分析总结可以为从事下一代芯片研究和设计的研究人员提供参考。


**chiple是什么？**

一般来讲，IC设计人员有两种开发下一代IC产品的方法。主流方法是将旧设计直接转换到较小的工艺节点中，以获得更高的设备频率从而获得更好的PPA。第二种方法是在同一处理节点下合并更多功能块，以降低掩模和EDA工具的成本。

然而，随着芯片制造工艺的发展，由于工艺更加复杂以及芯片设计和实现更困难，总体芯片设计成本已显着增加。根据国际商业策略公司（IBS）的调查，经过22纳米工艺后，每代技术的设计成本增长已超过50％，其中包括EDA，设计验证，IP核，流片等。例如，如图1所示，7纳米工艺的总设计成本约为3亿美元，而3纳米工艺的总设计成本预计将增加5倍，达到15亿美元。基于工艺改进的高性能芯片升级正在增加，性价比也在增加。此外，由于产量方面的技术限制（例如光刻机的掩模尺寸），现有的单片集成变得无法通过升级和扩展功能和性能的新工艺来实现。


*图1.不同工艺节点下的芯片设计和制造成本：数据源自IBS*

在这种情况下，chiplet为未来的芯片设计提供了一种可行的方法。1980年代出现的多芯片模块（MCM）技术已经体现了chiplet的概念。MCM技术连接了基板或其他介质上的多个芯片，以满足复杂系统芯片的性能和功能要求。MCM可以减少板级互连的开销和板级系统设计的复杂性，从而大大节省了构建系统的成本。最近，英特尔，AMD和其他公司已经开发了基于MCM技术的一系列高性能芯片产品。但是，MCM主要关注基础封装技术，它没有考虑芯片异构集成的高层次问题，包括多层互连标准，接口，工具和生态。

2017年，DARPA在“电子复兴计划”中提出了“通用异构集成和IP重用策略”（General Heterogeneous Integration and IP Reuse Strategy：CHIPS）。该项目试图利用半导体行业和学术资源来解决上述问题。参与者包括系统集成供应商（洛克希德·马丁，诺斯罗普·格鲁曼公司，波音，英特尔，美光等），EDA供应商（Cadence，Synopsys等）和研究机构（密歇根大学，乔治亚理工学院和北卡罗来纳州州立大学等）。该项目着重于开发一种新技术框架，该框架结合了具有不同功能的芯片die，然后将它们匹配并组合到中介层上。它不仅以较低的成本将die集成到片上系统中，而且还增强了整体灵活性，并缩短了下一代产品的设计时间。

Facebook和其他公司也提出了开放计算项目（Open Compute Project ：OCP），该项目致力于开放领域特定架构（Open Domain-Specific Architecture：ODSA）的研究（已在2018年底积极开展）。同时OCP试图开发完整的架构接口堆栈并开拓开放的chiplet市场。通过定义开放的标准化接口，集成在chiplet中的芯片可以进行互操作，以支持为构建更灵活的芯片系统灵活组合，以整合来自不同供应商的资源。

为了实现上述目标，软件工具链的研发和特殊应用将是进一步开发chiplet所要解决的重要问题。具体来说，软件工具链包括物理层，链路层和网络层、先进的芯片封装技术等完整堆栈可行互连接口规范和标准。


**chiplet的优势**

与传统的印刷电路板（PCB）板集成和单片ASIC集成相比，chiplet的优势主要体现在技术，开发成本和业务层面上。

## **一、技术**


chiplet技术通过重组多个chiplet提高了性能和功耗方面的优化潜力。因此，它支持特定领域的自定义，并减轻了摩尔定律放缓对开发各种芯片的影响。例如，对于具有高密度和高速接口的网络芯片，高速SerDes对功耗有更高的要求。基于chiplet技术的网络芯片将高速SerDes IO模块与其核心逻辑分开，从而为功耗提供了更多的布局方面的选择。这也是将chiplet技术应用于英特尔的可编程交换芯片Tofino2的重要原因。

此外，内存访问带宽通常是高性能CPU和AI芯片的性能瓶颈。chiplet通过将处理器内核和内存芯片与3D堆栈技术相结合，提高了信号传输质量和带宽，并减轻了“存储墙”问题。这是AMD和Intel早期关注并采用chiplet的关键原因。

## **二、开发成本**


chiplet通常使用先进的封装工艺将多个chiplet集成到一个大的单芯片中。由于chiplet占据的面积相对较小，其成本和成品率也会相应提高，因此这种方式可以有效降低总体成本。除了芯片制造成本外，研究与开发成本逐渐占整个芯片成本的很大一部分。通过直接组合已知KGD，研发周期大大缩短，相关投资也可以节省一部分。由于chiplet的利用，AMD 32核EPYC CPU的开发和制造成本降低了40％。此外，在传统的单片集成中经过多次硅验证后，大型高性能芯片（尤其是商用芯片）通常成为成熟产品并投入市场。该解决方案通常给研发成本带来了巨大压力。相反，用chiplet开发的芯片通常会选择使用广泛且成熟的芯片来进行集成，从而降低了芯片开发的风险。因此，re-spins和封装的数量也会减少，成本也会有效降低。

**三、商业模式**

chiplet可以有效提高芯片开发速度，降低相关的成本并减少障碍。因此，科研和商业机构非常重视核心算法和技术，这有效地促进了技术创新。此外，芯片生态系统的不断发展和完善将加速新兴产业的诞生。chiplet的业务模型可能会产生三种类型的商业角色，包括提供chiplet模块芯片的chiplet供应商，将chiplet模块芯片集成以形成完整系统的chiplet集成商以及提供工具链和设计自动化服务的EDA软件。目前，英特尔，美光等公司开始在产业链中扮演重要角色，而初创公司（如zGlue）则专注于开拓chiplet产业链中缺失的部分。

表1对比了chiplet技术与传统技术。具体而言，chiplet在性能，功耗和集成方面非常接近单个ASIC芯片。而在成本和设计周期方面，chiplet与传统PCB技术之间差距很小。总而言之，chiplet在单个ASIC和PCB技术之间取得了很好的折衷，因此具有很大的发展潜力。


*表1 chiplet技术与传统芯片集成技术的对比*


**chiplet的挑战**

尽管chiplet具有上述许多优点，但如果要进一步开发仍面临许多挑战，包括互连接口和协议，封装技术和质量控制方面。

## **一、互连接口和协议**


chiplet之间的互连接口和协议对于chiplet的开发非常关键。接口和协议的设计必须考虑匹配制造过程和封装技术，以及系统集成和扩展的要求。此外，chiplet在不同领域的相关性能指标也至关重要，例如每单位面积的传输带宽，每一位所产生的功耗。通常，上述因素是矛盾的，这给互连接口和协议的设计带来了更大的挑战。

chiplet技术在物理层中使用的互连接口可以分为以下几类。

### **（1） 串行接口**


从应用程序传输距离的角度来看，串行接口包括长/中/短距离的SerDes（LR / MR / VSR SerDes），超短距离（XSR）SerDes和极短距离（USR）SerDes。图2表明了这些接口的应用场景。


*图2.典型串行接口的分类和应用； *
*（a）串行接口的分类，（b）串行接口的应用。*

LR / MR / VSR SerDes通常用于芯片间连接和芯片与模块连接，这两种连接方式都基于PCB板。它们被广泛用于通信接口，例如PCI-E，以太网和RapidIO。这些接口的主要特点是可靠，传输距离长，成本低以及易于集成。然而，由于这些接口在功耗，面积和延迟方面没有优势，因此难以支持对上述指标有很高要求的高性能芯片的构造。

XSR SerDes为“Die-to-Die”（D2D）和“Die-to-Optical”（D2OE）的互连提供了相应的SerDes标准。XSR SerDes的设计主要集中在D2OE的互连上。它是基于传统的SerDes结构开发的，该结构集成了时钟数据恢复电路（clock data recovery circuit：CDR），并且对插入损耗的成本有严格的要求。为了实现较低的误码率，必须集成复杂的前向纠错（forward error correction：FEC）机制。但是，这将导致明显的延迟和功耗。尤其是当带宽达到112 G或更高时，信号反射会带来额外的延迟和功耗。此外，为了保证良好的信号完整性，需要高性能芯片工艺和封装基板材料来支持大规模集成。XSR适合在具有端到端FEC的光学设备和裸芯片之间部署。

与XSR相比，USR SerDes主要致力于通过2.5D / 3D封装技术在超短距离（10毫米级别）上实现芯片对芯片的高速互连通信。由于通信距离短，USR通过高级编码，多位传输和其他技术提供了更好的性能和功耗比，以及更好的可伸缩性。例如，使用CNRZ-5编码的Kandou的Glasswing 112 G USR SerDes可以产生0.72 pJ / bit的功耗，而224 G SerDes可以产生0.8 pJ / bit的功耗。由于USR接口的实现通常涉及专利技术（例如编码方法），因此其互操作性的兼容性面临更大的挑战。此外，USR对传输距离的要求阻碍了chiplet的大规模集成。

我们根据参考文献定义的56 G SerDes接口规范，从传输，应用和其他方面对多个接口进行了全面对比，如表2所示。


*表2.不同类型的OIF 56 G SerDes对比*
### 

### **（2）并行接口**


目前，用于互连chiplet的通用并行接口是英特尔的AIB / MDIO，台积电的LIPINCON，OCP的BoW等。HBM接口也属于这种类型的接口，这种接口专用于高带宽存储之间的互连。

英特尔的AIB（高级接口总线）是物理层中的并行互连标准，与DDR DRAM接口相似。在DARPA的CHIPS项目中，英特尔向相关供应商提供了免费的AIB接口许可，以支持广泛的chiplet生态系统。作为AIB的升级版本，MIDO提供了更高的传输效率，并且响应速度和带宽密度是AIB的两倍以上。AIB和MDIO技术主要适用于通信距离短，损耗低的2.5D和3D封装技术，例如EMIB，Foveros。

LIPINCON是TSMC为chiplet提出的高性能互连接口。通过使用先进的基于硅的互连封装技术（例如InFO和CoWoS）和时序补偿技术，LIPINCON可以在没有PLL / DLL的情况下降低功耗和占用面积。LIPINCON接口包含两种类型的PHY：PHYC和PHYM。PHYC用于SoC芯片，而PHYM用于存储器和收发器芯片。

OCP ODSA小组提出的BoW接口专注于解决基于有机基板的并行互连问题。BoW有三种类型，即BoW Base，BoW-Fast和BoW-Turbo。BoW-Base专为10 mm以下的传输距离而设计，并使用无端接的单向接口。每条线的数据传输速率可以达到4 Gbps。就BoW-Fast而言，它使用端接接口，并且线长最大为50 mm。每条线的传输速率为16 Gbps。与BoW-Fast相比，Bow-Turbo使用两条线来支持双向16 Gbps传输带宽。此外，BoW支持向后兼容，并且对芯片工艺和封装技术的限制较少。它不依赖于先进的基于硅的互连封装技术，具有广泛的应用范围。如表3所示，表3对比了物理层中chiplet的这些并行接口的封装，传输速率和带宽密度。

物理层中的上述高级电信号接口在每位数据传输上实现了低功耗。鉴于高性能网络和计算的带宽需求急剧增长，由数据传输引起的功耗增加仍然是芯片开发的关键问题。马克·韦德（Mark Wade）等人提议使用光电混合技术解决IO瓶颈，这为开发高性能和低功耗的互连技术和标准提供了新思路。

以上所有接口标准都是根据特定的互连要求设计的，最佳的chiplet互连解决方案与特定的应用有关。尽管并行接口提供低功耗，低延迟和高带宽，但它需要更多的路由资源。相反，串行接口需要较少的路由资源，但会带来更多的功耗和延迟。因此，chiplet设计人员必须根据实际应用需求，约束条件和芯片特性，在物理层中选择一个或多个接口来实现系统优化的目标。


*表3.物理层的chiplet并行接口之间的比较*
### 

### **（3）其他接口**


原则上来讲，通过适应底层物理层（PHY），可以将传统接口标准（例如以太网MAC，PCIe等）用于链路层的chiplet传输。Tilelink接口协议的开放性和开源模式引起了广泛的关注。它试图使片上网络和缓存控制器的实现与缓存一致性协议脱钩。遵循Tilelink事务结构的任何缓存一致性协议都可以与任何物理层网络和缓存控制器结合使用。CCIX接口标准是专门为芯片间加速器结构设计的。它通过在标准PCIe数据链路层上扩展事务层和协议层中的功能来支持缓存一致性。CCIX还支持灵活的拓扑，主要用于主CPU和加速器之间的通信。

为了提高同步通信机制（例如Tilelink，CCIX）的可伸缩性，OSDA项目的积极参与者Netronome设计了ISF接口协议。ISF是支持异步存储访问的轻量级消息协议（lightweight message protocol），由传输层，网络层和链路层组成。ISF最初用于Netronome的NFP网络流处理器上的片上组件的互连，它将支持chiplet的芯片对芯片的互连。

与密切研究和chiplet相关的互连标准和规范的半导体行业不同，学术界主要关注网络层中芯片之间的NOC架构和算法的设计和优化。此外，基于有源中间层的高性能片上网络通信的实现也引起了很多关注。

## **二、封装技术**


chiplet中die互连的物理实现取决于芯片封装过程的完成。多芯片封装技术的性能，成本和成熟度极大地影响了chiplet的应用。如图3所示，支持chiplet互连的封装技术可以根据连接介质和工艺的不同而分为三种类型。它们是基于基板和硅中介层的封装技术，以及基于RDL（重分布层）的扇出封装技术。


*图3.chiplet封装技术说明；*
*（a）基于基板的封装，（b）基于硅中介层的封装，*
*（c）基于硅桥的封装，（d）基于RDL的封装。*

目前，出于成本和其他因素的原因，有机基板被广泛使用。与传统的PCB相似，有机基板材料通过蚀刻工艺完成布线连接，而蚀刻工艺不依赖于半导体设备中使用的硅工艺。多个die可以通过引线键合或倒装芯片技术在基板上来进行高密度连接。由于基于衬底的封装方法不依赖于芯片铸造工艺，因此相关材料和生产成本较低。通过这种方法，封装尺寸可以达到110 mm×110 mm（Land Grid Array Packaging，LGA），并且被广泛用于大规模chiplet系统。

但是，通过引线键合和倒装芯片，IO引脚的密度较低，并且芯片的大多数引脚都被电源占用。结果，用于数据传输的引脚更加稀缺，并且整个芯片的外部带宽受到限制。此外，串扰效应阻碍了单个引脚的传输能力的提高。此外，这些上述问题还将限制die到die连接的传输带宽，并影响具有更高性能的chiplet的开发。

2.5D / 3D封装技术主要采用基于硅中介层的封装技术的形式。die之间的互连和通信是通过在基板和die之间放置一个额外的硅层来实现的。芯片和衬底之间的连接是通过硅通孔（TSV）和微型凸块实现的。由于微型凸块和TSV的凸块间距和走线距离较小，因此基于硅中介层的封装技术可提供更高的IO密度以及更低的传输延迟和功耗。

然而，与有机衬底相比，芯片代工厂提供的硅中介层的实施增加了材料和工艺上成本。为了解决这个问题，硅桥技术试图将基于衬底的技术和基于硅中介层的技术相结合。它在基板上集成了小的薄层，以实现晶粒间互连（小于75 um）（inter-die interconnection ），从而在性能和成本之间取得了良好的平衡。
通常，硅中介层有两种类型：一种是仅包含连接电路的无源中介层，另一种是不仅包含连接电路而且集成了逻辑电路的有源中介层。尽管有源中介层的实现成本更高，但与无源中介层相比，它可以提供更灵活和可扩展的解决方案。

因此，学术界更多地关注interposers.。

基于再分布层（redistribution layer：RDL）的无基板无扇出封装技术将金属和介电层沉积在晶圆表面上。它形成一个重新分布层以承载相应的金属布线图案，并在裸片外部的松散区域上重新排列芯片的IO端口。在扇出封装技术中，RDL可以通过缩短电路长度来提高信号质量，并通过减chiplet面积来提高chiplet集成度。

此外，扇出封装作为具有较低垂直高度的无基板封装方法，为更多的要向上堆叠的组件提供了额外的垂直空间。与基于硅中介层的封装技术相比，扇出封装的成本相对较低。但是，扇出封装的布线资源受到RDL布线级别的限制。自从台积电的InFo（集成扇出封装）技术成功应用于苹果iPhone 7的A10处理器以来，扇出技术已受到封装测试工厂和芯片代工厂的广泛关注。目前，市场上推出了十多种扇出封装技术，这为芯片集成提供了丰富的选择。

表4对比了可用于chiplet集成的封装技术。随着chiplet技术和相关封装技术的发展，由于性能，功耗，成本和实施性的问题的解决，chiplet技术将得到更好的发展。


*表4.chiplet封装技术对比*

**三、质量控制技术**
****
chiplet集成的die通常是经过硅认证的产品。它可以保证其设计和物理实现的有效性，但是在过滤和封装过程中仍然会出现成品率问题。至于chiplet，由于单个裸片中的问题会导致单片芯片出现故障，因此失败的代价很高。因此，完善和全面的测试对于chiplet的质量控制尤为重要。因为chiplet将多个die封装在一起，所以与单片集成相比，其芯片测试的难度要高得多。由于chiplet的引脚受到限制，因此只能保证在测试期间必须满足某些引脚和die的连接要求。

因此，这些给chiplet全面测试带来了新的挑战。

chiplet中的EDA软件是解决此问题的重要解决方案。在芯片设计和制造过程中，30％–40％的成本来自软件工具。chiplet需要EDA工具在架构探索，芯片设计，物理和封装实施方面提供全面的支持。因此，在每个过程中提供智能和优化的帮助，可以最大程度地减少人员参与，并避免其他问题的出现。

当前，学术界和半导体行业的许多研究机构和公司已经开始进行大量的生产。Jinwoo Kim等来自佐治亚理工学院的工程师介绍了基于2.5D的chiplet封装的EDA工艺。它涵盖并自动执行架构，电路和封装的整个设计阶段。此外，EDA流程的可用性通过配置了NOC的ROCKET-64 CPU进行了验证。而且，诸如Cadence，Synopsys和Mentor之类的传统集成电路EDA公司正在开发相关工具来支持chiplet集成。


**chiplet的应用及发展趋势**

尽管chiplet的标准化才刚刚起步，但是它已经在许多领域表现出其独特的优势，从高性能CPU，FPGA，网络芯片到应用于蓝牙，物联网（IoT）和可穿戴设备的低端芯片。

在高性能CPU方面，AMD的Zen 2架构通过在不同的处理节点中组合多个处理器核心芯片（7纳米工艺），IO芯片（14纳米工艺）和内存芯片来构建chiplet。这样高端处理的计算性能改善就可以以较低的成本来实现。

英特尔Stratix 10高性能FPGA最初是采用chiplet技术开发的。它基于EMIB硅桥封装技术（2.5D）将FPGA die和SerDes IOdie与AIB接口集成在一起。Stratix 10在3个芯片代工厂的6个工艺节点中集成了die，从而有效地证明了芯片技术在不同代工厂之间的互操作性。英特尔的Agilex FPGA使用先进的3D封装技术来集成10 nm FPGA内核和112 G SerDes。它证明了chiplet技术在构建高科技工艺和具有高IO性能的芯片方面的可行性。

zGlue公司专注于中低端chiplet的开发和标准化。由zGlue开发和制造的芯片（例如蓝牙，物联网和WiFi）是基于ADI，Dialog，Macronix和Vishay等30多家公司的近100个芯片开发的。此外，zGlue构建了一组基本的chipletEDA工具链，从而构建die并且快速重复使用。

总体而言，由于chiplet可以在多个维度（例如产量和成本）上提供可定制性和优化性，因此它将广泛应用于更多领域。随着芯片领域开源生态的迅速兴起和开发，chiplet技术将成为未来芯片开发的主流方向。因此，科研机构和半导体行业有必要深入研与究chiplet相关的技术挑战和问题。


**结论**

综上所述，本文概述了chiplet技术的概念及其发展。作为缓解摩尔定律放缓的可行性方案，近年来的chiplet异构集成技术已受到广泛关注。过去的十年已经证明，半导体行业为降低制造成本和提高产量所做出的努力是有效的。为了更好地利用chiplet技术，我们应该对互连和封装等相关技术进行更多的研究，以简化系统集成的复杂性，使其具有更高的性能，更低的功耗和更高的面积利用率。此外，从IC设计者的角度来看，chiplet设计将基于新的体系结构，该体系结构将可重复使用的异构IP芯片系统地集成到了单芯片中。如此一来，设计方法论和相应的EDA工具开发是我们需要迫切关注的方向。


本文由“壹伴编辑器”提供技术支持
**参考文献：**

1. Cadence. Imec and Cadence Tape Out Industrys First 3 nm Test Chip. 2018. Available online:https://www.cadence.com/content/cadence-www/global/en_US/home/company/newsroom/press-releases/pr/2018/imec-and-cadence-tape-out-industry-s-fifirst-3nm-test-chip.html (accessed on2 March 2020).
2. IBS. As Chip Design Costs Skyrocket, 3 nm Process Node Is in Jeopardy. 2020. Available online: https://www.extremetech.com/computing/272096-3nm-process-node (accessed on 13 March 2020).
3. Moore, G.E. Cramming more components onto integrated circuits. Electronics 1965, 38, 8. [CrossRef]
4. Dennard, R.H.; Gaensslen, F.H.; Rideout, V.L.; Bassous, E.; LeBlanc, A.R. Design of ion-implanted MOSFET’swith very small physical dimensions. IEEE J. Solid-State Circuits 1974, 9, 256–268. [CrossRef]
5. DeBenedictis, E. P. It’s time to redefifine moore’s law again. Computer 2017, 50, 72–75. [CrossRef]
6. Ndubuisi G. Orji, Yaw S. Obeng, Carlos Beitia, Supika Mashiro, James Moyne. Virtual Metrology WhitePaper-International Roadmap for Devices and Systems(IRDS). 2018. Available online: https://www.nist.gov/publications/virtual-metrology-white-paper-international-roadmap-devices-and-systemsirds(accessed on 13 March 2020).
7. Ramalingam, S. HBM package integration: Technology trends, challenges and applications. In Proceedingsof the 2016 IEEE Hot Chips 28 Symposium (HCS), Cupertino, CA, USA, 21–23 August 2016; pp. 1–17.
8. Shilov, A. AMD Unveils ‘Chiplet’ Design Approach: 7 nm Zen 2 Cores Meet 14 nm I/O Die. 2018.Available online: https://www.anandtech.com/show/13560/amd-unveils-chiplet-design-approach-7nmzen-2-cores-meets-14-nm-io-die (accessed on 4 March 2020).
9. Intel. INTEL AGILEX FPGAS and SOCS. 2019. Available online: https://www.intel.com/content/www/us/en/products/programmable/fpga/agilex.html (accessed on 6 March 2020).
10. Fotouhi, P.; Werner, S.; Lowe-Power, J.; Yoo, S.B. Enabling scalable chiplet-based uniform memoryarchitectures with silicon photonics. In Proceedings of the International Symposium on Memory Systems,Washington, DC, USA, 3 September–3 October 2019; pp. 222–334.
11. Kim, J.; Murali, G.; Park, H.; Qin, E.; Kwon, H.; Chaitanya, V.; Chekuri, K.; Dasari, N.; Singh, A.; Lee, M.;others. Architecture, chip, and package co-design flflow for 2.5 D IC design enabling heterogeneous IP reuse.In Proceedings of the 56th Annual Design Automation Conference 2019, Las Vegas, NV, USA, 2–6 June 2019;pp. 1–6.
12. DARPA. DARPA Common Heterogeneous Integration and IP Reuse Strategies (CHIPS). 2020. Availableonline: https://www.darpa.mil/program/common-heterogeneous-integration-and-ip-reuse-strategies(accessed on 7 March 2020).
13. Netronome. The Open Domain-Specific Architecture: A Chiplet-Based Open Architecture. 2020. Availableonline: https://www.netronome.com/m/documents/WP_ODSA_Open_Accelerator_Architecture_wqLcezt.pdf(accessed on 10 March 2020).
14. Wong, C.; Wong, M.M. Recent advances in plastic packaging of flflip-chip and multichip modules (MCM) ofmicroelectronics. IEEE Trans. Compon. Packag. Technol. 1999, 22, 21–25. [CrossRef]
15. Project), O.C. Open Domain-Specifific Architecture. 2020. Available online: https://www.opencompute.org/wiki/Server/ODSA (accessed on 8 March 2020).
16. Kannan, A.; Jerger, N.E.; Loh, G.H. Enabling interposer-based disintegration of multi-core processors.In Proceedings of the 2015 48th Annual IEEE/ACM International Symposium on Microarchitecture (MICRO),Waikiki, HI, USA, 5–9 December 2015; pp. 546–558.
17. Netronome. It’s Time for Disaggregated Silicon. 2020. Available online: https://www.netronome.com/blog/its-time-disaggregated-silicon/ (accessed on 12 March 2020).
18. zGlue. zGlue. 2020. Available online: https://zglue.com/technology#smart-fabric (accessed on15 March 2020).Electronics 2020, 9, 670 12 of 12
19. Kandou. Kandou XSR and USR Interfaces. 2020. Available online: https://kandou.com/assets/downloads/presentation-XSR-USR-Interface-Analysis-Including-Chord-Signaling-Options.pdf (accessed on 11 March 2020).
20. OIF. 56G Serdes Specifificationss. 2020. Available online: https://www.oiforum.com/wp-content/uploads/2019/01/OIF-CEI-04.0.pdf (accessed on 13 March 2020).
21. Intel. Overview of Heterogeneous Integration. 2020. Available online: https://www.intel.com/content/www/us/en/architecture-and-technology/programmable/heterogeneous-integration/overview.html(accessed on 13 March 2020).
22. OCP. OCP Bunch of Wires: A New Open Chiplet Interface for Organic Substrates. 2020. Availableonline: https://fuse.wikichip.org/news/3199/ocp-bunch-of-wires-a-new-open-chiplets-interface-fororganic-substrates/ (accessed on 15 March 2020).
23. Intel. Embedded Multi-Die Interconnect Bridge (EMIB). 2020. Available online: https://www.intel.com/content/www/us/en/foundry/emib-an-interview-with-babak-sabi.html (accessed on 16 March 2020).
24. Intel. Foveros. 2020. Available online: https://en.wikichip.org/wiki/intel/foveros (accessed on 14 March 2020).
25. Lin, M.S.; Huang, T.C.; Tsai, C.C.; Tam, K.H.; Hsieh, C.H.; Chen, T.; Huang, W.H.; Hu, J.; Chen, Y.C.;Goel, S.K.; et al. A 7 nm 4 GHz ArmR-core-based CoWoSR Chiplet Design for High Performance Computing.In Proceedings of the 2019 Symposium on VLSI Circuits, Kyoto, Japan, 9–14 June 2019; pp. C28–C29.
26. CCIX. 2020. Available online: https://www.ccixconsortium.com (accessed on 16 March 2020).
27. Ellinidou, S.; Sharma, G.; Kontogiannis, S.; Markowitch, O.; Dricot, J.M.; Gogniat, G. MicroLET: A newSDNoC-based communication protocol for chipLET-based systems. In Proceedings of the 2019 22ndEuromicro Conference on Digital System Design (DSD), Chalkidiki, Greece, 28–30 August 2019; pp. 61–68.
28. Yin, J.; Lin, Z.; Kayiran, O.; Poremba, M.; Altaf, M.S.B.; Jerger, N.E.; Loh, G.H. Modular routing design forchiplet-based systems. In Proceedings of the 2018 ACM/IEEE 45th Annual International Symposium onComputer Architecture (ISCA), Los Angeles, CA, USA, 2–6 June 2018; pp. 726–738.
29. Berkeley. Tilelink. 2020. Available online: https://bar.eecs.berkeley.edu/projects/tilelink.html (accessed on11 March 2020).
30. AMD. AMD Previews Epyc Rome Processor: Up to 64 Zen 2 Cores. 2020. Available online: https://www.anandtech.com/show/13561/amd-previews-epyc-rome-processor-up-to-64-zen-2-cores (accessedon 14 March 2020).
31. Coudrain, P.; Charbonnier, J.; Garnier, A.; Vivet, P.; Vélard, R.; Vinci, A.; Ponthenier, F.; Farcy, A.; Segaud,R.; Chausse, P.; et al. Active Interposer Technology for Chiplet-Based Advanced 3D System Architectures.In Proceedings of the 2019 IEEE 69th Electronic Components and Technology Conference (ECTC), Las Vegas,NV, USA, 28–31 May 2019; pp. 569–578.
32. Stow, D.; Xie, Y.; Siddiqua, T.; Loh, G.H. Cost-effective design of scalable high-performance systemsusing active and passive interposers. In Proceedings of the 2017 IEEE/ACM International Conference onComputer-Aided Design (ICCAD), Irvine, CA, USA, 13–16 November 2017; pp. 728–735.
33. Nabeel, M.; Ashraf, M.; Patnaik, S.; Soteriou, V.; Sinanoglu, O.; Knechtel, J. An Interposer-Based Rootof Trust: Seize the Opportunity for Secure System-Level Integration of Untrusted Chiplets. arXiv 2019,arXiv:1906.02044.
34. Gu, P.; Li, S.; Stow, D.; Barnes, R.; Liu, L.; Xie, Y.; Kursun, E. Leveraging 3D technologies for hardwaresecurity: Opportunities and challenges. In Proceedings of the 2016 International Great Lakes Symposium onVLSI (GLSVLSI), Boston, MA, USA, 18–20 May 2016; pp. 347–352.
35. Hennessy, J.L.; Patterson, D.A. A new golden age for computer architecture: Domain-specififichardware/software co-design, enhanced security, open instruction sets, and agile chip development.In Proceedings of the 2018 ACM/IEEE 45th Annual International Symposium on Computer Architecture(ISCA), Los Angeles, CA, USA, 1–6 June 2018. [CrossRef] 


*免责声明：本文由作者原创。文章内容系作者个人观点，半导体行业观察转载仅为了传达一种不同的观点，不代表半导体行业观察对该观点赞同或支持，如果有任何异议，欢迎联系半导体行业观察。


**今天是《半导体行业观察》为您分享的第2448期内容，欢迎关注。**


推荐阅读


★[第三代半导体真的会火吗？](https://mp.weixin.qq.com/s?__biz=MzU3OTA0MjQ3Mg==&mid=2247554912&idx=1&sn=0a601905ca5d64d6357121261c270646&chksm=fd6e7aa7ca19f3b12f3c4a2dd32fbf57b09ad8d35b3f0c9bb83d05132cec71c795ecca83d49d&token=1397262943&lang=zh_CN&scene=21#wechat_redirect)
★[半导体并购的池子](https://mp.weixin.qq.com/s?__biz=MzU3OTA0MjQ3Mg==&mid=2247554748&idx=2&sn=6d5d55c9b6d3044bc03b60e6641f2736&chksm=fd6e7b7bca19f26d7946f75eccf0d11061f3fcefbf0e7d11802ee063ec8d13c8a4bef006c443&token=1000937566&lang=zh_CN&scene=21#wechat_redirect)
★[1nm将如何实现？](https://mp.weixin.qq.com/s?__biz=MzU3OTA0MjQ3Mg==&mid=2247554692&idx=2&sn=c4c04d30e5e958bedd33f1ea0661f22b&chksm=fd6e7b43ca19f255d86b4d5dc0f82eccac68b62b97d18a7d26f5214ba176925bb610d0b18893&token=1157833549&lang=zh_CN&scene=21#wechat_redirect)


半导体行业观察


『**半导体第一垂直媒体**』
**实时 专业 原创 深度**

**识别二维码**，回复下方关键词，阅读更多

晶圆｜IP｜SiC｜并购｜射频｜台积电｜Nvidia｜苹果

回复 **投稿**，看《如何成为“半导体行业观察”的一员 》
回复 **搜索**，还能轻松找到其他你感兴趣的文章！

---
**Tags:** [[SDSoW]] [[Chiplet]]
