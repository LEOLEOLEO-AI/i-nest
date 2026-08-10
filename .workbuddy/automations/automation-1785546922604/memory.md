# 知识库每日自进化 — 执行记忆

## 运行方式（重要）
- 工作目录：`D:/obsidian/vault`
- 解释器：**必须用系统 Python 3.10**
  `C:/Users/LEO/AppData/Local/Programs/Python/Python310/python.exe 90_System/scripts/self_evolve.py`
  （bash 中无 `python3`/`python` 命令；脚本内部用 `sys.executable` 派生子进程，解释器需一致）
- 典型耗时约 2-5 分钟（wiki_compiler 超时已提至 3600s，大积压不再误超时）。
- 脚本自带超时与失败隔离，单步失败不影响其余；**不要重试或做破坏性操作**。
- git push 已内置 non-fast-forward 自动恢复（pull --no-rebase 后重推）。
- **wiki_grow 性能注意**：概念数 3000+ 时 O(n²) 共现链接耗时约 30 分钟。如积压大，建议先跑 compile 再单独跑 grow。

## 已知常态现象（非故障，勿误报）
- `99_Meta/self_evolve_log.json` 在 git 提交之后才写入，故每次跑完必残留 1 个未提交改动，下一轮自动带走。
- `import_processor` 提示 "New imports detected — wiki_compiler should be triggered next"：
  因 compile 步骤排在 phase4 之前，当轮新导入会顺延到**下一轮**编译。属设计行为。
- 断链/孤儿基数偏大（千级）主要来自历史日记页、S2 长标题文献、含反斜杠的 Windows 路径式链接。

## 执行历史

### 2026-08-02（首次记录，全绿）
- 全部步骤成功：compile / grow / health / grow_concepts / phase4(4子项) / homepage / git
- compile 增量：1 篇文章 → 5 个概念（走了 LLM 抽取）
- wiki_grow：概念 304，已链接 299，图谱内孤儿 107
- 健康自检：笔记 4573 · 断链 1334 · 孤儿 2058 · 缺 FM 36
- 概念补全：0 篇（高频缺失项均已存在或被 DENY 规则过滤）
- git：提交 288 文件，push github main 成功（HEAD 与 github/main 一致）
- 待办观察：raw/ 新增 1 个 Genspark 导入、Inbox 积压 15 个待处理文件

### 2026-08-04（compile 先超时后手动补跑，最终全绿）
- **第一轮**（03:00 自动触发）：compile 超时（300s），其余 6 步全绿
  - wiki_grow：概念 485（↑181），已链接 472，孤儿 242
  - 健康自检：笔记 5141 · 断链 2441 · 孤儿 2505 · 缺 FM 355
  - 概念补全：10 篇；phase4 4/4；homepage 5324 chars
  - git：提交 564 文件，push 首次 non-fast-forward，pull 后重推成功
- **第二轮**（手动补跑 wiki_compiler）：处理 734 篇积压文件
  - 来源分布：raw/ 23 + 00_Inbox/ 144 + 20_Processing/ 567
  - 耗时 59m34s，抽取 2595 个概念
  - 1 篇 LLM 超时（2026_05_26_2605_25224.md），优雅跳过
  - git：提交 3352 文件（+66074/-1240），push github main 成功
- **经验**：734 篇积压致 wiki_compiler 远超 300s 超时；后续应考虑提高 self_evolve.py 中 compile 步骤超时或分批处理
- 待办观察：积压已清零，下轮 compile 应恢复正常增量模式

### 2026-08-04（下午迭代修订）
- **self_evolve.py 三处修订**：
  1. compile 超时 300s → 3600s
  2. `git add -A` → 精确目录列表（避免吞入 AI 工具残留）
  3. git push 增加 non-fast-forward 自动恢复
- **camelCase 别名修复**：1258 个概念文件添加 camelCase 别名，修复系统性命名不一致断链
- **wiki_grow 重新运行**：3005 概念，2974 已链接（98.9%），合并 20 个重复概念，耗时 31 分钟
- **断链分类诊断**：other 2241 + GetNote_long 561 + date 42 = 总计 2845
- **待办**：wiki_grow.py O(n²) 性能优化（倒排索引）；health_repair.py 引用旧目录结构需更新

### 2026-08-05（日进化全绿 + FM 批量修复）
- self_evolve.py 全部通过（12m17s）：compile 45 概念 / wiki_grow 3095 概念 99.9% / health 8463 笔记 / phase4 4/4 / homepage / git 3054 文件
- **缺 FM 3701 (44%) 根因诊断**：wiki_compiler.py `write_concept()` 从未写入 frontmatter
- **两步修复**：
  1. wiki_compiler.py 第 332 行：新建概念时 prepend YAML frontmatter（title/type/domain/created/auto）
  2. add_frontmatter_batch.py：一次性补 2779 concepts + 754 articles
