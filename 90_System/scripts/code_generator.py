# -*- coding: utf-8 -*-
\"\"\"
代码生成器模块 - CodeGenerator
根据灵感生成工程代码
\"\"\"

import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

logger = logging.getLogger('code_generator')


class CodeGenerator:
    def __init__(self, config):
        self.config = config
        self.base_dir = Path(__file__).parent.parent
        self.code_dir = self.base_dir / 'code_generator' / 'projects'
        self.code_dir.mkdir(parents=True, exist_ok=True)

    def generate_project(self, idea_title: str, direction: str = 'iNEST') -> Dict:
        \"\"\"根据灵感生成完整项目\"\"\"
        project_name = idea_title[:50].replace(' ', '_').replace('/', '_')
        project_dir = self.code_dir / direction / project_name
        project_dir.mkdir(parents=True, exist_ok=True)

        # 创建项目结构
        files = {
            'README.md': self._readme_template(project_name, direction, idea_title),
            'main.py': self._main_template(project_name),
            'config.py': self._config_template(direction),
            'requirements.txt': f'# Project: {project_name}\n# Direction: {direction}\nnetworkx>=3.1\nnumpy>=1.24.0\nscipy>=1.10.0\nmatplotlib>=3.7.0\n',
            'tests/test_main.py': self._test_template(project_name),
        }

        for filename, content in files.items():
            file_path = project_dir / filename
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding='utf-8')

        return {
            'project_name': project_name,
            'project_dir': str(project_dir),
            'direction': direction,
            'created_at': datetime.now().isoformat(),
        }

    def _readme_template(self, name: str, direction: str, idea: str) -> str:
        return f'''# {name}

**方向:** {direction}
**灵感来源:** {idea}
**创建时间:** {datetime.now().strftime('%Y-%m-%d')}

## 概述

本项目基于 {direction} 方向的研究灵感自动生成。

## 安装

`ash
pip install -r requirements.txt
`

## 使用

`ash
python main.py
`

## 测试

`ash
python -m pytest tests/
`

## 目录结构

`
{direction}/
├── README.md
├── main.py
├── config.py
├── requirements.txt
└── tests/
    └── test_main.py
`
'''

    def _main_template(self, name: str) -> str:
        return f'''# -*- coding: utf-8 -*-
\"\"\"
{name} - 主程序
\"\"\"

import logging
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    config = Config()
    logger.info(\"Starting {name}\")

    # TODO: Implement core logic

    logger.info(\"Done\")


if __name__ == '__main__':
    main()
'''

    def _config_template(self, direction: str) -> str:
        return f'''# -*- coding: utf-8 -*-
\"\"\"
{direction} 配置
\"\"\"

class Config:
    DIRECTION = \"{direction}\"

    # Simulation parameters
    MAX_ITERATIONS = 1000
    POPULATION_SIZE = 100
    MUTATION_RATE = 0.01
'''

    def _test_template(self, name: str) -> str:
        return f'''# -*- coding: utf-8 -*-
\"\"\"
{name} - 测试
\"\"\"

def test_main():
    assert True  # Placeholder
'''

    def list_projects(self) -> List[Dict]:
        projects = []
        for d in self.code_dir.iterdir():
            if d.is_dir():
                for proj in d.iterdir():
                    if proj.is_dir():
                        readme = proj / 'README.md'
                        projects.append({
                            'name': proj.name,
                            'path': str(proj),
                            'direction': d.name,
                        })
        return projects
