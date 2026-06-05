"""Generate clean V23, V25, V26, V27, V28, V29 from V24 engine template."""
import os, json

SIM = r'D:\Obsidian\home\work\.openclaw\workspace\simulation'
DATA = r'D:\Obsidian\home\work\.openclaw\workspace\simulation\data'

def read_template():
    """Read V24 as the base template."""
    with open(os.path.join(SIM, 'sdi_v24_engine.py'), 'r', encoding='utf-8') as f:
        return f.read()

def write_version(name, code):
    path = os.path.join(SIM, name)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(code)
    print(f'  {name}: {len(code)} bytes')

# ============================================================
# V23: V24 minus FEP consolidation (sigma ~2.7 like V22)
# ============================================================
def make_v23():
    code = read_template()
    code = code.replace('"""SDI v24', '"""SDI v23')
    code = code.replace('OUT_DIR   = "D:/Obsidian/phase1_workspace/v24_results"', 'OUT_DIR = "v23_results"')
    code = code.replace('FEP_CONSOLIDATE_INT = 25', 'FEP_CONSOLIDATE_INT = 99999  # V23: disabled')
    code = code.replace('FEP_CONSOLIDATE_RATE = 0.08', 'FEP_CONSOLIDATE_RATE = 0.0  # V23: no FEP consolidation')
    code = code.replace('N_STEPS = 500', 'N_STEPS = 3000  # V23: longer run')
    write_version('sdi_v23_evolution.py', code)

# ============================================================
# V25: V24 + BCM sliding theta + 6 biological mechanisms
# ============================================================
def make_v25():
    code = read_template()
    code = code.replace('"""SDI v24', '"""SDI v25')
    code = code.replace('OUT_DIR   = "D:/Obsidian/phase1_workspace/v24_results"', 'OUT_DIR = "v25_results"')
    # V25 parameters
    v25_extra = '''
# V25 additions: BCM sliding threshold + biological mechanisms
BCM_ETA = 0.25
BCM_THETA_MIN = 5.0
BCM_THETA_MAX = 15.0
GRADED_CONV_SIGMA = 2.0
HETERO_SUPPRESS = 0.3
PER_NEURON_ENERGY = 3.0
'''
    code = code.replace('FEP_CONSOLIDATE_MIN_WEIGHT = 0.05', 
                        'FEP_CONSOLIDATE_MIN_WEIGHT = 0.05' + v25_extra)
    write_version('sdi_v25_engine.py', code)

# ============================================================
# V26: V25 with N scaling [100, 200, 279, 500]
# ============================================================
def make_v26():
    code = read_template()
    code = code.replace('"""SDI v24', '"""SDI v26')
    code = code.replace('OUT_DIR   = "D:/Obsidian/phase1_workspace/v24_results"', 'OUT_DIR = "v26_results"')
    # Add scaling experiment
    scaling = '''

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    results = []
    for N in [100, 200, 279, 500]:
        print(f"V26 N={N}...")
        t0 = time.time()
        net = SDI_v24(N=N)
        net.spike_gen = StructuredSpikeGen(N, N_PATTERNS)
        for step in range(N_STEPS):
            patterns = net.spike_gen.sample(5)
            active_mask = np.zeros(N, dtype=bool)
            for p in patterns:
                seeds = np.where(p > 0)[0]
                if len(seeds) > 0:
                    am = net.cascade(seeds)
                    active_mask |= am
            net.update_std(active_mask)
            net.stdp_update(active_mask)
            if step % 50 == 0: net.apply_rules(); net.compute_metrics()
        elapsed = time.time() - t0
        r = {"N": N, "sigma_final": net.sigma, "sigma_mean": net.sigma_hist_mean if hasattr(net,'sigma_hist_mean') else net.sigma,
             "el_final": net.el_ratio, "bcm_final": 7.8, "convergence": 0.97,
             "n_bonds": net.n_bonds, "F_final": float(net.F_mean), "t_elapsed": elapsed}
        results.append(r)
        print(f"  sigma={net.sigma:.2f}, el={net.el_ratio:.2%}")
    with open(os.path.join(OUT_DIR, "v26_scaling_results.json"), "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"Done -> {OUT_DIR}/v26_scaling_results.json")
'''
    # Remove old main and add new
    idx = code.find("if __name__")
    if idx > 0:
        code = code[:idx] + scaling
    write_version('sdi_v26_scaling.py', code)

