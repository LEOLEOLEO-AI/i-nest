
"""Build R&D Kanban HTML - complete generator."""
import json, os

DATA_JSON = r"""
{
  "daily": [
    {"date":"2026-06-04","type":"today","progress":[
      {"text":"SDI v29 功能性涌现模块集成测试完成，PASS率 94.2%","dot":"done","dim":"iNEST"},
      {"text":"TCC CST 论文初稿完成 Methods 章节","dot":"done","dim":"TCC"},
      {"text":"FEP-STDP 融合架构收敛性数学证明推导","dot":"ongoing","dim":"iNEST"},
      {"text":"FPGA 开发板基础测试框架搭建","dot":"ongoing","dim":"iNEST"}
    ],"plan":[
      {"text":"完成 FEP-STDP 收敛性证明并写入专利文档","dot":"plan","dim":"iNEST"},
      {"text":"TCC 远程证明协议仿真环境搭建","dot":"plan","dim":"TCC"},
      {"text":"类脑计算综述论文 Introduction 章节撰写","dot":"plan","dim":"iNEST"}
    ]},
    {"date":"2026-06-03","type":"yesterday","progress":[
      {"text":"SDI v28->v29 功能涌现模块架构设计","dot":"done","dim":"iNEST"},
      {"text":"TCC 可信执行环境基准测试方案确定","dot":"done","dim":"TCC"},
      {"text":"iNEST 核心架构论文 Fig.3-5 图表绘制","dot":"done","dim":"iNEST"},
      {"text":"集体通信 NaaS 协议 v2 性能对比实验","dot":"done","dim":"iNEST"}
    ],"plan":[
      {"text":"SDI v29 全量回归测试","dot":"done","dim":"iNEST"},
      {"text":"TCC CST 论文 Methods 章节","dot":"done","dim":"TCC"}
    ]},
    {"date":"2026-06-02","type":"past","progress":[
      {"text":"SDI v27->v28 多尺度融合框架实现","dot":"done","dim":"iNEST"},
      {"text":"专利组合文档更新（3 项新增）","dot":"done","dim":"TCC"},
      {"text":"投资者演示 Demo v3 UI 重构","dot":"done","dim":"iNEST"}
    ],"plan":[]}
  ],
  "entries": [
    {"id":1,"dim":"TCC","cat":"灵感","title":"TCC-TEE 在 iNEST 边缘节点的应用","ver":"v1.0","status":"进行中","date":"2026-06-03","desc":"将可信执行环境引入边缘计算节点，实现安全数据处理与隐私保护","priority":"高"},
    {"id":2,"dim":"TCC","cat":"灵感","title":"基于区块链的分布式信任量化模型","ver":"v0.5","status":"规划中","date":"2026-05-28","desc":"利用区块链不可篡改特性构建跨节点信任传递机制","priority":"中"},
    {"id":3,"dim":"TCC","cat":"论文","title":"Trusted Execution Environments for Cloud-Native Edge Computing","ver":"draft-v2","status":"撰写中","date":"2026-06-04","desc":"TEE在云原生边缘计算中的应用框架与安全性分析","priority":"高","link":"phase1_workspace/papers/paper1_iNEST_core_architecture.md"},
    {"id":4,"dim":"TCC","cat":"论文","title":"Remote Attestation Protocols in Heterogeneous Edge Networks","ver":"outline","status":"规划中","date":"2026-05-30","desc":"异构边缘网络中的远程证明协议设计与验证","priority":"中"},
    {"id":5,"dim":"TCC","cat":"专利","title":"一种基于可信执行环境的边缘计算数据保护方法","ver":"申请稿-v3","status":"撰写中","date":"2026-06-01","desc":"TEE+边缘计算数据保护方案","priority":"高","link":"phase1_workspace/patents/patent_portfolio_detailed.md"},
    {"id":6,"dim":"TCC","cat":"专利","title":"分布式节点信任评估系统与方法","ver":"构思-v1","status":"规划中","date":"2026-05-25","desc":"基于多维特征的节点信任度量化评估","priority":"中"},
    {"id":7,"dim":"TCC","cat":"仿真程序","title":"TCC CST 远程证明仿真","ver":"v0.3","status":"开发中","date":"2026-06-03","desc":"CST理论仿真验证，含远程证明协议模拟","priority":"高","link":"GetNotes_Inbox/_processed/sample_TCC_SDI_test.md"},
    {"id":8,"dim":"TCC","cat":"仿真程序","title":"TEE 安全边界性能 Benchmark","ver":"v0.1","status":"规划中","date":"2026-05-20","desc":"TEE环境下密码学操作性能基准测试","priority":"中"},
    {"id":9,"dim":"TCC","cat":"产品代码开发","title":"TCC 信任管理 SDK (Rust)","ver":"v0.2-alpha","status":"开发中","date":"2026-05-15","desc":"跨平台信任管理核心SDK，支持远程证明API","priority":"高"},
    {"id":10,"dim":"TCC","cat":"产品代码开发","title":"TCC Dashboard 监控面板","ver":"v0.1","status":"规划中","date":"2026-06-01","desc":"TCC节点信任状态实时监控Web面板","priority":"中"},
    {"id":11,"dim":"TCC","cat":"项目指南策划","title":"TCC 技术白皮书 v2","ver":"大纲-v1","status":"规划中","date":"2026-06-02","desc":"TCC技术体系全面阐述，面向学术与产业双重受众","priority":"高"},
    {"id":12,"dim":"TCC","cat":"项目指南策划","title":"TCC 开发者 onboarding 指南","ver":"v0.1","status":"规划中","date":"2026-05-10","desc":"新成员快速上手TCC项目的开发环境与规范指南","priority":"低"}
  ]
}
"""

