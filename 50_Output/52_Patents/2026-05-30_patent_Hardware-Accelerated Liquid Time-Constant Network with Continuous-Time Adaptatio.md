---
title: "Hardware-Accelerated Liquid Time-Constant Network with Continuous-Time Adaptation"
date: 2026-05-30
channel: patent
status: ideation
tags: [patent, inest, liquid-neural-networks, efficient-ai, drone-navigation, edge-ai, neuromorphic, chiplet]
---

# Hardware-Accelerated Liquid Time-Constant Network with Continuous-Time Adaptation

## 技术领域

## 背景与问题

## 技术方案

### 核心创新点

### 与现有技术对比

## 权利要求草案

## 仿真/实验验证

## 商业化评估

## 行动清单
- [ ] 现有技术检索
- [ ] 创新点确认
- [ ] 权利要求细化
- [ ] 仿真验证
- [ ] 专利代理沟通

## 技术领域
Efficient online learning for spatiotemporal data on resource-constrained devices

## 核心创新
A hardware implementation of liquid neural networks where neuron time constants are realized by analog RC circuits or digital accumulators that adapt continuously based on input dynamics, enabling real-time learning and inference with minimal parameters and energy, suitable for drones and edge AI.

## 与现有技术区别
Existing liquid network implementations rely on software differential equation solvers or fixed-time-step digital approximations that lose the continuous-time adaptation property. This invention provides a direct physical embodiment of the liquid time-constant dynamics, allowing true continuous-time evolution and online adaptation without discretization artifacts, and achieves orders of magnitude lower power than GPU-based solutions.

## 可用仿真工具
- Loihi 2
- BrainChip Akida
- SpiNNaker2
- Nengo

## 权利要求草案
1. A neural network circuit comprising: a plurality of neuron units, each including an analog integrator with a tunable time constant; a synapse array that connects neuron units with configurable weights; and a control module that adjusts the time constant of each neuron unit in response to a measure of input variation, thereby implementing a liquid time-constant network in continuous time.
2. The circuit of claim 1, wherein the analog integrator is implemented using a programmable transconductance-capacitor (gm-C) filter, and the time constant is tuned by varying a bias current or a capacitor array.
3. A method for processing a temporal data stream using the circuit of claim 1, comprising: feeding the data stream as currents into the neuron units; allowing the network state to evolve continuously; and reading out the state at desired time points for classification or control, while the time constants adapt online to compress irrelevant input variations.
