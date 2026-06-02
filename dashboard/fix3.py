f = r'D:\Research\research_platform\dashboard\index.html'
with open(f, 'r', encoding='utf-8-sig') as fh:
    lines = fh.readlines()

# Lines are 0-indexed. renderPaperList broken lines: 407-412 (1-indexed) = 406-411 (0-indexed)
# renderInsights broken lines: 418-423 (1-indexed) = 417-422 (0-indexed)

new_pl_lines = [
    "            el.innerHTML = papers.map(p =>\n",
    "                '<li>' +\n",
    "                    '<div class=\"paper-title\">' + (p.title || '') + '</div>' +\n",
    "                    '<div class=\"paper-meta\">' + (p.authors || 'unknown') + '  |  ' + (p.date || '') + ' | <span class=\"tag ' + (p.direction || '').toLowerCase().replace(/[^a-z0-9]/g,'') + '\">' + (p.source || '') + '</span></div>' +\n",
    "                '</li>'\n",
    "            ).join('');\n",
]

new_in_lines = [
    "        el.innerHTML = insights.slice(0, 5).map(i =>\n",
    "            '<div class=\"insight-item\">' +\n",
    "                '<h4>' + (i.title || '') + ' <span class=\"tag ' + (i.priority || '').toLowerCase() + '\">' + (i.priority || '') + '</span></h4>' +\n",
    "                '<p>' + (i.description || '') + '</p>' +\n",
    "            '</div>'\n",
    "        ).join('');\n",
]

# Replace lines 406-411 (6 lines -> 6 lines)
result = lines[:406] + new_pl_lines + lines[412:417] + new_in_lines + lines[423:]

with open(f, 'w', encoding='utf-8-sig', newline='') as fh:
    fh.writelines(result)

print(f'Replaced! Old lines: {len(lines)}, New: {len(result)}')
