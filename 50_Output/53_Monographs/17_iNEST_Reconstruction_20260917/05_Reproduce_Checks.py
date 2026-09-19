"""Numerical checks of analytic counterexamples, not an intelligence benchmark."""

from pathlib import Path
import math
import platform

import numpy as np


def main():
    rows = []
    tol = 1e-10
    for a in (0.2, 0.8, 0.99):
        var_x = 1 / (1 - a * a)
        mse = 1 - 1 / var_x
        capacity = (1 - a * a) * np.sum(a ** (2 * np.arange(10000)))
        assert abs(mse - a * a) < tol
        assert abs(capacity - 1) < tol
        rows.append(("V-TH02", f"a={a}", f"current-input MSE={mse:.12g}; capacity sum={capacity:.12g}"))
    for delay in (0, 1, 4, 16):
        q_star = delay / (delay + 1)
        grid = np.linspace(0, 0.999999, 100001)
        capacities = (1 - grid) * grid ** delay
        q_grid = grid[np.argmax(capacities)]
        assert abs(q_grid - q_star) < 1.1e-5
        rows.append(("V-TH02", f"delay={delay}", f"optimal a^2={q_star:.12g}; grid a^2={q_grid:.12g}"))

    for coupling in (0.1, 0.5):
        matrix = np.array([[-1.0, coupling], [coupling, -1.0]])
        largest = np.linalg.eigvalsh(matrix)[-1]
        assert abs(largest - (-1 + coupling)) < tol
        assert largest > -1
        rows.append(("V-TH06", f"coupling={coupling}", f"coupled lambda_max={largest:.12g}; isolated=-1"))

    for gain in (0.0, 4.0, 12.0):
        propagator = math.exp(-1) * np.array([[1.0, gain], [0.0, 1.0]])
        norm = np.linalg.svd(propagator, compute_uv=False)[0]
        if gain >= 4:
            assert norm > 1
        rows.append(("V-TH01", f"nonnormal gain={gain}", f"norm at t=1: {norm:.12g}; both exponents=-1"))

    a, diffusion = 2.0, 0.7
    rotation = np.array([[0.0, -1.0], [1.0, 0.0]])
    covariance = diffusion / a * np.eye(2)
    for omega in (0.0, 1.0, 3.0):
        drift = -a * np.eye(2) + omega * rotation
        residual = drift @ covariance + covariance @ drift.T + 2 * diffusion * np.eye(2)
        ep_rate = np.trace((omega * rotation).T @ (omega * rotation) @ covariance) / diffusion
        assert np.linalg.norm(residual) < tol
        assert abs(ep_rate - 2 * omega * omega / a) < tol
        rows.append(("V-TH05", f"OU omega={omega}", f"entropy rate / kB={ep_rate:.12g}; exponents=(-2,-2)"))

    rng = np.random.default_rng(20260917)
    mapping = rng.normal(size=(5, 8))
    noise = 0.3 * np.eye(5)
    sigma = mapping @ mapping.T + noise
    geometry = mapping.T @ np.linalg.solve(sigma, mapping)
    eigenvalues = np.linalg.eigvalsh(geometry)
    assert eigenvalues.min() > -tol and eigenvalues.max() <= 1 + tol
    assert np.trace(geometry) <= np.linalg.matrix_rank(sigma) + tol
    target = rng.normal(size=8)
    readout = np.linalg.solve(sigma, mapping @ target)
    mse_direct = np.linalg.norm(target - mapping.T @ readout) ** 2 + readout @ noise @ readout
    mse_formula = target @ target - target @ geometry @ target
    assert abs(mse_direct - mse_formula) < tol
    rows.append(("V-TH07", "fixed Gaussian channel", f"trace G={np.trace(geometry):.12g}; risk identity residual={abs(mse_direct-mse_formula):.3g}"))

    direction = rng.normal(size=mapping.shape)
    task_weight = np.outer(target, target) / (target @ target)
    inv_sigma = np.linalg.inv(sigma)
    delta_sigma = direction @ mapping.T + mapping @ direction.T
    gradient = 2 * np.trace(task_weight @ mapping.T @ inv_sigma @ direction)
    gradient -= np.trace(inv_sigma @ mapping @ task_weight @ mapping.T @ inv_sigma @ delta_sigma)

    def score(channel):
        covariance = channel @ channel.T + noise
        return np.trace(task_weight @ channel.T @ np.linalg.solve(covariance, channel))

    step = 1e-6
    difference = (score(mapping + step * direction) - score(mapping - step * direction)) / (2 * step)
    assert abs(gradient - difference) < 1e-7
    rows.append(("V-TH09", "fixed-noise Gaussian channel", f"directional derivative residual={abs(gradient-difference):.3g}"))

    output = Path(__file__).with_name("08_Numerical_Checks.md")
    lines = [
        "# Numerical Checks", "",
        "Evidence: [仿真]. These are deterministic numerical checks of analytic examples, not hardware measurements or intelligence performance results.",
        "Parameters are [假设] synthetic test configurations, not fitted physical measurements.",
        f"Runtime: Python {platform.python_version()}, NumPy {np.__version__}.",
        "Seed: 20260917. Algebra tolerance: 1e-10; grid location tolerance: 1.1e-5.",
        "Derivative check: central step 1e-6, absolute tolerance 1e-7; fixed additive noise for this example only.",
        "Time units are normalized; the OU example assumes even time-reversal parity and constant diffusion.", "",
        "| Task | Configuration | Result |", "|---|---|---|",
    ]
    lines += [f"| {task} | {config} | {result} |" for task, config, result in rows]
    lines += ["", "Result: all assertions passed. Analytic proofs and scope restrictions are in the main report."]
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"PASS: {len(rows)} checks; {output}")


if __name__ == "__main__":
    main()
