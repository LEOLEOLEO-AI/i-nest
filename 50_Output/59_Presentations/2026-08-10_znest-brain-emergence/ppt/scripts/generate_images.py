"""Generate thematic raster assets for the iNEST academic deck."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyArrowPatch, Rectangle, Wedge, RegularPolygon, Polygon

OUT = os.path.join(os.path.dirname(__file__), "..", "images")
os.makedirs(OUT, exist_ok=True)

INK = "#0A0A0A"
BLUE = "#002FA7"
BRIGHT = "#5B7BFF"
PALE = "#E8EDF7"
GREY = "#8A8F98"
WHITE = "#FFFFFF"
DARK = "#0B1224"
DARK_EDGE = "#24344F"


def base(dark=False, figsize=(16, 9)):
    fig = plt.figure(figsize=figsize, dpi=100)
    fig.patch.set_facecolor(DARK if dark else WHITE)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_facecolor(DARK if dark else WHITE)
    ax.axis("off")
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    return fig, ax


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=100, facecolor=fig.get_facecolor(), bbox_inches=None)
    plt.close(fig)
    print("wrote", path)


def rect(ax, x, y, w, h, fc=PALE, ec=INK, lw=1.4, alpha=1.0, zorder=2):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw, alpha=alpha, zorder=zorder))


def line(ax, pts, color=INK, lw=1.4, ls="-", zorder=2, alpha=1.0):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color, lw=lw, linestyle=ls, zorder=zorder, alpha=alpha)


def dots(ax, xs, ys, color=BLUE, size=14, zorder=3):
    ax.scatter(xs, ys, s=size, color=color, zorder=zorder, edgecolors="none")


def arrow(ax, x1, y1, x2, y2, color=INK, lw=1.6, style="-|>", zorder=3):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=14,
                                 color=color, lw=lw, zorder=zorder))


# 1. Cover: luminous network on a wafer
def cover_network_glow():
    fig, ax = base(dark=True)
    # wafer disc
    ax.add_patch(Circle((8, 4.6), 3.35, facecolor="#0E1830", edgecolor="#2D4A82", lw=2))
    ax.add_patch(Circle((8, 4.6), 2.75, facecolor="#0B1224", edgecolor="#1D2F52", lw=1.2))
    rng = np.random.default_rng(7)
    nodes = []
    for _ in range(46):
        a = rng.uniform(0, 2 * np.pi)
        r = rng.uniform(0.35, 2.7)
        nodes.append((8 + r * np.cos(a), 4.6 + r * np.sin(a)))
    pts = np.array(nodes)
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            d = np.hypot(*(pts[i] - pts[j]))
            if d < 0.75:
                ax.plot([pts[i][0], pts[j][0]], [pts[i][1], pts[j][1]],
                        color=BRIGHT, lw=0.5, alpha=0.28, zorder=2)
    ax.scatter(pts[:, 0], pts[:, 1], s=26, c="#9DB8FF", zorder=3)
    # central critical point
    ax.add_patch(Circle((8, 4.6), 0.34, facecolor=BRIGHT, edgecolor=WHITE, lw=1.4, zorder=4))
    ax.add_patch(Circle((8, 4.6), 0.62, facecolor="none", edgecolor=BRIGHT, lw=1.2, alpha=0.65, zorder=3))
    ax.add_patch(Circle((8, 4.6), 1.0, facecolor="none", edgecolor=BRIGHT, lw=0.8, alpha=0.3, zorder=3))
    # faint grid
    for x in np.linspace(0.4, 15.6, 12):
        ax.plot([x, x], [0.2, 8.8], color="#20304F", lw=0.4, alpha=0.4)
    for y in np.linspace(0.4, 8.6, 8):
        ax.plot([0.2, 15.8], [y, y], color="#20304F", lw=0.4, alpha=0.4)
    save(fig, "cover_network_glow.png")


# 2. Energy gap: log bars 20 W vs 20 MW
def energy_gap():
    fig, ax = base()
    ax.text(0.6, 8.5, "ENERGY GAP  ~10^6", fontsize=22, color=BLUE, fontweight="bold")
    bars = [("Human brain", 20, "W"), ("Frontier cluster", 20e6, "W")]
    xs = [3.2, 9.2]
    for (label, val, unit), x in zip(bars, xs):
        rect(ax, x, 1.4, 2.4, 5.2, fc=PALE, ec=BLUE, lw=1.6)
        ax.text(x + 1.2, 6.9, f"{val:.0e}", ha="center", fontsize=26, color=INK, fontweight="bold")
        ax.text(x + 1.2, 6.2, unit, ha="center", fontsize=16, color=GREY)
        ax.text(x + 1.2, 0.75, label, ha="center", fontsize=18, color=INK, fontweight="bold")
    ax.annotate("", xy=(7.5, 5.0), xytext=(6.2, 5.0),
                arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=2))
    ax.text(6.85, 5.25, "10^6", fontsize=18, color=BLUE, fontweight="bold", ha="center")
    save(fig, "energy_gap.png")


# 3. Four walls closing in
def four_walls():
    fig, ax = base()
    rect(ax, 2.2, 2.0, 11.6, 6.2, fc=WHITE, ec=GREY, lw=1.2)
    walls = [("POWER", 2.4, 5.4), ("MEMORY", 12.1, 5.4), ("INTERCONNECT", 2.4, 2.6), ("DATA", 12.1, 2.6)]
    for label, x, y in walls:
        rect(ax, x, y, 3.4, 1.1, fc=PALE, ec=BLUE, lw=1.5)
        ax.text(x + 1.7, y + 0.55, label, ha="center", va="center", fontsize=16, color=BLUE, fontweight="bold")
    arrow(ax, 8, 4.4, 8, 5.5, color=INK, lw=2.2)
    ax.text(8.4, 4.6, "no way out", fontsize=16, color=INK, fontweight="bold")
    save(fig, "four_walls.png")


# 4. Scaling returns collapse
def scaling_collapse():
    fig, ax = base()
    x = np.linspace(0, 10, 200)
    y_old = np.minimum(x * 1.05, 8.1)
    y_new = 2.1 + 2.8 * np.log1p(x) / np.log1p(10)
    ax.plot(x, y_old, color=GREY, lw=2.2, ls="--")
    ax.plot(x, y_new, color=BLUE, lw=3)
    ax.text(5.5, 7.0, "linear expectation", fontsize=15, color=GREY, fontweight="bold")
    ax.text(5.6, 4.5, "measured capability", fontsize=15, color=BLUE, fontweight="bold")
    ax.text(0.5, 0.6, "10x parameters  ->  <20% capability", fontsize=16, color=INK, fontweight="bold")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 9)
    save(fig, "scaling_collapse.png")


# 5. Neuron vs synapse counts
def neuron_vs_synapse():
    fig, ax = base()
    rect(ax, 3.4, 1.8, 2.6, 3.1, fc=PALE, ec=BLUE, lw=1.6)
    rect(ax, 9.6, 1.8, 2.6, 6.3, fc=BLUE, ec=BLUE, lw=1.6)
    ax.text(4.7, 5.2, "86B", ha="center", fontsize=24, color=INK, fontweight="bold")
    ax.text(4.7, 4.3, "neurons", ha="center", fontsize=15, color=GREY)
    ax.text(10.9, 8.4, "10^14", ha="center", fontsize=24, color=WHITE, fontweight="bold")
    ax.text(10.9, 7.5, "synapses", ha="center", fontsize=15, color="#CFDCFF")
    ax.text(0.6, 8.4, "WIN BY CONNECTION", fontsize=20, color=BLUE, fontweight="bold")
    save(fig, "neuron_vs_synapse.png")


# 6. Water three phases
def water_phases():
    fig, ax = base()
    rect(ax, 0.7, 1.1, 4.6, 7.0, fc=WHITE, ec=GREY, lw=1.2)
    rect(ax, 5.7, 1.1, 4.6, 7.0, fc=WHITE, ec=GREY, lw=1.2)
    rect(ax, 10.7, 1.1, 4.6, 7.0, fc=WHITE, ec=GREY, lw=1.2)
    for x, label in [(3.0, "ICE"), (8.0, "WATER"), (13.0, "VAPOR")]:
        ax.text(x, 7.8, label, ha="center", fontsize=18, color=BLUE, fontweight="bold")
    # ice lattice
    ice = [(2.2, 3.2), (3.8, 3.2), (3.0, 4.5), (4.6, 4.5), (2.6, 5.8), (4.2, 5.8)]
    for i, p in enumerate(ice):
        ax.add_patch(Circle(p, 0.16, facecolor=BRIGHT, edgecolor=BLUE, zorder=3))
        for q in ice[i + 1:]:
            if np.hypot(p[0] - q[0], p[1] - q[1]) < 1.8:
                line(ax, [p, q], color=BLUE, lw=1.0)
    # water
    rng = np.random.default_rng(2)
    wpts = [(7.2, 2.6), (8.7, 2.8), (8.0, 4.2), (7.0, 5.3), (8.8, 5.1), (7.6, 6.6)]
    for i, p in enumerate(wpts):
        ax.add_patch(Circle(p, 0.16, facecolor=BRIGHT, edgecolor=BLUE, zorder=3))
        for q in wpts[i + 1:]:
            d = np.hypot(p[0] - q[0], p[1] - q[1])
            if 0.8 < d < 2.2:
                line(ax, [p, q], color=BLUE, lw=0.7, alpha=0.65)
    # vapor
    vpts = [(11.5, 2.2), (13.6, 3.0), (12.2, 4.0), (14.0, 4.8), (12.6, 6.0), (14.4, 6.7)]
    for p in vpts:
        ax.add_patch(Circle(p, 0.14, facecolor=BRIGHT, edgecolor=BLUE, lw=1.0, zorder=3))
    for p, q in [(vpts[0], vpts[4]), (vpts[1], vpts[2]), (vpts[3], vpts[5])]:
        line(ax, [p, q], color=BLUE, lw=0.5, alpha=0.3)
    save(fig, "water_phases.png")


# 7. Diamond vs graphite
def crystal_lattices():
    fig, ax = base()
    ax.text(0.7, 8.3, "sp3  DIAMOND   hardness 10", fontsize=18, color=BLUE, fontweight="bold")
    ax.text(8.7, 8.3, "sp2  GRAPHITE   hardness 1-2", fontsize=18, color=GREY, fontweight="bold")
    # diamond tetrahedron grid
    rng = np.random.default_rng(1)
    for ix in range(3):
        for iy in range(3):
            x0, y0 = 1.5 + ix * 1.7, 1.6 + iy * 1.7
            ax.add_patch(RegularPolygon((x0, y0), 3, radius=0.32, orientation=np.pi, facecolor=PALE, edgecolor=BLUE, lw=1.2, zorder=2))
            ax.add_patch(RegularPolygon((x0 + 0.85, y0 + 0.5), 3, radius=0.32, orientation=0, facecolor=PALE, edgecolor=BLUE, lw=1.2, zorder=2))
            line(ax, [(x0, y0), (x0 + 0.85, y0 + 0.5)], color=INK, lw=0.8)
    # graphite layers
    for layer in range(3):
        y = 1.7 + layer * 2.0
        for ix in range(4):
            x = 9.2 + ix * 1.35 + (0.67 if layer % 2 else 0)
            ax.add_patch(Rectangle((x, y), 0.85, 0.55, facecolor=GREY, ec=INK, lw=1.0, alpha=0.8))
    save(fig, "crystal_lattices.png")


# 8. Insulin disulfide correctness
def insulin_disulfide():
    fig, ax = base()
    ax.text(0.7, 8.4, "SEQUENCE IS NOT ENOUGH", fontsize=20, color=BLUE, fontweight="bold")
    chainA = [(1.6, 5.0), (3.0, 5.4), (4.4, 4.9), (5.8, 5.3), (7.2, 4.8), (8.6, 5.2)]
    chainB = [(1.6, 2.6), (3.2, 2.9), (4.8, 2.5), (6.4, 2.9), (8.0, 2.5), (9.6, 2.9)]
    for pts, label in [(chainA, "CHAIN A"), (chainB, "CHAIN B")]:
        xs, ys = zip(*pts)
        ax.plot(xs, ys, color=INK, lw=2.4, zorder=2)
        ax.text(pts[0][0], pts[0][1] + 0.45, label, fontsize=13, color=GREY, fontweight="bold")
    # correct disulfide
    for (a, b) in [((3.0, 5.4), (3.2, 2.9)), ((5.8, 5.3), (6.4, 2.9)), ((8.6, 5.2), (8.0, 2.5))]:
        line(ax, [a, b], color=BLUE, lw=3.0)
        ax.plot([a[0], b[0]], [a[1], b[1]], color=BLUE, lw=1.0, ls="--", alpha=0.4)
    ax.text(10.8, 5.3, "correct\nS-S bonds\n=> activity", fontsize=16, color=BLUE, fontweight="bold")
    ax.text(10.8, 2.2, "wrong S-S\n=> activity 0", fontsize=16, color=GREY, fontweight="bold")
    save(fig, "insulin_disulfide.png")


# 9. Connectome: 302 neurons, 7000 links
def connectome_302():
    fig, ax = base()
    rng = np.random.default_rng(11)
    pts = np.array([(8 + 6.8 * np.cos(t), 4.5 + 4.0 * np.sin(t)) for t in np.linspace(0, 2 * np.pi, 42, endpoint=False)])
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            d = np.hypot(*(pts[i] - pts[j]))
            if d < 2.4:
                ax.plot([pts[i][0], pts[j][0]], [pts[i][1], pts[j][1]], color=BLUE, lw=0.35, alpha=0.45, zorder=1)
    ax.scatter(pts[:, 0], pts[:, 1], s=16, color=BLUE, zorder=3)
    ax.text(1.0, 8.3, "C. elegans  302 neurons", fontsize=18, color=BLUE, fontweight="bold")
    ax.text(1.0, 7.7, "~7,000 connections", fontsize=16, color=GREY, fontweight="bold")
    save(fig, "connectome_302.png")


# 10. Same components, different topology
def topology_function():
    fig, ax = base()
    rect(ax, 1.0, 2.8, 4.0, 3.4, fc=WHITE, ec=GREY, lw=1.2)
    rect(ax, 6.1, 2.8, 4.0, 3.4, fc=PALE, ec=BLUE, lw=1.5)
    rect(ax, 11.2, 2.8, 3.8, 3.4, fc=WHITE, ec=GREY, lw=1.2)
    for x0, label in [(3.0, "SAME ATOMS"), (8.1, "NEW CONNECTIONS"), (13.1, "NEW FUNCTION")]:
        ax.text(x0, 2.2, label, ha="center", fontsize=14, color=INK, fontweight="bold")
    for x0 in [2.2, 3.0, 3.8, 7.2, 8.1, 9.0, 12.3, 13.1, 13.9]:
        ax.add_patch(Circle((x0, 5.0), 0.22, facecolor=BRIGHT, edgecolor=BLUE, zorder=3))
    for (x1, y1), (x2, y2) in [((2.2, 5.0), (3.0, 5.0)), ((3.0, 5.0), (3.8, 5.0)), ((7.2, 5.0), (9.0, 5.0)),
                                ((8.1, 5.0), (7.2, 5.0)), ((8.1, 5.0), (9.0, 5.0)), ((12.3, 5.0), (13.9, 5.0)),
                                ((13.1, 5.0), (12.3, 5.0)), ((13.1, 5.0), (13.9, 5.0))]:
        line(ax, [(x1, y1), (x2, y2)], color=INK, lw=1.2)
    arrow(ax, 5.4, 4.5, 5.9, 4.5, color=BLUE, lw=2.0)
    arrow(ax, 10.5, 4.5, 11.0, 4.5, color=GREY, lw=2.0)
    save(fig, "topology_function.png")


# 11. Linear vs nonlinear
def linear_vs_nonlinear():
    fig, ax = base()
    x = np.linspace(0, 9, 200)
    y_lin = 0.8 + 0.8 * x
    y_nl = 0.8 + 0.18 * np.exp(0.45 * x)
    ax.plot(x, y_lin, color=GREY, lw=2.4, ls="--", label="linear stack")
    ax.plot(x, y_nl, color=BLUE, lw=3.2, label="cascade gain")
    ax.text(2.5, 3.6, "linear: same function class", fontsize=15, color=GREY, fontweight="bold")
    ax.text(5.8, 6.8, "nonlinear: new classes", fontsize=15, color=BLUE, fontweight="bold")
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)
    save(fig, "linear_vs_nonlinear.png")


# 12. Cascade function-class expansion
def cascade_gain():
    fig, ax = base()
    rings = [3.2, 4.5, 5.9]
    cx, cy = 8.0, 4.5
    for i, r in enumerate(rings):
        ax.add_patch(Circle((cx, cy), r, facecolor="none", edgecolor=BLUE, lw=2.0, alpha=0.35 + i * 0.2, zorder=2))
    for i, r in enumerate(rings):
        ax.text(cx + r + 0.25, cy, f"L{i+1}", fontsize=15, color=BLUE, fontweight="bold", va="center")
    ax.text(1.0, 8.2, "FUNCTION CLASS EXPANSION", fontsize=18, color=INK, fontweight="bold")
    ax.text(1.0, 7.5, "each cascade layer adds classes absent above", fontsize=15, color=GREY, fontweight="bold")
    save(fig, "cascade_gain.png")


# 13. Physics emergence: phase transition / laser threshold
def emergence_physics():
    fig, ax = base()
    x = np.linspace(0, 10, 300)
    y = np.piecewise(x, [x < 6, x >= 6], [lambda v: 1.2 + 0.12 * v, lambda v: 1.2 + 0.12 * v + 2.8 * (v - 6) ** 2 / 16])
    ax.plot(x, y, color=BLUE, lw=3.0)
    ax.axvline(6, color=GREY, lw=1.5, ls="--")
    ax.text(6.25, 5.6, "threshold", fontsize=15, color=GREY, fontweight="bold")
    ax.text(1.0, 7.6, "PHASE TRANSITION / LASER", fontsize=18, color=BLUE, fontweight="bold")
    ax.text(1.0, 6.9, "multiplicative response above threshold", fontsize=15, color=INK, fontweight="bold")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8.5)
    save(fig, "emergence_physics.png")


# 14. Six-level intelligence staircase
def intelligence_scale():
    fig, ax = base()
    levels = ["VI  SUPER", "V  GENERAL", "IV  CREATE", "III  ADAPT", "II  REACT", "I  SENSE"]
    y = np.arange(6)
    heights = np.arange(1.2, 7.4, 1.2)
    for i, (lvl, h) in enumerate(zip(levels, heights)):
        x = 1.0 + (h - 1.2) * 0.55
        rect(ax, x, i * 1.15 + 0.35, h, 0.85, fc=PALE if i % 2 else BLUE, ec=BLUE, lw=1.4)
        ax.text(x + 0.15, i * 1.15 + 0.78, lvl, fontsize=14, color=WHITE if i % 2 == 0 else INK, fontweight="bold", va="center")
    save(fig, "intelligence_scale.png")


# 15. SDDE: a string with echo
def sdde_echo():
    fig, ax = base()
    t = np.linspace(0, 10, 500)
    y1 = 4.5 + 1.4 * np.sin(1.8 * t) * np.exp(-0.12 * t)
    y2 = 4.5 + 1.0 * np.sin(1.8 * (t - 1.2)) * np.exp(-0.22 * t)
    ax.plot(t, y1, color=INK, lw=2.6)
    ax.plot(t, y2, color=BLUE, lw=2.2, ls="--")
    ax.text(1.0, 8.2, "A STRING WITH ECHO", fontsize=18, color=BLUE, fontweight="bold")
    ax.text(1.0, 7.5, "delay remembers, noise searches, nonlinearity multiplies", fontsize=15, color=INK, fontweight="bold")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 9)
    save(fig, "sdde_echo.png")


# 16. Four local rules loop
def local_rules_loop():
    fig, ax = base()
    labels = ["STDP", "PREDICTION ERROR", "HOMEOSTASIS", "CRITICAL BRANCHING"]
    for i, label in enumerate(labels):
        a = np.pi / 2 + i * np.pi / 2
        cx, cy = 8 + 4.6 * np.cos(a), 4.5 + 4.6 * np.sin(a)
        rect(ax, cx - 1.6, cy - 0.65, 3.2, 1.3, fc=PALE, ec=BLUE, lw=1.5)
        ax.text(cx, cy, label, ha="center", va="center", fontsize=14, color=BLUE, fontweight="bold")
    for i in range(4):
        a1 = np.pi / 2 + i * np.pi / 2
        a2 = np.pi / 2 + (i + 1) * np.pi / 2
        x1, y1 = 8 + 2.9 * np.cos(a1), 4.5 + 2.9 * np.sin(a1)
        x2, y2 = 8 + 2.9 * np.cos(a2), 4.5 + 2.9 * np.sin(a2)
        ax.plot([x1, x2], [y1, y2], color=INK, lw=1.4)
        ax.plot((x1 + x2) / 2, (y1 + y2) / 2, marker=">", color=INK, ms=9)
    ax.add_patch(Circle((8, 4.5), 0.5, facecolor=BLUE, edgecolor=WHITE, lw=1.5, zorder=3))
    ax.text(8, 4.5, "4", ha="center", va="center", fontsize=16, color=WHITE, fontweight="bold", zorder=4)
    save(fig, "local_rules_loop.png")


# 17. Criticality power law
def criticality_powerlaw():
    fig, ax = base()
    x = np.logspace(0, 2.5, 200)
    y = 120 * np.power(x, -1.5)
    ax.loglog(x, y, color=BLUE, lw=3.0)
    ax.text(1.2, 70, "avalanche size distribution", fontsize=15, color=INK, fontweight="bold")
    ax.text(20, 9, "power law  tau ~ 1.5", fontsize=15, color=BLUE, fontweight="bold")
    ax.set_xlim(1, 300)
    ax.set_ylim(0.05, 200)
    save(fig, "criticality_powerlaw.png")


# 18. SDI control loop
def sdi_control():
    fig, ax = base()
    rect(ax, 1.4, 3.4, 4.4, 2.4, fc=PALE, ec=BLUE, lw=1.5)
    rect(ax, 10.4, 3.4, 4.4, 2.4, fc=BLUE, ec=BLUE, lw=1.5)
    ax.text(3.6, 4.6, "LOCAL RULES\nbottom-up growth", ha="center", va="center", fontsize=14, color=BLUE, fontweight="bold")
    ax.text(12.6, 4.6, "SDI CONTROL\ntopology budget", ha="center", va="center", fontsize=14, color=WHITE, fontweight="bold")
    arrow(ax, 5.9, 4.6, 10.3, 4.6, color=INK, lw=2.2)
    arrow(ax, 10.3, 3.6, 5.9, 3.6, color=GREY, lw=1.8, style="-|>")
    ax.text(8.1, 5.0, "boundary / budget", fontsize=13, color=INK, fontweight="bold")
    ax.text(8.1, 2.8, "measured state", fontsize=13, color=GREY, fontweight="bold")
    save(fig, "sdi_control.png")


# 19. TCC topology-centric
def tcc_topology():
    fig, ax = base()
    ax.add_patch(Circle((8, 4.5), 3.4, facecolor=PALE, edgecolor=BLUE, lw=2.0))
    ax.add_patch(Circle((8, 4.5), 1.5, facecolor=BLUE, edgecolor=BLUE, lw=2.0))
    ax.text(8, 4.5, "TOPOLOGY\nIS COMPUTE", ha="center", va="center", fontsize=16, color=WHITE, fontweight="bold", zorder=3)
    rng = np.random.default_rng(4)
    for i in range(12):
        a = i * 2 * np.pi / 12
        x = 8 + 2.6 * np.cos(a)
        y = 4.5 + 2.6 * np.sin(a)
        ax.add_patch(Circle((x, y), 0.2, facecolor=BRIGHT, edgecolor=BLUE, zorder=3))
        line(ax, [(8 + 1.5 * np.cos(a), 4.5 + 1.5 * np.sin(a)), (x, y)], color=INK, lw=0.9)
    ax.text(1.0, 8.3, "TOPOLOGY-CENTRIC COMPUTING", fontsize=18, color=INK, fontweight="bold")
    ax.text(1.0, 7.6, "interconnect is not a pipe; it is the machine", fontsize=15, color=GREY, fontweight="bold")
    save(fig, "tcc_topology.png")


# 20. Three generations
def three_generations():
    fig, ax = base()
    steps = [("Z-Brain I", 2.2, "10^6-10^7"), ("Z-Brain II", 5.0, "10^9-10^11"), ("Z-Brain III", 8.2, "10^14")]
    for i, (name, h, scale) in enumerate(steps):
        x = 1.8 + i * 4.4
        rect(ax, x, 1.4, 3.0, h, fc=PALE if i < 2 else BLUE, ec=BLUE, lw=1.6)
        ax.text(x + 1.5, 1.0, name, ha="center", fontsize=15, color=INK, fontweight="bold")
        ax.text(x + 1.5, 0.45, scale, ha="center", fontsize=14, color=GREY, fontweight="bold")
    save(fig, "three_generations.png")


# 21. Five partners in one formula
def five_partners():
    fig, ax = base()
    rect(ax, 1.2, 3.6, 13.6, 3.2, fc=PALE, ec=BLUE, lw=1.8)
    parts = [("Sc", "NDSC"), ("Tc", "TIANDA"), ("alpha", "SUZHOU·PKU·FUDAN"), ("Gamma_st", "TIANDA·NDSC")]
    x = 2.2
    for p, owner in parts:
        ax.text(x, 6.0, p, fontsize=24, color=BLUE, fontweight="bold")
        ax.text(x, 4.3, owner, fontsize=12, color=GREY, fontweight="bold")
        x += 3.4
    ax.text(1.2, 7.5, "ONE FORMULA, FIVE CUTS", fontsize=20, color=INK, fontweight="bold")
    save(fig, "five_partners.png")


# 22. Four funding channels
def funding_channels():
    fig, ax = base()
    labels = ["NSFC\nscience question", "BRAIN PROJECT\nmechanism", "AI PROJECT\nparadigm", "S&T COMMISSION\ncapability"]
    for i, label in enumerate(labels):
        x = 1.4 + i * 3.7
        rect(ax, x, 2.2, 2.9, 4.0, fc=PALE if i % 2 == 0 else BLUE, ec=BLUE, lw=1.5)
        ax.text(x + 1.45, 4.2, label, ha="center", va="center", fontsize=14,
                color=WHITE if i % 2 else INK, fontweight="bold")
    save(fig, "funding_channels.png")


# 23. Industry radar
def industry_radar():
    fig, ax = base()
    labels = ["EMBODIED", "UAV", "ORBIT", "INDUSTRIAL", "EDGE AI", "MEDICAL"]
    for i, label in enumerate(labels):
        a = np.pi / 2 + i * 2 * np.pi / 6
        x, y = 8 + 5.4 * np.cos(a), 4.5 + 5.4 * np.sin(a)
        ax.plot([8, x], [4.5, y], color=GREY, lw=1.2, alpha=0.7)
        ax.add_patch(Circle((x, y), 0.32, facecolor=BLUE, edgecolor=WHITE, lw=1.3, zorder=3))
        ax.text(x, y + 0.55 if y > 4.5 else y - 0.55, label, ha="center", fontsize=13, color=INK, fontweight="bold")
    for r in [1.8, 3.6, 5.4]:
        ax.add_patch(Circle((8, 4.5), r, facecolor="none", edgecolor=GREY, lw=0.9, alpha=0.5))
    ax.text(1.0, 8.3, "SIX APPLICATION SECTORS", fontsize=18, color=INK, fontweight="bold")
    save(fig, "industry_radar.png")


# 24. Closing: soil with growing network
def closing_soil_glow():
    fig, ax = base(dark=True)
    for x in np.linspace(0, 16, 17):
        ax.plot([x, x], [0, 9], color="#16223A", lw=0.5, alpha=0.5)
    for y in np.linspace(0, 9, 10):
        ax.plot([0, 16], [y, y], color="#16223A", lw=0.5, alpha=0.5)
    rng = np.random.default_rng(21)
    pts = []
    for _ in range(60):
        pts.append((rng.uniform(1.5, 14.5), rng.uniform(1.5, 7.8)))
    pts = np.array(pts)
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            d = np.hypot(*(pts[i] - pts[j]))
            if d < 1.0:
                ax.plot([pts[i][0], pts[j][0]], [pts[i][1], pts[j][1]], color=BRIGHT, lw=0.5, alpha=0.35)
    ax.scatter(pts[:, 0], pts[:, 1], s=14, c="#9DB8FF", zorder=3)
    ax.add_patch(Circle((8, 4.5), 0.9, facecolor="none", edgecolor=BRIGHT, lw=1.6, alpha=0.85, zorder=4))
    ax.add_patch(Circle((8, 4.5), 0.42, facecolor=BRIGHT, edgecolor=WHITE, lw=1.3, zorder=5))
    ax.text(0.8, 8.4, "INTELLIGENCE GROWS, NOT COMPUTES", fontsize=20, color=WHITE, fontweight="bold")
    save(fig, "closing_soil_glow.png")


# 25. CST formula card
def cst_formula():
    fig, ax = base()
    rect(ax, 1.4, 2.2, 13.2, 4.6, fc=PALE, ec=BLUE, lw=2.0)
    ax.text(8, 5.5, r"$C_{ST} = (S_c \cdot T_c)\; e^{\alpha \cdot \Gamma_{st}}$",
            ha="center", va="center", fontsize=42, color=INK, fontweight="bold")
    ax.text(8, 3.1, "space x time x nonlinear gain x spatiotemporal synergy",
            ha="center", va="center", fontsize=17, color=BLUE, fontweight="bold")
    save(fig, "cst_formula.png")


if __name__ == "__main__":
    cover_network_glow()
    energy_gap()
    four_walls()
    scaling_collapse()
    neuron_vs_synapse()
    water_phases()
    crystal_lattices()
    insulin_disulfide()
    connectome_302()
    topology_function()
    linear_vs_nonlinear()
    cascade_gain()
    emergence_physics()
    intelligence_scale()
    sdde_echo()
    local_rules_loop()
    criticality_powerlaw()
    sdi_control()
    tcc_topology()
    three_generations()
    five_partners()
    funding_channels()
    industry_radar()
    closing_soil_glow()
    cst_formula()
