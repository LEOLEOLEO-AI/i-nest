import numpy as np, matplotlib.pyplot as plt
from matplotlib import gridspec, rcParams

rcParams['font.sans-serif'] = ['Microsoft YaHei', 'Arial']
rcParams['axes.unicode_minus'] = False
rcParams['font.size'] = 16

eps = np.logspace(-3, -1, 400)          # 1 - lambda
lam = 1 - eps
M = {'L1  CST复杂度收益 (下限)':      (0.02/eps,  '#C0392B', '-'),
     'L2  网络容量':                  (52.5*eps,  '#1F77B4', '-'),
     'L3  供电/热峰值':               (55.6*eps,  '#E67E22', '-'),
     'L4  学习可证明性 T1':           (50.0*eps,  '#2E7D32', '-'),
     'L5  临界安全裕度':              (62.5*eps,  '#7B4FA0', '-')}
Q = np.minimum.reduce([v[0] for v in M.values()])

fig = plt.figure(figsize=(13.33, 7.5), dpi=300)
gs = gridspec.GridSpec(1, 2, width_ratios=[2.1, 1], wspace=0.28)
ax, bx = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])

for k, (y, c, ls) in M.items():
    lw = 3.4 if k.startswith(('L1', 'L4')) else 2.2
    ax.plot(lam, y, ls, color=c, lw=lw, label=k)
ax.axhspan(1e-2, 1, color='0.85', alpha=.55, zorder=0)      # 不可行区
ax.axhline(1, color='k', lw=1.6, ls='--')
ax.axvline(0.98, color='k', lw=1.8, ls=':')
ax.plot(0.98, 1.0, 'o', ms=15, mfc='#FFD54F', mec='k', mew=2, zorder=5)
ax.annotate(r'$\lambda^{*}=0.98$', xy=(0.98, 1.0), xytext=(0.935, 3.2),
            fontsize=21, fontweight='bold',
            arrowprops=dict(arrowstyle='->', lw=2))
ax.text(0.9035, 0.30, '不可行区  裕度 < 1', fontsize=15, color='0.3')

ax.set_xscale('logit'); ax.set_yscale('log')
ax.set_xlim(0.90, 0.999); ax.set_ylim(3e-2, 3e1)
ax.set_xticks([0.90, 0.95, 0.98, 0.99, 0.995, 0.999])
ax.set_xticklabels(['0.90','0.95','0.98','0.99','0.995','0.999'])
ax.set_xlabel(r'分支比  $\lambda_{br}$   （临界距离 $\varepsilon=1-\lambda_{br}$ 向右减小）', fontsize=18)
ax.set_ylabel('归一化设计裕度  $M$', fontsize=18)
ax.set_title('五条独立约束交汇于同一分支比', fontsize=22, fontweight='bold', pad=12)
ax.grid(alpha=.3, which='both'); ax.legend(fontsize=14.5, loc='upper right', framealpha=.95)
ax.text(0.9035, 12, r'工程上限族  $M\propto\varepsilon$', fontsize=14, color='#1F77B4')
ax.text(0.9905, 12, r'收益  $M\propto\varepsilon^{-1}$', fontsize=14, color='#C0392B')

bx.plot(lam, Q, color='#111', lw=3.6)
bx.fill_between(lam, 3e-2, Q, color='#FFD54F', alpha=.35)
bx.axvline(0.98, color='k', lw=1.8, ls=':')
bx.plot(0.98, 1.0, 'o', ms=13, mfc='#FFD54F', mec='k', mew=2, zorder=5)
bx.set_xscale('logit'); bx.set_yscale('log')
bx.set_xlim(0.90, 0.999); bx.set_ylim(3e-2, 3e0)
bx.set_xticks([0.90, 0.95, 0.98, 0.99, 0.999])
bx.set_xticklabels(['0.90','0.95','0.98','0.99','0.999'])
bx.set_xlabel(r'$\lambda_{br}$', fontsize=18)
bx.set_ylabel(r'综合品质因子  $Q=\min_i M_i$', fontsize=17)
bx.set_title('单峰最优', fontsize=22, fontweight='bold', pad=12)
bx.grid(alpha=.3, which='both')

fig.text(0.5, 0.015, '注：L1/L4 为紧约束，L2/L3/L5 余量 5%–25%。'
         '参数：$\\Delta t$=4 ms，学习时标 10 s，$\\sigma_{drift}$=0.004，'
         '峰值功率设计点 20 kW。', ha='center', fontsize=13.5, color='0.35')
plt.subplots_adjust(left=.07, right=.985, top=.90, bottom=.13)
plt.savefig('lambda_star_convergence.svg')
plt.savefig('lambda_star_convergence.png', dpi=300)
plt.show()
