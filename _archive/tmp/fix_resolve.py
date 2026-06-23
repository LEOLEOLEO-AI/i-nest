fpath = r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html"
with open(fpath, "r", encoding="utf-8") as f:
    html = f.read()

# Fix: add resolvePath helper and update openDetail to use it
# 1. Add resolvePath function
old_insert = "function openDetail"
new_func = '''function resolvePath(link){
  var outside=["phase1_workspace/","GetNotes_Inbox/","scripts/","iNEST_CS","iNEST对外","DEMO_SCRIPT"];
  for(var i=0;i<outside.length;i++){
    if(link.indexOf(outside[i])===0)return"file:///D:/Obsidian/"+encodeURI(link);
  }
  return"file:///D:/Obsidian/home/work/.openclaw/workspace/"+encodeURI(link);
}
function openDetail'''

if old_insert in html:
    html = html.replace(old_insert, new_func)
    print("Added resolvePath function")
else:
    print("Insert point not found")

# 2. Update the link href in openDetail to use resolvePath
# Old: file:///D:/Obsidian/home/work/.openclaw/workspace/'+encodeURI(e.link)+'
# New: "'+resolvePath(e.link)+'"
old_href = "file:///D:/Obsidian/home/work/.openclaw/workspace/'+encodeURI(e.link)+'\""
new_href = "\"'+resolvePath(e.link)+'\""
count = html.count(old_href)
html = html.replace(old_href, new_href)
print(f"Replaced {count} href templates")

with open(fpath, "w", encoding="utf-8") as f:
    f.write(html)
print("Done:", len(html))