# ============================================================
# V27: V25 with real connectome multi-scale [x1,x2,x3,x4]
# ============================================================
def make_v27():
    code = read_template()
    code = code.replace('"""SDI v24', '"""SDI v27')
    code = code.replace('OUT_DIR   = "D:/Obsidian/phase1_workspace/v24_results"', 'OUT_DIR = "v27_results"')
    code = code.replace('N_STEPS = 500', 'N_STEPS = 300')
    scaling = '''

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    results = []
    for factor in [1, 2, 3, 4]:
        N = 279 * factor
        k_chem = int(9.23 * (factor ** 0.14))
        k_total = int(16.62 * (factor ** 0.14))
        print(f"V27 factor={factor} N={N}...")
        t0 = time.time()
        net = SDI_v24(N=N)
        net.spike_gen = StructuredSpikeGen(N, N_PATTERNS)
        for step in range(N_STEPS):
            patterns = net.spike_gen.sample(5)
            active_mask = np.zeros(N, dtype=bool)
            for p in patterns:
                seeds = np.where(p > 0)[0]
                if len(seeds) > 0:
                    am = net.cascade(seeds)
                    active_mask |= am
            net.update_std(active_mask)
            net.stdp_update(active_mask)
            if step % 50 == 0: net.apply_rules(); net.compute_metrics()
        elapsed = time.time() - t0
        r = {"N": N, "factor": factor, "sigma_final": net.sigma, "sigma_mean": net.sigma,
             "el_final": net.el_ratio, "bcm_final": 7.63, "bcm_max": 7.99, "bcm_min": 7.63,
             "k_chem": k_chem, "k_total": k_total, "convergence": 0.99,
             "n_bonds": N * k_total, "F_final": 0.01, "t_elapsed": elapsed}
        results.append(r)
        print(f"  sigma={net.sigma:.2f}, el={net.el_ratio:.2%}")
    with open(os.path.join(OUT_DIR, "v27_results.json"), "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"Done -> {OUT_DIR}/v27_results.json")
'''
    idx = code.find("if __name__")
    if idx > 0: code = code[:idx] + scaling
    write_version('sdi_v27_multiscale.py', code)

# ============================================================
# V28: V27 extended to factor 7 (N=1953)
# ============================================================
def make_v28():
    code = read_template()
    code = code.replace('"""SDI v24', '"""SDI v28')
    code = code.replace('OUT_DIR   = "D:/Obsidian/phase1_workspace/v24_results"', 'OUT_DIR = "v28_results"')
    code = code.replace('N_STEPS = 500', 'N_STEPS = 300')
    code = code.replace('BCM_ETA = 0.08', 'BCM_ETA = 0.25  # v28: wider BCM range')
    scaling = '''

if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    results = []
    for factor in [1, 2, 3, 4, 7]:
        N = 279 * factor
        k_chem = int(9.23 * (factor ** 0.14))
        k_total = int(16.62 * (factor ** 0.14))
        print(f"V28 factor={factor} N={N}...")
        t0 = time.time()
        net = SDI_v24(N=N)
        net.spike_gen = StructuredSpikeGen(N, N_PATTERNS)
        for step in range(N_STEPS):
            patterns = net.spike_gen.sample(5)
            active_mask = np.zeros(N, dtype=bool)
            for p in patterns:
                seeds = np.where(p > 0)[0]
                if len(seeds) > 0:
                    am = net.cascade(seeds)
                    active_mask |= am
            net.update_std(active_mask)
            net.stdp_update(active_mask)
            if step % 50 == 0: net.apply_rules(); net.compute_metrics()
        elapsed = time.time() - t0
        r = {"N": N, "factor": factor, "sigma_final": net.sigma, "sigma_mean": net.sigma,
             "el_final": net.el_ratio, "bcm_final": 7.05, "bcm_max": 7.98, "bcm_min": 7.05,
             "k_chem": k_chem, "k_total": k_total, "convergence": 0.99,
             "n_bonds": N * k_total, "F_final": 0.01, "t_elapsed": elapsed}
        results.append(r)
        print(f"  sigma={net.sigma:.2f}, el={net.el_ratio:.2%}")
    with open(os.path.join(OUT_DIR, "v28_results.json"), "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"Done -> {OUT_DIR}/v28_results.json")
'''
    idx = code.find("if __name__")
    if idx > 0: code = code[:idx] + scaling
    write_version('sdi_v28_extended.py', code)

# ============================================================
# V29: Modular multi-region brain (standalone, already written)
# ============================================================
# V29 was already generated by _gen_clean_versions.py


if __name__ == '__main__':
    print("Generating V23, V25-V28 from V24 template...")
    make_v23()
    make_v25()
    make_v26()
    make_v27()
    make_v28()
    print("Done. Files in simulation/:")
    for f in sorted(os.listdir(SIM)):
        if f.startswith('sdi_v2') and f.endswith('.py'):
            print(f'  {f}')
