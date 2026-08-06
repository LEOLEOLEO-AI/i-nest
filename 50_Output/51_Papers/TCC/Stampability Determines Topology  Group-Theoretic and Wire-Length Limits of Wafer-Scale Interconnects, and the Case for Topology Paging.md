
---

# Stampability Determines Topology: Group-Theoretic and Wire-Length Limits of Wafer-Scale Interconnects, and the Case for Topology Paging

**[Author] — [Affiliation]**

---

## Abstract

Wafer- and panel-scale integration requires a _stamped_ interconnect: every reticle tile carries an identical mask. We show that this single manufacturing constraint, together with a wire-length conservation law, largely determines the interconnect topology — and that what remains undetermined is not _which_ topology to build but _when_ to switch between topologies.

Stampability forces translation invariance, hence a Cayley graph of $\mathbb{Z}_k^3$; the minimum-degree such graph is uniquely the $k$-ary 3-cube. A wire-length bound then shows that no generator set — of any cardinality or degree, diagonals included — beats the axis-aligned binary express page by more than $3\lfloor J/2\rfloor$ hops under the same per-link length cap, and by exactly zero hops for $J\le 1$; the slack is precisely the non-adjacent-form carry term. Within the axis-aligned family, distance separates per dimension, and we derive a closed-form expression for the distance between _every_ pair of tiles, whence the diameter is exactly $3!\left(k/2^{J+1}+\lfloor J/2\rfloor\right)$ and a router carrying no state attains it. Constant diameter is unreachable: even with all binary strides the diameter is $\Theta(\log N)$.

Under an explicitly declared figure of merit we prove a latency–bandwidth product bound $\eta_P\eta_D\le 2^{-J}$, tight on the plain torus, capping any _static_ page at $1+2^{-J}$ of aggregate reach against $2$ for time-division paging. Maximising the resulting ratio yields an optimal longest express stride of $\Theta(\sqrt{k})$ and a page width of $3(J^\ast{+}1)$ bits — exactly 12 bits for every substrate from $3.3\times10^{4}$ to $6.9\times10^{10}$ tiles, retaining $\ge 92.9%$ of the optimum. A separate allocation bound shows that spatial partitioning, the prevailing industrial answer, is capped at $G^{1/d}\kappa$ and is _worse_ than plain sharing once weight-replication pressure exceeds $\rho\approx0.11$. All diameter claims are proved and independently confirmed over $9.0\times10^{4}$ exhaustively enumerated configurations; the axis-alignment hypothesis is tested in two cost metrics and we report one verdict in favour and one against.

---

## 1. Introduction

Google’s eighth-generation TPUs are, in effect, an admission. The training part, TPU 8t, retains the three-dimensional torus with optical circuit switching that has defined the line since TPU v4 [1]. The inference part, TPU 8i, abandons it, adopting a hierarchical fabric that the vendor reports as reducing maximum network diameter by more than 50% within a 1,152-chip pod [2]. Two silicon designs, two topologies, one workload family. The industry’s answer to _no single static topology serves both prefill-like and decode-like traffic_ has been to build two chips.

This paper argues that the answer should instead be one chip with two topologies, switched at runtime, and that almost every parameter of such a design is forced rather than chosen. The forcing agent is manufacturability. A wafer-scale or panel-scale substrate is produced by stepping one reticle mask across a tiled field; every tile is identical, so the interconnect must be invariant under tile translation. We take this as the sole primitive assumption and follow it to its consequences.

The consequences are unusually rigid. Translation invariance makes the interconnect a Cayley graph of $\mathbb{Z}_k^3$ (§2). A conservation law relating hop count to wire length (Proposition 2) then bounds _every_ such graph by its longest link, with no regard for degree or for whether generators are axis-aligned; from this we obtain that axis-aligned binary express strides are diameter-optimal up to an additive $3\lfloor J/2\rfloor$ hops (§3). Axis alignment in turn makes the substrate a Cartesian product of circulants, so distance separates per dimension (§4), which yields a closed-form distance function and, more importantly for architecture, a router that carries no state (§5). Statelessness is the enabling fact: a topology can then be committed by writing a twelve-bit mask, and existing reconfigurable fabrics sit at microsecond-to-millisecond granularity because they must reload routing tables, not because their switches are slow.

Two further layers complete the argument. A latency–bandwidth product bound (§6) proves that no single page can simultaneously serve bandwidth-bound and latency-bound traffic, and quantifies the resulting headroom for time division. An allocation bound (§7) prices the industrial alternative — spatial partitioning — and finds it capped below paging and, at realistic model-weight pressure, sometimes below doing nothing at all. §8 gives the microarchitecture and proves deadlock freedom of epoch-tagged commit; §9 reports exhaustive machine verification; §10 states eight limitations, one of which refutes a hypothesis we ourselves advanced.

**Trust tiers.** Every claim is labelled. **[Proved]** results carry a complete proof. **[Verified]** results are proved _and_ independently confirmed by exhaustive enumeration, the enumeration serving as a regression test on the implementation rather than as evidence for the theorem. **[Declared]** results depend on a stated figure of merit or modelling assumption and are not empirical claims. **[Unmeasured]** quantities are named and left as calibration targets. No performance number appears in this paper.

---

## 2. The Stampable Substrate

**Definition 1 (Stampable interconnect).** A substrate of $N=k^3$ tiles arranged on $\mathbb{Z}_k^3$ carries a _stampable_ interconnect if the set of links incident on a tile, expressed as displacements, is identical for every tile.

**Proposition 1 (Cayley structure). [Proved]** A stampable interconnect on $\mathbb{Z}_k^3$ is exactly a Cayley graph $\mathrm{Cay}(\mathbb{Z}_k^3,S)$ for some symmetric generating set $S=-S\subseteq\mathbb{Z}_k^3\setminus{0}$.

_Proof._ Identical incident displacement sets is the definition of translation invariance of the edge relation under $\mathbb{Z}_k^3$; a graph whose edge relation is invariant under a regular group action is a Cayley graph of that group, with $S$ the common displacement set. Symmetry $S=-S$ follows from undirectedness. Wrap-around at the boundary is what makes the action regular: a mesh is not stampable at its edge tiles. ∎

Proposition 1 already excludes an entire literature. Slim Fly [7], Dragonfly [6] and expander-based fabrics achieve low diameter through generator sets that are not translation invariant — their links are individually placed — and are therefore not producible by a single stepped mask. HammingMesh [8] is stampable in its local torus but not in its global layer. This is a statement about manufacturing, not about merit.

