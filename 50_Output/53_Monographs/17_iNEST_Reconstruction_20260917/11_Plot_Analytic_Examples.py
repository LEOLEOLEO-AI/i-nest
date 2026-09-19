"""Plot exact derived curves; no experimental data are represented."""

from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


OUTPUT = Path("D:/Obsidian/Output/17_iNEST_Reconstruction_20260917")
OUTPUT.mkdir(parents=True, exist_ok=True)
plt.rcParams.update({"font.size": 11, "axes.spines.top": False,
                     "axes.spines.right": False, "savefig.dpi": 200})
fig, axes = plt.subplots(2, 1, figsize=(7.2, 7.4), constrained_layout=True)
a = np.linspace(0, 0.9999, 1200)
for delay, color in zip((0, 1, 4, 16), ("#087F8C", "#B23A48", "#496D2E", "#6A4C93")):
    capacity = (1 - a * a) * a ** (2 * delay)
    axes[0].plot(a, capacity, label=f"delay k = {delay}", color=color, linewidth=2)
    optimum = np.sqrt(delay / (delay + 1))
    axes[0].scatter([optimum], [(1 - optimum**2) * optimum ** (2 * delay)], color=color, s=30)
axes[0].set(title="A. The best memory scale depends on the task",
            xlabel="Stable recurrence parameter a", ylabel="Linear capacity C_k", xlim=(0, 1))
axes[0].legend(frameon=False, loc="upper right")
axes[0].grid(alpha=0.2)
omega = np.linspace(0, 3, 200)
axes[1].plot(omega, omega * omega, color="#B23A48", linewidth=2,
             label="Entropy production rate / k_B")
axes[1].plot(omega, np.full_like(omega, -2), color="#087F8C", linewidth=2,
             label="Both Lyapunov exponents")
axes[1].set(title="B. The same full spectrum can have different dissipation",
            xlabel="Nonconservative rotation strength omega", ylabel="Rate (normalized time)")
axes[1].legend(frameon=False, loc="upper left")
axes[1].grid(alpha=0.2)
fig.suptitle("Analytic counterexamples | Derived, not measured", fontsize=13)
fig.savefig(OUTPUT / "02_Analytic_Counterexamples.png", facecolor="white")
plt.close(fig)
print(OUTPUT / "02_Analytic_Counterexamples.png")
