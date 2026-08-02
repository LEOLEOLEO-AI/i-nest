# -*- coding: utf-8 -*-
"""Fix getnote/GetNote wikilinks in file content after filename cleanup.

After renaming 648 files to strip getnote prefixes, the wikilinks INSIDE files
still reference the old names. This script:
1. Builds a mapping from old filenames (with prefix) → new filenames (without)
2. Scans all .md files and replaces [[getnote_*]] links with [[new_name]]
3. Respects Obsidian display aliases (preserves |display text)

Safety: DRY RUN by default; --apply to execute.
"""
import re
import sys
from pathlib import Path

VAULT = Path(r"D:/obsidian/vault")
APPLY = "--apply" in sys.argv
SKIP = {'.git', '.obsidian', '.workbuddy', 'node_modules', '__pycache__',
        '.smart-env', '.claudian', '.claudian-plus', '.neural_db', '_vendor'}

def skip(p):
    return any(s in p.relative_to(VAULT).parts for s in SKIP)


def build_rename_map():
    """Infer old→new name mapping from the files that got renamed.
    Gets the stem (no extension) mapping since wikilinks reference by note name."""
    mapping = {}  # old_stem → new_stem

    # For files in external_imports that had GetNote_ prefixes stripped
    ext = VAULT / "20_Processing" / "external_imports"
    if ext.exists():
        for f in ext.glob("GetNote_*.md"):
            name = f.stem
            # GetNote_20260606_100554_kb_iNEST_ActualTitle
            # → remove GetNote_DATETIME_kb_NAMESPACE_
            new = re.sub(r'^GetNote_\d{8}_\d{6}_kb_[A-Za-z-]+_', '', name)
            if new != name:
                mapping[name] = new

    return mapping


def fix_links(filepath, rename_map):
    """Replace getnote-prefixed wikilink targets with cleaned names."""
    txt = filepath.read_text(encoding='utf-8', errors='ignore')
    
    def replacer(m):
        full = m.group(1)  # everything inside [[...]]
        # Split target from display alias
        parts = full.split('|', 1)
        tgt = parts[0].split('#')[0].strip()
        rest = '|' + parts[1] if len(parts) > 1 else ''
        # Also preserve #heading anchors
        anchor = ''
        if '#' in parts[0]:
            anchor = '#' + parts[0].split('#', 1)[1]
        
        # Check if target is an old getnote filename
        if tgt in rename_map:
            new_tgt = rename_map[tgt]
            return f'[[{new_tgt}{anchor}{rest}]]'
        # Try stripping getnote_ prefix inline
        if 'getnote_' in tgt.lower():
            cleaned = re.sub(r'^(getnote_)+', '', tgt, flags=re.IGNORECASE)
            cleaned = re.sub(r'_getnote_\d{16,20}_', '_', cleaned)
            # Don't create broken links — only replace if we can verify
            # For now, strip the getnote prefix from the link target inline
            return f'[[{cleaned}{anchor}{rest}]]'
        if 'GetNote_' in tgt:
            cleaned = re.sub(r'^GetNote_\d{8}_\d{6}_', '', tgt)
            cleaned = re.sub(r'_getnote_\d{16,20}_', '_', cleaned)
            return f'[[{cleaned}{anchor}{rest}]]'
        return m.group(0)
    
    new_txt = re.sub(r'\[\[([^\]]+)\]\]', replacer, txt)
    return new_txt if new_txt != txt else None


def main():
    rename_map = build_rename_map()
    print(f"GetNote_ → 映射表: {len(rename_map)} entries")
    
    LINK_RE = re.compile(r'\[\[([^\]]+)\]\]')
    files_with_links = 0
    total_links = 0
    fixed = 0
    candidates = []
    
    # Phase 1: scan
    for f in VAULT.rglob("*.md"):
        if skip(f):
            continue
        try:
            txt = f.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            continue
        count = 0
        for m in LINK_RE.findall(txt):
            tgt = m.split('|')[0].split('#')[0].strip()
            if 'getnote' in tgt.lower() or 'GetNote' in tgt:
                count += 1
        if count > 0:
            total_links += count
            files_with_links += 1
            candidates.append((f, count))
    
    print(f"含旧链接文件: {files_with_links} | 旧链接总数: {total_links}")
    print()
    
    if APPLY:
        ok = fail = 0
        for fpath, _ in candidates:
            try:
                result = fix_links(fpath, rename_map)
                if result is not None:
                    fpath.write_text(result, encoding='utf-8')
                    ok += 1
            except Exception as e:
                print(f"  FAIL: {fpath.relative_to(VAULT)} — {e}")
                fail += 1
        print(f"修复: {ok} 文件 | 失败: {fail}")
    else:
        # Show samples of what would change
        for fpath, c in sorted(candidates, key=lambda x: -x[1])[:10]:
            print(f"  [{c}] {fpath.relative_to(VAULT)}")
        print()
        print(f"DRY RUN。共 {files_with_links} 文件含旧链接，加 --apply 批量修复。")


if __name__ == "__main__":
    main()
