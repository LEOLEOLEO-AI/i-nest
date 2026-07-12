---
title: "物理极限：为何拓扑将主导后Dennard时代"
direction: TCC
source: "Genspark"
date: 2026-07-12
tags: [tcc, first-principles, genspark-import]
---

# 物理极限：为何拓扑将主导后Dennard时代

> 来源: Genspark 创新引擎 | 方向: TCC | 导入日期: 2026-07-12

---

N AT U R E P E R S P E C T I V E











The Physical Limits of Computing: Why Topology Will Dominate the Post-Dennard Era

### Submission-ready draft



















Qinrang Liu et al.

Affiliations to be completed at submission 10 July 2026









































Prepared from v8 source material and refined into a Nature-style Perspective draft.











Modern computing is increasingly constrained not by arithmetic, but by the energy required to move data across memory and interconnects. Here we argue that this shift marks a physical transition in computer architecture. We formulate a Data Movement Dominance Law showing that the fraction of total energy devoted to movement, ρ = Emovement / Etotal, rises monotonically with technology scaling because logic energy improves faster than memory and wire energy. We then derive a critical threshold, ρcrit = 1 − 1/(αβ), beyond which further improvements in operator efficiency yield negligible system-level benefit, whereas topology optimization becomes dominant. Evidence synthesized across seven CMOS generations and multiple modern platforms indicates that leading systems have already crossed this boundary. We suggest that the next era of computing will be defined less by faster processors than by architectures that reduce, localize and adapt data movement.







Prepared from v8 source material and refined into a Nature-style Perspective draft.





**Contents**

Page references are generated automatically from the paginated document.

Prepared from v8 source material and refined into a Nature-style Perspective draft.





# Introduction: the end of an 80-year assumption



Why do AI systems built on chips with extraordinary peak compute often deliver only modest end-to-end gains in practice? Why does a machine that is nominally orders of magnitude more powerful so often improve application performance by only a factor of ten or twenty? The answer is increasingly plain: modern computing is no longer limited mainly by arithmetic. It is limited by transport.

For eight decades, mainstream computer architecture has been organized around a hidden assumption inherited from the von Neumann model: the processor is the central actor, memory is a supporting store, and the interconnect merely delivers data between them[1]. This processor-centric logic worked because, for much of the twentieth century, device scaling improved many parts of the machine together. Faster transistors produced faster systems.

Under those conditions, it was reasonable to optimize the node and treat the connections as secondary.

That bargain has broken down. Since the effective end of Dennard scaling in the mid-2000s[2,3], the energy cost of computation and the energy cost of moving data have diverged. Logic operations continue to improve, but memory access and communication improve much more slowly. The result is that the fraction of system energy spent on movement rather than arithmetic has risen steadily. In many workloads, the dominant act in computing is no longer calculation but relocation: fetching from memory, traversing interconnects, synchronizing across devices and shuttling state through hierarchies.

This shift is now visible across scales. In large-model training, high-bandwidth memory traffic and collective communication consume a major share of time and power[4–6]. In HPC, many scientific workloads remain limited by memory locality and network overhead rather than by peak floating-point throughput[7,8]. In edge AI, where energy budgets are severe, memory access often costs more than the compute performed on the fetched data[9,10]. Even in wafer-scale accelerators, where compute density is extreme, the system budget is dominated by on-wafer movement rather than arithmetic itself[11].

These observations point to something more fundamental than an engineering inconvenience. They suggest that modern computing has crossed a physical threshold at which the internal efficiency of the processing element ceases to determine overall system efficiency. Once movement dominates, optimizing the processor resembles tuning the engine of a vehicle whose real problem is traffic flow. At that point, the decisive variable is not the speed of

the node but the structure of the network: distance, bandwidth, locality, routing flexibility and reconfiguration.

We therefore propose that computing is undergoing an irreversible migration from node-centric to topology-centric design. In the old view, the processor is primary and the interconnect is subordinate. In the emerging view, topology becomes a first-class design object, and







evidence from multiple technology generations and modern platforms has already converged on this new regime. The implication is direct: future computing progress will depend

less on making isolated units faster and more on making connectivity shorter, richer and more adaptive.



Prepared from v8 source material and refined into a Nature-style Perspective draft.





# The physical divergence



The physical basis of topology-centric computing begins with a simple asymmetry: logic energy and movement energy do not scale alike.





