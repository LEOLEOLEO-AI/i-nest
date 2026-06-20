import json, urllib.request, os

# Get the API key
cfg_path = os.path.expanduser('~/.genspark-tool-cli/config.json')
with open(cfg_path) as f:
    cfg = json.load(f)
api_key = cfg.get('api_key', '')

# Try the models endpoint
req = urllib.request.Request(
    'https://www.genspark.ai/api/llm_proxy/v1/models',
    headers={'Authorization': f'Bearer {api_key}'}
)
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        data = json.loads(resp.read())
        print(json.dumps(data, indent=2))
except Exception as e:
    print('Error:', e)
    
# Also try the anthropic models endpoint
req2 = urllib.request.Request(
    'https://www.genspark.ai/api/anthropic/v1/models',
    headers={'Authorization': f'Bearer {api_key}'}
)
try:
    with urllib.request.urlopen(req2, timeout=10) as resp:
        data = json.loads(resp.read())
        print(json.dumps(data, indent=2))
except Exception as e:
    print('Anthropic endpoint error:', e)