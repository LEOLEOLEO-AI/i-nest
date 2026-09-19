"""Check final traceability, source integrity, native math and PDF bounds."""

from hashlib import sha256
from pathlib import Path
import re
from zipfile import ZipFile
import xml.etree.ElementTree as ET

import fitz
from PIL import Image, ImageOps, ImageDraw


SOURCE = Path(__file__).resolve().parent
OUTPUT = Path("D:/Obsidian/Output/18_iNEST_Final_Theory_20260917")
PARTS = ["01_Final_Theory.md", "06_SEI_Engineering_Protocol.md",
         "05_Numerical_Checks.md", "02_Claim_Passport.md", "03_Evidence_Integration.md"]


def main():
    manuscript = (SOURCE / PARTS[0]).read_text(encoding="utf-8")
    combined = "\n".join((SOURCE / name).read_text(encoding="utf-8") for name in PARTS)
    verification = manuscript.split("# 附录 B ", 1)[1].split("# 附录 C ", 1)[0]
    used_ids = set(re.findall(r"\bV-[A-Z]+\d+\b", combined))
    defined_ids = set(re.findall(r"\bV-[A-Z]+\d+\b", verification))
    assert used_ids <= defined_ids, used_ids - defined_ids
    bibliography = manuscript.split("# 参考文献", 1)[1]
    ref_ids = set(re.findall(r"\bR\d{2}\b", combined))
    declared_refs = set(re.findall(r"^- \[(R\d{2})\]", bibliography, re.M))
    assert ref_ids <= declared_refs, ref_ids - declared_refs
    tags = list(map(int, re.findall(r"\\tag\{(\d+)\}", manuscript)))
    assert tags == list(range(1, len(tags) + 1)), tags
    original = Path("D:/Obsidian/Output/Genspark/卷二理论基石篇合并版-v1.1.docx")
    original_hash = sha256(original.read_bytes()).hexdigest()
    assert original_hash == "2751a9e5bd880bee914871ebd1d559e0a06ddb0d3cb077c72fab074a78f520d3"
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
          "m": "http://schemas.openxmlformats.org/officeDocument/2006/math"}
    docx_path = OUTPUT / "01_Final_Theory.docx"
    with ZipFile(docx_path) as archive:
        document = ET.fromstring(archive.read("word/document.xml"))
        equations = len(document.findall(".//m:oMath", ns))
        assert equations > 100
        text = "".join(n.text or "" for n in document.findall(".//w:t", ns))
        for raw in ["\\boxed", "\\tag{", "$$", "\\begin{", "Table of Contents"]:
            assert raw not in text, raw
        assert any(n.startswith("word/media/") for n in archive.namelist())
        math_text = "".join(n.text or "" for n in document.findall(".//m:t", ns))
        for number in tags:
            assert f"({number})" in math_text, f"Missing rendered equation {number}"
    pdf_path = OUTPUT / "01_Final_Theory.pdf"
    pdf = fitz.open(pdf_path)
    empty, outside = [], []
    for index, page in enumerate(pdf):
        if len(page.get_text().strip()) < 20:
            empty.append(index + 1)
        for block in page.get_text("blocks"):
            x0, y0, x1, y1 = block[:4]
            if x0 < -1 or y0 < -1 or x1 > page.rect.width + 1 or y1 > page.rect.height + 1:
                outside.append(index + 1)
                break
    assert not empty, empty
    assert not outside, outside
    full_text = "\n".join(p.get_text() for p in pdf)
    assert "连接塑形" in full_text and "SEI" in full_text
    assert "Error!" not in full_text and "错误!" not in full_text
    for number in tags:
        assert f"({number})" in full_text, f"Missing PDF equation {number}"
    samples = sorted(set([0, 1, 2, len(pdf) - 1] +
                         [round(i * (len(pdf) - 1) / 15) for i in range(16)]))
    thumbs = []
    for index in samples:
        pixmap = pdf[index].get_pixmap(matrix=fitz.Matrix(0.65, 0.65))
        picture = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
        picture = ImageOps.expand(picture, border=(8, 24, 8, 8), fill="white")
        ImageDraw.Draw(picture).text((10, 6), f"Page {index + 1}", fill="black")
        thumbs.append(picture)
    width, height = max(p.width for p in thumbs), max(p.height for p in thumbs)
    sheet = Image.new("RGB", (4 * width, ((len(thumbs) + 3) // 4) * height), "#dddddd")
    for index, thumbnail in enumerate(thumbs):
        sheet.paste(thumbnail, ((index % 4) * width, (index // 4) * height))
    sheet.save(OUTPUT / "04_Review_Contact_Sheet.png")
    lines = ["# 交付检查记录", "", "V-PAPER01：以下是工件检查，不是科学性能或硬件实测。", "",
             "- 原始 Word 的 SHA-256 保持一致：通过。",
             f"- 验证任务引用已解析：{len(used_ids)} 项。",
             f"- 参考文献引用已解析：{len(ref_ids)} 项。",
             f"- 主文公式编号连续且唯一：{len(tags)} 项。",
             "- 主文公式编号在 Word 数学对象与 PDF 中均可检出。",
             f"- 原生 Word 数学对象：{equations} 个。",
             f"- PDF 页数：{len(pdf)}。",
             f"- 空白页：{empty}。", f"- 越出页边界的正文块：{outside}。",
             "- LaTeX 原始标记泄漏、未更新目录英文占位、字段错误：未检测到。",
             "- 数值图已嵌入；抽样联系表已生成，仍需人工视觉检查。",
             "- 几何与动力学的人工条件审查见主张护照；启发式文字检查不是形式化证明。", "",
             "| 工件 | 字节数 | SHA-256 |", "|---|---|---|"]
    for path in [SOURCE / PARTS[0], docx_path, pdf_path, SOURCE / "04_Reproduce_Core.py"]:
        lines.append(f"| {path.name} | {path.stat().st_size} | {sha256(path.read_bytes()).hexdigest()} |")
    (SOURCE / "09_Delivery_Validation.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:15]))


if __name__ == "__main__":
    main()
