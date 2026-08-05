# Transformer 推理全流程的计算—通信—拓扑匹配白皮书

**副标题：从算子谱系到相位可重构互连——为什么 Prefill 要 bisection、Decode 要小直径、MoE 要高谱隙、KV 迁移要隔离带宽**

---

|文档项|内容|
|---|---|
|文档类型|技术白皮书（可打印稿）|
|版本|V1.0|
|日期|2026 年 8 月|
|密级|公开资料研究，可公开发布|
|适用读者|互连架构师、推理系统工程师、AI 基础设施决策者|

**打印排版规范**：标题使用微软雅黑，正文使用宋体，强调使用楷体，英文与数字使用 Times New Roman，公式统一采用标准数学排版体，全文标点采用全角，段落首行缩进两字符，页面 A4 纵向、页边距 2.5 cm。

---

## 摘要

本白皮书完整拆解 Transformer 推理的全部算子谱系（共十九类运算），并逐一给出其计算强度、通信原语、消息尺度与主导瓶颈项，进而论证一个核心命题：**推理系统的互连需求不是单一指标，而是由矩阵形状的相变所驱动的四类正交图论诉求**。

具体而言，Prefill 阶段的厚矩阵通用矩阵乘（GEMM）产生大块归约流量，受制于二分带宽（bisection bandwidth）；Decode 阶段的瘦向量矩阵乘（GEMV）产生高频微型归约流量，受制于网络直径（diameter）；混合专家（MoE）的稀疏路由矩阵产生随机置换全对全流量，受制于图的谱隙（spectral gap）；键值缓存（KV Cache）迁移是零算力的单向大象流，受制于带宽的独占性（isolation）。

本白皮书进一步证明存在一个**不可能四边形**：任何静态拓扑无法同时最优化上述四个指标。由此得出的前瞻性结论是：推理互连的下一代范式不在于继续堆叠带宽，而在于**拓扑的时间复用**——将谱隙、直径、二分带宽从设计期常量转化为运行期可调度变量。本白皮书给出该范式的可行性判据 $\tau_{\text{recfg}} \ll T_{\text{phase}}$，并按相位驻留时间对不同重构技术的适用边界作出定量划分。

---

## 第一章 引言：从"节点算力"到"网络结构"

_“计算机体系结构的历史，就是不断发现瓶颈、然后把瓶颈从一个地方搬到另一个地方的历史。”_——这句体系结构界的老话在大模型推理上应验得格外彻底。

2020 年至 2023 年，行业的共识是"算力为王"。2024 年之后，随着上下文长度从 4K 扩展至 1M、模型结构从稠密转向稀疏专家、服务架构从合并式转向分离式，瓶颈已经系统性地从**节点内的浮点算力**转移到**节点间的互连结构**。

这一转移有一个精确的判据。设单卡峰值算力为 $\Pi$（FLOPS）、显存带宽为 $\beta_{\text{mem}}$（Byte/s），Roofline 模型（Williams、Waterman 与 Patterson，2009）给出转折点：

$$I^{*} = \frac{\Pi}{\beta_{\text{mem}}}$$

对 NVIDIA H100 而言 $I^{*} = 989\ \text{TFLOPS} / 3.35\ \text{TB/s} \approx 295\ \text{FLOP/Byte}$。而 Transformer 推理两个主要相位的算术强度分别为：

$$I_{\text{prefill}} \approx L \qquad\qquad I_{\text{decode}} \approx B$$

其中 $L$ 为序列长度，$B$ 为批大小。于是出现了一个跨越两个数量级的不等式：

$$\underbrace{L \sim 10^{4}!\sim!10^{6}}_{\text{Prefill}} ;\gg; \underbrace{I^{*} \approx 295}_{\text{硬件转折点}} ;\gg; \underbrace{B \sim 1!\sim!64}_{\text{Decode}}$$

*这一个不等式，就是全部架构分歧的源头。*它告诉我们：同一个模型的两个执行相位，在硬件视角下是两种完全不同的负载——一个撞算力墙，一个撞内存墙。而当它们各自被拆分并行化之后，其通信足迹的差异更为夸张，最终落到互连拓扑上，便呈现为四种互相冲突的结构诉求。

本白皮书的组织逻辑是自下而上的：第二章穷举算子；第三章建立三套第一性模型；第四章将算子归并为六个相位并给出拓扑匹配；第五章建立并行维度与拓扑维度的映射；第六章给出端到端时序与预算；第七章证明不可能四边形；第八章提出相位可重构互连范式。

---

## 第二章 Transformer 推理的完整算子谱系

业界讨论推理通信时，习惯只提"每层两次 all-reduce"。这是一种严重的简化。完整的推理链路包含十九类运算，其中至少七类携带通信语义。本章逐一穷举，参考模型取两个：稠密模型以 70B 级为准（层数 $n_l=80$，隐藏维 $d=8192$，查询头 64、键值头 8、头维 $d_h=128$，FFN 中间维 28672，词表 $V=128{,}256$）；稀疏模型以 671B/37B 激活级为准（层数 61、其中 58 层为 MoE，$d=7168$，256 路由专家 + 1 共享专家，top-8，采用多头潜在注意力 MLA）。

### 2.1 输入侧：分词与嵌入查表

分词（Tokenization）是纯 CPU 的字符串操作，无矩阵运算、无通信，但它决定了后续所有张量的第一维，因此是整个流水线的形状发源地。

嵌入查表 $E = \text{Embed}[,\text{ids},]$ 在数学上等价于一次极端稀疏的矩阵乘 $E = S W_{\text{emb}}$，其中 $S$ 是独热（one-hot）选择矩阵，形状 $[L, V]$。实现上退化为 gather 访存，算术强度趋近于零，是纯带宽受限操作。

_通信语义_：当词表沿 $V$ 维切分（vocab parallel，嵌入表 $8192 \times 128256 \times 2\ \text{B} \approx 2.1\ \text{GB}$，值得切分）时，每张卡只能查到属于自己分片的 token，其余位置填零，因此必须做一次 all-reduce 将部分嵌入相加复原。**这是每 token 第一次全局同步，常被忽略。**

### 2.2 归一化：LayerNorm 与 RMSNorm

现代模型普遍采用 RMSNorm（Zhang 与 Sennrich，2019）：

$$\text{RMSNorm}(x) = \frac{x}{\sqrt{\frac{1}{d}\sum_{i=1}^{d} x_i^2 + \epsilon}} \odot \gamma$$

