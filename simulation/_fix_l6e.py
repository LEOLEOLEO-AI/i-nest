p = r'D:\Obsidian\home\work\.openclaw\workspace\simulation\sdi_l6_general.py'
c = open(p, 'r', encoding='utf-8').read()
# Fix the broken line - check what we have
import re
# Find the judgment section
idx = c.find('l6_s = ')
if idx > 0:
    # Show surrounding context
    snippet = c[idx:idx+200]
    print('Found:', repr(snippet[:120]))
    
# Fix: ensure l6_e is defined
old = "l6_s = s4['mean_sigma']>3.0  # BA scale-free threshold\nl6_e"
new = "l6_s = s4['mean_sigma']>3.0\nl6_e"
if old in c:
    c = c.replace(old, new)
else:
    # Try without newline
    for line in c.split('\n'):
        if 'l6_s' in line and 'mean_sigma' in line:
            print('Line:', repr(line))
    
open(p, 'w', encoding='utf-8').write(c)
print('Fixed')
