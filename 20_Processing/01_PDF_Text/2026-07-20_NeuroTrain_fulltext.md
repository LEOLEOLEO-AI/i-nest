---
title: "NeuroTrain: Surveying Local Learning Rules for Spiking Neural Networks with an Open Benchmarking Framework"
source_pdf: "[[2605.15058v1.pdf]]"
source_url: "https://arxiv.org/abs/2605.15058"
pdf_sha256: "d9f19500ee47dd2b28412c4a48f67378acef3b94d92589910514215dd82333f7"
pages: 28
text_status: extracted
analysis_status: pending_fulltext_review
ingested: "2026-07-19T16:31:38"
---

# NeuroTrain: Surveying Local Learning Rules for Spiking Neural Networks with an Open Benchmarking Framework - Full Text


--- PAGE 1 ---

NeuroTrain: Surveying Local Learning Rules for Spiking Neural Networks with an Open
Benchmarking Framework
Alessio Cavigliaa,∗, Filippo Marosticaa, Roberta Bardinia, Alessandro Savinoa, Stefano Di Carloa
aPolitecnico di Torino, Control and Computer Engineering Department, Corso Duca degli Abruzzi 24, Torino, I-10129, , Italy
Abstract
The rapid expansion of spiking neural networks (SNNs) has led to a proliferation of training algorithms that differ widely in bio-
logical inspiration, computational structure, and hardware suitability. Despite this progress, the field lacks a unified, fine-grained
taxonomy that systematically organizes these approaches and clarifies their conceptual relationships. This survey provides a com-
prehensive taxonomy of SNN training algorithms, spanning surrogate-gradient backpropagation, local and three-factor learning
rules, biologically inspired plasticity mechanisms, ANN-to-SNN conversion pipelines, and non-standard optimization strategies.
We analyze each class in terms of its computational principles, learning signals, and locality properties. To support reproducible re-
search, we release NeuroTrain, an open-source snnTorch-based framework that implements a representative set of these algorithms
within a unified, modular, and extendable framework, enabling consistent benchmarking across datasets, architectures, and training
regimes. By consolidating fragmented literature and providing a reusable benchmarking framework, this survey identifies common
patterns, highlights open challenges, and outlines promising directions for future work on scalable, efficient SNN training.
Keywords:spiking neural networks, local training, neuromorphic computing
1. Introduction
Spiking Neural Networks (SNNs) are event-driven neural
networks in which information is represented and processed
through spikes [1]. SNNs incorporate temporal dynamics and
can exploit sparse activity, i.e., computation is triggered only
when events occur. This enables low-latency processing and
the potential for substantial energy savings when deployed on
neuromorphic hardware [2]. These properties make SNNs at-
tractive for edge and always-on sensing scenarios, where power,
bandwidth, and response time are often the dominant con-
straints. Beyond their relevance to neuromorphic hardware,
they also provide a theoretically grounded setting for studying
computation under constraints that closely resemble those of
biological neural systems [3].
The main obstacle to widespread adoption of SNNs, how-
ever, remainstraining: while forward simulation is straightfor-
ward, assigning credit for errors through discontinuous spike
events and temporal dynamics is substantially more complex
than in other Artificial Neural Networks (ANNs). Training
SNNs is challenging for at least three intertwined reasons.
First, spike generation is non-differentiable, making gradient-
based optimization non-trivial and requiring approximations
(e.g., surrogate gradients). Second, information is carried over
∗Corresponding author
Email addresses:alessio.caviglia@polito.it(Alessio Caviglia),
filippo.marostica@polito.it(Filippo Marostica),
roberta.bardini@polito.it(Roberta Bardini),
alessandro.savino@polito.it(Alessandro Savino),
stefano.dicarlo@polito.it(Stefano Di Carlo)
time through membrane and synaptic state variables, so learn-
ing must address temporal credit assignment across many time
steps. Third, implementations face substantial computational
and memory costs: methods that rely on global backpropa-
gation through time can be accurate but expensive, and they
map poorly onto distributed neuromorphic hardware where cen-
tralized memory access and global error transport are unde-
sirable. These difficulties have catalyzed a large and rapidly
growing body of work on SNN learning, spanning direct train-
ing, conversion pipelines, and alternative optimization strate-
gies. This survey focuses ondirect trainingmethods, which
train SNNs by explicitly modeling their temporal dynamics and
spike-generation processes during optimization, rather than re-
lying on ANN to SNN conversion.
Within direct training,localityis often highlighted as a defin-
ing characteristic. Broadly, locality concerns the availability of
the information required to compute learning updates:temporal
locality refers to updates that can be computed from quantities
available at the current timestep. In contrast,spatiallocality
refers to updates that depend on signals available locally at the
synapse. Locality reduces global communication and memory
pressure and aligns well with low-power neuromorphic hard-
ware and online adaptation, yet relaxing locality often improves
training performance on challenging benchmarks. A key goal
of this survey is to discuss these trade-offs and provide instru-
ments for comparison across methods.
Several surveys in recent years have provided valuable
overviews of SNN training, spanning direct training methods,
conversion pipelines, and other approaches (see section 3).
However, the pace at which new algorithms appear makes the
arXiv:2605.15058v1  [cs.NE]  14 May 2026

--- PAGE 2 ---

landscape difficult to track, and, perhaps more importantly,fair
comparison remains hard. Existing surveys are primarily de-
scriptive: they synthesize ideas and trends, but typically cannot
provide standardized, side-by-side evaluations because meth-
ods live in heterogeneous codebases with differing datasets,
preprocessing pipelines, architectures, optimization details, and
reporting conventions. As a result, it is often difficult to dis-
entangle algorithmic contributions from experimental choices,
and readers may come away with a rich qualitative map of ap-
proaches but a weaker sense ofwhichdesign decisions matter
most under controlled, unified conditions.
In this work, we address this gap by considering thebench-
markingas a key contribution, paired with a taxonomy that or-
ganizes the literature along explicit axes of variation, i.e.,train-
ing strategy,supervision, andlocality. While we cover the ma-
jor training paradigms, we place particular emphasis on direct
training, where the design space is richest, and locality con-
straints most directly shape both algorithmic structure and hard-
ware suitability. Concretely, our contributions are twofold: (i) a
unified taxonomy-driven review of SNN training methods; and
(ii)NeuroTrain, an open, extensible experimental framework
that enables reproducible implementations and comparisons of
SNN training algorithms under shared experimental conditions.
Beyond enabling replication,NeuroTrainis designed to lower
the barrier to integrating new algorithms by providing a com-
mon suite of reference models and pipelines for testing them.
In this sense, the present work goes beyond a conventional sur-
vey: it introduces reusable benchmarking tools to support more
rigorous, cumulative progress in this rapidly evolving field.
The remainder of the article is structured as follows. Sec-
tion 2 introduces the background required to understand the
SNN training challenges. Section 3 reviews related surveys
on SNNs training. Section 4 presents the proposed taxonomy.
Section 5 describes the benchmarking framework, experimen-
tal design, and results. Finally, Section 6 concludes the article
and outlines future research directions.
2. Background
SNNs are a class of neural models in which information
is represented and processed through discrete spikes evolving
over continuous or discretized time [1]. By explicitly mod-
eling neuronal dynamics over time, SNNs differ fundamen-
tally from conventional ANNs, which generally abstract neu-
rons as static input–output units rather than temporally evolv-
ing, spike-emitting systems. This event-driven formulation has
made SNNs particularly relevant to neuromorphic computing,
where sparse activity and asynchronous computation can be ex-
ploited to achieve low-latency, energy-efficient processing. At
the same time, these same properties make SNNs substantially
more difficult to train. This section establishes the minimal
conceptual framework for understanding the challenges of SNN
training.
2.1. Spiking computation and neuronal dynamics
Biological neurons communicate through action potentials
and integrate synaptic inputs over time before producing an
output spike (Figure 1). Incoming signals from differentloca-
tionsarriving at differenttimesare accumulated into an evolv-
ing membrane potential, and a spike is emitted once this state
crosses a threshold, typically followed by reset and refractori-
ness. Spiking neuron models used in SNNs, such as the Leaky
Integrate and Fire (LIF) model, abstract these mechanisms into
low-dimensional dynamical systems that preserve the key com-
putational ingredients of spatio-temporal integration, thresh-
olded event generation, and post-spike reset [3, 4].
This formulation endows SNNs with a computational regime
in which information may be carried not only by activation
magnitude, but also by spike timing and temporal structure.
Such temporal expressivity is one of the principal motiva-
tions for using SNNs, especially in domains involving streams,
events, or dynamical signals. However, it also introduces a
central optimization difficulty that impedes training these net-
works.
Figure 1: Biological neuron behavior. Spatiotemporal integration and action
potential dynamics at the single neuron.
2.2. Why training SNNs is challenging
The training of SNNs is difficult for several interconnected
reasons. First, the binary and threshold-based nature of spike
emission prevents the direct application of standard gradient-
based optimization in its usual form [5]. Moreover, because
SNNs are dynamical systems, parameter updates must often ac-
count for how present outputs depend on earlier hidden states
and past inputs [6]. Eventually, the sparse, event-driven na-
ture of spiking activity can make optimization unstable or in-
efficient, particularly when useful supervisory information is
weak, delayed, or distributed over time [7].
These challenges have given rise to a broad range of learning
strategies. Some methods avoid direct optimization of spik-
ing dynamics by transferring knowledge from rate-based or
non-spiking models. In contrast, others train spiking networks
directly by explicitly accounting for their temporal behavior.
Within this landscape, a particularly important distinction con-
cerns the nature of the information required to compute synap-
tic updates. Some methods rely on global error signals prop-
agated across layers and over time, whereas others construct
2

--- PAGE 3 ---

updates using only locally available signals within the network.
The latter class is especially relevant to this survey.
2.3. Locality as a principle of biological plasticity
A central feature of biological learning is that synaptic and
neuronal changes are driven predominantly by local variables.
In the nervous system, plasticity is generally understood to arise
from activity-dependent modifications that depend on informa-
tion available at or near the site of change, including presy-
naptic activity, postsynaptic activity, membrane state, local bio-
chemical traces, and modulatory influences. This spatial and
temporal locality is one of the main reasons local learning rules
are commonly regarded as more biologically grounded than al-
gorithms based on exact end-to-end error backpropagation.
The classical conceptual basis for local adaptation is Hebbian
plasticity, which holds that coordinated activity between neu-
rons tends to strengthen their functional coupling. In spiking
systems, this principle is refined into Spike-Timing-Dependent
Plasticity (STDP), where synaptic modification depends on the
relative timing of pre- and postsynaptic spikes [8]. When presy-
naptic spikes reliably precede postsynaptic spikes within an ap-
propriate temporal window, potentiation may occur; when the
order is reversed, depression may result. STDP thus provides
a canonical example of a rule that is local both in space, be-
cause it depends on synapse-specific activity, and in time, be-
cause it depends on temporally precise spike relationships. Im-
portantly, biological plasticity cannot be reduced to a single
timing-based mechanism. Experimental evidence indicates that
learning emerges from the interaction of multiple processes,
including synaptic plasticity, intrinsic plasticity, homeostatic
regulation, and neuromodulator-dependent modulation [9–11].
These mechanisms operate across multiple timescales and cel-
lular compartments, and their coordinated action contributes
to stability, adaptability, and functional specialization. For the
study of SNNs, this broader perspective is significant because
many local learning algorithms can be understood as abstrac-
tions of such mechanisms, even when they do not aim to repro-
duce them literally.
2.4. Local learning in SNNs
In the context of this paper,local learningrefers to training
schemes in which parameter updates are computed from infor-
mation available locally at the synapse, neuron, or layer level,
rather than from exact global gradients propagated throughout
the entire network. The relevant local signals may include spike
traces, membrane potentials, eligibility traces, local errors, lat-
eral interactions, or modulatory factors, depending on the spe-
cific method under consideration.
This notion of locality should be interpreted as a principled
algorithmic constraint rather than as a claim of strict biolog-
ical realism. Most local training methods in machine learn-
ing are not intended as faithful models of cortical plasticity.
Rather, they are motivated by the observation that biological
learning appears to proceed without exact weight transport or
globally coordinated backward passes, and that useful learning
can instead emerge from the interaction of local activity, cir-
cuit structure, and modulatory processes. From this standpoint,
local learning in SNNs occupies an intermediate position be-
tween neuroscience-inspired modeling and practical algorithm
design.
2.5. Relevance to neuromorphic computing
The appeal of local learning is not only biological but also
architectural. Neuromorphic hardware substrates are typically
characterized by distributed computation, co-localized memory
and processing, event-driven execution, and limited support for
globally synchronized communication [12]. Under such con-
straints, training rules that require long-range error propagation,
exact symmetry between forward and backward pathways, or
repeated global coordination may be difficult to implement ef-
ficiently, particularly in online or on-chip settings.
By contrast, learning rules based on locally accessible vari-
ables are better compatible with the distributed and asyn-
chronous organization of neuromorphic systems [2, 13–18].
For this reason, locality has become a key organizing principle
in the design of training algorithms for SNNs, linking biologi-
cal plausibility, hardware efficiency, and algorithmic scalability.
This convergence of motivations explains why local learning
occupies a central place in contemporary research on spiking
neural networks.
2.6. Implications for this survey
The following sections build on this background to exam-
ine how training algorithms for SNNs navigate the trade-offs
among optimization effectiveness, biological plausibility, and
hardware realizability. Particular emphasis is placed on local
learning methods, not as a single algorithmic family, but as a
broad design space defined by the use of spatially and tempo-
rally local learning signals to train spiking systems.
3. Related Work
The rise in popularity of SNNs over the last decades has been
accompanied by survey and perspective works offering peri-
odic wrap-ups of the state of the art and recent advancements.
Given the breadth of concepts and techniques encompassed by
SNNs, these works span architectures, encoding techniques,
datasets, applications, and related topics. In this section, we
analyze these surveys with the specific aim of identifying those
that cover training SNNs. We comment on them to highlight
their strengths and clarify their differences, and to motivate
the choices behind our survey taxonomy and the accompany-
ing benchmarking framework. To position this work, we first
provide a concise, chronological account of how training has
been covered as the field has evolved, and then discuss more
recent surveys by scope, highlighting where the current view of
training algorithms remains fragmented.
Chronology-driven filtering of prior surveys.When working in
rapidly evolving fields such as neuromorphic computing and the
training of SNNs, time becomes a critical factor in evaluating
review papers. Earlier surveys, even if well-written and thor-
ough, can quickly fall out of scope as the literature expands. At
3

--- PAGE 4 ---

the same time, they are valuable to understand how the com-
munity’s focus evolved, which techniques were emphasized,
and which directions matured into today’s dominant practices.
In the following, we summarize representative works excluded
from the present survey due to their temporal coverage and the
methods they employ. One of the first works in this category
by Ponulak et al. [19] provides a clear snapshot of the field
in the early 2010s. Although positioned as a general introduc-
tion covering models, coding, and applications, it devotes sub-
stantial space to learning, surveying STDP-like rules and early
supervised methods such as ReSuMe [20] and SpikeProp [21],
as well as reinforcement formulations. Toward the end of the
previous decade, surveys became more frequent. Beyond dif-
ferences in focus, several recurring themes emerged in this pe-
riod: training by conversion from ANNs was widely discussed
as a practical route to high accuracy, while direct training re-
mained actively explored, with early algorithms receiving most
attention and initial adaptations of backpropagation, together
with surrogate gradient-like approaches, appearing in the sur-
vey landscape [22–24]. In parallel, local learning was often
framed in terms of STDP and its variants, often in an unsuper-
vised setting [25, 26]. Several reviews from this timeframe are
not centered on training, but still contain curated and informa-
tive sections on learning and optimization [12, 27–34]. After
this phase, the emphasis of surveys shifted. As assessed in [5],
backpropagation techniques with surrogate gradients, particu-
larly Back-Propagation Through Time (BPTT) adaptations to
SNNs, increasingly dominated as leading approaches for direct
training on complex architectures and datasets. At the same
time, local learning was increasingly discussed as a supervised
candidate, beyond its established role in unsupervised settings,
aligning with the broader goal of bringing machine-learning ca-
pabilities to constrained and low-power devices where back-
propagation can be challenging. In this evolving landscape,
STDP remained a widely used unsupervised algorithm and con-
tinued to inspire new techniques [35]. In parallel, more sys-
tematic meta-analyses began to appear, for instance in [36],
which compares training approaches through a complexity-
oriented lens. As interest in SNNs and their training continued
to grow, more structured, field-specific, and application-driven
reviews emerged, including reviews focused on hardware plat-
forms [37, 38]. In particular, Frenkel et al. [39] survey neu-
romorphic computing with a focus on hardware design, includ-
ing a detailed section on the current state of the art in train-
ing. A broad training coverage spanning datasets and applica-
tions is presented in [40]; however, given its publication date,
it does not include the latest proposed techniques. As SNNs
extend toward more complex architectures, dedicated works re-
port that top results in these settings are still largely associated
with backpropagation-based training and conversion methods,
which can achieve high accuracy in complex scenarios [41].
Overall, this chronological view clarifies how the emphasis in
SNN training has shifted over time, from early STDP-inspired
rules and classical supervised methods to conversion pipelines
and, more recently, surrogate-gradient backpropagation, with
renewed attention to local and online learning as a practical
direction for constrained deployments. At the same time, it
highlights how quickly surveys become outdated in this area,
motivating an updated synthesis that consolidates the training
landscape under a unified view.
Scope-driven positioning of recent surveys.Complementary to
the chronological view, we now analyze the landscape of more
recent works by scope and focus. The goal is to clarify what
each review covers well and what remains underdeveloped with
respect to this work, which aims to provide a thorough taxon-
omy of training algorithms with an emphasis on local, direct
training rules and practical benchmarking.
A broad overview of learning and training can be found in
works such as [42–44]. These works survey SNNs more gen-
erally; consequently, they do not aim to provide a complete
and systematic taxonomy of training algorithms, and training
is necessarily treated as one component within a wider per-
spective. Among works that lean more explicitly towards train-
ing, each focuses on a different aspect, as expected in a field
that is varied and complex. Works such as [45–47] focus on
large networks for complex problems, where backpropagation
and conversion training dominate, and therefore give compar-
atively less attention to approaches more suited to embedded
and resource-constrained deployments, including many bio-
inspired algorithms. Other specialized works include [48, 49]
focusing on continual learning, [50] concentrating on evolu-
tionary approaches, and [51] analyzing FPGA hardware adap-
tations. We also found works centered on biologically plausi-
ble and local learning rules, each focusing on a particular sub-
space. For instance, [52] focuses on algorithms structured as
three-factor learning rules. In contrast, [3] emphasizes biolog-
ical plausibility and local learning mechanisms, with a strong
focus on the STDP-family and related synaptic plasticity rules.
Finally, a major gap in the current landscape is the lack of clear,
reproducible benchmarking. While work exists that compares
algorithms primarily in terms of accuracy [53], these efforts
typically consider only a limited subset of training rules and do
not provide a practical, extensible toolchain for cross-method
evaluation. Related software ecosystems (e.g., snnTorch [54])
facilitate implementation and experimentation, but, by them-
selves, they do not provide a survey-driven taxonomy coupled
with systematic, reproducible comparisons across training ap-
proaches. A complementary perspective is taken by [55], which
benchmarks five neuromorphic training frameworks across im-
age, text, and neuromorphic datasets under both direct train-
ing and ANN-to-SNN conversion, providing actionable guid-
ance on framework selection but without covering local learn-
ing rules or supplying a taxonomy of training algorithms.
In summary, existing surveys collectively cover a broad
range of SNN topics. Still, a consolidated view of training al-
gorithms, particularly local methods, remains fragmented, and
systematic comparisons across methods are still scarce. Table 1
provides a compact map of the survey landscape, which we use
to position the scope of this work. Building on these obser-
vations, the next sections introduce our taxonomy and bench-
marking framework, with the explicit goal of enabling consis-
tent, reproducible comparisons across training approaches.
4

