#!/usr/bin/env python3
"""
iNEST 知识转化引擎
自动从文档提炼启迪点，推进论文、专利、工程、项目

使用方法:
    python inesst_insight_extractor.py --paper_title "..." --abstract "..." --source "arXiv:2406.xxxxx"
    或集成到 arXiv 日报处理流程
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class InsightPoint:
    """启迪点数据结构"""
    source: str                    # 文献来源
    inesst_dimension: List[str]   # iNEST 维度
    mechanism: str                 # 机制描述
    insight_type: str              # 类型
    title: str                     # 标题
    description: str               # 详细描述
    action_paper: str              # 论文行动
    action_patent: str             # 专利行动
    action_engineering: str        # 工程行动
    action_project: str            # 项目行动
    timestamp: str                 # 时间
    confidence: float              # 置信度


class INeSTInsightExtractor:
    """iNEST 启迪点提取器"""
    
    def __init__(self):
        """初始化"""
        self.inesst_dimensions = {
            'T1': '拓扑理论',
            'E1': 'SDI - 软件定义互连',
            'E2': '分布式智能计算',
            'T3': 'SOC - 自组织临界态',
            'T4': '生物启迪 - 神经连接组',
            'E3': '多尺度脑区实现',
            'E4': '类脑系统工程',
            'γ_t': '时间复杂度',
            'γ_s': '空间复杂度',
            'STC': '时空协同系数',
            'α': '非线性放大指数'
        }
        
        # 关键词-维度映射
        self.keyword_map = {
            # 复杂度相关
            'power spectrum': ['γ_t', 'T3'],
            'pink noise': ['γ_t', 'T3'],
            '1/f': ['γ_t', 'T3'],
            'power law': ['γ_s', 'T1'],
            'scale-free': ['γ_s', 'T1'],
            'degree distribution': ['γ_s'],
            'small-world': ['γ_s', 'T1'],
            'temporal dynamics': ['γ_t', 'T3'],
            
            # 拓扑相关
            'topology': ['T1', 'E1'],
            'network': ['T1', 'E2'],
            'graph': ['T1'],
            'connectivity': ['T1'],
            
            # SDI 相关
            'software-defined': ['E1'],
            'programmable': ['E1', 'E2'],
            'reconfigurable': ['E1'],
            'liquid': ['E1'],
            
            # 生物相关
            'connectome': ['T4', 'E3'],
            'elegans': ['T4'],
            'hemibrain': ['T4'],
            'neural': ['T4', 'E3'],
            'synapse': ['T4', 'STC'],
            'brain': ['E3', 'E4'],
            
            # 分布式计算
            'distributed': ['E2', 'E4'],
            'parallel': ['E2'],
            'communication': ['E2', 'STC'],
            
            # 临界态
            'avalanche': ['α', 'T3'],
            'branching': ['α', 'T3'],
            'critical': ['α', 'T3', 'γ_t'],
            'threshold': ['α'],
            
            # 工程实现
            'chip': ['E1', 'E4'],
            'hardware': ['E1', 'E4'],
            'energy': ['E2', 'E4'],
            'efficient': ['E2'],
        }
        
        self.insights = []
    
    def extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        text_lower = text.lower()
        keywords = set()
        
        for keyword in self.keyword_map.keys():
            if keyword in text_lower:
                keywords.add(keyword)
        
        return sorted(list(keywords))
    
    def map_dimensions(self, keywords: List[str]) -> List[str]:
        """映射维度"""
        dimensions = set()
        for kw in keywords:
            if kw in self.keyword_map:
                dimensions.update(self.keyword_map[kw])
        return sorted(list(dimensions))
    
    def extract_insights(self, source: str, title: str, abstract: str) -> List[InsightPoint]:
        """提取启迪点"""
        keywords = self.extract_keywords(f"{title} {abstract}")
        dimensions = self.map_dimensions(keywords)
        
        if not dimensions:
            return []
        
        insights = []
        
        # 启迪点 1: 复杂度相关
        if any(d in dimensions for d in ['γ_t', 'γ_s', 'α']):
            insights.append(InsightPoint(
                source=source,
                inesst_dimension=dimensions,
                mechanism=f"通过 {', '.join(keywords[:2])} 量化系统复杂度",
                insight_type='直接应用',
                title=f'复杂度指标体系扩展 - {keywords[0]}',
                description=f'融合 {", ".join(keywords[:2])} 的方法，建立多维复杂度评估框架',
                action_paper='V26: 新增多尺度复杂度对比章节',
                action_patent='权利要求新增: 基于复杂度的自适应控制',
                action_engineering='工具: γ_t/γ_s/α 联合分析模块',
                action_project='v41: 用本方法验证不同脑区',
                timestamp=datetime.now().isoformat(),
                confidence=0.85
            ))
        
        # 启迪点 2: 拓扑理论相关
        if 'T1' in dimensions or 'T3' in dimensions:
            insights.append(InsightPoint(
                source=source,
                inesst_dimension=dimensions,
                mechanism=f"通过 {keywords[0]} 验证临界态理论",
                insight_type='理论补充',
                title=f'临界态理论验证 - {keywords[0]}',
                description=f'用 {keywords[0]} 数据验证 iNEST 的 SOC 假设',
                action_paper='V26: 补充临界态理论验证',
                action_patent='背景技术: SOC 的生物实现机制',
                action_engineering='参数优化: 基于生物数据的临界态范围',
                action_project='v42: SOC 放大机制研究',
                timestamp=datetime.now().isoformat(),
                confidence=0.80
            ))
        
        # 启迪点 3: 工程实现相关
        if 'E1' in dimensions or 'E2' in dimensions:
            insights.append(InsightPoint(
                source=source,
                inesst_dimension=dimensions,
                mechanism=f"从 {keywords[0]} 到硅基实现的映射",
                insight_type='工程优化',
                title=f'硅基实现的能效优化 - {keywords[0]}',
                description=f'应用 {keywords[0]} 优化 SDI 芯片设计',
                action_paper='V26: 工程案例分析',
                action_patent='权利要求: 基于复杂度的功耗控制器',
                action_engineering='设计: 参数化 FPGA 配置工具',
                action_project='v43: 完整的理论到硅基流程',
                timestamp=datetime.now().isoformat(),
                confidence=0.75
            ))
        
        # 启迪点 4: 项目扩展
        if 'T4' in dimensions:
            insights.append(InsightPoint(
                source=source,
                inesst_dimension=dimensions,
                mechanism=f"多物种对比验证通过 {keywords[0]}",
                insight_type='项目规划',
                title=f'多物种对比研究扩展',
                description=f'利用新数据源 {keywords[0]} 扩展验证物种',
                action_paper='附录: 新增多物种对比',
                action_patent='范围扩展: 通用生物神经模型',
                action_engineering='数据管道: 新数据预处理流程',
                action_project='v44: 物种无关的复杂度体系',
                timestamp=datetime.now().isoformat(),
                confidence=0.70
            ))
        
        return insights
    
    def process_paper(self, source: str, title: str, abstract: str):
        """处理单篇论文"""
        insights = self.extract_insights(source, title, abstract)
        self.insights.extend(insights)
        print(f"✓ {title[:50]}... → {len(insights)} 条启迪点")
        return insights
    
    def generate_summary(self) -> str:
        """生成摘要"""
        if not self.insights:
            return "暂无启迪点"
        
        lines = []
        lines.append("=" * 80)
        lines.append("📊 iNEST 启迪点汇总")
        lines.append("=" * 80)
        lines.append(f"\n总计: {len(self.insights)} 条启迪点\n")
        
        # 统计
        by_type = {}
        for insight in self.insights:
            t = insight.insight_type
            by_type[t] = by_type.get(t, 0) + 1
        
        lines.append("【类型分布】")
        for t, cnt in sorted(by_type.items()):
            lines.append(f"  {t}: {cnt} 条")
        
        # 维度覆盖
        all_dims = set()
        for insight in self.insights:
            all_dims.update(insight.inesst_dimension)
        
        lines.append("\n【维度覆盖】")
        for dim in sorted(all_dims):
            count = sum(1 for i in self.insights if dim in i.inesst_dimension)
            lines.append(f"  {dim}: {count} 条")
        
        # 行动方向
        lines.append("\n【行动方向】")
        paper_cnt = sum(1 for i in self.insights if i.action_paper)
        patent_cnt = sum(1 for i in self.insights if i.action_patent)
        eng_cnt = sum(1 for i in self.insights if i.action_engineering)
        proj_cnt = sum(1 for i in self.insights if i.action_project)
        
        lines.append(f"  论文: {paper_cnt} 条")
        lines.append(f"  专利: {patent_cnt} 条")
        lines.append(f"  工程: {eng_cnt} 条")
        lines.append(f"  项目: {proj_cnt} 条")
        
        # 详细列表
        lines.append("\n" + "=" * 80)
        lines.append("【启迪点详表】\n")
        
        for i, insight in enumerate(self.insights, 1):
            lines.append(f"[{i}] {insight.title}")
            lines.append(f"    来源: {insight.source}")
            lines.append(f"    维度: {', '.join(insight.inesst_dimension)}")
            lines.append(f"    类型: {insight.insight_type}")
            lines.append(f"    【论文】{insight.action_paper}")
            lines.append(f"    【专利】{insight.action_patent}")
            lines.append(f"    【工程】{insight.action_engineering}")
            lines.append(f"    【项目】{insight.action_project}")
            lines.append("")
        
        return "\n".join(lines)
    
    def save_json(self, filepath: str):
        """保存为 JSON"""
        data = {
            'timestamp': datetime.now().isoformat(),
            'total': len(self.insights),
            'insights': [asdict(i) for i in self.insights]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ 保存到 {filepath}")


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='iNEST 启迪点提取器')
    parser.add_argument('--title', type=str, help='论文标题')
    parser.add_argument('--abstract', type=str, help='摘要')
    parser.add_argument('--source', type=str, help='来源')
    parser.add_argument('--batch', type=str, help='批处理 JSON 文件')
    parser.add_argument('--output', type=str, default='insights.json', help='输出文件')
    
    args = parser.parse_args()
    
    extractor = INeSTInsightExtractor()
    
    if args.batch:
        # 批处理
        with open(args.batch, 'r') as f:
            papers = json.load(f)
        
        for paper in papers:
            extractor.process_paper(
                paper['source'],
                paper['title'],
                paper['abstract']
            )
    else:
        # 单篇处理
        extractor.process_paper(
            args.source or 'unknown',
            args.title or '未指定',
            args.abstract or ''
        )
    
    # 输出
    print("\n" + extractor.generate_summary())
    extractor.save_json(args.output)


if __name__ == '__main__':
    main()
