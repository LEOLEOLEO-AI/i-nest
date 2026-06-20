# -*- coding: utf-8 -*-
"""
调度器模块 - Scheduler
定时触发各项研究任务
"""

import logging
import time
import schedule
from pathlib import Path

logger = logging.getLogger('scheduler')


class Scheduler:
    def __init__(self, config):
        self.config = config
        self.base_dir = Path(__file__).parent.parent
        self.running = False

    def run(self):
        logger.info('启动调度器...')
        self.running = True

        # 每日论文抓取
        cron = self.config['paper_search']['daily_cron']
        schedule.every().day.at(cron).do(self._daily_paper_scrape)

        # 每小时知识图谱更新
        schedule.every().hour.do(self._hourly_kg_update)

        # 每日灵感生成
        schedule.every().day.at('10:00').do(self._daily_insights)

        # 每30分钟同步
        interval = self.config['sync'].get('sync_interval_minutes', 30)
        schedule.every(interval).minutes.do(self._sync)

        # 每日进度报告
        schedule.every().day.at('18:00').do(self._daily_report)

        logger.info(f'调度器已启动: 论文抓取={cron}, 灵感生成=10:00, 同步={interval}分钟')

        while self.running:
            schedule.run_pending()
            time.sleep(60)

    def stop(self):
        self.running = False
        logger.info('调度器已停止')

    def _daily_paper_scrape(self):
        logger.info('触发每日论文抓取...')
        from scripts.paper_scraper import PaperScraper
        scraper = PaperScraper(self.config)
        scraper.run_daily()

    def _hourly_kg_update(self):
        logger.info('触发知识图谱更新...')
        from scripts.knowledge_graph import KnowledgeGraph
        kg = KnowledgeGraph(self.config)
        kg.update()

    def _daily_insights(self):
        logger.info('触发灵感生成...')
        from scripts.inspiration_engine import InspirationEngine
        engine = InspirationEngine(self.config)
        engine.generate_all()

    def _sync(self):
        logger.info('触发同步...')
        from scripts.sync_manager import SyncManager
        sm = SyncManager(self.config)
        sm.sync_all()

    def _daily_report(self):
        logger.info('触发每日进度报告...')
        from scripts.progress_report import ProgressReport
        report = ProgressReport(self.config)
        report.generate_daily()
