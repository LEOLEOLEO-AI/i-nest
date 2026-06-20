---
author:
- '[[小九]]'
category: Web-Clips
created: 2026-04-27
description: 2026年春天，科技圈上演了一场精彩的“隔空对话”。一边，英伟达创始人黄仁勋在接受访谈时，被问及如何看待谷歌TPU的竞争。
published: null
quality: low
source: https://mp.weixin.qq.com/s/3sMcq1u6szfMrmdd8bfvxA
tags:
- clippings
- needs-review
title: 从“备胎”到训练推理“正式分家”：谷歌TPU的十一年
---

小九 *2026年4月27日 11:00*

![[09f9eaf2ac96c4b4895c4879fbeac9aa_MD5.webp]]

2026年春天，科技圈上演了一场精彩的“隔空对话”。

一边，英伟达创始人黄仁勋在接受访谈时，被问及如何看待谷歌TPU的竞争。

他姿态从容，将TPU定位为“个例而非趋势”，并重申英伟达的护城河在于覆盖“世界上所有类型应用”的通用加速平台。

话音落下不久，另一边，谷歌在拉斯维加斯的Cloud Next大会上，正式发布了第八代TPU。

这次发布没有延续“更强一代”的剧本，而是做了一个更激进的决定：将训练与推理，彻底“分家”，推出独立的TPU 8t（training)与TPU 8i(inference)。

![[3b1320e14cdbabbbf072d7f02fe601e4_MD5.webp]]

## 一、 为什么要“分家”？

要理解这场“分家”，得先看看今天的AI在干什么。

几年前，AI的世界相对纯粹：目标是做出一个大模型，大家比拼的是训练速度和算力规模。

那时的芯片，像一枚重型运载火箭，核心任务就是把模型这个“卫星”又快又好地送上天。

但智能体（Agent）的崛起，改变了一切。现在的AI，不仅要学习，更要工作。

它需要处理万字长文、进行多步逻辑推理、在虚拟环境中规划未来，还要同时响应全球数百万用户的实时请求。

于是，AI的工作负载出现了分岔路口。

**训练，追求的是极致的吞吐量和规模** 。

它像建造一艘航母，可以忍受数周甚至数月的工期，但要求所有部件并行作业，效率至上。

**推理与服务，追求的则是极致的延迟和能效** 。

它像指挥一个蜂群无人机编队，每一次决策都必须瞬间完成，任何微小的卡顿都会导致任务失败。

这两种需求，在物理上是矛盾的。

追求吞吐，需要巨大的内存带宽和密集的计算阵列；追求低延迟，则需要极快的数据访问路径和精巧的协同机制。

试图用同一套硬件满足两者，就像要求一辆车同时是F1赛车和重型卡车——结果往往是两头不靠，成本高昂。

谷歌的答案简单而彻底：承认矛盾，彻底分家。

TPU 8t和TPU 8i，是两套从 **设计目标、合作方到物理拓扑** 都截然不同的系统。

这不是产品的简单细分，而是对AI现实演进的一次诚实回应。

那么，谷歌是如何一步步走到这个“必然”的岔路口的？

这需要我们把时钟拨回十一年前。

## 二、 TPU简史：一场始于“备胎”的逆袭

故事的开头，没有宏伟蓝图，只有一场迫在眉睫的 **算力危机** 。

2013年，谷歌的研究人员算了一笔账，结果让人头皮发麻：如果全球仅1亿安卓用户，每人每天使用3分钟语音搜索，所需的神经网络算力，将是 **谷歌整个数据中心总算力的两倍** 。

而全球安卓用户，远不止1亿。

当时摆在面前的有三条路：继续用CPU（太慢）、采购现成的GPU（效率有损且受制于人），或者，走上那条最艰难的路— **—自研芯片** 。

谷歌选择了第三条。通常需要数年的ASIC开发周期，一支由Norman Jouppi带领的团队，只用15个月就走完了从立项到大规模部署的全过程。

更惊人的是，首批交付的硅片 **无需任何纠错** 。

2015年，第一代TPU悄然问世。它采用28nm制程，初衷只是为了加速搜索排名中的神经网络推理，像个“备胎”。

但它带来的效果是震撼的：15至30倍的性能提升和30至80倍的能效飞跃。

它的核心秘密，是一个名为“脉动阵列”的古老架构——让数据像血液一样在计算单元间规律流动，极大减少了数据搬运的能耗。

这颗“备胎”证明了，专用芯片的潜力超乎想象。

真正的命运转折发生在2017年。

谷歌研究员发表了《Attention Is All You Need》，提出了Transformer架构。

有趣的是， **Transformer的核心注意力机制，完完全全就是三次极其规整的大型矩阵乘法，与TPU的脉动阵列简直是“天作之合”** 。

