#!/usr/bin/env python3
"""
iNEST Wiki 自我健康诊断与进化脚本
按卡帕西法则检查知识库健康状态
"""
import os, re, json, datetime
from pathlib import Path
from collections import defaultdict

VAULT = Path('/home/work/obsidian-vault')
REPORT_PATH = VAULT / '00_MOC' / '健康诊断-MOC.md'

def scan_notes():
    notes = {}
    for md in VAULT.rglob('*.md'):
        rel = md.relative_to(VAULT)
        parts = rel.parts
        if any(p.startswith('.') for p in parts):
            continue
        text = md.read_text(errors='replace')
        links = re.findall(r'\[\[([^\]|#]+)', text)
        notes[str(rel)] = {
            'path': md,
            'text': text,
            'links': links,
            'size': len(text),
            'mtime': md.stat().st_mtime,
        }
    return notes

def check_health(notes):
    issues = defaultdict(list)
    stats = {}
    all_names = {Path(p).stem for p in notes}
    all_paths = set(notes.keys())

    # 1. 孤岛笔记（无出链也无入链）
    incoming = defaultdict(list)
    for path, data in notes.items():
        for link in data['links']:
            incoming[link].append(path)

    orphans = []
    for path, data in notes.items():
        name = Path(path).stem
        has_outlink = len(data['links']) > 0
        has_inlink = len(incoming.get(name, [])) > 0
        skip_dirs = ('Journal', '99-', '00_MOC', 'arxiv-auto')
        if not any(path.startswith(d) for d in skip_dirs):
            if not has_outlink and not has_inlink:
                orphans.append(path)
    stats['orphans'] = len(orphans)
    if orphans:
        issues['孤岛笔记（无链接）'] = orphans[:10]

    # 2. 空文件
    empties = [p for p, d in notes.items() if d['size'] < 50]
    stats['empty'] = len(empties)
    if empties:
        issues['空文件或过短笔记'] = empties[:10]

    # 3. 断链
    broken = []
    for path, data in notes.items():
        for link in data['links']:
            link_name = Path(link).stem if '/' not in link else link
            if link_name not in all_names and link not in all_paths:
                broken.append(f'{path} → [[{link}]]')
    stats['broken_links'] = len(broken)
    if broken:
        issues['断链（目标笔记不存在）'] = broken[:15]

    # 4. arXiv 高分未精读
    unread = []
    arxiv_dir = VAULT / '02_Papers' / 'arxiv-auto'
    if arxiv_dir.exists():
        for md in arxiv_dir.glob('*.md'):
            if 'index' in md.name:
                continue
            text = md.read_text(errors='replace')
            m = re.search(r'relevance_score:\s*([45])', text)
            if m and '精读' not in text and 'TODO' not in text:
                unread.append(md.name)
    stats['high_score_unread'] = len(unread)
    if unread:
        issues['arXiv 高分（≥4）未精读'] = unread[:10]

    # 5. Fleeting 滞留超7天
    fleeting_dir = VAULT / '05_Fleeting'
    stale_fleeting = []
    now = datetime.datetime.now().timestamp()
    if fleeting_dir.exists():
        for md in fleeting_dir.rglob('*.md'):
            age_days = (now - md.stat().st_mtime) / 86400
            if age_days > 7:
                stale_fleeting.append(f'{md.name} ({int(age_days)}天)')
    stats['stale_fleeting'] = len(stale_fleeting)
    if stale_fleeting:
        issues['05_Fleeting 滞留 >7天'] = stale_fleeting[:10]

    # 6. 01_Concepts 覆盖核心概念
    concepts_dir = VAULT / '01_Concepts'
    core_concepts = ['SOC', 'TCC', 'SDI', '小世界', '神经雪崩', '自由能', '元拓扑', 'SDSoW']
    missing_concepts = []
    if concepts_dir.exists():
        existing = [md.stem for md in concepts_dir.glob('*.md')]
        for c in core_concepts:
            if not any(c in e for e in existing):
                missing_concepts.append(c)
    else:
        missing_concepts = core_concepts
    stats['missing_concepts'] = len(missing_concepts)
    if missing_concepts:
        issues['核心概念笔记缺失'] = missing_concepts

    return stats, issues

def score_health(stats, issues):
    """计算综合健康分（0-100）"""
    deductions = 0
    deductions += min(stats.get('orphans', 0) * 2, 20)
    deductions += min(stats.get('empty', 0) * 3, 15)
    deductions += min(stats.get('broken_links', 0), 15)
    deductions += min(stats.get('high_score_unread', 0) * 3, 15)
    deductions += min(stats.get('stale_fleeting', 0) * 2, 10)
    deductions += min(stats.get('missing_concepts', 0) * 3, 15)
    return max(0, 100 - deductions)

