# build_kanban_v3.py - Complete rebuilt generator with all fixes
import json, os

OUT = r"D:\Obsidian\home\work\.openclaw\workspace\dashboard\index.html"

DAILY = [
  {"date":"2026-06-05","type":"today","progress":[
    {"text":"看板v3迭代：修复筛选联动、文件超链接、新增14篇论文专利索引文件","dot":"done","dim":"TCC+iNEST"},
    {"text":"Meta-Topology SDI-Bond论文 v3修订完成","dot":"done","dim":"TCC"},
    {"text":"CST Theory V26修订版定稿（From Compute to Complexity）","dot":"done","dim":"TCC"},
    {"text":"SDI v30多区域拓扑仿真参数调优中","dot":"ongoing","dim":"TCC"},
    {"text":"连接组数据下载管线搭建（CONNECTOME_DOWNLOAD_TASK）","dot":"ongoing","dim":"iNEST"}
  ],"plan":[
    {"text":"SDI v30多区域跨尺度耦合验证实验","dot":"plan","dim":"TCC"},
    {"text":"FEP-STDP收敛性证明完成并写入专利文档","dot":"plan","dim":"iNEST"},
    {"text":"iNEST核心架构论文Results章节撰写","dot":"plan","dim":"iNEST"}
  ]},
  {"date":"2026-06-04","type":"yesterday","progress":[
    {"text":"SDI v30多区域拓扑仿真框架搭建完成","dot":"done","dim":"TCC"},
    {"text":"SDI v29功能性涌现模块集成测试，PASS率94.2%","dot":"done","dim":"iNEST"},
    {"text":"iNEST核心架构论文Methods章节定稿","dot":"done","dim":"iNEST"},
    {"text":"海河V8 SDI仿真验证数据补充完成","dot":"done","dim":"TCC"}
  ],"plan":[
    {"text":"SDI v30多区域耦合验证","dot":"done","dim":"TCC"},
    {"text":"专利组合文档v2.1更新","dot":"ongoing","dim":"TCC+iNEST"}
  ]},
  {"date":"2026-06-03","type":"past","progress":[
    {"text":"SDI v8-v28版本批量回归测试与性能对比","dot":"done","dim":"iNEST"},
    {"text":"FPGA Verilog代码：sdio_bond_core_v24模块实现","dot":"done","dim":"iNEST"},
    {"text":"STDP-FEP梯度下降统一映射理论文档完成","dot":"done","dim":"iNEST"},
    {"text":"SDI化合物键四型架构文档完成","dot":"done","dim":"TCC"},
    {"text":"iNEST爬虫系统更新，知识采集管线优化","dot":"done","dim":"iNEST"},
    {"text":"自演化机制全景总结文档完成","dot":"done","dim":"iNEST"}
  ],"plan":[]},
  {"date":"2026-06-02","type":"past","progress":[
    {"text":"SDI v27-v28多尺度融合框架实现完成","dot":"done","dim":"iNEST"},
    {"text":"专利组合详细方案初稿（FEP-STDP/涌现检测/拓扑优化）","dot":"done","dim":"TCC+iNEST"},
    {"text":"每日网络爬取管线建立（iNEST Daily Crawl）","dot":"done","dim":"iNEST"}
  ],"plan":[]}
]

