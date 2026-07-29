# -*- coding: utf-8 -*-
"""
Generate EX2_curves.pdf for the iNEST-SDDE paper.

Two-node tanh network (Eq. 7 in the paper):
  dX1 = [-alpha*X1 + kappa*tanh(X2(t-tau))] dt + sigma*X1 dW1
  dX2 = [-alpha*X2 + kappa*tanh(X1(t-tau))] dt + sigma*X2 dW2

Parameters: alpha=1.0, sigma=0.4, tau=1.0, h=1e-3, M=10^4 paths
  (甲) Sub-threshold: kappa=0.3, Theta*=-1.24  -> exponential decay
  (丙) Super-threshold: kappa=1.3, Theta*=+0.76 -> growth then saturation

Initial history: phi = 0.3  (E|X(0)|^2 = 0.18, below saturation level)
Integer alignment: tau/h = 1000 in Z, zero interpolation error.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from scipy.optimize import brentq
import os

# CJK font for panel labels (甲)(丙)
cjk = FontProperties(fname='C:/Windows/Fonts/msyh.ttc', size=11)

# ========== Model parameters ==========
alpha = 1.0
sigma = 0.4
tau   = 1.0
h     = 1e-3
T     = 15.0
M     = 10000                       # Monte Carlo paths
phi   = 0.3                         # constant initial history

n_steps  = int(round(T / h))       # 15000
n_delay  = int(round(tau / h))     # 1000
buf_size = n_delay + 1             # 1001

# ========== Simulation (vectorised over M paths) ==========
def simulate(kappa, M, seed=42):
    rng  = np.random.default_rng(seed)
    # Circular buffers for delayed state; initial history = phi
    buf1 = np.full((buf_size, M), phi)
    buf2 = np.full((buf_size, M), phi)
    pos  = 0                         # buf[pos] = X(t)

    store_every = 100                # store every 0.1 time units
    n_store     = n_steps // store_every
    times       = np.zeros(n_store + 1)
    energy      = np.zeros(n_store + 1)
    energy[0]   = np.mean(buf1[pos]**2 + buf2[pos]**2)   # = 2*phi^2 = 0.18
    si          = 0
    sqrt_h      = np.sqrt(h)

    for k in range(n_steps):
        pd   = (pos - n_delay) % buf_size
        X1   = buf1[pos]
        X2   = buf2[pos]
        X1d  = buf1[pd]              # X1(t - tau)
        X2d  = buf2[pd]              # X2(t - tau)

        dW1  = rng.standard_normal(M) * sqrt_h
        dW2  = rng.standard_normal(M) * sqrt_h

        # Euler-Maruyama step
        X1n  = X1 + (-alpha * X1 + kappa * np.tanh(X2d)) * h + sigma * X1 * dW1
        X2n  = X2 + (-alpha * X2 + kappa * np.tanh(X1d)) * h + sigma * X2 * dW2

        pos       = (pos + 1) % buf_size
        buf1[pos] = X1n
        buf2[pos] = X2n

        if (k + 1) % store_every == 0:
            si += 1
            times[si]  = (k + 1) * h
            energy[si] = np.mean(X1n**2 + X2n**2)

    return times, energy

# ========== Theoretical rates ==========
# Sub-threshold: a1 = -2*alpha + sigma^2 + kappa, a2 = kappa
k_sub  = 0.3
a1_sub = -2 * alpha + sigma**2 + k_sub          # -1.54
a2_sub = k_sub                                   # 0.30
Theta_sub = a1_sub + a2_sub                      # -1.24

# Optimal lambda:  lambda + a1 + a2 * exp(lambda * tau) = 0
lam_star = brentq(
    lambda l: l + a1_sub + a2_sub * np.exp(l * tau),
    1e-12, -Theta_sub - 1e-12
)

# Super-threshold
k_sup  = 1.3
a1_sup = -2 * alpha + sigma**2 + k_sup           # -0.54
a2_sup = k_sup                                   # 1.30
Theta_sup = a1_sup + a2_sup                      # +0.76

# Characteristic exponent:  z - a1 - a2 * exp(-z * tau) = 0
z_star = brentq(
    lambda z: z - a1_sup - a2_sup * np.exp(-z * tau),
    1e-12, 20.0
)

print(f"Sub-threshold:  a1={a1_sub:.2f}, a2={a2_sub:.2f}, "
      f"Theta*={Theta_sub:.2f}, lambda*={lam_star:.4f}")
print(f"Super-threshold: a1={a1_sup:.2f}, a2={a2_sup:.2f}, "
      f"Theta*={Theta_sup:.2f}, z*={z_star:.4f}")

# ========== Run simulations ==========
print(f"\nSimulating sub-threshold  (kappa={k_sub})  M={M} paths  T={T} ...")
t1, E1 = simulate(k_sub, M, seed=42)
print(f"  Final E|X|^2 = {E1[-1]:.4e}")

print(f"\nSimulating super-threshold (kappa={k_sup})  M={M} paths  T={T} ...")
t2, E2 = simulate(k_sup, M, seed=43)
print(f"  Final E|X|^2 = {E2[-1]:.4f}")

# ========== Fit empirical rates ==========
# Sub-threshold: fit asymptotic decay rate (after delay activates, before noise floor)
mask = (t1 > 3.0) & (t1 < 12.0) & (E1 > 1e-10)
p_fit = np.polyfit(t1[mask], np.log(E1[mask]), 1)
lam_hat = -p_fit[0]
print(f"\nEmpirical decay rate:  lambda_hat = {lam_hat:.4f}  "
      f"(theory {lam_star:.4f})")

# Super-threshold: fit initial growth rate
mask_g = (t2 > 1.0) & (t2 < 4.0) & (E2 > 0)
p_grow = np.polyfit(t2[mask_g], np.log(E2[mask_g]), 1)
z_hat  = p_grow[0]
print(f"Empirical growth rate: z_hat      = {z_hat:.4f}  "
      f"(theory {z_star:.4f})")

# Saturation level
E_sat = np.mean(E2[t2 > 10])
print(f"Saturation level:      E_sat      = {E_sat:.4f}")

# ========== Plot ==========
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "cm",
    "axes.linewidth": 0.8,
    "font.size": 10,
})

NAVY  = "#1f4e79"
RED   = "#c0504d"
GREEN = "#2e7d32"
GREY  = "#999999"

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 3.2))

# ---- Panel (甲): sub-threshold — semilogy ----
ax1.semilogy(t1, E1, '-', color=NAVY, lw=1.3,
             label=r'MC  $\mathbb{E}|\mathbf{X}(t)|^2$')
# Theoretical decay
E0 = E1[0]
ax1.semilogy(t1, E0 * np.exp(-lam_star * t1), '--', color=RED, lw=1.0,
             label=rf'theory  $e^{{-{lam_star:.2f}\,t}}$')
# Fitted decay
ax1.semilogy(t1, np.exp(p_fit[1]) * np.exp(-lam_hat * t1), ':', color=GREEN, lw=1.0,
             label=rf'fit  $e^{{-{lam_hat:.2f}\,t}}$')

ax1.set_xlabel(r'$t$', fontsize=11)
ax1.set_ylabel(r'$\mathbb{E}|\mathbf{X}(t)|^2$', fontsize=11)
ax1.text(0.03, 0.95, '(甲)', transform=ax1.transAxes, fontsize=12,
         fontproperties=cjk, va='top', ha='left')
ax1.set_title(r'$\kappa=0.3,\;\Theta^{\ast}=-1.24$', fontsize=9, pad=4)
ax1.legend(fontsize=7.5, frameon=False, loc='upper right')
ax1.grid(True, which="both", ls=":", alpha=0.3)
ax1.set_xlim(0, T)
ax1.set_ylim(bottom=1e-7, top=1)

# ---- Panel (丙): super-threshold — linear ----
ax2.plot(t2, E2, '-', color=RED, lw=1.3,
         label=r'MC  $\mathbb{E}|\mathbf{X}(t)|^2$')
# Initial exponential growth reference (linear scale, limited to growth phase)
t_grow = t2[(t2 >= 0.5) & (t2 < 6)]
ax2.plot(t_grow, np.exp(p_grow[1]) * np.exp(z_hat * t_grow),
         ':', color=GREY, lw=0.8,
         label=rf'$e^{{{z_hat:.2f}\,t}}$  (initial growth)')
# Saturation level
ax2.axhline(E_sat, color=GREY, ls='--', lw=0.6, alpha=0.5)
ax2.text(T * 0.98, E_sat * 1.08, f'saturation $\\approx${E_sat:.2f}',
         fontsize=7.5, color=GREY, ha='right', va='bottom')

ax2.set_xlabel(r'$t$', fontsize=11)
ax2.set_ylabel(r'$\mathbb{E}|\mathbf{X}(t)|^2$', fontsize=11)
ax2.text(0.03, 0.95, '(丙)', transform=ax2.transAxes, fontsize=12,
         fontproperties=cjk, va='top', ha='left')
ax2.set_title(r'$\kappa=1.3,\;\Theta^{\ast}=+0.76$', fontsize=9, pad=4)
ax2.legend(fontsize=7.5, frameon=False, loc='center right')
ax2.grid(True, which="both", ls=":", alpha=0.3)
ax2.set_xlim(0, T)
ax2.set_ylim(0, max(E2) * 1.15)

fig.tight_layout(pad=0.5)

out_dir = os.path.dirname(os.path.abspath(__file__))
fig.savefig(os.path.join(out_dir, "EX2_curves.pdf"), bbox_inches="tight")
fig.savefig(os.path.join(out_dir, "EX2_curves.png"), dpi=300, bbox_inches="tight")
print(f"\nSaved: {out_dir}/EX2_curves.pdf  and  .png")