--- PAGE 5 ---

Work Y ear Focus Training Scope Methodology
Conv BP Loc Train Large HW Taxon Bench
Chronology-driven set
[19] 2011 Introduction◦X X◦ ◦
[22] 2018 Training survey◦X◦X◦X X
[23] 2019 Training surveyX X◦X X◦ ◦
[27] 2019 Perspective◦ ◦ ◦ ◦X◦
[24] 2020 Training survey◦X◦X◦X◦
[25] 2020 Local learningX X◦
[26] 2020 Local learningX X X X◦ ◦
[28] 2021 General SNN◦ ◦ ◦ ◦ ◦ ◦
[29] 2021 HW design◦ ◦ ◦ ◦ ◦X
[30] 2022 Perspective◦X
[12] 2022 HW design◦X
[31] 2022 General SNN◦ ◦ ◦ ◦ ◦ ◦ ◦
[32] 2022 Perspective◦ ◦ ◦ ◦
[33] 2022 HW design◦X
[34] 2022 General SNN◦ ◦ ◦ ◦ ◦ ◦ ◦
[5] 2023 Direct training◦X X X◦
[35] 2023 Local learningX X X◦
[37] 2023 HW design◦ ◦ ◦ ◦X
[39] 2023 HW design◦ ◦ ◦ ◦X◦
[40] 2023 Training surveyX X X X◦ ◦X
[38] 2024 HW design◦ ◦ ◦X
[41] 2024 Training surveyX X X X◦X
Scope-driven set
[36] 2023 Systematic analysisX X◦X◦
[54] 2023 Tutorial/software◦X X X◦ ◦ ◦
[49] 2023 Cont. learning◦ ◦ ◦ ◦ ◦
[44] 2024 General SNN◦ ◦ ◦ ◦ ◦ ◦ ◦
[45] 2024 Direct trainingX X◦X X◦ ◦
[46] 2024 Direct training◦X X X X◦
[50] 2024 Evolutionary◦ ◦ ◦X◦
[42] 2025 General SNN◦ ◦ ◦ ◦ ◦ ◦ ◦
[43] 2025 Tutorial/software◦ ◦ ◦X◦
[47] 2025 Direct training◦ ◦ ◦ ◦ ◦ ◦
[48] 2025 Cont. learning◦ ◦ ◦ ◦ ◦
[52] 2025 Local learningX X◦ ◦
[3] 2025 Local learning◦X X◦
[51] 2025 HW design◦ ◦ ◦X
[53] 2025 Systematic analysis◦ ◦X X X
[55] 2025 Systematic analysis◦ ◦X◦X
This work2026 Training surveyX X X X◦X X
Table 1: Surveys related to SNN training, grouped by scope.Chronology-driven: earlier surveys, included to trace the evolution of the field.Scope-driven: recent
surveys differing from this work in focus (hardware, continual learning, large-scale architectures, etc.); local learning rules and cross-method comparisons receive
limited coverage in this literature, motivating the present work.Training(Section 4):Conv=ANN-to-SNN conversion;BP=gradient-based direct training;Loc=
local/online rules.Scope:Train=training is a primary subject;Large=focus on large-scale architectures;HW=neuromorphic hardware design.Methodology:
Taxon=systematic taxonomy of training methods;Bench=reproducible cross-method comparisons.X=substantial;◦=partial coverage; blank=not a focus.
5

--- PAGE 6 ---

Figure 2: Two complementary taxonomies for SNN training algorithms. (A)
Classification by training strategy (ANN-to-SNN conversion, direct training,
optimization), with direct training further divided by learning paradigm (re-
inforcement, supervised, unsupervised). (B) Classification by learning scope
(global vs. local), with local methods distinguished by spatial or temporal lo-
cality.
4. Taxonomy
Navigating the literature on training algorithms for SNNs is
increasingly challenging: the number of proposed methods is
rapidly growing, and closely related ideas are often presented
under different names, with different assumptions or implemen-
tation choices. In this section, we introduce a systematic tax-
onomy, organized along multiple axes, to help readers structure
the design space and locate individual contributions. We first
describe the taxonomy architecture by defining the categoriza-
tion axes and motivating their relevance. We then map the cur-
rent algorithmic landscape onto these axes, justifying the place-
ment of representative works within each category. Figure 2
graphically summarizes the complete structure.
4.1. Taxonomy Categorization Axes
To ease exploration, the taxonomy is organized along a set of
categorization axes that reflect the most common characteris-
tics used in the literature to describe and compare SNN training
algorithms. These axes provide a structure for highlighting re-
curring design choices and positioning different works within a
shared framework.
We begin by clarifying what it means to “train” an SNN,
as the literature encompasses substantially different approaches
under this umbrella. A first key axis is the chosen learn-
ing strategy (Figure 2, panel A); we identify three main
paradigms: (i)direct SNN training, where learning is performed
while explicitly simulating spiking dynamics, spanning both
gradient-based methods (e.g., surrogate-gradient BPTT) and
non-gradient synaptic plasticity rules (e.g., STDP- and three-
factor-inspired updates); (ii)ANN-to-SNN conversion, where a
standard ANN is first trained with conventional techniques and
subsequently mapped to an SNN for deployment; and (iii)evo-
lutionary and population-based optimization, where network
parameters, architectures, or both are optimized through black-
box search over a population of candidate solutions, generally
without computing analytic gradients of the spiking dynamics.
Direct training constitutes the largest and most methodologi-
cally diverse body of work, introducing the widest range of
credit-assignment mechanisms; it therefore forms the primary
focus of this survey. Conversion and evolutionary approaches
are discussed in dedicated sections to avoid conflating funda-
mentally different objectives and constraints.
Within direct training strategies, we further organize algo-
rithms based on a second key axis: the type of learning signal
available. We distinguishsupervisedalgorithms, which lever-
age labeled targets;unsupervisedalgorithms, which optimize
objectives derived from the structure of the input; andreinforce-
ment learningalgorithms, where learning is driven by reward
signals that may be delayed and obtained through interaction
with an environment. This axis is central because it directly
constrains the form, timing, and observability of credit assign-
ment.
Motivated by the potential computational advantages offered
by biological learning mechanisms and by hardware efficiency
constraints, contemporary research increasingly emphasizes the
importance of locality in training algorithms. This concept
is typically decomposed into two distinct dimensions: tem-
poral locality and spatial locality.Temporal localityrequires
that parameter updates at timetdepend exclusively on infor-
mation available at the current timestep, possibly alongside a
bounded internal state (e.g., eligibility traces). This contrasts
with methods that store and replay complete activity histories
across all timesteps, such as the network unrolling performed
during the backward pass of BPTT [56].Spatial localitycon-
cerns instead the availability of information across the network
structure. Consistent with established literature, we define a
learning rule as spatially local if it computes synaptic weight
changes using only variables physically present at the synapse
(i.e., pre- and postsynaptic activity), possibly modulated by a
global signal, provided this does not introduceupdate locking.
Update locking occurs when weight modifications cannot pro-
ceed synchronously with the forward pass but must wait for
a global network operation to complete (e.g., a full backward
pass), coupling each synaptic update to the network’s overall
latency. Based on these definitions, training algorithms can be
classified according to their adherence to spatial, temporal, or
both locality, or to neither.
In addition to the primary categorization axes described
above, we introduce a second layer of categorization based
oncross-cutting algorithmic mechanisms. While the axes cap-
ture high-level properties, many direct-training methods reuse
a small set of recurring building blocks that are combined and
instantiated in different ways across papers. We therefore use
these mechanisms asnon-exclusive descriptorsto annotate al-
gorithms and make shared structure explicit, helping readers
identify commonalities and pinpoint the substantive differences
between approaches.
6

--- PAGE 7 ---

From our survey of the literature, we highlight six mecha-
nisms that recur frequently.
Eligibility traces.A central challenge in training SNNs is tem-
poral credit assignment: determining how a synaptic weight
changes at timetshould account for activity that unfolded over
preceding timesteps. Many methods address this by equipping
each synapse with aneligibility trace, an auxiliary state vari-
able that accumulates a temporally decaying record of recent
pre- and postsynaptic activity. Rather than storing complete
activity histories, traces compress temporal information into a
compact, continuously updated quantity that can be maintained
locally and forward in time. Weight updates (∆wji) are then pro-
duced by combining the trace (e ji) with a modulatory learning
signal (M), an error broadcast, a reward, or a target projection,
following the general form of a three-factor rule [57]:
∆w ji ∝e ji ·M(1)
Direct Feedback Alignment (DFA).In standard backpropaga-
tion, hidden-layer gradients are computed by transporting the
output error backward through the transpose of the forward
weight matrices.DFA[58] bypasses this by projecting the out-
put erroredirectly to each hidden layerlthrough a fixed ran-
dom matrixB l, yielding a learning signalg l =B le. This elim-
inates the weight-transport problem and removes the layer-by-
layer backward pass dependency. In the SNN context, DFA is
attractive because the error can be broadcast to all layers si-
multaneously; however, it still requires the output error to be
computed, meaning the full forward pass must complete before
learning signals become available.
Direct Random Target Projection (DRTP). DRTP[59] replaces
the error-based feedback of DFA with a direct projection of the
target signal to hidden layers:g l =f(B ly∗), wherey ∗ is the tar-
get andfa nonlinearity. The crucial distinction is that DRTP
does not require the output error and therefore does not need to
wait for the forward pass to complete: the target is known at
the beginning of each sample. This makes DRTP compatible
with update-free, fully pipelined training and naturally com-
bines with eligibility traces to produce algorithms that are both
temporally and spatially local.
Auxiliary local classifiers.Rather than relying on a single
global loss at the output, some methods attachauxiliary per-
layer structures, local readout heads, linear classifiers, or cus-
tom decoding circuits, to intermediate layers. Each generates a
layer-wise loss or teaching signal, enabling weight updates that
do not depend on error propagation from the output. This ad-
dresses both spatial locality and the vanishing-gradient problem
in deep networks, at the cost of additional parameters and the
design choice of how to formulate each local objective.
Spatial backpropagation with online temporal credit assign-
ment.A family of methods retains standard backpropagation
across the spatial dimension at each timestep, but decouples
temporal credit assignment from the unrolling required by
BPTT. At each timet, a conventional backward pass is com-
puted through the layer stack using an instantaneous loss. At the
same time, temporal dependencies are handled separately via
online mechanisms, such as eligibility traces or filtered presy-
naptic activity. This achieves constant memory cost with re-
spect to the number of timesteps while preserving the expres-
sive spatial gradients of backpropagation. These methods are
not spatially local, but they achieve full temporal locality, of-
fering a practical middle ground between the performance of
BPTT and the constraints of online learning.
STDP-inspired mechanisms.A substantial body of work builds
on the conceptual template of STDP, adapting spike-timing-
based correlations to supervised objectives, reinforcement sig-
nals, or specific coding schemes. While classical STDP is a
two-factor Hebbian rule driven by relative pre-/post-synaptic
spike timing, many modern variants extend it to three-factor
form by gating the update with a modulatory signal, bridg-
ing unsupervised correlation detection with task-driven learn-
ing (cf. Equation 1).
Importantly, not all algorithms emphasize any of these mech-
anisms, and some introduce orthogonal ideas; we therefore treat
this list as a pragmatic set of common denominators rather than
a complete basis for the full design space.
4.2. Training Algorithms
We now examine the core of the taxonomy by analyzing the
current state of the art in SNN training algorithms. In this
section, we contextualize the existing literature within the pro-
posed framework and provide the rationale for the structure il-
lustrated in Figure 2. The discussion is organized around the
three primary paradigms identified previously:direct training,
evolutionary algorithms, andANN-to-SNN conversion. We pri-
oritize the direct training category, as it represents the most
diverse and active area of research and provides a concise
overview of conversion and evolutionary approaches. Our anal-
ysis of direct training proceeds from supervised learning to un-
supervised methods, concluding with reinforcement learning.
4.2.1. Direct Training
The direct training paradigm encompasses all strategies that
derive parameter updates explicitly from the simulation of SNN
dynamics. This category is the primary focus of our survey,
reflecting the rapidly expanding body of work that exploits the
temporal richness of spiking neurons to solve complex tasks.
Furthermore, direct training arguably offers the most promising
path to highly efficient implementations, particularly in low-
latency, energy-constrained embedded scenarios.
Early Supervised Approaches.The majority of research on
SNNs uses supervised learning because it is a simpler, more sta-
ble, and straightforward way to train SNNs. Supervised learn-
ing in traditional neural networks is a mature field, where back-
propagation is the most widely used training technique. As
a consequence of the supervised learning problem for SNNs,
researchers sought to adapt backpropagation algorithms to the
specific dynamics of spiking neurons.
7

--- PAGE 8 ---

Early direct supervised methods for SNNs predominantly
relied on explicit coding schemes to circumvent the non-
differentiability of spike generation. A prominent paradigm
employs exact spike-time (latency) coding, where the loss func-
tion is defined directly in terms of output firing times. Spike-
Prop serves as the seminal example, backpropagating the error
between desired and observed spike times by linearizing the
membrane potential at threshold crossings [21]. In its origi-
nal formulation, this method was tightly coupled to a complex
synapse model featuring multiple delayed terminals per con-
nection. This architecture increased parameter complexity, ren-
dering training highly sensitive to initialization and neuronal
quiescence. Subsequent variants introduced mechanisms such
as delay and threshold adaptation, forced firing for silent units,
or accelerated optimization to enhance convergence [60–62].
Despite these refinements, the approach faces significant scal-
ability challenges; spike creation and annihilation induce dis-
continuities in the error landscape, and the requirement for en-
gineered temporal targets limits flexibility.
A second category of methods avoids direct differentiation of
spike times, instead comparing output and teacher spike trains
through local learning rules. Remote Supervised Method (Re-
SuMe) formulates supervision as the minimization of the dis-
crepancy between desired and generated spike trains, deriv-
ing a delta-rule implemented via STDP-like correlations [20].
Similarly, SPAN filters spike trains into continuous traces to
enable Widrow-Hoff-style updates in the analog domain [63].
At the same time, the Chronotron optimizes spike-train sim-
ilarity to reproduce temporal output patterns [64] precisely.
Alternatively, the Tempotron targets a binary classification
task, updating weights only upon error by utilizing the tim-
ing of the maximal membrane potential [65]. Finally, SW AT
adopts a rate-based coding perspective, encoding inputs as
spike trains with class-specific frequencies, combining STDP
with a Bienenstock–Cooper–Munro (BCM)-like rule for classi-
fication [66].
Collectively, these methods established the founda-
tional paradigms for supervised spiking learning, including
timing-based backpropagation, spike-train matching, and
classification-oriented rules. However, their utility in modern
contexts is limited; they are typically constrained to shallow
architectures (often single layers) and rely on rigid temporal
codes. Consequently, they lack the robustness and scalability
offered by contemporary surrogate-gradient and BPTT-based
training within standard deep-learning frameworks.
Enabling Backpropagation in SNNs.Following the initial ex-
ploration period, the resounding success of deep ANNs moti-
vated a paradigm shift toward training SNNs using gradient-
based optimization. The fundamental challenge in this domain
is the non-differentiability of the spike generation mechanism
S[t]= Θ(U[t]−U thr). The derivative of the Heaviside step
functionΘ(·) is zero almost everywhere and undefined at the
threshold, which leads to vanishing (or ill-posed) gradients. It
can prevent subthreshold neurons from receiving a useful learn-
ing signal. To overcome this, researchers have developed mul-
tiple distinct strategies to enable error backpropagation through
spiking dynamics.
The strategy pioneered by Lee et al. [67] circumvented the
discontinuity by treating the accumulated membrane potential,
rather than the discrete spike, as the primary signal carrying in-
formation. By effectively smoothing the signal and ignoring the
sharp reset mechanism during the backward pass, this method
provided one of the first demonstrations of direct deep SNN
training. However, the resulting mismatch between forward and
backward dynamics limited its precision.
A more systematic line of work explicitly adapts BPTT to
spiking dynamics, most notably formalized in Spatio-Temporal
Back-Propagation (STBP) [68]. In this view, an SNN is treated
as a discretized Recurrent Neural Network (RNN): the network
is unrolled over time and gradients are accumulated jointly
along spatial (layer-to-layer) and temporal (time-to-time) de-
pendencies of the membrane state. Practical training is en-
abled by thesurrogate gradienttrick, which replaces the non-
differentiable factor∂S[t]/∂U[t] in the backward pass by a
bounded proxyσ ′(·) while keeping the forward pass strictly
spiking [69].
Closely related in spirit, but organized around spike-train ob-
jectives rather than an explicit unroll-and-backprop implemen-
tation, SuperSpike [70] optimizes a spike-train distance (via the
van Rossum metric) and introduces a smooth pseudo-derivative
in voltage space, yielding an error-modulated learning rule that
can be interpreted through eligibility traces and that directly tar-
gets precise spike timing.
A complementary “temporal specialist” route is exemplified
by SLAYER [71], which adopts a Spike Response Model view-
point and redistributes error through temporal response ker-
nels so that credit assignment aligns with delayed postsynap-
tic effects; this formulation naturally supports learning not only
synaptic weights but also axonal delays on event-driven tasks
(e.g., Dynamic Vision Sensor (DVS) gesture recognition [72]).
Building on this line, EXODUS [73] revisits SLAYER’s effi-
cient layer-wise, time-vectorized gradient computation and im-
proves stability by explicitly accounting for the neuron reset
in the backward pass via implicit differentiation, reducing the
need for ad-hoc gradient scaling while recovering gradients
equivalent to BPTT.
While these approaches highlight different routes to mak-
ing gradients usable in the presence of spikes, the STBP-style
surrogate-gradient BPTT pipeline has arguably become the
most widely adopted template in deep-learning-oriented SNN
research, largely because it maps naturally onto modern autodiff
frameworks and scales to deep architectures and large datasets.
At the same time, the community has clarified that surrogate-
gradient training is often surprisingly robust to theparticular
surrogate shape, even though stability can depend strongly on
scaling and implementation details [74]. Building on this mo-
mentum, the field has seen rapid advancements aimed at stabi-
lizing convergence and scaling to deeper architectures.
Key improvements include the introduction of learnable
membrane time constants [75] and unified gated neuron mod-
els [76] to enhance parametric flexibility. Furthermore, op-
timization stability has been significantly improved through
SNN-specific normalization techniques, including threshold-
8

