#!/usr/bin/env python3
"""
P1.3: 双向链接引擎 — 基于内容相似度自动建立 [[双向链接]]
扫描 30_TCC + 40_iNEST，为孤立笔记找到关联并插入链接
"""
import os, sys, json, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime
from collections import defaultdict

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
KEY = os.environ.get("DEEPSEEK_API_KEY") or "REDACTED_DEEPSEEK_KEY"

def tokenize(text):
    """Simple multi-language tokenizer"""
    # Split by whitespace, punctuation, and Chinese characters
    tokens = set()
    # English words
    tokens.update(re.findall(r'[a-zA-Z]{3,}', text.lower()))
    # Chinese bigrams
    chinese = re.findall(r'[\u4e00-\u9fff]+', text)
    for seg in chinese:
        for i in range(len(seg)-1):
            tokens.add(seg[i:i+2])
    return tokens

def build_index(directories, max_files=1000):
    """Build TF-IDF-like index for fast similarity search"""
    index = {}
    all_tokens = defaultdict(int)
    doc_tokens = {}
    
    files = []
    for d in directories:
        p = VAULT / d
        if p.exists():
            files.extend(list(p.rglob("*.md"))[:max_files])
    
    print(f"  Indexing {len(files)} files...")
    
    for f in files:
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
            title = f.stem
            # Title + first 1000 chars
            text = (title + " " + content[:1000]).lower()
            tokens = tokenize(text)
            doc_tokens[str(f.relative_to(VAULT))] = tokens
            for t in tokens:
                all_tokens[t] += 1
        except:
            pass
    
    # IDF
    total_docs = len(doc_tokens)
    idf = {t: __import__('math').log(total_docs / (c + 1)) + 1 for t, c in all_tokens.items()}
    
    return doc_tokens, idf, files

def find_links(filepath, doc_tokens, idf, files, top_n=5):
    """Find most similar files for linking"""
    rel_path = str(filepath.relative_to(VAULT))
    if rel_path not in doc_tokens:
        return []
    
    my_tokens = doc_tokens[rel_path]
    if not my_tokens:
        return []
    
    scores = []
    for f in files:
        other_rel = str(f.relative_to(VAULT))
        if other_rel == rel_path:
            continue
        if other_rel not in doc_tokens:
            continue
        
        other_tokens = doc_tokens[other_rel]
        # Cosine-like: weighted intersection
        intersection = my_tokens & other_tokens
        if not intersection:
            continue
        
        score = sum(idf.get(t, 1) for t in intersection)
        # Normalize by doc length
        score = score / (len(my_tokens) ** 0.5 * len(other_tokens) ** 0.5 + 1)
        if score > 0.05:
            scores.append((score, f))
    
    scores.sort(reverse=True)
    return [s[1] for s in scores[:top_n]]

def add_links_to_file(filepath, related):
    """Insert [[links]] to a file if not present"""
    content = filepath.read_text(encoding="utf-8", errors="replace")
    
    # Check if already has related links
    existing_links = set(re.findall(r'\[\[([^\]]+)\]\]', content))
    new_links = []
    
    for r in related:
        name = r.stem
        if name not in existing_links and name not in str(existing_links):
            new_links.append(f"- [[{name}]]")
            existing_links.add(name)
    
    if not new_links:
        return False
    
    # Check if "## 相关链接" section exists
    if "## 相关链接" in content:
        # Append to existing section
        content = content.rstrip() + "\n" + "\n".join(new_links) + "\n"
    elif "## Related" in content:
        content = content.rstrip() + "\n" + "\n".join(new_links) + "\n"
    else:
        # Add new section at end
        section = "\n\n---\n## 相关链接\n" + "\n".join(new_links) + "\n"
        content = content.rstrip() + section
    
    filepath.write_text(content, encoding="utf-8")
    return True

def link_engine(max_files=500, dry_run=False):
    """Main link engine"""
    print("Building content index...")
    doc_tokens, idf, files = build_index(["30_TCC", "40_iNEST"], max_files)
    
    print(f"Finding links (max {max_files} files)...")
    linked = 0
    total_links = 0
    
    for f in files[:max_files]:
        try:
            if f.stat().st_size < 200:
                continue
            
            related = find_links(f, doc_tokens, idf, files, top_n=5)
            if not related:
                continue
            
            rel_names = [r.stem[:40] for r in related]
            if not dry_run:
                changed = add_links_to_file(f, related)
                if changed:
                    linked += 1
                    total_links += len(related)
                    if linked <= 10 or linked % 100 == 0:
                        print(f"  [{linked}] {f.name[:50]} → {len(related)} links: {', '.join(rel_names[:3])}")
        except Exception as e:
            pass
    
    print(f"\nLinked: {linked} files with {total_links} total links")
    return linked, total_links

if __name__ == "__main__":
    link_engine(dry_run="--dry-run" in sys.argv)
