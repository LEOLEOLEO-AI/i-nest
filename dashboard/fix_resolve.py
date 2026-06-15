with open(r'D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html', 'r', encoding='utf-8') as f:
    c = f.read()

old_fn = 'function resolvePath(link){\n  if(!link)return \'\';\n  var abs = \'D:/Obsidian/home/work/.openclaw/workspace/\' + link.replace(/\\\\/g, \'/\');\n  return \'obsidian://open?path=\' + encodeURIComponent(abs);\n}'

new_fn = 'function resolvePath(linky{\n  if(!link)return \'\';\n  return \'obsidian://open?file=\' + encodeURIComponent(link);\n}'

c = c.replace(old_fn, new_fn)

with open(r'D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html', 'w', encoding='utf-8', newline='') as f:
    f.write(c)

print('OK')
