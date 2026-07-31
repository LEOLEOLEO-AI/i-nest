# -*- coding: utf-8 -*-
"""
对上一轮「位置候选 own」(confidence=location) 再做一层细筛：
把其中「明显是文献 / 网页剪藏导入」的文件从 own 重新归为 external 或 pending，降低误判。

判定依据（来自上一轮文本扫描遗漏的 FRONTMATTER / 文件名信号）：
  高置信文献 (-> external):
    R1  frontmatter 含 source/url/original_url/href/link 且值为 http(s)
    R2  frontmatter category 为 web-clip / 剪藏 / import / 导入 等
    R3  文件名含「无标题」(剪藏器未命名笔记)
    R4  文件名含 getnote
  中置信 / 歧义 (-> pending, 移出 own 但需人工确认):
    R5  文件名带 (1)/(2) 等重复后缀 且 同时具备 note_id 或 source 等导入痕迹
    R6  文件名带 (1)/(2) 等重复后缀 但无其他信号 (保守置 pending)
仅对确实发生迁移的文件改写 frontmatter 的 provenance 字段。
"""
import os, re, json, sys
from collections import Counter
from pathlib import Path

VAULT = Path(r"D:\obsidian\vault")
OUT = VAULT / "99_Meta" / "classification.json"
EXCLUDE_DIRS = {".git", ".obsidian", "node_modules", "__pycache__", ".trash"}

URL_KEYS = ("source", "url", "original_url", "href", "link")
CLIP_CATS = ("web-clips", "webclip", "clippings", "clip", "web clip", "导入", "剪藏", "import", "web")


def parse_frontmatter(text):
    if not text.startswith('---'):
        return {}, text, text
    m = re.match(r'^---\s*\n(.*?)\n---', text, re.S)
    if not m:
        return {}, text, text
    fm_raw = m.group(1)
    body = text[m.end():]
    fm = {}
    for line in fm_raw.splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip().lower()] = v.strip()
    return fm, body, text


def basename_no_ext(rel):
    name = os.path.basename(rel)
    return name[:-3] if name.endswith('.md') else name


def is_literature(fm, basename):
    """返回 (is_lit, reason)；is_lit=True 表示高置信文献 -> external"""
    for k in URL_KEYS:
        val = fm.get(k, '')
        if val and ('http' in val.lower() or 'www.' in val.lower() or '.com' in val.lower() or '.cn' in val.lower()):
            return True, f"frontmatter {k} 含链接: {val[:60]}"
    cat = fm.get('category', '').lower()
    if any(c in cat for c in CLIP_CATS):
        return True, f"frontmatter category=剪藏/导入: {cat}"
    if '无标题' in basename:
        return True, "文件名含「无标题」(剪藏未命名)"
    if 'getnote' in basename.lower() or 'getnote' in (fm.get('source','').lower()):
        return True, "文件名/来源含 getnote"
    return False, ""


def is_dup_suffix(basename):
    return bool(re.search(r'\(\d+\)\s*$', basename))


# 自有研究意图信号：标题/正文出现这些词，倾向于「自有产出」而非「网上文献」
OWN_INTENT = ["建议", "方案", "折子", "计划", "报告", "纪要", "申报", "立项",
              "专项", "战略", "设计", "路线", "规划", "v1", "v2", "v3", "v4", "v5",
              "草稿", "草案", "思考", "设想", "笔记", "提纲", "框架", "待办", "总结"]


def looks_like_own(basename, text):
    low = (basename + "\n" + text[:400]).lower()
    return any(k.lower() in low for k in OWN_INTENT)


def refine_record(rec, text):
    """对单条 location 候选重新判定。返回 (new_prov, new_conf, reason)。"""
    rel = rec['path']
    basename = basename_no_ext(rel)
    fm, body, _ = parse_frontmatter(text)
    # 高置信文献 -> external
    lit, reason = is_literature(fm, basename)
    if lit:
        return 'external', 'refined', "细筛→文献(高置信): " + reason
    # 重复后缀 (N) 处理：歧义较大，按意图区分
    if is_dup_suffix(basename):
        has_import_trace = ('note_id' in fm and fm.get('note_id', '').strip() not in ('', '""')) \
            or any('http' in fm.get(k, '').lower() for k in URL_KEYS)
        if has_import_trace:
            return 'pending', 'refined', "细筛→疑似导入(重复后缀+导入痕迹),待确认"
        # 无导入痕迹：看是否像自有产出
        if looks_like_own(basename, text):
            return 'own', 'location-dup', "细筛→重复后缀但含自有研究意图,保留own(待复核)"
        return 'pending', 'refined', "细筛→重复后缀,疑似剪藏重复,待确认"
    # 其余保持原 location 候选
    return rec['provenance'], rec['confidence'], rec['reason']


def main(apply=False, dry=True):
    data = json.load(open(OUT, encoding='utf-8'))
    by_path = {r['path']: r for r in data}
    moved = []          # (old, new) provenance changes
    changed_fm = 0
    report = Counter()
    for rec in data:
        if rec.get('confidence') != 'location':
            continue
        rel = rec['path']
        fp = VAULT / rel
        if not fp.exists():
            continue
        text = fp.read_text(encoding='utf-8', errors='ignore')
        old = rec['provenance']
        new_prov, new_conf, reason = refine_record(rec, text)
        # 始终记录最新判定（即便 provenance 未变，confidence 也可能从 location -> location-dup）
        rec['provenance'] = new_prov
        rec['confidence'] = new_conf
        rec['reason'] = reason
        if new_prov != old:
            moved.append((rel, old, new_prov, reason))
            report[f"{old}->{new_prov}"] += 1
            if apply:
                # 改写 frontmatter provenance
                newtext = re.sub(r'(?m)^(provenance:\s*).*$', f'provenance: {new_prov}', text, count=1)
                if newtext != text:
                    fp.write_text(newtext, encoding='utf-8')
                    changed_fm += 1
    if apply:
        json.dump(data, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    # 汇总
    pc = Counter(r['provenance'] for r in data)
    print(f"总文件: {len(data)}")
    print(f"迁移(location候选中被重新归类): {len(moved)}")
    for k, v in report.most_common():
        print(f"    {k:18s} {v}")
    print(f"新 provenance 分布: {dict(pc)}")
    if apply:
        print(f"frontmatter 改写: {changed_fm}")
        print(f"已写回 {OUT}")
    else:
        print("(dry-run，未写回；加 --apply 执行)")
    # 列出少量样例
    print("\n--- 迁移样例(前 20) ---")
    for rel, old, new, reason in moved[:20]:
        print(f"  [{old}->{new}] {rel[:70]}")
        print(f"        {reason[:70]}")


if __name__ == '__main__':
    apply = '--apply' in sys.argv
    main(apply=apply, dry=not apply)
