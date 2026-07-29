#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
iNEST × SDDE 三图可视化脚本
============================
期刊视觉风格 : Physical Review E (深蓝-橙高对比, 物理质感)
输出         : 300 dpi TIFF + PDF (矢量, 投稿/PPT 双兼容)
依赖         : numpy, matplotlib (>= 3.5)
作者         : iNEST × SDDE 联合工作流
日期         : 2026-07-25
用法         : python inest_sdde_visualization.py
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import rcParams
import os

# ============================================================
# 0.  全局 PRE 风格设定
# ============================================================
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Helvetica']
rcParams['mathtext.fontset'] = 'cm'           # LaTeX-like 数学字体
rcParams['axes.linewidth'] = 1.0
rcParams['xtick.major.width'] = 1.0
rcParams['ytick.major.width'] = 1.0
rcParams['xtick.labelsize'] = 9
rcParams['ytick.labelsize'] = 9
rcParams['axes.labelsize'] = 10
rcParams['axes.titlesize'] = 10
rcParams['legend.fontsize'] = 8
rcParams['legend.frameon'] = False
rcParams['savefig.dpi'] = 300
rcParams['savefig.bbox'] = 'tight'
rcParams['savefig.pad_inches'] = 0.05

# PRE 风配色 (深蓝主 + 暖橙对比)
C_BLUE_DARK  = '#1F3A93'   # 深蓝 (主)
C_BLUE       = '#3F5FB8'   # 中蓝
C_ORANGE     = '#D6602C'   # 暖橙
C_ORANGE_LT  = '#F4A582'   # 浅橙 (阴影)
C_GRAY       = '#4D4D4D'

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'inest_sdde_figs')
os.makedirs(OUTPUT_DIR, exist_ok=True)


def save_fig(fig, basename):
    """统一输出 PDF (矢量) + TIFF (位图)"""
    for ext in ('pdf', 'tiff'):
        path = os.path.join(OUTPUT_DIR, f'{basename}.{ext}')
        fig.savefig(path)
        print(f'[保存] {path}')


# ============================================================
# 图 1   Euler-Maruyama 半阶 vs Milstein 一阶收敛
# ============================================================
def figure1_convergence():
    fig, ax = plt.subplots(figsize=(3.5, 3.0))

    # 步长 h 与对应均方误差 (Buckwar 理论基准)
    h       = np.array([2**-4, 2**-6, 2**-8, 2**-10, 2**-12])
    err_em  = np.array([1.00e-1, 5.00e-2, 2.50e-2, 1.25e-2, 6.25e-3])
    err_mil = np.array([1.00e-1, 2.50e-2, 6.25e-3, 1.56e-3, 3.91e-4])

    lh    = np.log10(h)
    le_em = np.log10(err_em)
    le_ml = np.log10(err_mil)

    # 主曲线
    ax.plot(lh, le_em, 'o-', color=C_ORANGE, lw=1.8, ms=6,
            label=r'Euler--Maruyama ($p=1\!/\!2$)')
    ax.plot(lh, le_ml, 's-', color=C_BLUE_DARK, lw=1.8, ms=5,
            label=r'Milstein ($p=1$)')

    # 斜率参考虚线
    ref = np.array([lh.min(), lh.max()])
    ax.plot(ref, ref*0.5 + le_em[0],  '--', color=C_ORANGE,  lw=0.7, alpha=0.5)
    ax.plot(ref, ref*1.0 + le_ml[0],  '--', color=C_BLUE,    lw=0.7, alpha=0.5)

    # 斜率标注
    ax.annotate('slope = 0.5',
                xy=(lh[1], le_em[1]), xytext=(-2.35, -1.30),
                fontsize=8, color=C_ORANGE,
                arrowprops=dict(arrowstyle='->', color=C_ORANGE, lw=0.8))
    ax.annotate('slope = 1.0',
                xy=(lh[2], le_ml[2]), xytext=(-2.85, -2.55),
                fontsize=8, color=C_BLUE_DARK,
                arrowprops=dict(arrowstyle='->', color=C_BLUE_DARK, lw=0.8))

    ax.set_xlabel(r'$\log_{10}\,h$')
    ax.set_ylabel(r'$\log_{10}\,\mathrm{(MSE)}$')
    ax.legend(loc='lower right')
    ax.grid(True, ls=':', color=C_GRAY, alpha=0.4)

    save_fig(fig, 'fig1_em_milstein_convergence')
    plt.close(fig)


# ============================================================
# 图 2   加性 vs 乘性噪声 SDDE 轨迹对比
# ============================================================
def simulate_sdde(a, b, tau, g_func, X0=1.0, T=20.0, dt=0.005,
                  n_traj=15, seed=42):
    """
    线性 SDDE 的 Euler-Maruyama 离散:
        dX = (a X(t) + b X(t-tau)) dt + g(X(t)) dW(t)
    步内常数插值 + 共享随机增量以保证样本可比。
    """
    rng = np.random.default_rng(seed)
    n_steps, n_delay = int(T / dt), int(round(tau / dt))
    t_grid = np.linspace(0, T, n_steps + 1)

    # 共享的 Wiener 增量 (固定 seed 保证跨子图可比)
    dW_shared = rng.normal(0, np.sqrt(dt), (n_traj, n_steps))

    traj = np.zeros((n_traj, n_steps + 1))
    for k in range(n_traj):
        X = np.zeros(n_steps + 1)
        X[:n_delay + 1] = X0
        for i in range(n_delay, n_steps):
            X_t   = X[i]
            X_tau = X[i - n_delay]
            X[i+1] = X_t + (a*X_t + b*X_tau)*dt + g_func(X_t)*dW_shared[k, i]
        traj[k] = X
    return t_grid, traj, traj.mean(0), traj.std(0)


