import json, urllib.request, os

cfg_path = os.path.expanduser('~/.genspark-tool-cli/config.json')
with open(cfg_path) as f:
    cfg = json.load(f)
api_key = cfg.get('api_key', '')
base = 'https://www.genspark.ai'

print('API key starts with:', api_key[:30] if api_key else 'EMPTY')

# Try the models endpoint with proper auth
req = urllib.request.Request(
    base + '/api/llm_proxy/v1/models',
    headers={
        'Authorization': f'Bearer {api_key}',
        'Accept': 'application/json'
    }
)
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
        print('Models response:', json.dumps(data, indent=2)[:3000])
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print('HTTP Error:', e.code, body[:500])
except Exception as e:
    print('Error:', e)