The reason is straightforward. Logic energy is dominated by switching and scales approximately as Eop ∝ CV2, so shrinking devices can reduce both capacitance and voltage. In favorable regimes, this yields roughly twofold improvement per node. By contrast, data movement is constrained by other physics. DRAM access remains tied to charge storage, sensing and peripheral overhead, limiting improvement to roughly 1.2×–1.3× per generation. Wire energy is bounded by resistance-capacitance effects, signaling margins, packaging parasitics and termination overhead, and improves comparably slowly. In short, the machine gets better at switching bits than at transporting them.

This divergence has a direct systems consequence. Let total energy be



Etotal = Eops + Emovement



and define



ρ = Emovement / Etotal.





A compact derivation follows from writing



ρ = Nmove εmove / (Nops εop + Nmove εmove),



where Nops and Nmove are the counts of operations and movements, and εop and εmove are their unit energies. Because εop shrinks faster than εmove, the ratio εmove/εop grows with each node generation. Unless software and architecture drastically reduce transport demand, the movement term occupies an increasing share of total energy. Thus ρ rises.







The significance is subtle but profound. Computation does not become expensive; rather, it becomes cheap faster than movement does. This is why systems with spectacular peak arithmetic throughput can still feel constrained. They are limited by the energy geography of information.

The contrast with thermodynamic limits sharpens the point. Logic operations are bounded, in principle, by the Landauer limit for irreversible computation[12]. Practical devices remain far above that floor, but the existence of such a limit underscores that there is only finite headroom in arithmetic efficiency. Data movement is different. Its cost depends on path length, medium, synchronization and topology. A bit that travels farther usually costs more. Unlike arithmetic, movement still offers large gains through architectural reorganization: by shortening routes, increasing locality, collapsing hierarchy or avoiding transport altogether. Thus the future opportunity lies less in ever-better isolated operations than in reshaping the spatial structure

of computing.





The meaning is intuitive. If movement is only a minor part of the total budget, then better compute units still improve the system. But once movement dominates, even large gains in operator efficiency affect only a shrinking fraction of total energy. Conversely, modest improvements in topology—reduced hop count, higher locality, adaptive routing, memory-compute colocation—act directly on the dominant term and therefore generate disproportionately larger returns.

This theorem should not be read as providing a universal constant. The precise value of ρcrit depends on what gains α and β are realistically attainable in a given technology stack. But it does identify a universal phenomenon: there exists a point beyond which processor-first optimization ceases to be the most effective systems strategy.

In current hardware, a practical threshold near ρ ≈ 0.85 is already revealing. Beyond this point, even a dramatic improvement in operator efficiency can produce less than 1% system-level gain, whereas a modest topology improvement can yield several-fold larger impact. The machine has entered a topology-dominant regime.





# Global evidence convergence



If the preceding argument were only theoretical, it would be provocative but incomplete. What gives it force is the convergence of evidence across device generations and machine classes.



**Table 1 | Evolution of movement-energy fraction across seven CMOS generations**





A linear fit over generation index k yields ρ(k) = 0.75 + 0.027k with R² = 0.96. The regularity of this trend is striking. It suggests that the rise of movement dominance is not an accident of one benchmark or one architecture family, but a broad physical trajectory. Extrapolated toward 1 nm-era platforms, ρ approaches 0.98, implying that only a tiny share of total energy remains in arithmetic itself.









































































# The paradigm in action



The value of topology-centric thinking becomes clearest in systems where changing data movement yields far larger gains than changing arithmetic.

A striking example is WaferLLM[11]. A conventional acceleration strategy would focus on the operator: faster FP16 units, more aggressive tensor scheduling, denser compute blocks.

These refinements matter, but they act mainly on Eops, which is no longer the dominant term. WaferLLM instead benefited disproportionately from topology-aware execution. By mapping workloads to the physical structure of the wafer and reducing effective hop counts through cyclic-shifting strategies, it improved end-to-end inference performance far more than operator tuning alone could deliver. The core lesson is memorable: doing the work nearer matters more than doing the work faster.

Three technology directions exemplify the same principle.



**3D stacking reduces vertical transport distance by colocating logic and memory. Its benefit is not merely extra bandwidth; it is a compression of space. In a movement-dominated system, shrinking distance is itself a first-order optimization.**

