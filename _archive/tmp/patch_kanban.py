import re

fpath = r'D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html'
with open(fpath, 'r', encoding='utf-8') as f:
    html = f.read()

print('Size:', len(html))

# FIX 1: Filter chips onclick quoting
# The bug: onclick='setIndexFilter(\"cat\",\"...\")' generates nested quotes
# Fix: find these patterns in the JS source and replace backslash-quote with HTML entity
count = 0
def fix_onclick(m):
    global count
    count += 1
    s = m.group(0)
    # Replace escaped quotes inside onclick with HTML entities
    # Pattern: onclick='setIndexFilter(\"X\",\"Y\")' 
    s = s.replace('\\\"', '&quot;')
    return s

# Match onclick attributes in the JS source
html = re.sub(r'onclick=\\"setIndexFilter\([^\)]*\)\\"', fix_onclick, html)
print('Patched onclick handlers:', count)

# Verify
if '&quot;dim&quot;' in html:
    print('OK: HTML entities in dim filter')
if '&quot;cat&quot;' in html:
    print('OK: HTML entities in cat filter')
if '&quot;status&quot;' in html:
    print('OK: HTML entities in status filter')

# FIX 2: Modal links - make file paths clickable
# The openDetail function generates: <code>'+e.link+'</code>
# We want: <a href='file:///D:/Obsidian/'+e.link+' target='_blank'>'+e.link+'</a>
old_code = "<code style=\\\"background:var(--surface2);padding:4px 8px;border-radius:4px;font-size:0.85em;word-break:break-all\\\">'+e.link+'</code>"
new_link = "<a href=\\\"file:///D:/Obsidian/'+e.link+'\\\" style=\\\"color:var(--tcc);text-decoration:underline;word-break:break-all\\\" target=\\\"_blank\\\">'+e.link+'</a>"

if old_code in html:
    html = html.replace(old_code, new_link)
    print('OK: Modal links now clickable')
else:
    print('WARNING: Old modal code pattern not found')
    # Try simpler pattern
    alt_old = \"'+e.link+'</code>\"
    if alt_old in html:
        print('Found alternate pattern')

# FIX 3: Daily progress - add 6/5 
old_daily = '\\'daily\\': [{\\'date\\':\\'2026-06-04\\''
new_daily_0605 = '\\'daily\\': [{\\'date\\':\\'2026-06-05\\',\\'type\\':\\'today\\',\\'progress\\':[{\\'text\\':\\'看板v3迭代：修复筛选联动、文件超链接、新增14篇论文专利索引\\',\\'dot\\':\\'done\\',\\'dim\\':\\'TCC+iNEST\\'},{\\'text\\':\\'Meta-Topology SDI-Bond论文v3修订完成\\',\\'dot\\':\\'done\\',\\'dim\\':\\'TCC\\'},{\\'text\\':\\'CST Theory V26修订版定稿\\',\\'dot\\':\\'done\\',\\'dim\\':\\'TCC\\'},{\\'text\\':\\'SDI v30多区域拓扑仿真参数调优\\',\\'dot\\':\\'ongoing\\',\\'dim\\':\\'TCC\\'},{\\'text\\':\\'连接组数据下载管线搭建\\',\\'dot\\':\\'ongoing\\',\\'dim\\':\\'iNEST\\'}],\\'plan\\':[{\\'text\\':\\'SDI v30多区域跨尺度耦合验证\\',\\'dot\\':\\'plan\\',\\'dim\\':\\'TCC\\'},{\\'text\\':\\'FEP-STDP收敛性证明完成并写入专利\\',\\'dot\\':\\'plan\\',\\'dim\\':\\'iNEST\\'},{\\'text\\':\\'iNEST核心架构论文Results撰写\\',\\'dot\\':\\'plan\\',\\'dim\\':\\'iNEST\\'}]},{\\'date\\':\\'2026-06-04\\''

if old_daily in html:
    html = html.replace(old_daily, new_daily_0605)
    print('OK: Added 6/5 daily record')
else:
    print('WARNING: Daily pattern not found, checking...')
    if '2026-06-04' in html:
        print('  6/4 exists in HTML')

with open(fpath, 'w', encoding='utf-8') as f:
    f.write(html)
print('Final size:', len(html))
print('Done!')