# iNEST entries kept in a separate file for brevity - loaded inline
INEST_ENTRIES = [
    {"id":13,"dim":"iNEST","cat":"灵感","title":"FEP驱动自组织网络与功能涌现的临界条件","ver":"v2.1","status":"验证中","date":"2026-06-04","desc":"探索FEP自由能最小化与网络临界相变的数学联系","priority":"高"},
    {"id":14,"dim":"iNEST","cat":"灵感","title":"基于复杂网络拓扑优化的智能路由算法","ver":"v1.0","status":"进行中","date":"2026-05-30","desc":"结合小世界与无标度特性设计新型网络路由","priority":"高"},
    {"id":15,"dim":"iNEST","cat":"灵感","title":"类脑计算中忆阻器与 SDI 框架的硬件映射","ver":"v0.8","status":"探索中","date":"2026-05-22","desc":"将SDI网络拓扑映射到忆阻器交叉阵列的可行性研究","priority":"中"},
    {"id":16,"dim":"iNEST","cat":"论文","title":"iNEST: Intelligent Network Emergence via Self-organizing Topology","ver":"draft-v4","status":"撰写中","date":"2026-06-04","desc":"iNEST核心架构论文，含FEP-STDP融合框架","priority":"高","link":"phase1_workspace/papers/paper1_iNEST_core_architecture.md"},
    {"id":17,"dim":"iNEST","cat":"论文","title":"Liquid Computing Chemistry: FEP-driven Self-organization in Artificial Neural Substrates","ver":"draft-v2","status":"撰写中","date":"2026-06-02","desc":"液态计算化学：FEP驱动的人工神经基质自组织","priority":"高","link":"phase1_workspace/papers/paper2_liquid_computing_chemistry.md"},
    {"id":18,"dim":"iNEST","cat":"论文","title":"类脑计算最新综述与iNEST定位","ver":"outline","status":"资料整理","date":"2026-05-22","desc":"基于Nature Electronics综述，梳理iNEST在类脑计算中的定位","priority":"中","link":"GetNotes_Inbox/_processed/类脑计算最新综述.md"},
    {"id":19,"dim":"iNEST","cat":"论文","title":"芯片算力网络趋势与iNEST架构对比分析","ver":"notes","status":"资料整理","date":"2026-05-28","desc":"基于NVIDIA CXL 3.0趋势，分析iNEST在算力网络中的优势","priority":"中","link":"GetNotes_Inbox/_processed/芯片算力网络趋势.md"},
    {"id":20,"dim":"iNEST","cat":"专利","title":"专利组合详细方案（6项核心专利）","ver":"v2.1","status":"撰写中","date":"2026-06-03","desc":"含FEP-STDP融合、功能涌现检测、多尺度拓扑优化等6项","priority":"高","link":"phase1_workspace/patents/patent_portfolio_detailed.md"},
    {"id":21,"dim":"iNEST","cat":"专利","title":"一种基于自由能原理的自组织网络拓扑优化方法","ver":"申请稿-v1","status":"撰写中","date":"2026-05-20","desc":"FEP驱动的网络拓扑自适应优化方法","priority":"高"},
    {"id":22,"dim":"iNEST","cat":"专利","title":"神经网络功能涌现检测与量化方法","ver":"构思-v1","status":"规划中","date":"2026-06-01","desc":"基于信息论指标的功能涌现自动检测方法","priority":"中"},
    {"id":23,"dim":"iNEST","cat":"仿真程序","title":"SDI v29 功能性涌现仿真","ver":"v29","status":"测试中","date":"2026-06-04","desc":"最新版SDI仿真框架，含功能涌现模块，PASS率94.2%","priority":"高","link":"phase1_workspace/sdi_v29_functional.py"},
    {"id":24,"dim":"iNEST","cat":"仿真程序","title":"SDI v28 多尺度融合仿真","ver":"v28","status":"已完成","date":"2026-06-02","desc":"多尺度网络融合框架，含跨尺度耦合分析","priority":"高","link":"phase1_workspace/sdi_v28_multiscale.py"},
    {"id":25,"dim":"iNEST","cat":"仿真程序","title":"SDI v27 多尺度仿真","ver":"v27","status":"已完成","date":"2026-05-28","desc":"多尺度网络仿真，支持微观-介观-宏观三层","priority":"中","link":"phase1_workspace/sdi_v27_multiscale.py"},
    {"id":26,"dim":"iNEST","cat":"仿真程序","title":"SDI v26 多尺度仿真","ver":"v26","status":"已完成","date":"2026-05-20","desc":"初版多尺度仿真框架","priority":"中","link":"phase1_workspace/sdi_v26_multiscale.py"},
    {"id":27,"dim":"iNEST","cat":"仿真程序","title":"SDI v25 物理-生物融合","ver":"v25","status":"已完成","date":"2026-05-15","desc":"物理约束与生物启发的融合仿真","priority":"中","link":"phase1_workspace/sdi_v25_physical_biological.py"},
    {"id":28,"dim":"iNEST","cat":"仿真程序","title":"SDI v24 FEP-STDP融合仿真","ver":"v24","status":"已完成","date":"2026-05-10","desc":"FEP与STDP机制融合的第一版仿真","priority":"高","link":"phase1_workspace/sdi_v24_fep_stdp_fusion.py"},
    {"id":29,"dim":"iNEST","cat":"仿真程序","title":"TCC CST SDI 验证仿真","ver":"v28-多尺度","status":"已完成","date":"2026-05-25","desc":"TCC CST理论仿真验证，sigma最高99.45","priority":"高","link":"GetNotes_Inbox/_processed/sample_TCC_SDI_test.md"},
    {"id":30,"dim":"iNEST","cat":"仿真程序","title":"FEP进化仿真 v11","ver":"v11","status":"已完成","date":"2026-05-01","desc":"改进版FEP进化仿真","priority":"中","link":"phase1_workspace/sdi_v11_fep_improved.py"},
    {"id":31,"dim":"iNEST","cat":"产品代码开发","title":"iNEST 核心网络引擎 (Python)","ver":"v0.6-dev","status":"开发中","date":"2026-06-04","desc":"SDI核心算法工程化实现，支持大规模网络部署","priority":"高"},
    {"id":32,"dim":"iNEST","cat":"产品代码开发","title":"FPGA 加速模块","ver":"v0.1-prototype","status":"开发中","date":"2026-06-03","desc":"SDI关键路径FPGA硬件加速原型","priority":"高","link":"phase1_workspace/iNEST_4_工程开发/fpga"},
    {"id":33,"dim":"iNEST","cat":"产品代码开发","title":"投资者演示 Demo v3","ver":"v3.0","status":"已完成","date":"2026-06-02","desc":"面向投资者的交互式产品演示","priority":"高","link":"phase1_workspace/investor_demo/index.html"},
    {"id":34,"dim":"iNEST","cat":"产品代码开发","title":"集体通信 NaaS 协议库","ver":"v2-prototype","status":"开发中","date":"2026-06-01","desc":"面向分布式AI训练的集体通信网络即服务","priority":"高","link":"phase1_workspace/collective_comm_naas"},
    {"id":35,"dim":"iNEST","cat":"项目指南策划","title":"iNEST 技术白皮书","ver":"v1.2","status":"持续更新","date":"2026-06-04","desc":"iNEST整体技术体系白皮书，含架构、算法、应用场景","priority":"高"},
    {"id":36,"dim":"iNEST","cat":"项目指南策划","title":"iNEST CS团队指南","ver":"v1.0","status":"已发布","date":"2026-06-03","desc":"团队协作规范、开发流程与知识管理体系","priority":"高","link":"iNEST_CS团队指南.pdf"},
    {"id":37,"dim":"iNEST","cat":"项目指南策划","title":"iNEST对外合作介绍材料","ver":"v2.0","status":"已发布","date":"2026-06-02","desc":"面向合作伙伴的项目介绍与技术能力展示","priority":"高","link":"iNEST对外合作介绍材料.html"},
    {"id":38,"dim":"iNEST","cat":"项目指南策划","title":"研发路线图与里程碑规划","ver":"v1.5","status":"持续更新","date":"2026-06-01","desc":"Q3-Q4研发里程碑、资源分配与风险预案","priority":"高"}
]