ENTRIES = [
  # ═══ TCC - 拓扑中心计算 ═══
  # -- 灵感 --
  {"id":1,"dim":"TCC","cat":"灵感","title":"从节点中心到拓扑中心：计算范式根本转变的理论框架","ver":"v2.0","status":"进行中","date":"2026-06-05","desc":"提出将计算的基本单元从单个节点提升至网络拓扑结构本身，以拓扑不变量（Betti数、持续同调等）作为计算原语","priority":"高"},
  {"id":2,"dim":"TCC","cat":"灵感","title":"多区域网络拓扑的涌现性耦合机制","ver":"v1.5","status":"验证中","date":"2026-06-04","desc":"探索多个拓扑子区域间的信息流耦合与协同涌现条件，对应SDI v30 multi-region实验","priority":"高"},
  {"id":3,"dim":"TCC","cat":"灵感","title":"最小作用量原理驱动的网络拓扑自组织","ver":"v1.0","status":"进行中","date":"2026-06-03","desc":"基于最小作用量原理，将网络拓扑演化建模为变分问题，统一FEP与STDP框架","priority":"高","link":"home/work/.openclaw/workspace/03_Topics/Concepts-Theory/iNEST_自演化机制全景总结_最小作用量到物理智能.md"},

  # -- 论文 --
  {"id":4,"dim":"TCC","cat":"论文","title":"Meta-Topology and SDI-Bond: Variational Framework for Communication Primitive Generation and Fractal Network Evolution","ver":"v3","status":"撰写中","date":"2026-06-04","desc":"元拓扑与SDI化合物键：最小作用量原理下通信原语生成与分形网络演化的变分框架","priority":"高","link":"home/work/.openclaw/workspace/iNEST_2_论文撰写/P-Theory_v3_Revised.md"},
  {"id":5,"dim":"TCC","cat":"论文","title":"From Compute to Complexity: A Physical Theory of Intelligence Emergence and Its Implications for AGI","ver":"V26","status":"撰写中","date":"2026-06-04","desc":"从计算到复杂性：智能涌现的物理理论及其对AGI的启示（CST Theory核心论文）","priority":"高","link":"home/work/.openclaw/workspace/TCC_2_论文撰写/A1_CST_Theory_V26_REVISED.md"},
  {"id":6,"dim":"TCC","cat":"论文","title":"SDI化合物键四型架构：通信原语生成与分形网络演化的变分框架","ver":"v1","status":"撰写中","date":"2026-06-03","desc":"SDI化合物键的四种类型（离子/共价/金属/氢键）在通信原语中的应用","priority":"高","link":"home/work/.openclaw/workspace/03_Topics/Concepts-Theory/08_SDI化合物键_四型架构.md"},
  {"id":7,"dim":"TCC","cat":"论文","title":"NCL神经计算定律详解：零约定逻辑在拓扑中心计算中的应用","ver":"v1","status":"资料整理","date":"2026-06-03","desc":"NULL Convention Logic在拓扑中心计算架构中的异步计算优势分析","priority":"中","link":"home/work/.openclaw/workspace/03_Topics/Concepts-Theory/08_NCL神经计算定律详解.md"},

  # -- 专利 --
  {"id":8,"dim":"TCC","cat":"专利","title":"一种基于网络拓扑不变量的分布式计算方法","ver":"构思-v2","status":"撰写中","date":"2026-06-04","desc":"利用拓扑不变量（Betti数、Euler示性数）作为分布式计算原语，突破节点中心范式","priority":"高"},
  {"id":9,"dim":"TCC","cat":"专利","title":"多区域拓扑网络的自适应耦合系统与方法","ver":"构思-v1","status":"规划中","date":"2026-06-01","desc":"基于SDI v30 multi-region架构的多区域拓扑自适应耦合方法","priority":"中"},
  {"id":10,"dim":"TCC","cat":"专利","title":"基于最小作用量原理的网络拓扑自组织优化方法","ver":"构思-v1","status":"规划中","date":"2026-06-03","desc":"以最小作用量原理统一FEP与STDP，实现网络拓扑的全局最优演化","priority":"高"},

  # -- 仿真 --
  {"id":11,"dim":"TCC","cat":"仿真程序","title":"SDI v30 多区域拓扑仿真","ver":"v30","status":"测试中","date":"2026-06-04","desc":"最新版SDI，实现多区域拓扑网络的跨尺度耦合与区域间涌现交互","priority":"高","link":"phase1_workspace/sdi_v30_multiregion.py"},
  {"id":12,"dim":"TCC","cat":"仿真程序","title":"拓扑不变量计算与可视化工具","ver":"v0.2","status":"规划中","date":"2026-05-25","desc":"基于持续同调的网络拓扑特征提取与可视化工具","priority":"中"},
  {"id":13,"dim":"TCC","cat":"仿真程序","title":"海河V8 SDI仿真验证","ver":"v8","status":"已完成","date":"2026-06-04","desc":"海河V8平台上的SDI仿真验证实验，含数据补充报告","priority":"高","link":"home/work/.openclaw/workspace/TCC_1_项目策划/海河V8_SDI仿真验证数据补充.md"},

  # -- 产品代码 --
  {"id":14,"dim":"TCC","cat":"产品代码开发","title":"TCC拓扑中心计算引擎 (Python)","ver":"v0.3-dev","status":"开发中","date":"2026-06-05","desc":"拓扑中心计算核心引擎，将网络拓扑结构作为一等计算对象","priority":"高"},
  {"id":15,"dim":"TCC","cat":"产品代码开发","title":"FPGA拓扑加速模块 (Verilog)","ver":"v0.1-prototype","status":"开发中","date":"2026-06-03","desc":"SDI关键路径FPGA硬件加速原型，含sdio_bond_core_v24","priority":"高","link":"phase1_workspace/iNEST_4_工程开发/fpga"},

  # -- 项目指南 --
  {"id":16,"dim":"TCC","cat":"项目指南策划","title":"TCC拓扑中心计算技术白皮书","ver":"大纲-v1","status":"规划中","date":"2026-06-04","desc":"全面阐述拓扑中心计算范式：理论基础、计算模型、工程实现与产业前景","priority":"高"},
  {"id":17,"dim":"TCC","cat":"项目指南策划","title":"论文总清单与投稿计划","ver":"v1.0","status":"持续更新","date":"2026-06-04","desc":"TCC/iNEST全部论文的状态跟踪、目标期刊与投稿时间线","priority":"高","link":"home/work/.openclaw/workspace/TCC_2_论文撰写/00_论文总清单.md"},
  {"id":18,"dim":"TCC","cat":"项目指南策划","title":"专利布局总览","ver":"v1.0","status":"持续更新","date":"2026-06-04","desc":"TCC/iNEST专利组合的全局视图、优先级排序与申请策略","priority":"高","link":"home/work/.openclaw/workspace/TCC_3_专利撰写/00_专利布局总览.md"},

  # ═══ iNEST - 复杂网络涌现智能 ═══
  # -- 灵感 --
  {"id":19,"dim":"iNEST","cat":"灵感","title":"FEP自由能原理驱动的网络功能涌现临界条件","ver":"v2.1","status":"验证中","date":"2026-06-04","desc":"探索FEP自由能最小化与网络临界相变的数学联系，寻找涌现智能的相变边界","priority":"高"},
  {"id":20,"dim":"iNEST","cat":"灵感","title":"SDI框架下的多尺度拓扑自组织机制","ver":"v1.8","status":"进行中","date":"2026-06-03","desc":"研究微观-介观-宏观三层网络中自组织拓扑的形成与演化规律","priority":"高"},
  {"id":21,"dim":"iNEST","cat":"灵感","title":"JEPA架构与iNEST的借鉴路径","ver":"v1.0","status":"探索中","date":"2026-06-03","desc":"分析JEPA（联合嵌入预测架构）与iNEST自演化机制的交叉借鉴可能性","priority":"中","link":"home/work/.openclaw/workspace/03_Topics/AI-ML/JEPA-LNN-iNEST_借鉴路径与快速验证策略.md"},

  # -- 论文 --
  {"id":22,"dim":"iNEST","cat":"论文","title":"SDI Compound-Bond Self-Evolving Network Architecture","ver":"draft-v5","status":"撰写中","date":"2026-06-04","desc":"SDI化合物键自演化网络架构：核心架构论文","priority":"高","link":"phase1_workspace/papers/paper1_iNEST_core_architecture.md"},
  {"id":23,"dim":"iNEST","cat":"论文","title":"Liquid Computing Chemistry: FEP-driven Self-organization in Artificial Neural Substrates","ver":"draft-v2","status":"撰写中","date":"2026-06-03","desc":"液态计算化学：FEP驱动的人工神经基质自组织与涌现","priority":"高","link":"phase1_workspace/papers/paper2_liquid_computing_chemistry.md"},
  {"id":24,"dim":"iNEST","cat":"论文","title":"STDP-FEP梯度下降统一映射：脉冲时间依赖可塑性与自由能原理的数学桥接","ver":"v1","status":"撰写中","date":"2026-06-03","desc":"建立STDP与FEP之间的严格数学对应关系，为自演化网络提供统一理论","priority":"高","link":"home/work/.openclaw/workspace/03_Topics/Concepts-Theory/08_STDP-FEP梯度下降统一映射.md"},
  {"id":25,"dim":"iNEST","cat":"论文","title":"类脑计算最新综述与iNEST定位分析","ver":"outline","status":"资料整理","date":"2026-05-22","desc":"基于Nature Electronics综述，梳理iNEST在类脑计算与涌现智能领域的定位","priority":"中","link":"GetNotes_Inbox/_processed/类脑计算最新综述.md"},
  {"id":26,"dim":"iNEST","cat":"论文","title":"算力网络拓扑趋势与iNEST架构对比分析","ver":"notes","status":"资料整理","date":"2026-05-28","desc":"基于CXL 3.0等算力网络趋势，分析iNEST拓扑中心架构的差异化优势","priority":"中","link":"GetNotes_Inbox/_processed/芯片算力网络趋势.md"},

  # -- 专利 --
  {"id":27,"dim":"iNEST","cat":"专利","title":"专利组合详细方案（6项核心专利）","ver":"v2.1","status":"撰写中","date":"2026-06-03","desc":"含FEP-STDP融合、功能涌现检测、多尺度拓扑优化、多区域耦合等6项","priority":"高","link":"phase1_workspace/patents/patent_portfolio_detailed.md"},
  {"id":28,"dim":"iNEST","cat":"专利","title":"一种基于自由能原理的自组织网络拓扑优化方法","ver":"申请稿-v1","status":"撰写中","date":"2026-05-20","desc":"FEP驱动的网络拓扑自适应优化方法","priority":"高"},
  {"id":29,"dim":"iNEST","cat":"专利","title":"神经网络功能涌现检测与量化方法","ver":"构思-v1","status":"规划中","date":"2026-06-01","desc":"基于信息论与拓扑指标的神经网络功能涌现自动检测","priority":"中"},

  # -- 仿真 --
  {"id":30,"dim":"iNEST","cat":"仿真程序","title":"SDI v29功能性涌现仿真","ver":"v29","status":"已完成","date":"2026-06-04","desc":"功能性涌现模块集成，含自组织临界检测与涌现度量，PASS率94.2%","priority":"高","link":"phase1_workspace/sdi_v29_functional.py"},
  {"id":31,"dim":"iNEST","cat":"仿真程序","title":"SDI v28多尺度融合仿真","ver":"v28","status":"已完成","date":"2026-06-02","desc":"微观-介观-宏观三层多尺度网络融合框架","priority":"高","link":"phase1_workspace/sdi_v28_multiscale.py"},
  {"id":32,"dim":"iNEST","cat":"仿真程序","title":"SDI v27真实连接组多尺度仿真","ver":"v27","status":"已完成","date":"2026-06-03","desc":"基于真实连接组数据的多尺度仿真，四组实验全部通过","priority":"中","link":"phase1_workspace/sdi_v27_multiscale.py"},
  {"id":33,"dim":"iNEST","cat":"仿真程序","title":"SDI v26多尺度仿真框架","ver":"v26","status":"已完成","date":"2026-05-20","desc":"多尺度仿真框架初步实现","priority":"中","link":"phase1_workspace/sdi_v26_multiscale.py"},
  {"id":34,"dim":"iNEST","cat":"仿真程序","title":"SDI v25物理-生物融合仿真","ver":"v25","status":"已完成","date":"2026-06-03","desc":"物理第一性原理与生物启发机制六项验证","priority":"中","link":"phase1_workspace/sdi_v25_physical_biological.py"},
  {"id":35,"dim":"iNEST","cat":"仿真程序","title":"SDI v24 FEP-STDP融合仿真","ver":"v24","status":"已完成","date":"2026-06-03","desc":"FEP与STDP双目标首次同时达成，融合机制验证","priority":"高","link":"phase1_workspace/sdi_v24_fep_stdp_fusion.py"},
  {"id":36,"dim":"iNEST","cat":"仿真程序","title":"SDI v11 FEP进化仿真改进版","ver":"v11","status":"已完成","date":"2026-05-01","desc":"改进版FEP驱动的网络进化仿真，解决v10坍缩问题","priority":"中","link":"phase1_workspace/sdi_v11_fep_improved.py"},

  # -- 产品代码 --
  {"id":37,"dim":"iNEST","cat":"产品代码开发","title":"iNEST核心网络引擎 (Python)","ver":"v0.6-dev","status":"开发中","date":"2026-06-04","desc":"SDI核心算法的工程化实现，支持大规模复杂网络的拓扑分析与涌现检测","priority":"高"},
  {"id":38,"dim":"iNEST","cat":"产品代码开发","title":"FPGA硬件加速模块 (Verilog)","ver":"v0.1-prototype","status":"开发中","date":"2026-06-03","desc":"SDI关键路径硬件加速：sdio_bond_core_v24及其测试平台","priority":"高","link":"phase1_workspace/iNEST_4_工程开发"},
  {"id":39,"dim":"iNEST","cat":"产品代码开发","title":"投资者演示Demo v3","ver":"v3.0","status":"已完成","date":"2026-06-03","desc":"面向投资人的交互式产品演示站点","priority":"高","link":"phase1_workspace/investor_demo/index.html"},
  {"id":40,"dim":"iNEST","cat":"产品代码开发","title":"iNEST知识采集爬虫","ver":"v1.2","status":"已完成","date":"2026-06-03","desc":"自动化文献与资讯采集管线，支持每日网络爬取","priority":"中","link":"scripts/iNEST_crawler.py"},
  {"id":41,"dim":"iNEST","cat":"产品代码开发","title":"CONNECTOME数据下载与预处理管线","ver":"v0.1","status":"开发中","date":"2026-06-04","desc":"连接组数据批量下载、格式转换与SDI输入适配","priority":"中","link":"phase1_workspace/CONNECTOME_DOWNLOAD_TASK.md"},

  # -- 项目指南 --
  {"id":42,"dim":"iNEST","cat":"项目指南策划","title":"iNEST复杂网络涌现智能技术白皮书","ver":"v1.2","status":"持续更新","date":"2026-06-05","desc":"iNEST整体技术体系：拓扑中心计算范式、FEP-STDP融合、SDI框架、应用场景","priority":"高"},
  {"id":43,"dim":"iNEST","cat":"项目指南策划","title":"V29功能性涌现仿真推进计划","ver":"v1.0","status":"已完成","date":"2026-06-03","desc":"SDI v29功能性涌现模块的开发计划、里程碑与验证标准","priority":"高","link":"phase1_workspace/V29_Simulation_Advancement_Plan.md"},
  {"id":44,"dim":"iNEST","cat":"项目指南策划","title":"iNEST CS团队协作指南","ver":"v1.0","status":"已发布","date":"2026-06-03","desc":"团队协作规范、开发流程、知识管理与工具链","priority":"高","link":"iNEST_CS团队指南.pdf"},
  {"id":45,"dim":"iNEST","cat":"项目指南策划","title":"iNEST对外合作介绍材料","ver":"v2.0","status":"已发布","date":"2026-06-04","desc":"面向合作伙伴与投资人的项目介绍与技术能力展示","priority":"高","link":"iNEST对外合作介绍材料.html"},
  {"id":46,"dim":"iNEST","cat":"项目指南策划","title":"研发路线图与里程碑规划 (Q3-Q4)","ver":"v1.5","status":"持续更新","date":"2026-06-01","desc":"Q3-Q4研发里程碑、资源分配、风险评估与应对预案","priority":"高"},
  {"id":47,"dim":"iNEST","cat":"项目指南策划","title":"关键指标参考手册","ver":"v1.0","status":"已完成","date":"2026-06-03","desc":"SDI全部关键指标的物理含义、计算公式与生物权威来源对照","priority":"中","link":"home/work/.openclaw/workspace/03_Topics/Concepts-Theory/08_关键指标参考手册.md"},
]

default_data = {"daily": DAILY, "entries": ENTRIES}
print(f"Data ready: {len(ENTRIES)} entries, {len(DAILY)} days")
