# -*- coding: utf-8 -*-
"""
补全 §7 数值证据：EM 半阶收敛 vs Milstein 一阶收敛的 log-log 强收敛验证图。

测试方程（标量线性 SDDE，乘性噪声，Buckwar 2000 风格）：
    dX(t) = [ a*X(t) + b*X(t-tau) ] dt + [ c*X(t) ] dW(t),   t in [0,T]
    X(t)  = phi = 1,  t in [-tau, 0]
其中扩散项 g(X)=c*X 仅依赖当前态，g' = c，Milstein 修正项闭式：
    Milstein 增量 = ... + 0.5 * c^2 * X_n * (dW_n^2 - h)
延迟态由整数对齐 (tau/h in Z) 直接从历史缓冲区读取，零插值误差。

强误差定义：  err(h) = ( E| X_h(T) - X_exact(T) |^2 )^{1/2}
参考解 X_exact 用线性 SDDE 的解析基本解 + 细网格梯形求积计算（非数值参考解，
避免同路径 EM 误差相关性导致视在阶数偏高）。

解析解（逐段求解）：
  在 [k*tau, (k+1)*tau] 上：
    X(t) = Psi_k(t) * [ X(k*tau) + b * integral_{k*tau}^t Psi_k^{-1}(s) * X(s-tau) ds ]
  其中 Psi_k(t) = exp( (a-c^2/2)*(t-k*tau) + c*(W(t)-W(k*tau)) )

理论：EM 均方阶 p=1/2 ；可交换/标量乘性噪声下 Milstein p=1 。

输出：EM_Milstein_convergence.png / .pdf   (300 dpi)
"""
import numpy as np
import matplotlib.pyplot as plt

rng = np.random.default_rng(20260725)
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "cm",
    "axes.linewidth": 1.0,
    "font.size": 12,
})

# ---------------- 模型参数 ----------------
# 参数选择：a/c 比值适中，确保扩散 discretization 误差 O(h^{1/2}) 在所测步长范围内
# 压倒漂移误差 O(h)，从而 EM 的半阶收敛清晰可见。
# （a=-3,c=0.3 时漂移误差主导，EM 视在阶数偏向 1）
a, b, c = -1.0, 0.5, 1.0       # 漂移、延迟耦合、乘性噪声强度
tau, T  = 1.0, 2.0            # 延迟、终端时刻（T>tau 使延迟在 [tau,T] 内激活）
phi     = 1.0                 # 常值历史

def drift(x_now, x_del):
    return a * x_now + b * x_del

def diffusion(x_now):
    return c * x_now
# g'(x) = c  (对 x 求导)，Milstein 修正用

# ---------------- 解析精确解 ----------------
def exact_solution_T(dW_ref, h_ref):
    """
    线性 SDDE 的精确解 X(T)，基于解析基本解 + 细网格梯形求积。

    逐段求解：在 [k*tau, (k+1)*tau] 上，
      X(t) = Psi_k(t) * [ X(k*tau) + b * I_k(t) ]
      I_k(t) = integral_{k*tau}^t Psi_k^{-1}(s) * X(s-tau) ds
      Psi_k(t) = exp( (a-c^2/2)*(t-k*tau) + c*(W(t)-W(k*tau)) )

    积分用梯形法则在细网格上计算，误差 O(h_ref^{1-eps})，远优于 EM 的 O(h^{1/2})。
    """
    n_ref = int(round(T / h_ref))
    N_ref = int(round(tau / h_ref))
    n_tau = int(round(T / tau))

    # Brownian 路径: W[0]=0, W[k]=W(k*h_ref)
    W = np.concatenate([[0.0], np.cumsum(dW_ref)])

    alpha = a - c**2 / 2

    # buf[k]: k=0 -> t=-tau, k=N_ref -> t=0, k=N_ref+j -> t=j*h_ref
    buf = np.empty(n_ref + N_ref + 1)
    buf[:N_ref + 1] = phi                     # 历史 [-tau, 0]

    for seg in range(n_tau):
        k_start = N_ref + seg * N_ref          # t = seg * tau
        k_end   = N_ref + (seg + 1) * N_ref if seg < n_tau - 1 else N_ref + n_ref
        seg_len = k_end - k_start + 1

        # 基本解 Psi_k 及其逆
        w_start = seg * N_ref
        dt_seg  = np.arange(seg_len) * h_ref
        dW_seg  = W[w_start : w_start + seg_len] - W[w_start]
        log_Psi = alpha * dt_seg + c * dW_seg
        Psi     = np.exp(log_Psi)
        Psi_inv = np.exp(-log_Psi)

        X_start = buf[k_start]
        I_val   = 0.0

        for j in range(1, seg_len):
            k = k_start + j
            # 延迟值 X(s-tau): buf[k - N_ref]（对 seg=0 落在历史区，已初始化为 phi）
            f_prev = Psi_inv[j - 1] * buf[k - 1 - N_ref]
            f_curr = Psi_inv[j]     * buf[k     - N_ref]
            I_val += 0.5 * (f_prev + f_curr) * h_ref
            buf[k] = Psi[j] * (X_start + b * I_val)

    return buf[n_ref + N_ref]                   # X(T)

