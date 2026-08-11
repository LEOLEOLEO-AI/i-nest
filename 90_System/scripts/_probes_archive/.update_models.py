import json, re

path = '/home/work/.openclaw/openclaw.json'
with open(path) as f:
    content = f.read()

old_models = '''[
          {
            \"id\": \"minimax-m2p7\",
            \"name\": \"MiniMax M2.7\",
            \"reasoning\": false,
            \"input\": [
              \"text\"
            ],
            \"contextWindow\": 196608,
            \"maxTokens\": 16384,
            \"cost\": {
              \"input\": 0,
              \"output\": 0,
              \"cacheRead\": 0,
              \"cacheWrite\": 0
            },
            \"api\": \"openai-completions\"
          },
          {
            \"id\": \"claude-haiku-4-5\",
            \"name\": \"Claude Haiku 4.5\",
            \"reasoning\": false,
            \"input\": [
              \"text\",
              \"image\"
            ],
            \"contextWindow\": 200000,
            \"maxTokens\": 8192,
            \"cost\": {
              \"input\": 0,
              \"output\": 0,
              \"cacheRead\": 0,
              \"cacheWrite\": 0
            },
            \"api\": \"openai-completions\"
          }
        ]'''

new_models = '''[
          {
            \"id\": \"minimax-m2p7\",
            \"name\": \"MiniMax M2.7\",
            \"reasoning\": false,
            \"input\": [
              \"text\"
            ],
            \"contextWindow\": 196608,
            \"maxTokens\": 16384,
            \"cost\": {
              \"input\": 0,
              \"output\": 0,
              \"cacheRead\": 0,
              \"cacheWrite\": 0
            },
            \"api\": \"openai-completions\"
          },
          {
            \"id\": \"claude-haiku-4-5\",
            \"name\": \"Claude Haiku 4.5\",
            \"reasoning\": false,
            \"input\": [
              \"text\",
              \"image\"
            ],
            \"contextWindow\": 200000,
            \"maxTokens\": 8192,
            \"cost\": {
              \"input\": 0,
              \"output\": 0,
              \"cacheRead\": 0,
              \"cacheWrite\": 0
            },
            \"api\": \"openai-completions\"
          },
          {
            \"id\": \"claude-sonnet-4-6\",
            \"name\": \"Claude Sonnet 4.6\",
            \"reasoning\": false,
            \"input\": [
              \"text\",
              \"image\"
            ],
            \"contextWindow\": 200000,
            \"maxTokens\": 8192,
            \"cost\": {
              \"input\": 0,
              \"output\": 0,
              \"cacheRead\": 0,
              \"cacheWrite\": 0
            },
            \"api\": \"openai-completions\"
          },
          {
            \"id\": \"claude-opus-4-6\",
            \"name\": \"Claude Opus 4.6\",
            \"reasoning\": false,
            \"input\": [
              \"text\",
              \"image\"
            ],
            \"contextWindow\": 200000,
            \"maxTokens\": 8192,
            \"cost\": {
              \"input\": 0,
              \"output\": 0,
              \"cacheRead\": 0,
              \"cacheWrite\": 0
            },
            \"api\": \"openai-completions\"
          }
        ]'''

if old_models in content:
    new_content = content.replace(old_models, new_models, 1)
    with open(path, 'w') as f:
        f.write(new_content)
    print('Models updated successfully')
else:
    print('Could not find exact match, showing found content:')
    # Try to find the models array with flexible whitespace
    pattern = r'models.*?api.*?openai-completions.*?claude-haiku-4-5'
    m = re.search(pattern, content, re.DOTALL)
    if m:
        print('Found pattern at:', m.start(), m.end())
        print(repr(content[m.start():m.start()+500]))