**有人说，是Transformer“中了TPU的彩票”** 。

从此，TPU从推理“备胎”，一跃成为支撑大模型时代的核心引擎。

此后，谷歌的迭代快得令人目眩：上云服务、引入液冷、采用光互联（OCS）解决超大规模集群的通信瓶颈……

去年 11 月，谷歌正式推出Gemini 3，该模型全程由自研 TPU 集群训练，完全摒弃英伟达 GPU。受自研算力突破、AI 竞争力兑现提振，谷歌股价一路走高，11 月 25 日创下历史新高，单日收涨 1.53%。

反观英伟达，同日盘中大跌超 7%。市场意识到：顶级大模型训练不再刚需英伟达 GPU，其算力垄断壁垒被击穿，成长预期承压，资金大幅出逃。

曾经沦为备选的 TPU，一跃成为改写 AI 算力格局的核心利器。

依靠十一年技术沉淀，谷歌在 2026 年拆分出8t 训练芯片、8i 推理芯片，以专用化芯片布局，正式向算力赛道发起冲击。

## 三、 第八代TPU详解：“分家”后的双星闪耀

“分家”不是削弱，而是让各自在专业领域做到极致。

这是对过去“既要又要”设计哲学的彻底扬弃。

### TPU 8t：为“建造宇宙”而生的超级工程机

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

它的使命很明确：把万亿参数模型的训练，从“以月计”压缩到“以周计”。

为此，它成了一台纯粹的规模怪兽。

