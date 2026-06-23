# 当神经网络遇见物理：PINN的原理应用及代码实现

> 笔记本: 我的剪贴板  
> 创建时间: 2025-09-27  

---

原文链接: [https://mp.weixin.qq.com/s/CzFfrFBOA7Ryfkp8Z1gYTA](https://mp.weixin.qq.com/s/CzFfrFBOA7Ryfkp8Z1gYTA)


在物理世界中，微分方程几乎无处不在。它们描述着流体如何运动，热量如何传递，材料如何变形。但遗憾的是，大多数微分方程很难有一个漂亮的解析解，所以通常不得不借助数值方法来进行计算。传统的数值方法（如有限元法、有限差分法、有限体积法等）虽然在求解偏微分方程（PDE）方面发展成熟，但其计算复杂度和计算资源消耗在处理高维问题或复杂几何时往往十分庞大。与此同时，深度学习在图像识别、自然语言处理等领域大放异彩，于是有人提出：**能否让神经网络来近似微分方程的解？**
****
然而，传统神经网络在处理科学计算问题时存在严重的问题：即**对物理规律的忽视**，仅仅依赖数据训练，无法保证预测结果符合基本物理定律。在这种背景下，PINN(物理信息神经网络Physics-Informed Neural Network)的概念被提出：PINN结合了**传统神经网络的函数逼近能力**与**物理定律约束**，**将已知的物理定律直接融入神经网络的训练过程，从而在训练时仍能保持对真实物理规律的遵循。其核心思想是：在训练神经网络时，不仅利用观测数据来计算误差，还通过引入物理定律的控制方程、边界条件和初始条件来构建物理约束，使神经网络的输出自动满足这些约束。**这一思想由 Raissi 等学者在 2017 年至2019 年间系统化提出，并迅速成为科学计算和工程仿真中的研究热点。

可以这样简单理解：传统神经网络像是一个只会死记硬背的学生，只要把数据给够，它就能记忆下来。但一旦遇到没学过的题目，就容易出错。PINN则更像一个既背了题库，又掌握了原理的学生——它在训练时必须同时通过“记忆考试”和“原理考试”。前者要求它拟合观测数据，后者要求它遵守物理定律。
**
PINN 将深度神经网络视为未知解的近似表示函数。其输入通常为时空坐标(x, y, z, t)，输出则对应于待求解的物理量（如速度场、温度场、压力场等）。在训练过程中，PINN 的损失函数通常由两部分构成：数据损失项与物理损失项**。
·**数据损失项** 用于衡量神经网络预测结果与观测数据之间的误差，从而保证模型在已知样本点上的拟合精度。
·**物理损失项** 则通过将网络输出代入控制系统的偏微分方程（PDE），并结合边界条件与初始条件进行约束。具体计算时，借助自动微分（Automatic Differentiation, AD）获取所需的偏导数，从而构造方程残差并量化其大小，以确保神经网络近似解满足底层物理规律。
通过同时最小化这两个损失项，PINN 能够在保持数据一致性的同时，遵循控制方程所蕴含的物理约束，从而得到更合理、更具泛化性的解。得益于此，PINN 在解决传统数值方法难以应对的问题时表现突出。PINN 已在流体力学、传热学、固体力学、量子力学、材料科学等多个领域得到应用，既能用于正问题的高精度求解，也能在反问题与参数辨识中展现独特优势。

接下来通过一个简单的传热案例案例来展示如何实现PINN算法。首先定义简单的神经网络结构和数据集类。


import torch
torch.manual_seed(42)

class Net(torch.nn.Module):

    def __init__(self, indim=1, outdim=1):
        super().__init__()
        self.actf = torch.tanh
        self.lin1 = torch.nn.Linear(indim, 100)
        self.lin2 = torch.nn.Linear(100, outdim)

    def forward(self, x):
        x = self.lin1(x)
        x = self.lin2(self.actf(x))
        return x.squeeze()


from torch.utils.data import Dataset, DataLoader

class MyDataset(Dataset):

    def __init__(self, in_tensor, out_tensor):
        self.inp = in_tensor
        self.out = out_tensor

    def __len__(self):
        return len(self.inp)

    def __getitem__(self, idx):
        return self.inp[idx], self.out[idx]

构建求解方程的精确解并可视化


import numpy as np
import matplotlib.pyplot as plt

def u(x, t):
    return np.exp(-2*np.pi*np.pi*t)*np.sin(np.pi*x)

pts = 200
ts = np.linspace(0.2, 0, pts)
xs = np.linspace(-5, 5, pts)

X, T = np.meshgrid(xs, ts)
U = u(X, T)

plt.imshow(U)
plt.colorbar()


准备PINN训练所需的数据集，并定义物理损失函数。


DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

train_in = torch.tensor([[x, t] for x, t in zip(X.flatten(), T.flatten())], dtype=torch.float32, requires_grad=True)
train_out = torch.tensor(u(X.flatten(), T.flatten()), dtype=torch.float32)

train_in.to(DEVICE)
train_out.to(DEVICE)

train_dataset = MyDataset(train_in, train_out)
train_dataloader = DataLoader(train_dataset, batch_size=256, shuffle=True)

def phys_loss(inp, out):
    dudt = torch.autograd.grad(out, inp, grad_outputs=torch.ones_like(out), create_graph=True, allow_unused=True)[0][:,[1]]
    dudx = torch.autograd.grad(out, inp, grad_outputs=torch.ones_like(out), create_graph=True, allow_unused=True)[0][:,[0]]
    d2udx2 = torch.autograd.grad(dudx, inp, grad_outputs=torch.ones_like(dudx), create_graph=True, allow_unused=True)[0][:,[0]]
    return torch.nn.MSELoss()(d2udx2, 0.5*dudt)

bdry_pts = 200
xs_bdry = np.linspace(-5, 5, bdry_pts)
ts_bdry = np.asarray([0 for x in xs_bdry])
us_bdry = u(xs_bdry, ts_bdry)

train_in_bd = torch.tensor([[x, t] for x, t in zip(xs_bdry, ts_bdry)], dtype=torch.float32, requires_grad=True)
train_out_bd = torch.tensor(us_bdry, dtype=torch.float32)

train_in_bd.to(DEVICE)
train_out_bd.to(DEVICE)

建立传统神经网络模型并进行训练，注意此时的损失函数中没有物理损失函数项。


from torch.optim import Adam, LBFGS
from torch.optim.lr_scheduler import LambdaLR
from torch.autograd import Variable
import torch

model = Net(indim=2, outdim=1).to(DEVICE)
epochs = 1000
optimizer = Adam(model.parameters(), lr=0.1)
scheduler = LambdaLR(
    optimizer=optimizer,
    lr_lambda=lambda epoch: 0.999**epoch,
    last_epoch=-1
)

loss_fcn = torch.nn.MSELoss()

for epoch in range(epochs):
    for batch_in, batch_out in train_dataloader:
        batch_in = Variable(batch_in.to(DEVICE), requires_grad=True)
        batch_out = batch_out.to(DEVICE)

        model.train()

        def closure():
            optimizer.zero_grad()
            loss = loss_fcn(model(batch_in), batch_out)
            loss.backward()
            return loss

        optimizer.step(closure)

    model.eval()
    train_in_dev = train_in.to(DEVICE)
    train_out_dev = train_out.to(DEVICE)
    train_in_bd_dev = train_in_bd.to(DEVICE)
    train_out_bd_dev = train_out_bd.to(DEVICE)

    base = loss_fcn(model(train_in_dev), train_out_dev)
    phys = phys_loss(train_in_dev, model(train_in_dev))
    bdry = loss_fcn(model(train_in_bd_dev), train_out_bd_dev)

    epoch_loss = base + phys + bdry
    print(f"Epoch: {epoch+1} | Loss: {base.item():.4f} | {phys.item():.4f} | {bdry.item():.4f}")

利用训练好的神经网络模型，预测解的情况，并将预测结果可视化。


def u_model(xs, ts):
    pts = torch.stack([xs, ts], dim=1).to(DEVICE)
    return model(pts)

pts = 200
ts = torch.linspace(0.2, 0, pts, device=DEVICE)
xs = torch.linspace(-5, 5, pts, device=DEVICE)
X, T = torch.meshgrid(xs, ts, indexing="ij")
X = X.T
T = T.T

img = []
for x, t in zip(X, T):
    img.append(u_model(x, t).detach().cpu().numpy().tolist())

plt.imshow(img)
plt.colorbar()


从上图中可见，传统的神经网络模型由于无法理解物理过程，仅仅是对数据的拟合，训练出的结果与精确解差距较大，且有些位置的结果不符合我们所定义的物理方程。接下来建立PINN模型再次进行训练，此时将在损失函数中加入物理损失项。训练完成后，使用PINN模型进行预测，并可视化。


model_pinn = Net(indim=2, outdim=1).to(DEVICE)
epochs = 1000
optimizer_pinn = Adam(model_pinn.parameters(), lr=0.1)
scheduler_pinn = LambdaLR(
    optimizer=optimizer_pinn,
    lr_lambda=lambda epoch: 0.999 ** epoch,
    last_epoch=-1
)

loss_fcn = torch.nn.MSELoss()

for epoch in range(epochs):
    for batch_in, batch_out in train_dataloader:
        batch_in = batch_in.to(DEVICE).requires_grad_(True)
        batch_out = batch_out.to(DEVICE)

        model_pinn.train()

        def closure():
            optimizer_pinn.zero_grad()
            loss = loss_fcn(model_pinn(batch_in), batch_out)
            loss += phys_loss(batch_in, model_pinn(batch_in))
            loss += loss_fcn(model_pinn(train_in_bd.to(DEVICE)), train_out_bd.to(DEVICE))

            loss.backward()
            return loss

        optimizer_pinn.step(closure)

    model_pinn.eval()
    train_in_dev = train_in.to(DEVICE)
    train_out_dev = train_out.to(DEVICE)
    train_in_bd_dev = train_in_bd.to(DEVICE)
    train_out_bd_dev = train_out_bd.to(DEVICE)

    base = loss_fcn(model_pinn(train_in_dev), train_out_dev)
    phys = phys_loss(train_in_dev, model_pinn(train_in_dev))
    bdry = loss_fcn(model_pinn(train_in_bd_dev), train_out_bd_dev)

    epoch_loss = base + phys + bdry
    print(
        f"Epoch: {epoch+1} | Loss: {epoch_loss.item():.4f} = "
        f"{base.item():.4f} + {phys.item():.4f} + {bdry.item():.4f}"
    )


def u_model_pinn(xs, ts):
    pts = torch.stack([xs, ts], dim=1).to(DEVICE)
    return model_pinn(pts)

pts = 200
ts = torch.linspace(0.2, 0, pts, device=DEVICE)
xs = torch.linspace(-5, 5, pts, device=DEVICE)
X, T = torch.meshgrid(xs, ts, indexing="ij")
X = X.T
T = T.T

img = []
for x, t in zip(X, T):
    img.append(u_model_pinn(x, t).detach().cpu().numpy().tolist())

plt.imshow(img)
plt.colorbar()


为了实现更好的精度，采用 **两阶段优化策略，先用 Adam 粗调，再用 LBFGS 精调，使模型在数据拟合、PDE 约束和边界条件之间取得平衡，并可视化结果。**


from torch.optim import Adam, LBFGS

model_pinn_v2 = Net(indim=2, outdim=1).to(DEVICE)
epochs_adam = 100
epochs_lbfgs = 30
optimizer_pinn_adam = Adam(model_pinn_v2.parameters(), lr=0.1)
optimizer_pinn_lbfgs = LBFGS(model_pinn_v2.parameters(), lr=0.01)

loss_fcn = torch.nn.MSELoss()

train_in = train_in.to(DEVICE)
train_out = train_out.to(DEVICE)
train_in_bd = train_in_bd.to(DEVICE)
train_out_bd = train_out_bd.to(DEVICE)

for epoch in range(0, epochs_adam + epochs_lbfgs):
    current_optimizer = optimizer_pinn_adam if epoch <= epochs_adam else optimizer_pinn_lbfgs
    for batch_in, batch_out in train_dataloader:

        batch_in = batch_in.to(DEVICE).requires_grad_(True)
        batch_out = batch_out.to(DEVICE)

        model_pinn_v2.train()

        def closure():
            current_optimizer.zero_grad()
            loss = loss_fcn(model_pinn_v2(batch_in), batch_out)
            loss += phys_loss(batch_in, model_pinn_v2(batch_in))
            loss += loss_fcn(model_pinn_v2(train_in_bd), train_out_bd)
            loss.backward()
            return loss

        current_optimizer.step(closure)

    model_pinn_v2.eval()

    base = loss_fcn(model_pinn_v2(train_in), train_out)
    phys = phys_loss(train_in, model_pinn_v2(train_in))
    bdry = loss_fcn(model_pinn_v2(train_in_bd), train_out_bd)
    epoch_loss = base + phys + bdry
    print(f'Epoch: {epoch+1} | Loss: {round(float(epoch_loss), 4)} = {round(float(base), 4)} + {round(float(phys), 4)} + {round(float(bdry), 4)}')


def u_model_pinn_v2(xs, ts):
    pts = torch.stack([xs, ts], dim=1).to(DEVICE)
    return model_pinn_v2(pts)

pts = 200
ts = torch.linspace(0.2, 0, pts, device=DEVICE)
xs = torch.linspace(-5, 5, pts, device=DEVICE)
X, T = torch.meshgrid(xs, ts, indexing="ij")
X = X.T
T = T.T

img = []
for x, t in zip(X, T):
    img.append(u_model_pinn_v2(x, t).detach().cpu().numpy().tolist())

plt.imshow(img)
plt.colorbar()

****
**以上内容只是对 PINN 的一个简要介绍。在写作过程中，我参考了许多文献和网络资料，也借助了 AI 工具。如今，AI 已经越来越多地融入人们的日常生活，数值仿真领域也不例外。各大仿真软件公司纷纷加大在 AI 项目的投入和布局，传统数值分析正逐步向 AI 驱动的方向演进，这一趋势已经十分明显。未来几年，AI 很可能会对传统的数值仿真模式产生巨大影响。但这并不意味着传统数值方法会被取代，二者各自都有独特的优势。可以预见，AI 与传统方法的结合将成为数值仿真领域的发展方向。希望我的文章能够对读者有所启发，让大家在学习传统数值方法的同时，也能了解并掌握一些 AI 的知识。**