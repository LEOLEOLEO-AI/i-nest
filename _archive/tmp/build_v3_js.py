# build_v3_js.py - Fixed JS for filter chips and modal links
import json

# Read the data
exec(open(r"D:\Obsidian\tmp\build_v3_data.py", encoding="utf-8").read())

JS = r"""
var CATS=["灵感","论文","专利","仿真程序","产品代码开发","项目指南策划"];
var DIMS=["TCC","iNEST"];
var STATUSES=["规划中","进行中","撰写中","开发中","测试中","验证中","探索中","资料整理","已完成","已发布","持续更新"];
var appData=JSON.parse(localStorage.getItem("rd_kanban_v3")||"null")||JSON.parse(JSON.stringify(DEFAULT_DATA));
function saveData(){localStorage.setItem("rd_kanban_v3",JSON.stringify(appData))}

function catEmoji(c){var m={"灵感":"\ud83d\udca1","论文":"\ud83d\udcc4","专利":"\ud83c\udff7\ufe0f","仿真程序":"\ud83e\uddea","产品代码开发":"\ud83d\udcbb","项目指南策划":"\ud83d\udccb"};return m[c]||"\ud83d\udccc"}
function statusTag(s){if(["已完成","已发布"].includes(s))return"tag-done";if(["进行中","撰写中","开发中","测试中","验证中"].includes(s))return"tag-ongoing";return"tag-plan"}
function fmtDate(d){return new Date(d).toLocaleDateString("zh-CN",{month:"short",day:"numeric"})}
var WEEKDAYS=["日","一","二","三","四","五","六"];

function renderMetrics(){
  var e=appData.entries;
  var tcc=e.filter(function(x){return x.dim==="TCC"}).length;
  var inest=e.filter(function(x){return x.dim==="iNEST"}).length;
  var active=e.filter(function(x){return !["已完成","已发布"].includes(x.status)}).length;
  var done=e.filter(function(x){return ["已完成","已发布"].includes(x.status)}).length;
  var high=e.filter(function(x){return x.priority==="高"&&!["已完成","已发布"].includes(x.status)}).length;
  document.getElementById("metrics").innerHTML=
    '<div class="metric tcc"><div class="num">'+tcc+'</div><div class="lbl">TCC 拓扑中心</div></div>'+
    '<div class="metric inest"><div class="num">'+inest+'</div><div class="lbl">iNEST 涌现智能</div></div>'+
    '<div class="metric warn"><div class="num">'+active+'</div><div class="lbl">进行中</div></div>'+
    '<div class="metric" style="border-color:rgba(74,222,128,0.3)"><div class="num" style="color:var(--inest)">'+done+'</div><div class="lbl">已完成</div></div>'+
    '<div class="metric purple"><div class="num">'+high+'</div><div class="lbl">高优待办</div></div>';
}

function renderDaily(){
  var days=appData.daily;
  document.getElementById("daily-badge").textContent="最近 "+days.length+" 天";
  document.getElementById("daily-grid").innerHTML=days.map(function(d){
    var html='<div class="daily-card"><div class="daily-card-header"><span class="date">'+d.date+" "+WEEKDAYS[new Date(d.date).getDay()]+'</span><span class="date-badge '+(d.type==="today"?"today":"yesterday")+'">'+(d.type==="today"?"今天":d.type==="yesterday"?"昨天":fmtDate(d.date))+'</span></div>';
    if(d.progress.length){html+='<div class="daily-section-label">\ud83d\udcdd 进展</div>';d.progress.forEach(function(p){html+='<div class="daily-item"><span class="dot '+p.dot+'"></span><span>'+p.text+' <span style="font-size:0.7em;color:var(--text-dim);margin-left:4px">['+p.dim+']</span></span></div>'})}
    if(d.plan.length){html+='<div class="daily-section-label">\ud83c\udfaf 计划</div>';d.plan.forEach(function(p){html+='<div class="daily-item"><span class="dot '+p.dot+'"></span><span>'+p.text+' <span style="font-size:0.7em;color:var(--text-dim);margin-left:4px">['+p.dim+']</span></span></div>'})}
    html+='</div>';return html;
  }).join("");
}

function renderKanban(){
  document.getElementById("kanban-dual").innerHTML=DIMS.map(function(dim){
    var dc=dim.toLowerCase();
    var cols=CATS.map(function(cat){
      var items=appData.entries.filter(function(e){return e.dim===dim&&e.cat===cat});
      var col='<div class="kanban-col"><div class="kanban-col-header">'+catEmoji(cat)+" "+cat+'<span class="count">'+items.length+'</span></div>';
      items.forEach(function(item){
        col+='<div class="kanban-card" onclick="openDetail('+item.id+')"><div class="card-title">'+item.title+'</div><div class="card-meta"><span class="card-tag '+statusTag(item.status)+'">'+item.status+'</span><span>v'+item.ver+'</span><span class="card-tag '+(item.priority==="高"?"tag-high":item.priority==="中"?"tag-med":"")+'">'+item.priority+'</span></div>'+(item.link?'<div style="font-size:0.7em;color:var(--tcc);margin-top:3px">\ud83d\udcce '+item.link.split("/").pop()+'</div>':"")+'</div>';
      });
      if(!items.length)col+='<div style="font-size:0.75em;color:var(--text-dim);padding:8px;text-align:center">暂无条目</div>';
      col+='</div>';return col;
    }).join("");
    return '<div class="kanban-column-group '+dc+'"><h3>'+(dim==="TCC"?"\ud83d\udd37 TCC · 拓扑中心计算":"\ud83d\udd36 iNEST · 复杂网络涌现智能")+'</h3><div class="kanban-grid">'+cols+'</div></div>';
  }).join("");
}

// ---- INDEX TABLE ----
var indexSort={field:"date",dir:-1};
var indexFilters={dim:null,cat:null,status:null,search:""};

function sortArrow(field){
  if(indexSort.field!==field)return'<span class="sort-arrow">\u21c5</span>';
  return indexSort.dir===1?'<span class="sort-arrow">\u2191</span>':'<span class="sort-arrow">\u2193</span>';
}

function toggleSort(field){
  if(indexSort.field===field)indexSort.dir*=-1;
  else{indexSort.field=field;indexSort.dir=1}
  applyIndexFilters();
}

// FIXED: uses &quot; HTML entities to avoid nested double-quote bug in onclick
function setIndexFilter(type,val){
  indexFilters[type]=val;
  if(type==="search"){
    var sb=document.getElementById("index-search");
    if(sb)indexFilters.search=sb.value;
  }
  renderIndexControls();
  applyIndexFilters();
}

function renderIndexControls(){
  var h='<div class="search-box"><span class="search-icon">\ud83d\udd0d</span><input type="text" placeholder="搜索标题、描述、版本..." id="index-search" oninput="setIndexFilter(\'search\')" value="'+indexFilters.search+'"></div>';
  // Dim filters - use &quot; for inner quotes to prevent HTML parse conflicts
  h+='<div class="filter-group">';
  h+='<button class="filter-chip '+(indexFilters.dim===null?"active":"")+'" onclick="setIndexFilter(&quot;dim&quot;,null)">全部维度</button>';
  h+='<button class="filter-chip '+(indexFilters.dim==="TCC"?"active":"")+'" onclick="setIndexFilter(&quot;dim&quot;,&quot;TCC&quot;)">TCC</button>';
  h+='<button class="filter-chip '+(indexFilters.dim==="iNEST"?"active inest-chip":"")+'" onclick="setIndexFilter(&quot;dim&quot;,&quot;iNEST&quot;)">iNEST</button>';
  h+='</div>';
  // Cat filters
  h+='<div class="filter-group">';
  h+='<button class="filter-chip '+(indexFilters.cat===null?"active":"")+'" onclick="setIndexFilter(&quot;cat&quot;,null)">全部分类</button>';
  CATS.forEach(function(c){h+='<button class="filter-chip '+(indexFilters.cat===c?"active":"")+'" onclick="setIndexFilter(&quot;cat&quot;,&quot;'+c+'&quot;)">'+c+'</button>'});
  h+='</div>';
  // Status filters
  h+='<div class="filter-group">';
  h+='<button class="filter-chip '+(indexFilters.status===null?"active":"")+'" onclick="setIndexFilter(&quot;status&quot;,null)">全部状态</button>';
  STATUSES.slice(0,7).forEach(function(s){h+='<button class="filter-chip '+(indexFilters.status===s?"active":"")+'" onclick="setIndexFilter(&quot;status&quot;,&quot;'+s+'&quot;)">'+s+'</button>'});
  h+='</div>';
  h+='<span class="result-count" id="result-count"></span>';
  document.getElementById("index-controls").innerHTML=h;
}

function applyIndexFilters(){
  var entries=[].concat(appData.entries);
  if(indexFilters.dim)entries=entries.filter(function(e){return e.dim===indexFilters.dim});
  if(indexFilters.cat)entries=entries.filter(function(e){return e.cat===indexFilters.cat});
  if(indexFilters.status)entries=entries.filter(function(e){return e.status===indexFilters.status});
  if(indexFilters.search){
    var q=indexFilters.search.toLowerCase();
    entries=entries.filter(function(e){return e.title.toLowerCase().indexOf(q)>=0||e.desc.toLowerCase().indexOf(q)>=0||e.ver.toLowerCase().indexOf(q)>=0});
  }

  var f=indexSort.field,d=indexSort.dir;
  var prioMap={"高":3,"中":2,"低":1};
  entries.sort(function(a,b){
    var va,vb;
    if(f==="priority"){va=prioMap[a.priority]||0;vb=prioMap[b.priority]||0}
    else if(f==="date"){va=a.date;vb=b.date}
    else{va=(a[f]||"").toString();vb=(b[f]||"").toString()}
    if(va<vb)return -1*d;if(va>vb)return 1*d;return 0;
  });

  var rc=document.getElementById("result-count");
  if(rc)rc.textContent="共 "+entries.length+" 条";
  var ib=document.getElementById("index-badge");
  if(ib)ib.textContent=entries.length+" 条记录";

  if(!entries.length){
    document.getElementById("index-tbody").innerHTML="";
    document.getElementById("no-results").style.display="block";
    return;
  }
  document.getElementById("no-results").style.display="none";

  document.getElementById("index-tbody").innerHTML=entries.map(function(e){
    var dc=e.dim.toLowerCase();
    return '<tr>'+
      '<td><span class="dim-badge '+dc+'">'+e.dim+'</span></td>'+
      '<td>'+catEmoji(e.cat)+" "+e.cat+'</td>'+
      '<td><strong style="cursor:pointer;color:var(--tcc)" onclick="openDetail('+e.id+')" title="点击查看详情">'+e.title+'</strong></td>'+
      '<td>'+(e.link?'<span class="ver-link" onclick="openDetail('+e.id+')" title="'+e.link.replace(/"/g,"&quot;")+'">'+e.ver+'</span>':e.ver)+'</td>'+
      '<td><span class="card-tag '+statusTag(e.status)+'">'+e.status+'</span></td>'+
      '<td><span class="card-tag '+(e.priority==="高"?"tag-high":e.priority==="中"?"tag-med":"")+'">'+e.priority+'</span></td>'+
      '<td style="white-space:nowrap">'+e.date+'</td>'+
      '<td style="white-space:nowrap">'+
        '<button class="btn-sm info" onclick="openDetail('+e.id+')">详情</button> '+
        '<button class="btn-sm edit" onclick="openEditForm('+e.id+')">编辑</button> '+
        '<button class="btn-sm danger" onclick="deleteEntry('+e.id+')">删除</button>'+
      '</td></tr>';
  }).join("");
}

function renderIndex(){
  document.getElementById("index-thead").innerHTML='<tr>'+
    '<th onclick="toggleSort(\'dim\')">维度 '+sortArrow("dim")+'</th>'+
    '<th onclick="toggleSort(\'cat\')">分类 '+sortArrow("cat")+'</th>'+
    '<th onclick="toggleSort(\'title\')">名称 '+sortArrow("title")+'</th>'+
    '<th onclick="toggleSort(\'ver\')">版本 '+sortArrow("ver")+'</th>'+
    '<th onclick="toggleSort(\'status\')">状态 '+sortArrow("status")+'</th>'+
    '<th onclick="toggleSort(\'priority\')">优先级 '+sortArrow("priority")+'</th>'+
    '<th onclick="toggleSort(\'date\')">更新时间 '+sortArrow("date")+'</th>'+
    '<th>操作</th></tr>';
  renderIndexControls();
  applyIndexFilters();
}

// ---- DETAIL MODAL (with clickable file links) ----
function openDetail(id){
  var e=appData.entries.find(function(x){return x.id===id});
  if(!e)return;
  var linkHtml="";
  if(e.link){
    linkHtml='<div class="modal-field"><label>关联文件</label><div class="val" style="display:flex;align-items:center;gap:8px;flex-wrap:wrap"><a href="file:///D:/Obsidian/'+e.link+'" class="modal-link" target="_blank">\ud83d\udcc4 '+e.link.split("/").pop()+'</a><span style="font-size:0.7em;color:var(--text-dim)">('+e.link+')</span><button class="btn-sm info" onclick="copyPath(\''+e.link.replace(/'/g,"\\'")+'\')">\ud83d\udccb 复制路径</button></div></div>';
  }
  document.getElementById("modal-content").innerHTML=
    '<button class="close-btn" onclick="closeModal()">\u2715</button>'+
    '<h3>'+e.title+'</h3>'+
    '<span class="modal-dim dim-badge '+e.dim.toLowerCase()+'">'+e.dim+" \u00b7 "+e.cat+'</span>'+
    '<div class="modal-field"><label>版本</label><div class="val">'+e.ver+'</div></div>'+
    '<div class="modal-field"><label>状态</label><div class="val"><span class="card-tag '+statusTag(e.status)+'">'+e.status+'</span></div></div>'+
    '<div class="modal-field"><label>优先级</label><div class="val"><span class="card-tag '+(e.priority==="高"?"tag-high":e.priority==="中"?"tag-med":"")+'">'+e.priority+'</span></div></div>'+
    '<div class="modal-field"><label>更新时间</label><div class="val">'+e.date+'</div></div>'+
    '<div class="modal-field"><label>描述</label><div class="val">'+e.desc+'</div></div>'+
    linkHtml;
  document.getElementById("modal-overlay").classList.add("show");
}

function copyPath(path){
  navigator.clipboard.writeText(path).then(function(){
    showToast("已复制: "+path);
  }).catch(function(){
    showToast("复制失败，请手动复制");
  });
}

function showToast(msg){
  var t=document.createElement("div");
  t.textContent=msg;
  t.style.cssText="position:fixed;bottom:100px;left:50%;transform:translateX(-50%);background:var(--surface2);color:var(--text);padding:10px 20px;border-radius:20px;font-size:0.85em;z-index:300;border:1px solid var(--border);box-shadow:0 4px 20px rgba(0,0,0,0.4);animation:fadeInOut 2.5s forwards";
  var s=document.createElement("style");
  s.textContent="@keyframes fadeInOut{0%{opacity:0;transform:translateX(-50%) translateY(10px)}15%{opacity:1;transform:translateX(-50%) translateY(0)}80%{opacity:1}100%{opacity:0}}";
  document.head.appendChild(s);
  document.body.appendChild(t);
  setTimeout(function(){t.remove();s.remove()},2600);
}

function openEditForm(id){
  var e=appData.entries.find(function(x){return x.id===id});if(!e)return;
  var cos=CATS.map(function(c){return'<option value="'+c+'"'+(c===e.cat?" selected":"")+'>'+c+'</option>'}).join("");
  var sos=STATUSES.map(function(s){return'<option value="'+s+'"'+(s===e.status?" selected":"")+'>'+s+'</option>'}).join("");
  var pos=["高","中","低"].map(function(p){return'<option value="'+p+'"'+(p===e.priority?" selected":"")+'>'+p+'</option>'}).join("");
  document.getElementById("modal-content").innerHTML=
    '<button class="close-btn" onclick="closeModal()">\u2715</button>'+
    '<h3>\u270f\ufe0f 编辑条目</h3>'+
    '<form onsubmit="saveEdit(event,'+id+')" style="margin-top:16px">'+
    '<div class="modal-field"><label>维度</label><select id="edit-dim" class="form-input"><option value="TCC"'+(e.dim==="TCC"?" selected":"")+'>TCC</option><option value="iNEST"'+(e.dim==="iNEST"?" selected":"")+'>iNEST</option></select></div>'+
    '<div class="modal-field"><label>分类</label><select id="edit-cat" class="form-input">'+cos+'</select></div>'+
    '<div class="modal-field"><label>标题</label><input id="edit-title" class="form-input" value="'+e.title.replace(/"/g,"&quot;")+'" required></div>'+
    '<div class="modal-field"><label>版本</label><input id="edit-ver" class="form-input" value="'+e.ver+'"></div>'+
    '<div class="modal-field"><label>状态</label><select id="edit-status" class="form-input">'+sos+'</select></div>'+
    '<div class="modal-field"><label>优先级</label><select id="edit-priority" class="form-input">'+pos+'</select></div>'+
    '<div class="modal-field"><label>描述</label><textarea id="edit-desc" class="form-input" rows="3">'+e.desc+'</textarea></div>'+
    '<div class="modal-field"><label>关联文件路径</label><input id="edit-link" class="form-input" value="'+(e.link||"")+'"></div>'+
    '<button type="submit" style="width:100%;background:linear-gradient(135deg,var(--tcc),var(--inest));border:none;color:#000;padding:10px;border-radius:8px;font-weight:600;cursor:pointer;font-family:inherit;margin-top:8px">保存修改</button></form>';
  document.getElementById("modal-overlay").classList.add("show");
}

function saveEdit(ev,id){
  ev.preventDefault();
  var e=appData.entries.find(function(x){return x.id===id});if(!e)return;
  e.dim=document.getElementById("edit-dim").value;
  e.cat=document.getElementById("edit-cat").value;
  e.title=document.getElementById("edit-title").value;
  e.ver=document.getElementById("edit-ver").value;
  e.status=document.getElementById("edit-status").value;
  e.priority=document.getElementById("edit-priority").value;
  e.desc=document.getElementById("edit-desc").value;
  e.link=document.getElementById("edit-link").value||null;
  e.date=new Date().toISOString().split("T")[0];
  saveData();
  document.getElementById("modal-overlay").classList.remove("show");
  refreshAll();
  showToast("条目已更新");
}

function openAddForm(){
  var cos=CATS.map(function(c){return'<option value="'+c+'">'+c+'</option>'}).join("");
  var sos=STATUSES.map(function(s){return'<option value="'+s+'">'+s+'</option>'}).join("");
  document.getElementById("modal-content").innerHTML=
    '<button class="close-btn" onclick="closeModal()">\u2715</button>'+
    '<h3>\u2795 添加新条目</h3>'+
    '<form onsubmit="addEntry(event)" style="margin-top:16px">'+
    '<div class="modal-field"><label>维度</label><select id="add-dim" class="form-input"><option value="TCC">TCC \u00b7 拓扑中心计算</option><option value="iNEST">iNEST \u00b7 复杂网络涌现智能</option></select></div>'+
    '<div class="modal-field"><label>分类</label><select id="add-cat" class="form-input">'+cos+'</select></div>'+
    '<div class="modal-field"><label>标题</label><input id="add-title" class="form-input" required></div>'+
    '<div class="modal-field"><label>版本</label><input id="add-ver" class="form-input" value="v0.1"></div>'+
    '<div class="modal-field"><label>状态</label><select id="add-status" class="form-input">'+sos+'</select></div>'+
    '<div class="modal-field"><label>优先级</label><select id="add-priority" class="form-input"><option value="高">高</option><option value="中">中</option><option value="低">低</option></select></div>'+
    '<div class="modal-field"><label>描述</label><textarea id="add-desc" class="form-input" rows="3"></textarea></div>'+
    '<div class="modal-field"><label>关联文件路径 (可选)</label><input id="add-link" class="form-input" placeholder="如 phase1_workspace/sdi_v30_multiregion.py"></div>'+
    '<button type="submit" style="width:100%;background:linear-gradient(135deg,var(--tcc),var(--inest));border:none;color:#000;padding:10px;border-radius:8px;font-weight:600;cursor:pointer;font-family:inherit;margin-top:8px">添加条目</button></form>';
  document.getElementById("modal-overlay").classList.add("show");
}

function addEntry(ev){
  ev.preventDefault();
  var ids=appData.entries.map(function(e){return e.id});
  var entry={
    id:(ids.length?Math.max.apply(null,ids):0)+1,
    dim:document.getElementById("add-dim").value,
    cat:document.getElementById("add-cat").value,
    title:document.getElementById("add-title").value,
    ver:document.getElementById("add-ver").value,
    status:document.getElementById("add-status").value,
    priority:document.getElementById("add-priority").value,
    desc:document.getElementById("add-desc").value,
    date:new Date().toISOString().split("T")[0],
    link:document.getElementById("add-link").value||null
  };
  appData.entries.push(entry);saveData();
  document.getElementById("modal-overlay").classList.remove("show");
  refreshAll();
  showToast("新条目已添加");
}

function deleteEntry(id){
  if(!confirm("确定要删除此条目吗？此操作不可撤销。"))return;
  appData.entries=appData.entries.filter(function(e){return e.id!==id});
  saveData();refreshAll();
  showToast("条目已删除");
}

function closeModal(ev){
  if(ev&&ev.target!==document.getElementById("modal-overlay"))return;
  document.getElementById("modal-overlay").classList.remove("show");
}

function switchView(view){
  document.querySelectorAll(".header-nav button").forEach(function(b){b.classList.remove("active")});
  var btn=document.querySelector('[data-view="'+view+'"]');
  if(btn)btn.classList.add("active");
  document.querySelectorAll(".view-panel").forEach(function(p){p.classList.remove("active")});
  var panel=document.getElementById("view-"+view);
  if(panel){panel.classList.add("active");gsap.from(panel,{opacity:0,duration:0.3,ease:"power2.out"})}
  if(view==="index")renderIndex();
}

function refreshAll(){
  renderMetrics();renderDaily();renderKanban();
  var av=document.querySelector(".view-panel.active");
  if(av&&av.id==="view-index")renderIndex();
}

function animateIn(){
  gsap.from(".metric",{opacity:0,y:20,duration:0.5,stagger:0.06,ease:"power2.out"});
  gsap.from(".paradigm-banner",{opacity:0,y:10,duration:0.5,ease:"power2.out",delay:0.15});
  gsap.from(".daily-card",{opacity:0,y:16,duration:0.4,stagger:0.08,ease:"power2.out",delay:0.2});
  gsap.from(".kanban-col",{opacity:0,y:12,duration:0.35,stagger:0.04,ease:"power2.out",delay:0.4});
}

document.addEventListener("DOMContentLoaded",function(){
  document.getElementById("header-date").textContent=new Date().toLocaleDateString("zh-CN",{year:"numeric",month:"long",day:"numeric",weekday:"long"});
  document.querySelectorAll(".header-nav button").forEach(function(b){
    b.addEventListener("click",function(){switchView(b.dataset.view)});
  });
  document.addEventListener("keydown",function(e){if(e.key==="Escape")closeModal()});
  refreshAll();animateIn();
});
"""

print(f"JS ready: {len(JS)} chars")