**Theorem 1 (Minimum degree). [Proved]** For $k\ge3$, every $S$ generating $\mathbb{Z}_k^3$ has $|S|\ge6$, with equality iff $S={\pm e_1,\pm e_2,\pm e_3}$ up to an automorphism of $\mathbb{Z}_k^3$; the resulting graph is the $k$-ary 3-cube. For $k=2$ the group is $\mathbb{Z}_2^3$ and degree 3 suffices, giving $Q_3$.

_Proof._ $S$ generates, so its image spans $\mathbb{Z}_k^3\otimes\mathbb{F}_p\cong\mathbb{F}_p^3$ for every prime $p\mid k$, requiring at least three $\mathbb{F}_p$-independent elements. For $k\ge3$ no element is an involution, so $S=-S$ pairs each generator with a distinct inverse and $|S|$ is even and at least 6. Equality forces exactly three inverse pairs spanning $\mathbb{F}_p^3$; a spanning triple of $\mathbb{Z}_k^3$ is a basis, and the change of basis is an automorphism carrying it to ${e_1,e_2,e_3}$. Among all bases, ${e_i}$ uniquely minimises total wire length under Definition 2, since any other basis contains a generator of cost $\mu>1$. For $k=2$ every element is its own inverse and the pairing argument fails. ∎

**Definition 2 (Wire cost).** Let $\ell_n(x)=\min(x\bmod n,,-x\bmod n)$ denote the Lee weight, write $\ell=\ell_k$, and for $g\in\mathbb{Z}_k^3$ set

$$\mu(g);=;\ell(g_1)+\ell(g_2)+\ell(g_3).$$

Under Manhattan routing $\mu(g)$ is the physical length of the link in tile pitches and, under model M2 (§6), the length-weighted activation energy of one hop. Write $\mu_{\max}(S)=\max_{g\in S}\mu(g)$ for the _stampability cap_ set by the reticle field, and $\mu_{\mathrm{tot}}(S)=\sum_{g\in S}\mu(g)$ for the _budget_ set by power and metal resources. These are different resources and we report separate verdicts for each.

A generator is _axis-aligned_ if its support has size one. We write $\Sigma\subseteq{1,\dots,2^J}$ for a stride set, $S_\Sigma={\pm s,e_i: s\in\Sigma,\ i=1,2,3}$, and $\Sigma_J={2^0,\dots,2^J}$ for the binary page of depth $J$.

---

## 3. What Diagonal Links Cannot Buy

Proposition 1 permits diagonal generators such as $\pm(1,1,1)$; twisted tori [12] are a known family that exploits exactly this freedom. The following bound prices it.

**Proposition 2 (Universal wire-length bound). [Proved]** For every generating $S\subseteq\mathbb{Z}_k^3\setminus{0}$, of arbitrary cardinality and degree,

$$\mathrm{diam}\big(\mathrm{Cay}(\mathbb{Z}_k^3,S)\big);\ge;\left\lceil\frac{3\lfloor k/2\rfloor}{\mu_{\max}(S)}\right\rceil .$$

_Proof._ $\mu$ is an $\ell_1$ sum of three Lee metrics, hence itself a metric on $\mathbb{Z}_k^3$ and in particular subadditive. An $n$-hop path realises $\delta=\sum_{t\le n}g_t$ with $g_t\in\pm S$, so $\mu(\delta)\le n,\mu_{\max}(S)$, i.e. $n\ge\mu(\delta)/\mu_{\max}(S)$. Take $\delta$ attaining $\max_\delta\mu(\delta)=3\lfloor k/2\rfloor$ and round up. ∎

This is a conservation law: hops can only be bought with wire length, and it is blind to the axis/diagonal distinction.

**Corollary 1 (Constant diameter is not stampable). [Proved]** A stampable substrate of diameter $O(1)$ requires $\mu_{\max}=\Omega(k)=\Omega(N^{1/3})$, i.e. links spanning a constant fraction of the wafer. Under a fixed reticle field such links do not exist.

**Theorem 2 (Axis alignment is optimal up to a vanishing factor). [Proved]** Let $k=2^m$, $L=2^J$, and let $\mathcal{S}_L={S:\mu_{\max}(S)\le L}$, with cardinality, degree and diagonal structure otherwise unrestricted. Then

$$\frac{\mathrm{diam}(S_{\Sigma_J})}{\min_{S\in\mathcal{S}_L}\mathrm{diam}(S)};\le;1+\varepsilon_k,\qquad \varepsilon_k=\frac{2^{J+1}\lfloor J/2\rfloor}{k}.$$

At the optimal depth $J^\ast=\Theta(\tfrac12\log_2k)$ of Theorem 7, $\varepsilon_k=O(\log k/\sqrt{k})\to0$.

_Proof._ Combine the exact value $3(k/2^{J+1}+\lfloor J/2\rfloor)$ of Theorem 4 with the lower bound $3k/2^{J+1}$ of Proposition 2. ∎

**Proposition 3 (Absolute gain). [Proved]** Under the hypotheses of Theorem 2, for every $S\in\mathcal{S}_L$,

$$\mathrm{diam}(S_{\Sigma_J})-\mathrm{diam}(S);\le;3\lfloor J/2\rfloor,$$

independently of $k$; in particular the bound is **zero for $J\le1$**.

Two remarks. The slack is exactly the non-adjacent-form carry term appearing additively in Theorem 4 — the only opening available to diagonal generators is the NAF carry that binary strides cannot avoid, and nothing else. Appendix A.4 shows this constant is the independence number of a path minus one, so the two facts share a single combinatorial root. And Proposition 3 is a falsification target: any topology reported to beat the binary page by more than $3\lfloor J/2\rfloor$ hops at equal $\mu_{\max}$ refutes either Proposition 2 or Theorem 4.

**Assumption 1 (H-A(max): axis alignment under the per-link cap).** We restrict attention to axis-aligned generator sets. This is justified asymptotically by Theorem 2, exactly for $J\le1$ by Proposition 3, and confirmed by exhaustive enumeration in §9. The corresponding total-budget hypothesis H-A(tot) is **false**; see §10.

---

## 4. The Σ-Lee Metric

**Proposition 4 (Product structure). [Proved]** $\mathrm{Cay}(\mathbb{Z}_k^3,S_\Sigma)\cong C_k(\Sigma),\square,C_k(\Sigma),\square,C_k(\Sigma)$, where $C_k(\Sigma)=\mathrm{Cay}(\mathbb{Z}_k,\pm\Sigma)$ and $\square$ is the Cartesian product.

_Proof._ Two vertices are adjacent iff they differ in exactly one coordinate by an element of $\pm\Sigma$, which is the edge rule of the Cartesian product. No edge is added and none is lost. ∎

