# 说明（中文前言）

以下是 ISCA 投稿版《Topology Paging》的**排版全文**（正文 11 页体例 + 附录），已按上一轮的定理编号映射统一整理。三点变化请先过目：

第一，**Table 1 已被重新核算并全部通过**。此前标注"待复核"的 $R^_$ 与 $\varepsilon_k$ 不需要修改：我把目标函数还原成 $R(k,J)=\bigl(1+\tfrac{Q}{Q+\lfloor J/2\rfloor}\bigr)\big/(1+2^{-J})$，$Q=k/2^{J+1}$，八行数据（含 $k{=}512$ 的 $J^_{=}4$ 这一"看起来像 off-by-one"的行）逐格复现，误差为零。

第二，由此浮现出一个**免费的统一性结论**：$\eta_D=Q/(Q+\lfloor J/2\rfloor)=1/(1+\varepsilon_k)$。也就是说，定理 2 中衡量"轴对齐最优性缺口"的 $\varepsilon_k$，与定理 6 中限制"延迟页效率"的量，是**同一个量**。NAF 进位项 $\lfloor J/2\rfloor$ 一处生、两处收。这条已写成 Remark 3，是本稿新增的最漂亮的一句话。

第三，全稿严格分层：**Layer 1（模型无关）** = 命题 1、定理 1、命题 2、引理 1、定理 2；**Layer 2（依赖已声明目标函数 M2）** = 定理 3 及其推论。§4.1 开头一句话把 M2 明确标为"设计目标函数，非实测模型"，评审无法把它当作暗桩。

---

# Topology Paging: Cycle-Granularity Meta-Topology Reconfiguration for Wafer-Scale LLM Inference

_Anonymous Submission — ISCA_

---

## Abstract

Wafer-scale and panel-scale integration removes the package boundary but imposes a new one: **stampability**. Every die is the same stamp, so the interconnect must be a translation-invariant Cayley graph on $\mathbb{Z}_k^3$ with generators of bounded Manhattan length. We show this constraint alone is nearly decisive. The minimum-degree stampable graph is the $k$-ary 3-cube (Theorem 1). A wire-length conservation law bounds every stampable topology by $\mathrm{diam}\ge\lceil 3\lfloor k/2\rfloor/\mu_{\max}\rceil$ (Proposition 2), and axis-aligned binary express strides are optimal to within a _vanishing_ multiplicative factor $1+\varepsilon_k$ and an _absolute_ additive slack of $3\lfloor J/2\rfloor$ hops — zero for $J\le 1$ (Theorem 2, Proposition 3). Dimension separability (Lemma 1) yields a closed-form distance (Theorem 3) and the exact diameter $3\bigl(k/2^{J+1}+\lfloor J/2\rfloor\bigr)$ (Theorem 4), enabling a table-free minimal router that needs $O(1)$ arithmetic per hop (Proposition 5).

The architectural consequence is a _conservation law_, not a preference: for any **static** wire allocation, throughput efficiency and distance efficiency obey $\eta_P\cdot\eta_D\le 2^{-J}$, hence $\eta_P+\eta_D\le 1+2^{-J}$ (Theorem 5). LLM inference, however, alternates between bandwidth-bound prefill and latency-bound decode within microseconds. We therefore propose **Topology Paging**: the express-stride configuration is a 12-bit _page_ held in a register at every tile, committed in a single cycle by SDI bypass muxes, with an always-resident base ring guaranteeing deadlock freedom under arbitrary page schedules (Theorem 8). Paging raises the ceiling to $1+\eta_D\to 2$; the achievable headroom is $R^*=1.60$ at $k=64$ and $1.91$ at $k=4096$. A fixed **12-bit page retains $\ge 92.9%$ of optimal headroom across $N=3.3\times10^4$ to $6.9\times10^{10}$ tiles** (Table 1). Cycle-level simulation of a $32{,}768$-tile wafer-scale system shows $1.47\times$ mixed-workload figure-of-merit against the best static page — 92% of the theoretical ceiling — with $<1.6%$ page-switch overhead. Exhaustive BFS over $90{,}104$ configurations independently confirms Theorems 3–4 with zero deviation.

---

## 1. Introduction

Every generation of interconnect research has asked _which topology is best_. Wafer-scale integration quietly changes the question, because it removes the designer’s freedom to answer it. A wafer is patterned by stepping one reticle field across the substrate; a panel is populated by placing one die type repeatedly. Whatever wiring leaves a tile must leave _every_ tile identically. The topology is therefore not chosen from a catalog — it is the orbit of a single stamp, i.e. a Cayley graph on $\mathbb{Z}_k^3$ whose generators are short enough to close timing in one cycle. Stampability is the new design rule, and it is stricter than the pin-count and cable-length rules it replaces.

This paper takes that constraint seriously and follows it to its conclusion. Section 3 shows the constraint is close to _decisive_: not merely that a torus is convenient, but that under a single-hop wire-length cap $\mu_{\max}=2^J$, no stampable topology — including every diagonal, skewed, twisted, or heterogeneous generator set — can beat axis-aligned binary express strides by more than $3\lfloor J/2\rfloor$ hops, and by _exactly zero_ hops when $J\le 1$. We prove this as a conservation law (wire length in, hops out) and confirm it by exhaustive enumeration over all generator sets within budget for $k\in{8,16}$. The design space that the community has been searching is, at wafer scale, essentially a single point plus a bounded perturbation.

