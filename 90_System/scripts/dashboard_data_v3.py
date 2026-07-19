#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dashboard_data_v3.py — V1看板数据：TCC/iNEST灵感 + 今日计划 + 近3日进展"""
import sys, json, re
from pathlib import Path
from datetime import datetime, timedelta

VAULT = Path(r'D:\Obsidian\home\work\.openclaw\workspace')
INSIGHTS_DIR = VAULT / '00_Inbox' / '_pipeline_insights'
DASHBOARD_DIR = VAULT / '70_Dashboard'
DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)
DASHBOARD_JS = DASHBOARD_DIR / 'data.js'
META = VAULT / '99_Meta'
MOC = VAULT / '60_MOC'
INBOX = VAULT / '00_Inbox'
LOG_DIR = VAULT / 'logs'
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
        tcc_m = re.search(r'## (?:TCC Insights|TCC 价值|TCC 启示)\s*\n+(.+?)(?=\n##|\Z)', c, re.DOTALL | re.IGNORECASE)
        tcc = clean(tcc_m.group(1).strip()[:100]) if tcc_m else ''
        inest_m = re.search(r'## (?:iNEST Insights|iNEST 价值|iNEST 启示)\s*\n+(.+?)(?=\n##|\Z)', c, re.DOTALL | re.IGNORECASE)
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

def load_state_counts():
    """Load live vault counts from the unified state bus."""
    state_file = META / 'research_state.json'
    if not state_file.exists():
        return {}

def classify_plan_dimension(text):
    """Assign a dashboard lane without changing the source task text."""
    value = text.lower()
    has_tcc = any(k in value for k in ('tcc', 'p-paradigm', '拓扑', '互连', '专利'))
    has_inest = any(k in value for k in ('inest', 'cst', 'snn', '涌现', '神经', '临界'))
    if has_tcc and has_inest:
        return 'TCC+iNEST'
    if has_tcc:
        return 'TCC'
    if has_inest:
        return 'iNEST'
    return 'System'

def clean_plan_text(text):
    """Convert markdown task text into compact dashboard text."""
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    text = re.sub(r'[*`_]', '', text)
    return re.sub(r'\s+', ' ', text).strip(' -:')

def extract_source_plan(path, section_markers):
    """Extract numbered tasks from a current daily markdown file."""
    if not path.exists():
        return []
    try:
        lines = path.read_text(encoding='utf-8', errors='replace').splitlines()
    except OSError:
        return []
    active = False
    tasks = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('#'):
            active = any(marker.lower() in stripped.lower() for marker in section_markers)
            if active:
                continue
        if active:
            match = re.match(r'^\d+[.)]\s+(.+)$', stripped)
            if match:
                task = clean_plan_text(match.group(1))
                if task:
                    tasks.append(task)
    return tasks

def generate_source_plan():
    """Use today's action and focus files as the dashboard plan source."""
    action = extract_source_plan(MOC / '03_Daily_Action.md', ('今日推荐行动', '今日行动'))
    focus = extract_source_plan(MOC / '04_Daily_Focus.md', ('并行主线', '今日焦点'))
    merged = []
    seen = set()
    for task in action + focus:
        key = task.lower()
        if key in seen:
            continue
        seen.add(key)
        merged.append({'text': task, 'dot': 'ongoing' if len(merged) < 3 else 'plan', 'dim': classify_plan_dimension(task)})
    return merged[:8]
    try:
        state = json.loads(state_file.read_text(encoding='utf-8'))
        vault = state.get('vault', {})
        return {
            'total_md': vault.get('total_md', 0),
            'tcc': vault.get('tcc_30', 0),
            'inest': vault.get('inest_40', 0),
            'inbox': vault.get('inbox_00', 0),
            'papers': vault.get('output_50', 0),
            'services': state.get('services', {})
        }
    except (OSError, json.JSONDecodeError):
        return {}

def generate_operational_plan(papers):
    """Generate an execution-oriented plan for the current deadline."""
    high = len([p for p in papers if p['score'] >= 3])
    plan = [
        {'text': 'P-Paradigm《拓扑中心计算范式》完成 Engineering 投稿前终稿与证据核对（7月30日前）', 'dot': 'ongoing', 'dim': 'TCC'},
        {'text': 'CST《智能涌现》完成 Section 4/5 仿真结果、图表与结论闭环（7月30日前）', 'dot': 'ongoing', 'dim': 'iNEST'},
        {'text': 'TCC 架构专利与实现专利完成权利要求、实施例和附图终审（7月30日前）', 'dot': 'ongoing', 'dim': 'TCC'},
        {'text': f'精读今日 {high} 篇高相关论文，提取可引用证据并回写论文/专利', 'dot': 'plan', 'dim': 'TCC+iNEST'},
        {'text': '运行一次 CST/TCC 可复现实验检查：参数、数据、脚本、图表和指标来源齐全', 'dot': 'plan', 'dim': 'TCC+iNEST'},
        {'text': '21:00 完成 GitHub/Gitee 同步，并检查看板与知识库链接', 'dot': 'plan', 'dim': 'System'}
    ]
    return plan

def generate_operational_progress():
    """Build the latest three daily summaries from real pipeline logs."""
    runs = {}
    for log_file in sorted(LOG_DIR.glob('pipeline_*.json'), reverse=True):
        try:
            item = json.loads(log_file.read_text(encoding='utf-8'))
            date = item.get('date', '')[:10]
            if date and date not in runs:
                runs[date] = item
        except (OSError, json.JSONDecodeError):
            continue

    summaries = []
    for offset in range(3):
        date = (datetime.now() - timedelta(days=offset)).strftime('%Y-%m-%d')
        run = runs.get(date)
        if run:
            summary = (
                f"科研管线完成：入库 {run.get('new_papers', 0)} 篇，"
                f"图谱 {run.get('graph_nodes', 0)} 节点/{run.get('graph_edges', 0)} 边，"
                f"耗时 {round(run.get('elapsed_s', 0) / 60)} 分钟。"
            )
        else:
            summary = '暂无管线运行记录，今天优先检查任务执行与输入输出链路。'
        summaries.append({'date': date, 'summary': summary})
    return summaries

def main():
    papers = scan_insights()
    high = [p for p in papers if p['score'] >= 3]
    tcc_ins, inest_ins = generate_insights(papers)
    plan = generate_source_plan() or generate_operational_plan(papers)
    progress = generate_operational_progress()
    counts = load_state_counts()
    
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
        'recent_progress': progress,
        'counts': counts,
        'generated_at': datetime.now().isoformat(timespec='minutes')
    }
    
    js = f'// TCC+iNEST 研发看板 — {TODAY}\nvar DASHBOARD_DATA = {json.dumps(data, ensure_ascii=False)};\n'
    DASHBOARD_JS.write_text(js, encoding='utf-8')
    print(f'看板已更新: {DASHBOARD_JS}')

if __name__ == '__main__':
    main()
