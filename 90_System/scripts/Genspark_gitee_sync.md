# Genspark 同步 Gitee 指令

## 触发词
当对话中出现 **"同步gitee"** / **"sync gitee"** / **"推送到gitee"** 时，执行本协议。

## 仓库信息
- **地址**: `https://gitee.com/iBrainNest/i-nest.git`
- **分支**: `main`
- **本地路径**: `~/i-nest-sync/` （首次使用需 clone）

## 同步协议 (Pull-First → 提交 → Push)

### Step 1: 准备
```bash
cd ~/i-nest-sync
# 如果还没 clone
if [ ! -d .git ]; then
    git clone https://gitee.com/iBrainNest/i-nest.git .
fi
```

### Step 2: 拉取远程更新
```bash
git fetch origin main
BEHIND=$(git rev-list --count HEAD..origin/main)
if [ "$BEHIND" -gt 0 ]; then
    echo "远程有 $BEHIND 个新提交，拉取中..."
    git pull origin main --no-rebase
fi
```

### Step 3: 检测变更
```bash
git status --porcelain
```

### Step 4: 提交并推送
```bash
git add -A
git commit -m "sync: genspark - $(date '+%Y-%m-%d %H:%M')"
git push origin main
```

### Step 5: 报告
输出：远程拉取数 + 本地上传文件数 + 提交哈希

## 目录对应关系（Genspark 产出的内容应放在）
| 内容类型 | Gitee 目录 |
|---------|-----------|
| 论文草稿/文献综述 | `papers/iNEST/` |
| 专利撰写 | `iNEST_3_专利撰写/` |
| 仿真代码 | `iNEST_4_工程开发/`, `_archive_02_Zettelkasten/` |
| 仿真结果数据 | `simulation/data/` |
| 知识库条目 | `03_Topics/`, `knowledge_graph/` |
| 灵感/创意 | `iNEST_灵感池/`, `00_Inbox/` |

## 冲突处理
- 拉取冲突时：保留远程版本，本地修改以 `.genspark_backup` 后缀保存
- 绝不使用 `--force` 推送
