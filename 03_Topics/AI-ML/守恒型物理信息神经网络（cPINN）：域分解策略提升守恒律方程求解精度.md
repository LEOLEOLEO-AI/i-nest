---
title: "守恒型物理信息神经网络（cPINN）：域分解策略提升守恒律方程求解精度"
source: "https://mp.weixin.qq.com/s/6bOiZokOt1RvARuJcQb_Fw"
created: 2025-10-26
note_id: "1891323798016320360"
tags:
  - "AI链接笔记"
  - "守恒型物理信息神经网络"
  - "cPINN"
  - "域分解策略"
  - "get-笔记"
  - "AI研究"
---

# 守恒型物理信息神经网络（cPINN）：域分解策略提升守恒律方程求解精度

## 摘要

🔬 **研究背景与核心问题**   传统物理信息神经网络（PINNs）在求解守恒律方程时存在两大局限：   - **精度瓶颈**：面对激波、陡峭梯度等不连续解，误差常停留在10⁻⁵量级，难以突破   - **训练效率低**：单一网络覆盖全域，复杂区域与简单区域无法差异化适配，导致"大材小用"或"小马

## 正文

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F17c723df432fbc5eb74bcf67ded7f4b8?Expires=1780064943&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=ExqRNpDa5iMM0VZ4obAni6qtf08%3D)

**PINNs****｜精选 · 论文推荐**

AI for Science｜第二期

**守恒型物理信息神经网络****在离散域上的守恒定律：应用于正向和逆向问题**

Conservative physics-informed neural networks on discrete domains for
conservation laws: Applications to forward and inverse problems

**第一作者：Ameya D. Jagtapi**

**作者单位：**美国布朗大学应用数学系

Computer Methods in Applied Mechanics and Engineering

**论文主页：**

**https://www.sciencedirect.com/science/article/pii/S0045782520302127?via%3Dihub**

**论文｜PDF 下载 ↓**

**https://www.jianguoyun.com/p/DY2wPusQ7P3jDRj4s5UGIAA**

点击打印论文信息

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F57eebd54872766d45af10f4732d12861?Expires=1780064943&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=6VYgt6ThCiCeMVWfSUyk1HbjJl8%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fbf612be9540de8e1c05b633843e31cfb?Expires=1780064943&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=1DioRnTRpfL3148pujZWcIlEgkM%3D)

Published 2020-06

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F1934f1c1b64716367e2a473a26ae0623?Expires=1780064943&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=u5qdIjxO%2F0KtMzDANnd%2FYi%2BZYTQ%3D)

当PINNs遇到激波、不连续解等复杂守恒律问题时，单一神经网络往往力不从心。**布朗大学Jagtap团队在计算力学顶刊CMAME上提出的守恒型物理信息神经网络(cPINN)**，通过**域分解策略**让每个子区域使用专属网络，并在界面强制守恒量连续。这项研究不仅大幅提升了PINNs求解守恒律方程的精度，更为科学计算中的并行化和多尺度问题提供了新思路。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F04dc8c4c5a7c502c53958c5738c77a73?Expires=1780064943&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=0MRXCwEbOFwzzfPJDX6x5LGSCG0%3D)

**研究背景 · 问题意识**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fe3428cae870097a4257ac074fad9ef8f?Expires=1780064943&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Q%2BrQj71xajDQcfIMC5mUTy3g7rU%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064943&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=UykIRi6vGOkye2UgTK9Tftu2ERI%3D)

**研究背景**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064943&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=UykIRi6vGOkye2UgTK9Tftu2ERI%3D)

**守恒律**是自然界的基本规律，质量守恒、动量守恒、能量守恒支配着从流体流动到天气演变的一切过程。这些守恒律可以用偏微分方程(PDE)来描述，比如描述激波的Euler方程、描述流体的Navier-Stokes方程。**传统数值方法**虽然能求解，但面对复杂几何、多尺度现象时**计算成本极高**。

