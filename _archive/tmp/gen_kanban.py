# gen_kanban.py - generates the full R&D kanban HTML
import json

OUT = r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html"

CSS = """/* Auto-generated compact CSS */
:root{--bg:#080c14;--surface:#111827;--surface2:#1a2236;--border:#1e2d4a;--text:#e2e8f0;--text-dim:#7c8aa0
--tcc:#38bdf8;--tcc-glow:rgba(56,189,248,0.3);--tcc-bg:rgba(56,189,248,0.06);--inest:#4ade80
--inest-glow:rgba(74,222,128,0.3);--inest-bg:rgba(74,222,128,0.06);--warn:#fbbf24;--danger:#f87171
--purple:#a78bfa;--pink:#f472b6;--radius:10px;--transition:0.25s cubic-bezier(0.4,0,0.2,1)}
*{margin:0;padding:0;box-sizing:border-box}html{scroll-behavior:smooth}
body{font-family:Inter,-apple-system,BlinkMacSystemFont,Segoe UI,Noto Sans SC,sans-serif
background:var(--bg);color:var(--text);line-height:1.6;min-height:100vh}
body::before{content:"";position:fixed;inset:0
background:radial-gradient(ellipse 80% 60% at 30% 20%,rgba(56,189,248,0.04),transparent),radial-gradient(ellipse 70% 50% at 70% 80%,rgba(74,222,128,0.04),transparent)
pointer-events:none;z-index:0}
.header{position:sticky;top:0;z-index:100;background:rgba(17,24,39,0.85);backdrop-filter:blur(20px)
border-bottom:1px solid var(--border);padding:14px 32px;display:flex;align-items:center
justify-content:space-between;gap:16px}
.header-left{display:flex;align-items:center;gap:14px}
.header-logo{width:38px;height:38px;border-radius:10px
background:linear-gradient(135deg,var(--tcc),var(--inest));display:flex;align-items:center
justify-content:center;font-weight:800;font-size:16px;color:#000}
.header h1{font-size:1.2em;font-weight:600;letter-spacing:-0.3px}
.header h1 .tcc{color:var(--tcc)}.header h1 .inest{color:var(--inest)}
.header-nav{display:flex;gap:6px}
.header-nav button{background:transparent;border:1px solid var(--border);color:var(--text-dim)
padding:7px 16px;border-radius:20px;font-size:0.82em;cursor:pointer;transition:var(--transition)
font-family:inherit}
.header-nav button:hover{border-color:var(--tcc);color:var(--text)}
.header-nav button.active{background:var(--tcc);border-color:var(--tcc);color:#000;font-weight:600}
.header-date{font-size:0.85em;color:var(--text-dim)}
.main{max-width:1600px;margin:0 auto;padding:24px 28px;position:relative;z-index:1}
.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:20px}
.metric{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius)
padding:16px 18px;text-align:center;transition:var(--transition)}
.metric:hover{transform:translateY(-2px);box-shadow:0 8px 25px rgba(0,0,0,0.3)}
.metric .num{font-size:2em;font-weight:700;line-height:1;margin:4px 0}
.metric .lbl{font-size:0.75em;color:var(--text-dim);text-transform:uppercase;letter-spacing:0.5px}
.metric.tcc{border-color:rgba(56,189,248,0.3)}.metric.tcc .num{color:var(--tcc)}
.metric.inest{border-color:rgba(74,222,128,0.3)}.metric.inest .num{color:var(--inest)}
.metric.warn .num{color:var(--warn)}.metric.purple .num{color:var(--purple)}
.section-title{font-size:1em;font-weight:600;margin:28px 0 14px;display:flex;align-items:center;gap:8px
letter-spacing:-0.2px}
.section-title .badge{font-size:0.7em;font-weight:500;padding:2px 10px;border-radius:12px
background:var(--surface2);color:var(--text-dim)}
.daily-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:14px;margin-bottom:8px}
.daily-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius)
padding:18px;transition:var(--transition);cursor:default}
.daily-card:hover{border-color:rgba(255,255,255,0.15)}
.daily-card-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:12px}
.daily-card-header .date{font-weight:600;font-size:0.95em}
.date-badge{font-size:0.7em;padding:3px 10px;border-radius:12px;font-weight:500}
.date-badge.today{background:rgba(56,189,248,0.2);color:var(--tcc)}
.date-badge.yesterday{background:rgba(124,138,160,0.15);color:var(--text-dim)}
.daily-item{padding:7px 0;border-bottom:1px solid rgba(255,255,255,0.04);font-size:0.84em
display:flex;align-items:flex-start;gap:8px}
.daily-item:last-child{border-bottom:none}
.daily-item .dot{width:6px;height:6px;border-radius:50%;margin-top:6px;flex-shrink:0}
.dot.done{background:var(--inest)}.dot.ongoing{background:var(--tcc)}.dot.plan{background:var(--text-dim)}
.daily-section-label{font-size:0.7em;font-weight:600;text-transform:uppercase;letter-spacing:1px
color:var(--text-dim);margin:10px 0 4px}
.view-panel{display:none}.view-panel.active{display:block}
.kanban-dual{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.kanban-column-group h3{font-size:0.9em;font-weight:700;margin-bottom:12px;padding:8px 14px;border-radius:8px}
.kanban-column-group.tcc h3{background:var(--tcc-bg);color:var(--tcc)
border:1px solid rgba(56,189,248,0.2)}
.kanban-column-group.inest h3{background:var(--inest-bg);color:var(--inest)
border:1px solid rgba(74,222,128,0.2)}
.kanban-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.kanban-col{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius)
padding:12px;min-height:180px}
.kanban-col-header{font-size:0.75em;font-weight:600;color:var(--text-dim);text-transform:uppercase
letter-spacing:0.5px;margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid var(--border)
display:flex;align-items:center;gap:6px}
.kanban-col-header .count{font-size:0.85em;color:var(--text-dim);margin-left:auto}
.kanban-card{background:var(--surface2);border:1px solid var(--border);border-radius:8px
padding:10px 12px;margin-bottom:8px;font-size:0.8em;transition:var(--transition);cursor:pointer}
.kanban-card:hover{border-color:rgba(255,255,255,0.2);transform:translateY(-1px)
box-shadow:0 4px 15px rgba(0,0,0,0.3)}
.kanban-card .card-title{font-weight:500;margin-bottom:4px}
.kanban-card .card-meta{font-size:0.85em;color:var(--text-dim);display:flex;gap:8px;align-items:center
flex-wrap:wrap}
.card-tag{font-size:0.7em;padding:2px 8px;border-radius:4px;font-weight:500}
.tag-done{background:rgba(74,222,128,0.15);color:var(--inest)}
.tag-ongoing{background:rgba(56,189,248,0.15);color:var(--tcc)}
.tag-plan{background:rgba(124,138,160,0.12);color:var(--text-dim)}
.tag-high{background:rgba(248,113,113,0.12);color:var(--danger)}
.tag-med{background:rgba(251,191,36,0.12);color:var(--warn)}
.index-controls{display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap;align-items:center}
.search-box{flex:1;min-width:220px;position:relative}
.search-box input{width:100%;background:var(--surface);border:1px solid var(--border);color:var(--text)
padding:10px 14px 10px 38px;border-radius:24px;font-size:0.88em;font-family:inherit;outline:none
transition:var(--transition)}
.search-box input:focus{border-color:var(--tcc);box-shadow:0 0 0 3px var(--tcc-glow)}
.search-box .search-icon{position:absolute;left:14px;top:50%;transform:translateY(-50%);color:var(--text-dim)}
.filter-group{display:flex;gap:6px;flex-wrap:wrap}
.filter-chip{padding:6px 14px;border-radius:20px;font-size:0.78em;border:1px solid var(--border)
background:var(--surface);color:var(--text-dim);cursor:pointer;transition:var(--transition)
font-family:inherit;white-space:nowrap}
.filter-chip:hover{border-color:rgba(255,255,255,0.3);color:var(--text)}
.filter-chip.active{background:var(--tcc);border-color:var(--tcc);color:#000;font-weight:600}
.filter-chip.active.inest-chip{background:var(--inest);border-color:var(--inest);color:#000}
.table-wrap{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius)
overflow:hidden;overflow-x:auto}
.index-table{width:100%;border-collapse:collapse;font-size:0.84em}
.index-table th{text-align:left;padding:12px 16px;font-size:0.72em;font-weight:600;text-transform:uppercase
letter-spacing:0.8px;color:var(--text-dim);background:var(--surface2);border-bottom:1px solid var(--border)
cursor:pointer;user-select:none;white-space:nowrap}
.index-table th:hover{color:var(--text)}
.index-table th .sort-arrow{margin-left:4px;font-size:0.7em}
.index-table td{padding:11px 16px;border-bottom:1px solid rgba(255,255,255,0.03)}
.index-table tbody tr:hover{background:rgba(255,255,255,0.02)}
.dim-badge{display:inline-block;padding:3px 10px;border-radius:4px;font-size:0.78em;font-weight:600}
.dim-badge.tcc{background:var(--tcc-bg);color:var(--tcc)}
.dim-badge.inest{background:var(--inest-bg);color:var(--inest)}
.ver-link{color:var(--tcc);text-decoration:none;cursor:pointer;font-weight:500}
.ver-link:hover{text-decoration:underline}
.no-results{text-align:center;padding:40px;color:var(--text-dim);font-size:0.9em}
.result-count{font-size:0.78em;color:var(--text-dim);margin-left:auto}
.btn-sm{background:none;border:1px solid var(--border);padding:4px 10px;border-radius:6px
cursor:pointer;font-size:0.8em;font-family:inherit;transition:var(--transition)}
.btn-sm:hover{border-color:rgba(255,255,255,0.3)}
.btn-sm.info{color:var(--tcc);border-color:rgba(56,189,248,0.3)}
.btn-sm.danger{color:var(--danger);border-color:rgba(248,113,113,0.3)}
.btn-sm.danger:hover{background:rgba(248,113,113,0.1)}
.modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,0.7);backdrop-filter:blur(4px);z-index:200
display:flex;align-items:center;justify-content:center;opacity:0;pointer-events:none;transition:opacity 0.3s}
.modal-overlay.show{opacity:1;pointer-events:auto}
.modal{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:28px
max-width:560px;width:90%;max-height:80vh;overflow-y:auto;box-shadow:0 20px 60px rgba(0,0,0,0.5)
position:relative}
.modal h3{font-size:1.1em;margin-bottom:8px}
.modal .close-btn{position:absolute;top:12px;right:16px;background:none;border:none;color:var(--text-dim)
font-size:1.3em;cursor:pointer}
.modal .close-btn:hover{color:var(--text)}
.modal-field{margin-bottom:12px}
.modal-field label{display:block;font-size:0.72em;color:var(--text-dim);text-transform:uppercase
letter-spacing:0.5px;margin-bottom:4px}
.modal-field .val{font-size:0.9em}
.form-input{width:100%;background:var(--surface2);border:1px solid var(--border);color:var(--text)
padding:8px;border-radius:6px;font-family:inherit;font-size:0.9em}
.form-input:focus{outline:none;border-color:var(--tcc)}
.add-entry-btn{position:fixed;bottom:28px;right:28px;z-index:150;width:52px;height:52px;border-radius:50%
background:linear-gradient(135deg,var(--tcc),var(--inest));border:none;color:#000;font-size:1.6em
cursor:pointer;box-shadow:0 6px 24px rgba(56,189,248,0.3);transition:var(--transition)
display:flex;align-items:center;justify-content:center}
.add-entry-btn:hover{transform:scale(1.08);box-shadow:0 8px 30px rgba(56,189,248,0.4)}
@media(max-width:1200px){.kanban-dual{grid-template-columns:1fr}}
@media(max-width:768px){.kanban-grid{grid-template-columns:1fr 1fr}.daily-grid{grid-template-columns:1fr}
.header{padding:10px 16px}.main{padding:14px}}
"""
print("CSS OK:", len(CSS))
