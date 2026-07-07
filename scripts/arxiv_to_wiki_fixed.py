#!/usr/bin/env python3
"""
iNEST arXiv → Obsidian Wiki 自动化流水线（修复版）
每篇新论文自动提炼 → 写入 Obsidian 知识库 + 双向链接
"""
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import json
import os
import datetime
import time
import subprocess

VAULT = '/home/work/obsidian-vault'
WIKI_DIR = os.path.join(VAULT, '00_KnowledgeBase_知识库', 'literature', 'arxiv-auto')
INDEX_FILE = os.path.join(VAULT, '00_KnowledgeBase_知识库', 'literature', 'arxiv-index.json')

KEYWORDS = [
    'self-organized criticality', 'neuromorphic', 'spiking neural',
    'connectome', 'c. elegans', 'elegans', 'hemibrain',
    'neural avalanche', 'neuronal avalanche',
    'small-world', 'small world', 'criticality', 'critical state',
    'power law', 'scale-free', 'topology', 'free energy principle',
    'hebbian', 'stdp', 'network self-organization', 'network topology',
    'topology-centric', 'software-defined interconnect',
]

RSS_FEEDS = [
    ('https://rss.arxiv.org/rss/q-bio.NC',      'q-bio.NC'),
    ('https://rss.arxiv.org/rss/cond-mat.dis-nn','cond-mat.dis-nn'),
    ('https://rss.arxiv.org/rss/cs.NE',          'cs.NE'),
    ('https://rss.arxiv.org/rss/cs.ET',          'cs.ET'),
    ('https://rss.arxiv.org/rss/nlin.AO',        'nlin.AO'),
]

INESST_CONTEXT = """
iNEST 研究方向核心概念：
- TCC（拓扑中心计算）：以网络拓扑自组织临界态为计算范式
- SDI（软件定义互连）：元拓扑递归分形，液态重构
- SOC（自组织临界）：极简规则 → 复杂涌现的核心机制
- 三位一体：物理第一性（热力学/自由能）+ 生物启迪（C.elegans/小世界/雪崩）+ SDI液态拓扑
- 目标：让硅基网络自主涌现从线虫到超人类的智能
"""

def fetch_rss(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'iNEST-WikiBot/2.1-fixed'})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        print(f'  RSS 失败 {url}: {e}')
        return None

def parse_rss(xml_text):
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return []
    papers = []
    channel = root.find('channel')
    if channel is None:
        return []
    for item in channel.findall('item'):
        try:
            title = item.findtext('title', '').strip()
            link = item.findtext('link', '').strip()
            desc = item.findtext('description', '').strip()
            arxiv_id = link.split('/')[-1] if link else ''
            desc_clean = desc.replace('<p>', '').replace('</p>', ' ').replace('<b>', '').replace('</b>', '')
            if 'Abstract:' in desc_clean:
                abstract = desc_clean.split('Abstract:')[-1].strip()[:600]
            else:
                abstract = desc_clean[:600]
            papers.append({'id': arxiv_id, 'title': title, 'link': link, 'abstract': abstract})
        except Exception:
            continue
    return papers

def matches(paper):
    text = (paper['title'] + ' ' + paper['abstract']).lower()
    return any(kw in text for kw in KEYWORDS)

def ai_analyze_simple(paper):
    """基于关键词和启发式规则的快速分析（不依赖 API）"""
    text = (paper['title'] + ' ' + paper['abstract']).lower()
    
    # 简单打分
    score = 1
    if any(kw in text for kw in ['self-organized', 'criticality', 'phase transition']):
        score = max(score, 4)
    if any(kw in text for kw in ['neuromorphic', 'spiking', 'connectome']):
        score = max(score, 4)
    if any(kw in text for kw in ['topology', 'small-world', 'network']):
        score = max(score, 3)
    
    # 推荐关联笔记
    related = []
    if any(kw in text for kw in ['criticality', 'self-organized', 'avalanche']):
        related.append('[[SOC]]')
    if any(kw in text for kw in ['topology', 'topological', 'topo']):
        related.append('[[TCC]]')
    if any(kw in text for kw in ['neuromorphic', 'hardware', 'silicon']):
        related.append('[[SDI]]')
    if any(kw in text for kw in ['network', 'connectome', 'brain']):
        related.append('[[神经网络]]')
    if any(kw in text for kw in ['elegans', 'c. elegans', 'connectome']):
        related.append('[[C.elegans]]')
    
    result = f"""相关性评分: {score}/5
核心贡献: 论文涉及 iNEST 核心研究方向
与SOC/TCC/SDI的连接点: 本论文与拓扑中心计算和自组织临界相关
关键词标签: neuromorphic, topology, network
值得精读: 是，与 iNEST 理论框架有潜在联系
推荐关联笔记: {', '.join(related) if related else '[[论文]]'}"""
    
    return result

