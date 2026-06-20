---
title: 英伟达研究：NVIDIA智能驾驶战略对比分析
tags:
- chip
- chip-hardware
- deep-learning
- large-language-model
- patent
- robotics
- semiconductor
- simulation
- survey
---
> 笔记本: 我的剪贴板  
> 创建时间: 2025-05-16  

---

原文链接: [https://mp.weixin.qq.com/s/dr83e8G_6Io3bDwZrqp3pw](https://mp.weixin.qq.com/s/dr83e8G_6Io3bDwZrqp3pw)


佐思汽研发布《**2025年英伟达汽车与AI业务分析报告**》。

英伟达从智驾芯片、智驾方案、仿真系统、端到端、大模型等，构建了完整的智能驾驶生态系统。


来源：英伟达，Egil Juliussen

智能驾驶领域，能够与英伟达生态抗衡的，主要是地平线机器人和高通。

以下是英伟达（NVIDIA）与地平线（Horizon Robotics）在智能驾驶生态布局的对比：


**英伟达 vs 地平线智能驾驶生态对比**


英伟达在高阶智驾方案、舱驾融合方案、中阶智驾方案方面均有布局。


**英伟达高阶智驾芯片和竞品的对比**

英伟达在高阶智驾方面的主要产品包括Orin-X和Orin-Y，主要挑战者包括地平线J6P和黑芝麻智能华山®A2000。


**英伟达舱驾一体芯片和竞品的对比**

英伟达推出了舱驾一体芯片Thor。性能最强的Thor-Super算力可达2000TOPS，最高可支持L4级智驾的Thor-X算力达1000TOPS，Thor-U算力达700TOPS。


**英伟达中阶智驾芯片和竞品的对比**

英伟达在中阶智驾方面的主要产品是Orin-N，主要挑战者包括地平线J6E/M 和高通8650。


**英伟达在工具链、仿真和AI领域与竞争对手的对比**

以下为英伟达、地平线、高通在智能驾驶工具链、仿真和AI领域的布局对比：


**《2025年英伟达汽车与AI业务分析报告》目录**


页数：168页


**01**


**英伟达简介和综述**


**1.1 英伟达  公司简介**
英伟达公司简介和汽车业务四大支柱
英伟达主要业务板块
英伟达营收情况（自然年）
英伟达2021-2024各季度分业务收入
英伟达数据中心、汽车业务收入同比增速
英伟达的收购
英伟达收购近30家公司，打造AI帝国
为什么大厂做AI训练都选择英伟达而不是英特尔AMD？
**1.2 英伟达  产品布局**
英伟达布局了AI产业从芯片到应用的几乎所有层级
英伟达主要芯片产品
英伟达芯片路线图
英伟达芯片产品路线（2025-2028）
英伟达主要AI芯片
AI芯片GB200
英伟达AI硬件平台
英伟达的AI工具
英伟达CUDA
英伟达NVLink
英伟达大语言模型和GenAI
英伟达推出全栈综合安全系统NVIDIA Halos
**1.3 英伟达 GPU产品**
英伟达GPU历代架构和代表芯片
英伟达超级芯片和超级计算机平台
英伟达发布超级芯片B200
英伟达推出新一代GPU：GB300和B300
英伟达GB300、B300、B200对比
英伟达 AI GPU 路线图与单芯片技术规格
**1.4 英伟达  2024-2025动态**
NVIDIA推出6G研究云平台
英伟达展望未来 AI 加速器
英伟达入股自动配送机器人公司
英伟达与卡耐基梅隆大学研究团队合作
英伟达和通用汽车扩大合作


**02**


**英伟达 座舱芯片**


英伟达切入汽车芯片
英伟达汽车芯片演进
联发科与英伟达合作打造智能座舱芯片
英伟达深度学习处理器Parker
英伟达汽车中央计算芯片
奔驰MBUX使用英伟达芯片


**03**


**英伟达 智驾芯片**


**3.1 英伟达 自动驾驶SOC综述**
英伟达智驾 SoC 产品组合
英伟达ORIN主要支持Tier1及量产方案（1）
英伟达ORIN主要支持Tier1及量产方案（2）
Thor+S32G+TC397架构方案
单Orin英伟达开发板框图
智驾、座舱、泊车三合一双Orin跨域融合系统方案
Orin-X/J5+8295+S32G 跨域融合系统方案
Orin-X+8295+2*TC397 跨域融合系统方案
单Nvidia Xavier 智驾系统方案
**3.2 英伟达 ORIN**
英伟达ORIN SoC系统架构：框架图
英伟达ORIN SoC系统架构：功能设计
英伟达ORIN SoC系统架构：CPU
英伟达ORIN SoC系统架构：GPU
英伟达ORIN SoC系统架构：深度学习加速器DLA
英伟达ORIN SoC系统架构：可编程视觉加速器PVA
英伟达ORIN SoC系统架构：接口
以Orin为核心的智能驾驶域控制器的框架图
英伟达推出智驾芯片Orin Y
Orin X, Orin N和Orin Y参数对比
**3.3 英伟达 THOR**
英伟达下一代中央计算SoC Thor
英伟达Thor架构设计：英伟达Hopper 架构GPU系统框图
英伟达Thor架构设计：英伟达Grace 架构CPU采用Arm Neoverse V2内核
英伟达Thor架构设计：Blackwell架构
英伟达Thor支持NVLink多片级联


**04**


**英伟达 基础软件**


**4.1 英伟达 智驾算法**
英伟达感知算法
英伟达感知算法模型
英伟达算法库：VPI
开源FoundationPose
英伟达软件解决方案
英伟达Hyperion技术路线图
Hyperion 9 在2026年装车
英伟达Drive Hyperion 8
英伟达Drive Hyperion 8.1
英伟达Drive Hyperion 面向L3/L4的开发平台架构
英伟达Drive Hyperion 的最新进展
**4.2 英伟达 中间件和工具链**
英伟达自动驾驶全栈工具链
英伟达软件解决方案：底层DRIVE ® OS，中间件DRIVEWORKS
英伟达：Drive OS简介
英伟达：Drive OS SDK架构
**4.3 英伟达 功能安全**
英伟达适用于自动驾驶汽车的全栈综合安全系统NVIDIA Halos
英伟达自动驾驶系统功能安全部署方案
英伟达自动驾驶系统DRIVE OS功能安全设计
英伟达ORIN芯片功能安全设计
**4.4 英伟达 云服务和仿真**
英伟达Omniverse Cloud
NVIDIA Omniverse平台
英伟达Omniverse合作案例
NVIDIA DRIVE Sim端到端仿真平台
NVIDIA Drive Sim应用案例一
NVIDIA Drive Sim应用案例二
NVIDIA Omniverse应用案例一
NVIDIA Omniverse应用案例二
NVIDIA Omniverse应用案例三
NVIDIA Omniverse应用案例四
英伟达专利提出一种基于“虚拟轨道”的自动驾驶系统
英伟达仿真的最新进展
NVIDIA Omniverse 物理 AI 操作系统扩展至更多行业和伙伴
NVIDIA Omniverse推动AI感知生成到计划决策


**05**


**英伟达 智驾域控**


**5.1 英伟达 THOR平台域控**
英伟达DRIVE Thor SoC芯片智驾域控解决方案
英伟达DRIVE Thor+S32G+TC397架构方案
**5.2 英伟达 ORIN平台域控**
英伟达Orin-X/N SoC芯片智驾域控解决方案（1）
英伟达Orin-X/N SoC芯片智驾域控解决方案（2）
英伟达Orin-X/N SoC芯片智驾域控解决方案（3）
英伟达Orin-X/N SoC芯片智驾域控解决方案（4）
英伟达Orin-X/N SoC芯片智驾域控解决方案（5）
小鹏汽车双ORIN-X自动驾驶域控板拆解
比亚迪双ORIN-X自动驾驶域控
创时智驾单ORIN-X开发板框图
智驾、座舱、泊车三合一双Orin跨域融合系统方案（1）
智驾、座舱、泊车三合一双Orin跨域融合系统方案（2）
智驾、座舱、泊车三合一双Orin跨域融合系统方案（3）
Orin-X/J5+8295+S32G 跨域融合系统方案
Orin-X+8295+2*TC397 跨域融合系统方案
**5.3 英伟达 Xavier平台域控**
英伟达Xavier SoC芯片智驾域控解决方案
单Nvidia Xavier SoC自动驾驶域控方案


**06**


**英伟达智驾系统**


英伟达自动驾驶解决方案
NVIDIA Multicast 的核心设计思想
NVIDIA最新发布端到端自动驾驶框架Hydra-MDP
NVIDIA 自研搭建模型架构 Model room
三方合作，打造基于Thor芯片量产智驾解决方案


**07**


**英伟达AI大模型**


英伟达自动驾驶汽车软件栈
Nvidia发布Llama3-ChatQA-1.5
英伟达推出模型套件Cosmos - Reason1
麻省理工学院与英伟达推出AI模型工具
英伟达的AI演进路线


**08**


**英伟达在机器人的布局**


英伟达机器人开发解决方案
英伟达机器人开发三个计算平台
麻省理工学院与英伟达推出机器人新框架
英伟达推出开源人形机器人功能模型


更多佐思报告
[佐思2025年研究报告撰写计划](http://mp.weixin.qq.com/s?__biz=MzA4NTcwMDQwMg==&mid=2650838978&idx=1&sn=4790191727c0dbcdfca15dd1c9d30c43&chksm=8427cd9fb35044896f7751a817c6d5f2d1096384f728d88a44a754422015132498cd83cc10ad&scene=21#wechat_redirect)


[智能网联汽车产业链全景图（2024年12月版）](https://mp.weixin.qq.com/s?__biz=MzA4NTcwMDQwMg==&mid=2650841001&idx=1&sn=2cc8e8254a4197f4cedb235049830b66&scene=21#wechat_redirect)


**「****佐思研究月报****」**
[ADAS/智能汽车月报](https://mp.weixin.qq.com/s?__biz=MzA4NTcwMDQwMg==&mid=2650844888&idx=1&sn=e91c32c46fb589bba7e5b8713c1602de&scene=21#wechat_redirect)  | [汽车座舱电子月报](https://mp.weixin.qq.com/s?__biz=MzA4NTcwMDQwMg==&mid=2650844743&idx=1&sn=3305c61f5f4406a21ddf3b324822f849&scene=21#wechat_redirect) | [传感器月报](https://mp.weixin.qq.com/s?__biz=MzA4NTcwMDQwMg==&mid=2650844750&idx=1&sn=917f524efe0115a5fed2fc48bf0bea80&scene=21#wechat_redirect) | 电池、电机、电控月报 | [车载信息系统月报](https://mp.weixin.qq.com/s?__biz=MzA4NTcwMDQwMg==&mid=2650844297&idx=1&sn=3eaf5b7fb4a0728436a000211c15f87c&scene=21#wechat_redirect)[ |](https://mp.weixin.qq.com/s?__biz=MzA4NTcwMDQwMg==&mid=2650844297&idx=1&sn=3eaf5b7fb4a0728436a000211c15f87c&scene=21#wechat_redirect) 新技术[月报](https://mp.weixin.qq.com/s?__biz=MzA4NTcwMDQwMg==&mid=2650844849&idx=1&sn=9434c52b69d0b4ecdb9eae93662fb971&scene=21#wechat_redirect) | [中国](https://mp.weixin.qq.com/s?__biz=MzA4NTcwMDQwMg==&mid=2650844296&idx=2&sn=f4219dbfd412c64d6e1b26915601727f&scene=21#wechat_redirect)[AI与机器人月报](https://mp.weixin.qq.com/s?__biz=MzA4NTcwMDQwMg==&mid=2650844296&idx=2&sn=f4219dbfd412c64d6e1b26915601727f&scene=21#wechat_redirect)


「联系方式」
手机号同微信号


产业研究部丨符先生 15810027571
赵先生 18702148304
数据服务部丨 张女士 13716037793
战略咨询部丨 韩女士 15810133447
推广传播部｜廖女士 13718845418

---
## 相关笔记 (AI 自动关联)
- [[一文弄清楚全球智能驾驶芯片竞争格局和各家优劣势]]
