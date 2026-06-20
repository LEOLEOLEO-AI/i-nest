---
title: "Software-Defined Wafer-Scale Neuromorphic Computing Platform for Edge AI"
date: 2026-05-30
channel: project
status: planning
tags: [project, inest, project-proposal]
---

# Software-Defined Wafer-Scale Neuromorphic Computing Platform for Edge AI

## 背景与动机

## 研究现状

## 技术路线

## 里程碑

## 资源需求

## 风险评估

## 产出预期
- 论文: 
- 专利: 
- 工程IP: 
- 项目指南: 

## 执行计划
- [ ] 调研阶段
- [ ] 方案设计
- [ ] 原型验证
- [ ] 正式立项
- [ ] 阶段交付

## 背景
Edge AI applications demand ultra-low latency, high energy efficiency, and adaptability. Traditional architectures face memory wall and scalability limits. The NICE framework and SDSoW paradigm enable reconfigurable wafer-scale integration of neuromorphic cores, overcoming interconnect bottlenecks and enabling dynamic resource allocation. This project aims to build a prototype SDSoW-based neuromorphic platform that can be software-defined for diverse edge workloads, from autonomous sensing to on-device learning.

## 目标
['Design a wafer-scale neuromorphic fabric with software-defined routing and processing elements based on the NICE architecture.', 'Implement a complexity-aware mapping framework that partitions spiking neural networks across chiplets using the mesoscopic complexity threshold theory.', 'Demonstrate >10x energy efficiency improvement over GPU/TPU edge solutions on representative benchmarks (DVS gesture, keyword spotting).', 'Develop a complete software stack (compiler, runtime, simulator) for the platform.']

## 时间线
{'Q1': 'Architecture specification and simulation model; tape-out of test chiplet with 4 neuromorphic cores.', 'Q2': 'Chiplet fabrication and testing; wafer-scale integration design (interposer, power delivery); initial compiler framework.', 'Q3': 'Wafer-scale prototype assembly (4 full-reticle wafers); bring-up and validation of inter-chiplet communication; runtime system development.', 'Q4': 'System optimization; benchmark evaluation; demonstration of software-defined reconfiguration; deliver final SDK and hardware prototype.'}

## 里程碑
- M1 (Q1): Test chiplet functional at 200 MHz, power <2 W.
- M2 (Q2): Inter-chiplet link BER <1e-12 at 16 Gbps/lane.
- M3 (Q3): Full wafer-scale system boots and runs 1000-neuron SNN.
- M4 (Q4): End-to-end keyword spotting at <10 mW, latency <5 ms.

## 交付物
- 论文: 0
- 专利: 0
- 工程IP: 0

## 预算
¥18,000,000 (RMB) over 1 year, including: chip fabrication (MPW + wafer-scale) ¥8M, equipment ¥3M, personnel ¥5M, software/EDA ¥2M.

## 团队需求
['1 Principal Investigator (neuromorphic computing/architecture)', '2 Postdoctoral Researchers (chip design, software stack)', '4 PhD Students (circuit design, compiler, benchmarking, system integration)', '2 Senior Engineers (analog/mixed-signal, packaging)', '1 Project Manager']
