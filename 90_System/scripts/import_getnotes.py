#!/usr/bin/env python3
"""
Get 笔记 Import Pipeline
Imports notes from Get 笔记 (Get Notes by ByteDance) exports into Obsidian.

Supports:
- Markdown file exports (batch .md files)
- ZIP archives containing Markdown files
- Direct directory watching

Usage:
    python import_getnotes.py --source ./getnotes_export/       # Import from directory
    python import_getnotes.py --source ./export.zip             # Import from ZIP
    python import_getnotes.py --watch ./getnotes_watch/         # Watch directory for new exports
"""

import os
import sys
import re
import json
import shutil
import zipfile
import hashlib
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import List, Optional

import yaml
import frontmatter


# ============================================================================
# Configuration
# ============================================================================

DEFAULT_CONFIG = {
    "inbox_dir": "00_Inbox",
    "processed_dir": "90_System/imports_processed",
    "supported_extensions": [".md", ".markdown", ".txt", ".html"],
    "cleanup": {
        "remove_empty_notes": True,
        "min_content_length": 50,
        "normalize_whitespace": True,
        "extract_pure_text": True,
        "remove_base64_images": True,
        "remove_script_tags": True,
    },
    "naming": {
        "prefix": "",  # Optional prefix like "GetNotes-"
        "use_date_prefix": True,
        "date_format": "%Y%m%d",
        "max_filename_length": 100,
    },
    "tags": {
        "auto_add": ["from-getnotes", "inbox"],
        "preserve_existing": True,
    }
}




# ============================================================================
# Content Filtering: Diary exclusion + TCC/iNEST inclusion
# ============================================================================

DIARY_KEYWORDS = [
    "日记", "日志", "周记", "备忘",
    "todo", "TODO", "购物清单",
    "今天天气", "今天吃了", "今天去了", "今天买",
    "健身", "跑步", "游泳", "瑜伽", "锻炼",
    "做饭", "菜谱", "美食", "餐厅",
    "旅游", "酒店", "机票", "火车票",
    "购物", "淘宝", "京东", "拼多多", "快递",
    "账单", "工资", "理财", "基金", "股票", "保险",
    "孩子", "家长会", "幼儿园", "学校", "作业",
    "医院", "挂号", "体检", "看病",
    "朋友圈", "抖音", "微博", "小红书", "刷手机",
    "心情", "情绪", "焦虑", "失眠", "冥想",
]

TCC_INEST_KEYWORDS = [
    "tcc", "inest", "拓扑", "拓扑中心计算", "cst", "sdi",
    "sdsow", "metatopology", "sdi-cc",
    "神经形态", "类脑", "脉冲神经网络", "snn", "stdp",
    "自由能", "fep", "变分", "bayesian", "主动推理",
    "忆阻器", "memristor", "异步电路", "aer",
    "自组织", "临界", "小世界", "连接组", "connectome",
    "复杂网络", "涌现", "标度律", "幂律",
    "神经计算", "脑启发", "brain-inspired", "neuromorphic",
    "晶圆级", "chiplet", "存算一体", "3d堆叠",
    "c.elegans", "线虫", "drosophila", "斑马鱼",
    "risc-v", "fpga", "asic",
    "路由算法", "片上网络", "noc", "network-on-chip",
    "spike", "event-driven", "事件驱动",
    "神经", "脑", "海马", "皮层", "突触",
    "nature", "science", "cell", "论文", "科研",
    "深度学习", "transformer", "大模型", "gpt",
    "codex", "claude", "agent",
    "学习规则", "可塑性", "plasticity",
    "连接", "环路", "circuit",
]

def is_diary_content(text: str) -> bool:
    text_lower = text.lower()
    for kw in DIARY_KEYWORDS:
        if kw.lower() in text_lower:
            return True
    return False

def is_tcc_inest_content(text: str) -> bool:
    text_lower = text.lower()
    for kw in TCC_INEST_KEYWORDS:
        if kw.lower() in text_lower:
            return True
    return False

def load_config(config_path: str = None) -> dict:
    """Load configuration, merging with defaults."""
    config = DEFAULT_CONFIG.copy()
    
    if config_path and Path(config_path).exists():
        with open(config_path, "r", encoding="utf-8") as f:
            user_config = yaml.safe_load(f)
        if user_config:
            _deep_merge(config, user_config)
    
    return config


