import zipfile, re
from pathlib import Path

src = Path(r"D:\Output\Genspark\TCC拓扑中心计算范式：论文背景综述、相关工作对比与引用框架.docx")

with zipfile.ZipFile(src) as z:
    doc_xml = z.read("word/document.xml").decode("utf-8")
    
    # Search for formula content in paragraph text
    # MathType formulas often leave behind MTEquationSection or similar
    # Also check for common formula artifacts
    paras = re.findall(r"<w:p[ >].*?</w:p>", doc_xml, re.DOTALL)
    
    empty_or_formula = 0
    for p in paras:
        texts = re.findall(r"<w:t[^>]*>(.*?)</w:t>", p)
        text = "".join(texts).strip()
        # Find paragraphs that have embedded images (potential formulas)
        has_image = "w:drawing" in p or "wp:inline" in p or "r:embed" in p
        if has_image and len(text) < 5:
            empty_or_formula += 1
            if len(text) > 0:
                print(f"Formula text fragment: '{text}'")
    
    print(f"\nPotential formula paragraphs: {empty_or_formula}")
    
    # List all image/media files
    media = [n for n in z.namelist() if "media" in n.lower()]
    print(f"Media files: {len(media)}")
    for m in media:
        info = z.getinfo(m)
        print(f"  {m} ({info.file_size}B)")