该算子的浮点运算量为 $O(Ld)$，访存量同为 $O(Ld)$，算术强度约为常数 4～6，**远低于任何硬件的转折点，是彻底的带宽受限算子**。在 Decode 相位它与其他逐元素算子共同构成"访存税"，通常通过算子融合（kernel fusion）隐藏。

_通信语义_：在标准张量并行下，归一化前激活已被 all-reduce 复原为全量，故本算子零通信。但在序列并行（Sequence Parallelism，Korthikanti 等，2023）中，激活沿 $L$ 维切分，归一化虽仍可独立计算（归约沿 $d$ 维），却需要在其前后插入 reduce-scatter 与 all-gather 以完成布局转换——**通信总量与 all-reduce 相同，但被拆成两半，从而节省激活显存。**这是"以布局换显存"的典型交易。

### 2.3 QKV 投影

$$Q = XW_Q,\quad K = XW_K,\qu004 V = XW_V$$

（正文取 $Q = XW_Q$，$K = XW_K$，$V = XW_V$。）在分组查询注意力（GQA，Ainslie 等，2023）下，$W_Q \in \mathbb{R}^{d \times d}$，而 $W_K, W_V \in \mathbb{R}^{d \times n_{kv}d_h}$，参数量为 $8192\times8192 + 2\times8192\times1024 \approx 83.9\ \text{M}$，单 token 运算量约 168 MFLOP。

_通信语义_：采用**列并行**切分（$W$ 按输出维切开），$Y = X[W_1 | W_2] = [XW_1 | XW_2]$，各卡结果直接拼接即为最终结果，**前向零通信**。这是 Megatron-LM（Shoeybi 等，2019）最精妙的设计：将必然发生的通信推迟并合并到行并行层。

### 2.4 旋转位置编码（RoPE）

$$\tilde q_m = R_{\Theta,m}, q_m,\qquad R_{\Theta,m} = \bigoplus_{i=1}^{d_h/2}\begin{pmatrix}\cos m\theta_i & -\sin m\theta_i\ \sin m\theta_i & \cos m\theta_i\end{pmatrix}$$

RoPE（Su 等，2021）是分块对角旋转矩阵作用，实现上为逐元素三角运算，运算量 $O(Ld)$，带宽受限，零通信。长上下文外推所用的 YaRN、NTK 缩放等只改变 $\theta_i$ 的取值，不改变通信特性。

### 2.5 KV Cache 写入与读取

这是推理区别于训练的**根本性算子**。每生成一个 token，将其 $K, V$ 追加至缓存：

$$V_{\text{KV}} = 2 \cdot L \cdot n_l \cdot n_{kv} \cdot d_h \cdot b$$

代入 70B 参数：$2 \times 80 \times 8 \times 128 \times 2\ \text{B} = 320\ \text{KB/token}$。十万 token 上下文即 **32 GB**——已超过单卡显存的三分之一。这就是 PagedAttention（Kwon 等，2023，vLLM）引入分页管理、前缀复用与写时复制的直接动因。

多头潜在注意力（MLA）将其压缩为低秩潜在向量（潜在维 512 + 位置维 64 = 576）：$576 \times 61 \times 2\ \text{B} \approx 70\ \text{KB/token}$，压缩比约 4.5 倍。**KV Cache 的体量直接决定了第 2.19 节所述迁移相位的网络代价，因此注意力结构的选择本质上是一个网络架构决策。**

_通信语义_：缓存读写本身在卡内，零跨卡通信。但缓存的**位置**决定了后续迁移流量，这是全文最容易被低估的耦合点。

### 2.6 注意力打分：$L^2$ 相变的发生地

$$S = \frac{QK^{\top}}{\sqrt{d_h}} + M$$

这是全流程中唯一产出 $[L, L]$ 方阵的运算，也是唯一随序列长度**平方增长**的运算。运算量为 $2L^2 d$（单层，全头合计）。

_一个关键的定量结论_：单层投影类运算量为 $2Ld(d + 2n_{kv}d_h) + 2Ld \cdot d + 6Ld \cdot d_{\text{ffn}} \approx 1.71\ \text{GFLOP}$（每 token），而注意力类运算量为 $4Ld_{\text{eff}}$。取上述参数解交叉点：

$$L_{\text{crossover}} \approx 5 \times 10^{4}$$

即：**当上下文超过约五万 token，注意力计算开始压倒全部权重投影计算。**这解释了为什么 NVIDIA Rubin CPX 将"3 倍注意力加速"列为核心指标，也解释了为什么百万 token 场景必须引入上下文并行（Context Parallelism）。

_通信语义_：单头内零通信；但当 $L$ 沿序列维切分（上下文并行）时，需要环形轮转 $K, V$ 块——**Ring Attention（Liu 等，2023）将通信模式从全局归约降级为纯近邻交换**，这是"算法重塑拓扑需求"的最佳范例，详见第七章。

### 2.7 Softmax 与在线安全归一化

$$\text{softmax}(s)_j = \frac{e^{s_j - \max_k s_k}}{\sum_k e^{s_k - \max_k s_k}}$$

朴素实现需三遍扫描（求最大值、求指数和、归一化），访存量为运算量的数倍。FlashAttention（Dao 等，2022）采用在线安全 softmax 与分块重标定，将 $[L,L]$ 矩阵**从不物化到高带宽显存**，把访存复杂度由 $O(L^2)$ 降至 $O(L)$。

需要明确指出：**FlashAttention 优化的是显存墙，不是网络墙。**它不改变任何跨卡通信量。这一区分对架构决策至关重要——大量工程实践误以为 FlashAttention 能缓解通信压力。

_通信语义_：单卡内零通信；上下文并行下需跨块归约 $(\max, \text{sumexp})$ 二元组进行统计量合并，消息极小（每块两个标量），但构成同步点。

### 2.8 加权聚合与 2.9 输出投影

$$O = \text{softmax}(S)V, \qquad Y = OW_O$$

输出投影 $W_O \in \mathbb{R}^{d\times d}$ 采用**行并行**：$Y = [O_1|O_2]\begin{bmatrix}W_{O,1}\ W_{O,2}\end{bmatrix} = O_1W_{O,1} + O_2W_{O,2}$。

**部分和必须相加，于是产生本层第一次 all-reduce。这不是设计选择，而是分块矩阵乘法的代数必然。**

### 2.10 残差连接

$$X’ = X + Y$$

逐元素加法，运算量 $O(Ld)$，零通信。但它有一个隐含的架构含义：残差要求全量激活，因此**行并行层的 all-reduce 不可推迟、不可省略**，它是数据流上的硬同步栅栏（barrier）。