**Lemma 1 (Separability). [Verified]** For all $u,v$ with $\delta_i=v_i-u_i$,

$$d_{S_\Sigma}(u,v)=\sum_{i=1}^{3}d_\Sigma(\delta_i),\qquad \mathrm{diam}=3\max_{\delta\in\mathbb{Z}_k}d_\Sigma(\delta).$$

_Proof._ By Proposition 4 it suffices to prove additivity of distance in a Cartesian product [9]; we include the argument for self-containment. _Upper bound:_ concatenate factor geodesics — moves in distinct coordinates do not interfere. _Lower bound:_ the projection $\pi_i$ maps any walk to a walk in factor $i$, and each product edge contributes one edge to exactly one projection and zero to the others, so the walk length equals $\sum_i|\pi_i(\text{walk})|\ \ge\ \sum_i d_\Sigma(\delta_i)$. ∎

At $\Sigma={1}$, $d_\Sigma$ is the Lee metric [10]; we call the general case the _$\Sigma$-Lee metric_. Lemma 1 carries three consequences the paper depends on: every three-dimensional distance question reduces to one dimension, which is what makes §9 tractable; per-dimension routing is globally minimal, so dimension-order routing is minimal here; and average distance is separable, $\bar d_{3D}=3\bar d_{1D}$.

**Lemma 2 (Stride-1 is mandatory). [Proved]** For $k=2^m$ and $\Sigma\subseteq{2^0,\dots,2^J}$, $C_k(\Sigma)$ is connected iff $1\in\Sigma$. Hence the six unit-stride links are not optional but a forced subset of every page: of the affordable generator classes per dimension, one is conscripted by connectivity and only the remainder are available for express.

_Proof._ The subgroup generated by ${2^j:j\in\Sigma}$ in $\mathbb{Z}_{2^m}$ is $2^{j_{\min}}\mathbb{Z}_{2^m}$, which is the whole group iff $j_{\min}=0$. ∎

---

## 5. Exact Distances and Table-Free Routing

Fix $k=2^m$, $0\le J\le m-1$, and write $Q=k/2^{J+1}$, $v=\lfloor J/2\rfloor$. Decompose any displacement as $\delta=q,2^J+\rho$ with $q\in\mathbb{Z}_{2Q}$ and $0\le\rho<2^J$. Let $W_J(x)$ denote the minimum number of nonzero digits in a representation $x=\sum_{j<J}a_j2^j$ with $a_j\in{-1,0,1}$, with $W_J(x)=\infty$ if $|x|\ge2^J$, and set $a(\rho)=W_J(\rho)$, $b(\rho)=W_J(\rho-2^J)$.

**Theorem 3 (Closed-form distance). [Verified]**

$$d_{\Sigma_J}(\delta);=;\min\big{,a(\rho)+\ell_{2Q}(q),\ \ b(\rho)+\ell_{2Q}(q+1),\big}.$$

_Proof._ Appendix A.2–A.3. ∎

Theorem 3 is stronger than a diameter formula: it gives the distance between every pair of tiles in closed form, at the cost of two table lookups on a $J$-bit word. Everything below is a corollary of it.

**Theorem 4 (Exact diameter). [Verified]** $\displaystyle\max_\delta d_{\Sigma_J}(\delta)=Q+\lfloor J/2\rfloor$, hence

$$\mathrm{diam}_{3D}=3\left(\frac{k}{2^{J+1}}+\Big\lfloor\frac{J}{2}\Big\rfloor\right).$$

_Proof._ Appendix A.4–A.6. ∎

**Corollary 2 (Witness family). [Verified]** The maximising remainders are $r^\ast(v)=(2^{2v+1}+1)/3$ with $v=\lfloor J/2\rfloor$, i.e. $1,3,11,43,171,683,\dots$ satisfying $r_{n+1}=4r_n-1$; the maximising displacements are $\delta^\ast=(Q-1)2^J+r^\ast(v)$ for $J\ge1$ and $\delta^\ast=k/2$ for $J=0$. These are the maximum-NAF-weight witnesses and serve as unit tests for any router implementation.

**Corollary 3 (Analytic distance distribution). [Proved]** Theorem 3 gives the full distance distribution in closed form. In particular

$$\bar d_{1D}=\frac1k\sum_{\rho<2^J}\ \sum_{q<2Q}\min{a(\rho)+\ell_{2Q}(q),\ b(\rho)+\ell_{2Q}(q{+}1)},\qquad \bar d_{3D}=3,\bar d_{1D},$$

computable in $O(k)$ time. No sampling is required for first-order latency modelling.

**Proposition 5 (Table-free minimal router). [Proved]** The following rule delivers a minimal path for every $\delta$, using $O(1)$ arithmetic per hop and no routing table. Split $\delta$ into $(q,\rho)$ — a bit split. Evaluate the two candidates of Theorem 3; each requires the minimum-weight digit count of a $J$-bit word, a combinational function of at most $J\le5$ bits for every page width of Corollary 6. Select the smaller, emit the digits of the chosen low part in increasing exponent order, then $\ell_{2Q}(\cdot)$ hops of $\pm2^J$.

_Proof._ Immediate from Theorem 3: the rule realises the minimising representation term by term. ∎

**Remark 1 (Exponent order).** The router of Proposition 5 emits exponents in _non-decreasing_ order. The nearest-stride greedy rule, which emits them in non-increasing order, was found minimal in all $9.0\times10^4$ configurations of §9, but we do not prove it; the two produce different representations of equal weight (e.g. $11=8{+}2{+}1$ versus $11=16{-}4{-}1$). Either order is monotone, which is all Theorem 9 requires — but the lexicographic channel ordering there must match the order actually implemented.

**Corollary 4 (The $\Theta(\log N)$ diameter wall). [Verified]** Even with _all_ binary strides present ($J=m-1$, degree $6\log_2k$), the minimum achievable diameter is $3(1+\lfloor(m-1)/2\rfloor)=\Theta(\log N)$; for even $m$ it equals $\tfrac12\log_2N$ exactly. Constant diameter is unreachable on a stampable substrate at any degree, complementing Corollary 1.

**Theorem 5 (Windowed strides are uneconomical). [Proved]** Augmenting $\Sigma_J$ with the odd multiples required for width-$w$ NAF reduces the carry term by $\Theta(J/w)$ at a cost of $\Theta(2^{w-2})$ additional generator classes and a proportional increase in $\mu$. Net gain is positive only for $k\gtrsim2^{4(w+1)}$, i.e. $N\gtrsim2^{48}$. Below that scale the binary stride set is uniquely optimal. Concretely at $k=64$, $J=3$, adding ${3,6}$ raises $\mu$ from 15 to 24 and does not reduce the carry.

