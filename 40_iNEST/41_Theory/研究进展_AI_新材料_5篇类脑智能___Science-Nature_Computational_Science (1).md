---
title: 研究进展：AI+新材料，5篇类脑智能 | Science-Nature Computational Science
tags:
- ai-ml
- artificial-intelligence
- brain
- deep-learning
- dynamics
- graph-neural-network
- neural-networks
- neuroscience
- patent
---
- **笔记本**: 1.1 新导入
- **时间**: 2026-02-25 03:52

---

原文链接: https://mp.weixin.qq.com/s/6eKKwuDpl1qGE17RVImlYw

            
  
          
    
    
            
      
          
        
      
                                                                                
                    
## 研究进展：AI+新材料，5篇类脑智能 | Science-Nature Computational Science          
                                                                                                                            今日新材料                                                                                                                              今日新材料                                          
                                                  2026年2月24日 11:31              北京                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      

01.

低维概念操控高维感知
Nature Computational Science

人类大脑具有一种非凡的能力，从传感器运动经验中，形成抽象的概念表征，并在没有直接感官输入的情况下，灵活地应用（例如，听到“晚餐”一词能唤起相关的意象，即使眼前没有食物）。这种将心理概念与即时感官内容解耦的能力是人类语言和思维的独特特征，允许人类规划、模拟和表征超越“此时此地”的信息。近日，中国科学院自动化研究所Liangxuan Guo、陈阳副研究员团队与北京大学毕彦超教授团队在Nature Computational Science上发文，提出了一种名为CATS Net的双模块神经网络框架，旨在模拟人类从感官经验中形成抽象概念，并灵活应用这些概念进行理解和交流的能力。该模型包含“概念抽象模块”concept-abstraction，CA和“任务解决模块task-solving，TS，通过分层门控机制，将高维感官输入压缩为低维概念向量，并利用这些向量动态重构网络，以执行视觉判断任务。研究发现，CATS Net生成的概念空间，不仅在功能上具有语义结构，能与人类语义模型（如Binder65, SPOSE49）高度对齐，还能在不同网络间通过低维概念进行知识迁移（即“交流”）。更重要的是，模型的表征模式与人脑腹侧枕颞皮层ventral occipitotemporal cortex，VOTC，及语义控制网络的激活模式显著相关，为理解人类概念认知的计算机制提供了统一的框架。
第一作者：Liangxuan Guo, Haoyang Chen, Yang Chen.通讯作者：Yang Chen, Yanchao Bi & Shan Yu 通讯单位：中国科学院自动化研究所脑认知与类脑智能技术国家重点实验室、北京大学麦戈文脑科学研究所
图1 | CATS Net的动机、实验方法和架构

图2 | CATS Net的语义组织与功能特异性

图3 | CATS概念层与人类语义模型的对齐

图4 | 通过独立训练的CATS Net间通信实现知识迁移

图5 | 使用Word2Vec嵌入在CATS Net中进行概念习得文献链接Guo, L., Chen, H., Chen, Y. et al. A neural network for modeling human concept formation, understanding and communication. Nat Comput Sci (2026). https://doi.org/10.1038/s43588-026-00956-4

02.

无需集体变量学习承诺函数
Nature Computational Science

（引子：复杂分子系统中，稀有事件（如构象转变或化学反应）取决于“承诺函数”的准确估计，该函数量化了系统从初始态到达目标态的概率，为最优的一维反应坐标。传统方法需取决于人工选择的集体变量（如二面角、原子距离等），但常受限于主观经验，难以全面捕捉高维空间中的动态特征。机器学习方法（如神经网络）已尝试通过非线性组合描述符来优化集体变量CVs，但仍需预设输入特征。直接从笛卡尔坐标学习CVs往往导致计算成本激增。亟需一种无需显式集体变量CVs、能直接从原子坐标提取物理意义的方法）近日，法国洛林大学Sergio Contreras Arredondo，Christophe Chipot等在Nature Computational Science上发文，提出了一种基于几何向量感知器geometric vector perceptrons，GVP的图神经网络graph neural network，qGNN架构，可直接从原子坐标学习分子系统的“承诺函数”committor function，无需依赖人工设计的集体变量collective variables，CVs。该方法在多种分子系统（如二肽异构化、三肽构象平衡、Diels-Alder反应及Trp-cage蛋白折叠）中验证了准确性，不仅能精确预测反应速率常数，还能通过节点敏感性分析自动识别关键原子，为理解复杂分子动力学提供了可解释且高效的工具。

