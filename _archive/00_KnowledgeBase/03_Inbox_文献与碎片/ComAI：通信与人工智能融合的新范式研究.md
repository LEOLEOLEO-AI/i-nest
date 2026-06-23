---
title: "ComAI：通信与人工智能融合的新范式研究"
source: "https://mp.weixin.qq.com/s/GKCdxrdzDNC6sEqEBpU4Yw"
created: 2025-10-09
note_id: "1889753436640128360"
tags:
  - "AI链接笔记"
  - "6G关键技术"
  - "ComAI"
  - "语义通信"
  - "get-笔记"
  - "学术论文"
---

# ComAI：通信与人工智能融合的新范式研究

## 摘要

📄 **论文核心信息**   - **标题**：ComAI: The Convergence of Communication and Artificial Intelligence   - **期刊**：IEEE Communications Surveys & Tutorials（JCR Q1/

## 正文

**本期精读论文**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ffb73906face7fe98b4843b2b925bef78?Expires=1780065990&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=cFhHjM6QgnTc5IE9mUbVI7xyvHM%3D)

**ComAI: The Convergence of Communication and Artificial Intelligence**

**作者:**

Ping Zhang; Kai Niu; Xiaoyun Wang; Yiming Liu; Zijian Liang; Chen Dong

**期刊**：IEEE Communications Surveys & Tutorials

**发表时间： 10 September 2025**

**DOI:**10.1109/COMST.2025.3608174

IF:46.7(参考easy schalor)

**01**

**摘要**

通信和人工智能（AI）的融合正在改变下一代无线网络。受自然智能的启发，特别是在如何处理数据、信息和知识以进行认知、推理、学习、决策和环境交互方面，我们引入了一种称为ComAI的新范式。这种范式有望在未来的无线网络中发挥关键作用。

在本文中，我们强调了通信和人工智能融合背后的动机，并提出了一个路线图，概述了无线通信的演变以及人工智能的进步。

然后，我们介绍了 ComAI的关键思想，并给出了ComAI的总体框架，包括信息感知和数据收集、通过智能语义通信网络的信息认知和利用大规模模型的信息决策。

特别的，智能化语义通信网络是指利用语义级信息来简化和重构信号处理、信息认知和网络组织的智能和简洁的通信系统。我们进一步讨论了通信和人工智能融合的基础理论和关键技术。

此外，我们还提供了实验验证，包括来自6G测试网络的见解，并强调了潜在的应用场景，如嵌入式人工智能机器人和多智能体协作通信。

最后，我们概述了ComAI发展的未来方向和开放问题，分享了我们对潜在解决方案的想法和见解。

**02**

**内容提炼 - 动机与路线图-总体框架**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fbe1479c700d0f5429d5ea3b9d9b62e6a?Expires=1780065990&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=nD%2FuO77ls4WBXddU3Z5Mn1BOiCw%3D)

Fig. 1. The structure of the survey.

（1）动机与路线图

* **通信与AI的独立演进**：传统通信系统基于香农信息论，强调符号级传输可靠性；AI则关注数据处理、认知与决策。
* **融合的必要性**：6G及未来网络需支持智能体（如机器人、AI代理）之间的高效协作，传统通信方式难以满足语义级、任务导向的传输需求。
* **ComAI的提出**：提出“通信与AI融合”的新范式，强调语义通信、智能决策和系统级协同优化。

  ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fc1b4a23a7f76cc727f26d6a3f0fb573e?Expires=1780065990&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=hh8LbSAJK%2FjGFF1JddIfUwG0Az4%3D)

  Fig. 2. The roadmap of wireless communication.

  ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F466a3e9a6a9132e00e8cfdc4c83d93d6?Expires=1780065990&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=wL3AZAVeA7lIRKS5gdc7vCm4pt8%3D)

  Fig. 3. The roadmap of AI.

  ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fac44525f4b8c0163eb0ba8c59c5997f8?Expires=1780065990&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=CbRNeyQq1ugTdkcdQtO9%2BVDj3W4%3D)

  ![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F43edef8d1143707fe71a277deb45e5ba?Expires=1780065990&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=hY9q%2F0kK8aLXpNQ5xvV28t843HE%3D)

  Fig. 4. Different stages of the convergence of communications and artificial
  intelligence from the perspective of end-to-end wireless communication link

  designing: from separate optimization to
  convergence.（从端到端无线通信链路的角度来看，通信与人工智能融合的不同阶段设计：从独立优化到收敛。）

    AI在通信中的作用主要集中在利用AI或机器学习优化通信链路内的某些功能或模块，仍然依赖于复杂臃肿的传统网络和协议架构。

   