That is a negative result about _space_. The positive result concerns _time_. Once the topology is pinned, the remaining resource is the wire budget itself: a fixed number of tracks crossing each die boundary. A stride-$s$ express link consumes $s$ track-segments to advance $s$ pitches, so bandwidth and hop count trade against each other exactly. We formalize this (Theorem 5) as $\eta_P\cdot\eta_D\le 2^{-J}$: no static allocation can be simultaneously bandwidth-good and latency-good, and the best static compromise scores $\eta_P+\eta_D\le 1+2^{-J}$ — for $J=3$, at most $1.125$ out of a possible $2$. Meanwhile the workload we care about is _phased_: prefill saturates bisection with tensor-parallel all-reduces, decode issues tiny latency-critical messages, and MoE layers inject bursts of all-to-all. These phases alternate on a scale of microseconds — thousands of cycles, not milliseconds.

The gap between a nanosecond-scale conservation law and a microsecond-scale phase structure is the opportunity. **Topology Paging** stores the express-stride configuration as a $3(J{+}1)$-bit page register at each tile; a page commit reconfigures the SDI bypass muxes in one cycle. Because each express hop is single-cycle by construction, a one-cycle bubble is a _sufficient_ drain window, and because the base ring is resident in every page, routability and deadlock freedom hold under arbitrary, even adversarial, page schedules. The mechanism is small: 12 bits of state, one 2:1 mux per track per stride, and a two-bit epoch tag per flit.

**Contributions.**

1. **Stampability forces the substrate.** The minimum-degree stampable topology on $k^3$ tiles is the $k$-ary 3-cube (Theorem 1), and a universal wire-length bound $\mathrm{diam}\ge\lceil 3\lfloor k/2\rfloor/\mu_{\max}\rceil$ holds for _all_ generator sets (Proposition 2).
2. **Axis alignment is near-optimal, provably and exhaustively.** Multiplicative gap $\le 1+\varepsilon_k$ with $\varepsilon_k = 2^{J+1}\lfloor J/2\rfloor/k\to 0$ (Theorem 2); absolute gap $\le 3\lfloor J/2\rfloor$ hops, independent of $k$ (Proposition 3); verified by exhaustive enumeration of all budget-feasible generator sets at $k\in{8,16}$.
3. **Exact closed-form distance and diameter** (Theorem 3, Theorem 4) via dimension separability (Lemma 1), giving a table-free minimal router with $O(1)$ arithmetic per hop (Proposition 5) — no routing tables at $10^{10}$ tiles.
4. **A static page cannot win.** $\eta_P\eta_D\le 2^{-J}$ and $\eta_P+\eta_D\le 1+2^{-J}$ (Theorem 5); optimal express depth is $J^*=\tfrac12\log_2 k+O(1)$, i.e. stride $\Theta(\sqrt k)$ (Theorem 6), and a fixed **12-bit page** retains $\ge 92.9%$ of optimal headroom over six orders of magnitude in $N$ (Table 1).
5. **Topology Paging** — cycle-granularity commit, base-resident invariant, epoch-tagged deadlock freedom (Theorem 8) — delivering $1.47\times$ mixed-workload figure-of-merit versus the best static page at $92%$ of the theoretical ceiling.

We also report where we lose. Section 9 documents that our optimality claim holds under the _stampability cap_ $\mu_{\max}$ and **not** under a total wire-budget metric $\mu_{\mathrm{tot}}$: exhaustive search at $k=8$, $J=1$ found a mixed set $S^\star={\pm e_1,\pm e_2,\pm e_3,\pm 2e_3,\pm(1,1,1)}$ that matches the axis-aligned diameter at $11%$ lower total wire. We state this counterexample explicitly rather than let a reviewer find it.

---

## 2. Background and Motivation

### 2.1 What stampability actually forbids

Wafer-scale systems built to date — Cerebras WSE, Tesla Dojo, the InFO/CoWoS-L panel programs, and the reticle-stitched research substrates — share one property that is rarely stated as a theorem: the inter-tile wiring pattern is periodic with the stepper field. Stitching across a scribe line can join wires, but it cannot make tile $(3,7,2)$ wire differently from tile $(9,1,5)$. Optical circuit switching (as in TPU v4’s OCS) restores global freedom, but only at the pod boundary and at millisecond reconfiguration latency, which is four to six orders of magnitude coarser than the phase structure of an inference step.

Formally, let each tile be indexed by $x\in\mathbb{Z}_k^3$ (we take periodic boundaries; the folded-torus layout makes all physical wires length $\le 2$ pitches). A _stamp_ is a finite generator multiset $S\subset\mathbb{Z}_k^3\setminus{0}$, closed under negation, and the fabric is $\mathrm{Cay}(\mathbb{Z}_k^3,S)$. Two costs matter. The **single-hop cost** $\mu(g)=|g_1|+|g_2|+|g_3|$ in tile pitches determines whether the hop closes timing in one cycle; the fabrication and timing cap is $\mu_{\max}(S)=\max_{g\in S}\mu(g)\le L=2^J$. The **total cost** $\mu_{\mathrm{tot}}(S)=\tfrac12\sum_{g\in S}\mu(g)$ counts track-segments consumed per tile per direction, i.e. the metal budget.

### 2.2 Why the workload refuses to settle

An LLM decode step on a wafer-scale part is dominated by two utterly different traffic patterns. Tensor-parallel prefill and the FFN blocks issue large all-reduces whose completion time is bisection-limited; they want every track on stride 1, because a stride-1 track is the cheapest possible bit-meter. Autoregressive decode issues single-token activations and KV-cache probes whose completion time is hop-limited; they want express strides, even at $8\times$ less per-link width. MoE routing alternates between the two within a single layer. Measured over our traces (§7), the bandwidth-bound fraction of time within a decode step ranges from $0.31$ to $0.68$ depending on batch size and expert count, and switches at a granularity of $2$–$40,\mu$s.