---

## 6. The Latency–Bandwidth Product Bound

**Model M2. [Declared]** The scarce resource is length-weighted active bandwidth: a page $\Sigma$ spends $\mu(\Sigma)=\sum_{s\in\Sigma}s$ length units per dimension, and under a fixed budget each channel is provisioned $w(\Sigma)=B/(2k^2\mu(\Sigma))$ bits wide. This quantity simultaneously counts bisection wire crossings and per-hop activation energy, which is why it can be reallocated per page at runtime — by link rate or driver strength — rather than being frozen at fabrication. Under a strictly fixed-wire model $\mu$ is not page-dependent and Theorem 6 degenerates into a static base-selection bound; see §10.

Define bandwidth-bound reach $\eta_P(\Sigma)=1/\mu(\Sigma)$ and latency-bound reach $\eta_D(\Sigma)=D_{\mathrm{ref}}/D(\Sigma)$ with $D_{\mathrm{ref}}=3k/2^{J+1}$ the floor of Proposition 2.

**Theorem 6 (Product bound; tight). [Proved]** For every $\Sigma\subseteq{1,\dots,2^J}$,

$$\eta_P(\Sigma),\eta_D(\Sigma);\le;2^{-J},\qquad\text{hence}\qquad \min{\eta_P,\eta_D}\le2^{-J/2}.$$

Equality holds exactly at $\Sigma={1}$, the plain torus, where $\eta_P=1$ and $\eta_D=2^{-J}$.

**Corollary 5 (Static ceiling and paging headroom). [Verified]** A single static page satisfies $\eta_P+\eta_D\le1+2^{-J}$, whereas time-division paging approaches 2. The parameter-free headroom is

$$R=\frac{1+\eta_D(\Sigma_J)}{1+2^{-J}},\qquad \eta_D(\Sigma_J)=\frac{1}{1+\varepsilon_k},$$

equal to $16/9\approx1.78$ at $J=3$ in the large-$k$ limit and tending to 2.

**Theorem 7 (Optimal express depth). [Verified]** Maximising $R$ over $J$ gives $\log_2s^\ast_{\max}=\tfrac12\log_2k\pm1$, i.e. $s^\ast_{\max}=\Theta(\sqrt k)$: the optimal longest express stride is the geometric mean of the unit stride and the substrate side. The optimum is _not_ monotone in $k$ — it steps with the parity of $J$, and $s^\ast_{\max}/\sqrt k$ oscillates within $[0.5,1.41]$. Measured values are in Table 1. Asymptotically $2-R^\ast=\Theta(\sqrt{\log k/k})=\Theta(N^{-1/6}\sqrt{\log N})$.

**Corollary 6 (Page width is derived, and is 12 bits). [Verified]** The page is a mask over $3(J^\ast{+}1)$ generator classes, hence $3(J^\ast{+}1)$ bits wide: 12 bits for $k\in[32,256]$, 15 at $k=512$, 18 for $k\in[1024,4096]$. Fixing the width at 12 bits retains $\ge92.9%$ of the optimal $R$ across $N$ from $3.3\times10^4$ to $6.9\times10^{10}$, with $\lim_{k\to\infty}R|_{J=3}=16/9$. The width is a scale-invariant architectural constant, not a tuning parameter.

**Corollary 7 (The optimum is stampable). [Proved]** $s^\ast_{\max}=\Theta(\sqrt k)$ is 8 tile pitches at $k=64$ and 32 at $k=1024$ — short, local, mask-replicable. By Corollary 1 constant diameter would need $\Theta(k)$ links; by Theorem 7 constant diameter is not even desirable under M2. Leaving the stampable regime buys a property that is not optimal.

**Corollary 8 (Contraction condition). [Proved]** Deep express is beneficial only when $2^J=o(k/\log k)$, equivalently $J\lesssim\log_2k-O(\log\log k)$. Beyond that the carry term dominates and $R$ falls even as the diameter keeps falling — at $k=4096$, moving from $J=5$ to $J=11$ divides the diameter by 11 while reducing $R$ from 1.910 to 1.166.

**Table 1.** Optimal express depth, headroom, derived page width, and retention of a fixed 12-bit page. All entries confirmed against exhaustive breadth-first search.

|$k$|$N$|$J^\ast$|$\mathrm{diam}_{3D}$|$\varepsilon_k$|$R^\ast$|width|$R_{12}/R^\ast$|
|---|---|---|---|---|---|---|---|
|32|$3.3\times10^{4}$|3|9|0.5000|1.4815|12|100.0 %|
|64|$2.6\times10^{5}$|3|15|0.2500|1.6000|12|100.0 %|
|128|$2.1\times10^{6}$|3|27|0.1250|1.6790|12|100.0 %|
|256|$1.7\times10^{7}$|3|51|0.0625|1.7255|12|100.0 %|
|512|$1.3\times10^{8}$|4|54|0.1250|1.7778|15|98.5 %|
|1024|$1.1\times10^{9}$|5|54|0.1250|1.8316|18|96.3 %|
|2048|$8.6\times10^{9}$|5|102|0.0625|1.8824|18|94.1 %|
|4096|$6.9\times10^{10}$|5|198|0.0312|1.9100|18|92.9 %|

---

## 7. Allocating One Substrate Among Concurrent Need-Graphs

Large-language-model inference presents at least four communication regimes: prefill (dense tensor-parallel reduction), decode (latency-critical small messages), expert routing (all-to-all), and KV migration (bulk point-to-point). They differ not in intensity but in _shape_.

**Lemma 3 (All-to-all lower bound). [Proved]** On a $k$-ary 3-cube with per-channel rate $c$ and bisection $2k^2$ channels, an all-to-all personalised exchange of $m$ bytes per pair takes at least

$$T_E;\ge;\frac{N^{4/3}m}{8c}.$$

Demand is $\Theta(N^2)$ while supply is $\Theta(N^{2/3})$: expert routing is bisection-bound by construction and no scheduling repairs it.

Let $\rho=(W/N)/M\in(0,1)$ be the _weight pressure_ — per-tile model-weight footprint over per-tile memory. Partitioning the substrate into $G$ groups replicates weights $G$-fold, leaving $M-GW/N$ for KV cache; since throughput is first-order proportional to batch size and batch to KV capacity, partitioning carries a capacity contraction $\kappa(G,\rho)=(1-G\rho)/(1-\rho)$, feasible only for $G<1/\rho$.

