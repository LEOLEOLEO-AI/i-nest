---
title: 3 Tech-Trends brought about by Chiplet
tags:
- chip-hardware
- chiplet
- project
- semiconductor
- simulation
---
> 笔记本: 我的剪贴板  
> 创建时间: 2024-03-10  

---

# 
 

 

 
key words  

Jack Kilby, Integrated Circuits, Gordon Moore, Moore's Law, Exponential Curve, Homogeneous Integration, Heterogeneous Integration, Chiplet, System Space, Functional Density, 3 Tech-Trends, IP Chipletization, Integration Heterogeneity, IO Incrementalization, EDA tools.  
  
  
** **Preface** **  
On September 12, 1958, Jack Kilby invented Integrated Circuit.   
At that time, no one knew that this invention would bring such a big change to the human world.  
  
42 years later, Kilby won the 2000 Nobel Prize in Physics for his invention of Integrated Circuit.   
"Laid the foundation for modern information technology" was the pertinent evaluation given by Nobel Prize to Kilby.  
The progress of science and technology is often driven by a series of Great dreams, and Integrated Circuit is no exception.  
Kilby, a TI engineer who is two meters tall with gentle and steady personality, has a dream: "to make all the devices of circuits by silicon."  
Seven years after the invention of the integrated circuit, Intel founder Gordon Moore proposed his prophetic dream: "The number of devices on integrated circuit will double every eighteen months." This is what we know today as Moore's Law.   
  
Finally, they both realized their dreams and promoted great progress in science and technology. The combination of two great dreams also generated today's semiconductor industry.  
**"All devices can be integrated on one silicon chip, and the number of devices will grow exponentially." This is my summary of two great dreams. **  
Today, more than sixty years later, the development of the entire Integrated Circuit industry is still based on them!  
 
 From homogeneity to heterogeneity  
The development of things has its own process of emergence, development, maturity and end, and the same is true for the development of IC technology. 
Kilby once believed that making all the devices needed for a circuit in one material is the way to miniaturize circuits. Only one semiconductor material is needed to integrate all electronic devices. Today, we call it homogeneous integration. In this article, we focus on another technology: heterogeneous integration. 
First, let’s understand the development process from homogeneity to heterogeneity. 
Since Kilby, humans have been committed to producing all the devices needed for circuits on silicon chips. Driven by Moore's Law, the number of devices on silicon chips has increased exponentially. Today, the number of devices that can be integrated on a square millimeter of silicon easily exceeds 100 million, and mainstream chips integrate tens of billions of transistors. 
The development of homogeneous integration technology has become so mature that it will inevitably go through the process of ending. In the process of homogeneous integration gradually maturing and making it difficult to continue to develop, humans must find a new integration method to continue. This is Heterogeneous integration. 
There is a key concept that we need to understand in heterogeneous integration, which is Chiplet.  
Chiplet means small chip, which means cutting the existing large chip into small chips and then integrating them together in package.  
Why do we need to cut large chips into Chiplets? There are 3 tech-trends brought about by Chiplet technology that we will describe below. 
In addition to cutting large chips into chiplets, the number of devices on the chip is no longer growing exponentially, which means that Moore's Law will eventually come to the end.   
**I believes: "Devices will be integrated in multiple ways, and the function density within the System Space will continue to grow"** For details about the end of Moore's Law, system space, function density, etc., please refer to my book "MicroSystems Based on SiP Technology".  
 
The emergence of Chiplet technology has brought about new changes in chip design, which we briefly describe as: IP chipization, integration heterogeneity, and IO incrementalization, referred to as the  3 tech-trends.  
 Chiplet   
Chiplet, as the name suggests, is the small chip. We can think of it as a high-tech version of Lego bricks.   
First, complex functions are decomposed, and then a variety of "chips" (Chiplets) with a single specific function that can be modularly assembled are developed, such as data storage, calculation, signal processing, data management and other functions, and with this as a basis, establish a multi-chiplet integrated system.  
Chiplet technology is like building blocks, packaging some pre-produced chiplets that implement specific functions through advanced integration technology to form a Multi-die system, and these basic dies are Chiplets. 
Chiplets can be made using more reliable and cheaper technology. Smaller silicon chips are also inherently less prone to manufacturing defects. In addition, chiplets do not need to use the same process. Chiplets produced by different processes can be organically integrated through SiP technology. 
 
  
 Three Tech-Trends   
 1.  IP Chipletization  
IP (Intelligent Property) is also called IP core, the general term for integrated circuits with intellectual property. It is a macro module with specific functions that has been repeatedly verified and can be transplanted to different semiconductor processes.   
At SoC stage, IP core design has become an important task for ASIC design companies and FPGA providers, and it is also a reflection of their strength. For chip development software, the richer the IP cores it provides, the more convenient it is for users to design, and the higher its market share.   
At present, IP cores have become the basic unit of SoC system design and are exchanged, transferred and sold as independent design results.  
IP cores are divided into three categories corresponding to the different descriptions of functional behaviors, namely Soft IP Core, Firm IP Core and Hard IP Core.  
When the hard IP core is provided in the form of silicon chip, it becomes chiplet.  
 