2019年Raissi提出的**物理信息神经网络(PINNs)**为PDE求解带来了革命性思路，但很快研究者发现了**两个****弱点**：

其一是**精度瓶颈**——对于陡峭梯度、激波等不连续解，单一神经网络难以准确捕捉，**误差往往停留在10⁻⁵量级**无法下降；

其二是**训练成本**——对于高维、长时间问题，全局网络的训练非常耗时，尤其是解在不同区域复杂度差异巨大时，全局统一的网络架构显得'**大材小用**'或'小马拉大车'。

更关键的是，PINNs虽然嵌入了物理方程，但对于守恒律这类特殊方程，并**没有显式保证守恒量(如通量)在空间中的连续性**。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064943&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=UykIRi6vGOkye2UgTK9Tftu2ERI%3D)

**问题意识**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064943&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=UykIRi6vGOkye2UgTK9Tftu2ERI%3D)

核心矛盾在于：物理问题往往具有区域异质性(如激波只在局部出现、边界层很薄)，但**PINNs用单一网络覆盖整个求解域**，无法灵活适配。研究团队的洞察是：能否借鉴传统数值方法中的**域分解思想**，将计算域拆成多个子域，**每个子域用独立的神经网络**，然后通过物理约束(守恒量连续性)把它们'缝合'起来？这就是cPINN的核心理念——**让AI学会'因地制宜'，在简单区域用浅网络快速求解，在复杂区域用深网络精细刻画。**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fd877e8b20294131bd43cd965723c3b3d?Expires=1780064943&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=iwo2vA7WK5PsuQozaNpANuvUhCk%3D)

**研究意义 · 方法论 · 创新点**

**研究意义**

cPINN首次将域分解与守恒量约束深度融合到PINNs框架中，为守恒律方程提供了精度更高、灵活性更强的求解范式。理论上，它通过在界面强制通量连续性，确保了**全局守恒性**这一物理本质；应用上，多网络架构天然**支持并行计算**，每个子域可以分配到不同计算节点，大幅降低训练时间。这为复杂工程问题(如高速流动、多相流)的实时预测提供了可行路径。

**方法论**

**① 域分解**：将计算域Ω分割成若干不重叠的子域Ω₁, Ω₂,
...，分割可以是规则的(如网格状)，也可以是不规则的(如沿激波位置划分)。关键是根据解的先验知识(如哪里有陡峭梯度)进行智能划分。

**②
子网络构建**：每个子域Ωᵢ配备独立的神经网络uᵢ(x,t;θᵢ)，网络的深度、宽度、激活函数都可以不同。比如在激波区域用6层深网络，在平滑区域用2层浅网络。研究团队还引入了自适应激活函数(在每层激活函数前乘以可学习的缩放因子)来加速收敛。

**③ 守恒约束缝合**：这是**cPINN的灵魂**。在相邻子域的公共界面上，必须满足两个条件——通量连续性(Flux
Continuity)和解的平均值匹配。具体来说，如果Ωᵢ和Ωⱼ相邻，在界面Γᵢⱼ上要强制：Fᵢ·n = Fⱼ·n(法向通量相等)，且(uᵢ + uⱼ)/2 =
界面值。前者保证守恒，后者加速收敛。

**④
联合优化**：损失函数包含三部分——初边值条件MSE、PDE残差MSE、界面条件MSE。关键是界面项的权重wᵢₙₜ可以调节，研究发现适当增大界面权重可以显著提升收敛速度。所有子网络参数{θ₁,
θ₂, ...}联合优化，但**每个子网络可以异步更新，天然支持并行**。

**创新点**

**①
物理驱动的域分解**：不是机械地均匀划分，而是根据守恒律的特点(如双曲方程沿特征线传播)和解的结构(如激波位置)进行自适应划分。在二维Burgers方程案例中，他们用不规则的三子域划分成功捕捉了斜激波；

