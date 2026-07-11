import argparse
import datetime as _dt
import os
import re
import shutil
import sys
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path


_IMG_MD_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
_IMG_HTML_RE = re.compile(r'<img[^>]+src=["\']([^"\']+)["\']', re.IGNORECASE)


def _now_iso() -> str:
    return _dt.datetime.now().replace(microsecond=0).isoformat(sep=" ")


def _yyyy_mm() -> str:
    return _dt.datetime.now().strftime("%Y-%m")


def _is_http_url(s: str) -> bool:
    try:
        u = urllib.parse.urlparse(s)
        return u.scheme in ("http", "https") and bool(u.netloc)
    except Exception:
        return False


def _safe_filename(name: str) -> str:
    name = name.strip().strip(".")
    name = re.sub(r"[<>:\"/\\\\|?*]", "_", name)
    name = re.sub(r"\s+", " ", name).strip()
    if not name:
        return "untitled"
    return name[:160]


def _unique_path(dest_dir: Path, filename: str) -> Path:
    p = dest_dir / filename
    if not p.exists():
        return p
    stem = p.stem
    suffix = p.suffix
    for i in range(2, 1000):
        cand = dest_dir / f"{stem}-{i}{suffix}"
        if not cand.exists():
            return cand
    raise RuntimeError(f"Could not create unique filename for {p}")


def _read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def _write_text(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")


def _ensure_front_matter(text: str, updates: dict[str, str]) -> str:
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        end = None
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                end = i
                break
        if end is None:
            return text
        fm = lines[1:end]
        kv = {}
        for line in fm:
            if ":" in line and not line.lstrip().startswith("#"):
                k, v = line.split(":", 1)
                kv[k.strip()] = v.strip()
        for k, v in updates.items():
            kv[k] = v
        new_fm = [f"{k}: {kv[k]}" for k in sorted(kv.keys())]
        return "\n".join(["---", *new_fm, "---", *lines[end + 1 :]]) + "\n"

    new_fm = [f"{k}: {updates[k]}" for k in sorted(updates.keys())]
    return "\n".join(["---", *new_fm, "---", "", text.rstrip(), ""]) + "\n"


def _download(url: str, out_path: Path, timeout_s: int = 30) -> bool:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            data = resp.read()
        out_path.write_bytes(data)
        return True
    except Exception:
        return False


def _ext_from_url(url: str) -> str:
    try:
        path = urllib.parse.urlparse(url).path
        ext = Path(path).suffix.lower()
        if ext and len(ext) <= 10:
            return ext
    except Exception:
        pass
    return ".bin"


def _rewrite_images(
    text: str,
    export_root: Path,
    note_src_path: Path,
    assets_dir: Path,
    download_remote_images: bool,
) -> tuple[str, int, int]:
    local_copied = 0
    remote_downloaded = 0

    def handle_url(raw: str) -> str:
        nonlocal local_copied, remote_downloaded
        url = raw.strip().strip('"').strip("'")

        if _is_http_url(url):
            if not download_remote_images:
                return raw
            ext = _ext_from_url(url)
            file_name = _safe_filename(Path(urllib.parse.urlparse(url).path).stem) + ext
            out_path = _unique_path(assets_dir, file_name)
            ok = _download(url, out_path)
            if ok:
                remote_downloaded += 1
                rel = os.path.relpath(out_path, note_src_path.parent).replace("\\", "/")
                return rel
            return raw

        if url.startswith("data:") or url.startswith("#"):
            return raw

        if url.startswith("/") or url.startswith("\\"):
            return raw

        candidate = (note_src_path.parent / url).resolve()
        if not candidate.exists():
            candidate = (export_root / url).resolve()
        if candidate.exists() and candidate.is_file():
            out_path = _unique_path(assets_dir, candidate.name)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(candidate, out_path)
            local_copied += 1
            rel = os.path.relpath(out_path, note_src_path.parent).replace("\\", "/")
            return rel

        return raw

    def md_repl(m: re.Match) -> str:
        return m.group(0).replace(m.group(1), handle_url(m.group(1)))

    def html_repl(m: re.Match) -> str:
        return m.group(0).replace(m.group(1), handle_url(m.group(1)))

    text = _IMG_MD_RE.sub(md_repl, text)
    text = _IMG_HTML_RE.sub(html_repl, text)
    return text, local_copied, remote_downloaded


def _collect_markdown_files(root: Path) -> list[Path]:
    return [p for p in root.rglob("*.md") if p.is_file()]


def _extract_if_zip(src: Path, work_dir: Path) -> Path:
    if src.is_dir():
        return src
    if src.is_file() and src.suffix.lower() == ".zip":
        out_dir = work_dir / f"unzipped_{_dt.datetime.now().strftime('%Y%m%d_%H%M%S')}"
        out_dir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(src, "r") as zf:
            zf.extractall(out_dir)
        return out_dir
    raise ValueError("Source must be a directory or a .zip file.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Import Get Note markdown export into this Obsidian vault.")
    parser.add_argument("source", help="Path to Get export folder or zip file.")
    parser.add_argument("--download-remote-images", action="store_true", help="Download remote images into assets.")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    vault_root = script_dir.parents[1]

    src = Path(args.source).expanduser().resolve()
    inbox_get_dir = vault_root / "00_KnowledgeBase_知识库" / "03_Inbox_文献与碎片" / "Get" / _yyyy_mm()
    assets_root = vault_root / "assets" / "get" / _yyyy_mm()
    work_dir = vault_root / ".smart-env" / "get_import"

    work_dir.mkdir(parents=True, exist_ok=True)
    export_root = _extract_if_zip(src, work_dir)

    md_files = _collect_markdown_files(export_root)
    if not md_files:
        print("No markdown files found.")
        return 2

    imported = 0
    copied_local = 0
    downloaded_remote = 0

    for md in md_files:
        raw = _read_text(md)
        title = _safe_filename(md.stem)
        dest_md = _unique_path(inbox_get_dir, f"{title}.md")
        note_assets_dir = assets_root / dest_md.stem

        updated = _ensure_front_matter(
            raw,
            {
                "source_app": "get",
                "imported_at": _now_iso(),
            },
        )
        updated, lc, rd = _rewrite_images(
            updated,
            export_root=export_root,
            note_src_path=md,
            assets_dir=note_assets_dir,
            download_remote_images=bool(args.download_remote_images),
        )
        copied_local += lc
        downloaded_remote += rd

        _write_text(dest_md, updated)
        imported += 1

    print(f"Imported: {imported}")
    print(f"Local attachments copied: {copied_local}")
    print(f"Remote images downloaded: {downloaded_remote}")
    print(f"Destination: {inbox_get_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
