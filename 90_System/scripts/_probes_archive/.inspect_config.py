import json
with open('/home/work/.openclaw/openclaw.json') as f:
    data = json.load(f)

providers = data.get('models', {}).get('providers', {})
for name, cfg in providers.items():
    print('Provider:', name, '| api:', cfg.get('api'), '| baseUrl:', cfg.get('baseUrl', 'N/A'))
    for m in cfg.get('models', []):
        print('  -', m.get('id'), '|', m.get('name'), '| ctx:', m.get('contextWindow'), '| reasoning:', m.get('reasoning'))

print()
env = data.get('env', {}).get('vars', {})
for k in sorted(env.keys()):
    print(k)