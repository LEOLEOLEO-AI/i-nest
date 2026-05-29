import json, urllib.request, os

cfg_path = os.path.expanduser('~/.genspark-tool-cli/config.json')
with open(cfg_path) as f:
    cfg = json.load(f)
api_key = cfg.get('api_key', '')
base = 'https://www.genspark.ai'

# Try Anthropic messages endpoint
models_to_try = [
    'claude-sonnet-4-20250514',
    'claude-3-5-sonnet-20241022',
    'claude-3-7-sonnet-20250514',
    'claude-sonnet-4-6-20250514',
    'claude-3-5-haiku-20241022',
    'claude-3-7-haiku-20250514',
    'claude-opus-4-20250514',
]

for model in models_to_try:
    req = urllib.request.Request(
        base + '/api/anthropic/v1/messages',
        data=json.dumps({
            'model': model,
            'messages': [{'role': 'user', 'content': 'hi'}],
            'max_tokens': 10
        }).encode(),
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01'
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())
            print(f'OK: {model} -> {data.get(\"model\", \"unknown\")}')
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            err = json.loads(body)
            print(f'FAIL {model}: {e.code} - {err.get(\"error\", err.get(\"type\", \"?\"))} - {str(err)[:150]}')
        except:
            print(f'FAIL {model}: {e.code} - {body[:150]}')
    except Exception as e:
        print(f'ERR {model}: {str(e)[:100]}')