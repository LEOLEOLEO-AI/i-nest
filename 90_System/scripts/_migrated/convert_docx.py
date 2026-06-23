from docx import Document
import os

def convert_docx_to_md(docx_path, md_path):
    if not os.path.exists(docx_path):
        print(f"Error: {docx_path} does not exist.")
        return
        
    doc = Document(docx_path)
    md_content = []
    
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
            
        # Basic heading detection based on style name
        style_name = para.style.name.lower()
        if 'heading 1' in style_name:
            md_content.append(f"\n# {text}\n")
        elif 'heading 2' in style_name:
            md_content.append(f"\n## {text}\n")
        elif 'heading 3' in style_name:
            md_content.append(f"\n### {text}\n")
        elif 'title' in style_name:
            md_content.append(f"# {text}\n")
        else:
            md_content.append(f"{text}\n")
            
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(md_content))
    print(f"Successfully converted {docx_path} to {md_path}")

file1 = r'd:\Obsidian\home\work\.openclaw\workspace\30_Outputs\论文\A组_CST基础理论\A1_CST_Theory_V25_FINAL.docx'
md1 = r'd:\Obsidian\home\work\.openclaw\workspace\30_Outputs\论文\A组_CST基础理论\A1_CST_Theory_V25_FINAL.md'

file2 = r'd:\Obsidian\home\work\.openclaw\workspace\30_Outputs\专利\P0-5_基于液态拓扑的实时生成式结构计算方法及系统.docx'
md2 = r'd:\Obsidian\home\work\.openclaw\workspace\30_Outputs\专利\P0-5_基于液态拓扑的实时生成式结构计算方法及系统.md'

convert_docx_to_md(file1, md1)
convert_docx_to_md(file2, md2)
