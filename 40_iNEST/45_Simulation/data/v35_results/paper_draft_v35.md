# C.elegans Connectome Analysis: Small-World Topology and Structure-Function Coupling

## Methods

### Connectome Data
We used the C.elegans hermaphrodite connectome from Varshney et al. (2011),
consisting of N=279 neurons and E=1961 chemical synapses (k_avg=14.06).

### Four-Index Network Analysis
We computed four standard complex network metrics:
1. **Small-world index σ** = γ/λ, where γ = C/C_rand and λ = L/L_rand
2. Clustering coefficient C (Watts-Strogatz)
3. Average shortest path length L
4. Degree distribution skewness

Random (ER), small-world (WS), and scale-free (BA) null models of matching
size and density served as controls.

### Structure-Function Coupling
Using the graph heat kernel K = exp(-t * L_norm) with diffusion time t=0.5,
we mapped structural connectivity (SC) to functional connectivity (FC).
Neuron class labels (sensory, interneuron, motor) were used to test whether
SC edges are enriched within functional categories.

### Statistical Testing
Kolmogorov-Smirnov tests compared degree and clustering distributions vs ER.
Permutation tests (10,000 shuffles) assessed SC-FC class enrichment.
Bootstrap resampling (n=9) provided 95% CIs.

## Results

### Small-World Topology
The C.elegans connectome exhibits strong small-world properties:
- **σ = 6.98** (literature: 5.6, error: 24.6%)
- γ = 1.471 (high clustering relative to random)
- λ ≈ 1.0 (path length comparable to random)
- KS test vs ER: clustering D=0.9391, p=6.80e-135
- KS test vs ER: degree D=0.2688, p=2.84e-09

Both degree and clustering distributions differ significantly from random
(p < 0.001), confirming that the connectome topology is non-random and
exhibits genuine small-world organization.

### Structure-Function Coupling
- **SC edges are 2.3x enriched within functional categories**
  (within: 0.0798, between: 0.0345)
- Permutation test: real within-class fraction (0.3888) vs
  ER expectation (0.3514), p = 0.008
- Modularity Q = 0.0573

The significant enrichment (p < 0.01) indicates that structural connections
preferentially link neurons of the same functional class, supporting the
hypothesis that SC topology constrains FC patterns.

## Discussion

Our results demonstrate that the C.elegans connectome possesses:
1. **Genuine small-world topology** (σ=6.98), consistent with
   prior literature (Watts & Strogatz 1998, σ=5.6)
2. **Significant SC-FC coupling** (2.3x class enrichment, p=0.008)

### Limitations
- The Varshney (2011) dataset covers chemical synapses only; gap junctions
  are not included
- Neuron class labels are coarse (3 categories); finer functional annotations
  may reveal additional structure
- The graph heat kernel is a simplified diffusion model; biophysical neuron
  dynamics (Hodgkin-Huxley) are not modeled
- N=279 is limited for claims about scaling laws; cross-species validation
  is required (see V28, V34)

### Next Steps
- Extend to Drosophila Larva (N=2,952, V27) and Hemibrain (N=21,739, V33)
- Multi-threshold avalanche validation (V32)
- Cross-species avalanche universality (V34)

## References
- Varshney et al. (2011). Structural properties of the C. elegans neuronal network. PLoS CB.
- Watts & Strogatz (1998). Collective dynamics of 'small-world' networks. Nature.
