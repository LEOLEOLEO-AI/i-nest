---
title: "2025 VLSI会议：AMD AI硬件平台架构趋势报告"
source: "https://mp.weixin.qq.com/s/Ea01mGKpgvSAPbVpwOLsuQ"
created: 2025-09-02
note_id: "1886318265962608184"
tags:
  - "AI链接笔记"
  - "AI硬件平台架构"
  - "UALink接口标准"
  - "加速器功率优化"
  - "get-笔记"
  - "会议记录"
---

# 2025 VLSI会议：AMD AI硬件平台架构趋势报告

## 摘要

### 一、AI硬件平台定义  🔍 **核心构成**   由前端数据中心网络、Scale-Out集群网络、Scale-Up Pod网络组成，包含CPU/GPU计算单元及DPU/RDMA NICs连接设备，实现存储与互联网连接。   ![AI硬件平台架构](https://get-notes.umiw

## 正文

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F9675699ca3656dba1ef41a4189cb7f75?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=7Srss%2FtbwVmMy2QT%2FbOGk8xbqmE%3D)

      该报告是2025年VLSI会议上AMD关于AI硬件平台的架构趋势的短课内容，作者为Norm James。

一、AI硬件平台定义

      AI硬件平台由前端数据中心网络、Scale-Out集群网络、Scale-Up
Pod网络等部分构成，包含CPU、GPU等计算单元，以及DPU、RDMA NICs等连接设备，实现与存储、其他系统及互联网等的连接。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F889867c7ccee75a3d206a9fc42d96af8?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=uTzbRS4mRV4O6OcDZ52xsYH2e9Q%3D)

二、AI平台接口

 

1. PCIe的作用与局限

      通用计算平台长期依赖PCIe连接设备与主机CPU，其带宽约每3年翻倍，但无法满足AI平台对更高带宽和更低延迟的需求，促使加速器设计者寻找替代接口。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F7f372b59082be65998d3a683cd2225c6?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=vboYR1%2F6XZvcQYZ%2FFbJtFqOLqsE%3D)

2. 其他接口

      包括Nvlink、INFINIBAND以及自定义接口等，用于满足不同场景下的连接需求。

3. 新的Scale-up接口（UALink）

     
由UALink联盟开发，旨在为AI加速器提供优化的Scale-up解决方案，具备固定负载、虚拟通道、低延迟等特性，支持数百个加速器在一个pod集群中，聚焦低延迟、高带宽等方面。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F0647074ffe72e4f2bf41153adda3f765?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=WpWADo7sDFrOZdDCmaDCepe9k28%3D)

三、加速器趋势

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fbcdbd34f243eb54006e8dac7a37b4111?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=n0BWRuS44oIioztpJlRUNH%2BSMdo%3D)

1. 功率不断增加，为在插槽内实现性能最大化，因为插槽内通信更高效，可处理更大工作负载。

2. I/O功率在总功率中的占比逐渐增大。

3. 封装内存容量不断提升，同时封装和电源解决方案占用空间更多。

四、Scale Up与Scale Out

1. Scale Up

      指加速器之间紧密耦合的互连，通常使用铜缆以降低成本和功耗，可直接连接或通过交换机连接，带宽高，域大小适中（<1000个节点），需先进行Scale
Up再进行Scale Out。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F9208cedb2611afa1f4e0683c057fbe3f?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=jcFRhGyoBVUV56IpbQNTUxvlG0c%3D)

2. Scale Out

      指更大的数据路径网络，通常使用传统网络适配器和交换机，短距离用铜缆，长距离用光纤，带宽中等，域大小大（数千个节点）。

3. 历史发展

      非加速服务器经历了从Scale Up到Scale Out的过渡，大型SMP系统构建复杂，后来将复杂性转移到应用程序以管理大量服务器。

五、Scale Up相关要点

1. 域大小与带宽

      AI平台需要更多功率、内存容量等，多种并行算法（如张量并行、管道并行、专家并行）都对高Scale
Up带宽有需求，接口速度不断提升以满足带宽需求，且希望使用无源铜缆以降低成本和功耗，目前尚未完成从Scale Up到Scale Out的过渡。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F30cf170a72b2c560703ff09d14a2deae?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=e6As39bQRdvnndJgGbkvd8BEdcg%3D)

2. 网络考虑

      Scale Out通常由PCIe连接的传统网络适配器提供，可能影响密度，与Scale Up的带宽比约为10:1，不同机架的Scale
Out交换机使用光收发器。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F0cb3edb3cb1f3c273e234f7e3232b5e5?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=ZNiJhbDJPGEMxUKVgdJo2mmx%2Bto%3D)

3. 互连与影响

      pod大小受铜缆传输距离限制，每个加速器需相互连接或与交换机连接，pod大小增大会增加物理分离；Scale Up
pod受复杂性、铜缆传输距离、封装密度等因素限制，可能需要液体冷却等特殊基础设施。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd452eae7b25ffb5f2746e087ab95e1b8?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=C1pF1CM5wZgabuLJrmKJMmoiKpw%3D)

六、高密度计算趋势及影响

1. 趋势

      AI集群的规模不断扩大，远超HPC超级计算机和大型机。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F4a203ddc59247fbcd074b2f1afb681ad?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=3bzxokxo69%2BYiuDEYBRzE74yzuI%3D)

