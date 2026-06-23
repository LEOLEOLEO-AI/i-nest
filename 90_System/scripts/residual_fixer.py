#!/usr/bin/env python3
"""
Residual Fixer: Tag + Link remaining notes
- Untagged real notes -> LLM-generated tags
- Orphans -> directory + tag-overlap cross-links
"""

import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import re, yaml, json, time
import sys
sys.path.insert(0, r"D:\Obsidian\scripts")
from llm_router import llm_call
from pathlib import Path
from collections import defaultdict

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
EXCLUDE = {".venv",".git",".neural_db",".neural_memory",".obsidian",".trash","node_modules","copilot","__pycache__"}
SKIP_NAMES = {"AGENTS.md","BOOTSTRAP.md","MEMORY.md","RULES.md","SOUL.md","TOOLS.md","USER.md","conflict-files-obsidian-git.md"}


def parse_fm(text):
    if not text.startswith("---"): return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3: return {}, text
    try: return yaml.safe_load(parts[1]) or {}, parts[2]
    except: return {}, text

# ── Step 1: Find remaining issues ──────────────────────────────
print("[1/3] Scanning...")
untagged = []
orphans = []
all_notes = []

for f in VAULT.rglob("*.md"):
    if any(e in f.parts for e in EXCLUDE): continue
    if f.name in SKIP_NAMES and f.parent == VAULT: continue
    text = f.read_text(encoding="utf-8", errors="ignore")
    meta, body = parse_fm(text)

    tags = meta.get("tags", [])
    if isinstance(tags, list) and tags and isinstance(tags[0], dict):
        tags = [t.get("name","") for t in tags]
    elif not isinstance(tags, list):
        tags = []

    links = re.findall(r"\[\[([^\]|#]+)(?:[|#][^\]]+)?\]\]", text)
    title = meta.get("title", f.stem)
    rel = str(f.relative_to(VAULT))
    topic_dir = rel.split("/")[0] if "/" in rel else "root"

    nd = {"path": f, "title": title, "tags": tags, "links": links,
          "body": body[:2000], "topic_dir": topic_dir}
    all_notes.append(nd)

    if not tags:
        untagged.append(nd)
    if not links:
        orphans.append(nd)

print(f"  Untagged: {len(untagged)}")
print(f"  Orphans: {len(orphans)}")

# ── Step 2: LLM-tag untagged notes ─────────────────────────────
if untagged:
    print(f"\n[2/3] LLM-tagging {len(untagged)} untagged notes...")
    pass  # Using llm_router instead of direct OpenAI client
    fixed_tags = 0

    for nd in untagged:
        body_snippet = nd["body"][:1500]
        if len(body_snippet.strip()) < 30:
            continue  # too short

        prompt = f"""Analyze this note and output 3-5 concise tags (lowercase, hyphen-separated, English). 
Return ONLY a JSON list of strings, no explanation.

Note title: {nd["title"]}
Content: {body_snippet}"""

        try:
            r_text = llm_call(
                prompt,
                messages=[{"role":"user","content":prompt}],
                max_tokens=100, temperature=0.3, timeout=30
            )
            raw = r.choices[0].message.content.strip()
            if raw.startswith("```"): raw = raw.split("\n",1)[1][:-3] if raw.endswith("```") else raw.split("\n",1)[1]
            new_tags = json.loads(raw)
            if isinstance(new_tags, list) and all(isinstance(t,str) for t in new_tags):
                # Update frontmatter
                f = nd["path"]
                text = f.read_text(encoding="utf-8", errors="ignore")
                meta, body = parse_fm(text)
                meta["tags"] = new_tags[:5]
                new_fm = "---\n" + yaml.dump(meta, allow_unicode=True, default_flow_style=False, sort_keys=False, width=200).strip() + "\n---\n" + body.lstrip("\n")
                f.write_text(new_fm, encoding="utf-8")
                fixed_tags += 1
                print(f"  Tagged: {nd['title'][:60]} -> {new_tags}")
                time.sleep(0.5)
        except Exception as e:
            print(f"  Skip {nd['title'][:40]}: {e}")

    print(f"  Tagged {fixed_tags} notes")

# ── Step 3: Cross-link orphans by topic+tag overlap ────────────
if orphans:
    print(f"\n[3/3] Cross-linking {len(orphans)} orphans...")

    # Build index: topic_dir -> list of (path, title, tags)
    topic_index = defaultdict(list)
    for nd in all_notes:
        topic_index[nd["topic_dir"]].append(nd)

    linked = 0
    for orphan in orphans:
        td = orphan["topic_dir"]
        candidates = topic_index.get(td, [])
        if not candidates:
            continue

        # Score candidates by tag overlap
        orphan_tags = set(orphan["tags"])
        scored = []
        for c in candidates:
            if c["path"] == orphan["path"]: continue
            if not c["links"]: continue  # prefer notes that already have links
            c_tags = set(c["tags"])
            overlap = len(orphan_tags & c_tags)
            scored.append((c["path"], c["title"], overlap))

        scored.sort(key=lambda x: x[2], reverse=True)
        best = [s for s in scored[:5] if s[2] > 0]
        if not best:
            # Fallback: just link to other notes in same dir
            best = [(c["path"], c["title"], 0) for c in candidates[:3]
                    if c["path"] != orphan["path"]]

        if not best:
            continue

        # Add [[links]] section
        f = orphan["path"]
        text = f.read_text(encoding="utf-8", errors="ignore")
        if "## Related" in text or "## 相关" in text:
            continue

        link_lines = ["\n## Related Notes\n"]
        for cpath, ctitle, _ in best[:3]:
            link_lines.append(f"- [[{ctitle}]]")
        link_lines.append("")

        new_text = text.rstrip() + "\n" + "\n".join(link_lines)
        f.write_text(new_text, encoding="utf-8")
        linked += 1
        if linked % 100 == 0:
            print(f"  Linked {linked}/{len(orphans)}...")

    print(f"  Linked {linked} orphans")

print("\nDone.")
