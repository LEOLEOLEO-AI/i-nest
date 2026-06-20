import json, urllib.request, os

cfg_path = os.path.expanduser('~/.genspark-tool-cli/config.json')
with open(cfg_path) as f:
    cfg = json.load(f)
api_key = cfg.get('api_key', '')
base = 'https://www.genspark.ai'

models_to_try = [
    'claude-sonnet-4-20250514',
    'claude-3-5-sonnet-20241022',
    'claude-3-7-sonnet-20250514',
    'claude-sonnet-4-6-20250514',
    'claude-3-5-haiku-20241022',
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
            'Authorization': 'Bearer ' + api_key,
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01'
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())
            result_model = data.get('model', 'unknown')
            print('OK: ' + model + ' -> ' + result_model)
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            err = json.loads(body)
            err_msg = err.get('error', err.get('type', '?'))
            print('FAIL ' + model + ': ' + str(e.code) + ' - ' + str(err_msg)[:100])
        except:
            print('FAIL ' + model + ': ' + str(e.code) + ' - ' + body[:100])
    except Exception as e:
        print('ERR ' + model + ': ' + str(e)[:100])