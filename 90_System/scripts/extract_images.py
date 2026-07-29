import zipfile, re, os
from pathlib import Path

src = Path(r"D:\Output\Genspark\TCC拓扑中心计算范式：论文背景综述、相关工作对比与引用框架.docx")
dst_dir = Path(r"D:\Obsidian\vault\30_TCC\31_Theory\tcc_paper_background_assets")
dst_dir.mkdir(parents=True, exist_ok=True)

# Extract all images
with zipfile.ZipFile(src) as z:
    media = [n for n in z.namelist() if "media" in n.lower()]
    
    # Read the document XML to map images to positions
    doc_xml = z.read("word/document.xml").decode("utf-8")
    
    # Find all paragraphs with images and their surrounding text
    paras = re.findall(r"<w:p[ >].*?</w:p>", doc_xml, re.DOTALL)
    
    img_map = {}  # rId -> image filename
    for m in media:
        img_map[m] = m
    
    # Extract images
    for m in media:
        data = z.read(m)
        name = Path(m).name
        dst = dst_dir / name
        dst.write_bytes(data)
        print(f"Extracted: {name} ({len(data)}B)")
    
    # Now rebuild the markdown with image references
    # Read current markdown
    md_path = Path(r"D:\Obsidian\vault\30_TCC\31_Theory\tcc_paper_background.md")
    content = md_path.read_text(encoding="utf-8")
    
    # Find image reference patterns in the docx XML to insert into markdown
    img_refs = re.findall(r'<wp:inline.*?</wp:inline>', doc_xml, re.DOTALL)
    img_refs += re.findall(r'<wp:anchor.*?</wp:anchor>', doc_xml, re.DOTALL)
    
    print(f"\nImage references in XML: {len(img_refs)}")
    
    # Get the r:embed IDs
    for i, ref in enumerate(img_refs):
        embed_match = re.search(r'r:embed="([^"]+)"', ref)
        if embed_match:
            rid = embed_match.group(1)
            print(f"  Image {i+1}: rId={rid}")

print(f"\nAssets saved to: {dst_dir}")
