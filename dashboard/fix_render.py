import re

with open(r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html", "r", encoding="utf-8") as f:
    content = f.read()

# correct Chinese strings
new_renderDaily = """function renderDaily(){
  try{
    var days=appData.daily;
    var today=(new Date()).toISOString().slice(0,10);
    var y=(new Date(Date.now()-86400000)).toISOString().slice(0,10);
    var d2=(new Date(Date.now()-172800000)).toISOString().slice(0,10);
    var d3=(new Date(Date.now()-259200000)).toISOString().slice(0,10);
    var pastDates=[y,d2,d3];
    days.forEach(function(d){d._t=d.date===today?"today":d.date===y?"yesterday":"past"});

    document.getElementById("daily-badge").textContent="\u6700\u8fd1 "+days.length+" \u5929";

    var td=days.find(function(d){return d._t==="today"});
    var pl=document.getElementById("today-plan-list");
    var pe=document.getElementById("plan-empty");
    var pd=document.getElementById("plan-date");
    if(td&&td.plan&&td.plan.length){
      pd.textContent=td.date;
      pl.innerHTML=td.plan.map(function(p){
        var dc=p.dim==="TCC"?"tcc-dot":p.dim==="iNEST"?"inest-dot":"both-dot";
        return "<div class=\\"plan-item\\"><span class=\\"plan-dot "+dc+"\\">"+(p.dim||"?")[0]+"</span><span>"+p.text+" <span style=\\"font-size:0.7em;color:var(--text-dim)\\">["+(p.dim||"")+"]</span></span></div>";
      }).join("");
      pe.style.display="none";pl.style.display="";
    }else{
      pd.textContent=today;pl.innerHTML="";pl.style.display="none";pe.style.display="";
    }

    var grid=document.getElementById("daily-grid");
    grid.innerHTML=days.filter(function(d){return pastDates.indexOf(d.date)>=0}).map(function(d){
      var h="<div class=\\"daily-card\\"><div class=\\"daily-card-header\\"><span class=\\"date\\">"+d.date+"</span><span class=\\"date-badge "+(d._t==="yesterday"?"yesterday":"past")+"\\">"+(d._t==="yesterday"?"\u6628\u5929":d.date)+"</span></div>";
      if(d.progress&&d.progress.length){
        h+="<div class=\\"daily-section-label\\">[\u8fdb\u5c55]</div>";
        h+=d.progress.slice(0,5).map(function(p){
          return "<div class=\\"daily-item\\"><span class=\\"dot "+p.dot+"\\"></span><span>"+p.text+" <span style=\\"font-size:0.7em;color:var(--text-dim)\\">["+p.dim+"]</span></span></div>";
        }).join("");
      }
      h+="</div>";return h;
    }).join("");
  }catch(e){
    document.getElementById("daily-grid").innerHTML="<div style=\\"color:#f87171;padding:20px\\">\u52a0\u8f7d\u5931\u8d25\uff0c\u8bf7\u5237\u65b0</div>";
    console.error("renderDaily",e);
  }
}"""

old = r'function renderDaily\(data\) \{.*?\nfunction renderDaily\(\) \{.*?\n\}'
content = re.sub(old, new_renderDaily, content, flags=re.DOTALL)

with open(r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html", "w", encoding="utf-8", newline="") as f:
    f.write(content)
print("OK")