def generate_report(notes, stats, issues, score):
    today = datetime.date.today().isoformat()
    total = len(notes)

    status_emoji = '🟢' if score >= 80 else '🟡' if score >= 60 else '🔴'

    lines = [
        '# 知识库健康诊断 (Self-Health Dashboard)',
        '',
        f'> 自动维护 | 每周运行 `python3 ~/workspace/scripts/wiki_health.py`',
        f'> 上次诊断：**{today}** | 综合评分：{status_emoji} **{score}/100**',
        '',
        '---',
        '',
        '## 📊 健康指标',
        '',
        '| 检查项 | 标准 | 当前 | 状态 |',
        '|---|---|---|---|',
        f'| 总笔记数 | — | {total} 篇 | ℹ️ |',
        f'| 孤岛笔记（无链接） | < 10% | {stats.get("orphans",0)} 篇 | {"🟢" if stats.get("orphans",0)/max(total,1)<0.1 else "🔴"} |',
        f'| 空文件 | = 0 | {stats.get("empty",0)} 篇 | {"🟢" if stats.get("empty",0)==0 else "🔴"} |',
        f'| 断链 | = 0 | {stats.get("broken_links",0)} 处 | {"🟢" if stats.get("broken_links",0)==0 else "🟡"} |',
        f'| arXiv 高分未精读 | 每周清零 | {stats.get("high_score_unread",0)} 篇 | {"🟢" if stats.get("high_score_unread",0)==0 else "🟡"} |',
        f'| Fleeting 滞留 >7天 | = 0 | {stats.get("stale_fleeting",0)} 篇 | {"🟢" if stats.get("stale_fleeting",0)==0 else "🟡"} |',
        f'| 核心概念笔记缺失 | = 0 | {stats.get("missing_concepts",0)} 个 | {"🟢" if stats.get("missing_concepts",0)==0 else "🔴"} |',
        '',
        '---',
        '',
    ]

    if issues:
        lines += ['## ⚠️ 待处理问题', '']
        for category, items in issues.items():
            lines.append(f'### {category}')
            for item in items:
                lines.append(f'- {item}')
            lines.append('')
    else:
        lines += ['## ✅ 无问题', '', '知识库状态良好。', '']

    lines += [
        '---',
        '',
        '## 🏗️ 目录结构规范（卡帕西法则）',
        '',
        '```',
        'obsidian-vault/',
        '├── 00_MOC/          ← 入口地图，不放内容只放索引',
        '├── 01_Concepts/     ← 原子概念笔记（一文一概念）',
        '├── 02_Papers/       ← 文献（arxiv-auto 自动 + manual 手动）',
        '├── 03_Projects/     ← 项目文档（TCC计算范式 / iNEST）',
        '├── 04_Research/     ← 实验数据与结果',
        '├── 05_Fleeting/     ← 临时捕获（7天内处理）',
        '├── Journal/         ← 日志',
        '├── 99-Templates/    ← 模板',
        '└── 99-Attachments/  ← 附件',
        '```',
        '',
        '**原则：** 扁平 · 原子 · 链接>分类 · MOC驱动 · Inbox临时缓冲',
        '',
        '---',
        '',
        '## 🔄 进化机制',
        '',
        '- **每日 08:00** arXiv 自动追踪 → `02_Papers/arxiv-auto/`',
        '- **每周** 运行本脚本 → 更新健康报告',
        '- **每周** 把 05_Fleeting 中想法升级为 01_Concepts 原子笔记',
        '- **每月** 检查项目进展，更新 MOC',
        '',
        '---',
        f'*自动生成于 {today} | iNEST Wiki Health Bot*',
    ]

    return '\n'.join(lines)

def main():
    print('iNEST Wiki 健康诊断启动...\n')
    notes = scan_notes()
    print(f'共扫描 {len(notes)} 篇笔记')

    stats, issues = check_health(notes)
    score = score_health(stats, issues)

    print(f'\n综合健康分: {score}/100')
    for k, v in stats.items():
        print(f'  {k}: {v}')

    if issues:
        print(f'\n⚠️ 发现 {len(issues)} 类问题：')
        for cat, items in issues.items():
            print(f'  [{cat}] {len(items)} 项')

    report = generate_report(notes, stats, issues, score)
    REPORT_PATH.write_text(report)
    print(f'\n✅ 健康报告已更新: {REPORT_PATH}')
    return score

if __name__ == '__main__':
    main()
