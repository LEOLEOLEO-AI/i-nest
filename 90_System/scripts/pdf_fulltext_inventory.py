#!/usr/bin/env python3
"""Inventory local PDFs before full-text conversion and LLM review.

The script never changes PDFs. It writes a Markdown manifest that identifies
duplicates, likely scanned files, and files that should not enter literature
analysis (for example, generated project deliverables).
"""
import argparse
import hashlib
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from pypdf import PdfReader

VAULT = Path(r"D:\Obsidian\vault")
DEFAULT_ROOTS = [
    VAULT / "00_Inbox" / "01_PDF_Source",
    VAULT / "20_Processing" / "_attachments_knowledge",
    VAULT / "80_Archive" / "00_KnowledgeBase" / "literature" / "pdf",
]
REPORT = VAULT / "20_Processing" / "00_PDF_Fulltext_Inventory.md"


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def inspect_pdf(path):
    try:
        reader = PdfReader(str(path))
        pages = len(reader.pages)
        sample = "".join((page.extract_text() or "") for page in reader.pages[:3]).strip()
        return pages, len(sample), "machine_readable" if len(sample) >= 400 else "ocr_required"
    except Exception as error:
        return 0, 0, f"unreadable: {type(error).__name__}"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", action="append", type=Path, help="Additional PDF root; repeatable")
    args = parser.parse_args()
    roots = [root for root in DEFAULT_ROOTS if root.exists()] + (args.root or [])
    files = sorted({path.resolve() for root in roots for path in root.rglob("*.pdf")})
    hashes = defaultdict(list)
    records = []
    for path in files:
        digest = sha256(path)
        pages, chars, status = inspect_pdf(path)
        hashes[digest].append(path)
        records.append({
            "path": path,
            "sha256": digest,
            "pages": pages,
            "sample_chars": chars,
            "status": status,
        })

    lines = [
        f"# PDF 全文处理盘点 — {datetime.now().strftime('%Y-%m-%d')}",
        "",
        "> 本清单由 `pdf_fulltext_inventory.py` 生成。`machine_readable` 仅表示可抽取文本，不代表全文已通过人工核验。",
        "",
        f"- 扫描根目录: {len(roots)}",
        f"- PDF 文件: {len(records)}",
        f"- 唯一 SHA-256: {len(hashes)}",
        f"- 重复文件: {sum(len(paths) - 1 for paths in hashes.values() if len(paths) > 1)}",
        "",
        "| 文件 | 页数 | 前三页字符数 | 提取状态 | SHA-256 |",
        "|---|---:|---:|---|---|",
    ]
    for item in records:
        relative = item["path"].relative_to(VAULT) if item["path"].is_relative_to(VAULT) else item["path"]
        lines.append(
            f"| `{str(relative).replace('\\\\', '/')}` | {item['pages']} | {item['sample_chars']} | "
            f"{item['status']} | `{item['sha256']}` |"
        )
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK] {REPORT} ({len(records)} PDFs)")


if __name__ == "__main__":
    main()
