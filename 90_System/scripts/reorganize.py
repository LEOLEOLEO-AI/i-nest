#!/usr/bin/env python3
"""
Obsidian Knowledge Base Reorganizer (Karpathy Wiki LLM Style)
Uses DeepSeek API to auto-categorize, tag, link, and organize notes.

Usage:
    python reorganize.py                    # Full reorganization of Zettelkasten
    python reorganize.py --dry-run          # Preview changes without modifying files
    python reorganize.py --process-inbox    # Process inbox notes only
    python reorganize.py --update-moc       # Only update MOC pages
    python reorganize.py --dedup            # Only check for duplicates
"""

import os
import sys
import re
import json
import yaml
import hashlib
import shutil
import time
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

import frontmatter
from openai import OpenAI
from tqdm import tqdm
import networkx as nx
import numpy as np


# ============================================================================
# Configuration
# ============================================================================

def load_config(config_path="90_System/scripts/config.yaml"):
    """Load configuration from YAML file."""
    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    # Resolve API key from environment variable if using placeholder
    llm_config = config.get("llm", config.get("deepseek", {}))
    api_key = llm_config.get("api_key", "")
    if api_key.startswith("${") and api_key.endswith("}"):
        env_var = api_key[2:-1]
        llm_config["api_key"] = os.environ.get(env_var, "")
    
    return config


def setup_llm_client(config):
    """Initialize LLM API client (OpenAI-compatible, supports OpenRouter and DeepSeek)."""
    llm_config = config.get("llm", config.get("deepseek", {}))
    api_key = llm_config.get("api_key", "")
    base_url = llm_config.get("base_url", "https://api.deepseek.com")
    provider = llm_config.get("provider", "deepseek")
    
    # Try auto-detecting API key from various sources
    if not api_key or api_key.startswith("${"):
        env_var = api_key[2:-1] if api_key.startswith("${") else "DEEPSEEK_API_KEY"
        api_key = os.environ.get(env_var, "")
    
    if not api_key:
        # Try from .neural_memory/.env
        env_path = Path(".neural_memory/.env")
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("DEEPSEEK_API_KEY="):
                        api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                    elif line.startswith("OPENAI_API_KEY="):
                        api_key = line.split("=", 1)[1].strip().strip('"').strip("'")
    
    if not api_key:
        # Try from neural-composer plugin data.json (nested in providers array)
        nc_data = Path(".obsidian/plugins/neural-composer/data.json")
        if nc_data.exists():
            try:
                with open(nc_data) as f:
                    nc = json.load(f)
                # Search providers array for apiKey
                for p in nc.get("providers", []):
                    key = p.get("apiKey", "")
                    if key and len(key) > 10:
                        api_key = key
                        base_url = p.get("baseUrl", "https://openrouter.ai/api/v1")
                        provider = "openrouter"
                        break
                if not api_key:
                    api_key = nc.get("apiKey", "") or nc.get("openAIApiKey", "")
            except Exception:
                pass
    
    if not api_key:
        # Try from copilot plugin data.json
        cp_data = Path(".obsidian/plugins/copilot/data.json")
        if cp_data.exists():
            try:
                with open(cp_data) as f:
                    cp = json.load(f)
                api_key = cp.get("openAIApiKey", "")
            except Exception:
                pass
    
    if not api_key:
        print("Warning: No API key found. Set DEEPSEEK_API_KEY env variable or configure in neural-composer.")
        return None
    
    print(f"   Provider: {provider} | Model: {llm_config.get('model', 'unknown')}")
    return OpenAI(api_key=api_key, base_url=base_url)


# ============================================================================
# Note Analysis with DeepSeek
# ============================================================================

NOTE_ANALYSIS_PROMPT = """你是一个知识库管理助手。请分析以下笔记内容，返回 JSON 格式的分析结果。

笔记内容:
---
{content}
---

请返回 JSON（只返回 JSON，不要其他文字）:
{{
  "title_cn": "中文标题（简洁，不超过30字）",
  "title_en": "English title (concise, max 15 words)",
  "summary": "一句话摘要（中文，不超过50字）",
  "category": "主题分类，从以下选一个: AI-ML, Neuroscience, Chip-Hardware, TCC-SDI, Research-Methods, Papers, Project-Management, Tools-Tutorials, Concepts-Theory, Web-Clips",
  "tags": ["标签1", "标签2", "标签3"],
  "quality": "high/medium/low",
  "is_duplicate_likely": false,
  "key_entities": ["关键概念/术语1", "关键概念/术语2"]
}}"""


