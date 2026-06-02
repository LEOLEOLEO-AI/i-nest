# -*- coding: utf-8 -*-
\"\"\"
论文抓取模块 - PaperScraper
从 arXiv、IEEE、ACM、知网等源抓取论文，按 TCC/iNEST 方向分类
\"\"\"

import json
import logging
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional

import requests

logger = logging.getLogger('paper_scraper')


@dataclass
class Paper:
    title: str
    authors: List[str]
    abstract: str
    source: str
    url: str
    direction: str  # TCC or iNEST
    keywords: List[str] = field(default_factory=list)
    published_date: str = ''
    pdf_url: str = ''
    tags: List[str] = field(default_factory=list)
    relevance_score: float = 0.0

    def to_dict(self):
        return {
            'title': self.title,
            'authors': self.authors,
            'abstract': self.abstract,
            'source': self.source,
            'url': self.url,
            'direction': self.direction,
            'keywords': self.keywords,
            'published_date': self.published_date,
            'pdf_url': self.pdf_url,
            'tags': self.tags,
            'relevance_score': self.relevance_score,
        }


class PaperScraper:
    def __init__(self, config):
        self.config = config
        self.base_dir = Path(__file__).parent.parent
        self.output_dir = self.base_dir / 'papers' / datetime.now().strftime('%Y%m%d')
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def run_daily(self):
        logger.info('开始每日论文抓取...')
        papers = []

        # arXiv 搜索
        papers.extend(self._scrape_arxiv())

        # IEEE Xplore 搜索
        papers.extend(self._scrape_ieee())

        # ACM Digital Library 搜索
        papers.extend(self._scrape_acm())

        # CNKI 搜索
        papers.extend(self._scrape_cnki())

        # 保存结果
        self._save_papers(papers)
        logger.info(f'抓取完成，共找到 {len(papers)} 篇论文')

    def _scrape_arxiv(self) -> List[Paper]:
        papers = []
        sources = self.config['paper_search']['sources']
        arxiv_source = next((s for s in sources if s['name'] == 'arXiv'), None)
        if not arxiv_source or not arxiv_source.get('enabled'):
            return papers

        query = '+AND+'.join(arxiv_source['keywords'])
        url = f'http://export.arxiv.org/api/query?search_query=all:{query}&max_results=50'

        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                import xml.etree.ElementTree as ET
                root = ET.fromstring(resp.text)
                ns = {'atom': 'http://www.w3.org/2005/Atom'}
                for entry in root.findall('atom:entry', ns):
                    title = entry.find('atom:title', ns).text.strip()
                    authors = [a.find('atom:name', ns).text for a in entry.findall('atom:author', ns)]
                    abstract = entry.find('atom:summary', ns).text.strip()
                    link = entry.find('atom:link', ns).get('href')

                    direction = self._classify_direction(title, abstract)
                    paper = Paper(
                        title=title,
                        authors=authors,
                        abstract=abstract,
                        source='arXiv',
                        url=link,
                        direction=direction,
                        published_date=datetime.now().strftime('%Y-%m-%d'),
                        relevance_score=self._calc_relevance(title, abstract, direction),
                    )
                    papers.append(paper)
        except Exception as e:
            logger.error(f'arXiv 抓取失败: {e}')

        return papers

    def _scrape_ieee(self) -> List[Paper]:
        papers = []
        # IEEE Xplore API 示例（需要 API Key）
        return papers

    def _scrape_acm(self) -> List[Paper]:
        papers = []
        return papers

    def _scrape_cnki(self) -> List[Paper]:
        papers = []
        return papers

    def _classify_direction(self, title: str, abstract: str) -> str:
        tcc_keywords = ['trust', 'secure', 'attestation', 'TEE', 'enclave', 'cryptocurrency', 'blockchain', 'verification']
        inest_keywords = ['edge', 'network', 'topology', 'computing', 'distributed', 'intelligent', 'scale-free', 'small-world']

        text = (title + ' ' + abstract).lower()
        tcc_score = sum(1 for kw in tcc_keywords if kw in text)
        inest_score = sum(1 for kw in inest_keywords if kw in text)

        if tcc_score > inest_score:
            return 'TCC'
        elif inest_score > tcc_score:
            return 'iNEST'
        return 'both'

    def _calc_relevance(self, title: str, abstract: str, direction: str) -> float:
        text = (title + ' ' + abstract).lower()
        score = 0.0
        if direction == 'TCC':
            keywords = ['trust', 'secure', 'enclave', 'attestation', 'crypto']
        else:
            keywords = ['network', 'topology', 'edge', 'distributed', 'complex']
        for kw in keywords:
            if kw in text:
                score += 0.2
        return min(score, 1.0)

    def _save_papers(self, papers: List[Paper]):
        direction_dirs = {}
        for paper in papers:
            if paper.direction not in direction_dirs:
                dir_path = self.output_dir / paper.direction
                dir_path.mkdir(exist_ok=True)
                direction_dirs[paper.direction] = dir_path

            md_file = dir_path / f'{datetime.now().strftime("%Y%m%d_%H%M%S")}_{paper.title[:50].replace(" ", "_")}.md'
            content = self._format_paper_md(paper)
            md_file.write_text(content, encoding='utf-8')

        # 保存摘要索引
        index_file = self.output_dir / 'index.json'
        index = {
            'scrape_date': datetime.now().isoformat(),
            'total': len(papers),
            'papers': [p.to_dict() for p in papers],
        }
        index_file.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding='utf-8')

    def _format_paper_md(self, paper: Paper) -> str:
        return f\"\"\"---
title: \"{paper.title}\"
date: {paper.published_date}
source: {paper.source}
url: {paper.url}
direction: {paper.direction}
relevance: {paper.relevance_score:.2f}
authors: {', '.join(paper.authors)}
---

# {paper.title}

**来源:** {paper.source}
**作者:** {', '.join(paper.authors)}
**方向:** {paper.direction}
**相关度:** {paper.relevance_score:.2f}

## 摘要

{paper.abstract}
\"\"\"
