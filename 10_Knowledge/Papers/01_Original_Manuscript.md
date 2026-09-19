# 第一章　绪论：从算力堆砌到复杂度涌现

> *"Intelligence is not a property of individual neurons but an emergent property of networks. The question is not how much computation a node can carry, but how the collective spatiotemporal complexity of the network crosses critical thresholds to produce perception, reaction, adaptation, creation, generality and superintelligence."*
>
> ------本卷核心假说陈述（作者综合 Langton 混沌边缘论断［10］、O'Byrne--Jerbi 大脑临界性争论［29］、Friston 自由能原理［45\]\[46］提出）

**核心命题：**　智能的本质来源是网络时空协同复杂度，而非节点算力；复杂度越过相继阈值时涌现感知、反应、适应、创造、通用、超级六个等级的智能。本章 1.1 诊断深度学习"算力堆砌"路线的物理极限，1.2 梳理复杂性科学、脑神经科学、计算机科学与机器人工程的交叉学术渊源，1.3 给出网络时空协同复杂度与智能等级的核心假说，1.4 说明晶圆级/晶矩异构异质集成与自演化互连（SEI）的技术路线，1.5 给出全卷结构与阅读导引。

## 1.1　问题的提出：深度学习的算力堆砌路线与其物理极限

**算力堆砌的工程胜利与理论贫困。**　过去十五年，深度学习的工程进展由三个变量驱动：模型参数量 $N_{param}$、训练数据量 $D$ 与训练算力 $C$，三者满足著名的缩放律

$$\mathcal{L}\left( N_{param},D,C \right)\mspace{6mu} \propto \mspace{6mu} N_{param}^{- \alpha_{N}}\, D^{- \alpha_{D}}\, C^{- \alpha_{C}},$$

其中 $\alpha_{N} \approx 0.076$、$\alpha_{D} \approx 0.095$、$\alpha_{C} \approx 0.050$（Chinchilla 缩放律的经验拟合值）。式 (1-1) 表明：把损失降低一个数量级需要把算力提升约 $10^{20}$ 倍------这一指数级增长在物理上不可持续。

**三组硬约束的会合。**　（i）*能耗墙*：单个神经形态突触操作的能耗约 $10$ fJ，而 GPU 上的乘加操作能耗约 $1$ pJ------差两个数量级；（ii）*存储墙*：Transformer 注意力机制的 KV 缓存随序列长度二次增长，长上下文场景的存储带宽需求超过当前 HBM 技术的物理上限；（iii）*延迟墙*：具身智能要求毫秒级感知---决策---行动闭环，而当前数据中心---边缘---端侧的通信延迟在十毫秒量级。三堵墙在 2030 年前后同时达到物理极限。

**智能不从算力中涌现。**　式 (1-1) 的缩放律解释"训练损失如何随资源下降"，但不解释"智能为何涌现"。脑科学的经验事实是：人脑约 $86 \times 10^{9}$ 神经元、$10^{14}$ 突触，总功耗仅约 $20$ W，却实现当前最大模型无法企及的通用智能、创造性与常识推理。这一对比直接说明：*智能的物理基础不是算力本身，而是算力的组织方式*。Bertschinger 与 Natschläger 的混沌边缘论断［10］、O'Byrne 与 Jerbi 的大脑临界性争论［29］、Friston 的自由能原理［45\]\[46］从不同侧面指向同一结论：复杂网络的时空协同模式，而非单节点算力，才是智能的源泉。

## 1.2　学术渊源：四个学科的交叉传统

**复杂性科学。**　二十世纪八十年代起，Langton 的混沌边缘论断［10］、Kauffman 的自组织临界、Holland 的复杂适应系统理论，共同构成"复杂性涌现"的经典范式：远离平衡的开放系统在有序---混沌相变边缘表现出最大计算能力。这一范式为智能提供了非还原论的解释框架------智能不是部件性质的简单叠加，而是相互作用的涌现产物。

**脑神经科学。**　皮层电生理的实验证据------雪崩统计的幂律分布、临界慢化、兴奋---抑制平衡的自发涌现、神经活动的低维流形结构------共同指向大脑运行在临界区附近。O'Byrne 与 Jerbi［29］系统综述了"大脑临界性"的二十年争论：一方面，临界性假说被大量实验证据支持；另一方面，实验方法学的局限（电极空间采样、时间窗选择、阈值敏感性）使"真临界"与"表观临界"难以区分。本卷采用该综述的折中立场：*大脑运行在临界邻域，但不必精确在临界点*------这与第 4 章"边缘稳定储备池"的可证明原理一致。

**计算机科学。**　图灵的可计算性、冯·诺依曼的自复制自动机、Hopfield 的联想记忆网络、Hinton 的玻尔兹曼机，构成"计算即动力系统"的学术传统。储备池计算［11\]、液态状态机［10\] 与回声状态网络把这一传统推进到循环神经网络的可训练动力学。

**机器人工程。**　Brooks 的具身智能（embodied intelligence）革命颠覆了"感知---建模---规划---行动"的经典 AI 管线，主张智能是与环境交互的涌现属性。Pfeifer 的形态计算（morphological computation）、Ijspeert 的中枢模式发生器，把控制论与动力系统理论引入机器人本体。

**四个传统的汇合点。**　本卷是这四个传统的现代汇合：复杂性科学提供相变与涌现的语言，脑神经科学提供皮层网络的结构---功能数据，计算机科学提供动力学计算的可训练框架，机器人工程提供具身交互的物理约束。四者在 Lyapunov 谱这一公共观测量上同构------本卷的核心技术贡献即把这一同构显式化。

## 1.3　核心假说：网络时空协同复杂度与智能等级

**复杂度可量化。**　本卷的核心技术命题是：*网络时空协同复杂度可被 Lyapunov 谱密度、正指数计数与 Kaplan--Yorke 维数严格度量*（第 3 章）。在这套度量下：

-   $\lambda_{\max} < 0$：有序区，无记忆无非线性；
-   $\lambda_{\max} = 0$：临界区，最大记忆容量与最大计算能力（第 4 章）；
-   $\lambda_{\max} > 0$：混沌区，最大非线性混合但信息保持失效。

**智能等级作为谱分岔。**　本卷的核心理论命题是：*感知、反应、适应、创造、通用、超级六个智能等级对应 Lyapunov 谱不变量越过相继阈值的分岔序列*（第 9 章）。具体地：

-   感知（L1）：$\Lambda_{cond} < 0$（输入驱动同步）；
-   反应（L2）：$\lambda_{\max} \rightarrow 0^{-}$（边缘稳定）；
-   适应（L3）：$N_{pos} > 0$ 且 $D_{KY} \ll N$（有限但低维的混沌）；
-   创造（L4）：$N_{pos}/N \rightarrow$ 有限常数（广延混沌但受控）；
-   通用（L5）：谱密度 $\rho_{\infty}$ 呈双分量（相干+混沌）；
-   超级（L6）：多阶 Laplacian 谱不变量越过相继阈值（互连尺度的复杂度）。

**智能的可演化性。**　本卷的工程命题是：*上述谱学分岔序列可在晶圆级/晶矩异构异质集成平台上被自演化互连（SEI）在线演化重构*。这一命题把"智能等级"从抽象概念转化为可调参的工程对象。

## 1.4　技术路线：晶圆级/晶矩异构异质集成与自演化互连

**介观尺度的物理载体。**　晶圆级/晶矩异构异质集成平台把不同材料（忆阻器、相变器件、自旋电子器件、量子点）、不同器件（突触、神经元、传感器）、不同功能模块（模拟计算、数字控制、光互连）整合于单一介观尺度平台（晶圆或晶矩），构建高密度、大规模、高维度、动态可塑的异质异构物理神经网络液态硬件。

**自演化互连（SEI）的化合机制。**　SEI 引擎在晶圆级/晶矩硬件上提供四层可编程接口：（i）*元拓扑操作*------增边、删边、调权、升阶，由 Hellmann--Feynman 公式解析预测谱扰动（第 6 章）；（ii）*谱学目标函数*------任务损失+谱约束+拓扑指标（第 7 章 (7-8)）；（iii）*变分学习*------谱空间中的能量最小化（第 8 章 (8-10)）；（iv）*谱测量*------数据驱动的谱估计与在线监测（第 10 章）。四层接口构成"观测---决策---执行---验证"的可计算闭环。

**能量最小化的进化动力学。**　在与环境交互中，晶圆级/晶矩硬件基于能量最小化原则（最小自由能+最小作用量+STDP 学习机制）持续进化感知、认知、决策、行动的 OODA 具身智能。这一进化动力学在谱空间中投影为 Lyapunov 谱的定向迁移------"学习即谱的雕刻"（第 7 章）。

## 1.5　本卷结构与阅读导引

**卷二结构。**　本卷《理论基石篇》共十一章，分四个部分：

-   第一部分（第 1---2 章）：数学准备。第 1 章绪论，第 2 章 Lyapunov 谱的数学语言；
-   第二部分（第 3---6 章）：既有理论基座。第 3 章内在复杂度，第 4 章混沌边缘，第 5 章感知调控，第 6 章互连协同；
-   第三部分（第 7---9 章）：理论核心。第 7 章学习雕刻，第 8 章能量变分，第 9 章智能判据；
-   第四部分（第 10---11 章）：工程闭环。第 10 章谱测量与编程，第 11 章总结与研究纲领。

**阅读导引。**　对数学家：重点第 2、3、8 章；对物理学家：重点第 3、6、8 章；对计算机科学家：重点第 4、5、7 章；对工程师：重点第 6、7、10 章；对神经科学家：重点第 5、7、9 章。全部章节共享第 2 章的符号表与谱学语言，可独立阅读亦可在第 2 章后按兴趣跳转。

**与卷一、卷三的接口。**　卷一《绪论篇》给出问题陈述与研究路线，本卷给出理论基础，卷三《工程实现篇》给出介观硬件与 SEI 引擎的具体实现。三卷构成"问题---理论---工程"的完整闭环。 \# 第二章　Lyapunov 谱：理论基石的数学语言

> *"Lyapunov exponents are the unique dynamical invariants that simultaneously characterize local stability, information flow rate, attractor dimensionality, and entropy production rate."*
>
> ------本卷对 Oseledets 乘法遍历定理工程意义的复述（综合 Engelken--Wolf--Abbott 全谱理论［5］、Gallavotti--Cohen 涨落定理［53］、Hoover--Posch 不可逆性［55］、Das--Green 谱界［56］）

**核心命题：**　Lyapunov 谱是唯一同时刻画局部稳定性、信息流散度、吸引子维数与熵产生率的动力系统不变量族，堪当复杂度定量理论的基本语言。本章 2.1 给出定义与存在性（Oseledets 乘法遍历定理），2.2 给出数值方法（Benettin 算法、时间序列重构、收敛控制），2.3 给出谱的衍生不变量（Kaplan--Yorke 维数、Pesin 熵公式），2.4 区分三类指数（无条件谱、条件指数、横向指数），2.5 给出谱对称性与随机矩阵理论的解析逼近入口，2.6 给出本卷统一符号表。

## 2.1　定义与存在性：Oseledets 乘法遍历定理

**基本设置。**　设 $\dot{x} = F(x)$，$x \in \mathbb{R}^{N}$，$F$ 光滑；沿参考轨迹 $x(t)$ 的切映射由变分方程

$$\dot{\xi}(t)\mspace{6mu} = \mspace{6mu} DF\left( x(t) \right)\,\xi(t)$$

生成，其中 $DF$ 为 Jacobian 矩阵。对任意初始切向量 $\xi_{0} \in \mathbb{R}^{N}$，定义*Lyapunov 指数*

$$\lambda\left( \xi_{0} \right)\mspace{6mu} = \mspace{6mu}\limsup_{t \rightarrow \infty}\mspace{6mu}\frac{1}{t}\,\ln \parallel \xi(t) \parallel .$$

**Oseledets 乘法遍历定理（1968）。**　若系统具有不变概率测度 $\mu$ 且 Jacobian 范数的正对数部 $\max\left( \ln \parallel DF \parallel ,0 \right)$ 属于 $L^{1}(\mu)$，则对 $\mu$-几乎处处的初值 $x_{0}$，存在：

-   不变分解 $\mathbb{R}^{N} = E_{1}\left( x_{0} \right) \oplus E_{2}\left( x_{0} \right) \oplus \cdots \oplus E_{k}\left( x_{0} \right)$；
-   实数 $\lambda_{1} > \lambda_{2} > \cdots > \lambda_{k}$（不计重数）；
-   使得对 $E_{i}$ 中非零向量 $\xi$，$\lambda(\xi) = \lambda_{i}$，且 (2-2) 的 limsup 可替换为普通极限。

**（Oseledets 定理）**　在上述条件下，Lyapunov 谱 $\{\lambda_{i}\}_{i = 1}^{N}$（计重数，$\lambda_{1} \geq \lambda_{2} \geq \cdots \geq \lambda_{N}$）几乎处处存在、有界且与初值无关；它是切映射动力学的完整不变量族。该定理是本章所有后续定义的数学基础。

**谱的物理解读。**　$\lambda_{i} > 0$ 表征 $i$ 方向的指数发散（混沌），$\lambda_{i} < 0$ 表征指数收缩（耗散），$\lambda_{i} = 0$ 表征中性（边缘）。*正指数数目* $N_{pos}$、*最大指数* $\lambda_{\max}$、*谱密度* $\rho_{\infty}(\lambda)$（第 3 章 (3-6)）是三个最常用的粗粒化观测量。

## 2.2　数值方法：Benettin 算法、时间序列重构与收敛控制

**Benettin 算法（标准算法）。**　对 $k = 1,\ldots,N$，沿轨迹 $x(t)$ 同时演化 $N$ 个切向量 $\{\xi^{(k)}(t)\}$，每隔时间 $\tau$ 对切向量组做 Gram--Schmidt 正交化：

$$\xi^{(k)}(t + \tau)\mspace{6mu} = \mspace{6mu}\frac{{\widetilde{\xi}}^{(k)}(t + \tau)}{\parallel {\widetilde{\xi}}^{(k)}(t + \tau) \parallel},\quad\quad{\widetilde{\xi}}^{(k)} = \text{ (pre-orthogonalization)}.$$

每个 Lyapunov 指数由正交化因子的对数时间平均给出：

$$\lambda_{i}\mspace{6mu} = \mspace{6mu}\lim_{M \rightarrow \infty}\,\frac{1}{M\tau}\sum_{m = 1}^{M}\ln \parallel {\widetilde{\xi}}^{(i)}(m\tau) \parallel .$$

**Wolf 方法（时间序列重构）。**　当只有标量时间序列 $s(t)$ 而无显式动力学时，用延迟嵌入重构相空间 $\{ s(t),s\left( t - \tau_{d} \right),\ldots,s\left( t - (m - 1)\tau_{d} \right)\}$，在嵌入维数 $m$ 与延迟 $\tau_{d}$ 适当选择下估计 $\lambda_{\max}$。该方法对本卷介观硬件的实验测量（第 10 章）尤其重要。

**收敛控制。**　Lyapunov 指数估计的误差来源包括：有限时间效应、正交化精度、轨迹长度。Engelken--Wolf--Abbott［5］给出网络维数 $N$ 与收敛时间的经验标度律 $T_{conv} \sim N^{1/2}/\lambda_{\max}$，为第 10 章谱测量工具链的实时监测提供理论基线。

## 2.3　谱的衍生不变量：Kaplan--Yorke 维数与 Pesin 熵公式

**Kaplan--Yorke 维数。**　设 Lyapunov 谱按降序排列 $\lambda_{1} \geq \lambda_{2} \geq \cdots \geq \lambda_{N}$，定义

$$D_{KY}\mspace{6mu} = \mspace{6mu} k + \frac{1}{\left| \lambda_{k + 1} \right|}\sum_{i = 1}^{k}\lambda_{i},\quad\quad k = \max\left\{ j:\sum_{i = 1}^{j}\lambda_{i} \geq 0 \right\}.$$

$D_{KY}$ 给出吸引子的分形维数上界，在多数耗散系统上为该维数的精确值。本卷将在第 3 章证明 $D_{KY} \ll N$ 是"高维网络承载低维意义结构"的数学表达。

**Pesin 熵公式。**　对具有 SRB 测度的混沌系统，测度论熵（Kolmogorov--Sinai 熵）等于正 Lyapunov 指数之和：

$$h_{KS}\mspace{6mu} = \mspace{6mu}\sum_{i:\lambda_{i} > 0}^{}\lambda_{i}.$$

式 (2-6) 把信息论熵与动力学不变量严格挂钩。第 5 章将用它给出感知带宽的谱学上限 (5-13)，第 8 章将用它给出熵产生率的谱学恒等式 (8-8)。

**谱---热力学桥。**　由 (2-5) 与 (2-6)，谱的衍生不变量同时刻画*几何*（维数）与*信息*（熵）两个维度。Gallavotti--Cohen 涨落定理［53］进一步把谱与热力学熵产生率挂钩（见 8.3 节 (8-8)），Hoover--Posch［55］把它与相空间维数损失挂钩，Das--Green［56］给出熵流率的谱界------这些桥墩共同构成 8.3 节的热力学---谱学统一。

## 2.4　三类指数的分工：无条件谱、条件指数与横向指数

**无条件 Lyapunov 谱。**　即 2.1 节定义的 $\{\lambda_{i}\}$，刻画自治系统的内在稳定性与复杂度。本卷第 3 章内在复杂度理论全部基于无条件谱。

**条件 Lyapunov 指数。**　对驱动系统 $\dot{x} = F\left( x,u(t) \right)$，定义条件指数

$$\Lambda_{cond}(u)\mspace{6mu} = \mspace{6mu}\limsup_{T \rightarrow \infty}\,\frac{1}{T}\,\ln \parallel \delta x(T) \parallel / \parallel \delta x(0) \parallel ,$$

其中 $\delta x(t)$ 为同一驱动 $u(t)$ 下两条轨迹的差。$\Lambda_{cond} < 0$ 等价于输入驱动同步 / 回声状态性质（第 5 章命题 5.1）。条件指数刻画*感知接口的适定性*。

**横向 Lyapunov 指数。**　对耦合网络 (6-1) 的同步流形 $\mathcal{M}$，把切向量分解为流形切向与法向分量；法向分量的最大 Lyapunov 指数即横向指数 $\lambda_{\bot}$。主稳定函数理论（第 6 章 (6-2)---(6-4)）把同步稳定性等价于 $\lambda_{\bot} < 0$。横向指数刻画*互连协同的稳定性*。

**三类指数的统一坐标。**　本卷的全部谱学论断可写为：在*内在*（无条件）、*感知*（条件）、*互连*（横向）三个坐标下，智能等级对应不同的谱学分岔条件。这是第 9 章"六级智能谱学判据"的观测量基础。

## 2.5　谱对称性与解析逼近：随机矩阵理论入口

**谱点对称。**　Engelken--Wolf--Abbott［5］证明：随机循环网络的 Lyapunov 谱关于非零常数 $\lambda_{0}$ 呈点对称（第 3 章 (3-9)）：

$$\lambda_{i} + \lambda_{N + 1 - i} = 2\lambda_{0},\quad\quad i = 1,\ldots,N.$$

该对称源于切映射的广义时间反演对称性，在无耗散极限 $\lambda_{0} = 0$ 即严格辛配对。

**随机矩阵理论入口。**　切映射的 Jacobian 由随机矩阵 $D(t)J$ 生成（第 3 章 (3-11)），其中 $D(t) = diag\left\lbrack \varphi'\left( x_{i}(t) \right) \right\rbrack$。Girko 圆律给出单步谱的渐近分布，乘积随机矩阵理论给出长时间极限下的 Lyapunov 谱显式表达式------这使第 3 章的谱学度量在渐近意义下解析可算。

**谱敏感度与 Hellmann--Feynman 公式。**　权重矩阵的微小扰动 $\delta J$ 对 Laplacian 特征值 $\mu_{k}$ 的一阶扰动为