**② 强形式界面约束**：传统有限元中的mortar方法用弱形式耦合，而cPINN直接在配点上强制通量相等，实现了真正的'点对点'守恒。这比vanilla
PINNs的全局残差最小化更符合守恒律本质；

**③异构网络架构**：在12子域的Navier-Stokes算例中，不同子域的网络层数从2层到6层不等，残差点数从200到10000不等。这种灵活性让网络能够'精准打击'复杂区域，避免过度参数化导致的过拟合和欠参数化导致的表达力不足；

**④ 并行友好设计**：子网络的部分独立性(只通过界面耦合)使得训练可以分布到多个GPU，每个负责一个子域。虽然论文中没有实现并行，但架构已经铺好了路。

**实验结果 · 研究结论 ·**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fc7fd7d55dbca025e0896d4023c5bb7e0?Expires=1780064943&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=tdmtLjN5F%2BzyAGEySLg83%2Fq6dzg%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064943&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=UykIRi6vGOkye2UgTK9Tftu2ERI%3D)

**实验结果**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064943&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=UykIRi6vGOkye2UgTK9Tftu2ERI%3D)

研究团队在六类经典守恒律问题上验证了cPINN的有效性，从一维到三维、从平滑解到不连续解、从正问题到逆问题全覆盖。

在**一维Burgers方程**(粘性系数0.01，陡峭冲击)中，4子域cPINN的相对L²误差在各子域均保持在0.005-0.06之间，而同参数量的单网络PINN误差高达0.15。强制界面平均值约束后，收敛速度提升约3倍。

在**KdV方程**(色散波传播)中对比最为惊艳：PINN完全失败(点误差达0.5以上)，而2子域cPINN准确捕捉所有色散波结构，点误差仅0.005。原因是cPINN在界面提供的额外通量信息起到了'中继站'作用，阻止了误差在全域扩散。

在**可压Euler方程**(马赫2斜激波)中，12子域均匀划分的密度场相对误差7.5%，而3子域沿激波方向不规则划分的误差降至0.8%——证明智能域分解比暴力堆子域更有效。

**逆问题**方面，在二维无粘Burgers方程中，cPINN从含1%噪声的数据成功识别出粘性系数μ(真值为0)，误差仅0.0002，而PINN在噪声下容易陷入局部最优。

所有算例均在单GPU上训练，迭代次数1.5万至50万不等，训练时间从几分钟到数小时。**相比传统谱方法，cPINN的优势在于无需网格生成、自动适配复杂几何****。**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064943&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=UykIRi6vGOkye2UgTK9Tftu2ERI%3D)

**研究结论**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064943&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=UykIRi6vGOkye2UgTK9Tftu2ERI%3D)

核心发现有三点：

第一，**域分解+守恒约束是破解PINNs精度瓶颈的有效策略**，尤其对于不连续解和多尺度问题。界面的通量连续性不仅是物理要求，更是阻断误差传播的'防火墙'。

第二，**子网络的异构性(不同架构、超参数)大幅提升了网络的表达能力和训练效率**。这印证了'No Free
Lunch'定理——没有单一最优网络，最好的策略是让问题本身决定网络结构。

第三，**强制界面平均值虽然在物理上不是必需的(对于连续解来说冗余)**，但在实践中起到了正则化作用，防止相邻子网络的预测'撕裂'。这揭示了数值稳定性与物理一致性的微妙平衡：有时'过度约束'反而有益。

研究还发现，**cPINN的误差来源**有三：近似误差(网络表达力)、泛化误差(配点分布)、优化误差(局部极小值)，它们在不同子域相互耦合。未来需要理论工具分析这种跨域误差传播机制。

**论文评价 · 未来展望**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064943&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=UykIRi6vGOkye2UgTK9Tftu2ERI%3D)

**领域贡献**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064943&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=UykIRi6vGOkye2UgTK9Tftu2ERI%3D)

这篇论文是**PINNs域分解方向的奠基之作**，引用量已近800余次，直接催生了XPINNs(时空域分解)、hp-VPINNs(变分域分解)等后续工作。