图1：qGNN学习流程。

图2：NANMA分子异构化过程。文献链接Contreras Arredondo, S., Tang, C., Talmazan, R.A. et al. Learning the committor without collective variables. Nat Comput Sci (2026). https://doi.org/10.1038/s43588-026-00958-2

03.

交替方向乘子法
Nature Machine Intelligence

## （引子：交替方向乘子法Alternating Direction Method of Multipliers，ADMM是一种用于求解约束优化问题的迭代算法。在分布式优化中具有分解复杂问题的优势，但早期ADMM类算法需计算全梯度或精确求解子问题，计算成本高，难以适用于大规模深度学习任务。随机ADMM（SADMM）及其加速变体仍依赖较多假设或需访问全梯度，限制了在异构数据上的应用）深度学习模型主要基于随机梯度下降stochastic gradient descent，SGD优化器（如Adam、AdaGrad、FedAvg等）进行训练。然而，这些方法存在以下固有局限：收敛速度慢，假设条件严苛以及数据异构挑战。近日，北京交通大学Shenglong Zhou  (周声龙)联合英国帝国国理工学院Ouya Wang  (王欧亚)等在Nature Machine Intelligence上发文，提出了一种名为PISA(preconditioned inexact stochastic alternating direction method of multipliers）的新型深度学习优化算法，旨在解决传统随机梯度下降SGD类算法在数据异构Non-IID场景下收敛慢、假设条件苛刻的问题。该项算法，以严格理论保证为基础，仅在梯度在有界区域上，满足利普希茨连续性这一假设下，即可收敛，从而无需随机方法，通常要求的其他条件。这一特性使得所提出的算法，有效应对数据异质性的挑战。该算法架构支持可扩展的并行计算，并可兼容多种预条件，例如二阶信息、二阶矩以及通过牛顿-舒尔茨迭代实现的正交化动量。将后两种预条件融入PISA中，便产生了两个计算高效的变体：SISA和NSISA。为训练或微调各类深度模型（包括视觉模型、大语言模型、强化学习模型、生成对抗网络和循环神经网络）而进行的综合实验评估证明，相比于多种当前最先进的优化器，SISA和NSISA具有更优越的数值性能。

图 1：在 CIFAR-10数据集上，视觉模型的训练损失和测试准确率随训练轮数变化。
图 2：三个GPT2模型的验证损失，随处理词元数和挂钟时间（秒）变化。
图 3：在 CIFAR-10 数据集上，生成对抗网络的训练FID随训练轮数变化。文献链接Zhou, S., Wang, O., Luo, Z. et al. Preconditioned inexact stochastic ADMM for deep models. Nat Mach Intell (2026). https://doi.org/10.1038/s42256-026-01182-3

04.

大语言模型专利分类
Nature Energy

## 电池技术带来了重大经济机遇，衍生出多种基于不同金属离子的电池化学体系，这些体系，在材料、性能及供应链特性上各有差异。因此，了解这些不同电池化学体系之间的知识如何共享，对于以技术经济预测为基础的产业战略至关重要，然而这方面的研究尚不充分。近日，瑞士苏黎世联邦理工学院André Hemmelder，Tobias S. Schmidt等在Nature Energy上发文，运用先进大语言模型进行专利自动分类，基于包含超过1.5万个化学结构层级分类专利家族的引证网络，绘制了锂离子与钠离子电池化学体系内及跨体系的知识流动图谱。研究发现，在产品创新和工艺创新方面，化学体系内及跨体系，均存在持续显著的知识流动，且存在从成熟的锂离子体系，向新兴钠离子体系的持续定向知识流动。对于某些锂离子化学体系，跨化学体系的知识流动，甚至超过体系内流动。这些结果表明，试图绕过现有化学体系的设计制造经验直接跃迁至新化学体系的产业战略，难以成功，因此，在预测模型中，不应将不同电池化学体系视为完全独立的技术路线。

图1| 电池化学体系结构类别间的知识流动热力图

图2| 按创新类型划分的金属离子电池化学结构类别间知识流动
图3| 金属离子电池类别间跨结构知识流动的时序演化文献链接Hemmelder, A., Panda, A., Peiseler, L. et al. Knowledge interdependencies between lithium- and sodium-ion battery chemistries. Nat Energy 11, 313–323 (2026). https://doi.org/10.1038/s41560-026-01985-z

05.

大语言模型概念提取与控制
Science

