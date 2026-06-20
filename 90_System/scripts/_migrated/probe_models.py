import json, urllib.request, os

cfg_path = os.path.expanduser('~/.genspark-tool-cli/config.json')
with open(cfg_path) as f:
    cfg = json.load(f)
api_key = cfg.get('api_key', '')
base = 'https://www.genspark.ai'

# Try to call chat completions with different model IDs to see which ones are available
# This is a live probe approach
test_models = [
    'claude-sonnet-4-5',
    'claude-sonnet-4-6',
    'claude-3.5-sonnet',
    'claude-3.7-sonnet',
    'claude-4-sonnet',
    'claude-sonnet-4',
    'claude-opus-4',
    'gpt-4.5',
    'gpt-4o',
    'gpt-4o-mini',
    'gemini-2.0-flash',
    'gemini-3-flash',
]

for model_id in test_models:
    req = urllib.request.Request(
        base + '/api/llm_proxy/v1/chat/completions',
        data=json.dumps({
            'model': model_id,
            'messages': [{'role': 'user', 'content': 'hi'}],
            'max_tokens': 5
        }).encode(),
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())
            model_used = data.get('model', 'unknown')
            print(f'OK: {model_id} -> {model_used}')
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:200]
        if e.code == 400:
            # Bad request means model might not exist or be accessible
            print(f'REJECTED: {model_id} (400)')
        elif e.code == 403:
            print(f'FORBIDDEN: {model_id}')
        elif e.code == 404:
            print(f'NOT_FOUND: {model_id}')
        else:
            print(f'HTTP {e.code}: {model_id} -> {body[:150]}')
    except Exception as e:
        print(f'ERR: {model_id} -> {str(e)[:100]}')