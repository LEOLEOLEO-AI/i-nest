# -*- coding: utf-8 -*-
"""
进度报告模块 - ProgressReport
生成每日/每周进度报告
"""

import json
import logging
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List

logger = logging.getLogger('progress_report')


class ProgressReport:
    def __init__(self, config):
        self.config = config
        self.base_dir = Path(__file__).parent.parent
        self.reports_dir = self.base_dir / 'reports'
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def generate_daily(self):
        logger.info('生成每日进度报告...')
        report = self._collect_metrics()
        report['generated_at'] = datetime.now().isoformat()
        report['report_type'] = 'daily'

        date_str = datetime.now().strftime('%Y%m%d')
        report_file = self.reports_dir / f'daily_report_{date_str}.md'
        report_file.write_text(self._format_report(report), encoding='utf-8')

        # 同时生成 JSON 供看盘使用
        json_file = self.reports_dir / f'daily_report_{date_str}.json'
        json_file.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')

        logger.info(f'进度报告已生成: {report_file}')

    def _collect_metrics(self) -> Dict:
        metrics = {
            'papers': {},
            'insights': 0,
            'sync_status': {},
            'code_commits_last_7d': 0,
        }

        # 论文统计
        papers_dir = self.base_dir / 'papers'
        papers_tcc = list(papers_dir.glob('TCC/**/*.md')) if papers_dir.exists() else []
        papers_inest = list(papers_dir.glob('iNEST/**/*.md')) if papers_dir.exists() else []

        metrics['papers'] = {
            'TCC': len(papers_tcc),
            'iNEST': len(papers_inest),
            'total': len(papers_tcc) + len(papers_inest),
        }

        # 灵感统计
        inspo_dir = self.base_dir / 'inspiration_engine'
        inspo_index = inspo_dir / 'index.json'
        if inspo_index.exists():
            with open(inspo_index, 'r', encoding='utf-8') as f:
                inspo_data = json.load(f)
                metrics['insights'] = len(inspo_data.get('insights', []))

        # 同步状态
        sync_log = self.base_dir / 'logs' / 'sync.log'
        if sync_log.exists():
            with open(sync_log, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if lines:
                    last_sync = json.loads(lines[-1])
                    metrics['sync_status'] = last_sync.get('results', {})

        # 代码提交统计
        try:
            result = subprocess.run(
                ['git', '-C', str(self.base_dir), 'log', '--oneline', '--since=7.days'],
                capture_output=True, text=True
            )
            if result.stdout.strip():
                metrics['code_commits_last_7d'] = len(result.stdout.strip().split('\n'))
        except Exception:
            pass

        return metrics

    def _format_report(self, report: Dict) -> str:
        lines = [
            '# TCC-iNEST 研究平台每日进度报告',
            f'**生成时间:** {report.get("generated_at", "N/A")}',
            '',
            '## 总体概览',
            '',
            '| 指标 | 数值 |',
            '|------|------|',
        ]

        papers = report.get('papers', {})
        lines.append(f'| 论文总数 | {papers.get("total", 0)} |')
        lines.append(f'| TCC 方向 | {papers.get("TCC", 0)} |')
        lines.append(f'| iNEST 方向 | {papers.get("iNEST", 0)} |')
        lines.append(f'| 灵感数量 | {report.get("insights", 0)} |')
        lines.append(f'| 代码提交(近7天) | {report.get("code_commits_last_7d", 0)} |')

        lines.extend([
            '',
            '## TCC 方向',
            '',
            '- 论文: 进行中',
            '- 专利: 待分配',
            '- 代码开发: 待分配',
            '',
            '## iNEST 方向',
            '',
            '- 论文: 进行中',
            '- 专利: 待分配',
            '- 代码开发: 待分配',
            '',
            '## 今日待办',
            '',
            '- [ ] 检查新导入论文',
            '- [ ] 审阅生成的灵感',
            '- [ ] 更新知识图谱',
            '- [ ] 同步到 Gitee',
            '',
        ])

        return '\n'.join(lines)