def _deep_merge(base: dict, override: dict):
    """Deep merge two dictionaries."""
    for key, value in override.items():
        if key in base and isinstance(base[key], dict) and isinstance(value, dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value


# ============================================================================
# Note Extraction
# ============================================================================

def extract_notes_from_directory(source_dir: str, config: dict) -> List[dict]:
    """Extract notes from a directory of files."""
    notes = []
    source_path = Path(source_dir)
    
    if not source_path.exists():
        print(f"❌ Source directory not found: {source_dir}")
        return notes
    
    for ext in config["supported_extensions"]:
        for file_path in source_path.rglob(f"*{ext}"):
            note_data = _extract_single_note(file_path, config)
            if note_data:
                notes.append(note_data)
    
    return notes


def extract_notes_from_zip(zip_path: str, config: dict) -> List[dict]:
    """Extract notes from a ZIP archive."""
    notes = []
    zip_path = Path(zip_path)
    
    if not zip_path.exists():
        print(f"❌ ZIP file not found: {zip_path}")
        return notes
    
    # Extract to temp directory
    temp_dir = zip_path.parent / f"_temp_import_{int(time.time())}"
    temp_dir.mkdir(exist_ok=True)
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as zf:
            zf.extractall(temp_dir)
        
        notes = extract_notes_from_directory(str(temp_dir), config)
    finally:
        # Cleanup temp
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    return notes


def _extract_single_note(file_path: Path, config: dict) -> Optional[dict]:
    """Extract and clean a single note."""
    try:
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            raw_content = f.read()
    except Exception as e:
        print(f"  ⚠️  Could not read {file_path}: {e}")
        return None
    
    # Skip diary / personal content immediately
    if is_diary_content(raw_content):
        return None
    
    # Skip content not related to TCC/iNEST
    if not is_tcc_inest_content(raw_content):
        return None
    
    # Skip empty or very short content
    if len(raw_content.strip()) < config["cleanup"]["min_content_length"]:
        return None
    
    # Clean content
    cleaned_content = clean_note_content(raw_content, config)
    
    if len(cleaned_content.strip()) < config["cleanup"]["min_content_length"]:
        return None
    
    # Generate filename
    filename = generate_filename(cleaned_content, file_path, config)
    
    # Build frontmatter
    metadata = {
        "tags": config["tags"]["auto_add"].copy(),
        "source": "get-notes",
        "original_file": file_path.name,
        "imported": datetime.now().isoformat(),
    }
    
    # Try to extract title from content
    title = extract_title(cleaned_content)
    if title:
        metadata["title"] = title
    
    # Try to extract original date
    orig_date = extract_date(cleaned_content, file_path)
    if orig_date:
        metadata["date"] = orig_date
        metadata["created"] = orig_date
    
    return {
        "filename": filename,
        "content": cleaned_content,
        "metadata": metadata,
        "source_path": str(file_path),
    }


# ============================================================================
# Content Cleaning
# ============================================================================

def clean_note_content(raw_content: str, config: dict) -> str:
    """Clean and normalize note content."""
    content = raw_content
    
    if config["cleanup"]["remove_script_tags"]:
        # Remove <script> tags and their content
        content = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
        # Remove <style> tags
        content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
    
    if config["cleanup"]["remove_base64_images"]:
        # Remove base64 embedded images
        content = re.sub(r'!\[.*?\]\(data:image/[^;]+;base64,[^)]+\)', '', content)
        content = re.sub(r'<img[^>]+src="data:image/[^"]+"[^>]*>', '', content, flags=re.IGNORECASE)
    
    if config["cleanup"]["extract_pure_text"]:
        # Convert HTML to plain text (basic)
        # Remove HTML tags but keep line breaks
        content = re.sub(r'<br\s*/?>', '\n', content, flags=re.IGNORECASE)
        content = re.sub(r'</p>', '\n\n', content, flags=re.IGNORECASE)
        content = re.sub(r'</div>', '\n', content, flags=re.IGNORECASE)
        content = re.sub(r'<[^>]+>', '', content)
        # Decode common HTML entities
        content = content.replace('&nbsp;', ' ')
        content = content.replace('&amp;', '&')
        content = content.replace('&lt;', '<')
        content = content.replace('&gt;', '>')
        content = content.replace('&quot;', '"')
        content = content.replace('&#39;', "'")
    
    if config["cleanup"]["normalize_whitespace"]:
        # Normalize line endings
        content = content.replace('\r\n', '\n').replace('\r', '\n')
        # Remove excessive blank lines
        content = re.sub(r'\n{4,}', '\n\n\n', content)
        # Remove trailing whitespace
        content = '\n'.join(line.rstrip() for line in content.split('\n'))
    
    return content.strip()


def extract_title(content: str) -> Optional[str]:
    """Try to extract a title from the note content."""
    # Look for Markdown heading
    match = re.search(r'^#\s+(.+?)(?:\s*#+)?$', content, re.MULTILINE)
    if match:
        title = match.group(1).strip()
        # Remove markdown formatting
        title = re.sub(r'[*_~`]', '', title)
        if len(title) <= 100:
            return title
    
    # Use first non-empty line as title
    lines = [l.strip() for l in content.split('\n') if l.strip()]
    if lines:
        first_line = re.sub(r'^#+\s*', '', lines[0])
        first_line = re.sub(r'[*_~`]', '', first_line)
        if len(first_line) <= 80:
            return first_line
    
    return None


def extract_date(content: str, file_path: Path) -> Optional[str]:
    """Try to extract a date from content or filename."""
    # Look for date patterns in content
    date_patterns = [
        r'(\d{4}[-/]\d{2}[-/]\d{2})',  # 2024-01-15 or 2024/01/15
        r'(\d{4}年\d{1,2}月\d{1,2}日)',  # 2024年1月15日
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, content[:500])
        if match:
            date_str = match.group(1)
            # Normalize to ISO format
            date_str = date_str.replace('/', '-').replace('年', '-').replace('月', '-').replace('日', '')
            try:
                datetime.strptime(date_str[:10], "%Y-%m-%d")
                return date_str[:10]
            except ValueError:
                pass
    
    # Try from filename
    name = file_path.stem
    match = re.search(r'(\d{8})', name)  # YYYYMMDD
    if match:
        date_str = match.group(1)
        return f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
    
    return None


def generate_filename(content: str, original_path: Path, config: dict) -> str:
    """Generate a clean filename for the imported note."""
    naming = config["naming"]
    
    # Try to use title from content
    title = extract_title(content)
    if title:
        base_name = sanitize_filename(title, naming["max_filename_length"])
    else:
        base_name = sanitize_filename(original_path.stem, naming["max_filename_length"])
    
    # Add prefix
    if naming["prefix"]:
        base_name = f"{naming['prefix']}{base_name}"
    
    # Add date prefix
    if naming["use_date_prefix"]:
        date_str = extract_date(content, original_path)
        if date_str:
            date_prefix = date_str.replace('-', '')
            base_name = f"{date_prefix}_{base_name}"
        else:
            today = datetime.now().strftime(naming["date_format"])
            base_name = f"{today}_{base_name}"
    
    return f"{base_name}.md"


def sanitize_filename(name: str, max_length: int = 100) -> str:
    """Sanitize a string to be a valid filename."""
    invalid_chars = r'[<>:"/\\|?*\n\r\t]'
    name = re.sub(invalid_chars, '-', name)
    name = re.sub(r'\.+$', '', name)
    name = name.strip(' .-')
    
    if len(name) > max_length:
        name = name[:max_length].rstrip(' .-')
    
    return name or "untitled_note"


# ============================================================================
# Import to Obsidian
# ============================================================================

def import_notes_to_obsidian(notes: List[dict], vault_root: str, config: dict, dry_run: bool = False):
    """Import cleaned notes into the Obsidian vault."""
    inbox_dir = Path(vault_root) / config["inbox_dir"]
    inbox_dir.mkdir(parents=True, exist_ok=True)
    
    imported_count = 0
    skipped_count = 0
    
    for note in notes:
        target_path = inbox_dir / note["filename"]
        
        # Check if already imported (by content hash)
        content_hash = hashlib.md5(note["content"].encode()).hexdigest()
        
        if target_path.exists():
            # Check if same content
            with open(target_path, "r", encoding="utf-8") as f:
                existing = f.read()
            existing_hash = hashlib.md5(existing.encode()).hexdigest()
            
            if existing_hash == content_hash:
                skipped_count += 1
                continue
            
            # Different content - add suffix
            stem = target_path.stem
            suffix = target_path.suffix
            counter = 1
            while target_path.exists():
                target_path = inbox_dir / f"{stem}_{counter}{suffix}"
                counter += 1
        
        if dry_run:
            print(f"  [DRY-RUN] Would import: {target_path.name}")
            imported_count += 1
            continue
        
        # Build final note with frontmatter
        post = frontmatter.Post(note["content"], **note["metadata"])
        final_content = frontmatter.dumps(post)
        
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(final_content)
        
        imported_count += 1
    
    print(f"\n📥 Import complete: {imported_count} imported, {skipped_count} skipped (duplicates)")
    return imported_count


# ============================================================================
# Directory Watcher
# ============================================================================

def watch_directory(source_dir: str, vault_root: str, config: dict, interval: int = 60):
    """Watch a directory for new Get 笔记 exports and import them."""
    print(f"👀 Watching {source_dir} for new exports (checking every {interval}s)...")
    print(f"   Press Ctrl+C to stop.")
    
    processed_dir = Path(vault_root) / config.get("processed_dir", "90_System/imports_processed")
    processed_dir.mkdir(parents=True, exist_ok=True)
    
    known_files = set()
    
    # Initialize with existing files
    for ext in config["supported_extensions"]:
        for f in Path(source_dir).rglob(f"*{ext}"):
            known_files.add(str(f))
    
    try:
        while True:
            current_files = set()
            new_files = []
            
            for ext in config["supported_extensions"]:
                for f in Path(source_dir).rglob(f"*{ext}"):
                    fp = str(f)
                    current_files.add(fp)
                    if fp not in known_files:
                        new_files.append(f)
            
            if new_files:
                print(f"\n🆕 Found {len(new_files)} new file(s) at {datetime.now().strftime('%H:%M:%S')}")
                notes = []
                for f in new_files:
                    note_data = _extract_single_note(f, config)
                    if note_data:
                        notes.append(note_data)
                
                if notes:
                    import_notes_to_obsidian(notes, vault_root, config)
            
            known_files = current_files
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n👋 Stopped watching.")


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Get 笔记 Import Pipeline for Obsidian"
    )
    parser.add_argument("--source", help="Source directory or ZIP file containing Get 笔记 exports")
    parser.add_argument("--vault", default=".", help="Obsidian vault root directory")
    parser.add_argument("--config", default="90_System/scripts/config_getnotes.yaml", help="Config file path")
    parser.add_argument("--watch", action="store_true", help="Watch source directory for new exports")
    parser.add_argument("--interval", type=int, default=60, help="Watch interval in seconds")
    parser.add_argument("--dry-run", action="store_true", help="Preview without importing")
    parser.add_argument("--inbox", default="00_Inbox", help="Inbox directory name")
    
    args = parser.parse_args()
    
    # Load config
    config = load_config(args.config)
    if args.inbox:
        config["inbox_dir"] = args.inbox
    
    vault_root = args.vault
    
    print("=" * 60)
    print("📥 Get 笔记 Import Pipeline")
    print("=" * 60)
    
    if args.watch:
        if not args.source:
            print("❌ --watch requires --source to specify the directory to watch.")
            sys.exit(1)
        watch_directory(args.source, vault_root, config, args.interval)
        return
    
    if not args.source:
        print("Usage examples:")
        print("  python import_getnotes.py --source ./getnotes_export/")
        print("  python import_getnotes.py --source ./export.zip")
        print("  python import_getnotes.py --source ./getnotes_watch/ --watch")
        sys.exit(0)
    
    # Determine source type
    source_path = Path(args.source)
    
    if not source_path.exists():
        print(f"❌ Source not found: {args.source}")
        sys.exit(1)
    
    if source_path.suffix.lower() == '.zip':
        print(f"📦 Extracting from ZIP: {source_path}")
        notes = extract_notes_from_zip(str(source_path), config)
    else:
        print(f"📂 Scanning directory: {source_path}")
        notes = extract_notes_from_directory(str(source_path), config)
    
    if not notes:
        print("No valid notes found to import.")
        return
    
    print(f"   Found {len(notes)} notes to import.")
    import_notes_to_obsidian(notes, vault_root, config, dry_run=args.dry_run)
    
    print("\n✅ Done! Run 'python reorganize.py --process-inbox' to categorize imported notes.")


if __name__ == "__main__":
    main()
