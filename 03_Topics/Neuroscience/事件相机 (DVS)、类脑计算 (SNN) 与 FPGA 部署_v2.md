# 事件相机 (DVS)、类脑计算 (SNN) 与 FPGA 部署

- **类型**: plain_text
- **时间**: 2025-10-10 22:57:09

## 内容

太好了 ✅ 那我就为你写一个 `README.md` **模板**，把整个 **DVS → SNN → FPGA Demo** 项目的安装步骤、依赖和运行方法整理出来。这样你或团队成员可以直接使用和分享。

---

# 📘 README.md 模板

```markdown
# DVS → SNN → FPGA Demo

本项目展示了如何从 **动态视觉传感器 (DVS)** 数据出发，训练 **脉冲神经网络 (SNN)**，并通过 **量化 + HLS 转换** 部署到 **FPGA** 上运行的完整流程。

---

## 📂 项目结构

```

dvs\_snn\_fpga\_demo/ ├── data/ # 数据集 (N-MNIST) ├── notebooks/ # Jupyter Notebook 实验 ├── src/ # Python 源码 (训练/量化/HLS 转换) ├── fpga/ # FPGA 工程 (HLS + Vivado) ├── tests/ # 单元测试 ├── run\_demo.sh # 一键运行脚本 └── README.md # 项目说明

````auto

---

## 🔧 环境依赖