--- PAGE 9 ---

dependent batch normalization [77], batch normalization
through time [78], and temporal effective batch normaliza-
tion [79, 80], as well as gradient re-weighting strategies like
TET [81]. Recent works have further refined the learning land-
scape by rectifying membrane potential distributions [82], max-
imizing information flow via novel loss functions [83], and en-
hancing gradient precision via differentiation on spike represen-
tations [84] or learnable surrogate shapes [85].
Despite these successes, most of these gradient-based meth-
ods share a common limitation regarding the proposed taxon-
omy: they are fundamentally non-local. Spatially, they rely on
global error propagation, which violates strict spatial locality.
Temporally, explicit BPTT pipelines require unrolling dynam-
ics over the full simulation horizon and storing intermediate
states, leading to a memory footprint ofO(T) and weight up-
dates that are typically locked to the end of the sequence [54].
Alternative formulations (e.g., trace- or kernel-based credit as-
signment) can reduce the need to store full trajectories. How-
ever, they still depend on temporally extended history and non-
local error signals, leaving online learning on memory-limited
neuromorphic hardware as a central challenge.
Emergence of locality and bioinspiration.As surrogate-
gradient BPTT matured into a reliable recipe for high accuracy,
its practical drawbacks, update locking, a backward pass span-
ning the full depth, and the need to retain temporal state for
gradient computation, made its mismatch with neuromorphic
constraints increasingly apparent [54]. This tension helped re-
vive an older intuition from computational neuroscience: learn-
ing in the brain is largelylocal, shaped by pre- and postsynaptic
activity and modulated by relatively simple global factors [86–
88]. Early in this renewed direction, several works revisited
STDP [88] not merely as an unsupervised feature learner, but
as a scaffold for supervision. A representative example is the
stable supervised STDPlineage [89, 90], which keeps weight
updates synapse-local by enforcing bounded, weight-dependent
potentiation/depression and by injecting a teaching signal at the
output so that spike timing becomes class-discriminative. More
recent variants such as S2-STDP [90] further stabilize learning
by coupling supervision to latency objectives (encouraging tar-
get neurons to fire early and non-target neurons late) and by
structuring the classifier around paired competition, effectively
obtaining stronger separability with minimal output circuitry
while remaining close to an event-driven, plasticity-rule mind-
set.
A parallel and highly influential thread sought locality
througheligibility traces, translating temporal credit assign-
ment into forward-time state variables that resemble synaptic
tags; conceptually, this idea traces back to Real-Time Recurrent
Learning (RTRL) [86], which computes exact online gradients
for continually running fully recurrent networks by maintaining
state–parameter sensitivities over time. In recurrent settings,
Eligibility Propagation (e-prop) [91] is emblematic: it factor-
izes gradients into a product of a synapse-specific eligibility
trace and a (possibly broadcast) learning signal, enabling on-
line updates without storing the entire unfolded history, but typ-
ically remaining spatially non-local because the learning signal
depends on output error and must be delivered to hidden units.
This same basic decomposition, a local trace modulated by a
teaching term, reappears in many later rules, differing mainly
in (i) how closely the trace approximates exact gradients, and
(ii) whether the teaching term is obtained by true backprop-
agation, by random projections, or by fully local objectives.
Online Spatio-Temporal Learning (OSTL) [92] sharpens this
picture by explicitly separating spatial learning signals from
temporal traces and clarifying when the resulting updates are
gradient-equivalent and when they become controlled approxi-
mations (e.g., by dropping higher-order terms to tame complex-
ity). In [93] the authors adapt to SNNs the Forward Propaga-
tion Through Time (FPTT) algorithm, which recasts temporal
credit assignment as a consensus problem and avoids backward
unrolling by augmenting the instantaneous loss with a dynamic
regularisation term based on a running average of past weight
updates. Combined with liquid time-constant spiking neurons
whose input-driven membrane time-constants provide the gat-
ing structure FPTT requires to converge on recurrent tasks.
Several methods then push further along the “BPTT-like but
cheaper” axis: Online Training Through Time (OTTT) [94] de-
rives instantaneous updates by combining a time-local loss with
forward traces, Spatial Learning Through Time (SLTT) [95]
makes an even more aggressive simplification by discarding
temporal gradient paths so that one essentially performs spa-
tial backprop at selected time steps with constant-in-time mem-
ory, and STOP [96] keeps spatial backprop per time step but
enriches temporal assignment through traces while extending
adaptation beyond weights to include intrinsic parameters such
as thresholds and leak factors; S-TLLR [97] applies the same
spatial-BP-per-step template with STDP-inspired causal and
non-causal eligibility traces. In the same spirit of improving
temporal approximationsin deep networks, OTPE [98] high-
lights that many efficient trace rules under-credit early-layer
parameters for errors that only manifest downstream after leak-
age and synaptic filtering; it restores these delayed postsynap-
tic influences via additional traces (with a further approxima-
tion to recover near-linear scaling). At the end of scalability,
ES-D-RTRL/BrainScale [99] revisits the classic RTRL objec-
tive, exact online gradients, and makes it practical by aggres-
sively approximating the eligibility tensor (e.g., diagonal/rank-
structured forms with smoothing), reaching network sizes that
are far beyond what synapse-wise trace methods can store.
In contrast to trace-centric approaches that mainly attack
temporalnon-locality, another family targetsspatialnon-
locality by removing global backpropagation across layers.
Deep Continuous Local Learning (DECOLLE) [100] is a clean
example: by attaching auxiliary readouts to each layer and op-
timizing layer-wise losses, it avoids a global backward pass and
allows layers to learn in parallel, using three-factor, surrogate-
gradient-style updates driven by local errors and forward traces.
A key limitation of strictly fixed/random readouts is “weak
coupling”, early layers may learn representations that satisfy
their own local objective but are suboptimal for downstream
processing, which motivates refinements where auxiliary clas-
sifiers become trainable and where the temporal approxima-
tion is made explicit. Exact Local Learning (ELL)/Backward
9

--- PAGE 10 ---

Exact Local Learning (BELL)/Forward Exact Local Learning
(FELL) [101] fit here: ELL prioritizes strict efficiency by ig-
noring temporal dependencies, BELL performs local BPTT
within each layer to recover accuracy at the cost of time-
locking, and FELL uses forward traces to approximate the
temporal component online, offering a middle ground that of-
ten narrows the gap to global training while preserving layer-
wise decoupling; STDL [102] generalizes the local-classifier
idea to multi-layer blocks, using downstream blocks as auxil-
iary classifiers rather than dedicated readout heads, while dis-
carding temporal gradient terms for fully online updates. A
related, hardware-oriented route replaces backpropagated er-
rors withdirectprojections: Spike-Train-level Direct Feedback
Alignment (ST-DFA) [103] adapts direct feedback alignment
to spike-train level signals so that hidden layers receive teach-
ing information through fixed random feedback rather than
weight-transported gradients; Event-based Three-factor Local
Plasticity (ETLP) [104] and Online Spatio-Temporal Learn-
ing with Target Projection (OSTTP) [105] push this logic into
three-factor, trace-modulated plasticity by combining eligibil-
ity traces with DRTP [59], aiming for fully online updates with
minimal global coordination. Spiking Time Sparse Feedback
(STSF) [106] takes a particularly pragmatic hybrid stance by
pairing a sparse feedback-alignment-style global signal with an
STDP-like local rule, leveraging sparsity to reduce the cost of
feedback while preserving an event-driven learning core.
Finally, a few approaches attempt to avoid the usual back-
ward infrastructure more radically. Temporally and Spatially
Local Learning Rule (TESS) [107] achieves spatial and tempo-
ral locality by generating errors locally at each layer through
fixed projections into a task space (local error generation), cou-
pled with instantaneous, STDP-flavored traces that include both
causal and non-causal components; this keeps learning simple
and hardware-friendly, at the price of leaning on carefully de-
signed layer-wise targets. Traces Propagation (TP) [108] goes
further by eliminating the backward pass via a forward-only,
dual-path scheme in which target information is propagated in
parallel to the input-driven activity, enabling synapses to up-
date using only locally available traces and the locally deliv-
ered target signal; notably, this forward-only design is among
the few fully local rules reported to scale to deep convolutional
backbones. A complementary forward-only paradigm draws
directly on the Forward-Forward (FF) algorithm [109], which
replaces the backward pass with two forward passes over posi-
tive (correctly labeled) and negative (incorrectly labeled) data,
optimizing a layer-wisegoodnessobjective locally. In [110]
this framework is adapted to SNNs by using accumulated spike
counts as the goodness measure, applying layer normalization
between layers to decouple representations across depth, and
computing layer-local weight updates via surrogate gradients.
Taken together, these works illustrate a broad spectrum of com-
promises: methods closer to BPTT tend to preserve accuracy
but relax locality (often spatially), while more bio-inspired and
hardware-friendly rules improve locality and online capabil-
ity by introducing auxiliary objectives, random feedback, or
forward-only teaching signals, with the central practical chal-
lenge remaining how to retain strong performance as depth,
temporal structure, and task complexity increase.
Table 2 summarizes the locality and mechanistic properties
of all supervised direct-training algorithms surveyed above.
Unsupervised approaches for SNNs.Unsupervised learning
has received sustained attention in SNN research, motivated by
its deep roots in the neuroscience of synaptic plasticity and by
the practical appeal of learning rules that require no global er-
ror signal, a property well suited to neuromorphic hardware.
Although unsupervised methods alone do not yet rival super-
vised approaches on complex benchmarks, they have produced
a diverse methodological landscape and remain essential where
labeled data or global feedback pathways are unavailable.
The dominant mechanism underlying unsupervised SNN
training is STDP, whose experimental basis was established in
the late 90s [87, 111]: synaptic strength increases when a presy-
naptic spike precedes a postsynaptic spike, and decreases for
the reverse order, with approximately exponential dependence
on the temporal difference. In [88], STDP was shown to func-
tion as a competitive Hebbian rule, producing self-organized
input selectivity without explicit normalization. Two subse-
quent works established STDP as a viable mechanism for un-
supervised representation learning. In [112], STDP in a hi-
erarchical feedforward SNN with rank-order temporal coding
was shown to enable neurons to become selective to repeat-
ing spatiotemporal patterns (e.g., faces, object parts) in natu-
ral images. Later, 95% accuracy on MNIST was achieved in
[113] using a two-layer network of Leaky Integrate and Fire
(LIF) neurons trained entirely without supervision, demonstrat-
ing that combining STDP with lateral inhibition, winner-take-
all competition, and adaptive thresholds suffices for competitive
digit recognition. This work became the standard reference for
unsupervised STDP-based classification and showed that bio-
logically motivated circuit-level inductive biases can effectively
substitute for global optimization.
Classical pair-based STDP cannot account for the frequency
dependence of plasticity observed experimentally. This was ad-
dressed with triplet-based rules [114, 115], which extend stan-
dard STDP with additional traces and connect to the BCM
learning rule [116], and with a voltage-based formulation in
[117] where synaptic changes additionally depend on the post-
synaptic membrane potential. Network stability requires com-
plementary mechanisms: weight-dependent update rules [118,
119] and homeostatic processes, such as synaptic scaling [120],
maintain weight distributions and firing rates within a func-
tional range. Hardware-oriented simplifications have also been
explored, such as Spike-Driven Synaptic Plasticity (SDSP) with
bistable synapses [121], a robust and implementation-friendly
alternative to full STDP.
Extending STDP from shallow to deep architectures is chal-
lenging because the rule provides no mechanism for propagat-
ing learning signals across layers. The dominant solution is
greedy layer-wise training, where each layer is trained with
STDP independently and then frozen before training the next,
analogous to the unsupervised pre-training of deep belief net-
works [122]. Since purely unsupervised SNNs lack a classifica-
tion mechanism, most works in this area evaluate learned rep-
10

--- PAGE 11 ---

resentations through a supervised readout (e.g., SVM or linear
probe) appended after training; the feature learning itself, how-
ever, remains unsupervised. The first deep convolutional SNN
with multiple STDP-trained layers (SDNN) was introduced
in [123], learning hierarchical features via rank-order tempo-
ral coding and achieving 98.4% on MNIST. Subsequent work
addressed the sequential bottleneck of greedy training through
a dual-accumulator neuron model enabling simultaneous layer-
wise learning from event streams [124], showed that LIF dy-
namics under rank-order coding reduce to a ReLU-like opera-
tion amenable to GPU-accelerated mini-batch STDP [125], and
demonstrated that residual connections are critical for sustain-
ing learning beyond two or three layers [126]. Despite these
advances, STDP-trained networks have been shown to perform
effectively only up to roughly five layers, and their accuracy
on complex benchmarks such as CIFAR-10 remains well below
that of supervised surrogate-gradient methods.
An important theoretical thread provides formal justifica-
tion for STDP as an unsupervised learning principle. In [127],
stochastic spiking networks were shown to implement Markov
Chain Monte Carlo (MCMC) sampling from Boltzmann-like
distributions, and in [128] it was proved that STDP in winner-
take-all circuits approximates expectation-maximization for
mixture models, recasting the rule as an implementation of
principled statistical inference rather than an ad hoc biologi-
cal mechanism. Event-driven contrastive divergence for spiking
restricted Boltzmann machines [129] and stochastic synaptic
sampling [130] translated these ideas into engineering practice,
with particular relevance for neuromorphic substrates where
device-level stochasticity is intrinsic.
More recently, self-supervised paradigms from mainstream
deep learning have been adapted to spiking networks. Con-
trastive Signal-Dependent Plasticity (CSDP) [131] is inspired
by forward-forward-style local objectives and adapts them to
spike-based communication, adjusting synapses locally using
contrastive signals without backpropagation. Momentum con-
trastive learning was adapted to SNNs in [132], achieving
strong results on neuromorphic datasets. More broadly, the
paradigm of unsupervised STDP-based pre-training followed
by supervised fine-tuning has also proven effective for deep
spiking convolutional networks [133]. Classical STDP has
also been revisited with adaptive mechanisms, pushing unsu-
pervised plasticity to CIFAR-10 for the first time [134].
Overall, unsupervised methods lie at the local end of the SNN
training spectrum, and their evolution from early STDP demon-
strations to modern contrastive and generative approaches
shows that architectural inductive biases and principled objec-
tives have proven as important as the plasticity rule itself. The
scalability ceiling of pure STDP remains the central open chal-
lenge, increasingly addressed by self-supervised paradigms that
provide richer training signals while preserving locality.
Reinforcement learning in SNNs.Reinforcement Learning
(RL) in SNNs is grounded in the observation that synaptic plas-
ticity is modulated by neuromodulatory signals (most notably
dopamine) whose phasic responses encode reward prediction
errors closely matching the temporal-difference signal of RL
theory [135]. This provides a natural instantiation of the three-
factor rule (cf. Equation 1): an STDP-derived eligibility trace
records local pre- and postsynaptic correlations. At the same
time, a global reward signal acts as the modulatory factor that
converts the trace into an actual weight change. Unlike super-
vised methods, the learning signal is scalar, delayed, and evalu-
ative rather than instructive, making credit assignment substan-
tially harder. Two broad algorithmic families have emerged to
address this: local reward-modulated rules, which preserve bi-
ological plausibility, and surrogate-gradient methods that adapt
deep RL pipelines to spiking networks.
The theoretical foundations of Reward-modulated Spike-
Timing-Dependent Plasticity (R-STDP) were established by
several concurrent contributions [136–138], deriving reward-
gated STDP updates and showing that transient synaptic eligi-
bility traces can bridge the gap between neural activity and de-
layed reward signals. Subsequent analysis proved that R-STDP
variants require the modulatory signal to encode reward relative
to a learned baseline [139, 140], motivating spiking actor-critic
architectures in which critic neurons supply this baseline via
temporal-difference learning [141, 142]. A unified taxonomy
of spiking RL rules (R-max, R-STDP, and TD-STDP) was pro-
vided in [57], which remains the standard theoretical reference
for local reward-modulated plasticity.
R-STDP has since been extended to deeper architectures
and applied settings. In [143], reward-modulated STDP was
shown to train the decision layer of a convolutional SNN us-
ing first-spike temporal coding, with the key observation that
R-STDP extracts task-discriminative features. In contrast, un-
supervised STDP extracts any recurring pattern. A hybrid
strategy combining unsupervised STDP in early convolutional
layers with R-STDP in classification layers was demonstrated
in [144], and R-STDP has been applied to end-to-end sensori-
motor tasks including lane keeping [145] and target-reaching
navigation [146], illustrating the rule’s suitability for event-
driven robotic control.
e-prop [91] factorizes loss gradients into synapse-local eligi-
bility traces propagated forward in time and a top-down learn-
ing signal available online, fitting exactly the three-factor tem-
plate. Applied to an evidence-accumulation task requiring in-
tegration of cues over hundreds of timesteps, e-prop with adap-
tive LIF neurons succeeded where standard LIF neurons could
not, demonstrating that slow neuronal dynamics are critical for
temporal credit assignment under delayed rewards.
More recently, deep RL methods have been adapted to train
SNNs using surrogate gradients directly. A pivotal contribu-
tion was the Population-coded Spiking Actor Network (Pop-
SAN) [147], which uses population coding at the input and
output layers to increase representational capacity. PopSAN
trains a spiking actor network alongside a conventional deep
critic using standard policy optimization algorithms [148–150];
the critic supplies the policy gradient during training and is dis-
carded at deployment, so only the spiking actor runs on neu-
romorphic hardware. This hybrid actor-critic design has be-
come the dominant template for deep spiking RL: it inherits the
training stability of established deep RL pipelines while con-
fining the energy-efficient spiking inference to the deployed
11

