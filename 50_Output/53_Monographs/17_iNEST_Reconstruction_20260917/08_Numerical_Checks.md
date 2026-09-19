# Numerical Checks

Evidence: [仿真]. These are deterministic numerical checks of analytic examples, not hardware measurements or intelligence performance results.
Parameters are [假设] synthetic test configurations, not fitted physical measurements.
Runtime: Python 3.12.14, NumPy 2.3.5.
Seed: 20260917. Algebra tolerance: 1e-10; grid location tolerance: 1.1e-5.
Derivative check: central step 1e-6, absolute tolerance 1e-7; fixed additive noise for this example only.
Time units are normalized; the OU example assumes even time-reversal parity and constant diffusion.

| Task | Configuration | Result |
|---|---|---|
| V-TH02 | a=0.2 | current-input MSE=0.04; capacity sum=1 |
| V-TH02 | a=0.8 | current-input MSE=0.64; capacity sum=1 |
| V-TH02 | a=0.99 | current-input MSE=0.9801; capacity sum=1 |
| V-TH02 | delay=0 | optimal a^2=0; grid a^2=0 |
| V-TH02 | delay=1 | optimal a^2=0.5; grid a^2=0.4999995 |
| V-TH02 | delay=4 | optimal a^2=0.8; grid a^2=0.7999992 |
| V-TH02 | delay=16 | optimal a^2=0.941176470588; grid a^2=0.94117905882 |
| V-TH06 | coupling=0.1 | coupled lambda_max=-0.9; isolated=-1 |
| V-TH06 | coupling=0.5 | coupled lambda_max=-0.5; isolated=-1 |
| V-TH01 | nonnormal gain=0.0 | norm at t=1: 0.367879441171; both exponents=-1 |
| V-TH01 | nonnormal gain=4.0 | norm at t=1: 1.55836232033; both exponents=-1 |
| V-TH01 | nonnormal gain=12.0 | norm at t=1: 4.44499992745; both exponents=-1 |
| V-TH05 | OU omega=0.0 | entropy rate / kB=0; exponents=(-2,-2) |
| V-TH05 | OU omega=1.0 | entropy rate / kB=1; exponents=(-2,-2) |
| V-TH05 | OU omega=3.0 | entropy rate / kB=9; exponents=(-2,-2) |
| V-TH07 | fixed Gaussian channel | trace G=4.57163081089; risk identity residual=4.44e-16 |
| V-TH09 | fixed-noise Gaussian channel | directional derivative residual=6.01e-11 |

Result: all assertions passed. Analytic proofs and scope restrictions are in the main report.
