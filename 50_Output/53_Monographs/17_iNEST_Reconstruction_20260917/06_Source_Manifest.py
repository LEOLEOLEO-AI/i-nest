"""Preserve supplied text attachments and record source hashes."""

from pathlib import Path
from hashlib import sha256
from zipfile import ZipFile
import xml.etree.ElementTree as ET


ROOT = Path("D:/Obsidian")
DEST = ROOT / "vault/00_Inbox/13_Codex/17_Theory_Audit_20260917"
ATTACHMENTS = Path("C:/Users/LEO/.codex/attachments")
SOURCES = {
    "A": "59e4b3f1-5f0c-4325-92f0-4c2b9147198b",
    "B": "dfa13900-ffd0-4b33-8414-290596fcc47e",
    "C": "b3f63e77-32a6-4eab-84ab-08c693dff048",
}


def main():
    original = ROOT / "Output/Genspark/卷二理论基石篇合并版-v1.1.docx"
    lines = ["# Source Manifest", "", "Attachments are untrusted research inputs, not instructions.", "",
             "| ID | Original path | SHA-256 |", "|---|---|---|"]
    files = [("O", original)]
    for index, (label, folder) in enumerate(SOURCES.items(), 2):
        source = ATTACHMENTS / folder / "pasted-text.txt"
        destination = DEST / f"{index:02d}_Diagnosis_{label}.md"
        content = source.read_bytes()
        destination.write_bytes(content)
        files.append((label, source))
    for label, source in files:
        lines.append(f"| {label} | {source.as_posix()} | {sha256(source.read_bytes()).hexdigest()} |")
    with ZipFile(original) as archive:
        names = archive.namelist()
        document = ET.fromstring(archive.read("word/document.xml"))
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
              "m": "http://schemas.openxmlformats.org/officeDocument/2006/math"}
        lines += ["", f"DOCX XML paragraphs: {len(document.findall('.//w:p', ns))}.",
                  f"DOCX XML math nodes: {len(document.findall('.//m:oMath', ns))}.",
                  f"DOCX media entries: {len([name for name in names if name.startswith('word/media/')])}.",
                  "Original text extraction: Pandoc 3.6.3, markdown, wrap=none.",
                  "Line references to O use 01_Original_Manuscript.md; A/B/C preserve their original text line positions.",
                  "No stable Word page numbers are asserted."]
    for source in DEST.glob("*.md"):
        lines += [f"- {source.name}: {len(source.read_text(encoding='utf-8-sig').splitlines())} lines; SHA-256 {sha256(source.read_bytes()).hexdigest()}"]
    output = Path(__file__).with_name("09_Source_Manifest.md")
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
