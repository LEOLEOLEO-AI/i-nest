"""Check traceability, source integrity, Word math, and PDF layout bounds."""

from hashlib import sha256
from pathlib import Path
import re
from zipfile import ZipFile
import xml.etree.ElementTree as ET

import fitz
from PIL import Image, ImageOps, ImageDraw


SOURCE = Path(__file__).resolve().parent
OUTPUT = Path("D:/Obsidian/Output/17_iNEST_Reconstruction_20260917")


def main():
    report = (SOURCE / "01_Theory_Audit_and_Reconstruction.md").read_text(encoding="utf-8")
    plan = (SOURCE / "02_Verification_Plan.md").read_text(encoding="utf-8")
    ledger = (SOURCE / "03_Evidence_Ledger.md").read_text(encoding="utf-8")
    used = set(re.findall(r"\bV-[A-Z]+\d+\b", report))
    defined = set(re.findall(r"\bV-[A-Z]+\d+\b", plan))
    assert used <= defined, used - defined
    references = set(re.findall(r"\bR\d{2}\b", report))
    assert references <= set(re.findall(r"\bR\d{2}\b", ledger))
    original = Path("D:/Obsidian/Output/Genspark/卷二理论基石篇合并版-v1.1.docx")
    assert sha256(original.read_bytes()).hexdigest() == "2751a9e5bd880bee914871ebd1d559e0a06ddb0d3cb077c72fab074a78f520d3"

    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
          "m": "http://schemas.openxmlformats.org/officeDocument/2006/math"}
    docx_path = OUTPUT / "01_Theory_Audit_and_Reconstruction.docx"
    with ZipFile(docx_path) as archive:
        document = ET.fromstring(archive.read("word/document.xml"))
        equations = len(document.findall(".//m:oMath", ns))
        assert equations > 100
        text = "".join(node.text or "" for node in document.findall(".//w:t", ns))
        assert "\\boxed" not in text and "$$" not in text

    pdf = fitz.open(OUTPUT / "01_Theory_Audit_and_Reconstruction.pdf")
    empty_pages, outside_pages = [], []
    for index, page in enumerate(pdf):
        if len(page.get_text().strip()) < 20:
            empty_pages.append(index + 1)
        for block in page.get_text("blocks"):
            x0, y0, x1, y1 = block[:4]
            if x0 < -1 or y0 < -1 or x1 > page.rect.width + 1 or y1 > page.rect.height + 1:
                outside_pages.append(index + 1)
                break
    assert not empty_pages, empty_pages
    assert not outside_pages, outside_pages
    samples = sorted(set([0, 1, 2, len(pdf) - 1] + [round(i * (len(pdf) - 1) / 11) for i in range(12)]))
    thumbs = []
    for index in samples:
        pixmap = pdf[index].get_pixmap(matrix=fitz.Matrix(0.6, 0.6))
        picture = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
        picture = ImageOps.expand(picture, border=(8, 24, 8, 8), fill="white")
        ImageDraw.Draw(picture).text((10, 6), f"Page {index + 1}", fill="black")
        thumbs.append(picture)
    width = max(item.width for item in thumbs)
    height = max(item.height for item in thumbs)
    cols = 4
    sheet = Image.new("RGB", (cols * width, ((len(thumbs) + cols - 1) // cols) * height), "#dddddd")
    for index, thumbnail in enumerate(thumbs):
        sheet.paste(thumbnail, ((index % cols) * width, (index // cols) * height))
    sheet.save(OUTPUT / "04_Review_Contact_Sheet.png")
    lines = ["# Delivery Validation", "", "These are file and numerical verification results, not scientific performance measurements.", "",
             f"- Source DOCX hash unchanged: PASS.",
             f"- Verification IDs resolved: {len(used)}.",
             f"- Reference IDs resolved: {len(references)}.",
             f"- Native Word math objects: {equations}.",
             f"- PDF pages: {len(pdf)}.",
             f"- Empty pages: {empty_pages}.",
             f"- Text blocks outside page boundaries: {outside_pages}.",
             "- Formula markup leakage (boxed/display delimiters): none detected.",
             "- Visual samples: 04_Review_Contact_Sheet.png; automated bounds do not replace visual inspection.", "",
             "| Artifact | Bytes | SHA-256 |", "|---|---|---|"]
    for path in [docx_path, OUTPUT / "01_Theory_Audit_and_Reconstruction.pdf"]:
        lines.append(f"| {path.name} | {path.stat().st_size} | {sha256(path.read_bytes()).hexdigest()} |")
    (SOURCE / "15_Delivery_Validation.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:13]))


if __name__ == "__main__":
    main()