- **结果**：缺 FM 3701 → 163（1.7%），3535 文件已推 github main
- 待办：add_frontmatter_batch.py 为一次性脚本，日后可归档删除
- **wiki_grow.py 5x 提速**：
  - 预编译 5988 个正则 + `in` 快速预筛选，避免 900 万次循环内 `re.compile`
  - shared-term O(n²) → 倒排索引；incoming Step4 二次扫描 → Step2-3 同步构建
  - **耗时: 30m53s → 6m21s**；链接覆盖率 98.9% → 99.9%；孤儿 2307 → 1872
- **health_repair.py 目录适配**：EXCLUDE/moc_map/archive 路径/MOC_TEMPLATES/TOP_STUBS 全部更新为当前编号体系
- **self_evolve.py 补充修复**：wiki_grow timeout 300s → 600s；git add `check=True` → 手动检查（部分目录无匹配时不阻断）
- **验证运行**：self_evolve.py 全流水线通过（compile 17 篇/40 概念增量，health 8376 笔记，phase4 4/4，homepage 刷新）
- git 提交 3 次，push github main 成功
- **状态**：积压清零，wiki_grow 6 分钟完成，下轮自动化应恢复正常 2-8 分钟模式

### 2026-08-05（全绿，12 分钟）
- 全部步骤成功：compile / grow / health / grow_concepts / phase4(4子项) / homepage / git
- 总耗时 12m17s（含 wiki_grow ~7min）。
- compile 增量：12 篇文章 → 45 个概念（LLM 抽取 4 个额外概念）
- wiki_grow：概念 3095，已链接 3091（99.9%），孤儿 1780
- 健康自检：笔记 8463 · 真正断链 2195 · 孤儿 2425 · 缺 FM 3701
- 概念补全：10 个占位笔记
- cross_domain_insight：3 篇跨域文章（TCC↔iNEST）
- homepage：5342 chars 刷新成功
- git：提交 3054 文件，push github main 成功
- 观察：import_processor 提示 "New imports detected"（28 个 Inbox 待处理文件），下轮 compile 自动带走。缺 FM 3701 基数较大（~44%），多为 wiki/ 概念自动占位笔记缺少 frontmatter。

### 2026-08-06（全绿，16 分钟）
- 全部步骤成功：compile / grow / health / grow_concepts / phase4(4子项) / homepage / git
- 总耗时 16m08s（含 wiki_grow ~9min，regex 预编译 3205 短语+3227 slug）。
- compile 增量：35 篇文章 → 127 个概念（LLM 抽取 4 个额外概念）
- wiki_grow：概念 3227，已链接 3223（99.9%），孤儿 1743
- 健康自检：笔记 8632 · 真正断链 2145 · 孤儿 2432 · 缺 FM 209（较上周 3701 大幅下降，已<3%）
- 概念补全：10 个占位笔记（长标题 GetNote/Nature/清华 等文献）
- phase4：import_processor raw/ 新文件 0 / Inbox 待处理 27；task_recommender 3 条 LOW；research_evolution 0 更新；cross_domain_insight 1 篇（TCC↔iNEST）
- homepage：5341 chars + data.js 刷新成功
- git：提交 3230 文件，push github main 成功
- 观察：import_processor 提示 "New imports detected"（27 个 Inbox 待处理），下轮 compile 自动带走。缺 FM 已降至 209。

### 2026-08-07（全绿，13 分钟）
- 全部步骤成功：compile / grow / health / grow_concepts / phase4(4子项) / homepage / git
- 总耗时 13m00s（含 wiki_grow ~8min，regex 预编译 3250 短语+3272 slug）。
- compile 增量：10 篇文章 → 35 个概念（LLM 抽取 4 个额外概念）
- wiki_grow：概念 3272，已链接 3268（99.9%），孤儿 1642
- 健康自检：笔记 8692 · 真正断链 2105 · 孤儿 2432 · 缺 FM 219（较上周 209 略升，仍<3%）
- 概念补全：10 个占位笔记（含若干 getnote/长标题文献）
- phase4：import_processor raw/ 新文件 0 / Inbox 待处理 34；task_recommender 3 条 LOW；research_evolution 0 更新；cross_domain_insight 1 篇（TCC↔iNEST）
- homepage：5342 chars + data.js 刷新成功
- git：提交 3202 文件，push github main 成功（knowledge_graph 被 .gitignore 忽略属正常，已优雅跳过）
- 观察：import_processor 提示 "New imports detected"（34 个 Inbox 待处理），下轮 compile 自动带走。
