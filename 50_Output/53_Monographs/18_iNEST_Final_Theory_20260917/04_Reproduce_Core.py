"""Reproducible algebra checks and a synthetic connection-only example.

No result from this script is hardware evidence or an intelligence benchmark.
"""

from itertools import combinations, product
from pathlib import Path
import platform
import numpy as np
import scipy
from scipy.optimize import root
from scipy.linalg import expm
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
OUT = Path("D:/Obsidian/Output/18_iNEST_Final_Theory_20260917")
EDGES = list(combinations(range(5), 2))
B = np.zeros((5, len(EDGES)))
for k, (i, j) in enumerate(EDGES):
    B[i, k], B[j, k] = 1.0, -1.0
LEAK = np.array([0.7, 0.9, 0.8, 1.0, 0.6])
NONLIN = 0.4
INPORT = np.eye(5)[:, :2]
OUTPORT = np.eye(5)[[3, 4]]


def laplacian(g):
    return (B * g) @ B.T


def state(g, u, target=None, beta=0.0):
    matrix = np.diag(LEAK) + laplacian(g)
    def force(x):
        out = matrix @ x + NONLIN * x**3 - INPORT @ u
        if target is not None:
            out += beta * OUTPORT.T @ (OUTPORT @ x - target)
        return out
    def jac(x):
        h = matrix + np.diag(3 * NONLIN * x**2)
        if target is not None:
            h += beta * OUTPORT.T @ OUTPORT
        return h
    result = root(force, np.zeros(5), jac=jac, tol=1e-11)
    assert np.max(np.abs(force(result.x))) < 1e-9
    return result.x, jac(result.x)


