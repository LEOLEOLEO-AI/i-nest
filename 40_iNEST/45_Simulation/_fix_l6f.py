p = r'D:\Obsidian\home\work\.openclaw\workspace\simulation\sdi_l6_general.py'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()

# Find and fix the problematic line
old_bad = "l6_s = s4['mean_sigma']>3.0  # BA scale-free threshold; l6_e = s4['mean_el']>0.10 or s4['cross_el_ratio']>0.10"
new_good = "l6_s = s4['mean_sigma']>3.0\n    l6_e = s4['mean_el']>0.10 or s4['cross_el_ratio']>0.10"

if old_bad in c:
    c = c.replace(old_bad, new_good)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(c)
    print('Fixed: split l6_s and l6_e')
else:
    print('Pattern not found, searching...')
    for i, line in enumerate(c.split('\n')):
        if 'l6_s' in line and 'l6_e' in line:
            print(f'Line {i}: {line}')
