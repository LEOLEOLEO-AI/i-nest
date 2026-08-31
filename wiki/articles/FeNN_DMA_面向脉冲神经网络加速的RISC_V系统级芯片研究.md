# FeNN-DMA：面向脉冲神经网络加速的RISC-V系统级芯片研究

**Domain**: iNEST
**Source**: 00_Inbox\01_GetNotes\FeNN-DMA：面向脉冲神经网络加速的RISC-V系统级芯片研究.md
**Compiled**: 2026-09-01

## Summary
title: "FeNN-DMA：面向脉冲神经网络加速的RISC-V系统级芯片研究" date: 2026-08-31 07:23 FeNN-DMA：面向脉冲神经网络加速的RISC-V系统级芯片研究 传统人工神经网络（ANN）依赖密集矩阵乘法，适合GPU/TPU等加速器处理。但**脉冲神经网络（SNN）** 采用事件驱动机制，神经元仅在达到阈值时发放"脉冲"，具有天然稀疏性和能效优势。其核心矛盾在于：**计算简单但数据搬运与稀疏事件处理复杂**，传统GPU/TPU难以高效支持。 现有SNN加速器存在三大局限：支持神经元模型简单（如LIF）、网络结构灵活性不足（难支持循环连接/突触延迟）、片上存储容量有限。FeNN-DMA旨在平衡**灵活性、容量与能效**，主要贡献包括：

## Keywords
SDI, SNN, iNEST, interconnect, neuromorphic, spiking, 神经形态

---
*Auto-compiled by wiki_compiler.py*


## Related Concepts

[[Event_Driven_Architecture]]
[[Neuromorphic_Computing]]
[[SDI_Bond]]
[[SNN]]
[[Spiking_Neural_Network]]
[[Synaptic_Plasticity]]
[[iNEST]]
[[神经网络]]
[[脉冲神经网络]]