def loss(g, inputs, targets):
    return float(np.mean([0.5 * np.sum((OUTPORT @ state(g, u)[0] - y)**2)
                          for u, y in zip(inputs, targets)]))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(20260918)
    records = []
    g = np.linspace(0.12, 0.57, len(EDGES))
    u, target = np.array([0.7, -0.2]), np.array([0.2, -0.1])
    x, h = state(g, u)
    dx = -np.linalg.solve(h, B * (B.T @ x))
    step = 1e-5
    dx_fd = np.column_stack([(state(g + step * np.eye(len(g))[e], u)[0]
                              - state(g - step * np.eye(len(g))[e], u)[0]) / (2 * step)
                             for e in range(len(g))])
    residual = np.max(np.abs(dx - dx_fd))
    assert residual < 1e-7
    records.append(("V-TH12", "implicit response derivative", residual, "< 1e-7"))

    exact = dx.T @ OUTPORT.T @ (OUTPORT @ x - target)
    errors = []
    betas = np.array([1e-2, 1e-3, 1e-4, 1e-5])
    for beta in betas:
        xp, _ = state(g, u, target, beta)
        estimate = ((B.T @ xp)**2 - (B.T @ x)**2) / (2 * beta)
        errors.append(np.linalg.norm(estimate - exact))
    assert errors[-1] < 2e-6 and np.all(np.diff(errors) < 0)
    records.append(("V-TH13", "two-phase gradient, smallest beta", errors[-1], "< 2e-6; decreasing error"))

    caps = np.diag([1.0, 1.3, 0.7, 1.8, 0.9])
    cinv = np.linalg.inv(caps)
    m = np.diag(LEAK) + laplacian(g)
    drift = -cinv @ m
    covariance = 0.02 * cinv
    noise = 0.04 * cinv @ m @ cinv
    residual = np.linalg.norm(drift @ covariance + covariance @ drift.T + noise)
    assert residual < 1e-12 and np.max(np.real(np.linalg.eigvals(drift))) < 0
    records.append(("V-TH10", "normalized equilibrium noise covariance", residual, "< 1e-12; stable drift"))

    q = np.diag([1.0, 2.0, 4.0])
    v = np.array([0.8, 0.5, 0.2])
    optimum = np.array([0.1, 0.6, 0.7])
    grad = q @ (v - optimum)
    eta = 0.3
    updated = np.clip(v - eta * grad, 0.0, 1.0)
    d = updated - v
    f = lambda z: 0.5 * (z - optimum) @ q @ (z - optimum)
    lhs = f(updated) - f(v)
    rhs = -(1 / eta - 4 / 2) * (d @ d)
    assert lhs <= rhs + 1e-12
    records.append(("V-TH14", "projected descent inequality slack", rhs - lhs, ">= -1e-12"))

    theta = np.array([0.3, -0.4])
    prob = 1 / (1 + np.exp(-theta))
    score_grad = np.zeros(2)
    for bits in product([0, 1], repeat=2):
        bits = np.array(bits)
        mass = np.prod(np.where(bits, prob, 1 - prob))
        reward = float(bits.sum() == 1)
        score_grad += mass * (reward - 0.25) * (bits - prob)
    exact_score = prob * (1 - prob) * (1 - 2 * prob[::-1])
    residual = np.max(np.abs(score_grad - exact_score))
    assert residual < 1e-12
    records.append(("V-TH15", "local score x feedback vs enumeration", residual, "< 1e-12"))

    j1 = np.array([[0., -1, 0], [1, 0, 0], [0, 0, 0]])
    j2 = np.array([[0., 0, -1], [0, 0, 0], [1, 0, 0]])
    frame = expm(0.4 * j1) @ expm(-0.3 * j2)
    au = expm(0.3 * j2) @ j1 @ expm(-0.3 * j2)
    av = j2
    derivative = au @ j2 - j2 @ au
    curvature = -derivative + au @ av - av @ au
    assert np.linalg.norm(curvature) < 1e-12
    assert np.linalg.norm(j1 @ j2 - j2 @ j1) > 0.1
    records.append(("V-GEO02", "noncommuting frame generators, zero pure-gauge curvature", np.linalg.norm(curvature), "< 1e-12"))
    z = np.array([0.2, -0.5, 0.4])
    changed = expm(0.2 * j2)
    residual = np.linalg.norm(frame @ z - frame @ changed @ changed.T @ z)
    assert residual < 1e-12
    records.append(("V-GEO02", "basis-change preserves physical state", residual, "< 1e-12"))

    # Teacher-generated realizable task; all nodes, ports and readout stay fixed.
    train = rng.uniform(-1, 1, (24, 2))
    test = rng.uniform(-1, 1, (80, 2))
    teacher_set = {EDGES.index(e) for e in [(0, 2), (1, 2), (2, 3), (3, 4)]}
    teacher = np.array([float(e in teacher_set) for e in range(len(EDGES))])
    train_y = np.array([OUTPORT @ state(teacher, sample)[0] for sample in train])
    test_y = np.array([OUTPORT @ state(teacher, sample)[0] for sample in test])
    current = np.array([float(0 in edge) for edge in EDGES])
    initial = current.copy()
    history, train_calls, accepted = [], 0, 0
    while True:
        current_loss = loss(current, train, train_y)
        train_calls += 1
        history.append((current_loss, loss(current, test, test_y)))
        candidates = []
        for removed in np.flatnonzero(current):
            for added in np.flatnonzero(1 - current):
                trial = current.copy()
                trial[removed], trial[added] = 0, 1
                candidates.append((loss(trial, train, train_y), removed, added))
                train_calls += 1
        best_loss, removed, added = min(candidates)
        if best_loss >= current_loss - 1e-12:
            break
        current[removed], current[added] = 0, 1
        accepted += 1
        assert current.sum() == initial.sum() == 4
        assert accepted < 30
    assert history[-1][0] <= history[0][0]

    fig, axs = plt.subplots(1, 3, figsize=(12, 3.5), layout="constrained")
    axs[0].loglog(betas, errors, "o-", color="#137f72")
    axs[0].set(xlabel="Nudge beta", ylabel="Gradient error norm", title="Local two-phase derivative")
    angle = np.linspace(0, 2 * np.pi, 60)
    circle_inputs = np.column_stack([np.cos(angle), np.sin(angle)])
    for conductance, name, color in [(initial, "Initial wiring", "#b74747"), (current, "Adapted wiring", "#137f72")]:
        responses = np.array([OUTPORT @ state(conductance, sample)[0] for sample in circle_inputs])
        axs[1].plot(responses[:, 0], responses[:, 1], label=name, color=color)
    axs[1].set(xlabel="Output 1", ylabel="Output 2", title="Response geometry changes")
    axs[1].legend(fontsize=8)
    hist = np.array(history)
    axs[2].plot(np.maximum(hist[:, 0], 1e-16), "o-", label="Training", color="#137f72")
    axs[2].plot(np.maximum(hist[:, 1], 1e-16), "s--", label="Held-out synthetic", color="#b74747")
    axs[2].set(xlabel="Accepted edge swaps", ylabel="Squared loss", yscale="log", title="Fixed nodes and readout")
    axs[2].legend(fontsize=8)
    fig.savefig(OUT / "02_Core_Numerical_Examples.png", dpi=180)
    plt.close(fig)

    lines = ["# 解析校核与纯连接数值示例", "", "证据：[仿真]。不是器件实测，也不是智能性能基准。",
             "配置均为[假设]合成示例；单位归一化，不能兑换成真实功率或延迟。",
             f"运行环境：Python {platform.python_version()}，NumPy {np.__version__}，SciPy {scipy.__version__}。",
             "固定种子 20260918；节点数 5，候选边为完全无向图的 10 条边。",
             "节点线性泄漏为 [0.7,0.9,0.8,1.0,0.6]，三次系数 0.4；输入为节点 0、1，输出固定为节点 3、4。",
             "V-SIM02 验收：每项残差通过下表事先写入脚本的容差；只支持相应解析实现。", "",
             "| 任务 | 检验 | 数值 | 通过标准 |", "|---|---|---|---|"]
    lines += [f"| {key} | {name} | {value:.8g} | {criterion} |" for key, name, value, criterion in records]
    lines += ["", "## 只改变二值连接的示例", "",
              "每个候选均保持 4 条单位电导边；固定节点参数、输入、输出和读出，使用穷举邻居的贪心换边。",
              "这是有中央候选评价器的最小参考算法，不是已经完成的局部硬件自组织实现。",
              "训练输入 24 组、独立同分布留出输入 80 组；标签来自预先固定的同类教师网络。",
              "测试数据只用于记录，既不选候选也不选停止时刻。单一种子和可实现教师不支持外部任务泛化结论。",
              f"[仿真] 接受换边：{accepted}；训练损失评价调用：{train_calls}（每次包括全部训练输入）。",
              f"[仿真] 初始训练/留出损失：{history[0][0]:.10g} / {history[0][1]:.10g}。",
              f"[仿真] 最终训练/留出损失：{history[-1][0]:.10g} / {history[-1][1]:.10g}。",
              f"初始边：{[EDGES[i] for i in np.flatnonzero(initial)]}。",
              f"最终边：{[EDGES[i] for i in np.flatnonzero(current)]}。",
              "验收只要求合法边数与训练损失非增；未预设留出改善和教师图恢复。",
              "没有热噪声、延迟、器件漂移、总表计量或跨种子统计，故 V-EXP03 和 V-EXP04 仍待测。",
              "", "图：Output/18_iNEST_Final_Theory_20260917/02_Core_Numerical_Examples.png。"]
    (ROOT / "05_Numerical_Checks.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("PASS", len(records), "analytic checks; swaps", accepted, "evaluations", train_calls)
    print("Initial/final held-out loss:", history[0][1], history[-1][1])


if __name__ == "__main__":
    main()
