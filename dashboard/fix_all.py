import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html", "r", encoding="utf-8") as f:
    c = f.read()

# 1. Fix renderDaily: use dynamic "last 3 days in data" instead of hardcoded dates
new_renderDaily = """function renderDaily(){
  try{
    var days=appData.daily;
    var today=(new Date()).toISOString().slice(0,10);
    var y=(new Date(Date.now()-86400000)).toISOString().slice(0,10);
    days.forEach(function(d){d._t=d.date===today?'today':d.date===y?'yesterday':'past'});
    document.getElementById('daily-badge').textContent="\u6700\u8fd1 "+days.length+" \u5929";

    var td=days.find(function(d){return d._t==='today'});
    var pl=document.getElementById('today-plan-list');
    var pe=document.getElementById('plan-empty');
    var pd=document.getElementById('plan-date');
    if(td&&td.plan&&td.plan.length){
      pd.textContent=td.date;
      pl.innerHTML=td.plan.map(function(p){
        var dc=p.dim==='TCC'?'tcc-dot':p.dim==='iNEST'?'inest-dot':'both-dot';
        return '<div class=\"plan-item\"><span class=\"plan-dot '+dc+'\">'+(p.dim||'?')[0]+'</span><span>'+p.text+' <span style=\"font-size:0.7em;color:var(--text-dim)\">['+(p.dim||'')+']</span></span></div>';
      }).join('');
      pe.style.display='none';pl.style.display='';
    }else{
      pd.textContent=today;pl.innerHTML='';pl.style.display='none';pe.style.display='';
    }

    // Progress: last 3 days IN DATA (not hardcoded dates), excluding today
    var pastDays = days.filter(function(d){return d._t!=='today'}).slice(0,3);
    var grid=document.getElementById('daily-grid');
    grid.innerHTML=pastDays.map(function(d){
      var h='<div class=\"daily-card\"><div class=\"daily-card-header\"><span class=\"date\">'+d.date+'</span><span class=\"date-badge '+(d._t==='yesterday'?'yesterday':'past')+'\">'+(d._t==='yesterday'?"\u6628\u5929":d.date)+'</span></div>';
      if(d.progress&&d.progress.length){
        h+='<div class=\"daily-section-label\">[\u8fdb\u5c55]</div>';
        h+=d.progress.slice(0,5).map(function(p){
          return '<div class=\"daily-item\"><span class=\"dot '+p.dot+'\"></span><span>'+p.text+' <span style=\"font-size:0.7em;color:var(--text-dim)\">['+p.dim+']</span></span></div>';
        }).join('');
      }
      h+='</div>';return h;
    }).join('');
  }catch(e){
    document.getElementById('daily-grid').innerHTML='<div style=\"color:#f87171;padding:20px\">\u52a0\u8f7d\u5931\u8d25\uff0c\u8bf7\u5230\u65b0</div>';
    console.error('renderDaily',e);
  }
}"""

# Replace the entire renderDaily function
fnstart = c.find('function renderDaily(){')
kanstart = c.find('function renderKanban(){')
if fnstart >= 0 and kanstart > fnstart:
    before = c[:fnstart]
    after = c[kanstart:]
    c = before + new_renderDaily + "\n\n" + after

# 2. Fix resolvePath: use absolute path for all files

old_resolve = r'function resolvePath(link){\n  var isMd=\/\.md\$\/i.test(link);\n  var vaultPath;\n  var outside=["GetNotes_Inbox\/","scripts\/","iNEST_CS","iNEST对外","DEMO_SCRIPT"];\n  var isOutside=false;\n  for(var i=0;i<outside.length;i++){\n    if(link.indexOf(outside[i])===0){isOutside=true;break}\n  }\n  if(isOutside){\n    vaultPath=link;\n  }else{\n    vaultPath="home\/work\\.openclaw\.workspace\/"+link;\n  }\n  if(isMd){\n    return\"obsidian:\/\/open?file=\"+encodeURIComponent(vaultPath);\n  }\n  var base=isOutside?\"D:\/Obsidian\/\":\"D:\/Obsidian\/home\/work\\.openclaw\.workspace\/\";\n  return\"file:\/\/\/\"+base+link;\n}'

new_resolve = """function resolvePath(link){
  if(!link)return'';
  var base='D:/Obsidian/home/work/.openclaw/workspace/';
  var abs=base+link.replace(/\\/g,'/');
  return'obsidian://open?path='+encodeURIComponent(abs);
}"""

c = c.replace(old_resolve, new_resolve)

# 3. Fix openDetail: remove encodeURI from display text
# Also add a direct clickable link that works
old_openDetail = r'linkHtml=\'<div class=\"modal-field\"\'+''
old_openDetail_regex = r'linkHtml=\\'<div class=\"modal-field\"><label>\u5173\u8054\u6587\u4ef6<\/label><div class=\"val\" style=\"display:flex;align-items:center;gap:8px;flex-wrap:wrap\"><a href=\"\'+\'+\' \''+resolvePath(e.link)+\'\''+\'+\' style=\"color:var(--tcc);text-decoration:underline;word-break:break-all\" target=\"_blank\">\'\'+e\'.\'+\'link\'\'+\'\'\'+\'</a><button class=\"btn-sm info\" onclick=\"copyPath(\\'\'+e.link.replace(/\\'/g,\"\\\\'\")+\'\')\">\ud4f7\ub62f \u590d\u8ddd\u5f84\u843c<\/button><\/div><\/div>\';'

# New openDetail line: ensure obsidian:// link works
new_linkHtml = "linkHtml=\'<div class=\"modal-field\"><label>\u5173\u8054\u6587\u4ef6</label><div class=\"val\" style=\"display:flex;align-items:center;gap:8px;flex-wrap:wrap\"><a href=\"'+resolvePath(e.link)+'\" style=\"color:var(--tcc);text-decoration:underline;word-break:break-all;cursor:pointer\" target=\"_blank\">'+e.link+'</a><button class=\"btn-sm info\" onclick=\"copyPath(\\''+e.link.replace(/\\'/g,\"\\\\\'\")+'\')\">\ud4f7\ub62f \u590d\u8ddd\u5f84\u843c</button></div></div>\';'"

c = c.replace(old_openDetail_regex, new_linkHtml)

with open(r'D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html', 'w', encoding='utf-8', newline='') as f:
    f.write(c)

print('OK')
