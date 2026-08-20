from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from dataclasses import dataclass
from datetime import datetime
from html import unescape
from pathlib import Path
from typing import Any
import xml.etree.ElementTree as ET


@dataclass
class SourceConfig:
    name: str
    enabled: bool
    source_type: str
    author_or_source: str
    input_dirs: list[str]
    priority: str
    status: str
    task_link: str
    theme_tags: str
    formula_level: str
    default_next_action: str


class MLStripper:
    def __init__(self) -> None:
        self.parts: list[str] = []
        self.skip_depth = 0

    def feed(self, html_text: str) -> None:
        lower = html_text.lower()
        text = re.sub(r"<script\b.*?</script>", " ", lower, flags=re.DOTALL)
        text = re.sub(r"<style\b.*?</style>", " ", text, flags=re.DOTALL)
        text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
        text = re.sub(r"</p\s*>", "\n\n", text, flags=re.IGNORECASE)
        text = re.sub(r"</div\s*>", "\n", text, flags=re.IGNORECASE)
        text = re.sub(r"<[^>]+>", " ", text)
        text = unescape(text)
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"(\n\s*){3,}", "\n\n", text)
        self.parts.append(text.strip())

    def get_text(self) -> str:
        return "\n".join(part for part in self.parts if part).strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Ingest exported knowledge items into the local literature knowledge base.")
    parser.add_argument(
        "--config",
        default=r"D:\\Obsidian\\Agent\01-Theory-Research\knowledge_base_config.json",
        help="Path to knowledge base config JSON.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show what would be imported without writing files.")
    return parser.parse_args()


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def normalize_whitespace(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[\t ]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def is_unusable_shell_extract(path: Path, extracted: str) -> bool:
    if path.suffix.lower() not in {".html", ".htm"}:
        return False
    normalized = normalize_whitespace(extracted).lower()
    shell_texts = {
        "you need to enable javascript to run this app.",
        "enable javascript to run this app.",
    }
    if normalized in shell_texts:
        return True
    if "enable javascript to run this app" in normalized and len(normalized) < 160:
        return True
    return False


def strip_html(html_text: str) -> str:
    stripper = MLStripper()
    stripper.feed(html_text)
    return normalize_whitespace(stripper.get_text())


def try_read_text(path: Path) -> str:
    for encoding in ("utf-8", "utf-8-sig", "gb18030", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="ignore")


def extract_pdf_text(path: Path, max_pages: int) -> str:
    try:
        from pypdf import PdfReader
    except ImportError:
        return ""
    try:
        reader = PdfReader(str(path))
    except Exception:
        return ""
    chunks: list[str] = []
    for page in reader.pages[:max_pages]:
        try:
            chunks.append((page.extract_text() or "").strip())
        except Exception:
            continue
    return normalize_whitespace("\n\n".join(chunk for chunk in chunks if chunk))


def extract_docx_text(path: Path) -> str:
    try:
        import docx
    except ImportError:
        return ""
    try:
        document = docx.Document(str(path))
    except Exception:
        return ""
    paragraphs = [paragraph.text.strip() for paragraph in document.paragraphs if paragraph.text.strip()]
    return normalize_whitespace("\n\n".join(paragraphs))


def extract_enex_text(path: Path) -> tuple[str, str]:
    try:
        root = ET.fromstring(path.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return path.stem, ""
    notes: list[str] = []
    title = path.stem
    for note in root.findall("note"):
        note_title = (note.findtext("title") or "").strip()
        if note_title and title == path.stem:
            title = note_title
        content = note.findtext("content") or ""
        notes.append(strip_html(content))
    return title, normalize_whitespace("\n\n".join(item for item in notes if item))


def extract_content(path: Path, max_pdf_pages: int) -> tuple[str, str]:
    suffix = path.suffix.lower()
    title = path.stem
    if suffix == ".pdf":
        return title, extract_pdf_text(path, max_pdf_pages)
    if suffix == ".docx":
        return title, extract_docx_text(path)
    if suffix in {".html", ".htm"}:
        return title, strip_html(try_read_text(path))
    if suffix in {".md", ".txt", ".json"}:
        return title, normalize_whitespace(try_read_text(path))
    if suffix == ".enex":
        return extract_enex_text(path)
    return title, ""


def detect_source_type(path: Path, source: SourceConfig) -> str:
    suffix = path.suffix.lower()
    if suffix in {".pdf", ".docx", ".html", ".htm", ".md", ".txt", ".enex"}:
        return source.source_type
    return source.source_type


def file_fingerprint(path: Path) -> str:
    stat = path.stat()
    payload = f"{path.resolve()}|{stat.st_size}|{int(stat.st_mtime)}"
    return hashlib.sha1(payload.encode("utf-8")).hexdigest()


def safe_stem(path: Path) -> str:
    stem = re.sub(r"[^A-Za-z0-9._\-\u4e00-\u9fff]+", "_", path.stem).strip("_")
    return stem or "item"


def ensure_unique_path(path: Path) -> Path:
    if not path.exists():
        return path
    base = path.stem
    suffix = path.suffix
    parent = path.parent
    counter = 2
    while True:
        candidate = parent / f"{base}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def ensure_structure(kb_root: Path) -> None:
    required_dirs = [
        kb_root / "Inbox" / "web",
        kb_root / "Sources" / "web",
        kb_root / "Snapshots" / "web",
        kb_root / "Notes",
        kb_root / "Logs",
    ]
    for directory in required_dirs:
        directory.mkdir(parents=True, exist_ok=True)


def read_index(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def next_canonical_id(index_text: str) -> str:
    numbers = [int(match) for match in re.findall(r"LIT-(\d+)", index_text)]
    next_number = max(numbers, default=0) + 1
    return f"LIT-{next_number:04d}"


def escape_cell(value: str) -> str:
    text = value.replace("|", "\\|").replace("\n", " ").strip()
    return text


def insert_index_row(index_text: str, row: str) -> str:
    marker = "\n## Quick Inbox"
    if marker not in index_text:
        raise ValueError("Could not locate '## Quick Inbox' section in literature_index.md")
    return index_text.replace(marker, row + marker, 1)


def build_row(data: dict[str, str]) -> str:
    ordered_keys = [
        "canonical_id",
        "title",
        "author_or_source",
        "year",
        "source_type",
        "theme_tags",
        "priority",
        "status",
        "task_link",
        "original_path_or_uri",
        "local_snapshot_path",
        "formula_level",
        "quality_notes",
        "summary",
        "key_concepts",
        "next_action",
        "last_updated",
    ]
    values = [escape_cell(data.get(key, "")) for key in ordered_keys]
    return "| " + " | ".join(values) + " |\n"


def snapshot_text(title: str, source_path: Path, content: str, source_name: str) -> str:
    lines = [
        f"# {title}",
        "",
        f"- Source App: `{source_name}`",
        f"- Original Path: `{source_path}`",
        f"- Imported At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## Extracted Content",
        "",
        content if content else "No extractable text was found.",
        "",
    ]
    return "\n".join(lines)


def ingest_one(
    source: SourceConfig,
    file_path: Path,
    config: dict[str, Any],
    state: dict[str, Any],
    dry_run: bool,
) -> tuple[bool, str]:
    fingerprint = file_fingerprint(file_path)
    if fingerprint in state["items"]:
        return False, f"SKIP {file_path}"

    kb_root = Path(config["kb_root"])
    today = datetime.now().strftime("%Y%m%d")
    source_dir = kb_root / "Sources" / source.name / today
    snapshot_dir = kb_root / "Snapshots" / source.name / today
    source_dir.mkdir(parents=True, exist_ok=True)
    snapshot_dir.mkdir(parents=True, exist_ok=True)

    copied_path = ensure_unique_path(source_dir / file_path.name)
    title, extracted = extract_content(file_path, int(config.get("snapshot_pdf_max_pages", 20)))
    if is_unusable_shell_extract(file_path, extracted):
        return False, f"SKIP dynamic shell page {file_path}"
    snapshot_name = safe_stem(copied_path) + ".md"
    snapshot_path = ensure_unique_path(snapshot_dir / snapshot_name)

    index_path = Path(config["literature_index_path"])
    index_text = read_index(index_path)
    canonical_id = next_canonical_id(index_text)

    quality_notes = []
    if not extracted:
        quality_notes.append("No extractable text detected")
    if file_path.suffix.lower() == ".pdf":
        quality_notes.append("Auto-imported PDF")
    if file_path.suffix.lower() == ".enex":
        quality_notes.append("Imported from ENEX export")

    row_data = {
        "canonical_id": canonical_id,
        "title": title,
        "author_or_source": source.author_or_source,
        "year": str(datetime.now().year),
        "source_type": detect_source_type(file_path, source),
        "theme_tags": source.theme_tags,
        "priority": source.priority,
        "status": source.status,
        "task_link": source.task_link,
        "original_path_or_uri": str(file_path),
        "local_snapshot_path": str(snapshot_path),
        "formula_level": source.formula_level,
        "quality_notes": "; ".join(quality_notes),
        "summary": "",
        "key_concepts": "",
        "next_action": source.default_next_action,
        "last_updated": datetime.now().strftime("%Y-%m-%d"),
    }
    row = build_row(row_data)

    if dry_run:
        return True, f"DRY-RUN IMPORT {file_path} -> {snapshot_path}"

    shutil.copy2(file_path, copied_path)
    snapshot_path.write_text(snapshot_text(title, file_path, extracted, source.name), encoding="utf-8")
    updated_index = insert_index_row(index_text, row)
    index_path.write_text(updated_index, encoding="utf-8")

    state["items"][fingerprint] = {
        "canonical_id": canonical_id,
        "source_name": source.name,
        "original_path": str(file_path),
        "copied_path": str(copied_path),
        "snapshot_path": str(snapshot_path),
        "imported_at": datetime.now().isoformat(timespec="seconds"),
    }
    return True, f"IMPORTED {file_path} -> {snapshot_path}"


def iter_files(input_dirs: list[str]) -> list[Path]:
    files: list[Path] = []
    for folder in input_dirs:
        directory = Path(folder)
        if not directory.exists():
            continue
        for path in directory.rglob("*"):
            if path.is_file() and path.name != ".gitkeep":
                files.append(path)
    return sorted(files)


def main() -> int:
    args = parse_args()
    config_path = Path(args.config)
    config = load_json(config_path, None)
    if config is None:
        raise SystemExit(f"Config not found: {config_path}")

    kb_root = Path(config["kb_root"])
    ensure_structure(kb_root)

    state_path = Path(config["state_path"])
    state = load_json(state_path, {"items": {}})
    imported = 0
    scanned = 0

    sources = [SourceConfig(**source_data) for source_data in config.get("sources", [])]
    for source in sources:
        if not source.enabled:
            continue
        for file_path in iter_files(source.input_dirs):
            scanned += 1
            changed, message = ingest_one(source, file_path, config, state, args.dry_run)
            print(message)
            if changed:
                imported += 1

    if not args.dry_run:
        save_json(state_path, state)

    print(f"Scanned: {scanned}")
    print(f"Imported: {imported}")
    print(f"Dry run: {'yes' if args.dry_run else 'no'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