def figure2_noise_comparison():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0))
    a, b, tau = -1.0, 0.5, 1.0

    # ---- 左: 加性噪声 (外挂) ----
    t_g, tr_g, mu_g, sd_g = simulate_sdde(
        a, b, tau, lambda x: 0.30, n_traj=20, seed=7)
    ax = axes[0]
    for k in tr_g:
        ax.plot(t_g, k, color=C_BLUE_DARK, lw=0.4, alpha=0.30)
    ax.plot(t_g, mu_g, color=C_ORANGE, lw=1.9, label=r'mean $\pm$1 std')
    ax.fill_between(t_g, mu_g - sd_g, mu_g + sd_g,
                    color=C_ORANGE_LT, alpha=0.40)
    ax.set_xlabel(r'Time $t$')
    ax.set_ylabel(r'$X(t)$')
    ax.set_title(r'(a) Additive noise:  $g(X)=0.30$')
    ax.set_xlim(0, 20)
    ax.grid(True, ls=':', color=C_GRAY, alpha=0.4)
    ax.text(0.55, 0.92, r'$\mathrm{Var}(X)\simeq\mathrm{const}$',
            transform=ax.transAxes, fontsize=8, color=C_BLUE_DARK)

    # ---- 右: 乘性噪声 (状态耦合涨落) ----
    t_m, tr_m, mu_m, sd_m = simulate_sdde(
        a, b, tau, lambda x: 0.30*x, n_traj=20, seed=7)
    ax = axes[1]
    for k in tr_m:
        ax.plot(t_m, k, color=C_BLUE_DARK, lw=0.4, alpha=0.30)
    ax.plot(t_m, mu_m, color=C_ORANGE, lw=1.9, label=r'mean $\pm$1 std')
    ax.fill_between(t_m, mu_m - sd_m, mu_m + sd_m,
                    color=C_ORANGE_LT, alpha=0.40)
    ax.set_xlabel(r'Time $t$')
    ax.set_ylabel(r'$X(t)$')
    ax.set_title(r'(b) Multiplicative noise:  $g(X)=0.30\,X$')
    ax.set_xlim(0, 20)
    ax.grid(True, ls=':', color=C_GRAY, alpha=0.4)
    ax.text(0.55, 0.92, r'state-amplified bursts',
            transform=ax.transAxes, fontsize=8, color=C_ORANGE)

    fig.tight_layout()
    save_fig(fig, 'fig2_additive_vs_multiplicative_noise')
    plt.close(fig)


# ============================================================
# 图 3   涌现阈值 Θ 相图 + iNEST 六级智能热区
# ============================================================
def figure3_phase_diagram():
    fig, ax = plt.subplots(figsize=(4.0, 3.4))

    mu  = np.linspace(-2.0, 2.0, 501)
    lam = np.linspace( 0.0, 2.0, 501)
    MU, LAM = np.meshgrid(mu, lam)

    # 涌现指标 Θ ≡ 2 μ_max(A) + λ_g (耦合主导 + 噪声贡献)
    Theta = 2.0 * MU + LAM

    pcm = ax.pcolormesh(MU, LAM, Theta, cmap='RdYlBu_r',
                        shading='auto', vmin=-4, vmax=4)
    cs = ax.contour(MU, LAM, Theta,
                    levels=[-1.0, 0.0, 1.5, 3.0],
                    colors='black', linewidths=0.9,
                    linestyles=['--', '-', '-.', '-'])
    ax.clabel(cs, inline=1, fontsize=7, fmt=r'$\Theta=%.1f$')

    # iNEST 六级智能标签 (热区) — CJK font for Chinese labels
    cjk_font = fm.FontProperties(family='Microsoft YaHei', size=9)
    box_white = dict(facecolor='white',  edgecolor='none', pad=2, alpha=0.75)
    box_dark  = dict(facecolor='black',  edgecolor='none', pad=2, alpha=0.55)
    ax.text(-1.55, 1.45, 'L1 感知',   ha='center',
            color='black', bbox=box_white, fontproperties=cjk_font)
    ax.text(-0.65, 1.45, 'L2 反应',   ha='center',
            color='black', bbox=box_white, fontproperties=cjk_font)
    ax.text( 0.40, 1.45, 'L3 适应',   ha='center',
            color='black', bbox=box_white, fontproperties=cjk_font)
    ax.text( 1.20, 1.45, 'L4 创造',   ha='center',
            color='black', bbox=box_white, fontproperties=cjk_font)
    ax.text( 1.75, 1.45, 'L5–L6',     ha='center',
            color='white', bbox=box_dark, fontproperties=cjk_font)

    ax.set_xlabel(r'coupling spectral radius $\mu_{\max}(A)$')
    ax.set_ylabel(r'noise strength $\lambda_{g}$')
    ax.set_xlim(-2, 2); ax.set_ylim(0, 2)

    cbar = fig.colorbar(pcm, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label(r'emergence index $\Theta = 2\mu_{\max}(A)+\lambda_{g}$')

    save_fig(fig, 'fig3_emergence_threshold_phase')
    plt.close(fig)


# ============================================================
# 主流程
# ============================================================
if __name__ == '__main__':
    print('===== iNEST × SDDE 三图生成开始 =====')
    print('[1/3] 图 1  EM/Milstein 收敛阶对比 ...')
    figure1_convergence()
    print('[2/3] 图 2  加性 vs 乘性噪声 SDDE 轨迹 ...')
    figure2_noise_comparison()
    print('[3/3] 图 3  涌现阈值 Θ 相图 ...')
    figure3_phase_diagram()
    print(f'===== 全部完成  →  {os.path.abspath(OUTPUT_DIR)} =====')