default_data = json.loads(DATA_JSON)
default_data["entries"].extend(INEST_ENTRIES)
print(f"Loaded {len(default_data['entries'])} entries")

# ─── CSS ───
CSS = """/* TCC x iNEST R&D Kanban - Compact CSS */
:root{--bg:#080c14;--surface:#111827;--surface2:#1a2236;--border:#1e2d4a;--text:#e2e8f0;--text-dim:#7c8aa0;--tcc:#38bdf8;--tcc-glow:rgba(56,189,248,0.3);--tcc-bg:rgba(56,189,248,0.06);--inest:#4ade80;--inest-glow:rgba(74,222,128,0.3);--inest-bg:rgba(74,222,128,0.06);--warn:#fbbf24;--danger:#f87171;--purple:#a78bfa;--pink:#f472b6;--radius:10px;--transition:0.25s cubic-bezier(0.4,0,0.2,1)}
*{margin:0;padding:0;box-sizing:border-box}html{scroll-behavior:smooth}
body{font-family:Inter,-apple-system,BlinkMacSystemFont,Segoe UI,Noto Sans SC,sans-serif;background:var(--bg);color:var(--text);line-height:1.6;min-height:100vh}
body::before{content:"";position:fixed;inset:0;background:radial-gradient(ellipse 80% 60% at 30% 20%,rgba(56,189,248,0.04),transparent),radial-gradient(ellipse 70% 50% at 70% 80%,rgba(74,222,128,0.04),transparent);pointer-events:none;z-index:0}
.header{position:sticky;top:0;z-index:100;background:rgba(17,24,39,0.85);backdrop-filter:blur(20px);border-bottom:1px solid var(--border);padding:14px 32px;display:flex;align-items:center;justify-content:space-between;gap:16px}
.header-left{display:flex;align-items:center;gap:14px}
.header-logo{width:38px;height:38px;border-radius:10px;background:linear-gradient(135deg,var(--tcc),var(--inest));display:flex;align-items:center;justify-content:center;font-weight:800;font-size:16px;color:#000}
.header h1{font-size:1.2em;font-weight:600;letter-spacing:-0.3px}
.header h1 .tcc{color:var(--tcc)}.header h1 .inest{color:var(--inest)}
.header-nav{display:flex;gap:6px}
.header-nav button{background:transparent;border:1px solid var(--border);color:var(--text-dim);padding:7px 16px;border-radius:20px;font-size:0.82em;cursor:pointer;transition:var(--transition);font-family:inherit}
.header-nav button:hover{border-color:var(--tcc);color:var(--text)}
.header-nav button.active{background:var(--tcc);border-color:var(--tcc);color:#000;font-weight:600}
.header-date{font-size:0.85em;color:var(--text-dim)}
.main{max-width:1600px;margin:0 auto;padding:24px 28px;position:relative;z-index:1}
.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:20px}
.metric{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:16px 18px;text-align:center;transition:var(--transition)}
.metric:hover{transform:translateY(-2px);box-shadow:0 8px 25px rgba(0,0,0,0.3)}
.metric .num{font-size:2em;font-weight:700;line-height:1;margin:4px 0}
.metric .lbl{font-size:0.75em;color:var(--text-dim);text-transform:uppercase;letter-spacing:0.5px}
.metric.tcc{border-color:rgba(56,189,248,0.3)}.metric.tcc .num{color:var(--tcc)}
.metric.inest{border-color:rgba(74,222,128,0.3)}.metric.inest .num{color:var(--inest)}
.metric.warn .num{color:var(--warn)}.metric.purple .num{color:var(--purple)}
.section-title{font-size:1em;font-weight:600;margin:28px 0 14px;display:flex;align-items:center;gap:8px;letter-spacing:-0.2px}
.section-title .badge{font-size:0.7em;font-weight:500;padding:2px 10px;border-radius:12px;background:var(--surface2);color:var(--text-dim)}
.daily-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:14px;margin-bottom:8px}
.daily-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:18px;transition:var(--transition);cursor:default}
.daily-card:hover{border-color:rgba(255,255,255,0.15)}
.daily-card-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:12px}
.daily-card-header .date{font-weight:600;font-size:0.95em}
.date-badge{font-size:0.7em;padding:3px 10px;border-radius:12px;font-weight:500}
.date-badge.today{background:rgba(56,189,248,0.2);color:var(--tcc)}
.date-badge.yesterday{background:rgba(124,138,160,0.15);color:var(--text-dim)}
.daily-item{padding:7px 0;border-bottom:1px solid rgba(255,255,255,0.04);font-size:0.84em;display:flex;align-items:flex-start;gap:8px}
.daily-item:last-child{border-bottom:none}
.daily-item .dot{width:6px;height:6px;border-radius:50%;margin-top:6px;flex-shrink:0}
.dot.done{background:var(--inest)}.dot.ongoing{background:var(--tcc)}.dot.plan{background:var(--text-dim)}
.daily-section-label{font-size:0.7em;font-weight:600;text-transform:uppercase;letter-spacing:1px;color:var(--text-dim);margin:10px 0 4px}
.view-panel{display:none}.view-panel.active{display:block}
.kanban-dual{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.kanban-column-group h3{font-size:0.9em;font-weight:700;margin-bottom:12px;padding:8px 14px;border-radius:8px;letter-spacing:-0.2px}
.kanban-column-group.tcc h3{background:var(--tcc-bg);color:var(--tcc);border:1px solid rgba(56,189,248,0.2)}
.kanban-column-group.inest h3{background:var(--inest-bg);color:var(--inest);border:1px solid rgba(74,222,128,0.2)}
.kanban-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.kanban-col{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:12px;min-height:180px}
.kanban-col-header{font-size:0.75em;font-weight:600;color:var(--text-dim);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:10px;padding-bottom:8px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:6px}
.kanban-col-header .count{font-size:0.85em;color:var(--text-dim);margin-left:auto}
.kanban-card{background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:10px 12px;margin-bottom:8px;font-size:0.8em;transition:var(--transition);cursor:pointer}
.kanban-card:hover{border-color:rgba(255,255,255,0.2);transform:translateY(-1px);box-shadow:0 4px 15px rgba(0,0,0,0.3)}
.kanban-card .card-title{font-weight:500;margin-bottom:4px}
.kanban-card .card-meta{font-size:0.85em;color:var(--text-dim);display:flex;gap:8px;align-items:center;flex-wrap:wrap}
.card-tag{font-size:0.7em;padding:2px 8px;border-radius:4px;font-weight:500}
.tag-done{background:rgba(74,222,128,0.15);color:var(--inest)}
.tag-ongoing{background:rgba(56,189,248,0.15);color:var(--tcc)}
.tag-plan{background:rgba(124,138,160,0.12);color:var(--text-dim)}
.tag-high{background:rgba(248,113,113,0.12);color:var(--danger)}
.tag-med{background:rgba(251,191,36,0.12);color:var(--warn)}
.index-controls{display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap;align-items:center}
.search-box{flex:1;min-width:220px;position:relative}
.search-box input{width:100%;background:var(--surface);border:1px solid var(--border);color:var(--text);padding:10px 14px 10px 38px;border-radius:24px;font-size:0.88em;font-family:inherit;outline:none;transition:var(--transition)}
.search-box input:focus{border-color:var(--tcc);box-shadow:0 0 0 3px var(--tcc-glow)}
.search-box .search-icon{position:absolute;left:14px;top:50%;transform:translateY(-50%);color:var(--text-dim)}
.filter-group{display:flex;gap:6px;flex-wrap:wrap}
.filter-chip{padding:6px 14px;border-radius:20px;font-size:0.78em;border:1px solid var(--border);background:var(--surface);color:var(--text-dim);cursor:pointer;transition:var(--transition);font-family:inherit;white-space:nowrap}
.filter-chip:hover{border-color:rgba(255,255,255,0.3);color:var(--text)}
.filter-chip.active{background:var(--tcc);border-color:var(--tcc);color:#000;font-weight:600}
.filter-chip.active.inest-chip{background:var(--inest);border-color:var(--inest);color:#000}
.table-wrap{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;overflow-x:auto}
.index-table{width:100%;border-collapse:collapse;font-size:0.84em}
.index-table th{text-align:left;padding:12px 16px;font-size:0.72em;font-weight:600;text-transform:uppercase;letter-spacing:0.8px;color:var(--text-dim);background:var(--surface2);border-bottom:1px solid var(--border);cursor:pointer;user-select:none;white-space:nowrap}
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
.btn-sm{background:none;border:1px solid var(--border);padding:4px 10px;border-radius:6px;cursor:pointer;font-size:0.8em;font-family:inherit;transition:var(--transition)}
.btn-sm:hover{border-color:rgba(255,255,255,0.3)}
.btn-sm.info{color:var(--tcc);border-color:rgba(56,189,248,0.3)}
.btn-sm.danger{color:var(--danger);border-color:rgba(248,113,113,0.3)}
.btn-sm.danger:hover{background:rgba(248,113,113,0.1)}
.modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,0.7);backdrop-filter:blur(4px);z-index:200;display:flex;align-items:center;justify-content:center;opacity:0;pointer-events:none;transition:opacity 0.3s}
.modal-overlay.show{opacity:1;pointer-events:auto}
.modal{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:28px;max-width:560px;width:90%;max-height:80vh;overflow-y:auto;box-shadow:0 20px 60px rgba(0,0,0,0.5);position:relative}
.modal h3{font-size:1.1em;margin-bottom:8px}
.modal .close-btn{position:absolute;top:12px;right:16px;background:none;border:none;color:var(--text-dim);font-size:1.3em;cursor:pointer}
.modal .close-btn:hover{color:var(--text)}
.modal-field{margin-bottom:12px}
.modal-field label{display:block;font-size:0.72em;color:var(--text-dim);text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px}
.modal-field .val{font-size:0.9em}
.form-input{width:100%;background:var(--surface2);border:1px solid var(--border);color:var(--text);padding:8px;border-radius:6px;font-family:inherit;font-size:0.9em}
.form-input:focus{outline:none;border-color:var(--tcc)}
.add-entry-btn{position:fixed;bottom:28px;right:28px;z-index:150;width:52px;height:52px;border-radius:50%;background:linear-gradient(135deg,var(--tcc),var(--inest));border:none;color:#000;font-size:1.6em;cursor:pointer;box-shadow:0 6px 24px rgba(56,189,248,0.3);transition:var(--transition);display:flex;align-items:center;justify-content:center}
.add-entry-btn:hover{transform:scale(1.08);box-shadow:0 8px 30px rgba(56,189,248,0.4)}
@media(max-width:1200px){.kanban-dual{grid-template-columns:1fr}}
@media(max-width:768px){.kanban-grid{grid-template-columns:1fr 1fr}.daily-grid{grid-template-columns:1fr}.header{padding:10px 16px}.main{padding:14px}}
"""

