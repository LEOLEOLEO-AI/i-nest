#!/usr/bin/env python3
"""Ingest one local academic PDF and create a page-addressable Markdown text."""
import argparse
import hashlib
import shutil
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from pypdf import PdfReader

VAULT = Path(r"D:\Obsidian\home\work\.openclaw\workspace")
PDF_SOURCE = VAULT / "00_Inbox" / "01_PDF_Source"
TEXT_OUTPUT = VAULT / "20_Processing" / "01_PDF_Text"


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--title", required=True)
    parser.add_argument("--source-url", required=True)
    parser.add_argument("--slug", required=True)
    args = parser.parse_args()

    source = args.pdf.resolve()
    if not source.is_file() or source.suffix.lower() != ".pdf":
        raise SystemExit(f"PDF not found: {source}")

    PDF_SOURCE.mkdir(parents=True, exist_ok=True)
    TEXT_OUTPUT.mkdir(parents=True, exist_ok=True)
    stored_pdf = PDF_SOURCE / source.name
    if source != stored_pdf:
        shutil.copy2(source, stored_pdf)

    reader = PdfReader(str(stored_pdf))
    text_parts = []
    for index, page in enumerate(reader.pages, start=1):
        text_parts.append(f"\n\n--- PAGE {index} ---\n\n{page.extract_text() or ''}")

    pdf_hash = digest(stored_pdf)
    timestamp = datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(timespec="seconds")
    frontmatter = f'''---
title: "{args.title}"
source_pdf: "[[{stored_pdf.name}]]"
source_url: "{args.source_url}"
pdf_sha256: "{pdf_hash}"
pages: {len(reader.pages)}
text_status: extracted
analysis_status: pending_fulltext_review
ingested: "{timestamp}"
---

# {args.title} - Full Text
'''
    output = TEXT_OUTPUT / f"{args.slug}_fulltext.md"
    output.write_text(frontmatter + "".join(text_parts), encoding="utf-8")
    print(f"[OK] source={stored_pdf}")
    print(f"[OK] text={output}")
    print(f"[OK] sha256={pdf_hash} pages={len(reader.pages)}")


if __name__ == "__main__":
    main()
