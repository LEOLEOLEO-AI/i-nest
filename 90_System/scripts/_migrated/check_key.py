import json, os

with open(os.path.expanduser('~/.genspark-tool-cli/config.json')) as f:
    d = json.load(f)
key = d.get('api_key', '')
print('GSK CLI key starts with:', key[:40])
print('Starts with gsk-:', key.startswith('gsk-'))
print('Length:', len(key))

# Now check openclaw env
with open('/home/work/.openclaw/openclaw.json') as f:
    raw = f.read()
data = json.loads(raw)
env = data.get('env', {}).get('vars', {})
ant_base = env.get('ANTHROPIC_BASE_URL', '')
ant_key = env.get('ANTHROPIC_API_KEY', '')
print('OpenClaw ANTHROPIC_BASE_URL:', ant_base)
print('OpenClaw ANTHROPIC_API_KEY starts with:', ant_key[:30] if ant_key else 'EMPTY')
print('Starts with gsk-:', ant_key.startswith('gsk-') if ant_key else False)
print('Length:', len(ant_key) if ant_key else 0)