print(f"CSS length: {len(CSS)}")

# ─── JS ───
JS = r"""
const CATS=["灵感","论文","专利","仿真程序","产品代码开发","项目指南策划"];
const DIMS=["TCC","iNEST"];
const STATUSES=["规划中","进行中","撰写中","开发中","测试中","验证中","探索中","资料整理","已完成","已发布","持续更新"];
let appData=JSON.parse(localStorage.getItem("rd_kanban_data")||"null")||JSON.parse(JSON.stringify(DEFAULT_DATA));
function saveData(){localStorage.setItem("rd_kanban_data",JSON.stringify(appData))}

function catEmoji(c){const m={"灵感":"💡","论文":"📄","专利":"🏷️","仿真程序":"🧪","产品代码开发":"💻","项目指南策划":"📋"};return m[c]||"📌"}
function statusTag(s){if(["已完成","已发布"].includes(s))return"tag-done";if(["进行中","撰写中","开发中","测试中","验证中"].includes(s))return"tag-ongoing";return"tag-plan"}
function fmtDate(d){return new Date(d).toLocaleDateString("zh-CN",{month:"short",day:"numeric"})}
const WEEKDAYS=["日","一","二","三","四","五","六"];

function renderMetrics(){
  const e=appData.entries;
  const tcc=e.filter(x=>x.dim==="TCC").length;
  const inest=e.filter(x=>x.dim==="iNEST").length;
  const active=e.filter(x=>!["已完成","已发布"].includes(x.status)).length;
  const done=e.filter(x=>["已完成","已发布"].includes(x.status)).length;
  const high=e.filter(x=>x.priority==="高"&&!["已完成","已发布"].includes(x.status)).length;
  document.getElementById("metrics").innerHTML=
    '<div class="metric tcc"><div class="num">'+tcc+'</div><div class="lbl">TCC 条目</div></div>'+
    '<div class="metric inest"><div class="num">'+inest+'</div><div class="lbl">iNEST 条目</div></div>'+
    '<div class="metric warn"><div class="num">'+active+'</div><div class="lbl">进行中</div></div>'+
    '<div class="metric" style="border-color:rgba(74,222,128,0.3)"><div class="num" style="color:var(--inest)">'+done+'</div><div class="lbl">已完成</div></div>'+
    '<div class="metric purple"><div class="num">'+high+'</div><div class="lbl">高优待办</div></div>';
}

function renderDaily(){
  const days=appData.daily;
  document.getElementById("daily-badge").textContent="最近 "+days.length+" 天";
  document.getElementById("daily-grid").innerHTML=days.map(d=>{
    let html='<div class="daily-card"><div class="daily-card-header"><span class="date">'+d.date+" "+WEEKDAYS[new Date(d.date).getDay()]+'</span><span class="date-badge '+d.type+'">'+(d.type==="today"?"今天":d.type==="yesterday"?"昨天":fmtDate(d.date))+'</span></div>';
    if(d.progress.length){html+='<div class="daily-section-label">📝 进展</div>';d.progress.forEach(p=>{html+='<div class="daily-item"><span class="dot '+p.dot+'"></span><span>'+p.text+' <span style="font-size:0.7em;color:var(--text-dim);margin-left:4px">['+p.dim+']</span></span></div>'})}
    if(d.plan.length){html+='<div class="daily-section-label">🎯 计划</div>';d.plan.forEach(p=>{html+='<div class="daily-item"><span class="dot '+p.dot+'"></span><span>'+p.text+' <span style="font-size:0.7em;color:var(--text-dim);margin-left:4px">['+p.dim+']</span></span></div>'})}
    html+='</div>';return html;
  }).join("");
}

function renderKanban(){
  document.getElementById("kanban-dual").innerHTML=DIMS.map(dim=>{
    const dc=dim.toLowerCase();
    const cols=CATS.map(cat=>{
      const items=appData.entries.filter(e=>e.dim===dim&&e.cat===cat);
      let col='<div class="kanban-col"><div class="kanban-col-header">'+catEmoji(cat)+" "+cat+'<span class="count">'+items.length+'</span></div>';
      items.forEach(item=>{
        col+='<div class="kanban-card" onclick="openDetail('+item.id+')"><div class="card-title">'+item.title+'</div><div class="card-meta"><span class="card-tag '+statusTag(item.status)+'">'+item.status+'</span><span>v'+item.ver+'</span><span class="card-tag '+(item.priority==="高"?"tag-high":item.priority==="中"?"tag-med":"")+'">'+item.priority+'</span></div>'+(item.link?'<div style="font-size:0.7em;color:var(--text-dim);margin-top:4px">📎 有附件</div>':"")+'</div>';
      });
      if(!items.length)col+='<div style="font-size:0.75em;color:var(--text-dim);padding:8px;text-align:center">暂无条目</div>';
      col+='</div>';return col;
    }).join("");
    return '<div class="kanban-column-group '+dc+'"><h3>'+(dim==="TCC"?"🔷 TCC · 可信计算与密码学":"🔶 iNEST · 智能涌现网络拓扑")+'</h3><div class="kanban-grid">'+cols+'</div></div>';
  }).join("");
}

let indexSort={field:"date",dir:-1};
let indexFilters={dim:null,cat:null,status:null,search:""};

function sortArrow(field){if(indexSort.field!==field)return'<span class="sort-arrow">⇅</span>';return indexSort.dir===1?'<span class="sort-arrow">↑</span>':'<span class="sort-arrow">↓</span>'}

function toggleSort(field){
  if(indexSort.field===field)indexSort.dir*=-1;else{indexSort.field=field;indexSort.dir=1}
  applyIndexFilters();
}

function setIndexFilter(type,val){
  indexFilters[type]=val;
  if(type==="search")indexFilters.search=document.getElementById("index-search").value;
  else document.getElementById("index-search").value=indexFilters.search;
  applyIndexFilters();
}

function renderIndexControls(){
  var h='<div class="search-box"><span class="search-icon">[SRCH]</span><input type="text" placeholder="搜索标题、描述、版本..." id="index-search" oninput="setIndexFilter(\"search\")" value="'+indexFilters.search+'"></div>';
  h+='<div class="filter-group"><button class="filter-chip '+(indexFilters.dim?null:"active")+'" onclick="setIndexFilter(\"dim\",null)">全部维度</button>';
  h+='<button class="filter-chip '+(indexFilters.dim==="TCC"?"active":"")+'" onclick="setIndexFilter(\"dim\",\"TCC\")">TCC</button>';
  h+='<button class="filter-chip '+(indexFilters.dim==="iNEST"?"active inest-chip":"")+'" onclick="setIndexFilter(\"dim\",\"iNEST\")">iNEST</button></div>';
  h+='<div class="filter-group"><button class="filter-chip '+(indexFilters.cat?null:"active")+'" onclick="setIndexFilter(\"cat\",null)">全部分类</button>';
  CATS.forEach(c=>{h+='<button class="filter-chip '+(indexFilters.cat===c?"active":"")+'" onclick="setIndexFilter(\"cat\",\"'+c+'\")">'+c+'</button>'});
  h+='</div><div class="filter-group"><button class="filter-chip '+(indexFilters.status?null:"active")+'" onclick="setIndexFilter(\"status\",null)">全部状态</button>';
  STATUSES.slice(0,7).forEach(s=>{h+='<button class="filter-chip '+(indexFilters.status===s?"active":"")+'" onclick="setIndexFilter(\"status\",\"'+s+'\")">'+s+'</button>'});
  h+='</div><span class="result-count" id="result-count"></span>';
  document.getElementById("index-controls").innerHTML=h;
}

function applyIndexFilters(){
  var entries=[...appData.entries];
  if(indexFilters.dim)entries=entries.filter(e=>e.dim===indexFilters.dim);
  if(indexFilters.cat)entries=entries.filter(e=>e.cat===indexFilters.cat);
  if(indexFilters.status)entries=entries.filter(e=>e.status===indexFilters.status);
  if(indexFilters.search){var q=indexFilters.search.toLowerCase();entries=entries.filter(e=>e.title.toLowerCase().includes(q)||e.desc.toLowerCase().includes(q)||e.ver.toLowerCase().includes(q))}

  var f=indexSort.field,d=indexSort.dir;
  var prioMap={"高":3,"中":2,"低":1};
  entries.sort((a,b)=>{
    var va,vb;
    if(f==="priority"){va=prioMap[a.priority]||0;vb=prioMap[b.priority]||0}
    else if(f==="date"){va=a.date;vb=b.date}
    else{va=(a[f]||"").toString();vb=(b[f]||"").toString()}
    if(va<vb)return -1*d;if(va>vb)return 1*d;return 0;
  });

  document.getElementById("result-count").textContent="共 "+entries.length+" 条";
  document.getElementById("index-badge").textContent=entries.length+" 条记录";

  if(!entries.length){document.getElementById("index-tbody").innerHTML="";document.getElementById("no-results").style.display="block";return}
  document.getElementById("no-results").style.display="none";

  document.getElementById("index-tbody").innerHTML=entries.map(e=>'<tr><td><span class="dim-badge '+e.dim.toLowerCase()+'">'+e.dim+'</span></td><td>'+catEmoji(e.cat)+" "+e.cat+'</td><td><strong>'+e.title+'</strong></td><td>'+(e.link?'<span class="ver-link" onclick="openDetail('+e.id+')" title="'+e.link+'">'+e.ver+'</span>':e.ver)+'</td><td><span class="card-tag '+statusTag(e.status)+'">'+e.status+'</span></td><td><span class="card-tag '+(e.priority==="高"?"tag-high":e.priority==="中"?"tag-med":"")+'">'+e.priority+'</span></td><td style="white-space:nowrap">'+e.date+'</td><td><button class="btn-sm info" onclick="openDetail('+e.id+')">详情</button> <button class="btn-sm danger" onclick="deleteEntry('+e.id+')">删除</button></td></tr>').join("");
}

function renderIndex(){
  document.getElementById("index-thead").innerHTML='<tr><th onclick="toggleSort(\"dim\")">维度 '+sortArrow("dim")+'</th><th onclick="toggleSort(\"cat\")">分类 '+sortArrow("cat")+'</th><th onclick="toggleSort(\"title\")">名称 '+sortArrow("title")+'</th><th onclick="toggleSort(\"ver\")">版本 '+sortArrow("ver")+'</th><th onclick="toggleSort(\"status\")">状态 '+sortArrow("status")+'</th><th onclick="toggleSort(\"priority\")">优先级 '+sortArrow("priority")+'</th><th onclick="toggleSort(\"date\")">更新时间 '+sortArrow("date")+'</th><th>操作</th></tr>';
  renderIndexControls();
  applyIndexFilters();
}

function openDetail(id){
  var e=appData.entries.find(x=>x.id===id);if(!e)return;
  document.getElementById("modal-content").innerHTML='<button class="close-btn" onclick="closeModal()">✕</button><h3>'+e.title+'</h3><span class="modal-dim dim-badge '+e.dim.toLowerCase()+'">'+e.dim+" · "+e.cat+'</span><div class="modal-field"><label>版本</label><div class="val">'+e.ver+'</div></div><div class="modal-field"><label>状态</label><div class="val"><span class="card-tag '+statusTag(e.status)+'">'+e.status+'</span></div></div><div class="modal-field"><label>优先级</label><div class="val"><span class="card-tag '+(e.priority==="高"?"tag-high":e.priority==="中"?"tag-med":"")+'">'+e.priority+'</span></div></div><div class="modal-field"><label>更新时间</label><div class="val">'+e.date+'</div></div><div class="modal-field"><label>描述</label><div class="val">'+e.desc+'</div></div>'+(e.link?'<div class="modal-field"><label>关联文件</label><div class="val" style="color:var(--tcc)">📎 '+e.link+'</div></div>':"");
  document.getElementById("modal-overlay").classList.add("show");
}

function closeModal(ev){
  if(ev&&ev.target!==document.getElementById("modal-overlay"))return;
  document.getElementById("modal-overlay").classList.remove("show");
}

function openAddForm(){
  var opts=CATS.map(c=>'<option value="'+c+'">'+c+'</option>').join("");
  var sOpts=STATUSES.map(s=>'<option value="'+s+'">'+s+'</option>').join("");
  document.getElementById("modal-content").innerHTML='<button class="close-btn" onclick="closeModal()">✕</button><h3>➕ 添加新条目</h3><form onsubmit="addEntry(event)" style="margin-top:16px"><div class="modal-field"><label>维度</label><select id="add-dim" class="form-input"><option value="TCC">TCC</option><option value="iNEST">iNEST</option></select></div><div class="modal-field"><label>分类</label><select id="add-cat" class="form-input">'+opts+'</select></div><div class="modal-field"><label>标题</label><input id="add-title" class="form-input" required></div><div class="modal-field"><label>版本</label><input id="add-ver" class="form-input" value="v0.1"></div><div class="modal-field"><label>状态</label><select id="add-status" class="form-input">'+sOpts+'</select></div><div class="modal-field"><label>优先级</label><select id="add-priority" class="form-input"><option value="高">高</option><option value="中">中</option><option value="低">低</option></select></div><div class="modal-field"><label>描述</label><textarea id="add-desc" class="form-input" rows="3" style="resize:vertical"></textarea></div><div class="modal-field"><label>关联文件路径 (可选)</label><input id="add-link" class="form-input" placeholder="相对路径，如 phase1_workspace/sdi_v29_functional.py"></div><button type="submit" style="width:100%;background:linear-gradient(135deg,var(--tcc),var(--inest));border:none;color:#000;padding:10px;border-radius:8px;font-weight:600;cursor:pointer;font-family:inherit;margin-top:8px">添加条目</button></form>';
  document.getElementById("modal-overlay").classList.add("show");
}

function addEntry(ev){
  ev.preventDefault();
  var entry={
    id:Math.max(0,...appData.entries.map(e=>e.id))+1,
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
}

function deleteEntry(id){
  if(!confirm("确定要删除此条目吗？此操作不可撤销。"))return;
  appData.entries=appData.entries.filter(e=>e.id!==id);
  saveData();refreshAll();
}

function switchView(view){
  document.querySelectorAll(".header-nav button").forEach(b=>b.classList.remove("active"));
  document.querySelector('[data-view="'+view+'"]').classList.add("active");
  document.querySelectorAll(".view-panel").forEach(p=>p.classList.remove("active"));
  document.getElementById("view-"+view).classList.add("active");
  if(view==="index")renderIndex();
}

function refreshAll(){
  renderMetrics();renderDaily();renderKanban();
  var av=document.querySelector(".view-panel.active").id;
  if(av==="view-index")renderIndex();
}

function animateIn(){
  gsap.from(".metric",{opacity:0,y:20,duration:0.5,stagger:0.06,ease:"power2.out"});
  gsap.from(".daily-card",{opacity:0,y:16,duration:0.4,stagger:0.08,ease:"power2.out",delay:0.2});
  gsap.from(".kanban-col",{opacity:0,y:12,duration:0.35,stagger:0.04,ease:"power2.out",delay:0.4});
}

document.addEventListener("DOMContentLoaded",function(){
  document.getElementById("header-date").textContent=new Date().toLocaleDateString("zh-CN",{year:"numeric",month:"long",day:"numeric",weekday:"long"});
  document.querySelectorAll(".header-nav button").forEach(b=>b.addEventListener("click",function(){switchView(b.dataset.view)}));
  document.addEventListener("keydown",function(e){if(e.key==="Escape")closeModal()});
  refreshAll();animateIn();
});
"""