### 2.11 FFN 上投影与 SwiGLU 门控

$$\text{FFN}(x) = \big(\text{Swish}(xW_{\text{gate}}) \odot xW_{\text{up}}\big)W_{\text{down}}$$

SwiGLU（Shazeer，2020）需要三个权重矩阵而非两个，参数量为 $3d\cdot d_{\text{ffn}} = 3\times8192\times28672 \approx 704.6\ \text{M}$，占单层参数的 84%，是稠密模型的算力与显存主体。

_通信语义_：$W_{\text{gate}}$ 与 $W_{\text{up}}$ 列并行，零通信；门控逐元素乘不跨越切分维，故可完整保持并行度——**SwiGLU 对张量并行是"通信友好"的**。

### 2.12 FFN 下投影

$$Z = HW_{\text{down}}$$

行并行，产生本层第二次 all-reduce。至此确立全文的基准计数：**稠密模型每层恰有 2 次 all-reduce，$n_l = 80$ 层共 160 次全局同步。**

### 2.13 MoE 门控与 Top-K 路由

$$g = xW_g,\qquad P = \text{TopK}(\text{softmax}(g),, k)$$

门控矩阵 $W_g \in \mathbb{R}^{d\times E}$ 运算量微不足道（$7168\times256$），但其输出 $P \in {0,1}^{L\times E}$（每行 $k$ 个非零）却是**全流程中通信复杂度最高的对象**。

$P$ 的关键性质有三：其一，稀疏度极高（$k/E = 8/256 = 3.1%$）；其二，**每个 token 独立重新决定**，不存在跨 token 的稳定性；其三，负载天然不均衡，需辅助损失、无辅助损失偏置（DeepSeek-V3 的 aux-loss-free 策略）或专家选择路由来平衡。

_性质二是决定性的_：它意味着 MoE 的流量矩阵是**随机置换流（random permutation traffic）**，而非任何可预测的固定模式。因此不存在"把常用通信对放近一点"的优化空间——这一点将在第三章以谱图理论精确刻画。

### 2.14 Dispatch 与 Combine：全对全

$$\tilde X = P^{\top}X \quad(\text{dispatch}),\qquad \hat Y = P Z \quad(\text{combine})$$

在专家并行（Expert Parallelism）下，$P^{\top}X$ 意味着把每个 token 送往其选中专家所驻留的设备，$PZ$ 意味着把结果收回并加权求和。二者均为 all-to-all。

_定量_：单 token 单层 dispatch 流量 $k \cdot d \cdot b = 8 \times 7168 \times 2\ \text{B} \approx 114.7\ \text{KB}$，combine 同量，合计约 229 KB；乘以 58 个 MoE 层，得 **约 13.3 MB/token**——比稠密模型的张量并行 all-reduce（约 2.6 MB/token，$B=1$）高出一个数量级，且被打散为 $N^2$ 条碎流（专家并行度 64 时为 4096 条）。

工程侧的刚性约束由此而来：该模型 Decode 相位的最优配置约为每 GPU 4 个专家，即 64 张 GPU **必须全部位于同一个低延迟高带宽域内**；一旦部分专家跨出 NVLink 域落至 InfiniBand，全对全立即被慢速域拖垮。GB200 NVL72 提供的 130 TB/s 聚合全对全带宽、DeepEP 将 dispatch 时延压至约 163 μs 的低时延内核，均是针对此约束的直接工程回应。

### 2.15 最终归一化与语言模型头

$$\text{logits} = \text{RMSNorm}(X_{\text{final}}), W_{\text{lm}},\qquad W_{\text{lm}} \in \mathbb{R}^{d\times V}$$

该矩阵 $8192\times128256 \approx 1.05\ \text{G}$ 参数（FP16 约 2.1 GB），单 token 运算量 2.1 GFLOP，约占总量的 1.5%——看似次要，但其**输出张量**极为可观：$V \times b = 128256 \times 2\ \text{B} \approx 250\ \text{KB/token}$。

_两个重要工程后果_：第一，Prefill 阶段绝不能对全部 $L$ 个位置计算 logits（$8192 \times 250\ \text{KB} = 2\ \text{GB}$），只计算最后一个位置；第二，词表并行下 logits 需 all-gather 或 all-reduce，**单次 250 KB 的消息在 Decode 相位已可与整层张量并行归约相当**，构成"最后一公里的全局同步"。

### 2.16 采样

温度缩放、Top-K 截断、Top-P（核采样，Holtzman 等，2019）、重复惩罚等操作运算量极小，但在词表并行下需要跨卡求全局最大值、全局排序或全局前缀和——**又一次延迟敏感的小消息全局归约**。

至此可以给出 Decode 相位每 token 的完整同步预算：

$$N_{\text{sync}} = \underbrace{1}_{\text{嵌入}} + \underbrace{2 n_l}_{\text{张量并行}} + \underbrace{2 n_{\text{moe}}}_{\text{全对全}} + \underbrace{1}_{\text{logits}} + \underbrace{1}_{\text{采样}} ;\approx; 163\ \text{（稠密）} \sim 279\ \text{（稀疏）}$$

### 2.17 投机解码与多 token 预测

投机解码（Leviathan 等，2023）以小模型或多 token 预测（MTP）头一次性草拟 $\gamma$ 个候选 token，再由大模型一次前向并行验证。其效果是把激活矩阵从 $[B, d]$ 变为 $[B(\gamma+1), d]$，算术强度提升为：

$$I_{\text{spec}} \approx B(\gamma+1)$$

_这是对拓扑需求的一次重要扰动_：投机解码把 Decode 相位从"纯延迟受限"向"混合受限"推移，单次消息量放大 $(\gamma+1)$ 倍，从而在一定程度上**缓和了对小直径的绝对依赖，代价是提高了对带宽的要求**。架构上应视为在 Decode 与 Prefill 之间插入的第五种中间相位。

### 2.18 量化、反量化与流水线点对点通信

FP8/FP4/INT4 量化在数据流上表现为算子边界处的 scale/dequant 逐元素运算，其真正的网络意义是**把所有通信消息按位宽等比缩小**：FP8 通信相比 BF16 直接减半。DeepSeek 在 dispatch 使用 FP8、combine 使用 BF16 的非对称策略，正是基于"前向容忍低精度、归约累加需高精度"的数值考量。

