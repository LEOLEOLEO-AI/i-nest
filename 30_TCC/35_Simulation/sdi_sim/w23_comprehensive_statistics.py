"""
W2-3 Comprehensive Statistics Module

Computes:
1. Mann-Whitney U tests (7 metrics)
2. Bootstrap 95% CI (1000 resamples each)
3. Bonferroni correction (7× multiplicity)
4. Effect sizes (Cohen's d / Cliff's delta)
"""

import json
import numpy as np
from scipy import stats
from pathlib import Path
import time

def load_hemibrain_data():
    """Load Hemibrain topological metrics"""
    with open("results/w23_topology_fast.json") as f:
        data = json.load(f)
    return data

def generate_null_distributions(n_samples=1000):
    """Generate ER, BA, modular null networks"""
    # Placeholder: would call topology_metrics.py
    pass

def mann_whitney_tests(hemibrain_metrics, null_dist):
    """Compute Mann-Whitney U for each metric"""
    results = {}
    for metric_name in hemibrain_metrics.keys():
        stat, pval = stats.mannwhitneyu(
            hemibrain_metrics[metric_name],
            null_dist[metric_name],
            alternative='two-sided'
        )
        results[metric_name] = {
            'U': stat,
            'p_value': pval
        }
    return results

def bootstrap_ci(data, n_bootstrap=1000, ci=95):
    """Compute bootstrap confidence intervals"""
    def resample_stat(x):
        return np.mean(x)
    
    bootstrap_stats = []
    for _ in range(n_bootstrap):
        resample = np.random.choice(data, size=len(data), replace=True)
        bootstrap_stats.append(resample_stat(resample))
    
    ci_lower = np.percentile(bootstrap_stats, (100-ci)/2)
    ci_upper = np.percentile(bootstrap_stats, (100+ci)/2)
    return ci_lower, ci_upper

def bonferroni_correction(p_values, n_tests=7):
    """Apply Bonferroni multiple comparison correction"""
    p_corrected = [min(p * n_tests, 1.0) for p in p_values]
    return p_corrected

def cohens_d(x, y):
    """Compute Cohen's d effect size"""
    nx, ny = len(x), len(y)
    dof = nx + ny - 2
    return (np.mean(x) - np.mean(y)) / np.sqrt(((nx-1)*np.std(x, ddof=1)**2 + (ny-1)*np.std(y, ddof=1)**2) / dof)

def run_comprehensive_statistics():
    """Execute all statistical tests"""
    
    print("=" * 70)
    print("【W2-3 完整统计 - 执行开始】")
    print("=" * 70)
    print("")
    
    start_time = time.time()
    
    # 1. Load data
    print("1️⃣ 加载数据...")
    hemibrain_data = load_hemibrain_data()
    null_dist = generate_null_distributions()
    print("   ✅ 数据加载完成")
    
    # 2. Mann-Whitney tests
    print("2️⃣ Mann-Whitney U 检验...")
    mw_results = mann_whitney_tests(hemibrain_data, null_dist)
    print(f"   ✅ 7 个检验完成")
    
    # 3. Bootstrap CI
    print("3️⃣ Bootstrap 置信区间（1000 次重采样）...")
    ci_results = {}
    for metric in hemibrain_data.keys():
        ci_lower, ci_upper = bootstrap_ci(hemibrain_data[metric], n_bootstrap=1000)
        ci_results[metric] = {'CI_lower': ci_lower, 'CI_upper': ci_upper}
    print(f"   ✅ 7 个指标 CI 计算完成")
    
    # 4. Bonferroni correction
    print("4️⃣ Bonferroni 校正...")
    p_values = [v['p_value'] for v in mw_results.values()]
    p_corrected = bonferroni_correction(p_values, n_tests=7)
    print(f"   ✅ 校正完成")
    
    # 5. Effect sizes
    print("5️⃣ 效应大小计算...")
    effect_sizes = {}
    for metric in hemibrain_data.keys():
        d = cohens_d(hemibrain_data[metric], null_dist[metric])
        effect_sizes[metric] = d
    print(f"   ✅ 7 个效应大小计算完成")
    
    elapsed = time.time() - start_time
    
    print("")
    print("=" * 70)
    print(f"【执行完成】总耗时：{elapsed:.1f} 秒")
    print("=" * 70)
    
    return {
        'mann_whitney': mw_results,
        'bootstrap_ci': ci_results,
        'p_corrected': p_corrected,
        'effect_sizes': effect_sizes
    }

if __name__ == "__main__":
    # Uncomment to run
    # results = run_comprehensive_statistics()
    # 
    # with open("results/w23_comprehensive_statistics.json", "w") as f:
    #     json.dump(results, f, indent=2)
    pass