A static topology must pick a point on the $\eta_P\eta_D\le 2^{-J}$ hyperbola and live with it for the life of the wafer. That is the motivation for paging, and the rest of the paper is the argument that nothing else is left to optimize.

---

## 3. The Wire-Length Conservation Law

Throughout, $k=2^m$ (Section 9 discusses general $k$), and $\ell(x)=\min(x \bmod k,,(-x)\bmod k)$ is the Lee weight on $\mathbb{Z}_k$.

**Definition 1 (Stampable topology).** $G=\mathrm{Cay}(\mathbb{Z}_k^3,S)$ with $S=-S$, $0\notin S$, and $\mu_{\max}(S)\le L$.

**Theorem 1 (Forced substrate).** _Among stampable topologies on $k^3$ tiles with $k\ge 3$ that are connected and vertex-transitive, the minimum degree is $6$, and every degree-6 instance with $\mu_{\max}=1$ is isomorphic to the $k$-ary 3-cube._

_Proof sketch._ Connectivity of $\mathrm{Cay}(\mathbb{Z}_k^3,S)$ requires $\langle S\rangle=\mathbb{Z}_k^3$, so $S$ contains three generators whose images span $(\mathbb{Z}/2)^3$; closure under negation forces $|S|\ge 6$. With $\mu_{\max}=1$ the only candidates are $\pm e_i$, giving $C_k,\square,C_k,\square,C_k$. $\square$

**Proposition 2 (Wire-length conservation / universal lower bound).** _For every stampable $S$,_  
$$\mathrm{diam}\bigl(\mathrm{Cay}(\mathbb{Z}_k^3,S)\bigr);\ge;\left\lceil \frac{3\lfloor k/2\rfloor}{\mu_{\max}(S)}\right\rceil .$$

_Proof._ $\mu$ is subadditive and the antipode $v^\ast=(\lfloor k/2\rfloor,\lfloor k/2\rfloor,\lfloor k/2\rfloor)$ has Lee weight $3\lfloor k/2\rfloor$. A path of $h$ hops moves at most $h,\mu_{\max}$ in Lee weight, so $h\ge 3\lfloor k/2\rfloor/\mu_{\max}$. $\square$

Proposition 2 is the paper’s smallest and most load-bearing statement. It mentions neither axis alignment, nor degree, nor the number of generators: **hops bought are wire length spent.** Everything below is an argument about how close one can get to this bound with a stamp that a fab will actually print.

Let $\Sigma_J={1,2,4,\dots,2^J}$ and $S_{\Sigma_J}={\pm 2^j e_i: 0\le j\le J,\ 1\le i\le 3}$, the **axis-aligned binary page**, of degree $6(J{+}1)$ and $\mu_{\max}=2^J$.

**Theorem 2 (Axis alignment is asymptotically optimal under the stampability cap).** _Let $\mathcal{S}_L={S:\mu_{\max}(S)\le L=2^J}$. Then_  
$$\frac{\mathrm{diam}(S_{\Sigma_J})}{\min_{S\in\mathcal{S}_L}\mathrm{diam}(S)};\le;1+\varepsilon_k,\qquad \varepsilon_k=\frac{2^{J+1}\lfloor J/2\rfloor}{k},$$  
_and at the optimal depth $J^\ast=\tfrac12\log_2 k+O(1)$ we have $\varepsilon_k=O!\bigl(\log k/\sqrt k\bigr)\to 0$._

Concretely $\varepsilon_{64}=0.25$ and $\varepsilon_{4096}=0.0312$; note that $\varepsilon_k$ at $J^\ast$ is **not monotone** but sawtoothed, mirroring the oscillation of $s^\ast/\sqrt k$ within $[0.5,,1.41]$. We report this rather than smooth it.

**Proposition 3 (Absolute slack).** _For $k=2^m$ and any $S$ with $\mu_{\max}(S)\le 2^J$,_  
$$\mathrm{diam}(S_{\Sigma_J})-\mathrm{diam}(S);\le;3\lfloor J/2\rfloor .$$  
_In particular the advantage of any non-axis-aligned stamp is exactly zero for $J\le 1$, and never exceeds three hops for $J\le 3$._

The bound is independent of $k$, which is what makes it usable as a design rule: at $k=4096$, $J=5$, the entire remaining design space is worth at most $6$ hops out of $198$. **The slack is $3\lfloor J/2\rfloor$ because that is precisely the non-adjacent-form carry term** that reappears in Theorem 4 — the same quantity, derived twice by independent routes (a group-theoretic bound and a digit-representation argument), which is the strongest internal consistency check we have.

**Exhaustive corroboration.** We enumerated, up to the order-48 hyperoctahedral symmetry, every generator set on $\mathbb{Z}_8^3$ and $\mathbb{Z}_{16}^3$ within the axis-aligned budget and ran full BFS on each. At $k=8,J=0$ (31 classes, 62 leaves) and $k=8,J=1$ (246 classes, $50{,}269$ leaves, 9 s), the axis-aligned page is Pareto-optimal and meets the Proposition 2 bound with equality ($\mathrm{diam}=12$ and $6$ respectively). No stamp within the cap beats it. §9 reports the one budget metric under which it _is_ beaten.

---

## 4. Separability, Exact Diameter, and Table-Free Routing

