import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html", "r", encoding="utf-8") as f:
    c = f.read()

if len(c) < 50000:
    print("FAIL: file too small")
    exit(1)

# Replace renderDaily (positions 39486 to 41736)
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

# Find the end of current renderDaily (to the closing } just before renderKanban)
fnstart = c.find('function renderDaily(){')
fnend = c.find('function renderKanban(){')

# Find the closing } of renderDaily (search backwards from renderKanban)
search = c[:fnend]
# Find the last } before renderKanban, which closes renderDaily
close_pos = search.rfind('}') + fnstart
if close_pos < fnstart:
    print("FAIL: could not find closing }")
    exit(1)

print(f"Replacing renderDaily: {fnstart} to {close_pos+1}")
before = c[:fnstart]
after = c[close_pos+1:]
c = before + new_renderDaily + "\n\n" + after

# Now find and replace resolvePath
rstart = c.find('function resolvePath(link){')
rnext = c.find('function openDetail(id){')

if rstart >= 0 and rnext > rstart:
    search = c[:rnext]
    close_pos = search.rfind('}') + rstart
    
    new_resolvePath = """function resolvePath(linkk){
  if(!link)return '';
  var abs = 'D:/Obsidian/home/work/.openclaw/workspace/' + link.replace(/\\/g, '/');
  return 'obsidian://open?path=' + encodeURIComponent(abs);
}"""
    
    before = c[:rstart]
    after = c[close_pos:1:]
    c = before + new_resolvePath + "\n\n" + after
c = c.replace('var weekdays = ["\u65e5","\u4e00","\u4e8c","\u4e09","\u56db","\u4e94","\u516d"];', 'var WEEKDAYS = ["\u65e5","\u4e00","\u4e8c","\u4e09","\u56db","\u4e94","\u516d"];')

with open(r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html", "w", encoding="utf-8", newline="") as f:
    f.write(c)

print("OK - renderDaily and resolvePath fixed")