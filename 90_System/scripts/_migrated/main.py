#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TCC-iNEST Research Platform - Main Scheduler
=============================================
统一调度中心：每天固定时间触发论文搜索、知识图谱更新、灵感生成、进度跟踪。

Usage:
    python main.py --start          # 启动调度器
    python main.py --paper-scrape    # 手动触发论文抓取
    python main.py --update-kg       # 手动更新知识图谱
    python main.py --generate-insight # 生成灵感
    python main.py --sync            # 手动触发同步
    python main.py --report          # 生成进度报告
"""

import argparse
import json
import logging
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(Path('logs/platform.log'), encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('platform')


def load_config():
    config_path = Path(__file__).parent / 'config.json'
    if not config_path.exists():
        logger.error('config.json not found')
        sys.exit(1)
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def start_scheduler(config):
    from scripts.scheduler import Scheduler
    scheduler = Scheduler(config)
    logger.info('启动主调度器...')
    scheduler.run()


def run_paper_scrape(config):
    from scripts.paper_scraper import PaperScraper
    scraper = PaperScraper(config)
    scraper.run_daily()


def update_knowledge_graph(config):
    from scripts.knowledge_graph import KnowledgeGraph
    kg = KnowledgeGraph(config)
    kg.update()


def generate_insights(config):
    from scripts.inspiration_engine import InspirationEngine
    engine = InspirationEngine(config)
    engine.generate_all()


def run_sync(config):
    from scripts.sync_manager import SyncManager
    sm = SyncManager(config)
    sm.sync_all()


def generate_report(config):
    from scripts.progress_report import ProgressReport
    report = ProgressReport(config)
    report.generate_daily()


def main():
    parser = argparse.ArgumentParser(description='TCC-iNEST Research Platform')
    parser.add_argument('--start', action='store_true', help='启动调度器')
    parser.add_argument('--paper-scrape', action='store_true', help='抓取论文')
    parser.add_argument('--update-kg', action='store_true', help='更新知识图谱')
    parser.add_argument('--generate-insight', action='store_true', help='生成灵感')
    parser.add_argument('--sync', action='store_true', help='触发同步')
    parser.add_argument('--report', action='store_true', help='生成进度报告')
    parser.add_argument('--setup', action='store_true', help='初始化平台')

    args = parser.parse_args()

    if not any([args.start, args.paper_scrape, args.update_kg,
                args.generate_insight, args.sync, args.report, args.setup]):
        parser.print_help()
        sys.exit(1)

    config = load_config()

    if args.start:
        start_scheduler(config)
    if args.paper_scrape:
        run_paper_scrape(config)
    if args.update_kg:
        update_knowledge_graph(config)
    if args.generate_insight:
        generate_insights(config)
    if args.sync:
        run_sync(config)
    if args.report:
        generate_report(config)
    if args.setup:
        logger.info('正在初始化平台...')
        logger.info('平台初始化完成！')


if __name__ == '__main__':
    main()