--- PAGE 12 ---

policy. Deployed on Intel’s Loihi neuromorphic chip, Pop-
SAN achieved competitive performance on continuous-control
benchmarks [151] with reported energy savings of two orders
of magnitude relative to GPU baselines, establishing population
coding as a key enabler for scaling spiking RL to continuous
action spaces. Subsequent work improved on this paradigm:
in [152], a multi-scale dynamic coding scheme outperformed
both conventional actor networks and PopSAN on locomotion
tasks. In contrast, in [153], a fully spiking deep Q-network
(DSQN) was proposed that uses the membrane voltage of non-
spiking output neurons to represent Q-values, achieving com-
petitive performance on 17 Atari games without recourse to an
auxiliary ANN critic. A directly trained spiking Q-network was
also demonstrated in [154], addressing noisy value estimation
inherent in rate-coded spike outputs. The fully spiking actor
network with intralayer connections (ILC-SAN) [155] further
closed the performance gap with mainstream deep RL on con-
tinuous control by introducing biologically inspired lateral con-
nectivity within spiking layers. Surrogate-gradient spiking RL
has also been applied to event-driven robotic settings: in [156]
spatio-temporal backpropagation was combined with RL for
UA V obstacle avoidance using DVS inputs, with deployment
on a neuromorphic accelerator.
From the perspective of the proposed taxonomy, spiking RL
methods span a wide locality range: classical R-STDP rules
are both spatially and temporally local and map naturally onto
neuromorphic hardware [157], but are limited to shallow ar-
chitectures and simple tasks; e-prop achieves temporal local-
ity while remaining spatially non-local; and surrogate-gradient
methods inherit the non-locality of backpropagation while cur-
rently achieving the strongest results on complex benchmarks.
The central open challenge is closing the performance gap be-
tween highly local, hardware-friendly rules and globally trained
deep spiking RL systems, with spiking world models represent-
ing a recent step toward richer model-based settings [158].
4.2.2. ANN-to-SNN Conversion
ANN-to-SNN conversion sidesteps the core difficulties of di-
rect SNN training, non-differentiable spikes, temporal credit as-
signment, and the need for spiking-aware optimization, by of-
floading learning entirely to a standard ANN trained with back-
propagation and subsequently mapping the resulting parameters
to a spiking counterpart. Because the approach inherits the ma-
ture toolchain and scalability of conventional deep learning, it
has historically achieved some of the highest accuracy on static
vision benchmarks. It remains the most accessible route to de-
ploying large pretrained models on neuromorphic hardware.
The theoretical basis is the observation that the firing rate of
an integrate-and-fire neuron receiving constant input approx-
imates a ReLU activation: overTtimesteps with reset-by-
subtraction, the average spike count converges to the analog
activation with errorO(1/T) [159, 160]. The standard pipeline
trains a deep ReLU-based ANN (e.g., VGG, ResNet), then re-
places each activation with a spiking neuron (typically LIF or
Integrate and Fire (IF)), folds batch-normalization parameters
into preceding linear layers, and rescales weights and thresh-
olds so that firing rates remain in a functional range [160, 161].
In [159], the ReLU–IF equivalence was first formalized for con-
volutional architectures; in [161] data-driven weight normal-
ization and threshold balancing yielded near-lossless MNIST
conversion; and in [160] the framework was extended to han-
dle batch normalization, max-pooling, biases, and softmax, ac-
companied by a percentile-based threshold calibration that be-
came the de facto standard. Scalability to deep residual archi-
tectures and the complete ImageNet benchmark was demon-
strated in [162], although at the cost of up to∼2,500 simulation
timesteps for ResNet architectures.
Two intertwined limitations have driven subsequent research.
First, the mismatch between continuous activations and dis-
crete spike counts introduces anaccuracy gapwhose sources
were systematically decomposed into clipping error (bounded
firing rates cannot represent large activations), quantization er-
ror (onlyT+1 discrete output levels exist), and unevenness error
(asynchronous spike propagation distorts layer-wise input dis-
tributions) [163]. Second, rate-coded conversion requires many
timesteps for accurate firing-rate estimation, resulting inhigh
inference latencythat erodes the energy advantage of spiking
execution.
Addressing these bottlenecks has proceeded along two com-
plementary axes. On thelow-latencyfront, in [164] the residual
membrane potential (soft-reset) neuron was shown to eliminate
the systematic negative bias of hard-reset neurons, reducing
the required timesteps from thousands to hundreds. Temporal-
switch coding was proposed in [165] to exploit spike timing
rather than rate, achieving an order-of-magnitude reduction in
latency. A particularly influential contribution was the Quan-
tization Clip-Floor-Shift (QCFS) activation function [163],
which replaces ReLU during ANN training so that the source
network already produces outputs matching the quantization
resolution ofTspiking timesteps; this was the first method
to achieve competitive conversion atT=4. Subsequent work
pushed latency further through optimized membrane poten-
tial initialization [166], iterative retraining down to a single
timestep [167], and conversion from quantized ANNs that for-
mally establishes the equivalence betweenT-timestep spiking
inference and∼log 2(T)-bit weight quantization [168]. On the
calibrationaxis, post-training correction methods adjust thresh-
olds and other parameters using only a small calibration set
(often∼128 images), avoiding full retraining. In [169], layer-
wise activation transplanting was introduced, enabling conver-
sion of efficient architectures such as MobileNet for the first
time; in [170], a shift-threshold-ReLU formulation provided
analytically grounded bias correction; and in [171], a second-
order error analysis extended calibration to object detection on
MS COCO with privacy-preserving synthetic data.
A third line of work blurs the boundary between conversion
and direct training. Hybrid schemes use converted weights as
initialization and then fine-tune with surrogate-gradient back-
propagation, jointly optimizing membrane leak, firing thresh-
old, and synaptic weights to achieve strong accuracy at very
low latency [172]; progressive tandem learning [173] and op-
timized few-spike neuron models [174] similarly combine the
strengths of both paradigms. A conversion to a detection ar-
chitecture was first demonstrated with Spiking-YOLO [175],
12

--- PAGE 13 ---

which introduced channel-wise normalization and signed neu-
rons to map Leaky-ReLU activations. Most recently, the fron-
tier has shifted to Transformer architectures, where softmax,
layer normalization, and multiplicative attention lack natural
spiking equivalents. In [176], exact mathematical equivalence
between quantized Transformers and converted SNNs was es-
tablished through spike-based softmax and layer-normalization
operators, and in [177], training-free Transformer-to-SNN con-
version was achieved for both vision and NLP models with min-
imal accuracy degradation.
All learning occurs in the ANN domain via dense backprop-
agated gradients, and the SNN is obtained through a separate
mapping and optional calibration stage. This makes conversion
highly practical, it is the easiest route to deploying existing pre-
trained models on neuromorphic hardware, and it has delivered
some of the highest reported accuracies on static vision bench-
marks. However, it carries fundamental limitations that moti-
vate the emphasis on direct training in this survey. Conversion
inherently decouples learning from spiking dynamics: the net-
work never trains on spike-based representations, limiting its
ability to exploit temporal coding, adapt to event-driven inputs,
or perform on-chip learning. Even state-of-the-art low-latency
methods typically rely on rate coding and require strict archi-
tectural constraints (e.g., ReLU-only activations, folded nor-
malization), and the accuracy gap, while dramatically reduced,
tends to widen on tasks that require fine temporal structure,
such as neuromorphic event-stream processing. Furthermore,
conversion offers no path toward on-device adaptation, a cen-
tral goal for neuromorphic systems operating in non-stationary
environments. We therefore treat conversion primarily as an
important reference point and upper-bound baseline when eval-
uating the direct, local training methods that form the core of
this work.
4.2.3. Optimization
Gradient-free methods optimize SNN parameters by treating
the network as a black box evaluated against a fitness func-
tion, entirely sidestepping the non-differentiability of spiking
dynamics. Credit is assigned through population-level fitness
comparisons or global perturbation–reward correlations rather
than through local synaptic quantities.
Evolutionary parameter and topology optimization.Evolu-
tionary algorithms were among the earliest methods applied
to SNN training. Genetic algorithms were used in [178] to
evolve synaptic weights of spiking controllers for robot navi-
gation, and differential evolution was shown in [179] to solve
supervised classification tasks with compact spiking architec-
tures. Multi-objective evolutionary search was applied in [180]
to co-optimize accuracy, weights, delays, and connectivity via
Pareto-based selection. A key strength of these methods is
their ability to jointly optimize discrete and continuous pa-
rameters, connectivity masks, axonal delays, firing thresholds,
that gradient methods cannot handle natively. When the goal
extends to discovering network structure, NEAT-based neu-
roevolution has been adapted to spiking neurons for control
tasks [181] and deployed on neuromorphic hardware [182],
while the EONS framework [183] provides general-purpose co-
evolution of topology, weights, and neuron-level parameters for
neuromorphic deployment. More recently, evolution strategies
have been applied to evolve sparse connectivity distributions for
recurrent SNNs [184], and differential evolution with cosine-
annealing schedules has been used to train deeper architectures
on CIFAR-10/100 [185]. Neural architecture search extends
these ideas to structured, cell-based search spaces: approaches
such as AutoSNN [186] and SpikeDHS [187] use evolutionary
or differentiable outer search. However, their inner-loop weight
training typically relies on surrogate-gradient BPTT, making
their taxonomic status ambiguous. A comprehensive survey of
evolutionary methods for SNNs is provided in [50].
Perturbation-based and other gradient-free methods.An inter-
mediate class of methods estimates gradients through stochastic
perturbation. The foundational work of [188] proposed learn-
ing by correlating stochastic synaptic noise with a global reward
signal, and [189] extended this to estimate gradients by dy-
namically perturbing membrane conductances. More recently,
LocalZO [190] proposed neuron-level zeroth-order perturba-
tion with a formal connection to surrogate gradients, achiev-
ing competitive accuracy on CIFAR-10/100 and neuromorphic
datasets with training speedups over BPTT. Beyond evolution-
ary and perturbation-based approaches, particle swarm opti-
mization [191] and other metaheuristics [192] have been ap-
plied to SNN weight tuning, though exclusively on small-scale
tasks.
Limitations and outlook.Despite their flexibility, no purely
gradient-free method has yet matched the performance of
surrogate-gradient BPTT on large-scale benchmarks such as
ImageNet. The most competitive large-scale results come
from hybrid Network Architecture Search (NAS) approaches
that confine evolutionary search to the outer architectural loop
while relying on gradient-based weight training internally. The
genuine value of non-standard optimization lies in hardware-
constraint-aware search, multi-objective optimization over non-
differentiable quantities (energy, latency, spike count), and
compatibility with arbitrary neuron models and mixed discrete–
continuous parameter spaces. As neuromorphic deployment
matures and hardware constraints become first-class optimiza-
tion objectives, the role of these methods is poised to grow.
5. NeuroTrain framework
As discussed in the previous sections, the rapid emergence of
new training algorithms in the neuromorphic computing com-
munity makes the field increasingly difficult to track and, more
importantly, makes fair comparison challenging. Training al-
gorithms are often introduced in separate codebases with het-
erogeneous datasets, preprocessing pipelines, network architec-
tures, optimization procedures, and reporting conventions. As
a result, it is often difficult to separate the actual contribution of
a training algorithm from the particular experimental choices
used to evaluate it.
13

--- PAGE 14 ---

Algorithm Year
Local
in time
Local
in space Traces
STDP-
inspired
Spatial BP+
online temp.
Feedback
align.
Local
class./readout
Early approaches
SpikeProp [21] 2002
Tempotron [65] 2006◦
ReSuMe [20] 2010 X X X X
SW AT [66] 2010 X X
SPAN [63] 2012◦X
Chronotron [64] 2012◦
Enabling backpropagation in SNNs
Lee et al. [67] 2016
STBP [68] 2018
SuperSpike [70] 2018 X X◦
SLAYER [71] 2018
EXODUS [73] 2023
Trace-centric&spatial BP with online temporal credit
E-prop [91] 2020 X X
OTTT [94] 2022 X X X
OSTL [92] 2023 X X X
SLTT [95] 2023 X X
FPTT [93] 2023 X
S-TLLR [97] 2024 X X X X
OTPE [98] 2024 X X X
STOP [96] 2025 X X X
ES-D-RTRL/BrainScale [99] 2025 X X
STDP-based supervised locality
SSTDP [89] 2017 X X X
S2-STDP [90] 2024 X X X X
Spatial locality via local classifiers
DECOLLE [100] 2020 X X X X
ELL [101] 2023 X X X
BELL [101] 2023 X X
FELL [101] 2023 X X X X
STDL [102] 2025 X X◦X
FF-SNN [110] 2026 X X
Spatial locality via feedback alignment
ST-DFA [103] 2020 DFA
OSTTP [105] 2023 X X X DRTP
ETLP [104] 2024 X X X DRTP
STSF [106] 2025 X X X DFA◦
Fully local approaches
TESS [107] 2025 X X X X X
TP [108] 2026 X X X
Table 2: Taxonomy ofSuperviseddirect-training algorithms for SNNs.Local in time/space: adherence to temporal or spatial locality.Traces: uses eligibility
traces.STDP-inspired: learning rule inspired by spike-timing-dependent plasticity.Spatial BP+online temp.: retains spatial backpropagation per timestep
while handling temporal credit assignment online.Feedback align.: uses direct feedback alignment (DFA) or direct random target projection (DRTP).Local
class./readout: employs auxiliary per-layer classifiers or readout heads. X=present,◦=partial/approximate, empty=absent.
14

--- PAGE 15 ---

A similar challenge has recently been addressed at the
broader level of neuromorphic computing by NeuroBench
[193], a community-driven benchmarking framework designed
to support fair and consistent evaluation of neuromorphic meth-
ods and systems, with particular focus on shared tasks, datasets,
metrics, and software tools. Inspired by the same need for
transparency, reproducibility, and comparability, we introduce
NeuroTrain, an open framework specifically tailored for im-
plementing, comparing, and benchmarking SNN training al-
gorithms. NeuroTrain is conceived as a community-oriented
resource where researchers can contribute implementations of
training algorithms within a shared, standardized environment.
In its current version, the framework includes a set of repre-
sentative state-of-the-art learning rules. Its objective, however,
is not to declare a universally best rule, but rather to provide
a common setup in which different approaches can be imple-
mented, analyzed, and compared under consistent conditions.
Figure 3 illustrates the overall organization of NeuroTrain.
The framework is designed around two main principles:
modularityandcompartmentalization. Modularity makes Neu-
roTrain easily extensible, allowing new datasets, models, and
learning rules to be added with limited effort. Compartmental-
ization keeps the different components isolated, reducing un-
intended interactions and experimental artifacts that may bias
results. Most importantly, this design promotes orthogonality
across the framework’s elements, enabling systematic combi-
nations of datasets, models, and trainers whenever supported
by the corresponding learning rule. Among the SNN soft-
ware frameworks currently available, including snnTorch [54],
SLAYER [71], and SpikingJelly [194], we chose to build Neu-
roTrain on top of snnTorch. This choice is motivated by its
broad adoption in the research community, active maintenance,
and tight integration with PyTorch, which provides a flexible
and robust software foundation for implementing and bench-
marking learning algorithms.
Neurotrain foundation comprises three main building blocks
realized as abstract Python classes: (i)dataloaders, (ii)models,
and (iii)trainers.
5.1. Dataloaders
Since benchmarking training algorithms necessarily depends
on the availability of datasets, NeuroTrain begins from this
component. To avoid overlap with initiatives such as Neu-
roBench, NeuroTrain does not aim to define a new dataset
suite. Instead, it provides a standardized dataloader interface
that allows developers to uniformly integrate datasets into the
framework. The current version includes dataloaders for sev-
eral widely used neuromorphic and rate-encoded datasets, in-
cluding those available through NeuroBench [193] and Tonic
[195], while preserving the ability to add new ones in the fu-
ture.
5.2. Models
Network models are particularly important when benchmark-
ing training algorithms. Although many papers refer to com-
mon architectures such as VGG-style models or standard feed-
forward and recurrent networks, their actual implementations
often differ in subtle but important ways and are frequently
tightly coupled to the learning rule under study. While such
tight integration may be effective for demonstrating the best-
case performance of a specific algorithm, it complicates fair
comparison. For this reason, NeuroTrain adopts a different ap-
proach: it enforces a clear separation between learning rules
and network models, provides guidelines for representing net-
works within the framework, and includes a library of bench-
mark models. The current library spans fully connected feed-
forward networks, recurrent models, deep architectures, pure
LIF-based networks, and mixed convolutional models. At
present, all benchmark networks rely on the standard LIF neu-
ron model available in snnTorch, although the framework can
be extended with custom neuron models when needed.
5.3. Trainers
The third pillar of NeuroTrain is the set oftrainers. Train-
ers are Python classes integrated within the snnTorch environ-
ment that implement specific learning rules. They follow a
common interface so that, whenever compatible, they can oper-
ate directly with all supported dataloaders and network models.
This provides the basis for orthogonal benchmarking of learn-
ing rules across shared tasks and architectures. Naturally, this
orthogonality has practical limits: some rules may not apply
to certain model classes, such as deep convolutional architec-
tures, and therefore cannot be evaluated on the corresponding
datasets. Nevertheless, the common trainer abstraction substan-
tially improves the consistency and breadth of comparisons.
5.4. Benchmarking framework
In addition to its three main components, NeuroTrain pro-
vides abenchmarking enginethat automates the execution of
experiments generated by systematically combining trainers,
models, and datasets, while collecting relevant evaluation met-
rics. The compartmentalized design of the framework ensures
that different learning algorithms are executed within the same
software environment and under consistent experimental condi-
tions, thereby enabling fairer, more reproducible comparisons.
NeuroTrain supports two main execution modes:campaign
andcustom. In campaign mode, the framework automatically
generates an orthogonal experimental campaign by combining
selected dataloaders, models, and trainers. During campaign
generation, NeuroTrain automatically excludes invalid configu-
rations whenever incompatibilities arise between a trainer and a
model, or between a model and a dataset. To preserve encapsu-
lation, such incompatibilities are defined within the correspond-
ing objects, namely trainers, dataloaders, and models, and are
made available to the NeuroTrain engine during experimental
setup. We acknowledge that this form of standardization may
not always reproduce the absolute best performance achievable
by each algorithm, since some methods may benefit from cus-
tomized implementations, specialized architectures, or highly
tuned experimental settings. However, the broader objective of
NeuroTrain is to move beyond isolated, algorithm-specific eval-
uation scripts toward an open benchmarking ecosystem for the
SNN community, similar to the role shared libraries and bench-
marks play in other areas of artificial intelligence.
15

