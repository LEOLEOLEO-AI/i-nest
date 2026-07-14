import json, os
base = r'D:\Obsidian\home\work\.openclaw\workspace\simulation\data'

for vname, fname in [
    ('V22', 'v22_results/v22_results.json'),
    ('V23', 'v23_results/v23_results.json'),
    ('V25', 'v25_results/v25_results.json'),
    ('V26', 'v26_results/v26_scaling_results.json'),
    ('V27', 'v27_results/v27_results.json'),
    ('V28', 'v28_results/v28_results.json'),
]:
    p = os.path.join(base, fname)
    if os.path.exists(p):
        d = json.load(open(p, 'r', encoding='utf-8'))
        print(f'=== {vname} ===')
        if isinstance(d, dict):
            if 'final' in d:
                f = d['final']
                print(f'  final: sigma={f.get("sigma","?")}, el={f.get("el_ratio","?")}, alpha={f.get("alpha","?")}')
            for k in ['sigma_final','el_final_pct','F_final','FEP_convergence','BCM_theta_mean','consolidate_rate_final']:
                if k in d: print(f'  {k}: {d[k]}')
            if 'logs' in d and isinstance(d['logs'], list):
                logs = d['logs']
                step = max(1, len(logs)//4)
                for i in range(0, min(len(logs), step*4), step):
                    l = logs[i]
                    if isinstance(l, dict):
                        print(f'    step={l.get("step","?")} sigma={l.get("sigma","?"):.2f} el={l.get("el_ratio","?"):.3f}' if isinstance(l.get("sigma"), (int,float)) else f'    {list(l.keys())[:4]}')
        elif isinstance(d, list):
            for r in d:
                keys = [k for k in r.keys() if k not in ('logs','history')]
                vals = {k: round(r[k],2) if isinstance(r[k],float) else r[k] for k in keys}
                print(f'  {vals}')
    print('---')