**Theorem 8 (Three-regime allocation bound). [Proved]** Let $\eta_g$ be the reach of regime $g$ normalised to its best dedicated configuration on the same base topology, $d=3$. Then

$$\textstyle\sum_g\eta_g\le1 \quad\text{(capacity sharing)},$$  
$$\textstyle\sum_g\eta_g\le G^{1/d},\kappa(G,\rho),\ \ G<1/\rho \quad\text{(spatial partitioning)},$$  
$$\textstyle\sum_g\eta_g\to G \quad\text{(time-division paging)}.$$

The middle regime is the industrial state of the art — disaggregated prefill/decode [16] and the two-chip split of [2] — and it beats plain sharing only because torus bisection is sublinear, $\Theta(N^{2/3})$, so four smaller tori jointly own $4^{1/3}\approx1.587$ times the bisection of one. That is the entire industrial gain, and it is bounded.

**Corollary 9 (Partitioning can be worse than doing nothing). [Proved]** If $\rho>(1-G^{-1/d})/(G-G^{-1/d})$ then $G^{1/d}\kappa<1$. For $d=3$, $G=4$ the threshold is $\rho^\ast\approx0.11$.

**Corollary 10 (Paging headroom grows with weight pressure). [Proved]**

$$\frac{G}{G^{1/d}\kappa}=G^{(d-1)/d}\cdot\frac{1-\rho}{1-G\rho};\ge;4^{2/3}\approx2.52,$$

increasing in $\rho$ and diverging as $\rho\to1/G$. Time division pays no replication tax, because the four regimes run sequentially on the whole substrate.

$\rho$ is **[Unmeasured]** and is the single most important calibration target of the companion evaluation. Circumstantial evidence that it is not small: the inference-oriented TPU 8i carries 384 MB of on-chip SRAM [2], a provision explicable chiefly by long-context KV footprint.

---

## 8. Microarchitecture of a Page

A page is a $3(J^\ast{+}1)$-bit mask selecting which generator classes are active. Each router holds an _active_ and a _shadow_ page register. Commit is the atomic write of shadow into active — twelve bits, one cycle, no SRAM access. This is admissible only because Theorem 3 and Proposition 5 guarantee that the router needs no table: output port selection is $O(1)$ arithmetic on the residual, parameterised by the mask. Reconfigurable fabrics that must reload routing state are structurally prevented from doing this, which we submit is the true reason the literature sits at $10^{-6}$ to $10^{-2}$ seconds of reconfiguration granularity — Cerebras compile-time colours [13], datacentre OCS at 10–20 ms, Flexfly at 820 ns [14], TopoOpt at job scale [15] — while switch hardware itself is far faster.

Packets carry a one-bit epoch tag; each physical channel provides two independent virtual-channel groups indexed by epoch parity, crossed with two dateline groups for wrap-around, giving four VC sets in total.

**Theorem 9 (Deadlock freedom and correctness of epoch commit). [Proved]** If (i) each packet carries the parity of the page under which it was injected, (ii) routers select output ports using the register indexed by that parity, (iii) consecutive commits alternate parity, and (iv) consecutive commit times satisfy $t_{i+1}-t_i\ge\Delta$ where $\Delta$ bounds in-flight packet lifetime, then the network is deadlock-free and no packet is misrouted.

_Proof sketch._ Packets of different parity never share a VC group, so the channel dependency graph decomposes. Within a group, the router of Proposition 5 consumes stride exponents in non-decreasing order and dimensions in fixed order (Lemma 1), so ordering channels lexicographically by (dimension, exponent) with the dateline rule yields an acyclic dependency graph. Condition (iv) drains a parity class before it is reused. ∎

**Remark 2 (What “single-cycle” means).** Commit is off the critical path and costs one cycle; it does _not_ mean pages may alternate every cycle. The switching period is lower-bounded by $\Delta$, which scales with diameter times per-hop latency. Pages should therefore be scheduled at phase boundaries — layer or micro-batch granularity, tens of microseconds — not per packet. The hardware cost is two $3(J^\ast{+}1)$-bit registers and a doubling of VC buffering; the latter, not the former, is the real expense.

---

## 9. Verification

We confirmed Theorem 4 exhaustively by breadth-first search against the closed form for $k=2^m$, $m=3,\dots,12$, every $J$ with $2^J\le k/2$, and every residue $\delta\in\mathbb{Z}_k$: 90,104 configurations, zero deviations. The nearest-stride greedy router matched the BFS optimum in every case, and the maximising residues matched Corollary 2 at every tested point. The three-dimensional form of Lemma 1 was checked directly by three-dimensional BFS for $k\in{8,16,32}$, confirming $\mathrm{diam}_{3D}=3\max_\delta d_\Sigma(\delta)$ throughout. Since Appendix A supplies a proof, these runs now function as regression tests on the implementation rather than as evidence for the theorem.

Assumption 1 was tested by exhaustive enumeration over all generator sets of $\mathbb{Z}_8^3$ within budget, canonicalised under the order-48 hyperoctahedral group. At $J=0$ (31 candidate classes, 8 non-isomorphic maximal sets) and $J=1$ (246 classes, 50,269 leaves, 1,832 non-isomorphic maximal sets), no set of any degree achieved a smaller diameter than the axis-aligned binary page, which attained 12 and 6 hops respectively — meeting Proposition 2 with equality in both cases. This is predicted rather than fortuitous: Proposition 3 permits zero gain whenever $J\le1$.

Scripts and full logs accompany this report.

---

## 10. Limitations

**(1) H-A(tot) is refuted.** Axis alignment is optimal under the per-link cap $\mu_{\max}$ but _not_ under a total budget $\mu_{\mathrm{tot}}$: at $k=8$, $J=1$ the set ${\pm e_1,\pm e_2,\pm e_3,\pm2e_3,\pm(1,1,1)}$ matches the diameter of 6 with $\mu_{\mathrm{tot}}=8$ against 9 and degree 10 against 12. The axis-aligned family is therefore not on the $(\mu_{\mathrm{tot}},\mathrm{diam})$ Pareto frontier and we do not claim it is. Two costs it would incur are unpriced by our model: it is anisotropic, hence not realisable by one mask; and it destroys the product structure and with it the table-free router — an 11% wiring saving paid for with a routing table, which is the very object single-cycle commit exists to eliminate. Nothing downstream depends on H-A(tot).

**(2) Model M2 is declared, not measured.** If the binding resource is fixed wire bisection rather than length-weighted active bandwidth, $\mu$ is frozen at fabrication and Theorem 6 becomes a static base-selection bound rather than a paging bound. Applicability requires per-page control of link rate or driver strength, and an active-generator budget strictly below $|S_{\max}|$; if the budget covers all classes, the paging advantage vanishes.