人工智能Artificial intelligence (AI) 模型蕴含了人类知识的大部分内容。理解这些知识的表征方式，将有助于提升模型能力并完善模型的安全机制。近日，加州大学圣地亚哥分校Daniel Beaglehole，Mikhail Belkin等在Science上发文，在特征学习研究进展的基础上，开发了一种从AI模型中，提取语义概念线性表征的方法。研究表明，这些表征实现了模型引导，通过该方法既揭示了模型存在的脆弱性，又提升了模型性能。实验证明，概念表征具有跨语言的可迁移性，并能实现多概念协同引导。在数百个概念的测试中，研究发现规模更大的模型具有更强的可引导性，且相较于提示工程，引导技术能更有效地提升模型能力。研究还表明，概念表征在监控模型生成内容与人类价值观的偏离程度上，比直接使用评判模型更为有效。这些发现表明了内部表征机制在推动AI安全与模型能力发展方面的重要价值。

图1. 基于递归特征机Recursive Feature Machine (RFM)特征学习算法，多模态模型概念引导与监控示意图
图2. 采用递归特征机RFM的AI模型引导、概念向量的跨语言迁移性，及面向视觉语言模型Llama-3.2-90b-4bit多概念混合引导效果
图3. 递归特征机RFM引导方法的定量评估结果
图4. 大型语言模型评判与递归特征机RFM探针，在监测幻觉及不利内容方面的效能
图5. 分类方向与引导方向的概念区分理解现代人工智能模型，如何在内部参数中编码知识，对于提升模型能力及实施有效的安全防护至关重要——尤其是在AI解决方案迅猛发展。该项研究提出了一种稳健且可扩展的方法，从各类大规模AI系统（包括语言模型、视觉语言模型及推理模型）中，提取概念的线性表征。该技术，不仅能有效监控和引导模型输出，更揭示了大规模模型所习得表征的基础属性，为提升AI性能与安全性提供了实践价值。文献链接Daniel Beaglehole et al. , Toward universal steering and monitoring of AI models. Science 391, 787-792 (2026). DOI:10.1126/science.aea6792。

1 https://doi.org/10.1038/s43588-026-00956-4
2 https://doi.org/10.1038/s43588-026-00958-23 https://doi.org/10.1038/s42256-026-01182-34 https://doi.org/10.1038/s41560-026-01985-z5 https://www.science.org/doi/10.1126/science.aea6792                                          
预览时标签不可点                        
  

关闭

名称已清空

微信扫一扫赞赏作者
喜欢作者其它金额

赞赏后展示我的头像

文章
暂无文章

返回
其它金额

赞赏金额
¥
最低赞赏 ¥0

1
2
3
4
5
6
7
8
9
0
.

 
 

阅读原文

关闭

## 

搜索「」网络结果
 

                 

关闭

调整当前正文文字大小

100%
                                
          
    
                      
                  阅读原文                                                                                    
                
      
        
                    微信扫一扫
关注该公众号                        
  
      继续滑动看下一个  

  
  
        
              轻触阅读原文              
      
        
          
            
              
                
                  
                                                                                                                                          
                    
                      
                        今日新材料                                                                                                                                
          
                                                                              
        
    
      
                向上滑动看下一个            

当前内容可能存在未经审核的第三方商业营销信息，请确认是否继续访问。

继续访问取消
[微信公众平台广告规范指引](javacript:;)

  
          
  
  
    
    
      知道了      
  
      
                    微信扫一扫
使用小程序        
  
  
      
                      
            
          取消          允许        
  
  
    
              
        
      取消      允许      
  
  
    
              
        
      取消      允许      
  ×  分析
  
  
    
            
                        
                                        
      微信扫一扫可打开此内容，
使用完整服务          
    
      

今日新材料

已关注

赞分享
推荐 写留言 

              ：，，，，，，，，，，，，。 视频小程序赞，轻点两下取消赞在看，轻点两下取消在看分享留言收藏听过                  

可在「公众号 > 右上角  > 划线」找到划线过的内容

我知道了

,

,

关闭
选择留言身份
更多

留言

  

暂无留言

1条留言

已无更多数据

发消息

   写留言:

关闭

更多

关闭

## 确认提交投诉
你可以补充投诉原因（选填）
确定

## Related Notes

- [[研究进展：AI+新材料，5篇类脑智能 | Science-Nature Computational Science]]
- [[美国国家科学院院刊 (PNAS) | 脑启发神经环路演化赋能脉冲神经网络创新]]
- [[GNN图神经网络，非结构化数据分析利器！]]
