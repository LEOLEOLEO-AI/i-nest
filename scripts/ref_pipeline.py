#!/usr/bin/env python3
"""TCC iNEST Reference Pipeline - manages BibTeX refs + Zotero integration."""
import os, re, json, sqlite3
from pathlib import Path

class RefPipeline:
    def __init__(self, workspace):
        self.workspace = Path(workspace)
        self.papers_dir = self.workspace / '50_Output' / '51_Papers'
        self.bib_path = self.papers_dir / 'cst_references.bib'
        self.zotero_db = Path(os.path.expandvars(r'%USERPROFILE%\Zotero\zotero.sqlite'))
    
    def parse_refs_from_paper(self, paper_path):
        with open(paper_path, 'r', encoding='utf-8') as f:
            text = f.read()
        ref_start = text.find('References')
        if ref_start < 0:
            return []
        ref_text = text[ref_start:]
        refs = re.split(r'\n(?=\[\d+\])', ref_text)
        return [re.sub(r'^\[\d+\]\s*', '', r).replace('\n', ' ') for r in refs if r.strip() and 'References' not in r[:20]]
    
    def refs_to_bibtex(self, refs):
        entries = []
        for i, ref in enumerate(refs, 1):
            cleaned = ref.replace('\ufffd', '-')
            cleaned = re.sub(r'[锟斤拷紺鈥哻\xa0]+', '-', cleaned)
            parts = cleaned.split('.')
            author = parts[0].strip() if parts else 'Unknown'
            title = parts[1].strip() if len(parts) > 1 else cleaned[:100]
            year_match = re.search(r'\b(19|20)\d{2}\b', cleaned)
            year = year_match.group(0) if year_match else str(2000+i)
            last_name = re.sub(r'[^a-zA-Z]', '', author.split(',')[0].split()[-1] if author else 'Unknown')
            key = f'{last_name}{year}'
            entry = f'@article{{{key},\n  author = {{{author}}},\n  title = {{{title}}},\n  year = {{{year}}},\n  note = {{{cleaned}}}\n}}'
            entries.append(entry)
        return '\n\n'.join(entries)
    
    def export_bib(self, refs=None, paper_path=None):
        if refs is None and paper_path:
            refs = self.parse_refs_from_paper(paper_path)
        if not refs:
            return None
        bib = self.refs_to_bibtex(refs)
        self.bib_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.bib_path, 'w', encoding='utf-8') as f:
            f.write(bib)
        n = len(re.findall(r'@article', bib))
        print(f'Exported {n} references to {self.bib_path}')
        return str(self.bib_path)
    
    def check_zotero(self):
        if not self.zotero_db.exists():
            return {'ok': False, 'msg': 'DB not found'}
        db = sqlite3.connect(str(self.zotero_db))
        n = db.execute('SELECT COUNT(*) FROM items').fetchone()[0]
        db.close()
        return {'ok': True, 'items': n, 'msg': f'{n} items'}
    
    def validate(self, paper_path):
        refs = self.parse_refs_from_paper(paper_path)
        bib_count = 0
        if self.bib_path.exists():
            with open(self.bib_path, 'r', encoding='utf-8') as f:
                bib_count = len(re.findall(r'@article', f.read()))
        ok = bib_count == len(refs) if bib_count > 0 else None
        return {'paper_refs': len(refs), 'bib_entries': bib_count, 'match': ok}

if __name__ == '__main__':
    rp = RefPipeline(r'D:\Obsidian\home\work\.openclaw\workspace')
    paper = str(rp.papers_dir / 'A1_ARS评审与终稿' / 'A1_CST_FromPDF_MD.md')
    print('=== CST Reference Pipeline ===')
    print(f'Paper: {paper}')
    print(f'Zotero: {rp.check_zotero()["msg"]}')
    bib = rp.export_bib(paper_path=paper)
    v = rp.validate(paper)
    print(f'Validation: {v["paper_refs"]} paper refs, {v["bib_entries"]} bib entries')