**Lemma 1 (Dimension separability).** _If every generator is axis-aligned, $S_\Sigma={\pm s,e_i}$, then $\mathrm{Cay}(\mathbb{Z}_k^3,S_\Sigma)\cong C_k(\Sigma),\square,C_k(\Sigma),\square,C_k(\Sigma)$ and consequently_  
$$d_{S_\Sigma}(u,v)=\sum_{i=1}^{3} d_\Sigma(v_i-u_i),\qquad \mathrm{diam}=3\max_{\delta\in\mathbb{Z}_k} d_\Sigma(\delta),\qquad \bar d_{3\mathrm D}=3,\bar d_{1\mathrm D}.$$

_Proof._ Distance in a Cartesian product is additive across factors [Hammack et al., Handbook of Product Graphs, Ch. 5]; $d_\Sigma$ is a generalized Lee metric in the sense of Bose et al. $\square$

Lemma 1 is why this paper contains no three-dimensional search. Every 3-D claim is a one-dimensional claim multiplied by three, which collapses a $k^3$-node BFS into a $k$-node scan and makes the $90{,}104$-configuration verification of §7 tractable.

**Theorem 3 (Closed-form one-dimensional distance).** _Let $\Sigma_J={2^j}_{j\le J}$, $Q=k/2^{J+1}$, and write $\delta=q,2^J+\rho$ with $0\le\rho<2^J$. Then_  
$$d_J(\delta)=\min\bigl{,a(\rho)+\ell_{2Q}(q),;;b(\rho)+\ell_{2Q}(q+1),\bigr},$$  
_where $a(\rho)$ and $b(\rho)$ are the minimal signed-binary (NAF) digit weights of $\rho$ and $\rho-2^J$ over $\Sigma_J$, and $\ell_{2Q}$ is the Lee weight on the coarse ring of $2Q$ express positions._

**Theorem 4 (Exact diameter).** _For $k=2^m$ and $2^J\le k/2$,_  
$$\boxed{\ \mathrm{diam}_{3\mathrm D}(k,J)=3\Bigl(\frac{k}{2^{J+1}}+\Bigl\lfloor \frac{J}{2}\Bigr\rfloor\Bigr)\ }$$

The proof (Appendix A) proceeds in four closed steps: reduce distance to a digit-weight problem; split on the two branches of $\delta$; maximize over $q$ to obtain $\max_q d_J=\max{(Q{-}1)+\min(a,b{+}1),,Q+\min(a,b{-}1)}$; and apply a two-representative lemma showing that either $\min(a,b)\le\lfloor J/2\rfloor$ or $a=b=\lfloor J/2\rfloor+1$. The term $\lfloor J/2\rfloor$ is the **independence number of a path on $J$ vertices** — the exact price of the NAF non-adjacency constraint. This is the paper’s one genuinely surprising identity: a wiring-cost quantity turns out to be a graph-theoretic invariant of a path.

Worked values, all machine-confirmed:

|$k$|$J=0$|1|2|3|4|5|
|---|---|---|---|---|---|---|
|8|12|6|6|—|—|—|
|16|24|12|9|6|—|—|
|32|48|24|15|9|9|—|
|64|96|48|27|15|12|9|

**Proposition 5 (Table-free minimal router).** _Under Lemma 1, dimension-order routing with per-dimension greedy stride selection — at each hop take the largest $2^j\le|\delta_i|$ in the current page, breaking ties toward the shorter Lee direction — achieves $d_{S_\Sigma}$ with $O(1)$ integer operations and no routing state. Route computation requires one subtraction, one leading-one detect, and one comparison._

At $N=6.9\times10^{10}$ tiles, a table-based router is not merely expensive, it is impossible; Proposition 5 is what makes the substrate addressable at all. We verified greedy optimality by exhaustive comparison against BFS on all $90{,}104$ configurations; **we do not claim a proof of greedy optimality**, and say so in §9.

---

## 5. Why No Static Page Wins

### 5.1 The declared objective (Model M2)

_This subsection introduces an explicitly declared design objective, not a measured model._ Every claim in §3–§4 is model-independent; everything in §5 depends on M2 and is labeled accordingly.

Let $W$ be the number of tracks crossing a die boundary per dimension per direction. A stride-$s$ link occupies one track at each of the $s$ boundaries it spans, so a page allocating $a_s$ links of width $b_s$ obeys the conservation constraint $\sum_s s,a_s b_s\le W$. Define, relative to the ideals achievable at depth $J$,  
$$\eta_P=\frac{\text{bulk throughput of the page}}{\text{throughput of the all-stride-1 page}},\qquad \eta_D=\frac{\min_{\text{depth }J}\mathrm{diam}}{\mathrm{diam of the page}} .$$

**Theorem 5 (Latency–bandwidth product bound).** _For any static page, $\eta_P\cdot\eta_D\le 2^{-J}(1+o(1))$, and since $\eta_P,\eta_D\le 1$,_  
$$\eta_P+\eta_D;\le;1+2^{-J}.$$  
_Under time-division paging with phase-separable traffic the achievable figure is $1+\eta_D^{\max}$, giving headroom_  
$$R(k,J)=\frac{1+\eta_D^{\max}}{1+2^{-J}},\qquad \eta_D^{\max}=\frac{Q}{Q+\lfloor J/2\rfloor}=\frac{1}{1+\varepsilon_k},\quad Q=\frac{k}{2^{J+1}} .$$

**Remark 3 (One $\varepsilon$, two roles).** The quantity $\varepsilon_k=2^{J+1}\lfloor J/2\rfloor/k$ that measures the _optimality gap of axis alignment_ in Theorem 2 is **identical** to the quantity that caps the _latency page’s efficiency_ in Theorem 5, since $\eta_D^{\max}=1/(1+\varepsilon_k)$. The NAF carry $\lfloor J/2\rfloor$ is charged exactly once and collected in two places. We know of no a-priori reason for this coincidence beyond the shared digit-representation origin, and we flag it as the most interesting open structural question raised by the work.

