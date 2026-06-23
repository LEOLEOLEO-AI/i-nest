fpath = r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html"
with open(fpath, "r", encoding="utf-8") as f:
    html = f.read()

old_copy = '''function copyPath(path){
  navigator.clipboard.writeText(path).then(function(){
    showToast("已复制: "+path);
  }).catch(function(){
    showToast("复制失败，请手动复制");
  });
}'''

new_copy = '''function copyPath(path){
  if(navigator.clipboard&&navigator.clipboard.writeText){
    navigator.clipboard.writeText(path).then(function(){
      showToast("已复制: "+path);
    }).catch(function(){fallbackCopy(path)});
  }else{fallbackCopy(path)}
}
function fallbackCopy(text){
  var ta=document.createElement("textarea");
  ta.value=text;ta.style.position="fixed";ta.style.left="-9999px";
  document.body.appendChild(ta);ta.select();
  try{document.execCommand("copy");showToast("已复制: "+text)}
  catch(e){showToast("复制失败，请手动复制")}
  document.body.removeChild(ta);
}'''

if old_copy in html:
    html = html.replace(old_copy, new_copy)
    print("copyPath replaced with fallback")
else:
    print("old copyPath not found")

with open(fpath, "w", encoding="utf-8") as f:
    f.write(html)
print("Done. Size:", len(html))
