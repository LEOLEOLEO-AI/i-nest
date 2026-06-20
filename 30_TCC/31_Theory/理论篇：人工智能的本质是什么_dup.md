---
title: 理论篇：人工智能的本质是什么
tags:
- chiplet
- concepts-theory
- deep-learning
- embodied-ai
- fundamentals
- large-language-model
- neural-networks
- neuroscience
- project
- robotics
---
> 笔记本: 我的剪贴板  
> 创建时间: 2025-07-19  

---

原文链接: [https://mp.weixin.qq.com/s/oM-QhrDEhAhhflhsV4Utww](https://mp.weixin.qq.com/s/oM-QhrDEhAhhflhsV4Utww)


这篇文章不讲工具和应用，只和大家聊聊人工智能背后的“理论本质”。
很多朋友一提到人工智能就有两种本能反应：
① 会不会太难？毕竟背后都是数学公式；
② 不知道这些理论有什么用。
我本人是数学博士，但这篇文章，一个数学公式都不用，只想用简单的话，让你真正明白：人工智能，究竟是什么。
因为，只有看清一件事物的本质，才能在其中挖掘出真正的价值。很期待吧？
## 人工智能在干什么？

“人工智能”，顾名思义，就是让机器模仿人类的思考，去学着“看、听、读、写、想、做”。
但如果只是停留在这种比喻层面，还是太抽象。我们不妨用一个例子，来看看人工智能到底在“想”什么。
## 人工智能如何思考？

人工智能最经典、最本质的问题就是：分类和判断。
比如：

远处走来一只动物，可能是猫，也可能是狗。 我们目前只能测到两个数据：动物的体重、以及叫声的分贝。
当动物走到面前，我们知道它到底是猫还是狗。
如果我们采集了 1000 只动物的数据，就能把这些“体重 vs. 分贝”的数据画在一张坐标图里。
看到这张“红蓝散点图”，我们自然会想两个问题：
- 
1. 猫的点和狗的点，会不会各自集中在不同区域？
- 
2. 如果又来一只新动物，我们能不能根据它的坐标，判断它是猫还是狗？
这就是人工智能最核心的工作：从数据中找到规律，再用规律做出判断。
## 能不能简单地分？

如果散点分布得很工整，比如这样：

那么我们可以用一条直线，把猫和狗分在两边。这就是最简单的“线性模型”：

这很容易理解，也很容易实现。
## 那如果分布更复杂呢？

如果散点稍微复杂一点，比如左下角多了几个红点，右上角多了几个蓝点：

用一条直线，虽然还能大致分出猫和狗，但一定会有一些点被分错。比如几只猫被误判成狗，或者反过来：

这背后反映了人工智能一个非常重要的哲学思想：
✅ 人工智能不追求绝对正确，而是追求“多数正确”。
大部分人工智能底层算法，都是信奉“多数原则”的。比如，如果你问 AI：1+1=几？如果有 80% 的人告诉它 1+1=3，它就会告诉你 3。
虽然听起来荒唐，但这就是 AI 的本质：相信数据里的“大多数”，而不是坚持绝对无误。
## 更复杂的分界

再复杂一点的散点，比如这样：

无论怎么画直线，都分不开猫和狗。这时候怎么办？
我们可以不再画直线，而是画一条弯曲的多项式曲线，就能把红蓝点更精细地区分开。这样的方式，就是“非线性模型”。比如：

但问题来了：
有些场景，就算画再复杂的多项式曲线，也不容易分开红蓝，比如下面这种：

于是，数学家们就发明了更多工具。其中较著名的一个，就是——
## 决策树模型

决策树，可以想象成一棵“会提问题”的树。
这棵树从一个问题开始，根据你的回答不断分支，直到做出最后判断。
比如在我们的例子里，决策树可以先把“体重”分成 5 段，再把“叫声分贝”分成 4 段。如此一来，就能把复杂的红蓝点，分割得非常精准：

这背后藏着一个很深的哲学思想：
✅ 单因素分类做二元判断，往往会出错；但多因素分类做二元判断，即使面对复杂问题，也能更接近真相。
## 企业家能懂的例子

举个企业家熟悉的例子：员工绩效考核。
假如你想判断：谁是真正的优秀员工？
如果你只用单一标准，比如“销售额”，就很容易出错：
- 有人业绩高，是因为分配了大客户，不代表个人能力强。
- 有人业绩一般，但客户极其满意，年年续单。
- 有人业绩高，但老是违反流程，带来风险。
- 有人业绩暂时不高，但正在攻坚新市场，潜力巨大。
因此，仅凭单因素，容易误判。
但如果用多因素，就不一样：
比如：
- 
1. 销售额（高 / 低）
- 
2. 客户满意度（高 / 低）
- 
3. 团队协作能力（好 / 差）
- 
4. 合规意识（强 / 弱）
- 
5. 成长潜力（大 / 小）
你就可以搭建一棵“决策树”：
通过多因素的分支判断，你才能看出：谁是真正的人才，谁只是表面光鲜。
中医也是类似的道理。中医诊断时，绝不会仅凭一个指标下结论，而是综合脉象、舌苔、声音、症状，甚至病人的精神状态。多因素判断，往往能找到问题的根源。
## 除了决策树，还有什么？

除了决策树，人工智能里还有很多非线性模型，比如：
- 神经网络模型
- 支持向量机（SVM）模型
- 决策森林模型 ……
这些模型都有一个共同点：效果往往取决于参数如何设置。
举个例子：
神经网络刚开始训练时，效果往往很差，准确率不高：

但是，只要调整一下参数，效果立刻好很多：

这说明一个重要的事实：
✅ 人工智能的表现，往往不是模型本身有多神，而是看参数调得合不合适。
所以，别盲目迷信 AI 的结果。它在某一类问题上可能很厉害，但换一类问题，就可能失灵，需要重新训练。
## 人工智能的本质总结

人工智能的本质，就是在做两件事：
✅ 分类：找出不同事物间的界限。 ✅ 判断：根据已有规律，给出最可能的答案。
而在这背后，有几条必须记住的真相：
✅ AI 不追求绝对正确，而是追求“多数正确”。
✅ 单一视角容易失真，多维判断才更接近真相。
✅ 再聪明的 AI，本质也是数据+参数的产物。
✅ 真正学好 AI，最重要的是理解背后的逻辑，而不是被复杂的公式吓退。
想学人工智能，不一定要从数学公式入手。先明白它的本质，你就已经赢在了起跑线上。

（来源：高博士深思考）

声明：本公众号转发内容（包括但不限于文字、图片、音频、视频等）仅供交流，其观点不代表本公众号立场；版权归原作者或机构所有，若涉及版权问题烦请留言联系，以便第一时间更正或删除。


往期回顾：


[史上最全的人工智能知识图谱](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247483769&idx=1&sn=8086355dbc080e97d3b148c8e2343707&scene=21#wechat_redirect)


[人工智能发展报告（2024）](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247483769&idx=3&sn=ce707f6143900783f780e90a2133b9b0&scene=21#wechat_redirect)


[互联网女皇玛丽・米克尔重磅回归！340页《AI趋势报告》万字干货解读！](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247497134&idx=1&sn=97c75350c232b434593550f1e0c24b9e&scene=21#wechat_redirect)
[2025 人工智能现状：ICONIQ Capital解读企业级AI的变现之路](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247502504&idx=4&sn=7ca5aa023011c0a7711b081ccac7633a&scene=21#wechat_redirect)
[SCBX丨2025年全球人工智能展望报告：引领AI未来](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247494794&idx=1&sn=827c0580454e662686a8374fcb8aac66&scene=21#wechat_redirect)
[人工智能简史：从概念到应用](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247484084&idx=2&sn=186c5e49b4abe483d191227d5d6a51b0&scene=21#wechat_redirect)
[全球人工智能简史](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247484933&idx=1&sn=ad5a9aa62f7f3fcbb9dd0999b1601a67&scene=21#wechat_redirect)
[中国人工智能应用发展报告（2025）](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247503290&idx=1&sn=a1b11df568521708dd1bdd9d0688f717&scene=21#wechat_redirect)
[2025年中国AIGC应用全景图谱报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247502912&idx=1&sn=1f7c187f966acb099b69588aa3329203&scene=21#wechat_redirect)
[最新「大模型简史」整理！从Transformer(2017)到DeepSeek-R1(2025)](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247484279&idx=1&sn=eb06105b978d14c57d8cad00d22bfb5d&scene=21#wechat_redirect)
[SuperCLUE 2025年5月中文大模型权威测评报告！43款国内外模型全方位能力比拼](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247497523&idx=1&sn=59fd344724719376d408d798da15efd1&scene=21#wechat_redirect)
[2025年推理模型综合测评报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247495396&idx=1&sn=a793ec1bcc82f8cdb903c919ef5494fc&scene=21#wechat_redirect)
[2025大模型发展回顾，国内外大模型进展与未来研判](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247491740&idx=1&sn=43caf7e1c5e9c06b537b56777b0d83e9&scene=21#wechat_redirect)
[国家工业信息安全发展研究中心丨大模型 2.0 产业发展报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247488541&idx=1&sn=8f6222f541b9c187f1dea47ece6acd54&scene=21#wechat_redirect)


[中国电子技术标准化研究院 丨面向智能制造的工业大模型标准化研究报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247493665&idx=1&sn=62d8e901355eb5bf8b63e4ee048a90ce&scene=21#wechat_redirect)


[罗克韦尔发布《智能制造现状报告》第十版](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247498374&idx=1&sn=45473145901966b6161c7c76149f7032&scene=21#wechat_redirect)
[人工智能+制造业应用落地研究报告 (2024)](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247484680&idx=1&sn=5c93f8ba6acefb87bfe02a549ab0219e&scene=21#wechat_redirect)
[广西工业互联网赋能企业数字化转型暨 “人工智能+制造”优秀案例集](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247491736&idx=1&sn=45f52bffc90f6de2e48b7347b1ed81af&scene=21#wechat_redirect)
[工业大模型赋能新型工业化：如何打通落地的“最后一公里”？](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247491582&idx=2&sn=c367b697f82f59f5ffbaf33842fb321d&scene=21#wechat_redirect)
[AI大模型融合工业软件的十大高价值应用场景](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247491048&idx=2&sn=be61534332d4d3f35bcf6405239ff014&scene=21#wechat_redirect)
[麦肯锡：融合生态 拥抱智能 ——2030 中国智能制造及自动化行业展望报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247500189&idx=1&sn=7578904fe5879fe0d4fd3de117ce05f4&scene=21#wechat_redirect)
[浅析中国制造业、汽车业和能源业转型](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247500189&idx=2&sn=c65b7fd239163d4cff51c17e6feb654c&scene=21#wechat_redirect)
[电子制造行业数字化转型白皮书](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247502505&idx=1&sn=b5dafa3dd2a5c5a67d87a7b9e1a1b761&scene=21#wechat_redirect)
[未来的制造：超自动化工厂蓝图](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247502505&idx=2&sn=45763645f5ceedc4466c69053188e6c3&scene=21#wechat_redirect)
[亚马逊云科技赋能制造业：生成式AI驱动的智能化转型](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247502505&idx=3&sn=9669ae7285b34bf992ef1a34c6c2ff5a&scene=21#wechat_redirect)


[中国信通院丨《政企行业智能体研究报告》——AI Agent 如何引领政企数字化转型](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247493027&idx=1&sn=8609509e5f4a642d47a3ddd67c51084a&scene=21#wechat_redirect)
[中国信通院丨中国智能物联网发展机遇与挑战](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247494280&idx=1&sn=5aff8c38f67eaa2a7bf186aa500c0cd9&scene=21#wechat_redirect)
[中国信通院丨“机器人+人工智能”工业应用研究报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247491582&idx=1&sn=f9408974f3b9304b6d94242dfd76e3fc&scene=21#wechat_redirect)
[中国信通院智能化医疗装备产业蓝皮书2024年](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247484733&idx=2&sn=0c9f16086ba4d42f3fd1c317c2fd669d&scene=21#wechat_redirect)
[中国信通院丨智能体技术和应用研究报告（2025年）](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247499815&idx=1&sn=32c5f8228fa04a2d673ef82950bd44d6&scene=21#wechat_redirect)
[中国信通院丨智能中台实践指南（1.0版）](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247489339&idx=2&sn=23e8937951be95463cab1ac3197e0e93&scene=21#wechat_redirect)
[中国信通院丨数字经济中的金砖力量：人工智能驱动的合作与创新](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247502220&idx=1&sn=ef33a4b4151f4f595a3589de1563ff67&scene=21#wechat_redirect)
[中国信通院丨算力中心服务商分析报告（2025年）](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247502504&idx=1&sn=3c5e9697e0b4ddfea105d43fa8daa7b1&scene=21#wechat_redirect)
[数字原生典型案例集 2024-2025](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247502504&idx=2&sn=6bdcb4e76b986de6daee9a834623d44f&scene=21#wechat_redirect)
[数据智能研究报告（2025年）](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247498813&idx=1&sn=350dfee1ccd356732f15570ec0ed1956&scene=21#wechat_redirect)
[《2025年数据库发展研究报告及产业图谱》（ 67 页全文+ 24 页解读）](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247503473&idx=2&sn=c650676b854294604760a7aef4c9543c&scene=21#wechat_redirect)
[高质量数据集实践指南（1.0）](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247503473&idx=3&sn=80c5368b370df8d7cd1812d0c35ae98b&scene=21#wechat_redirect)
[阿里云丨医疗健康行业 AI 应用白皮书](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247496764&idx=1&sn=64820c6c406385a2c3b8779b2ae76fe0&scene=21#wechat_redirect)
[2025医疗大模型研究报告：近300个医疗大模型在院内外场景的赋能实践](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247496764&idx=2&sn=da9a15149c35921cbd62c9c99b63a687&scene=21#wechat_redirect)

[医疗健康大模型白皮书（1.0版）](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247486548&idx=2&sn=e02ab58fdb073feefd41c297d75cbe4d&scene=21#wechat_redirect)
[2025中国智慧医院白皮书](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247499916&idx=1&sn=1d472228aec1b4d4b157a28dd7acf54e&scene=21#wechat_redirect)
[AI Agent+医疗行业研究报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247495256&idx=1&sn=ba3ace4549b0fcfa7bb9d86adbe780b5&scene=21#wechat_redirect)
[中国智慧医疗行业白皮书](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247501215&idx=1&sn=af70ee3c8cf1b48900c908a964ba1ee8&scene=21#wechat_redirect)
[DeepSeek+：医药行业办公实战讲义精华全版（附381页讲义免费下载）](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247501215&idx=2&sn=f066a3f5b3cb30634db2b2453a913da5&scene=21#wechat_redirect)

[31个AI医疗场景盘点，覆盖患者护理、医疗影像与诊断、药物研发、超级自动化···](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247495256&idx=3&sn=98ead71b47280ba41254eda450728243&scene=21#wechat_redirect)
[AI赋能农业高质量发展——AI在农业领域应用的十大案例](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247485133&idx=2&sn=148efd9f38cfba4560b949828c9680c0&scene=21#wechat_redirect)
[2025智慧农业发展现状及案例分析报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247499566&idx=1&sn=01b791b404e5738e99d6a6fdd5386def&scene=21#wechat_redirect)
[AI领域最具影响力的十位华人女性](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247484733&idx=1&sn=2a30775368dcd8e958780cc7231c5558&scene=21#wechat_redirect)
[中央企业人工智能应用场景优秀案例](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247485568&idx=1&sn=34221a35e0b48af407ffeca3ea0a8659&scene=21#wechat_redirect)
[2025央国企AI+数智化转型研究报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247498973&idx=1&sn=1de54d83b764ababb6d589f6b5ca6ac7&scene=21#wechat_redirect)
[2024大模型典型示范应用案例集](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247485927&idx=2&sn=e1716e9696314d5b483dd695bdd61c44&scene=21#wechat_redirect)
[2025具身智能行业发展研究报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247485927&idx=1&sn=62d3b2f44795878b86be3967b4213160&scene=21#wechat_redirect)
[生成式人工智能应用发展报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247486288&idx=2&sn=69ec3fd96c55348861184f8e34f14de6&scene=21#wechat_redirect)
[中国AI Agent行业研究报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247486288&idx=1&sn=3635bdb3bb23371c29ab6c425dcb5f4f&scene=21#wechat_redirect)
[中国AI行业系列观察报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247500309&idx=1&sn=cd51ce68778a45034b987da5b429b13e&scene=21#wechat_redirect)
[清华大学生成式人工智能（AIGC）理论与实践—AIGC如何帮助工作和学习](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247485721&idx=1&sn=4e73c1590ba03c51d5c3ffb7750e69bf&scene=21#wechat_redirect)
[清华大学2025年  DeepSeek政务应用场景与解决方案](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247486822&idx=1&sn=c8dfb06eda474ca871ba5566fef92f69&scene=21#wechat_redirect)
[清华大学丨迈向未来的AI教学实验（395页）](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247487975&idx=1&sn=97f64e8a181a653874e40472847ac1f3&scene=21#wechat_redirect)
[《2024 中国数字政府发展指数报告》发布，四大维度解析省级 / 城市发展现状](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247494105&idx=1&sn=77500ebecb4be2980b51e29aba860ad9&scene=21#wechat_redirect)
[智能数据标注产业发展观察报告丨清华大学](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247494105&idx=2&sn=52ba52c7c41b064adae628ea1ab71557&scene=21#wechat_redirect)
[清华大学丨AI赋能教育：高考志愿填报工具使用指南](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247498670&idx=1&sn=761844308b61f2b3a8bbe30e027125fd&scene=21#wechat_redirect)
[AI Agent智能体行业深度：产业格局、发展展望、产业链及相关企业深度梳理](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247486855&idx=1&sn=9d7b138cece95fbd489714eb1b4077fa&scene=21#wechat_redirect)
[深入解读：Bird & Bird《欧盟人工智能法案：指南》](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247492407&idx=1&sn=43d93af026290ae05ef410af20c45a33&scene=21#wechat_redirect)
[2025年人工智能法律政策图景研究报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247498973&idx=2&sn=1fff927db0250a5c1fe3ffb4c5288be7&scene=21#wechat_redirect)
[北京大学 DeepSeek原理与落地应用](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247487245&idx=2&sn=9f7d11f3e130a5c27752e4217b19ed95&scene=21#wechat_redirect)


[北京大学  DeepSeek提示词工程和落地场景](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247487861&idx=2&sn=b75239ead380482d760d2377041549dc&scene=21#wechat_redirect)
[北京大学 DeepSeek私有化部署和一体机报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247487861&idx=1&sn=3c9d5ee53701b0eeffae47b5ddc0de9b&scene=21#wechat_redirect)
[北京大学丨生成式人工智能与高等教育变革：价值、影响及未来发展](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247491471&idx=1&sn=da74dfe297df43b7dc407eaa4c593609&scene=21#wechat_redirect)
[北京大学丨DeepSeek在教育和学术领域的应用场景与案例（上篇）](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247498043&idx=1&sn=c295fcd3322b8377eb26661566689d5d&scene=21#wechat_redirect)
[北京大学丨DeepSeek在教育和学术领域的应用场景与案例（中篇）](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247498043&idx=2&sn=8cbb3952e02e7a79952b54dc58955d0e&scene=21#wechat_redirect)
[北京大学丨DeepSeek在教育和学术领域的应用场景与案例（下篇）](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247498043&idx=3&sn=8aacf9699741d965d8e3cd4c62f8e125&scene=21#wechat_redirect)
[北京大学丨DeepSeek 原理与教育场景应用报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247492246&idx=1&sn=70b61ca78b2ffd03980a6ac424d73164&scene=21#wechat_redirect)
[北京大学丨AI Agent与Agentic AI原理与应用](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247495796&idx=1&sn=c7be302562a7fba4ce322cf113fc1844&scene=21#wechat_redirect)
[必看！北大出品《AI工具深度测评与选型指南》，39 款工具全方位剖析助你精准选型](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247493248&idx=1&sn=b554984c0b10a5990c66b6c1afaea89e&scene=21#wechat_redirect)
[大任智库丨DeepSeek企业落地应用讲义精华全版（258页）](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247487974&idx=1&sn=00ee76a94d796e4cace399896ae8e855&scene=21#wechat_redirect)
[大任智库丨DeepSeek+：政务办公创新突围讲义精华全版（369页）](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247492563&idx=2&sn=60294b2c0bbbc6dc535c79c26f6302d1&scene=21#wechat_redirect)
[DAMA丨《2025智变：AI赋能政府与央国企智能化转型白皮书》从战略到落地的权威指南](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247492563&idx=1&sn=61c4a39504bded3d2eb976eacac0feeb&scene=21#wechat_redirect)
[2025大模型平台落地实践研究报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247494710&idx=1&sn=f1849b95585808eec09c727461fc6285&scene=21#wechat_redirect)
[中国大模型落地应用研究报告2025](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247501216&idx=1&sn=f66096a85545c595ffe60370cc7db42c&scene=21#wechat_redirect)
[智能体落地最佳实践白皮书](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247498091&idx=2&sn=805563f73634aadee9905196c5fcf43b&scene=21#wechat_redirect)
[破局AI落地困境，用友发布《企业AI应用落地白皮书》](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247498091&idx=1&sn=f22eee581a5cfd0321a77578c6adec48&scene=21#wechat_redirect)
[应用全生命周期智能化白皮书 —— 从技术架构到产业实践的破局之道](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247500667&idx=1&sn=e4b1c4f42082cc5e4aba5f95a86c41e5&scene=21#wechat_redirect)
[Agentic AI应用构建实践指南](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247500667&idx=2&sn=5514181b12905e1b7cc089538d24b12d&scene=21#wechat_redirect)
[AI+运维：构建智能化运维新范式](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247494280&idx=2&sn=b25cd1d8a9135d69d4cd303c0ba9e1ad&scene=21#wechat_redirect)
[数智化安全运营报告（2025）](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247501216&idx=3&sn=3b86e62b6e5634a25600b0f8247159fb&scene=21#wechat_redirect)
[云上人工智能安全发展研究报告（2025年）](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247502504&idx=3&sn=e5d6c0d45b837d2b4f78f4f51fbd9ec8&scene=21#wechat_redirect)
[腾讯云《Data+AI下一代数智平台建设指南》：解锁企业智能化转型的“超级钥匙”](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247499815&idx=2&sn=497f3b01c332ec008c6640f41d3d7ef2&scene=21#wechat_redirect)
[9位院士12位专家联合撰文：人工智能的进展、挑战与未来](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247487974&idx=2&sn=06b458e5e3f47f336f2371aabe0ed99e&scene=21#wechat_redirect)
[浙江大学DeepSeek系列公开课第一季合辑（视频+报告+案例）](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247488580&idx=2&sn=cdd9a5623bd70f0546bfff844e220f7a&scene=21#wechat_redirect)
[浙江大学DeepSeek系列公开课第二季合辑（视频+报告）](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247490766&idx=1&sn=2e2249d7c482c335b9f3c1e3237096d3&scene=21#wechat_redirect)
[厦门大学丨大模型科普报告实战篇：DeepSeek 等大模型工具使用手册](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247492071&idx=1&sn=1cfdb7f6d4728a4a797a01810317b364&scene=21#wechat_redirect)
[厦门大学丨DeepSeek大模型赋能高校教学和科研](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247488658&idx=2&sn=fa0f816f18745b81c7761c0dcb6dd37b&scene=21#wechat_redirect)
[厦大团队2025年  DeepSeek大模型及其企业应用实践](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247487559&idx=1&sn=53f4811e7b9a62c725d1cbf547ad77ab&scene=21#wechat_redirect)
[厦大团队2025年DeepSeek大模型赋能政府数字化转型](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247487245&idx=1&sn=a92ec5848acbd5053edb4a97246cc77c&scene=21#wechat_redirect)
[斯坦福2025年AI指数报告：10张图表看懂人工智能发展现状](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247489339&idx=1&sn=af82fd3e6bbe05fa86518f54dd1c8941&scene=21#wechat_redirect)
[斯坦福HAI《2025年人工智能指数报告》官方中文版正式发布](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247498373&idx=1&sn=b13ba94b3b3d84cd2ab64c9c824715c4&scene=21#wechat_redirect)
[人形机器人产业链市场洞察及方案介绍](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247501957&idx=1&sn=dfcd1ff4ae90e2b7c9b1abf84c257371&scene=21#wechat_redirect)
[中科创投研究院丨2025 中美机器人发展深度分析报告（初稿）](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247489409&idx=1&sn=0b4a6607ecea0f7b6a9f06845322e91a&scene=21#wechat_redirect)

[前瞻产业研究院丨2025年人形机器人产业发展蓝皮书](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247489778&idx=1&sn=024687a77507a9970065c22515ee2eea&scene=21#wechat_redirect)
[觅途咨询丨2025人形机器人应用场景洞察白皮书：工业场景篇](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247490854&idx=1&sn=db492b585d21cbb3777c371c92a2a8f6&scene=21#wechat_redirect)
[新能源智能汽车（AIEV）产业赋能人形机器人发展——2025人形机器人供应链洞察报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247496204&idx=1&sn=4150f9309f6fcf78c88dcc12579a24b3&scene=21#wechat_redirect)
[2025市场洞察报告：人形机器人的商业化路径还有多远](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247499826&idx=1&sn=e76a4d30a99c6b70a370b3a0b42f404e&scene=21#wechat_redirect)
[《人形机器人检测认证白皮书》](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247499826&idx=2&sn=fd2735e4fb9da07b8929f2f8f127c773&scene=21#wechat_redirect)
[2025机器人灵巧手四大模块、产业趋势、市场空间及竞争格局分析报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247501957&idx=2&sn=6cd8d592bc93ed37d4e7886ad4a24351&scene=21#wechat_redirect)
[垂直领域具身智能机器人：下一个科技风口？](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247501957&idx=4&sn=b68aa625c32a23b0345125325bfd69f0&scene=21#wechat_redirect)
[中国电信研究院丨大模型基础设施化下的新型无人经济发展研究报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247491738&idx=1&sn=e264af48bc04966c7169200067cac1e9&scene=21#wechat_redirect)
[中国信息协会丨低空经济发展报告(2024-2025)](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247491466&idx=1&sn=24e8c352d1b40fd08c216ccc35fb9f8c&scene=21#wechat_redirect)

[中国人民大学丨2025中国低空经济城市发展指数（LCDI）报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247489961&idx=1&sn=c46c81a83de8092f5227864649b24687&scene=21#wechat_redirect)
[未来移动通信论坛丨低空经济场景应用与通信需求](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247490795&idx=1&sn=13a4bc76c6e201b129083f8df69dbb7f&scene=21#wechat_redirect)
[赛迪研究院丨中国低空经济应用场景研究报告（2025）：从点状试点到全域融合](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247491466&idx=2&sn=b42a0e2354d4dca4e117558a9fe9b7fa&scene=21#wechat_redirect)
[中国低空经济发展指数报告（2025）](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247495240&idx=1&sn=10c661fc565ad3f2620e45fc2bc03db0&scene=21#wechat_redirect)


[地方低空经济平台建设指南白皮书](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247495240&idx=2&sn=30c147e4986d51df0c9fd5f972ef5d5c&scene=21#wechat_redirect)
[2025中国低空经济市场现状报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247500906&idx=1&sn=4933fe790aa6d1c0fe35219016270fe1&scene=21#wechat_redirect)
[2025低空经济城市发展全景研究报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247501214&idx=1&sn=25fe94fd931167936328012927da7391&scene=21#wechat_redirect)
[低空经济产业与标准化发展报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247501214&idx=2&sn=9cc81c0fb838d4c5fe646843b7e3c4e2&scene=21#wechat_redirect)
[数字低空安全技术体系白皮书](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247500906&idx=2&sn=44901298be98328b0dcf0a197170dbae&scene=21#wechat_redirect)
[低空经济频率研究白皮书](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247500906&idx=3&sn=9b196680fc63bbc033fe4994ca623b0c&scene=21#wechat_redirect)
[智能低空通感网络白皮书](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247501214&idx=3&sn=a5be28c348c4738b23960ad4eb70d9e2&scene=21#wechat_redirect)
[AI+大数据在智慧交通中的应用](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247484084&idx=4&sn=c5f6b603170c324deb82e73c6054540a&scene=21#wechat_redirect)
[智能交通产业联盟丨智慧出行与车路云一体化政策研究报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247489961&idx=2&sn=dd4c2c646ec228e85b3a1b8c004d4b63&scene=21#wechat_redirect)
[人工智能+”时代的智慧城市发展范式创新](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247499586&idx=1&sn=53f73bee3c04a7e18fb0bc2b4c4ca8dc&scene=21#wechat_redirect)
[新型智慧城市建设与展望：基于AI的大数据、大模型与大算力](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247499586&idx=2&sn=20b43df5f303873bf774e95c6e9cb790&scene=21#wechat_redirect)
[赛迪丨“ 十五五 ” 时期我国通用人工智能产业发展趋势研究](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247489980&idx=2&sn=6392d4517a775ab1ccecf070bc6e5f64&scene=21#wechat_redirect)
[赛迪丨人工智能赋能新型工业化：范式变革与发展路径](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247490601&idx=1&sn=1c54bc5521ae8573b28a71edea2e9221&scene=21#wechat_redirect)
[赛迪丨人工智能背景下“存算感连”发展新态势](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247491048&idx=1&sn=7dea3ef72be149ff431da330b60c0a3a&scene=21#wechat_redirect)
[全球智能体发展进展、面临挑战与对策建议](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247501589&idx=1&sn=54840b027981e88e6ed6e26593bd0369&scene=21#wechat_redirect)丨赛迪
[赛迪智库：中国“十五五”机器人产业发展趋势及落地策略](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247501957&idx=3&sn=559689446b046aa121198453ce0f305c&scene=21#wechat_redirect)
[阿里云2025 AI应用开发新范式](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247503290&idx=2&sn=ce5ee9458130d6c604810251a3ab9026&scene=21#wechat_redirect)
[阿里云原生应用平台丨AI应用AI Agent开发新范式](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247490655&idx=1&sn=75fc295924bcf9202be068aac0038e1c&scene=21#wechat_redirect)
[阿里云丨人人懂AI之：从机器学习到大模型](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247491741&idx=1&sn=5ee4b936a3b6f89732e8abfc9f45c49b&scene=21#wechat_redirect)
[阿里云丨金融行业 Agent 百景图](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247493723&idx=1&sn=1a40a91b5e125a4a3076fb50b64a21cf&scene=21#wechat_redirect)
[2025年中国人工智能计算力发展评估报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247485133&idx=1&sn=2178ced2653e0a312d242849ebbdeeaf&scene=21#wechat_redirect)
[中国算力中心产业现状、产业链与未来发展](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247491230&idx=2&sn=93d504a22a102f1aba349bd88a4f645a&scene=21#wechat_redirect)

[IDC丨2025新质算力发展白皮书：生成式AI驱动算力基础设施向纵深升级](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247491230&idx=1&sn=397246c66d9284d7f107165915788ef8&scene=21#wechat_redirect)
[兰德公司丨2025人工智能算法进展及近期发展预测](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247491742&idx=1&sn=a8b4af578ad9e53d42e1de99e605dfd6&scene=21#wechat_redirect)
[2024中国智算产业全景调研：技术重构与演进](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247499339&idx=1&sn=8af5ccd132c2187c2a55a37248e50886&scene=21#wechat_redirect)
[“AI智能体”与“智能主体AI”：人工智能的两种角色、工作方式与未来发展](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247497523&idx=2&sn=cf462710bbafbf015e04ed8cabcb3f9a&scene=21#wechat_redirect)
[一文搞懂：信息化，数字化，智能化，数智化是不同的概念吗？](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247489980&idx=3&sn=3c3cff02b0d47f2e1f51d23d612615ee&scene=21#wechat_redirect)
[通俗易懂！智能体（Agent）、AIGC、AGI：大模型时代的“三剑客”](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247487773&idx=3&sn=8cf7cc559ce8f35a01a08480950779d6&scene=21#wechat_redirect)
[终于清楚了！机器学习、深度学习、强化学习、迁移学习、集成学习和关联规则学习大解析](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247487975&idx=2&sn=e77d9cb577e677211a0046b70da04dea&scene=21#wechat_redirect)
[揭秘：大模型的参数到底是什么？用大白话让你彻底搞懂！](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247491740&idx=3&sn=ed29542870ad27400a0552e80f12e888&scene=21#wechat_redirect)
[深入理解Token与分词器：Transformer学习的关键突破](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247491741&idx=2&sn=368f6f7061bf5079c2acde74bad54657&scene=21#wechat_redirect)
[下一场范式革命：谁是大模型架构新王者？](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247496292&idx=1&sn=9fea578c88fee2e08ff49b5617e2d01a&scene=21#wechat_redirect)
[复旦大学丨大语言模型能力来源与边界](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247494279&idx=1&sn=85d27858b99b3771583adc32ee6d9fc1&scene=21#wechat_redirect)
[2024中国企业数字化转型典范案例集（514页）](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247494558&idx=1&sn=1ffce4194e4da41c3462e77f9fd2004f&scene=21#wechat_redirect)
[商务部流通发展司发布《数智供应链案例集》](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247496559&idx=1&sn=08d4269e8d575380c1a31880f272d1b8&scene=21#wechat_redirect)
[深入解读：上海交大《2025“人工智能+”行业发展蓝皮书》](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247492562&idx=1&sn=029b121c29600cb143ea5b3f3d9c40db&scene=21#wechat_redirect)
[全球人工智能科研态势报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247503473&idx=1&sn=e76efb78076ef6be9991a261ee733897&scene=21#wechat_redirect)
[《科学智能白皮书2025》全球发布：AI驱动科研新范式，中国引领创新潮流](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247495239&idx=1&sn=a25f041b4f8c41be9ea33e43cec863ed&scene=21#wechat_redirect)
[AI X Science十大前沿观察报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247499339&idx=2&sn=e64db226a0d7eac655ebb5c1fed11ded&scene=21#wechat_redirect)
[驾驭AI：人工智能赋能教学创新实践手册](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247493273&idx=1&sn=43df0baa6f1483fd3e112ee7c5c0557b&scene=21#wechat_redirect)
[深圳市福田小学教研团队丨AI可以这样用——小学数学AI教学应用手册](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247493429&idx=1&sn=bbfd4449bc86d9351841c130391424c8&scene=21#wechat_redirect)
[一文读懂丨什么是低空经济？低空经济应用全场景](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247490794&idx=1&sn=8f13532d305e1c1c0a1fb7eb828379dc&scene=21#wechat_redirect)
[一文读懂丨中国无人机产业链全景与发展趋势](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247491738&idx=2&sn=2342db0035dcf25afda3110d95ace803&scene=21#wechat_redirect)
[低空经济的十大核心技术现状及未来趋势](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247490794&idx=2&sn=01c051315c3a8ed748f7663e47655e52&scene=21#wechat_redirect)
[一文纵览：低空经济产业链](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247495240&idx=3&sn=1051a2d4ae4b6f97b6a681888e387fc7&scene=21#wechat_redirect)
[一文纵览：AI大模型产业链全景图](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247491740&idx=2&sn=6509ed307e6219df3a20559bd9d26594&scene=21#wechat_redirect)
[一文纵览：AI Agent（智能体）产业链全解](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247496292&idx=3&sn=dfdcb24c962d832efb84ba548831b4c9&scene=21#wechat_redirect)

[一文纵览：数字经济产业链全景图](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247492562&idx=3&sn=d53b41051f4c8bcf54fd6758c4cb5471&scene=21#wechat_redirect)
[一文纵览：人形机器人产业链全景](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247496204&idx=3&sn=7afa8a1c65e77ef16b7c3e40f12007d8&scene=21#wechat_redirect)
[一文纵览：具身智能产业链全景解析](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247496387&idx=2&sn=c60f17bde51ca92c0c04dd3c82b48904&scene=21#wechat_redirect)
[一文纵览：AI 玩具产业链全景图](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247496559&idx=3&sn=3edd79da59235071864bf6ac71ecc6cb&scene=21#wechat_redirect)

[DeepSeek、豆包、Kimi、通义千问、元宝、文心一言各有什么优势？选AI就像挑队友，这份「职场搭档指南」请收好！](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247492071&idx=2&sn=f0bf34c1368c50f529ff87208a5126d7&scene=21#wechat_redirect)
[中国互联网协会丨人工智能赋能教育发展研究报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247491743&idx=1&sn=718ff29bf80ca3127694697fb291de49&scene=21#wechat_redirect)
[教育数字化转型与变革白皮书（446页）](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247501801&idx=1&sn=f5d47b001a4d5300bd93248949591b9b&scene=21#wechat_redirect)
[高等教育人工智能发展报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247501801&idx=2&sn=46da0bd8da5806c5c5bd4efd154a9494&scene=21#wechat_redirect)
[AI大模型教育行业白皮书](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247501801&idx=3&sn=e0efb09c7ab31fc424330d8dd4d63f59&scene=21#wechat_redirect)
[《中小学人工智能通识教育指南（2025年版）》正式发布！](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247493273&idx=2&sn=d5186b01e56d14e3a376334c03808196&scene=21#wechat_redirect)
[《中小学生成式人工智能使用指南（2025年版）》发布，各学段人工智能以后这样使用](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247493429&idx=2&sn=fdca0744a36b4b28fb2a14b0f326f418&scene=21#wechat_redirect)
[《中国智慧教育白皮书》发布，国家教育数字化战略行动2.0正式启动丨教育部（附发布视频，白皮书全解析）](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247493867&idx=1&sn=9ef32e79b1f66c820eceb7a99565833d&scene=21#wechat_redirect)
[国家中小学智慧教育平台上线“人工智能教育”版块](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247493867&idx=2&sn=ee1c5b962d56269fdb292fc3af111bfb&scene=21#wechat_redirect)
[《国家中小学智慧教育平台与人工智能融合应用指南》](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247498670&idx=2&sn=074d610eda75b2d57b3077c5020fd341&scene=21#wechat_redirect)
[教育部：《职业院校人工智能应用指引》发布](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247496294&idx=1&sn=6e2dd97dab317900995a910a57d5111d&scene=21#wechat_redirect)
[人工智能在教育领域中的应用](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247499785&idx=3&sn=5105c602e3cc6e07f85ad86f9d0a00f0&scene=21#wechat_redirect)
[6大行动，让数字化赋能教师发展！来看教育部最新通知](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247501801&idx=4&sn=2679be67dbf6c700adc5b0ef9c6a1a8b&scene=21#wechat_redirect)
[AI赋能教育：教师必备的20个AI教学场景，重塑课堂新生态](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247491471&idx=2&sn=6da9b1936b4bc84ce513ec9eb7e2ef03&scene=21#wechat_redirect)
[新质生产力赋能技工院校专业建设指南](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247499785&idx=1&sn=1988e891fea5d412e01b46a3771cdb22&scene=21#wechat_redirect)
[《学生人工智能素养提升与应用指南》](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247496294&idx=2&sn=6e0e9e6a9b1cfbbddd69d85c08e53d92&scene=21#wechat_redirect)
[关于“人工智能+”AI的最新定位、政策文件汇总（蓝字附跳转链接）](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247492407&idx=2&sn=913c986bb47205eb2432ade634f87dec&scene=21#wechat_redirect)
[中国AI人工智能城市TOP50](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247492407&idx=3&sn=9bf7e6bd5c0da77dcba7ddaaba3e6c2a&scene=21#wechat_redirect)
[2025全国企业“人工智能+”行动创新案例TOP100](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247492562&idx=2&sn=66bf9575ae7b103d89ad4c2d7475cbb7&scene=21#wechat_redirect)


[2025年DeepSeek私有化部署解决方案TOP30](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247493665&idx=3&sn=9c29522fc05c11d12f40370ee4ab3027&scene=21#wechat_redirect)
[2025中国智算服务市场领军企业TOP100](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247494280&idx=3&sn=581f1921868f96051f27c46fbaf7a257&scene=21#wechat_redirect)
[2025 AI新型解决方案提供商TOP25](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247494333&idx=3&sn=0474d22af6068b6a406890a44fceabc3&scene=21#wechat_redirect)
[2025中国人工智能500强](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247494794&idx=3&sn=83155bc46baa11838ede5f92d6c4b267&scene=21#wechat_redirect)
[2025多模态AI大模型排行](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247494279&idx=3&sn=d293e485505d1a6c2f9d5b2741f7b96b&scene=21#wechat_redirect)
[2025中国人工智能分类排行](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247500667&idx=3&sn=045cfe946057cf10ae1487e0ba2be212&scene=21#wechat_redirect)
[DeepSeek回答效果不好？90%是因为你的提问方式不对！我来教你几招](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247492752&idx=3&sn=41bcbb9d27f464704df70369696fa8e9&scene=21#wechat_redirect)
[中国机器人30强出炉，《2025年国产智能机器人企业竞争力报告》发布](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247493027&idx=3&sn=de435ccb30259b07838fd999fe5ed9bd&scene=21#wechat_redirect)
[2025年AI智能体构建平台大爆发，哪家最值得选](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247493248&idx=2&sn=b346e8c35e5301c43aeef2b301a6c03d&scene=21#wechat_redirect)
[张亚勤：后ChatGPT时代，中国人工智能产业的机遇、5大发展方向与3个预测](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247493664&idx=1&sn=51246d0b7f937f9f243ed7c0e1c57e12&scene=21#wechat_redirect)
[张亚勤：人工智能发展的一些观点（2025）](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247496292&idx=2&sn=8aff6db37b77c8f03d0caf449c6d73d7&scene=21#wechat_redirect)
[张亚勤：人工智能如何赋能千行百业](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247502220&idx=4&sn=190a53fd47d9858e9c47d918a6f047ff&scene=21#wechat_redirect)
[采购领域的 AI 革命：101 个人工智能用例全解析](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247493665&idx=2&sn=3c967b605c90fe9e394515858fe17ae5&scene=21#wechat_redirect)
[AI银行进化论：从智能客服到风险管理的深度变革与创新路径](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247493789&idx=3&sn=81bce37df01dd2a4b646685e1ed21bb6&scene=21#wechat_redirect)
[数字化转型：战略引领与实践指南](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247494558&idx=2&sn=31d0191f0c6ff5c5034f6c451af9f374&scene=21#wechat_redirect)
[国家数据局《数字中国建设2025年行动方案》，八大任务解读与趋势展望](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247494710&idx=2&sn=f150d43f4281a35ccd22089868f687e1&scene=21#wechat_redirect)
[国家数据局丨数字中国发展报告（2024年）](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247495922&idx=1&sn=051e7f2039843e443a62a8684dca5aae&scene=21#wechat_redirect)
[国家数据局重磅发布《2024年“数据要素×”优秀项目案例集》！（附全文476页免费下载）](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247496939&idx=1&sn=4364aff863838a6861c5fe589f6f1505&scene=21#wechat_redirect)
[国家数据局丨数据标注优秀案例集（2025年）](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247502220&idx=2&sn=d22ac9f5e948895d8cc689d2a50925b5&scene=21#wechat_redirect)
[AI Agent在人力资源落地的5个案例故事](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247495396&idx=2&sn=21fd110dfb1d03e4ccb26cd65dce3650&scene=21#wechat_redirect)
[AI拼到最后，拼的是数据还是模型？](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247495796&idx=2&sn=5471b9522050172afc1a53db4c837236&scene=21#wechat_redirect)
[10个AI生成PPT神器：总有一款适合你](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247496294&idx=3&sn=d282899c8111106530fa165aaa0373df&scene=21#wechat_redirect)
[豆包使用指南，这20个好用的功能你用过几个？](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247497039&idx=3&sn=51e259be1dc33e3f3f2b8bf9235b4d54&scene=21#wechat_redirect)
[国内大模型竞争格局：三大梯队战斗力透视与突围路径](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247497039&idx=1&sn=1240f5cfd7ffb5926b2d3ec3e4996668&scene=21#wechat_redirect)
[一篇写给老板的企业AI落地说明书](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247497134&idx=2&sn=248ec06f2b25d802cb3e174c4484fcec&scene=21#wechat_redirect)
[AI 落地企业 70 问：从入门到避坑，一篇搞定所有难题！](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247490601&idx=2&sn=5e5385264555036b65016687bcf275ce&scene=21#wechat_redirect)
[人工智能AI在数字化转型有哪些应用？](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247497523&idx=3&sn=32e4a4aacd2589109b6be7007f9bc825&scene=21#wechat_redirect)
[AI+数据智能体的三大支点：数据治理、知识库和大模型](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247498091&idx=3&sn=900c0151fff78878b60ebca2a2ca154b&scene=21#wechat_redirect)

[我国人工智能发展态势与战略前瞻](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247498373&idx=2&sn=d3e3ffbe17178a9401b1e23cfbf29251&scene=21#wechat_redirect)


[2025中国人工智能产业人才报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247498374&idx=2&sn=610b923ebfcccf8a8bb663eb3d1a8b2e&scene=21#wechat_redirect)
[2025年机器人产业人才发展报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247499785&idx=2&sn=aae34a30d0b3c8c2072b5a1f2e19fbb4&scene=21#wechat_redirect)
[人力资源智能化：2025年的机遇与合规挑战](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247501589&idx=2&sn=b708afa5ec78374bf41b909b6304513d&scene=21#wechat_redirect)
[智驾和机器人领域人才洞察报告](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247501589&idx=3&sn=c60c5bb7be69eb8a049443c82d3dfbe9&scene=21#wechat_redirect)
[AI落地应用最新工具集](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247498813&idx=2&sn=515ddabecfbce01ae0f074fad8cabb46&scene=21#wechat_redirect)
[AI智能体创业，一定要搞清楚这100个问题清单（建议收藏）](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247498813&idx=3&sn=d378a21d2c3a205ca6d9efefc7fd5d6c&scene=21#wechat_redirect)
[2025年，AI大模型在企业场景走到哪了？](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247499339&idx=3&sn=548da133b19285c23f08b0bb5634fb47&scene=21#wechat_redirect)
[关于人工智能前沿的十个问题](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247499566&idx=3&sn=8635cf7467feccce06a73bda7cf315ef&scene=21#wechat_redirect)
[2025年 AI 发展总结与下半年预测](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247499815&idx=3&sn=dadf087932d50b50f01cc89d92035e29&scene=21#wechat_redirect)
[中国AI医疗大模型七强—AI中医大模型](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247499916&idx=2&sn=4518b33b44ed8e239d6b5fb136659285&scene=21#wechat_redirect)
[复旦大学附属华山医院AI+医疗探索](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247501215&idx=3&sn=124b520cdb8ee6322edea4d800648ff7&scene=21#wechat_redirect)
[人工智能AI在中医药领域中应用场景](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247499916&idx=3&sn=827cdaf2688158dce8a17fcc7f6fa7a7&scene=21#wechat_redirect)
[AI智能体需求五花八门，怎么判断场景值不值得做？](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247500309&idx=4&sn=a7bff882e5dd905d86ea29b20c682f1f&scene=21#wechat_redirect)
[低空经济的蛋糕，哪些城市能分到？](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247500906&idx=4&sn=3b460a1859aeba0041e43f12a48007a7&scene=21#wechat_redirect)
[中国低空经济100家企业梳理](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247501214&idx=4&sn=b2208aabeaa04c8244c4c1a074482cfd&scene=21#wechat_redirect)
[59% 的 AI 项目没能活过落地期](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247501216&idx=4&sn=00465e4e3895f1fd6bc225652d00667c&scene=21#wechat_redirect)
[AI赋能：数据管理的智能变革](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247501589&idx=4&sn=22285a48b3d9d9b18439a6838659f1d3&scene=21#wechat_redirect)
[深度丨AI 原生应用的定义、生态图谱，与五维评估框架](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247503290&idx=3&sn=fc0927a921c0db122fca7dfece6da003&scene=21#wechat_redirect)
[什么是新质生产力？从理论提出到战略体系全面梳理](https://mp.weixin.qq.com/s?__biz=Mzk3NTMxODQzOA==&mid=2247503473&idx=4&sn=7cb657ec6aa8d4d0b06be6bc97b777e2&scene=21#wechat_redirect)


**AI科普馆：打开AI世界之窗**
“AI科普馆”是由浙江省人工智能学会倾力打造的科普媒体平台，主要围绕AI开展理论、技术、产品、应用等方面的科学普及。
平台每天推送优质内容：AI基础知识，让初学者轻松入门；AI技术解析，助力智能技术爱好者紧跟潮流；行业应用案例剖析，展现AI在各行业的应用实践；产业研究报告与行业资讯，为专业人士提供前沿洞察。她不仅是AI知识宝库，更是大众连接AI世界的桥梁。
运营主体浙江省人工智能学会，是经浙江省政府批准的专业社会团体，集聚了包括10余位院士在内的3,600+高校教授、工程师、企业家、创业者等AI专业人士，致力于推动浙江经济社会高质量发展。学会定期举办长三角人工智能大会、中国人工智能技术大会、中国AIoT未来论坛、中国首席技术官大会等品牌活动。
走进“AI科普馆”内容平台，加入浙江省人工智能学会，让我们携手拥抱AI智能世界！

---
**Tags:** [[StrategicProposal]] [[Chiplet]]
