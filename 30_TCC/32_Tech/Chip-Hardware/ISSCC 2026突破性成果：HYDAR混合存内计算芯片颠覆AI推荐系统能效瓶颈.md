---
title: "ISSCC 2026突破性成果：HYDAR混合存内计算芯片颠覆AI推荐系统能效瓶颈"
source: "https://mp.weixin.qq.com/s/wdR5XviiUtzCAOqsz8a3jw"
created: 2026-03-01
note_id: "1903039861062012456"
tags:
  - "AI链接笔记"
  - "ISSCC 2026"
  - "HYDAR芯片"
  - "混合存内计算"
  - "get-笔记"
  - "学术论文"
---

# ISSCC 2026突破性成果：HYDAR混合存内计算芯片颠覆AI推荐系统能效瓶颈

## 摘要

### **🏆 核心成果概述（背景）**  **ISSCC 2026发布** - **发布主体**：清华大学、华为与字节跳动联合团队。 - **核心论文**：《HYDAR: A Hybrid In-Memory Computing Framework for Efficient Recommenda

## 正文

电子发烧友网报道（文 / 吴子鹏）作为全球集成电路设计领域的顶级盛会，ISSCC 自 1953 年创办以来，一直是世界最前沿固态电路技术的首发阵地，被誉为 “芯片设计国际奥林匹克会议”。ISSCC 2026 上，清华大学、华为与字节跳动联合团队在会上发布论文《HYDAR: A Hybrid In-Memory Computing Framework for Efficient Recommendation System Acceleration》（HYDAR：面向高效推荐系统加速的混合存内计算框架），首次提出基于 28nm 工艺的混合存内计算（Compute-in-Memory, CiM）芯片，为 AI 推荐系统（RecSys）的能效瓶颈带来革命性突破。

这款芯片的核心突破在于，通过创新架构设计，将推荐系统核心运算的效率和能效提升 1–2 个数量级（QPS 提升 66 倍，QPS/W 提升 181 倍），为打破困扰行业多年的 “存储墙” 提供了全新路径。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F1f76133085234a82e3545a6eb1433166?Expires=1780059367&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=7%2FJTX8vjTQZUIOdoj%2FSimvlwSsQ%3D)

## **痛点攻坚：推荐系统硬件困局亟待破局**

在数字经济时代，推荐系统已成为连接用户与内容、产品的核心枢纽。无论是短视频分发、电商推荐还是智能搜索，背后都依赖海量用户行为数据的实时分析与精准匹配，而这一过程的核心运算单元是相似向量检索（SVS）—— 通过计算查询向量与大规模向量库之间的距离，检索出 Top-K 最邻近向量，进而实现个性化推荐。

然而，SVS 运算长期面临 “高耗低效” 的行业痛点。据联合团队论文披露，传统基于 CPU 或 GPU 的架构中，数据需要在处理器和内存之间频繁搬运，SVS 占据了推荐系统绝大部分的计算时间与功耗。核心症结在于外部存储器访问（EMA）的高昂开销：采用混合键合技术的 DRAM 加速器成本居高不下，难以大规模普及；基于 NAND TCAM 的加速器则存在读取延迟高、数据与距离表示精度有限等问题，无法满足实时推荐需求。

SVS 的现有困境，为新型计算架构的诞生留下了空间。

## **HYDAR 框架：三大创新协同破局**

HYDAR 芯片的创新之处，在于采用基于电阻式随机存储器（RRAM）的混合模数存内计算架构。与传统计算架构 “数据存储与计算分离” 不同，基于 RRAM 的存内计算（Compute-in-RRAM, CiR）将计算单元与存储单元深度融合，能最大限度减少数据移动，具备存储密度高、并行度极大的优势，被公认为深度学习加速极具前景的技术路线。

不过，在此之前将 CiR 应用于 SVS 仍面临多重挑战：随着向量库规模扩大，能耗与延迟会急剧增加，同时会降低处理单元（PE）利用率与吞吐量，还可能导致检索精度下降。如何解决这些矛盾，成为全球芯片设计领域的研究热点。

针对上述痛点，清华、华为、字节跳动联合团队提出的 HYDAR 框架，通过 “硬件架构 + 数据流调度 + 检索策略” 三维协同优化，成功实现了 CiR 技术在推荐系统加速器中的高效应用。基于该框架，团队采用 28nm 工艺流片实现了一款 CiR 原型芯片，包含 36M RRAM 单元，分为 16 个并行 PE，每个 PE 包含一个 288×4096 阵列。

根据论文，HYDAR 芯片集成三大核心技术以应对实际应用挑战：

动态延迟模数转换器（DL-ADC）：实现非 Top-K 计算的早期终止。在向量检索过程中，芯片能提前将计算出的距离与阈值比较，直接跳过不可能成为最优结果的向量，大幅降低不必要的计算延迟与功耗。

基于预测的预取调度流水线（PPSP）数据流：针对推荐系统中常见的非规则、动态变化的工作负载，该技术能智能预测数据访问模式、优化调度，显著提升系统吞吐量。

由粗到精（Coarse-to-Fine）检索架构：该设计在保证系统召回精度的前提下，实现检索任务的高效分层处理，使得系统能够轻松扩展至百万甚至更大规模的向量库，满足商业级推荐系统需求。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F168f74591a617bd30a294137d61450cd?Expires=1780059367&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=KmFSUsAv56WhDNosTCkVMsVQVC8%3D)