流水线并行的层间点对点通信传输激活 $[L, d]$：Prefill 相位约 134 MB（$L=8192$），Decode 相位仅 16 KB（$B=1$）。其拓扑诉求是**纯近邻高带宽**，对全局直径与谱隙均不敏感，但对气泡（bubble）率极为敏感。

### 2.19 KV Cache 跨池迁移

这是**唯一不含任何矩阵运算的相位**，纯直接内存访问搬运。在分离式服务架构下，Prefill 池算完的 KV Cache 必须整体迁移至 Decode 池。体量已在 2.5 节给出：GQA 结构下十万 token 约 32 GB，MLA 结构下约 7 GB。

经 400 GbE 传输 32 GB 需约 640 ms，经 NVLink 仅需约 18 ms。**该相位对自身延迟不敏感（仅影响首 token 时延尾部），但对邻居具有毁灭性——它是教科书级的大象流。**逐层流水（第 $k$ 层算完即传）可与计算重叠，将其时延隐藏，但无法消除其对共享链路的挤占。

### 本章小结：算子谱系全表

|序号|算子|矩阵形状|算术强度|通信原语|消息尺度（Decode）|
|---|---|---|---|---|---|
|1|分词|—|—|无|—|
|2|嵌入查表|稀疏 gather|≈0|all-reduce（词表并行）|16 KB|
|3|RMSNorm|逐元素|4～6|无／SP 转换|—|
|4|QKV 投影|厚×厚，列并行|$L$ 或 $B$|无|—|
|5|RoPE|逐元素|≈2|无|—|
|6|KV 写入|访存|≈0|无（卡内）|—|
|7|$QK^{\top}$|$[L,d_h]\times[d_h,L]$|$O(L)$|CP 环形轮转|视 CP|
|8|Softmax|行归约|≈2|CP 统计量归约|数十 B|
|9|$\text{P}V$|$[L,L]\times[L,d_h]$|$O(L)$|CP 环形轮转|视 CP|
|10|$W_O$|厚×厚，行并行|$L$ 或 $B$|**all-reduce ①**|16 KB～512 KB|
|11|残差|逐元素|2|无（但为同步栅栏）|—|
|12|FFN 上投影/门控|列并行|$L$ 或 $B$|无|—|
|13|SwiGLU|逐元素|≈3|无|—|
|14|FFN 下投影|行并行|$L$ 或 $B$|**all-reduce ②**|16 KB～512 KB|
|15|MoE 门控 TopK|$[L,d]\times[d,E]$|极低|无|—|
|16|Dispatch|稀疏置换 $P^{\top}X$|碎片|**all-to-all**|115 KB×$N^2$ 碎流|
|17|Combine|稀疏加权 $PZ$|碎片|**all-to-all**|115 KB×$N^2$ 碎流|
|18|LM Head|$[B,d]\times[d,V]$|$B$|**all-gather logits**|250 KB|
|19|采样|归约／排序|极低|**全局归约**|KB 级，延迟敏感|
|附|流水线 P2P|激活传递|—|send/recv|16 KB～134 MB|
|附|KV 迁移|无|0|P2P bulk|7～32 GB／请求|

---

## 第三章 三套第一性模型

### 3.1 计算侧：Roofline

$$P_{\text{attain}} = \min\left(\Pi,; I \cdot \beta_{\text{mem}}\right)$$

该模型将第二章的十九类算子划为两族：受算力约束者（Prefill 的四类投影与两类注意力矩阵乘）与受带宽约束者（其余全部十三类）。Decode 相位在 $B=32$ 时算力利用率约 10%，即**九成算力空转**——这既是分离式服务的动因，也是投机解码的动因。

### 3.2 通信侧：Hockney $\alpha$-$\beta$ 模型与集合通信下界

$$T = \alpha + \frac{V}{\beta}$$

其中 $\alpha$ 为端到端延迟（含协议栈、交换跳数），$\beta$ 为有效带宽。两个极限分别对应两个相位：

$$V \gg \alpha\beta ;\Rightarrow; T \approx V/\beta \quad(\text{Prefill，带宽受限})$$  
$$V \ll \alpha\beta ;\Rightarrow; T \approx \alpha \quad(\text{Decode，延迟受限})$$

进一步引入集合通信算法的经典下界（Chan、Heimlich、Purkayastha 与 van de Geijn，2007）。对 $N$ 节点、数据量 $V$ 的 all-reduce：

$$T_{\text{ring}} = 2\frac{N-1}{N}\cdot\frac{V}{\beta} + 2(N-1)\alpha \qquad\text{（带宽最优，延迟线性）}$$

$$T_{\text{tree/RHD}} = 2\log_2 N \cdot \frac{V}{\beta} + 2\log_2 N \cdot \alpha \qquad\text{（延迟最优）}$$

**这两个公式解释了一个常被误解的现象：Ring All-Reduce 并非"更好的算法"，而是"为 Prefill 而生、对 Decode 有害的算法"。**$N=64$ 时，Ring 的延迟项为 $126\alpha$，Tree 仅为 $12\alpha$——十倍之差，在 20 μs 的通信预算下即为生死之别。

### 3.3 拓扑侧：四个图论量与四条定理

设互连网络为图 $G=(V,E)$，$|V|=n$，邻接矩阵 $A$，归一化拉普拉斯 $\mathcal{L} = I - D^{-1/2}AD^{-1/2}$，其特征值 $0=\lambda_1 \le \lambda_2 \le \cdots \le \lambda_n$。

**（一）二分带宽**：$\text{BW}_{\text{bisect}} = \min_{|S|=n/2} \sum_{e \in \partial S} c_e$。它刻画最坏切分下的总通行能力，是**容量指标**。Leiserson（1985）证明胖树是"通用网络"，可在多项式常数内模拟任意等造价网络；Valiant（1982）的两阶段随机化路由定理进一步表明，只要二分带宽充足，任意置换流量均可无热点转发。

**（二）直径**：$D = \max_{u,v} \text{dist}(u,v)$。它刻画最坏情形的跳数，直接乘入 $\alpha$，是**延迟指标**。

**（三）谱隙与电导**：Cheeger 不等式给出双向夹逼：

$$\frac{\phi(G)^2}{2} ;\le; \lambda_2 ;\le; 2\phi(G),\qquad \phi(G) = \min_{S}\frac{|\partial S|}{\min(\text{vol}(S),\text{vol}(\bar S))}$$

