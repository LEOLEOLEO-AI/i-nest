#!/usr/bin/env python3
"""
v3：用 neuprint Cypher 直接查全脑边列表，避免批次截断问题。
策略：直接查 pre>20 AND post>20 的神经元之间所有连接，
weight 聚合到神经元对级别（不拆ROI）。
分页拉取，每次10万条。
"""
import json, time
from neuprint import Client

TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InFpbnJhbmdsaXVAZ21haWwuY29tIiwibGV2ZWwiOiJub2F1dGgiLCJpbWFnZS11cmwiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NLWUdKRkJ3Y3gxMWwzTjVUZHdSRWhMZkJ5aVBYazFoZXd1OTRZQ0l1ZElETmsxYkE9czk2LWM_c3o9NTA_c3o9NTAiLCJleHAiOjE5NTgxNjY4NTB9.n_x-lQSyXa4a6LoKY40bSnT4yyVopZsbVg18aT0_5PA'
OUT = '/home/work/.openclaw/workspace/sdi_sim/hemibrain_real_connectome_v3.json'

c = Client('neuprint.janelia.org', dataset='hemibrain:v1.2.1', token=TOKEN)
print(f'Connected: {c.fetch_version()}', flush=True)

# Cypher: 查 pre>20 AND post>20 神经元之间的连接，按神经元对聚合weight
# SKIP/LIMIT 分页
PAGE = 100000
skip = 0
all_edges = []
t0 = time.time()

print('Fetching edges via Cypher (paginated)...', flush=True)
while True:
    cypher = f"""
    MATCH (a:Neuron)-[c:ConnectsTo]->(b:Neuron)
    WHERE a.pre >= 20 AND a.post >= 20
      AND b.pre >= 20 AND b.post >= 20
      AND a.status = 'Traced' AND b.status = 'Traced'
      AND c.weight >= 3
    RETURN a.bodyId AS src, b.bodyId AS tgt, c.weight AS w
    SKIP {skip} LIMIT {PAGE}
    """
    result = c.fetch_custom(cypher)
    n = len(result)
    if n == 0:
        print(f'  No more results at skip={skip}', flush=True)
        break
    rows = result[['src','tgt','w']].values.tolist()
    all_edges.extend(rows)
    elapsed = time.time()-t0
    print(f'  skip={skip}: {n} rows | total={len(all_edges)} | {elapsed:.0f}s', flush=True)
    if n < PAGE:
        break
    skip += PAGE
    time.sleep(0.3)

print(f'\nTotal edges: {len(all_edges)} in {time.time()-t0:.1f}s', flush=True)

# 建立bodyId→idx映射
body_set = set()
for e in all_edges:
    body_set.add(int(e[0]))
    body_set.add(int(e[1]))
body_list = sorted(body_set)
b2i = {b: i for i, b in enumerate(body_list)}
N = len(body_list)
print(f'Unique neurons: {N}', flush=True)

valid = [[b2i[int(e[0])], b2i[int(e[1])], int(e[2])] for e in all_edges]

result = {
    'N': N,
    'n_edges': len(valid),
    'edges': valid,
    'body_ids': body_list,
    'dataset': 'hemibrain:v1.2.1',
    'filter': 'Traced, pre>=20, post>=20, weight>=3 (Cypher full-graph)',
    'min_weight': 3,
}
with open(OUT, 'w') as f:
    json.dump(result, f)
print(f'Saved → {OUT}')
print('DONE')
