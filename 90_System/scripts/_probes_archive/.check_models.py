import json
with open('/home/work/.openclaw/openclaw.json') as f:
    data = json.load(f)
providers = data.get('models', {}).get('providers', {})
for name, cfg in providers.items():
    print('Provider:', name)
    print('  baseUrl:', cfg.get('baseUrl', 'N/A'))
    print('  api:', cfg.get('api', 'N/A'))
    models = cfg.get('models', [])
    for m in models:
        print('  -', m.get('id'), '|', m.get('name'), '| context:', m.get('contextWindow'), '| reasoning:', m.get('reasoning'))

# Also check env vars for model configs
env = data.get('env', {}).get('vars', {})
for k, v in env.items():
    if 'model' in k.lower() or 'claude' in k.lower() or 'anthropic' in k.lower():
        print(k, '=', v[:20] + '...' if len(str(v)) > 20 else v)