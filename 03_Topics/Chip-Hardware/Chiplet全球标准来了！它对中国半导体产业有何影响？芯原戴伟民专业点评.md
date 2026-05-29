# Chiplet全球标准来了！它对中国半导体产业有何影响？芯原戴伟民专业点评

> 笔记本: 技术学习  
> 创建时间: 2022-03-04  

---

随着半导体工艺尺寸进一步缩小，集成电路制造面临的挑战日益增大，摩尔定律日趋放缓，所以Chiplet概念应运而生，Chiplet就是通过工艺的改进来解决“摩尔定律”失效的一种方法，Chiplet走向了和传统的片上系统（SOC）完全不同的道路，类似于搭建乐高积木，通过一组小芯片混搭成“类乐高”的组件。Chiplet技术是SoC集成发展到一定程度之后的一种新的芯片设计方式，它通过将SoC分成较小的裸片（Die），再将这些模块化的小芯片（裸片）互联起来，采用新型封装技术，将不同功能不同工艺制造的小芯片封装在一起，成为一个异构集成芯片。 
 
其实，Chiplet的概念早在10多年前就被提出了，Chiplet技术的概念源于号称印尼神童的Marvell 创始人周秀文博士提出Mochi架构 ，他在ISSCC2015的大会上提出了这个概念，希望Mochi成为许多应用的基础架构。几年后，这个概念开花结果，就是现在的Chiplet。 
  
使用Chiplet 的好处很多，因为先进制程成本非常高昂，特别是模拟电路、I/O 等愈来愈难以随着制程技术缩小，而Chiplet 是将电路分割成独立的小芯片，并各自强化功能、制程技术及尺寸，最后整合在一起，以克服制程难以微缩的挑战。此外，基于Chiplet还可以使用现有的成熟芯片降低开发和验证成本。 
 
 
IBM、英特尔、AMD等都是Chiplet的拥趸，AMD 的EPYC 处理器通过Chiplet成功实现了集成64核的高性能服务器芯片，英特尔的Intel Stratix 10 GX 10M FPGA 也是采用了Chiplet技术。 
 
2019年以后，Chiplet技术快速发展，更多公司开始看好这个技术，台积电、日月光、格芯等晶圆厂封测厂也开始支持Chiplet技术，本土也也有很多IC公司如芯原股份等都开始提供Chiplet设计服务，但是Chiplet还需要解决一个最大的挑战，那就是标准问题，有了一个公开的开放标准，才可以让更多公司用起来。 
 
昨天，关于Chiplet最大的挑战---Chiplet国际标准来了！3月2日，半导体十巨头ASE、AMD、ARM、Google云、Intel、Meta(Facebook)、微软、高通、三星、台积电十大行业巨头联合宣布，成立行业联盟，共同打造Chiplet互连标准、推进开放生态，**并制定了标准规范“UCIe”。**UCIe标准的全称为“Universal Chiplet Interconnect Express”，在芯片封装层面确立互联互通的统一标准。 
 
UCIe是一个开放的工业标准互连，提供高带宽、低延迟、高功率和高成本效益的芯片封装连接。芯片之间的连接。它解决了整个计算连续体中对计算、内存、存储和连接的预期增长需求。它可以满足整个计算连续体中不断增长的计算、内存、存储和连接需求，涵盖云、边缘、企业、5G、汽车。高性能计算和手持设备领域。 
 
UCIe提供了对来自不同来源的芯片进行封装的能力，包括不同的晶圆厂，以及不同的技术。不同的来源，包括不同的工厂、不同的设计和不同的封装技术。UCIe是行业领导者共同开发一个共同标准的结果。UCIe推动者涵盖了云计算、半导体制造、OSAT、IP供应商和芯片设计者的广泛交集。 
UCIe 1.0标准定义了芯片间I/O物理层、芯片间协议、软件堆栈等，并利用了PCIe、CXL两种成熟的高速互连标准。该标准最初由Intel提议并制定，后开放给业界，共同制定而成。UCIe标准面向全行业开放，相关白皮书已提供下载，规范也可以联系UCIe联盟获得。 
 
 
 