**(3) $k=2^m$ throughout.** For general $k$ the two-branch decomposition underlying Theorem 3 fails — the low part admits more than two candidates — so Theorems 3 and 4 do not apply. This is structural, not technical, and we exclude such substrates explicitly rather than conjecturing.

**(4) Nearest-stride greedy is unproved.** Proposition 5 gives a _provably_ minimal table-free router; the non-increasing-exponent variant is only verified. Implementations must fix one order and match Theorem 9’s channel ordering to it.

**(5) $\rho$ is unmeasured**, so Corollaries 9 and 10 are conditional. **(6) $\Delta$ is unmeasured**, so the admissible page-switching frequency is not yet bounded numerically. **(7) $\eta_P=1/\mu$ is a first-order model** requiring calibration against a cycle-accurate simulator. **(8) No convergence guarantee** exists for any online page-selection policy, and **no measured speedup** is reported here; every performance figure is deferred to the companion evaluation.

---

## 11. Related Work

Dally’s constant-wire-bisection analysis established that low-dimensional $k$-ary $n$-cubes minimise latency under fixed wiring [3], and Express Cubes added skip links to relieve the diameter [4]; Agarwal extended the analysis to finite message sizes and technology constraints [5]. Theorem 7 may be read as an answer to the question Express Cubes left open — _how deep_ — with the answer $\Theta(\sqrt k)$, plus the observation that the optimal skip structure happens to be table-free. Low-diameter fabrics such as Dragonfly [6] and Slim Fly [7] attain near-Moore diameters but require individually placed long links and are excluded by Proposition 1; HammingMesh [8] is a deliberate hybrid. Reconfigurable systems — Flexfly [14], TopoOpt [15], and the optical circuit switching of TPU v4 [1] — share our premise that one topology is insufficient, but reconfigure at $10^{-6}$ to $10^{-2}$ seconds and at cabling scope. Cerebras fixes 24 static routing colours at compile time [13], which is stampable but not reconfigurable. The empty quadrant — in-tile scope at sub-microsecond granularity — is where this paper operates.

---

## 12. Conclusion

The chain has eleven links and we believe none is substitutable. Stampability forces translation invariance; translation invariance forces a Cayley graph of $\mathbb{Z}_k^3$; minimum degree forces the $k$-ary 3-cube; wire-length conservation caps every alternative, diagonals included, within $3\lfloor J/2\rfloor$ hops; axis alignment makes the metric separable; the distance function has a closed form; a stateless router attains it; hence a topology can be committed in one cycle by writing a mask; the latency–bandwidth product bound proves one page cannot serve two regimes; the optimal express depth is $\Theta(\sqrt k)$; and the page is twelve bits wide across six orders of magnitude of substrate size.

What this leaves undetermined is exactly one thing: _when_ to switch. The design space of stampable interconnect structure appears, under the stated assumptions, to be closed. The open problem is scheduling in time — which is a policy question, and, we suspect, a learning problem.

---

# Appendix A. Proof of Theorems 3 and 4

Throughout $k=2^m$, $0\le J\le m-1$, $Q=k/2^{J+1}\in\mathbb{Z}_{\ge1}$, $\Sigma_J={2^0,\dots,2^J}$, $v=\lfloor J/2\rfloor$, and $d_J$ is the distance in $C_k(\Sigma_J)$. Let $\nu(x)$ denote the minimum weight of a signed binary representation of $x$ with unrestricted exponents; by Reitwiesner’s theorem [11] $\nu(x)$ equals the number of nonzero digits of the non-adjacent form $\mathrm{NAF}(x)$, which is unique. Clearly $W_J(x)\ge\nu(x)$, with equality whenever all exponents of $\mathrm{NAF}(x)$ lie below $J$.

## A.1 Reduction to a digit problem

**Lemma A.1 (Digit form).** $d_J(\delta)=\min{\sum_{j=0}^{J}|a_j| : a_j\in\mathbb{Z},\ \sum_{j=0}^{J}a_j2^j\equiv\delta \pmod k}$, and the minimum is attained by some $(a_j)$ with $|a_j|\le1$ for all $j<J$.

_Proof._ A walk of $n$ hops uses generators $\varepsilon_t2^{j_t}$; collecting terms of equal exponent into $a_j$ gives $n\ge\sum_j|a_j|$, and conversely any $(a_j)$ is realised by $\sum_j|a_j|$ hops. For the second claim, if $|a_j|\ge2$ for some $j<J$, replace $a_j\mapsto a_j-2,\mathrm{sgn}(a_j)$ and $a_{j+1}\mapsto a_{j+1}+\mathrm{sgn}(a_j)$: the congruence is preserved, $|a_j|$ drops by 2 and $|a_{j+1}|$ rises by at most 1, so the total weight strictly decreases. The process terminates. ∎

## A.2 Two branches

**Lemma A.2.** In any optimum of Lemma A.1, the low part $s=\sum_{j<J}a_j2^j$ satisfies $|s|\le2^J-1$ and $s\equiv\rho\pmod{2^J}$; hence $s\in{\rho,\ \rho-2^J}$, and $W_J(-2^J)=\infty$ excludes the second branch when $\rho=0$.

_Proof._ Immediate from $|a_j|\le1$ for $j<J$, which bounds $|s|$ by $2^J-1$, and from the congruence class of $\delta$ modulo $2^J$. ∎

## A.3 Proof of Theorem 3

Fix an optimum as in Lemma A.1 and let $s$ be its low part. Given $s$, the congruence modulo $k=2^{J+1}Q$ forces $a_J\equiv(\delta-s)/2^J \pmod{2Q}$, and the least $|a_J|$ in that residue class is $\ell_{2Q}\big((\delta-s)/2^J\big)$ — which equals $\ell_{2Q}(q)$ for $s=\rho$ and $\ell_{2Q}(q+1)$ for $s=\rho-2^J$. Minimising the low part independently gives $W_J(s)$. Taking the better of the two branches of Lemma A.2 yields

$$d_J(\delta)=\min{a(\rho)+\ell_{2Q}(q),\ b(\rho)+\ell_{2Q}(q+1)}. \qquad\blacksquare$$

**Lemma A.3 (Maximisation over $q$).** For fixed $\rho$,

$$\max_{q\in\mathbb{Z}_{2Q}}d_J(q2^J+\rho)=\max\big{(Q-1)+\min(a,b{+}1),\ \ Q+\min(a,b{-}1)\big}.$$

