import json, urllib.request, os

cfg_path = os.path.expanduser('~/.genspark-tool-cli/config.json')
with open(cfg_path) as f:
    cfg = json.load(f)
api_key = cfg.get('api_key', '')
base = 'https://www.genspark.ai'

# Try various endpoints
endpoints = [
    '/api/llm_proxy/v1/models',
    '/api/anthropic/v1/models',
    '/api/v1/models',
    '/api/models',
    '/api/llm/models',
    '/api/proxy/models',
    '/api/tools/models',
]

for ep in endpoints:
    req = urllib.request.Request(
        base + ep,
        headers={'Authorization': f'Bearer {api_key}'}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            print(f'SUCCESS {ep}:', json.dumps(data)[:500])
    except Exception as e:
        print(f'FAIL {ep}: {e}')

# Also try without auth
for ep in endpoints:
    req = urllib.request.Request(base + ep)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            print(f'PUBLIC {ep}:', json.dumps(data)[:500])
    except Exception as e:
        print(f'PUBLIC_FAIL {ep}: {e}')