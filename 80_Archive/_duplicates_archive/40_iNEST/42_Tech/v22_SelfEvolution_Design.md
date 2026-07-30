# v22 SDI Self-Evolution Mechanism Design

**Project**: iNEST SDI Self-Evolving Network Simulation Platform
**Document**: v22 Upgrade Design from v8 Baseline
**Version**: v1.0
**Date**: 2026-06-03
**Prerequisite**: v8 baseline + phase transition scan results

---

## 1. Problem-Driven Upgrade (v8 to v22)

### 1.1 v8 Core Findings

| Metric | v8 Result | Issue |
|--------|-----------|-------|
| alpha | 2.281 | PASS - criticality achieved |
| sigma | 2.701 | FAIL - below 4.0, degraded from initial 4.71 |
| E-L percent | 41.8 percent | FAIL - over-consolidation (target 15-28 percent) |
| Scan alpha | all > 2.5 | FAIL - no N satisfies both alpha+sigma |

### 1.2 Root Cause Analysis

Fixed theta period leads to small-network over-update, causing E-L avalanche accumulation.
Long-range shortcuts are flooded by E-L bonds, degrading sigma and pushing alpha upward.

Physics insight: Biological theta wave frequency (4-8Hz) is strongly correlated with brain volume
and network diameter. Small networks propagate information faster; using a large-network theta
window leads to LTP oversaturation.

---

## 2. Three Core Upgrades

### Upgrade 1: Adaptive Theta Period (Scale-Dependent Rhythm)

```
T_theta(t) = T_theta_base * (L(t) / L_ref) / v_c
```

Parameters:
- L(t): current network average path length
- L_ref: reference path length (C. elegans L=2.44)
- v_c: signal propagation speed (normalized to 1.0)
- T_theta_base: base theta window (default 25 steps)

Pseudo-code:
```python
def adaptive_theta(network, T_base=25, L_ref=2.44, v_c=1.0):
    L_current = nx.average_shortest_path_length(network.graph)
    T_theta = int(T_base * (L_current / L_ref) / v_c)
    return max(5, min(T_theta, 100))
```

Expected effect:
- Small network (N~100): T_theta approximately 5-10, consolidation frequency reduced
- Large network (N~1000): T_theta approximately 30-50, normal consolidation
- Key hypothesis: sigma degradation eliminated, sigma >= 4.0 sustainable

### Upgrade 2: FEP Global Homeostasis (Homeostatic Plasticity)

For each node i:
```
total_out_w = sum(w_ij for j in out_neighbors(i))
if total_out_w > target_out_w:
    w_ij *= target_out_w / total_out_w  (Multiplicative Scaling)
```

Difference from v8 Turrigiano scaling:
- Turrigiano: global scope, triggered by total network weight threshold
- FEP Homeostasis: per-node scope, triggered by node-level out-degree weight

### Upgrade 3: External Data Closed-Loop Drive (Embodied Interaction)

Without external input, networks evolve to dead states (full sync or full crystallization).
Intelligence emergence must be driven by minimizing prediction error while processing information.

Experiment Design:
- Condition A (control): Random noise, expected sigma=2.7, alpha=2.28
- Condition B (v22): MNIST spike stream, expected sigma>=4.0, alpha=1.5-2.0
- Condition C (v22+): Temporal MNIST, expected sigma>=5.0, alpha=1.3-1.7

---

## 3. v22 Simulation Flow (Abbreviated)

```python
class SDI_v22(SDI_v8):
    def step(self):
        self.T_theta = adaptive_theta(self)
        cascade = self.cascade_activation()
        self.stdp_update(cascade)
        if self.t % self.T_theta == 0:
            self.fep_consolidate()
            self.fep_homeostasis()  # NEW
        if self.t % self.SCALING_INT == 0:
            self.synaptic_scaling()
        self.record_metrics()
```

---

## 4. Validation Plan

### 4.1 Ablation Study Matrix

| Experiment | Adaptive theta | FEP Homeostasis | External Data | Expected |
|------------|---------------|-----------------|---------------|----------|
| v22-A | N | N | N | v8 baseline reproduction |
| v22-B | Y | N | N | E-L improved, sigma partial restore |
| v22-C | Y | Y | N | E-L on target, sigma >= 4.0 |
| v22-D | Y | Y | Y (MNIST) | alpha converges to 1.5-1.8 |

### 4.2 Success Criteria

| Metric | v8 Baseline | v22 Target |
|--------|------------|------------|
| sigma | 2.701 | >= 4.0 |
| alpha | 2.281 | 1.5-2.0 |
| E-L percent | 41.8 percent | 15-28 percent |
| F_total monotonicity | Not tracked | Monotonically decreasing |
| N_min_critical | Not found | <= 200 |

---

## 5. Implementation Plan

### 5.1 File Structure
```
D:/Obsidian/phase1_workspace/
  sdi_v8_patched.py            (v8 baseline, unchanged)
  sdi_v22_evolution.py         (v22 new file)
  sdi_v22_ablation.py          (ablation study script)
  sdi_v22_mnist_driver.py      (MNIST spike stream driver)
  v22_results/
    ablation_comparison.png
    F_convergence.png
    phase_scan_v22.png
```

### 5.2 Key Functions

| Function | Input | Output | Status |
|----------|-------|--------|--------|
| adaptive_theta(G, L_ref, v_c) | Network graph | T_theta | To implement |
| fep_homeostasis(G, target) | Network graph | Modified weights | To implement |
| mnist_to_spikes(image, dur) | MNIST image | Spike trains | To implement |
| run_v22_simulation(config) | Config dict | Results dict | To implement |
| run_ablation_study() | - | Ablation comparison | To implement |

---

> iNEST Research Team, Tianjin University. (2026). v22 Self-Evolution Mechanism Design.