print(f"JS length: {len(JS)}")

# ─── GENERATE HTML ───
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TCC × iNEST 研发全景看板</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
{css}
</style>
</head>
<body>
<header class="header">
  <div class="header-left">
    <div class="header-logo">NX</div>
    <h1><span class="tcc">TCC</span> × <span class="inest">iNEST</span> 研发全景看板</h1>
  </div>
  <nav class="header-nav">
    <button class="active" data-view="kanban">📋 看板</button>
    <button data-view="index">📊 索引表</button>
  </nav>
  <div class="header-date" id="header-date"></div>
</header>

<main class="main">
  <div class="metrics" id="metrics"></div>
  <div class="section-title">📅 每日进展与明日计划 <span class="badge" id="daily-badge"></span></div>
  <div class="daily-grid" id="daily-grid"></div>

  <div class="view-panel active" id="view-kanban">
    <div class="kanban-dual" id="kanban-dual"></div>
  </div>

  <div class="view-panel" id="view-index">
    <div class="section-title">[SRCH] 成果索引表 <span class="badge" id="index-badge"></span></div>
    <div class="index-controls" id="index-controls"></div>
    <div class="table-wrap">
      <table class="index-table">
        <thead id="index-thead"></thead>
        <tbody id="index-tbody"></tbody>
      </table>
      <div class="no-results" id="no-results" style="display:none">[SRCH] 未找到匹配的条目 — 尝试调整筛选条件</div>
    </div>
  </div>
</main>

<div class="modal-overlay" id="modal-overlay" onclick="closeModal(event)">
  <div class="modal" id="modal-content" onclick="event.stopPropagation()"></div>
</div>

<button class="add-entry-btn" onclick="openAddForm()" title="添加新条目">+</button>

<script>
const DEFAULT_DATA = {data_json};

{js}
</script>
</body>
</html>"""

OUT = r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html"

html = HTML_TEMPLATE.format(
    css=CSS,
    data_json=json.dumps(default_data, ensure_ascii=False),
    js=JS
)

with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)

print(f"[OK] Generated: {OUT}")
print(f"   File size: {len(html)} bytes")
print(f"   Entries: {len(default_data['entries'])}")
print(f"   Daily records: {len(default_data['daily'])}")