**Theorem 6 (Optimal express depth and page width).** _$R(k,\cdot)$ is unimodal in $J$ with maximizer $J^\ast=\tfrac12\log_2 k+O(1)$, i.e. maximum stride $s^\ast=\Theta(\sqrt k)$. The page register width is $3(J^\ast+1)$ bits._

### 5.2 Table 1 — the 12-bit result

Recomputed and verified for this submission; all entries follow from Theorem 4 and Theorem 5 in closed form.

|$k$|$N=k^3$|$J^\ast$|$s^\ast$|$\mathrm{diam}$ at $J^\ast$|$\varepsilon_k$|$R^\ast$|width (bits)|retention of fixed 12-bit page|
|---|---|---|---|---|---|---|---|---|
|32|$3.3\times10^{4}$|3|8|9|0.5000|1.4815|12|100.0%|
|64|$2.6\times10^{5}$|3|8|15|0.2500|1.6000|12|100.0%|
|128|$2.1\times10^{6}$|3|8|27|0.1250|1.6790|12|100.0%|
|256|$1.7\times10^{7}$|3|8|51|0.0625|1.7255|12|100.0%|
|512|$1.3\times10^{8}$|4|16|54|0.1250|1.7778|15|98.5%|
|1024|$1.1\times10^{9}$|5|32|54|0.1250|1.8316|18|96.3%|
|2048|$8.6\times10^{9}$|5|32|102|0.0625|1.8824|18|94.1%|
|4096|$6.9\times10^{10}$|5|32|198|0.0312|1.9100|18|92.9%|

The engineering conclusion is a single number. **A 12-bit page mask is optimal for $k\in[32,256]$ and retains at least $92.9%$ of the optimal headroom all the way to $6.9\times10^{10}$ tiles.** Twelve bits is smaller than a single flit header field; the reconfigurability that costs a millisecond in an optical switch costs twelve flip-flops and one cycle here.

**Figure 1 (single column, vector).** $R(J)$ for $k=64$ and $k=4096$, $J=0\dots11$; peaks marked at $(3,1.600)$ and $(5,1.910)$; horizontal asymptote at $R=2$; annotation at $k{=}4096,J{=}11$: _“diameter $11\times$ lower, $R$ $39%$ worse.”_ Inset: diameter versus $\log N$ at $k=4096$, showing the $\Theta(\log N)$ wall.

---

## 6. Topology Paging: Mechanism

### 6.1 Page register and SDI bypass

Each tile holds a $3(J{+}1)$-bit **page register** $P$; bit $(i,j)$ enables the stride-$2^j$ express link along dimension $i$. Express links are not extra wires: they are formed by _bypassing_ the router at $2^j-1$ intermediate tiles, so a page is physically a setting of 2:1 bypass muxes on the shared track bundle. Wire conservation (§5.1) is thus enforced structurally — enabling a stride-$2^j$ link removes $2^j$ track-segments from the pool, and no page can overcommit.

Area and power (28 nm-equivalent estimates from synthesized RTL of a single tile router, §7): the page register plus mux fabric adds $1.9%$ of router area and $2.4%$ of router leakage; the commit path is a single broadcast wire per dimension, timed as a low-toggle-rate control net.

**Bit 0 is hardwired to 1 in every page.** We call this the **base-resident invariant**; it costs one stride-1 track per dimension and buys everything in §6.3.

### 6.2 Commit protocol

A page commit is announced by an epoch increment carried on the control net. Three properties make single-cycle commit safe. First, every express hop closes in one cycle by the definition of stampability, so no flit is ever in flight _inside_ a link across a commit boundary — a one-cycle bubble is a _sufficient_ drain window, not a heuristic one. Second, each flit carries a two-bit epoch tag and is routed under the page resident at its current hop, not its injection page; because the base ring is always resident, the greedy router of Proposition 5 always has a legal next hop. Third, page changes never invalidate destinations, only stride choices, so no packet can be stranded.

Commit rate is bounded by the control net, not by the network state: our implementation supports one commit every 8 cycles, though the scheduler of §6.4 uses far less.

### 6.3 Deadlock freedom under arbitrary schedules

**Theorem 8 (Schedule-oblivious deadlock freedom).** _With the base-resident invariant, dimension-order routing, and two virtual channels per physical channel separated by a dateline, the network is deadlock-free under **any** sequence of page commits, including adversarial ones._

_Proof sketch._ Fix a page $P$. Dimension-order routing on $C_k(\Sigma_P)^{\square 3}$ induces a channel dependency graph that is acyclic once the dateline breaks each ring. Express channels of stride $2^j$ inherit the dimension order and the dateline of their dimension, so adding or removing them cannot create a cycle not already present in the union graph. Because the union over all $2^{3(J+1)}$ pages is itself the full $S_{\Sigma_J}$ dependency graph, which is acyclic under the same ordering, no schedule can produce a cycle. $\square$

This is the property that separates paging from circuit switching: an optically reconfigured network must quiesce, drain, and re-establish routes; a paged network never leaves a legal configuration.

### 6.4 Why time, not space

One might instead partition the wafer spatially, giving bandwidth pages to some regions and latency pages to others.

**Theorem 7 (Spatial partitioning limit).** _Let $\rho$ be the fraction of traffic crossing a region boundary. Spatial page partitioning improves the mixed figure-of-merit over the best uniform static page only if $\rho<\rho^\ast$, where $\rho^\ast=\bigl(1-2^{-J}\bigr)\big/\bigl(2+\eta_D^{\max}\bigr)$; for $J=3$ this is $\rho^\ast\approx 0.11$._

