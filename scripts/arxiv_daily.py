#!/usr/bin/env python3
"""
iNEST arXiv Daily Tracker v2
使用 arXiv RSS feed（绕过 API 限速）+ Semantic Scholar API
追踪 SOC / 神经形态 / 连接组 / 神经雪崩方向
"""
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import json
import os
import datetime
import time

# arXiv RSS feeds - 按分类订阅，再本地过滤关键词
# q-bio.NC: 神经科学计算
# cond-mat.dis-nn: 无序系统和神经网络
# cs.NE: 神经演化计算
# cs.ET: 新兴技术（含神经形态）
RSS_FEEDS = [
    'https://rss.arxiv.org/rss/q-bio.NC',
    'https://rss.arxiv.org/rss/cond-mat.dis-nn',
    'https://rss.arxiv.org/rss/cs.NE',
    'https://rss.arxiv.org/rss/cs.ET',
    'https://rss.arxiv.org/rss/nlin.AO',  # 非线性科学-自适应/自组织
]

# 关键词过滤（命中任一即保留）
KEYWORDS = [
    'self-organized criticality', 'self organised criticality',
    'neuromorphic', 'spiking neural',
    'connectome', 'c. elegans', 'elegans',
    'neural avalanche', 'neuronal avalanche',
    'small-world', 'small world network',
    'criticality', 'critical state',
    'power law', 'scale-free',
    'topology', 'topological',
    'free energy principle',
    'hebbian', 'stdp',
    'hemibrain', 'drosophila connectome',
    'network self-organization',
]

def fetch_rss(url, timeout=20):
    """抓取 arXiv RSS feed"""
    req = urllib.request.Request(url, headers={'User-Agent': 'iNEST-Research-Tracker/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode('utf-8', errors='replace')
    except Exception as e:
        print(f'  RSS 获取失败 {url}: {e}')
        return None

def parse_rss(xml_text):
    """解析 RSS XML"""
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
            # arXiv RSS 用 dc:description 或 description
            arxiv_id = link.split('/')[-1] if link else ''

            papers.append({
                'id': arxiv_id,
                'title': title,
                'link': link,
                'summary': desc[:500],
            })
        except Exception:
            continue
    return papers

def matches_keywords(paper):
    """检查论文是否匹配关键词"""
    text = (paper['title'] + ' ' + paper['summary']).lower()
    return any(kw in text for kw in KEYWORDS)

def fetch_semantic_scholar(query, limit=5):
    """使用 Semantic Scholar API 搜索（免费，无 API key）"""
    url = 'https://api.semanticscholar.org/graph/v1/paper/search'
    params = {
        'query': query,
        'limit': limit,
        'fields': 'title,authors,year,abstract,externalIds,publicationDate',
        'publicationDateOrYear': f'{datetime.date.today().year}',
    }
    full_url = url + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(full_url, headers={'User-Agent': 'iNEST-Research-Tracker/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read())
        return data.get('data', [])
    except Exception as e:
        return []

def main():
    print('iNEST arXiv 追踪器 v2 启动...\n')
    today = datetime.date.today().isoformat()
    all_papers = []
    seen_ids = set()

    # 方式1: arXiv RSS（主要来源）
    print('=== 抓取 arXiv RSS Feeds ===')
    for feed_url in RSS_FEEDS:
        cat = feed_url.split('/')[-1]
        xml_text = fetch_rss(feed_url)
        if not xml_text:
            continue
        papers = parse_rss(xml_text)
        matched = [p for p in papers if matches_keywords(p)]
        for p in matched:
            if p['id'] not in seen_ids:
                seen_ids.add(p['id'])
                p['source'] = f'arXiv:{cat}'
                all_papers.append(p)
        print(f'  [{cat}] {len(papers)} 篇 → 过滤后 {len(matched)} 篇命中')
        time.sleep(1)

    # 方式2: Semantic Scholar 补充
    print('\n=== Semantic Scholar 补充搜索 ===')
    ss_queries = [
        'self-organized criticality neural network 2025',
        'neuromorphic computing topology criticality 2025',
        'connectome C elegans computation 2025',
        'neural avalanche criticality brain 2025',
    ]
    for query in ss_queries:
        results = fetch_semantic_scholar(query, limit=5)
        count = 0
        for r in results:
            ext_ids = r.get('externalIds', {})
            arxiv_id = ext_ids.get('ArXiv', r.get('paperId', ''))
            if arxiv_id and arxiv_id not in seen_ids:
                seen_ids.add(arxiv_id)
                authors = [a['name'] for a in r.get('authors', [])[:3]]
                all_papers.append({
                    'id': arxiv_id,
                    'title': r.get('title', ''),
                    'link': f'https://arxiv.org/abs/{arxiv_id}' if ext_ids.get('ArXiv') else f'https://www.semanticscholar.org/paper/{arxiv_id}',
                    'summary': (r.get('abstract') or '')[:400],
                    'authors': authors,
                    'published': r.get('publicationDate', ''),
                    'source': 'SemanticScholar',
                })
                count += 1
        print(f'  [{query[:50]}] → {count} 篇新增')
        time.sleep(1)

    print(f'\n✅ 总计 {len(all_papers)} 篇相关论文')

    # 生成报告
    output_dir = os.path.expanduser('~/.openclaw/workspace/research/arxiv-daily')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f'{today}.md')

    lines = [
        f'# iNEST arXiv 日报 — {today}',
        '',
        '> 追踪方向：SOC · 神经形态计算 · 连接组 · 神经雪崩 · 小世界网络 · 拓扑临界',
        f'> 共 **{len(all_papers)}** 篇',
        '',
    ]

    if not all_papers:
        lines.append('今日无新论文匹配。')
    else:
        for i, p in enumerate(all_papers, 1):
            authors = p.get('authors', [])
            authors_str = ', '.join(authors) + (' et al.' if len(authors) >= 3 else '') if authors else ''
            pub = p.get('published', '')
            source = p.get('source', 'arXiv')
            lines += [
                f'## {i}. {p["title"]}',
                f'`{source}`' + (f' | {authors_str}' if authors_str else '') + (f' | {pub}' if pub else ''),
                f'🔗 {p["link"]}',
                '',
                f'{p["summary"]}{"..." if len(p["summary"]) >= 400 else ""}',
                '',
                '---',
                '',
            ]

    report = '\n'.join(lines)
    with open(output_path, 'w') as f:
        f.write(report)

    print(f'📄 报告: {output_path}')
    print('\n' + report[:3000])
    return report, len(all_papers)


if __name__ == '__main__':
    main()
