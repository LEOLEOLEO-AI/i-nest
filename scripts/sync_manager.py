# -*- coding: utf-8 -*-
"""
同步管理器模块 - SyncManager
管理 Obsidian、Gitee、Genspark 之间的双向同步
"""

import logging
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional

logger = logging.getLogger('sync_manager')


class SyncManager:
    def __init__(self, config):
        self.config = config
        self.base_dir = Path(__file__).parent.parent
        self.obsidian_path = Path(config['sync']['obsidian_path'])
        self.gitee_repo = config['sync']['gitee_repo']
        self.sync_log = self.base_dir / 'logs' / 'sync.log'
        self.sync_log.parent.mkdir(parents=True, exist_ok=True)

    def sync_all(self):
        logger.info('开始全量同步...')
        results = {}

        # 1. 从 Gitee 拉取
        results['pull_gitee'] = self.pull_from_gitee()

        # 2. 同步到 Obsidian
        results['to_obsidian'] = self.sync_to_obsidian()

        # 3. 从 Obsidian 拉取
        results['from_obsidian'] = self.sync_from_obsidian()

        # 4. 推送到 Gitee
        results['push_gitee'] = self.push_to_gitee()

        # 记录同步日志
        self._log_sync(results)
        logger.info(f'同步完成: {json.dumps(results, ensure_ascii=False)}')

    def pull_from_gitee(self) -> dict:
        try:
            repo_dir = self.base_dir
            subprocess.run(
                ['git', '-C', str(repo_dir), 'pull', 'origin', 'main'],
                capture_output=True, text=True, timeout=60
            )
            return {'status': 'success', 'message': '从 Gitee 拉取成功'}
        except subprocess.TimeoutExpired:
            return {'status': 'timeout', 'message': 'Gitee 拉取超时'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def push_to_gitee(self) -> dict:
        try:
            repo_dir = self.base_dir

            # 添加所有变更
            subprocess.run(
                ['git', '-C', str(repo_dir), 'add', '-A'],
                capture_output=True, text=True, timeout=30
            )

            # 检查是否有变更
            status = subprocess.run(
                ['git', '-C', str(repo_dir), 'status', '--porcelain'],
                capture_output=True, text=True, timeout=30
            )
            if not status.stdout.strip():
                return {'status': 'no_changes', 'message': '无变更需要推送'}

            # 提交
            commit_msg = f'Auto sync: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
            subprocess.run(
                ['git', '-C', str(repo_dir), 'commit', '-m', commit_msg],
                capture_output=True, text=True, timeout=30
            )

            # 推送
            subprocess.run(
                ['git', '-C', str(repo_dir), 'push', 'origin', 'main'],
                capture_output=True, text=True, timeout=60
            )

            return {'status': 'success', 'message': '推送到 Gitee 成功'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def sync_to_obsidian(self) -> dict:
        if not self.obsidian_path.exists():
            return {'status': 'skipped', 'message': 'Obsidian 路径不存在'}

        try:
            import shutil
            for subdir in ['papers', 'knowledge_graph']:
                src = self.base_dir / subdir
                dst = self.obsidian_path / subdir
                if src.exists():
                    shutil.copytree(str(src), str(dst), dirs_exist_ok=True)

            return {'status': 'success', 'message': '同步到 Obsidian 成功'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def sync_from_obsidian(self) -> dict:
        if not self.obsidian_path.exists():
            return {'status': 'skipped', 'message': 'Obsidian 路径不存在'}

        try:
            import shutil
            obsidian_files = self.obsidian_path.glob('**/*.md')
            count = 0
            for md_file in obsidian_files:
                relative = md_file.relative_to(self.obsidian_path)
                dst = self.base_dir / 'obsidian_sync' / relative
                dst.parent.mkdir(parents=True, exist_ok=True)
                if md_file != dst:
                    shutil.copy2(str(md_file), str(dst))
                    count += 1

            return {'status': 'success', 'message': f'从 Obsidian 拉取 {count} 个文件'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def _log_sync(self, results: dict):
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'results': results,
        }
        with open(self.sync_log, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
