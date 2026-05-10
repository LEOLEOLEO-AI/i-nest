# 液态神经网络LNNs是什么？又如何使用 PyTorch从零构建一个LNNs？

> 笔记本: 我的剪贴板  
> 创建时间: 2025-01-03  

---

原文链接: [https://mp.weixin.qq.com/s/sRyF3lY8LAuTj5GyyIAbcg?_refluxos=a10](https://mp.weixin.qq.com/s/sRyF3lY8LAuTj5GyyIAbcg?_refluxos=a10)


在过去35年里，科学家构建了一系列基于数据和可学习参数（θ）的概率模型，用于输出预测结果。
这些模型的核心组成部分是神经元，每个神经元都可以视为一个逻辑处理单元，它接收来自其他神经元的加权输入信号，并通过激活函数产生输出。
当我们将这种神经元机制与反向传播算法相结合时，就得到了神经网络。
反向传播算法是一种强大的训练技术，它根据神经网络的输出与期望输出之间的误差，通过逐层计算梯度来更新网络的权重和偏置。
这种能力使得神经网络能够从数据中自动学习并调整其参数，从而提高预测的准确性。
**不过神经网络也存在一些局限性：**


- 
它们在统一任务上表现良好，但无法跨任务泛化知识，即存在固化状态。
- 
它们非顺序地处理数据，在处理实时数据时效率不高
**解决方案：**“一种在工作中学习的神经网络，而不仅仅是在训练阶段。”
这就是我们所说的LNN——液态神经网络。
液态神经网络（LNN）是一种能够顺序处理数据并实时适应变化数据的神经网络，很像人类大脑的工作方式。

液态神经网络是一种时间连续的循环神经网络（RNN），能够顺序处理数据，保留过往输入的记忆，根据新输入调整行为，并且能够处理可变长度的输入，从而增强神经网络的任务理解能力。
其自适应特性使其能够持续学习和适应，最终在 **处理时间序列数据 **方面比传统神经网络更为有效。
连续时间神经网络是一种具有以下特性的神经网络ƒ：

如果ƒ对隐藏状态的导数进行参数化，我们就可以从离散计算图过渡到连续时间图。
这赋予了LNN以下两个特性：

- 
由于液态状态，可能函数的空间要大得多。
- 
任意时间步长的计算使LNN成为处理顺序数据的理想选择。
**为了让大家可以更系统的学习人工智能（机器学习深度学习），小墨学长为大家整理了一份60天入门人工智能（机器学习深度学习）的学习路线，**

**学习路线的资料都下载打包好了**
**大家可以添加任意一位小助手让她把学习路线的思维导图和相关资料一起发给你**

**LNN的优势**

- 
液态神经网络提供了许多核心优势，其中包括。
- 
实时决策能力。
- 
能够迅速响应各种数据分布。
- 
具有韧性，能够过滤掉异常或噪声数据。
- 
比黑箱机器学习算法更具可解释性。
- 
降低了计算成本。
**LNN的挑战**

虽然液态神经网络非常有用，但也有非常多的难点和挑战：

- 
难以处理静态或固定数据。
- 
由于梯度过高或消失导致的训练困难。
- 
由于梯度问题导致的学习长期依赖性的局限性。
- 
缺乏对液态神经网络工作原理的深入研究。
- 
耗时的参数调整过程。
- 
处理静态或固定数据的挑战。
**LNN与RNN有何不同？**
**神经元状态架构：**在液态状态机（LSM）中，循环连接是随机生成并固定的。输入信号被输入到这个随机连接的网络中，网络对这些输入的响应会进一步处理，以执行分类或预测等任务。
训练：RNN使用随时间反向传播算法（BPTT）进行训练，而LNN通常依赖于一种称为“水库计算”的无监督学习形式。
在这种方法中，循环连接（水库）是随机生成并保持固定的。
只有读出层（将水库的动态映射到所需输出）使用监督学习技术进行训练。这使得LSM的训练比RNN更简单。
**梯度消失问题：**由于LNN具有固定的循环连接，因此通常被认为对参数变化更具鲁棒性。
**应用：**RNN非常适合顺序建模，但LNN已知能够解决各种任务，包括语音识别、机器人控制和时序模式识别。
**灵感来源**
这个神经网络的灵感来自秀丽隐杆线虫，这是一种体长仅1毫米、拥有302个神经元的非常简单的小虫子，但它却有能力自主决策、探索世界。
LNNs的核心在于思维方式的根本转变——它摒弃了传统的纯算法式AI方法。
麻省理工学院（MIT）的几位研究人员研究了生物系统及其高效的决策过程，从智能的源头——灵活的神经元中汲取灵感。
正如我们大脑中的复杂神经网络在不断适应和进化，以动态和灵活的方式处理信息一样，LNNs通过融入神经生物学原理来模仿这种行为。
LNNs模仿线虫相互连接的电信号或冲动，以预测网络随时间的行为，表达任何给定时刻的系统状态。
通过模拟生物神经网络的适应性和响应性，LNNs具有独特的优势：能够按顺序处理数据，并实时适应变化的输入/权重。
这一能力在处理传统神经网络难以应对的场景时尤为宝贵，例如处理时间序列数据（如股票市场）或自动驾驶汽车捕获的长期依赖关系，以及应对快速变化的环境。
**PyTorch训练LNNs的分步指南**
**安装PyTorch：**


pip install torch

**导入必要的库：**


import torch  # 导入 PyTorch 库，主要用于深度学习
import torch.nn as nn  # 导入 PyTorch 的神经网络模块
import torch.optim as optim  # 导入 PyTorch 的优化器模块
import numpy as np  # 导入 NumPy 库，主要用于数值计算

# - torch 是 PyTorch 的核心库。
# - torch.nn 提供了构建和训练神经网络的模块。
# - torch.optim 包含常用的优化算法。
# - numpy 是一个强大的数学库，广泛用于科学计算。

**定义网络架构：**


import torch.nn as nn  # 导入 PyTorch 的神经网络模块

# 定义液态神经网络类，继承自 nn.Module
class LiquidNeuralNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers):
        """
        初始化液态神经网络
        :param input_size: 输入特征的维度
        :param hidden_size: 隐藏层的神经元数量
        :param num_layers: 网络中的层数
        """
        super(LiquidNeuralNetwork, self).__init__()  # 初始化父类 nn.Module
        self.hidden_size = hidden_size  # 保存隐藏层大小
        self.num_layers = num_layers  # 保存网络层数
        # 使用 nn.ModuleList 存储多个子层，每一层通过 _create_layer 方法创建
        self.layers = nn.ModuleList([self._create_layer(input_size, hidden_size) for _ in range(num_layers)])

    def _create_layer(self, input_size, hidden_size):
        """
        创建单个网络层，包含线性变换和激活函数
        :param input_size: 输入特征的维度
        :param hidden_size: 隐藏层的神经元数量
        :return: 一个 nn.Sequential，包含两层线性层和 LeakyReLU 激活函数
        """
        return nn.Sequential(
            nn.Linear(input_size, hidden_size),  # 线性变换层，输入到隐藏层
            nn.LeakyReLU(),  # 激活函数：LeakyReLU，用于处理非线性特性
            nn.Linear(hidden_size, hidden_size)  # 第二个线性变换层，隐藏层到隐藏层
        )

    def forward(self, x):
        """
        前向传播函数，定义输入数据如何通过网络传播
        :param x: 输入数据张量
        :return: 最终的输出张量
        """
        # 遍历所有子层，每层依次处理输入
        for i, layer in enumerate(self.layers):
            x = layer(x)  # 数据通过当前层
        return x  # 返回最后的输出


