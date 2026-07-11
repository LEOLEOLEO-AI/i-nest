#!/usr/bin/env python3
"""
iNEST Wiki 断链批量修复脚本
策略：构建全库文件名→实际路径映射，批量修正 [[旧路径]] → [[新路径]]
"""
import os, re
from pathlib import Path
from collections import defaultdict

VAULT = Path('/home/work/obsidian-vault')

def build_file_map():
    """建立 文件名(stem) → 实际相对路径 的映射"""
    file_map = {}       # stem → 最短相对路径（唯一）
    stem_count = defaultdict(list)

    for md in VAULT.rglob('*.md'):
        rel = md.relative_to(VAULT)
        parts = rel.parts
        if any(p.startswith('.') for p in parts):
            continue
        stem = md.stem
        stem_count[stem].append(str(rel))

    # 优先选择路径最短的（最顶层的）
    for stem, paths in stem_count.items():
        paths.sort(key=lambda p: (len(p.split('/')), p))
        file_map[stem] = paths[0]  # 最短路径

    return file_map, stem_count

def extract_link_target(link_text):
    """从 [[target|alias]] 或 [[target#section]] 中提取目标"""
    # 去掉 alias 和 section
    target = link_text.split('|')[0].split('#')[0].strip()
    return target

def fix_links_in_file(filepath, file_map, stem_count, dry_run=False):
    """修复单个文件中的断链"""
    text = filepath.read_text(errors='replace')
    all_md_stems = set(file_map.keys())

    # 找所有 [[...]] 链接
    pattern = re.compile(r'\[\[([^\]]+)\]\]')
    fixes = []
    new_text = text

    for m in pattern.finditer(text):
        full_link = m.group(0)
        inner = m.group(1)
        target = extract_link_target(inner)
        alias_part = ('|' + inner.split('|', 1)[1]) if '|' in inner else ''
        section_part = ('#' + inner.split('#', 1)[1].split('|')[0]) if '#' in inner else ''

        # 如果 target 是路径形式（含/），取最后一段作为 stem
        if '/' in target:
            stem = Path(target).stem
        else:
            stem = target

        # 跳过明显不是文件名的（单字符、纯数字等）
        if len(stem) <= 2:
            continue

        # 检查是否已存在（相对路径可以直接解析）
        abs_target = VAULT / (target + '.md')
        if abs_target.exists():
            continue  # 链接有效，跳过

        # 尝试通过 stem 找到正确路径
        if stem in all_md_stems:
            correct_rel = file_map[stem]
            correct_rel_no_ext = str(Path(correct_rel).with_suffix(''))

            # 如果当前链接和正确路径不同
            if target != correct_rel_no_ext and target != stem:
                new_link = f'[[{correct_rel_no_ext}{section_part}{alias_part}]]'
                fixes.append((full_link, new_link, stem))
                new_text = new_text.replace(full_link, new_link, 1)

    if fixes and not dry_run:
        filepath.write_text(new_text)

    return fixes

def main(dry_run=False):
    print(f'iNEST 断链修复工具 {"（预演模式）" if dry_run else "（执行模式）"}\n')
    print('建立文件映射...')
    file_map, stem_count = build_file_map()
    print(f'共索引 {len(file_map)} 个唯一文件名')

    # 重复文件名统计（同名文件有多个，链接有歧义）
    ambiguous = {s: ps for s, ps in stem_count.items() if len(ps) > 1}
    print(f'同名文件（有歧义）: {len(ambiguous)} 个')

    md_files = [f for f in VAULT.rglob('*.md')
                if not any(p.startswith('.') for p in f.relative_to(VAULT).parts)]
    print(f'扫描 {len(md_files)} 篇笔记...\n')

    total_fixes = 0
    fixed_files = 0

    for md in sorted(md_files):
        try:
            fixes = fix_links_in_file(md, file_map, stem_count, dry_run=dry_run)
            if fixes:
                rel = md.relative_to(VAULT)
                print(f'[{len(fixes)} 处] {rel}')
                for old, new, stem in fixes[:3]:
                    print(f'  {old[:60]} → {new[:60]}')
                if len(fixes) > 3:
                    print(f'  ...还有 {len(fixes)-3} 处')
                total_fixes += len(fixes)
                fixed_files += 1
        except Exception as e:
            pass

    print(f'\n{"预演" if dry_run else "修复"}完成:')
    print(f'  涉及文件: {fixed_files} 篇')
    print(f'  修复链接: {total_fixes} 处')

if __name__ == '__main__':
    import sys
    dry_run = '--dry-run' in sys.argv
    main(dry_run=dry_run)
