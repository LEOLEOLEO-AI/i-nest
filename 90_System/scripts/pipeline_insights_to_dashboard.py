#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""insights_to_dashboard_v2.py - 洞察→看板灵感 + 今日计划生成 + TLDR中文化"""
import sys, json, re
from pathlib import Path
from datetime import datetime

sys.path.insert(0, r'D:\Obsidian\scripts')
from llm_router import llm_call

VAULT = Path(r'D:\Obsidian\home\work\.openclaw\workspace')
INSIGHTS_DIR = VAULT / '00_Inbox' / '_pipeline_insights'
DASHBOARD_JS = VAULT / 'dashboard' / 'data.js'
META = VAULT / '99_Meta'

TODAY = datetime.now().strftime('%Y-%m-%d')
T = datetime.now().strftime('%m-%d')

def translate_tldr(text):
    if not text or len(text) < 20:
        return ''
    if any('\u4e00' <= c <= '\u9fff' for c in text[:30]):
        return text[:200]
    prompt = f'请将以下英文论文摘要翻译为简洁中文，保留核心技术术语，不超过150字：\n\n{text[:1000]}'
    try:
        result = llm_call(prompt)
        if result and len(result) > 5:
            return result.strip()[:200]
    except:
        pass
    return ''

def scan_insights():
    papers = []
    for f in sorted(INSIGHTS_DIR.glob(f'{TODAY}*.md')):
        c = f.read_text(encoding='utf-8', errors='ignore')
        m = re.search(r'relevance: (\d+)', c)
        score = int(m.group(1)) if m else 0
        title_m = re.search(r'^# (.+)$', c, re.MULTILINE)
        title = title_m.group(1).strip() if title_m else f.stem
        tldr_m = re.search(r'## 一句话总结(?:\(中文\))?\n\n(.+?)(?:\n>|\n##|\n---)', c, re.DOTALL)
        tldr = tldr_m.group(1).strip()[:500] if tldr_m else ''
        tcc_m = re.search(r'## TCC 启示\n\n(.+?)(?:\n##|\n---)', c, re.DOTALL)
        tcc = tcc_m.group(1).strip()[:300] if tcc_m else ''
        inest_m = re.search(r'## iNEST 启示\n\n(.+?)(?:\n##|\n---)', c, re.DOTALL)
        inest = inest_m.group(1).strip()[:300] if inest_m else ''
        act_m = re.search(r'## 可执行行动\n\n(.+?)(?:\n---)', c, re.DOTALL)
        action = act_m.group(1).strip()[:300] if act_m else ''
        papers.append({'title': title[:120], 'score': score, 'tldr': tldr, 'tcc': tcc, 'inest': inest, 'action': action, 'path': str(f.relative_to(VAULT))})
    return papers

def generate_inspiration(papers):
    """从高分论文生成灵感条目"""
    items = []
    high = [p for p in papers if p['score'] >= 3]
    for p in high[:6]:
        insight = ''
        dim = ''
        if p['tcc'] and p['inest']:
            dim = 'TCC+iNEST'
            insight = p['tcc'][:60] + ' | ' + p['inest'][:60]
        elif p['tcc']:
            dim = 'TCC'
            insight = p['tcc'][:120]
        elif p['inest']:
            dim = 'iNEST'
            insight = p['inest'][:120]
        if insight:
            items.append({'text': f'[灵感] {p["title"][:50]} — {insight[:80]}', 'dot': 'inspiration', 'dim': dim})
    return items