- **专治“偏科”的SparseCore** ：大模型训练中有大量像“嵌入查找”这样不规则、耗时的“杂活”。8t集成了一个专门的SparseCore来处理它们，好比给主计算单元配了个专业的助理，让其能心无旁骛地冲刺。
- **原生FP4与内存洪流** ：它直接支持4位浮点计算，在保证精度的前提下，让核心算力吞吐直接翻倍。配合216GB的海量HBM内存，它为史上最大的模型预备了“记忆海洋”。
- **Virgo网络** ：连接百万芯片的血管：单颗芯片再强，也有极限。8t的真正威力在于集群。全新的Virgo网络，让单一逻辑集群可以连接超过100万颗TPU芯片，实现近乎线性的性能增长，这是为建造“AI宇宙”准备的基石。
![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

### TPU 8i：为“运行世界”而雕琢的精密时空管理器

如果说8t是重工业，8i就是精密外科。它的世界里，毫秒级的延迟就是一切。

- **炸掉“内存墙”** ：推理，尤其是生成长文本，最怕等数据。8i塞进了384MB的片上SRAM，是上一代的3倍。这能让庞大的“KV缓存”完全住在芯片上，把处理器等待数据搬运的时间压到极限。
![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

- **CAE** ：消灭“等待开会”的时间：当智能体进行复杂思考或多专家（MoE）协同时，芯片间需要频繁“对答案”。8i内置了集合通信加速引擎（CAE），专门硬件加速这种同步，将延迟降低5倍，让思考流程再无停顿。
- **Boardfly网络** ：重构通信的几何学：8i抛弃了传统的环形网络，创造了Boardfly分层全互联拓扑。在1024颗芯片的集群里，它将最远的通信距离从16跳缩短到7跳，延迟直接砍半，为智能体协作铺设了“高速公路”。
![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

| 特性 | TPU 8t (建造者) | TPU 8i (响应者) |
| --- | --- | --- |
| 核心使命 | 大规模预训练 | 实时推理与服务 |
| 网络 | 3D Torus (Virgo，为扩展而生) | Boardfly (为低延迟而生) |
| 秘密武器 | SparseCore (处理杂活) | CAE (加速协同) |
| 片上SRAM | 128 MB | 384 MB (驻留关键数据) |
| 设计哲学 | 极致吞吐，规模至上 | 碾压延迟，效率为王 |

## 四、 谷歌的算计与黄仁勋的回应

谷歌为何不惜工本也要“分家”？这背后是多重战略算计。

首先， **是技术上的诚实** 。

训练与推理对硬件资源的需求已是镜像对立。

强行合一意味着巨大的性能妥协和成本浪费。“分家”是工程思维下最诚实的答案。

其次， **是抢占未来定义权** 。

谷歌判断，未来的价值不在于“训练出AI”，而在于“让AI持续运行起来”。

TPU 8i及其代表的低延迟架构，正是在为未来数以亿计的智能体交互经济铺设底层轨道。

**最关键的一点，是构建“系统级经济性”护城河，直接回应黄仁勋** 。

黄仁勋的自信源于两点： **一是英伟达提供的是全栈加速计算平台** ，覆盖科学计算、图形渲染等远超AI的范畴； **二是牢不可破的CUDA生态** ，他认为专用芯片因“可编程性不足”而无法适应快速演进的AI算法。

谷歌的第八代TPU，正是冲着这两点来的。

它通过 **全栈协同（AI Hypercomputer）** ——整合自研Axion CPU、定制网络、液冷散热和软件栈——直接在客户最关心的总拥有成本（TCO） 上发起挑战。

用“训练性价比提升2.7倍”、“推理延迟腰斩”这些硬指标，证明在确定性的主流负载上，专用方案的效率可以碾压通用方案的“灵活性溢价”。

同时， **原生支持PyTorch** 成为破局关键。谷歌不再强迫开发者适应自己，而是主动拥抱主流生态。

这正是为了破解黄仁勋所依仗的“生态迁移成本”护城河，告诉开发者：来用TPU，没那么难。

## 五、 结语：一场持久战的序幕

谷歌TPU的“分家”，正式拉开了一场新竞争的序幕。

对产业而言，价值正在 **从销售标准芯片，向上游的系统集成、定制网络和内存分层设计能力** 迁移。

而对整个AI硬件格局来说，这将是一场“通用生态”与“专用效率”的持久战。

黄仁勋表面从容，但深层担忧的，正是出现一个脱离CUDA的“另一个技术栈”。

谷歌通过吸引Anthropic、Meta等大客户，正在将这种担忧变为现实。

**未来，市场可能会分层：前沿的、探索性的、复杂多变的研发负载，可能仍将首选英伟达的通用GPU；而规模化、稳定化的核心生产负载，将越来越多地权衡像TPU这样专用方案的系统级经济性** 。

回望这十一年，谷歌TPU从解决一个具体的算力焦虑出发，用持续的迭代回答了“专用化”的价值，最终在智能体时代，敢于用“分家”这一大胆举动，来回应关于未来的所有疑问。

**精彩内容**

**[九章智算云上架DeepSeek-V4 Pro！AI 编程直接封神！](https://mp.weixin.qq.com/s?__biz=Mzk2NDM3NzYzNg==&mid=2247493260&idx=1&sn=de1242f611c1716ff66d5680e804f18a&scene=21#wechat_redirect)**

**[阿里云Coding Plan 限购，Token Plan 接力，上哪还能买到coding plan？](https://mp.weixin.qq.com/s?__biz=Mzk2NDM3NzYzNg==&mid=2247493194&idx=1&sn=bec94be5cdbb741ed6e7622ff06fce31&scene=21#wechat_redirect)**

**[超详细版：Obsidian + Claude Code 搭建个人知识库实践指南](https://mp.weixin.qq.com/s?__biz=Mzk2NDM3NzYzNg==&mid=2247493136&idx=1&sn=9ab86af9581864f0616833e8d02fa70a&scene=21#wechat_redirect)**

**[0门槛的openclaw小龙虾省钱秘籍，打工人直接抄作业](https://mp.weixin.qq.com/s?__biz=Mzk2NDM3NzYzNg==&mid=2247492900&idx=1&sn=a89f47cc50a79ef6c0d78fe95718221d&scene=21#wechat_redirect)**

**[OpenClaw史诗级更新！但别急着更新，我们有更省事的办法](https://mp.weixin.qq.com/s?__biz=Mzk2NDM3NzYzNg==&mid=2247492709&idx=1&sn=f16fd5efd0d7dc973f8556faed297001&scene=21#wechat_redirect)**

**[为了不让你的“龙虾”裸奔，我们做了一本73页的《OpenClaw 安全操作指南》](https://mp.weixin.qq.com/s?__biz=Mzk2NDM3NzYzNg==&mid=2247492485&idx=1&sn=c2496512d950d4ebd3c3b5aa2570bef6&scene=21#wechat_redirect)**

**[我们做了一本OpenClaw 像素级实操案例集，看完直接上手](https://mp.weixin.qq.com/s?__biz=Mzk2NDM3NzYzNg==&mid=2247492750&idx=1&sn=afb1ca904a1c34d95f19ac3c642137a6&scene=21#wechat_redirect)**

**[【完整版PPT】英伟达2026 GTC黄仁勋演讲稿，附下载](https://mp.weixin.qq.com/s?__biz=Mzk2NDM3NzYzNg==&mid=2247492562&idx=2&sn=a07f58e0752941ca47fd88a7d56f23b1&scene=21#wechat_redirect)**

**[我佩服我同事，竟然整理了一本83页的OpenClaw“红宝书”](https://mp.weixin.qq.com/s?__biz=Mzk2NDM3NzYzNg==&mid=2247492342&idx=1&sn=65a4aa65b02ca2161e6a14c605ffdea3&scene=21#wechat_redirect)**