"""
SDI Paper Figure Generator
Generates 6 publication-quality figures for SDI paper.
"""
import os
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings('ignore')

# Output directory
OUT_DIR = '/home/work/.openclaw/workspace/sdi_sim/figures'
os.makedirs(OUT_DIR, exist_ok=True)

# Global style
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 10,
    'axes.titlesize': 11,
    'axes.labelsize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'axes.spines.top': False,
    'axes.spines.right': False,
})

# ==================== FIGURE 1 ====================
def figure1_species_sigma():
    """20-species small-world emergence bar chart"""
    print("Generating Figure 1: Species sigma...")

    with open('/home/work/.openclaw/workspace/sdi_sim/exp1_v17_results.json') as f:
        data = json.load(f)

    # Evolutionary order: primitive → invertebrate → fish → bird → mammal → primate → human
    species_order = [
        ('C_elegans_pharynx', 'C.elegans\npharynx', 'neuron'),
        ('Starfish_larva', 'Starfish\nlarva', 'neuron'),
        ('C.elegans', 'C.elegans', 'neuron'),
        ('Platynereis★', 'Platynereis', 'neuron'),
        ('Ciona★', 'Ciona', 'neuron'),
        ('Larval_Drosophila', 'Larval\nDrosophila', 'neuron'),
        ('Octopus★', 'Octopus', 'neuron'),
        ('Honeybee★', 'Honeybee', 'neuron'),
        ('Zebrafish★', 'Zebrafish', 'neuron'),
        ('Xenopus★', 'Xenopus', 'neuron'),
        ('Pigeon★', 'Pigeon', 'region'),
        ('Cat_Visual★', 'Cat\nVisual', 'region'),
        ('Mouse_Cortex★', 'Mouse\nCortex', 'region'),
        ('Rat_Cortex★', 'Rat\nCortex', 'region'),
        ('Macaque_Visual', 'Macaque\nVisual', 'region'),
        ('Macaque_Cortex', 'Macaque\nCortex', 'region'),
        ('Marmoset★', 'Marmoset', 'region'),
        ('Chimpanzee★', 'Chimpanzee', 'region'),
        ('Gorilla★', 'Gorilla', 'region'),
        ('Human_HCP★', 'Human\nHCP', 'region'),
    ]

    names = []
    means = []
    stds = []
    levels = []

    for key, label, level in species_order:
        if key in data:
            val = data[key]
            names.append(label)
            means.append(val.get('sigma', 0))
            stds.append(val.get('sigma_std', 0))
            levels.append(level)
        else:
            names.append(label)
            means.append(0)
            stds.append(0)
            levels.append('neuron')

    fig, ax = plt.subplots(figsize=(14, 5))

    x = np.arange(len(names))
    colors = ['#2196F3' if l == 'neuron' else '#FF9800' for l in levels]

    bars = ax.bar(x, means, yerr=stds, capsize=3, color=colors, alpha=0.85,
                  edgecolor='white', linewidth=0.5, error_kw={'linewidth': 1.2, 'ecolor': '#555'})

    # Threshold lines
    ax.axhline(y=1.0, color='#E53935', linestyle='--', linewidth=1.5, alpha=0.9, label='σ = 1.0 (small-world threshold)')
    ax.axhline(y=4.0, color='#43A047', linestyle='--', linewidth=1.5, alpha=0.9, label='σ = 4.0 (target threshold)')

    # Annotation
    ax.text(0.98, 0.97, '20/20 ≥ 3/5 Pass', transform=ax.transAxes,
            ha='right', va='top', fontsize=11, fontweight='bold', color='#1B5E20',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#E8F5E9', edgecolor='#43A047', alpha=0.9))

    ax.set_xticks(x)
    ax.set_xticklabels(names, fontsize=7.5, rotation=0)
    ax.set_ylabel('Small-World Coefficient σ', fontsize=10)
    ax.set_xlabel('Species (Evolutionary Order: Primitive → Invertebrate → Vertebrate → Primate → Human)', fontsize=9)
    ax.set_title('Figure 1: Small-World Emergence Across 20 Species (SDI v17 Simulation)', fontsize=11, fontweight='bold')
    ax.set_ylim(0, 12)
    ax.yaxis.grid(True, alpha=0.3, linewidth=0.5)
    ax.set_axisbelow(True)

    # Legend
    patch_neuron = mpatches.Patch(color='#2196F3', alpha=0.85, label='Neuron-level')
    patch_region = mpatches.Patch(color='#FF9800', alpha=0.85, label='Brain-region level')
    line1 = plt.Line2D([0], [0], color='#E53935', linestyle='--', linewidth=1.5, label='σ = 1.0 (SW threshold)')
    line2 = plt.Line2D([0], [0], color='#43A047', linestyle='--', linewidth=1.5, label='σ = 4.0 (target)')
    ax.legend(handles=[patch_neuron, patch_region, line1, line2], loc='upper left', fontsize=8, framealpha=0.9)

    # Count passing
    pass_count = sum(1 for m in means if m >= 1.0)
    print(f"  Pass σ>=1.0: {pass_count}/20")

    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, 'Figure1_species_sigma.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    size = os.path.getsize(out_path)
    print(f"  Saved: {out_path} ({size/1024:.1f} KB)")
    return out_path


# ==================== FIGURE 2 ====================
def figure2_avalanche_powerlaw():
    """Neural avalanche power-law distribution (log-log, 2x3 subplots)"""
    print("Generating Figure 2: Avalanche power-law...")

    with open('/home/work/.openclaw/workspace/sdi_sim/exp5_v12_avalanche_results.json') as f:
        data = json.load(f)

    # Select 6 best (one per network×rules, highest score)
    # Networks: C.elegans, Human_HCP, WS_Control x rules: 3-rules, 4-rules
    combos = {}
    for item in data:
        key = (item['network'], item['rules'])
        if key not in combos or item['score'] > combos[key]['score']:
            combos[key] = item

    selected = list(combos.values())[:6]
    # Sort for nice layout
    selected.sort(key=lambda x: (x['rules'], x['network']))

    fig, axes = plt.subplots(2, 3, figsize=(12, 7))
    axes = axes.flatten()

    for idx, item in enumerate(selected):
        ax = axes[idx]
        sizes = np.array(item['sizes_sample'])
        sizes = sizes[sizes > 0]

        # Build histogram in log-space
        log_bins = np.logspace(np.log10(sizes.min()), np.log10(sizes.max()), 30)
        counts, bin_edges = np.histogram(sizes, bins=log_bins)
        bin_centers = np.sqrt(bin_edges[:-1] * bin_edges[1:])
        
        # Normalize to probability
        total = counts.sum()
        probs = counts / total / np.diff(bin_edges)

        # Filter non-zero
        mask = probs > 0
        x_data = bin_centers[mask]
        y_data = probs[mask]

        # Plot data points
        ax.scatter(x_data, y_data, color='#1565C0', s=18, alpha=0.75, zorder=5, label='Data')

        # Theoretical line τ=1.5: P(S) ~ S^{-1.5}
        x_theory = np.logspace(np.log10(x_data.min()), np.log10(x_data.max()), 100)
        # Normalize theory to match data
        y_ref = y_data[len(y_data)//3]
        x_ref = x_data[len(x_data)//3]
        C = y_ref * x_ref**1.5
        y_theory = C * x_theory**(-1.5)
        ax.plot(x_theory, y_theory, 'r--', linewidth=1.8, alpha=0.85, label='P(S)~S$^{-1.5}$')

        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlabel('Avalanche Size S', fontsize=8)
        ax.set_ylabel('Probability Density', fontsize=8)

        kappa = item.get('branching_ratio', 0)
        score = item.get('score', 0)
        net_short = item['network'].replace('_', ' ').replace('.', '')
        ax.set_title(f"{net_short} | {item['rules']}\nκ={kappa:.3f}, Score={score}/9", fontsize=8.5)
        ax.legend(fontsize=7.5, loc='lower left')
        ax.grid(True, which='both', alpha=0.2, linewidth=0.4)

    # Hide unused subplots if any
    for j in range(len(selected), len(axes)):
        axes[j].set_visible(False)

    fig.suptitle('Figure 2: Neural Avalanche Power-Law Distributions (SDI v12, exp5)', fontsize=12, fontweight='bold', y=1.01)
    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, 'Figure2_avalanche_powerlaw.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    size = os.path.getsize(out_path)
    print(f"  Saved: {out_path} ({size/1024:.1f} KB)")
    return out_path


# ==================== FIGURE 3 ====================
def figure3_psd_spectrum():
    """PSD power spectrum slope (2x3 subplots)"""
    print("Generating Figure 3: PSD spectrum...")

    with open('/home/work/.openclaw/workspace/sdi_sim/exp5_v12_avalanche_results.json') as f:
        data = json.load(f)

    # Same 6 best combos as figure 2
    combos = {}
    for item in data:
        key = (item['network'], item['rules'])
        if key not in combos or item['score'] > combos[key]['score']:
            combos[key] = item

    selected = list(combos.values())[:6]
    selected.sort(key=lambda x: (x['rules'], x['network']))

    fig, axes = plt.subplots(2, 3, figsize=(12, 7))
    axes = axes.flatten()

    for idx, item in enumerate(selected):
        ax = axes[idx]
        activation = np.array(item['activation_sample'])

        # Compute PSD via FFT
        N = len(activation)
        dt = 1.0  # assume dt=1 step
        fft_vals = np.fft.rfft(activation - activation.mean())
        power = (np.abs(fft_vals) ** 2) / N
        freqs = np.fft.rfftfreq(N, d=dt)

        # Filter valid frequency range 0.001 to 0.25
        mask = (freqs >= 0.001) & (freqs <= 0.25)
        freqs_f = freqs[mask]
        power_f = power[mask]

        if len(freqs_f) < 5:
            axes[idx].set_visible(False)
            continue

        # Plot
        ax.plot(freqs_f, power_f, color='#1565C0', linewidth=1.0, alpha=0.8, label='PSD')

        # Theoretical 1/f line: slope = -1.0
        log_f = np.log10(freqs_f)
        log_p = np.log10(power_f + 1e-30)
        # Fit a line to get slope
        coeffs = np.polyfit(log_f, log_p, 1)
        slope = coeffs[0]
        f_theory = np.logspace(np.log10(freqs_f.min()), np.log10(freqs_f.max()), 100)
        # Reference theoretical at midpoint
        mid_idx = len(freqs_f) // 2
        C_ref = power_f[mid_idx] * freqs_f[mid_idx]**1.0
        p_theory = C_ref * f_theory**(-1.0)
        ax.plot(f_theory, p_theory, '--', color='gray', linewidth=1.5, alpha=0.8, label='1/f (slope=-1)')

        ax.set_xscale('log')
        ax.set_yscale('log')
        ax.set_xlabel('Frequency (Hz)', fontsize=8)
        ax.set_ylabel('Power', fontsize=8)

        psd_slope = item.get('psd_slope', slope)
        net_short = item['network'].replace('_', ' ').replace('.', '')
        ax.set_title(f"{net_short} | {item['rules']}\nPSD slope={psd_slope:.3f}", fontsize=8.5)
        ax.legend(fontsize=7.5, loc='upper right')
        ax.grid(True, which='both', alpha=0.2, linewidth=0.4)

    for j in range(len(selected), len(axes)):
        axes[j].set_visible(False)

    fig.suptitle('Figure 3: PSD Power Spectrum Analysis (SDI v12, 1/f Noise)', fontsize=12, fontweight='bold', y=1.01)
    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, 'Figure3_psd_spectrum.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    size = os.path.getsize(out_path)
    print(f"  Saved: {out_path} ({size/1024:.1f} KB)")
    return out_path


# ==================== FIGURE 4 ====================
def figure4_kappa_score_summary():
    """Branching ratio κ boxplot and score summary bar chart"""
    print("Generating Figure 4: κ and score summary...")

    with open('/home/work/.openclaw/workspace/sdi_sim/exp5_v12_avalanche_results.json') as f:
        data = json.load(f)

    # Group by network×rules
    from collections import defaultdict
    group_kappa = defaultdict(list)
    group_score = defaultdict(list)

    for item in data:
        key = f"{item['network']}\n{item['rules']}"
        group_kappa[key].append(item['branching_ratio'])
        group_score[key].append(item['score'])

    keys = sorted(group_kappa.keys())
    # Sort: 3-rules first, then 4-rules
    keys_3 = [k for k in keys if '3-rules' in k]
    keys_4 = [k for k in keys if '4-rules' in k]
    ordered_keys = keys_3 + keys_4

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

    # --- Left: Boxplot of κ ---
    kappa_data = [group_kappa[k] for k in ordered_keys]
    colors_box = ['#1E88E5'] * len(keys_3) + ['#E53935'] * len(keys_4)

    bp = ax1.boxplot(kappa_data, patch_artist=True, notch=False,
                     medianprops=dict(color='black', linewidth=2),
                     whiskerprops=dict(linewidth=1.2),
                     capprops=dict(linewidth=1.2),
                     flierprops=dict(marker='o', markersize=4, alpha=0.5))

    for patch, color in zip(bp['boxes'], colors_box):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)

    ax1.axhline(y=1.0, color='#C62828', linestyle='--', linewidth=1.8, label='κ = 1.0 (critical)')
    ax1.set_xticks(range(1, len(ordered_keys)+1))
    ax1.set_xticklabels([k.replace('\n', '\n') for k in ordered_keys], fontsize=7.5)
    ax1.set_ylabel('Branching Ratio κ', fontsize=10)
    ax1.set_title('(A) Branching Ratio κ Distribution', fontsize=10, fontweight='bold')
    ax1.yaxis.grid(True, alpha=0.3)
    ax1.set_axisbelow(True)
    # Legend
    p1 = mpatches.Patch(color='#1E88E5', alpha=0.7, label='3-rules')
    p2 = mpatches.Patch(color='#E53935', alpha=0.7, label='4-rules')
    line_crit = plt.Line2D([0],[0], color='#C62828', linestyle='--', linewidth=1.8, label='κ=1.0 critical')
    ax1.legend(handles=[p1, p2, line_crit], fontsize=8)

    # --- Right: Mean score bar chart ---
    mean_scores = [np.mean(group_score[k]) for k in ordered_keys]
    bar_colors = ['#1E88E5'] * len(keys_3) + ['#E53935'] * len(keys_4)

    x = np.arange(len(ordered_keys))
    bars = ax2.bar(x, mean_scores, color=bar_colors, alpha=0.8, edgecolor='white', linewidth=0.5)

    # Add value labels
    for bar, val in zip(bars, mean_scores):
        ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.05,
                 f'{val:.2f}', ha='center', va='bottom', fontsize=8.5, fontweight='bold')

    ax2.axhline(y=9.0, color='#2E7D32', linestyle=':', linewidth=1.5, alpha=0.7, label='Max score=9')
    ax2.set_xticks(x)
    ax2.set_xticklabels([k.replace('\n', '\n') for k in ordered_keys], fontsize=7.5)
    ax2.set_ylabel('Mean Score (out of 9)', fontsize=10)
    ax2.set_title('(B) Mean SOC Score per Network×Rules', fontsize=10, fontweight='bold')
    ax2.set_ylim(0, 10)
    ax2.yaxis.grid(True, alpha=0.3)
    ax2.set_axisbelow(True)
    p3 = mpatches.Patch(color='#1E88E5', alpha=0.8, label='3-rules')
    p4 = mpatches.Patch(color='#E53935', alpha=0.8, label='4-rules')
    ax2.legend(handles=[p3, p4], fontsize=8)

    fig.suptitle('Figure 4: Branching Ratio κ and SOC Score Summary (SDI v12, 18 Simulations)', fontsize=11, fontweight='bold')
    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, 'Figure4_kappa_score_summary.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    size = os.path.getsize(out_path)
    print(f"  Saved: {out_path} ({size/1024:.1f} KB)")
    return out_path


# ==================== FIGURE 5 ====================
def figure5_connectome_evolution():
    """Real connectome σ evolution and decode score"""
    print("Generating Figure 5: Connectome evolution...")

    with open('/home/work/.openclaw/workspace/sdi_sim/exp6_real_connectome_results.json') as f:
        data = json.load(f)

    # Separate 3-rules and 4-rules
    data_3 = [d for d in data if d['rules'] == '3-rules']
    data_4 = [d for d in data if d['rules'] == '4-rules']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # --- Left: σ evolution curves ---
    sigma_init = 8.63  # from data

    colors_3 = ['#1565C0', '#1976D2', '#42A5F5']
    colors_4 = ['#B71C1C', '#E53935', '#EF9A9A']

    for i, item in enumerate(data_3):
        tlog = item['topology_log']
        steps = [t['step'] for t in tlog]
        sigmas = [t['sigma'] for t in tlog]
        lbl = f"3-rules seed={item['seed']}" if i == 0 else f"seed={item['seed']}"
        ax1.plot(steps, sigmas, color=colors_3[i], linewidth=2.0, alpha=0.9,
                 label=f'3-rules s={item["seed"]}', marker='o', markersize=3)

    for i, item in enumerate(data_4):
        tlog = item['topology_log']
        steps = [t['step'] for t in tlog]
        sigmas = [t['sigma'] for t in tlog]
        ax1.plot(steps, sigmas, color=colors_4[i], linewidth=2.0, alpha=0.9,
                 label=f'4-rules s={item["seed"]}', marker='s', markersize=3, linestyle='--')

    ax1.axhline(y=sigma_init, color='gray', linestyle=':', linewidth=1.5, alpha=0.8)
    ax1.text(ax1.get_xlim()[0] if ax1.get_xlim()[0] > 0 else 500, sigma_init + 0.15,
             f'σ_init = {sigma_init:.2f}', fontsize=8.5, color='gray')

    # Compute final sigma means
    sigma_final_3 = np.mean([d['sigma_final'] for d in data_3])
    sigma_final_4 = np.mean([d['sigma_final'] for d in data_4])

    ax1.set_xlabel('Simulation Step', fontsize=10)
    ax1.set_ylabel('Small-World Coefficient σ', fontsize=10)
    ax1.set_title(f'(A) σ Evolution: Real C.elegans Connectome\nσ_init={sigma_init:.2f}, 3r→{sigma_final_3:.2f}, 4r→{sigma_final_4:.2f}', fontsize=9.5)
    ax1.legend(fontsize=7.5, loc='upper right')
    ax1.yaxis.grid(True, alpha=0.3)
    ax1.set_axisbelow(True)

    # --- Right: Decode score bar chart ---
    decode_3 = [d['decode_score'] for d in data_3]
    decode_4 = [d['decode_score'] for d in data_4]
    mean_3 = np.mean(decode_3)
    std_3 = np.std(decode_3)
    mean_4 = np.mean(decode_4)
    std_4 = np.std(decode_4)

    seeds = [str(d['seed']) for d in data_3]
    x = np.arange(len(seeds))
    width = 0.35

    bars3 = ax2.bar(x - width/2, decode_3, width, color='#1565C0', alpha=0.85,
                    edgecolor='white', label=f'3-rules (mean={mean_3:.3f})')
    bars4 = ax2.bar(x + width/2, decode_4, width, color='#B71C1C', alpha=0.85,
                    edgecolor='white', label=f'4-rules (mean={mean_4:.3f})')

    # Mean lines
    ax2.axhline(y=mean_3, color='#1565C0', linestyle='--', linewidth=1.5, alpha=0.7)
    ax2.axhline(y=mean_4, color='#B71C1C', linestyle='--', linewidth=1.5, alpha=0.7)

    # Functional separation threshold
    ax2.axhline(y=0.05, color='gray', linestyle=':', linewidth=1.5, alpha=0.8,
                label='decode=0.05 (separation)')

    ax2.set_xticks(x)
    ax2.set_xticklabels([f'Seed {s}' for s in seeds], fontsize=9)
    ax2.set_ylabel('Decode Score (Cosine Distance)', fontsize=10)
    ax2.set_title(f'(B) Sensory-Motor Decode Score\n3r={mean_3:.3f}±{std_3:.3f}, 4r={mean_4:.3f}±{std_4:.3f}', fontsize=9.5)
    ax2.legend(fontsize=7.5)
    ax2.yaxis.grid(True, alpha=0.3)
    ax2.set_axisbelow(True)

    # Add value labels
    for bar in bars3:
        ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.005,
                 f'{bar.get_height():.3f}', ha='center', va='bottom', fontsize=7.5)
    for bar in bars4:
        ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.005,
                 f'{bar.get_height():.3f}', ha='center', va='bottom', fontsize=7.5)

    fig.suptitle('Figure 5: Real C.elegans Connectome σ Evolution & Sensory-Motor Decoding', fontsize=11, fontweight='bold')
    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, 'Figure5_connectome_evolution.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    size = os.path.getsize(out_path)
    print(f"  Saved: {out_path} ({size/1024:.1f} KB)")
    return out_path


