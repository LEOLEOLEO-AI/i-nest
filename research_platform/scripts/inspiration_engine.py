# -*- coding: utf-8 -*-
\"\"\"
灵感引擎模块 - InspirationEngine
基于新导入论文分析，生成跨方向的研究灵感
\"\"\"

import logging
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass, field
from collections import Counter

logger = logging.getLogger('inspiration_engine')


@dataclass
class Insight:
    title: str
    description: str
    source_directions: List[str]
    source_papers: List[str]
    category: str  # theory, method, application, patent, engineering
    priority: str  # high, medium, low
    confidence: float = 0.0
    ideas: List[str] = field(default_factory=list)

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'source_directions': self.source_directions,
            'source_papers': self.source_papers,
            'category': self.category,
            'priority': self.priority,
            'confidence': self.confidence,
            'ideas': self.ideas,
        }


class InspirationEngine:
    def __init__(self, config):
        self.config = config
        self.base_dir = Path(__file__).parent.parent
        self.inspiration_dir = self.base_dir / 'inspiration_engine'
        self.inspiration_dir.mkdir(parents=True, exist_ok=True)

    def generate_all(self):
        logger.info('开始生成研究灵感...')

        papers_tcc = self._load_papers('TCC')
        papers_inest = self._load_papers('iNEST')

        insights = []

        # 跨方向灵感
        cross_insights = self._generate_cross_direction(papers_tcc, papers_inest)
        insights.extend(cross_insights)

        # 方向内深化灵感
        tcc_insights = self._generate_deepening_insights(papers_tcc, 'TCC')
        insights.extend(tcc_insights)

        inest_insights = self._generate_deepening_insights(papers_inest, 'iNEST')
        insights.extend(inest_insights)

        # 保存
        self._save_insights(insights)
        logger.info(f'灵感生成完成: {len(insights)} 条灵感')

    def _load_papers(self, direction: str) -> List[Dict]:
        papers = []
        papers_dir = self.base_dir / 'papers' / direction
        if not papers_dir.exists():
            return papers

        index_file = papers_dir / 'index.json'
        if index_file.exists():
            with open(index_file, 'r', encoding='utf-8') as f:
                index = json.load(f)
                for paper in index.get('papers', []):
                    paper['direction'] = direction
                    papers.append(paper)

        return papers

    def _generate_cross_direction(self, papers_tcc: List[Dict], papers_inest: List[Dict]) -> List[Insight]:
        insights = []

        # 找出 TCC 和 iNEST 论文中的共同关键词
        tcc_kw = set()
        for p in papers_tcc:
            tcc_kw.update(kw.lower() for kw in p.get('keywords', []))

        inest_kw = set()
        for p in papers_inest:
            inest_kw.update(kw.lower() for kw in p.get('keywords', []))

        common = tcc_kw & inest_kw
        if common:
            insights.append(Insight(
                title=f'跨方向融合: {", ".join(list(common)[:5])}',
                description='TCC 和 iNEST 方向存在共同关注点，建议探索交叉研究',
                source_directions=['TCC', 'iNEST'],
                source_papers=[p['title'] for p in (papers_tcc[:3] + papers_inest[:3])],
                category='theory',
                priority='high',
                confidence=0.8,
                ideas=[
                    f'将 TCC 的 {", ".join(list(common)[:3])} 应用于 iNEST 的网络拓扑优化',
                    '探索双向标签系统在跨方向知识检索中的价值',
                    '设计统一的跨方向知识表示方法',
                ],
            ))

        # 论文互引关系
        if papers_tcc and papers_inest:
            insights.append(Insight(
                title='TCC-iNEST 跨方向互引分析',
                description='两个方向已有论文存在潜在互引关系，可构建跨方向知识图谱',
                source_directions=['TCC', 'iNEST'],
                source_papers=[papers_tcc[0]['title']] if papers_tcc else [],
                category='method',
                priority='medium',
                confidence=0.6,
                ideas=[
                    '构建跨方向引文网络',
                    '分析 TCC 方法在 iNEST 中的迁移性',
                ],
            ))

        return insights

    def _generate_deepening_insights(self, papers: List[Dict], direction: str) -> List[Insight]:
        insights = []

        if len(papers) < 2:
            return insights

        # 发现趋势
        kw_counter = Counter()
        for p in papers:
            for kw in p.get('keywords', []):
                kw_counter[kw.lower()] += 1

        trending = kw_counter.most_common(3)
        if trending:
            insights.append(Insight(
                title=f'{direction} 方向热点趋势',
                description=f'基于最新论文分析，{direction} 方向最热门的研究方向: {", ".join([kw for kw, _ in trending])}',
                source_directions=[direction],
                source_papers=[p['title'] for p in papers],
                category='theory',
                priority='high',
                confidence=0.9,
                ideas=[f'围绕 "{kw}" 展开深入研究' for kw, _ in trending],
            ))

        # 方法交叉灵感
        method_papers = [p for p in papers if 'method' in p.get('abstract', '').lower() or 'approach' in p.get('abstract', '').lower()]
        if len(method_papers) >= 2:
            insights.append(Insight(
                title=f'{direction} 方法融合',
                description='发现多个论文提出了不同方法，可以尝试融合创新',
                source_directions=[direction],
                source_papers=[p['title'] for p in method_papers],
                category='method',
                priority='medium',
                confidence=0.7,
                ideas=['方法A + 方法B = 新方法C', '对比实验设计', '消融实验方案'],
            ))

        return insights

    def _save_insights(self, insights: List[Insight]):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        insights_file = self.inspiration_dir / f'insights_{timestamp}.json'

        data = {
            'generated_at': datetime.now().isoformat(),
            'total': len(insights),
            'insights': [i.to_dict() for i in insights],
        }

        with open(insights_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        # 更新灵感索引
        index_file = self.inspiration_dir / 'index.json'
        all_insights = []
        if index_file.exists():
            with open(index_file, 'r', encoding='utf-8') as f:
                idx = json.load(f)
                all_insights = idx.get('insights', [])

        all_insights.extend([i.to_dict() for i in insights])
        index_file.write_text(
            json.dumps({'insights': all_insights, 'updated_at': datetime.now().isoformat()}, ensure_ascii=False, indent=2),
            encoding='utf-8'
        )

    def list_insights(self) -> List[Dict]:
        index_file = self.inspiration_dir / 'index.json'
        if not index_file.exists():
            return []
        with open(index_file, 'r', encoding='utf-8') as f:
            return json.load(f).get('insights', [])
