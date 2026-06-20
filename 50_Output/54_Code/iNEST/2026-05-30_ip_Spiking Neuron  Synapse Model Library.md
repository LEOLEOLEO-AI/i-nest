---
title: "Spiking Neuron & Synapse Model Library"
date: 2026-05-30
channel: engineering
status: concept
tags: [engineering, ip, inest, spiking-neural-networks, neuron-models, synapse-models, simulation, cross-simulator]
---

# Spiking Neuron & Synapse Model Library

## 功能需求

## 技术架构

## 仿真工具链
- 工具: brian2, snntorch, nest-simulator

## 核心代码框架

## IP 封装方案

## 可复用性评估

## 开发计划
- [ ] 原型仿真
- [ ] 核心算法实现
- [ ] 接口定义
- [ ] IP 打包
- [ ] 文档与测试

## 用途
Provides a unified interface to a collection of biologically plausible neuron (LIF, Izhikevich, Hodgkin-Huxley) and synapse (static, STDP, conductance-based) models, enabling cross-simulator compatibility for iNEST neuromorphic engineering.

## 接口定义
Input: JSON/YAML model configuration (neuron type, parameters, connectivity). Output: spike trains (time, neuron ID), membrane potentials, synaptic currents as NumPy arrays or Pandas DataFrames.

## 复用场景
Rapid prototyping of custom spiking neural network architectures for sensory encoding, motor control, or cognitive tasks; benchmarking neuron models across simulators.

## 复杂度
medium
