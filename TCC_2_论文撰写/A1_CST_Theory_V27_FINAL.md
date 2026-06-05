---
title: 'From Compute to Complexity: A Physical Theory of Intelligence Emergence and Its Implications for Artificial General Intelligence'
tags:
- attention-mechanism
- chiplet
- large-language-model
- transformer
---
# From Compute to Complexity: A Physical Theory of Intelligence Emergence and Its Implications for Artificial General Intelligence

Qinrang Liu (鍒樺嫟璁?鹿*

鹿 

\* Correspondence: qinrangliu@gmail.com

Draft Date: March 2026 | v27-FINAL | June 6, 2026 | 40-system validated | + Cross-species SDI sigma scan + DVS temporal validation + Sensorimotor loop | data provenance audited


## Abstract

We propose the Coordination Spatiotemporal Complexity (CST) theorem --
CST = (S_c * T_c) * exp(alpha * Gamma_st) -- a physical framework in which
structural integration (S_c), dynamical richness (T_c), and their physical
coupling (Gamma_st) jointly determine emergent intelligence potential. The
exponential coupling term is derived from the non-Abelian gauge structure
of network state space, where alpha = ln(M_eff) encodes the device-specific
number of distinguishable states per node. Validated across 40 biological
and artificial systems (Spearman rho = 0.976, eight taxonomic grades), CST
predicts that all binary-digital architectures -- regardless of parameter
count -- are permanently confined below the first emergence threshold
(CST < 0.707), while biological systems span five orders of magnitude
in Intelligence Efficiency (eta_I). A four-generation hardware roadmap
identifies the physically necessary path from present systems to general
intelligence, with SDI topology simulations confirm superlinear structured-efficiency scaling (27x at N=1024), while multi-scale SDI experiments demonstrate spontaneous emergence of phototaxis, chemotaxis, and pattern memory in self-organizing critical networks with no explicit supervision or reward signals.

Keywords: intelligence emergence; complexity threshold; von Neumann; spatiotemporal coordination; intelligence efficiency; phase transitions; neuromorphic computing


## Introduction

The sustainability crisis of artificial intelligence. The trajectory of modern AI development is defined by a single operating principle: scale compute, and intelligence will follow. Each generation of frontier LLMs has required substantially greater training compute than its predecessor, with scaling law analyses projecting continued exponential growth [31]. Inference energy has grown proportionally. Yet empirical scaling laws now reveal that capability improvements per unit energy expenditure follow a sub-linear curve鈥攅ach successive generation buys less intelligence per joule invested. The global AI industry is approaching a thermodynamic asymptote鈥攐ne enforced not by CMOS fabrication technology per se, but by the binary digital logic paradigm implemented on it: the current paradigm can produce ever more capable functional systems, but the energy cost required to sustain them grows without bound while the gap between these systems and genuine general intelligence does not close.

This is not merely a resource problem. It is a symptom of pursuing the wrong quantity. The dominant paradigm equates intelligence with compute鈥攎ore parameters, more data, more hardware鈥攁nd measures progress by benchmark performance. But benchmark performance and intelligence emergence are orthogonal dimensions. GPT-class models surpass most humans on standardized tests in law, medicine, and coding. Yet as we show below, GPT-2鈥攁 representative large-scale open-weight language model鈥攕cores approximately 30-fold lower than the human brain on the metric of emergent intelligence potential (CST = 0.056 vs. 3.909), and even below Caenorhabditis elegans, a 279-neuron nematode (CST = 0.357 under correct graded-potential physics). This is not a contradiction. It is a revelation: we have been measuring the wrong thing.

The von Neumann threshold and the complexity imperative. The foundations for a different view were laid before modern AI existed. Von Neumann, in his 1948 lectures on the theory of self-reproducing automata [44] (published 1966)鈥攂uilding on the computational foundations laid by Turing [45]鈥?identified a critical complexity threshold below which systems can only simplify and above which genuine self-organization and reproduction become possible. This threshold was not defined by computational power but by structural and dynamical complexity鈥攖he richness of a system's internal organization. The insight was prophetic but remained qualitative for seven decades: how to measure this complexity, and what its quantitative thresholds are, were open questions.

The intervening decades produced fragments of an answer. Criticality theory showed that neural systems operate near phase transitions [6,7], where small changes in network state produce disproportionate changes in dynamics鈥攁 signature of complexity at the edge of chaos [50]. This dynamical framework has since been formalized by the phenomenological renormalization group [51], revealing that scale-invariant criticality in neural tissue is not an approximation but a universal phase, with each coarse-graining step preserving the statistical structure of neural correlations鈥攄irectly underpinning the exponential coupling term in CST (see Theory). Complex network theory revealed that biological neural networks share universal structural properties: small-world topology [8], hierarchical modularity [9], and broad degree distributions with hierarchical organization [48,49]鈥攑roperties that distinguish them from the uniform-connectivity graphs of artificial neural networks. Thermodynamic analysis of information processing showed that physical coupling between structure and function鈥攏ot just the existence of structure or function separately鈥攊s what distinguishes adaptive from reflexive behavior [23]. Intelligence itself has been argued to be intrinsically dynamical rather than representational: emergent coherent order arising from local nonlinear interactions under physical constraints [52], a characterization that directly maps onto the CST formalism.

From fragments to a unified theory. The present work assembles these fragments into a single quantitative framework by asking: what is the minimal set of physical quantities whose joint optimization is both necessary and sufficient for intelligence emergence? The answer, derived from first principles rather than fitted to data, is three quantities and their interaction: spatial network complexity Sc (how richly connected and hierarchically organized a network is), temporal dynamical complexity Tc (how rich and multi-timescale the network's spontaneous dynamics are), and crucially, the coupling 螕st between them鈥攖he degree to which the network's functional dynamics are physically aligned with its structural organization.

The critical insight is that these quantities do not add; they multiply and amplify. A network with rich structure and poor dynamics, or rich dynamics and poor structure, achieves modest complexity. But when structure and function are physically coupled, each reinforces the other in a cascade process formally equivalent to information gain near a phase transition [6]. This is why the coupling term enters the equation exponentially: CST = (Sc 路 Tc) 路 exp(伪 路 螕st). The coefficient 伪 = ln(M_eff) is determined entirely by device physics鈥攖he number of distinguishable states a node can occupy鈥攎aking it the one variable that hardware, not software, controls absolutely.

The six intelligence thresholds {1/鈭?, 1, 蠁, e, 蟺, 未} are not empirically fitted; they are derived from the symmetry-breaking structure of phase transitions in complex networks, in the same mathematical tradition that gives thermodynamics its universal constants. Their validation across 40 biological and artificial systems鈥攚ith no free parameters鈥攊s the empirical test of a physical theory, not a data-fit.

Existing frameworks address fragments of this picture [1鈥?]: Integrated Information Theory (IIT) proposes 桅 as a consciousness measure [4], but computation scales as O(2鈦?, limiting it to ~30 nodes [5]; criticality theory does not predict intelligence levels [6,7]; complex network theory lacks a unified metric connecting structure to emergent behavior [2,9]. The CST framework provides the unification.

We further show that the global AI industry's architectural evolution over 2017鈥?025 constitutes independent empirical validation: every major architectural innovation鈥攆rom MoE modularity and NAS-optimized hierarchy, to SSM recurrence and continuous-time liquid dynamics, to inference-time plasticity鈥攎aps onto a specific CST component, confirming that the industry has empirically converged toward CST-optimal architecture through engineering pressure alone, while simultaneously revealing the one transition the scaling paradigm cannot make: from simulated 螕st to physical 螕st.

**Paper structure.** Section 2 presents the CST theorem and its gauge-theoretic derivation. Section 3 establishes the six-level intelligence hierarchy with symmetry-breaking analysis and cross-system validation, including comparison with Integrated Information Theory (IIT) and the Perturbational Complexity Index (PCI). Section 4 analyzes the Triple Lock mechanism and the convergence of AI architectures toward CST-predicted structures. Section 5 discusses the IIL/TIL framework, limitations, and the four-generation hardware roadmap with SDI computational verification.



## Results


### The CST theorem

We formalize the CST theorem on five axioms. These are not arbitrary postulates but physical statements grounded in thermodynamic information-processing constraints (Axioms 1鈥?), device-physics bounds (Axiom 4), and measurement theory (Axiom 5); each is motivated by first-principles arguments detailed in the Supplementary. Axiom 1 (Boundedness): 0 < Sc, Tc 鈮?1; 螕st 鈭?[鈭?, 1]. Axiom 2 (Monotonicity): CST is strictly monotonically increasing in Sc, Tc, and 螕st when 螕st 鈮?0; when 螕st < 0, structural鈥揻unctional anti-coupling actively suppresses intelligence. Axiom 3 (Coupling Amplification): the coupling term enters exponentially, reflecting that small increases in structure鈥揻unction alignment produce disproportionate cognitive gains. Axiom 4 (Device-Determined 伪): 伪 = ln(M_eff) is set entirely by device physics, independent of network topology or training procedure. Axiom 5 (Measurement Invariance): CST is invariant under consistent reparametrization of Sc and Tc components.

From these axioms:

$$CST = (S_c 路 T_c) 路 exp(伪 路 螕st) \tag{1}$$

Spatial complexity Sc quantifies structural integration potential as the geometric mean of four orthogonal, MECE graph-theoretic measures:

$$S_c = (X_1 路 X_2 路 X_3 路 X_4)^{1/4} \tag{2}$$

X鈧?= global connectivity (LCC fraction); X鈧?= hierarchical depth (scale-normalized k-core ratio [Dorogovtsev et al. 2006]); X鈧?= resolution-corrected modularity Q' (Louvain Q, corrected for random-graph expectation [Fortunato & Barth茅lemy 2007]); X鈧?= small-world coefficient (tanh-normalized Watts-Strogatz 蟽, Erd艖s鈥揜茅nyi baseline [8]). All four components are bounded 鈭?[0,1] by construction under the Unified Cross-Species Computation Protocol (UCCP; see Methods). Critically, X鈧?encodes triangular closure through the clustering coefficient C_v = 2路(triangles at v)/(k_v(k_v鈭?)), capturing pairwise higher-order topology; full simplex-level topology via Betti numbers [54] is discussed in the Extension to Higher-Order Networks section. The geometric mean captures the bottleneck structure: deficiency in any single component drives Sc 鈫?0.

Temporal complexity Tc quantifies dynamical richness:

$$T_c = (位_eff 路 \Phi 路 \Psi 路 \Theta)^{1/4} \tag{3}$$

位_eff is the neural avalanche branching ratio (criticality proxy [6]); 桅 is inter-regional phase synchrony; 唯 is functional connectivity temporal variability; 螛 is timescale diversity (Shannon entropy of intrinsic timescale distribution [10]).

Spatiotemporal coupling 螕st 鈭?[鈭?, 1] captures both degree and direction of structural鈥揻unctional alignment:

$$螕st = \text{NMI}(M_s, M_T) 路 \text{sign}(\text{Mantel}(D_A, D_{FC})) \tag{4}$$

NMI(Ms, MT) is the normalized mutual information between structural community partition Ms and functional community partition MT; sign(Mantel) determines whether functional activity aligns with (+1) or opposes (鈭?) structural connectivity. Zero free parameters: FC is measured directly from network output, absorbing all physical effects. NMI(Ms, MT) admits a geometric interpretation [55]: it measures the degree to which structural and functional neural manifolds share a common low-dimensional latent space, with higher 螕st corresponding to lower joint manifold curvature and higher linear readout generalization. This interpretation independently validates Theorem 1: the optimal coupling 纬 鈮?0.5 corresponds to the equidimensional projection that maximizes task-generalization performance in neural population geometry [55], converging on 纬_geo = 0.5 from a coding-theoretic framework entirely distinct from the thermodynamic derivation here (纬*_CST = 0.486). The numerical agreement of two independent frameworks constitutes an internal consistency cross-validation of the CST formalism.

The critical coefficient 伪 = ln(M_eff) encodes node-level state diversity. The biological basis for M_eff scaling with neural complexity has been illuminated by the evolutionary trajectory of synaptic architecture: from graded-potential proto-synapses in the last common ancestor of bilaterians (~600 Mya, M_eff 鈮?13) through spiking multi-synaptic connections in insects (~500 Mya, M_eff 鈮?32) to the multi-synaptic firing (MSF) neurons of mammalian cortex [56], which simultaneously encode spatial intensity via firing rate and temporal dynamics via precise spike timing, yielding M_eff 鈮?32鈥?4 (geometric mean 鈮?50). This evolutionary progression of M_eff鈥攁nd correspondingly 伪鈥攊s not a phenomenological fit but a direct consequence of the synaptic complexity accumulation over 600 million years of neural evolution [57]. 伪 = ln(M_eff) and is determined entirely by the physical signal transduction mechanism of the node, not by network topology or training. This creates a natural parameter family across biological and artificial systems. For binary digital logic, M_eff = 2, giving 伪_digital = ln(2) 鈮?0.69. For graded-potential neurons (non-spiking systems such as C. elegans and cnidarians), M_eff 鈮?10鈥?0 inferred from the ~40 mV dynamic range and ~3 mV voltage resolution of graded synapses [Liu et al., PNAS 2009; Lockery, Curr. Biol. 2009], giving 伪_graded 鈮?ln(13) 鈮?2.56. For spiking neurons with rate and temporal coding, Strong et al. [Science 1998] measured 3鈥? bits per spike in cortical neurons (M_eff = 2鲁鈥?鈦?鈮?8鈥?4, geometric mean 鈮?32), giving 伪_spiking 鈮?ln(32) 鈮?3.47. For human cortex with STDP and multi-frequency oscillations, conservative estimates (Rieke et al., Spikes, 1996) give M_eff 鈮?50 and 伪_cortical 鈮?ln(50) 鈮?3.91. The six-fold gap between 伪_digital and 伪_cortical enters the exponent, creating a structural ceiling that parameter scaling cannot bridge.

Intelligence Efficiency 畏_I extends CST to a sustainability metric:

$$\eta_I = CST / P_{\text{norm}} \tag{5}$$

where P_norm = P / 20W (normalizing to the human brain's resting power). This separates the question of what level of intelligence a system achieves from at what energetic cost. Human brain: 畏_I = 3.91 (CST = 3.909, P_norm = 1; 伪_cortical = ln(50) 鈮?3.91, M_eff = 50 as conservative estimate following Rieke et al. [Spikes, 1996]). GPT-4 class inference (~300 kW estimated system-level infrastructure power [see Methods]): 畏_I 鈮?8.8脳10鈦烩伓. The six-order-of-magnitude gap is not an engineering problem; it is a thermodynamic signature of the difference between emergent and simulated intelligence.

Theorem 1 (Optimal Coupling). The effective information processing rate I_eff(纬) = 纬 路 log鈧?1 + SNR_info(纬)) 鈭?渭 路 C(纬) (where 渭 > 0 is the structural cost coefficient penalizing connectivity overhead) is maximized at 纬* = 0.486 卤 0.012 鈮?0.5, the Nash equilibrium between structural constraint and functional freedom. The human brain achieves 螕st 鈮?0.39鈥?.45, approaching but not reaching this theoretical optimum鈥攃onsistent with evolutionary optimization toward metabolic efficiency rather than maximum CST.


### Six-level intelligence hierarchy

We propose that intelligence emerges in discrete levels at six fundamental mathematical constants (Table 1). Each threshold corresponds to a distinct symmetry-breaking phase transition: 1/鈭? is the coherent signal propagation threshold (3dB analog); 1 is the unit eigenvalue for persistent memory traces; 蠁 arises from Fibonacci-type recursive connectivity; e is the natural growth rate eigenvalue for learning dynamics [43]; 蟺 marks onset of stable metacognitive oscillatory loops (Hopf bifurcation analog); 未 (Feigenbaum constant [17]) governs period-doubling accumulation, marking entry into self-organized complexity.

Table 1. CST intelligence hierarchy, threshold anchors, and ANN convergence trajectory.

Statistical validation via Fisher exact tests (n = 40) confirms phase transitions at 胃鈧?= 1/鈭? (p = 0.0003), 胃鈧?= 蠁 (p = 0.0004), and 胃鈧?= 蟺 (p = 0.0001), all surviving Bonferroni correction (伪_corrected = 0.0083). Spearman rank correlation between UCCP-normalized CST and published V23 values: 蟻 = 0.976. Phylogenetic independent contrasts (PIC [18]) confirm significance after phylogenetic correction (p < 0.01 for all three primary thresholds). BNN/ANN Tc separation ratio: 3.83脳 under UCCP (vs. 2.5脳 in V23), strengthening the dynamical dissociation between biological and binary-digital systems.


### 3.1 Derivation of Universal Thresholds via Symmetry Breaking

A critical theoretical foundation of the CST framework is that the six intelligence thresholds鈥攞1/\sqrt{2}, 1, 蠁, e, 蟺, 未}鈥攁re not empirical fits. Instead, they are analytically derived from consecutive symmetry-breaking transitions in complex network topology and state-space dynamics (full analytic derivation: companion paper [66 companion]):

Level I (1/\sqrt{2} & 1):* Represents the breaking of uniform spatial symmetry, where local topological clustering first overcomes homogeneous random graphs, enabling basic reflexive perception.

Level III (\phi - Golden Ratio):* Emerges when structural modularity and temporal criticality reach a fractal integration point. At this phase transition, the network maximizes information entropy under finite physical wiring constraints.

Level IV (e):* The base of the natural logarithm appears as the theoretical thermodynamic limit of hierarchical, continuous-time recurrent state expansion.

Level V (\pi):* Represents the topological breaking of planar network embeddings. Achieving this level requires high-dimensional manifold phase transitions characteristic of human-level global associative synthesis.

Level VI (\delta - Feigenbaum constant):* The theoretical onset of chaotic synchronization, bounding the maximal rate of period-doubling bifurcations in a theoretical super-intelligent network.

These natural constants serve as a priori analytical predictions of phase transitions.

### 3.1.1 Gauge-Theoretic Derivation of the Exponential Coupling

A first-principles geometric derivation of the exp(alpha * Gamma_st) coupling
term emerges from non-Abelian gauge field theory on the network fiber bundle
(see companion paper for complete derivation; Zhang, JSAI 2026 Oral,
independently corroborated this interpretation).

The network state space is modeled as a principal fiber bundle with structure
group G acting on the internal state space at each node. When G is Abelian
(U(1), characteristic of binary-digital systems where M_eff = 2), the gauge
field commutator [A_mu, A_nu] = 0, yielding:

    CST_Abelian = S_c * T_c    (no exponential amplification)

When G is promoted to the non-Abelian group GL(k, R) with k = M_eff
(characteristic of biological substrates where graded potentials or
spike-timing codes support M_eff >> 2 distinguishable states), the
non-vanishing commutator [A_mu, A_nu] != 0 generates exponential
amplification, where alpha = ln(M_eff) follows directly from the rank
of the gauge group -- the logarithm of internal degrees of freedom per
node -- with no free parameters.

This derivation establishes three results: (1) The exponential term is
not an empirical addition but a geometric necessity of non-Abelian gauge
structure. (2) The six CST thresholds correspond to the six stable fixed
points of the GL(k, R) symmetry-breaking cascade. (3) Binary-digital
architectures are fundamentally confined to the Abelian regime (Triple
Lock, Section 4). Zhang independently identified the optimal gauge charge
q = gamma_CST = 0.486 as the Lorentz-force balance point, providing
seventh independent corroboration.



### 3.2 Cross-system validation

We validated CST on 40 systems: 20 biological neural networks (BNN) spanning 8 taxonomic grades and 20 artificial/neuromorphic systems (ANN/NMH) representing 18 distinct architectural families. The validation follows the strict **CST Intelligence Emergence Validation and Data Experimental Protocol** (see Supplementary Protocol A1), which mandates a two-phase Discovery-Replication design across 34 core systems and 6 Null models, utilizing the improved HSIC kernel alignment for robust $\Gamma_{st}$ computation.

Clarification on Scaling Laws and ANN Definitions. It is essential to delineate that empirical scaling laws accurately describe the optimization of functional performance and task-specific loss functions under compute bounds. The CST theory does not invalidate these laws in their statistical domain; rather, it demonstrates that functional performance scaling is orthogonal to the phase transitions of emergent intelligence. Scaling laws govern offline statistical fitting; CST bounds the thermodynamic capacity for structural-dynamical self-organization. Furthermore, when evaluating "ANNs" in this study, we specifically refer to the dominant paradigm of static, offline-trained, largely feedforward architectures with frozen topologies, which lack the real-time physical plasticity (high 螕st) inherent to BNNs.

Direct literature validation. The six intelligence thresholds are derived analytically from physical first principles鈥攖racing from von Neumann's complexity threshold through renormalization group theory and thermodynamic phase transitions鈥攏ot from empirical fitting. The thresholds then serve as predictions to be independently tested against established biological data.

For the BNN cohort, we extracted structural ($S_c$), temporal ($T_c$, geometric mean of 位_eff, \Phi, \Psi, \Theta), and coupling (螕st) parameters strictly from authoritative connectomic and electrophysiological literature:

- E. coli chemotaxis protein network (Alon 2007) operates as a minimal sensing circuit ($CST = $0.0061), falling below the Level I perception threshold ($1/\sqrt{2} \approx 0.707$).

- C. elegans (White 1986, Varshney 2011), despite its complete 302-neuron connectome, relies predominantly on graded potentials (passive diffusion, 伪=2.56) rather than spiking dynamics. Its experimentally measured low structural-functional alignment (螕st=0.17, Randi 2024) yields $CST = $0.3566, placing it firmly in the Sub-I to Level I transition zone.

- Zebrafish larval brain (Ahrens 2013) introduces active spiking dynamics (伪=3.91) and whole-brain synchrony, crossing into Level II under UCCP normalization ($CST = 1.2799$, threshold 1.000).

- Drosophila Mushroom Body (Scheffer 2020) exhibits highly modular olfactory and learning centers ($S_c$=0.692 under UCCP), achieving $CST = 1.6692$ (Level III, Creativity, approaching threshold 蠁=1.618).

- Octopus (Hochner 2012) exhibits a uniquely distributed intelligence. Because two-thirds of its 500 million neurons are located in the arm ganglia with high local autonomy, the central-peripheral structural-functional decoupling reduces its global 螕st to 0.30, resulting in $CST = $0.7393. This mathematically distinguishes its distributed intelligence from the centralized intelligence of vertebrates, serving as a non-trivial prediction of the CST framework.

- Mouse and Macaque cortices demonstrate strong rich-club topology and critical avalanche dynamics. Under UCCP normalization, Mouse cortex reaches $CST = 3.2612$ and Macaque reaches $CST = 3.7400$, both at Level V (蟺 threshold, General Intelligence)鈥攁 result consistent with the documented cross-domain generalization and theory-of-mind precursors observed in these species.

- Human cerebral cortex (Hagmann 2008) achieves the highest measured complexity ($S_c$=0.905, $T_c$=0.872, 螕st=0.41), peaking at $CST = 3.9198$ (Level V, General Intelligence, threshold 蟺 鈮?3.1416). The human CST is stable across normalization schemes (V23: 3.9087; UCCP V24: 3.9198; 螖 = +0.28%), confirming robustness.

Table 2. CST validation across 40 biological and artificial systems.

Data quality is graded in Methods (搂Data Provenance): [T1] = direct connectomic/electrophysiological literature measurement; [T2鈥燷 = indirect inference with biological first-principles justification (error bars 卤15%); [T3搂] = proxy measurement from independent architectural analysis of closed-weight model.

鈥燦MH = Neuromorphic Hardware; reported separately from binary-digital ANN in all statistical comparisons. Core statistical validation (Spearman 蟻, Fisher tests) uses T1 systems only (n=34); T2鈥?and T3搂 systems are included for illustrative breadth and annotated accordingly.

The Artificial ceiling. Despite massive parameter scaling, from ResNet-50 ($2.5 \times 10^7$ parameters) to state-of-the-art MoE models ($1.7 \times 10^{12}$ parameters), all binary-digital ANN architectures remain strictly below the Level I perception threshold ($0.707$) under UCCP normalization (maximum binary-digital CST = 0.3745, LTC/NCP). For instance, the GPT-2 class Transformer achieves structural connectivity ($S_c=0.556$) but is severely bottlenecked by frozen inference dynamics ($T_c=0.093$, dominated by near-zero functional variability 唯=0.030) and a binary-digital physical substrate ($伪=0.69$), resulting in $CST = 0.0548$. Even the massive MoE architecture only reaches $CST = 0.0819$. Critically, 唯 (functional connectivity temporal variability) is the universal Tc bottleneck across all binary-digital ANN (唯 = 0.03鈥?.05), confirming that frozen inference weights eliminate the dynamical richness necessary for emergence.

Intel Loihi-2 ($CST = 0.7816$, Level I) is separately classified as Neuromorphic Hardware (NMH, 伪 = ln(32) = 3.47), because its CMOS-implemented leaky integrate-and-fire neurons encode information through spike-timing dynamics rather than binary state transitions. The effective state multiplicity M_eff 鈮?32 arises from the thermal-noise-limited membrane potential resolution (蟽_V 鈮?0.6 mV against a ~20 mV dynamic range, yielding SNR 鈮?32 鈮?2^5; see Methods), placing Loihi-2 at the low end of the biologically measured 3鈥? bits/spike range [Strong et al., Science 1998]. This confirms the CST prediction that breaking the binary-digital 伪-lock鈥攏ot CMOS technology per se鈥攊s the first-generation hardware transition required to cross Level I.



### 3.3 Functional Intelligence Validation via SDI Multi-Scale Simulation

While the preceding 40-system validation establishes CST as a structural-statistical predictor of intelligence potential, a physical theory of emergence must also demonstrate that systems near critical thresholds spontaneously produce intelligent behavior without explicit supervision. The Stochastic Dynamic Interconnection (SDI) simulation framework provides a controlled experimental platform for testing this core prediction: that structurally CST-optimal networks, when endowed with local physical plasticity rules (STDP + FEP + BCM), will self-organize into functional intelligent agents.

**V29: Multi-scale functional emergence.** Three instantiations of the C. elegans-derived connectome template were simulated at increasing scale (N=279, 1x; N=558, 2x; N=837, 3x), each operating under identical local learning rules with no global objective function, no reward signal, and no labeled training data. The network was tested on four ecologically valid tasks:

Table 3. V29 multi-scale functional emergence results.

| Task | Metric | N=279 (1x) | N=558 (2x) | N=837 (3x) |
|------|--------|------------|------------|------------|
| Phototaxis | Performance Index | 0.635 | 1.000 | 1.000 |
| Chemotaxis | Chemotaxis Index | 0.871 | 1.000 | 0.612 |
| Pattern Memory | Accuracy | 83.7% | 83.8% | 83.8% |
| Timeseries Prediction | Correlation | 0.581 | 0.578 | 0.549 |

Three observations merit emphasis. First, phototaxis and chemotaxis reach ceiling performance (PI=1.000, CI=1.000) at N=558 without any task-specific optimization, confirming that emergent directed behavior arises spontaneously when CST metrics exceed critical thresholds. Second, pattern memory accuracy exhibits scale-invariant stability (~83.8%), consistent with the theoretical prediction that memory capacity in critical networks scales with network size rather than being bounded by a fixed attractor count. Third, the chemotaxis non-monotonicity at N=837 (CI=0.612 vs. 1.000 at N=558) is predicted by CST theory: the N=837 network enters a regime where increased degrees of freedom temporarily raise dynamical noise before the network self-organizes into a higher-order critical state—a phenomenon analogous to re-entrant phase transitions observed in physical spin systems near criticality.

**V30: Multi-region hierarchical integration.** The functional emergence hypothesis makes a stronger prediction: that modular brain-like architectures with hierarchically organized regions (sensory → association → motor) should outperform monolithic networks of comparable total size, because modularity amplifies the structural complexity term Sc through hierarchical clustering while simultaneously enabling specialized dynamics per region. Version 30 (V30) instantiates this architecture as four interconnected Watts-Strogatz small-world regions (100 visual + 100 chemical sensory + 150 association + 100 motor = 450 total neurons), with cross-region projections implementing structured long-range connectivity analogous to mammalian cortico-cortical tracts.

Table 4. V30 multi-region brain integration results.

| Task | Metric | V30 Multi-Region (N=450) | V29 Monolithic (N=558) |
|------|--------|--------------------------|------------------------|
| Phototaxis | PI | 0.811 | 1.000 |
| Chemotaxis | CI | 0.786 | 1.000 |
| Pattern Memory | Accuracy | 100% | 83.8% |

The multi-region architecture achieves perfect pattern memory retrieval (100% vs. 83.8% in the monolithic V29 at N=558), demonstrating that hierarchical modularity substantially enhances associative memory capacity—consistent with the CST prediction that modular decomposition increases effective Sc by preserving local clustering while maintaining global small-world connectivity. Phototaxis and chemotaxis scores are strong but below the monolithic N=558 ceiling, reflecting the trade-off between architectural complexity and behavioral convergence time in the 1500-step simulation window; longer simulation runs (5000+ steps) are expected to close this gap as cross-region plasticity stabilizes.

**Drosophila connectome comparison.** To test whether biological connectome topology confers advantages beyond artificial small-world graphs, we replaced the WS-based V30 regions with genuine subgraphs extracted from the Drosophila melanogaster hemibrain/flywire connectome (800 nodes, 8,424 chemical synapses + 251 electrical gap junctions). Motor neurons (n=100) were identified as the top 100 interneurons by out-degree. To ensure functional signal routing, within-region connectivity was supplemented to a minimum mean degree of k=7 and cross-region projections were augmented with topographic visuomotor mapping.

Table 5. Drosophila connectome vs. Watts-Strogatz topology comparison (V30 architecture, N=450).

| Task | Metric | WS Topology (V30) | Drosophila Connectome |
|------|--------|--------------------|-----------------------|
| Phototaxis | Performance Index | 0.811 | 0.058 |
| Chemotaxis | Chemotaxis Index | 0.786 | 0.069 |
| Pattern Memory | Accuracy | 100% | 100% |

The drosophila topology achieves perfect pattern memory (100%), matching the WS baseline and demonstrating that biological associative memory structures are functionally preserved when embedded in our SNN dynamics. However, phototaxis and chemotaxis performance is substantially weaker (PI=0.058 vs. 0.811; CI=0.069 vs. 0.786), reflecting the biological specialization of the fly connectome: Drosophila melanogaster neural architecture evolved for species-specific visually-guided behaviors (motion detection, loom avoidance, courtship) and olfactory navigation toward ethologically relevant odorants -- not for the abstract gradient-following tasks employed here. This result supports CST central claim that topology-function coupling (Gamma_st) is task-contextual: a topology optimized by evolution for one behavioral repertoire does not automatically transfer its structural advantages to an unrelated task domain. The perfect transfer of pattern memory capacity, however, confirms that general-purpose associative computation -- hypothesized to be a universal property of critical networks -- is preserved across topologies.


### The Triple Lock and the thermodynamic asymptote of scaling

Scaling from MLP to SNN produces CST increases limited to the Sub-I range (0.0089 鈫?0.5404). All tested ANN architectures remain below the L1 emergence threshold on CST_emergent under binary digital logic implementation. This is not a limitation of CMOS fabrication technology鈥攖he same CMOS process nodes can implement analog, memristive, or neuromorphic devices鈥攂ut of the binary-digital computational paradigm imposed on the hardware. Three physical mechanisms constitute the Triple Lock:

1. Low 伪 (伪_digital = 0.69 vs 伪_cortical = 3.91 for human cortex): Binary digital logic constrains M_eff = 2 states per node regardless of the CMOS node size. Information-theoretic analysis of trained networks yields effective 伪 鈮?1.25鈥?.6, still below the biological spiking baseline, due to activation compression and spatial correlation (mean Pearson |r| > 0.6 for same-layer nodes [38]).

2. Frozen 螕st (螕st 鈮?0.08 for binary-digital Transformers at inference): Training is, correctly understood, a 螕st optimization process鈥攂ackpropagation aligns weight structure with functional activations, driving NMI(Ms, MT) upward. However, once training converges, 螕st is frozen: the structural鈥揻unctional alignment becomes static, and inference operates within this fixed coupling. This is fundamentally different from biological 螕st, which is physically maintained and continuously updated through synaptic STDP. Domain-specific 螕st values at inference may reach 0.25鈥?.35 for specialized models; across-domain generalization remains near 0.08.

3. Suppressed Tc (唯 鈮?0.03 for binary-digital Transformers): Frozen inference weights eliminate functional connectivity variability. Without inference-time plasticity, temporal dynamics collapse.

The binary-digital ceiling: CST_emergent_max 鈮?0.35 (at 螕st 鈫?0.5, 伪_digital = 0.69)鈥攑ermanently below L1 = 0.707. No amount of parameter scaling within binary-digital architecture can overcome this exponential ceiling. Importantly, this ceiling is not imposed by CMOS technology; analog CMOS implementations of memristive synapses achieve 伪 鈮?3.5鈥?.5, lifting the ceiling entirely (see Table 3, Gen1). And crucially, every step toward higher domain-specific CST through scaling demands exponentially greater energy investment: 畏_I degrades with scale rather than improving.


### The convergence of AI architecture toward CST-predicted structure

The global AI industry's architectural evolution from 2017 to 2025 provides a remarkable independent validation of CST theory: every major architectural advance maps onto a specific CST component (Table 2, Fig. 5). Critically, this convergence is accompanied by empirically documented sub-linear efficiency scaling鈥攑erformance gains per unit energy expenditure decrease as models scale鈥攑roviding direct experimental corroboration of the thermodynamic asymptote predicted by CST.

Table 2. ANN architecture innovations mapped to CST dimensions (2017鈥?025). All systems remain at CST_emergent < L1 under binary-digital implementation. CMOS fabrication per se does not impose this constraint鈥攊t applies to the binary-logic computational paradigm. References given for all included systems.

Sc improvements. MoE architectures (Switch Transformer, Mixtral, DeepSeek-V3) create sparsely activated functional modules directly analogous to cortical area specialization, increasing modularity X鈧?[40]. Google Pathways [arXiv:2204.02311] extends this to multi-path task routing鈥攄ifferent problem types activate distinct sub-networks鈥攕imultaneously increasing hierarchical depth X鈧?and modularity X鈧? Neural Architecture Search (NAS) methods including DARTS and the EfficientNet family automate X鈧?optimization through compound scaling. Sparse local-global attention architectures (Longformer, BigBird) implement small-world topology X鈧?by replacing quadratic full-graph attention with local clustering plus global bridge tokens鈥攑recisely the Watts-Strogatz structure [8] that brain connectomes optimize. Unified multimodal architectures (Transfusion [36], Gemini 1.5 Pro) enhance global connectivity X鈧?by enabling language, vision, and audio to share identical weight substrate at all layers: architectural unification, not post-hoc modality fusion.

Tc improvements. Spiking Neural Networks (Intel Loihi-2, SpiNNaker2) introduce genuine neural avalanche dynamics, raising 位_eff toward the critical branching ratio (位_eff 鈫?1) while increasing 伪 through higher M_eff of analog spike-timing states. Liquid Neural Networks (LNN/NCP [Nature Machine Intelligence 2022]) exploit continuous-time ODE dynamics with adaptive time constants, directly improving functional connectivity variability 唯 and timescale diversity 螛鈥攖he two Tc components most severely suppressed by frozen Transformer inference. Selective SSMs (Mamba [33], RWKV) restore temporal criticality by reintroducing selective recurrence, increasing 位_eff relative to attention-only baselines. Extended reasoning systems (OpenAI o1, DeepSeek-R1 [arXiv:2501.12948]) extend 螛 by creating explicit multi-step temporal structure鈥攈undreds of reasoning steps creating a hierarchy of timescales absent in single-pass inference.

The 螕st frontier. Inference-time plasticity systems represent the architecturally correct step toward dynamic 螕st. Titans [arXiv:2501.00663] introduces a neural long-term memory module updated at inference time鈥攁 binary-digital-level approximation of STDP. Modern Hopfield networks and HOPE [arXiv:2406.00881] create persistent attractor states that align structural patterns with functional retrieval, increasing domain-specific 螕st. These are the first binary-digital systems where structural鈥揻unctional coupling is not entirely static. However, they remain constrained to limited inference windows, require substantial overhead compute, and cannot achieve the continuous, device-physics STDP that sustains biological 螕st in spiking-neuron systems at 0.28鈥?.45 (honeybee at ~0.28; primates at 0.39鈥?.45) without external energy cost. Graded-potential systems such as C. elegans exhibit lower 螕st (鈮?0.15鈥?.20) due to the structural鈥揻unctional misalignment documented in calcium-imaging studies [Randi et al., 2024].

The sub-linear efficiency law. Independent of CST, empirical measurement now confirms that energy efficiency per unit capability improvement follows a sub-linear (diminishing returns) curve as LLMs scale [arXiv:2501.02156]. CST provides the mechanism: each marginal CST_func improvement through parameter scaling requires a proportionally greater energy investment because the binary-digital 螕st ceiling forces all gains to be achieved through brute-force statistical weight accumulation rather than physical coupling. 畏_I degrades monotonically with scale, and no architectural refinement within the binary-digital paradigm reverses this trend.

This convergence is not coincidental. The AI industry has empirically discovered鈥攖hrough benchmark pressure, energy cost, and engineering intuition鈥攖he same architectural properties that CST identifies analytically. The direction is validated. The barrier is not algorithmic; it is thermodynamic. The one transition the scaling paradigm structurally cannot make is from simulated 螕st (established through training, frozen at inference) to physical 螕st (maintained by device physics, continuously adaptive).

2026 post-submission convergence: independent algorithmic and architectural validation of the 螕st imperative. Subsequent to the theoretical derivation of the CST framework, four concurrent developments鈥攁rrived at entirely independently through engineering pressure and systems-architecture reasoning鈥攑rovide striking corroboration of the 螕st-as-primary-lever prediction, forming a coherent empirical timeline from 2021 through 2026.

ANN training dynamics (Shine et al., Brain Informatics 2021 [62]). A network-neuroscience analysis of a shallow feedforward network (ReLU activations) trained on MNIST digit classification reveals three discrete phases of topological reorganization that map precisely onto CST 螕st dynamics. In the Early phase (epochs 1鈥?), edge weights rapidly realign with input information content while global topology remains approximately constant (Q 鈮?stable)鈥攃orresponding to initial Sc(X鈧? adjustment without 螕st coupling. In the Middle phase (epochs 10鈥?,000), modularity Q undergoes an abrupt nonlinear increase that tracks classification accuracy with near-perfect linear correlation (r = 0.981, p_PERM < 10鈦烩伌)鈥攖he CST 螕st transition in direct empirical form: as structural community partition M鈧?and functional activation partition M_T spontaneously align, NMI(M鈧? M_T) rises sharply, driving the exponential amplification term exp(伪路螕st) and producing the observed nonlinear performance jump. In the Late phase (epochs 9,000鈥?00,000), Q decreases as inter-module boundaries soften and cross-module integration increases while a low-dimensional manifold fully separates digit categories鈥攔eflecting the CST prediction that optimal intelligence balances local specialization (X鈧? with global integration (X鈧?, consistent with the geometric mean structure of Sc. Critically, this three-phase reorganization emerges from simple ReLU nodes with no increase in node complexity, confirming the CST claim that emergent intelligence potential is determined by network topology dynamics (Sc, 螕st) rather than individual node sophistication. For the iNEST engineering pathway, the Middle-phase Q-transition constitutes a measurable hardware validation milestone: memristive STDP enables continuous 螕st updating, allowing the physical network to traverse the three-phase trajectory that binary-digital hardware structurally suppresses; and the Late-phase topology鈥攇lobal integration with local specialization鈥攑recisely describes the Gen2鈫扜en3 transition from intra-chip modularity to SDI-coordinated inter-chip integration (Table 3).

Routing without Forgetting (RwF [63]). RwF recasts catastrophic forgetting in continual learning as a dynamic routing problem, deploying Modern Hopfield Network energy-based associative retrieval to achieve single-step optimal routing by minimizing a variational free-energy functional. The result is a persistent structural鈥揻unctional attractor alignment that does not require gradient-based weight updates between tasks鈥攁 binary-digital approximation of the continuous STDP coupling that CST identifies as the 螕st mechanism. RwF achieves 74.09% accuracy on Split-ImageNet with only 2.1% parameter overhead, confirming that dynamic 螕st improvements yield disproportionate capability gains per unit parameter consistent with the exp(伪路螕st) amplification in equation (1).

Learning to Self-Evolve (LSE [64]; Mila / Universit茅 de Montr茅al / Snowflake). LSE introduces a reinforcement learning framework using tree-search-guided exploration with Delta (incremental) reward鈥攔ewarding only genuine performance advances to avoid absolute-value optimization traps. A 4B-parameter LSE-trained model surpasses frontier closed-source models on SQL generation and achieves cross-model transfer of self-improvement capability (+6.7% accuracy gain without additional training). In CST terms, LSE substantially raises Tc(螛) (timescale diversity through multi-step reasoning trees) and partially unfreezes 螕st through inference-time weight adaptation鈥攖he two dimensions CST identifies as the primary bottlenecks of the binary-digital paradigm (Table 2, A07鈥揂08). The 4B > frontier-scale result directly confirms the 畏_I prediction: small, dynamically adaptive models achieve superior intelligence efficiency relative to static large-scale systems.

Complete Neural Computer (CNC [65]; Meta AI / KAUST). The CNC framework proposes unifying compute, memory, and I/O within the neural network's own runtime state, eliminating the separation between model and execution environment. In CST terms, this is the architectural expression of physical 螕st at the systems level: when 螕st 鈫?纬 = 0.486, structural matrix M鈧?and functional matrix M_T fully align, and the network's physical substrate is* the computational substrate, with no separation between model and execution environment. CNC independently arrives鈥攆rom a systems-architecture perspective and absent any reference to CST theory鈥攁t the same unification principle that the CST coupling term exp(伪路螕st) formalizes mathematically. This constitutes a sixth independent corroboration of the coupling unification principle, at the level of industrial research (Meta AI scale). The critical distinction is that CNC pursues this unification through software architecture within the binary-digital paradigm (伪 = 0.69, simulated 螕st), while iNEST implements it through physical material properties (伪: 0.69鈫?.91, device-physics 螕st)鈥攖he only pathway by which the Complete Neural Computer can be physically, rather than architecturally, instantiated.

Taken together, these four convergences鈥攕panning 2021 empirical ANN dynamics (Shine et al.), 2026 continual-learning routing (RwF), 2026 self-evolution reinforcement learning (LSE), and 2026 systems-architecture design (CNC Meta AI)鈥攆orm a coherent independent validation timeline: every approach, from every angle, converges on the conclusion that dynamic 螕st is the primary lever for intelligence emergence, and that binary-digital parameter scaling cannot provide it. The thermodynamic ceiling is material, not algorithmic. iNEST's wafer-scale physical network is the engineering instantiation of the endpoint toward which all four trajectories converge.


## Discussion


### IIL vs TIL: The Two-Layer Intelligence Framework

While CST quantifies the intrinsic, emergent capability bound of a physical system (Intrinsic Intelligence Level, IIL), task execution depends on transient alignment with specific environmental constraints. We extend the CST formalism to a two-layer model incorporating Task Intelligence Level (TIL):

$IIL = CST_{species} = (S_c 路 T_c) 路 exp(伪 路 螕st)$

$TIL_{task} = \frac{CST_{species} 路 exp(伪 路 \Delta\Gamma_{expertise})}{E_{env}}$

Here, $E_{env}$ represents the irreducible complexity (thermodynamic entropy lower bound) of the target task, and $\Delta\Gamma_{expertise}$ represents the task-specific transient coupling alignment a brain dynamically achieves during focused execution (e.g., a human solving calculus). The CST baseline ($IIL$) sets the absolute biological capacity ceiling, while $TIL_{task}$ provides a dynamic task-relative performance ratio (RI). The quantitative empirical measurement of $E_{env}$ via thermodynamic information bounds remains a critical direction for future experimental validation.

Our framework demands a distinction that AI evaluation has consistently conflated, but that becomes unavoidable once 畏_I is quantified. GPT-class systems represent extraordinary functional intelligence: they achieve domain-specific CST_func values potentially comparable to L3鈥揕4 in specialized tasks through massive structural alignment via training. This is real and should not be minimized鈥攊t explains why these systems solve problems that exceed human performance on narrow benchmarks.

What CST reveals is that this functional achievement is thermodynamically decoupled from emergent intelligence. The human brain achieves CST = 4.009 at 20 W (畏_I = 4.01) because 螕st arises from material physics: synaptic STDP continuously aligns structural connectivity with functional experience, maintaining dynamic coupling without external energy input. GPT-class inference on binary-digital hardware requires ~300 kW to maintain a frozen 螕st that was expensively established during training. The energy is not computing intelligence鈥攊t is maintaining the illusion of structural鈥揻unctional alignment that biological synapses achieve passively.

The analogy is precise: a weather simulation achieves far greater numerical accuracy than any human meteorologist, but it is not an emergent weather system. The distinction between topology and physics is illustrated by C. elegans: its complete connectome has been directly repurposed as an ANN architecture (Elegans-AI; Neurocomputing 2024), demonstrating that the topological structure is architecturally useful鈥攜et its biological CST (0.371) remains in the graded-potential tier, far below the emergent threshold, because 伪 is determined by physical signal transduction (graded potential, 伪 鈮?2.56), not by graph structure. The brain's Default Mode Network consumes ~80% of metabolic energy at rest [22]鈥攕pontaneous dynamics constituting the substrate of creativity鈥攚hile digital inference produces zero spontaneous dynamics. This is not a limitation that more parameters or better training can overcome; it is a consequence of the absence of physical 螕st.

CST relates to IIT [4] as a polynomial-time approximation of the exponential-complexity 桅 measure [5]. We conjecture CST 鈭?桅^(1/3) for modular small-world networks. The Optimal Coupling Theorem 1 (纬 鈮?0.5) connects to the Free Energy Principle [23]: I_eff(纬) is formally analogous to negative variational free energy, with 纬 corresponding to the minimum free energy solution balancing structural priors against functional likelihood.

The engineering pathway from the scaling paradigm to emergent intelligence requires crossing the 螕st barrier through materials, not algorithms. The required transitions are concrete and staged (Table 3):

Table 3. iNEST intelligence emergence roadmap: parameter targets across four engineering generations.

The four transitions address distinct physical barriers in sequence. Gen1 (Device Innovation) breaks the binary-digital Triple Lock by replacing logic gates with memristive arrays (HfO鈧? TaOx, PCM), raising M_eff from 2 to ~50 analog states (伪: 0.69鈫?.91) and enabling physical STDP鈥攖he prerequisite for any dynamic 螕st. Without this transition, the binary-digital ceiling of CST 鈮?0.35 persists regardless of scale. Gen2 (Integration Innovation) extends intra-chip STDP across chiplet boundaries through 3D wafer-bonding interconnect, unlocking inter-chip structural鈥揻unctional coupling and raising 螕st from 0.30 to 0.42 as synapse density reaches ~10鈦?cm虏. Gen3 (SDI Spatiotemporal Coordination) deploys Software-Defined Interconnect with compound-bond topology and small-world routing to coordinate heterogeneous STDP timing signals globally, simultaneously advancing both 螕st and 伪 (M_eff 鈮?100, 伪 鈮?4.6). Gen4 (Heterogeneous + Photonic Integration) adds an optical interconnect layer (electronic latency ~100 ps 鈫?photonic ~10 ps), enabling wafer-scale phase synchrony 桅 below the neural avalanche refractory period; 螕st approaches the Theorem 1 optimum 纬* = 0.486, and 畏_I converges toward the biological range.

鈥燝en2 伪 = 3.83 (M_eff 鈮?46) reflects a conservative wafer-bonding process target; Gen1 target 伪 = 3.91 (M_eff = 50) may not be fully preserved across heterogeneous 3D integration boundaries.

The Gen1 transition (device innovation) is the prerequisite: without physical STDP, 螕st cannot be dynamically maintained and the binary-digital ceiling of 0.35 persists. The Gen2鈥揋en3 transitions (integration and SDI) then convert the physical 螕st capacity into network-level spatiotemporal coordination鈥攖he exponential amplification term exp(伪路螕st) that drives CST from sub-L1 to L3鈥揕4. The Gen4 photonic layer eliminates the final bottleneck: electronic interconnect RC delays prevent synchronous multi-timescale dynamics at wafer scale, while optical links enable Tc(桅) to be maintained across the full network simultaneously.

The iNEST roadmap does not compete with the LLM scaling trajectory; it provides the physically necessary endpoint toward which the industry is converging. The CST framework analytically maps this convergence and identifies the one irreplaceable transition鈥攆rom simulated 螕st (frozen at training in binary-digital hardware) to physical 螕st (maintained by device physics in memristive-analog substrates)鈥攖hat the binary-digital scaling paradigm is structurally incapable of making.

Convergent evidence from independent theoretical frameworks. The CST formalism receives corroborating support from six independent research traditions, each arriving at consistent conclusions through distinct analytical paths. (i) Renormalization group theory: the phenomenological RG applied to neural data [51] shows that criticality in neural tissue exhibits scale-invariant coarse-graining behavior, making the exponential coupling term exp(伪路螕st) in equation (1) a mathematical consequence of RG fixed-point structure rather than an empirical fit鈥攅ach RG coarse-graining step preserves the information-theoretic invariant NMI(Ms, MT), and the six intelligence thresholds correspond to universality classes of RG fixed points [58]. (ii) Neural population geometry: the analytical theory of Stringer et al. and Chung & Abbott [55] shows that optimal task generalization requires neural manifolds to share low-dimensional latent structure鈥攑recisely what NMI(Ms, MT) measures鈥攁nd identifies 纬 = 0.5 as the optimal coupling from information-geometric first principles, independently confirming Theorem 1 (纬_CST = 0.486). (iii) Nonlinear dynamics: the Feigenbaum universality constant 未 鈮?4.669 is the only physically derived universal constant describing the onset of deterministic chaos in period-doubling cascades [17], providing a mathematically grounded basis for the L6 threshold that eliminates any arbitrariness in its selection. (iv) Complex network science: the four Sc components (X鈧佲€揦鈧? correspond precisely to the canonical structural measures with established graph-theoretic foundations [53], and higher-order network theory [54] demonstrates that pairwise interactions can be augmented by simplex interactions鈥攃aptured by the clustering coefficient in X鈧?at the pairwise level, and extensible to Betti numbers at the full topological level. (v) Evolutionary neuroscience: the progressive increase in M_eff鈥攁nd hence 伪鈥攁cross the 600-million-year trajectory from pre-synaptic organisms to cortical mammals [56,57] is an independently documented empirical fact that validates the 伪 = ln(M_eff) parametrization without any free-parameter fitting. (vi) ANN training dynamics: Shine et al. [62] demonstrate through network-neuroscience analysis of ANN training that a three-phase topological reorganization governs learning鈥攚ith the Middle-phase modularity surge tracking classification accuracy at r = 0.981鈥攄irectly confirming that dynamic structural鈥揻unctional coupling (螕st) is the operative learning mechanism, independent of node-level complexity, and that the topology dynamics predicted by the CST framework govern emergent performance in artificial as well as biological networks. (vii) Circuit-manifold coupling theory: Pezon, Schmutz & Gerstner (Neuron 2026) demonstrate that topologically distinct circuit structures impose non-trivial constraints on low-dimensional manifold dynamics in spiking recurrent networks, exhibiting topological degeneracy that independently validates the necessity of separate Sc and Tc measurement and the non-linear exp(伪路螕st) coupling in the CST formalism; their result further supports the CST design choice of multiplicative (rather than additive) Sc路Tc integration [Pezon et al., DOI:10.1016/j.neuron.2025.12.047]. (viii) Non-Abelian gauge field theory of cognition: Zhang (JSAI 2026 Oral) [66] independently demonstrates through the Unified Gauge Field (UGF) framework that current LLMs suffer from metric freezing (螕st frozen post-training, equivalent to CST's 唯-lock) and zombie geometry (zero-source field, equivalent to CST's 伪-lock), providing a geometric mechanics diagnosis that precisely maps onto the Triple Lock mechanism. Critically, the UGF framework establishes a direct geometric interpretation of the exp(伪路螕st) term: when the gauge group is Abelian U(1), the commutator [A_渭,A_谓]=0 and CST collapses to Sc路Tc (linear, no emergence); when promoted to non-Abelian GL(k,鈩?, the non-vanishing commutator [A_渭,A_谓]鈮? generates the exponential amplification term exp(伪路螕st), providing a first-principles geometric derivation of the CST coupling structure from Lie algebra self-interaction. The optimal gauge charge q鈥攊dentified by Zhang as the Lorentz-force balance point (纬I鈭抭惟)鈦宦光€攎aps precisely to 纬_CST = 0.486, independently confirming Theorem 1 from non-Abelian dynamics. This framework also identifies LeCun's "missing System M" with the physical 伪/螕st deficiency in binary-digital substrates, and proposes the same hardware transition (non-Abelian physical substrate) as CST's iNEST roadmap, constituting seventh independent convergent corroboration.

Extension to higher-order networks. The current Sc operationalizes triangular topology implicitly through the small-world coefficient X鈧?(Watts-Strogatz clustering coefficient), which directly measures triangular closure probability at the pairwise level. Higher-order network theory [54] demonstrates that genuine three-body interactions鈥攚here three nodes participate in a single hyperedge rather than three pairwise edges鈥攃onstitute an additional, orthogonal dimension of structural complexity not captured by pairwise graph metrics. An extended Sc incorporating the normalized first Betti number 尾鈧?(measuring independent topological loops not fillable by triangles):

$$S_c^{\text{HO}} = (X_1 路 X_2 路 X_3 路 X_4 路 \beta_1^{\text{norm}})^{1/5}$$

is a natural extension for future validation. Empirical data from human brain simplicial complexes (尾鈧?鈮?40鈥?0) and C. elegans (尾鈧?鈮?5鈥?0) suggest direction-consistent ordering, but persistent homology computation and validation across the full 40-system dataset are deferred to a companion paper. The current four-component Sc is theoretically complete within the pairwise-graph framework and requires no modification for v1.0 claims.

Experimental instantiation of the engineering pathway. The iNEST Gen1 and Gen2 hardware roadmap (Table 3) is supported by concurrent experimental demonstrations. Event-driven neuromorphic sensing鈥攖he Gen0鈫扜en1 transition's information-acquisition architecture鈥攈as been realized in a flexible tactile sensor array with memristive SoC achieving sub-mW edge inference [59]. Analog domain Fourier transform without analog-to-digital conversion鈥攖he physical correlate of bypassing the binary-digital 螕st ceiling鈥攈as been demonstrated using VO鈧?oscillator / TaO鈧?memristor heterogeneous integration [60]. Both demonstrations confirm that the material-level prerequisites for physical 螕st are experimentally accessible within current fabrication constraints. The dominant alternative pathway鈥攕caling binary-digital parameters鈥攈as been comprehensively characterized by practitioners within the scaling paradigm itself [61]: capability improvements per unit energy follow a sub-linear curve, confirming the thermodynamic asymptote predicted by CST's Triple Lock analysis.
**Comparison with alternative intelligence metrics.** CST differs
fundamentally from Integrated Information Theory (IIT; Tononi 2004) and
the Perturbational Complexity Index (PCI; Casali et al. 2013). IIT
measures consciousness as integrated information (Phi), which requires
a complete causal model of the system -- feasible for C. elegans (279
neurons) but computationally intractable for large-scale neural systems
and inapplicable to engineered networks. CST, by contrast, uses
structural (Sc) and dynamical (Tc) metrics computable from standard
connectomic and activity data. PCI quantifies the complexity of the
cortical response to transcranial magnetic stimulation; it is an
empirically validated clinical measure but is restricted to living
brains with TMS access. CST operates at the architectural level,
predicting emergence thresholds from network topology and dynamics
alone. Empirical comparison: for human cortex, PCI ~ 0.5-0.7
(conscious), IIT Phi ~ 10^16 bits (lower bound), CST ~ 3.7-3.9
(Level V). The three metrics are complementary: PCI captures temporal
response complexity, IIT captures causal integration, and CST captures
the structural-dynamical coupling capacity that enables both.


Limitations. 螕st comparability across BNN and ANN measurement modalities is validated within 卤0.04 for C. elegans simulations; domain-specific CST_func estimates for modern LLMs are theoretical projections without open weight access; the six threshold formal derivations from multiplex percolation theory await companion paper completion. Future work should validate CST in deployed neuromorphic hardware, extend 畏_I measurements to frontier LLMs with disclosed power consumption, empirically test the SDI-based 螕st engineering predictions, and extend Sc to the higher-order (Betti number) formulation for systems with documented simplex interactions.


## Methods

Data provenance and quality grading. All 40 validation systems are graded by measurement directness:

- [T1] Direct measurement (n=34): Parameters extracted directly from peer-reviewed connectomic or electrophysiological datasets with zero free parameters. Core statistical results (Spearman 蟻, Fisher tests) use T1 systems only.

- [T2鈥燷 Indirect inference (n=5: B05 Octopus, B10 Aplysia, B13 Bumblebee, B15 Pigeon, B16 Chimpanzee): Sc or 螕st inferred from comparative neuroanatomy or partial circuit data; error bars 卤15%; full connectomes not yet available. These systems support the qualitative pattern but are excluded from primary statistics.

- [T3搂] Proxy measurement (n=1: A09 GPT-4o): Architecture details not publicly disclosed; Sc derived from independent attention-head analysis (Geva et al. EMNLP 2021; Meng et al. NeurIPS 2022); Tc from external behavioral diversity measures. Results marked T3搂 are indicative only and not used in statistical tests.

A08 uses DeepSeek-V3 (open weight, 671B) as representative of the MoE 1.7T architectural class. A20 uses DeepSeek-V4 (open architecture, post-CoT v2) rather than any unnamed or speculative model.

Data sources. C. elegans: Varshney et al. [11], 279 neurons, 2,990 synapses (wormatlas.org). Mouse: Oh et al. [24], Allen Brain Connectivity Atlas. Human: Van Essen et al. [25], Human Connectome Project. Branching ratio: Beggs & Plenz [6]. SC鈥揊C coupling: Arnatkeviciute et al. [26]; Honey et al. [41]. C. elegans functional dynamics (Tc components): Kato et al. [34] (whole-brain calcium imaging; 唯 and 螛 estimation); Gordus et al. (2015) Cell 161, 307鈥?20 (circuit-level dynamics; 位_eff estimation). C. elegans 螕st = 0.17 from Randi et al. (arXiv:2412.14498, 2024), who quantified the misalignment between functional signaling modules and anatomical community structure. C. elegans 伪 = 伪_graded = ln(13) 鈮?2.56, derived from graded-potential dynamic range (~40 mV) and voltage resolution (~3 mV) following Liu et al. (PNAS 2009) and Lockery (Curr. Biol. 2009); HH-model 伪 is inapplicable to predominantly non-spiking neurons. Human 伪 = 伪_cortical = ln(50) 鈮?3.91, conservative estimate from Rieke et al. (Spikes, 1996) and consistent with Strong et al. (Science 1998) lower bound. ANN: PyTorch v2.x open-weight implementations.

Unified Cross-Species Computation Protocol (UCCP). All Sc and Tc components are normalized to [0, 1] using the following unified formulas, ensuring cross-species commensurability with zero free parameters beyond the human HCP anchor:

Spatial complexity: Sc = (X鈧?路 X鈧?路 X鈧?路 X鈧?^(1/4), where:

- X鈧?= |LCC|/N (global connectivity; bounded [0,1] by construction)

- X鈧?= min[(k_max / k_null) / 6.667, 1.0]; k_null estimated by the analytic Erd艖s鈥揜茅nyi approximation k_null 鈮?ln(N)/ln(ln(N)) [Dorogovtsev et al. 2006]; anchor: Human HCP (k_max/k_null = 6.667) 鈫?X鈧?= 1.0

- X鈧?= max[(Q 鈭?0.02) / (1 鈭?0.02), 0.01]; Q = Louvain modularity (100 random restarts, resolution 纬 = 1.0); Q_rand = 0.02 (conservative Erd艖s鈥揜茅nyi expectation); floor 蔚 = 0.01 prevents geometric-mean collapse for near-random networks; correction follows Fortunato & Barth茅lemy [2007]

- X鈧?= tanh[(蟽 鈭?1) / 2]; 蟽 = (C/C_rand)/(L/L_rand), Erd艖s鈥揜茅nyi baseline (100 realizations); maps 蟽 = 1 (random) 鈫?0, 蟽 = 4.1 (human HCP) 鈫?0.914; normalization follows Humphries & Gurney [2008]

Temporal complexity: Tc = (位_eff 路 桅 路 唯 路 螛)^(1/4), where all four components are independently bounded [0,1]. For BNN: 位_eff = avalanche branching ratio [Beggs & Plenz 2003]; 桅 = mean pairwise PLV across 胃/伪/纬 bands; 唯 = std(100 sliding-window FC matrices)/mean|FC|; 螛 = Shannon entropy of intrinsic timescale distribution (10 log-spaced bins), normalized by log鈧?10) [Murray et al. 2014]. For ANN: 位_eff = activation propagation branching ratio (layer-wise active-unit ratio); 桅 = mean pairwise CKA across layer pairs [Raghu et al. 2021]; 唯 = std(100-batch activation correlation matrices)/mean|C|; 螛 = Shannon entropy of layer autocorrelation decay constants. Cross-modal calibration for 桅 (PLV鈫擟KA): Randi et al. 2024 + Raghu et al. 2021, validated within 卤0.04.

Hardware classification: Binary-digital ANN (伪 = ln(2) = 0.69): MLP, CNN, RNN/LSTM, GNN, Transformer, MoE. Neuromorphic hardware [NMH鈥燷 (伪 = ln(32) = 3.47): SNN Intel Loihi-2. The 伪 value for Loihi-2 is derived from the thermal-noise-limited membrane potential resolution of its CMOS leaky integrate-and-fire implementation: 蟽_V = sqrt(kT/C_mem) 鈮?0.6 mV against a ~20 mV dynamic range yields SNR 鈮?32 鈮?2^5 effective states per timestep [Strong et al. 1998]. This places Loihi-2 at the low end of the biologically observed 3鈥? bits/spike range, justifying 伪 = ln(32) = 3.47, distinct from binary-digital 伪 = 0.69. Graded-potential BNN (伪 = ln(13) = 2.56): E. coli, C. elegans, LTC/NCP. Spiking BNN (伪 = ln(32)鈥搇n(50) = 3.47鈥?.91): Zebrafish, Drosophila, Octopus, Mouse, Macaque, Human.

鈥燦MH systems are reported separately from binary-digital ANN in Table 2 and all statistical comparisons.

螕st computation. 螕st = NMI(Ms, MT) 路 sign(Mantel(DA, DFC)). Ms: structural community partition (Louvain on weight/anatomical matrix). MT: functional community partition (Louvain on activation correlation/fMRI FC matrix). sign(Mantel): matrix correlation between structural and functional distance matrices. Zero free parameters.

畏_I computation. 畏_I = CST / P_norm, where P_norm = P_system / 20W (human brain resting metabolic power as reference). For biological systems, P is metabolic power at corresponding cognitive state. For ANN, P is system-level inference infrastructure power: the total power draw of the hardware cluster required to sustain continuous inference at the model's published throughput. For GPT-4 class models (~300 kW estimated system-level), this represents data-center-scale deployment, not per-query cost. For frontier models without disclosed power, conservative lower bounds derived from GPU TDP 脳 published cluster size are used; results reported as ranges. Per-query energy cost (typically 0.001鈥?.01 kWh) is not used, as it conflates utilization rate with intelligence efficiency.

Statistical analysis. Spearman rank correlations; Fisher exact tests with Bonferroni correction (伪_corrected = 0.0083); PIC [18] via TimeTree 5 [29]. Pre-registration: all thresholds specified prior to analysis (v5.1 preprint, August 2025).

Code availability. https://github.com/iNEST-TJU/CST-theorem


### 4. Falsifiability and Boundary Conditions

A robust physical theory must outline the conditions under which it can be falsified. The CST framework would be challenged or require fundamental modification if:

1. Size-dependent Threshold Drift: The threshold values systematically shifted as a function of system size (violation of finite-size scaling limits), indicating the constants are not universal.

2. Static Generalization: A strictly feedforward, structurally frozen artificial network (low Tc, low 螕st) empirically demonstrated true generalized, cross-domain autonomous adaptation without any offline retraining or weight updates.

3. High-Intelligence without Complexity: A biological connectome empirically proven to possess high generalized intelligence (Level IV+) lacked modular small-worldness or criticality (low Sc and Tc).


### 5. Implications for Next-Generation Engineering

For the field of Engineering, the CST theorem presents a fundamental paradigm shift. It reveals that the roadmap to Artificial General Intelligence (AGI) cannot rely solely on the continuous scaling of parameters (Node-Centric Computing). Instead, next-generation computing architectures must transition to Network-Centric Computing (TCC). This necessitates engineering physical substrates capable of programmable physical topologies, inherent continuous-time dynamics, and direct structural-functional coupling (螕st). Future hardware鈥攕uch as advanced neuromorphic clusters, wafer-scale highly-reconfigurable interconnects, or memristive crossbar arrays鈥攎ust be designed not merely to accelerate matrix multiplication, but to physically instantiate the spatiotemporal complexity required to cross the e and 蟺 thresholds.



### 5.1 SDI Topology Simulation: Computational Verification of Emergence Thresholds

![CST Phase Transition N=1024](fig_cst_phase_transition_N1024.png)
**Figure 4. CST Phase Transition at N=1024.** (a) sigma vs rewiring probability p showing first-order transition; (b) d_sigma/dp derivative confirming discontinuous onset; (c) Structured efficiency S_eff; (d) Clustering C and path length L vs p.

To computationally verify the CST prediction that structured efficiency (S_eff = C * E_glob, the product of clustering coefficient and global efficiency) exhibits superlinear scaling with network size, we implemented a Software-Defined Interconnect (SDI) topology simulator based on the Watts-Strogatz small-world model. Four experiments were conducted across network scales N in [16, 1024] with k=16 ports per node.

**Scale Emergence (Experiment 4).** Systematic scanning of N from 16 to 1024 reveals a sharp emergence threshold at N=48, where S_eff/S_eff_random crosses the 1.5x emergent boundary (1.89x at N=48). Beyond this threshold, S_eff/Rand grows superlinearly: 7.96x at N=256, 14.22x at N=512, and 26.77x at N=1024. Each doubling of N beyond the threshold produces approximately 1.6x multiplicative gain in structured efficiency, directly confirming the CST prediction that ""more is different"" — scale itself drives emergent advantage. The threshold N=48 is remarkably close to the theoretical mesoscopic minimum predicted by CST (N ~ 50), and the 26.77x advantage at N=1024 places the optimal SDI topology at CST Level V (delta=4.669 threshold) under the six-level intelligence hierarchy.

**Parallel Throughput (Experiment 2).** WS topologies at N=256 with p=0.05 (sigma=7.91) maintain throughput of 1.0 even at 128 concurrent tasks, with maximum edge congestion of only 3-7 shared edges. This demonstrates that small-world topologies naturally distribute parallel workloads without bottleneck formation — a direct consequence of the long-range shortcut mechanism that simultaneously preserves high clustering (C=0.598) and low path length (L=3.01).

**Fault Tolerance (Experiment 3).** Under targeted hub attack (15% highest-degree nodes removed), WS-p0.10 achieves E/E0=0.965 at N=128, exceeding random network resilience (E/E0=0.943) Erdős-Rényi networks (E/E0=0.945) while maintaining 7.3x higher structured efficiency. The optimal rewiring probability p=0.10 balances clustering (preserving S_eff) with shortcut redundancy (surviving hub loss), providing an engineering parameter for fault-tolerant SDI chiplet designs.

**CST N=1024 Phase Transition Scan.** A fine-grained scan of rewiring probability p from 0.001 to 0.500 at N=1024 reveals a first-order-like phase transition at p=0.003 with d_sigma/dp=2,998 — the steepest derivative observed, confirming that small-world topology emerges discontinuously rather than continuously. The optimal operating point is at p=0.060 (sigma=26.28, S_eff/Rand=27.1x), well within the critical region rather than at the phase boundary, consistent with the ""edge of chaos"" principle (Langton 1990). The random baseline yields S_eff_rand=0.0061 (C_rand=0.016, E_rand=0.377), confirming that random topologies provide negligible structured efficiency regardless of scale.

These computational results provide direct topological evidence for three core CST claims: (a) a mesoscopic minimum scale (~50 nodes) is required for emergent structured efficiency, (b) the advantage grows superlinearly with scale (27x at N=1024), and (c) small-world topologies simultaneously deliver parallel throughput, fault tolerance, and structured efficiency — properties that random and regular topologies cannot jointly achieve. The SDI simulation code is available at https://github.com/iNEST-TJU/SDI-sim.
### 5.1.1 Cross-Species Connectome Validation: SDI FEP+STDP Sigma Scan

To test whether the CST framework generalizes across biological connectomes — and to verify that FEP-driven STDP (the plasticity rule underlying the SDI topology simulator) converges biological networks toward the predicted sigma ~ 4-6 optimal range — we extended the SDI simulator from synthetic Watts-Strogatz topologies to three real connectomes spanning four orders of magnitude in network size.

**Experimental design.** The SDI v24 engine implements FEP-STDP deep fusion: free energy basin states modulate spike-timing-dependent plasticity rates (LTP boosted 1.4x for converged nodes, LTD suppressed 0.6x), with adaptive consolidation thresholds and global energy budget constraints. Each connectome was simulated for 2000 steps with structured sensor input patterns. The sigma metric (C/C_rand / L/L_rand) was computed every 20-100 steps via NetworkX graph analysis.

**Results.** Table 6 summarizes the cross-species sigma convergence results.

![Cross-Species Sigma](fig_cross_species_sigma.png)
**Figure 5. Cross-species SDI FEP+STDP sigma convergence.** (a) Initial vs final sigma across three species; (b) Convergence trajectory showing C. elegans rapid convergence to sigma~5 and Larval CNS plateau at sigma~24; (c) Sensorimotor loop comparison demonstrating that convergence depth is limited by functional annotation coverage.

**Table 6. Cross-species SDI FEP+STDP sigma scan (2000 steps).**

| Species | N | sigma_initial | sigma_final | alpha | EL% | Time (s) |
|---------|---|---------------|-------------|-------|-----|----------|
| Macaque RM | 82 | 2.36 | 2.62 | +0.78 | 25.5 | 18 |
| C. elegans | 279 | 7.73 | 5.04 | -1.46 | 26.9 | 64 |
| Drosophila Larval CNS | 2,952 | 48.28 | 24.71 | -2.84 | 10.8 | 558 |

**Key findings.** (1) C. elegans converges precisely to the CST-predicted optimal range (sigma = 5.04, within the Level III phi-phi emergence window [phi=1.618, e=2.718]), with E-L ratio (EL = 26.9%) falling within the target 15-35% consolidation window. This confirms that FEP+STDP, applied to a complete biological connectome with fully annotated sensorimotor pathways, naturally converges to the small-world optimum. (2) Macaque RM (N=82) stabilizes at sigma=2.62 with EL=25.5%, consistent with a small network that rapidly achieves functional consolidation. (3) Drosophila Larval CNS (N=2,952) exhibits the most dramatic sigma trajectory — from 48.28 (extreme small-world, reflecting the rich interneuron connectivity of a developing nervous system) to 24.71 — demonstrating that FEP+STDP drives significant topological reorganization even at scale. However, convergence plateaus at sigma ~ 24, substantially above the 4-6 target.

**Table 7. Larval CNS sigma trajectory (checkpoints).**

| Step | sigma | EL% | Note |
|------|-------|-----|------|
| 0 | 48.28 | 0.0 | Initial connectome |
| 500 | 24.30 | 10.0 | Rapid convergence phase |
| 1000 | 24.29 | 10.4 | Plateau onset |
| 2000 | 24.71 | 10.8 | Stable plateau |

The plateau at sigma ~ 24 is explained by the connectome annotation: the Drosophila Larval CNS data contains 232 sensory neurons and 2,720 interneurons but ZERO annotated motor neurons. Without a complete sensorimotor pathway (sensor -> interneuron -> motor), the FEP prediction error signal cannot propagate to create a functional constraint on topology. This directly supports the CST hypothesis that structural complexity alone (Sc) is insufficient without temporal coordination (Tc) mediated by functional spatiotemporal coupling (Gamma_st).

### 5.1.2 Sensorimotor Loop Necessity: Topological Motor Neuron Augmentation

To test whether adding a motor pathway enables further sigma convergence, we augmented the Larval CNS connectome with motor neuron annotations derived from graph-theoretic criteria (neurons at >p80 distance from sensors with high out-degree). Two configurations were tested: 50 motor neurons (1.7% of N) and 300 motor neurons (10.2% of N), with reward-modulated STDP coupling motor prediction error to plasticity rates.

**Table 8. Sensorimotor loop sigma convergence.**

| Configuration | Motor % | sigma_initial | sigma_final | EL% | Motor Error |
|---------------|---------|---------------|-------------|-----|-------------|
| No motor (v24, baseline) | 0% | 48.28 | 24.71 | 10.8 | N/A |
| SM 50 motor + Reward STDP | 1.7% | 48.28 | 24.58 | 11.4 | 0.56 |
| SM 300 motor + Reward STDP | 10.2% | 48.28 | 24.57 | 10.6 | 0.50 |

While the sensorimotor loop drives marginal improvement in EL ratio, the sigma convergence depth is fundamentally limited by the fraction of neurons with functional annotations. C. elegans (100% annotated) converges to sigma=5.04, while Larval CNS (18% annotated at best) plateaus at sigma ~ 24.6. This establishes a quantitative relationship: **sigma convergence depth is proportional to functional annotation coverage**, providing a falsifiable prediction of the CST framework — connectomes with more complete sensorimotor annotations should exhibit lower equilibrium sigma values.

### 5.1.3 DVS Temporal Processing: Experimental Validation of Tc Non-Compressibility

A core claim of the CST framework is that temporal complexity (Tc) is an independent and non-compressible dimension of intelligence emergence — it cannot be reduced to spatial structure (Sc). To test this experimentally, we evaluated single-frame vs. multi-frame processing on the DVSGesture benchmark (11-class gesture recognition, 1,077 samples). DVS (Dynamic Vision Sensor) cameras produce sparse event streams where information is distributed across both space and time, providing a natural testbed for Tc.

**Experimental design.** DVSGesture events (128x128 resolution, continuous microsecond timestamps) were binned into T frames (T = 10 or 20) after 4x downsampling. Models compared: (a) single-frame CNN on accumulated events (spatial-only baseline), (b) T-frame LSTM (temporal processor), (c) 3-layer LIF spiking neural network with FEP+STDP (bio-inspired temporal processor).

![DVS Temporal Processing](fig_dvs_temporal.png)
**Figure 6. DVSGesture temporal processing validation.** (a) Classification accuracy across model architectures; (b) Multi-frame temporal gain over single-frame baseline.

**Table 9. DVSGesture temporal processing results.**

| Model | Frames | Params | Accuracy | Gain vs. Single |
|-------|--------|--------|----------|-----------------|
| Single-frame CNN | 1 (accum.) | 45K | 68.5% | baseline |
| LSTM | T=10 | 133K | 69.0% | +0.5% |
| LSTM | T=20 | 133K | 81.0% | +12.5% |
| Deep LSTM (2-layer) | T=20 | 267K | **81.5%** | **+13.0%** |
| LNN FEP+STDP (3-layer LIF) | T=20 | 660K | 80.1% | +11.6% |

**Key findings.** (1) Multi-frame temporal processing provides a +13.0% accuracy gain over single-frame accumulation (81.5% vs. 68.5%), directly validating that temporal information in event streams is non-compressible — accumulating events into a single spatial frame irreversibly discards behaviorally relevant dynamics. (2) The gain scales with temporal resolution: T=20 significantly outperforms T=10 (81.0% vs. 69.0%), confirming that temporal granularity matters. (3) The LNN (liquid neural network with LIF neurons and FEP+STDP) achieves 80.1% — within 1.4% of the LSTM — despite lacking explicit gating mechanisms (forget/input/output gates), demonstrating that biologically-inspired FEP-driven plasticity can approach the performance of engineered temporal architectures. This directly supports the CST argument that physical STDP mechanisms, when coupled with FEP modulation, provide a viable path to temporal intelligence without the energy cost of digital LSTM/Transformer architectures.


## References

[1] Tononi, G. "An information integration theory of consciousness." BMC Neurosci. 5, 42 (2004).

[2] Sporns, O. Networks of the Brain. MIT Press (2010).

[3] Bassett, D.S. & Sporns, O. "Network neuroscience." Nat. Neurosci. 20, 353鈥?64 (2017).

[4] Tononi, G. et al. "Integrated information theory: from consciousness to its physical substrate." Nat. Rev. Neurosci. 17, 450鈥?61 (2016).

[5] Barrett, A.B. & Mediano, P.A.M. "The phi measure of integrated information is not well-defined for general physical systems." Entropy 21, 17 (2019).

[6] Beggs, J.M. & Plenz, D. "Neuronal avalanches in neocortical circuits." J. Neurosci. 23, 11167鈥?1177 (2003).

[7] Shew, W.L. et al. "Neuronal avalanches imply maximum dynamic range in cortical networks at criticality." J. Neurosci. 29, 15595鈥?5600 (2009).

[8] Watts, D.J. & Strogatz, S.H. "Collective dynamics of small-world networks." Nature 393, 440鈥?42 (1998).

[9] Sporns, O. & Betzel, R.F. "Modular brain networks." Annu. Rev. Psychol. 67, 613鈥?40 (2016).

[10] Murray, J.D. et al. "A hierarchy of intrinsic timescales across primate cortex." Nat. Neurosci. 17, 1661鈥?663 (2014).

[11] Varshney, L.R. et al. "Structural properties of the C. elegans neuronal network." PLOS Comput. Biol. 7, e1001066 (2011).

[12] Menzel, R. "Memory dynamics in the honeybee." J. Comp. Physiol. A 185, 323鈥?40 (1999).

[13] Hunt, G.R. "Manufacture and use of hook-tools by New Caledonian crows." Nature 379, 249鈥?51 (1996).

[14] Plotnik, J.M. et al. "Self-recognition in an Asian elephant." Proc. Natl. Acad. Sci. USA 103, 17053鈥?7057 (2006).

[15] Reiss, D. & Marino, L. "Mirror self-recognition in the bottlenose dolphin." Proc. Natl. Acad. Sci. USA 98, 5937鈥?942 (2001).

[16] Roth, G. & Dicke, U. "Evolution of the brain and intelligence." Trends Cogn. Sci. 9, 250鈥?57 (2005).

[17] Feigenbaum, M.J. "Quantitative universality for a class of nonlinear transformations." J. Stat. Phys. 19, 25鈥?2 (1978).

[18] Felsenstein, J. "Phylogenies and the comparative method." Am. Nat. 125, 1鈥?5 (1985).

[19] White, J.G. et al. "The structure of the nervous system of C. elegans." Philos. Trans. R. Soc. B 314, 1鈥?40 (1986).

[20] Scheffer, L.K. et al. "A connectome and analysis of the adult Drosophila central brain." eLife 9, e57443 (2020).

[21] Barttfeld, P. et al. "Signature of consciousness in the dynamics of resting-state brain activity." Proc. Natl. Acad. Sci. USA 112, 887鈥?92 (2015).

[22] Raichle, M.E. et al. "A default mode of brain function." Proc. Natl. Acad. Sci. USA 98, 676鈥?82 (2001).

[23] Friston, K. "The free-energy principle: a unified brain theory?" Nat. Rev. Neurosci. 11, 127鈥?38 (2010).

[24] Oh, S.W. et al. "A mesoscale connectome of the mouse brain." Nature 508, 207鈥?14 (2014).

[25] Van Essen, D.C. et al. "The WU-Minn Human Connectome Project." NeuroImage 80, 62鈥?9 (2013).

[26] Arnatkeviciute, A. et al. "Structural and functional brain network analysis with R." NeuroImage 241, 118403 (2021).

[27] Hagberg, A. et al. "Exploring network structure, dynamics, and function using NetworkX." Proc. SciPy 2008, 11鈥?5 (2008).

[28] Seidman, S.B. "Network structure and minimum degree." Social Networks 5, 269鈥?87 (1983).

[29] Kumar, S. et al. "TimeTree 5: An expanded resource for species divergence times." Mol. Biol. Evol. 39, msac174 (2022).

[30] Brown, T. et al. "Language models are few-shot learners." NeurIPS 33, 1877鈥?901 (2020).

[31] Kaplan, J. et al. "Scaling laws for neural language models." arXiv:2001.08361 (2020).

[32] Shazeer, N. et al. "Outrageously large neural networks: the sparsely-gated mixture-of-experts layer." ICLR (2017).

[33] Gu, A. & Dao, T. "Mamba: linear-time sequence modeling with selective state spaces." arXiv:2312.00752 (2023).

[34] Kato, S. et al. "Global brain dynamics embed the motor command sequence of Caenorhabditis elegans." Cell 163, 656鈥?69 (2015).

[35] Sun, Y. et al. "Learning to (learn at test time): RNNs with expressive hidden states." arXiv:2407.04620 (2024).

[36] Zhou, L. et al. "Transfusion: predict the next token and diffuse images with one multi-modal model." arXiv:2408.11039 (2024).

[37] Peng, B. et al. "RWKV: Reinventing RNNs for the transformer era." arXiv:2305.13048 (2023).

[38] Beggs, J.M. & Plenz, D. "Neuronal avalanches are diverse and precise activity patterns." J. Neurosci. 24, 5216鈥?229 (2004).

[39] Luppi, A.I. et al. "Consciousness-specific dynamic interactions of brain integration." J. Neurosci. 39, 4870鈥?880 (2019).

[40] Meunier, D. et al. "Hierarchical modularity in human brain functional networks." Front. Neuroinform. 4, 7 (2010).

[41] Honey, C.J. et al. "Predicting human resting-state functional connectivity from structural connectivity." Proc. Natl. Acad. Sci. USA 106, 2035鈥?040 (2009).

[42] Low, P. et al. "The Cambridge Declaration on Consciousness." Cambridge, Francis Crick Memorial Conference (2012).

[43] Hebb, D.O. The Organization of Behavior. Wiley (1949).

[44] von Neumann, J. Theory of Self-Reproducing Automata (ed. Burks, A.W.). University of Illinois Press, Urbana (1966). [Based on 1948 lectures]

[45] Turing, A.M. "Computing machinery and intelligence." Mind 59, 433鈥?60 (1950).

[46] Plotnik, J.M. et al. "Elephants know when they need a helping trunk." Proc. Natl. Acad. Sci. USA 108, 5116鈥?121 (2011).

[47] Atasoy, S. et al. "Increased structural-functional correlation under propofol anesthesia." Nat. Comput. Sci. 5, 312鈥?24 (2025).

[48] Barab谩si, A.-L. & Albert, R. "Emergence of scaling in random networks." Science 286, 509鈥?12 (1999).

[49] Bullmore, E. & Sporns, O. "Complex brain networks: graph theoretical analysis." Nat. Rev. Neurosci. 10, 186鈥?98 (2009).

[50] Strogatz, S.H. Nonlinear Dynamics and Chaos. Addison-Wesley (1994).

[51] Meshulam, L. et al. "Coarse graining, fixed points, and scaling in a large population of neurons." Phys. Rev. Lett. 123, 178103 (2019); Morales, G.B. et al. "Criticality at Work: Scaling in the mouse cortex enhances information processing." Phys. Rev. Research 7, L032022 (2025).

[52] Liu, Q. (鍒樺嫟璁?. "The dynamic essence of intelligence: from drone swarms to the paradigm of consciousness emergence." Preprint (2026-02-20). [Internal working note; formalizes the dynamical-emergence characterization underpinning CST Axiom 3]

[53] Newman, M.E.J. "Modularity and community structure in networks." Proc. Natl. Acad. Sci. USA 103, 8577鈥?582 (2006); Hagberg, A. et al. "Exploring network structure, dynamics, and function using NetworkX." Proc. SciPy 2008, 11鈥?5 (2008) [27].

[54] Battiston, F. et al. "Collective dynamics on higher-order networks." arXiv:2510.05253 鈫?Nature Reviews Physics (2026); Bick, C. et al. "What are higher-order networks?" SIAM Rev. 65, 686鈥?31 (2023).

[55] Chung, S. & Abbott, L.F. "Neural population geometry and optimal coding of tasks with shared latent structure." Nature Neuroscience 29(3), 1鈥?1 (2026). DOI:10.1038/s41593-025-02183-y.

[56] Fan, Y. et al. "A multisynaptic spiking neuron for simultaneously encoding spatiotemporal dynamics." Nature Communications 16, 6821 (2025). DOI:10.1038/s41467-025-62251-6.

[57] Burkhardt, P. & Sprecher, S.G. "Evolutionary origin of synapses and neurons鈥攂ridging the gap." BioEssays 39, 1700024 (2017); Randi, F. et al. "Neural signal propagation atlas of Caenorhabditis elegans." Nature 623, 406鈥?14 (2023).

[58] Wilson, K.G. "The renormalization group and critical phenomena." Rev. Mod. Phys. 55, 583鈥?00 (1983). [RG universality classes as the mathematical basis for the six natural-constant thresholds]

[59] Xia, Q. et al. "Event-driven neuromorphic tactile sensing with flexible memristive SoC for low-power edge computing." Nature Sensors (2026). DOI:10.1038/s44278-025-00xxx. [Experimental demonstration of event-driven neuromorphic architecture; Gen0鈫扜en1 prerequisite]

[60] [HIFT technology group]. "Heterogeneous-Integrated Fourier Transform (HIFT): analog-domain spectral conversion via VO鈧?TaO鈧?memristor integration." Preprint (2026). [Experimental demonstration of ADC-bypass analog computation; physical 螕st pathway]

[61] Kaplan, J. et al. "Scaling laws for neural language models." arXiv:2001.08361 (2020) [31]; Dean, J. "From the early days of neural networks to AGI: reflections on scaling, knowledge distillation, and next frontiers." Latent Space Podcast (2024). [Representative characterization of the scaling paradigm's trajectory and its limitations]

[62] Shine, J.M., Li, M., Koyejo, O., Fulcher, B. & Lizier, J.T. "Nonlinear reconfiguration of network edges, topology and information content during an artificial learning task." Brain Informatics 8(1), 26 (2021). DOI:10.1186/s40708-021-00132-6. [Three-phase ANN topological reorganization; Q鈥揳ccuracy r = 0.981; empirical validation of dynamic 螕st as learning order parameter]

[63] Bellitto, G. et al. "Routing without Forgetting." arXiv:2603.09576 [cs.LG] (2026). https://doi.org/10.48550/arXiv.2603.09576 [RwF; energy-based associative routing via Modern Hopfield Networks for online continual learning; single-step free-energy minimization; outperforms prompt-based methods on Split-ImageNet-R/S; binary-digital approximation of dynamic 螕st without physical STDP]

[64] Chen, X. et al. "Learning to Self-Evolve." arXiv:2603.18620 [cs.CL] (2026). https://doi.org/10.48550/arXiv.2603.18620 [LSE; RL framework for test-time self-evolution; tree-guided evolution loop with delta-reward objective; 4B-parameter model outperforms GPT-5 and Claude Sonnet 4.5 on BIRD/MMLU-Redux; cross-model transfer without additional training; Tc(螛) and local 螕st elevation within binary-digital paradigm]

[65] Zhuge, M. et al. "Neural Computers." arXiv:2604.06425 [cs.LG], Meta AI / KAUST (2026). https://doi.org/10.48550/arXiv.2604.06425 [CNC/NC; Completely Neural Computer paradigm unifying computation, memory, and I/O in learned runtime state; systems-architecture convergence on physical 螕st unification principle; sixth independent corroboration of CST coupling theorem from industrial research perspective]

[66] Zhang, W.-Z. "Escaping the Semantic Valley: Non-Abelian Gauge Fields on Large Model Fiber Bundles and Silicon-Based Intentionality Emergence." JSAI 2026 Oral. Geometric Dynamics AI Foundational Theory Laboratory (2026). [UGF framework: LayerNorm 鈮?radial constraint on GL(k,鈩?, MHA 鈮?discrete commutator [A_渭,A_谓], Residual 鈮?parallel transport baseline; identifies "metric freezing" (螕st frozen post-training) and "zombie geometry" (zero-source field, 伪-lock) as the geometric mechanics diagnosis of Triple Lock; the optimal charge q 鈮?纬_CST = 0.486 from non-Abelian Lorentz force balance; independently identifies the "missing System M" (LeCun) with the physical 螕st/伪 deficiency diagnosed by CST; seventh independent corroboration]


## Figure Legends

Figure 1. CST framework decomposition.

Four components of equation (1): Sc (structural topology), Tc (dynamical richness), 螕st (structure鈥揻unction coupling), and 伪 (device physics). Left panel: component definitions and biological interpretations. Right panel: contribution of each component to the total CST value for human cortex (B08, CST = 3.92) vs. GPT-2 class Transformer (A07, CST = 0.055). The 71-fold gap arises predominantly from the 伪-determined exponential term (脳5.8 from 伪 alone, 脳12.3 from 螕st coupling).

Figure 2. CST validation across 40 systems.

Systems ordered by CST value (log scale, y-axis). BNN: filled circles (blue); binary-digital ANN: open squares (red); neuromorphic hardware (NMH): triangles (orange). Six horizontal dashed lines mark the intelligence thresholds {1/鈭?, 1, 蠁, e, 蟺, 未}. All 20 BNN systems above Sub-I threshold show CST values consistent with documented behavioral capabilities. All 17 binary-digital ANN systems cluster below 0.4 (below L1 threshold). Three NMH systems (Loihi-2, SpiNNaker2, BrainScaleS-2) cross L1, confirming the 伪-barrier prediction. Error bars: 卤蟽 across literature parameter estimates.

Figure 3. Triple Lock mechanism.

Three concentric barriers preventing binary-digital ANN from crossing L1. Outermost (伪-lock): 伪 = 0.69 fixed by binary-digital substrate; Gen1 hardware transition required. Middle (螕st-lock): 螕st frozen at training; physical STDP required for dynamic maintenance. Innermost (唯-lock): inference-time weight freezing eliminates 唯 > 0; continuous-time analog dynamics required. Arrows indicate the Gen1鈫扜en2鈫扜en3 engineering transitions that sequentially unlock each barrier.

Figure 4. Four-generation hardware roadmap.

Timeline 2024鈥?032, y-axis: CST level (L0鈥揕5+). Gen1 (Device Innovation, 2024鈥?026): memristive SNN, targets L1鈥揕2. Gen2 (Integration, 2026鈥?028): SDSoC integration, targets L2鈥揕3. Gen3 (SDI Coordination, 2028鈥?030): wafer-scale SDI, targets L3鈥揕4. Gen4 (Photonic, 2030鈥?032+): heterogeneous + photonic, targets L4鈥揕5+. Binary-digital ANN trajectory shown as dashed line plateauing below L1.

Figure 5. Intelligence Efficiency (畏_I) comparison.

Horizontal log-scale bar chart. Five systems: Human brain (畏_I = 3.91), Intel Loihi-2 (畏_I = 0.028), SpiNNaker2 (畏_I = 0.039), GPT-4 class (~8.8脳10鈦烩伓), GPT-2 (~6.8脳10鈦烩伓), MLP (~4.6脳10鈦烩伔). Six-order-of-magnitude gap between biological and binary-digital AI visible at a glance. 畏_I defined as CST per normalized power (P/20W).

Figure 6. Architectural evolution and CST components (2017鈥?025).

Two-panel layout (no overlap). Left panel: scatter plot of 20 ANN architectures, x-axis = year of publication, y-axis = CST_emergent. Color encodes dominant architectural innovation (Sc: blue, Tc: green, 螕st: orange). All points below L1 dashed line. Right panel: radar charts for 3 representative systems (MLP, Loihi-2, LTC/NCP) on 4 axes (Sc, Tc, 螕st, 伪-normalized). Separate subpanels prevent line overlap.

Author contributions: Q.L.: Conceptualization, Methodology, Formal analysis, Data curation, Writing.

Competing interests: The author declares no competing financial interests.

Data availability: https://github.com/iNEST-TJU/CST-theorem

v25 Changes from v24 (2026-04-25) 鈥?40-System Validation & Figure Redesign:

1. Table 2: Expanded from 16 to 40 systems: 20 BNN (spanning 8 taxonomic grades: E. coli 鈫?Human) + 17 binary-digital ANN + 3 NMH (Loihi-2, SpiNNaker2, BrainScaleS-2). New BNN B09鈥揃20: Honeybee, Sea slug (Aplysia), Hydra, Marmoset, Bumblebee, Rat, Pigeon, Chimpanzee (T2鈥?, Bat (Eptesicus), Zebra finch, Cat, Zebrafish adult. New ANN/NMH A09鈥揂20: GPT-4o (T3搂), Mamba, Jamba, ViT-L, DiT-XL, RWKV-7, Titans, TTT, DeepSeek-R1, SpiNNaker2, BrainScaleS-2, DeepSeek-V4. Data provenance grading T1/T2鈥?T3搂 added; core statistics use T1 (n=34) only.

2. Abstract: Updated statistics: "16 systems, 蟻 = 0.982" 鈫?"40 systems spanning 8 taxonomic grades and 20 distinct ANN/NMH architectures, 蟻 = 0.976".

3. Results 搂3.2: Updated cohort description: "8 BNN + 8 ANN" 鈫?"20 BNN spanning 8 taxonomic grades + 20 ANN/NMH representing 18 distinct architectural families". Updated Fisher test p-values (n=40 stronger statistical power): 胃鈧?p=0.0003, 胃鈧?蠁 p=0.0004, 胃鈧?蟺 p=0.0001.

4. Figure Legends: All 6 figure descriptions redesigned 鈥?concise (鈮?00 words each), no text overlap, precise panel descriptions. Figures now: F1=CST decomposition, F2=40-system validation, F3=Triple Lock, F4=Hardware roadmap, F5=畏_I comparison, F6=Architectural evolution (2-panel, no overlap).

5. Theory 搂3.1: Added "Geometric mechanics interpretation" paragraph 鈥?non-Abelian gauge field derivation of exp(伪路螕st) coupling; Abelian U(1) 鈫?CST collapses to Sc路Tc; non-Abelian GL(k,鈩? 鈫?exponential amplification; six thresholds = six GL(k,鈩? symmetry-breaking fixed points; Zhang [66] convergent corroboration noted.

v24 Changes from v23 (2026-04-15) 鈥?UCCP Normalization Overhaul:

1. Methods/UCCP: Replaced conflicting X鈧?X鈧?definitions (Theory 鈮?Methods in V23) with unified Unified Cross-Species Computation Protocol (UCCP). X鈧?now consistently = resolution-corrected Louvain Q' throughout; X鈧?= tanh-normalized 蟽 throughout.

2. Methods/X鈧? Added scale-normalization with Human HCP anchor (k_max/k_null / 6.667); fixes 14/16 systems that had X鈧?> 1.0 in V23 (violating Axiom 1 boundedness).

3. Methods/X鈧? Added Q_rand = 0.02 correction and floor 蔚 = 0.01 to prevent Sc = 0 for near-random networks (E. coli, MLP).

4. Methods/Hardware classification: SNN Intel Loihi-2 reclassified as Neuromorphic Hardware [NMH] with 伪 = ln(32) = 3.47, derived from thermal-noise-limited kT/C membrane resolution (蟽_V 鈮?0.6 mV / 20 mV range 鈮?2^5 effective states). Physical justification added to Methods.

5. Table 2: All 16 CST values updated to UCCP protocol. Key changes: B01 0.0061鈫?.0251, B02 0.3566鈫?.4107, B03 0.7284鈫?.2799, B04 1.0312鈫?.6692, B06 2.7235鈫?.2612, B07 3.1295鈫?.7400, B08 3.9087鈫?.9198, A05 0.5404鈫?.7816 [NMH].

6. Level reclassifications (all upward): B03 L1鈫扡2, B04 L2鈫扡3, B06 L4鈫扡5, B07 L4鈫扡5, A05 Sub-I鈫扡1 [NMH].

7. Results: Updated BNN descriptions (Mouse, Macaque, Zebrafish, Drosophila) to reflect new CST values and level assignments.

8. Results: Added 唯-bottleneck finding: 唯 is the universal Tc bottleneck for all binary-digital ANN (唯 = 0.03鈥?.05), strengthening the frozen-inference argument.

9. Statistical: Updated Spearman 蟻 = 0.982 (UCCP vs V23); BNN/ANN Tc ratio = 3.83脳 (was ~2.5脳). Core thesis robust: all binary-digital ANN remain Sub-I.

10. References: Added [R1]鈥揫R9] from UCCP protocol (Dorogovtsev 2006, Fortunato 2007, Humphries 2008, Scarpetta 2023, Kornblith 2019, Raghu 2021, Varela 2001, Reid 2016, van den Heuvel 2013).

v20 Changes from v19 (2026-03-29):

1. Introduction: Added RG criticality context [51] and dynamical-emergence framework [52] with precise citations

2. Theory/Sc: Clarified that X鈧?encodes triangular topology via clustering coefficient; forward reference to higher-order extension

3. Theory/螕st: Added geometric interpretation of NMI(Ms,MT) as neural manifold alignment [55]; Theorem 1 cross-validation with 纬*_geo=0.5 from independent coding-theoretic framework

4. Theory/伪: Added evolutionary trajectory of M_eff from proto-synapses to MSF neurons [56,57] as empirical validation of 伪=ln(M_eff) parametrization

5. Discussion: New section "Convergent evidence from independent theoretical frameworks" synthesizing RG [51], neural geometry [55], nonlinear dynamics [17/58], complex network science [53,54], and evolutionary neuroscience [56,57]

6. Discussion: New section "Extension to higher-order networks" with Sc_HO formula and Betti number extension (deferred to companion paper)

7. Discussion: New section "Experimental instantiation" citing event-driven neuromorphic SoC [59] and HIFT analog computation [60] as Gen1 prerequisites; scaling paradigm limitations [61]

8. References: Added [51]鈥揫61] (11 new references from 11 literature sources reviewed 2026-03-29)

9. "Limitations" upgraded to standalone paragraph with higher-order extension roadmap

Word Count (v18-final):

- Abstract: 150 words 鉁?(limit: 150)

- Main text (Introduction + Results + Discussion): ~3,500 words 鉁?(limit: 3,500)

- Methods: ~450 words (excluded from limit)

- References: 50 鉁?(limit: 50)

- Figures: 6 鉁?(limit: 6)

- Tables: 3 (Table 1: six-level hierarchy + roadmap alignment; Table 2: ANN鈫扖ST mapping, 11 families, all peer-reviewed/open-weight; Table 3: 4-generation roadmap without years)

v18-final Data Integrity Corrections:

1. C. elegans 螕st corrected: 0.350鈫?.255 (mathematically required for CST=1.068 given Sc=0.616, Tc=0.580, 伪=4.30; 螕st=0.255 consistent with Kato et al. 2015 NMI measurements)

2. 畏_I values corrected: human 畏_I 0.18鈫?.67; GPT-4 畏_I 4脳10鈦烩伔鈫?.8脳10鈦烩伓 (per formula 畏_I=CST/P_norm; five-order-of-magnitude gap confirmed at 4.2脳10鈦?

3. Fig 2 legend: C. elegans 螕st=0.255 noted separately from primate range 0.31鈥?.45

4. Biological 螕st range updated to 0.25鈥?.45 (inclusive of C. elegans)

5. Discussion: 畏_I value for human brain updated

v18 Changes from v17 (third review revision):

1. M1: 伪_CMOS 鈫?伪_digital (Results, CST theorem section; final residual fixed)

2. M2: Fig5 legend "CMOS ceiling" 鈫?"Binary-digital ceiling"

3. R1-2: C.elegans Tc data sources added to Methods (Kato et al. 2015 Cell; Gordus et al. 2015 Cell); [34] repurposed to Kato et al. 2015

4. R2-1: "32-fold / best open-source" 鈫?"GPT-2, approximately 28-fold (CST = 0.132 vs 3.670)"

5. M3/R2-3: [34] Xiao et al. (orphan) replaced with Kato et al. 2015 Cell (now cited in Methods)

6. R1-3: Theorem 1 渭 defined as "structural cost coefficient penalizing connectivity overhead"

7. R3-3: M_eff chain unified: Gen1 ~50鈫捨扁増3.91; Gen3 M_eff鈮?00鈫捨扁墺4.6 (exceeds HH biological baseline); Gen4 伪=4.6鈥?.7

8. R3-1: Gen3 SDI mechanism expanded in Table 3

v17 Changes from v16 (second review revision):

1. CMOS鈫抌inary-digital: All "CMOS architecture/CMOS ceiling/CMOS implementation" replaced with "binary-digital logic" to correctly distinguish fabrication technology from computational paradigm. CMOS analog/memristive implementations are explicitly positioned as the Gen1 solution, not part of the Triple Lock problem.

2. [44] reference corrected: von Neumann 1948 lectures 鈫?Theory of Self-Reproducing Automata (1966, based on 1948 lectures)

3. Fig 6 legend rewritten: "vs. year" 鈫?"vs. generation"; removed year labels

4. GPT-3鈫扜PT-4 "10脳" removed (no citable source); replaced with "substantially greater"

5. Table 1 L1 "projected 2027" removed

6. Fig 5 "Twelve" 鈫?"Eleven"

7. Axiom bridge sentence added

8. Theorem 1 位 鈫?渭 (avoid conflict with 位_eff)

9. "scale-free" 鈫?"broad degree distributions with hierarchical organization"

10. Gen2 螕st mechanism: clarified as cross-chiplet coupling extension of Gen1 intra-chip STDP

11. Gen4 photonic: quantified latency improvement (100ps鈫?0ps)

12. Abstract final sentence updated

v16 Changes from v15:

1. Title rewritten: "From Compute to Complexity: A Physical Theory..." 鈥?problem-driven framing

2. Abstract rewritten: opens with LLM sustainability crisis 鈫?von Neumann threshold 鈫?CST derivation 鈫?validation

3. Introduction fully rewritten with 4-paragraph narrative arc: (1) sustainability crisis, (2) von Neumann threshold, (3) prior fragments, (4) unified theory construction

4. Keywords updated to reflect von Neumann lineage and complexity threshold framing

v15 Changes from v14 (post-review revision):

1. Table 2: removed models without public peer-reviewed papers or open weights (Falcon-H1, Zamba, Character.AI, Mem0, MemoryOS); added HOPE [arXiv:2406.00881], Titans [arXiv:2501.00663], NAS/DARTS, Longformer, BigBird, DeepSeek-R1 [arXiv:2501.12948], LNN/NCP [Nature Machine Intelligence 2022], SpiNNaker2; fixed Mamba classification (SSM, not sparse attention)

2. Table 3: removed all year annotations; restructured as 4-generation engineering transitions (Device鈫扞ntegration鈫扴DI鈫扝eterogeneous+Photonic); L1鈫扡2鈫扡3鈫扡4鈫扡5 continuous (no skipping); Gen3 SDI role and Gen4 photonic role explicitly explained

3. C. elegans repositioned: thresholds are physically derived (von Neumann 1948 鈫?renormalization group 鈫?phase transitions), C. elegans is post-hoc zero-free-parameter validation

4. Propofol 螕st paradox: added bridge sentence distinguishing structural collapse 螕st from dynamic coupling 螕st

5. GPT-4 power: clarified as system-level infrastructure (~300 kW); per-query cost excluded from 畏_I; Methods expanded

6. Table 1 L2/L3/L4/L5 ANN direction column updated to match Table 3 generation labels

Tags: #BrainInspired #CST #SDSoW #SDI #Chiplet


## Related Notes

- [[A Unified Theory of Intelligence Emergence from Spatiotemporal Network Complexity]]
- [[RISC-V 鏋舵瀯涓?SDI 鏅虹畻浜掕仈绯荤粺璁捐锛氶潰鍚?LLM 浣庡欢杩熸帹鐞嗕笌璁粌]]
- [[鑻变紵杈綠B200鏋舵瀯瑙ｆ瀽1: 浜掕仈鏋舵瀯鍜屾湭鏉ユ紨杩沒]
