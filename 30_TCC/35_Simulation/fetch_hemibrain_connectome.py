#!/usr/bin/env python3
"""
最终版：拉取 Hemibrain 全脑中高度连接神经元的真实突触连接矩阵
策略：pre>20 AND post>20，约46K神经元，保留全脑hub拓扑
分批拉取，每批2000神经元，min_total_weight=3过滤噪声
"""
import json, time, pandas as pd
from neuprint import Client, fetch_neurons, fetch_adjacencies, NeuronCriteria as NC

TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InFpbnJhbmdsaXVAZ21haWwuY29tIiwibGV2ZWwiOiJub2F1dGgiLCJpbWFnZS11cmwiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NLWUdKRkJ3Y3gxMWwzTjVUZHdSRWhMZkJ5aVBYazFoZXd1OTRZQ0l1ZElETmsxYkE9czk2LWM_c3o9NTA_c3o9NTAiLCJleHAiOjE5NTgxNjY4NTB9.n_x-lQSyXa4a6LoKY40bSnT4yyVopZsbVg18aT0_5PA'
OUT = '/home/work/.openclaw/workspace/sdi_sim/hemibrain_real_connectome_v2.json'
LOG = '/home/work/.openclaw/workspace/sdi_sim/fetch_log_v2.txt'

c = Client('neuprint.janelia.org', dataset='hemibrain:v1.2.1', token=TOKEN)
print(f'Connected: {c.fetch_version()}', flush=True)

# 获取全脑中高度连接神经元
print('Fetching neurons (pre>20, post>20)...', flush=True)
t0 = time.time()
df, _ = fetch_neurons(NC(status='Traced', min_pre=20, min_post=20), client=c)
core_bodies = df['bodyId'].tolist()
print(f'N={len(core_bodies)} neurons ({time.time()-t0:.1f}s)', flush=True)

# 分批拉取连接
print('\nFetching adjacencies in batches (min_total_weight=3)...', flush=True)
BATCH = 2000
edges_all = []
t0 = time.time()

for i in range(0, len(core_bodies), BATCH):
    batch = core_bodies[i:i+BATCH]
    bno = i//BATCH+1
    total_batches = (len(core_bodies)-1)//BATCH+1
    print(f'  [{bno}/{total_batches}] {len(batch)} neurons...', end=' ', flush=True)
    try:
        _, conn_df = fetch_adjacencies(batch, batch, min_total_weight=3, client=c)
        agg = conn_df.groupby(['bodyId_pre','bodyId_post'])['weight'].sum().reset_index()
        eb = agg.values.tolist()
        edges_all.extend(eb)
        elapsed = time.time()-t0
        print(f'{len(eb)} edges | total={len(edges_all)} | {elapsed:.0f}s', flush=True)
    except Exception as e:
        print(f'ERR: {e}', flush=True)
    time.sleep(0.5)

print(f'\nFetch done: {len(edges_all)} edges in {time.time()-t0:.1f}s', flush=True)

# 构建索引映射
b2i = {int(b): i for i, b in enumerate(core_bodies)}
valid = []
for row in edges_all:
    s, t, w = int(row[0]), int(row[1]), int(row[2])
    if s in b2i and t in b2i:
        valid.append([b2i[s], b2i[t], w])

print(f'Valid edges (both endpoints in set): {len(valid)}', flush=True)

# 神经元类型信息
meta = []
for _, row in df.iterrows():
    meta.append({
        'bodyId': int(row['bodyId']),
        'type': str(row.get('type','')) if 'type' in row.index and pd.notna(row.get('type')) else '',
        'instance': str(row.get('instance','')) if 'instance' in row.index and pd.notna(row.get('instance')) else ''
    })

result = {
    'N': len(core_bodies),
    'n_edges': len(valid),
    'edges': valid,
    'body_ids': [int(b) for b in core_bodies],
    'neuron_meta': meta[:5000],  # 只存前5000条meta避免文件太大
    'dataset': 'hemibrain:v1.2.1',
    'filter': 'pre>20 AND post>20 (all brain regions)',
    'min_total_weight': 3,
}
with open(OUT, 'w') as f:
    json.dump(result, f)
print(f'Saved → {OUT}')
print('DONE')
