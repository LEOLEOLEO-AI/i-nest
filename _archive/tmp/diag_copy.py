fpath = r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html"
with open(fpath, "r", encoding="utf-8") as f:
    html = f.read()

# Find the copyPath function
idx = html.find("function copyPath")
if idx > 0:
    end = html.find("function ", idx + 10)
    if end < 0:
        end = idx + 400
    print(html[idx:end])