--- PAGE 16 ---

FrameworkTrainersTrainer 1Trainer 2···Trainer NCustom trainer
ModelsSNN FCSNN ConvolutionalSNN RecurrentVGG-SNNCustom model
DatasetsDataset 1Dataset 2···Dataset NCustom dataset
TrainerModelDataLoader
neurotrain.py--campaign benchmarking.yaml∀trainer ×model ×datasetruns Experimentinstantiates classesResultsaccuracy
Trainer 1Trainer 2Trainer NCustom trainer··· Custom trainerSNN FCSNN ConvSNN RecVGG-SNNCustom model············ ···
Trainer 1Trainer 2Trainer NCustom trainer··· Custom trainerSNN FCSNN ConvSNN RecVGG-SNNCustom model············ ···
Benchmarking Results on Dataset 1Trainer 1Trainer 2Trainer NCustom trainer··· Custom trainerSNN FCSNN ConvSNN RecVGG-SNNCustom model············ ···
Accuracyhighlown/a
neurotrain.py--custom experiment.yamlruns ExperimentResultsaccuracy
Figure 3: NeuroTrain framework and benchmarking workflow. The framework organizes SNN training experiments around modular trainers, models, and datasets,
including user-defined extensions. A campaign configuration automatically runs all trainer–model–dataset combinations, while a custom configuration executes a
single experiment. Results are collected as accuracy scores and summarized in benchmark matrices for systematic comparison across methods.
To address the need for more targeted evaluations, Neuro-
Train also provides a custom execution mode. This mode al-
lows users to define specific experiments to answer particular
research questions or to stress-test a given training algorithm,
model, or dataset. A custom experiment is defined as a prede-
fined combination of a trainer, a model, and a dataset, possibly
accompanied by user-specified hyperparameters and execution
settings.
To further improve fairness, NeuroTrain integratesOptuna
[196] for hyperparameter optimization. This allows each train-
ing algorithm to be evaluated using a tuned set of hyperparame-
ters rather than arbitrary fixed settings. The framework reports
a range of metrics relevant to training and benchmarking, in-
cluding training accuracy, test accuracy, loss, total execution
time, and time per epoch. In addition, for each network, Neu-
roTrain reports structural and efficiency-related quantities, such
as the number of parameters, memory footprint, and activation
sparsity.
To demonstrate the framework’s capabilities, the current re-
lease of NeuroTrain includes implementations of a represen-
tative set of learning rules surveyed in this paper. These im-
plementations reflect our effort to interpret the corresponding
papers and, whenever possible, to adapt existing code to Neu-
roTrain’s design principles. Consequently, some implementa-
tions may still be improved, refined, or extended. NeuroTrain
is therefore intended as an open and community-driven project,
and contributions from the community are strongly encouraged.
In this spirit, the set of implemented training algorithms, mod-
els, and datasets is expected to evolve over time, supporting the
continued development of the research community.
To showcase NeuroTrain’s benchmarking capabilities, Fig-
ure 4 presents a representative snapshot of the results available
at the time of submission. The snapshot refers to a benchmark-
ing campaign evaluating the available trainers across a set of
small-scale network models with different layer configurations
and connectivity patterns. Each experiment was run for 20
epochs, and hyperparameter exploration was performed using
Optuna with 10 trials per experiment. Further details on the ex-
perimental setup are provided in the official GitHub repository
(see section 6). Overall, the campaign required approximately
850 GPU hours.
The heatmap shows the test accuracy for each experiment.
Entries marked as N/S indicate configurations that are not
supported by the corresponding trainer or model. The fig-
ure illustrates how NeuroTrain enables systematic comparison
across trainers, network architectures, and tasks, thereby pro-
viding a compact overview of their interactions. These re-
sults are not intended to establish a definitive ranking of al-
gorithms. Rather, they demonstrate how NeuroTrain can sup-
port exploratory benchmarking and help identify research gaps
where further methodological improvements may be needed.
Because NeuroTrain is designed as a living, open resource
that will continue to evolve through new implementations, up-
dated configurations, and additional benchmark results, we de-
liberately avoid embedding the complete benchmark outcomes
in this paper. Instead, readers are referred to the official GitHub
repository, where the most recent implementations, configura-
tions, and benchmarking results will be maintained.
16

--- PAGE 17 ---

Conv-SNN FC-SNN R-SNN
BPTT
DECOLLE
E-prop
ESD-RTRL
ETLP
OSTL
OSTTP
OTTT
STSF
TP
44.9% 35.9% 34.3%
35.2% 39.9% N/S
N/S N/S 42.5%
56.9% 42.6% 31.1%
N/S 24.9% 26.1%
N/S 37.9% 23.7%
N/S 31.5% 21.5%
49.2% 34.9% 35.0%
N/S 27.7% N/S
54.7% 33.9% 34.8%
CIFAR-10
Conv-SNN FC-SNN R-SNN
37.9% 33.7% 34.0%
39.4% 36.1% N/S
N/S N/S 25.3%
23.3% 37.9% 19.1%
N/S 26.4% 30.8%
N/S 32.4% 32.3%
N/S 25.3% 10.0%
35.7% 29.7% 35.7%
N/S 19.9% N/S
33.3% 30.7% 33.8%
DVS-CIFAR10
Conv-SNN FC-SNN R-SNN
63.6% 68.9% 71.2%
78.4% 70.8% N/S
N/S N/S 66.7%
47.4% 73.1% 70.8%
N/S 63.6% 68.9%
N/S 71.2% 71.2%
N/S 69.3% 65.5%
57.6% 57.2% 60.6%
N/S 70.8% N/S
62.9% 68.6% 70.1%
DVSGesture
Conv-SNN FC-SNN R-SNN
82.9% 83.7% 82.8%
78.3% 80.1% N/S
N/S N/S 85.5%
80.8% 86.4% 67.8%
N/S 82.2% 80.7%
N/S 83.7% 83.2%
N/S 82.3% 81.0%
73.8% 80.7% 81.0%
N/S 80.0% N/S
84.6% 86.2% 85.9%
Fashion-MNIST
Conv-SNN FC-SNN R-SNN
BPTT
DECOLLE
E-prop
ESD-RTRL
ETLP
OSTL
OSTTP
OTTT
STSF
TP
98.9% 97.8% 96.9%
97.1% 95.7% N/S
N/S N/S 97.8%
96.3% 95.6% 82.7%
N/S 93.2% 91.3%
N/S 96.3% 96.5%
N/S 92.5% 92.1%
95.4% 93.2% 93.0%
N/S 93.3% N/S
98.2% 97.5% 97.4%
MNIST
Conv-SNN FC-SNN R-SNN
98.2% 96.8% 95.8%
95.5% 93.1% N/S
N/S N/S 96.0%
94.9% 95.8% 80.1%
N/S 88.8% 90.1%
N/S 93.2% 94.1%
N/S 91.0% 91.8%
80.2% 87.0% 88.2%
N/S 90.4% N/S
97.2% 96.3% 96.2%
N-MNIST
Conv-SNN FC-SNN R-SNN
N/S 49.6% 69.6%
N/S 37.5% N/S
N/S N/S 69.1%
N/S 51.0% 45.1%
N/S 26.0% 26.9%
N/S 23.6% 30.8%
N/S 28.0% 5.7%
N/S 26.4% 41.2%
N/S 22.1% N/S
N/S 49.8% 57.6%
SHD
Conv-SNN FC-SNN R-SNN
83.8% 53.6% 56.1%
55.9% 74.9% N/S
N/S N/S 59.6%
66.1% 73.2% 25.3%
N/S 36.1% 30.8%
N/S 61.8% 27.9%
N/S 30.0% 21.7%
79.5% 60.9% 58.3%
N/S 27.6% N/S
78.5% 45.7% 56.2%
SVHN
0% 20% 40% 60% 80% 100%
T est accuracy
Figure 4: Example of benchmarking results generated by NeuroTrain. Three architectures are benchmarked in variants tailored to the dataset. In the order MNIST,
F-MNIST, CIFAR-10, SVHN, N-MNIST, DVS Gesture, DVS CIFAR-10, SHD:FC(784-256-10/784-800-10/3072-1024-512-10/3072-1024-512-10/2312-
512-10/32768-2048-11/32768-1024-512-10/700-512-20),RC(784-256-10/784-256-10/3072-512-256-10/3072-512-256-10/2312-256-10/32768-1024-11
/32768-512-10/700-512-20), andConv(12C5-MP2-32C5-MP2-FC, fixed across datasets). Eprop replaces all multi-hidden-layer architectures with a single-
hidden-layer recurrent SNN with 512 units. Each experiment was run for 20 epochs, and hyperparameter exploration was performed using Optuna with 10 trials per
experiment for a total of about 850 GPU hours.
6. Conclusions and Future Challenges
This paper surveyed the rapidly evolving landscape of train-
ing algorithms for spiking neural networks, highlighting both
the diversity of existing approaches and the difficulty of com-
paring them fairly across heterogeneous experimental settings.
Beyond reviewing the main methodological families, we intro-
duced NeuroTrain, an open framework designed to support the
implementation, benchmarking, and comparison of SNN train-
ing rules within a standardized, common environment. By de-
coupling datasets, network models, training rules, and bench-
marking procedures, NeuroTrain aims to improve transparency,
reproducibility, and accessibility in this research area, while
fostering community-driven development of shared tools and
implementations.
As a takeaway, several important challenges remain open.
First, many training rules still exhibit limited portability across
datasets and architectures, making it difficult to assess their true
generality. Second, fair benchmarking requires not only com-
mon software interfaces but also careful treatment of hyperpa-
rameter optimization, computational cost, memory usage, spar-
sity, and scalability. Third, the field would benefit from stronger
17

--- PAGE 18 ---

convergence between algorithmic benchmarking and hardware-
aware evaluation, especially as neuromorphic systems move to-
ward real-world deployment. Future work will therefore fo-
cus on extending NeuroTrain with additional training rules,
broader dataset and model coverage, richer benchmarking met-
rics, and tighter integration with neuromorphic benchmarking
initiatives and hardware-oriented evaluation flows. In this per-
spective, NeuroTrain is intended not as a final benchmark, but
as an evolving foundation for more systematic and reproducible
progress in SNN training research.
Data A vailability and use of AI
The NeuroTrain framework and its associated implementa-
tions are publicly available at the official GitHub repository:
https://github.com/smilies-polito/neurotrain.
Generative AI tools were used to support language editing,
proofreading, and the improvement of writing clarity. They
were also used to assist in identifying potentially relevant lit-
erature. All suggested references were subsequently verified,
selected, and analyzed by the authors. The scientific content,
interpretation of the literature, and final manuscript remain the
sole responsibility of the authors.
References
[1] W. Maass, Networks of spiking neurons: The third
generation of neural network models, Neural Net-
works 10 (9) (1997) 1659–1671.doi:10.1016/
S0893-6080(97)00011-7.
[2] M. Davies, N. Srinivasa, T.-H. Lin, G. Chinya, Y . Cao,
S. H. Choday, G. Dimou, P. Joshi, N. Imam, S. Jain,
Y . Liao, C.-K. Lin, A. Lines, R. Liu, D. Mathaikutty,
S. McCoy, A. Paul, J. Tse, G. Venkataramanan, Y .-H.
Weng, A. Wild, Y . Yang, H. Wang, Loihi: A Neuromor-
phic Manycore Processor with On-Chip Learning, IEEE
Micro 38 (1) (2018) 82–99.doi:10.1109/MM.2018.
112130359.
[3] B. Huo, F. Li, S. Peng, H. Chen, S. Xin, H. Wang,
Research on SNN Learning Algorithms and Networks
Based on Biological Plausibility, IEEE Access 13 (2025)
95243–95256.doi:10.1109/ACCESS.2025.3566717.
[4] P. Lansky, S. Ditlevsen, A review of the methods for
signal estimation in stochastic diffusion leaky integrate-
and-fire neuronal models, Biological cybernetics 99 (4)
(2008) 253–262.doi:10.1007/s00422-008-0237-x.
[5] Y . Guo, X. Huang, Z. Ma, Direct learning-based deep
spiking neural networks: a review, Frontiers in Neuro-
science 17 (Jun. 2023).doi:10.3389/fnins.2023.
1209795.
[6] B. Mészáros, J. C. Knight, T. Nowotny, Efficient event-
based delay learning in spiking neural networks, Nature
Communications 16 (1) (2025) 10422.doi:10.1038/
s41467-025-65394-8.
[7] M. Xiao, Q. Meng, Z. Zhang, Y . Wang, Z. Lin, SPIDE:
A purely spike-based method for training feedback
spiking neural networks, Neural Networks 161 (2023)
9–24.doi:https://doi.org/10.1016/j.neunet.
2023.01.026.
[8] G.-Q. Bi, Spatiotemporal specificity of synaptic plas-
ticity: cellular rules and mechanisms, Biological cy-
bernetics 87 (5) (2002) 319–332.doi:10.1007/
s00422-002-0349-7.
[9] C. Zha, W. S. Sossin, The molecular diversity of plas-
ticity mechanisms underlying memory: An evolutionary
perspective, Journal of neurochemistry 163 (6) (2022)
444–460.doi:10.1111/jnc.15717.
[10] J. D. Sweatt, Neural plasticity and behavior–sixty years
of conceptual advances, Journal of neurochemistry 139
(2016) 179–199.doi:10.1111/jnc.13580.
[11] A. R. McFarlan, C. Y . Chou, A. Watanabe,
N. Cherepacha, M. Haddad, H. Owens, P. J.
Sjöström, The plasticitome of cortical interneurons,
Nature Reviews Neuroscience 24 (2) (2023) 80–97.
doi:10.1038/s41583-022-00663-9.
[12] D. Ivanov, A. Chezhegov, M. Kiselev, A. Grunin,
D. Larionov, Neuromorphic artificial intelligence sys-
tems, Frontiers in Neuroscience 16 (Sep. 2022).doi:
10.3389/fnins.2022.959626.
[13] A. Caviglia, F. Marostica, A. Carpegna, A. Savino,
S. Di Carlo, Sfatti: Spiking fpga accelerator for tem-
poral task-driven inference - a case study on mnist, in:
2025 IEEE International Conference on Image Process-
ing Workshops (ICIPW), 2025, pp. 59–64.doi:10.
1109/ICIPW68931.2025.11385983.
[14] J. Pedersen, et al., Spinnaker 2: A 10 million core pro-
cessor system for brain simulation and machine learning,
Communicating Process Architectures 2017 & 2018:
WoTUG-39 & WoTUG-40 70 (2019) 277.doi:10.
3233/978-1-61499-949-2-277.
[15] A. Carpegna, A. Savino, S. D. Carlo, Spiker+: A frame-
work for the generation of efficient spiking neural net-
works fpga accelerators for inference at the edge, IEEE
Transactions on Emerging Topics in Computing 13 (3)
(2025) 784–798.doi:10.1109/TETC.2024.3511676.
[16] F. Akopyan, J. Sawada, A. Cassidy, R. Alvarez-Icaza,
J. Arthur, P. Merolla, N. Imam, Y . Nakamura, P. Datta,
G.-J. Nam, B. Taba, M. Beakes, B. Brezzo, J. B. Kuang,
R. Manohar, W. P. Risk, B. Jackson, D. S. Modha,
TrueNorth: Design and Tool Flow of a 65 mW 1 Mil-
lion Neuron Programmable Neurosynaptic Chip, IEEE
Transactions on Computer-Aided Design of Integrated
Circuits and Systems 34 (10) (2015) 1537–1557.doi:
10.1109/TCAD.2015.2474396.
18

--- PAGE 19 ---

