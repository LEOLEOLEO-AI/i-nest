# -*- coding: utf-8 -*-
\"\"\"
智能体技能安装脚本
\"\"\"

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from scripts.agent_skills import AgentSkills

def main():
    # 加载配置
    import json
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    skills = AgentSkills(config)

    print('可用技能:')
    for s in skills.list_available():
        print(f'  [{s["id"]}] {s["name"]} - {s["description"]}')

    print('\\n安装所有技能...')
    for s in skills.list_available():
        result = skills.install_skill(s['id'])
        print(f'  [{result["status"]}] {s["name"]}')

    print('\\n已安装技能:')
    for s in skills.list_installed():
        print(f'  [installed] {s["name"]} v{s["version"]}')

if __name__ == '__main__':
    main()