2. 次要影响

      包括需要液体冷却以减小机箱尺寸，气流管理困难，维护性降低，以及液体冷却带来的泄漏控制和检测问题。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd67159ffcb9aa77bb93d24297f49e2ae?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=T%2FYfpyXgQJkBpw3qkVBh%2Ffvpl5E%3D)

3. 液体冷却

      HPC率先采用液体冷却，AI平台也逐渐更多地使用液体冷却，AI对功率的高需求推动流体温度降低，且液体冷却会增加组件拆卸难度。

七、铜互连与光学互连

1. 铜互连限制

      存在多种损耗，随着比特率增加，短距离将向光学过渡。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F67203f2c9692fbf2be4bc43d827fea15?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=FGmt8y2MzDfUx9LzhddbuOXdRTY%3D)

2. 光学互连

     
AI的发展推动光学互连的应用，预计在计算层面也将很快采用；但光学互连在短距离应用中面临冷却、硅封装尺寸、激光器可靠性和成本等挑战；同时，光学互连除了提供高带宽、低功耗解决方案，还能简化AI系统中的一些挑战，如允许降低密度等。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F4aa1c29768059eb6ccfb4b024b945a12?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=H71Q8AE4%2B17ej3lflNneNQid0N4%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F3ba5d310af2f53c48905d6f397feb642?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=89iptebwaJE9t0gYLBAsOByMyes%3D)

八、总结

1. 目前AI硬件平台主要推动高密度解决方案，以最小化铜互连长度。

2. 高密度平台带来了液体冷却等额外问题。

3. 未来若光学互连成本、功耗足够低且可靠性高，可能取代铜作为本地互连，此时密度的重要性将降低。

以下为完整Slides：

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F118d7658758e25c5204a7f93733de272?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=KZNyttWm9iEUMi7joSQQz7Xj0h4%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F2e2cac0b5a20ae5c59180e92523d9c11?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=QJzQu5UCVA6yOT6G6Zyi0HjWtFU%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F889867c7ccee75a3d206a9fc42d96af8?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=uTzbRS4mRV4O6OcDZ52xsYH2e9Q%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F59ea00f196c5db6dbb4b3744aa1deb6b?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Lo%2BCKLo6KAXS2CKsxsKnkwxEfAw%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F77c2c93aad015b98347153b205e0286c?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=8XC80dryGUvtATcYt86dNIphsOM%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F7f372b59082be65998d3a683cd2225c6?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=vboYR1%2F6XZvcQYZ%2FFbJtFqOLqsE%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F66ff94ea3d64bd51a80186903ab1f34d?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=s20qf05d1XKxNlrXERziTp1geLk%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F0647074ffe72e4f2bf41153adda3f765?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=WpWADo7sDFrOZdDCmaDCepe9k28%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fbcdbd34f243eb54006e8dac7a37b4111?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=n0BWRuS44oIioztpJlRUNH%2BSMdo%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F9208cedb2611afa1f4e0683c057fbe3f?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=jcFRhGyoBVUV56IpbQNTUxvlG0c%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F833187954e367959e7f6104207307310?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=JQ8EzIK2DEhEMHs69Y3lcywuvO4%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F3510b03887a16ecc5e94cfd3b607c4b9?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=VYoa1yXr6a0TfPa3wgqDWdQcjYQ%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F0cb3edb3cb1f3c273e234f7e3232b5e5?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=ZNiJhbDJPGEMxUKVgdJo2mmx%2Bto%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd452eae7b25ffb5f2746e087ab95e1b8?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=C1pF1CM5wZgabuLJrmKJMmoiKpw%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F30cf170a72b2c560703ff09d14a2deae?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=e6As39bQRdvnndJgGbkvd8BEdcg%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F4a203ddc59247fbcd074b2f1afb681ad?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=3bzxokxo69%2BYiuDEYBRzE74yzuI%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F6185793ae7984113ccba0431200b58ea?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=r0PaNpT%2FIZnSm5nrGlm1bTRHDL0%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fad5c04f318006f764468ea608e7a0678?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=3Z%2FxmbjmyMfX6p4jnhTgUH6Q1z4%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fcbb3045059e1f35e47db5ffdd208c63e?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Nf8cWly7HbZwhI7RBNrHSdr1zCs%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd67159ffcb9aa77bb93d24297f49e2ae?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=T%2FYfpyXgQJkBpw3qkVBh%2Ffvpl5E%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fb68e58d7ac1fd2e3e536c520522f7e93?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=lqJFLWW0%2B5X9JYhXj%2BYfvDil2Sg%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F67203f2c9692fbf2be4bc43d827fea15?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=FGmt8y2MzDfUx9LzhddbuOXdRTY%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F9028921c97c71d07cf88056d6e561cba?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=8Mge4XDdXfjufXPKHjUowhvCyRU%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fbf5cd03931742cc92986c7e2276bc9a2?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=uQA8EXSR5HZW00R9biW3v6PJzSQ%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F4e6105fb3fff8cc8cd05b759d89833f5?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Lljr%2FVaebBXYejgSQyaCvXxb1Ro%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F4aa1c29768059eb6ccfb4b024b945a12?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=H71Q8AE4%2B17ej3lflNneNQid0N4%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F3ba5d310af2f53c48905d6f397feb642?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=89iptebwaJE9t0gYLBAsOByMyes%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F5fcfb3a2148ca5471d6568f552eade6b?Expires=1780068069&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=211H9bwxFz%2FbnBiB7%2FDRvjgzEhE%3D)

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 11:21*