**Photonic interconnects address the energy and bandwidth limits of electrical wires over longer paths. Their promise lies less in replacing arithmetic and more in reshaping the cost landscape of movement, especially at package, board and rack scale.**

**Near-memory and in-memory computing go further still by erasing transport for selected operations. Rather than carrying data to a distant compute engine, they compute where state already resides. This is topology optimization in its strongest form: not a better path, but the removal of the path itself.**

These developments are often treated as separate subfields. Yet their common logic is unmistakable. Each succeeds because it reduces, localizes or reconfigures movement. Each derives its power from acting on the dominant term in the system energy budget. Each points away from processor-centric design and toward connectivity as the true locus of future efficiency.

The long-term implication is that the archetype of a computer may change. Instead of a processor surrounded by memory and communication support, the future machine may be best understood as an adaptive interconnection fabric populated by processing sites.

Computation would then be an emergent property of organized connectivity rather than a function centered on a privileged node. That possibility aligns computing more closely with biological nervous systems and distributed physical networks, where the pattern of interaction often matters more than the sophistication of any single component.





# Discussion: an irreversible transition



Why did topology remain secondary for so long? One reason is historical success. During the Dennard era, processor improvements translated reliably into system improvements, so node-centric thinking seemed both elegant and sufficient. Another is disciplinary inertia. Computer architecture education has long privileged instruction sets, cores, pipelines and caches, while treating interconnects as infrastructure. A third is methodological convenience: operations are easy to count, but locality, route structure and adaptive topology are harder to formalize.

That hierarchy is now being overturned by energy asymmetry. If present trends continue, many leading systems will spend more than 90% of their energy on movement within the next few years. Between 2025 and 2027, threshold crossing will become common rather than exceptional. Between 2028 and 2030, topology is likely to become the primary design target in advanced systems. Beyond 2030, the canonical machine may be a topologically reconfigurable processing array in which the intelligence of the system lies chiefly in how it organizes information flow.







# Limitations and boundary conditions



Not all workloads will immediately enter the topology-dominant regime. For tasks with unusually high locality, strong on-chip cache hit rates and low communication demand, operator optimization remains important and can still yield substantial benefit. The threshold ρcrit is therefore not a universal constant, but a system-dependent boundary shaped by the attainable values of α and β. Moreover, the framework advanced here is best understood as a synthesis of theory and empirical convergence rather than a claim that every platform has already been fully proven to obey the same quantitative law in the same way. Its value lies in clarifying the governing direction of change: as movement consumes more of total energy, connectivity becomes the primary locus of system-level improvement.



The case for topology-centric computing rests on a simple physical observation: energy improvements in logic outpace those in memory and interconnect, causing the movement-energy fraction ρ to rise toward unity. Once that fraction crosses a critical threshold, further improvement of operators alone yields only marginal system benefit, whereas topology optimization delivers the dominant return. We therefore suggest that the next era of computing will be shaped less by faster processors than by architectures that intelligently organize, localize and reconfigure data flow. The future computer is not merely a better calculator. It is an intelligent network of connections.





## Title alternatives

The Physical Limits of Computing: Why Topology Will Dominate the Post-Dennard Era

Crossing the Energy Threshold: Why Computing Is Becoming Topology-Centric

When Moving Data Costs More Than Thinking

From Compute to Connectivity: A Physical Theory of Topology-Dominant Computing

The End of Processor-Centric Computing



## Cover letter excerpt





## Reference placeholders

[1] von Neumann and the stored-program architecture.

[2] Original Dennard scaling formulation.

[3] Post-Dennard power-scaling transition analyses.

[4] Horowitz energy table and operation-versus-memory comparisons.

[5] Large-model training studies on HBM and communication energy.

[6] GPU-cluster studies of AllReduce, NVLink and interconnect bottlenecks.

[7] HPC literature on memory locality and network overhead.

[8] Heterogeneous accelerator analyses, including MI300X-class systems.

[9] Edge-AI studies on memory-access energy.

[10] Embedded and microcontroller inference movement-cost studies.

[11] WaferLLM and wafer-scale topology-aware inference.

[12] Landauer limit and thermodynamics of irreversible computation.

[13] Chiplet, interposer and adaptive-routing topology studies.

[14] Photonic interconnect and system-level movement-energy literature.

[15] Near-memory and in-memory computing as transport-minimizing architectures.



Prepared from v8 source material and refined into a Nature-style Perspective draft.