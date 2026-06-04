import json, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

with open('D:/Obsidian/phase1_workspace/v30_results/v30_results.json','r') as f:
    r = json.load(f)

pc = r['phototaxis_chemotaxis']
pm = r['pattern_memory']

fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))

# Plot 1: Trajectory
ax = axes[0]
traj = np.array(pc['trajectory'])
light_pos = [75, 50]
chem_src = [85, 85]
ax.plot(traj[:,0], traj[:,1], 'b-', linewidth=0.8, alpha=0.7)
ax.scatter(traj[0,0], traj[0,1], c='green', s=80, label='Start', zorder=5)
ax.scatter(traj[-1,0], traj[-1,1], c='red', s=80, label='End', zorder=5)
ax.scatter(light_pos[0], light_pos[1], c='yellow', s=200, marker='*', edgecolors='orange', linewidths=1.5, label='Light', zorder=5)
ax.scatter(chem_src[0], chem_src[1], c='cyan', s=150, marker='s', edgecolors='blue', linewidths=1.5, label='Chemical', zorder=5)
ax.set_xlim(0, 100); ax.set_ylim(0, 100)
ax.set_xlabel('X'); ax.set_ylabel('Y')
pi_str = 'PI=' + str(round(pc['phototaxis'], 3))
ci_str = 'CI=' + str(round(pc['chemotaxis'], 3))
ax.set_title('V30 Agent Trajectory (' + pi_str + ' ' + ci_str + ')')
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3)

# Plot 2: Distance
ax = axes[1]
pos_x = pc['pos_x']
light_dist = [abs(x - 75) for x in pos_x]
steps = list(range(0, len(light_dist)*100, 100))[:len(light_dist)]
ax.plot(steps, light_dist, 'orange', linewidth=2)
ax.set_xlabel('Step'); ax.set_ylabel('Distance to Light')
ax.set_title('Light Approach Over Time')
ax.grid(True, alpha=0.3)

# Plot 3: Accuracy
ax = axes[2]
epochs = list(range(1, len(pm['accuracy'])+1))
acc_pct = [a*100 for a in pm['accuracy']]
ax.bar(epochs, acc_pct, color='steelblue', edgecolor='navy')
ax.axhline(y=70, color='red', linestyle='--', label='Threshold 70%')
ax.set_xlabel('Epoch'); ax.set_ylabel('Accuracy (%)')
ax.set_title('Pattern Memory (' + str(round(pm['accuracy_final']*100)) + '%)')
ax.set_ylim(0, 110)
ax.legend(fontsize=8)
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('D:/Obsidian/phase1_workspace/v30_results/v30_summary.png', dpi=150, bbox_inches='tight')
plt.close()
print('Saved.')