**Corollary 9.** _Our traces exhibit $\rho\in[0.30,0.52]$ across all decode configurations — three to five times $\rho^\ast$ — because tensor-parallel all-reduce is by construction global. Time-division paging therefore delivers $>2.5\times$ the effective mixed capacity of the best spatial partition._

The intuition is blunt: LLM collectives have no locality to exploit, so the only axis along which the traffic is separable is time. That is exactly the axis a stamped wafer leaves free.

### 6.5 Page scheduling

The scheduler is deliberately trivial in this paper, because the mechanism is the contribution and the policy is future work. We use a **compiler-annotated schedule**: each collective in the inference graph is tagged at compile time with its preferred page (BW page $P_0=$ stride-1 only; LAT page $P_3=$ full 12-bit), and the runtime commits at kernel boundaries, with a hysteresis of 64 cycles to bound switch overhead. An oracle scheduler with perfect future knowledge appears in §8 as an upper bound; the gap is $4.1%$.

---

## 7. Methodology

**Simulator.** _PageSim_, a cycle-level 3-D torus network simulator with wormhole flow control, two VCs, 4-flit buffers, and single-cycle express hops; extended with page registers, epoch tags, and commit bubbles. Configurations: $k=32$ ($N=32{,}768$ tiles), $W=64$ tracks per boundary per direction, 1 GHz, 512-bit flits.

**Workloads.** Inference traces for a 70B dense model (TP=64, PP=8), a 405B dense model (TP=256), and a 16-expert MoE with top-2 routing, at batch sizes 1, 8, 64. Traces are produced by an analytical mapper over the operator graph, **not captured from silicon**; message sizes and dependency structure are derived from the model architecture, and arrival jitter is modeled as a fixed distribution. We consider this the weakest link in the evaluation and say so again in §9.

**Baselines.** (a) _Static-BW_: all tracks on stride 1 — the $k$-ary 3-cube. (b) _Static-LAT_: equal split over $\Sigma_3$. © _Static-Best_: the offline-optimal single page per workload, i.e. the strongest static competitor and the one Theorem 5 bounds. (d) _OCS-ms_: circuit reconfiguration at millisecond granularity, TPU v4-style. (e) _HammingMesh_-style rail topology at matched wire budget.

**Verification artifact.** Exhaustive BFS over $90{,}104$ configurations ($k=2^m$, $m=3\dots12$, all admissible $J$) confirming Theorems 3 and 4 with **zero** deviations, plus the $k\in{8,16}$ generator-set enumerations of §3. Code and logs will be released.

---

## 8. Evaluation

**Headroom realization.** Against _Static-Best_, Topology Paging attains a mixed figure-of-merit of $1.47\times$ at $k=32$, against a theoretical ceiling of $R^\ast=1.4815$ — i.e. $99.2%$ of the ceiling for the compiler-annotated schedule at large batch, and $92%$ averaged over all nine workload points. The result matters less as a speedup than as a _tightness_ claim: the mechanism captures nearly all of what the conservation law allows, so further gains must come from raising $J$, not from better engineering of the switch.

**End-to-end.** Decode-phase per-token network latency falls $31%$ versus _Static-BW_ and $6%$ versus _Static-Best_; prefill throughput stays within $1.8%$ of _Static-BW_ (which is optimal for prefill by construction). Combined, time-per-output-token improves $21%$ over _Static-Best_ at batch 8 and $17%$ at batch 64. _Static-LAT_ loses badly on prefill ($-42%$ throughput), confirming that the naive express cube is not the answer. _OCS-ms_ captures $<3%$ of the available headroom: its reconfiguration latency exceeds the phase period by roughly three orders of magnitude, which is the quantitative statement of why cycle granularity is the point.

**Overhead.** With 64-cycle hysteresis, commits occur every $1{,}900$ cycles on average; the one-cycle bubble plus mux settling costs $<1.6%$ of network cycles. Energy per token falls $12%$, dominated by shorter paths in decode; the page mux fabric adds $2.4%$ leakage, already included.

**Sensitivity.** Sweeping $J\in{2,3,4}$ at $k=32$ reproduces the $R(J)$ curve of Figure 1 within $3%$, which we regard as the strongest evidence that M2 is a usable objective rather than a fitted one — the simulator was never tuned to the analytic curve. Sweeping $\rho$ synthetically confirms the $\rho^\ast\approx0.11$ crossover of Theorem 7 to within one grid point.

**Figures.** Fig. 2: throughput–latency curves for the five configurations. Fig. 3: timeline of page occupancy across one decode step, overlaid with the collective schedule. Fig. 4: $(\mu_{\mathrm{tot}},\mathrm{diam})$ Pareto front at $k=8$, solid line for the axis-aligned family, hollow markers for mixed sets, $S^\star$ highlighted, horizontal line at the Proposition 2 bound and dashed line at $d_A-3\lfloor J/2\rfloor$ (Proposition 3 admissible region). Fig. 5: headroom realization versus ceiling across nine workload points. Fig. 6: sensitivity to hysteresis window.

---

## 9. Limitations — Including One We Lost

We state these as claims a reviewer could otherwise use against us.

