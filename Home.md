---
cssclass: dashboard
---

# TCC + iNEST 自进化研发中枢

> 主页只负责导航和决策；具体任务以[研发看板](http://127.0.0.1:8899/home/work/.openclaw/workspace/70_Dashboard/index.html)为准，论文洞察以[每日行动](http://127.0.0.1:8899/home/work/.openclaw/workspace/60_MOC/03_Daily_Action.md)为准，知识库状态以[统一状态快照](http://127.0.0.1:8899/home/work/.openclaw/workspace/99_Meta/research_state.json)为准。

## 今日控制台

| 项目 | 当前值 | 入口 |
|---|---:|---|
| 知识库文件 | <span class="vault-count" data-key="total">--</span> | [知识库根目录](http://127.0.0.1:8899/home/work/.openclaw/workspace/) |
| TCC 资料 | <span class="vault-count" data-key="tcc">--</span> | [TCC 主索引](http://127.0.0.1:8899/home/work/.openclaw/workspace/30_TCC/TCC_Master_Index.md) |
| iNEST 资料 | <span class="vault-count" data-key="inest">--</span> | [iNEST 主索引](http://127.0.0.1:8899/home/work/.openclaw/workspace/40_iNEST/iNEST_Master_Index.md) |
| 今日待处理 | <span class="vault-count" data-key="inbox">--</span> | [论文收件箱](http://127.0.0.1:8899/home/work/.openclaw/workspace/00_Inbox/_pipeline_insights/) |
| 处理区 | <span class="vault-count" data-key="processing">--</span> | [处理中](http://127.0.0.1:8899/home/work/.openclaw/workspace/20_Processing/) |
| 成果区 | <span class="vault-count" data-key="outputs">--</span> | [50_Output](http://127.0.0.1:8899/home/work/.openclaw/workspace/50_Output/) |

**今天先做什么：**打开[今日行动洞察](http://127.0.0.1:8899/home/work/.openclaw/workspace/60_MOC/03_Daily_Action.md)，按重要性和紧迫性执行；完成后把证据链接回写到论文、专利或仿真记录。

## 实时工作摘要

<div id="live-work-summary">正在读取知识库当前任务与管线状态...</div>

## 研发总入口

| 决策入口 | 解决的问题 | 更新节奏 |
|---|---|---|
| [研发看板](http://127.0.0.1:8899/home/work/.openclaw/workspace/70_Dashboard/index.html) | 今天做什么、近三日完成什么、TCC/iNEST 当前洞察是什么 | 每日 |
| [今日行动洞察](http://127.0.0.1:8899/home/work/.openclaw/workspace/60_MOC/03_Daily_Action.md) | 把论文信息转成可执行任务、实验和写作动作 | 每日 |
| [今日焦点任务](http://127.0.0.1:8899/home/work/.openclaw/workspace/60_MOC/04_Daily_Focus.md) | 锁定并行主线和当天最重要的少数任务 | 每日 |
| [研究洞察](http://127.0.0.1:8899/home/work/.openclaw/workspace/60_MOC/02_Research_Insights.md) | 汇总论文对 TCC/iNEST 的方法论启发 | 每日 |
| [成果全景](http://127.0.0.1:8899/home/work/.openclaw/workspace/60_MOC/TCC_iNEST_成果全景.md) | 检查论文、专利、代码和项目指南落地 | 每周 |
| [健康报告](http://127.0.0.1:8899/home/work/.openclaw/workspace/60_MOC/weekly_health_20260719.md) | 检查服务、管线、链接、Git 和知识库健康度 | 每周 |

## 并行研发双轨

### TCC：拓扑中心计算

| 层级 | 当前推进 | 必须留下的证据 |
|---|---|---|
| 理论 | P-Paradigm：拓扑作为计算原语，完成投稿前终稿 | 定义、定理、推导、引用和反例 |
| 技术 | SDI/NoC/Chiplet/晶上互连拓扑与调度 | 拓扑参数、路由策略、复杂度和对照组 |
| 工程 | CST 仿真、FPGA/RTL 原型、工具链验证 | 可复现实验脚本、配置、日志和图表 |
| 交付 | TCC 架构专利与实现专利 | 权利要求、实施例、附图和现有技术对比 |

入口：[TCC 主索引](http://127.0.0.1:8899/home/work/.openclaw/workspace/30_TCC/TCC_Master_Index.md) · [TCC 论文库](http://127.0.0.1:8899/home/work/.openclaw/workspace/50_Output/51_Papers/) · [TCC 专利库](http://127.0.0.1:8899/home/work/.openclaw/workspace/50_Output/52_Patents/)

### iNEST：复杂网络涌现智能

| 层级 | 当前推进 | 必须留下的证据 |
|---|---|---|
| 理论 | CST 智能涌现、临界性、自组织与非线性增益 | 模型假设、动力学方程、临界指标和边界条件 |
| 技术 | SNN、储备池、STDP/FEP、多尺度网络 | 网络结构、学习规则、训练配置和基线比较 |
| 工程 | SNN/异步电路/存算一体与晶上部署 | 仿真、综合、资源、功耗和时延测量 |
| 交付 | iNEST 论文、专著、白皮书和相关专利 | 版本、章节状态、引用证据和下一步任务 |

入口：[iNEST 主索引](http://127.0.0.1:8899/home/work/.openclaw/workspace/40_iNEST/iNEST_Master_Index.md) · [iNEST 论文库](http://127.0.0.1:8899/home/work/.openclaw/workspace/50_Output/51_Papers/) · [iNEST 代码库](http://127.0.0.1:8899/home/work/.openclaw/workspace/50_Output/54_Code/)

## 从知识到成果

```text
论文/微信/得到大脑剪藏
        ↓
00_Inbox/_pipeline_insights（原始来源 + 摘要 + 链接）
        ↓
科研管线：去重 → 相关性筛选 → TCC/iNEST 深度分析
        ↓
每日行动：价值判断 → 研究问题 → 实验/写作/专利任务
        ↓
20_Processing：待验证内容
        ↓
30_TCC / 40_iNEST：稳定知识与双向链接
        ↓
50_Output：论文、专利、代码、项目指南
        ↓
验证证据回写 → 看板更新 → 周度复盘 → 下一轮检索与任务
```

目录入口：[论文收件箱](http://127.0.0.1:8899/home/work/.openclaw/workspace/00_Inbox/_pipeline_insights/) · [处理中](http://127.0.0.1:8899/home/work/.openclaw/workspace/20_Processing/) · [TCC知识区](http://127.0.0.1:8899/home/work/.openclaw/workspace/30_TCC/) · [iNEST知识区](http://127.0.0.1:8899/home/work/.openclaw/workspace/40_iNEST/) · [成果输出区](http://127.0.0.1:8899/home/work/.openclaw/workspace/50_Output/)

## 自进化规则

1. 每条重要结论必须关联论文、实验、仿真或可复现推导；没有来源的数字只能标记为“待测”。
2. 每篇进入知识库的论文必须回答：对 TCC 的价值、对 iNEST 的价值、可执行的研究启发、下一步验证任务。
3. 每个研究任务必须有输出物和验收证据，完成后才从“进行中”转为“已完成”。
4. 每周检查重复内容、断链、过期计划、模型调用、管线耗时和 Git 状态；问题进入[健康诊断](http://127.0.0.1:8899/home/work/.openclaw/workspace/60_MOC/00_Diagnostic_Report.md)。

## 自动化节奏

| 时间 | 自动动作 | 结果 |
|---|---|---|
| 08:00 | 科研管线检索与相关性筛选 | 新论文、摘要、TCC/iNEST 洞察 |
| 08:30 | 看板更新 | 今日计划、双轨洞察、近三日进展 |
| 20:00 | Inbox 处理 | 去重、归类、链接和待验证项 |
| 21:00 | GitHub/Gitee 同步 | 版本留痕与成果备份 |
| 周日 03:00 | 健康检查与自进化 | 证据账本、假设注册表、改进队列 |

系统入口：[统一状态快照](http://127.0.0.1:8899/home/work/.openclaw/workspace/99_Meta/research_state.json) · [证据账本](http://127.0.0.1:8899/home/work/.openclaw/workspace/99_Meta/evolution_ledger.json) · [假设注册表](http://127.0.0.1:8899/home/work/.openclaw/workspace/99_Meta/hypothesis_registry.json) · [进化队列](http://127.0.0.1:8899/home/work/.openclaw/workspace/99_Meta/evolution_queue.json)

<script>
(async function(){
  try{
    const r=await fetch('/home/work/.openclaw/workspace/99_Meta/research_state.json?ts='+Date.now());
    if(!r.ok)return;
    const d=await r.json();
    const v=d.vault||{};
    const values={total:v.total_md,tcc:v.tcc_30,inest:v.inest_40,inbox:v.inbox_00,processing:v.processing_20,outputs:v.output_50};
    document.querySelectorAll('.vault-count').forEach(function(e){
      const value=values[e.dataset.key];
      if(value!==undefined)e.textContent=value;
    });

    const script=await fetch('/home/work/.openclaw/workspace/70_Dashboard/data.js?ts='+Date.now()).then(function(x){return x.text()});
    const match=script.match(/window\.RESEARCH_DASHBOARD\s*=\s*(\{[\s\S]*\});\s*$/);
    if(!match)return;
    const live=JSON.parse(match[1]);
    const plan=(live.plan||[]).slice(0,5).map(function(item){return '<li><strong>'+item.track+'</strong> · '+item.text+'</li>'}).join('');
    const progress=(live.progress||[]).slice(0,3).map(function(item){return '<li>'+item.date+' · '+item.summary+'</li>'}).join('');
    document.getElementById('live-work-summary').innerHTML=
      '<h3>今日计划</h3><ol>'+plan+'</ol><h3>近三日进展</h3><ul>'+progress+'</ul>';
  }catch(e){}
})();
</script>
