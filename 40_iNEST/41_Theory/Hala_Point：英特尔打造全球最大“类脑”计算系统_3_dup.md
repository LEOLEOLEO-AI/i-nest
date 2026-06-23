# Hala Point：英特尔打造全球最大“类脑”计算系统

> 笔记本: 1.1 新导入  
> 创建时间: 2025-07-02  

---

原文链接: [https://mp.weixin.qq.com/s/mxCKMtE7T8BP-0pglfsNUA](https://mp.weixin.qq.com/s/mxCKMtE7T8BP-0pglfsNUA)


原创林之语                未来芯谈              *2025年05月28日 05:30**浙江*

英特尔的Loihi芯片代表了神经形态计算领域的一次重大突破，其设计灵感源自人脑的神经元结构，旨在实现更高效、低功耗的人工智能计算。
## 🧠 什么是Loihi？——模仿人脑的AI芯片

Loihi是英特尔于2017年推出的首款神经形态研究芯片，采用异步脉冲神经网络（SNN）架构，模拟人脑神经元之间的通信方式。该芯片集成了约13万个人工神经元和1.3亿个突触，能够在极低的功耗下实现自学习和自适应能力。
与传统芯片将计算和存储分离不同，Loihi将两者融合，使数据在芯片内部流动更高效，显著降低了能耗。据报道，Loihi在处理视频等任务时的能耗仅为传统芯片的千分之一。 

神经形态核心组成的完全异步多核网格。它实现了一个脉冲神经网络(SNN)，在任何给定时间，一个或多个已实现的神经元可以通过定向链接（突触）向其相邻神经元发出脉冲（即脉冲）。所有神经元都拥有一个局部状态，并拥有一套独特的规则，这些规则会影响神经元的演化和脉冲产生的时间。交互完全异步、零星，并且独立于网络上的任何其他神经元。Loihi 神经形态核心的独特之处在于其集成的学习引擎，该引擎可通过可编程微代码学习规则实现完整的片上学习。
性能突破：
◦ 能效比：MNIST手写识别任务中，Loihi的能效比GPU高109倍，比IoT芯片高5倍。
◦ 实时性：200ns级时间步长，支持无人机避障、机械臂控制等毫秒级响应场景。
## 🔄 Loihi 2：性能与灵活性的飞跃


2021年，英特尔发布了第二代神经形态芯片Loihi 2，带来了多项关键升级：


- 
**神经元数量**：从13万增加到104万个，提升了8倍。
- 
**制程工艺**：采用先进的Intel 4工艺，芯片面积缩小至31 mm²。
- 
**可编程性**：引入可编程神经元模型，支持更复杂的学习规则和算法。
- 
**通信能力**：支持3D芯片堆叠和千兆以太网接口，提升了芯片间的通信带宽。

这些改进使Loihi 2在处理速度上提高了10倍，资源密度提升了15倍，能效也得到了显著优化。 
## 🧩 Hala Point：全球最大的神经形态计算系统

2024年4月基于Loihi 2芯片，英特尔与桑迪亚国家实验室合作开发了名为“Hala Point”的神经形态计算系统。该系统集成了1,152颗Loihi 2芯片，拥有11.5亿个人工神经元和1,280亿个突触，分布在140,544个神经形态处理核心上。

Hala Point的计算能力达到每秒20千万亿次操作（20 POPS），在能效方面也优于当前的许多数据中心AI加速器。
## 🔧 软件生态：Lava框架的支持

为了支持神经形态计算的开发，英特尔推出了开源软件框架Lava。Lava旨在为研究人员和开发者提供统一的工具和方法，使其能够在传统处理器和神经形态处理器上开发和部署应用。

Lava 是一个开源软件库，致力于开发神经形态计算算法。为此，Lava 提供了一个易于使用的 Python 接口，用于创建此类神经形态算法所需的代码。为了方便开发，Lava 允许在标准冯·诺依曼硬件（例如 CPU）上运行和测试所有神经形态算法，然后才能将它们部署到神经形态处理器（例如英特尔 Loihi 1/2 处理器）上，以充分利用其速度和功耗优势。

此外，Lava 的设计可扩展到神经形态行为的自定义实现，并支持新的硬件后端。
## 🚀 应用前景：从边缘计算到智能机器人

Loihi系列芯片的低功耗和自学习能力使其在多个领域具有广阔的应用前景：
- 
**边缘设备**：如智能摄像头和无人机，可实现本地数据处理，减少对云端的依赖。
- 
**智能机器人**：通过实时学习和适应，提高自主决策能力。
- 
**医疗设备**：实现更高效的生物信号处理和分析。

## 🧭 结语：迈向更智能的未来

英特尔的Loihi芯片系列展示了神经形态计算在实现高效、低功耗人工智能方面的巨大潜力。随着技术的不断进步和应用场景的拓展，神经形态计算有望在未来的AI发展中扮演关键角色。

欢迎关注**「未来芯谈」**探索更多有价值内容

**更多干货**
- 
[A2A加速AI智能互联网到来](https://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247484466&idx=1&sn=4a05a8afb0ddbeac4d86309dfa14bb12&scene=21#wechat_redirect)
- 
[从协议到框架，谁将主导下一代AI应用开发？](https://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247484459&idx=1&sn=0dc1bf0e61a661436c3f225023efa7ed&scene=21#wechat_redirect)
- 
[从谷歌TPU到LPU：Groq如何用一颗芯片改写AI推理规则？](https://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247484450&idx=1&sn=87336884f86a2c2b28efc47e58d404a9&scene=21#wechat_redirect)
- 
[量子战争抢戏，坐看微软如何踢馆](https://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247484436&idx=1&sn=368526cbfda09bcf10b49fed3dbc205a&scene=21#wechat_redirect)
- 
[DeepSeek浪潮汹涌，应用的机会在哪里？](https://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247484425&idx=1&sn=d4f3af212f6edaf924db1fde2c184784&scene=21#wechat_redirect)
- 
[新的风口加速到来](https://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247484414&idx=1&sn=9a9c9bb36d72bd08af45a888cd7019b3&scene=21#wechat_redirect)
- 
[超级智能高歌猛进](https://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247484405&idx=1&sn=574f46423e05f151daeabbf440a0507b&scene=21#wechat_redirect)
- 
[AI ASIC大象转身](https://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247484394&idx=1&sn=c8fc2a65e148a71f1014174debdb9ab8&scene=21#wechat_redirect)
- 
[AI ASIC王者之争](https://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247484352&idx=1&sn=1b1e146bcc125e6f3da21c8d0469b6a9&scene=21#wechat_redirect)
- 
[震惊！Google量子芯片又获得突破性进展](https://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247484335&idx=1&sn=c4bcd636984ce519732a799a53c68de0&scene=21#wechat_redirect)
- 
[亚马逊的秘密武器](https://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247484310&idx=1&sn=0cda0eaf2c7129846bf4d12417367a88&scene=21#wechat_redirect)
- 
[亚马逊Kuiper与马斯克Starlink能否一战？](https://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247484309&idx=1&sn=3cb1fb9cd2d59a9c2f3a1592e13bf6c7&scene=21#wechat_redirect)
- 
[榜一大哥Starlink独孤求败](https://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247484297&idx=1&sn=e47d77c29bed7ecabf77c78ea8a71dc5&scene=21#wechat_redirect)
- 
[Archer eVTOL加速，明年可以拼飞车露营？](https://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247484281&idx=1&sn=face2a32eefa6a46ac1bb70f8f89850d&scene=21#wechat_redirect)
- 
[d-Matrix能否将NVDIA挑落马下？](https://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247484263&idx=1&sn=e71702fc0ac6ed9ad446cc65417e9909&scene=21#wechat_redirect)****
- 
[搅局还是颠覆？5G AI-RAN新变量](https://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247484245&idx=1&sn=5ab29fd41c37636cb9889906d6427d91&scene=21#wechat_redirect)****
- 
[RAN or AI打不过就加入？](http://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247484244&idx=1&sn=ff6bcbb4196186615db5307878c974a4&chksm=c11db47cf66a3d6a44988c5bb4c3a41022d0c3a4a3e813f2fd50f6cabdb5ab4757f87019a4c4&scene=21#wechat_redirect)****
- 
[硬核！山姆奥特曼翻牌永动机](http://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247484211&idx=1&sn=d4bca571d6c500fa16597bcd726cf10d&chksm=c11db41bf66a3d0d4629a2988b1e1935a4b27680cebde2f8f92b776578b68da8dcb0bddf1ddd&scene=21#wechat_redirect)****
- 
[Tesla特斯拉强劲的对手已出现？](http://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247484191&idx=1&sn=f5b4bdd37b092b9529fd7859f120d881&chksm=c11db437f66a3d218afa7801cc44f7019c8dab1fd7fd9a0b907c6cc0cda3bfa866d473cf7eec&scene=21#wechat_redirect)****
- 
[Waymo新一轮56亿融资市值高达450亿美金](http://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247484176&idx=1&sn=8b6c72da5f5900159ce20f44b425c133&chksm=c11db438f66a3d2e699d676ca3fbe15ec5ae8874aa0693d8538120c9593b2faa5e47375ebe89&scene=21#wechat_redirect)
- 
[自动驾驶卡车引擎Aurora](http://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247484166&idx=1&sn=fa10c1fe825e10444ada7f1575b8d309&chksm=c11db42ef66a3d3867d9408a07ecb460ab46e284506ff059a3fe018a76b83ee2909162be2538&scene=21#wechat_redirect)
- 
[W](http://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247484147&idx=1&sn=569fbfaec988c3a3564083cb35365ce4&chksm=c11db5dbf66a3ccdedeb41d0b7cdde087ac31ce147bd712c6e404d4f7901145c4047550bad5f&scene=21#wechat_redirect)[ayve自动驾驶最新进展](http://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247484147&idx=1&sn=569fbfaec988c3a3564083cb35365ce4&chksm=c11db5dbf66a3ccdedeb41d0b7cdde087ac31ce147bd712c6e404d4f7901145c4047550bad5f&scene=21#wechat_redirect)
- 
[人工智能里程碑时刻](http://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247484135&idx=1&sn=236e115278d959c00011871c295f86d1&chksm=c11db5cff66a3cd9e2e189c86b7929982dbb15361fb1ec12f951711df9eeec60d118b7c4c407&scene=21#wechat_redirect)****
- 
[山姆奥特曼的核赌注](http://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247484106&idx=1&sn=ba9613aa6f4e8c17c1eaf1b0274a7cbe&chksm=c11db5e2f66a3cf446eb49b645eb44ca4c63b425ed14bd2fd9fff2f223ed063dd39b8e8ab62f&scene=21#wechat_redirect)****
- 
[Android AI奇点来临](http://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247484098&idx=1&sn=8a96ce127566fa400732d1939b0f3b11&chksm=c11db5eaf66a3cfce59b0305ceec34f13c6cf610c2f7c96bab01a12c3179843c9a2cdf959fcb&scene=21#wechat_redirect)
- 
[5分钟了解Apple Intelligence](http://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247484085&idx=1&sn=81539d78a67be309f9365e8bb98e69a4&chksm=c11db59df66a3c8b81a0f2b9576b73b8b4ded49e40d80dd571be7bfe872d14f7b9021e208a3f&scene=21#wechat_redirect)
- 
[OpenAI O1 LLM的进化](http://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247484072&idx=1&sn=57e57c6e1bc800eeb7d4d44bce28fbdf&chksm=c11db580f66a3c964a237f7a6172311d6889b6fb951048b660e310c8861eb0a2c20280c42c6e&scene=21#wechat_redirect)
- 
[特斯拉TTPoE：以太网通信革命](http://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247484063&idx=1&sn=9c447bb0d9a8b1ca954a52e29af16696&chksm=c11db5b7f66a3ca138a863aeb63546a5adb9002a6be183a210007d3936e6e0de359d941e4993&scene=21#wechat_redirect)
- 
[Tesla特斯拉FSD AI5](http://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247483827&idx=1&sn=fb37270f564ac5e755949eff7700c2c9&chksm=c11db69bf66a3f8d8c874909f03f090d4d5a06249647b1a1a918ef3b0267c0356beaffd86daa&scene=21#wechat_redirect)
- 
[下一代人工智能芯片革命者Rain AI](http://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247484040&idx=1&sn=b34c9957eaa3f246c97400cb366e4c67&chksm=c11db5a0f66a3cb60ec4c64977c0e19402016f8b6efad3738132794961169ec868eee36b00cf&scene=21#wechat_redirect)
- 
[太空AI数据中心先驱—流明轨道Lumen Orbit](http://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247484023&idx=1&sn=a2aa4c1efa142f935949724872fd6372&chksm=c11db55ff66a3c49f1cc3ee10252da1e88f00d5fec1dc85436fd35a1c577e775f304ed68cbb8&scene=21#wechat_redirect)
- 
[量子计算机启蒙](http://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247483989&idx=1&sn=831916c15c73511cd73040b8e7b057cd&chksm=c11db57df66a3c6b46810e77c6e0e08495797344851016d46d87fbc44f8c9132c3f36bb98a59&scene=21#wechat_redirect)
- 
[Neuralink脑机接口2024](http://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247483973&idx=1&sn=141d1534bdfe1ce4627e9ad9745ad020&chksm=c11db56df66a3c7bc34f378b1a331e28ebfc9b9dee2743125ec50640c1733edf7f20c33279c2&scene=21#wechat_redirect)
- 
[Starlink星链 全球高速互联网](http://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247483929&idx=1&sn=ef31126aa32e30a2c2275d7ef143887d&chksm=c11db531f66a3c27a0d3b9332916a18fe0ff3c88de5f12054a41525f57b4e23fb0a864ece6cc&scene=21#wechat_redirect)
- 
[OpenAI加速人形机器人产业之Figure02](http://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247483904&idx=1&sn=b18a3879ddef6db562cd32f0898718c8&chksm=c11db528f66a3c3e650348b42f7cec4425c1fdd82faa3558d1942442fe9f7266bd47c679754d&scene=21#wechat_redirect)
- 
[OpenAI加速人形机器人产业之Figure01](http://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247483744&idx=1&sn=bea0863010adda1bce1bc97b28d200de&chksm=c11db648f66a3f5e4d74d4b1675dc1eadbf6a10912447019d06e48e4698677c348d1c0d10877&scene=21#wechat_redirect)
- 
[AI集群之中继器独角兽Astera Labs(长文）](http://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247483872&idx=1&sn=8d6bbb54d06cdf1742dfaf28213c5aaf&chksm=c11db6c8f66a3fde42a2ed0ca6c18c75f65517201e97b43d2d70bc3a72e022e209825fd9de5b&scene=21#wechat_redirect)
- 
[从英伟达GTC观察Chiplet趋势](http://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247483759&idx=1&sn=7640da2e11c18367f8e64b409c2b48fe&chksm=c11db647f66a3f514ac0895745a924773e1433eecfccc428e8ac021713b29bc1b7ac74778630&scene=21#wechat_redirect)
- 
[超级赛道Hyper AIPC之二](http://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247483793&idx=1&sn=5b6e2cdbdb7629abeacc75a1678daddf&chksm=c11db6b9f66a3fafaf7393fb06035f465225c0d7279346e402c42241fd0f844eaa38eec9d17a&scene=21#wechat_redirect)
- 
[超级赛道Hyper AIPC](http://mp.weixin.qq.com/s?__biz=MzkxMTM4NTE1OQ==&mid=2247483782&idx=1&sn=534ab094701bbfc0471fd3fd75eaea01&chksm=c11db6aef66a3fb835024b4c4e0f0ba7e3c2b08f554976069a390f6fe1a5a86d792fa9921ff9&scene=21#wechat_redirect)


预览时标签不可点


林之语


**微信扫一扫赞赏作者**喜欢作者


关闭
**


名称已清空
微信扫一扫赞赏作者**
喜欢作者其它金额

赞赏后展示我的头像

文章
暂无文章


返回
**其它金额**


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


AI算力暗战 · 目录
上一篇从谷歌TPU到LPU：Groq如何用一颗芯片改写AI推理规则？下一篇AlphaChip：AI变革芯片设计的“下棋大师”


关闭
**


搜索「」网络结果


微信扫一扫
关注该公众号

继续滑动看下一个


轻触阅读原文


                        未来芯谈                      


向上滑动看下一个


当前内容可能存在未经审核的第三方商业营销信息，请确认是否继续访问。


继续访问取消
[微信公众平台广告规范指引](javacript:;)


知道了


                    微信扫一扫
使用小程序


取消允许


取消允许


取消允许
×分析


微信扫一扫可打开此内容，
使用完整服务


未来芯谈

关注 

赞分享推荐 写留言 ：，，，，，，，，，，，，。视频小程序赞，轻点两下取消赞在看，轻点两下取消在看分享留言收藏听过


可在「公众号 > 右上角  > 划线」找到划线过的内容

我知道了


,


,


关闭
选择留言身份**
更多


该账号因违规无法跳转


**
留言**


暂无留言
1条留言


已无更多数据


发消息


写留言:


关闭
**写留言**
提交更多


表情


关闭
**0个朋友**
更多


关闭

更多


## 确认提交投诉


你可以补充投诉原因（选填）
确定

---
**Tags:** #BrainInspired #Chiplet