并且随机游走的混合时间满足 $t_{\text{mix}} = O(\lambda_2^{-1}\log n)$。**谱隙是网络的"搅拌速率"，是均匀性指标。**Alon–Boppana 定理给出 $d$ 正则图的极限 $\lambda_2 \le d - 2\sqrt{d-1} + o(1)$，达到该界者称 Ramanujan 图（Lubotzky、Phillips 与 Sarnak，1988 给出显式构造），是随机置换流量下的理论最优拓扑。

**（四）隔离度**：本白皮书定义为在并发负载 $\mathcal{W}$ 下，目标流可独占获得的带宽比 $\eta = \beta_{\text{eff}}(\mathcal{W}) / \beta_{\text{nominal}}$。它不是纯图论量，而是图论量与队列调度的复合量。

**（五）一条被低估的定理**：Birkhoff–von Neumann 分解指出，任意双随机流量矩阵可分解为置换矩阵的凸组合 $T = \sum_i \alpha_i P_i$，$\sum \alpha_i = 1$。这意味着——**一个能承载任意置换的网络，就能承载一切可行流量。**而"能承载任意置换且不产生热点"的图论刻画正是扩张性，即谱隙。MoE 的路由矩阵恰恰是逐 token 重新抽取的置换，因此 MoE 对拓扑的诉求在数学上被精确地归约为谱隙，而非带宽。

### 3.4 三套模型的正交性

*容量（bisection）、距离（diameter）、均匀性（λ₂）、独占性（isolation）四者在数学上不可互相替代。*一个常见误区是"带宽够大就行"：二分带宽保证最坏一刀的总带宽足够，但不保证在随机置换下不出现局部热点；一个 32 端口交换机组成的哑铃图可以有可观的二分带宽，却因电导极低而在洗牌流量下彻底崩塌。反之，一个高谱隙的随机正则图可能有较大直径，从而在 Decode 相位表现糟糕。

---

## 第四章 六个相位与拓扑原生匹配

将第二章十九类算子按"矩阵形状 + 通信原语"归并，得到六个相位。

```
════════════════ Transformer 推理全景时序图 ════════════════

  用户 Prompt（例：十万 token 代码仓库）
       │
       ├─▶【相位 Ⅴ：词表与采样】共享于 Ⅰ／Ⅱ 末端
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│ 相位 Ⅰ  PREFILL（预填充池）                                   │
│  矩阵：X=[8192×8192] 厚矩阵 GEMM；QKᵀ 产出 [L×L]              │
│  算子：2、3、4、5、6、7、8、9、10、11、12、13、14              │
│  算术强度 I = L ≈ 8192 ≫ I* = 295  → 算力受限                 │
│  通信：all-reduce 134 MB × 160 次（Ring 算法带宽最优）         │
│  主导项：V/β                                                  │
│  ★ 拓扑指标：BISECTION 二分带宽                                │
│  硬件：胖树 full-bisection；Rubin CPX（30 PF NVFP4，          │
│        128 GB GDDR7，3× attention）                           │
│  算法替代：上下文并行 + Ring Attention → 通信降级为近邻        │
└──────────────────────────────────────────────────────────────┘
       │
       │ ┌────────────────────────────────────────────────┐
       └▶│ 相位 Ⅳ  KV CACHE 迁移                          │
         │  矩阵运算：无（纯 DMA）                         │
         │  体量：GQA 32 GB／MLA 7 GB，单向突发大象流      │
         │  优化：逐层流水，与计算重叠                     │
         │  主导项：β_eff 被抢占                           │
         │  ★ 拓扑指标：隔离带宽（割的独占性 η）           │
         │  硬件：独立 rail／独立 NIC／独立平面／SmartNIC   │
         └────────────────────────────────────────────────┘
       │
       ▼
┌──────────────────────────────────────────────────────────────┐
│ 相位 Ⅱ  DECODE（生成池）                                      │
│  矩阵：X=[1×8192] 瘦向量 GEMV，权重读一遍只用一次              │
│  算子：同 Ⅰ，但全部退化为带宽受限                              │
│  算术强度 I = B ≈ 32 ≪ I* = 295 → 内存受限，算力空转 90%      │
│  通信：all-reduce 512 KB × 160 次（Tree／RHD 延迟最优）        │
│  主导项：D·α，单次预算仅 ~20 μs                                │
│  ★ 拓扑指标：DIAMETER 网络直径                                 │
│  硬件：72 卡 NVLink 域，1 跳可达，1.8 TB/s per GPU             │
│                                                               │
│   └─每层内嵌 ┌─────────────────────────────────────────┐      │
│              │ 相位 Ⅲ  MoE 专家路由                     │      │
│              │  矩阵：P = TopK(XW_g)，每 token 重掷骰子  │      │
│              │  dispatch PᵀX → 专家 FFN → combine PZ    │      │
│              │  随机置换 all-to-all，13.3 MB/token       │      │
│              │  EP=64 时 4096 条碎流，无稳定通信模式     │      │
│              │  主导项：热点／电导 φ(G)                  │      │
│              │  ★ 拓扑指标：SPECTRAL GAP 谱隙 λ₂         │      │
│              │  硬件：扩张器／Ramanujan 图；130 TB/s     │      │
│              │        单域全对全；DeepEP ~163 μs         │      │
│              └─────────────────────────────────────────┘      │
│                                                               │
│   └─可选 ┌───────────────────────────────────────────┐         │
│          │ 相位 Ⅵ  投机验证（MTP）                    │         │
│          │  矩阵：[B(γ+1) × d]，介于 Ⅰ 与 Ⅱ 之间       │         │
│          │  I = B(γ+1) → 向算力受限迁移               │         │
│          │  ★ 拓扑指标：直径与带宽的混合诉求           │         │
│          └───────────────────────────────────────────┘         │
└──────────────────────────────────────────────────────────────┘
       │
       ▼
  输出 token 流（ITL 预算 10～20 ms／token）
```

### 4.1 相位 Ⅰ：Prefill —— 厚矩阵搬山，要"车道总数"

当单次归约达 134 MB 时，微秒级的 $\alpha$ 完全被淹没，$T \approx V/\beta$。性能天花板即最坏切分处的跨面总带宽。

```
        ┃ ← 最坏的那一刀（bisection cut）
  ●─●─●─╋─●─●─●     线／环：BW = 1×B        ✗ 搬山即堵死
        ┃
  ●─●─●━╋━●─●─●     胖树：BW = (N/2)×B      ✓ 全速
  ●─●─●━╋━●─●─●
```

三维 Torus 的二分带宽仅按 $N^{2/3}$ 增长，胖树可达全二分。这也是为何 Prefill 集群的拓扑选择几乎与训练集群同构。