We can understand Chiplet in this way: Chiplets in SiP correspond to the IP hard core in SoC. Chiplet is a new IP reuse mode, which is silicon chip level IP reuse.  
To design a SoC, the general method was to purchase some IP from different IP suppliers, soft core, form core or hard core, combine them with self-developed modules, integrate all of them into an SoC, and then complete it on a certain chip process node to complete the chip design and production.  
With chiplets, you no longer need to phurchase IP or design IP yourself. Instead, you only need to buy chiplets that have been implemented by others, and then integrate them in a package to form a SiP. So Chiplet can be seen as a hard IP core, but it is provided in the form of sililcon chip. Therefore, we call it IP chipletization. 
 2.  Integration heterogeneity  
Integration heterogeneity means Heterogeneous integration will become the mainstream integration. 
In the semiconductor area, Heterogeneous can be divided into two levels: HeteroStructure and HeteroMaterial. 
**HeteroStructure Integration** 
In this article, HeteroStructure Integration can also be called HeteroProcess Integration which mainly refers to packaging multiple chips manufactured separately by different processes into one package to enhance functionality and improve working performance. It can be manufactured by using different processes, different functions, and different manufacturers components and packaged together. 
 
For example, as shown in the figure above: 7nm, 10nm, 28nm, and 45nm chiplets are packaged together. 
Through HeteroStructure integration, engineers can assemble chiplets of different processes in SiP like building blocks. 
**HeteroMaterial Integration**  
CMOS and BiCMOS radio frequency technology has made huge progress in power in recent years, while also extending the frequency to about 100GHz. However, there are many applications that can only be realized using compound semiconductor technologies such as Indium Phosphide (InP) and Gallium Nitride (GaN). InP can provide transistors with a maximum frequency of 1 terahertz, high gain and high power, and ultra-high-speed mixed-signal circuits. GaN can enable devices with large bandwidth, high breakdown voltage, and output frequency up to 100GHZ.  
Therefore, integrating semiconductors of different materials into one, that is, HeteroMaterial Integration, can produce products with small size, good economy, high design flexibility, and better system performance. 
As shown in the figure below, chiplets produced and processed by Si, GaN, SiC, and InP are packaged together through heteroMaterial integration technology, forming a scenario where semiconductors of different materials work together in the same package.  
  
Integration of semiconductor devices (silicon and compound semiconductors) of different materials and passive components (including filters and antennas) on a single substrate is a common integration method in chiplet applications.  
Readers should note that the current multi-chip integration of different materials is mainly integrated on the substrate using a horizontal tiling method. For vertical stacking integration, the chips in the stack tend to be made of the same material, thus avoiding thermal expansion inconsistency and other issues, which influence the product reliability, as shown in the figure below.  
  
  
 3.  IO incrementalization  
If the previous 2 Tech-Trends are the advantages of Chiplet technology, then the incremental IO brings challenges to Chiplet. The  IO incrementalization is reflected in the horizontal interconnection (RDL) and also the vertical interconnection (TSV). 
In traditional packaging design, the number of IOs is generally controlled at hundreds or thousands. The bondwire process generally supports up to hundreds of IOs. When the number of IOs exceeds a thousand, the FlipChip process is often used. In chiplet design, the number of IOs may be as high as hundreds of thousands. Why is there such a large IO increase? 
We know that a PCB usually has no more than a few dozen external interfaces, a package has hundreds to thousands of external interfaces, and within a chip, the number of interconnections between transistors may be as high as billions to tens of billions.  
The deeper you go into the chip, the number of interconnections will increase dramatically. Chiplets are small chips cut from large chips, and there are naturally many interconnections between them.  
Often, the silicon interposer of a advanced package exceeds 100K+ TSV and 250K+ interconnections, which is unimaginable in traditional packaging design. 
Due to the IO increment, chiplet design also poses new challenges to EDA software. Chiplet technology requires EDA tools to provide comprehensive support from architecture exploration, chip design, physics and packaging implementation to provide intelligent and optimized solutions in each process. Assistance to avoid human-induced problems and errors. 
EDA companies such as Synopsys, Cadence and Siemens EDA have successively launched design simulation verification tools that support Chiplet integration. 
 Summary   
Starting from Kilby, after more than sixty years of development, homogeneous integration technology has become quite mature and is gradually reaching its extreme. At the same time, the exponential growth trend of Moore's Law is also unsustainable, and humans must find a new integration method to carry out continuation, this is heterogeneous integration.  
Heterogeneous integration allows function units to be integrated in system space in a more flexible way, and allows the function density of the system space to continue to grow, but this growth is no longer exponential. 
Heterogeneous integrated units can be called chiplets. Chiplet has brought new changes to the integrated circuit industry. This technology has both new advantages and new challenges. 
To sum up, the new changes that Chiplet brings to integration technology are: IP chipletization, Integration heterogeneity, IO incrementalization, which we call the 3 Tech-Trends brought about by Chiplet. 

 

 
  

 
 
 

 《基于SiP技术的微系统》内容涵盖“概念和技术”、“设计和仿真”、“项目和案例”三大部分，包含30章内容，总共约110万+字，1000+张插图，约650页。
 
 关注SiP、先进封装、微系统，以及产品小型化、低功耗、高性能等技术的读者推荐本书。 
 
   
    

 

 
  

 
 
 

The book "MicroSystem Based on SiP Technology" covers three parts: "Concept and Technology", "Design and Simulation", "Project and Case". It contains 30 chapters, with a total of about 1.1 million+ words, 1000+ illustrations, and about 890 pages.
 
This book is recommended for readers who are concerned about SiP, Advanced Packaging, Microsystem, and product miniaturization, low power consumption and high performance. 
 
   
    
Articles of the Author：

---
**Tags:** [[Chiplet]]
