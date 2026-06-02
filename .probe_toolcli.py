import json, urllib.request, os

cfg_path = os.path.expanduser('~/.genspark-tool-cli/config.json')
with open(cfg_path) as f:
    cfg = json.load(f)
api_key = cfg.get('api_key', '')
base = 'https://www.genspark.ai'

# Probe /api/tool_cli/ endpoints
endpoints = [
    ('GET', '/api/tool_cli/models'),
    ('GET', '/api/tool_cli/available_models'),
    ('GET', '/api/tool_cli/llm_models'),
    ('POST', '/api/tool_cli/models'),
    ('POST', '/api/tool_cli/llm_models'),
]

for method, ep in endpoints:
    req = urllib.request.Request(
        base + ep,
        headers={'Authorization': 'Bearer ' + api_key}
    )
    req.get_method = lambda m=method: m
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            print('OK', method, ep + ':', json.dumps(data)[:500])
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print('HTTP', method, ep, e.code, ':', body[:150])
    except Exception as e:
        print('ERR', method, ep + ':', str(e)[:100])