LNNs由一系列层组成，每一层都对输入应用一个非线性变换。
每一层的输出都会通过一个Leaky ReLU激活函数，这有助于在网络中引入非线性。
**实现ODE求解器：**
ODE求解器（Ordinary Differential Equation solver）负责根据输入数据更新网络的权重。你可以使用PyTorch的自动梯度（autograd）系统来实现ODE求解器。


import torch  # 导入 PyTorch 框架
import torch.nn as nn  # 导入 PyTorch 的神经网络模块

# 定义 ODE（常微分方程）求解器类，继承自 nn.Module
class ODESolver(nn.Module):
    def __init__(self, model, dt):
        """
        初始化 ODESolver 类
        :param model: 一个神经网络模型，提供用于逐层前向传播的层
        :param dt: 时间步长，用于时间序列处理
        """
        super(ODESolver, self).__init__()  # 初始化父类 nn.Module
        self.model = model  # 保存传入的神经网络模型
        self.dt = dt  # 保存时间步长

    def forward(self, x):
        """
        前向传播函数，定义输入数据如何通过模型传播
        :param x: 输入数据张量
        :return: 经过所有层处理后的输出张量
        """
        with torch.enable_grad():  # 启用梯度计算（用于反向传播）
            outputs = []  # 用于存储每一层的输出
            # 遍历模型的每一层，并逐层处理输入
            for i, layer in enumerate(self.model.layers):
                outputs.append(layer(x))  # 将当前层的输出添加到列表中
                x = outputs[-1]  # 更新输入为当前层的输出，传递到下一层
        return x  # 返回最终的输出

    def loss(self, x, t):
        """
        计算损失函数的方法（占位符，可以根据需求自定义）
        :param x: 输入数据张量
        :param t: 时间步长或目标值
        :return: 经过所有层处理后的输出张量
        """
        with torch.enable_grad():  # 启用梯度计算
            outputs = []  # 用于存储每一层的输出
            # 遍历模型的每一层，并逐层处理输入
            for i, layer in enumerate(self.model.layers):
                outputs.append(layer(x))  # 将当前层的输出添加到列表中
                x = outputs[-1]  # 更新输入为当前层的输出，传递到下一层
        return x  # 返回最终的输出


