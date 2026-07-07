#!/usr/bin/env python3
"""
升级所有现存 arXiv 论文笔记
添加双向链接 + 改进 frontmatter + 同步到 git
"""
import os
import re
import json
from pathlib import Path

WIKI_DIR = '/home/work/obsidian-vault/00_KnowledgeBase_知识库/literature/arxiv-auto'
KEYWORDS_MAP = {
    '[[SOC]]': ['self-organized', 'self organised', 'criticality', 'critical state', 'power law', 'avalanche'],
    '[[TCC]]': ['topology', 'topological', 'topology-centric', 'topo'],
    '[[SDI]]': ['software-defined', 'software defined', 'interconnect', 'reconfigurable', 'dynamic routing'],
    '[[神经网络]]': ['neuromorphic', 'spiking neural', 'snn', 'neural network', 'neural'],
    '[[C.elegans]]': ['elegans', 'c. elegans', 'connectome'],
    '[[Hemibrain]]': ['hemibrain', 'drosophila', 'fruit fly', 'fly'],
}

def extract_backlinks(title, abstract):
    """从标题和摘要提取双向链接"""
    text = (title + ' ' + abstract).lower()
    backlinks = set()
    
    for link, keywords in KEYWORDS_MAP.items():
        if any(kw in text for kw in keywords):
            backlinks.add(link)
    
    return sorted(list(backlinks)) if backlinks else []

def parse_frontmatter(content):
    """解析 YAML frontmatter"""
    if not content.startswith('---'):
        return {}, content
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content
    
    fm_text = parts[1]
    body = parts[2]
    
    fm = {}
    for line in fm_text.strip().split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            fm[key.strip()] = val.strip()
    
    return fm, body

def upgrade_note(filepath):
    """升级单个笔记"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    fm, body = parse_frontmatter(content)
    
    # 提取标题和摘要
    title = fm.get('title', '').strip('"')
    abstract_match = re.search(r'## 原始摘要\s*\n>\s*(.+?)(?=\n---|\Z)', body, re.DOTALL)
    abstract = abstract_match.group(1).strip() if abstract_match else ''
    
    # 生成双向链接
    backlinks = extract_backlinks(title, abstract)
    
    # 更新 frontmatter
    fm['has_backlinks'] = 'true' if backlinks else 'false'
    if 'tags' not in fm:
        fm['tags'] = []
    
    # 重建 frontmatter
    fm_lines = ['---']
    for key in ['title', 'arxiv_id', 'link', 'date_added', 'relevance_score', 'has_backlinks']:
        if key in fm:
            val = fm[key]
            if key == 'title':
                fm_lines.append(f'{key}: {val}')
            else:
                fm_lines.append(f'{key}: {val}')
    
    fm_lines.append('tags:')
    if isinstance(fm.get('tags'), list):
        for tag in fm['tags']:
            fm_lines.append(f'  - {tag}')
    fm_lines.append('---')
    
    # 更新笔记体内容：替换或添加双向链接部分
    if '## 相关笔记（双向链接）' in body:
        # 替换已有的链接部分
        pattern = r'## 相关笔记（双向链接）\n[^\n]*(?:\n|$)'
        backlinks_text = ' '.join(backlinks) if backlinks else '_待关联_'
        body = re.sub(pattern, f'## 相关笔记（双向链接）\n{backlinks_text}\n', body)
    else:
        # 在"原始摘要"之前插入链接部分
        if '## 原始摘要' in body:
            backlinks_text = ' '.join(backlinks) if backlinks else '_待关联_'
            body = body.replace(
                '## 原始摘要',
                f'## 相关笔记（双向链接）\n{backlinks_text}\n\n## 原始摘要'
            )
    
    # 组合新内容
    new_content = '\n'.join(fm_lines) + body
    
    # 写回文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return len(backlinks)

def main():
    files = sorted([f for f in os.listdir(WIKI_DIR) if f.endswith('.md') and not f.endswith('index.md')])
    
    print(f"开始升级 {len(files)} 篇论文笔记...")
    print("=" * 80)
    
    total_backlinks = 0
    stats = {'updated': 0, 'with_links': 0}
    
    for i, filename in enumerate(files, 1):
        filepath = os.path.join(WIKI_DIR, filename)
        try:
            links_count = upgrade_note(filepath)
            total_backlinks += links_count
            if links_count > 0:
                stats['with_links'] += 1
            stats['updated'] += 1
            
            if i % 10 == 0 or i == len(files):
                print(f"[{i}/{len(files)}] 已处理 {stats['updated']} 篇，{stats['with_links']} 篇含双向链接")
        except Exception as e:
            print(f"❌ 处理失败 {filename}: {e}")
    
    print("=" * 80)
    print(f"✅ 升级完成")
    print(f"   总笔记数: {stats['updated']}")
    print(f"   含双向链接: {stats['with_links']}")
    print(f"   总链接数: {total_backlinks}")
    
    # 同步到 git
    print("\n同步到 Obsidian Vault git...")
    import subprocess
    vault_dir = '/home/work/obsidian-vault'
    try:
        subprocess.run(['git', 'add', 'obsidian-vault/00_KnowledgeBase_知识库/literature/arxiv-auto/'],
                      cwd='/home/work', capture_output=True, timeout=30)
        subprocess.run(['git', 'commit', '-m', f'feat: upgrade {stats["updated"]} arxiv notes with backlinks'],
                      cwd=vault_dir, capture_output=True, timeout=30)
        subprocess.run(['git', 'push', 'origin', 'main'],
                      cwd=vault_dir, capture_output=True, timeout=30)
        print("✅ 已同步到 git")
    except Exception as e:
        print(f"⚠️  git 同步失败: {e}")

if __name__ == '__main__':
    main()

