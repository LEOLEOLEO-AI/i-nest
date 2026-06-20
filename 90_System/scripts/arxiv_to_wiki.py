#!/usr/bin/env python3
"""
iNEST arXiv → Obsidian Wiki 自动化流水线
每篇新论文自动提炼 → 写入 Obsidian 知识库
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

NS = 'http://www.w3.org/2005/Atom'

RSS_FEEDS = [
    ('https://rss.arxiv.org/rss/q-bio.NC',      'q-bio.NC'),
    ('https://rss.arxiv.org/rss/cond-mat.dis-nn','cond-mat.dis-nn'),
    ('https://rss.arxiv.org/rss/cs.NE',          'cs.NE'),
    ('https://rss.arxiv.org/rss/cs.ET',          'cs.ET'),
    ('https://rss.arxiv.org/rss/nlin.AO',        'nlin.AO'),
]

KEYWORDS = [
    'self-organized criticality', 'neuromorphic', 'spiking neural',
    'connectome', 'c. elegans', 'elegans', 'hemibrain',
    'neural avalanche', 'neuronal avalanche',
    'small-world', 'small world', 'criticality', 'critical state',
    'power law', 'scale-free', 'topology', 'free energy principle',
    'hebbian', 'stdp', 'network self-organization', 'network topology',
    'topology-centric', 'software-defined interconnect',
]

# iNEST 核心概念（用于 AI 提炼时的上下文）
INESST_CONTEXT = """
iNEST 研究方向核心概念：
- TCC（拓扑中心计算）：以网络拓扑自组织临界态为计算范式
- SDI（软件定义互连）：元拓扑递归分形，液态重构
- SOC（自组织临界）：极简规则 → 复杂涌现的核心机制
- 三位一体：物理第一性（热力学/自由能）+ 生物启迪（C.elegans/小世界/雪崩）+ SDI液态拓扑
- 目标：让硅基网络自主涌现从线虫到超人类的智能
"""

def load_index():
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE) as f:
            return json.load(f)
    return {}

def save_index(index):
    os.makedirs(os.path.dirname(INDEX_FILE), exist_ok=True)
    with open(INDEX_FILE, 'w') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

def fetch_rss(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'iNEST-WikiBot/2.0'})
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
            # 清理 RSS 描述中的 HTML
            desc_clean = desc.replace('<p>', '').replace('</p>', ' ').replace('<b>', '').replace('</b>', '')
            # 提取 abstract 部分
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

def ai_analyze(paper):
    """用 openclaw ask 调用 Claude 分析论文与 iNEST 方向的相关性"""
    prompt = f"""你是 iNEST 研究方向的专家助理。请分析以下论文与 iNEST 方向的关联性。

{INESST_CONTEXT}

论文标题：{paper['title']}
arXiv 链接：{paper['link']}
摘要：{paper['abstract']}

请用中文输出以下结构（严格按格式，每项一行）：
相关性评分: [1-5，5最高]
核心贡献: [一句话，中文]
与SOC/TCC/SDI的连接点: [具体说明，不超过60字]
关键词标签: [3-5个，用逗号分隔]
值得精读: [是/否，理由一句话]
推荐关联笔记: [如[[SOC]]、[[TCC]]等，逗号分隔]"""

    try:
        result = subprocess.run(
            ['openclaw', 'ask', '--no-stream', prompt],
            capture_output=True, text=True, timeout=60
        )
        return result.stdout.strip() if result.returncode == 0 else None
    except Exception:
        return None

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
    """写入 Obsidian Wiki 笔记"""
    os.makedirs(WIKI_DIR, exist_ok=True)
    arxiv_id = paper['id'].replace('/', '-')
    filename = f"{today}-{arxiv_id}.md"
    filepath = os.path.join(WIKI_DIR, filename)

    score = analysis.get('相关性评分', '?')
    contribution = analysis.get('核心贡献', paper['abstract'][:100])
    connection = analysis.get('与SOC/TCC/SDI的连接点', '')
    tags_raw = analysis.get('关键词标签', '')
    must_read = analysis.get('值得精读', '')

    tags = [t.strip() for t in tags_raw.split(',') if t.strip()]
    tags += ['arxiv-auto', 'literature', today[:7]]  # YYYY-MM

    frontmatter_tags = '\n'.join([f'  - {t}' for t in tags])

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

## 原始摘要
> {paper['abstract']}

---
*自动抓取于 {today} | iNEST arXiv WikiBot*
"""

    with open(filepath, 'w') as f:
        f.write(content)

    return filepath

def update_daily_index(new_papers, today):
    """更新每日索引文件"""
    index_path = os.path.join(WIKI_DIR, f'{today}-index.md')
    lines = [
        f'# arXiv 日报索引 — {today}',
        f'',
        f'> 本日新增 **{len(new_papers)}** 篇相关论文',
        f'',
    ]
    for p in new_papers:
        arxiv_id = p['id'].replace('/', '-')
        note_name = f'{today}-{arxiv_id}'
        score = p.get('score', '?')
        title = p['title'][:60]
        lines.append(f'- [{title}]({note_name}) | 相关性: {score}/5')
    lines.append('')
    lines.append('---')
    lines.append('[[arxiv-index|← 返回总索引]]')

    with open(index_path, 'w') as f:
        f.write('\n'.join(lines))
    return index_path


def main():
    today = datetime.date.today().isoformat()
    print(f'iNEST arXiv → Wiki 流水线启动 [{today}]\n')

    # 加载已处理索引（避免重复）
    index = load_index()
    processed_ids = set(index.get('processed', []))

    # 抓取 RSS
    all_papers = []
    seen = set()
    for feed_url, cat in RSS_FEEDS:
        xml = fetch_rss(feed_url)
        if not xml:
            time.sleep(2)
            continue
        papers = parse_rss(xml)
        matched = [p for p in papers if matches(p) and p['id'] not in seen and p['id'] not in processed_ids]
        for p in matched:
            seen.add(p['id'])
            p['category'] = cat
            all_papers.append(p)
        print(f'  [{cat}] {len(papers)} 篇 → {len(matched)} 篇新命中')
        time.sleep(2)

    if not all_papers:
        print('\n今日无新匹配论文。')
        # 仍然写一条空记录
        os.makedirs(WIKI_DIR, exist_ok=True)
        with open(os.path.join(WIKI_DIR, f'{today}-index.md'), 'w') as f:
            f.write(f'# arXiv 日报索引 — {today}\n\n今日无新论文匹配。\n')
        return []

    print(f'\n共 {len(all_papers)} 篇待处理，开始写入 Wiki...\n')

    written = []
    for i, paper in enumerate(all_papers, 1):
        print(f'[{i}/{len(all_papers)}] {paper["title"][:60]}...')

        # AI 分析（尝试，失败则用默认）
        analysis = ai_analyze(paper)
        parsed = parse_ai_output(analysis) if analysis else {}
        paper['score'] = parsed.get('相关性评分', '?')

        # 写入 Wiki
        filepath = write_wiki_note(paper, parsed, today)
        written.append(paper)
        processed_ids.add(paper['id'])
        print(f'  → 已写入: {os.path.basename(filepath)} (相关性: {paper["score"]}/5)')
        time.sleep(1)

    # 更新日索引
    idx_path = update_daily_index(written, today)
    print(f'\n📋 日索引: {idx_path}')

    # 保存已处理 ID
    index['processed'] = list(processed_ids)
    index['last_run'] = today
    save_index(index)

    print(f'\n✅ 完成：{len(written)} 篇论文已写入 {WIKI_DIR}')
    return written


if __name__ == '__main__':
    main()