UCIe是一个分层协议，如上图所示。物理层负责的是电信号、时钟、链路训练、边带等。芯片到芯片的适配器提供了链接状态管理和参数协商。它可以通过循环冗余保证数据的可靠传输。它可以通过循环冗余检查（CRC）和链路级重试机制保证数据的可靠传输。当支持多种协议时它定义了底层仲裁机制。一个256字节的FLIT（流控制单元）定义了底层传输机制，当适配器负责可靠传输时。UCIe对PCIe和CXL协议进行了原生映射，因为这些协议被广泛部署在板级，跨越计算的所有部分。这样做是为了通过利用现有的生态系统来确保无缝的互操作性。 
 
UCIe支持两种广泛的使用模式。第一种是封装级集成，以提供高功率和高性价比的性能，如图5a所示。连接在板级上的组件如内存、加速器、网络设备、调制解调器等，可以在封装层面上进行集成。适用于从手持设备到高端服务器，并通过不同的封装方案将来自多个来源的芯片连接起来甚至在同一个封装上通过不同的封装选项连接。第二种用途是利用UCIe提供非包装连接，使用不同类型的介质（如光缆、电线、毫米波）。 
 
UCIe支持不同的数据速率、位宽、凸点间距和信道范围，以确保最广泛的互操作性。上表1中详细列出了最广泛的互操作性。它定义了一个边带接口，便于设计和验证。互联的结构单元是一个集群，包括N个单端、单向、全双工的数据通道（标准封装的N=16，高级封装的N=64）。可以说，UCIe的发布打通了Chiplet未来发展障碍，对于推动Chiplet有历史性的意义。 
 
 
**芯原股份戴伟民总专业点评UCIe** 
3月3日，电子创新网总编张国斌专访了芯原股份创始人、董事长兼总裁戴伟民博士，请他从专业角度UCIe标准做一点评和解读。 
 
**戴伟民博士指出四点：** 
 
 
1、此次支持UCIe标准的十大公司中没有IBM ，是因为UCIel来自2019年英特尔牵头的CXL（Compute Express Link）标准组织，该联盟有微软、阿里、思科、戴尔EMC、Facebook、谷歌、惠普、华为等巨头，而IBM主推的是开放式内存接口（Open Memory Interface,OMI)，以前英特尔推CXL的时候，AMD没有加入，这次AMD加入了UCIe，也意味着UCIe标准将成为大芯片主流公司力推Chiplet的标准，IBM的标准可能被放弃掉。 
2、关于Chiplet被翻译为“小芯片”的提法 ，他认为这个叫法不严谨，因为Chiplet并不小，以前有叫芯粒 ，希望业界同仁可以给Chiplet一个响亮的名称，也便于这个技术的推广和应用。（**这里我们有奖征集一下Chiplet中文名，有被采用的会收到一份惊喜礼物！**） 
3、在昨日的发布，十大发起者并没有本土IC公司未来是否对本土公司造成影响？对此，戴伟民表示UCIe原则是开放免费，其实很多本土公司可以申请加入，其实在该标准早期形成中，芯原以及一些本土公司都参与了讨论，本土半导体公司都可以申请加入该标准组织，他认为Chiplet将给中国集成电路产业带来巨大发展机遇！ 
 
 
4、戴伟民博士强调，Chiplet要国际化开放化才可以有生命力，UCIe正体现了开放性， 不必纠结于要搞中国的本地Chiplet标准，虽然这个标准发起者是国际大公司，但是不妨碍本土公司加入，而且英特尔前段时间也提出要将X86开放，正好可以在Chiplet上应用，他认为芯原有可能是第一批面向客户推出Chiplet商用产品的企业。 
 
 
他表示，芯原基于自身先进的芯片设计能力，致力于“IP芯片化”“芯片平台化”的发展。例如，芯原采用Chiplet架构所设计和推出的高端应用处理器平台，从定义到流片仅用了12个月的时间，2021年5月工程样片已回片并在当天被顺利点亮， Linux/Chromium操作系统、YouTube等应用在工程样片上已顺利运行，基于该样片的Chromebook 样机也已经在各大活动中成功展示并吸引了大量关注。这个高端应用处理器平台还集成了芯原的很多IP，包括芯原的神经网络处理器NPU、图像信号处理器ISP、视频处理器、音频数字信号处理器和显示控制器等。 
 
 
他表示从技术角度来说每个**Chiplet一定是个通用芯片，如果做成ASIC就不合适了，但是几个Chiplet**可以拼成一个ASIC，在不适合用Chiplet、用ASIC会更合适的领域，就不必强行分成Chiplet。他认为平板电脑、自动驾驶、数据中心将是**Chiplet**率先落地的应用领域。 
根据市场研究公司Omdia预测，在制造流程中采用Chiplets的处理器芯片全球市场预计将从2018年的6.45亿美元扩大至2024年的58亿美元。不到10年时间，增长9倍之多，可见，Chiplets技术被寄予厚望，其市场潜力发展前景诱人，本土公司在这个领域可以大有作为！ 
 

 