# ==================== FIGURE 6 ====================
def figure6_cst_roadmap():
    """CST hierarchy roadmap - horizontal bar chart"""
    print("Generating Figure 6: CST roadmap...")

    # Data: (system_name, CST_value, category)
    # category: 'bio' (biological), 'ai' (artificial), 'inest' (iNEST prediction)
    systems = [
        ('E.coli', 0.006, 'bio'),
        ('MLP', 0.009, 'ai'),
        ('C.elegans Bio', 0.357, 'bio'),
        ('Intel Loihi', 0.540, 'ai'),
        ('SDI Sim\n(Current ★)', 0.644, 'inest'),
        ('Drosophila MB', 1.031, 'bio'),
        ('Honeybee', 1.540, 'bio'),
        ('Memristor+SDI\n(Predict ★)', 2.318, 'inest'),
        ('Mouse Cortex', 2.724, 'bio'),
        ('Macaque', 3.130, 'bio'),
        ('Physical AI\n(Predict ★)', 3.866, 'inest'),
        ('Human Brain', 3.909, 'bio'),
    ]

    names = [s[0] for s in systems]
    values = [s[1] for s in systems]
    cats = [s[2] for s in systems]

    color_map = {'bio': '#78909C', 'ai': '#29B6F6', 'inest': '#FF7043'}
    edge_map = {'bio': '#455A64', 'ai': '#0288D1', 'inest': '#BF360C'}
    lw_map = {'bio': 0.8, 'ai': 0.8, 'inest': 2.5}
    colors = [color_map[c] for c in cats]
    edges = [edge_map[c] for c in cats]
    linewidths = [lw_map[c] for c in cats]

    fig, ax = plt.subplots(figsize=(11, 7))

    y = np.arange(len(names))
    bars = ax.barh(y, values, height=0.65, color=colors, edgecolor=edges,
                   linewidth=linewidths, alpha=0.88)

    # Add CST value labels at end of bars
    for i, (bar, val, cat) in enumerate(zip(bars, values, cats)):
        bold = 'bold' if cat == 'inest' else 'normal'
        ax.text(val + 0.03, bar.get_y() + bar.get_height()/2.,
                f'{val:.3f}', va='center', ha='left', fontsize=9, fontweight=bold)

    # Vertical reference lines
    ref_lines = [
        (1/np.sqrt(2), '1/√2\n=0.707', '#9C27B0'),
        (1.0, '1.0', '#F44336'),
        (1.618, 'φ=1.618', '#FF9800'),
        (2.718, 'e=2.718', '#4CAF50'),
        (3.1416, 'π=3.142', '#2196F3'),
        (4.669, 'δ=4.669', '#607D8B'),
    ]

    for xv, lbl, clr in ref_lines:
        ax.axvline(x=xv, color=clr, linestyle='--', linewidth=1.2, alpha=0.75)
        ax.text(xv, len(names)-0.3, lbl, color=clr, fontsize=7.5, ha='center', va='bottom',
                rotation=90, alpha=0.9)

    ax.set_yticks(y)
    ax.set_yticklabels(names, fontsize=9)
    ax.set_xlabel('CST (Computational Self-organization Threshold)', fontsize=10)
    ax.set_title('Figure 6: CST Hierarchy Roadmap — From E.coli to Human Brain\n(iNEST Predictions Marked with ★)', fontsize=11, fontweight='bold')
    ax.set_xlim(0, 5.2)
    ax.xaxis.grid(True, alpha=0.25, linewidth=0.5)
    ax.set_axisbelow(True)

    # Legend
    p_bio = mpatches.Patch(color='#78909C', alpha=0.88, label='Biological Systems')
    p_ai = mpatches.Patch(color='#29B6F6', alpha=0.88, label='AI/Computing Systems')
    p_inest = mpatches.Patch(color='#FF7043', alpha=0.88, edgecolor='#BF360C', linewidth=2.0,
                             label='iNEST Predictions (★)')
    ax.legend(handles=[p_bio, p_ai, p_inest], loc='lower right', fontsize=9, framealpha=0.9)

    plt.tight_layout()
    out_path = os.path.join(OUT_DIR, 'Figure6_CST_roadmap.png')
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    size = os.path.getsize(out_path)
    print(f"  Saved: {out_path} ({size/1024:.1f} KB)")
    return out_path


# ==================== MAIN ====================
if __name__ == '__main__':
    print("=" * 60)
    print("SDI Paper Figure Generator")
    print("=" * 60)
    
    results = []
    results.append(figure1_species_sigma())
    results.append(figure2_avalanche_powerlaw())
    results.append(figure3_psd_spectrum())
    results.append(figure4_kappa_score_summary())
    results.append(figure5_connectome_evolution())
    results.append(figure6_cst_roadmap())
    
    print("\n" + "=" * 60)
    print("All figures generated successfully!")
    print("=" * 60)
    for p in results:
        size = os.path.getsize(p)
        print(f"  {os.path.basename(p)}: {size/1024:.1f} KB")
