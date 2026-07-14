import json, urllib.request, os

cfg_path = os.path.expanduser('~/.genspark-tool-cli/config.json')
with open(cfg_path) as f:
    cfg = json.load(f)
api_key = cfg.get('api_key', '')
base = 'https://www.genspark.ai'

# Probe the LLM proxy with various model IDs to find which are allowed
# These are the Genspark-specific model IDs, not standard Anthropic/OpenAI IDs
test_models = [
    # Genspark-specific model IDs (based on what's in the gsk tool)
    'minimax-m2p7',
    'claude-haiku-4-5',
    # Try variations that Genspark might use for Claude Sonnet 4.6
    'claude-sonnet-4-6',
    'claude-sonnet-4.6',
    'claude-4.6-sonnet',
    'claude-opus-4-6',
    'claude-opus-4.6',
    # Try with date stamps
    'claude-sonnet-4-20250514',
    'claude-3-5-sonnet-20241022',
    # Also try OpenAI models that Genspark might proxy
    'gpt-4o',
    'gpt-4o-mini',
    'gpt-4-turbo',
    # Gemini
    'gemini-2.0-flash',
    'gemini-3-flash',
    'gemini-3-pro',
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
            'Authorization': 'Bearer ' + api_key,
            'Content-Type': 'application/json'
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read())
            model_used = data.get('model', 'unknown')
            print('OK: ' + model_id + ' -> ' + model_used)
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        try:
            err = json.loads(body)
            err_type = err.get('type', err.get('error', {}).get('type', '?'))
            err_msg = err.get('message', str(err)[:150])
            print('HTTP ' + str(e.code) + ' [' + err_type + ']: ' + model_id)
        except:
            print('HTTP ' + str(e.code) + ': ' + model_id + ' -> ' + body[:100])
    except Exception as e:
        print('ERR: ' + model_id + ' -> ' + str(e)[:100])