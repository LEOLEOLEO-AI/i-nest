import sys

html_path = r'D:\Research\research_platform\dashboard\index.html'

with open(html_path, 'r', encoding='utf-8-sig') as f:
    content = f.read()

def replace_between(text, start_marker, end_marker):
    start = text.find(start_marker)
    if start < 0:
        return text, False
    end = text.find(end_marker, start) + len(end_marker)
    if end < len(end_marker):
        return text, False
    return text[:start] + end_marker.replace(end_marker, '') + text[end:], True

# Replace renderPaperList body (between the function def and its closing })
old_pl = """            el.innerHTML = papers.map(p =>
                <li>
                    <div class="paper-title"></div>
                    <div class="paper-meta">  |  <span class="tag "></span></div>
                </li>
            ).join('');"""

new_pl = """            el.innerHTML = papers.map(p =>
                '<li>' +
                    '<div class="paper-title">' + (p.title || '') + '</div>' +
                    '<div class="paper-meta">' + (p.authors || 'unknown') + '  |  ' + (p.date || '') + ' | <span class="tag ' + (p.direction || '').toLowerCase().replace(/[^a-z0-9]/g,'') + '">' + (p.source || '') + '</span></div>' +
                '</li>'
            ).join('');"""

# Use regex to replace the body between el.innerHTML = papers.map and ).join('');
import re

# Pattern for renderPaperList
pl_pattern = r'(el\.innerHTML = papers\.map\(p => )\s*(<li>[\s\S]*?)\s*(\.join\(\'\);\))'
new_pl_replacement = r'''el.innerHTML = papers.map(p =>
                '<li>' +
                    '<div class="paper-title">' + (p.title || '') + '</div>' +
                    '<div class="paper-meta">' + (p.authors || 'unknown') + '  |  ' + (p.date || '') + ' | <span class="tag ' + (p.direction || '').toLowerCase().replace(/[^a-z0-9]/g,'') + '">' + (p.source || '') + '</span></div>' +
                '</li>'
            ).join('');'''

# Pattern for renderInsights
in_pattern = r'(el\.innerHTML = insights\.slice\(0, 5\)\.map\(i => )\s*(<div class="insight-item">[\s\S]*?)\s*(\.join\(\'\);\))'
new_in_replacement = r'''el.innerHTML = insights.slice(0, 5).map(i =>
            '<div class="insight-item">' +
                '<h4>' + (i.title || '') + ' <span class="tag ' + (i.priority || '').toLowerCase() + '">' + (i.priority || '') + '</span></h4>' +
                '<p>' + (i.description || '') + '</p>' +
            '</div>'
        ).join('');'''

content = re.sub(pl_pattern, new_pl_replacement, content)
content = re.sub(in_pattern, new_in_replacement, content)

with open(html_path, 'w', encoding='utf-8-sig', newline='') as f:
    f.write(content)

print('Done!')
