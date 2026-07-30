#!/usr/bin/env python3
"""
P1.2: 20_Processing 工作流 — LLM提取观点 + 去重 + 质量过滤
处理: 20_Processing → 提取核心观点 → 去重 → 分派到 TCC/iNEST
"""
import os, sys, json, re, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from openai import OpenAI
from dotenv import load_dotenv

VAULT = Path(r"D:\Obsidian\vault")
load_dotenv(VAULT / ".env", override=True)
PROCESSING = VAULT / "20_Processing"
KEY = os.environ.get("DEEPSEEK_API_KEY", "")
client = OpenAI(api_key=KEY, base_url="https://api.deepseek.com/v1")

def extract_opinions(files, batch_size=10):
    """Batch process files to extract key opinions"""
    all_opinions = []
    for i in range(0, len(files), batch_size):
        batch = files[i:i+batch_size]
        file_texts = []
        for f in batch:
            try:
                c = f.read_text(encoding="utf-8", errors="replace")[:2000]
                file_texts.append(f"FILE: {f.name}\n{c}")
            except: pass
        
        if not file_texts: continue
        
        prompt = f"""分析以下{len(file_texts)}篇研究资料，返回JSON数组。每篇提取:
[{{"file": "文件名", "direction": "TCC/iNEST/both", "opinion": "核心观点(30字)", "value": "high/medium/low", "action": "可转化行动"}}]

资料内容:
{chr(10).join(file_texts)[:12000]}"""
        
        try:
            resp = client.chat.completions.create(
                model="deepseek-chat", messages=[{"role":"user","content":prompt}],
                temperature=0.3, max_tokens=2048, timeout=90
            )
            text = resp.choices[0].message.content
            arr = re.search(r'\[[\s\S]*\]', text)
            if arr:
                items = json.loads(arr.group())
                all_opinions.extend(items)
        except Exception as e:
            print(f"  Batch error: {e}")
    
    return all_opinions

def deduplicate_files(files):
    """Find near-duplicate files by content hash"""
    from hashlib import md5
    hashes = defaultdict(list)
    for f in files:
        try:
            h = md5(f.read_text(encoding="utf-8", errors="replace")[:500].encode()).hexdigest()
            hashes[h].append(f)
        except: pass
    
    dupes = {h: flist for h, flist in hashes.items() if len(flist) > 1}
    return dupes

def process_processing_dir(dry_run=False):
    """Main processing workflow"""
    if not PROCESSING.exists():
        print("20_Processing not found")
        return
    
    files = list(PROCESSING.rglob("*.md"))
    if not files:
        print("No files in 20_Processing")
        return
    
    print(f"Processing {len(files)} files...")
    
    # Step 1: Dedup
    print("[1/3] Checking duplicates...")
    dupes = deduplicate_files(files)
    if dupes:
        print(f"  Found {len(dupes)} duplicate groups")
        archive_dir = VAULT / "80_Archive" / "processing_dupes"
        archive_dir.mkdir(parents=True, exist_ok=True)
        for h, flist in dupes.items():
            # Keep largest, archive rest
            flist.sort(key=lambda x: x.stat().st_size, reverse=True)
            for dup in flist[1:]:
                if not dry_run:
                    dest = archive_dir / dup.name
                    shutil.move(str(dup), str(dest))
                    print(f"    Archived duplicate: {dup.name}")
    
    # Step 2: Extract opinions
    print("[2/3] Extracting opinions via DeepSeek...")
    remaining = list(PROCESSING.rglob("*.md"))
    opinions = extract_opinions(remaining)
    print(f"  Extracted {len(opinions)} opinions")
    
    # Step 3: Dispatch to TCC/iNEST
    print("[3/3] Dispatching to target directories...")
    tcc_count, inest_count = 0, 0
    for f in remaining:
        try:
            op = next((o for o in opinions if o and o.get("file") == f.name), None)
            direction = "TCC"
            value = "medium"
            if op:
                direction = str(op.get("direction", "TCC")) if op.get("direction") else "TCC"
                value = str(op.get("value", "medium")) if op.get("value") else "medium"
            
            if value == "low":
                dest_dir = VAULT / "80_Archive" / "low_value"
            elif direction == "iNEST" or direction == "both":
                dest_dir = VAULT / "40_iNEST" / "41_Theory"
                inest_count += 1
            else:
                dest_dir = VAULT / "30_TCC" / "31_Theory"
                tcc_count += 1
            
            dest_dir.mkdir(parents=True, exist_ok=True)
            if not dry_run:
                dest = dest_dir / f.name
                if not dest.exists():
                    shutil.move(str(f), str(dest))
        except Exception as e:
            print(f"  Error moving {f.name}: {e}")
    
    print(f"Done: TCC={tcc_count}, iNEST={inest_count}, low_value archived")

if __name__ == "__main__":
    process_processing_dir(dry_run="--dry-run" in sys.argv)