def generate_today_plan(papers):
    """基于洞察和项目状态生成今日计划"""
    plan = []
    
    # 统计今日洞察
    high = [p for p in papers if p['score'] >= 3]
    tcc_papers = [p for p in papers if p['tcc']]
    inest_papers = [p for p in papers if p['inest']]
    
    plan.append({'text': f'[洞察] 处理今日{len(high)}篇高相关论文的TCC/iNEST启示', 'dot': 'ongoing', 'dim': 'TCC+iNEST'})
    
    if tcc_papers:
        plan.append({'text': f'[TCC] 分析{len(tcc_papers)}篇互连/拓扑相关文献，更新SDI拓扑设计空间', 'dot': 'plan', 'dim': 'TCC'})
    if inest_papers:
        plan.append({'text': f'[iNEST] 分析{len(inest_papers)}篇临界态/涌现文献，更新理论框架', 'dot': 'plan', 'dim': 'iNEST'})
    
    # 检查项目状态
    snapshot = META / 'project_snapshot.md'
    if snapshot.exists():
        c = snapshot.read_text(encoding='utf-8', errors='ignore')
        if '论文' in c:
            plan.append({'text': '[论文] 推进撰写: Topology-Centric Computing', 'dot': 'plan', 'dim': 'TCC'})
            plan.append({'text': '[论文] 推进撰写: iNEST涌现智能理论', 'dot': 'plan', 'dim': 'iNEST'})
        if '专利' in c:
            plan.append({'text': '[专利] 推进撰写: 复杂网络拓扑的分布式计算方法', 'dot': 'plan', 'dim': 'TCC'})
        if 'CST' in c or '仿真' in c:
            plan.append({'text': '[仿真] CST仿真实验推进', 'dot': 'plan', 'dim': 'TCC+iNEST'})
    
    plan.append({'text': f'[同步] Git+Gitee 版本同步 (21:00)', 'dot': 'plan', 'dim': 'TCC+iNEST'})
    plan.append({'text': f'[采集] 得到大脑剪藏导入 Obsidian', 'dot': 'plan', 'dim': 'TCC+iNEST'})
    
    return plan

def main():
    papers = scan_insights()
    high = [p for p in papers if p['score'] >= 3]
    
    print(f'洞察: {len(papers)}篇 (高相关{len(high)}篇)')
    
    # TLDR中文化
    translated = 0
    for p in high:
        if p['tldr'] and not any('\u4e00' <= c <= '\u9fff' for c in p['tldr'][:30]):
            cn = translate_tldr(p['tldr'])
            if cn:
                p['tldr_cn'] = cn
                translated += 1
                fp = VAULT / p['path']
                if fp.exists():
                    c = fp.read_text(encoding='utf-8', errors='ignore')
                    if '## 一句话总结 (中文)' not in c:
                        c = c.replace('## 一句话总结', '## 一句话总结 (中文)')
                    if p['tldr'][:80] in c:
                        c = c.replace(p['tldr'][:80], cn + '\n\n> *原文*: ' + p['tldr'][:200])
                        fp.write_text(c, encoding='utf-8')
    print(f'翻译: {translated}篇')
    
    # 生成灵感
    inspiration = generate_inspiration(papers)
    print(f'灵感: {len(inspiration)}条')
    
    # 生成今日计划
    plan = generate_today_plan(papers)
    print(f'计划: {len(plan)}条')
    
    # 保存看板数据
    data = {
        'date': TODAY,
        'total_papers': len(papers),
        'high_score': len(high),
        'tcc_count': len([p for p in papers if p['tcc']]),
        'inest_count': len([p for p in papers if p['inest']]),
        'inspiration': inspiration,
        'plan': plan
    }
    
    out = META / f'insights_dashboard_{TODAY}.json'
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    
    # 更新 data.js
    update_js = f'''
// 今日洞察数据 — {TODAY}
var DASHBOARD_INSIGHTS = {json.dumps(inspiration, ensure_ascii=False)};
var TODAY_PLAN = {json.dumps(plan, ensure_ascii=False)};
'''
    
    js = DASHBOARD_JS.read_text(encoding='utf-8', errors='ignore')
    # 替换旧的 INSIGHTS 和 PLAN
    js = re.sub(r'// AUTO-GENERATED.*?var DASHBOARD_INSIGHTS.*?;', '', js, flags=re.DOTALL)
    js = re.sub(r'var TODAY_PLAN.*?;', '', js, flags=re.DOTALL)
    # 在 DATA_VERSION 之后插入
    js = js.replace(f'var DATA_VERSION = ', update_js + f'var DATA_VERSION = ')
    DASHBOARD_JS.write_text(js, encoding='utf-8')
    
    print(f'看板已更新: {DASHBOARD_JS}')
    return data

if __name__ == '__main__':
    main()
