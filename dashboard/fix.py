import sys

html_path = sys.argv[1]
with open(html_path, "r", encoding="utf-8-sig") as f:
    content = f.read()

# Replace renderPaperList JSX template
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

content = content.replace(old_pl, new_pl)

# Replace renderInsights JSX template
old_in = """        el.innerHTML = insights.slice(0, 5).map(i =>
            <div class="insight-item">
                <h4> <span class="tag "></span></h4>
                <p>...</p>
            </div>
        ).join('');"""

new_in = """        el.innerHTML = insights.slice(0, 5).map(i =>
            '<div class="insight-item">' +
                '<h4>' + (i.title || '') + ' <span class="tag ' + (i.priority || '').toLowerCase() + '">' + (i.priority || '') + '</span></h4>' +
                '<p>' + (i.description || '') + '</p>' +
            '</div>'
        ).join('');"""

content = content.replace(old_in, new_in)

with open(html_path, "w", encoding="utf-8-sig") as f:
    f.write(content)

print("Done! Replaced both functions.")