通信在AI中的作用是通过传统的符号级或分组级的传输方式消耗大量的通信带宽来弥补AI模型的弱点，如计算能力不足或绕过隐私限制，这种方式既不够有效，也不够灵活。

   
但是，面对面向未来的智能通信系统，通信和AI不应该作为插件互补。相反，它们应该相互融合，并有助于克服现有的缺点，包括在理论上解决基本的通信机制，打破模块、层和架构之间的限制以设计关键技术，并实现旨在成为更智能和自适应的网络生态系统的通信系统，即“ComAI”。

（2）ComAI的总体框架

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fe951ad1796dc3ddd120d6ab8c1e0b617?Expires=1780065990&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=oNSrwlLwAs6DpaEsTRdw%2Bbk8wYw%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F6263013a8dfa1062a0f8bd6cab01273c?Expires=1780065990&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=pFNo3%2BJ5Et3RlzgzhP7%2BWiZzDdw%3D)

Fig5. A General Framework of ComAI and its relationships with three levels of
the communication problems and natural
intelligence.(ComAI的总体框架及其与三个层面的沟通问题及自然智能之间的关系。)

 
  近年来，对语义通信的研究表明，通信方法的设计不能局限于A级的符号准确性，还可以关注B级的意义准确性和C级的效用有效性。当通信和人工智能的融合贯穿整个流程架构时，我们认为三阶段工作流自然与相应的三个层次的信息处理流，即句法、语义和语用，由浅入深：

句法：对于信息感知，在采集过程中，感知信息的符号能被感知到多准确？

语义学：对于信息认知来说，输入数据的意义在传递过程中能有多精确的认知？

语用学：对于信息决策，在推理过程中如何有效地决定来自接收意义的自然判断？

    ComAI框架主要包括三个处理步骤：信息感知和数据收集、具有可理解语义通信网络的信息认知和具有大规模模型的信息决策。此外，还包括短期/长期记忆和持续学习，以支持整体智能信息处理。

1. 通过数据收集进行信息感知：这一步与自然智能的“感知”过程相一致。未来，包括传感器和可穿戴设备在内的各种数据生成设备将持续监测和感知环境、社会和个人，将物理通过先进的传感技术将观测转化为数字数据。例如，移动人群感测利用诸如智能手机和可穿戴设备的移动IoT设备的能力来从传感器收集语法数据并将其传输到云/边缘服务器以经由通信网络进行进一步处理。数据收集的频率和方法至关重要，因为它们直接影响通信和人工智能中后续流程的性能。
2. 智能语义通信网络的信息认知：这一步符合自然智能的“认知”过程。所感测的语法数据经由无线或有线链路传输到数据接收器。利用智能语义通信网络，系统可以基于语义信息认知来处理、压缩和传输数据。ComAI不是专注于比特级或符号级的准确性，而是优先将内容含义传输到智能实体或不同人工智能代理之间，从而提高通信效率和有效性。此外，通过在各种复杂的通信场景中使用原生AI优化整体通信系统，科迈将实现系统级的“智能化”，带来通信性能的显著提升。
3. 大规模模型的信息决策：这一步符合自然智能的“决策”过程。接收到的语义信息由智能实体或AI代理进一步处理，以实现特定目标。这涉及分析上下文和用户意图以生成适当响应或动作的信息决策。通过利用大规模模型，ComAI增强了对复杂场景的理解能力，并做出更准确的决策。ComAI内部的这些模型还能够高效处理大数据量，促进跨各种场景的快速决策，从而拥有强大的务实级处理能力。
4. 短期/长期记忆和持续学习：这些组成部分对应于自然智能中的“记忆”和“学习”。它们作为智能信息处理的基础支撑，使ComAI在面对新场景或新信息时具有更强的自适应能力。通过利用短时记忆和自适应调整，智能化语义通信系统将具备为语义信息处理和更深层次的语义信息认知进行短期连续性预测的能力，从而赋予通信系统强大的适应性和自进化能力。此外，在长期记忆和持续学习的帮助下，大规模模型通过从现实世界中学习规则模式和新知识来维持高决策性能，从而实现持续的自我学习和进化。这些组件导致了一个反应更灵敏、更智能的系统，能够有效地满足不同用户或代理的需求。



ComAI的主要研究方向应集中在以下领域：

ComAI基础理论：从语义信息论入手，探索支持ComAI的基础理论，包括语义信息的核心思想、基本测度、编码定理和理论极限，为ComAI的进一步发展提供有效指导。

ComAI的关键技术：以AI和深度学习为切入点，研究智能语义通信的通用技术框架，包括点对点、多址、全双工场景的物理模型和传输机制，挖掘ComAI的性能潜力。

ComAI的验证和展望：针对现实世界的应用，应对现有解决方案进行真机性能验证，并探索潜在的应用场景，以研究ComAI框架的可扩展性和扩展潜力。