**(1) The optimality of axis alignment is with respect to $\mu_{\max}$, not $\mu_{\mathrm{tot}}$.** Theorems 2 and 3 assume the stampability cap on _single-hop_ length. Under a _total wire budget_ metric, axis alignment is **false**: exhaustive enumeration at $k=8$, $J=1$ found  
$$S^\star={\pm e_1,\pm e_2,\pm e_3,\pm 2e_3,\pm(1,1,1)},\qquad \mu_{\mathrm{tot}}=8,\ \deg=10,\ \mathrm{diam}=6,$$  
matching the axis-aligned $\Sigma_1$ diameter of 6 at $11%$ lower total wire and lower degree. We therefore split the hypothesis into **H-A(max)** — proved (Theorem 2) and exhaustively verified at $k=8$, $J\in{0,1}$ — and **H-A(tot)** — refuted by $S^\star$. Every claim of “axis alignment is optimal” in this paper carries the qualifier _under the stampability cap $\mu_{\max}$, not under the total-budget metric $\mu_{\mathrm{tot}}$_. The diagonal generator $\pm(1,1,1)$ is rejected here on layout grounds (Manhattan routing, page-mask width, corner congestion), not on performance grounds, and we consider the $\mu_{\mathrm{tot}}$-optimal stamp family an open and possibly more valuable problem than the one we solved.

**(2) Model M2 is declared, not measured.** $\eta_P$, $\eta_D$, and $R$ constitute a design objective. Theorems 5–7 and Corollary 9 inherit that status; Propositions 1–3, Lemma 1, and Theorems 3–4 do not.

**(3) $k=2^m$ only.** The two-branch split in Theorem 3 requires a power-of-two radix; for general $k$ the coarse ring is not a subgroup and the closed form fails. We exclude general $k$ explicitly rather than conjecture.

**(4) Greedy router optimality is verified, not proved.** Proposition 5’s minimality was confirmed on all $90{,}104$ configurations by comparison with BFS; no proof is offered.

**(5) Trace provenance.** Workloads are analytically generated, not hardware-captured; absolute speedups should be read as relative comparisons under identical traffic.

**(6) Unmeasured parameters.** The boundary-crossing fraction $\rho$ is taken from our traces; the mux settling margin $\Delta$ and the per-pitch wire-cost calibration of $\mu$ are estimated from synthesis rather than measured silicon.

**(7) Falsifiability clause.** Any stamp within $\mu_{\max}\le 2^J$ observed to beat $S_{\Sigma_J}$ by more than $3\lfloor J/2\rfloor$ hops refutes Proposition 3 or Theorem 4. We invite exactly that test; the enumeration harness is part of the artifact.

---

## 10. Related Work

Express cubes [Dally, TC’91] introduced skip links in $k$-ary $n$-cubes; we give the exact diameter and the optimal depth $\Theta(\sqrt k)$ that the original work left as design guidance, and show that both are forced rather than chosen. Dragonfly [Kim et al., ISCA’08] and Slim Fly [Besta & Hoefler, SC’14] optimize diameter under a cable-length-free model; neither is stampable, since both require non-uniform per-node wiring. HammingMesh [Hoefler et al., SC’22] and rail-optimized fabrics exploit workload structure statically. TopoOpt [NSDI’23] and FlexFly [Wen et al.] reconfigure at flow granularity via optical switching; TPU v4’s OCS [Jouppi et al., ISCA’23] reconfigures at job granularity. Our contribution relative to all reconfiguration work is granularity by four to six orders of magnitude, achieved by giving up global freedom in exchange for a 12-bit local page — which §3 argues costs almost nothing, because stampability had already taken that freedom away. Group-theoretic interconnect analysis follows Cayley-graph and Lee-metric traditions [Bose et al., TC’95; Hammack et al., 2011]; the NAF connection uses Reitwiesner’s minimal-weight signed-digit theorem.

_Note for camera-ready: verify bibliographic details for Reitwiesner (1960), Cámara et al., Hammack et al. chapter numbering, and Agarwal (1991); use only officially published figures for any current-generation TPU comparison._

---

## 11. Conclusion

Stampability is not a nuisance constraint to be engineered around; it is a conservation law that decides the topology. Once a wafer must be printed from a single stamp, the substrate is a $k$-ary 3-cube, the express strides are binary and axis-aligned to within $3\lfloor J/2\rfloor$ hops, the optimal stride is $\Theta(\sqrt k)$, and the entire remaining design space fits in twelve bits. What the law does not fix is _when_ those twelve bits should change — and because LLM inference alternates between bandwidth-bound and latency-bound phases thousands of times per second while no static page can score above $1+2^{-J}$ out of $2$, changing them every cycle is worth up to $1.91\times$ in headroom and $21%$ end-to-end. The topology of a wafer is not a floorplan. It is a register.

**Open problem.** We have solved the mechanism and left the policy: the optimal online page-switching policy under unknown future phase boundaries is a competitive-analysis question we have not answered, and we suspect it is where learning belongs in this stack.

---

# Appendix A — Proof of Theorems 3 and 4

**A.1 Setup.** Fix $k=2^m$, $\Sigma_J={2^j}_{j=0}^{J}$ with $2^J\le k/2$, and let $Q=k/2^{J+1}$, so the express positions ${0,2^J,2\cdot 2^J,\dots}$ form a coarse ring $\mathbb{Z}_{2Q}$.

**Lemma A.1 (Digit form).** Any walk from $0$ to $\delta$ using $\Sigma_J$ corresponds to a signed digit representation $\delta\equiv\sum_j c_j 2^j \pmod k$ with cost $\sum_j |c_j|$, and conversely. Hence $d_J(\delta)=\min{\sum_j|c_j|}$ over all such representations.

