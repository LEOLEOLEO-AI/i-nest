---
category: Chip-Hardware
date: 2026-06-15 22:42
entities:
- PyTorch
- FPGA
- Tensil工具链
- NPU
- C语言驱动
- 脉动阵列
processed: '2026-06-16T00:41:31.247294'
score: 18
source: GetNotes
source_file: getnote_2026-06-15_PyTorch模型FPGA部署全流程_从训练到C语言驱动实现.md
summary: 从PyTorch训练到Tensil生成NPU，手写C驱动在FPGA上完成推理验证的完整指南。
tags:
- PyTorch
- chip
- design
- hardware
- fpga
- architecture
- semiconductor
- FPGA
- C语言驱动
- NPU
- 模型部署
- Tensil
- network
title: getnote_1912899989282157824_PyTorch模型FPGA部署全流程_从训练到C语言驱动实现
---

## Original Note

---
note_id: 1912899989282157824
title: "PyTorch模型FPGA部署全流程：从训练到C语言驱动实现"
type: link
created: 2026-06-15 20:35:43
source: getnote
kb: 
---

# PyTorch模型FPGA部署全流程：从训练到C语言驱动实现

### **📌 前言：AI模型部署的痛点与解决方案**

#### **(一) 行业痛点**
- **训练与部署割裂**：PyTorch教程侧重训练，FPGA教程聚焦基础硬件（点灯、UART），缺乏AI模型到FPGA的端到端指导。
- **工具链门槛高**：Tensil官方文档为英文，示例可复现性差，中间技术鸿沟无人填补。

#### **(二) 本文目标**

提供完整链路：**PyTorch训练→Tensil工具链生成NPU→手写C驱动→FPGA推理验证**，最终交付：
- 可运行的机器学习加速器原型
- 可复用的C语言驱动代码
- 全流程验证方法

### **🔍 核心价值：为什么选择手写C驱动？**

| 方案 | 优势 | 局限性 |
| :--- | :--- | :--- |
| **Python + PYNQ** | 开发速度快，适合快速验证 | 依赖Linux系统，无法用于嵌入式裸机场景 |
| **手写C驱动** | ✅ 支持嵌入式平台（STM32/RISC-V/Cortex-M）<br>✅ 无需操作系统，可运行于裸机<br>✅ 深入理解NPU硬件工作原理 | 开发周期较长，需硬件知识 |

### **📋 前置准备清单**

| 类别 | 具体要求 |
| :--- | :--- |
| **硬件** | ZCU102/ZCU104/VCU118或zynq7020等Tensil兼容FPGA开发板 |
| **软件** | Ubuntu 20.04/22.04、Vivado 2022.1+、Tensil工具链、PyTorch |
| **知识** | 基础Python、C语言、FPGA开发流程概念 |

### **🏗️ 第一部分：系统架构概览**

#### **1.1 整体架构**
- **核心组件**：Tensor Compute Unit (TCU) 包含指令解码器、内存控制器、SIMD寄存器、脉动阵列（Systolic Array）等模块。
- **存储架构**：
  - **DRAM0**：输入/输出数据存储
  - **DRAM1**：权重/常量存储
  - **Local Memory**：计算中间缓冲
  - **Accumulator Memory**：累加结果存储

#### **1.2 数据流全景**
1. 指令解码器解析控制指令 → 内存控制器管理数据访问
2. 权重从DRAM1加载至Local Memory → 输入数据从DRAM0加载至SIMD寄存器
3. 脉动阵列执行计算 → 结果存入Accumulator Memory
4. 最终输出写回DRAM0

### **🔧 第二部分：环境准备**

#### **2.1 版本确认**
- **硬件**：zynq7020开发板
- **软件**：Vivado 2017.4（Windows）、Ubuntu 22.04（Tensil编译环境）、PyTorch 2023.2.4（Professional Edition）

#### **2.2 Tensil工具链安装**
1. **获取代码**：
   ```bash
   wget https://github.com/tensil-ai/tensil-models/archive/main.tar.gz
   tar xf main.tar.gz && mv tensil-models-main models && rm main.tar.gz
   ```
2. **生成RTL代码**（NPU顶层模块TCU）：
   ```bash
   ./mill rtl.run -a ./arch/pynqz1.tarch -s true  # pynqz1.tarch为架构配置文件
   ```
3. **生成NPU指令与权重**：
   ```bash
   ./mill compiler.run -a ./arch/pynqz1.tarch -m ./models/cifar10.onnx -o "Identity:0" -s true
   ```
