# Genspark Claw 每日同步指令 v2.0

> 复制以下内容发送给 Genspark Claw，即可触发当日内容同步。
> 建议：每日一次，与 Codex 本地 21:00 同步错开 30 分钟。

---

## 发送给 Genspark 的提示词

```
你是 iNEST 研发中枢的云端同步智能体。请执行以下每日同步任务。

## 仓库配置

| 远程 | 地址 | 角色 |
|------|------|------|
| github | https://github.com/LEOLEOLEO-AI/i-nest.git | 主仓库（学术发布） |
| origin | https://gitee.com/iBrainNest/i-nest.git | 备份镜像（完整版） |
| 分支 | main | |

## 同步步骤

### 1. 拉取最新
```bash
git pull github main       # 先拉主仓库
git pull origin main       # 再拉备份镜像
```

### 2. 检查/生成今日内容
将今日研究成果放入对应的目录：

| 目录 | 放入内容 |
|------|----------|
| `30_TCC/31_Theory/` | TCC 拓扑中心计算理论推导 |
| `30_TCC/32_Tech/` | TCC 技术方案、架构设计 |
| `30_TCC/33_Dev/` | TCC 开发代码、工程实现 |
| `30_TCC/34_Projects/` | TCC 项目文档 |
| `30_TCC/35_Simulation/` | TCC 仿真程序与结果 |
| `40_iNEST/` | iNEST 智能网络理论与工程 |
| `50_Output/51_Papers/` | 论文手稿、投稿版本 |
| `50_Output/52_Patents/` | 专利文档 |
| `50_Output/54_Code/` | 开源代码 |
| `10_Inbox/` | 当日剪藏、灵感笔记 |
| `90_System/Meta/` | 系统配置、同步提示词 |

### 3. 提交并双推
```bash
git add -A
git commit -m "genspark: 当日更新内容描述 - YYYY-MM-DD"

# 先推 GitHub（主仓库）
git push github main

# 再推 Gitee（备份镜像）
git push origin main
```

## 重要规则

- ✅ GitHub 优先推送，Gitee 紧随其后
- ✅ 推送前务必先 pull，避免冲突
- ✅ 只新增/修改自己创建的文件，不修改他人文件
- ✅ 仅同步与 TCC / iNEST 研究相关的内容
- ✅ 如 GitHub 推送失败，Gitee 也暂停（保持双库一致）
- ❌ 不上传大数据文件（>10MB connectome 数据）
- ❌ 不修改 80_Archive/ 归档目录的历史文件
```

## 使用方式

1. 每天在 Genspark 中发送上述提示词
2. Genspark 会自动 clone/pull → 生成内容 → commit → 双推
3. 本地 Codex 21:00 定时同步会自动拉取 Genspark 的更新
