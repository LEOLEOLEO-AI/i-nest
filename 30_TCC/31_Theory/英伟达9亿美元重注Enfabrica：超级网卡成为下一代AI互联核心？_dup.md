# 英伟达9亿美元重注Enfabrica：超级网卡成为下一代AI互联核心？

> 笔记本: 1.1 新导入  
> 创建时间: 2025-09-30  

---

# 
英伟达9亿美元重注Enfabrica：超级网卡成为下一代AI互联核心？

          

                                      原创
                                                      
                                      虎啸
                                  
                                      
                        
              [
                网络技术趋势洞察              ](#)
              
              

            
            
            
              *2025年09月30日 11:36*
              *江苏*
              
                            
            
            
          

          
          
          
            
              
              
            
              
              
                
              
            
          

          
          

          
                                        

          
                    

          
                    
                    
          
          
          
          
          
                                                            


英伟达近期对Enfabrica的9亿美元战略投资，标志着下一代互联技术已成为AI基础设施的关键战场。在该公司的产品矩阵中，3.2 Tbps的ACF（Accelerated Compute Fabric (ACF)-S超级网卡以其高度集成的芯片架构脱颖而出，技术实现远超英伟达自有的ConnectX-8系列。


与仅集成PCIe交换芯片的CX8（如上图所示）不同，ACF-S （如下图所示）在单芯片上融合了以太网交换（Packet Switch）与PCIe交换(Memory Switch)功能，形成一个高度集成的设备。这一设计显著增强了GPU横向和纵向扩展互联、内存解耦方面的能力。


### 一、核心应用场景

**1.内存解构**


在长上下文AI推理迈向百万令牌级别的进程中，KV缓存对GPU显存的巨大需求已成为制约性能与成本的根本性瓶颈。业界大模型开始探索分布式KV Cache池和分级Cache机制，比如Kimi的Mooncake架构（如上图所示）和SGLang的HiCache架构。
Enfabrica 的 EMFASYS（弹性内存架构系统）通过 ACF-S 高速互联协议构建基于 DDR 的设备级池化内存资源，实现了计算与内存的彻底解耦。该系统支持通过RDMA以太网访问的共享内存池架构，以模块化方式灵活扩展内存容量，为长上下文推理引擎提供了可线性扩展的内存资源池，显著降低了对高成本 GPU 或 HBM 的依赖。


****
**据 Enfabrica 宣称，EMFASYS 可为大规模推理负载扩展高达 18TB 的 DDR5 内存容量，并将单令牌生成成本降低多达 50%，从而在提升性能的同时优化了 AI 推理的总体经济效益。**
**2. 纵向扩展网络：从PCIe到以太网**
当前，国内多数GPU仍依赖PCIe构建纵向扩展（Scale-Up）网络，但PCIe交换芯片的带宽能力较以太网交换芯片低一个数量级，制约了系统规模的进一步扩展。
ACF-S通过实现PCIe至以太网的协议转换，有效解决了这一瓶颈：
- 
每个GPU通过PCIe接口直连ACF-S；
- 
数据流量在芯片内部转换为以太网报文；
- 
网卡提供4×800G以太网端口，支持多平面、高带宽的纵向扩展网络，具备负载均衡与冗余保护能力。
这一转换标志着纵向扩展网络从PCIe走向以太网已成为明确的技术趋势。
**3. 增强型横向扩展RNIC：集成PCIe交换能力**


在横向扩展（如上图所示）场景中，GPU通过PCIe交换芯片连接RNIC，RNIC连接到横向扩展网络。ACF-S作为集成PCIe交换功能的超级网卡，使CPU与GPU能够直接连接到该超级网卡，无需外置PCIe交换芯片（如下图所示）。


在跨节点All-to-All通信等场景中，现有架构需消耗GPU的流式多处理器即SM资源执行数据复制与转发（见下图，来自Insight into DeeSeek-V3论文，[DeepSeek-V3洞察论文个人解读](https://mp.weixin.qq.com/s?__biz=Mzk2NDMzODkxMA==&mid=2247483914&idx=1&sn=14ca4364ae4c9fe9790bb8e306f2de90&scene=21#wechat_redirect)，[DeepSeek最新论文深度解读 (续)](https://mp.weixin.qq.com/s?__biz=Mzk2NDMzODkxMA==&mid=2247483931&idx=1&sn=fda7415339a6ac5f941287f6548451a3&scene=21#wechat_redirect)）。此外，基于PTX的节点内跨轨道跳转同样需要消耗SM计算资源。


ACF-S设备内的网卡之间已实现以太互联，数据包可在NIC之间通过以太网交换芯片转发，上述在节点限制路由由SM执行的数据面转发任务可以完全卸载至ACF-S，无需消耗SM资源，从而显著提升通信效率。


### 二、ACF-S与英伟达CX8关键能力对比


### 从上图中可以发现，英伟达自家的CX8超级网卡也集成了PCIe Switch。但是，仍然沿用了之前在DGX H100/H200架构下的连接拓扑（如下图所示），即GPU以及NIC在PCIe Switch上并没有实现全互联，而是分为两个相对独立的连接拓扑。如此一来，要实现DeepSeek-V3的节点限制路由以及Rail-only组网下节点内的跨轨道中转，仍然需要消耗SM计算资源。相比较而言，ACF-S更胜一筹。


特性
Enfabrica ACF-S
英伟达CX8**集成架构**
以太网交换 + PCIe交换 + 网卡三合一
网卡 + PCIe交换**端口吞吐**
3.2 Tbps（可支持4×800G以太网）
800Gbps（支持单口和双口模式）**扩展支持**
统一平台支持纵向扩展、横向扩展及内存解耦场景
主要面向横向扩展场景**数据转发**
硬件卸载，几乎不消耗SM资源
依赖GPU SM参与数据复制与转发
### 三、结论

Enfabrica ACF-S代表了一类新型“超级网卡”，它在单一芯片上融合了纵向与横向扩展网络能力。通过集成以太网与PCIe交换功能，ACF-S实现了大规模KV缓存资源池、高效集成的PCIe转以太网纵向扩展网络模组。英伟达此次重金投资表明，此类融合互联架构将成为支撑下一代AI工作负载扩展的关键基石。
**四、参考连接:**
- 
https://www.servethehome.com/enfabrica-acf-s-a-huge-multi-tbps-supernic-at-hot-chips-2024/
- 
https://www.unite.ai/enfabrica-unveils-ethernet-based-memory-fabric-that-could-redefine-ai-inference-at-scale/
- 
https://www.servethehome.com/this-is-the-nvidia-mgx-pcie-switch-board-with-connectx-8-for-8x-pcie-gpu-servers/
- 
https://resources.nvidia.com/en-us-accelerated-networking-resource-library/connectx-datasheet-c
- 
https://www.servethehome.com/why-enfabrica-has-the-coolest-technology/
- 
https://arxiv.org/pdf/2407.00079
- 
https://developer.nvidia.com/blog/nvidia-connectx-8-supernics-advance-ai-platform-architecture-with-pcie-gen6-connectivity/
- 
https://lmsys.org/blog/2025-09-10-sglang-hicache/


- 

- 

- 


- 


- 


          
        
                        
                
        
  

 


 个人观点，仅供参考


        
        


                
              
    

    

    
    

      

        
        


​


      
    

    
    
  

  
  


  
  

    
    
  

    
    


    
    
    


    


  


,


选择留言身份

---
**Tags:** #NaaS
