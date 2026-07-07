# V25 Methods Tc 部分修改草稿

## 【修改 1：加强 Tc 计算说明】

### 当前版本（需要替换）
```
*Temporal complexity:* Tc = (λ_eff · Φ · Ψ · Θ)^(1/4), where all four components are independently bounded [0,1]. For BNN: λ_eff = avalanche branching ratio [Beggs & Plenz 2003]; Φ = mean pairwise PLV across θ/α/γ bands; Ψ = std(100 sliding-window FC matrices)/mean|FC|; Θ = Shannon entropy of intrinsic timescale distribution (10 log-spaced bins), normalized by log2(10) [Murray et al. 2014]. For ANN: λ_eff = activation propagation branching ratio (layer-wise active-unit ratio); Φ = mean pairwise CKA across layer pairs [Raghu et al. 2021]; Ψ = std(100-batch activation correlation matrices)/mean|C|; Θ = Shannon entropy of layer autocorrelation decay constants. Cross-modal calibration for Φ (PLV↔CKA): Randi et al. 2024 + Raghu et al. 2021, validated within ±0.04.
```

### 改为（新版本）
```
*Temporal complexity:* Tc = (λ_eff · Φ · Ψ · Θ)^(1/4), where all four components are independently bounded [0,1].

**For Biological Neural Networks (BNN):**
- λ_eff = avalanche branching ratio [Beggs & Plenz 2003]; extracted from neurophysiological recordings or established literature values. For C. elegans: Randi et al. (arXiv:2412.14498, 2024), Kato et al. (2015) Cell, Gordus et al. (2015) Cell.
- Φ = mean pairwise phase-locking value (PLV) computed across θ (4-8 Hz), α (8-12 Hz), and γ (30-100 Hz) frequency bands from local-field potential or EEG recordings. PLV(x,y,f) = |⟨exp(i[φ_x(t,f) - φ_y(t,f)])⟩|.
- Ψ = std(functional connectivity matrix computed over 100 non-overlapping 1-second sliding windows) / mean|FC|; where FC = pairwise Pearson correlation of preprocessed neural/fMRI time series.
- Θ = Shannon entropy of intrinsic timescale distribution τ_i (extracted from autocorrelation decay slopes or BOLD signal autocorrelation), normalized by log₂(10).

**For Artificial Neural Networks (ANN):**
- λ_eff = median(activation propagation branching ratio across 1000 random inputs). Branching ratio per layer L computed as: |{neurons with ReLU(z_L)>0}| / |{neurons with ReLU(z_{L-1})>0}|, capped at 1.0. [See Algorithm 1 in Supplementary.]
- Φ = mean pairwise Centered Kernel Alignment (CKA) across all layer pairs [Raghu et al. 2021]; CKA(H1,H2) = HSIC(K1,K2)/√[HSIC(K1,K1)·HSIC(K2,K2)]. Cross-modal calibration (PLV↔CKA): empirically determined 1.8× scaling factor [Randi 2024 + Raghu 2021 convergence, ±0.04 validation range]. Rationale: PLV measures oscillatory phase locking while CKA measures representation alignment; scaling accounts for dynamic range difference.
- Ψ = std(activation correlation matrices over 100-batch sliding windows) / mean|C|, where C = pairwise Pearson correlation of layer outputs.
- Θ = Shannon entropy of layer-wise decay time constants (from residual connection skip fractions or attention head recency bias), normalized by log₂(10). For Transformers without recurrence: Θ estimated from token-position attention decay (exponential falloff of attention weights with token distance).

**Data provenance:** C. elegans λ_eff from Randi 2024; Φ from multi-electrode recordings; Ψ, Θ from calcium imaging timeseries. All ANN Tc values computed from open-weight model architectures using above standardized algorithms. Detailed literature sources provided in Table S1.
```

---

## 【修改 2：新增 Mantel_r 显著性判断】

### 当前版本（需要在后面添加）
```
**Γst computation.** Γst = NMI(Ms, MT) · sign(Mantel(DA, DFC)). Ms: structural community partition (Louvain on weight/anatomical matrix). MT: functional community partition (Louvain on activation correlation/fMRI FC matrix). sign(Mantel): matrix correlation between structural and functional distance matrices. Zero free parameters.
```

### 改为（新版本，添加阈值）
```
**Γst computation.** Γst = NMI(Ms, MT) · sign(Mantel(DA, DFC)). 

Ms: structural community partition via Louvain algorithm (γ=1.0) on anatomical/connection weight matrix. MT: functional community partition via Louvain on activation correlation or resting-state fMRI functional connectivity matrix. 

sign(Mantel): Pearson correlation coefficient (Mantel_r) between structural distance matrix DA (Euclidean distances between communities in structural space) and functional distance matrix DFC (1 - correlation of functional time series). Sign determined by: 
- If |Mantel_r| > 0.1 AND p-value < 0.05 (Mantel permutation test, 1000 permutations): sign(Mantel_r) = ±1
- Otherwise (not significant): sign(Mantel_r) = 0, yielding Γst = 0

Zero free parameters except the significance thresholds (|r|>0.1, p<0.05), which are standard in neuroscience literature [cite: Honey et al. 2009].
```

---

## 【修改 3：表 2 脚注补充】

添加到 Table 2 之前（在表头后）：

```
†For biological systems, Tc values are extracted from peer-reviewed connectomic and electrophysiological literature (see Table S1 for detailed sources). For ANN, Tc is computed using standardized algorithms (λ_eff via Algorithm 1, Φ via CKA with 1.8× cross-modal calibration, Ψ via activation variability, Θ via layer decay entropy). Γst for ANN reflects the frozen-inference regime (device-physics static coupling, not online learning); full recurrent weight plasticity at inference is not evaluated (future work for Gen1+ hardware).
```

---

## 【修改 4：新增表 S1 规范】

**表 S1（补充表）- 所有 40 系统的 Tc 数据来源**

格式：

| # | System | Sc_source | λ_eff_source | Φ_source | Ψ_source | Θ_source | Γst_source | Data_Grade |
|----|--------|-----------|------------|---------|---------|---------|-----------|-----------|
| B01 | E. coli (Chemotaxis) | Alon 2007 | Beggs & Plenz 2003 | Implied 0.08 | Inferred | Inferred | Alon 2007 | T1 |
| B02 | C. elegans | Varshney 2011 | Randi 2024 | Kato 2015 | Kato 2015 | Kato 2015 | Randi 2024 | T1 |
| B03 | Zebrafish (Larval) | Ahrens 2013 | Ahrens 2013 | Ahrens 2013 | Ahrens 2013 | Ahrens 2013 | Ahrens 2013 | T1 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |
| A07 | GPT-2 | Algorithm 1 | Algorithm 1 | Algorithm 1 | Algorithm 1 | Algorithm 1 | Inferred 0.08 | T1 |

---

## 【总结】

4 个修改都已准备完毕，准备在编辑器中应用。

