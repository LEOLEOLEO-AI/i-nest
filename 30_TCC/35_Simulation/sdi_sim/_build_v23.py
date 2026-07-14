#!/usr/bin/env python3
"""Build v23 fusion: v22 base + v11 attractor + JEPA + gradient clipping"""
import os

workspace = r"D:\Obsidian\phase1_workspace"
base_path = os.path.join(workspace, "sdi_v22_evolution.py")
out_path = os.path.join(workspace, "sdi_v23_fusion.py")

with open(base_path, "r", encoding="utf-8") as f:
    code = f.read()

# ---- Version strings ----
code = code.replace("SDI v22", "SDI v23")
code = code.replace("v22:", "v23:")
code = code.replace("v22_results", "v23_results")
code = code.replace("v22 Design Doc", "v23 Fusion")
code = code.replace("sdi_v22_evolution.py", "sdi_v23_fusion.py")
code = code.replace("v8 base", "v8 base + v11 FEP attractor + JEPA")
code = code.replace("3 upgrade", "5 upgrade")
code = code.replace("1. Adaptive Theta", "1. Adaptive Theta + v11 FEP Attractor")
code = code.replace("2. FEP Global Homeostasis", "2. FEP Global Homeostasis + Gradient Clip")
code = code.replace("3. External Data Closed Loop", "3. External Data Closed Loop + JEPA Adaptive Beta")
code = code.replace("from v8 baseline", "from v8 baseline + v11 FEP attractor + JEPA")

# ---- Add v23 config after FEP config block ----
marker = "FEP_HOMEOSTASIS_INT = 20"
mpos = code.find(marker)
assert mpos > 0, f"Marker not found: {marker}"
end_line = code.find("\n", mpos) + 1

v23_config = """
# ============ v23 Fusion: v11 FEP Attractor + JEPA ============
FEP_GRAD_CLIP = 0.5
FEP_ATTRACTOR_STRENGTH = 0.3
FEP_BASIN_WINDOW = 10
JEPA_BETA_MIN = 0.5
JEPA_BETA_MAX = 5.0
JEPA_TARGET_ENTROPY = 0.35
GLOBAL_ENERGY_BUDGET = 500.0
"""
code = code[:end_line] + v23_config + code[end_line:]

# ---- Add basin tracking init after self.F_local ----
f_init = "self.F_local = np.zeros(self.N)"
fpos = code.find(f_init)
assert fpos > 0
f_end = code.find("\n", fpos) + 1

basin_init = """        # v23: FEP basin tracking (from v11 attractor guidance)
        self.F_basin_min = np.full(self.N, np.inf)
        self.F_basin_count = np.zeros(self.N, np.int32)
        self.F_converged = np.zeros(self.N, bool)
        self.F_gradient = np.zeros(self.N)
        self.F_prediction_error = np.zeros(self.N)
        self.F_complexity = np.zeros(self.N)
        # v23: JEPA adaptive beta
        self.beta_eff = JEPA_BETA_MIN
        self.entropy_history = []
        self.sigma_history = []
        self.el_ratio_history = []
        self.beta_eff_history = []
"""
code = code[:f_end] + basin_init + code[f_end:]

# ---- Add v23 methods before step() ----
step_marker = "    def step(self):"
spos = code.find(step_marker)
assert spos > 0

v23_methods = """
    # ===== v23: FEP basin tracking (from v11) =====
    def fep_basin_update(self):
        for i in range(self.N):
            if abs(self.F_local[i]) < 1e-12:
                continue
            if self.F_local[i] < self.F_basin_min[i] * 0.99:
                self.F_basin_min[i] = self.F_local[i]
                self.F_basin_count[i] = 0
                self.F_converged[i] = False
            else:
                self.F_basin_count[i] += 1
                if self.F_basin_count[i] > FEP_BASIN_WINDOW:
                    self.F_converged[i] = True

    # ===== v23: FEP gradient with clipping (from v11) =====
    def fep_gradient_clip(self):
        for i in range(self.N):
            out_mask = (self.src == i)
            if not out_mask.any():
                self.F_gradient[i] = 0.0
                continue
            grad = 0.0; n_out = 0
            for j in np.where(out_mask)[0]:
                tgt_node = self.tgt[j]
                prediction = self.h[i] * self.weight[j]
                actual = self.h[tgt_node]
                grad += 2.0 * (prediction - actual) * self.weight[j]
                n_out += 1
            raw_grad = grad / max(n_out, 1)
            self.F_gradient[i] = np.clip(raw_grad, -FEP_GRAD_CLIP, FEP_GRAD_CLIP)

    # ===== v23: JEPA entropy regulation (from v11) =====
    def jepa_entropy_regulation(self):
        if len(self.entropy_history) < 5:
            return
        recent_H = np.mean(self.entropy_history[-5:])
        error_H = recent_H - JEPA_TARGET_ENTROPY
        self.beta_eff = np.clip(
            JEPA_BETA_MIN + (JEPA_BETA_MAX - JEPA_BETA_MIN) *
            (1.0 / (1.0 + np.exp(-2.0 * error_H))),
            JEPA_BETA_MIN, JEPA_BETA_MAX
        )

    # ===== v23: FEP-modulated theta (fusion innovation) =====
    def fep_modulate_theta(self):
        conv_rate = self.F_converged.mean()
        modulation = 1.0 - FEP_ATTRACTOR_STRENGTH * (conv_rate - 0.5)
        modulation = np.clip(modulation, 0.7, 1.3)
        self.theta_ltp_current = max(T_THETA_MIN,
            min(int(self.theta_ltp_current * modulation), T_THETA_MAX))

    # ===== v23: global energy budget (from v11) =====
    def energy_budget_check(self):
        total_energy = self.F_local.sum() + (self.Ea * self.weight**2).sum()
        if total_energy > GLOBAL_ENERGY_BUDGET:
            scale = GLOBAL_ENERGY_BUDGET / total_energy
            self.Ea *= (1.0 + scale) / 2.0
            self.Ea = np.clip(self.Ea, 0.005, Ea_L)

"""
code = code[:spos] + v23_methods + "\n" + code[spos:]

# ---- Insert v23 calls in step() after compute_local_F() ----
cf_marker = "self.compute_local_F()"
cf_pos = code.find(cf_marker)
assert cf_pos > 0
cf_end = code.find("\n", cf_pos) + 1

v23_step_calls = """        # v23: FEP basin + gradient + JEPA + theta modulation + energy budget
        self.fep_basin_update()
        self.fep_gradient_clip()
        self.jepa_entropy_regulation()
        self.fep_modulate_theta()
        self.energy_budget_check()
"""
code = code[:cf_end] + v23_step_calls + code[cf_end:]

# ---- Save ----
with open(out_path, "w", encoding="utf-8") as f:
    f.write(code)

print(f"v23 fusion written: {out_path}")
print(f"Size: {len(code)} bytes")