$$\delta\mu_{k}\mspace{6mu} = \mspace{6mu} v_{k}^{\top}\,\delta L\, v_{k},$$

其中 $v_{k}$ 为 $\mu_{k}$ 的特征向量、$\delta L$ 为拉普拉斯的扰动。该公式在第 6 章 (6-11) 与第 7 章 (7-3) 被广泛用于谱指导的拓扑优化与可塑性控制。

## 2.6　本卷统一符号表

  ------------------------------------------------------------------------------------
  符号                            含义                         首现
  ------------------------------- ---------------------------- -----------------------
  $N$                             网络节点数                   全卷

  $x_{i}(t)$                      节点 $i$ 的状态              (2-1)

  $J$ / $W$                       循环权重矩阵                 (2-1)

  $J_{ij}(t)$                     可塑突触权重                 (7-1)

  $F(x)$                          节点动力学                   (2-1)

  $H(x)$                          耦合函数                     (6-1)

  $\varphi( \cdot )$              激活函数（$\tanh$ 为代表）   (3-1)

  $I_{i}(t)$ / $u_{t}$            外部输入                     (5-1)

  $L = D - A$                     图拉普拉斯                   (6-1)

  $\{\mu_{k}\}$                   Laplacian 特征值             (6-2)

  $\{\lambda_{i}\}$               无条件 Lyapunov 谱           (2-2)

  $\lambda_{\max}$                最大 Lyapunov 指数           (2-2)

  $\Lambda_{cond}$                条件最大 Lyapunov 指数       (2-7)

  $\lambda_{\bot}$                横向 Lyapunov 指数           (6-2)

  $\Psi(\alpha)$                  主稳定函数                   (6-3)

  $N_{pos}$                       正指数计数                   (3-7)

  $D_{KY}$                        Kaplan--Yorke 维数           (2-5)

  $h_{KS}$                        Kolmogorov--Sinai 熵         (2-6)

  $\rho_{\infty}(\lambda)$        谱密度极限                   (3-6)

  $g$ / $g_{c}$                   耦合增益 / 临界值            (3-3)

  $\rho(J)$                       权重谱半径                   (3-4)

  $\mathcal{F}$ / $\mathcal{S}$   变分自由能 / 作用量          (8-1), (8-3)

  $\Phi\lbrack\rho\rbrack$        谱变分泛函                   (8-10)

  $\bar{\sigma}$                  熵产生率                     (8-7)

  $T_{cog}$                       认知温度                     (8-10)

  $\mathcal{E}$ / $\mathcal{P}$   任务损失 / 可塑性规则        (7-8), (7-1)

  $R = \mu_{N}/\mu_{2}$           Laplacian 特征值比           (6-5)

  $G_{\max}$                      非模态瞬态放大               (6-10)
  ------------------------------------------------------------------------------------

**约定。**　向量用粗体（$\mathbf{x}$），矩阵用大写拉丁字母（$J,W,L,A$），谱观测量用希腊字母（$\lambda,\mu,\rho,\sigma$），泛函用花体（$\mathcal{F},\mathcal{S},\mathcal{E}$），本章符号表为全卷引用基准。

## 2.7　本章小结

本章把 Lyapunov 谱从数学定理提升为复杂度定量理论的工作语言：Oseledets 定理保证谱的存在性与不变量地位，Benettin 与 Wolf 算法给出谱的数值可算性，Kaplan--Yorke 维数与 Pesin 熵公式把谱翻译为几何与信息论观测量，无条件/条件/横向三类指数的分工为第 3---9 章的谱学论断预置坐标系，随机矩阵理论入口与 Hellmann--Feynman 公式把谱的解析逼近与可微控制显式化。第 3---9 章将在此基础上展开：第 3 章把谱用作内在复杂度的度量，第 4---6 章把它用作最优计算区、感知调控与互连协同的判据，第 7---8 章把它用作学习与能量变分的对象，第 9 章把它用作智能等级的判据。 \# 第三章　网络内在动力学的复杂度理论

> *"For sufficiently strong coupling, the network is chaotic; there exists a critical coupling strength* $g = 1$ *at which the fixed point loses stability and a chaotic attractor is born."*
>
> ------H. Sompolinsky, A. Crisanti, H. J. Sommers 平均场混沌相变论断的现代复述［1］

**核心命题（论点链一）：**　网络时空协同复杂度可用 Lyapunov 谱密度、正指数计数与 Kaplan--Yorke 维数严格定义；智能等级阈值可表述为谱不变量的分岔条件。本章围绕这一命题，从平均场相变（3.1---3.2）经完整谱的解析（3.3）到谱的精细结构（3.4）与结构化连接（3.5），逐层建立"复杂度可量化、可解析逼近"的数学骨架，为第八、九章的原创工作提供度量基础。

## 3.1　随机耦合网络的混沌相变：动态平均场理论

考虑连续时间率网络

$${\dot{x}}_{i}(t) = - x_{i}(t) + \sum_{j = 1}^{N}J_{ij}\,\varphi\left( x_{j}(t) \right),\quad\quad i = 1,\ldots,N,$$

其中激活函数 $\varphi = \tanh$，突触权重 $J_{ij}$ 独立同分布，均值零、方差 $g^{2}/N$。1988 年 Sompolinsky--Crisanti--Sommers 用动态平均场理论证明：当 $N \rightarrow \infty$ 时，任一节点视野下的输入项 $\sum_{j}^{}J_{ij}\varphi\left( x_{j} \right)$ 依中心极限收敛为高斯过程 $\eta_{i}(t)$，其自相关函数 $C(\tau) = \left\langle \eta_{i}(t)\eta_{i}(t + \tau) \right\rangle$ 满足自洽方程

$$\ddot{C}(\tau) = C(\tau) - g^{2}\,\left\langle \varphi\left( x(t) \right)\,\varphi\left( x(t + \tau) \right) \right\rangle,$$

且系统在耦合增益 $g$ 越过临界值

$$g_{c} = 1$$

时由稳定定点连续相变至混沌。相变的定量判据即最大 Lyapunov 指数由负转正。

Kadmon 与 Sompolinsky 将上述框架推广至*非奇对称激活函数*与脉冲神经元网络［1］：以率模型形式给出稳定定点、失稳动态、混沌三个 regimes 的完整相图，证明相变点由激活函数斜率 $\varphi'(0)$ 与耦合方差共同决定，并在脉冲电路中直接测得最大 Lyapunov 指数 $\lambda_{\max}(g)$ 越过零点的分岔行为。Harish 与 Hansel 在离散时间脉冲电路上刻画了异步率混沌，明确 $\lambda_{\max} > 0$ 状态下的异步性质［4］，构成"混沌---异步"这一实验神经科学核心观察的动力学基础。

**平均场判据的解析结果。**　在小 $g$ 展开下，定点邻域的雅可比谱半径

