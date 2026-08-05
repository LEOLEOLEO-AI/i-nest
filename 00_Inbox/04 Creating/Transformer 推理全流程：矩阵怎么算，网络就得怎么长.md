# Transformer 推理全流程：矩阵怎么算，网络就得怎么长

## 〇、总纲：一句话

**Transformer 推理的四个相位，本质是同一组矩阵乘法在"形状"上的四次剧变；形状一变，通信原语跟着变，拓扑的最优解也跟着变。**

所以那四句话不是四条调参经验，而是四个矩阵形状对物理网络提出的**原生结构诉求**：

```
  矩阵形状  ──→  并行切分  ──→  通信原语  ──→  拓扑指标
  ─────────────────────────────────────────────────────
  厚矩阵 GEMM      张量/上下文并行   大块 all-reduce    二分带宽 bisection
  瘦向量 GEMV      张量并行         微型 all-reduce     直径 diameter
  稀疏置换 P       专家并行         随机 all-to-all     谱隙 λ₂
  纯搬运 memcpy    池间迁移         单向大象流          隔离带宽
```

---

## 一、先把 Transformer 推理拆成 6 个矩阵动作

抛开所有工程包装，一层 Transformer 只做六件事（$X$ 为激活，$d$ 为隐藏维，$L$ 为序列长）：

$$  
\begin{aligned}  
&\text{①投影：} && Q,K,V = X W_Q,; X W_K,; X W_V &&\quad [L,d]\times[d,d]\  
&\text{②打分：} && S = QK^{\top}/\sqrt{d_h} &&\quad [L,d_h]\times[d_h,L]\ \Rightarrow\ [L,L]\  
&\text{③加权：} && O = \mathrm{softmax}(S),V &&\quad [L,L]\times[L,d_h]\  
&\text{④输出：} && Y = O W_O &&\quad [L,d]\times[d,d]\  
&\text{⑤路由：} && P = \mathrm{TopK}(X W_g) &&\quad [L,d]\times[d,E]\ \Rightarrow\ \text{稀疏 }[L,E]\  
&\text{⑥专家：} && Z = \mathrm{FFN}_e(P^{\top}X),\ \ \hat{Y}=P Z &&\quad [\cdot,d]\times[d,4d]\times[4d,d]  
\end{aligned}  
$$

注意第②步：$QK^\top$ 产出一个 $L\times L$ 的方阵，这就是长上下文一切痛苦的源头——**它是唯一随 $L$ 平方增长的东西**。而第⑤步的 $P$ 是一个每 token 重新掷骰子的稀疏 0/1 矩阵——这是 MoE 一切痛苦的源头。

---

## 二、最关键的一次相变：$L=8192 \to L=1$

Prefill 与 Decode 跑的是**完全相同的权重、完全相同的算子**，唯一区别是激活矩阵的行数：

```
   PREFILL：X = [ 8192 × 8192 ]        DECODE：X = [ 1 × 8192 ]
        ┌──────────────────┐               ┌──────────────────┐
        │██████████████████│               │██████████████████│  ← 只有一行！
        │██████████████████│               └──────────────────┘
        │██████████████████│  ×  W          ×  W
        │██████████████████│               厚矩阵×瘦向量 = GEMV
        │       ...        │               权重被读一遍，只用一次
        └──────────────────┘               ══> 内存墙
        厚矩阵×厚矩阵 = GEMM
        权重被读一遍，复用 8192 次
        ══> 算力墙
```

用 Roofline（Williams & Patterson）把它量化。计算强度 $I$（FLOP/Byte，BF16 权重主导）：

$$I_{\text{prefill}}=\frac{2Ld^2}{2d^2}=L \qquad\qquad I_{\text{decode}}=\frac{2Bd^2}{2d^2}=B$$

H100 的转折点（ridge point）$I^* = 989,\text{TFLOPS} / 3.35,\text{TB/s} \approx 295$。于是：

||计算强度|与 $I^*!\approx!295$ 比较|结论|
|---|---|---|---|
|Prefill|$I=L=8192$|远大于|计算受限，GPU 算力吃满|
|Decode|$I=B=32$|远小于|带宽受限，算力闲置 ~90%|