### 4.2 相位 Ⅱ：Decode —— 瘦向量传花，要"最远两人的距离"

预算推演如下（这是本白皮书最应被记住的一组数字）：

$$\frac{\text{ITL 预算 } 15\ \text{ms}}{160\ \text{次同步}} = 94\ \mu\text{s／次（含计算）} ;\Rightarrow; \text{通信预算约 } 20\ \mu\text{s} ;\Rightarrow; \text{仅容 } 2!\sim!3\ \text{跳}$$

```
   直径大：GPU ─sw─ sw ─sw─ GPU   往返 6 跳 ≈ 9 μs 起步，预算立即透支
   直径小：GPU ───── 1 跳 ───── GPU   NVLink 域内，1.8 TB/s
```

更严峻的是，all-reduce 具有全局同步语义，服从木桶效应：最慢的一跳决定全队节奏，**尾延迟即真延迟**。NVLink 域从 HGX H200 的 8 卡（900 GB/s）扩展至 GB200 NVL72 的 72 卡（1.8 TB/s，聚合归约 260 TB/s，较 400 GbE 快约 36 倍），其唯一动机正在此。仿真数据显示，大 NVLink 域配合分离式服务，使 70B 级模型在中等延迟区间吞吐提升约 3 倍。

_David Clark（MIT）的判词在此最为贴切_：带宽问题可以用钱解决，延迟问题很难，因为光速是固定的。

### 4.3 相位 Ⅲ：MoE —— 稀疏置换洗牌，要"搅拌均匀度"

```
  T = 0          T = 1          T = 2      ← 每个 token 重新洗牌
  ●╲ ╱●          ●──●           ●╮ ╭●        不存在"常用路径"
  ●╳╳●    ──▶    ●╲╱●    ──▶    ●╳ ╳●        任意一对都可能瞬时成对
  ●╱ ╲●          ●╱╲●           ●╯ ╰●

  低谱隙（哑铃图 λ₂→0）              高谱隙（扩张器 λ₂ 大）
   ◉◉◉ ── 单桥 ── ◉◉◉                ◉─◉─◉    任意两点 O(log n) 跳
   ◉◉◉             ◉◉◉               │╳│╳│    任意随机洗牌均不成热点
   任意洗牌都堵死这座桥                ◉─◉─◉
```

**核心区分（本白皮书的关键论点）**：二分带宽保证"最坏一刀的总带宽够用"，属容量范畴；谱隙保证"任意一刀 × 任意随机置换都不产生热点"，属均匀性范畴。MoE 要的是后者。这一区分由 Birkhoff–von Neumann 分解与 Cheeger 不等式共同支撑，不是经验判断。

### 4.4 相位 Ⅳ：KV 迁移 —— 零算力搬家，要"救护车专用道"

```
  混跑（错误）：═══[KV 32 GB 大象流]═════════════▶ ┐
                ─[decode all-reduce 512 KB]───────┘ 同一 NIC 队列
                → 队头阻塞（HoL blocking）：ITL 由 15 ms 抖升至 60 ms，SLO 破产

  隔离（正确）：═══[KV 迁移]═══▶ 独立 rail／独立 NIC／独立平面／SmartNIC 卸载
                ───[decode]───▶ 优先级队列 + QoS + pacing
                并行叠加：逐层流水，第 k 层算完即传，与计算重叠
```

隔离含两个层次：物理隔离（独立网卡、独立 rail、独立网络平面，或以智能网卡卸载实现无干扰前缀缓存，如 ShadowServe 方案）与逻辑隔离（优先级队列、QoS、发送速率整形、拥塞控制）。代表性系统 Mooncake 以 KV Cache 为中心组织 CPU、DRAM、SSD 与 RDMA 的独立池化与独立传输平面，在特定场景下吞吐提升可达 525%。

_结论要说得直白_：问题从来不是带宽不够，而是不能与别人挤在同一条道上。

### 4.5 相位 Ⅴ：词表与采样 —— 最后一公里的全局同步

嵌入 all-reduce、logits all-gather（250 KB）与采样归约共三次全局同步，消息小、频率等于 token 速率、延迟敏感度与 Decode 相位一致。其拓扑诉求与相位 Ⅱ 同类（小直径），但常因位于流水线首尾而被跨域部署，成为隐蔽的尾延迟来源。**工程建议：词表并行组必须与张量并行组同域共置。**

### 4.6 相位 Ⅵ：投机验证 —— 拓扑诉求的中间态

$I = B(\gamma+1)$，典型 $\gamma = 4$ 时算术强度提升五倍，消息量同步放大五倍。它使 Decode 相位部分脱离纯延迟受限区，向带宽敏感区迁移，从而**同时提高对二分带宽与小直径的要求**——这是六个相位中唯一对两个冲突指标同时提出诉求的相位，也是第七章不可能四边形最尖锐的体现处。

### 4.7 六相位匹配总表

|相位|矩阵形态|算术强度|通信原语|最优算法|消息尺度|主导项|图论指标|原生拓扑|
|---|---|---|---|---|---|---|---|---|
|Ⅰ Prefill|厚×厚 GEMM|$L$（大）|all-reduce／all-gather|Ring（带宽最优）|约 134 MB|$V/\beta$|二分带宽|胖树全二分；Torus + CP|
|Ⅱ Decode|厚×瘦 GEMV|$B$（小）|all-reduce|Tree／RHD（$\log N$）|16～512 KB|$D\cdot\alpha$|直径|高 radix 全互连团|
|Ⅲ MoE|稀疏置换 $P$|碎片化|all-to-all|DeepEP 低时延核|115 KB × $N^2$|电导／热点|谱隙 $\lambda_2$|扩张器／Ramanujan|
|Ⅳ KV 迁移|无（memcpy）|0|P2P bulk|逐层流水重叠|7～32 GB|$\beta_{\text{eff}}$|隔离度 $\eta$|独立 rail／独立平面|
|Ⅴ 词表采样|$[B,d]\times[d,V]$|$B$|all-gather／归约|Tree|250 KB|$D\cdot\alpha$|直径|与 TP 组同域共置|
|Ⅵ 投机验证|$[B(\gamma{+}1),d]$|$B(\gamma{+}1)$|all-reduce|混合|×$(\gamma{+}1)$|$\alpha$ 与 $V/\beta$ 兼有|直径 ∧ 带宽|**冲突区**|

---

## 第五章 并行维度与拓扑维度的映射

