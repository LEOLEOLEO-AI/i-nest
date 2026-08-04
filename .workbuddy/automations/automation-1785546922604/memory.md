# 知识库每日自进化 — 执行记忆

## 运行方式（重要）
- 工作目录：`D:/obsidian/vault`
- 解释器：**必须用系统 Python 3.10**
  `C:/Users/LEO/AppData/Local/Programs/Python/Python310/python.exe 90_System/scripts/self_evolve.py`
  （bash 中无 `python3`/`python` 命令；脚本内部用 `sys.executable` 派生子进程，解释器需一致）
- 典型耗时约 2-5 分钟（wiki_compiler 偶有超时 300s，不影响后续步骤）。
- 脚本自带超时与失败隔离，单步失败不影响其余；**不要重试或做破坏性操作**。
- git push 偶发 non-fast-forward（远端有 arxiv-auto 等自动提交）：`git pull github main --no-rebase` 再 push 即可，属标准操作。

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

### 2026-08-04（compile 超时，其余全绿）
- compile：**超时**（wiki_compiler 300s 未返回，可能因 raw/ 积压较大；不影响后续步骤）
- wiki_grow：概念 485（↑181），已链接 472，图谱内孤儿 242
- 健康自检：笔记 5141（↑568）· 断链 2441（↑1107）· 孤儿 2505（↑447）· 缺 FM 355（↑319）
  - 断链增长主要来自 GetNote 长标题文献、S2 论文标题、日记页交叉引用
- 概念补全：10 篇（getnote 智能涌现/晶上自演化/晶圆级神经网络/数字孪生大脑/SDSoW/陆超超访谈/NICE/清华类脑/MIT Chiplet 等）
- phase4：4/4 成功（import_processor/task_recommender/research_evolution/cross_domain_insight）
  - cross_domain 发现 2 篇跨域文章（TCC_iNEST_教材编写规划、iNEST_理论体系系统总结报告）
- homepage：Home.md 生成 5324 chars
- git：提交 564 文件；push 首次失败（non-fast-forward，远端有 arxiv-auto 新提交），pull 后重推成功
- 待办观察：Inbox 积压 18 文件；compile 超时需关注（下轮可能仍有积压）