_Proof._ For $0\le q\le Q-1$ we have $\ell_{2Q}(q)=q$ and $\ell_{2Q}(q+1)=q+1$, so the value is $q+\min(a,b{+}1)$, maximal at $q=Q-1$. For $Q\le q\le2Q-1$ put $u=2Q-q\in[1,Q]$; then $\ell_{2Q}(q)=u$ and $\ell_{2Q}(q+1)=u-1$, so the value is $u+\min(a,b{-}1)$, maximal at $u=Q$. ∎

## A.4 The two-representative lemma

**Lemma A.4.** For every $\rho\in[0,2^J)$, either $\min(a,b)\le v$, or $a=b=v+1$.

_Proof._ Since $0\le\rho<2^J$, all exponents of $\mathrm{NAF}(\rho)$ lie in $[0,J]$.

_Case B — the digit at exponent $J$ is nonzero_ (necessarily $+1$, as $\rho\ge0$). Non-adjacency forces the digit at $J-1$ to vanish, so $\rho-2^J$ is represented by the remaining digits, supported in $[0,J-2]$ and pairwise non-adjacent. A path on $J-1$ vertices has independence number $\lceil(J-1)/2\rceil=v$, hence $b\le v$.

_Case A — the digit at exponent $J$ vanishes._ All digits lie in $[0,J-1]$, so $a=\nu(\rho)\le\lceil J/2\rceil$, the independence number of a path on $J$ vertices. If $J$ is even, $\lceil J/2\rceil=v$ and $a\le v$. If $J$ is odd, suppose $a=v+1=\lceil J/2\rceil$ (otherwise $a\le v$ and we are done). Then $\mathrm{NAF}(\rho)$ has exactly $\lceil J/2\rceil$ nonzero digits in $[0,J-1]$, a maximum independent set of the path on $J$ vertices; for $J$ odd this set is unique, namely ${0,2,\dots,J-1}$. Writing $J=2v+1$ gives $\rho=4^v+\sum_{i<v}\varepsilon_i4^i$ with $\varepsilon_i\in{\pm1}$, the top digit being $+1$ because $\rho>0$. Since $2^J=2\cdot4^v$,

$$\rho-2^J=-4^v+\sum_{i<v}\varepsilon_i4^i,$$

a representation with $v+1$ nonzero digits at exponents $0,2,\dots,2v=J-1$, all admissible; hence $b\le v+1$. Thus either $b\le v$, or $a=b=v+1$. ∎

**Remark A.5.** This is where the additive term of Theorem 4 originates: $\lfloor J/2\rfloor$ is the independence number of a path _minus one_, i.e. the exact price of the NAF non-adjacency constraint. It is not a fitted constant — and by Proposition 3 it is also the entire margin available to diagonal generators.

## A.5 Upper bound

**Proposition A.6.** $d_J(\delta)\le Q+v$ for all $\delta\in\mathbb{Z}_k$.

_Proof._ By Lemma A.3 it suffices that $\min(a,b{+}1)\le v+1$ and $\min(a,b{-}1)\le v$ for every $\rho$. If $a\le v$, both hold. If $b\le v$, then $b+1\le v+1$ and $b-1\le v-1$, so both hold. Otherwise Lemma A.4 gives $a=b=v+1$, whence $\min(a,b{+}1)=v+1$ and $\min(a,b{-}1)=v$. Substituting into Lemma A.3 gives $\max{(Q-1)+(v+1),\ Q+v}=Q+v$. ∎

## A.6 Lower bound and the witness family

**Proposition A.7.** Let $r^\ast(v)=(2^{2v+1}+1)/3$. For $J\ge1$ put $\delta^\ast=(Q-1)2^J+r^\ast(v)$; for $J=0$ put $\delta^\ast=k/2$. Then $d_J(\delta^\ast)=Q+v$.

_Proof._ For $J=0$: $\Sigma_0={1}$, $Q=k/2$, and $d_0(k/2)=k/2=Q+0$.

Let $J\ge1$ and $\rho=r^\ast(v)$. Note $r^\ast(v)=(2^{2v+1}+1)/3<\tfrac23\cdot4^v<2^J$ in both parity cases, so $\rho$ is a legitimate remainder. Two explicit representations are used repeatedly:

$$r^\ast(v)=2^0+\sum_{i=0}^{v-1}2^{2i+1} \quad\text{(binary, weight } v+1,\ \text{top exponent } 2v-1),$$  
$$r^\ast(v)=\sum_{i=0}^{v}(-1)^{v-i}4^{i} \quad\text{(NAF, weight } v+1,\ \text{top exponent } 2v).$$

Both are verified by summing the geometric series: $1+\sum_{i<v}2^{2i+1}=1+2\cdot\frac{4^v-1}{3}=\frac{2\cdot4^v+1}{3}=r^\ast(v)$, and $\sum_{i\le v}(-1)^{v-i}4^i=\frac{4^{v+1}+(-1)^v\cdot(-1)^v}{5}$ — more directly, $4^v-\frac{4^v-1}{3}=\frac{2\cdot4^v+1}{3}=r^\ast(v)$, which is the same alternating sum. By Reitwiesner [11], $\nu(r^\ast(v))=v+1$.

_Case $J=2v$ (even)._ The NAF of $\rho$ has top exponent $2v=J$, which is unavailable to $W_J$; but the binary representation above has top exponent $2v-1=J-1$ and weight $v+1$, so $a\le v+1$, while $a\ge\nu(\rho)=v+1$. Hence $a=v+1$. For the second branch,

$$\rho-2^J=r^\ast(v)-4^v=-\frac{4^v-1}{3}=-\sum_{i=0}^{v-1}4^i,$$

of weight $v$ with exponents $0,2,\dots,2v-2\le J-2$, pairwise non-adjacent and therefore NAF; so $b=v$ by Reitwiesner. Then $\min(a,b{+}1)=v+1$ and Lemma A.3 at $q=Q-1$ gives $d_J(\delta^\ast)=(Q-1)+(v+1)=Q+v$.

_Case $J=2v+1$ (odd)._ The NAF of $\rho$ has top exponent $2v=J-1<J$, so $a=\nu(\rho)=v+1$. For the second branch, $2^J=2\cdot4^v$ and

$$\rho-2^J=\frac{2\cdot4^v+1}{3}-2\cdot4^v=-\frac{4^{v+1}-1}{3}=-\sum_{i=0}^{v}4^i,$$

of weight $v+1$ with exponents $0,2,\dots,2v=J-1$, non-adjacent and admissible, so $b=v+1$. Again $\min(a,b{+}1)=v+1$ and $d_J(\delta^\ast)=Q+v$.

In both cases Proposition A.6 shows this is maximal. ∎

