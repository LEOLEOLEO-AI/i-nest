import re, os
from collections import Counter

v29 = r'D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_CST_Theory_V29_FROM_PDF.md'
with open(v29, 'r', encoding='utf-8') as f:
    t = f.read()

log = []
log.append(f'Original size: {len(t)}')
log.append(f'U+FFFD (replacement): {t.count(chr(0xFFFD))}')
log.append(f'U+2013 (en-dash): {t.count(chr(0x2013))}')

# STEP 1: Fix en-dash encoding issues
# Check for the specific pattern
count_2013 = t.count(chr(0x2013))
count_c3a2 = t.count('\u00e2\u20ac\u201c')  # UTF-8 encoded en-dash
log.append(f'Raw en-dash U+2013: {count_2013}')

# Look for en-dash patterns shown as "鈥愨€盧" or similar
# Actually, let me check what the garbled characters are
bad_chars = Counter()
for c in t:
    o = ord(c)
    if o > 127 and not (0x0370 <= o <= 0x03FF) and not (0x2000 <= o <= 0x2070) and not (0x2100 <= o <= 0x2150) and not (0x2200 <= o <= 0x2300) and o != 0x221a and o != 0x2264 and o != 0x2265 and o != 0x00b7 and o != 0x00d7 and o != 0x00b1 and not (0x2010 <= o <= 0x2020) and not (0x4e00 <= o <= 0x9fff) and o != 0x03c0 and o != 0x03c6 and o != 0x03b1 and o != 0x03b3 and o != 0x03b7 and o != 0x03b4 and o != 0x03c8 and o != 0x03b5 and o != 0x0393 and o != 0x0398 and o != 0x03a6 and o != 0x03a0 and o != 0x03a3 and o != 0x03bb and o != 0x03b8 and o != 0x03c1 and o != 0x03c3 and o != 0x03c4 and o != 0x03b9 and o != 0x00d7:
        bad_chars[c] += 1

log.append(f'\\nUnusual non-ASCII chars found:')
for c, cnt in bad_chars.most_common(30):
    log.append(f'  U+{ord(c):04X} = {c!r} : {cnt}')

with open(v29.replace('.md', '_diagnosis.txt'), 'w', encoding='utf-8') as f:
    f.write('\\n'.join(log))
print('Diagnosis completed')
