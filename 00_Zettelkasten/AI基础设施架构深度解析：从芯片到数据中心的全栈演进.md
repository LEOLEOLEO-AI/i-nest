---
title: "AI基础设施架构深度解析：从芯片到数据中心的全栈演进"
source: "https://mp.weixin.qq.com/s/35gAvAUyI6-hmdmn_sQahQ"
created: 2026-02-20
note_id: "1902227880314757728"
tags:
  - "AI链接笔记"
  - "AI基础设施架构"
  - "Scale-Up与Scale-Out"
  - "NVIDIA AI Factory"
  - "get-笔记"
  - "AI研究"
---

# AI基础设施架构深度解析：从芯片到数据中心的全栈演进

## 摘要

### **1. NVIDIA算力五层架构与AI Factory叙事**  #### **(一) 五层架构逻辑（Tokens TurnKey Solution）**  从单芯片到AI工厂的完整技术栈：**GPU→Die-to-Die→NVLink→NVSwitch→AI Factory**，实现AI

## 正文

1. NV算力五层架构/叙事逻辑（Tokens TurnKey
Solution）：从单芯片到AI工厂，GPU→Die-to-Die→NVLink→NVSwitch→AI Factory，AI基础设施“吃干抹净”。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F3fbaaddc9a71065094f4c8da90a6642d?Expires=1780060037&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=SL9M3%2BF2hOolTHtoTO6LydxCnZ0%3D)

AI Factory是Nvidia从“芯片提供商”到“AI基础设施提供者”的新叙事。 Nvidia正试图通过AI
Factory，将其角色从提供算力武器的供应商，转变为定义和运营智能时代核心基础设施的“能源公司”。以数据和电力为原料，高效生产智能能力“Token”，持续提升智能生产效率（Tokens/Dollar,
Tokens/Watt）。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ff367859d4bf977d0bcd72b4256173e28?Expires=1780060037&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=x2up2po%2BQdxpFV6DEDGfBoOAcuE%3D)

2. Google：Scale up与Scale out

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F087eb770b2c70a4478df5449a52c53c9?Expires=1780060037&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=%2FoDu2XmEwhCnFQbD0DSNqQOb18k%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fff2db85f37382c39a8ce8f20ea478aa2?Expires=1780060037&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=3p42b5drAKkujrms6nmKXnrMw%2Bc%3D)

3. Broadcom - Enabling AI Infrastructure

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ffeadf62f74247c79c69a97614a824841?Expires=1780060037&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=ZKLixE3JtNBhQDGORSdH%2F05J1HI%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ff261ec2f0e8035d0321273c1d198f8c7?Expires=1780060037&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=bXwIxqx8%2BmaC0jEAH%2FlUfK%2Bxh5Q%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fe647b4a99635206b81eacd96fea235f6?Expires=1780060037&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=6kEOSYZY9AWrCnPv99urb2U%2F0uA%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fe37eb9749b1d58da2f2c5f8ac1c0965f?Expires=1780060037&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=GGN28DWYnfc%2B3hiHqdcFU%2Fca6qQ%3D)

4. AMD likeAs NV AI Foundation

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fb8e21aa4fb53abf997bdfce6471bb6fc?Expires=1780060037&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=kCSnulIeW1eG%2BbzJx2330X2ymbI%3D)

5. Marvell定义的前端网络、后端网络、计算节点

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F5091d2a6e786fdd3ad84c6acf662cdb3?Expires=1780060037&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=wjA9FouxGXnH08JPUisHysUE4%2BE%3D)

6. Cisco （BRKDCN-2921）Fabric Network

AI 工厂网络由三个特殊的网络组成：

* 南北向矩阵，专用于用户和存储访问
* Scale-Up Fabric，利用 NVIDIA 的 NVLink 将多个 GPU 连接在一起的网络
* 东西向 Scale-Out Fabric，横向水平扩展到数千颗 GPU 的相互连接的网络

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fb6f9e7a75945f1c739903f194c71f3f1?Expires=1780060037&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=q12pteXwpyqQ1EFBayN2jVdpWpQ%3D)

显然南北向矩阵对应的就是图上的 Front-End，绿色的Back End部分对应的则是东西向 Scale-Out。

=======================================================

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd9ffd25839d0fb52063f85941b4ea8a4?Expires=1780060037&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=YNtej%2BafYKsWTwRWlP9ckRv22oI%3D)

===========================================================

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 09:07*