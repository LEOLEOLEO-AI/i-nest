---
title: "华为网卡产品矩阵深度分析：从基础网络到DPU加速的技术演进"
source: "https://mp.weixin.qq.com/s/6iHyitjwSsEmI5UcaafaTw"
created: 2025-12-05
note_id: "1895033199134964288"
tags:
  - "AI链接笔记"
  - "华为网卡"
  - "DPU技术"
  - "Hi1822处理器"
  - "get-笔记"
  - "科技资讯"
---

# 华为网卡产品矩阵深度分析：从基础网络到DPU加速的技术演进

## 摘要

### **🔍 产品体系概览**  华为网卡产品分为四大类，覆盖从基础网络连接到高性能数据处理的全场景需求，核心技术依托**华为海思Hi1822处理器**，实现从PCIe 3.0到5.0、网络带宽从25G到200G的跨越。  ### **📌 四大产品类别技术参数对比**  #### **一、 SP6

## 正文

华为官网上的网卡

型号众多但是分为几大类

最基础款有SP600 系列标准网卡

> SP600系列是基于华为海思Hi1822网卡芯片开发的PCIe网卡，为服务器提供扩展的对外业务接口。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fcec10b1ec6ab25ac58d676052a1015d7?Expires=1780063518&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=M%2F9NlUo7St2JZEND7KlfG5DCCwQ%3D)

第二类是智能网卡

硬件升级为支持PCIe 5.0

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F516f01be79c298243d858e7415688ade?Expires=1780063518&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=E8uwatvPacBn4EnnS1jlPUI5WnA%3D)

第三类叫做互联网卡

追求高带宽开始引入200G接口

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fb74886b5ba4c9b80801a8858173a48cc?Expires=1780063518&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=AWtG5rG2YccscsyYBmU0hRNyZZ8%3D)

第四类卡叫做DPU卡

> SP900是面向云计算裸机和虚拟机部署场景推出的DPU（Data Processing
> Unit），同时支持存储卸载、网络卸载、管理面卸载，解决虚拟机场景遇到的软件生态问题。
>
> 通过在SP900上部署云计算存储、网络、管理软件及代理程序，向主机侧呈现了标准的VirtIO设备（virtual I/O
> device），彻底解决存储网络安全问题和虚拟机软件生态问题；同时通过卸载原来部署在主机侧的存储、网络和管理软件，降低了主机侧CPU占用，降低了总体部署成本。
>
> SP900适用于大数据加速、虚拟化加速场景。可以通过在SP900上部署其他软件实现更多的功能。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F8515ce3e9074b4b42e5dd52140254fd8?Expires=1780063518&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=FZPx83lVTQV6TiV2gQ3Oj8bcalQ%3D)

也许是24核不够震撼

某产品市场材料直接变成

4\*DPU (2048线程并行处理)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fef42abbf75dd716d855d94029557bce0?Expires=1780063518&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=WA0yqrQMs9lPuVnGuTTl4iCjC24%3D)

CloudMatrix 384老值钱了

所以论文中的Qingtian卡是SP925D吧

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F921147ebacc4e06278a588ce76c2e85b?Expires=1780063518&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=qj%2FZZLeTrtosdLH%2FjkmuUXW26JY%3D)

PCIe从3.0到5.0

网络带宽从25G到200G

华为海思Hi1822处理器还真神奇

所以网卡初创怎么跟？Forever Young？

从Fungible到Pensando，这是个好赛道吗

[ARM收购Dreambig，割袍断义还是投桃报李](https://mp.weixin.qq.com/s?__biz=MzIwNjI2MDU3OA==&mid=2650817781&idx=1&sn=e0d6afda9a67e5d74a85f8471488cfd2&scene=21#wechat_redirect)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F8a1f57f29ad611a90915038c8fb49852?Expires=1780063518&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=n0kcKHDGXYGIJSbx2%2B6PQkFGGiM%3D)

最后无奖问答

什么叫做“百度分流”

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F757a430d12fb9548ae9f7d3135528d2c?Expires=1780063518&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Y5UaskvaA0rqmeNd2G2PzdF0O68%3D)

相关资料移步汗牛充栋星球。

相关阅读：

# [P4可编程SDN交换机](https://mp.weixin.qq.com/s?__biz=MzIxODA5MzQ2MQ==&mid=2247483711&idx=1&sn=1b6a1ac88d03f3f461a8f9a7b224a08e&chksm=97ee83c5a0990ad37618b95ba91a26e66e09f1d1bb06a3379ad785a793094ce5802be3ddd8e7&scene=21#wechat_redirect)

# [P4教程](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzIwNjI2MDU3OA==&action=getalbum&album_id=1366109717906538497&token=1695902941&lang=zh_CN#wechat_redirect) [P4应用](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzIwNjI2MDU3OA==&action=getalbum&album_id=1366124433823449089#wechat_redirect) [P4论文](https://mp.weixin.qq.com/mp/appmsgalbum?__biz=MzIxODA5MzQ2MQ==&action=getalbum&album_id=2258770492021080069&scene=173&from_msgid=2247484125&from_itemidx=1&count=3&nolastread=1#wechat_redirect)

# [Tofino1](http://mp.weixin.qq.com/s?__biz=MzIxODA5MzQ2MQ==&mid=2247483711&idx=1&sn=1b6a1ac88d03f3f461a8f9a7b224a08e&chksm=97ee83c5a0990ad37618b95ba91a26e66e09f1d1bb06a3379ad785a793094ce5802be3ddd8e7&scene=21#wechat_redirect) | [Tifino 2](http://mp.weixin.qq.com/s?__biz=MzIxODA5MzQ2MQ==&mid=2247483866&idx=1&sn=7065b901434f919b48de11aad218d07a&chksm=97ee8320a0990a36024ff24557352152aab1491f2c8d22c51896faea077f3143e63fff7c4a5b&scene=21#wechat_redirect) |[国产P4交换机](https://mp.weixin.qq.com/s?__biz=MzIxODA5MzQ2MQ==&mid=2247484377&idx=1&sn=3da6b327a1f4e4a987ac26fb53e78649&scene=21#wechat_redirect)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Ff9b8f880021cbb3d5502ae2ec235fc54?Expires=1780063518&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=pOca2SHSBnsrw2xExGdvwydnHgk%3D)

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 10:05*

## Related Notes

- [[2028全球智能危机：人工智能引发的经济与制度冲击全景分析]]
- [[ClearSight：基于人类视觉启发的事件驱动运动去模糊研究]]
- [[DSPO：传感器位置与深度学习模型的双层可微分联合优化框架]]