[17] B. V . Benjamin, P. Gao, E. McQuinn, S. Choudhary,
A. R. Chandrasekaran, J.-M. Bussat, R. Alvarez-Icaza,
J. V . Arthur, P. A. Merolla, K. Boahen, Neurogrid:
A Mixed-Analog-Digital Multichip System for Large-
Scale Neural Simulations, Proceedings of the IEEE
102 (5) (2014) 699–716.doi:10.1109/JPROC.2014.
2313565.
[18] F. Marostica, A. Carpegna, A. Savino, S. D. Carlo,
Energy-efficient digital design: A comparative study
of event-driven and clock-driven spiking neurons, in:
2025 IEEE Computer Society Annual Symposium on
VLSI (ISVLSI), V ol. 1, 2025, pp. 1–6.doi:10.1109/
ISVLSI65124.2025.11130320.
[19] F. Ponulak, A. Kasinski, Introduction to spiking neural
networks: Information processing, learning and applica-
tions, Acta Neurobiologiae Experimentalis 71 (4) (2011)
409–433.doi:10.55782/ane-2011-1862.
[20] F. Ponulak, A. Kasi ´nski, Supervised Learning in Spik-
ing Neural Networks with ReSuMe: Sequence Learning,
Classification, and Spike Shifting, Neural Computation
22 (2) (2010) 467–510.doi:10.1162/neco.2009.
11-08-901.
[21] S. M. Bohte, J. N. Kok, H. La Poutré, Error-
backpropagation in temporally encoded networks of
spiking neurons, Neurocomputing 48 (1) (2002) 17–37.
doi:10.1016/S0925-2312(01)00658-0.
[22] M. Pfeiffer, T. Pfeil, Deep Learning With Spiking Neu-
rons: Opportunities and Challenges, Frontiers in Neuro-
science 12 (Oct. 2018).doi:10.3389/fnins.2018.
00774.
[23] A. Tavanaei, M. Ghodrati, S. R. Kheradpisheh,
T. Masquelier, A. Maida, Deep learning in spiking neu-
ral networks, Neural Networks 111 (2019) 47–63.doi:
10.1016/j.neunet.2018.12.002.
[24] X. Wang, X. Lin, X. Dang, Supervised learning in spik-
ing neural networks: A review of algorithms and eval-
uations, Neural Networks 125 (2020) 258–280.doi:
10.1016/j.neunet.2020.02.011.
[25] A. Vigneron, J. Martinet, A critical survey of STDP in
Spiking Neural Networks for Pattern Recognition, in:
2020 International Joint Conference on Neural Networks
(IJCNN), 2020, pp. 1–9.doi:10.1109/IJCNN48605.
2020.9207239.
[26] A. Taherkhani, A. Belatreche, Y . Li, G. Cosma, L. P.
Maguire, T. M. McGinnity, A review of learning in bio-
logically plausible spiking neural networks, Neural Net-
works 122 (2020) 253–272.doi:10.1016/j.neunet.
2019.09.036.
[27] K. Roy, A. Jaiswal, P. Panda, Towards spike-based ma-
chine intelligence with neuromorphic computing, Na-
ture 575 (7784) (2019) 607–617.doi:10.1038/
s41586-019-1677-2.
[28] S. Dora, N. Kasabov, Spiking Neural Networks for Com-
putational Intelligence: An Overview, Big Data and
Cognitive Computing 5 (4) (2021) 67.doi:10.3390/
bdcc5040067.
[29] D.-A. Nguyen, X.-T. Tran, F. Iacopi, A Review of Al-
gorithms and Hardware Implementations for Spiking
Neural Networks, Journal of Low Power Electronics
and Applications 11 (2) (2021) 23.doi:10.3390/
jlpea11020023.
[30] D. V . Christensen, R. Dittmann, B. Linares-Barranco,
A. Sebastian, M. Le Gallo, A. Redaelli, S. Slesazeck,
T. Mikolajick, S. Spiga, S. Menzel, I. Valov, G. Mi-
lano, C. Ricciardi, S.-J. Liang, F. Miao, M. Lanza, T. J.
Quill, S. T. Keene, A. Salleo, J. Grollier, D. Markovi ´c,
A. Mizrahi, P. Yao, J. J. Yang, G. Indiveri, J. P. Strachan,
S. Datta, E. Vianello, A. Valentian, J. Feldmann, X. Li,
W. H. P. Pernice, H. Bhaskaran, S. Furber, E. Neftci,
F. Scherr, W. Maass, S. Ramaswamy, J. Tapson, P. Panda,
Y . Kim, G. Tanaka, S. Thorpe, C. Bartolozzi, T. A.
Cleland, C. Posch, S. Liu, G. Panuccio, M. Mahmud,
A. N. Mazumder, M. Hosseini, T. Mohsenin, E. Do-
nati, S. Tolu, R. Galeazzi, M. E. Christensen, S. Holm,
D. Ielmini, N. Pryds, 2022 roadmap on neuromorphic
computing and engineering, Neuromorphic Computing
and Engineering 2 (2) (2022) 022501.doi:10.1088/
2634-4386/ac4a83.
[31] J. D. Nunes, M. Carvalho, D. Carneiro, J. S. Cardoso,
Spiking Neural Networks: A Survey, IEEE Access 10
60738–60764.doi:10.1109/ACCESS.2022.3179968.
[32] C. D. Schuman, S. R. Kulkarni, M. Parsa, J. P. Mitchell,
P. Date, B. Kay, Opportunities for neuromorphic com-
puting algorithms and applications, Nature Computa-
tional Science 2 (1) (2022) 10–19.doi:10.1038/
s43588-021-00184-y.
[33] A. Shrestha, H. Fang, Z. Mei, D. P. Rider, Q. Wu, Q. Qiu,
A survey on neuromorphic computing: Models and
hardware, IEEE Circuits and Systems Magazine 22 (2)
(2022) 6–35.doi:10.1109/MCAS.2022.3166331.
[34] K. Yamazaki, V .-K. V o-Ho, D. Bulsara, N. Le, Spik-
ing Neural Networks and Their Applications: A Re-
view, Brain Sciences 12 (7) (2022) 863.doi:10.3390/
brainsci12070863.
[35] L. Khacef, P. Klein, M. Cartiglia, A. Rubino, G. Indi-
veri, E. Chicca, Spike-based local synaptic plasticity: a
survey of computational models and neuromorphic cir-
cuits, Neuromorphic Computing and Engineering 3 (4)
(2023) 042001.doi:10.1088/2634-4386/ad05da.
[36] P. Pietrzak, S. Szczesny, D. Huderek, L. Przyborowski,
Overview of Spiking Neural Network Learning Ap-
proaches and Their Computational Complexities, Sen-
sors 23 (6) (2023) 3037.doi:10.3390/s23063037.
19

--- PAGE 20 ---

[37] N. Rathi, I. Chakraborty, A. Kosta, A. Sengupta,
A. Ankit, P. Panda, K. Roy, Exploring Neuromorphic
Computing Based on Spiking Neural Networks: Algo-
rithms to Hardware, ACM Comput. Surv. 55 (12) (2023)
243:1–243:49.doi:10.1145/3571155.
[38] S. Al Abdul Wahid, A. Asad, F. Mohammadi, A Sur-
vey on Neuromorphic Architectures for Running Artifi-
cial Intelligence Algorithms, Electronics 13 (15) (2024)
2963.doi:10.3390/electronics13152963.
[39] C. Frenkel, D. Bol, G. Indiveri, Bottom-Up and Top-
Down Approaches for the Design of Neuromorphic Pro-
cessing Systems: Tradeoffs and Synergies Between Nat-
ural and Artificial Intelligence, Proceedings of the IEEE
111 (6) (2023) 623–652.doi:10.1109/JPROC.2023.
3273520.
[40] Z. Yi, J. Lian, Q. Liu, H. Zhu, D. Liang, J. Liu, Learning
rules in spiking neural networks: A survey, Neurocom-
puting 531 (2023) 163–179.doi:https://doi.org/
10.1016/j.neucom.2023.02.026.
[41] M. Dampfhoffer, T. Mesquida, A. Valentian, L. Anghel,
Backpropagation-Based Learning Techniques for Deep
Spiking Neural Networks: A Survey, IEEE Transactions
on Neural Networks and Learning Systems 35 (9) (2024)
11906–11921.doi:10.1109/TNNLS.2023.3263008.
[42] A. H. Khan, X. Cao, C. Luo, S. Zhang, W. Guo, V . N.
Katsikis, S. Li, Spiking Neural Networks: A Com-
prehensive Survey of Training Methodologies, Hard-
ware Implementations and Applications, Artificial Intel-
ligence Science and Engineering 1 (3) (2025) 175–207.
doi:10.23919/AISE.2025.000013.
[43] B. Ayasi, C. J. Carmona, M. Saleh, A. M. García-Vico, A
Practical Tutorial on Spiking Neural Networks: Compre-
hensive Review, Models, Experiments, Software Tools,
and Implementation Guidelines, Eng 6 (11) (2025) 304.
doi:10.3390/eng6110304.
[44] J. Wu, Y . Wang, Z. Li, L. Lu, Q. Li, A Review of
Computing with Spiking Neural Networks, Computers,
Materials & Continua 78 (3) (2024) 2909–2939.doi:
10.32604/cmc.2024.047240.
[45] Y . Hu, Q. Zheng, G. Li, H. Tang, G. Pan, Toward
Large-scale Spiking Neural Networks: A Comprehen-
sive Survey and Future Directions, preprint on arXiv
(Aug. 2024).doi:10.48550/arXiv.2409.02111.
[46] C. Zhou, H. Zhang, L. Yu, Y . Ye, Z. Zhou, L. Huang,
Z. Ma, X. Fan, H. Zhou, Y . Tian, Direct training high-
performance deep spiking neural networks: a review of
theories and methods, Frontiers in Neuroscience 18 (Jul.
2024).doi:10.3389/fnins.2024.1383844.
[47] Progress and Challenges in Large Scale Spiking
Neural Networks for AI and Neuroscience, preprint
on TechRxiv (2025).doi:10.36227/techrxiv.
174197995.54372833.
[48] M. Fatima Minhas, R. Vidya Wicaksana Putra,
F. Awwad, O. Hasan, M. Shafique, Continual Learn-
ing With Neuromorphic Computing: Foundations, Meth-
ods, and Emerging Applications, IEEE Access 13
(2025) 124824–124873.doi:10.1109/ACCESS.2025.
3588665.
[49] R. Mishra, M. Suri, A survey and perspective on neuro-
morphic continual learning systems, Frontiers in Neuro-
science 17 (May 2023).doi:10.3389/fnins.2023.
1149410.
[50] S. Shen, R. Zhang, C. Wang, R. Huang, A. Tuer-
hong, Q. Guo, Z. Lu, J. Zhang, L. Leng, Evolution-
ary spiking neural networks: a survey, Journal of Mem-
brane Computing 6 (4) (2024) 335–346.doi:10.1007/
s41965-024-00156-x.
[51] M. Karamimanesh, E. Abiri, M. Shahsavari, K. Hassanli,
A. van Schaik, J. Eshraghian, Spiking neural networks
on FPGA: A survey of methodologies and recent ad-
vancements, Neural Networks 186 (2025) 107256.doi:
10.1016/j.neunet.2025.107256.
[52] S. Mazurek, J. Caputa, J. K. Argasi ´nski, M. Wielgosz,
Three-factor learning in spiking neural networks: An
overview of methods and trends from a machine learn-
ing perspective, Patterns 6 (12) (2025) 101414.
URLhttps://www.sciencedirect.com/science/
article/pii/S2666389925002624
[53] J. Lin, S. Lu, M. Bal, A. Sengupta, Benchmarking Spik-
ing Neural Network Learning Methods With Varying Lo-
cality, IEEE Access 13 (2025) 113606–113617.doi:
10.1109/ACCESS.2025.3582564.
[54] J. K. Eshraghian, M. Ward, E. O. Neftci, X. Wang,
G. Lenz, G. Dwivedi, M. Bennamoun, D. S. Jeong,
W. D. Lu, Training Spiking Neural Networks Using
Lessons From Deep Learning, Proceedings of the IEEE
111 (9) (2023) 1016–1054.doi:10.1109/JPROC.
2023.3308088.
[55] Y .-C. Cheng, W.-X. Hu, Y .-L. He, J. Z. Huang, A
comprehensive multimodal benchmark of neuromorphic
training frameworks for spiking neural networks, En-
gineering Applications of Artificial Intelligence 159
(2025) 111543.doi:https://doi.org/10.1016/j.
engappai.2025.111543.
[56] P. Werbos, Backpropagation through time: what it does
and how to do it, Proceedings of the IEEE 78 (10) (1990)
1550–1560.doi:10.1109/5.58337.
[57] N. Frémaux, W. Gerstner, Neuromodulated Spike-
Timing-Dependent Plasticity, and Theory of Three-
Factor Learning Rules, Frontiers in Neural Circuits 9
(Jan. 2016).doi:10.3389/fncir.2015.00085.
20

--- PAGE 21 ---

[58] A. Nø kland, Direct Feedback Alignment Provides
Learning in Deep Neural Networks, in: Advances in
Neural Information Processing Systems, V ol. 29, Curran
Associates, Inc., 2016.
URLhttps://proceedings.
neurips.cc/paper/2016/hash/
d490d7b4576290fa60eb31b5fc917ad1-Abstract.
html
[59] C. Frenkel, M. Lefebvre, D. Bol, Learning Without
Feedback: Fixed Random Learning Signals Allow for
Feedforward Training of Deep Neural Networks, Fron-
tiers in Neuroscience 15 (Feb. 2021).doi:10.3389/
fnins.2021.629892.
[60] B. Schrauwen, J. Van Campenhout, Extending spike-
prop, in: 2004 IEEE International Joint Conference on
Neural Networks (IEEE Cat. No.04CH37541), V ol. 1,
2004, pp. 471–475.doi:10.1109/IJCNN.2004.
1379954.
[61] S. McKennoch, D. Liu, L. Bushnell, Fast Modifications
of the SpikeProp Algorithm, in: The 2006 IEEE In-
ternational Joint Conference on Neural Network Pro-
ceedings, 2006, pp. 3970–3977.doi:10.1109/IJCNN.
2006.246918.
[62] I. Sporea, A. Grüning, Supervised Learning in Mul-
tilayer Spiking Neural Networks, Neural Computation
25 (2) (2013) 473–509.doi:10.1162/NECO_a_00396.
[63] A. Mohemmed, S. Schliebs, S. Matsuda, N. Kasabov,
Span: spike pattern association neuron for learning
spatio-temporal spike patterns, International Journal of
Neural Systems 22 (04) (2012) 1250012.doi:10.
1142/S0129065712500128.
[64] R. V . Florian, The Chronotron: A Neuron That Learns
to Fire Temporally Precise Spike Patterns, PLOS ONE
7 (8) (2012) e40233.doi:10.1371/journal.pone.
0040233.
[65] R. Gütig, H. Sompolinsky, The tempotron: a neuron
that learns spike timing-based decisions, Nature Neuro-
science 9 (3) (2006) 420–428.doi:10.1038/nn1643.
[66] J. J. Wade, L. J. McDaid, J. A. Santos, H. M. Sayers,
SW AT: A Spiking Neural Network Training Algorithm
for Classification Problems, IEEE Transactions on Neu-
ral Networks 21 (11) (2010) 1817–1830.doi:10.1109/
TNN.2010.2074212.
[67] J. H. Lee, T. Delbruck, M. Pfeiffer, Training Deep Spik-
ing Neural Networks Using Backpropagation, Frontiers
in Neuroscience 10 (Nov. 2016).doi:10.3389/fnins.
2016.00508.
[68] Y . Wu, L. Deng, G. Li, J. Zhu, L. Shi, Spatio-Temporal
Backpropagation for Training High-Performance Spik-
ing Neural Networks, Frontiers in Neuroscience 12 (May
2018).doi:10.3389/fnins.2018.00331.
[69] E. O. Neftci, H. Mostafa, F. Zenke, Surrogate Gradi-
ent Learning in Spiking Neural Networks: Bringing the
Power of Gradient-Based Optimization to Spiking Neu-
ral Networks, IEEE Signal Processing Magazine 36 (6)
(2019) 51–63.doi:10.1109/MSP.2019.2931595.
[70] F. Zenke, S. Ganguli, SuperSpike: Supervised Learning
in Multilayer Spiking Neural Networks, Neural Compu-
tation 30 (6) (2018) 1514–1541.doi:10.1162/neco_
a_01086.
[71] S. B. Shrestha, G. Orchard, SLAYER: Spike Layer Error
Reassignment in Time, in: Advances in Neural Infor-
mation Processing Systems, V ol. 31, Curran Associates,
Inc., 2018.
URLhttps://proceedings.neurips.
cc/paper_files/paper/2018/hash/
82f2b308c3b01637c607ce05f52a2fed-Abstract.
html
[72] A. Amir, B. Taba, D. Berg, T. Melano, J. McKinstry,
C. Di Nolfo, T. Nayak, A. Andreopoulos, G. Gar-
reau, M. Mendoza, J. Kusnitz, M. Debole, S. Esser,
T. Delbruck, M. Flickner, D. Modha, A Low Power,
Fully Event-Based Gesture Recognition System, in:
2017 IEEE Conference on Computer Vision and Pat-
tern Recognition (CVPR), IEEE, Honolulu, HI, 2017,
pp. 7388–7397.doi:10.1109/CVPR.2017.781.
[73] F. C. Bauer, G. Lenz, S. Haghighatshoar, S. Sheik, EXO-
DUS: Stable and efficient training of spiking neural net-
works, Frontiers in Neuroscience 17 (Feb. 2023).doi:
10.3389/fnins.2023.1110444.
[74] F. Zenke, T. P. V ogels, The Remarkable Robustness
of Surrogate Gradient Learning for Instilling Complex
Function in Spiking Neural Networks, Neural Compu-
tation 33 (4) (2021) 899–925.doi:10.1162/neco_a_
01367.
[75] W. Fang, Z. Yu, Y . Chen, T. Masquelier, T. Huang,
Y . Tian, Incorporating Learnable Membrane Time Con-
stant To Enhance Learning of Spiking Neural Networks,
2021, pp. 2661–2671.
URLhttps://openaccess.thecvf.com/
content/ICCV2021/html/Fang_Incorporating_
Learnable_Membrane_Time_Constant_To_
Enhance_Learning_of_Spiking_ICCV_2021_
paper.html
[76] X. Yao, F. Li, Z. Mo, J. Cheng, GLIF: A Unified Gated
Leaky Integrate-and-Fire Neuron for Spiking Neural
Networks, Advances in Neural Information Processing
Systems 35 (2022) 32160–32171.
URLhttps://proceedings.neurips.
cc/paper_files/paper/2022/hash/
cfa8440d500a6a6867157dfd4eaff66e-Abstract-Conference.
html
21

--- PAGE 22 ---

