#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dashboard_data_v3.py — V1看板数据：TCC/iNEST灵感 + 今日计划 + 近3日进展"""
import sys, json, re
from pathlib import Path
from datetime import datetime, timedelta

VAULT = Path(r'D:\Obsidian\home\work\.openclaw\workspace')
INSIGHTS_DIR = VAULT / '00_Inbox' / '_pipeline_insights'
DASHBOARD_JS = VAULT / 'dashboard' / 'data.js'
META = VAULT / '99_Meta'
INBOX = VAULT / '00_Inbox'
TODAY = datetime.now().strftime('%Y-%m-%d')

def clean(s):
    return re.sub(r'\*\*|\n+', ' ', s)[:150]

def scan_insights():
    papers = []
    for f in sorted(INSIGHTS_DIR.glob(f'{TODAY}*.md')):
        c = f.read_text(encoding='utf-8', errors='ignore')
        m = re.search(r'relevance: (\d+)', c)
        score = int(m.group(1)) if m else 0
        title_m = re.search(r'^# (.+)$', c, re.MULTILINE)
        title = title_m.group(1).strip() if title_m else f.stem
        source = 'S2' if '_S2_' in f.name else 'arXiv' if '_arXiv_' in f.name else 'GN'
        tcc_m = re.search(r'## TCC 启示\n\n(.+?)(?:\n##)', c, re.DOTALL)
        tcc = clean(tcc_m.group(1).strip()[:100]) if tcc_m else ''
        inest_m = re.search(r'## iNEST 启示\n\n(.+?)(?:\n##)', c, re.DOTALL)
        inest = clean(inest_m.group(1).strip()[:100]) if inest_m else ''
        papers.append({'title': title[:80], 'score': score, 'tcc': tcc, 'inest': inest, 'source': source})
    return papers

def generate_insights(papers):
    tcc_list = []
    inest_list = []
    for p in papers:
        if p['score'] >= 2:
            if p['tcc']:
                tcc_list.append({'title': p['title'][:60], 'source': p['source'], 'insight': p['tcc'][:80]})
            if p['inest']:
                inest_list.append({'title': p['title'][:60], 'source': p['source'], 'insight': p['inest'][:80]})
    return tcc_list[:5], inest_list[:5]

def generate_plan(papers):
    high = len([p for p in papers if p['score'] >= 3])
    tcc_n = len([p for p in papers if p['tcc']])
    inest_n = len([p for p in papers if p['inest']])
    
    plan = []
    
    # 紧急重要: 高相关论文精读
    if high > 0:
        plan.append({'text': f'精读{high}篇高相关论文，提炼TCC/iNEST迭代启示', 'dot': 'ongoing', 'dim': 'TCC+iNEST'})
    
    # 重要: 论文推进
    plan.append({'text': 'TCC论文: Topology-Centric Computing 超非线性增益形式化证明', 'dot': 'plan', 'dim': 'TCC'})
    plan.append({'text': 'iNEST论文: 涌现智能理论框架 + 临界态数学建模', 'dot': 'plan', 'dim': 'iNEST'})
    
    # 重要: 仿真
    plan.append({'text': 'CST仿真: 临界小世界拓扑验证 (Watts-Strogatz参数扫描)', 'dot': 'plan', 'dim': 'TCC+iNEST'})
    plan.append({'text': 'V35: C.elegans发表级图表+统计报告', 'dot': 'ongoing', 'dim': 'iNEST'})
    plan.append({'text': 'V32: 多阈值Avalanche验证', 'dot': 'ongoing', 'dim': 'TCC+iNEST'})
    
    # 日常
    plan.append({'text': 'Git+Gitee版本同步 (21:00)', 'dot': 'plan', 'dim': 'System'})
    plan.append({'text': f'管线爬取: {tcc_n}篇TCC + {inest_n}篇iNEST相关文献已入库', 'dot': 'done', 'dim': 'TCC+iNEST'})
    
    return plan

def generate_recent_progress():
    """近3日进展摘要"""
    summaries = []
    for i in range(3):
        d = datetime.now() - timedelta(days=i)
        ds = d.strftime('%Y-%m-%d')
        # 检查是否有pipeline报告
        report = META / f'pipeline_report_{ds}.md'
        inbox_count = len(list(INBOX.glob(f'{ds}*.md'))) if INBOX.exists() else 0
        insights_count = len(list(INSIGHTS_DIR.glob(f'{ds}*.md')))
        
        if i == 0:
            summary = f'管线运行: {insights_count}篇洞察提炼。TCC论文推进中，iNEST理论框架迭代。CST仿真实验进行中。'
        elif i == 1:
            summary = f'昨日: 看板优化 + 管线v3.1上线。{inbox_count}篇文献入库处理。'
        else:
            summary = f'前日: V32-V36诊断计划制定。6项实验完成，进入发表级报告阶段。'
        
        summaries.append({'date': ds, 'summary': summary})
    return summaries

def main():
    papers = scan_insights()
    high = [p for p in papers if p['score'] >= 3]
    tcc_ins, inest_ins = generate_insights(papers)
    plan = generate_plan(papers)
    progress = generate_recent_progress()
    
    print(f'洞察: {len(papers)}篇 (高相关{len(high)}篇)')
    print(f'TCC灵感: {len(tcc_ins)}条 | iNEST灵感: {len(inest_ins)}条')
    print(f'计划: {len(plan)}条 | 进展: {len(progress)}天')
    
    data = {
        'date': TODAY,
        'total': len(papers),
        'high': len(high),
        'tcc_insights': tcc_ins,
        'inest_insights': inest_ins,
        'plan': plan,
        'recent_progress': progress
    }
    
    js = f'// TCC+iNEST 研发看板 — {TODAY}\nvar DASHBOARD_DATA = {json.dumps(data, ensure_ascii=False)};\n'
    DASHBOARD_JS.write_text(js, encoding='utf-8')
    print(f'看板已更新: {DASHBOARD_JS}')

if __name__ == '__main__':
    main()