**这一个不等式 $L \gg I^* \gg B$，就是"分离式推理"（Prefill/Decode Disaggregation）存在的全部数学理由。**把两种计算强度差 200 倍的负载塞进同一台机器，必然一边饿死一边撑死。NVIDIA 索性为此造了两种芯片：Rubin CPX（30 PFLOPS NVFP4 + 128 GB GDDR7，3× attention 加速）专供 prefill 的算力墙，标准 Rubin 专供 decode 的内存墙。

---

## 三、矩阵怎么切，通信就怎么长出来

这是全文最需要"看见"的一步。Megatron 式张量并行不是给算子加通信，而是**切开矩阵后，加法的补齐动作变成了通信**。

```
【列并行】W 按列切：  Y = X·[W₁ | W₂] = [X W₁ | X W₂]
   GPU0 ──► XW₁ ─┐
   GPU1 ──► XW₂ ─┘   拼接即可，前向零通信 ✓

【行并行】W 按行切：  Y = [X₁ | X₂]·[W₁ ; W₂] = X₁W₁ + X₂W₂
   GPU0 ──► X₁W₁ ─┐
                  ├──►  ✚  必须求和 ──►  ALL-REDUCE（前向强制同步）
   GPU1 ──► X₂W₂ ─┘
```

于是每层出现**恰好 2 次 all-reduce**（Attention 的 $W_O$ 之后、FFN 的下投影之后）。这不是设计选择，是矩阵分块乘法的**代数必然**：部分和必须相加。

把数字代进去，同一个 all-reduce 在两个相位的体量差异令人不适（$d=8192$，BF16，80 层）：

||单次 all-reduce 体量|每 token/序列总同步量|同步次数|
|---|---|---|---|
|Prefill（$L$=8192）|$Ld\cdot2 = 134$ MB|≈ 21.5 GB／序列|160 次|
|Decode（$B$=32）|$Bd\cdot2 = 512$ KB|≈ 82 MB／token|160 次|
|Decode（$B$=1）|$16$ KB|2.6 MB／token|160 次|

**同一个原语，消息量相差 260～8000 倍。**这就是"同一根线，两种物理"的根源。

---

## 四、四相位 × 四指标：逐一看图

### ① Prefill 要 bisection ——厚矩阵搬山，要的是"车道总数"

Hockney 模型 $T=\alpha+V/\beta$。当 $V=134,$MB 时，微秒级的 $\alpha$ 完全被淹没，$T\approx V/\beta$。**性能上限就是总吞吐，也就是最坏一刀的跨切面带宽——bisection bandwidth。**

```
        ┃ ← 最坏的那一刀
  ●─●─●─╋─●─●─●     线/环：bisection = 1×B      ✗ 搬山堵死
        ┃
  ●─●─●━╋━●─●─●     胖树：bisection = (N/2)×B    ✓ 全速
  ●─●─●━╋━●─●─●     （Leiserson 1985：胖树是"通用网络"）
```

Valiant 随机化路由定理进一步说明：只要 bisection 足够，任意置换流量都可两阶段无热点转发——bisection 是**容量层面的通行证**。

但这里有个漂亮的反例，值得单独框起来：

> **算法可以改写拓扑需求。** Prefill 若改用上下文并行 + Ring Attention，$L\times L$ 的打分矩阵沿 $L$ 切块，$K,V$ 块沿环形逐跳轮转——通信退化为**纯近邻**，只吃邻居带宽，不吃全局 bisection。Ring All-Reduce 同理：$T=2\frac{N-1}{N}\frac{V}{\beta}+2(N-1)\alpha$，带宽最优、延迟随 $N$ 线性增长——**天生为 prefill 而生，天生毒害 decode。**

### ② Decode 要小直径 ——瘦向量传花，要的是"最远两人的距离"

当 $V\to$ KB 级，$V/\beta \to 0$，时间退化为 $T\approx D\cdot\alpha$（$D$ 为跳数）。做一次预算，生死线立刻显形：