- Python 3.8+
- PyTorch >= 1.10
- [SpikingJelly](https://spikingjelly.readthedocs.io/)
- [tonic](https://github.com/neuromorphs/tonic) (事件数据集工具)
- [hls4ml](https://fastmachinelearning.org/hls4ml/)
- Vivado 2020.2+ (Xilinx FPGA 工具链)

安装依赖：
```bash
pip install torch spikingjelly tonic hls4ml
````

---

## 📊 数据准备

下载 **N-MNIST 数据集**：

```bash
mkdir -p data
cd data
wget http://www.garrickorchard.com/datasets/n-mnist/NMNIST.zip
unzip NMNIST.zip
```

---

## 🚀 运行流程

### 1\. 训练 SNN

```bash
python src/train.py
```

输出：`snn_model.pth`

### 2\. 模型量化

```bash
python src/quantize.py
```

输出：`snn_model_quantized.pth`

### 3\. HLS 转换

```bash
python src/hls_convert.py
```

输出：`fpga/hls4ml_prj/`

### 4\. FPGA 部署

```bash
vivado -mode batch -source fpga/build.tcl
```

输出：`fpga/bitstream/snn_fpga_demo.bit`

### 5\. 一键运行

```bash
./run_demo.sh
```

---

## 📈 验证与测试

-   数据集：N-MNIST 测试集
    
-   指标：
    
    -   分类准确率
        
    -   推理延迟 (ms)
        
    -   每脉冲能耗 (pJ/spike)
        

---

## 📚 参考资源

-   [SpikingJelly 文档](https://spikingjelly.readthedocs.io/)
    
-   [tonic 数据集工具](https://github.com/neuromorphs/tonic)
    
-   [hls4ml 项目](https://github.com/fastmachinelearning/hls4ml)
    
-   [Xilinx FINN](https://github.com/Xilinx/finn)
    

---

## ✨ 致谢

本项目整合了 **事件相机 (DVS)**、**类脑计算 (SNN)** 与 **FPGA 部署** 的开源工具链，适合作为科研与教学的入门 Demo。

```auto

---

# ✅ 总结
这个 `README.md` 模板已经把 **依赖安装 → 数据准备 → 训练 → 量化 → HLS 转换 → FPGA 部署** 全流程写清楚了，你可以直接放到项目根目录，团队成员一看就能上手。  

要不要我再帮你写一个 **`tests/test_model.py` 单元测试模板**，用来快速验证训练好的 SNN 模型能否正确加载和推理？
```

好的 ✅ 我来帮你把之前所有的代码（训练、量化、HLS 转换、Vivado TCL、运行脚本、README）汇总成一个完整的文档，方便你保存和使用。你可以直接复制到一个文件里，作为项目的 **开发手册**。

---

# 📘 DVS → SNN → FPGA Demo 全流程代码文档

## 1\. `train.py` —— 训练 SNN 模型

```python
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
import tonic
import tonic.transforms as transforms
import spikingjelly.activation_based as sj

# 1. 数据加载
sensor_size = tonic.datasets.NMNIST.sensor_size
transform = transforms.ToFrame(sensor_size=sensor_size, n_time_bins=10)

trainset = tonic.datasets.NMNIST(save_to='./data', train=True, transform=transform)
testset = tonic.datasets.NMNIST(save_to='./data', train=False, transform=transform)

trainloader = DataLoader(trainset, batch_size=32, shuffle=True)
testloader = DataLoader(testset, batch_size=32, shuffle=False)

# 2. 定义模型
class SNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(34*34*2, 10, bias=False)
        self.lif = sj.neuron.LIFNode(surrogate_function=sj.surrogate.ATan())

    def forward(self, x):
        x = x.view(x.size(0), -1)
        x = self.fc(x)
        return self.lif(x)

net = SNN()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
net.to(device)

# 3. 训练配置
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(net.parameters(), lr=1e-3)

# 4. 训练循环
for epoch in range(5):
    net.train()
    for data, targets in trainloader:
        data, targets = data.to(device), targets.to(device)
        outputs = net(data)
        loss = criterion(outputs, targets)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")

# 5. 保存模型
torch.save(net.state_dict(), "snn_model.pth")
print("✅ 模型训练完成并保存为 snn_model.pth")
```

---

## 2\. `quantize.py` —— 模型量化

```python
import torch
import torch.quantization as tq
from train import SNN

# 1. 加载训练好的模型
net = SNN()
net.load_state_dict(torch.load("snn_model.pth"))
net.eval()

# 2. 配置量化
net.qconfig = tq.get_default_qat_qconfig('fbgemm')
print("✅ 使用 QAT 配置:", net.qconfig)

# 3. 准备量化模型
net_prepared = tq.prepare_qat(net, inplace=False)

# 4. （可选）继续训练以适应量化
# ...

# 5. 转换为量化模型
net_quantized = tq.convert(net_prepared.eval(), inplace=False)

# 6. 保存量化模型
torch.save(net_quantized.state_dict(), "snn_model_quantized.pth")
print("✅ 量化模型已保存为 snn_model_quantized.pth")
```

---

## 3\. `hls_convert.py` —— HLS 转换

```python
import torch
import hls4ml
from train import SNN

# 1. 加载量化后的模型
net = SNN()
net.load_state_dict(torch.load("snn_model_quantized.pth"))
net.eval()

# 2. 定义输入形状
input_shape = (1, 34*34*2)

# 3. 生成 hls4ml 配置
config = hls4ml.utils.config_from_pytorch_model(
    net,
    granularity='model',
    default_precision='ap_fixed<16,6>',
    input_shape=input_shape
)

# 4. 转换为 HLS 工程
hls_model = hls4ml.converters.convert_from_pytorch_model(
    net,
    hls_config=config,
    output_dir='hls4ml_prj',
    part='xc7z020clg400-1'  # FPGA 型号
)

# 5. 构建 HLS 工程
hls_model.build(csim=False, synth=True, cosim=False, validation=False)

print("✅ HLS 工程已生成，路径：hls4ml_prj/")
```

---

## 4\. `build.tcl` —— Vivado 自动化脚本

```tcl
set proj_name "snn_fpga_demo"
set proj_dir "./vivado_project"

create_project $proj_name $proj_dir -part xc7z020clg400-1 -force

add_files ./hls4ml_prj/myproject_prj/solution1/syn/verilog/*.v
add_files -fileset constrs_1 ./constraints.xdc

set_property top myproject [current_fileset]

launch_runs synth_1 -jobs 4
wait_on_run synth_1

launch_runs impl_1 -to_step write_bitstream -jobs 4
wait_on_run impl_1

write_bitstream -force ./fpga/bitstream/snn_fpga_demo.bit
write_hw_platform -fixed -include_bit -force ./fpga/bitstream/snn_fpga_demo.xsa

puts "✅ Bitstream 已生成，路径：./fpga/bitstream/snn_fpga_demo.bit"
```

---

## 5\. `run_demo.sh` —— 一键运行脚本

```bash
#!/bin/bash
set -e

echo "🚀 开始运行 DVS → SNN → FPGA Demo 流程"

echo "📌 Step 1: 训练 SNN 模型..."
python3 src/train.py

echo "📌 Step 2: 量化模型..."
python3 src/quantize.py

echo "📌 Step 3: 转换为 HLS 工程..."
python3 src/hls_convert.py

echo "📌 Step 4: 调用 Vivado 生成 bitstream..."
vivado -mode batch -source fpga/build.tcl

echo "✅ 全流程完成！bitstream 已生成在 ./fpga/bitstream/ 目录下"
```

---

## 6\. `README.md` —— 项目说明

````markdown
# DVS → SNN → FPGA Demo

本项目展示了如何从 **DVS 数据** 出发，训练 **SNN 模型**，并通过 **量化 + HLS 转换** 部署到 **FPGA**。

## 📂 项目结构
- src/train.py —— 训练 SNN
- src/quantize.py —— 模型量化
- src/hls_convert.py —— HLS 转换
- fpga/build.tcl —— Vivado 自动化脚本
- run_demo.sh —— 一键运行脚本

## 🔧 环境依赖
```bash
pip install torch spikingjelly tonic hls4ml
````

需要安装 Vivado 2020.2+。

## 🚀 运行流程

```bash
./run_demo.sh
```

## 📈 输出结果

-   `snn_model.pth` —— 训练好的模型
    
-   `snn_model_quantized.pth` —— 量化模型
    
-   `hls4ml_prj/` —— HLS 工程
    
-   `fpga/bitstream/snn_fpga_demo.bit` —— FPGA bitstream
    

```auto

---

# ✅ 总结
这份文档已经把 **训练 → 量化 → HLS 转换 → Vivado 部署 → 一键运行脚本 → README** 全部汇总在一起，你可以直接保存为 `DVS_SNN_FPGA_Demo_Doc.md`，作为完整的开发手册。  

要不要我帮你把这些代码再整理成一个 **压缩包目录结构清单**，让你可以直接生成一个项目骨架？
```

---
**Tags:** [[BrainInspired]]
