import re, os, json

v29=r'D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_CST_Theory_V29_FROM_PDF.md'
t=open(v29,encoding='utf-8').read()
lines=t.split('\n')

# Find References section
ref_idx = None
for i,l in enumerate(lines):
    if l.strip()=='## References':
        ref_idx = i
        break

# Extract 69 references
refs = []
current = ''
for i in range(ref_idx+1, min(ref_idx+350, len(lines))):
    l = lines[i]
    if l.strip().startswith('## '):
        break
    if l.strip():
        if re.match(r'^\[\d+\]', l.strip()):
            if current:
                refs.append(current.strip())
            current = l.strip()
        else:
            if current:
                current += ' ' + l.strip()

if current:
    refs.append(current.strip())

# Generate citation keys + bib entries
bib_entries = []
key_map = {}  # [1] -> key_name

for i, ref in enumerate(refs):
    num = i + 1
    text = ref.split('] ', 1)[1] if '] ' in ref else ref
    
    # Extract first author surname
    author_match = re.match(r'^([^,]+)', text)
    surname = author_match.group(1) if author_match else 'Unknown'
    surname = surname.split(' ')[0] if surname else 'Unknown'
    surname = surname.replace('.','').replace('"','').strip()
    
    # Extract year
    year_match = re.search(r'\((\d{4})\)', text)
    year = year_match.group(1) if year_match else '0000'
    
    # Extract first meaningful word of title
    title_match = re.search(r'"([^"]+)"', text)
    title_word = ''
    if title_match:
        words = title_match.group(1).split()
        title_word = words[0].lower() if words else 'ref'
        title_word = re.sub(r'[^a-z0-9]', '', title_word)[:15]
    
    # Build citation key
    key = surname.lower() + year + (title_word if len(surname + year) < 20 else '')
    key = re.sub(r'[^a-z0-9]', '', key)
    if not key or len(key) < 3:
        key = 'ref' + str(num)
    
    key_map[str(num)] = key
    
    # Build bib entry
    bib = '@article{' + key + ',\n'
    bib += '  author = {' + text.split('"')[0].strip(', .') + '},\n'
    
    title_end = text.find('"')
    title_start = title_end + 1 if title_end >= 0 else 0
    title_end2 = text.find('"', title_start) if title_end >= 0 else len(text)
    title = text[title_start:title_end2] if title_end >= 0 else text[:60]
    
    bib += '  title = {' + title + '},\n'
    bib += '  year = {' + year + '},\n'
    
    # Journal info
    journal_part = text[title_end2+1:] if title_end >= 0 else text
    journal_match = re.match(r'[^.]*\.\s*([^,]+)', journal_part)
    if journal_match:
        bib += '  journal = {' + journal_match.group(1).strip().strip('"') + '},\n'
    
    bib += '  note = {' + text + '}\n'
    bib += '}\n'
    bib_entries.append(bib)

# Write .bib file
bib_path = r'D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\cst_references_v29.bib'
with open(bib_path, 'w', encoding='utf-8') as f:
    f.write('% CST Theory V29 - Auto-generated references\n')
    f.write('% Generated: 2026-06-21\n\n')
    for entry in bib_entries:
        f.write(entry + '\n')

# Write key mapping for reference
map_path = r'D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\ref_key_map.json'
with open(map_path, 'w', encoding='utf-8') as f:
    json.dump(key_map, f, indent=2, ensure_ascii=False)

# Summary
print('=' * 60)
print(f'Total references extracted: {len(refs)}')
print(f'Bib file: {bib_path}')
print(f'Key map: {map_path}')
print()
print('Sample keys (first 10):')
for k, v in list(key_map.items())[:10]:
    ref = refs[int(k)-1][:60]
    print(f'  [{k}] -> @{v}  ({ref}...)')
print()
print('Sample keys (last 5):')
for k, v in list(key_map.items())[-5:]:
    print(f'  [{k}] -> @{v}')
