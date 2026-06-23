import re, os

v29 = r'D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_CST_Theory_V29_FROM_PDF.md'
with open(v29, 'r', encoding='utf-8') as f:
    t = f.read()

changes = []
t0 = t

# === FIX 1: Fix combining circumflex (e^ artifact) ===
# Pattern: e^{  or similar where ^ generates U+0302
old = t
t = t.replace('\u0302', '')
if t != old: changes.append(f'Removed {old.count(chr(0x0302))} combining circumflex')

# === FIX 2: Wrap inline Greek letters in body text ===
# Process line by line to avoid $$ blocks
lines = t.split('\n')
new_lines = []
in_block = False  # $$ display math
in_image = False  # <img> or <p> tags  
fix_count = 0

for i, line in enumerate(lines):
    raw = line
    
    # Skip display math blocks
    if '$$' in raw:
        in_block = not in_block
        new_lines.append(raw)
        continue
    if in_block or raw.startswith('```') or raw.startswith('<img') or raw.startswith('<p') or raw.startswith('<table'):
        new_lines.append(raw)
        continue
    if raw.startswith('#') or raw.startswith('|') or raw.startswith('-') or raw.startswith('['):
        new_lines.append(raw)
        continue
    if not raw.strip():
        new_lines.append(raw)
        continue
    
    # Check if this line has Greek letters outside math mode
    has_greek = bool(re.search(r'[\u0370-\u03FF]', raw))
    has_dollar = '$' in raw
    
    if has_greek and not has_dollar:
        # Smart wrapping: wrap entire line content in $...$ if it contains Greek
        # But skip if it's figure legend or table
        if not raw.startswith('Figure') and not raw.startswith('Table'):
            # Wrap Greek-containing segments in $...$
            # First, isolate text segments that have Greek
            result = []
            i_pos = 0
            greek_mode = False
            # Use regex to find consecutive Greek+math characters
            parts = re.split(r'(\s+)', raw)
            new_parts = []
            for p in parts:
                has_g = bool(re.search(r'[\u0370-\u03FF\u00b7\u00d7\u221a\u2264\u2265\u2070-\u209f\u2080-\u208f]', p))
                if has_g and not p.startswith('(') and not p.startswith('['):
                    p = '$' + p + '$'
                    fix_count += 1
                new_parts.append(p)
            raw = ''.join(new_parts)
    
    new_lines.append(raw)

t = '\n'.join(new_lines)
changes.append(f'Wrapped {fix_count} inline Greek occurrences')

# === FIX 3: Join broken lines in paragraphs ===
# Strategy: lines ending with lowercase/hyphen/conjunction that aren't in special blocks
lines = t.split('\n')
new_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    stripped = line.strip()
    
    # Keep headings, empty lines, lists, tables, code blocks
    if not stripped or stripped.startswith('#') or stripped.startswith('|') or stripped.startswith('- ') or stripped.startswith('* ') or stripped.startswith('```') or stripped.startswith('[') or stripped.startswith('<') or stripped.startswith('$$') or stripped.startswith('!['):
        new_lines.append(line)
        i += 1
        continue
    
    # Check if next line should be joined
    # Join if: current line doesn't end with sentence-ending punctuation AND next line exists and isn't a special line
    if i + 1 < len(lines):
        next_line = lines[i+1].strip()
        if next_line and not next_line.startswith('#') and not next_line.startswith('|') and not next_line.startswith('- ') and not next_line.startswith('* ') and not next_line.startswith('[') and not next_line.startswith('<') and not next_line.startswith('$$') and not next_line.startswith('!['):
            # Don't join if current line ends with period, question, exclamation
            if not stripped.rstrip().endswith('.') and not stripped.rstrip().endswith('?') and not stripped.rstrip().endswith('!') and not stripped.rstrip().endswith(':') and not stripped.rstrip().endswith(';'):
                # Also check if next line starts with uppercase (likely a new sentence)
                if next_line and next_line[0].islower():
                    # Join: remove the line ending from current line
                    if line.endswith(' '):
                        line = line.rstrip()
                    elif line.endswith('-') and not line.endswith('--') and not line.endswith(' \u2013'):
                        line = line[:-1]  # remove hyphen
                    else:
                        line = line.rstrip()
                    line += ' ' + next_line
                    i += 1  # skip next line since we consumed it
                    continue
    
    new_lines.append(line)
    i += 1

t = '\n'.join(new_lines)
changes.append(f'Joined broken lines (reduced from {len(lines)} to {len(t.split(chr(10)))})')

# === FIX 4: Clean up reference section ===
# Remove extra blank lines between reference entries
t = re.sub(r'\n{3,}', '\n\n', t)

# === FIX 5: Fix key formula patterns in abstract and body ===
# Replace standalone formula patterns with $ wrapping
formula_fixes = [
    (r'(?<!\$)CST = \([^)]+\)', lambda m: '$' + m.group(0) + '$'),
]

# === Summary ===
with open(v29, 'w', encoding='utf-8') as f:
    f.write(t)

print('Changes made:')
for c in changes:
    print(f'  {c}')
print(f'Size: {len(t)} (was {len(t0)})')
