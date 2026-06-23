import json, urllib.request, os

# Get the ANTHROPIC_API_KEY from openclaw config
with open('/home/work/.openclaw/openclaw.json') as f:
    data = json.load(f)
api_key = data['env']['vars']['ANTHROPIC_API_KEY']
base_url = data['env']['vars']['ANTHROPIC_BASE_URL']  # https://www.genspark.ai/api/anthropic

print('Testing Anthropic-compatible endpoint at:', base_url)
print('API key starts with:', api_key[:30])

# Try the messages endpoint with different model ID formats
models_to_try = [
    # Vertex format (what the built-in provider uses)
    'claude-sonnet-4-6',
    'claude-opus-4-6',
    # Standard Anthropic format
    'claude-3-5-sonnet-20241022',
    'claude-3-7-sonnet-20250514',
    'claude-4-sonnet-20250514',
    # Haiku
    'claude-3-5-haiku-20241022',
    # Opus
    'claude-4-opus-20250514',
]

for model in models_to_try:
    req = urllib.request.Request(
        base_url + '/messages',
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
            result = json.loads(resp.read())
            print('OK: ' + model + ' -> ' + result.get('model', '?'))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            err = json.loads(body)
            t = err.get('type', '?')
            msg = str(err.get('message', err.get('error', err)))[:100]
            print('FAIL ' + str(e.code) + ' [' + t + ']: ' + model)
        except:
            print('FAIL ' + str(e.code) + ': ' + model + ' -> ' + body[:80])
    except Exception as e:
        print('ERR: ' + model + ' -> ' + str(e)[:80])

# Also try with x-api-key header (some endpoints use this)
print('\n--- Trying x-api-key header ---')
for model in ['claude-sonnet-4-6', 'claude-3-5-sonnet-20241022']:
    req = urllib.request.Request(
        base_url + '/messages',
        data=json.dumps({
            'model': model,
            'messages': [{'role': 'user', 'content': 'hi'}],
            'max_tokens': 10
        }).encode(),
        headers={
            'x-api-key': api_key,
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01'
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            result = json.loads(resp.read())
            print('OK: ' + model + ' -> ' + result.get('model', '?'))
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            err = json.loads(body)
            t = err.get('type', '?')
            print('FAIL ' + str(e.code) + ' [' + t + ']: ' + model)
        except:
            print('FAIL ' + str(e.code) + ': ' + model)
    except Exception as e:
        print('ERR: ' + model + ' -> ' + str(e)[:80])