```
   ITL 预算 15 ms ÷ 160 次全局同步 = 94 μs／次（含计算）
   通信预算 ≈ 20 μs   →   单跳 ~1.5 μs（含协议栈）→ 只够 2～3 跳！
```

```
   直径大：GPU ─sw─ sw ─sw─ GPU     来回 6 跳 ≈ 9 μs 起步，预算即刻透支
   直径小：GPU ──── 单跳 ──── GPU     NVLink 域内 1 跳，1.8 TB/s
```

而且 all-reduce 是**全局同步语义**，服从木桶效应：最慢那一跳决定整队节奏，尾延迟即真延迟。算法侧也必须换人——decode 弃用 Ring，改用 Tree / Recursive-Halving-Doubling，延迟 $O(\log N)\cdot\alpha$，其原生拓扑诉求正是**超立方式的高 radix 短直径**。

这就是 NVLink 域从 8 卡（900 GB/s）扩到 GB200 NVL72 的 72 卡（1.8 TB/s，聚合 all-reduce 260 TB/s，较 400 GbE 快约 36 倍）的唯一动机。NVIDIA 仿真显示，大 NVLink 域 + 分离式服务使 Llama-70B 在中等延迟区吞吐提升约 3 倍。

David Clark（MIT）那句判词在此处最为精准：_“带宽问题可以用钱解决，延迟问题很难，因为光速是固定的。”_

### ③ MoE 要高谱隙 ——稀疏置换洗牌，要的是"搅拌均匀度"

这是四句话里最深、也最容易被误读为"MoE 要大带宽"的一句。看清它必须回到路由矩阵 $P$：

$$\text{dispatch: } \tilde X = P^{\top}X \qquad\qquad \text{combine: } \hat Y = P Z$$

$P \in {0,1}^{L\times E}$ 每行恰有 $k$ 个 1（DeepSeek-R1：$E=256$，$k=8$），**且每个 token 重新掷骰子**。所以 MoE 的流量矩阵不是固定模式，而是**随机置换流**。

```
  T = 0          T = 1          T = 2       每一步 P 重新洗牌
  ●╲ ╱●          ●──●           ●╮ ╭●       没有任何"常用路径"可优化
  ●╳╳●    ──►    ●╲╱●    ──►    ●╳ ╳●       任意一对都可能瞬时成对
  ●╱ ╲●          ●╱╲●           ●╯ ╰●
```

这里有一条常被忽略的定理级依据：**Birkhoff–von Neumann 分解**——任意双随机流量矩阵都可写成置换矩阵的凸组合 $T=\sum_i \alpha_i P_i$。也就是说，**一个能承载任意置换的网络，就能承载一切可行流量**。而"能承载任意置换且不出热点"的图论刻画，正是扩张性（expansion），由 Cheeger 不等式与谱隙双向夹住：

$$\frac{\phi(G)^2}{2};\le;\lambda_2;\le;2\phi(G),\qquad t_{\text{mix}}=O!\left(\lambda_2^{-1}\log n\right)$$

```
  低谱隙（λ₂→0）                  高谱隙（扩张器）
   ◉◉◉ ── 单桥 ── ◉◉◉              ◉─◉─◉    任意两点 O(log n) 跳
   ◉◉◉             ◉◉◉             │╳│╳│    任意随机洗牌均不成热点
   任意洗牌都堵死这座桥              ◉─◉─◉
```

**关键区分：bisection 保证"最坏一刀的总带宽够用"（容量）；谱隙保证"任意一刀 × 任意随机置换都不出热点"（均匀性）。MoE 要的是后者。**理论最优是 Ramanujan 图（$|\lambda_i|\le 2\sqrt{d-1}$，触达 Alon–Boppana 下界，LPS 显式构造）——这正是近年 AI 网络拓扑研究频繁引入它的原因。