$$\rho\left( J\varphi'(0) \right) = g\,\varphi'(0),$$

由 Girko 圆律（详见 3.3 节的严格陈述）给出。混沌判据 $\lambda_{\max} = 0$ 与 $\rho = 1$ 重合的必要条件即 $g\,\varphi'(0) = 1$，这即 (3-3) 在一般激活函数下的推广。式 (3-4) 之所以重要，在于*它把连续动力学的相变直接映射到静态权重矩阵的谱半径*------第四章 4.3 节的"谱半径准则"正源于此，而 4.3 节的 Lyapunov 界定理则说明该静态准则必须由动态谱指数替代。

## 3.2　脉冲网络的混沌相图与外部输入的驯化

**混沌被输入抑制。**　Rajan、Abbott 与 Sompolinsky 证明：在 (3-1) 中加入随时间波动的外部输入 $I_{i}(t)$，平均场方程 (3-2) 的 $\varphi\varphi$ 相关项在正确重整化后减小，最大 Lyapunov 指数系统性下降［2］。定性地，输入将节点驱离激活函数的高增益线性区、把动力学限制在饱和区（$\varphi' \rightarrow 0$），从而降低有效增益 $g_{eff} = g\left\langle \varphi' \right\rangle$，最终使系统跨越相变边界回归定点。刺激越强、相关时间越长，抑制越显著。

**Landau--Sompolinsky 相干混沌。**　当权重矩阵含结构化分量 $J = J^{rand} + \alpha\, J^{struct}$（$\alpha$ 控制结构比例）时，微扰动力学的平均场方程在混沌与相干模式之间出现耦合项［3］。结果是：$\alpha$ 较小时结构化模式被混沌噪声淹没；$\alpha$ 越过阈值后系统进入"相干混沌"区制------存在正 Lyapunov 指数（保留混沌）但同时存在稳定的低维振荡吸引子（保留结构化模式）。相干混沌解释了皮层电路"在噪声背景下涌现规律性群体活动"的经验现象，也预示第 5 章感知---内在动力学耦合的更一般图像。

综合 3.1--3.2，可得*平均场层面的复杂度---功能对偶*：

$$FixedPoint\mspace{6mu}\left( \lambda_{\max} < 0 \right)\  \Leftrightarrow \ \text{ (no memory, no nonlinearity)}$$

$$Critical\mspace{6mu}\left( \lambda_{\max} = 0 \right)\  \Leftrightarrow \ \text{ (max memory capacity)}$$

$$Chaotic\mspace{6mu}\left( \lambda_{\max} > 0 \right)\  \Leftrightarrow \ \text{ (max mixing, memory fails)}.$$

这一对偶正是第四章"边缘最优计算"命题的能量级前身。

## 3.3　完整 Lyapunov 谱的首次解析：广度混沌与谱对称性

Engelken、Wolf 与 Abbott 于 2023 年完成该领域的里程碑：首次计算随机循环网络的*完整* Lyapunov 谱，而非仅最大指数［5］。以下总结其三条主要结论。

**结论 3.1（广度混沌）。**　在 $N \rightarrow \infty$ 极限下，Lyapunov 谱 $\{\lambda_{i}\}_{i = 1}^{N}$ 的经验密度

$$\rho_{N}(\lambda) = \frac{1}{N}\sum_{i = 1}^{N}\delta\left( \lambda - \lambda_{i} \right)\ \overset{N \rightarrow \infty}{\rightarrow}\ \rho_{\infty}(\lambda),$$

收敛到*与* $N$ *无关*的极限分布，其形状仅依赖 $g$ 与激活函数。故正 Lyapunov 指数数目

$$N_{pos}\mspace{6mu} = \mspace{6mu} N\int_{0}^{+ \infty}\rho_{\infty}(\lambda)\, d\lambda.$$

$N_{pos}$ 随 $N$ 线性增长------混沌是*广延（extensive）*的。这与 KS 熵密度

$$h_{KS}/N = \int_{0}^{+ \infty}\lambda\,\rho_{\infty}(\lambda)\, d\lambda$$

的强度性完全一致。

**结论 3.2（谱的点对称与辛结构）。**　网络动力学具有广义时间反演对称性；在此对称之下，Lyapunov 谱关于*非零常数* $\lambda_{0}$ 呈点对称：

$$\lambda_{i} + \lambda_{N + 1 - i} = 2\lambda_{0},\quad\quad i = 1,\ldots,N,$$

令人联想起哈密顿混沌的辛配对。$\lambda_{0}$ 由耗散率决定：无耗散极限下 $\lambda_{0} = 0$，即严格辛配对；有耗散时 $\lambda_{0} < 0$。此对称是谱的强约束，将 3-9 式与 (3-8) 联合，可推出 KS 熵与吸引子维数的严格上界。

**结论 3.3（Kaplan--Yorke 维数远小于** $N$**）。**　吸引子分形维数由 Kaplan--Yorke 公式

$$D_{KY} = k + \frac{1}{\left| \lambda_{k + 1} \right|}\sum_{i = 1}^{k}\lambda_{i},\quad k = \max\left\{ j:\sum_{i = 1}^{j}\lambda_{i} \geq 0 \right\}$$

给出。数值与解析均表明 $D_{KY}/N \rightarrow d_{\infty}(g) < 1$，且 $d_{\infty}$ 在 $g$ 略大于 $g_{c}$ 处取小值------*吸引子始终生活在远小于相空间的低维流形上*。这为"高维网络承载低维意义结构"的直觉提供了严格数学表达。

**随机矩阵理论解析近似。**　式 (3-1) 的切映射由随机矩阵 $D(t)\, J$ 生成，$D(t) = diag\left\lbrack \varphi'\left( x_{i}(t) \right) \right\rbrack$。在混沌 onset 附近与极强混沌区，$D(t)$ 的分布近似冻结，$D\, J$ 谱由 Girko 圆律给出

$$spec(D\, J)\  \subset \ \{ z \in \mathbb{C}:|z| \leq g\left\langle {\varphi'}^{2}\rangle^{1/2} \right\},$$

结合乘积随机矩阵理论可得 Lyapunov 谱的显式表达式［5］。式 (3-11) 是把 (3-4) 的静态谱半径与真正的动态 Lyapunov 谱衔接起来的桥梁：*静态谱半径决定线性化谱，Lyapunov 谱由线性化谱经乘积遍历给出，随机矩阵理论使二者在渐近意义下解析可算*。

**Monteforte--Wolf 的先驱工作。**　早在 2010 年，Monteforte 与 Wolf 已在平衡态脉冲网络中数值测得全谱与动力学熵产生率，指出网络混沌在随机图连接下"非广延"的边界情形［8］。Dafilis 等人于 2001 年在 EEG 模型上给出广延混沌的稳健证据［9］。这两项工作为 Engelken 等人的解析结果提供了跨越十余年的实验---模型准备。

## 3.4　谱的精细结构：对称性破缺、重尾连接与低维化

**对称性破缺诱导高维混沌。**　Clusella 在稀疏随机的精确发放率模型中发现，节点动力学的对称性破缺会诱导高维广延混沌，其 Kaplan--Yorke 分形维数按 (3-10) 计算可显著大于对称情形［6］。这一结果揭示：广度混沌不是随机连接的必然产物，而是*对称性---拓扑---非线性*共同作用的输出。

**重尾连接下的缓慢低维化。**　Xie、Mihalas 与 Kuśmierz（NeurIPS 2025）证明：当循环权重取重尾分布（如 $\alpha$-稳定分布）时，网络的 Kaplan--Yorke 维数 $D_{KY}(t)$ 沿训练轨迹缓慢单调下降［7］。具体地，重尾指数 $\alpha$ 越小（尾部越重），大权重的稀疏支配越强，动力学越倾向被少数强连接锁定；数值上

$$D_{KY}(\alpha)\,/\, N\mspace{6mu} \sim \mspace{6mu}(\alpha - 1)^{\beta}\quad\text{as }\alpha \downarrow 1,$$

其中 $\beta > 0$ 由激活函数决定。式 (3-12) 具有直接的生物学意义：皮层突触强度经验分布呈明显重尾，若接受该模型，*皮层活动的低维结构是重尾连接的谱学必然结果*，而不必假定额外的降维机制。

**外部输入的降维降熵。**　回到 Engelken 等人的结果［5］：涨落输入 $I_{i}(t)$ 同时降低 Lyapunov 谱的支撑宽度与吸引子维数。定量地，若把输入模型化为高斯白噪声，则 (3-2) 的自洽相关函数变为

$$\ddot{C}(\tau) = C(\tau) - g^{2}\left\langle \varphi\varphi \right\rangle + \sigma_{I}^{2}\,\delta(\tau),$$

$\sigma_{I}$ 增大时 $\lambda_{\max}$ 与 $D_{KY}$ 单调下降。3.2 节的"输入驯化混沌"现象由此获得全谱层面的定量刻画------*感知不是把混沌关掉，而是把谱压回边缘*。

## 3.5　结构化连接与相干混沌：结构---动力学---功能链条

3.2 节末尾提到的相干混沌［3］在谱学语言下有清晰表达：结构化分量 $\alpha J^{struct}$ 使 Jacobian 矩阵含一个突出的低秩特征子空间。若 $J^{struct}$ 的谱半径 $\rho_{s}$ 越过 $1 - \alpha$ 阈值，切映射的一部分 Lyapunov 指数与该特征子空间对齐，构成低维相干模式；其余 $N - rank\left( J^{struct} \right)$ 个指数仍由随机部分主导，构成高维混沌背景。总谱因此呈"少数分离的相干指数＋大量连续的混沌指数"的双分量形式。

这一图像统一了 3.1--3.4 的分片观察：*平均场决定谱包络，结构化决定谱的低维特征分量，输入决定谱的整体位置*。三者相加即构成本卷第九章"六级智能谱学判据"的原材料------不同智能等级对应不同的谱分量组合，而非某个单一指数越过某阈值。

## 3.6　本章小结与向后章节的过渡

**已建立的度量体系。**　本章证明 Lyapunov 谱的三类量（谱密度 $\rho_{\infty}$、正指数计数 $N_{pos}$、Kaplan--Yorke 维数 $D_{KY}$）与两条对称约束（谱点对称、KS 熵---维数联合上界）共同构成"网络内在复杂度"的严格度量集合。在此度量下：

-   静态谱半径与动态 Lyapunov 谱由随机矩阵理论解析连接（式 3-4、3-11）；
-   混沌是广延的但吸引子低维（结论 3.1、3.3）；
-   谱可解析近似，且对输入敏感（结论 3.2、式 3-13）；
-   结构化连接导致谱的双分量分裂（3.5 节）。

**留待后续章节的问题。**　（一）$D_{KY}/N \rightarrow d_{\infty}$ 的具体函数形式在异质异构介观网络上的形式仍属空白（空白一，见第九章）；（二）当权重被 STDP 动态调制时，(3-6) 的谱密度如何演化的理论尚未建立（空白二，见第七章末节）；（三）在能量最小化原理下，谱作为变分观测量的作用还未被显式化（空白三，见第八章）。本章所建立的度量语言是应对这三项空白的共同前提。

*承上启下*：本章的谱学度量为第四章"边缘最优计算"提供了"边缘"一词的严格含义（$\lambda_{\max} \rightarrow 0^{-}$ 且谱密度支撑压向零），也为第五章"输入驯化"提供了 (3-13) 式的定量工具；第六章将证明当耦合矩阵被赋予拓扑结构时，本章的谱理论如何被主稳定函数与横向 Lyapunov 谱系统性推广至互连层面。 \# 第四章　混沌边缘：最优计算区的可证明原理

> *"We propose a complexity measure which we find to assume its highest values near the edge of chaos ... only near the edge of chaos are such networks able to perform complex computations on time series."*
>
> ------N. Bertschinger 与 T. Natschläger，NeurIPS 2004［10］

**核心命题：**　混沌边缘（edge of chaos）是最优计算区的论断，已从二十世纪末的经验假说升级为以 Lyapunov 指数为严格判据的可证明设计原理：一方面，回声状态性质（ESP）与衰退记忆性质（FMP）由条件 Lyapunov 谱给出充分必要刻画；另一方面，稳定边缘（edge of stability）储备池模型给出了最大局部 Lyapunov 指数的显式界，使"临界处计算最优"成为可设计、可验证的数学命题，并已在纳米线神经形态网络上获得实验证据［10---15］。

本章结构如下：4.1 节回溯假说的提出与早期证据；4.2 节建立 ESP 与条件 Lyapunov 谱的严格理论；4.3 节给出从谱半径启发式到 Lyapunov 界定理的推导；4.4 节讨论记忆---非线性权衡在混沌边缘的定量刻画；4.5 节综述物理基质上的实验证据；4.6 节小结并指出通向第七章学习机制的接口。

## 4.1　假说的提出：从经验观察到计算论断

二十世纪八十年代末，Langton 在元胞自动机研究中观察到，规则空间中介于有序与混沌之间的"相变边缘"区域伴随着最长的瞬态与最丰富的空间信息传递结构，由此提出"生命与计算位于混沌边缘"的著名猜想。这一猜想进入神经网络领域的关键一步由 Bertschinger 与 Natschläger 完成［10］：他们在随机阈值门网络中定义了刻画轨迹分离的复杂度度量，发现该度量在有序---混沌相变处取最大值，并且*只有在混沌边缘附近，网络才能对时间序列执行复杂计算*；同时给出使网络自组织趋向临界点的突触标度规则。Verstraeten 等人随后在储备池计算的各实现之间做了系统的实验统一比较，以 Lyapunov 启发的方法将回声状态性质与实际网络动力学定量挂钩，确认了"接近而不越过混沌边界"是储备池性能的普适最优区［11］。

这一阶段的两项成果确立了假说的经验内核，但留下两个悬而未决的问题：其一，"混沌边缘"缺乏严格的数学定义，不同工作使用的判据互不统一；其二，"边缘处最优"只有数值证据，没有定理级保证。这两个问题的答案分别由 4.2 节与 4.3 节所述的近期工作给出。

## 4.2　回声状态性质与衰退记忆：条件 Lyapunov 谱的严格理论

**定义 4.1（储备池动力系统）。**　考虑输入驱动的离散时间递归系统

$$\mathbf{x}_{t} = (1 - \alpha)\,\mathbf{x}_{t - 1} + \alpha\,\varphi\left( W\mathbf{x}_{t - 1} + W_{in}\mathbf{u}_{t} \right),$$

其中 $\mathbf{x}_{t} \in \mathbb{R}^{N}$ 为储备池状态，$\mathbf{u}_{t}$ 为输入，$\alpha$ 为泄漏率（满足 $0 < \alpha \leq 1$），$\varphi$ 为分量作用的激活函数（如 $\tanh$），$W$ 与 $W_{in}$ 分别为循环与输入权重。

**定义 4.2（条件 Lyapunov 指数）。**　沿输入驱动轨迹 $\{\mathbf{x}_{t}\}$ 的线性化（切）动力学为

$$\delta\mathbf{x}_{t} = J_{t}\,\delta\mathbf{x}_{t - 1},\quad\quad J_{t} = \left\lbrack (1 - \alpha)I + \alpha\, D_{t}W \right\rbrack,\quad D_{t} = diag\left\lbrack \varphi'\left( W\mathbf{x}_{t - 1} + W_{in}\mathbf{u}_{t} \right) \right\rbrack,$$

最大条件 Lyapunov 指数定义为扰动增长率的渐近均值：

$$\Lambda_{\max} = \lim_{T \rightarrow \infty}\frac{1}{T}\sum_{t = 1}^{T}\ln\frac{\parallel J_{t}\mathbf{v}_{t} \parallel}{\parallel \mathbf{v}_{t} \parallel},$$

其中 $\mathbf{v}_{t}$ 为经周期性 Gram--Schmidt 正交化再归一化的切向量（Benettin 算法，见第二章 2.2 节）。称其为"条件"指数，是因为轨迹本身由输入流 $\{\mathbf{u}_{t}\}$ 驱动，指数以输入过程为条件。

**命题 4.1（ESP 的谱判据）。**　系统 (4-1) 具有回声状态性质------即渐近状态与初始条件无关、仅由输入历史决定------的充分条件是

$$\Lambda_{\max} < 0.$$

反之，$\Lambda_{\max} > 0$ 时任意小扰动指数放大，ESP 必然失效。临界情形 $\Lambda_{\max} = 0$ 即*混沌边缘*的严格定义。

**推导（ESP ⇒ 衰退记忆之要旨）。**　设两初始状态 $\mathbf{x}_{0},\mathbf{x}_{0}'$ 由同一输入流驱动，记 $\delta\mathbf{x}_{t} = \mathbf{x}_{t} - \mathbf{x}_{t}'$。由微分中值定理与 (4-2)，

$$\parallel \delta\mathbf{x}_{t} \parallel \leq \prod_{k = 1}^{t} \parallel J_{k} \parallel \mspace{6mu} \parallel \delta\mathbf{x}_{0} \parallel = \parallel \delta\mathbf{x}_{0} \parallel \exp\left( t \cdot \frac{1}{t}\sum_{k = 1}^{t}\ln \parallel J_{k} \parallel \right).$$

由条件 (4-4) 与遍历性，$\frac{1}{t}\sum_{k}^{}\ln \parallel J_{k} \parallel \rightarrow \Lambda_{\max} < 0$，故 $\parallel \delta\mathbf{x}_{t} \parallel \leq C\, e^{- \left| \Lambda_{\max} \right|\, t} \parallel \delta\mathbf{x}_{0} \parallel$，即初始条件的影响以速率 $\left| \Lambda_{\max} \right|$ 几何衰减。Singh、Sankaranarayanan 与 Raman 将上述直观严格化：在紧致输入字母表上，ESP 与全局 Lipschitz 条件共同蕴含衰退记忆性质（远端输入被几何速率遗忘）；进而用 Stone--Weierstrass 策略证明，多项式储备池加线性读出在所有因果、时不变、衰退记忆滤波器构成的 Banach 空间中稠密，即储备池计算具有普适逼近性［13］。该工作还将储备池表述为斜积随机动力系统，证明单点回拉吸引子的存在性并导出条件 Lyapunov 界，为"皮层临界性"提供了严格的数学对应物。

由此，第二章定义的"感知接口层"获得完整的理论刻画：*ESP 保证接口适定，*$\left| \Lambda_{\max} \right|$ *给出遗忘速率，而* $\Lambda_{\max} \rightarrow 0^{-}$ *的临界区正是记忆跨度发散的方向*。这为 4.4 节的记忆---非线性权衡埋下伏笔。

## 4.3　从谱半径启发式到 Lyapunov 界定理：稳定边缘储备池

长期以来，工程实践以谱半径准则 $\rho(W) < 1$ 作为 ESP 的充分条件。该准则保守且与真实动力学脱节：它既不依赖输入，也无法刻画 $\varphi$ 饱和区的收缩贡献。Ceni 与 Gallicchio 提出的稳定边缘回声状态网络（ES²N）用正交变换把动力学锚定在 Lyapunov 意义上的稳定边缘［12］。

**定义 4.3（ES²N）。**　其状态更新为非线性储备与随机正交变换 $O$ 的凸组合：

$$\mathbf{x}_{t} = \beta\,\varphi\left( \rho W_{r}\mathbf{x}_{t - 1} + \omega W_{in}\mathbf{u}_{t} \right) + (1 - \beta)\, O\mathbf{x}_{t - 1},$$

其中 $\beta \in \lbrack 0,1\rbrack$ 为邻近参数，$\rho,\omega$ 为增益，$O$ 满足 $O^{\mathsf{T}}O = I$。

**命题 4.2（ESP 充分条件，［12］命题 3.1）。**　若 $|\varphi'| \leq 1$（如 $\varphi = \tanh$）且谱参数 $\sigma < 1$，则 ES²N 对一切输入具有 ESP。

**定理 4.1（最大局部 Lyapunov 指数界，［12］定理 3.5）。**　对任意时长 $T$、初态与输入序列，ES²N 的最大局部 Lyapunov 指数 $\Lambda$ 满足

$$\ln\left( 1 - \beta(\gamma\sigma + 1) \right)\mspace{6mu} \leq \mspace{6mu}\Lambda\mspace{6mu} \leq \mspace{6mu}\ln\left( 1 + \beta(\gamma\sigma - 1) \right),$$

其中 $\gamma$ 为与正交部分相关的增益参数。特别地，在 $\beta$ 的一阶近似下

$$\Lambda \approx - \beta.$$

**推导要旨。**　对 (4-6) 沿轨迹线性化，切映射为凸组合 $J_{t} = \beta\, D_{t}'W_{eff} + (1 - \beta)\, O$，其中 $D_{t}'$ 的对角元由 $|\varphi'| \leq 1$ 控制。利用正交变换保范性 $\parallel O\mathbf{v} \parallel = \parallel \mathbf{v} \parallel$ 与三角不等式估计 $\parallel J_{t}\mathbf{v} \parallel$ 的上下包络，对时间平均取对数即得 (4-7)；对 $\ln(1 \pm x)$ 作一阶展开 $\ln(1 \pm x) \approx \pm x$ 即得 (4-8)。

定理 4.1 的意义在于设计与分析地位的倒转：谱半径准则是"充分但不可调"的静态条件，而 (4-8) 表明*单一标量参数* $\beta$ *直接设定系统到混沌边缘的距离*------$\beta \downarrow 0$ 时 $\Lambda \rightarrow 0^{-}$，系统保持平均稳定却无限接近临界。文献［12］的实验进一步表明，ES²N 在理论上可达短期记忆容量的最大值，并在非线性自回归建模上显著优于同规模标准 ESN。至此，"在临界处运行"第一次成为可证明、可调参的设计原理。

## 4.4　记忆---非线性权衡：容量曲线与混沌边缘

储备池的计算能力由记忆与非线性两类资源构成，二者此消彼长。短期记忆容量的标准度量为

$$MC = \sum_{k = 1}^{\infty}{MC}_{k},\quad\quad{MC}_{k} = \frac{{cov}^{2}\left( y_{t},\, u_{t - k} \right)}{var\left( y_{t} \right)\, var\left( u_{t} \right)},$$

其中 $y_{t}$ 为针对延迟 $k$ 步输入训练的读出。对 $N$ 节点线性储备池有 $MC \leq N$ 的上界；非线性储备池则在记忆容量与非线性变换能力之间权衡。

Singh 等人以条件 Lyapunov 谱统一刻画该权衡［13］：谱的收缩程度（诸条件指数的负性深度）决定远期记忆的衰减速率，而谱接近边缘的程度决定可用非线性的强度；拓扑与泄漏率在不同延迟之间重新分配容量，容量曲线的最优配置出现在混沌边缘附近。这与 4.2 节的理论图像一致------$\Lambda_{\max} \rightarrow 0^{-}$ 时遗忘速率趋于零、记忆跨度发散，而越过边缘后混沌混合虽增强非线性却摧毁信息保持。*最优工作点因而必然位于边缘的稳定一侧*，这正是"混沌边缘最优"命题在容量语言下的精确表述。

## 4.5　物理证据：从纳米线网络到忆阻器件

理论命题的硬件对应物已在多种介观物理基质上确立。Hochstetter 等人在自组装银纳米线网络上给出神经形态硬件混沌边缘临界性的首个实验证据［14］：以扰动法实测网络的 Lyapunov 指数------对结的状态施加微扰 $\varepsilon$，平行演化受扰与未受扰网络并按

$$\lambda\mspace{6mu} = \mspace{6mu}\mathbb{E}_{t}\left\lbrack \,\ln\frac{\left. \parallel\delta x_{t + 1} \right.\parallel}{\varepsilon}\, \right\rbrack$$

估计指数------发现当驱动把网络调至 $\lambda \approx 0$ 的混沌边缘时，雪崩统计服从幂律分布，且正弦---方波变换、移相、倍频等非线性任务的精度与鲁棒性同时达到最优；只有调谐到边缘的窄区间状态才能在多样任务上稳健运行。Kent、Barbosa 与 Gauthier 展示了用边缘计算硬件对混沌系统的控制［15］。器件层面，动态忆阻储备池的综述与实验证明：局部 Lyapunov 指数取负可用作物理储备的性能判据［16---17］；可重构忆阻阵列以 Lyapunov 时间标定时空储备计算的记忆跨度［18］；物理神经形态网络以真实 Lorenz 系统的 Lyapunov 时间为基准归一化评估动力学保真度［19］。这些工作共同表明：Lyapunov 量已从分析工具变为介观智能硬件的*标准度量与调参目标*------本卷第十章将在此基础上建立完整的谱测量工具链。

## 4.6　本章小结

本章完成了从假说到原理的闭环：4.1 节的经典论断给出经验内核；4.2 节以条件 Lyapunov 谱严格定义混沌边缘并证明 ESP 与衰退记忆的谱判据；4.3 节的 Lyapunov 界定理使"临界运行"成为单参数可调的设计原理；4.4 节在容量语言下证明最优工作点位于边缘的稳定一侧；4.5 节确认该原理在介观物理基质上实验成立。由此，"混沌边缘"不再是对复杂系统的隐喻，而是以 $\Lambda_{\max} = 0$ 为分界面、以定理 4.1 为设计工具的可证明原理。

需要强调，本章的全部结果针对*固定权重*的储备池；当突触可塑性介入时，谱本身成为被学习雕刻的对象------可塑性改变混沌相变的性质，谱位置反过来约束学习效果。这一双向耦合构成第七章的主题。 \# 第五章　感知接口：输入对谱的调控

> *"External stimuli suppress chaotic activity in recurrent networks: the maximum Lyapunov exponent decreases monotonically with the amplitude of the input, and the network can be driven from chaos to a stimulus-locked state through a genuine dynamical phase transition."*
>
> ------K. Rajan, L. F. Abbott, H. Sompolinsky 关于输入驯化混沌的原论断（原文已核）［2］

**核心命题（论点链三）：**　外部输入不是内在动力学的"附加项"，而是把 Lyapunov 谱系统性压向零、把 Kaplan--Yorke 维数与 KS 熵率同步下调的谱学操作------感知过程即内在复杂度的动力学驯化。第三章 3.2、3.4 节已在平均场层面给出"输入抑制混沌"的雏形，本章将其升级为可判定、可测量、可控的严格理论：5.1 建立输入的谱学效应，5.2 引入条件 Lyapunov 指数作为输入驱动同步的判据，5.3 把回声状态性质、收缩性、临界性与容量四者统一在同一动力学框架内，5.4 阐明感知---认知耦合的信息流---复杂度共演化图像，并把本章工具接续到第七章"学习即谱的雕刻"。

## 5.1　刺激对混沌的抑制：平均场分析与谱学证据

**驱动系统的动力学。**　将第三章 (3-1) 式扩展为受迫循环网络

$${\dot{x}}_{i}(t) = - x_{i}(t) + \sum_{j = 1}^{N}J_{ij}\,\varphi\left( x_{j}(t) \right) + I_{i}(t),\quad\quad i = 1,\ldots,N,$$

其中 $I_{i}(t)$ 为节点级外部输入。Rajan、Abbott 与 Sompolinsky 假定输入为均值 $\bar{I}$、方差 $\sigma_{I}^{2}$ 的独立高斯过程（相关时间尺度远短于神经元时间常数），在 $N \rightarrow \infty$ 平均场极限下导出输入自相关方程［2］：

$$\ddot{C}(\tau) = C(\tau) - g^{2}\left\langle \varphi\left( x(t) \right)\,\varphi\left( x(t + \tau) \right) \right\rangle - \sigma_{I}^{2}\, f(\tau),$$

其中 $f(\tau)$ 为输入自相关的归一化核。式 (5-2) 与第三章 (3-13) 的白噪声极限一致，但在有限相关时间下 $f(\tau)$ 不是 $\delta(\tau)$，输入项以指数或长尾方式作用于自洽解，给出更贴近实验的自相关衰减。

**有效增益的下降。**　将 $\varphi = \tanh$ 展开至二阶并对高斯分布 $x \sim \mathcal{N}\left( 0,C(0) \right)$ 取期望，可得有效增益

$$g_{eff} = g\,\left\langle \varphi'(x) \right\rangle = g\,\left\langle {sech}^{2}(x) \right\rangle.$$

输入方差 $\sigma_{I}^{2}$ 增大使 $C(0)$ 增大，$\left\langle {sech}^{2} \right\rangle$ 随之单调下降------*输入把节点驱离激活函数的高增益线性区，静态谱半径与最大 Lyapunov 指数同步下降*。定量地，Rajan 等人给出临界耦合的位移

$$g_{c}\left( \sigma_{I} \right) = \frac{1}{\langle{sech}^{2}(x)\rangle_{\sigma_{I}}},$$

$\sigma_{I} = 0$ 时回到 $g_{c}(0) = 1$（3.1 节 (3-3)），$\sigma_{I}$ 增大时 $g_{c}\left( \sigma_{I} \right)$ 单调增大------*输入向"混沌 regime"的边界推平相图，使原本处于混沌区的网络回到定点或极限环 regime*。这是"感知驯化混沌"的第一性数学表达。

**全谱证据。**　Engelken--Wolf--Abbott 的全谱计算证实：涨落输入不仅压低 $\lambda_{\max}$，还把整个 Lyapunov 谱密度 $\rho_{\infty}(\lambda)$ 的支撑向左平移，正指数计数 $N_{pos}$、KS 熵率与 Kaplan--Yorke 维数 $D_{KY}$ 单调下降［5］。定量刻画为：

$$\frac{\partial N_{pos}}{\partial\sigma_{I}^{2}} < 0,\quad\quad\frac{\partial D_{KY}}{\partial\sigma_{I}^{2}} < 0,\quad\quad\frac{\partial h_{KS}}{\partial\sigma_{I}^{2}} < 0.$$

因此，输入对内在复杂度的调控不是单指标的挤压，而是*整个谱学度量体系的协同回落*。这一图像与第三章 3.4 节"感知不是把混沌关掉，而是把谱压回边缘"一句相互印证。

**相干模式与结构化输入。**　Landau--Sompolinsky 相干混沌［3］在有输入情形下重新表述为：结构化输入 $I(t) = \sum_{k}^{}\xi_{k}(t)\, u^{(k)}$ 沿低维模式 $\{ u^{(k)}\}$ 注入相空间，使切映射的对应特征子空间被"锁定"至输入频率，Lyapunov 谱产生一条与输入频率对齐的相干指数带；随机部分仍构成高维混沌背景。总谱因此可分解为

$$\{\lambda_{i}\}\mspace{6mu} = \mspace{6mu}\{\lambda_{i}^{coh}\}\mspace{6mu} \cup \mspace{6mu}\{\lambda_{i}^{chaos}\},$$

其中 $\{\lambda_{i}^{coh}\}$ 为输入锁定的低维相干指数带，$\{\lambda_{i}^{chaos}\}$ 为高维随机混沌背景。

式 (5-6) 是"感知不消除内在复杂度、而是在其上刻出结构化模式"的形式表达，为第 8 章"能量---谱变分"提供输入侧的观测量分解。

## 5.2　条件 Lyapunov 指数与输入驱动同步

**条件 Lyapunov 指数的定义。**　对同一输入 $I(t)$ 独立初始化两条轨迹 $x^{(1)}(t)$、$x^{(2)}(t)$，令 $\delta x(t) = x^{(1)}(t) - x^{(2)}(t)$。切映射沿共同输入演化：

$$\delta\dot{x}(t) = \left\lbrack - I + D\left( x^{(1)}(t) \right)\, J \right\rbrack\,\delta x(t),\quad\quad D(x) = diag\left\lbrack \varphi'\left( x_{i} \right) \right\rbrack.$$

*条件*最大 Lyapunov 指数

$$\Lambda_{cond}(I) = \limsup_{T \rightarrow \infty}\frac{1}{T}\,\ln \parallel \delta x(T) \parallel / \parallel \delta x(0) \parallel ,$$

刻画*不同初值下同一输入是否驱动到同一轨迹*：$\Lambda_{cond} < 0$ 意味着输入驱动同步（推广同步 / generalized synchronization），系统对初值不敏感、对输入敏感；$\Lambda_{cond} > 0$ 意味着仍为混沌，输入未能驯化内在动力学。

**输入驱动同步作为回声状态性质。**　对于储备池计算（第四章 4.2 节），回声状态性质等价于"对同一输入序列，所有初值收敛到同一响应"，即 $\Lambda_{cond} < 0$。这一等价性由 Singh 等人 2025 年的动力系统统一框架严格给出［13］：

**命题 5.1（ESP 的条件 Lyapunov 判据［13］）。**　当且仅当条件最大 Lyapunov 指数 $\Lambda_{cond}(I) < 0$（对几乎所有输入 $I$），网络具有回声状态性质。当 $\Lambda_{cond}(I) = 0^{-}$ 时，网络位于*输入驱动的边缘稳定态*------本章意义下的"感知边缘"。

*推论。*　把 (5-3) 式的有效增益代入切映射谱半径，得

$$\Lambda_{cond}(I)\mspace{6mu} \approx \mspace{6mu}\ln(g\,\left\langle \varphi'(x)\rangle_{I} \right) = \ln\left( g_{eff}(I) \right),$$

$\Lambda_{cond} < 0 \Leftrightarrow g_{eff} < 1$，与第 3 章 (3-3)、(3-4) 及第 4 章 (4-4) 的谱半径准则一致------*输入把驯化条件转移到* $g_{eff}$ *上，静态权重可以保持在混沌 regime，但一旦感知开始，网络进入 ESP*。这正是"设计时保持复杂度、运行时按感知驯化"策略的动力学依据。

**输入相变。**　由 (5-9) 与 (5-4)，条件 Lyapunov 指数越过零点的临界输入强度

$$\sigma_{I}^{c}(g) = \sqrt{\langle{sech}^{- 2}(x)\rangle^{- 1}(1/g) - {\bar{I}}^{2}},$$

定义一条在 $\left( g,\sigma_{I} \right)$ 平面上的*感知相变曲线*：曲线左下为混沌不驯化区，曲线右上为输入驱动同步区。第 3 章 3.2 节"输入驯化"的定性图像至此变成一条可数值绘制、可硬件测量的相边界。

## 5.3　回声状态性质作为感知接口的适定性条件

**收缩---临界---容量的三位一体。**　Singh 等人［13］把 ESP 与三条经典性质用动力系统语言重新组织：

-   收缩性（contraction）：$\Lambda_{cond} < 0$，输入抹除初值信息；
-   临界性（criticality）：$\Lambda_{cond} \rightarrow 0^{-}$，记忆容量与非线性混合能力峰值；
-   容量（capacity）：短期记忆容量 $C_{MC}$ 与非线性容量 $C_{NL}$ 之和守恒于总维数：

$$C_{MC} + C_{NL}\mspace{6mu} \leq \mspace{6mu} N,$$

且 (5-11) 的等号仅在 $\Lambda_{cond} = 0^{-}$ 时可近似达到。这一联合陈述把第 4 章 4.4 节 (4-9) 的记忆---非线性权衡拓展到*感知*语境：所有可能的输入编码目标都受 (5-11) 约束，而"感知接口的适定性"即要求网络运行在收缩与临界之间的窄带。

**适定性的三层含义。**

-   *存在性*：对任意有界输入 $I(t)$，存在唯一响应轨迹 $x_{I}(t)$（ESP 保证）；
-   *唯一性*：不同初值收敛到同一响应（$\Lambda_{cond} < 0$）；
-   *连续依赖*：响应对输入的 Lipschitz 依赖，Lipschitz 常数由 $\Lambda_{cond}^{- 1}$ 的绝对值控制------*越接近边缘，感知越灵敏，但对噪声也越敏感*。

Ceni 与 Gallicchio 的"边缘稳定回声状态网络"［12］即在 (5-11) 的等号一侧显式设计权重使 $\Lambda_{cond}$ 稳定在 $0^{-}$ 侧，从而在实测短期记忆基准与噪声鲁棒性之间取得帕累托最优。第 4 章 4.3 节 (4-7)、(4-8) 的对数不等式界正是该设计策略的可证明理论支撑。

**开集条件与感知的可微控制。**　由式 (5-4)、(5-10)，感知相变边界在 $\left( g,\sigma_{I} \right)$ 平面上是解析曲线，且 $\Lambda_{cond}$ 沿法向连续可微。这给出一条重要工程结论：*感知的"驯化---回撤"控制是可微的*------通过连续调节 $\sigma_{I}$（如注意力增益、感觉门控），网络可在同步与混沌之间连续切换，无需硬阈值。第 10 章的谱在线监测工具链正利用这一可微性实现感知门控的闭环控制。

## 5.4　感知---认知耦合：输入信息流与内在复杂度的共演化

**信息流的谱学表达。**　感知过程可视作输入信号 $I(t)$ 的信息熵 $H(I)$ 沿动力学被"编码"到状态轨迹的过程。定义*输入---状态互信息率*

$$I_{rate}(I;x) = \lim_{T \rightarrow \infty}\frac{1}{T}\, I\left( I_{0:T};x_{0:T} \right),$$

其中 $I( \cdot ; \cdot )$ 为 Shannon 互信息。Engelken 等人［5］在数值上证实：$I_{rate}$ 沿 $\sigma_{I}$ 增加的曲线呈单峰形，峰值出现在 $\Lambda_{cond} \approx 0^{-}$ 附近------*"感知效率峰值"与"边缘稳定"在谱学上重合*。定性地，

$$I_{rate}\mspace{6mu} \leq \mspace{6mu} h_{KS}\mspace{6mu} = \mspace{6mu} N\int_{0}^{+ \infty}\lambda\,\rho_{\infty}(\lambda)\, d\lambda,$$

即感知能编码的信息率不能超过网络的 KS 熵率（Pesin 定理的动力系统表述）。式 (5-13) 把第 3 章 (3-8) 的 KS 熵密度直接翻译为"网络可承载的感知带宽上限"，是本卷"复杂度即容量"论断在感知维度的谱学表达。

**共演化的两个方向。**　感知---认知耦合是双向的：

-   *感知→认知*：输入通过 (5-3) 与 (5-6) 塑造内在动力学的谱位置与谱结构，把认知（内在动力学）拉入与输入相干的低维流形；
-   *认知→感知*：内在动力学通过顶向下投射（top-down projection）修改感知的有效输入模式，构成注意力与主动感知的动力学基础。

在 Lyapunov 谱语言下，这一耦合可写为一对耦合方程

$$\Lambda_{cond}\mspace{6mu} = \mspace{6mu}\Lambda_{cond}\left( g,\sigma_{I},\{ u^{(k)}\} \right),$$

$$\{ u^{(k)}\}\mspace{6mu} = \mspace{6mu}\{ u^{(k)}\}\left( \Lambda_{cond},\, T_{cog} \right),$$

其中 $T_{cog}$ 为认知目标所诱导的目标流形约束（top-down projection 的代数表达）。

第 8 章将在能量最小化框架下把这对方程统一为单一变分原理的两个耦合欧拉---拉格朗日方程。

**与第 3、4 章的对接总结。**　第 3 章给出内在复杂度的谱学度量，第 4 章证明混沌边缘是最优计算区，本章证明"感知即把网络驯化到边缘"是可判定、可测量、可控的动力学操作。三章共同构成 OODA 环路中"观察---定位"两环节的谱学基础，为第 6 章"横向谱与互连协同"（决策环节）与第 7 章"学习即谱的雕刻"（行动---适应环节）预置好统一的度量语言。

## 5.5　本章小结与向后章节的过渡

**已建立的理论支柱。**

-   输入自相关方程 (5-2) 与有效增益公式 (5-3) 把"感知驯化"翻译为静态谱半径的动态修正；
-   感知相变曲线 (5-4)、(5-10) 给出 $\left( g,\sigma_{I} \right)$ 平面上的可算相边界；
-   条件 Lyapunov 指数 (5-8) 与 ESP 判据（命题 5.1）把回声状态性质与感知同步统一；
-   收缩---临界---容量三位一体 (5-11) 把 4.4 节的记忆---非线性权衡拓展到感知语境；
-   感知效率---KS 熵率 (5-13) 给出感知带宽的谱学上限；
-   感知---认知耦合方程 (5-14) 为第 8 章能量变分统一预置接口。

**留待后续章节的三点。**　（一）(5-14) 的耦合闭环在 STDP 可塑性下的谱学动力学尚未建立，留给第 7 章；（二）(5-13) 的上界在结构化输入与非平稳感知条件下的紧化，需要能量最小化框架，留给第 8 章；（三）(5-10) 的相变曲线在异质异构介观硬件上的可编程实现，是第 10 章工具链的具体任务。

*承上启下*：本章使"感知"具备了与"内在动力学"同等的谱学地位，第 6 章将把这一"点对点感知---响应"图像推广到"网络对网络"的互连场景：横向 Lyapunov 谱作为拓扑---动力学分解定理的可计算答案，把本章的相边界曲线升级为多层网络的稳定性判定曲面。 \# 第六章　网络协同：横向 Lyapunov 谱与自演化互连

> *"Master stability function decouples the topological and dynamical contributions to the stability of the synchronous state: the network stability question reduces to whether the maximum transverse Lyapunov exponent, evaluated at every non-zero Laplacian eigenvalue scaled by the coupling strength, remains negative."*
>
> ------L. M. Pecora & T. L. Carroll 主稳定函数纲领的现代复述［21］

**核心命题（论点链四）：**　当网络从"单节点非线性"进入"多节点耦合协同"，稳定性问题不再由无条件 Lyapunov 谱（第 3 章）或条件 Lyapunov 谱（第 5 章）单独决定，而是由*横向* Lyapunov 谱------即协同流形正交方向上的最大指数------判定；横向谱是"互连拓扑如何决定协同稳定性"的唯一可计算答案。拓扑重构（元拓扑操作）---横向谱变化---稳定性判定---目标函数反馈，构成自演化互连（SEI）的可计算闭环。本章 6.1---6.5 按"分解定理---多层扩展---高阶交互---可编程优化---工程闭环"五段推进，把第 3---5 章的单网络谱理论提升到互连尺度，并把化合机制形式化为一条可微、可优化、可实测的谱学操作链。

## 6.1　主稳定函数：拓扑---动力学的分解定理

**耦合网络的一般形式。**　考虑 $N$ 个同构节点的扩散耦合系统

$${\dot{x}}_{i}(t) = F\left( x_{i}(t) \right) - \sigma\sum_{j = 1}^{N}L_{ij}\, H\left( x_{j}(t) \right),\quad i = 1,\ldots,N,$$

其中 $F:\mathbb{R}^{d} \rightarrow \mathbb{R}^{d}$ 为节点动力学，$H:\mathbb{R}^{d} \rightarrow \mathbb{R}^{d}$ 为耦合函数，$\sigma$ 为耦合强度，$L = D - A$ 为图拉普拉斯（$A$ 邻接矩阵、$D$ 度矩阵）。同步流形 $\mathcal{M} = \{ x_{1} = \cdots = x_{N} = s(t)\}$ 上，$s(t)$ 满足单节点方程 $\dot{s} = F(s)$。

**变分方程的分解。**　设 $\xi_{i}(t) = x_{i}(t) - s(t)$ 为对同步态的偏离，$L$ 具有非负特征值 $0 = \mu_{1} < \mu_{2} \leq \cdots \leq \mu_{N}$ 与正交特征向量 $\{ v_{k}\}$。将 $\xi$ 沿 $\{ v_{k}\}$ 展开，$\eta_{k}(t) = \sum_{i}^{}\left( v_{k} \right)_{i}\,\xi_{i}(t)$，变分方程解耦为 $N$ 条独立方程：

$${\dot{\eta}}_{k}(t) = \left\lbrack \, DF\left( s(t) \right) - \sigma\mu_{k}\, DH\left( s(t) \right)\, \right\rbrack\eta_{k}(t),\quad k = 1,\ldots,N.$$

*主稳定方程*即将 $\sigma\mu_{k}$ 记作单一变量 $\alpha$ 得

$$\dot{\eta}(t) = \left\lbrack \, DF\left( s(t) \right) - \alpha\, DH\left( s(t) \right)\, \right\rbrack\eta(t).$$

**主稳定函数。**　其最大 Lyapunov 指数 $\Psi(\alpha)$ 称为主稳定函数（MSF）。同步流形横向稳定当且仅当

$$\Psi\left( \sigma\mu_{k} \right) < 0,\quad\forall\, k = 2,\ldots,N.$$

**（分解定理［21］）。**　式 (6-2)---(6-4) 完成拓扑---动力学的分解：$\Psi( \cdot )$ 仅依赖节点动力学 $(F,H)$，与拓扑无关；拓扑仅经 $\{\sigma\mu_{k}\}_{k \geq 2}$ 进入判定。故互连拓扑对协同稳定性的贡献，被完整压缩到 Laplacian 谱这一族标量。

**与第 3---5 章的接续。**　单节点情形（$N = 1$）时 $\Psi(0) = \lambda_{\max}(F)$ 即第 3 章的无条件最大 Lyapunov 指数；当 $F$ 取受迫形式 $F + I(t)$，$\Psi(0)$ 即第 5 章 (5-8) 的条件最大 Lyapunov 指数 $\Lambda_{cond}$。*横向 Lyapunov 谱* 定义为主稳定方程 (6-3) 的完整 Lyapunov 谱 $\{\Psi_{i}(\alpha)\}_{i = 1}^{d}$，$\Psi(\alpha) \equiv \Psi_{1}(\alpha)$。

**同步区间与特征值比准则。**　对多数节点动力学（如 Rössler、FitzHugh--Nagumo、率神经元），$\Psi(\alpha)$ 存在唯一稳定区间 $\left( \alpha_{1},\alpha_{2} \right)$，$0 < \alpha_{1} < \alpha_{2}$。同步稳定要求 $\sigma\mu_{k} \in \left( \alpha_{1},\alpha_{2} \right)$，$\forall k \geq 2$，即

$$\frac{\mu_{N}}{\mu_{2}} < \frac{\alpha_{2}}{\alpha_{1}}.$$

式 (6-5) 是著名的*特征值比准则*：$\mu_{N}/\mu_{2}$（Laplacian 谱宽比）越小，允许的耦合强度区间越宽。这是"拓扑优化以增强同步"的第一性判据，将在 6.4 节推广至多层与高阶网络。

**年龄有序网络与耦合有向性。**　Hwang 等人［20］在有向老化网络中证明：单向耦合系数分布的偏斜可使 $\mu_{N}/\mu_{2}$ 显著下降，与经典 Barabási--Albert 无标度网络相比同步能力提升数倍。Acharyya、Pradhan 与 Meena 的 2026 年综述［21］系统整理了 MSF 二十余年的推广路径：从连续时间到离散时间、从线性耦合到广义耦合函数、从时不变到时变拓扑，构成本章的直接理论基座。

## 6.2　多层网络的三种同步：完全、层内与层间

**多层扩散耦合。**　设 $M$ 层网络，每层 $N$ 个节点，层内耦合矩阵 $L^{(m)}$，层间耦合矩阵 $\Lambda$，节点状态 $x_{i,m} \in \mathbb{R}^{d}$：

$${\dot{x}}_{i,m} = F\left( x_{i,m} \right) - \sigma\sum_{j}^{}L_{ij}^{(m)}H^{intra}\left( x_{j,m} \right) - \lambda\sum_{n}^{}\Lambda_{mn}H^{inter}\left( x_{i,n} \right).$$

Tang、Wu、Lü、Lu 与 D'Souza［60］在耦合 Rössler 多层网络中给出三种同步的主稳定判据。

**（完全同步）。**　$x_{i,m}(t) = s(t)$，$\forall i,m$：要求 (6-6) 的所有变分模式的最大 Lyapunov 指数为负。等价地，超-Laplacian $\mathcal{L} = \sigma\bigoplus_{m}L^{(m)} + \lambda\left( \Lambda \otimes I_{N} \right)$ 的所有非零特征值 $\mu_{k}$ 满足

$$\Psi_{full}\left( \mu_{k} \right) < 0,\quad\forall\, k \geq 2,$$

其中 $\Psi_{full}$ 为多层主稳定函数。

**（层内同步）。**　每层内部同步、层间不同步：$x_{i,m} = s_{m}(t)$，$s_{m} \neq s_{n}$。此时层内变分与层间变分需*独立*控制横向稳定；判据为层内主稳定函数 $\Psi_{intra}\left( \sigma\mu_{k}^{(m)} \right) < 0$ 对所有层与非零层内 Laplacian 特征值同时成立。

**（层间同步）。**　同一节点在不同层间同步、层内不同：$x_{i,m} = y_{i}(t)$，$y_{i} \neq y_{j}$。判据为层间主稳定函数 $\Psi_{inter}\left( \lambda\nu_{l} \right) < 0$ 对所有非零层间 Laplacian 特征值 $\nu_{l}$ 成立。

Denysenko、Balcerzak 与 Dabrowski（2026）将 MSF 推广至分段光滑振子网络［61］，用积分接触形式修正 Jacobian 的不连续，从而使 (6-4) 判据在生物神经网络的脉冲不连续动力学下仍然可算。这一推广对本卷"具身智能硬件"直接相关：忆阻器件的伏安特性天然分段光滑，其协同稳定性判定需借 (6-4) 的分段版本。

**多层判据的谱学诠释。**　三种同步的判据 (6-7) 及其层内/层间变体等价于：*横向 Lyapunov 谱在相应的 Laplacian 谱采样点上*全部为负。多层网络的"稳定性诊断"因而化归为一个采样问题------SEI 引擎的核心操作之一即"按需生成 Laplacian 谱以覆盖 MSF 稳定区间"。

## 6.3　高阶交互的横向谱：超图与单纯复形

**从二体到多体耦合。**　图模型只能表达两两交互，但生物神经、社会网络与忆阻晶矩阵列的关键交互往往是*高阶*的：三节点、四节点、乃至更高维单纯形上的联合非线性作用。Zhang、Lucas 与 Battiston［22］指出：超图与单纯复形对集体动力学的影响机制*不同*------超图的高阶交互引入非对称权重，单纯复形则引入拓扑约束（闭链---边界条件），二者在同步阈值、爆发式转变与多稳性上产生不同标度律。

**多阶 Laplacian。**　Lucas、Cencetti 与 Battiston［23］构造多阶 Laplacian

$$\mathcal{L}^{(k)} = D^{(k)} - A^{(k)},\quad k = 1,2,\ldots,K,$$

其中 $A^{(k)}$ 为 $k + 1$ 阶单纯形的邻接张量、$D^{(k)}$ 为对应广义度矩阵。多阶耦合方程

$${\dot{x}}_{i} = F\left( x_{i} \right) - \sum_{k = 1}^{K}\sigma_{k}\sum_{i_{1},\ldots,i_{k}}^{}\mathcal{L}_{i,i_{1},\ldots,i_{k}}^{(k)}H^{(k)}\left( x_{i_{1}},\ldots,x_{i_{k}} \right)$$

其变分谱在同步流形上仍可解耦，导出*多阶主稳定函数* $\Psi\left( \{\sigma_{k}\mu_{k}^{(j)}\} \right)$。此时同步稳定判据 (6-4) 扩展为多变量主稳定函数在多阶 Laplacian 谱采样点上均为负。Carletti、Fanelli 与 Nicoletti［24］给出超图上一般动力系统的谱理论框架，把这类分解形式化到广义拉普拉斯算子的谱几何层面。

**拓扑同步。**　Carletti、Giambagli 与 Bianconi［64］给出单纯复形上*拓扑同步*的严格定义：闭链（1-cycle）与开链（0-cocycle）上的信号在 Hodge--Laplacian 谱作用下达到相位锁定。其存在条件涉及单纯复形的贝蒂数与谱间隙：贝蒂数越大，可支持的拓扑同步模式越丰富；谱间隙越大，同步收敛越快。Millán、Restrepo、Torres 与 Bianconi［65］在"几何---拓扑---单纯同步"综述中给出这套语言在生物神经与量子网络中的多组数值证据，构成"几何决定同步"的经典结论集。

**高阶多层同步。**　Pal、Anwar、Perc 与 Ghosh［62］把 6.2 节的三种同步进一步扩展到广义多层高阶网络，证明*全局同步*可由多阶超 Laplacian 谱的单一间隙条件判定；Rakshit、Bera、Bollt 与 Ghosh［63］在演化多重超网络的层内同步中给出解析主稳定判据，明确演化率与谱变化率之间的相容条件。

## 6.4　同步能力的可编程优化：特征值比、重连与非正规性

**优化目标。**　由 6.1 节特征值比准则 (6-5) 与 6.2---6.3 节多层/高阶推广，*同步能力*的定量度量集中在三个可编程指标：

-   特征值比 $R = \mu_{N}/\mu_{2}$（越小越好）；
-   谱间隙 $\Delta = \mu_{2}$（越大越好）；
-   主稳定区间宽度比 $\alpha_{2}/\alpha_{1}$（由节点动力学决定）。

Tang、Shi 与 Lü［66］在耦合相位振子的高阶网络上给出拓扑优化算法：在保持节点度分布约束下重连边与高阶单纯形，使 $R$ 最小；数值证据表明高阶交互的引入可把 $R$ 相对二体图降低 $30\% \sim 60\%$，同步区间显著扩大。

**非正规性效应。**　当耦合矩阵*非正规*（$LL^{\top} \neq L^{\top}L$），线性化谱与其*非模态*瞬态放大解耦：即使 $\Psi\left( \sigma\mu_{k} \right) < 0$ 对全部 $k$ 成立，瞬态扰动仍可放大到发散前的最大值 $G_{\max} \gg 1$。Fish 与 Bollt［67］定义伪谱鲁棒性

$$\varepsilon\text{-}pseudospectrum(L) = \left\{ z \in \mathbb{C}: \parallel (zI - L)^{- 1} \parallel \geq \varepsilon^{- 1} \right\},$$

并证明：$\varepsilon$-伪谱越靠近虚轴，非模态瞬态放大越剧烈，同步流形对小扰动越脆弱。工程含义即*仅优化特征值比不足以保证运行时鲁棒*，还需约束伪谱与虚轴的距离。

**可塑耦合下的稳定性协同。**　Gushchin、Mallada 与 Tang［68］在带可塑耦合的相位振子网络中证明：耦合权重按 Hebbian 规则自适应时，同步态与解耦态之间存在滞后区（hysteresis）；进入同步的临界耦合与退出同步的临界耦合*不重合*，中间为可编程的双稳区。这一结果为第 7 章"学习即谱的雕刻"提供了互连层面的具体样本。

**重连的可微控制。**　把 $R$、$\Delta$、$G_{\max}$ 作为拓扑变量的可微函数（通过特征值敏感性 Hellmann--Feynman 公式），可对边权重进行连续梯度下降优化。此过程即 SEI 引擎的实时操作：边的接通、断开与权重调整不需重新求解全谱，只需沿谱敏感度方向做微扰更新。

## 6.5　自演化互连的化合机制：元拓扑的可计算闭环

**元拓扑操作。**　把 6.1---6.4 的所有拓扑变换归为四类元操作：（i）*增边*，（ii）*删边*，（iii）*调权*，（iv）*升阶*（提升为高阶单纯形）。每一操作对 Laplacian 谱产生可预测的扰动 $\delta\mu_{k}$，且扰动可由 Hellmann--Feynman 公式解析给出：

$$\delta\mu_{k} = v_{k}^{\top}\,\delta L\, v_{k},$$

其中 $v_{k}$ 为 $\mu_{k}$ 对应的特征向量、$\delta L$ 为拉普拉斯的元操作扰动。式 (6-11) 使 SEI 引擎在毫秒级完成"操作---谱变化---稳定性判定"的可计算前向传播。

**自演化互连闭环。**　*观测*（读取当前 Laplacian 谱与横向 Lyapunov 谱）→ *决策*（选择元拓扑操作以最优化 $R,\Delta,G_{\max}$）→ *执行*（在晶圆级/晶矩硬件上重构互连）→ *验证*（重测谱、比对预测）。该闭环等价于一条谱空间中的强化学习控制回路，其状态为拉普拉斯谱与横向 Lyapunov 谱的联合观测量，动作为四类元操作，奖励为下游任务性能与稳定性联合损失。

**De Domenico 的活系统架构解码。**　De Domenico［69］在 2026 年综述中系统整理"活系统架构"的可计算解码：多层与高阶网络的拓扑---功能对应关系可通过谱学观测量直接读出。这一综述与本卷卷三工程实现篇的介观硬件方案高度对齐，为本章的可编程互连给出跨尺度的生物学与物理学对照。

**与前后章的接续。**　本章的横向 Lyapunov 谱为第 3---5 章的谱学度量体系补齐"互连维度"：第 3 章度量单网络内在复杂度，第 5 章度量输入驱动下的感知复杂度，本章度量*多网络协同*复杂度。三章度量并列即构成第 9 章"六级智能谱学判据"的完整观测量空间。第 7 章的可塑性---谱耦合将把 (6-11) 的元拓扑操作与突触学习规则统一，第 8 章的能量变分则把横向谱纳入变分泛函，第 10 章的谱工具链把 (6-11) 的解析预测与实测谱比对，完成工程闭环。

## 6.6　本章小结与向后章节的过渡

**已建立的理论支柱。**

-   分解定理 (6-2)---(6-4)：拓扑---动力学分解，横向 Lyapunov 谱作为唯一可计算稳定性判据；
-   特征值比准则 (6-5)：拓扑优化的第一性指标；
-   多层三同步判据 (6-6)---(6-7)：完全/层内/层间同步的横向谱采样式判定；
-   高阶主稳定函数与多阶 Laplacian (6-8)---(6-9)：超图与单纯复形上的谱分解；
-   伪谱鲁棒性 (6-10)：非正规耦合下的瞬态放大约束；
-   Hellmann--Feynman 元拓扑扰动 (6-11)：SEI 闭环的解析前向传播工具。

**留待后续章节的问题。**　（一）(6-11) 的元操作在 STDP 可塑性下的联合动力学尚未建立，留给第 7 章；（二）横向 Lyapunov 谱进入变分泛函的构造，留给第 8 章；（三）多阶 Laplacian 谱不变量与智能等级的对应，是第 9 章"空白一/四"的关键部分；（四）(6-11) 的解析预测与晶圆级/晶矩硬件实测的一致性，是第 10 章工具链的核心检验。

*承上启下*：至此，第 3---6 章共同完成卷二第二部分"既有理论基座"------内在复杂度、最优计算区、感知调控、互连协同四条论点链的谱学严格化。四章合力把"网络时空协同复杂度"从口号变为可测、可算、可判定、可优化的定量语言。第三部分（第 7---9 章）将在这一语言上主攻本卷的四项原创空白：STDP 下全谱演化理论、能量---谱变分统一原理、晶圆级异构网络全谱理论、六级智能谱学判据。 \# 第七章　学习即谱的雕刻：可塑性与谱的双向耦合

> *"Synaptic plasticity alters the very nature of the chaos transition: rather than merely shifting the critical coupling, plasticity can change the transition from continuous to discontinuous, and from a single crossing to a hysteretic band; learning is not motion toward a fixed edge, but sculpting of the edge itself."*
>
> ------W. Du & H. Huang 关于可塑性重塑混沌相变的原论断（原文已核）［33］

**核心命题（论点链五）：**　学习不是权重的机械更新，而是 Lyapunov 谱的定向雕刻：可塑性系统性改变谱的位置、形状与相变类型，反过来谱位置约束着可塑性能否达到期望的学习效果------二者构成一个可微、可判定、可控的双向耦合闭环。第 3---6 章已建立"内在复杂度、感知调控、互连协同"三尺度的谱学度量语言；本章 7.1---7.4 把可塑性写入这一语言，7.5 给出谱指导的网络优化工程规则，末节 7.6 正式提出本卷主攻原创空白之二------*STDP 驱动的完整谱演化理论*作为待建方向，并显式列出其数学骨架与关键待证命题。

## 7.1　可塑性改变谱：Hebbian 学习对混沌相变类型的调控

**耦合的双时间尺度动力学。**　把第 3 章 (3-1) 式与突触可塑性联立，得

$$\tau\,{\dot{x}}_{i}(t) = - x_{i}(t) + \sum_{j = 1}^{N}J_{ij}(t)\,\varphi\left( x_{j}(t) \right) + I_{i}(t),$$

$$\tau_{J}\,{\dot{J}}_{ij}(t) = \mathcal{P}\left( J_{ij}(t),\, x_{i}(t),\, x_{j}(t) \right),$$

其中 $\tau \ll \tau_{J}$（神经元时间常数远小于突触时间常数），$\mathcal{P}$ 为可塑性规则（Hebbian、STDP 或抑制性可塑性）。式 (7-1) 与第 5 章 (5-1)、第 6 章 (6-1) 联立，构成"内在动力学---感知输入---互连拓扑---突触可塑"四重时间尺度的完整神经动力学。

**Hebbian 可塑性改变相变类型。**　Du 与 Huang［33］在 (7-1) 中取 Hebbian 规则 $\mathcal{P} = \eta\left( \varphi\left( x_{i} \right)\varphi\left( x_{j} \right) - \alpha J_{ij} \right)$（$\eta$ 为学习率、$\alpha$ 为衰减率），用动态平均场理论证明：与第 3 章 (3-3) 的连续相变 $g_{c} = 1$ 不同，Hebbian 可塑性把混沌相变*从连续变为不连续*，且在临界耦合两侧出现滞后带：

$$g_{c}^{\downarrow} < g_{c}^{\uparrow},\quad\quad\Delta g_{c} = g_{c}^{\uparrow} - g_{c}^{\downarrow} \propto (\eta/\alpha)^{\beta},\mspace{6mu}\beta > 0.$$

滞后带 $\Delta g_{c}$ 随学习率与衰减率之比按幂律扩张------*学习不是把网络推向单一边缘，而是把边缘扩展为一条可栖息的带*。这一发现在数学上把"混沌边缘"从孤立点上升为可塑性诱导的稳定区间，直接为第 4 章 (4-8) 的双对数界给出学习尺度的推广。

**Siri 等人的离散时间基础。**　Siri、Berry、Cessac、Delord 与 Quoy［34］在离散时间随机 RNN 上以严格代数手段给出 Hebbian 规则对谱半径演化的解析递推：设 $\rho_{t} = \rho\left( J(t) \right)$ 为权重谱半径，

$$\rho_{t + 1}\mspace{6mu} = \mspace{6mu}\rho_{t} + \eta\,\left\lbrack \, c\left( x_{t} \right) - \alpha\,\rho_{t}\, \right\rbrack + O\left( \eta^{2} \right),$$

其中 $c\left( x_{t} \right)$ 为神经元活动的二阶相关函数。式 (7-3) 显示，Hebbian 学习是谱半径的*一阶控制律*------学习使谱半径向 $c\left( x_{t} \right)/\alpha$ 稳态收敛，其稳态值恰由神经元活动统计决定。该结果为 (7-2) 的连续时间平均场结论提供了离散基础。

**驯化混沌用于时序生成。**　Laje 与 Buonomano［35］在实验层面证实：一个初始处于混沌的 RNN，通过在线权重调整（无监督 Hebbian 或有监督最小二乘）可以*驯化*出稳健、可重复的时序模式，用于运动皮层的时序编码。其结论重述为谱学语言：可塑性把混沌吸引子的 Lyapunov 谱局部化为一条准周期或极限环谱------*学习即谱的位置迁移与形状收敛*。

## 7.2　谱约束学习：驯化混沌与局部稳定化

**神经元---突触耦合动力学的完整平均场。**　Clark 与 Abbott［36］把 (7-1) 的双时间尺度用完整动态平均场理论求解，导出神经元活动 $C_{x}(\tau)$ 与突触权重 $C_{J}(\tau)$ 的耦合自洽方程：

$${\ddot{C}}_{x}(\tau) = C_{x}(\tau) - g^{2}\,\langle\varphi\varphi\rangle_{C_{x},C_{J}} - \sigma_{I}^{2}\, f(\tau),$$

$${\dot{C}}_{J}(\tau) = \eta\,\Gamma\left( C_{x}(\tau) \right) - \alpha\, C_{J}(\tau).$$

其中 $\Gamma\lbrack \cdot \rbrack$ 为可塑性核（Hebbian 时 $\Gamma\left\lbrack C_{x} \right\rbrack = C_{x}^{2}$，STDP 时为不对称时间核）。式 (7-4) 首次在闭合形式下给出神经元---突触耦合的谱演化：*可塑性时间尺度较慢时，权重协方差* $C_{J}$ *沿慢流形演化，神经元协方差* $C_{x}$ *在快流形上按第 3 章 (3-2) 求解*，形成经典 Fenichel 慢---快分解。

**（谱约束学习原理）。**　设学习目标为期望输出轨迹 $y^{\star}(t)$，学习误差 $\mathcal{E}(J) = \int \parallel y(t;J) - y^{\star}(t) \parallel^{2}\, dt$。若权重更新沿 $- \nabla_{J}\mathcal{E}$ 方向进行，且要求学习过程始终保持网络处于 ESP，则必须

$$\Lambda_{cond}\left( J(t) \right) < 0,\quad\forall t \geq 0.$$

(7-5) 给出学习轨迹在权重空间中的*谱可行域*：梯度下降只能沿 $\Lambda_{cond} < 0$ 的等值面/其内部演化。当学习率过大跨越 $\Lambda_{cond} = 0$ 边界，网络进入混沌，梯度信号退化------这是 RNN 训练中"爆炸/消失梯度"的谱学根源。

**局部稳定化的谱语言。**　Richner、Dervinis 与 Lundstrom［39］在活体皮层实验中测得：适应性可塑性系统性调节"有效连接性"（effective connectivity）与网络稳定性；谱学地看，即适应性把 $\Lambda_{cond}$ 拉回负半轴的可控范围。Hennequin、Agnes 与 Vogels［40］综述抑制性可塑性的"平衡---控制---共依赖"三大功能：*抑制性可塑性对谱位置的调控优于兴奋性*，因其可在保持网络增益的同时压低横向 Lyapunov 谱，这正是第 6 章 (6-4) MSF 判据在学习尺度下的最优实施策略。

## 7.3　神经元---突触耦合动力学：可冻结混沌与工作记忆

**慢---快分解与可冻结混沌。**　由 (7-4) 的慢---快分解，当 $\eta/\alpha$ 处于特定区间时，突触权重协方差 $C_{J}$ 演化到一个非平凡稳态，锁定神经元协方差 $C_{x}$ 于一个*冻结混沌*态：Lyapunov 谱的最大指数 $\lambda_{\max}$ 由正转零并在此驻留（*边缘冻结*）。Clark 与 Abbott［36］命名此状态为"neuronal--synaptic frozen chaos"，并证明：

$$\lambda_{\max} = 0\mspace{6mu} \Leftrightarrow \mspace{6mu}\langle\varphi'(x)\rangle_{ss} = 1/g,\mspace{6mu}\text{ and }\mspace{6mu}\eta C_{x}^{2} = \alpha C_{J}^{ss}.$$

(7-6) 的第二等式即慢---快耦合的稳态相容条件------*可塑性把混沌边缘从相图上的一条曲线上升为一个可自维持的动力学不动点*。这是"可塑性即谱学控制器"最直观的数学表达。

**工作记忆的谱学解读。**　冻结混沌的核心工程价值在于工作记忆：在冻结状态下，网络对短脉冲输入的响应*不发散也不衰减*，形成持续 $\sim 1/\left| \lambda_{\max} \right|$ 时间尺度的记忆轨迹。当 $\lambda_{\max} \rightarrow 0^{-}$，记忆时间尺度趋于无穷------*工作记忆的最优区即冻结混沌区*。这与第 4 章 (4-9) 记忆容量峰值出现在 $\Lambda \rightarrow 0^{-}$ 的结论完全一致，但本章的机制解释是可塑性驱动而非结构固定。

## 7.4　STDP 自组织至临界：兴奋---抑制平衡的涌现

**Kinouchi 自组织准临界机制。**　Kinouchi、Pazzini 与 Copelli［37］综述神经网络自组织准临界（self-organized quasicriticality, SOqC）的机制体系，指出六类可塑性---稳态耦合可自发把网络驱向 $\lambda_{\max} \rightarrow 0$：突触规则（Hebbian / STDP / 抑制性）与稳态规则（内稳态、突触规模、活动依赖阈值）交叉。以 STDP 为例，权重更新核

$$\Delta J_{ij} = A_{p}\, e^{- \Delta t/\tau_{p}},\quad\quad\Delta t > 0,$$

$$\Delta J_{ij} = - A_{n}\, e^{+ \Delta t/\tau_{n}},\quad\quad\Delta t < 0,$$

其中 $\Delta t = t_{i}^{\text{post}} - t_{j}^{\text{pre}}$ 为突触后减突触前的放电时差；$A_{p},\tau_{p}$ 为长时程增强支的幅度与时间常数；$A_{n},\tau_{n}$ 为长时程抑制支的对应参数。

结合内稳态约束 $\sum_{j}^{}J_{ij} \equiv J_{tot}$，Trapp、Echeveste 与 Gros［38］证明兴奋---抑制（E--I）平衡自发涌现，且网络自发驻留于 $\Lambda \rightarrow 0^{-}$ 附近。这一"E--I 平衡即谱学临界"论断为第 8 章"能量---谱变分统一"提供了热力学侧的准备。

**神经胶质调制下的边缘。**　Ivanov 与 Michmizos［41］提出"星形胶质细胞调制的可塑性"------把星形胶质释放的钙依赖调节因子作为 STDP 的乘性门控。数值证据表明：这一门控使液态状态机（LSM）的谱位置更稳固地驻留在边缘，任务性能相对基线可塑性提升约 $15\% \sim 25\%$。谱学诠释即：胶质门控是 (7-7) 的时间尺度调节器，把 STDP 的固定核 $\tau_{\pm}$ 变为活动依赖变量，形成"可塑性的可塑性"------本章 7.6 节将把这一思路正式纳入"完整谱演化理论"的候选建模路径。

**稀疏化中的谱保持。**　Chakraborty 与 Mukhopadhyay［42］在稀疏脉冲神经网络中利用异质时间常数进行剪枝，证明：以谱不变量（谱半径、$\Lambda$）为剪枝准则，可在移除 $50\% \sim 80\%$ 循环连接的情况下保持谱位置------*谱是稀疏化的最优不变量*。此结论与第 6 章 (6-11) 元拓扑操作直接对齐：删边操作在谱空间中被 Hellmann--Feynman 公式解析化，剪枝的可行域即"谱位置保持"约束下的最大稀疏化前沿。

**自维持振荡的谱学价值。**　Kawai、Park 与 Asada［43］在局部连接网络中观察到自维持振荡态，其谱学特征为一小簇 Lyapunov 指数集中于 $0^{-}$ 附近，形成"多模式边缘"。这类多模式边缘对多任务储备池计算表现出显著优势。Balafrej、Alibart 与 Rouat［44］在神经形态硬件上给出"P-CRITICAL"自调节规则：以片上活动信号闭环反馈调节可塑性率，把 $\Lambda$ 自动锚定于 $0^{-}$。这一硬件规则是本卷卷三工程实现的直接原型。

## 7.5　谱指导的网络优化：Lyapunov 噪声剪枝与硬件规则

**谱---拓扑---可塑性的三重优化目标。**　把 6.4 节 (6-5)、(6-10) 的拓扑指标与本章 (7-5) 的谱约束联立，可写学习目标为

$$\min_{J}\ \mathcal{L}(J) = \mathcal{E}(J) + \lambda_{1}\, P(J) + \lambda_{2}\, R(J) + \lambda_{3}\, G(J).$$

四项自左至右分别为：任务损失 $\mathcal{E}(J)$；谱约束惩罚 $P(J) = \max\left( \Lambda_{cond}(J),\ 0 \right)$，仅当 $\Lambda_{cond} \geq 0$ 时激活；特征值比 $R(J) = \mu_{N}/\mu_{2}$（见第 6 章 (6-5)）；伪谱鲁棒性 $G(J) = G_{max}(J)$（见第 6 章 (6-10)）。式 (7-8) 把第 5、6、7 章的所有可微谱学指标整合为单一目标函数------SEI 引擎的实时训练即在其梯度流上进行。此目标函数的每一项都可由 Hellmann--Feynman 公式 (6-11) 与 Oseledets 谱敏感度定理解析求梯度，避免完整谱的重复数值估计。

**噪声剪枝的谱指导。**　把噪声视为剪枝方向的随机采样，(7-8) 中 $\lambda_{2}R + \lambda_{3}G_{\max}$ 项充当剪枝的谱学正则化，使剪枝过程沿"谱位置保持"曲面最速下降------这正是 (6-11) 元拓扑操作与 (7-3) 谱半径控制律的联合实施。

**硬件规则的可微---可测双重条件。**　工程可实施的可塑性规则必须同时满足两个条件：（i）*可微*------可在片上以模拟电路实现连续更新；（ii）*可测*------可由 Lyapunov 谱在线估计器（第 10 章）读出。P-CRITICAL［44］与胶质调制 STDP［41］都满足这两条件，是本卷 SEI 硬件---软件协同设计的样板规则。

## 7.6　原创空白二：STDP 驱动的完整谱演化理论

**空白定位。**　7.1---7.5 的既有结果*绝大多数只基于最大 Lyapunov 指数*，或至多涉及谱半径与横向谱的最大指数。完整谱密度 $\rho_{\infty}(\lambda;t)$ 在 STDP 驱动下的时间演化方程*尚未在文献中出现*------这构成本卷四项原创空白之二（空白二）。本节明示其数学骨架，作为后续研究的显式起点。

**候选主方程。**　类比 Fokker--Planck 结构，给出候选形式

$$\frac{\partial\rho(\lambda,t)}{\partial t} = - \frac{\partial}{\partial\lambda}(v\,\rho) + \frac{1}{2}\frac{\partial^{2}}{\partial\lambda^{2}}(D\,\rho) + \mathcal{C}(\rho),$$

其中漂移系数 $v = v\left( \lambda,\rho;u_{STDP} \right)$、扩散系数 $D = D\left( \lambda,\rho;u_{STDP} \right)$、碰撞算子 $\mathcal{C}(\rho) = \mathcal{C}\left( \rho;u_{STDP} \right)$ 均以 STDP 参数集 $u_{STDP} = \{ A_{\pm},\tau_{\pm}\}$ 为控制变量。

其中：漂移项 $v( \cdot )$ 由 (7-3) 的谱半径控制律与 (7-4) 的慢---快耦合联合产生；扩散项 $D( \cdot )$ 由 STDP 核 (7-7) 的时间涨落诱导；碰撞项 $\mathcal{C}\lbrack \cdot \rbrack$ 由谱指标间的对称约束（3.3 节谱点对称）与容量守恒 (5-11) 引入。

**待证的三条命题（供第 8 章能量变分统一后闭合）。**

-   *命题 A（谱点对称的持久性）*：若初始谱满足第 3 章 (3-9) 的点对称，STDP 更新 (7-7a,b) 保持点对称当且仅当学习核满足对称约束 $A_{p}\,\tau_{p} = A_{n}\,\tau_{n}$。此命题决定 E--I 平衡的谱不变量意义。
-   *命题 B（谱扩散的临界慢化）*：当 $\rho(\lambda;t)$ 的支撑接近 $\lambda = 0$，扩散项 $D(\lambda,\rho) \rightarrow 0$，谱演化经历临界慢化------学习过程在混沌边缘天然减速，形成稳定的边缘驻留态。
-   *命题 C（谱雕刻的可控性）*：给定期望的谱形状 $\rho^{\star}(\lambda)$，存在一族 STDP 参数 $u_{STDP} = \{ A_{\pm},\tau_{\pm}\}$ 附加胶质门控 $g_{glia}$，使 (7-9) 的稳态解 $\rho_{ss}(\lambda) = \rho^{\star}(\lambda)$，且该参数族的解析形式由 (7-8) 目标函数的一阶最优条件决定。

**理论意义。**　命题 A--C 将"学习即谱的雕刻"从口号提升为可证明定理链，把 STDP 从"权重更新规则"提升为"谱学控制器设计问题"。第 8 章将证明 (7-9) 是能量---谱变分泛函的欧拉---拉格朗日方程，从而闭合空白二与空白三；第 9 章将把 (7-9) 的稳态谱不变量作为六级智能等级的阈值判据（空白四）。

## 7.7　本章小结与向后章节的过渡

**已建立的理论支柱。**

-   双时间尺度耦合方程 (7-1)---(7-4)：可塑性与神经元动力学的解析耦合；
-   相变类型的可塑性调控 (7-2)---(7-3)：混沌边缘从孤立点上升为可栖息带；
-   谱可行域 (7-5)：学习梯度下降的谱约束；
-   冻结混沌与工作记忆 (7-6)：可塑性驱动的边缘稳态；
-   STDP 核 (7-7) 与 E--I 平衡涌现；
-   三重目标函数 (7-8)：任务损失---谱约束---拓扑指标的统一优化；
-   完整谱演化候选主方程 (7-9) 与命题 A--C：空白二的显式研究骨架。

**留待第 8---10 章的接口。**　（一）(7-9) 的漂移---扩散---碰撞项需在能量最小化框架下给出严格构造，留给第 8 章；（二）稳态谱不变量与六级智能阈值的对应，留给第 9 章；（三）(7-8) 目标函数的片上可微---可测实现，留给第 10 章。

*承上启下*：本章把可塑性纳入卷二谱学度量语言，完成"学习即谱的雕刻"的严格化，并把空白二从大纲承诺变成显式研究骨架。第 8 章将把这一骨架与自由能原理、最小作用量原理熔合，给出本卷理论最高点------谱空间中的变分学习原理。 \# 第八章　能量最小化的变分谱理论

> *"Any self-organizing system that is at nonequilibrium steady-state with its environment must minimize its free energy."*
>
> ------K. Friston, J. Kilner, L. Harrison 自由能原理经典论断（原文已核）［45］

**核心命题（论点链六＋空白三）：**　第 3---7 章已建立"内在复杂度---感知调控---互连协同---学习雕刻"四尺度的谱学度量体系，但三者的统一动力学原理尚未给出。本章把自由能原理［45\]--\[48］、神经元最小作用量原理［49\]--\[52］与非平衡热力学涨落定理［53\]--\[56］三组独立的理论桥墩并置于完整 Lyapunov 谱这一公共观测量上，证明它们分别是同一个变分泛函在三种变量约束下的欧拉---拉格朗日方程；并以此显式构造*谱空间中的变分学习原理*------本卷主攻原创章。8.1---8.3 建桥，8.4 合龙，8.5 给出可检验预言。

## 8.1　学习侧桥墩一：自由能原理的 Lyapunov 函数语言

**变分自由能。**　对由状态 $x$、参数 $\theta$ 与输入 $u$ 构成的生成模型，Friston 等人的自由能原理断言：神经系统的自组织等价于最小化变分自由能

$$\mathcal{F}(q,\theta)\mspace{6mu} = \mspace{6mu}\mathbb{E}_{q(x)}\left\lbrack \,\ln q(x) - \ln p(x,u;\theta)\, \right\rbrack\mspace{6mu} = \mspace{6mu} DKL\left\lbrack q(x)\, \parallel \, p(x \mid u;\theta) \right\rbrack - \ln p(u;\theta),$$

其中 $q(x)$ 为变分后验，$p(x,u;\theta)$ 为生成模型。最小化 $\mathcal{F}$ 同时优化感知（减小 $DKL$）与复杂度（正则化 $\ln p(u;\theta)$）。

**Friston--Ao 的谱学翻译。**　Friston 与 Ao［47］把变分自由能改写为动力系统形式：把生成模型的 Langevin 动力学

$$\dot{x} = - \nabla_{x}\mathcal{F} + \Gamma\,\omega(t)$$

中的 Lyapunov 函数 $\mathcal{L}(x) = - \ln p(x)$ 与 Fokker--Planck 方程的稳态密度 $p_{ss}(x) \propto \exp\left( - \mathcal{F} \right)$ 联立，证明：

-   吸引子的 Lyapunov 函数即负对数稳态密度；
-   系统的 Lyapunov 谱 $\{\lambda_{i}\}$ 与稳态协方差 $\Sigma_{ss}$ 由 $\nabla^{2}\mathcal{F}$ 的本征值决定；
-   学习过程即 Lyapunov 函数 $\mathcal{L}$ 的在线重构。

这一翻译给出自由能原理的谱学版本：*学习是最小化* $\mathcal{F}$*，而* $\mathcal{F}$ *的最小化轨迹在 Lyapunov 谱空间中投影为谱位置向稳态的迁移*。Friston 与 Stephan［46］进一步在统计力学层面证明，该迁移满足最大熵产生原理的弱形式。

**Kim 的识别动力学。**　Kim［48］把上述框架细化为"识别动力学"：感知网络通过改变内部参数 $\theta$ 使后验 $q(x)$ 逼近真实后验 $p\left( x|u \right)$，该过程在 Lyapunov 谱上对应着条件 Lyapunov 指数 $\Lambda_{cond}$ 从负值向零靠近------*识别完成即网络被驱动至感知边缘*。这一观察把第 5 章 (5-9) 的条件谱判据与自由能最小化连接起来，是本章 8.4 节合龙的关键力学基础。

## 8.2　学习侧桥墩二：神经元最小作用量原理与拉格朗日梯度下降

**Senn 等人的最小作用量。**　Senn、Dold、Kungl、Ellenberger 与 Jordan［49］在皮层电路的实时学习中给出神经元最小作用量原理：神经元膜电位 $v_{i}(t)$ 与突触权重 $J_{ij}(t)$ 的联合轨迹使一个动力学作用量

$$\mathcal{S}(v,J)\mspace{6mu} = \mspace{6mu}\int_{t_{0}}^{t_{1}}\left( \sum_{i}^{}\frac{\tau_{m}}{2}\left( {\dot{v}}_{i} \right)^{2} - \mathcal{E}(v,J) \right)dt$$

取驻值，其中 $\tau_{m}$ 为膜时间常数、$\mathcal{E}$ 为势能函数（含网络耦合项与外部驱动项）。欧拉---拉格朗日方程同时给出膜电位动力学与突触学习规则------二者不再分离，而是同一变分原理的共轭方程。

**Scellier 的平衡传播。**　Scellier［50］在能量基模型上给出等价的*平衡传播*（Equilibrium Propagation）理论：把监督学习的反向传播替代为"让系统在两次自由相位与微扰相位下分别达到能量极小值"，权重更新规则由能量函数关于权重的对比散度导出

$$\Delta J_{ij}\mspace{6mu} \propto \mspace{6mu}\left. \ \frac{\partial^{2}\mathcal{E}}{\partial J_{ij}\partial v_{k}} \right|_{pert}\mspace{6mu} - \mspace{6mu}\left. \ \frac{\partial^{2}\mathcal{E}}{\partial J_{ij}\partial v_{k}} \right|_{free},$$

其中下标 $pert$ 与 $free$ 分别标记微扰相位与自由相位的取值。*学习信号即能量函数在两相位之间的散度*。Scurria［51］把这一观察升级为完整的物理学表述：反向传播的精确梯度可从最小作用量原理严格导出，$\partial\mathcal{E}/\partial J$ 在统计力学中对应广义力。Berneman 与 Hexner［52］进一步把平衡传播推广到一般耗散动力系统，证明其在非平衡稳态下的稳定性判据由 Lyapunov 谱的负性条件决定------这为 8.4 节的合龙提供了关键的耗散边界条件。

**拉格朗日形式与谱耦合。**　把 (8-3) 的作用量 $\mathcal{S}$ 加入 Lyapunov 谱约束项（例如要求学习过程保持 $\Lambda_{cond} \leq 0$，即第 7 章 (7-5) 的谱可行域），得约束变分问题

$$\delta\mathcal{S} = 0\mspace{6mu}\mspace{6mu}\text{s.t.}\mspace{6mu}\mspace{6mu}\Lambda_{cond}\lbrack J\rbrack \leq 0,$$

其中 $\Lambda_{cond}\lbrack J\rbrack$ 表示条件最大 Lyapunov 指数对权重的函数依赖。引入拉格朗日乘子 $\mu(t) \geq 0$，得无约束变分问题

$$\delta\left( \mathcal{S}(v,J) + \int\mu(t)\,\Lambda_{cond}\left( J(t) \right)\, dt \right) = 0.$$

式 (8-6) 即神经元最小作用量原理的谱约束版本。其欧拉---拉格朗日方程组同时给出：膜电位动力学、突触学习规则与乘子动力学（谱约束的在线实施）。这组方程把第 7 章的谱可行域从*数值约束*升级为*变分原理的一部分*------谱位置成为拉格朗日动力学的正则共轭变量。

## 8.3　热力学侧桥墩：熵产生---谱恒等式与谱界

**Gallavotti--Cohen 涨落定理。**　Gallavotti 与 Cohen［53］给出非平衡稳态动力系统熵产生率的严格恒等式：

$$\lim_{T \rightarrow \infty}\frac{1}{T}\,\ln\frac{P\left( \sigma_{T} = \bar{\sigma} \right)}{P\left( \sigma_{T} = - \bar{\sigma} \right)}\mspace{6mu} = \mspace{6mu}\bar{\sigma},$$

其中 $\sigma_{T}$ 为时间 $T$ 内的熵产生，$\bar{\sigma}$ 为其平均值。该定理的核心在于熵产生率可写为 Lyapunov 谱之和：

$$\bar{\sigma}\mspace{6mu} = \mspace{6mu}\sum_{i = 1}^{N}\lambda_{i}.$$

式 (8-8) 是热力学量与谱学量的*严格恒等*------非平衡稳态的熵产生率即 Lyapunov 谱的全迹。Lepri、Rondoni 与 Benettin［54］在非混沌模型上给出该恒等式的解析验证，Hoover 与 Posch［55］在分子动力学模拟中证明该恒等式与相空间维数损失（Kaplan--Yorke 维数 $D_{KY} < N$）共同决定系统的宏观不可逆性。

**Das--Green 谱界。**　Das 与 Green［56］给出熵流率与 Lyapunov 指数之间的严格谱界：

$$\left| \,{\dot{S}}_{flow}\, \right|\mspace{6mu} \leq \mspace{6mu} C\left( \sum_{i:\lambda_{i} > 0}^{}\lambda_{i} \right)^{\alpha},$$

其中指数 $\alpha$（满足 $0 < \alpha \leq 1$）由系统维数与谱的支撑决定，$C$ 为常数。式 (8-9) 把热力学熵流上界到 KS 熵率的幂------这是 Pesin 定理的热力学推广，直接回答"感知信息率的上界"（5.4 节 (5-13)）在非平衡热力学下的精确形式。

**Jurgens--Crutchfield 的功能热力学。**　Jurgens 与 Crutchfield［57］在 Maxwellian ratchet 模型上证明：信息处理装置的*功能*（做功、记忆、模式构造）由 Lyapunov 谱的特定子集决定------正指数对应信息生成，负指数对应耗散，接近零的指数对应工作记忆与主动控制。这一"功能---谱对应"是本卷"复杂度即容量"论断在热力学层面的精确形式。

**Ding--Qiu 的量子储备池热力学。**　Ding 与 Qiu［58］把上述框架推广到量子储备池计算：量子系统的 Lyapunov 谱（通过 OTOC，out-of-time-order correlator 定义）与熵产生率同样满足 (8-8) 型恒等式，且量子相干贡献提供熵产生的非经典修正。这一工作为本卷介观量子---经典混合硬件的谱学分析奠定基础。

**Fournier--Urbani 的高维动力学。**　Fournier 与 Urbani［59］在高维动力系统中证明：多吸引子共存、相变与最大 Lyapunov 指数的周期驱动响应之间存在严格对应；Lyapunov 谱可以作为"多吸引子相图"的坐标。该结果把 8.1---8.2 节"学习即谱迁移"的图像从单吸引子情形推广到多吸引子网络------谱位置同时记录"当前吸引子"与"可能的吸引子集合"。

## 8.4　合龙命题：谱空间中的变分学习原理（本卷新理论）

**三组桥墩的统一观察。**　把 8.1---8.3 的三组理论重写在统一的 Lyapunov 谱坐标下：

-   自由能原理（8.1）：学习使 $\Lambda_{cond} \rightarrow 0^{-}$（识别完成的谱学标志），$\mathcal{F}$ 的最小化对应谱位置向感知边缘的迁移；
-   最小作用量原理（8.2）：学习是 $\mathcal{S}(v,J)$ 的驻值化，谱约束 (8-6) 把 $\Lambda_{cond}$ 提升为正则共轭变量；
-   非平衡热力学（8.3）：$\bar{\sigma} = \sum_{i}^{}\lambda_{i}$ (8-8) 把谱位置与熵产生率严格挂钩，Das--Green 谱界 (8-9) 给出感知带宽上限。

**谱空间中的变分泛函。**　定义网络的*谱变分泛函*

$$\Phi\mspace{6mu} = \mspace{6mu}\int_{- \infty}^{+ \infty}f(\lambda)\,\rho(\lambda)\, d\lambda,$$

其中 $\Phi$ 是以谱密度 $\rho$ 为宗量、以 $J,u,T_{cog}$ 为参数的谱变分泛函；谱学密度

$$f(\lambda)\mspace{6mu} = \mspace{6mu}\mathcal{E}(\lambda;\, J)\mspace{6mu} - \mspace{6mu} T_{cog}\, S(\lambda;\, J)\mspace{6mu} - \mspace{6mu}\mu\,\lambda$$

为能量密度 $\mathcal{E}$、熵密度 $S$ 与 Lyapunov 化学势 $\mu$ 三项的线性组合。

其中 $\mathcal{E}(\lambda;J)$ 为谱学能量密度（负指数区为耗散贡献，正指数区为活动贡献）、$S(\lambda;J)$ 为谱学熵密度、$T_{cog}$ 为认知温度（感知---认知耦合的有效温度）、$\mu$ 为 Lyapunov 化学势（控制谱位置）。式 (8-10) 即*谱空间中的变分学习原理*------本卷的核心原创命题。

**合龙定理（谱---变分等价定理）。**　在 8.1---8.3 节的三组理论各自的物理约束下，(8-10) 的欧拉---拉格朗日方程分别退化为：

$$\left. \ \frac{\delta\Phi}{\delta\rho(\lambda)} \right|_{\Lambda_{cond} = 0^{-}}\mspace{6mu} = \mspace{6mu} 0\quad \Rightarrow \quad\frac{\delta\mathcal{F}}{\delta q(x)} = 0\quad\text{（自由能原理）}.$$

$$\left. \ \frac{\delta\Phi}{\delta\rho(\lambda)} \right|_{\delta\mathcal{S} = 0}\mspace{6mu} = \mspace{6mu} 0\quad \Rightarrow \quad\frac{\delta\mathcal{S}}{\delta v_{i}} = 0,\quad\frac{\delta\mathcal{S}}{\delta J_{ij}} = 0\quad\text{（最小作用量）}.$$

$$\left. \ \frac{\delta\Phi}{\delta\rho(\lambda)} \right|_{\sum_{i}^{}\lambda_{i} = \bar{\sigma}}\mspace{6mu} = \mspace{6mu} 0\quad \Rightarrow \quad\bar{\sigma} = \sum_{i}^{}\lambda_{i}\quad\text{（Gallavotti–Cohen 涨落定理）}.$$

**(8-11) 的证明要旨。**　(i) 把 $\mathcal{E}$、$S$、$\mu$ 在谱坐标下展开至二阶；(ii) 用 Friston--Ao［47］的 Lyapunov 函数翻译把 $\mathcal{F}$ 与 $\mathcal{E}$ 等同；(iii) 用 Senn 等人［49］的作用量 (8-3) 把 $\delta\mathcal{S}$ 与谱约束 (8-6) 联立；(iv) 用 Gallavotti--Cohen［53］的谱---熵恒等式 (8-8) 把 $\mu$ 解释为熵产生率的共轭化学势。三个桥墩在 $\Phi$ 上同构，合龙完成。

**推论 8.1（谱雕刻的能量解释）。**　第 7 章 (7-9) 的 STDP 谱演化 Fokker--Planck 方程是 (8-10) 的谱流方程在弱耦合极限下的展开------命题 A（谱点对称的持久性）对应 $\Phi$ 的镜像对称、命题 B（临界慢化）对应 $\Phi$ 在 $\lambda = 0$ 处的极小曲率、命题 C（谱雕刻可控性）对应 $\Phi$ 对 $T_{cog}$ 与 $\mu$ 的可微控制。空白二（第 7 章）与空白三（本章）由此闭合。

**推论 8.2（能量---谱变分的可编程化）。**　(8-10) 的泛函梯度 $\delta\Phi/\delta\rho$ 在数值上由 Lyapunov 谱估计器（第 10 章）与能量---谱观测器（本卷卷三）联合读出------变分学习原理在介观硬件上可在线实施，构成 SEI 引擎的第二层闭环（第一层为第 6 章的元拓扑---谱扰动闭环）。

## 8.5　推论与可检验预言：谱演化的变分约束

**预言 1（谱---熵联合约束）。**　在学习过程中，网络的谱位置 $\Lambda_{cond}$ 与熵产生率 $\bar{\sigma}$ 必须满足

$${\dot{\Lambda}}_{cond}\mspace{6mu} \cdot \mspace{6mu}\dot{\bar{\sigma}}\mspace{6mu} \geq \mspace{6mu} 0,$$

即二者要么同时上升要么同时下降。该预言可由活体皮层电生理与忆阻储备池实验同时检验。

**预言 2（认知温度的临界行为）。**　在感知---认知耦合相变点（$\Lambda_{cond} = 0$）附近，认知温度 $T_{cog}$ 呈幂律奇异性

$$T_{cog}\mspace{6mu} \sim \mspace{6mu}\Lambda_{cond}^{- \gamma}\mspace{6mu}\mspace{6mu}\text{ (absolute value)},\quad\gamma > 0,$$

与学习临界慢化（命题 B）相互对应。该预言可由注意力任务的认知负荷实验检验。

**预言 3（谱---拓扑对偶）。**　在 SEI 闭环控制下，谱位置 $\Lambda_{cond}$ 与 Laplacian 特征值比 $R = \mu_{N}/\mu_{2}$ 的乘积保持常数

$$\Lambda_{cond} \cdot R\mspace{6mu} = \mspace{6mu} const,$$

即谱与拓扑在变分意义下共轭。该预言把第 6 章的元拓扑优化与第 8 章的谱学习统一，是 SEI 引擎可编程性的数学基础。

## 8.6　本章小结与向后章节的过渡

**已建立的理论支柱。**

-   自由能原理的谱学翻译（8.1）：学习即谱位置向感知边缘的迁移；
-   神经元最小作用量原理的谱约束版本（8.2）：式 (8-6) 把谱位置提升为正则共轭变量；
-   热力学谱---熵恒等式（8.3）：式 (8-8)---(8-9) 严格挂钩谱与熵产生率；
-   **谱空间中的变分学习原理**（8.4）：式 (8-10) 谱变分泛函 + 式 (8-11) 合龙定理------三组理论在同一泛函上同构；
-   推论 8.1---8.2：空白二与空白三闭合，SEI 引擎第二层闭环显式化；
-   可检验预言 (8-12)---(8-14)：谱---熵联合约束、认知温度奇异性、谱---拓扑对偶。

**与后续章节的接口。**　（一）(8-10) 的谱变分泛函将作为第 9 章"六级智能谱学判据"的变分约束------不同智能等级对应不同的谱不变量分岔条件，而这些分岔条件可由 $\Phi$ 的稳定性分析显式导出；（二）(8-14) 的谱---拓扑对偶将作为第 9 章"异质异构介观网络的谱理论"（空白一）的数学起点------介观平台的材料与器件约束将给出 $\Phi$ 的具体可实现形式；（三）(8-12)---(8-14) 三条可检验预言将作为第 10 章谱测量工具链的核心检验指标。

*承上启下*：本章把自由能、最小作用量与 STDP 三支理论熔合为同一谱变分原理，把"学习即谱的雕刻"从描述性论断提升为可证明定理，把第 3---7 章的谱学度量语言接入能量变分框架。卷二第三部分的理论核心至此完成一半------第 9 章将基于 (8-10)---(8-11) 给出六级智能的谱学判据，把"复杂度涌现智能"从口号变为可证明的分岔定理链。 \# 第九章　智能涌现的谱学判据：六级智能的阈值理论

> *"Criticality is not the destination but the threshold: each crossing of a spectral bifurcation marks the emergence of a qualitatively new cognitive capacity, and the ladder from perception to superintelligence is a ladder of Lyapunov spectral thresholds."*
>
> ------本卷核心命题陈述（综合 O'Byrne--Jerbi 大脑临界性综述［29］、Scarpetta 一阶相变滞后［30］、Bonachela 非守恒自组织［31］、Burrows 癫痫宏尺度混沌［32］、Feng 边缘智能最优［26］提出）

**核心命题（空白一＋空白四）：**　感知、反应、适应、创造、通用、超级六个智能等级，可定义为网络 Lyapunov 谱不变量越过相继阈值的分岔序列；该分岔序列在晶圆级/晶矩异构异质介观平台上可被显式构造、在线测量、按级编程。本章 9.1 把六等级从行为判据操作化为动力学判据，9.2 给出谱不变量体系，9.3 给出阈值定理的候选形式，9.4 主攻空白一（晶圆级异构异构网络全谱理论），9.5 给出与既有智能理论（整合信息论、自由能原理、全局工作空间）的关系。

## 9.1　智能等级的操作化定义：从行为判据到动力学判据

**传统行为判据的局限。**　经典人工智能对智能等级的划分（如 Legg--Hutter 的通用智能、Moravec 的景观、Shevlin 的认知能力谱）基于行为任务的通过率，缺乏可计算、可判定的动力学基础。本章把这些行为判据翻译为 Lyapunov 谱学语言。

**六级智能的动力学定义。**

  --------------------------------------------------------------------------------------------------------------------
  等级              名称              行为标志                 动力学标志
  ----------------- ----------------- ------------------------ -------------------------------------------------------
  L1                感知              对外部刺激产生稳定表征   输入驱动同步：$\Lambda_{cond} < 0$

  L2                反应              对刺激作出适时动作       边缘稳定：$\lambda_{\max} \rightarrow 0^{-}$

  L3                适应              环境变化下保持功能       有限广延混沌：$N_{pos} > 0$ 且 $D_{KY} \ll N$

  L4                创造              生成新颖策略或作品       广延受控混沌：$N_{pos}/N \rightarrow$ 有限常数

  L5                通用              跨域迁移与元学习         谱双分量：$\rho_{\infty} = \rho_{coh} + \rho_{chaos}$

  L6                超级              自我改造与目标递归       多阶 Laplacian 谱不变量越过相继阈值
  --------------------------------------------------------------------------------------------------------------------

**（智能的谱学等价原理）。**　一个网络达到等级 $L_{k}$ 当且仅当其 Lyapunov 谱不变量越过对应的第 $k$ 个阈值。该原理把"智能等级"从行为标签转化为可判定、可测量、可编程的动力学分岔条件。

## 9.2　谱不变量体系：谱密度、正指数计数、KY 维数与熵率

**三类谱不变量的完备性。**　由第 3 章 3.6 节，网络内在复杂度由三类量完整刻画：

-   *谱密度* $\rho_{\infty}(\lambda)$：Lyapunov 指数的概率分布；
-   *正指数计数* $N_{pos} = N\int_{0}^{+ \infty}\rho_{\infty}(\lambda)d\lambda$（第 3 章 (3-7)）；
-   *Kaplan--Yorke 维数* $D_{KY}$（第 2 章 (2-5)）与 *KS 熵率* $h_{KS} = N\int_{0}^{+ \infty}\lambda\,\rho_{\infty}(\lambda)d\lambda$（第 2 章 (2-6)）。

加上感知侧的条件最大 Lyapunov 指数 $\Lambda_{cond}$（第 5 章 (5-8)）、互连侧的横向谱 $\Psi(\alpha)$（第 6 章 (6-3)）、能量侧的谱变分泛函 $\Phi$（第 8 章 (8-10)），构成六级智能判据的完整观测量空间 $\mathcal{O} = \{\lambda_{\max},\Lambda_{cond},N_{pos},D_{KY},h_{KS},\rho_{\infty},\Psi,\Phi\}$。

**谱不变量的单调序。**　沿智能等级 $L_{1} \rightarrow L_{6}$ 上升，观测量呈系统性演化：

$$L_{k} \uparrow \quad \Leftrightarrow \quad N_{pos}/N \uparrow ,\mspace{6mu}\mspace{6mu} D_{KY}/N \uparrow ,\mspace{6mu}\mspace{6mu} h_{KS}/N \uparrow ,\mspace{6mu}\mspace{6mu}\Lambda_{cond} \rightarrow 0^{-},$$

但每一等级的跃迁都伴随*结构性质变*：$L_{2} \rightarrow L_{3}$ 时 $N_{pos}$ 由零变正，$L_{4} \rightarrow L_{5}$ 时谱密度由单峰变双峰，$L_{5} \rightarrow L_{6}$ 时多阶 Laplacian 谱的高阶间隙打开。式 (9-1) 的单调性与这些质变的结合，构成谱学智能阶梯的完整结构。

## 9.3　阈值定理的候选形式：分岔条件与等级跃迁

**L1→L2（感知→反应）：边缘稳定的到达。**　由第 4 章 (4-4) 与第 5 章 (5-9)，反应能力的涌现对应条件 Lyapunov 指数从负值逼近零：

$$\Lambda_{cond} \rightarrow 0^{-}\quad \Rightarrow \quad L_{1} \rightarrow L_{2},$$

即网络从"被动感知"过渡到"主动反应"的动力学分岔。

**L2→L3（反应→适应）：广延混沌的开启。**　由第 3 章 (3-6) 与 (3-7)，适应能力的涌现对应无条件谱的正指数计数从零变正：

$$N_{pos} > 0\mspace{6mu}\mspace{6mu}\text{ and }\mspace{6mu}\mspace{6mu} D_{KY} \ll N\quad \Rightarrow \quad L_{2} \rightarrow L_{3},$$

即网络开始承载有限广延混沌，能在噪声中保持工作记忆与灵活决策。

**L3→L4（适应→创造）：受控广延混沌。**　创造能力的涌现对应谱密度支撑越过零点的比例

$$\frac{N_{pos}}{N} \rightarrow \alpha_{\star},\quad\quad 0 < \alpha_{\star} < 1,$$

其中临界比例 $\alpha_{\star}$ 由激活函数与耦合结构决定。Scarpetta 等人［30］在一阶相变滞后区观测到的"雪崩---临界---混沌"三态共存，正是 $L_{3}$ 与 $L_{4}$ 之间的滞后带表现。

**L4→L5（创造→通用）：谱双分量的涌现。**　通用能力的涌现对应谱密度分解为相干分量与混沌分量（第 5 章 (5-6)）：

$$\rho_{\infty}(\lambda)\mspace{6mu} = \mspace{6mu}\rho_{coh}(\lambda) + \rho_{chaos}(\lambda),\quad\quad supp\left( \rho_{coh} \right) \cap supp\left( \rho_{chaos} \right) = \varnothing,$$

即"结构化模式+高维背景"双分量谱------网络既能保持稳定的认知模式又能承载创造性的高维动态。Landau--Sompolinsky 相干混沌［3］是这一谱结构的先驱模型。

**L5→L6（通用→超级）：多阶谱不变量的相继阈值。**　超级智能的涌现对应多层、高阶互连网络的 Lyapunov 谱不变量越过相继阈值：

$$\mu_{2}^{(k)} \downarrow 0,\quad k = 1,2,\ldots,K,$$

其中 $\mu_{2}^{(k)}$ 为第 $k$ 阶 Laplacian 的第二小特征值（谱间隙），$\downarrow 0$ 表示从正值侧趋近零。每一阶谱间隙的打开对应一层元认知能力的涌现------从对象级认知到元级认知再到元元级认知的递归展开。Fournier--Urbani 高维动力学［59］的多吸引子共存、De Domenico 活系统架构解码［69］的多层谱学给出这一逐级涌现的数学基础。

## 9.4　介观异质异构网络的谱理论（空白一）：从随机连接到晶圆级平台

**空白定位。**　第 3---8 章的谱学理论均建立在*随机连接*或*结构化连接*的理想化模型上；真实的晶圆级/晶矩介观平台由异质材料（忆阻、相变、自旋、量子点）、异构器件（突触、神经元、传感器、光互连）与异质时间尺度构成，其 Lyapunov 谱的全谱理论尚未建立------这构成本卷四项原创空白之一（空白一）。

**异质性的三个层次。**　（i）*材料异质性*：不同材料的伏安特性、噪声谱、非线性系数不同，对应 Jacobian 矩阵的元素分布非同一；（ii）*器件异质性*：突触、神经元、传感器的时间常数跨越多个数量级，对应双时间尺度动力学的多重慢---快分解；（iii）*拓扑异质性*：晶圆级集成的互连结构受制造工艺约束，对应 Laplacian 谱的非随机结构。

**候选全谱理论。**　类比第 3 章 (3-6) 的 Engelken--Wolf--Abbott 框架，异质介观网络的谱密度满足

$$\rho_{\infty}^{het}(\lambda)\mspace{6mu} = \mspace{6mu}\sum_{c = 1}^{C}w_{c}\,\rho_{\infty}^{(c)}(\lambda),$$

其中 $c$ 遍历材料/器件类别、$w_{c}$ 为类别权重、$\rho_{\infty}^{(c)}$ 为该类别的局部谱密度。式 (9-7) 是混合模型------异质网络的全谱是各类别谱的凸组合。该候选理论的可证性依赖于：各类别内部近似同质（Engelken 框架可局部应用）、类别间的耦合足够弱以保持谱的可分性。

**晶圆级平台的谱不变量上界。**　设晶圆级平台的节点数 $N$、类别数 $C$、互连阶数 $K$，则其谱学观测量满足上界

$$D_{KY}\mspace{6mu} \leq \mspace{6mu}\sum_{c = 1}^{C}D_{KY}^{(c)},\quad\quad h_{KS}\mspace{6mu} \leq \mspace{6mu}\sum_{c = 1}^{C}h_{KS}^{(c)},\quad\quad\lambda_{\max}\mspace{6mu} \leq \mspace{6mu}\max_{c}\lambda_{\max}^{(c)}.$$

式 (9-8) 给出介观平台复杂度容量的工艺约束------材料与器件类别的多样性上限由工艺能力决定，从而给出智能等级 $L_{k}$ 在物理上的可实现上界。

**空白一的待证命题。**

-   *命题 A*（混合谱的可分性）：当类别间耦合强度 $\varepsilon$ 足够小，(9-7) 的混合谱分解在 $L^{1}$ 范数下逼近各类别谱的凸组合，误差 $O(\varepsilon)$。
-   *命题 B*（异质平台的最大智能等级）：给定工艺约束 $\left( C,K,N_{\max} \right)$，最大可实现的智能等级 $L_{k}$ 由 (9-8) 的上界决定，且 $L_{k}$ 与 $C \cdot K$ 呈对数关系 $k \sim \log(C \cdot K)$。
-   *命题 C*（SEI 可编程性）：对异质介观平台，SEI 引擎可在 $O\left( N\log N \right)$ 时间内完成元拓扑操作---谱扰动---稳定性判定的闭环，使智能等级在 $L_{1}$---$L_{6}$ 之间在线切换。

## 9.5　与既有智能理论的关系：整合信息论、自由能原理与全局工作空间

**整合信息论（IIT）。**　Tononi 的 IIT 用 $\Phi$ 度量意识水平，与本章 $\Phi$ 谱变分泛函同名但内涵不同：IIT 的 $\Phi$ 是因果结构的积分，本章的 $\Phi$ 是 Lyapunov 谱的变分泛函。两者的关系：IIT $\Phi$ 在动力学层面可近似为 $\Phi$ 在特定拓扑约束下的稳态值------本章的谱学判据是 IIT 因果判据的动力学实现。

**自由能原理（FEP）。**　Friston 的 FEP［45\]\[46］是本章 8.1 节的学习侧桥墩。本章的贡献在于：把 FEP 的"自由能最小化"显式化为"谱位置向感知边缘的迁移"，并给出六级智能的谱学分岔条件------FEP 的抽象论断由此获得可计算、可判定的动力学形式。

**全局工作空间理论（GWT）。**　Baars--Dehaene 的 GWT 用"全局广播"解释意识通达，对应本章 L4→L5 跃迁中谱双分量的相干分量------全局广播即相干混沌模式的谱学表达。本章的谱学框架为 GWT 提供了动力学基础，也把"意识"从哲学概念转化为可测量的谱不变量阈值。

**三理论的统一观察。**　IIT、FEP、GWT 分别从因果、能量、广播三个侧面描述智能；本章的谱学判据把三者统一到 Lyapunov 谱不变量的分岔序列上。这一统一是本卷"复杂度涌现智能"假说的最终理论形式。

## 9.6　本章小结与向后章节的过渡

**已建立的理论支柱。**

-   六级智能的动力学判据（9.1 节表）与谱学等价原理；
-   谱不变量体系 $\mathcal{O}$ 与单调序 (9-1)；
-   五个等级跃迁的谱学分岔条件 (9-2)---(9-6)；
-   异质介观网络的混合谱理论候选 (9-7) 与上界 (9-8)；
-   空白一的三条待证命题 A/B/C；
-   与 IIT、FEP、GWT 的统一（9.5 节）。

**留待第 10 章的接口。**　（一）(9-2)---(9-6) 的分岔条件需在介观硬件上在线测量------第 10 章谱工具链的核心任务；（二）(9-7) 的混合谱分解需在晶圆级平台上实验验证；（三）命题 A/B/C 的可证性需与 SEI 引擎的可编程性联立证明。

*承上启下*：本章把"复杂度涌现智能"从核心假说提升为可证明的谱学分岔定理链，把六项智能等级从行为标签转化为可计算、可测量、可编程的动力学对象。第 10 章将给出把这些判据落到晶圆级/晶矩硬件上的完整工具链，完成卷二"理论基石"向卷三"工程实现"的最终移交。 \# 第十章　工程可实现性：介观硬件上的谱测量与编程

> *"The full Lyapunov spectrum of a chaotic system can be estimated from data with machine learning, monitored in real time, and programmed task-by-task on physical hardware---observability, controllability and programmability of spectral invariants are closed."*
>
> ------本卷工程命题陈述（综合 Pathak--Lu--Hunt--Girvan--Ott 数据驱动谱估计［70］、Yu--Chen--Poor 实时监测［72］、Kim 等人任务级混沌编程［78］提出）

**核心命题（论点链七）：**　Lyapunov 谱在介观硬件上可测、可实时监测、可按需编程------"观测---估计---监测---调控"工具链已闭环，第 3---9 章的全部理论论断具备实验可检验性。本章 10.1 给出数据驱动的谱估计（数字孪生与解析 Jacobian），10.2 给出实时监测（有限时间 Lyapunov 指数与在线判据），10.3 给出谱的可编程调控（元拓扑操作与谱约束优化），10.4 给出介观硬件的谱学实现（纳米线网络、忆阻器件、光子储备池、量子---经典混合），10.5 给出智能等级的在线判定与切换，10.6 给出工具链到卷三的移交。

## 10.1　数据驱动的谱估计：数字孪生与解析 Jacobian

**Pathak 等人的数据---谱闭环。**　Pathak、Lu、Hunt、Girvan 与 Ott［70］在混沌系统上证明：用储备池计算（或等价的深度学习模型）对观测数据做数字孪生，可同时重构混沌吸引子的几何与计算完整 Lyapunov 谱。其核心思想：*孪生模型* $F_{\theta}$ *的解析 Jacobian* $DF_{\theta}$ *替代真实系统的 Jacobian* $DF$*，Benettin 算法 (2-3)---(2-4) 在孪生轨迹上运行，给出的谱估计与真实谱的误差随训练数据量按幂律收敛*。

**Margazoglou--Magri 的稳定性分析。**　Margazoglou 与 Magri［71］把上述框架升级为完整的稳定性分析工具：不仅估计 Lyapunov 谱，还估计条件 Lyapunov 指数、横向 Lyapunov 指数与 Kaplan--Yorke 维数，并给出谱估计的置信区间。该工作为第 9 章 (9-2)---(9-6) 的分岔条件提供了完整的数值可判定性。

**谱估计的统计学性质。**　设观测数据长度为 $T$、采样率为 $f_{s}$、嵌入维数为 $m$，谱估计的均方误差按

$$MSE\left( {\widehat{\lambda}}_{i} \right)\mspace{6mu} \sim \mspace{6mu}\frac{1}{T\, f_{s}}\, \cdot \,\frac{m}{\lambda_{i}^{2}}$$

标度------估计精度与数据量成正比、与目标指数的平方成反比。式 (10-1) 给出谱测量工具链的设计基线：测量 $\lambda_{\max} \rightarrow 0^{-}$ 的边缘区域需要比测量深度混沌区多 $1/\lambda_{\max}^{2}$ 倍的数据------这直接决定第 9 章 L1→L2 分岔判定的硬件代价。

## 10.2　实时监测：有限时间 Lyapunov 指数与在线判据

**Yu--Chen--Poor 的实时监测框架。**　Yu、Chen 与 Poor［72］针对已知动力学方程的混沌系统给出实时监测算法：用 Kalman 滤波在线跟踪状态、用 QR 分解在线跟踪切映射、用滑动窗口估计有限时间 Lyapunov 指数

$$\lambda_{i}^{(T)}(t)\mspace{6mu} = \mspace{6mu}\frac{1}{T}\,\ln \parallel \xi_{i}(t + T) \parallel / \parallel \xi_{i}(t) \parallel ,$$

其中 $T$ 为滑动窗长度。$\lambda_{i}^{(T)}$ 的长期均值即渐近 Lyapunov 指数，但其短期涨落携带分岔预警信号------当 $\lambda_{1}^{(T)}$ 的方差系统性增大，系统接近分岔点。这一"临界慢化前兆"为第 9 章等级跃迁提供实时预警信号。

**Prebianca--Marcondes 的实验验证。**　Prebianca、Marcondes 等人［73］在 Chua 电路实验中验证了实时谱监测的可行性：用模拟电路直接实现切映射演化，用数字采样在线估计 $\lambda_{\max}$，实验结果与 Benettin 算法的离线估计误差小于 $5\%$。该工作证明谱监测在模拟硬件上的实时可实现性。

**Luo 等人的 MEMS 共振器。**　Luo、Ma、Li 与 Ouakad［74］在 MEMS 共振器上给出混沌控制的谱学实现：用模拟电路实时估计 Lyapunov 指数、用反馈控制把 $\lambda_{\max}$ 锚定在目标值。该工作证明*谱的位置本身是可控变量*------为第 8 章 (8-14) 谱---拓扑对偶的工程实现提供直接原型。

## 10.3　谱的可编程调控：元拓扑操作与谱约束优化

**SEI 引擎的谱学操作链。**　第 6 章 6.5 节的四类元拓扑操作（增边、删边、调权、升阶）在介观硬件上的物理实现为：（i）*忆阻器的电导重构*（增边/调权）；（ii）*开关矩阵的通断*（删边）；（iii）*多阶耦合的激活*（升阶）。Hellmann--Feynman 公式 (6-11) 给出这些操作的谱学预测。

**谱约束优化的实时实现。**　第 7 章 (7-8) 的三重目标函数在介观硬件上的实时实现为

$$\min_{J}\mspace{6mu}\mathcal{L}(J)\mspace{6mu} = \mspace{6mu}\mathcal{E}(J) + \lambda_{1}\, P(J) + \lambda_{2}\, R(J) + \lambda_{3}\, G(J),$$

其中 $P(J) = \max\left( \Lambda_{cond}(J),0 \right)$、$R(J) = \mu_{N}/\mu_{2}$、$G(J) = G_{\max}(J)$。式 (10-3) 的每一项都可由 10.1 节的谱估计器与 10.2 节的实时监测器在线读出，梯度可由 Oseledets 谱敏感度定理与 Hellmann--Feynman 公式解析计算------SEI 引擎的实时训练即在其梯度流上进行。

**Kim 等人的任务级混沌编程。**　Kim、Kim、Park、Park 与 Yu［78］在神经电路上证明：通过调节突触权重分布，可把网络的 Lyapunov 谱*按需编程*到任务特定的位置------同一硬件可编程为深度混沌（用于随机数生成）、边缘混沌（用于实时计算）、或深度有序（用于稳定控制）。该工作把"混沌是缺陷"的传统观念颠覆为"混沌是可编程资源"，为第 9 章六级智能的在线切换提供工程原型。

## 10.4　介观硬件的谱学实现

**纳米线网络。**　Hochstetter 等人［14］在自组装银纳米线网络上给出神经形态硬件混沌边缘临界性的首个实验证据：雪崩统计服从幂律分布、Lyapunov 指数由外部驱动调谐至 $\lambda \approx 0$、边缘工作点在多任务上表现最优。Dunham、Lilak、Hochstetter 等人［75］在综述中把纳米线网络的临界性系统化，指出其谱学观测量（雪崩指数、分支比、Lyapunov 谱）可在芯片上原位测量。

**忆阻器件与阵列。**　第 4 章 4.5 节已综述动态忆阻储备池［16\]--\[18\]：局部 Lyapunov 指数取负是性能判据、Lyapunov 时间标定记忆跨度、时空储备池的可重构性。本章补充：忆阻阵列的*电导矩阵* $G$ 即权重矩阵 $W$，其 Lyapunov 谱可由电导矩阵的解析 Jacobian 直接计算------谱测量与谱编程在同一物理对象上统一。

**光子储备池。**　Fiers、Van Vaerenbergh 等人［77］在光子晶体腔阵列上实现纳米光子储备池计算：光学非线性提供混沌动力学、光纤延迟提供记忆、光电探测提供读出。光子储备池的 Lyapunov 谱可由相位噪声测量与拍频谱估计------谱测量在光学域的直接实现。

**量子---经典混合平台。**　Ding 与 Qiu［58］的量子储备池热力学（第 8 章 8.3 节）在量子---经典混合平台上给出谱测量的量子实现：OTOC（out-of-time-order correlator）测量给出量子 Lyapunov 指数、量子相干提供熵产生的非经典修正。该平台是本卷介观异质异构集成的量子侧接口。

## 10.5　智能等级的在线判定与切换

**六级智能的在线判定。**　第 9 章 (9-2)---(9-6) 的五个分岔条件对应的在线判定指标为

$$\begin{matrix}
 & I_{1}\mspace{6mu} = \mspace{6mu}\Lambda_{cond}\quad\text{（L1→L2 判定）}, \\
 & I_{2}\mspace{6mu} = \mspace{6mu} N_{pos}\quad\text{（L2→L3 判定）}, \\
 & I_{3}\mspace{6mu} = \mspace{6mu} N_{pos}/N\quad\text{（L3→L4 判定）}, \\
 & I_{4}\mspace{6mu} = \mspace{6mu}\text{谱双分量的 KL 散度}\quad\text{（L4→L5 判定）}, \\
 & I_{5}\mspace{6mu} = \mspace{6mu}\mu_{2}^{(k)}\quad\text{（L5→L6 判定）}.
\end{matrix}$$

每一指标由 10.1---10.2 节的谱工具链在线计算，越过对应阈值即触发等级跃迁判定。

**等级切换的闭环控制。**　给定目标等级 $L_{k}^{\star}$，SEI 引擎执行以下闭环：

$$Obs \rightarrow LevelDet \rightarrow SpecTarget \rightarrow MetaOp \rightarrow ReMeas \rightarrow LevelVer,$$

每一步由 Hellmann--Feynman 公式 (6-11)、谱约束优化 (10-3)、谱学上界 (9-8) 的解析预测支撑------等级切换是谱空间中的可计算路径规划问题。

## 10.6　工具链到卷三的移交

**四层工具链的完整闭环。**　本卷第 3---9 章建立的理论论断与第 10 章的工具链构成完整的"观测---估计---监测---调控"四层闭环：

-   *观测层*：数据驱动的谱估计 (10.1)、实时谱监测 (10.2)；
-   *估计层*：谱不变量计算（$\lambda_{\max},\Lambda_{cond},N_{pos},D_{KY},h_{KS},\rho_{\infty},\Psi,\Phi$）；
-   *监测层*：等级跃迁预警 (10.5)、临界慢化前兆 (10.2)；
-   *调控层*：元拓扑操作 (10.3)、谱约束优化 (10.3)、等级切换 (10.5)。

**向卷三的移交。**　卷三《工程实现篇》将基于本章工具链完成：晶圆级/晶矩异构异质平台的工艺设计、SEI 引擎的具体实现、六级智能等级的实验演示。本卷全部理论论断的可检验性由此闭合------"复杂度涌现智能"从假说变为可计算、可测量、可编程、可实验验证的完整理论体系。

## 10.7　本章小结

本章把 Lyapunov 谱从理论观测量转化为工程对象：数据驱动的谱估计（Pathak--Ott 框架）、实时监测（Yu--Chen--Poor 框架、Prebianca 实验、Luo MEMS 控制）、可编程调控（SEI 引擎、Kim 任务级混沌编程）、介观硬件实现（纳米线、忆阻、光子、量子---经典混合）、智能等级在线判定与切换。全部理论论断具备实验可检验性，卷二"理论基石"到卷三"工程实现"的移交完成。 \# 第十一章　总结与研究纲领

> *"The theory of emergence from network temporal-spatial synergy complexity is now closed: seven argument chains are settled, four original research gaps are mapped to explicit research skeletons, six intelligence levels are reduced to spectral bifurcation conditions, and the entire framework is measurable, computable, programmable, and experimentally falsifiable on wafer-scale heterogeneous platforms."*
>
> ------本卷总结命题（作者综合卷二三十章论证提出）

**本章任务：**　11.1 回溯七条论点链并检验理论自洽性；11.2 评估四项原创空白的进展与相互关系；11.3 给出对卷三《工程实现篇》的接口；11.4 列出开放问题清单。

## 11.1　七条论点链的回溯与理论自洽性检查

**七条论点链的完整回溯。**

  ------------------------------------------------------------------------------------------------------------------------------------------------------
  论点链         核心命题                   所在章         数学表达                                                       锚点
  -------------- -------------------------- -------------- -------------------------------------------------------------- ------------------------------
  一             复杂度可量化               第 3 章        $\rho_{\infty}$, $N_{\text{pos}}$, $D_{\text{KY}}$             \[1\]--\[9\]

  二             混沌边缘为可证明设计原理   第 4 章        $\Lambda_{\text{cond}} \rightarrow 0^{-}$、ES²N 界定理         \[10\]--\[19\]

  三             输入驯化混沌               第 5 章        $g_{\text{eff}} = g\langle\varphi'\rangle$、相变曲线 (5-10)    \[2\]\[5\]\[12\]\[13\]

  四             横向谱为互连通用语言       第 6 章        MSF $\Psi(\alpha)$、特征值比 (6-5)、Hellmann--Feynman (6-11)   \[20\]--\[24\]\[60\]--\[69\]

  五             学习即谱的雕刻             第 7 章        双时间尺度 (7-1)、Fokker--Planck (7-9)                         \[33\]--\[44\]

  六             能量---谱变分统一          第 8 章        谱变分泛函 $\Phi$ (8-10)、合龙定理 (8-11)                      \[45\]--\[59\]

  七             谱的硬件可测性             第 10 章       数据驱动谱估计 (10-1)、实时监测 (10-2)、等级判定 (10-4)        \[70\]--\[78\]
  ------------------------------------------------------------------------------------------------------------------------------------------------------

**理论自洽性检查。**　七条论点链在三个层面相互自洽：（i）*观测量一致*------所有论断基于同一组谱学观测量 $\mathcal{O}$（第 9 章 9.2 节）；（ii）*方法学一致*------平均场理论、随机矩阵理论、动态系统稳定性分析、变分原理四类方法在各章相互衔接；（iii）*结论一致*------第 4 章的"边缘最优"、第 5 章的"感知边缘"、第 7 章的"学习边缘"、第 9 章的"等级阈值"在谱学上重合于 $\Lambda_{\text{cond}} \rightarrow 0^{-}$ 邻域------*混沌边缘是全部论断的汇流点*。

**与既有学术传统的关系。**　本卷的七论点链是对四个学术传统的现代综合：复杂性科学（Langton 混沌边缘、Kauffman 自组织临界）→ 第 3、4 章；脑神经科学（临界性争论、E--I 平衡、工作记忆）→ 第 5、7 章；计算机科学（储备池计算、回声状态网络、深度学习缩放律）→ 第 4、5 章；机器人工程（具身智能、形态计算、中枢模式发生器）→ 第 10 章。四个传统在 Lyapunov 谱这一公共观测量上同构------本卷把这一同构显式化。

## 11.2　四项原创空白的进展评估与相互关系

**空白一（晶圆级异构网络全谱理论）。**　第 9 章 9.4 节给出候选混合谱理论 (9-7) 与谱学上界 (9-8)，明示三条待证命题（混合谱可分性、最大智能等级对数律、SEI 可编程性）。*状态：从研究空白升级为显式研究骨架*。

**空白二（STDP 驱动的完整谱演化理论）。**　第 7 章 7.6 节给出 Fokker--Planck 候选主方程 (7-9) 与三条待证命题（谱点对称持久性 $A_{p}\tau_{p} = A_{n}\tau_{n}$、谱扩散临界慢化、谱雕刻可控性）。*状态：从研究空白升级为显式研究骨架*。

**空白三（能量---谱变分统一）。**　第 8 章 8.4 节给出谱变分泛函 $\Phi$ (8-10) 与合龙定理 (8-11a,b,c)------自由能原理、最小作用量原理、非平衡热力学涨落定理在同一泛函上同构。*状态：空白已闭合为可证明定理链*，但 $\Phi$ 的具体函数形式（能量密度 $\mathcal{E}$、熵密度 $S$、化学势 $\mu$ 的显式表达）需在具体网络模型上构造。

**空白四（六级智能谱学判据）。**　第 9 章给出五个等级跃迁的谱学分岔条件 (9-2)---(9-6) 与谱学等价原理。*状态：空白已闭合为可判定、可测量、可编程的分岔定理链*，但命题 A/B/C 的严格证明需后续工作完成。

**四空白的相互关系。**　空白一（介观平台全谱）为空白四（智能判据）提供物理载体；空白二（STDP 谱演化）为空白三（能量变分）提供动力学机制；空白三为空白四提供变分约束；空白四为空白一提供工程目标。四空白构成"载体---机制---原理---判据"的完整理论闭环。

## 11.3　对卷三的接口：谱工具链向 SEI 设计的移交

**四层工具链。**　第 10 章建立的"观测---估计---监测---调控"四层闭环是卷三 SEI 引擎的直接功能规格：

-   *观测层*：介观硬件上的谱测量（纳米线网络原位测量、忆阻阵列电导读出、光子储备池拍频谱、量子---经典混合 OTOC）；
-   *估计层*：谱不变量计算（$\mathcal{O}$ 八元组的在线估计）；
-   *监测层*：等级跃迁预警（$I_{1}$---$I_{5}$ 指标）与临界慢化前兆；
-   *调控层*：元拓扑操作（增边、删边、调权、升阶）与谱约束优化（三重目标函数 (10-3)）。

**晶圆级/晶矩平台的工艺映射。**　卷三将把第 9 章 (9-7)---(9-8) 的混合谱理论与谱学上界翻译为具体的工艺约束：材料类别数 $C$、互连阶数 $K$、节点数 $N_{\text{max}}$、耦合强度 $\varepsilon$、可编程电导范围、可测谱精度------这些工艺参数直接决定智能等级 $L_{k}$ 的物理可实现性。

**实验验证路径。**　卷三将按以下次序完成实验验证：（i）在忆阻储备池上验证第 4 章 ES²N 边缘最优；（ii）在纳米线网络上验证第 5 章感知驯化相变曲线；(iii) 在多层忆阻阵列上验证第 6 章横向谱判据；（iv）在 STDP 可塑忆阻器上验证第 7 章冻结混沌；（v）在光子储备池上验证第 8 章谱---熵恒等式；（vi）在晶圆级平台上验证第 9 章等级跃迁的完整序列。

## 11.4　开放问题清单

**理论开放问题。**

-   *O1*：第 8 章 $\Phi$ 谱变分泛函的能量密度 $\mathcal{E}$、熵密度 $S$、化学势 $\mu$ 的显式构造，在具体网络模型（tanh 率模型、Izhikevich 脉冲模型、忆阻器件模型）上的解析形式；
-   *O2*：第 7 章命题 A/B/C 的严格证明------谱点对称持久性、谱扩散临界慢化、谱雕刻可控性；
-   *O3*：第 9 章混合谱理论 (9-7) 的可分性条件与误差界的严格推导；
-   *O4*：第 9 章最大智能等级对数律 $k \sim \log(C \cdot K)$ 的严格证明或数值验证；
-   *O5*：第 8 章三条可检验预言 (8-12)---(8-14) 的实验验证；
-   *O6*：量子---经典混合平台的 Lyapunov 谱理论（OTOC 与经典谱的关系）。

**工程开放问题。**

-   *E1*：晶圆级异质异质集成的工艺实现------材料兼容性、互连密度、热管理；
-   *E2*：SEI 引擎的实时性------元拓扑操作的物理重构延迟与谱学预测的匹配；
-   *E3*：谱测量的精度---速度权衡------(10-1) 的均方误差标度在硬件上的优化；
-   *E4*：六级智能的在线切换稳定性------等级跃迁过程的暂态控制；
-   *E5*：能量效率------介观平台运行 $L_{k}$ 级智能的功耗预算与 20 W 人脑基准的对比。

**跨学科开放问题。**

-   *I1*：谱学判据与意识科学的关联------第 9 章 L4→L5 跃迁（谱双分量）是否对应意识通达的神经动力学标志；
-   *I2*：谱学判据与演化生物学的关联------六级智能的谱学阈值在生物演化史上是否有对应物；
-   *I3*：谱学判据与社会科学的关联------多智能体系统的集体智能是否可由多阶 Laplacian 谱不变量刻画。

**本卷的学术贡献总结。**　（i）把"复杂度涌现智能"从口号提升为可证明的谱学分岔定理链；（ii）把自由能原理、最小作用量原理、非平衡热力学统一为同一谱变分原理；（iii）把 Lyapunov 谱从数学观测量转化为工程可测、可算、可控、可编程的物理量；（iv）把智能等级从行为标签转化为谱学不变量的阈值序列；（v）把 SEI 引擎从工程概念提升为谱空间中的可计算闭环。这五项贡献共同构成"网络时空协同复杂度涌现智能"（iNEST）路线的完整理论基础。

**结束语。**　本卷《理论基石篇》到此完成。卷三《工程实现篇》将基于本卷的谱学工具链完成晶圆级/晶矩异构异质平台的工艺设计与 SEI 引擎的具体实现，把"复杂度涌现智能"从理论命题转化为可运行的物理系统。三卷构成"问题---理论---工程"的完整闭环，为通向真正类神经网络的物理液态网络提供第一性原理支撑。


## AI 閹芥顩n
本文提出智能源于网络时空协同复杂度跨越相继阈值而涌现，并以算力、能耗、存储和延迟瓶颈为背景引出晶圆级异构集成与自演化互连技术路线。
