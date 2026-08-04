#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""批量修复 camelCase ↔ underscore 断链：给 wiki/concepts/ 下的概念文件
自动添加 camelCase 别名到 frontmatter aliases 字段。

例如：
  Memristor_Crossbar_Array.md → 添加 alias: MemristorCrossbarArray
  Gamma_ST_Revision.md → 添加 alias: GammaSTRevision, GammaStRevision
"""
import re
from pathlib import Path

CONCEPTS_DIR = Path(r"D:/obsidian/vault/wiki/concepts")


def to_camelcase(name):
    """将 underscore_separated 名称转为 CamelCase。
    Memristor_Crossbar_Array → MemristorCrossbarArray
    Gamma_ST_Revision → GammaSTRevision
    """
    parts = name.split("_")
    return "".join(p[:1].upper() + p[1:] for p in parts if p)


def to_camelcase_lower_first(name):
    """Gamma_ST_Revision → GammaSt_Revision (首词保留原样, 后续词大写连接)
    这处理 GammaSt_Revision 这种半 camelCase 变体。
    """
    parts = name.split("_")
    if len(parts) <= 1:
        return None
    # 首词保留, 后续词首字母大写直接连接
    first = parts[0]
    rest = "".join(p[:1].upper() + p[1:] for p in parts[1:] if p)
    return first + rest


def extract_aliases(txt):
    """提取现有 aliases 列表。"""
    als = []
    if not txt.startswith("---"):
        return als, None
    end = txt.find("\n---", 3)
    if end == -1:
        return als, None
    fm = txt[3:end]
    in_alias = False
    alias_start = -1
    for i, ln in enumerate(fm.split("\n")):
        s = ln.strip()
        if s.startswith("aliases:"):
            in_alias = True
            alias_start = i
            continue
        if in_alias:
            if s.startswith("- "):
                v = s[2:].strip().strip('"').strip("'")
                if v:
                    als.append(v)
            elif s and not s.startswith("#"):
                in_alias = False
    return als, fm


def add_aliases_to_file(path, new_aliases):
    """给文件添加新别名（不重复）。返回是否修改。"""
    txt = path.read_text(encoding="utf-8", errors="ignore")
    existing, fm = extract_aliases(txt)
    if fm is None:
        # 无 frontmatter, 添加一个
        alias_lines = "\n".join(f'- "{a}"' for a in new_aliases)
        new_fm = f'---\naliases:\n{alias_lines}\n---\n'
        path.write_text(new_fm + txt, encoding="utf-8")
        return True

    to_add = [a for a in new_aliases if a not in existing and a != path.stem]
    if not to_add:
        return False

    # 在 frontmatter 中添加 aliases 字段或扩展
    if "aliases:" in txt[:500]:
        # 已有 aliases, 在最后一个 alias 后添加
        lines = txt.split("\n")
        in_alias = False
        last_alias_idx = -1
        for i, ln in enumerate(lines):
            s = ln.strip()
            if s.startswith("aliases:"):
                in_alias = True
                continue
            if in_alias:
                if s.startswith("- "):
                    last_alias_idx = i
                elif s and not s.startswith("#"):
                    in_alias = False

        if last_alias_idx >= 0:
            new_alias_lines = [f'- "{a}"' for a in to_add]
            lines.insert(last_alias_idx + 1, "\n".join(new_alias_lines))
            path.write_text("\n".join(lines), encoding="utf-8")
            return True
    else:
        # 无 aliases 字段, 在 frontmatter 开头添加
        end = txt.find("\n---", 3)
        if end != -1:
            alias_lines = "\n".join(f'- "{a}"' for a in to_add)
            insertion = f"\naliases:\n{alias_lines}"
            new_txt = txt[:end] + insertion + txt[end:]
            path.write_text(new_txt, encoding="utf-8")
            return True
    return False


def main():
    fixed = 0
    skipped = 0
    total = 0

    for md in CONCEPTS_DIR.glob("*.md"):
        total += 1
        stem = md.stem
        camel = to_camelcase(stem)
        half_camel = to_camelcase_lower_first(stem)

        new_aliases = []
        if camel and camel != stem:
            new_aliases.append(camel)
        if half_camel and half_camel != stem and half_camel != camel:
            new_aliases.append(half_camel)

        if not new_aliases:
            skipped += 1
            continue

        if add_aliases_to_file(md, new_aliases):
            fixed += 1
        else:
            skipped += 1

    print(f"=== alias 批量修复完成 ===")
    print(f"  扫描概念文件: {total}")
    print(f"  添加别名: {fixed}")
    print(f"  跳过(无新别名/无需修改): {skipped}")


if __name__ == "__main__":
    main()