五种并行维度对物理网络提出的诉求彼此正交，合理的映射是系统设计的核心工艺。

|并行维度|切分对象|通信原语|频率|拓扑诉求|建议放置层级|
|---|---|---|---|---|---|
|张量并行 TP|权重矩阵行／列|all-reduce|每层 2 次，极高|**小直径、高带宽**|NVLink 域内，绝不跨机|
|专家并行 EP|专家（$P$ 矩阵）|all-to-all|每 MoE 层 2 次|**高谱隙、单域**|同一 NVLink 域（≤72 卡）|
|上下文并行 CP|序列维 $L$|环形 P2P|每注意力层|**近邻带宽**|域内环，或机架内|
|流水线并行 PP|层|send/recv|每层边界 1 次|**近邻，容忍高直径**|跨机架，用 IB／以太|
|数据并行 DP|批|推理期几乎无|极低|无特殊要求|跨集群任意|
|KV 迁移|缓存|P2P bulk|每请求 1 次|**独占平面**|独立网络平面|

_一条可直接使用的设计法则_：按通信频率从高到低，将并行维度由内向外映射到延迟由低到高的网络层级——TP 与 EP 置于最内层（NVLink），CP 次之，PP 最外，KV 迁移单独开平面。违反此序的部署（例如 TP 跨机、EP 跨域）在数学上必然导致 Decode 相位 SLO 失守。

---

## 第六章 端到端预算表（十万 token 输入，70B 稠密／671B 稀疏）

|环节|计算量／数据量|时间量级|主要受限于|
|---|---|---|---|
|分词|—|< 1 ms|CPU|
|Prefill 前向|约 $4\times10^{16}$ FLOP|数秒（8 卡 H100）|算力 + 二分带宽|
|Prefill 归约总量|约 21.5 GB／序列|与计算重叠|二分带宽|
|KV 迁移|32 GB（GQA）／7 GB（MLA）|640 ms（400 G）／18 ms（NVLink）|隔离带宽|
|单 token Decode 计算|140 GFLOP|约 3～5 ms|显存带宽|
|单 token TP 归约|82 MB（$B$=32）|约 2～4 ms|直径 × 频次|
|单 token MoE 全对全|13.3 MB|约 3～8 ms|谱隙|
|logits + 采样|250 KB + KB|约 0.1～0.5 ms|直径|
|**合计 ITL**|—|**目标 10～20 ms**|上述四者的最大值|

_读表要点_：Decode 的每 token 时间是四项的**最大值而非平均值**，因为它们串行于同一条关键路径。任一相位的拓扑失配都会独立地击穿整体 SLO——这是"四句话必须同时成立"的工程含义。

---

## 第七章 不可能四边形：静态拓扑的数学极限

将全部结论压缩为一个统一表达式。通信时间为 $T = \alpha + V/\beta_{\text{eff}}$，再叠加流量置换随机性 $\Pi$ 与并发干扰 $I$：

$$\underbrace{V \gg 0}_{\text{bisection}} \qquad \underbrace{\alpha\text{-bound}}_{\text{diameter}} \qquad \underbrace{\Pi \sim \text{random}}_{\text{spectral gap}} \qquad \underbrace{I \neq 0}_{\text{isolation}}$$

四句话只是四个项在不同相位轮流担任主角。而这里存在一个硬约束：

```
             bisection（需多链路 → 成本墙、功耗墙）
                     ╱          ╲
                    ╱      ✗     ╲
        diameter ──────────────────── λ₂
   （需高 radix，          （需随机连边，
     受引脚墙／            与规则布线、
     SerDes 限制）          可制造性冲突）
                    ╲            ╱
                     ╲          ╱
              isolation（需冗余平面 → 利用率下降）
```

**论证要点**：其一，Moore 界与 Alon–Boppana 界共同限制了给定度数 $d$ 下直径与谱隙的联合可达域，二者不能同时任意优化；其二，高 radix 交换受 SerDes 引脚数与封装面积的物理约束，$d$ 不可无限增大；其三，随机连边虽最优化谱隙，却与规则化布线、等长走线、可制造性直接冲突；其四，隔离要求预留冗余容量，与利用率构成零和。**因此这不是工程手艺问题，而是图论与物理层面的不可兼得。**

更值得注意的是第 2.6 与 4.6 节揭示的两个反向证据：Ring Attention 通过算法改造，把 Prefill 的全局归约降级为近邻交换，**从而把拓扑需求从二分带宽转移开**；投机解码则相反，它把 Decode 拉向带宽敏感区，**同时加重两个冲突指标**。这说明——_算法与拓扑不是层次关系，而是共设计（co-design）关系，需求可以被算法搬运，但不能被消灭。_

---

## 第八章 前瞻：相位可重构互连与其可行性判据

### 8.1 范式命题

既然六个相位在**时间上是可分辨的**，那么正确的解法不是寻找一个在四个指标上折中的静态拓扑，而是让同一批物理链路随相位重构其逻辑结构：

在 Prefill 相位重组为高二分带宽的胖树；在 Decode 相位收缩为小直径的全互连团；在 MoE 相位重连为高谱隙的扩张器；并常驻一条独占平面服务 KV 迁移。这需要软件定义互连（SDI）与元拓扑化合机制作为控制面，需要介观尺度的高密度可编程互连作为数据面。

### 8.2 可行性判据

该范式成立的充分条件是重构时延远小于相位驻留时间：

$$\tau_{\text{recfg}} ;\ll; T_{\text{phase}}$$

据此可对不同重构技术划出严格的适用边界：

|相位边界|相位驻留时间 $T_{\text{phase}}$|可用重构技术|判定|
|---|---|---|---|
|Prefill ↔ Decode|秒级至十秒级|光电路交换 OCS（毫秒级）|✓ 可行，已具工程条件|
|请求间调度|百毫秒级|OCS、SDN 流表|✓ 可行|
|KV 迁移窗口|数十至数百毫秒|独立平面 + QoS|✓ 可行（静态隔离即可）|
|稠密层 ↔ MoE 层|约 100～300 μs|需微秒级重构|△ 仅逻辑重构可行|
|层内 dispatch ↔ combine|约 100 μs|需亚微秒重构|✗ 物理重构不可行|

**这张表是本白皮书最具操作性的结论。**它表明：跨相位的**物理**拓扑重构在 Prefill/Decode 边界上已然可行；而 MoE 的层内相位切换过快，唯一出路是在同一物理域内以**逻辑手段**（路由策略、虚通道、优先级、自适应负载分担）近似实现"高谱隙视图"——即物理上必须一次性提供扩张性，逻辑上再做快速切换。

