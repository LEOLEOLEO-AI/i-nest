# Chiplet Summit 资料分享：展望10年后的GPU和HBM

> 笔记本: 我的剪贴板  
> 创建时间: 2024-04-04  

---

上周我分享了一份白皮书《[*基于Chiplet**的商业分析-**系统与技术*](https://mp.weixin.qq.com/s?__biz=MzAwODExNjI3NA==&mid=2649785087&idx=1&sn=c28100875c40ef5cba48dce38e7dc122&chksm=8377e3a2b4006ab41e4107e43aae268ea73abe38ec6a465a9dbcfddc1d2d23593f3fe8f8c5cf&token=400505657&lang=zh_CN&scene=21#wechat_redirect)》，其实是因为接下来还想发更多的资料。
 
**Chiplet Summit****会议资料 (2024&2023) ****网盘下载
** 
链接：https://pan.baidu.com/s/1y2OCoB2eCSPgW1t0NWCXoQ?pwd=rmix
 
提取码：rmix
 
为什么把去年的资料也列在这里？是因为一年前我在《[*Chiplet Summit **会议资料分享*](https://mp.weixin.qq.com/s?__biz=MzAwODExNjI3NA==&mid=2649784085&idx=1&sn=345414f086c2998d3651409555f56360&chksm=83771e48b400975ee90349f1ef169c027649a76f7e4284c62a50d183506de92fe91071923036&scene=21#wechat_redirect)》里发的其实不全。 
以今年的会议资料为例，https://chipletsummit.com/ 上能下载到大部分，而OCP网站上还有一些（https://www.opencompute.org/events/past-events/ocp-sponsored-chiplet-summit-tutorial-building-the-chiplet-economy）。
 
下面挑一些还不错的ppt页面，简单写一点我的解读。
 
**服务器和PC****是Chiplet****主要市场、HBM****内存的推动 
** 
 
上图是以AMD Ryzen作为PC芯片的代表，列了下Chiplet制造流程中的分工。首先，I/O Die、CPU和缓存内存（3D V-Cache）都是由AMD设计；然后到Front-End制造阶段，I/O Die由于制程要求不高在GF生产，CPU和3D V-Cache都是在TSMC台积电做；I/O Die的Back End 0是在马来西亚的TF-AMD完成，而CPU和3D V-Cache的Hybrid Bonding还是在TSMC；最后的CPU成品封测是在马来西亚。
 
 
服务器芯片先拿AMD的MI210举例，半导体工艺是TSMC的6nm FinFET。主要可以看下GPU处理器Die与HBM内存之间带有TSV的连接。
 
 
NVIDIA的4代顶级GPU，P100、V100、A100和H100分别采用16nm、12nm、7nm和4nm工艺，它们也都使用了HBM内存（从4片到5片）。
 
 
参考上图，Chiplet最大的市场应该是在Server，PC也还不错，而智能手机和自动驾驶领域到2028年渗透率预测也不高。我感觉后两者对芯片整体的面积要求较高，大家想想手机里寸土寸金的密度，能集成度更高显然更好。Automotive对功耗的限制也是较高的。
 
反而越是大型、复杂的，功耗不断提高的芯片，像服务器CPU和GPU，越喜欢Chiplet。具体好处除了我在前一篇分享中列出的之外，Winnie Shao博士的大作《[*多**Die**封装：**Chiplet**小芯片的研究报告*](https://mp.weixin.qq.com/s?__biz=MzAwODExNjI3NA==&mid=2649778994&idx=1&sn=5910a874075a72b61e644d81a29ce72a&chksm=83770a6fb4008379f62f1a3fa502560c328838eb96c64609c1ddbf6baeb7186fe76470319782&token=1132959584&lang=zh_CN&scene=21#wechat_redirect)》写得更好。
 
 
HBM是另一个重要的Chiplet市场。上图中有出货容量和销售额的预测，大致做个参考吧。
 
**从MI300****看3-10****年后的GPU****芯片规模****
** 
 
AMD这一代通用计算芯片分为MI300X（纯GPU）和MI300A（GPU+CPU的单芯片UMA架构）两款。
 
 
所谓MI300芯片的304个GPU处理单元，分布在8个XCD小芯片上。每颗MI300做成一个OCP OAM模组，然后8个OAM安装在一块UBB主板上。这样的一个机架，耗电大约在50kW左右，所以液冷是现在数据中心里的热门技术。
 
未来芯片还会越做越大，即使[NVIDIA暂时还不转向Chiplet？](https://mp.weixin.qq.com/s?__biz=MzAwODExNjI3NA==&mid=2649783312&idx=1&sn=ca8e7198a3837892b8488bd210561153&chksm=83771d4db400945bf6d192967eeef29afbac4593f2bdd4980d9d1f1c37bedb9a9f3a947e063b&scene=21#wechat_redirect)B100/GeForce 5090的功耗也会继续提高。下文中我还会接着讨论这个话题。
 
 
上图分解了MI300(A)的CPU、GPU、I/O Die和HBM Stack等，它们是层叠堆在OAM PCB基板上。6-8片GPU XCD、3片CPU CCD应该都是台积电N5工艺；这里的4个IOD（含NOC和SRAM）是N6工艺，周围HBM内存一共8颗。
 
右下角的芯片成本Breakdown显示，HBM占比达到53%。
 
 
我们先记一下几个数字：MI300 OAM的基板尺寸是102mm*170mm，中间Chiplet部分的边长约为78mm，HBM内存容量192GB，TDP功耗是750W。
 
 
预计3年之后，AMD芯片中GPU处理单元可能增加到456个，HBM内存达到1TB（大模型训练会推动这点吧），整个芯片功耗翻倍至1.5kW。此时OAM基板面积不变，但Chiplet部分的边长增加到约110mm。
 
 
继续预测10年后，芯片中增加到1000个GPU处理单元，HBM内存可能达到4TB，OAM模块的功耗将增加到3kW（到时用[冷板还是2相浸没液冷技术](https://mp.weixin.qq.com/s?__biz=MzAwODExNjI3NA==&mid=2649783782&idx=1&sn=ca6c793b19b5be5fbdc9336171230b6a&chksm=83771cbbb40095ad10292e5e2ee7a169e90ed5410ce2e15f60a877fed609addf4439f9041b69&token=2053678475&lang=zh_CN&scene=21#wechat_redirect)呢？）。对应的OAM PCB基板面积也增大到150mm*170mm。
 
 
最后也展望下10年后的HBM内存吧：Die堆叠封装的层数预计从今天的8-Hi、12-Hi提高到24Hi；数据总线位宽从1024增加到2048；rate/wire速率从8Gbps提高到32Gbps——最后这一点看上去变化最大，估计也是受益于半导体工艺的发展。
 
先写这么多，更多资料大家可以从网盘下载参考：） 
扩展阅读：《*[企业存储技术》文章分类索引（微信公众号专辑）](https://mp.weixin.qq.com/s?__biz=MzAwODExNjI3NA==&mid=2649779739&idx=1&sn=197697a3a20b6028b2fea4f665988993&chksm=83770f46b40086505001200e4264ebb3a904d9b2ba5b632216f42ee053e347bec8f491d1e30d&token=1778073683&lang=zh_CN&scene=21#wechat_redirect)*》****** 
***注****：本文只代表作者个人观点，与任何组织机构无关，如有错误和不足之处欢迎在留言中批评指正。**如果您想在这个公众号上分享自己的技术干货，也欢迎联系我：）* 
**尊重知识，转载时请保留全文，并包括本行及如下二维码。感谢您的阅读和支持！《企业存储技术》微信公众号：HL_Storage**** 
 
**长按二维****码可****直接识别关注** 
**历史文章汇总**：http://www.toutiao.com/c/user/5821930387/ 
http://www.zhihu.com/column/huangliang

---
**Tags:** #Chiplet