**03**

**基础理论和关键技术**

基础理论：语义信息论

突破香农理论限制：提出基于“同义性（Synonymity）”的语义信息论，解决语义不可见性与一对多映射问题；

三大语义编码定理：语义信源编码定理；语义信道编码定理；语义率失真编码定理；

核心度量：定义语义熵、语义互信息、语义信道容量等，建立语义通信的理论极限。

关键技术

> In this section, we introduce various key techniques for future ComAI systems,
> including two representation techniques—the Seb physical model and the SVI
> analysis framework—and three transmission techniques: NTSCC, MDMA,
>
> and SDD.

Seb 模型：语义表示的基本单位，类似“比特”，支持多模态数据；

SVI 框架：提供语义信息表示的理论优化方法；

NTSCC：实现端到端的语义压缩与传输，支持内容感知的动态带宽分配；

MDMA：利用语义模型区分用户，实现同频同时传输；

SDD：在全双工通信中利用语义差异抑制自干扰。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F709522723867c51c474aee78369169be?Expires=1780065990&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=RJCm%2BKwoI0LRgr3u9K%2Bz1PF9LCw%3D)

Fig. 9. The Technical Framework for ComAI

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F7cfe6ac2592813897d943a7456b7e6a3?Expires=1780065990&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=UW7%2Bh5GNvs553wz8boCETvQpC78%3D)

TABLE II 4SUMMARY OF THE KEY TECHNIQUES OF COMAI

**04**

实验验证&应用场景

实验验证

6G试验网平台：在工业巡检、视频传输等场景中验证语义通信的鲁棒性与有效性；相比传统通信，在压缩率、抗噪性、任务完成度上表现更优；

硬件部署：使用真实设备（如Nvidia Orin、YunSDR）验证语义通信系统的可实现性。

典型应用场景

具身智能机器人：机器人通过语义通信与云端大模型协同，实现人脸识别、动作预测与任务执行；

多智能体协同通信：在智慧港口等场景中，多个AI代理通过语义通信实现任务分配、协同搬运等集群智能行为。

**05**

未来方向和挑战

* ## 理论层面：

* 语义信息论与AI深度融合；

* 建立“语用信息论”以支持高阶决策；
* 重新审视AI辅助下的语义通信理论极限。
* 技术层面：

* AI模型的轻量化、可解释性、适应性；
* 多模态语义融合与实时处理；
* 多智能体系统中的安全与隐私问题；
* 与传统通信系统的兼容与协同设计。
* 实现层面

* 语义通信的标准化、协议设计；
* 建立语义级性能评估体系；
* 降低AI模型部署成本与能耗。

**06**

**结论**

在本文中，我们全面概述了通信和人工智能的融合，讨论了受自然智能启发的ComAI框架。

我们首先强调了这种融合的动机和意义，强调了它彻底改变未来无线网络的潜力。我们探索了ComAI的创新框架，包括信息感知和数据收集、智能语义通信网络的信息认知以及大规模模型的信息决策。

然后，我们讨论了支持这种融合的基础理论和关键技术，详细介绍了它们在推进ComAI系统中的作用。

此外，我们还展示了实验验证，如6G测试网络和语义卫星通信，说明了ComAI框架在现实场景中的实际应用和有效性。

最后，我们概述了ComAI发展需要解决的几个未来方向和开放问题。

欢迎查看其他文章~

[【论文】纯免费不限量的文档翻译（NEUer专属）](https://mp.weixin.qq.com/s?__biz=Mzk0ODU5ODQwOQ==&mid=2247489153&idx=1&sn=7115fc45dccb5aecc468be34f47cdb92&scene=21#wechat_redirect)

[【东北大学图标】制作东北大学PPT需要的素材](https://mp.weixin.qq.com/s?__biz=Mzk0ODU5ODQwOQ==&mid=2247489071&idx=1&sn=865a2320097bcf1b25e86c82fdee4de9&scene=21#wechat_redirect)

[【论文】实在不想读论文的时候可以试着碎片化AI阅读论文麻痹一下自己（教程贴）](https://mp.weixin.qq.com/s?__biz=Mzk0ODU5ODQwOQ==&mid=2247489038&idx=1&sn=59c324bf20509409c1ffe37bacd17804&scene=21#wechat_redirect)

[【论文】如何在图书馆找到你想了解的导师手下学生的毕业论文和研究方向+特色网络学术资源](https://mp.weixin.qq.com/s?__biz=Mzk0ODU5ODQwOQ==&mid=2247489029&idx=1&sn=ded8d48ebdaac684d33f63c601018d86&scene=21#wechat_redirect)

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 10:46*