近期微信热文推荐   

 

 

 

 
1、[开年专访谷泰微创始人兼CEO石方敏：2022本土IC要迎“大考”](http://mp.weixin.qq.com/s?__biz=MjM5MTE1MjI5MA==&mid=2652479559&idx=1&sn=1042785ccbe407c24f3b8c7aae1c5703&chksm=bd54e18a8a23689ce51dba111f1fd91e9f6a9a6451ade38788e4100215eb9a0eea108f425dc5&scene=21#wechat_redirect) 
2、[2021中国IC设计大盘点：深圳增速继续跌出前10 ，降速惊人！珠三角是四地区唯一负增长！](http://mp.weixin.qq.com/s?__biz=MjM5MTE1MjI5MA==&mid=2652479153&idx=1&sn=abffda38646207edb5b5df51287642de&chksm=bd54df7c8a23566a01436f30d3e7a03af3afd7137a54c05f220bf845e3cc225f99c74414e71c&scene=21#wechat_redirect) 
3[、美国封堵加剧！逼迫中国有望今年实现28nm制造国产化！](http://mp.weixin.qq.com/s?__biz=MjM5MTE1MjI5MA==&mid=2652473372&idx=1&sn=a5a3d383a32e4d34937dcbaa54e02543&chksm=bd54c9d18a2340c774cad45139ae74ac95a335be6b4175545b8cd3d8381437b72392e7b0da02&scene=21#wechat_redirect) 
4、[胡煜华履新后首秀，她谈了汇顶这些战略布局！](http://mp.weixin.qq.com/s?__biz=MjM5MTE1MjI5MA==&mid=2652476288&idx=1&sn=18a0ed1e815e803ca92d185fddde2a06&chksm=bd54d24d8a235b5b7a75d558936d58a7b38b0d80ed782c7461a70ab06904e6b5c7c46f1862e7&scene=21#wechat_redirect) 
[5、](http://mp.weixin.qq.com/s?__biz=MjM5MTE1MjI5MA==&mid=2652463321&idx=1&sn=8d2ed6e06aa3e63f31d6b6a4d36c296d&chksm=bd5421148a23a8022af62604c1004cdd58862ec691660a0ea62996a0a1e8771b015945f9f108&scene=21#wechat_redirect)[ST竟是本轮涨价受害者？本土MCU如何抓住大机遇？周立功有5点忠告](http://mp.weixin.qq.com/s?__biz=MjM5MTE1MjI5MA==&mid=2652473527&idx=1&sn=3ca8c290a9bc9fb14a43c28c08ca2e27&chksm=bd54c97a8a23406cbf58b5ca5fbf523e7b2808b8dcc1132cc06fef9a50abea15df292e818a2b&scene=21#wechat_redirect) 
6[、](http://mp.weixin.qq.com/s?__biz=MjM5MTE1MjI5MA==&mid=2652463075&idx=1&sn=1f4f10a347d9f4785521ff35656b27e8&chksm=bd541e2e8a2397388da782bdc95a651aa44d2a640a97b485359d5f0d9832e023c50093488116&scene=21#wechat_redirect)[国产替代风头劲，ST MCU扛不住开始放货？](http://mp.weixin.qq.com/s?__biz=MjM5MTE1MjI5MA==&mid=2652473497&idx=3&sn=ff3ef2e7a8fc9b1fb4948ecabea42ba0&chksm=bd54c9548a234042f53f592d3b730064df79b43d34689a2ebba3c73e4470acb9c32623196a55&scene=21#wechat_redirect) 
[7、](http://mp.weixin.qq.com/s?__biz=MjM5MTE1MjI5MA==&mid=2652463075&idx=1&sn=1f4f10a347d9f4785521ff35656b27e8&chksm=bd541e2e8a2397388da782bdc95a651aa44d2a640a97b485359d5f0d9832e023c50093488116&scene=21#wechat_redirect)[OPPO造芯，成了!](http://mp.weixin.qq.com/s?__biz=MjM5MTE1MjI5MA==&mid=2652478803&idx=1&sn=cbf98efdd6595b4d75995cdf1af54157&chksm=bd54dc9e8a2355888313329cfd887f6285d8f9b17b354fa8a8a63bf269995a46e95345c0a4ee&scene=21#wechat_redirect) 
8[、](http://mp.weixin.qq.com/s?__biz=MjM5MTE1MjI5MA==&mid=2652462585&idx=1&sn=4fbf93ba5ba5022dff470184cb826a94&chksm=bd541c348a239522c8e5220b178d5fc010fbc5767746d857eaf15b16baa6abb68d56a5f372c7&scene=21#wechat_redirect)[“美议员提出要将所有14nm中国公司纳入出口管制”的真相](http://mp.weixin.qq.com/s?__biz=MjM5MTE1MjI5MA==&mid=2652473212&idx=1&sn=2c1e3649e6bad46efc5cbe4a6d42e83f&chksm=bd54c6b18a234fa7beb5b80b52a22d226a859f2be009b03bd7c2d2f41c67e21319e542c009ad&scene=21#wechat_redirect) 
9、[“十年磨一剑”Armv9架构来了，V9CPU年底面市！](http://mp.weixin.qq.com/s?__biz=MjM5MTE1MjI5MA==&mid=2652472708&idx=1&sn=ca0fea3ef710fc82fa6bbcdd01293756&chksm=bd54c4498a234d5f37c071789cd8305efe4b915f24442e1f95a3c6884937ed12720737704289&scene=21#wechat_redirect) 
10[、TI为何再出手抛弃世平和文晔！直供是未来？](http://mp.weixin.qq.com/s?__biz=MjM5MTE1MjI5MA==&mid=2652461697&idx=1&sn=fb1520a4655787e3c6eaedc4b0b65a62&chksm=bd541b4c8a23925a8adb8178186065f431fc0e951c701855133fe7b633b40742561cfd191db5&scene=21#wechat_redirect)（**10万+爆文**）     
**觉得有价值请关注我的微信号** 

**关于张国斌微信公共号**
本信号由半导体领域资深媒体人张国斌亲自运营，粉丝多为半导体领域高管，本号关注全球半导体最新科技趋势信息和新兴技术应用，解读半导体产业最新动态，关注一下，让老张带你去一起无限精彩的半导体世界！**欢迎加我个人微信号号18676786761**

---
**Tags:** [[SDSoW]] [[Chiplet]]

---
## 相关笔记 (AI 自动关联)
- [[Chiplet成为半导体的下一个竞争高地]]
- [[中国首个原生Chiplet技术标准发布]]
- [[Chiplet电话会议纪要]]

> [!note]- 可能重复: [[Chiplet成为半导体的下一个竞争高地]] (相似度: 85%)