**定义训练循环：**
训练循环会根据输入数据和ODE求解器来更新网络的权重。


def train(model, dataset, optimizer, epochs, batch_size):
    """
    训练模型的函数
    :param model: 需要训练的神经网络模型
    :param dataset: 数据集，应该是可迭代对象，每个元素包含输入和标签（inputs, labels）
    :param optimizer: 优化器，用于更新模型参数
    :param epochs: 训练的总轮数
    :param batch_size: 每个批次的样本数
    """
    model.train()  # 将模型设置为训练模式，启用 dropout 和 batch normalization
    total_loss = 0  # 初始化总损失，用于记录训练期间的损失值
    for epoch in range(epochs):  # 遍历所有的训练轮次
        for batch in dataset:  # 遍历每个批次的数据
            inputs, labels = batch  # 获取输入数据（inputs）和对应标签（labels）
            optimizer.zero_grad()  # 清空优化器中存储的梯度，以准备计算新梯度
            outputs = model(inputs)  # 前向传播：将输入数据传递给模型，获得预测结果
            loss = model.loss(inputs, outputs)  # 计算损失值
            loss.backward()  # 反向传播：计算损失相对于模型参数的梯度
            optimizer.step()  # 优化：使用梯度更新模型参数
            total_loss += loss.item()  # 累积当前批次的损失值
        
        # 打印当前轮次的平均损失
        print(f'Epoch {epoch+1}, Loss: {total_loss / len(dataset)}')


另外我们打磨了一套基于数据与模型方法的 **AI科研入门学习方案**（已经迭代过 5 次），**包含时序、图结构、影像三大实验室，**我们会根据你的数据类型来选择合适的实验室，根据规划好的路线学习 **只需 5 个月左右**（很多同学通过学习已经发表了 sci 二区以下、ei 会议等级别论文）如果需要发高区也有其他形式。

**人工智能系统班学习路线**
**大家感兴趣可以直接添加小助手微信：ai0808q  通过后回复咨询既可！**


**大家想自学的我还给大家准备了一些机器学习、深度学习、神经网络资料大家可以看看以下文章（文章中提到的资料都打包好了，都可以直接添加小助手获取）**


**<**
** 人工智能资料分享 **
**>**


**时间序列学习仓库（点击图片即可跳转）**


**深度学习中文教程书（点击图片即可跳转）**


**神经网络学习资料****（点击图片即可跳转）**


**大家觉得这篇文章有帮助的话记得分享给你的死党**、**闺蜜**、同学、**朋友、**老师、敌蜜！


**B站：AI秃秃学长小墨**


**关注小墨**

**获取最新AI技能+最肝AI干货**

---
**Tags:** [[StrategicProposal]]
