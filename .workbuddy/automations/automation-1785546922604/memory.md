# 知识库每日自进化 — 执行记忆

## 运行方式（重要）
- 工作目录：`D:/obsidian/vault`
- 解释器：**必须用系统 Python 3.10**
  `C:/Users/LEO/AppData/Local/Programs/Python/Python310/python.exe 90_System/scripts/self_evolve.py`
  （bash 中无 `python3`/`python` 命令；脚本内部用 `sys.executable` 派生子进程，解释器需一致）
- 典型耗时约 1-2 分钟，远低于脚本内置超时上限，无需后台长等。
- 脚本自带超时与失败隔离，单步失败不影响其余；**不要重试或做破坏性操作**。

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
