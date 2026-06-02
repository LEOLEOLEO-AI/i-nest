# -*- coding: utf-8 -*-
\"\"\"
平台初始化脚本
创建必要的目录结构和配置文件
\"\"\"

import os
from pathlib import Path

BASE = Path(__file__).parent

def setup():
    dirs = [
        'papers/TCC', 'papers/iNEST',
        'papers/archive',
        'knowledge_graph/neo4j_data',
        'inspiration_engine',
        'reports',
        'code_generator/projects',
        'auto_verify/codes', 'auto_verify/simulations',
        'agent_skills/installed',
        'logs',
    ]

    for d in dirs:
        (BASE / d).mkdir(parents=True, exist_ok=True)
        print(f'  [mkdir] {d}')

    # 创建 .gitignore
    gitignore = '''# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.eggs/
*.egg

# Virtual env
venv/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
logs/*.log

# Data
papers/*.json
knowledge_graph/neo4j_data/graph.db/
'''
    (BASE / '.gitignore').write_text(gitignore, encoding='utf-8')
    print('  [.gitignore] created')
    print('\\n平台初始化完成！')
    print('下一步: pip install -r requirements.txt')

if __name__ == '__main__':
    setup()
