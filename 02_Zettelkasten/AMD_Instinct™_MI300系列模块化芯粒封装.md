# AMD Instinct™ MI300系列模块化芯粒封装

> 笔记本: 我的剪贴板  
> 创建时间: 2024-06-10  

---

芝能智芯出品
随着超级计算（HPC）和人工智能（AI）领域的发展，对更高性能计算和数据处理能力的需求日益增长。AMD推出的Instinct™ MI300系列加速器应运而生，旨在通过最先进的硅片和封装技术，最大化地提升HPC和AI性能。
**AMD Instinct™ MI300系列包括两种主要型号：MI300X和MI300A。**
**● ****MI300X**是一个传统的CPU托管PCIe®设备，
**● **而**MI300A**则是一个自托管的加速处理单元（APU）。
这两种型号都利用了AMD的芯粒技术和先进的封装技术，实现了数据中心级CPU、GPU加速计算、AMD Infinity Cache和8层HBM3内存系统的首次集成。
**AI和HPC操作通常受到内存带宽的限制。**为了解决这一问题，MI300系列旨在提供超过5TBps的HBM3峰值带宽。MI300X特别适用于传统的双插槽CPU服务器，可以支持八个GPU加速器，适合大型模型的AI训练和推理。它基于第四代Infinity架构，将八个基于AMD CDNA™ 3架构的GPU芯粒连接到一个统一的AMD Infinity Cache中，保持硬件一致性。
 
 

 

 

 
**01** 
 

**自托管加速处理单元**    
MI300A则面向最高密度的HPC系统，结合了三个AMD“Zen 4”CPU芯粒和六个AMD CDNA 3 GPU芯粒，形成一个异构计算系统。
通过AMD Infinity Fabric网络芯片（NoC），它们共享一个统一的AMD Infinity Cache和HBM3 DRAM。这种设计消除了需要独立CPU插槽、DDR内存和CPU与GPU之间互连的需求，从而提高了功率效率，减少了GPU编程的开销，并实现了性能优化。
 
 

 

 

 
**02** 
 

**芯粒和封装技术**    
MI300系列采用先进的芯粒技术，引入了输入/输出芯粒（IOD）和加速器复合芯粒（XCD）。IOD包括HBM3内存控制器、AMD Infinity Fabric和Infinity Cache、IO子系统以及低功耗低延迟的芯粒间超短距离（USR）PHY。
 
XCD则实现了AMD CDNA 3架构中的新计算GPU层次结构，即加速器计算复合体（XCC）。
 
 
 

 

 

 
**03** 
 

**3D混合键合技术**    
MI300利用了3D混合键合技术，使多个顶部芯粒能够与大约半个掩模尺寸的基底芯粒进行混合键合。每个IOD包含超过35万个电源和信号通孔，总共有超过140万个混合键合连接。
通过这种技术，MI300不仅是AMD首个多芯粒混合键合架构，也是首个将3D和2.5D架构结合的产品，利用硅中介层实现IOD-IOD和IOD-HBM之间的微凸块连接。
 
 

 

 

 
**04** 
 

**高效的电源和时钟管理**    
为了提高功率效率和性能，MI300系列芯片设计了统一的TSV模式，能够提供超过1.5A/mm²的电力。此外，IOD微凸块模式还能够在硅中介层接口处同时向IOD逻辑部分提供超过0.5A/mm²的电力。所有四个IOD芯粒共享相同的参考时钟，通过基板分配。
 

 

**小结** 
**AMD Instinct™ MI300X加速器通过其先进的封装、工艺节点和芯粒技术，结合8层HBM3内存系统，提供了超过2.5倍的矩阵FMA FP16操作/时钟和1.5倍的HBM容量。MI300模块化芯粒封装使MI300A自托管APU和MI300X PCIe® OAM能够为下一代AMD HPC和AI平台提供强大动力。**
参考文献 
- 
B. Munger, et al., “Zen 4”: The AMD 5nm 5.7GHz x86-64 Microprocessor Core,” ISSCC, pp. 38-39, Feb. 2023. 
- 
4TH GEN AMD EPYCTM PROCESSOR ARCHITECTURE 
- 
S. Naffziger, “Pioneering Chiplet Technology and Design for the AMD EPYCTM and RyzenTM Processor Families: Industrial Product,” ACM/IEEE Int. Symp. Computer Architecture, pp. 57-70, 2021.  

## 

### 
  

##

---
**Tags:** [[Chiplet]]