[77] H. Zheng, Y . Wu, L. Deng, Y . Hu, G. Li, Going Deeper
With Directly-Trained Larger Spiking Neural Networks,
Proceedings of the AAAI Conference on Artificial Intel-
ligence 35 (12) (2021) 11062–11070.doi:10.1609/
aaai.v35i12.17320.
[78] Y . Kim, P. Panda, Revisiting Batch Normalization for
Training Low-Latency Deep Spiking Neural Networks
From Scratch, Frontiers in Neuroscience 15 (Dec. 2021).
doi:10.3389/fnins.2021.773954.
[79] C. Duan, J. Ding, S. Chen, Z. Yu, T. Huang, Tempo-
ral Effective Batch Normalization in Spiking Neural
Networks, Advances in Neural Information Processing
Systems 35 (2022) 34377–34390.
URLhttps://proceedings.neurips.
cc/paper_files/paper/2022/hash/
de2ad3ed44ee4e675b3be42aa0b615d0-Abstract-Conference.
html
[80] Y . Guo, Y . Zhang, Y . Chen, W. Peng, X. Liu, L. Zhang,
X. Huang, Z. Ma, Membrane Potential Batch Nor-
malization for Spiking Neural Networks, 2023, pp.
19420–19430.
URLhttps://openaccess.thecvf.com/content/
ICCV2023/html/Guo_Membrane_Potential_
Batch_Normalization_for_Spiking_Neural_
Networks_ICCV_2023_paper.html
[81] S. Deng, Y . Li, S. Zhang, S. Gu, Temporal efficient
training of spiking neural network via gradient re-
weighting, in: International Conference on Learning
Representations, 2022.
URLhttps://openreview.net/forum?id=
_XNtisL32jv
[82] Y . Guo, X. Tong, Y . Chen, L. Zhang, X. Liu, Z. Ma,
X. Huang, RecDis-SNN: Rectifying Membrane Poten-
tial Distribution for Directly Training Spiking Neural
Networks, 2022, pp. 326–335.
URLhttps://openaccess.thecvf.com/content/
CVPR2022/html/Guo_RecDis-SNN_Rectifying_
Membrane_Potential_Distribution_for_
Directly_Training_Spiking_Neural_CVPR_
2022_paper.html
[83] Y . Guo, Y . Chen, L. Zhang, X. Liu, Y . Wang, X. Huang,
Z. Ma, IM-Loss: Information Maximization Loss for
Spiking Neural Networks, Advances in Neural Informa-
tion Processing Systems 35 (2022) 156–166.
URLhttps://proceedings.neurips.
cc/paper_files/paper/2022/hash/
010c5ba0cafc743fece8be02e7adb8dd-Abstract-Conference.
html
[84] Q. Meng, M. Xiao, S. Yan, Y . Wang, Z. Lin, Z.-Q.
Luo, Training High-Performance Low-Latency Spiking
Neural Networks by Differentiation on Spike Represen-
tation, 2022, pp. 12444–12453.
URLhttps://openaccess.thecvf.com/
content/CVPR2022/html/Meng_Training_
High-Performance_Low-Latency_Spiking_
Neural_Networks_by_Differentiation_on_
Spike_CVPR_2022_paper.html
[85] S. Lian, J. Shen, Q. Liu, Z. Wang, R. Yan, H. Tang,
Learnable surrogate gradient for direct training spiking
neural networks, in: Proceedings of the Thirty-Second
International Joint Conference on Artificial Intelligence,
IJCAI ’23, Macao, P.R.China, 2023, pp. 3002–3010.
doi:10.24963/ijcai.2023/335.
[86] R. J. Williams, D. Zipser, A Learning Algorithm for
Continually Running Fully Recurrent Neural Networks,
Neural Computation 1 (2) (1989) 270–280.doi:10.
1162/neco.1989.1.2.270.
[87] G.-q. Bi, M.-m. Poo, Synaptic Modifications in Cultured
Hippocampal Neurons: Dependence on Spike Timing,
Synaptic Strength, and Postsynaptic Cell Type, Journal
of Neuroscience 18 (24) (1998) 10464–10472.doi:10.
1523/JNEUROSCI.18-24-10464.1998.
[88] S. Song, K. D. Miller, L. F. Abbott, Competitive Heb-
bian learning through spike-timing-dependent synaptic
plasticity, Nature Neuroscience 3 (9) (2000) 919–926.
doi:10.1038/78829.
[89] A. Shrestha, K. Ahmed, Y . Wang, Q. Qiu, Stable spike-
timing dependent plasticity rule for multilayer unsuper-
vised and supervised learning, in: 2017 International
Joint Conference on Neural Networks (IJCNN), 2017,
pp. 1999–2006.doi:10.1109/IJCNN.2017.7966096.
[90] G. Goupy, P. Tirilly, I. M. Bilasco, Paired competing neu-
rons improving STDP supervised local learning in spik-
ing neural networks, Frontiers in Neuroscience 18 (Jul.
2024).doi:10.3389/fnins.2024.1401690.
[91] G. Bellec, F. Scherr, A. Subramoney, E. Hajek, D. Salaj,
R. Legenstein, W. Maass, A solution to the learning
dilemma for recurrent networks of spiking neurons, Na-
ture Communications 11 (1) (2020) 3625.doi:10.
1038/s41467-020-17236-y.
[92] T. Bohnstingl, S. Wo´ zniak, A. Pantazi, E. Elefthe-
riou, Online Spatio-Temporal Learning in Deep Neu-
ral Networks, IEEE Transactions on Neural Networks
and Learning Systems 34 (11) (2023) 8894–8908.doi:
10.1109/TNNLS.2022.3153985.
[93] B. Yin, F. Corradi, S. M. Bohté, Accurate online train-
ing of dynamical spiking neural networks through for-
ward propagation through time, Nature Machine In-
telligence 5 (5) (2023) 518–527.doi:10.1038/
s42256-023-00650-4.
[94] M. Xiao, Q. Meng, Z. Zhang, D. He, Z. Lin, Online
Training Through Time for Spiking Neural Networks,
22

--- PAGE 23 ---

Advances in Neural Information Processing Systems 35
(2022) 20717–20730.
URLhttps://proceedings.neurips.
cc/paper_files/paper/2022/hash/
82846e19e6d42ebfd4ace4361def29ae-Abstract-Conference.
html
[95] Q. Meng, M. Xiao, S. Yan, Y . Wang, Z. Lin, Z.-Q.
Luo, Towards memory- and time-efficient backpropa-
gation for training spiking neural networks, in: 2023
IEEE/CVF International Conference on Computer Vi-
sion (ICCV), 2023, pp. 6143–6153.doi:10.1109/
ICCV51070.2023.00567.
[96] H. Gao, X. Zhou, Y . Lin, M. Tian, L. Liu, C. Shi, STOP:
spatiotemporal orthogonal propagation for weight-
threshold-leakage synergistic training of deep spik-
ing neural networks, Neuromorphic Computing and
Engineering 5 (4) (2025) 044001.doi:10.1088/
2634-4386/ae0a78.
[97] M. P. E. Apolinario, K. Roy, S-TLLR: STDP-inspired
temporal local learning rule for spiking neural networks,
Transactions on Machine Learning Research (2025).
URLhttps://openreview.net/forum?id=
CNaiJRcX84
[98] T. M. Summe, C. J. Schaefer, S. Joshi, Estimating Post-
Synaptic Effects for Online Training of Feed-Forward
SNNs, in: 2024 International Conference on Neuro-
morphic Systems (ICONS), 2024, pp. 264–271.doi:
10.1109/ICONS62911.2024.00046.
[99] C. Wang, X. Dong, Z. Ji, J. Jiang, X. Liu, S. Wu, Brain-
Scale, Enabling Scalable Online Learning in Spiking
Neural Networks (Jul. 2025).doi:10.1101/2024.09.
24.614728.
[100] J. Kaiser, H. Mostafa, E. Neftci, Synaptic Plastic-
ity Dynamics for Deep Continuous Local Learning
(DECOLLE), Frontiers in Neuroscience 14 (May 2020).
doi:10.3389/fnins.2020.00424.
[101] C. Ma, R. Yan, Z. Yu, Q. Yu, Deep Spike Learning
With Local Classifiers, IEEE Transactions on Cyber-
netics 53 (5) (2023) 3363–3375.doi:10.1109/TCYB.
2022.3188015.
[102] C. Ma, X. Chen, K. C. Tan, J. Wu, Spatiotemporal decou-
pled learning for spiking neural networks, IEEE Transac-
tions on Neural Networks and Learning Systems (2026)
1–15doi:10.1109/TNNLS.2026.3671461.
[103] J. Lee, R. Zhang, W. Zhang, Y . Liu, P. Li, Spike-Train
Level Direct Feedback Alignment: Sidestepping Back-
propagation for On-Chip Training of Spiking Neural
Nets, Frontiers in Neuroscience 14 (Mar. 2020).doi:
10.3389/fnins.2020.00143.
[104] F. M. Quintana, F. Perez-Peña, P. L. Galindo, E. O.
Neftci, E. Chicca, L. Khacef, ETLP: event-based three-
factor local plasticity for online learning with neuromor-
phic hardware, Neuromorphic Computing and Engineer-
ing 4 (3) (2024) 034006.doi:10.1088/2634-4386/
ad6733.
[105] T. Ortner, L. Pes, J. Gentinetta, C. Frenkel, A. Pan-
tazi, Online Spatio-Temporal Learning with Target Pro-
jection, in: 2023 IEEE 5th International Conference on
Artificial Intelligence Circuits and Systems (AICAS),
2023, pp. 1–5.doi:10.1109/AICAS57966.2023.
10168623.
[106] P. He, R. Xiao, C. Tang, S. Huang, J. Lv, H. Tang,
STSF: Spiking Time Sparse Feedback Learning for Spik-
ing Neural Networks, IEEE Transactions on Neural
Networks and Learning Systems (2025) 1–14doi:10.
1109/TNNLS.2025.3527700.
[107] M. P. E. Apolinario, K. Roy, C. Frenkel, Tess: A scalable
temporally and spatially local learning rule for spiking
neural networks, in: 2025 International Joint Conference
on Neural Networks (IJCNN), 2025, pp. 1–9.doi:10.
1109/IJCNN64981.2025.11227652.
[108] L. Pes, B. Yin, S. Stuijk, F. Corradi, Traces propaga-
tion: memory-efficient and scalable forward-only learn-
ing in spiking neural networks, Neuromorphic Comput-
ing and Engineering 6 (1) (2026) 014002.doi:10.
1088/2634-4386/ae2ef9.
[109] G. Hinton, The Forward-Forward Algorithm: Some Pre-
liminary Investigations, preprint on arXiv (Dec. 2022).
doi:10.48550/arXiv.2212.13345.
[110] M. Ghader, S. R. Kheradpisheh, B. Farahani, M. Fazlali,
Backpropagation-free spiking neural networks with the
forward–forward algorithm, Scientific Reports (2026).
doi:10.1038/s41598-026-41671-4.
[111] H. Markram, J. Lübke, M. Frotscher, B. Sakmann, Regu-
lation of Synaptic Efficacy by Coincidence of Postsynap-
tic APs and EPSPs, Science 275 (5297) (1997) 213–215.
doi:10.1126/science.275.5297.213.
[112] T. Masquelier, S. J. Thorpe, Unsupervised Learning of
Visual Features through Spike Timing Dependent Plas-
ticity, PLOS Computational Biology 3 (2) (2007) e31.
doi:10.1371/journal.pcbi.0030031.
[113] P. U. Diehl, M. Cook, Unsupervised learning of
digit recognition using spike-timing-dependent plastic-
ity, Frontiers in Computational Neuroscience 9 (Aug.
2015).doi:10.3389/fncom.2015.00099.
[114] J.-P. Pfister, W. Gerstner, Triplets of spikes in a model
of spike timing-dependent plasticity, Journal of Neu-
roscience 26 (38) (2006) 9673–9682.doi:10.1523/
JNEUROSCI.1425-06.2006.
23

--- PAGE 24 ---

[115] J. Gjorgjieva, C. Clopath, J. Audet, J.-P. Pfister, A triplet
spike-timing–dependent plasticity model generalizes the
Bienenstock–Cooper–Munro rule to higher-order spa-
tiotemporal correlations, Proceedings of the National
Academy of Sciences 108 (48) (2011) 19383–19388.
doi:10.1073/pnas.1105933108.
[116] E. L. Bienenstock, L. N. Cooper, P. W. Munro, The-
ory for the development of neuron selectivity: orienta-
tion specificity and binocular interaction in visual cor-
tex, Journal of Neuroscience 2 (1) (1982) 32–48.doi:
10.1523/JNEUROSCI.02-01-00032.1982.
[117] C. Clopath, L. Büsing, E. Vasilaki, W. Gerstner, Connec-
tivity reflects coding: a model of voltage-based STDP
with homeostasis, Nature Neuroscience 13 (3) (2010)
344–352.doi:10.1038/nn.2479.
[118] M. C. W. v. Rossum, G. Q. Bi, G. G. Turrigiano, Stable
Hebbian Learning from Spike Timing-Dependent Plas-
ticity, Journal of Neuroscience 20 (23) (2000) 8812–
8821.doi:10.1523/JNEUROSCI.20-23-08812.
2000.
[119] R. Gütig, R. Aharonov, S. Rotter, H. Sompolinsky,
Learning Input Correlations through Nonlinear Tempo-
rally Asymmetric Hebbian Plasticity, Journal of Neu-
roscience 23 (9) (2003) 3697–3714.doi:10.1523/
JNEUROSCI.23-09-03697.2003.
[120] G. G. Turrigiano, K. R. Leslie, N. S. Desai, L. C. Ruther-
ford, S. B. Nelson, Activity-dependent scaling of quan-
tal amplitude in neocortical neurons, Nature 391 (6670)
(1998) 892–896.doi:10.1038/36103.
[121] J. M. Brader, W. Senn, S. Fusi, Learning Real-World
Stimuli in a Neural Network with Spike-Driven Synap-
tic Dynamics, Neural Computation 19 (11) (2007) 2881–
2912.doi:10.1162/neco.2007.19.11.2881.
[122] G. E. Hinton, S. Osindero, Y .-W. Teh, A Fast Learning
Algorithm for Deep Belief Nets, Neural Computation
18 (7) (2006) 1527–1554.doi:10.1162/neco.2006.
18.7.1527.
[123] S. R. Kheradpisheh, M. Ganjtabesh, S. J. Thorpe,
T. Masquelier, STDP-based spiking deep convolutional
neural networks for object recognition, Neural Networks
99 (2018) 56–67.doi:10.1016/j.neunet.2017.12.
005.
[124] J. C. Thiele, O. Bichler, A. Dupret, Event-Based,
Timescale Invariant Unsupervised Online Deep Learning
With STDP, Frontiers in Computational Neuroscience
12 (Jun. 2018).doi:10.3389/fncom.2018.00046.
[125] P. Ferré, F. Mamalet, S. J. Thorpe, Unsupervised Feature
Learning With Winner-Takes-All Based STDP, Frontiers
in Computational Neuroscience 12 (Apr. 2018).doi:
10.3389/fncom.2018.00024.
[126] G. Srinivasan, K. Roy, ReStoCNet: Residual Stochas-
tic Binary Convolutional Spiking Neural Network for
Memory-Efficient Neuromorphic Computing, Frontiers
in Neuroscience 13 (Mar. 2019).doi:10.3389/fnins.
2019.00189.
[127] L. Buesing, J. Bill, B. Nessler, W. Maass, Neural Dy-
namics as Sampling: A Model for Stochastic Computa-
tion in Recurrent Networks of Spiking Neurons, PLOS
Computational Biology 7 (11) (2011) e1002211.doi:
10.1371/journal.pcbi.1002211.
[128] B. Nessler, M. Pfeiffer, L. Buesing, W. Maass, Bayesian
Computation Emerges in Generic Cortical Microcir-
cuits through Spike-Timing-Dependent Plasticity, PLOS
Computational Biology 9 (4) (2013) e1003037.doi:
10.1371/journal.pcbi.1003037.
[129] E. Neftci, S. Das, B. Pedroni, K. Kreutz-Delgado,
G. Cauwenberghs, Event-driven contrastive divergence
for spiking neuromorphic systems, Frontiers in Neuro-
science 7 (Jan. 2014).doi:10.3389/fnins.2013.
00272.
[130] E. O. Neftci, B. U. Pedroni, S. Joshi, M. Al-Shedivat,
G. Cauwenberghs, Stochastic Synapses Enable Efficient
Brain-Inspired Learning Machines, Frontiers in Neuro-
science 10 (Jun. 2016).doi:10.3389/fnins.2016.
00241.
[131] A. G. Ororbia, Contrastive signal–dependent plasticity:
Self-supervised learning in spiking neural circuits, Sci-
ence Advances 10 (43) (2024) eadn6076.doi:10.
1126/sciadv.adn6076.
[132] Y . Ma, H. Wang, H. Shen, X. Chen, S. Duan,
S. Wen, NeuroMoCo: a neuromorphic momentum con-
trast learning method for spiking neural networks, Ap-
plied Intelligence 55 (2) (2024) 97.doi:10.1007/
s10489-024-05982-1.
[133] C. Lee, P. Panda, G. Srinivasan, K. Roy, Training Deep
Spiking Convolutional Neural Networks With STDP-
Based Unsupervised Pre-training Followed by Super-
vised Fine-Tuning, Frontiers in Neuroscience 12 (Aug.
2018).doi:10.3389/fnins.2018.00435.
[134] Y . Dong, D. Zhao, Y . Li, Y . Zeng, An unsupervised
STDP-based spiking neural network inspired by bio-
logically plausible learning rules and connections, Neu-
ral Networks 165 (2023) 799–808.doi:10.1016/j.
neunet.2023.06.019.
[135] W. Schultz, P. Dayan, P. R. Montague, A Neural Sub-
strate of Prediction and Reward, Science 275 (5306)
(1997) 1593–1599.doi:10.1126/science.275.
5306.1593.
[136] R. V . Florian, Reinforcement Learning Through Mod-
ulation of Spike-Timing-Dependent Synaptic Plasticity,
24

--- PAGE 25 ---