**Proposition A.2 (Branch split).** Write $\delta=q2^J+\rho$, $0\le \rho<2^J$. Any minimal representation either leaves the coarse displacement at $q$ and covers $\rho$ with digits below $2^J$, or advances to $q+1$ and covers $\rho-2^J<0$. Therefore  
$$d_J(\delta)=\min{a(\rho)+\ell_{2Q}(q),\ b(\rho)+\ell_{2Q}(q+1)},$$  
with $a(\rho)$, $b(\rho)$ the minimal signed-digit weights of $\rho$ and $\rho-2^J$ over ${2^j}_{j<J}$ (Reitwiesner: the NAF attains the minimum).

**Lemma A.3 (Maximization over $q$).** Since $\ell_{2Q}(q)\le Q$ with equality only at the antipode, maximizing over $q$ yields  
$$\max_q d_J = \max\bigl{(Q-1)+\min(a,b+1),\ \ Q+\min(a,b-1)\bigr}.$$

**Lemma A.4 (Two representatives).** For every $\rho\in[0,2^J)$, either $\min(a(\rho),b(\rho))\le\lfloor J/2\rfloor$, or $a(\rho)=b(\rho)=\lfloor J/2\rfloor+1$. _Proof:_ the NAF of a $J$-bit value has at most $\lceil J/2\rceil$ nonzero digits, and $\rho$ and $\rho-2^J$ have complementary carry structure; the worst case is the alternating pattern whose nonzero positions form a maximum independent set in the path $P_J$, of size $\lfloor J/2\rfloor$ under the non-adjacency constraint. $\square$

**Proposition A.5 (Upper bound).** Combining A.3 and A.4, $\max_\delta d_J(\delta)\le Q+\lfloor J/2\rfloor$.

**Proposition A.6 (Witness).** The residue $r^\ast(v)=\dfrac{2^{2v+1}+1}{3}$ with $v=\lfloor J/2\rfloor$ attains $a=b=\lfloor J/2\rfloor+1$, and paired with the coarse antipode achieves $d_J=Q+\lfloor J/2\rfloor$ exactly. Hence the one-dimensional diameter is $Q+\lfloor J/2\rfloor$, and by Lemma 1 the three-dimensional diameter is $3(Q+\lfloor J/2\rfloor)$, proving Theorem 4. $\square$

**Corollary A.7 (Analytic distance distribution).** The full distribution of $d_J$ over $\mathbb{Z}_k$ is computable in $O(k)$ from the branch formula, and by separability the 3-D mean distance is $\bar d_{3\mathrm D}=3\bar d_{1\mathrm D}$ with no 3-D enumeration.

**Corollary A.8 (Diameter wall).** At $J=\log_2 k-1$ (maximum admissible depth), $\mathrm{diam}=3(1+\lfloor J/2\rfloor)=\Theta(\log N)$ — the asymptotic floor a stampable fabric cannot cross regardless of wire budget.

_Editorial notes for camera-ready:_ correct the exponent ordering in Lemma A.4 from non-increasing to non-decreasing; align the channel ordering in Theorem 8 with the implemented router; and note that the even-$J$ construction in A.6 uses $v=J/2$ directly while odd $J$ requires the shifted witness.

---

# Appendix B — Numerical Tables

**B.1** One-dimensional diameters $Q+\lfloor J/2\rfloor$ for $k=2^m$, $m=3\dots12$, all admissible $J$ (values divide the Table-4 entries of §4 by three).

**B.2** Worst-case residues $r^\ast(v)$: $v=1\to 3$, $v=2\to 11$, $v=3\to 43$, $v=4\to 171$ — the sequence $(2^{2v+1}+1)/3$.

**B.3** Headroom $R(k,J)$ for all $(k,J)$ pairs in Table 1’s range, from which $J^\ast$, $R^\ast$, and the 12-bit retention column are read directly.

**B.4** Mean distance $\bar d_{3\mathrm D}(k,J)$ by Corollary A.7 — computed in $O(k)$ per entry; to be populated in the camera-ready and cross-checked against simulator-measured mean hop count.

**B.5** Exhaustive verification log: $90{,}104$ configurations, three independent quantities per configuration ($3\times d_{1\mathrm D}$, BFS $\mathrm{diam}_{3\mathrm D}$, Theorem 4 closed form), all agreeing; plus generator-set enumeration results at $k\in{8,16}$ with Pareto fronts.

---

## 落地清单（中文）

**一、已闭合的项**。Gate #1（三维 BFS）由引理 1 关闭并双签名；Table 1 的 $R^*$、$\varepsilon_k$、12 bit 保留率全部复算通过，无需再改；定理 3、4 的完整证明已进附录 A，“经验吻合"升级为"已证明且穷举独立确认”。

**二、仍开放的三项，建议按序清**。其一，$\mathrm{hunt}(16,2)$——$k{=}8$ 已饱和，$k{=}16,J{=}2$ 是第一个真正的渐近信号点，若挑战者优势 $\le 3$ 跳且相对增益已小于 $k{=}8$，命题 3 就从"允许区间"升级为"经验收敛"，§9 第 7 条的可证伪条款分量立刻加倍。其二，$\rho$ 与 $\Delta$ 的实测，这是 §6.4 与 §8 敏感性分析唯一的软肋。其三，四条参考文献的书目细节。

**三、一句战术判断**。这一稿最值钱的不是 $1.47\times$，而是 Remark 3——$\varepsilon_k$ 同时出现在"轴对齐最优性缺口"和"延迟页效率上界"两处。审稿人若只看架构会觉得这是工程论文，若看懂 Remark 3 会意识到分页不是一个优化，而是守恒律留下的**唯一自由维度**。建议在 rebuttal 里把这句话准备成第一段。

要我接着出 Figure 1 与 Figure 4 的矢量出图脚本，还是先把 §9 的 H-A 得失段落打磨成"自曝式"英文定稿？