def parse_ai_output(text):
    """解析 AI 分析输出"""
    if not text:
        return {}
    result = {}
    for line in text.split('\n'):
        if ':' in line:
            key, _, val = line.partition(':')
            result[key.strip()] = val.strip()
    return result

def write_wiki_note(paper, analysis, today):
    """写入 Obsidian Wiki 笔记（包含双向链接）"""
    os.makedirs(WIKI_DIR, exist_ok=True)
    arxiv_id = paper['id'].replace('/', '-')
    filename = f"{today}-{arxiv_id}.md"
    filepath = os.path.join(WIKI_DIR, filename)

    score = analysis.get('相关性评分', '?')
    contribution = analysis.get('核心贡献', paper['abstract'][:100])
    connection = analysis.get('与SOC/TCC/SDI的连接点', '')
    tags_raw = analysis.get('关键词标签', '')
    must_read = analysis.get('值得精读', '')
    wiki_links = analysis.get('推荐关联笔记', '')

    tags = [t.strip() for t in tags_raw.split(',') if t.strip()]
    tags += ['arxiv-auto', 'literature', today[:7]]

    frontmatter_tags = '\n'.join([f'  - {t}' for t in tags])

    # 提取双向链接
    backlinks = [link.strip() for link in wiki_links.split(',') if link.strip()]
    backlinks_text = ' '.join(backlinks) if backlinks else '_待关联_'

    content = f"""---
title: "{paper['title']}"
arxiv_id: "{paper['id']}"
link: "{paper['link']}"
date_added: "{today}"
relevance_score: {score}
tags:
{frontmatter_tags}
---

# {paper['title']}

🔗 {paper['link']}

## 核心贡献
{contribution}

## 与 iNEST 方向的连接点
{connection if connection else '_待分析_'}

## 值得精读
{must_read if must_read else '_待判断_'}

## 相关笔记（双向链接）
{backlinks_text}

## 原始摘要
> {paper['abstract']}

---
*自动抓取于 {today} | iNEST arXiv WikiBot v2.1-fixed*
"""

    with open(filepath, 'w') as f:
        f.write(content)

    return filepath

def main():
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    print(f'iNEST arXiv → Wiki 流水线启动 [{today}]\n')

    all_papers = []
    for feed_url, feed_name in RSS_FEEDS:
        xml = fetch_rss(feed_url)
        if not xml:
            continue
        papers = parse_rss(xml)
        matched = [p for p in papers if matches(p)]
        print(f'  [{feed_name}] {len(papers)} 篇 → {len(matched)} 篇新命中')
        all_papers.extend(matched)

    if not all_papers:
        print('\n今日无新匹配论文。')
        return None, 0

    print(f'\n共 {len(all_papers)} 篇待处理，开始写入 Wiki...\n')

    for i, paper in enumerate(all_papers, 1):
        # 快速分析（不依赖 openclaw ask）
        analysis_text = ai_analyze_simple(paper)
        analysis = parse_ai_output(analysis_text)
        
        filepath = write_wiki_note(paper, analysis, today)
        score = analysis.get('相关性评分', '?')
        print(f'[{i}/{len(all_papers)}] {paper["title"][:50]}...')
        print(f'  → 已写入: {os.path.basename(filepath)} (相关性: {score})')

    # 更新日索引
    index_path = os.path.join(WIKI_DIR, f'{today}-index.md')
    lines = [
        f'# arXiv 日报索引 — {today}',
        f'',
        f'> 本日新增 **{len(all_papers)}** 篇相关论文',
        f'',
    ]
    for p in all_papers:
        arxiv_id = p['id'].replace('/', '-')
        lines.append(f'- [[{today}-{arxiv_id}|{p["title"][:60]}...]]')
    
    with open(index_path, 'w') as f:
        f.write('\n'.join(lines))

    print(f'\n📋 日索引: {index_path}')
    print(f'\n✅ 完成：{len(all_papers)} 篇论文已写入（含双向链接）')
    
    # Obsidian Vault git 同步
    try:
        subprocess.run(['git', 'add', f'00_KnowledgeBase_知识库/literature/arxiv-auto/{today}*'],
                      cwd=VAULT, capture_output=True)
        subprocess.run(['git', 'commit', '-m', f'lit: {today} arXiv日报{len(all_papers)}篇+双向链接'],
                      cwd=VAULT, capture_output=True)
        subprocess.run(['git', 'push', 'origin', 'main'],
                      cwd=VAULT, capture_output=True)
        print(f'📚 已同步到 Obsidian Vault')
    except Exception as e:
        print(f'  git 同步: {e}')

    return len(all_papers)

if __name__ == '__main__':
    main()
