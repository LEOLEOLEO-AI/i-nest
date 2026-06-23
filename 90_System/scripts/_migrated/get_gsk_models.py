import json, urllib.request, os, subprocess

# Get the API key
cfg_path = os.path.expanduser('~/.genspark-tool-cli/config.json')
with open(cfg_path) as f:
    cfg = json.load(f)
api_key = cfg.get('api_key', '')

# Call gsk list-tools with debug to see what it uses
result = subprocess.run(
    ['gsk', 'list-tools', '--debug', '--output', 'json'],
    capture_output=True, text=True, timeout=30,
    env={**os.environ, 'GSK_API_KEY': api_key}
)
print('STDOUT:', result.stdout[:500])
print('STDERR:', result.stderr[:500])

# Check the tools cache for model info
cache_path = os.path.expanduser('~/.genspark-tool-cli/tools-cache.json')
if os.path.exists(cache_path):
    with open(cache_path) as f:
        cache = json.load(f)
    print('\nTools cache keys:', list(cache.keys())[:20])
    # Check for any model/provider info
    tools = cache.get('tools', cache.get('data', []))
    if isinstance(tools, list):
        print('Number of tools:', len(tools))
        for t in tools[:5]:
            print(' -', t.get('name') if isinstance(t, dict) else t)