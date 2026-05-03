import numpy as np
import matplotlib.pyplot as plt
import os

plt.style.use('default')
fig, axes = plt.subplots(1, 3, figsize=(18, 6), dpi=300)

ax1 = axes[0]
labels = ['CPU', 'GPU\n(H100)', 'ASIC\n(e.g., Groq)', 'FPGA', 'NCC\n(Liquid HW)']
flex = [9.5, 8.5, 1.5, 7.5, 9.0]
eff = [2, 20, 600, 15, 450]
colors = ['gray', '#ff7f0e', '#d62728', 'brown', '#1f77b4']
sizes = [300, 800, 800, 400, 1200]

ax1.scatter(flex, eff, c=colors, s=sizes, alpha=0.8, edgecolors='w', linewidth=2)
for i, label in enumerate(labels):
    y_offset = eff[i] * 1.4 if eff[i] < 100 else eff[i] * 0.5
    ax1.text(flex[i], y_offset, label, fontsize=11, ha='center', fontweight='bold')

ax1.set_yscale('log')
ax1.set_xlim(0, 11)
ax1.set_ylim(1, 2000)
ax1.axvline(x=5, color='k', linestyle='--', alpha=0.3)
ax1.axhline(y=50, color='k', linestyle='--', alpha=0.3)
ax1.set_xlabel('Algorithmic Flexibility / Adaptability', fontsize=12, fontweight='bold')
ax1.set_ylabel('Energy Efficiency (TOPS/W) [Log Scale]', fontsize=12, fontweight='bold')
ax1.set_title('(A) The "Magic Quadrant" of Architectures', fontsize=14, fontweight='bold')

ax1.text(8, 3, 'Flexible but\nInefficient', alpha=0.4, ha='center', fontsize=10)
ax1.text(2.5, 200, 'Efficient but Rigid\n(Algorithm Locked)', alpha=0.4, ha='center', fontsize=10)
ax1.text(8, 200, 'NCC:\nHigh Flex & High Eff\n(Network-Centric)', color='#1f77b4', fontweight='bold', ha='center', fontsize=11)

ax2 = axes[1]
nodes = np.array([1, 4, 16, 64, 256, 1024])
util_gpu = [0.98, 0.85, 0.72, 0.60, 0.52, 0.45]
util_ncc = [0.98, 0.96, 0.95, 0.94, 0.92, 0.91]

ax2.plot(nodes, util_gpu, 'o-', color='#ff7f0e', linewidth=3, markersize=8, label='GPU Cluster (Static Topology)')
ax2.plot(nodes, util_ncc, 's-', color='#1f77b4', linewidth=3, markersize=8, label='NCC (SDI Dynamic Fractal Scaling)')

ax2.set_xscale('log', base=2)
ax2.set_xticks(nodes)
ax2.set_xticklabels(nodes)
ax2.set_ylim(0.3, 1.05)
ax2.set_xlabel('Cluster Size (Number of Nodes)', fontsize=12, fontweight='bold')
ax2.set_ylabel('Effective Compute Utilization (%)', fontsize=12, fontweight='bold')
ax2.set_title('(B) Breaking the "Scaling Wall"', fontsize=14, fontweight='bold')
ax2.legend(loc='lower left', frameon=True)

ax2.fill_between(nodes, util_gpu, util_ncc, color='#2ca02c', alpha=0.15)
ax2.text(16, 0.82, 'NCC Dividend\n(Topology perfectly matching)', color='green', fontweight='bold', ha='center')

ax3 = axes[2]
categories = ['Logic Resources (ALUs)', 'Interconnect Wiring']
indep = np.array([100, 100])
ncc = np.array([65, 70]) 

x = np.arange(len(categories))
width = 0.35

ax3.bar(x - width/2, indep, width, label='Independent Design\n(AI Chip + Radar DBF Chip)', color='gray', alpha=0.6, edgecolor='black')
ax3.bar(x + width/2, ncc, width, label='NCC Liquid Hardware\n(Unified Chip)', color='#1f77b4', alpha=0.9, edgecolor='black')

ax3.set_ylabel('Normalized Resource Cost (%)', fontsize=12, fontweight='bold')
ax3.set_title('(C) Silicon Dividend via Isomorphism', fontsize=14, fontweight='bold')
ax3.set_xticks(x)
ax3.set_xticklabels(categories, fontsize=12, fontweight='bold')
ax3.set_ylim(0, 120)
ax3.legend(loc='upper right', frameon=True)

for i in range(len(categories)):
    ax3.text(i - width/2, indep[i] + 2, '100%', ha='center', fontsize=10)
    ax3.text(i + width/2, ncc[i] + 2, f'{ncc[i]}%\n(-{100-ncc[i]}%)', ha='center', color='darkgreen', fontweight='bold', fontsize=11)

plt.tight_layout()
out_dir = "/home/work/.openclaw/workspace/20_Projects/Projects/海河实验室重大专项/Figures"
os.makedirs(out_dir, exist_ok=True)
out_file = os.path.join(out_dir, "NCC_Comprehensive_Advantages.png")
plt.savefig(out_file)
print(f"Comprehensive plots saved to {out_file}")
