import json, urllib.request, os, subprocess

cfg_path = os.path.expanduser('~/.genspark-tool-cli/config.json')
with open(cfg_path) as f:
    cfg = json.load(f)
api_key = cfg.get('api_key', '')
base = 'https://www.genspark.ai'

# Try chat completions endpoint with a models probe
# OpenAI compatible endpoint often supports GET /models
for ep in [
    '/api/llm_proxy/v1/models',
    '/api/llm_proxy/models',
    '/v1/models',
    '/models',
]:
    req = urllib.request.Request(
        base + ep,
        headers={'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read())
            print('SUCCESS', ep, ':', json.dumps(data)[:1000])
    except Exception as e:
        print('FAIL', ep, ':', str(e)[:200])

# Try the completions endpoint with a special request
for ep in [
    '/api/llm_proxy/v1/chat/completions',
    '/api/anthropic/v1/messages',
]:
    req = urllib.request.Request(
        base + ep,
        data=json.dumps({'model': 'test', 'messages': [{'role': 'user', 'content': 'hi'}]}).encode(),
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            print('SUCCESS', ep, ':', resp.status, resp.headers.get('openai-model', 'no-model-header'))
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:300]
        print('HTTP', ep, ':', e.code, body[:200])
    except Exception as e:
        print('ERR', ep, ':', str(e)[:200])