# ---------------- 单条路径的强误差 ----------------
def one_path_errors(hs, h_ref, method):
    """
    在一条公共 Brownian 路径上，比较粗步长数值解与解析精确解在 T 处的误差。
    method: 'EM' 或 'Milstein'
    返回：dict{h: |X_h(T) - X_exact(T)|^2}
    """
    n_ref = int(round(T / h_ref))
    dW_ref = rng.standard_normal(n_ref) * np.sqrt(h_ref)

    def integrate(h):
        n = int(round(T / h))
        N = int(round(tau / h))
        m = int(round(h / h_ref))            # 每个粗步含多少细步
        buf = np.empty(n + N + 1)
        buf[:N + 1] = phi                     # 历史 [-tau,0]
        for k in range(N, N + n):
            x_now = buf[k]
            x_del = buf[k - N]
            j = (k - N) * m
            dW = dW_ref[j:j + m].sum()
            incr = drift(x_now, x_del) * h + diffusion(x_now) * dW
            if method == 'Milstein':
                incr += 0.5 * c * c * x_now * (dW * dW - h)
            buf[k + 1] = x_now + incr
        return buf[N:][-1]                     # X(T)

    x_exact = exact_solution_T(dW_ref, h_ref)
    return {h: (integrate(h) - x_exact) ** 2 for h in hs}

# ---------------- 蒙特卡洛聚合 ----------------
def convergence(method, hs, h_ref, M=2000):
    acc = {h: 0.0 for h in hs}
    for _ in range(M):
        errs = one_path_errors(hs, h_ref, method)
        for h in hs:
            acc[h] += errs[h]
    return np.array([np.sqrt(acc[h] / M) for h in hs])

# 步长序列：均为 tau 的整数分之一，保证整数对齐
levels = [4, 5, 6, 7, 8]                       # h = tau / 2^level
hs = np.array([tau / (2 ** L) for L in levels])
h_ref = tau / (2 ** 12)                         # 参考步长（远细于最细粗步）
M = 2000

err_EM  = convergence('EM',       hs, h_ref, M)
err_MIL = convergence('Milstein', hs, h_ref, M)

# ---------------- 拟合斜率 ----------------
slope_EM  = np.polyfit(np.log(hs), np.log(err_EM),  1)[0]
slope_MIL = np.polyfit(np.log(hs), np.log(err_MIL), 1)[0]
print(f"EM       fitted order  ~ {slope_EM:.3f}   (theory 0.5)")
print(f"Milstein fitted order  ~ {slope_MIL:.3f}   (theory 1.0)")

# ---------------- 绘图 ----------------
fig, ax = plt.subplots(figsize=(6.6, 5.2))
ax.loglog(hs, err_EM,  'o-', color="#1f4e79", lw=2, ms=7,
          label=rf"Euler--Maruyama  (slope $\approx {slope_EM:.2f}$)")
ax.loglog(hs, err_MIL, 's-', color="#c0504d", lw=2, ms=7,
          label=rf"Milstein  (slope $\approx {slope_MIL:.2f}$)")
# 参考斜率虚线
ax.loglog(hs, err_EM[0]  * (hs / hs[0]) ** 0.5, '--', color="#7f9bbf", lw=1.4,
          label=r"reference slope $1/2$")
ax.loglog(hs, err_MIL[0] * (hs / hs[0]) ** 1.0, ':',  color="#d8a0a0", lw=1.6,
          label=r"reference slope $1$")

ax.set_xlabel(r"step size $h$")
ax.set_ylabel(r"strong error $\left(\mathbb{E}|X_h(T)-X_{\mathrm{exact}}(T)|^2\right)^{1/2}$")
ax.set_title(r"Strong convergence: EM ($p=\frac{1}{2}$) vs Milstein ($p=1$)"
             "\n" r"scalar linear SDDE, $a{=}-1,\,b{=}0.5,\,c{=}1.0,\,\tau{=}1,\,T{=}2$",
             fontsize=12)
ax.grid(True, which="both", ls=":", alpha=0.5)
ax.legend(frameon=False, fontsize=11, loc="lower right")
fig.tight_layout()
fig.savefig("EM_Milstein_convergence.png", dpi=300, bbox_inches="tight")
fig.savefig("EM_Milstein_convergence.pdf", bbox_inches="tight")
print("已保存：EM_Milstein_convergence.pdf / .png")