据联合团队在 ISSCC 2026 上披露的实测数据，这款基于 HYDAR 框架的 28nm CiR 芯片表现亮眼：单芯片可实现 390K QPS 的吞吐率与 1574K QPS/W 的能效比，其构建的多芯片系统可支撑百万级实时端到端推荐系统。在实际推荐系统任务中，当芯片扩展至 576M 规模的多芯片系统时，QPS 较传统方案提升 66 倍，QPS/W 提升 181 倍，而检索准确率与 CPU 方案相当，实现 “高效、节能、精准” 三重目标。

HYDAR 芯片的成功验证，不仅为推荐系统这一特定场景带来革命性的能效提升，其混合模数存内计算的设计思路更具普适意义。随着大模型向端侧部署、边缘计算需求爆发，对高能效、低延迟 AI 计算硬件的需求日益迫切。HYDAR 芯片能够以极低功耗，支撑电商、内容平台等所需的百万级实时端到端推荐系统，有望将相关数据中心的算力成本降低一个数量级。

## **未来展望：从存内计算到存内智能**

此次清华、华为、字节跳动的联合突破，不仅为推荐系统硬件加速提供全新路径，更对我国集成电路产业与 AI 生态发展具有深远意义。从技术层面看，该成果填补了存内计算技术在推荐系统专用加速器领域的空白，验证了 28nm 工艺下 CiR 技术的商业化可行性 ——28nm 工艺兼具性能与成本优势，相较于先进制程更易实现规模化量产，为后续技术落地奠定基础。

对于产业而言，HYDAR 框架的成功，为存内计算技术在特定应用领域的深化应用指明方向。未来发展趋势可能包括：

* 技术路径分化与融合：存内计算领域存在基于 SRAM 的极速能效路径与基于新兴存储（RRAM）的大容量端侧路径。HYDAR 代表了后者，未来两条路径可能在不同应用场景中各自发展，也可能出现融合架构。
* 从存内计算到存内智能：随着技术成熟，计算可能不再是 “存内计算”，而是 “存内智能”—— 存储器不仅是计算单元，更是智能决策单元。HYDAR 中的预测调度、自适应阈值等技术，已经展现出这种 “存内智能” 的雏形。
* 生态系统构建：技术突破需要配套的软件栈、开发工具和标准支持。未来可能出现针对存内计算架构优化的编程模型、算法库和开发框架，降低开发者使用门槛。
* 新材料新器件探索：RRAM 作为新型存储器件，其非线性等特性曾是应用障碍，HYDAR 通过补偿算法等克服了这些挑战。未来可能出现更适合存内计算的新材料新器件，进一步提升性能。

多位行业专家分析认为，随着存内计算技术不断成熟，其有望成为下一代 AI 硬件的核心架构之一。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F656a0b9f792617a99d1e34486f604b6a?Expires=1780059367&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=mpiM8Gf8apLZp4hZtW3QyfTjjJg%3D)

**声明**：本文由电子发烧友原创，转载请注明以上来源。如需入群交流，请添加微信elecfans999，投稿爆料采访需求，请发邮箱wuzipeng@elecfans.com。

**更多热点文章阅读**

* [数据中心HVDC
  2027年量产，线缆升级正在悄然爆发](https://mp.weixin.qq.com/s?__biz=MzY4OTA0MDQ5NQ==&mid=2247601736&idx=1&sn=133fe8923ddd9a2c7425b6f72099f101&scene=21#wechat_redirect)
* [AI时代算力瓶颈如何破？先进封装成半导体行业竞争新高地](https://mp.weixin.qq.com/s?__biz=MzY4OTA0MDQ5NQ==&mid=2247601735&idx=1&sn=5d8d58c0a79eb77f1c3c680bf03d0403&scene=21#wechat_redirect)
* [存储涨价冲击波：AMOLED面板三年首跌](https://mp.weixin.qq.com/s?__biz=MzY4OTA0MDQ5NQ==&mid=2247601734&idx=1&sn=0928caac937cebdf44033b828962429b&scene=21#wechat_redirect)
* [AI吊坠健康革命：情绪识别、饮食追踪，2026可穿戴新赛道开启](https://mp.weixin.qq.com/s?__biz=MzY4OTA0MDQ5NQ==&mid=2247601677&idx=1&sn=578348d0b1e35407907b59044eff7374&scene=21#wechat_redirect)
* [虚拟电厂有望成为未来太空电网核心](https://mp.weixin.qq.com/s?__biz=MzY4OTA0MDQ5NQ==&mid=2247601676&idx=1&sn=c164e5be1db3172a5dcd67b27575c939&scene=21#wechat_redirect)

**点击关注 星标我们**

将我们设为星标，不错过每一次更新！

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fb25a409867a8d8553e1c88e897d7a287?Expires=1780059367&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=R%2F7vW1IN3PWy6n7Mb5flmFxkTk8%3D)喜欢就奖励一个“在看”吧！

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 08:56*

## Related Notes

- [[AutoResearchClaw：全自动端到端AI科研智能体深度解析]]
- [[ClearSight: 基于事件相机与生物启发的运动去模糊研究]]
- [[ComAI：通信与人工智能融合的新范式研究]]
