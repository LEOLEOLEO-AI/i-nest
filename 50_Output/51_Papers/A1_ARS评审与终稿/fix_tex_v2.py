
import re

path = r'D:\Obsidian\home\work\.openclaw\workspace\50_Output\51_Papers\A1_ARS评审与终稿\latex\A1_CST_clean.tex'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

fixes = {}

# 1. Gammast -> Gamma_{st}
fixes['Gammast'] = content.count('\\Gammast')
content = content.replace('\\Gammast', '\\Gamma_{st}')

# 2. Dollar-subscript-dollar pattern
pattern = re.compile(r'\\$([A-Za-z0-9]+)\\$_([a-zA-Z0-9_]+)\\$\\$')
fixes['dollar_sub'] = len(pattern.findall(content))
content = pattern.sub(r'\\$\\1_{\\2}\\$', content)

# 3. lambda_eff
content = content.replace('\\$\\\\lambda\\$_eff', '\\$\\\\lambda_{eff}\\$')

# 4. CST patterns  
content = content.replace('CS\\$T\\$_emergent_max\\$\\$', '\\$CST_{\\text{emergent_max}}\\$')
content = content.replace('CS\\$T_{species}\\$', '\\$CST_{\\text{species}}\\$')

# 5. Normalize line endings
content = content.replace('\r\n', '\n').replace('\r', '\n')

# 6. P_norm
content = content.replace('\\$P\\$_norm\\$\\$', '\\$P_{\\text{norm}}\\$')

out_path = path.replace('.tex', '_FIXED.tex')
with open(out_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

print(f'Fixes: {fixes}')
print(f'Output file written: {out_path}')
print(f'Size: {len(content)} chars, {len(content.splitlines())} lines')

# Find remaining $$ issues
remaining = []
for i, line in enumerate(content.split('\n'), 1):
    stripped = line.strip()
    if not stripped.startswith('%'):
        ds = stripped.count('$$')
        if ds > 0:
            remaining.append(f'L{i}: {stripped[:80]}')
print(f'Remaining lines with dollar-dollar: {len(remaining)}')
for r in remaining[:10]:
    print(f'  {r}')