#### **2.3 Vivado工程创建**
- **芯片选型**：xc7z020clg400-2（Zynq-7000系列）
- **工程设置**：新建RTL项目，目标语言Verilog，仿真语言Mixed

### **🧠 第三部分：PyTorch模型训练与导出**

#### **3.1 网络定义**
- **架构**：3个卷积块（含BatchNorm、ReLU、MaxPool、Dropout）+ 分类器（全连接层+ReLU）
- **关键特性**：仅使用Tensil支持的ReLU激活函数，输入尺寸32×32×3（CIFAR-10数据集）

#### **3.2 训练结果**
- **训练周期**：50轮，最终测试准确率**84.63%**
- **损失曲线**：从初始Loss 2.3385降至最终0.2442

#### **3.3 ONNX导出**
```python
torch.onnx.export(
    model, dummy_input, "cifar10_tensil_model.onnx",
    opset_version=10,  # Tensil支持的最高版本
    input_names=['input'], output_names=['output'],
    dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}}
)
```
### **💻 第四部分：Tensil导入与NPU生成**

#### **4.1 模型编译关键参数**

| 参数 | 数值 | 含义 |
| :--- | :--- | :--- |
| **Data type** | FP16BP8 | 数据精度（16位浮点+8位定点） |
| **Array size** | 8 | 脉动阵列规模 |
| **MAC efficiency** | 50.995% | 乘加单元利用率 |
| **Execution latency** | 1.102 MCycles | 推理延迟 |

#### **4.2 架构配置文件**
```json
{
  "data_type": "FP16BP8",
  "array_size": 8,
  "dram0_depth": 1048576,
  "dram1_depth": 1048576,
  "local_depth": 16384,
  "accumulator_depth": 1024
}
```
#### **4.3 生成文件**
- **RTL代码**：top_tsr_model.v（顶层模块）、bram_dp_*.v（双端口RAM）
- **驱动参数**：architecture_params.h（C代码配置头文件）
- **模型文件**：*.tmodel（模型结构）、*.tprog（指令）、*.tdata（权重）

### **🔗 第五部分：在Vivado中集成NPU**

#### **5.1 IP核集成流程**
1. 添加Tensil生成的RTL文件 → 拖拽至IP Integrator生成NPU IP
2. 添加Zynq ARM核、DMA、AXI SmartConnect等外设IP
3. 配置时钟（50MHz以保证时序收敛）、复位信号及AXI接口连接

#### **5.2 比特流生成**
- **步骤**：Run Synthesis → Run Implementation → Generate Bitstream
- **资源占用**：LUT 53200、FF 106400、BRAMs 140、DSPs 220

### **📝 第六部分：C语言驱动编写**

#### **6.1 驱动工作流程**
1. **初始化**：tensil_driver_init() → 配置硬件寄存器
2. **模型加载**：tensil_driver_load_model() → 加载*.tmodel/*.tprog/*.tdata至NPU
3. **数据输入**：tensil_driver_load_model_input_scalars() → 写入输入数据至DRAM0
4. **推理执行**：tensil_driver_run() → 启动NPU并轮询状态寄存器
5. **结果读取**：tensil_driver_get_model_output_scalars() → 从DRAM0读取输出

#### **6.2 关键配置宏定义**
```c
#define TENSIL_ARCHITECTURE_ARRAY_SIZE 8          // 脉动阵列大小
#define TENSIL_ARCHITECTURE_DRAM0_DEPTH 2097152   // 输入/输出RAM深度
#define TENSIL_PLATFORM_PROG_BUFFER_BASE 0x00400000  // 指令缓冲区基地址
```
### **✅ 第七部分：FPGA部署与验证**

#### **7.1 文件系统移植**
- **xilffs模块**：用于SD卡挂载，加载测试图片与模型文件

#### **7.2 推理验证**
- **测试场景**：CIFAR-10数据集图片（马）推理
- **结果**：成功识别，输出符合预期

### **⚠️ 第八部分：踩坑记录**
1. **ONNX算子兼容性**：仅支持ReLU等基础算子，opset_version需设为10
2. **时序收敛问题**：NPU路径较长，时钟需限制在50MHz及以下
3. **文件系统依赖**：需移植xilffs以支持SD卡文件读取

---
*getnote | 2026-06-15 22:42*


---

## Related Notes

[[FPGA原型]]
[[iNEST-MOC]]
[[SDI化合物键_四型架构]]
[[paper1_iNEST_core_architecture]]