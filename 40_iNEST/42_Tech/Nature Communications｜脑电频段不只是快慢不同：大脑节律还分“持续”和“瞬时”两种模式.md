---
author: null
category: Neuroscience
created: 2026-06-15
description: 我们谈到脑电活动时，最常听到的是 delta、theta、alpha、beta、gamma 这些频段。
entities:
- LAVI
- rhythmicity
processed: '2026-06-16T09:37:36.242309'
published: null
source: https://mp.weixin.qq.com/s/912rETbA68NsypDow26wsw
source_file: Nature Communications｜脑电频段不只是快慢不同：大脑节律还分“持续”和“瞬时”两种模式.md
summary: 研究提出基于相位一致性的LAVI方法，揭示脑电频谱由高节律性持续频段和低节律性瞬时频段交替组成。
tags:
- 神经振荡
- clippings
- 脑电频谱
- 节律持续性
title: Nature Communications｜脑电频段不只是快慢不同：大脑节律还分“持续”和“瞬时”两种模式
---

*2026年6月3日 09:15*

![图片](https://mmbiz.qpic.cn/sz_mmbiz_png/S3cLR5qAAdaMiaC7JBhY5FT6OqiaJIH77zfrgvLyrpZBiaKKupNSckOHuJy6SwLAdPkxibJTrcBsovqq4vDg7IkM96kd5cHBwjAw0nchr1bricbk/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

我们谈到脑电活动时，最常听到的是 delta、theta、alpha、beta、gamma 这些频段。delta 慢，gamma 快；alpha 常和闭眼休息有关，beta 常和运动或认知状态维持有关，gamma 则常被放在局部加工和信息整合的语境中讨论。

这套频段语言已经用了很多年。它很方便，也确实积累了大量研究。但它也有一个问题：这些频段通常是按 **频率** 来划分的，好像只要频率落在某个范围内，就天然属于同一类神经振荡。

可真实脑信号并不总是这样。一个频段里的活动，可能是连续维持好几秒的稳定节律，也可能只是几百毫秒内突然出现的一小段爆发。它们在频率上接近，但在时间结构上完全不同。前者更像背景节拍，后者更像短暂事件留下的波纹。

来自 **剑桥大学医学研究委员会认知与脑科学单元** （MRC Cognition and Brain Sciences Unit, University of Cambridge）、 **希伯来大学 Edmond and Lily Safra 脑科学中心** （Edmond and Lily Safra Center for Brain Sciences, The Hebrew University of Jerusalem）、 **哥伦比亚大学数据科学研究所** （Data Science Institute, Columbia University）、 **伦敦大学学院实验心理学系** （Department of Experimental Psychology, University College London）等团队，在 **Nature Communications** 发表了题为 **Universal rhythmic architecture uncovers two modes of neural dynamics** 的研究。文章提出，脑电频谱不能只按频率划分，还需要加入一个新维度： **rhythmicity，也就是节律持续性或相位一致性** 。作者基于 12 个数据集、848 名人类、11 只大鼠、2450 个记录位点，覆盖 EEG、MEG、ECoG、SEEG、LFP 等不同技术，发现大脑频谱中存在一种普遍的双模式架构：一类是高 rhythmicity 的持续节律频段，另一类是低 rhythmicity 的瞬时爆发频段。【434†source】

这篇文章真正想改写的，不是某一个频段的功能解释，而是我们看待脑节律的方式。过去我们问：“这个活动是 alpha 还是 beta？”现在作者认为还要再问一句：“它是持续振荡，还是短暂爆发？”

**只看功率会把很多瞬时事件误认为稳定振荡**

脑电分析里最常用的指标是功率。某个频率功率高，通常就会被理解为这个频率的振荡更强。但功率并不能区分一个信号是真的在稳定振荡，还是被短暂冲击拉高了频谱能量。

作者用一个简单例子说明这个问题。一个信号在 11 Hz 处可能具有稳定相位关系，经过几个周期后仍然能保持较一致的相位预测；另一个 16 Hz 信号虽然也有波动，但相位关系很快漂移，无法维持稳定节律。传统功率分析可能都看到频谱能量，但它不能告诉我们哪个频率更“像真正持续的振荡”。

为了解决这个问题，作者提出 LAVI，也就是 Lagged Angle Vector Index。它的核心思想很直接：如果一个频率上存在稳定振荡，那么当前时刻的相位应该能预测一段时间之后的相位。于是，LAVI比较原始信号和延迟一定周期后的信号之间的相位差，如果相位差在整个时间序列中很稳定，就说明这个频率具有高 rhythmicity；如果相位差很散，就说明它更不稳定、更短暂。

随后，作者进一步开发了 ABBA，也就是 Automated Band Border Algorithm。它不是凭经验指定 alpha 是 8–13 Hz、beta 是 13–30 Hz，而是根据每个个体自己的 LAVI 曲线，自动找出哪些频率显著高于基线、哪些频率显著低于基线。高于基线并超过噪声范围的频段，被定义为高 rhythmicity 的持续频段；低于基线并超过噪声范围的频段，被定义为低 rhythmicity 的瞬时频段。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**图1｜LAVI用相位一致性衡量一个频率是否真的在持续振荡** 作者不是只看某个频率的功率大小，而是比较该频率当前相位和延迟若干周期后相位之间的一致性。稳定振荡会产生较高的 lagged coherence，短暂或不稳定活动则相位关系较散。随机相位但保留1/f功率结构的替代数据没有真实数据中的峰和谷，说明LAVI捕捉到的是相位结构，而不只是功率背景。

这一步是整篇文章的方法基础。它把“脑电波强不强”换成了“这个波能不能持续保持相位关系”。这听起来只是技术指标改变，但后面会带来一个更大的结果：原本看似连续的频谱，被切成了两类交替出现的频段。

**传统频段之间的“空隙”，可能不是噪声，而是另一类瞬时频段**

当作者把 LAVI 和 ABBA 应用于 EEG 数据时，得到的图像很有意思。频谱不是简单从 delta 到 theta 到 alpha 到 beta 连续铺开，而是出现了交替排列的高 rhythmicity 和低 rhythmicity 区域。

高 rhythmicity 的峰大致落在传统 delta、theta、alpha、beta2 等频段附近，尤其 alpha 峰非常明显。低 rhythmicity 的谷则出现在这些峰之间，比如 delta/theta、theta/alpha、beta1、gamma1 等区域。作者把这些低 rhythmicity 区域看作新的瞬时频段，而不是传统频段之间无意义的空白。

换句话说，传统脑电频段像是只标出了“山峰”，但没有认真解释“山谷”。这篇文章认为，山谷并不只是背景噪声，它们可能对应另一种运行模式：短暂、爆发式、对输入或变化更敏感的神经活动。

作者还比较了同一批被试睁眼视觉任务和闭眼休息状态。闭眼时 alpha rhythmicity 升高，这和经典 alpha 功率增强相符合；beta2 rhythmicity 也在闭眼状态下增加，而 beta1 没有同样变化。这个结果提示，传统 beta 频段内部可能本来就包含功能不同的子频段：beta1 更像瞬时爆发，beta2 更像持续节律。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**图2｜ABBA把脑频谱分成持续频段和瞬时频段两类** 代表性被试的LAVI曲线显示，高rhythmicity频段以绿色标出，低rhythmicity频段以蓝色标出，两者沿频率轴交替出现。群体结果中，闭眼休息增强alpha rhythmicity，但自动检测出的频段边界仍然稳定。个体层面，同一频率在不同人身上可能被划入不同类型，说明个体化频段定义比固定频段更适合精细分析。

这里的意义不只是多分出几个频段，而是给脑电分析提供了一个更客观的坐标。过去不同研究组常把 beta、gamma 的范围划得不一样，比较结果时容易混乱。LAVI 和 ABBA 提供了一种从个体数据出发定义频段的方法，既能和传统频段名称对应，又能保留个体差异。

这对脑机接口、神经调控和临床诊断都很重要。因为这些应用面对的不是平均人群，而是单个个体。一个人的 beta1 和 beta2 分界在哪里，可能比教科书上的固定频段更有用。

**低 rhythmicity 频段不是弱振荡，而是更短、更频繁的爆发**

如果低 rhythmicity 频段只是高 rhythmicity 峰旁边的副产品，那它的意义就有限。作者因此进一步分析这些频段中的 burst，也就是短暂功率爆发。

结果显示，高 rhythmicity 频段和低 rhythmicity 频段的 burst 动态确实不同。alpha、beta2 这类高 rhythmicity 频段中的 burst 往往能持续多个周期，原始信号和滤波信号之间有较好对应，整体看起来更像真正的节律片段。相反，theta/alpha、beta1 这类低 rhythmicity 频段中的 burst 更短，衰减更快，相位也更容易发生偏移。

群体统计也支持这种区分。高 rhythmicity burst 持续时间更长；低 rhythmicity burst 出现得更频繁。两类 burst 在总占据时间上相近，但组织方式不同：一个是少而长，一个是多而短。作者还用相位随机的1/f替代数据做对照，排除了这些差异只是粉红噪声造成的可能。

更进一步的模拟显示，当 burst 短于大约 3.81 个周期时，LAVI 会落到低 rhythmicity 区间；当 burst 长于大约 5.45 个周期时，LAVI 会进入高 rhythmicity 区间。这说明 LAVI 确实和 burst 能持续多久有关。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**图3｜持续频段和瞬时频段具有不同的burst动力学** 高rhythmicity频段中的burst持续更久，通常能维持多个周期；低rhythmicity频段中的burst更短、更频繁，更像输入或事件引发的短暂波纹。模拟结果显示，burst持续周期数会系统性改变LAVI值，短burst对应低rhythmicity，长burst对应高rhythmicity。

这部分让“低 rhythmicity”有了具体生理含义。它不是说这些频率没用，也不是说它们只是噪声，而是说它们以不同方式工作：它们不负责维持一个稳定节律，而是在某些时刻短暂出现，标记系统中发生了事件或输入。

这也能帮助理解很多过去看似矛盾的发现。比如 beta 活动有时被认为维持当前运动或认知状态，有时又被认为是短暂 burst，和动作停止、抑制或事件反应有关。按照这篇文章的框架，问题可能不在于 beta 理论矛盾，而是传统 beta 频段里本来就有两个模式：beta1 更瞬时，beta2 更持续。

**这种双模式架构跨越记录技术、脑区和物种**

如果这个架构只在一个 EEG 数据集中出现，它可能只是某个实验的偶然结果。作者因此把分析扩展到12个数据集，包括健康志愿者 EEG、MEG，癫痫患者 ECoG 和 SEEG，帕金森患者 STN LFP，以及大鼠海马 LFP。

结果显示，持续频段和瞬时频段在不同记录方式中反复出现。六个 EEG 数据集中，大多数被试都能检测到多个高/低 rhythmicity 频段；ECoG 的867个皮层电极和 SEEG 的733个深部电极也呈现类似架构。虽然不同数据集、不同脑区的峰频率会略有差异，但频段之间的整体边界保持稳定。

这说明 rhythmicity 不是某一种设备的特性，也不只是头皮 EEG 的混合效应。它出现在非侵入性记录里，也出现在侵入性皮层和深部脑区记录里。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**图4｜持续—瞬时双模式架构在EEG、ECoG和SEEG中反复出现** 作者在六个EEG数据集、867个ECoG电极和733个SEEG电极中检测频段峰和边界。多数被试或记录位点都能检测到至少6个频段，包含高rhythmicity的持续频段和低rhythmicity的瞬时频段。不同脑区和技术之间峰频率略有变化，但整体架构保持一致。

这一步把文章从一个方法论文推进到“普遍架构”的层面。不同技术记录到的电信号来源和空间尺度并不一样：EEG 是头皮电位，ECoG 是皮层表面，SEEG 是深部电极，LFP 是局部场电位。如果它们都能看到类似的 rhythmicity 分段，就说明这可能反映了神经系统更基础的组织原则。

当然，这里的“普遍”不是说每个脑区、每个人、每只动物都完全一样。个体差异仍然存在，脑区差异也存在。更准确地说，是在差异之上存在一个共同框架：脑频谱沿着频率轴交替排列出持续模式和瞬时模式。

**人和鼠、头皮和颅内记录之间，频段对应关系变得更清楚**

这篇文章还有一个很实际的贡献：它可以帮助减少不同研究体系之间的频段翻译困难。

一个长期问题是，头皮 EEG 看到的频段，和颅内记录看到的频段是否能直接对应？作者利用一个同时记录头皮 EEG 和 SEEG 的数据集进行比较。结果显示，虽然群体平均的 EEG 曲线相对颅内信号略快一点，但个体层面 ABBA 定义出的频段峰值非常相似，贝叶斯因子支持两种记录方式之间没有显著差异。

另一个长期问题是，人类 alpha 和啮齿动物 theta 到底是不是功能上相似。大鼠海马常被认为以 theta 节律为主，但这篇文章的 ABBA 分析发现，大鼠海马中最突出的约8 Hz节律，在 rhythmicity 架构里更接近人类 alpha 的位置。作者因此提出，文献中常说的大鼠 theta，可能在这个框架下对应人类 alpha，也就是15 Hz以下最突出的高 rhythmicity 峰。

作者还比较了男性和女性 MEG 数据，结果显示 rhythmicity 架构和频段峰值非常相似，支持不存在明显性别差异。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**图5｜rhythmicity框架有助于对齐不同记录方式、物种和性别之间的频段定义** 同时记录的头皮EEG和SEEG在个体频段峰值上高度相似；人类海马SEEG与大鼠海马LFP也显示保守的双模式架构，其中大鼠约8 Hz强峰在ABBA框架下更接近人类alpha。女性和男性MEG数据没有明显频段差异，说明这一架构在多个维度上具有可比性。

这部分对跨物种神经科学很重要。很多机制研究来自大鼠和小鼠，但人类临床应用依赖 EEG、MEG 或颅内记录。如果频段名称本身不能对应，结果转化就会很困难。rhythmicity 提供了一种不完全依赖传统命名的对齐方式：看频段在整个架构中的位置和节律持续性，而不是只看它叫 theta 还是 alpha。

**健康老化和帕金森病会改变这种节律架构**

如果 rhythmicity 架构有功能意义，它应该会随着脑状态、年龄或疾病改变。作者首先分析了 Cam-CAN 数据集中625名18到88岁健康成人的 MEG。结果显示，随着年龄增长，不只是 alpha，delta、theta、beta2 等持续频段，以及 theta/alpha、beta1 等瞬时频段，rhythmicity 强度和峰频率都出现年龄相关变化。

这说明老化不只是让某个 alpha 变慢或变弱，而是会影响整个 sustained–transient 架构。它提供了一种新的方式来描述神经系统随年龄变化的节律组织。

随后，作者分析帕金森患者丘脑底核 STN 的 LFP 数据。帕金森病中 beta 活动增强是经典现象，尤其和运动迟缓、僵硬以及多巴胺状态有关。结果显示，患者停药状态下，STN beta 范围 rhythmicity 增强；更严格阈值下，这种药物相关效应主要定位在 beta1 这个瞬时频段。进一步 burst 分析发现，停药状态下 beta1 burst 持续时间显著变长，而 beta2 不表现出同样改变。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**图6｜老化和帕金森病都会改变rhythmicity架构，但影响方式不同** 成人寿命期MEG数据显示，多个持续频段和瞬时频段的rhythmicity强度及峰频率随年龄变化。帕金森患者STN记录显示，停用多巴胺药物后beta范围rhythmicity升高，严格分析下效应集中在beta1瞬时频段，并表现为beta1 burst持续时间延长。这提示疾病相关beta异常可能更具体地来自瞬时burst动力学改变。

这部分让 rhythmicity 从基础频谱分段变成了潜在临床指标。过去我们说帕金森 beta 增强，但 beta 里面到底哪一段、哪种模式更异常？这篇文章提示，beta1 瞬时 burst 的持续时间可能比整个 beta 功率更贴近某些病理过程。

对于老化也是一样。传统频谱分析常受到1/f背景活动影响，而 LAVI 因为关注相位一致性，可以在一定程度上减少功率背景变化带来的混淆。它可能为建立健康老化的神经节律参考范围提供新工具。

**TMS实验说明，瞬时频段响应输入，持续频段维持状态**

前面大多是观察性数据。为了更直接测试两种模式的功能差异，作者使用经颅磁刺激 TMS 给大脑输入外部脉冲，同时记录 EEG。

单脉冲 TMS 会诱发一串短暂脑电反应。传统功率分析显示，刺激后很多频率功率都会升高，看起来像一个宽频反应。但如果用时间分辨 rhythmicity 指标 WTPL 来看，增强主要集中在低 rhythmicity 的瞬时频段，包括 theta/alpha、beta1 和 gamma1，并持续到刺激后约300毫秒。这符合作者的预测：短暂输入应该优先激发瞬时频段。

接着，作者使用重复 TMS。每个被试先根据自己的 alpha、beta1、beta2 峰频率定制刺激频率，再接受节律性刺激和非节律性刺激。节律性刺激会在所有频段中增强相位一致性，因为外部脉冲按固定节奏打入系统。更有区分度的是非节律性刺激：它会削弱 alpha 和 beta2 这类持续频段的 rhythmicity，说明不规则输入干扰了原本稳定的持续节律；但在 beta1 瞬时频段中，非节律性刺激反而提高 rhythmicity，可能是多个短暂 ripple 累积形成的结果。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**图7｜TMS输入把持续频段和瞬时频段的功能差异拉开** 单脉冲TMS在功率上诱发宽频增加，但rhythmicity增强主要集中在theta/alpha、beta1和gamma1等瞬时频段。重复TMS中，节律性刺激提高相位一致性；非节律性刺激会降低alpha和beta2持续频段的rhythmicity，却增强beta1瞬时频段反应。这个双重分离支持：持续频段更适合维持正在进行的节律，瞬时频段更适合响应外部输入。

这部分是文章功能解释的核心。它说明持续和瞬时不是作者任意划分的标签，而是对输入有不同反应方式。持续频段像系统正在运行的节拍，非节律干扰会破坏它；瞬时频段像事件响应通道，外部脉冲来了就产生短暂波纹。

这也让“脑节律到底是持续振荡还是burst事件”的争论变得更细。答案可能不是二选一，而是两者都存在，只是分布在不同 rhythmicity 模式中。

**大脑频谱不是一条线，而是频率和持续性的二维架构**

最后，作者把传统观点和新观点放在一起。传统频谱是一维的：delta、theta、alpha、beta、gamma 依次排列，频段之间边界模糊，默认它们都是某种振荡。新框架则是二维的：横轴仍然是频率，另一个维度是 rhythmicity。频率告诉我们活动有多快，rhythmicity 告诉我们它能不能持续。

在这个框架中，高 rhythmicity 频段负责维持正在进行的神经状态。它们像稳定的载波，为脑区之间通信和状态保持提供时间结构。低 rhythmicity 频段则更像事件标记，反映外部或内部输入带来的短暂活动。它们不一定长时间存在，但正因为短暂，反而适合标记变化。

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**图8｜脑节律可以被理解为频率和rhythmicity共同定义的二维架构** 传统观点把脑频谱看成按频率排列的一维频段；作者提出的新框架在频率之外加入rhythmicity维度，将高rhythmicity频段定义为持续模式，将低rhythmicity频段定义为瞬时爆发模式。持续模式更适合维持脑状态和协调通信，瞬时模式更适合响应变化和标记输入事件。

这种二维观点的好处，是保留了传统频段知识，又避免把所有频段都当成同一种“振荡”。alpha 仍然可以是 alpha，beta 仍然可以是 beta，但我们不再把 beta 当作单一东西，而是区分 beta1 的瞬时 burst 和 beta2 的持续节律。这样，很多过去看起来互相矛盾的功能解释，可能会被重新整理。

**脑电分析可能需要从“频率标签”走向“运行模式”**

这项研究最大的启发，是让我们重新理解“脑电波”这个词。脑信号中确实有振荡，但不是所有频谱活动都以持续振荡的方式存在。有些活动更像短暂输入后的波纹，有些则像长期维持的节拍。它们都能出现在频谱图上，却不应该被同一种语言解释。

对基础研究来说，这意味着频段功能不应该只按 delta、theta、alpha、beta、gamma 来讨论，而要同时说明这个活动是 sustained 还是 bursty。对临床研究来说，rhythmicity 可能帮助更精确地区分病理性节律异常，比如帕金森病中的 beta1 burst 延长。对脑机接口和神经刺激来说，个体化 ABBA 频段定义可能比固定频率范围更适合作为刺激和反馈目标。

这项研究的局限性也需要放在这里说。首先，作者主要分析 3–45 Hz 范围，因此更低的 delta 活动和更高的 gamma/high-gamma 活动还没有被完整纳入。低频需要更长记录时间，高频又更容易受采样率和工频噪声影响，未来需要专门方法继续扩展。其次，TMS实验样本较小，且没有直接结合行为任务，因此虽然支持两种模式对输入的不同反应，但还不能完整说明这些模式如何影响具体认知表现。再次，LAVI 和 ABBA 是从宏观电生理信号中定义 rhythmicity，它们揭示的是测量信号中的相位结构，还需要细胞内记录、层状记录和电路模型来进一步解释背后的具体神经机制。

不过，这篇文章提供的框架很有价值。它没有推翻过去一百年的脑电频段研究，而是给它加了一层结构。过去我们把频谱看成一排频段，现在可以把它看成两种运行模式交替排列：持续模式维持当前状态，瞬时模式响应新的输入。大脑也许正是靠这种组合，在稳定和变化之间取得平衡。

最后让人继续想的是，大脑并不是一直用同一种节奏处理世界。它有时需要维持状态，让注意、姿势、认知控制和脑区通信保持稳定；有时又需要立刻响应变化，让外部刺激、内部想法或动作指令被快速标记出来。频率告诉我们节奏有多快，rhythmicity 则提醒我们：这个节奏是在持续运行，还是只在某个瞬间闪现。真正理解脑电活动，可能要从“这是什么频段”走向“它在用哪种方式工作”。

https://www.nature.com/articles/s41467-026-73553-8

请在手机微信登录投票

继续滑动看下一个

AI4Neuro

向上滑动看下一个