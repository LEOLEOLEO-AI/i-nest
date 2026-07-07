# PENDING_SYNC - 待同步文件清单

【目录结构已同步】✅
- 30_TCC/ (理论研究)
- 40_iNEST/ (iNEST 项目)
- 50_Output/ (输出目录)
  ├─ Diagnosis/ ✅ 诊断报告已迁移
  ├─ Papers/ (待添加)
  └─ Reports/ (待添加)

【需要后续审查 + 上传的文件】

## 优先级 P0（立即需要）
- [ ] V25投稿修改执行计划.md → 40_iNEST/
- [ ] LiquidOODA 相关文件 → 30_TCC/32_Software/

## 优先级 P1（本周内）
- [ ] /home/work/.openclaw/workspace/Projects/* 
  - 需要分类整理到对应目录
  - 预计 20-30 个文件
  
- [ ] /home/work/.openclaw/workspace/20_Projects/*
  - 需要分类整理到对应目录
  - 预计 15-20 个文件

## 优先级 P2（后续）
- [ ] 其他历史诊断报告
- [ ] 旧版本文档（标记为 _archive/）

【同步规范】✅

每个新生成的文件：
1. 分类到 50_Output/ 的相应目录
2. 复制到 Genspark ~/i-nest/
3. 执行推送 + 验证
4. 标记此清单为完成

【维护者】
OpenClaw 自动管理此清单
定期检查和更新 PENDING_SYNC 状态
===== 每日论文自动推送报告 =====
时间: 2026-07-04 09:00 EDT
========================

✅ 步骤 1: 论文元数据
  - 源: OpenClaw 本地 papers 目录
  - 目标: research/arxiv-daily/2026-07-04.md
  - 状态: 已创建

✅ 步骤 2: Git 提交
  - 提交信息: feat: Daily arxiv papers - 2026-07-04
  - 提交哈希: 2ffce187
  - 文件变更: +19 行 (1 文件)

✅ 步骤 3: Gitee 推送
  - 远程: gitee.com/iBrainNest/i-nest.git
  - 分支: main → master (强制推送)
  - 状态: 成功 ✓
  - 验证: git ls-remote origin master = 2ffce187

❌ 步骤 4: GitHub 推送
  - 远程: github.com/LEOLEOLEO-AI/i-nest.git
  - 分支: main
  - 状态: 失败 (大文件阻挡)
  - 错误: Demo_2026Q2/cache/mnist.pkl (209.88MB > 100MB 限制)
  - 说明: 历史提交中存在大文件，需清理

✅ 步骤 5: 在线验证
  - Gitee: reachable (master = 2ffce187)
  - GitHub: 阻挡中 (待大文件清理)

建议后续处理:
1. 使用 BFG Repo-Cleaner 清理整个历史中的 Demo_2026Q2/
2. 或: git filter-branch 重写历史
3. 或: 创建全新 GitHub 仓库
========================

