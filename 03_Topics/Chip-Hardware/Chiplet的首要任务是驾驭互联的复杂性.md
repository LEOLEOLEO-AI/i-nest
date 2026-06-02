---
title: Chiplet的首要任务是驾驭互联的复杂性
tags:
- chip
- chip-hardware
- chiplet
- emergence
- semiconductor
- wafer
---
> 笔记本: 我的剪贴板  
> 创建时间: 2024-02-29  

---

Chiplet技术呈现出了一系列多层次、多方面、多维度的技术和商业问题，没有一劳永逸的解决方案。众多初创公司正在提出各种方案，以解决die-to-die互连的复杂性。    
  
对半导体供应链中的每一个玩家（从芯片设计和EDA工具供应商，到代工厂、OSAT公司以及众多技术初创公司）来说，最大的挑战可以归结为如何连接chiplet。  
  
幸运的是，像Eliyan、Blue Cheetah和YorChip这样的初创公司正准备以各自的方式解决这些问题。 
 
    

 

 
**Die-to-die互连问题尚未解决** 
半导体公司转向chiplet技术有着众多动机。它们都希望降低制造成本，实现更灵活的芯片分割，并开发推进解构SoC的商业模式。但Blue Cheetah的CEO Elad Alon在最近的一次采访中说：“除了所有这些之外，互连部件确实是必需的粘合剂。”然而，在他看来，“没有足够的组件可以帮助实现互连性。”  
  
在chiplet之间发送信号是一个基本功能，但对许多芯片设计师来说，它已经成为一个巨大的障碍，主要根源在于chiplet开发者必须面对的技术层面和商业上的选择。他们必须在基板选择、接口设计、物理布局和测试计划中进行抉择，在此过程中，他们必须控制die之间的意外耦合。  
  
没有有效的通用解决方案。  
  
Blue Cheetah进场了。  
  
这家位于加州Sunnyvale的初创公司声称拥有一款名为BlueLynx的专有软件IP产品，它充当chiplet的PHY“生成器”。该软件使Blue Cheetah能够“快速定制基于标准的die-to-die互连解决方案”以满足不同客户的需求。  
  
对于外行来说，“基于标准”和“可定制”是相悖的概念。然而，在Blue Cheetah的Alon看来，这是一种混合方式，通过它，他的公司可以满足早期chiplet采纳者的即时需求。  
  
那些现在急于采用chiplet的，并不是像Intel或AMD这样已经在单一供应商环境中构建自己的大型chiplet的领先芯片公司。  
  
 
  
如今在chiplet市场急于尝试的企业要么没有能力创建单一供应商环境，要么缺乏耐心等待可互操作的chiplet“乐高式”混合搭配的承诺实现。  
  
Blue Cheetah解释说，其BlueLynx D2D互连子系统IP支持OCP（Open Compute Project）的BoW（Bunch of Wires）和UCIe（Universal Chiplet Interconnect Express）。BlueLynx还能够与片上总线/片上网络（NoCs）连接，支持多种标准，包括AMBA 4 CHI、AXI和ACE。  
  
该公司表示，BlueLynex是“可适应工艺”且是“可定制的”，能够为高性能计算、AI/机器学习、网络、移动和其他应用实现最先进的功耗、性能和面积。  
  
例如，Tenstorrent选择了Blue Cheetah来交付“高度定制化的、高性能的AI和RISC-V chiplet解决方案”，这些解决方案是为了适应特定的工作负载和应用而量身定做的。  
  
Tenstorrent的首席执行官Jim Keller在一份声明中赞扬了Blue Cheetah“提供可定制的、基于标准的die-to-die互连解决方案的能力，这些解决方案支持我们、我们的合作伙伴和我们的客户需要的全部范围的能力和工艺技术。”  
  
前不久宣布的与Tenstorrent的合作对Blue Cheetah来说是一个重大胜利。它为两家初创公司提供了“大量的学习”机会，同时与Tenstorrent的联系促使其他chiplet公司注意到了Blue Cheetah。  
  
简言之，Blue Cheetah将BlueLynx定位为与所有chiplet的所有接口兼容，因为BlueLynx IP可以根据客户公司的规格进行定制。  
  
那么，是什么使这种神奇的功能成为可能呢？  
  
Alon解释说，其起源在于他还在学术界时参与的一个定制化探索，这是在他创立Blue Cheetah很久之前的事了。Alon曾在加州大学伯克利分校担任教授17年。  
  
他的团队发现了一项他们现在称之为“生成器”的技术。  
  
 
  