Neural Computation 19 (6) (2007) 1468–1502.doi:
10.1162/neco.2007.19.6.1468.
[137] E. M. Izhikevich, Solving the Distal Reward Problem
through Linkage of STDP and Dopamine Signaling,
Cerebral Cortex 17 (10) (2007) 2443–2452.doi:10.
1093/cercor/bhl152.
URLhttps://doi.org/10.1093/cercor/bhl152
[138] M. A. Farries, A. L. Fairhall, Reinforcement learning
with modulated spike timing–dependent synaptic plas-
ticity, Journal of neurophysiology 98 (6) (2007) 3648–
3665.doi:10.1152/jn.00364.2007.
[139] N. Frémaux, H. Sprekeler, W. Gerstner, Functional
Requirements for Reward-Modulated Spike-Timing-
Dependent Plasticity, Journal of Neuroscience 30 (40)
(2010) 13326–13337.doi:10.1523/JNEUROSCI.
6249-09.2010.
[140] R. Legenstein, D. Pecevski, W. Maass, A Learning The-
ory for Reward-Modulated Spike-Timing-Dependent
Plasticity with Application to Biofeedback, PLOS Com-
putational Biology 4 (10) (2008) e1000180.doi:10.
1371/journal.pcbi.1000180.
[141] W. Potjans, A. Morrison, M. Diesmann, A Spiking Neu-
ral Network Model of an Actor-Critic Learning Agent,
Neural Computation 21 (2) (2009) 301–339.doi:10.
1162/neco.2008.08-07-593.
[142] N. Frémaux, H. Sprekeler, W. Gerstner, Reinforcement
Learning Using a Continuous Time Actor-Critic Frame-
work with Spiking Neurons, PLOS Computational Biol-
ogy 9 (4) (2013) e1003024.doi:10.1371/journal.
pcbi.1003024.
[143] M. Mozafari, S. R. Kheradpisheh, T. Masquelier,
A. Nowzari-Dalini, M. Ganjtabesh, First-Spike-Based
Visual Categorization Using Reward-Modulated STDP,
IEEE Transactions on Neural Networks and Learning
Systems 29 (12) (2018) 6178–6190.doi:10.1109/
TNNLS.2018.2826721.
[144] M. Mozafari, M. Ganjtabesh, A. Nowzari-Dalini, S. J.
Thorpe, T. Masquelier, Bio-inspired digit recognition
using reward-modulated spike-timing-dependent plastic-
ity in deep convolutional networks, Pattern Recognition
94 (2019) 87–95.doi:10.1016/j.patcog.2019.05.
015.
[145] Z. Bing, C. Meschede, K. Huang, G. Chen, F. Rohrbein,
M. Akl, A. Knoll, End to End Learning of Spiking
Neural Network Based on R-STDP for a Lane Keep-
ing Vehicle, in: 2018 IEEE International Conference on
Robotics and Automation (ICRA), 2018, pp. 4725–4732.
doi:10.1109/ICRA.2018.8460482.
[146] Z. Bing, I. Baumann, Z. Jiang, K. Huang, C. Cai,
A. Knoll, Supervised Learning in SNN via Reward-
Modulated Spike-Timing-Dependent Plasticity for a Tar-
get Reaching Vehicle, Frontiers in Neurorobotics 13
(May 2019).doi:10.3389/fnbot.2019.00018.
[147] G. Tang, N. Kumar, R. Yoo, K. Michmizos, Deep Re-
inforcement Learning with Population-Coded Spiking
Neural Network for Continuous Control, in: Proceed-
ings of the 2020 Conference on Robot Learning, PMLR,
2021, pp. 2016–2029.
URLhttps://proceedings.mlr.press/v155/
tang21a.html
[148] J. Schulman, F. Wolski, P. Dhariwal, A. Radford,
O. Klimov, Proximal Policy Optimization Algorithms,
preprint on arXiv (2017).doi:10.48550/arXiv.
1707.06347.
[149] S. Fujimoto, H. Hoof, D. Meger, Addressing function
approximation error in actor-critic methods, in: Inter-
national conference on machine learning, PMLR, 2018,
pp. 1587–1596.doi:https://proceedings.mlr.
press/v80/fujimoto18a/fujimoto18a.pdf.
[150] T. Haarnoja, A. Zhou, P. Abbeel, S. Levine, Soft actor-
critic: Off-policy maximum entropy deep reinforcement
learning with a stochastic actor, in: International confer-
ence on machine learning, Pmlr, 2018, pp. 1861–1870.
URLhttps://proceedings.mlr.press/v80/
haarnoja18b/haarnoja18b.pdf
[151] G. Brockman, V . Cheung, L. Pettersson, J. Schnei-
der, J. Schulman, J. Tang, W. Zaremba, OpenAI Gym,
preprint on arXiv (2016).doi:10.48550/arXiv.
1606.01540.
[152] D. Zhang, T. Zhang, S. Jia, B. Xu, Multi-Sacle Dy-
namic Coding Improved Spiking Actor Network for Re-
inforcement Learning, Proceedings of the AAAI Con-
ference on Artificial Intelligence 36 (1) (2022) 59–67.
doi:10.1609/aaai.v36i1.19879.
[153] D. Chen, P. Peng, T. Huang, Y . Tian, Deep reinforce-
ment learning with spiking q-learning, preprint on arXiv
(2024).arXiv:2201.09754.
URLhttps://arxiv.org/abs/2201.09754
[154] G. Liu, W. Deng, X. Xie, L. Huang, H. Tang, Human-
Level Control Through Directly Trained Deep Spik-
ing Q-Networks, IEEE Transactions on Cybernetics
53 (11) (2023) 7187–7198.doi:10.1109/TCYB.2022.
3198259.
[155] D. Chen, P. Peng, T. Huang, Y . Tian, Fully Spiking Actor
Network With Intralayer Connections for Reinforcement
Learning, IEEE Transactions on Neural Networks and
Learning Systems 36 (2) (2025) 2881–2893.doi:10.
1109/TNNLS.2024.3352653.
25

--- PAGE 26 ---

[156] L. Zanatta, A. Di Mauro, F. Barchi, A. Bartolini,
L. Benini, A. Acquaviva, Directly-trained Spiking Neu-
ral Networks for Deep Reinforcement Learning: Energy
efficient implementation of event-based obstacle avoid-
ance on a neuromorphic accelerator, Neurocomputing
562 (2023) 126885.doi:10.1016/j.neucom.2023.
126885.
[157] M. Mikaitis, G. Pineda García, J. C. Knight, S. B. Furber,
Neuromodulated Synaptic Plasticity on the SpiNNaker
Neuromorphic System, Frontiers in Neuroscience 12
(Feb. 2018).doi:10.3389/fnins.2018.00105.
[158] Y . Sun, F. Zhao, M. Lyu, Y . Zeng, Spiking world
model with multicompartment neurons for model-based
reinforcement learning, Proceedings of the National
Academy of Sciences 122 (50) (2025) e2513319122.
doi:10.1073/pnas.2513319122.
[159] Y . Cao, Y . Chen, D. Khosla, Spiking Deep Convolutional
Neural Networks for Energy-Efficient Object Recogni-
tion, International Journal of Computer Vision 113 (1)
(2015) 54–66.doi:10.1007/s11263-014-0788-3.
[160] B. Rueckauer, I.-A. Lungu, Y . Hu, M. Pfeiffer, S.-C.
Liu, Conversion of Continuous-Valued Deep Networks
to Efficient Event-Driven Networks for Image Classifi-
cation, Frontiers in Neuroscience 11 (Dec. 2017).doi:
10.3389/fnins.2017.00682.
[161] P. U. Diehl, D. Neil, J. Binas, M. Cook, S.-C. Liu,
M. Pfeiffer, Fast-classifying, high-accuracy spiking deep
networks through weight and threshold balancing, in:
2015 International Joint Conference on Neural Networks
(IJCNN), 2015, pp. 1–8.doi:10.1109/IJCNN.2015.
7280696.
[162] A. Sengupta, Y . Ye, R. Wang, C. Liu, K. Roy, Going
Deeper in Spiking Neural Networks: VGG and Residual
Architectures, Frontiers in Neuroscience 13 (Mar. 2019).
doi:10.3389/fnins.2019.00095.
[163] T. Bu, W. Fang, J. Ding, P. DAI, Z. Yu, T. Huang,
Optimal ANN-SNN conversion for high-accuracy and
ultra-low-latency spiking neural networks, in: Interna-
tional Conference on Learning Representations, 2022.
URLhttps://openreview.net/forum?id=
7B3IJMM1k_M
[164] B. Han, G. Srinivasan, K. Roy, RMP-SNN: Residual
Membrane Potential Neuron for Enabling Deeper High-
Accuracy and Low-Latency Spiking Neural Network,
2020, pp. 13558–13567.
URLhttps://openaccess.thecvf.com/content_
CVPR_2020/html/Han_RMP-SNN_Residual_
Membrane_Potential_Neuron_for_Enabling_
Deeper_High-Accuracy_and_CVPR_2020_paper.
html
[165] B. Han, K. Roy, Deep Spiking Neural Network: Energy
Efficiency Through Time Based Coding, in: A. Vedaldi,
H. Bischof, T. Brox, J.-M. Frahm (Eds.), Computer
Vision – ECCV 2020, Springer International Pub-
lishing, Cham, 2020, pp. 388–404.doi:10.1007/
978-3-030-58607-2_23.
[166] T. Bu, J. Ding, Z. Yu, T. Huang, Optimized Potential Ini-
tialization for Low-Latency Spiking Neural Networks,
Proceedings of the AAAI Conference on Artificial In-
telligence 36 (1) (2022) 11–20.doi:10.1609/aaai.
v36i1.19874.
[167] S. S. Chowdhury, N. Rathi, K. Roy, Towards Ultra Low
Latency Spiking Neural Networks for Vision and Se-
quential Tasks Using Temporal Pruning, in: S. Avi-
dan, G. Brostow, M. Cissé, G. M. Farinella, T. Hass-
ner (Eds.), Computer Vision – ECCV 2022, Springer
Nature Switzerland, Cham, 2022, pp. 709–726.doi:
10.1007/978-3-031-20083-0_42.
[168] Y . Hu, Q. Zheng, X. Jiang, G. Pan, Fast-SNN: Fast
Spiking Neural Network by Converting Quantized ANN,
IEEE Transactions on Pattern Analysis and Machine In-
telligence 45 (12) (2023) 14546–14562.doi:10.1109/
TPAMI.2023.3275769.
[169] Y . Li, S. Deng, X. Dong, R. Gong, S. Gu, A Free Lunch
From ANN: Towards Efficient, Accurate Spiking Neural
Networks Calibration, in: Proceedings of the 38th
International Conference on Machine Learning, PMLR,
2021, pp. 6316–6325.
URLhttps://proceedings.mlr.press/v139/
li21d.html
[170] S. Deng, S. Gu, Optimal conversion of conventional
artificial neural networks to spiking neural networks, in:
International Conference on Learning Representations,
2021.
URLhttps://openreview.net/forum?id=
FZ1oTwcXchK
[171] Y . Li, S. Deng, X. Dong, S. Gu, Error-Aware Con-
version from ANN to SNN via Post-training Param-
eter Calibration, International Journal of Computer
Vision 132 (9) (2024) 3586–3609.doi:10.1007/
s11263-024-02046-2.
[172] N. Rathi, K. Roy, DIET-SNN: A Low-Latency Spiking
Neural Network With Direct Input Encoding and Leak-
age and Threshold Optimization, IEEE Transactions on
Neural Networks and Learning Systems 34 (6) (2023)
3174–3182.doi:10.1109/TNNLS.2021.3111897.
[173] J. Wu, C. Xu, X. Han, D. Zhou, M. Zhang, H. Li, K. C.
Tan, Progressive Tandem Learning for Pattern Recogni-
tion With Deep Spiking Neural Networks, IEEE Trans-
actions on Pattern Analysis and Machine Intelligence
44 (11) (2022) 7824–7840.doi:10.1109/TPAMI.
2021.3114196.
26

--- PAGE 27 ---

[174] C. Stöckl, W. Maass, Optimized spiking neurons
can classify images with high accuracy through tem-
poral coding with two spikes, Nature Machine In-
telligence 3 (3) (2021) 230–238.doi:10.1038/
s42256-021-00311-4.
[175] S. Kim, S. Park, B. Na, S. Yoon, Spiking-YOLO: Spik-
ing Neural Network for Energy-Efficient Object Detec-
tion, Proceedings of the AAAI Conference on Artifi-
cial Intelligence 34 (07) (2020) 11270–11277.doi:
10.1609/aaai.v34i07.6787.
[176] K. You, Z. Xu, C. Nie, Z. Deng, Q. Guo, X. Wang,
Z. He, SpikeZIP-TF: Conversion is all you need
for transformer-based SNN, in: R. Salakhutdinov,
Z. Kolter, K. Heller, A. Weller, N. Oliver, J. Scarlett,
F. Berkenkamp (Eds.), Proceedings of the 41st Inter-
national Conference on Machine Learning, V ol. 235 of
Proceedings of Machine Learning Research, PMLR,
2024, pp. 57367–57383.
URLhttps://proceedings.mlr.press/v235/
you24b.html
[177] S. Hwang, S. Lee, D. Park, D. Lee, J. Kung, Spikedatten-
tion: Training-free and fully spike-driven transformer-
to-snn conversion with winner-oriented spike shift for
softmax operation, Advances in Neural Information Pro-
cessing Systems 37 (2024) 67422–67445.doi:10.
5555/3737916.3740068.
[178] D. Floreano, C. Mattiussi, Evolution of spiking neu-
ral controllers for autonomous vision-based robots, in:
T. Gomi (Ed.), Evolutionary Robotics. From Intelligent
Robotics to Artificial Life, Springer Berlin Heidelberg,
Berlin, Heidelberg, 2001, pp. 38–61.doi:10.1007/
978-3-540-74690-4_38.
[179] N. Pavlidis, O. Tasoulis, V . Plagianakos, G. Nikiforidis,
M. Vrahatis, Spiking neural network training using evo-
lutionary algorithms, in: Proceedings. 2005 IEEE Inter-
national Joint Conference on Neural Networks, 2005.,
V ol. 4, 2005, pp. 2190–2194 vol. 4.doi:10.1109/
IJCNN.2005.1556240.
[180] Y . Jin, R. Wen, B. Sendhoff, Evolutionary Multi-
objective Optimization of Spiking Neural Networks, in:
J. M. de Sá, L. A. Alexandre, W. Duch, D. Mandic
(Eds.), Artificial Neural Networks – ICANN 2007,
Springer, Berlin, Heidelberg, 2007, pp. 370–379.doi:
10.1007/978-3-540-74690-4_38.
[181] H. Qiu, M. Garratt, D. Howard, S. Anavatti, Evolving
Spiking Neural Networks for Nonlinear Control Prob-
lems, in: 2018 IEEE Symposium Series on Computa-
tional Intelligence (SSCI), 2018, pp. 1367–1373.doi:
10.1109/SSCI.2018.8628848.
[182] A. Vandesompele, F. Walter, F. Röhrbein, Neuro-
evolution of spiking neural networks on SpiNNaker neu-
romorphic hardware, in: 2016 IEEE Symposium Series
on Computational Intelligence (SSCI), 2016, pp. 1–6.
doi:10.1109/SSCI.2016.7850250.
[183] C. D. Schuman, J. P. Mitchell, R. M. Patton, T. E. Po-
tok, J. S. Plank, Evolutionary Optimization for Neu-
romorphic Systems, in: Proceedings of the 2020 An-
nual Neuro-Inspired Computational Elements Work-
shop, NICE ’20, Association for Computing Machinery,
New York, NY , USA, 2020, pp. 1–9.doi:10.1145/
3381755.3381758.
[184] G. Wang, Y . Sun, S. Cheng, S. Song, Evolving Connec-
tivity for Recurrent Spiking Neural Networks, Advances
in Neural Information Processing Systems 36 (2023)
2991–3007.
URLhttps://proceedings.neurips.
cc/paper_files/paper/2023/hash/
08f9de0232c0b485110237f6e6cf88f1-Abstract-Conference.
html
[185] R. Jiang, G. Du, S. Yu, Y . Guo, S. K. Goh, H.-K.
Tang, CADE: Cosine Annealing Differential Evolution
for Spiking Neural Network, in: 2024 International Joint
Conference on Neural Networks (IJCNN), 2024, pp. 1–
8.doi:10.1109/IJCNN60899.2024.10650360.
[186] B. Na, J. Mok, S. Park, D. Lee, H. Choe, S. Yoon,
AutoSNN: Towards Energy-Efficient Spiking Neural
Networks, in: Proceedings of the 39th International
Conference on Machine Learning, PMLR, 2022, pp.
16253–16269.
URLhttps://proceedings.mlr.press/v162/
na22a.html
[187] K. Che, L. Leng, K. Zhang, J. Zhang, Q. Meng,
J. Cheng, Q. Guo, J. Liao, Differentiable hierarchical
and surrogate gradient search for spiking neural net-
works, Advances in Neural Information Processing
Systems 35 (2022) 24975–24990.
URLhttps://proceedings.neurips.
cc/paper_files/paper/2022/hash/
9e8c2895db691eaab85af37bddee75aa-Abstract-Conference.
html
[188] H. S. Seung, Learning in Spiking Neural Networks
by Reinforcement of Stochastic Synaptic Transmission,
Neuron 40 (6) (2003) 1063–1073.doi:10.1016/
S0896-6273(03)00761-X.
[189] I. R. Fiete, H. S. Seung, Gradient Learning in Spiking
Neural Networks by Dynamic Perturbation of Conduc-
tances, Physical Review Letters 97 (4) (2006) 048104.
doi:10.1103/PhysRevLett.97.048104.
URLhttps://link.aps.org/doi/10.1103/
PhysRevLett.97.048104
[190] B. Mukhoty, V . Bojkovic, W. de Vazelhes, X. Zhao,
G. De Masi, H. Xiong, B. Gu, Direct Training of
SNN using Local Zeroth Order Method, Advances
in Neural Information Processing Systems 36 (2023)
27

--- PAGE 28 ---

18994–19014.
URLhttps://proceedings.neurips.
cc/paper_files/paper/2023/hash/
3c5e64f26a97db6a2b0bbb788236431e-Abstract-Conference.
html
[191] R. A. Vázquez, B. A. Garro, Training Spiking Neurons
by Means of Particle Swarm Optimization, in: Y . Tan,
Y . Shi, Y . Chai, G. Wang (Eds.), Advances in Swarm In-
telligence, Springer, Berlin, Heidelberg, 2011, pp. 242–
249.doi:10.1007/978-3-642-21515-5_29.
[192] A. Javanshir, T. T. Nguyen, M. A. P. Mahmud, A. Z.
Kouzani, Training Spiking Neural Networks with Meta-
heuristic Algorithms, Applied Sciences 13 (8) (Apr.
2023).doi:10.3390/app13084809.
[193] J. Yik, K. Van den Berghe, D. Den Blanken, Y . Bouhad-
jar, M. Fabre, P. Hueber, W. Ke, M. A. Khoei, D. Kleyko,
N. Pacik-Nelson, et al., The neurobench framework for
benchmarking neuromorphic computing algorithms and
systems, Nature communications 16 (1) (2025) 1545.
doi:10.1038/s41467-025-56739-4.
[194] W. Fang, Y . Chen, J. Ding, Z. Yu, T. Masquelier,
D. Chen, L. Huang, H. Zhou, G. Li, Y . Tian, Spik-
ingjelly: An open-source machine learning infrastruc-
ture platform for spike-based intelligence, Science Ad-
vances 9 (40) (2023) eadi1480.doi:10.1126/sciadv.
adi148.
[195] G. Lenz, K. Chaney, S. B. Shrestha, O. Oubari, S. Pi-
caud, G. Zarrella, Tonic: event-based datasets and trans-
formations, [Online available] (Jul. 2021).doi:10.
5281/zenodo.5079801.
[196] T. Akiba, S. Sano, T. Yanase, T. Ohta, M. Koyama,
Optuna: A next-generation hyperparameter optimiza-
tion framework, KDD ’19, Association for Computing
Machinery, New York, NY , USA, 2019, p. 2623–2631.
doi:10.1145/3292500.3330701.
28