### 8.3 载体：介观尺度异质异构集成

上述数据面对物理载体提出三项要求：极高的互连密度（以支撑高 radix 与随机连边）、极短的物理距离（以压低 $\alpha$）、动态可塑的连接关系（以支撑重构）。晶圆级／晶矩级异构异质集成在原理上同时满足三者：单一介观平台上整合不同材料、器件与功能模块，可构建高密度、大规模、高维度且动态可塑的物理网络硬件——这正是把 $\lambda_2$、$D$、$\text{BW}_{\text{bisect}}$ 从设计期常量转为运行期变量的技术物理基础。

### 8.4 评价指标提案

建议在现有 MFU、TPS、TTFT、ITL 之外，引入四项拓扑侧指标，用于评估推理集群的结构适配度：相位匹配度（各相位实测时间与其理论下界之比）、重构敏捷度（$T_{\text{phase}}/\tau_{\text{recfg}}$）、置换鲁棒度（随机置换流量下的实测吞吐相对理想值之比，直接反映 $\lambda_2$）、干扰隔离度（$\eta = \beta_{\text{eff}}(\mathcal{W})/\beta_{\text{nominal}}$）。

---

## 第九章 结论

第一，Transformer 推理不是一个负载，而是六个性格互斥的相位。其分野的数学根源是一个不等式：$L \gg I^{*} \gg B$。

第二，每个相位对互连提出的是**不同类别**的图论诉求，而非同一诉求的不同强度：Prefill 要容量（bisection），Decode 要距离（diameter），MoE 要均匀性（$\lambda_2$），KV 迁移要独占性（$\eta$）。四者数学上正交，不可互相替代。

第三，存在不可能四边形，任何静态拓扑无法同时最优。当前所有分离式推理方案只完成了**空间分离**（把 Prefill 与 Decode 放进不同机柜），尚未触及**拓扑的时间复用**。

第四，前瞻性判断：*推理系统的瓶颈已经从节点的算力，转移到网络在时空上重构自身结构的能力。*谁先把谱隙做成一个可实时调度的旋钮，谁就握住了下一代推理系统的定价权。

这也正是"从算力堆砌智能，走向网络时空协同复杂度涌现智能"在推理侧最直接、最可验证的落点——**智能的物理载体不是节点，而是网络；不是网络的静态结构，而是网络重构自身结构的能力。**

---

## 附录 A　白板速算卡

|量|速算式|典型值（70B／$d$=8192／80 层）|
|---|---|---|
|Roofline 转折点|峰值算力 ÷ 显存带宽|H100 约 295 FLOP/Byte|
|Prefill 算术强度|$I = L$|$L$=8192 → 8192|
|Decode 算术强度|$I = B$|$B$=32 → 32|
|单次 TP 归约量|$L\cdot d\cdot b$|Prefill 134 MB／Decode 512 KB|
|每 token 同步次数|$2n_l + 3,(+2n_{\text{moe}})$|稠密 163／稀疏 279|
|单次同步预算|ITL ÷ 同步次数|15 ms → 94 μs（通信约 20 μs）|
|KV 每 token|$2n_l n_{kv} d_h b$|GQA 320 KB／MLA 70 KB|
|MoE 每 token 每层|$2k,d,b$|约 229 KB（×58 层 = 13.3 MB）|
|logits 每 token|$V\cdot b$|约 250 KB|
|注意力／投影交叉点|$4Ld \approx$ 单层投影 FLOP|$L \approx 5\times10^{4}$|
|Ring 归约延迟项|$2(N-1)\alpha$|$N$=64 → $126\alpha$|
|Tree 归约延迟项|$2\log_2 N\cdot\alpha$|$N$=64 → $12\alpha$|

## 附录 B　符号表

$L$ 序列长度；$B$ 批大小；$d$ 隐藏维；$d_h$ 头维；$n_l$ 层数；$n_{kv}$ 键值头数；$E$ 专家总数；$k$ 每 token 激活专家数；$V$ 词表大小；$b$ 单元素字节数；$\gamma$ 投机草稿长度；$\Pi$ 峰值算力；$\beta$ 带宽；$\alpha$ 端到端延迟；$I$ 算术强度；$I^{*}$ Roofline 转折点；$D$ 网络直径；$\lambda_2$ 归一化拉普拉斯次小特征值（谱隙）；$\phi(G)$ 电导；$\eta$ 隔离度；$\tau_{\text{recfg}}$ 拓扑重构时延；$T_{\text{phase}}$ 相位驻留时间。

## 附录 C　主要参考文献

Williams、Waterman 与 Patterson，《Roofline: An Insightful Visual Performance Model》，CACM，2009。Shoeybi 等，《Megatron-LM》，2019。Korthikanti 等，《Reducing Activation Recomputation in Large Transformer Models》，MLSys，2023。Dao 等，《FlashAttention》，NeurIPS，2022。Liu 等，《Ring Attention with Blockwise Transformers》，2023。Kwon 等，《Efficient Memory Management for LLM Serving with PagedAttention》，SOSP，2023。Ainslie 等，《GQA》，EMNLP，2023。Su 等，《RoFormer: Enhanced Transformer with Rotary Position Embedding》，2021。Zhang 与 Sennrich，《Root Mean Square Layer Normalization》，NeurIPS，2019。Shazeer，《GLU Variants Improve Transformer》，2020。Leviathan 等，《Fast Inference from Transformers via Speculative Decoding》，ICML，2023。Holtzman 等，《The Curious Case of Neural Text Degeneration》，ICLR，2020。Chan 等，《Collective Communication: Theory, Practice, and Experience》，CCPE，2007。Leiserson，《Fat-Trees: Universal Networks for Hardware-Efficient Supercomputing》，IEEE TC，1985。Valiant，《A Scheme for Fast Parallel Communication》，SICOMP，1982。Lubotzky、Phillips 与 Sarnak，《Ramanujan Graphs》，Combinatorica，1988。Alon 与 Milman，《λ₁, Isoperimetric Inequalities for Graphs and Superconcentrators》，JCTB，1985。Qin 等，《Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving》，FAST，2025。DeepSeek-AI，《DeepSeek-V3 Technical Report》，2024。NVIDIA，《Beyond the Buzz: A Pragmatic Take on Inference Disaggregation》，2025。NVIDIA，《Rubin CPX Accelerates Inference for 1M-Token Context Workloads》，2025。

---

**（全文完）**