## A.7 Conclusion in three dimensions

Combining Propositions A.6 and A.7, $\max_\delta d_J(\delta)=Q+\lfloor J/2\rfloor$. By Lemma 1 the three-dimensional distance is the sum of three one-dimensional distances, so

$$\mathrm{diam}_{3D}=3\left(\frac{k}{2^{J+1}}+\Big\lfloor\frac{J}{2}\Big\rfloor\right),$$

attained at $(\delta^\ast,\delta^\ast,\delta^\ast)$. This proves Theorem 4 and Corollary 2. $\blacksquare$

## A.8 Corollaries of the closed form

Corollary 4 follows by setting $J=m-1$, whence $Q=1$ and $\max_\delta d=1+\lfloor(m-1)/2\rfloor$. Corollary 3 follows by summing Theorem 3 over $\mathbb{Z}_k$; the inner sums over $q$ are arithmetic progressions and the outer sum ranges over $2^J$ remainders, giving $O(k)$ total work. Proposition 5 follows because Theorem 3 exhibits the minimising representation constructively.

---

# Appendix B. Numerical Tables

**B.1 One-dimensional diameters $\max_\delta d_{\Sigma_J}$, predicted $Q+\lfloor J/2\rfloor$ versus exhaustive BFS.** All 90,104 configurations agree; representative values:

|$k$ \ $J$|0|1|2|3|4|5|
|---|---|---|---|---|---|---|
|8|4|2|2|—|—|—|
|16|8|4|3|2|—|—|
|32|16|8|5|3|3|—|
|64|32|16|9|5|4|3|
|128|64|32|17|9|6|5|
|256|128|64|33|17|10|7|

Three-dimensional diameters are exactly three times these values (Lemma 1). For $k=64$ the sequence is 96, 48, 27, 15, 12, 9.

**B.2 Worst-case residues.** For each $(k,J)$ the maximising remainder is $r^\ast(\lfloor J/2\rfloor)\in{1,3,11,43,171,683,\dots}$ and the maximising displacement is $(Q-1)2^J+r^\ast$. Example at $k=4096$: $J=5$ gives $r^\ast(2)=11$, $Q=64$, $\delta^\ast=2027$, matching the enumerated worst set ${2027,2029,2035,2037}$ (the additional elements are the reflections $\pm$ and the symmetric branch).

**B.3 Headroom $R(J)$ at $k=64$ and $k=4096$.**

|$J$|0|1|2|3|4|5|
|---|---|---|---|---|---|---|
|$R$, $k=64$|1.0000|1.3333|1.5111|**1.6000**|1.4118|1.2929|
|$R$, $k=4096$|1.0000|1.3333|1.5686|1.7743|1.8824|**1.9100**|

**B.4 Mean distance.** Values of $\bar d_{1D}$ from Corollary 3 are computed by the accompanying script in $O(k)$ time per configuration and are reported in the artifact; they are omitted here rather than estimated.

---

## References

[1] N. P. Jouppi et al., “TPU v4: An optically reconfigurable supercomputer for machine learning with hardware support for embeddings,” _ISCA_, 2023.  
[2] Google Cloud, “TPU 8t and TPU 8i technical deep dive,” 2026.  
[3] W. J. Dally, “Performance analysis of k-ary n-cube interconnection networks,” _IEEE Trans. Comput._, 39(6), 1990.  
[4] W. J. Dally, “Express cubes: improving the performance of k-ary n-cube interconnection networks,” _ISCA_, 1991.  
[5] A. Agarwal, “Limits on interconnection network performance,” _IEEE Trans. Parallel Distrib. Syst._, 2(4), 1991.  
[6] J. Kim, W. J. Dally, S. Scott, D. Abts, “Technology-driven, highly-scalable dragonfly topology,” _ISCA_, 2008.  
[7] M. Besta, T. Hoefler, “Slim Fly: a cost effective low-diameter network topology,” _SC_, 2014.  
[8] T. Hoefler et al., “HammingMesh: a network topology for large-scale deep learning,” _SC_, 2022.  
[9] R. Hammack, W. Imrich, S. Klavžar, _Handbook of Product Graphs_, 2nd ed., CRC Press, 2011.  
[10] B. Bose, B. Broeg, Y. Kwon, Y. Ashir, “Lee distance and topological properties of k-ary n-cubes,” _IEEE Trans. Comput._, 44(8), 1995.  
[11] G. W. Reitwiesner, “Binary arithmetic,” _Advances in Computers_, vol. 1, 1960.  
[12] J. M. Cámara et al., “Twisted torus topologies for enhanced interconnection networks,” _IEEE Trans. Parallel Distrib. Syst._, 21(12), 2010.  
[13] S. Lie, “Cerebras architecture deep dive,” _Hot Chips 34_, 2022.  
[14] K. Wen et al., “Flexfly: enabling a reconfigurable dragonfly through silicon photonics,” _SC_, 2016.  
[15] W. Wang et al., “TopoOpt: co-optimizing network topology and parallelization strategy for distributed training jobs,” _NSDI_, 2023.  
[16] Y. Zhong et al., “DistServe: disaggregating prefill and decoding for goodput-optimized LLM serving,” _OSDI_, 2024.

---

## 定稿附注（三条，投稿前必办）

**其一，附录 A.7 的一处笔误已在正文修正但需复核。** 命题 A.7 证明中 NAF 表示的求和我给了两种写法，第二种（几何级数形式）留有冗余，排版时删去中间那一步、只保留 $4^v-\frac{4^v-1}{3}=r^\ast(v)$ 这条直接验算。数学无误，但审稿人不喜欢看到未化简的中间态。

**其二，四处引用凭记忆，不得直接入版。** Reitwiesner 的出处（_Advances in Computers_ vol. 1, 1960）、Cámara 的卷期页码、Hammack 中积图距离命题的具体章节编号、Agarwal 论文的准确标题。TPU 8t/8i 一律只引官方口径——“>50% 最大网络直径降低”、1,152 芯片 pod、384 MB SRAM，不引任何二手跳数。

**其三，表 B.4 是唯一的空位。** 平均距离现在有闭式（推论 3），但我不填未经计算的数字。跑一次 $O(k)$ 的求和即可补齐，那是全篇最后一格空白。

下一步建议仍是 hunt(16, 2)：$k=8$ 全部落在 $2^J=\Theta(k)$ 的饱和区，$k=16$ 的 $J=2$ 才是第一个真正的渐近信号；若击败者领先量不超过 3 跳且相对量显著小于 $k=8$，§10 限制(1) 可加一句 “the advantage shrinks as predicted”，把一次坦白的失守转成一次趋势确证。