def analyze_note(client, content, model="deepseek-reasoner", max_retries=3):
    """Analyze a note using DeepSeek API to extract metadata."""
    # Truncate content if too long (~4000 chars for context)
    truncated = content[:4000] if len(content) > 4000 else content
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "你是一个知识库管理助手。请只返回有效的 JSON，不要添加任何解释。"},
                    {"role": "user", "content": NOTE_ANALYSIS_PROMPT.format(content=truncated)}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Extract JSON from the response (handle markdown code blocks)
            json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', result_text, re.DOTALL)
            if json_match:
                result_text = json_match.group(1)
            
            # Try to find JSON object
            json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
            if json_match:
                result_text = json_match.group(0)
            
            result = json.loads(result_text)
            return result
            
        except (json.JSONDecodeError, Exception) as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                print(f"  Failed to analyze note after {max_retries} attempts: {e}")
                # Return a basic fallback result
                return {
                    "title_cn": "Untitled",
                    "title_en": "Untitled",
                    "summary": content[:50].replace("\n", " ") + "...",
                    "category": "Web-Clips",
                    "tags": ["needs-review"],
                    "quality": "low",
                    "is_duplicate_likely": False,
                    "key_entities": []
                }
    
    return None


def get_embedding(client, text, model="text-embedding-3-small"):
    """Get embedding vector for text using DeepSeek-compatible API."""
    try:
        response = client.embeddings.create(
            model=model,
            input=text[:8000]  # Truncate to token limit
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"  Embedding error: {e}")
        return None


# ============================================================================
# Note Scanning & Processing
# ============================================================================

def scan_notes(directories, vault_root="."):
    """Scan directories for Markdown files, return list of note paths."""
    notes = []
    for dir_name in directories:
        dir_path = Path(vault_root) / dir_name
        if dir_path.exists():
            for md_file in dir_path.rglob("*.md"):
                notes.append(md_file)
    return notes


def read_note(filepath):
    """Read a note file, returning frontmatter metadata and content."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            post = frontmatter.load(f)
        return post
    except Exception as e:
        print(f"  Error reading {filepath}: {e}")
        return None


def extract_text_content(post):
    """Extract meaningful text content from a note for analysis."""
    content = post.content
    
    # Remove Obsidian-specific syntax for cleaner analysis
    # Remove wikilinks but keep link text
    content = re.sub(r'\[\[(.*?)\]\]', r'\1', content)
    # Remove markdown links but keep text
    content = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', content)
    # Remove images
    content = re.sub(r'!\[.*?\]\(.*?\)', '', content)
    # Remove code blocks
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
    # Remove HTML tags
    content = re.sub(r'<[^>]+>', '', content)
    # Collapse whitespace
    content = re.sub(r'\n\s*\n', '\n\n', content)
    
    return content.strip()


def sanitize_filename(name, max_length=80):
    """Sanitize a string to be a valid filename."""
    # Remove characters invalid for Windows filenames
    invalid_chars = r'[<>:"/\\|?*]'
    name = re.sub(invalid_chars, '-', name)
    # Remove leading/trailing spaces and dots
    name = name.strip(' .')
    # Truncate
    if len(name) > max_length:
        name = name[:max_length]
    return name or "untitled"


def build_note_metadata(post, analysis, filepath):
    """Build updated frontmatter metadata for a note."""
    metadata = dict(post.metadata) if post.metadata else {}
    
    # Add/update analysis fields
    if analysis:
        if not metadata.get("title") and analysis.get("title_cn"):
            metadata["title"] = analysis["title_cn"]
        if analysis.get("tags"):
            existing_tags = metadata.get("tags", [])
            if isinstance(existing_tags, str):
                existing_tags = [t.strip() for t in existing_tags.split(",")]
            new_tags = list(set(existing_tags + analysis["tags"]))
            metadata["tags"] = new_tags
        if analysis.get("category"):
            metadata["category"] = analysis["category"]
        if analysis.get("summary"):
            metadata["summary"] = analysis["summary"]
        if analysis.get("key_entities"):
            metadata["entities"] = analysis["key_entities"]
    
    # Add processing metadata
    metadata["processed"] = datetime.now().isoformat()
    metadata["source_file"] = str(filepath.name)
    
    return metadata


# ============================================================================
# File Operations
# ============================================================================

def move_note_to_topic(filepath, category, topics_dir="03_Topics", dry_run=False):
    """Move a note to its topic directory under 03_Topics/."""
    if not category:
        return None
    
    target_dir = Path(topics_dir) / category
    if dry_run:
        return target_dir / filepath.name
    
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / filepath.name
    
    # Handle filename conflicts
    if target_path.exists() and target_path != filepath:
        stem = target_path.stem
        suffix = target_path.suffix
        counter = 1
        while target_path.exists():
            target_path = target_dir / f"{stem}_{counter}{suffix}"
            counter += 1
    
    if target_path != filepath:
        shutil.move(str(filepath), str(target_path))
    
    return target_path


def update_note_frontmatter(filepath, metadata, content, dry_run=False):
    """Update a note's frontmatter and content."""
    post = frontmatter.Post(content, **metadata)
    new_content = frontmatter.dumps(post)
    
    if dry_run:
        return new_content
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)