其**学术贡献**在于：证明了**守恒律**的特殊结构(通量形式)**可以显式编码到神经网络训练中**；提出了物理嵌入与域分解协同的新范式；为PINNs的并行化打开了大门。

**工程影响方面**，cPINN已被应用于航空航天(跨声速流动)、能源(多相流)、气候(海洋模拟)等领域。其灵活的多网络架构特别适合工业场景中'局部复杂、整体简单'的问题，可大幅降低计算成本。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064943&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=UykIRi6vGOkye2UgTK9Tftu2ERI%3D)

**局限不足**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064943&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=UykIRi6vGOkye2UgTK9Tftu2ERI%3D)

方法存在四个主要局限：

第一，**域分解策略仍依赖人工经验**，如何自动识别最优划分(子域数量、形状、界面位置)缺乏理论指导，目前只能靠试错；

第二，**界面权重的选择是敏感超参数**，设置不当会导致界面处振荡或收敛缓慢，需要针对不同方程精心调参；

第三，虽然架构支持并行，但**论文未实现真正的分布式训练**，通信开销和负载均衡问题尚未解决；

第四，**对于三维高雷诺数湍流等极端复杂问题，即使用cPINN仍面临维度灾难**——子域数量指数增长导致界面条件难以管理。此外，方法假设子域界面不随时间变化(欧拉网格)，对于运动边界、相变等拉格朗日问题需要进一步扩展。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064943&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=UykIRi6vGOkye2UgTK9Tftu2ERI%3D)

**未来方向**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064943&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=UykIRi6vGOkye2UgTK9Tftu2ERI%3D)

**①
自适应域分解算法**：开发基于残差估计的动态划分策略，训练过程中自动增删子域或调整界面位置，类似于传统数值方法中的自适应网格加密(AMR)技术，但完全数据驱动；

**② 分层域分解架构**：对于多尺度问题，设计粗细两层分解——粗层捕捉全局趋势，细层聚焦局部结构，类似多重网格法的思想，但用神经网络替代传统插值；

**③ 物理引导的元学习**：构建元网络来自动预测给定PDE的最优子域数、网络架构、界面权重，将cPINN的'艺术性'调参转化为可学习的策略；

**④
异步并行训练框架**：实现真正的分布式cPINN，每个子域在独立节点训练，通过梯度聚合或界面信息交换实现全局协调，挑战在于如何高效同步界面条件避免通信瓶颈。

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064943&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=UykIRi6vGOkye2UgTK9Tftu2ERI%3D)

**欢迎讨论**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Faca9df8d981a56796f63223fc492b77b?Expires=1780064943&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=UykIRi6vGOkye2UgTK9Tftu2ERI%3D)

如果你是PINNs研究者，cPINN的哪个创新点对你最有启发? **欢迎在****评论区分享你的观点！**

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2F04dc8c4c5a7c502c53958c5738c77a73?Expires=1780064943&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=0MRXCwEbOFwzzfPJDX6x5LGSCG0%3D)

![图片](https://get-notes.umiwi.com/morphling%2Fvoicenotes%2Fprod%2Fc5818a1fd7701f607c1df8634974c2e4?Expires=1780064943&OSSAccessKeyId=LTAI5t7toTp72R3TvdXf9QdK&Signature=Adj5jBuvB%2FwD0%2F3IH7qZYvJZGew%3D)

关注**智核学术｜**少走弯弯路

**↙↙↙  点击下方 “阅读原文”  查看相关论文合集**

---
*来源：Get笔记 | 类型：link | 入库：2026-04-29 10:29*

## Related Notes

- [[物理信息神经网络（PINNs）：深度学习与物理融合的开创性框架]]
- [[FMPINN：基于傅里叶的混合物理信息神经网络求解多尺度椭圆PDEs]]
- [[物理信息神经网络（PINNs）研究综述：从理论框架到科学计算革命]]