量级感受一下（R1：$d=7168$，top-8，58 个 MoE 层）：单 token 单层 dispatch+combine ≈ 230 KB，×58 层 ≈ 13 MB／token——**比稠密 all-reduce 大一个数量级，且被打散成 $N^2$ 条碎流**（EP=64 时 4096 条）。工程后果非常刚性：R1 decode 最优约每 GPU 4 专家 → 64 GPU 必须**全部落在同一个低延迟高带宽域内**；一旦专家跨出 NVLink 域掉到 InfiniBand，all-to-all 立刻被慢速域拖垮。GB200 NVL72 的 130 TB/s 聚合 all-to-all、DeepEP 把 dispatch 压到 ~163 μs，都是为这条约束而生；仿真显示 R1 在中等延迟区可获约 6 倍吞吐增益。

### ④ KV 迁移要隔离带宽 ——零矩阵运算的搬家，要的是"专用道"

KV Cache 迁移是四者中唯一**不做任何矩阵运算**的相位，纯 DMA 搬运。但它的体量最野蛮：

$$V_{\text{KV}} = 2\cdot L\cdot n_{\text{layer}}\cdot n_{\text{kv}}\cdot d_h\cdot b$$

Llama-70B（80 层、GQA 8 头、$d_h$=128、FP16）→ **320 KB／token**；10 万 token 上下文 → **32 GB**。走 400 G 网络需 0.64 s，走 NVLink 仅 18 ms。

它本身对延迟不敏感，但对邻居是灾难——因为它是典型**大象流**：

```
  混跑（错误）：═══[KV 32 GB 大象流]═════════▶ ┐
                ─[decode all-reduce 512 KB]───┘ 同一 NIC 队列
                → 队头阻塞 HoL：ITL 从 15 ms 抖到 60 ms，SLO 直接破产

  隔离（正确）：═══[KV 迁移]═══▶  独立 rail／独立 NIC／独立平面／SmartNIC 卸载
                ───[decode]───▶  优先级队列 + QoS + pacing
                + 逐层流水：第 k 层算完即传，与计算重叠，隐藏迁移时延
```

代表系统：Mooncake（Kimi）以 KVCache 为中心组织 CPU/DRAM/SSD/RDMA 独立池与独立传输平面，特定场景吞吐提升可达 525%；ShadowServe 用 SmartNIC 卸载做到 interference-free 前缀缓存。**结论不是带宽不够，而是不能与别人挤在一条道上。**

---

## 五、全景总图：把矩阵、算子、通信、拓扑叠在一张图上

```
════════════════════ 一次推理请求的一生 ════════════════════

 用户 Prompt（10 万 token 代码仓库）
      │
      ▼
┌─────────────────────────────────────────────────────────┐
│ ① PREFILL 池          矩阵：[8192×8192] GEMM，QKᵀ 出 L²   │
│    算子：Attention + FFN 全并行                          │
│    通信：all-reduce 134 MB × 160，ring 算法              │
│    瓶颈：V/β  ══════════════▶  ★ BISECTION 二分带宽       │
│    硬件：胖树 full-bisection／Rubin CPX 专用算力芯片      │
└─────────────────────────────────────────────────────────┘
      │
      │ ② KV 迁移   矩阵运算：无（纯 DMA）
      │    32 GB 单向大象流，逐层流水与计算重叠
      │    瓶颈：β_eff 被抢  ═══▶  ★ 隔离带宽（独立平面／QoS）
      ▼
┌─────────────────────────────────────────────────────────┐
│ ③ DECODE 池           矩阵：[1×8192] GEMV（计算强度=B）   │
│    算子：权重全量重读，算力闲置 90%                       │
│    通信：all-reduce 512 KB × 160，tree 算法              │
│    瓶颈：D·α，20 μs 预算  ═══▶  ★ DIAMETER 小直径         │
│    硬件：72 卡 NVLink 域，1 跳可达，1.8 TB/s              │
│                                                          │
│   └─每层内嵌 ④ MoE：P = TopK(XWg) 每 token 重掷骰子      │
│       dispatch Pᵀ X → 专家 FFN → combine P Z             │
│       随机置换 all-to-all，13 MB/token，N² 条碎流         │
│       瓶颈：热点／电导  ═══▶  ★ SPECTRAL GAP 高谱隙        │
│       硬件：扩张器拓扑，130 TB/s a2a 单域                 │
└─────────────────────────────────────────────────────────┘
      │
      ▼
 输出 token 流（ITL 预算 10～20 ms／token）
```