Alon表示：“这些生成器本质上所做的是以一种自动可执行的方式捕捉我们的设计专长。”团队可以介入并更改用户寻求的不同参数集，使团队能够“更快速地复制新设计”，这些新设计遵循相同的验证集和相同的流程。他补充说，在许多情况下，BlueLynx正在使用他的团队之前在验证过的芯片中展示的完全相同的电路。  
  
Alon强调：“我们相信，我们可以提供最快的速度，但同时风险也最低，因为我们的IP复用了如此多的经过验证的基础设施和验证方法。” 
 
  
**Eliyan**  
如果Blue Cheetah坚决要提供“高度可定制和可移植工艺的die-to-die互连解决方案”，Eliyan的焦点则在其他地方。  
  
Eliyan（位于加州Santa Clara）并不专注于可定制性，而是提供“在标准封装中为die-to-die和die-to-memory接口带来新水平的性能和能效”。关键词是“标准封装”。  
  
Eliyan希望为那些可能不想使用先进封装的chiplet客户提供解决方案。Eliyan解释说，对于某些应用，先进封装和interposer可能会使chiplet过于昂贵或不够稳健。  
  
Eliyan的使命是解决内存瓶颈，因此也专注于内存chiplet和内存chiplet接口的改进。本周，该公司宣布完成了它所称的“行业中性能最高的多芯片架构PHY解决方案”的流片。  
  
Eliyan声称，其新的PHY在3nm工艺上使用标准封装实现了每个接点64Gbps的带宽。该公司补充说，“Blue Cheetah等公司能够实现的带宽是16Gbps”。  
  
虽然大多数用于die-to-die通信的PHY IP是为硅interposer优化的，但Eliyan强调其NuLink PHY也设计用于在有机基板这种非常不同的电气环境中提供全速率数据传输。  
  
Eliyan的PHY与行业互连标准UCIe和BoW兼容。但它还支持由Eliyan开发的一种新型chiplet互连技术UMI（Universal Memory Interconnect）。该公司表示，它将die-to-memory带宽效率提高了一倍以上。  
  
UMI旨在利用同时双向信号传输，这是Eliyan的PHY的另一个独特属性。根据Eliyan的说法，UMI的规格目前正在OCP/ODSA（Open Domain-Specific Architecture）中最终确定。 
 
  
**YorChip** 
另一家初创公司YorChip正专注于一种新的die-to-die技术，用于chiplet，特别关注大众市场和嵌入式IoT类型的应用。 
虽然其网站上关于这项技术的详细信息不多，但YorChip承诺很快将推出一款“低成本、节能、高性能”的芯片组合。 
在本周的一个chiplet行业会议上，这家初创公司宣布与Ditho建立了合作伙伴关系。该协议允许YorChip在后端制造过程中定制化每个晶圆上的chiplet，使YorChip能够为每个known-good-die chiplet嵌入一个独特的ID。公司表示，这反过来有助于保障chiplet供应链及其物理安全。 
**为什么乐高模式还不行？** 
如此多的die-to-die互连技术的涌现，它们常常声称既是“基于标准的”又是“可定制的”，明确地表明了一点，承诺的类似乐高的即插即用的chiplet市场仍是一个遥远的海市蜃楼。 
虽然许多chiplet设计者渴望在他们的chiplet分割中实现“可配置性”，但很少有人相信开放的chiplet市场会很快到来。 
要实现这样一个开放的chiplet市场，每个梦想构建GPU和CPU chiplet的人都必须能够定义某些功能集和接口。Alon解释说，设计符合该规格的chiplet，使其他人能够将该特定模板替换为其他供应商的chiplet。 
如果是这样，整个系统将“行为一致”，具有模块化的功率性能。Alon说，“从die-to-die接口的角度来看，这就是基于标准的互操作性显然变得更为重要的地方。” 
他补充说，“尽管即插即用愿景很有吸引力，要真正达到这一点，确实还存在一些技术和商业障碍。”  
*现在的行业是一个多供应商生态系统的格局。从近期来看，这种环境允许开发者配置和部署一个chiplet，甚至在完全即插即用市场到来之前。然后问题变成了谁将拥有这样一个多供应商生态系统。Blue Cheetah，凭借其定制能力，希望能够成为其答案。*
  
from A to B

---
**Tags:** CST [[Chiplet]]

---
## 相关笔记 (AI 自动关联)
- [[Chiplet的机遇与挑战]]
- [[Chiplet技术仍处于发展阶段]]
- [[Chiplet时代来临，Die-to-Die接口成新挑战]]
