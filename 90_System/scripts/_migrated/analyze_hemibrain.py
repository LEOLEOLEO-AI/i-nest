import json, csv, sys

# Read the v31 results
with open('/home/work/.openclaw/workspace/sdi_sim/sdi_v31_results.json') as f:
    d = json.load(f)
print('v31 results keys:', list(d.keys()))
for k, v in d.items():
    sigma = v.get('sigma', '?')
    alpha = v.get('alpha', '?')
    el = v.get('el_ratio_final', '?')
    C = v.get('C', '?')
    L = v.get('L', '?')
    print(f'  {k}: sigma={sigma}, alpha={alpha}, EL={el}, C={C}, L={L}')

# Read the hemibrain meta CSV
neurons = {}
with open('/home/work/.openclaw/workspace/10_Knowledge/专题归档/05_Datasets_仿真与实验数据/Simulation_Results/hemibrain_meta.csv') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        body_id = row[0]
        try:
            pre = float(row[11]) if row[11] else 0.0
        except:
            pre = 0.0
        try:
            post = float(row[12]) if row[12] else 0.0
        except:
            post = 0.0
        cell_class = row[4] or 'unknown'
        
        if body_id not in neurons:
            neurons[body_id] = {'pre': 0.0, 'post': 0.0, 'class': cell_class, 
                               'type': row[2], 'instance': row[1]}
        neurons[body_id]['pre'] += pre
        neurons[body_id]['post'] += post

print(f'\nHemibrain: {len(neurons)} unique neurons')
print(f'Total pre sites: {sum(v[\"pre\"] for v in neurons.values()):.0f}')
print(f'Total post sites: {sum(v[\"post\"] for v in neurons.values()):.0f}')

# Cell class distribution
from collections import Counter
classes = Counter(v['class'] for v in neurons.values())
print(f'\nCell classes:')
for k, v in classes.most_common():
    print(f'  {k}: {v}')

# Estimate connectivity (pre/post ≈ number of outputs/inputs)
# For a directed network, we need pre->post connections
# Each pre site connects to multiple post sites of downstream neurons

# Build edges from hemibrain meta: we have neuron types and their connectivity profiles
# But we don't have actual edge lists from the CSV alone.
# We need to use the neuprint API or a pre-existing edges file.

# Check if there's a hemibrain edges file anywhere
import os
for root, dirs, files in os.walk('/home/work/.openclaw/workspace/'):
    for fname in files:
        if 'hemibrain' in fname.lower() and fname.endswith('.json'):
            fpath = os.path.join(root, fname)
            size = os.path.getsize(fpath)
            print(f'Found: {fpath} ({size/1024:.1f} KB)')
            if size > 1000:
                with open(fpath) as f:
                    content = f.read()[:500]
                    print(f'  Preview: {content[:300]}...')

print('\nDone analysis.')