## 六、终极对照表

|相位|矩阵形态|计算强度|通信原语|最优算法|消息尺度|主导项|图论指标|原生拓扑|
|---|---|---|---|---|---|---|---|---|
|Prefill|厚×厚 GEMM|$L$（大）|all-reduce / all-gather|Ring（带宽最优）|100 MB|$V/\beta$|二分带宽|胖树、Torus（+CP）|
|Decode|厚×瘦 GEMV|$B$（小）|all-reduce|Tree／RHD（$\log N$）|KB～百 KB|$D\cdot\alpha$|直径|高 radix 全互连团|
|MoE|稀疏置换 $P$|碎片化|all-to-all|DeepEP 低时延核|中小 × $N^2$|热点／电导|谱隙 $\lambda_2$|扩张器／Ramanujan|
|KV 迁移|无（memcpy）|—|P2P bulk|逐层流水重叠|GB|$\beta_{\text{eff}}$|割的独占性|独立 rail／平面|

---

## 七、结论与前瞻：不可能四边形，与"拓扑的时间复用"

把上面全部收敛成一个公式——通信时间 $T=\alpha+V/\beta_{\text{eff}}$，再叠加流量置换随机性 $\Pi$ 与并发干扰 $I$：

$$\underbrace{V\gg 0}_{\text{bisection}}\quad \underbrace{\alpha\text{-bound}}_{\text{diameter}}\quad \underbrace{\Pi\sim\text{random}}_{\text{spectral gap}}\quad \underbrace{I\neq 0}_{\text{isolation}}$$

四句话只是四个项轮流当主角。而这里藏着一个硬约束——**不可能四边形**：

```
        bisection（要多链路 → 成本／功耗墙）
              ╱  ╲
             ╱ ✗  ╲          任何静态拓扑
   diameter ╱──────╲ λ₂       都无法同时最优化这四者
  （要高 radix    （要随机连边
    → 引脚墙）      → 与规则布线冲突）
              ╲  ╱
           isolation（要冗余平面 → 利用率下降）
```

这是图论层面的不可兼得，不是工程手艺问题。因此真正的出路不是继续堆带宽，而是：

**既然 prefill、decode、MoE、KV 迁移在时间上是可分辨的相位，拓扑就应该随相位切换。**在介观尺度上以软件定义互连（SDI）与元拓扑化合机制，让同一批物理链路——在 prefill 相位重组为高 bisection 的胖树，在 decode 相位收缩为小直径的全互连团，在 MoE 相位重连为高谱隙的扩张器，并常驻一条独占平面服务 KV 迁移。

当前所有分离式推理（Disaggregation）都只做到了**空间分离**：把 prefill 和 decode 放进不同机柜。而真正尚未被开采的红利在**拓扑的时间复用**——让 $\lambda_2$、$D$、bisection 从"设计期的常量"变成"运行期可调度的变量"。

这也正是"从算力堆砌智能，走向网络时空协同复杂度涌现智能"在推理侧最直接、最可验证的落点：**智能的瓶颈已经从节点的算力，转移到网络在时空上重构自身结构的能力。**谁先把谱隙做成一个可实时调度的旋钮，谁就握住了下一代推理系统的定价权。

---

## 附：数量级速算卡（可直接贴在白板上）

|量|速算式|典型值（70B／$d$=8192／80 层）|
|---|---|---|
|Roofline 转折点|算力 ÷ 带宽|H100 ≈ 295 FLOP/Byte|
|单次 TP all-reduce|$L\cdot d\cdot b$|prefill 134 MB／decode 512 KB|
|每 token 同步次数|$2\times n_{\text{layer}}$|160 次|
|单次同步预算|ITL ÷ 160|15 ms → 94 μs（通信 ~20 μs）|
|KV 每 token|$2,n_{\text{layer}}n_{\text{kv}}d_h b$|320 KB → 10 万 token = 32 GB|
|MoE 每 token 每层|$2k\cdot d\cdot b$|R1 ≈ 230 KB（×58 层 = 13 MB）|

---

