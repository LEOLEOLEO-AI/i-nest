import argparse
import datetime as _dt
import os
import re
from dataclasses import dataclass
from pathlib import Path


_TAG_RE = re.compile(r"(?<![\w/])#([0-9A-Za-z_\-\u4e00-\u9fff]+)")
_WIKI_LINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


@dataclass(frozen=True)
class NoteInfo:
    rel_path: str
    rel_link: str
    title: str
    mtime: float
    tags: tuple[str, ...]
    link_count: int


def _now_iso() -> str:
    return _dt.datetime.now().replace(microsecond=0).isoformat(sep=" ")


def _read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def _write_text(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")


def _extract_frontmatter_tags(text: str) -> list[str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return []
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return []
    fm = lines[1:end]
    tags = []
    in_tags = False
    for line in fm:
        s = line.rstrip()
        if not s:
            continue
        if not in_tags:
            if s.strip() == "tags:":
                in_tags = True
            continue
        if s.lstrip().startswith("- "):
            t = s.split("- ", 1)[1].strip().strip('"').strip("'")
            if t:
                tags.append(t.lstrip("#"))
            continue
        if ":" in s:
            break
    return tags


def _extract_inline_tags(text: str) -> list[str]:
    return [m.group(1) for m in _TAG_RE.finditer(text)]


def _normalize_tags(tags: list[str]) -> tuple[str, ...]:
    out = []
    seen = set()
    for t in tags:
        tt = t.strip().lstrip("#")
        if not tt:
            continue
        low = tt.lower()
        if low in seen:
            continue
        seen.add(low)
        out.append(tt)
    return tuple(sorted(out, key=lambda x: x.lower()))


def _note_link(rel_path: str) -> str:
    p = rel_path.replace("\\", "/")
    if p.lower().endswith(".md"):
        p = p[:-3]
    return p


def _iter_notes(vault_root: Path, wiki_root: Path) -> list[NoteInfo]:
    ignore_dirs = {
        ".git",
        ".obsidian",
        ".smart-env",
        ".neural_db",
        ".neural_memory",
        "assets",
    }
    notes = []
    for root, dirs, files in os.walk(vault_root):
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        root_path = Path(root)
        if wiki_root in root_path.parents or root_path == wiki_root:
            continue
        for f in files:
            if not f.lower().endswith(".md"):
                continue
            p = root_path / f
            try:
                rel = str(p.relative_to(vault_root))
            except Exception:
                continue
            text = _read_text(p)
            fm_tags = _extract_frontmatter_tags(text)
            inline_tags = _extract_inline_tags(text)
            tags = _normalize_tags(fm_tags + inline_tags)
            link_count = len(_WIKI_LINK_RE.findall(text))
            notes.append(
                NoteInfo(
                    rel_path=rel,
                    rel_link=_note_link(rel),
                    title=p.stem,
                    mtime=p.stat().st_mtime,
                    tags=tags,
                    link_count=link_count,
                )
            )
    return notes


def _format_link(rel_link: str, title: str | None = None) -> str:
    if title and title != Path(rel_link).name:
        return f"[[{rel_link}|{title}]]"
    return f"[[{rel_link}]]"


def _section(title: str) -> str:
    return f"## {title}\n"


def _build_home(notes: list[NoteInfo], wiki_rel: str) -> str:
    now = _now_iso()
    total = len(notes)
    total_links = sum(n.link_count for n in notes)
    total_tags = len({t.lower() for n in notes for t in n.tags})
    return "\n".join(
        [
            "# Wiki",
            "",
            f"Generated: {now}",
            "",
            _section("导航").rstrip(),
            f"- [[{wiki_rel}/Tags|Tags]]",
            f"- [[{wiki_rel}/Recent|Recent]]",
            f"- [[{wiki_rel}/Files|Files]]",
            f"- [[{wiki_rel}/SSOT|SSOT]]",
            f"- [[{wiki_rel}/ADR|ADR]]",
            f"- [[{wiki_rel}/Stats|Stats]]",
            "",
            _section("概览").rstrip(),
            f"- Notes: {total}",
            f"- Tags: {total_tags}",
            f"- Wiki links: {total_links}",
            "",
        ]
    )


def _build_files(vault_root: Path, wiki_rel: str) -> str:
    now = _now_iso()
    entries = []
    for p in sorted(vault_root.iterdir(), key=lambda x: x.name.lower()):
        if p.name in {".git", ".obsidian", ".smart-env", ".neural_db", ".neural_memory"}:
            continue
        if p.name == "assets":
            continue
        if p.name == wiki_rel.split("/")[0]:
            pass
        if p.is_dir():
            entries.append(f"- {p.name}/")
        else:
            if p.suffix.lower() == ".md":
                rel = str(p.relative_to(vault_root)).replace("\\", "/")
                entries.append(f"- {_format_link(_note_link(rel), p.stem)}")
            else:
                entries.append(f"- {p.name}")
    return "\n".join(
        [
            "# Files",
            "",
            f"Generated: {now}",
            "",
            "\n".join(entries),
            "",
        ]
    )


def _build_recent(notes: list[NoteInfo], limit: int = 50) -> str:
    now = _now_iso()
    items = sorted(notes, key=lambda n: n.mtime, reverse=True)[:limit]
    lines = ["# Recent", "", f"Generated: {now}", ""]
    for n in items:
        dt = _dt.datetime.fromtimestamp(n.mtime).strftime("%Y-%m-%d %H:%M")
        lines.append(f"- {dt} {_format_link(n.rel_link, n.title)}")
    lines.append("")
    return "\n".join(lines)


def _build_tags(notes: list[NoteInfo]) -> str:
    now = _now_iso()
    tag_map: dict[str, list[NoteInfo]] = {}
    for n in notes:
        for t in n.tags:
            k = t.lower()
            tag_map.setdefault(k, []).append(n)

    lines = ["# Tags", "", f"Generated: {now}", ""]
    for k in sorted(tag_map.keys()):
        lines.append(f"## #{k}")
        items = sorted(tag_map[k], key=lambda n: n.title.lower())
        for n in items[:200]:
            lines.append(f"- {_format_link(n.rel_link, n.title)}")
        if len(items) > 200:
            lines.append(f"- ... ({len(items) - 200} more)")
        lines.append("")
    return "\n".join(lines)


def _build_ssot(vault_root: Path) -> str:
    now = _now_iso()
    ssot_dir = vault_root / "00_KnowledgeBase_知识库" / "00_SSOT_权威条目"
    lines = ["# SSOT", "", f"Generated: {now}", ""]
    if not ssot_dir.exists():
        lines.append("- (missing) 00_SSOT_权威条目")
        lines.append("")
        return "\n".join(lines)
    for p in sorted(ssot_dir.rglob("*.md"), key=lambda x: str(x).lower()):
        if p.name.lower() == "readme.md":
            continue
        rel = str(p.relative_to(vault_root)).replace("\\", "/")
        lines.append(f"- {_format_link(_note_link(rel), p.stem)}")
    lines.append("")
    return "\n".join(lines)


def _build_adr(vault_root: Path) -> str:
    now = _now_iso()
    adr_dir = vault_root / "00_KnowledgeBase_知识库" / "00_ADR_决策记录"
    lines = ["# ADR", "", f"Generated: {now}", ""]
    if not adr_dir.exists():
        lines.append("- (missing) 00_ADR_决策记录")
        lines.append("")
        return "\n".join(lines)
    for p in sorted(adr_dir.rglob("*.md"), key=lambda x: str(x).lower()):
        if p.name.lower() == "readme.md":
            continue
        rel = str(p.relative_to(vault_root)).replace("\\", "/")
        lines.append(f"- {_format_link(_note_link(rel), p.stem)}")
    lines.append("")
    return "\n".join(lines)


def _build_stats(notes: list[NoteInfo]) -> str:
    now = _now_iso()
    total = len(notes)
    with_tags = sum(1 for n in notes if n.tags)
    total_links = sum(n.link_count for n in notes)
    tag_counts: dict[str, int] = {}
    for n in notes:
        for t in n.tags:
            tag_counts[t.lower()] = tag_counts.get(t.lower(), 0) + 1
    top_tags = sorted(tag_counts.items(), key=lambda kv: (-kv[1], kv[0]))[:30]
    lines = [
        "# Stats",
        "",
        f"Generated: {now}",
        "",
        f"- Notes: {total}",
        f"- Notes with tags: {with_tags}",
        f"- Wiki links: {total_links}",
        "",
        "## Top tags",
    ]
    for k, c in top_tags:
        lines.append(f"- #{k}: {c}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wiki-dir", default="00-索引/Wiki")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    vault_root = script_dir.parents[1]
    wiki_root = (vault_root / args.wiki_dir).resolve()
    wiki_rel = args.wiki_dir.replace("\\", "/")

    notes = _iter_notes(vault_root, wiki_root)

    _write_text(wiki_root / "Home.md", _build_home(notes, wiki_rel))
    _write_text(wiki_root / "Files.md", _build_files(vault_root, wiki_rel))
    _write_text(wiki_root / "Recent.md", _build_recent(notes))
    _write_text(wiki_root / "Tags.md", _build_tags(notes))
    _write_text(wiki_root / "SSOT.md", _build_ssot(vault_root))
    _write_text(wiki_root / "ADR.md", _build_adr(vault_root))
    _write_text(wiki_root / "Stats.md", _build_stats(notes))

    print(f"Wrote wiki to: {wiki_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