def add_backlinks(note_path, related_notes, max_links=3, dry_run=False):
    """Add [[wikilinks]] to related notes at the bottom of a note."""
    if not related_notes:
        return
    
    try:
        with open(note_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return
    
    # Check if "Related" section already exists
    if "## Related" in content or "## 相关笔记" in content:
        return
    
    # Build link section
    link_lines = ["\n---\n## 相关笔记 (AI 自动关联)\n"]
    for i, related in enumerate(related_notes[:max_links]):
        note_name = Path(related).stem
        link_lines.append(f"- [[{note_name}]]\n")
    
    new_content = content.rstrip() + "\n" + "".join(link_lines)
    
    if dry_run:
        return new_content
    
    with open(note_path, "w", encoding="utf-8") as f:
        f.write(new_content)


# ============================================================================
# Semantic Linking with NetworkX
# ============================================================================

def build_semantic_graph(notes_metadata, embeddings):
    """Build a NetworkX graph connecting notes based on embedding similarity."""
    G = nx.Graph()
    
    # Add nodes
    for filepath, meta in notes_metadata.items():
        G.add_node(str(filepath), **meta)
    
    # Add edges for similar notes
    filepaths = list(notes_metadata.keys())
    for i in range(len(filepaths)):
        for j in range(i + 1, len(filepaths)):
            fp_i, fp_j = filepaths[i], filepaths[j]
            emb_i = embeddings.get(str(fp_i))
            emb_j = embeddings.get(str(fp_j))
            
            if emb_i and emb_j:
                similarity = cosine_similarity(emb_i, emb_j)
                if similarity > 0.75:  # High similarity threshold for linking
                    G.add_edge(str(fp_i), str(fp_j), weight=similarity)
    
    return G


def cosine_similarity(a, b):
    """Compute cosine similarity between two vectors."""
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def find_related_notes(G, filepath, max_results=3):
    """Find the most related notes for a given note using the graph."""
    node = str(filepath)
    if node not in G:
        return []
    
    neighbors = sorted(
        G.neighbors(node),
        key=lambda n: G[node][n].get("weight", 0),
        reverse=True
    )
    return neighbors[:max_results]


# ============================================================================
# MOC (Map of Content) Management
# ============================================================================

def update_moc_pages(notes_by_category, moc_dir="01_MOC", dry_run=False):
    """Update or create MOC pages for each topic category."""
    moc_path = Path(moc_dir)
    moc_path.mkdir(parents=True, exist_ok=True)
    
    for category, notes in notes_by_category.items():
        _update_single_moc(category, notes, moc_path, dry_run)


def _update_single_moc(category, notes, moc_path, dry_run):
    """Update a single MOC page for a category."""
    moc_file = moc_path / f"{category}-MOC.md"
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Build MOC content
    lines = [
        f"# {category} — 全景导航 (Map of Content)",
        "",
        f"> 自动生成 | 最后更新: {now}",
        f"> 包含 {len(notes)} 条笔记",
        "",
        "---",
        "",
        "## [MOC] 笔记索引",
        ""
    ]
    
    for note_path in sorted(notes):
        note_name = note_path.stem
        lines.append(f"- [[{note_name}]]")
    
    lines.extend([
        "",
        "---",
        "",
        "## 📊 统计",
        "",
        f"- 笔记总数: {len(notes)}",
        f"- 生成时间: {now}",
    ])
    
    content = "\n".join(lines) + "\n"
    
    if dry_run:
        print(f"  [DRY-RUN] Would update MOC: {moc_file}")
        return
    
    with open(moc_file, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"  Updated MOC: {moc_file}")


# ============================================================================
# Deduplication
# ============================================================================

def check_duplicates(notes_data, embeddings, threshold=0.85, dry_run=False):
    """Check for duplicate/similar notes and mark them."""
    duplicates = []
    filepaths = list(notes_data.keys())
    
    for i in range(len(filepaths)):
        for j in range(i + 1, len(filepaths)):
            fp_i, fp_j = filepaths[i], filepaths[j]
            emb_i = embeddings.get(str(fp_i))
            emb_j = embeddings.get(str(fp_j))
            
            if emb_i and emb_j:
                similarity = cosine_similarity(emb_i, emb_j)
                if similarity > threshold:
                    duplicates.append((fp_i, fp_j, similarity))
    
    # Sort by similarity (highest first)
    duplicates.sort(key=lambda x: x[2], reverse=True)
    
    if dry_run:
        print(f"\n  [DRY-RUN] Found {len(duplicates)} potential duplicate pairs:")
        for fp_i, fp_j, sim in duplicates[:20]:
            print(f"    {sim:.3f}: {fp_i.name} <-> {fp_j.name}")
        if len(duplicates) > 20:
            print(f"    ... and {len(duplicates) - 20} more pairs")
    
    return duplicates


def mark_duplicates(duplicates, notes_data, dry_run=False):
    """Mark lower-quality notes as potential duplicates of higher-quality ones."""
    quality_scores = {"high": 3, "medium": 2, "low": 1, None: 1}
    
    for fp_i, fp_j, similarity in sorted(duplicates, key=lambda x: x[2], reverse=True):
        qi = quality_scores.get(notes_data.get(fp_i, {}).get("quality"), 1)
        qj = quality_scores.get(notes_data.get(fp_j, {}).get("quality"), 1)
        
        # Lower quality note gets marked as duplicate of higher quality one
        if qi >= qj:
            better, worse = fp_i, fp_j
        else:
            better, worse = fp_j, fp_i
        
        # Add duplicate note to the worse note
        try:
            with open(worse, "r", encoding="utf-8") as f:
                content = f.read()
            
            dup_note = f"\n> [!note]- 可能重复: [[{better.stem}]] (相似度: {similarity:.0%})\n"
            
            if "可能重复" not in content:
                content = content.rstrip() + "\n" + dup_note
            
            if not dry_run:
                with open(worse, "w", encoding="utf-8") as f:
                    f.write(content)
        except Exception:
            pass


# ============================================================================
# Inbox Processing
# ============================================================================

def process_inbox(client, config, dry_run=False):
    """Process notes in the inbox directory."""
    inbox_dir = Path(config["paths"]["inbox_dir"])
    topics_dir = Path(config["paths"]["topics_dir"])
    
    if not inbox_dir.exists():
        print(f"Inbox directory {inbox_dir} not found.")
        return
    
    inbox_notes = list(inbox_dir.rglob("*.md"))
    print(f"\n[INBOX] Processing {len(inbox_notes)} inbox notes...")
    
    for note_path in tqdm(inbox_notes, desc="Inbox"):
        post = read_note(note_path)
        if not post:
            continue
        
        text = extract_text_content(post)
        if len(text) < 50:  # Skip very short notes
            print(f"  Skipping short note: {note_path.name}")
            continue
        
        # Analyze with DeepSeek
        analysis = analyze_note(client, text, config.get("llm", config.get("deepseek", {}))["model"])
        if not analysis:
            continue
        
        category = analysis.get("category", "Web-Clips")
        quality = analysis.get("quality", "medium")
        
        if quality == "low":
            # Add a tag to mark for review
            metadata = dict(post.metadata) if post.metadata else {}
            tags = metadata.get("tags", [])
            if isinstance(tags, str):
                tags = [t.strip() for t in tags.split(",")]
            tags.append("needs-review")
            metadata["tags"] = tags
            metadata["quality"] = "low"
            metadata["category"] = category
            update_note_frontmatter(note_path, metadata, post.content, dry_run)
            print(f"  [WARN]  Low quality: {note_path.name} -> {category}")
            continue
        
        # Build metadata and move
        metadata = build_note_metadata(post, analysis, note_path)
        update_note_frontmatter(note_path, metadata, post.content, dry_run)
        
        # Move to topic directory
        new_path = move_note_to_topic(note_path, category, str(topics_dir), dry_run)
        if new_path:
            print(f"  [OK] {note_path.name} -> {category}/")
    
    print(f"\nInbox processing complete.")


# ============================================================================
# Main Reorganization
# ============================================================================

def reorganize(config, client, dry_run=False, max_notes=0):
    """Main reorganization pipeline."""
    vault_root = Path(config["paths"]["vault_root"])
    zettel_dirs = config["paths"]["zettelkasten_dirs"]
    topics_dir = config["paths"]["topics_dir"]
    
    print(f"\n[SCAN] Scanning Zettelkasten directories: {zettel_dirs}")
    notes = scan_notes(zettel_dirs, vault_root)
    print(f"   Found {len(notes)} notes to process.")
    
    if max_notes and max_notes > 0 and len(notes) > max_notes:
        print(f"   Limiting to {max_notes} notes (--max-notes)")
        notes = notes[:max_notes]
    
    if not notes:
        print("No notes found. Exiting.")
        return
    
    # Phase 1: Analyze all notes
    print(f"\n[ANALYZE] Phase 1: Analyzing notes with DeepSeek...")
    notes_metadata = {}
    embeddings = {}
    notes_by_category = defaultdict(list)
    
    batch_size = config["processing"]["batch_size"]
    
    for i in tqdm(range(0, len(notes), batch_size), desc="Analyzing"):
        batch = notes[i:i + batch_size]
        
        with ThreadPoolExecutor(max_workers=config["processing"]["max_workers"]) as executor:
            futures = {}
            for note_path in batch:
                futures[executor.submit(_analyze_single_note, note_path, client, config)] = note_path
            
            for future in as_completed(futures):
                note_path = futures[future]
                try:
                    result = future.result()
                    if result:
                        notes_metadata[note_path] = result["metadata"]
                        if result["embedding"]:
                            embeddings[str(note_path)] = result["embedding"]
                        cat = result["metadata"].get("category", "Web-Clips")
                        notes_by_category[cat].append(note_path)
                except Exception as e:
                    print(f"  Error processing {note_path.name}: {e}")
    
    print(f"\n   Analyzed {len(notes_metadata)}/{len(notes)} notes.")
    print(f"   Categories: {dict((k, len(v)) for k, v in notes_by_category.items())}")
    
    # Phase 2: Build semantic graph for linking
    print(f"\n[LINK] Phase 2: Building semantic link graph...")
    G = build_semantic_graph(notes_metadata, embeddings)
    print(f"   Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
    
    # Phase 3: Move notes to topic directories
    print(f"\n[MOVE] Phase 3: Moving notes to topic directories...")
    for category, cat_notes in tqdm(notes_by_category.items(), desc="Moving"):
        for note_path in cat_notes:
            move_note_to_topic(note_path, category, topics_dir, dry_run)
    
    # Phase 4: Add backlinks
    print(f"\n[LINK] Phase 4: Adding semantic backlinks...")
    for note_path in tqdm(list(notes_metadata.keys()), desc="Linking"):
        if note_path.exists():  # Note may have been moved
            related = find_related_notes(G, str(note_path), config["processing"]["max_links_per_note"])
            if related:
                add_backlinks(note_path, [Path(r) for r in related], config["processing"]["max_links_per_note"], dry_run)
    
    # Phase 5: Update MOC pages
    print(f"\n[MOC] Phase 5: Updating MOC pages...")
    update_moc_pages(notes_by_category, config["paths"]["moc_dir"], dry_run)
    
    # Phase 6: Deduplication check (skip if no embeddings)
    print(f"\n[SCAN] Phase 6: Checking for duplicates...")
    duplicates = check_duplicates(notes_metadata, embeddings, config["processing"]["dedup_threshold"], dry_run)
    if duplicates and not dry_run:
        mark_duplicates(duplicates, notes_metadata, dry_run)
    
    print(f"\n[OK] Reorganization complete!")
    print(f"   Notes processed: {len(notes_metadata)}")
    print(f"   Categories created: {len(notes_by_category)}")
    print(f"   Duplicates found: {len(duplicates)}")
    print(f"   Graph connections: {G.number_of_edges()}")


def _analyze_single_note(note_path, client, config):
    """Analyze a single note - used by ThreadPoolExecutor."""
    post = read_note(note_path)
    if not post:
        return None
    
    text = extract_text_content(post)
    if len(text) < 30:
        return None
    
    # Analyze with DeepSeek
    analysis = analyze_note(client, text, config.get("llm", config.get("deepseek", {}))["model"])
    if not analysis:
        return None
    
    # Get embedding for semantic search
    embedding = get_embedding(client, text[:2000], config.get("llm", config.get("deepseek", {}))["embedding_model"])
    
    # Build metadata
    metadata = build_note_metadata(post, analysis, note_path)
    
    return {
        "metadata": metadata,
        "embedding": embedding,
        "analysis": analysis
    }


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Obsidian Knowledge Base Reorganizer (Karpathy Wiki LLM Style)"
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without modifying files")
    parser.add_argument("--process-inbox", action="store_true", help="Process inbox notes only")
    parser.add_argument("--update-moc", action="store_true", help="Only update MOC pages")
    parser.add_argument("--dedup", action="store_true", help="Only check for duplicates")
    parser.add_argument("--config", default="90_System/scripts/config.yaml", help="Path to config file")
    parser.add_argument("--batch-size", type=int, default=10, help="Batch size for API calls")
    parser.add_argument("--max-notes", type=int, default=0, help="Max notes to process (0=all, for testing)")
    
    args = parser.parse_args()
    
    # Load config
    config = load_config(args.config)
    if args.batch_size:
        config["processing"]["batch_size"] = args.batch_size
    
    # Setup DeepSeek client
    client = setup_llm_client(config)
    if not client:
        print("❌ Cannot proceed without DeepSeek API key.")
        print("   Set DEEPSEEK_API_KEY environment variable or configure in config.yaml")
        sys.exit(1)
    
    print("=" * 60)
    print("Obsidian Knowledge Base Reorganizer")
    print("=" * 60)
    
    if args.process_inbox:
        process_inbox(client, config, dry_run=args.dry_run)
    elif args.dedup:
        # Dedup-only mode
        vault_root = Path(config["paths"]["vault_root"])
        zettel_dirs = config["paths"]["zettelkasten_dirs"]
        notes = scan_notes(zettel_dirs, vault_root)
        
        # Get embeddings for all notes
        embeddings = {}
        notes_metadata = {}
        for note_path in tqdm(notes, desc="Getting embeddings"):
            post = read_note(note_path)
            if post:
                text = extract_text_content(post)
                emb = get_embedding(client, text[:2000], config.get("llm", config.get("deepseek", {}))["embedding_model"])
                if emb:
                    embeddings[str(note_path)] = emb
                    notes_metadata[note_path] = dict(post.metadata) if post.metadata else {}
        
        duplicates = check_duplicates(notes_metadata, embeddings, 
                                      config["processing"]["dedup_threshold"], 
                                      dry_run=args.dry_run)
        if not args.dry_run:
            mark_duplicates(duplicates, notes_metadata, dry_run=False)
    elif args.update_moc:
        # MOC update only
        topics_dir = Path(config["paths"]["topics_dir"])
        notes_by_category = defaultdict(list)
        if topics_dir.exists():
            for cat_dir in topics_dir.iterdir():
                if cat_dir.is_dir():
                    notes_by_category[cat_dir.name] = list(cat_dir.rglob("*.md"))
        update_moc_pages(notes_by_category, config["paths"]["moc_dir"], dry_run=args.dry_run)
    else:
        # Full reorganization
        reorganize(config, client, dry_run=args.dry_run, max_notes=args.max_notes)
    
    print("\nDone!")


if __name__ == "__main__":
    main()







