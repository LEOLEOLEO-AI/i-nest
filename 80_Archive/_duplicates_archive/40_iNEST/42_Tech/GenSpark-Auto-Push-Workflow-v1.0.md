---
provenance: external
---

# GenSpark 自动化推送规范 v1.0

## 【核心规则】

**GenSpark 中生成的所有产出必须支持自动推送到 GitHub**

---

## 【产出分类与目录映射】

### 📊 程序输出和验证结果

| 产出类型 | 验证标准 | 目标目录 | 推送规则 |
|---------|---------|---------|---------|
| 诊断报告 | ✅ 通过 | 50_Output/Diagnosis/ | 自动 |
| 论文 | ✅ 通过 | 50_Output/Papers/ | 自动 |
| 研究报告 | ✅ 通过 | 50_Output/Reports/ | 自动 |
| 仿真代码 | ✅ 单测通过 | 35_Simulation/ | 自动 |
| 理论文档 | ✅ 同行审核 | 30_TCC/31_Theory/ | 自动 |
| iNEST 成果 | ✅ 通过 | 40_iNEST/41_Theory/ | 自动 |

### 🚫 不推送的产出

```
❌ 临时调试文件（.log, .tmp, .bak）
❌ 未验证的中间结果
❌ 私密信息（密钥、个人数据等）
❌ 第三方版权内容
```

---

## 【GenSpark 工作流规范】

### 阶段 1：代码编写与测试

```bash
# GenSpark 本地编写
~/i-nest/35_Simulation/experiment_v31.py

# 运行测试
python experiment_v31.py --test
# ✅ 所有单测通过
```

### 阶段 2：结果验证

```bash
# 验证输出
python experiment_v31.py --validate

# 验证包括：
  ✅ 输出文件大小
  ✅ 数据完整性
  ✅ 统计指标有效
  ✅ 与预期基准对比
```

### 阶段 3：自动分类

```bash
# 生成的报告自动分类
output_report.md
  ↓
如果内容类型 = "诊断" → 50_Output/Diagnosis/
如果内容类型 = "论文"   → 50_Output/Papers/
如果内容类型 = "报告"   → 50_Output/Reports/
```

### 阶段 4：自动推送

```bash
# 触发条件
验证通过 ✅ → 自动提交 + 推送

# 执行
git add <classified_files>
git commit -m "自动: 已验证的<类型>输出 ($(date +%Y-%m-%d_%H:%M))"
git push github master:main
git push origin master
```

### 阶段 5：强制验证

```bash
# 推送后必须验证
git ls-tree -r github/main | grep "<filename>"
✅ 文件在 GitHub 存在
✅ 大小/内容一致
✅ 报告成功
```

---

## 【自动推送脚本】

### 创建 `genspark_auto_push.sh`

```bash
#!/bin/bash
set -e

# GenSpark 自动推送脚本 v1.0
# 使用方法：./genspark_auto_push.sh <文件类型> <文件路径>

if [ $# -lt 2 ]; then
    echo "用法: $0 <类型> <文件路径>"
    echo "类型: diagnosis|paper|report|code|theory"
    exit 1
fi

FILE_TYPE=$1
FILE_PATH=$2
REPO_DIR=~/i-nest

# 验证文件存在
if [ ! -f "$FILE_PATH" ]; then
    echo "❌ 文件不存在: $FILE_PATH"
    exit 1
fi

echo "【自动推送流程】"
echo "================================"

# 1. 目录映射
case $FILE_TYPE in
    diagnosis)
        TARGET_DIR="$REPO_DIR/50_Output/Diagnosis/"
        ;;
    paper)
        TARGET_DIR="$REPO_DIR/50_Output/Papers/"
        ;;
    report)
        TARGET_DIR="$REPO_DIR/50_Output/Reports/"
        ;;
    code)
        TARGET_DIR="$REPO_DIR/35_Simulation/"
        ;;
    theory)
        TARGET_DIR="$REPO_DIR/30_TCC/31_Theory/"
        ;;
    *)
        echo "❌ 未知类型: $FILE_TYPE"
        exit 1
        ;;
esac

echo "1️⃣ 目标目录: $TARGET_DIR"

# 2. 复制文件
mkdir -p "$TARGET_DIR"
cp "$FILE_PATH" "$TARGET_DIR"
TARGET_FILE="$TARGET_DIR/$(basename $FILE_PATH)"
echo "✅ 文件已复制到: $TARGET_FILE"

# 3. Git 添加和提交
cd "$REPO_DIR"
git add "$TARGET_FILE"
git commit -m "自动: 已验证的 $FILE_TYPE 输出 - $(basename $FILE_PATH) ($(date +%Y-%m-%d_%H:%M))"
echo "✅ Git 提交成功"

# 4. 推送
echo ""
echo "2️⃣ 推送到 GitHub..."
git push github master:main

echo ""
echo "3️⃣ 推送到 Gitee..."
git push origin master

# 5. 验证
echo ""
echo "【强制验证】"
FILENAME=$(basename "$TARGET_FILE")
TARGET_REL_PATH="${TARGET_FILE#$REPO_DIR/}"

# 验证 GitHub
if git ls-tree -r github/main | grep -q "$TARGET_REL_PATH"; then
    GITHUB_SIZE=$(git show github/main:"$TARGET_REL_PATH" 2>/dev/null | wc -c)
    LOCAL_SIZE=$(wc -c < "$TARGET_FILE")
    
    if [ "$GITHUB_SIZE" -eq "$LOCAL_SIZE" ]; then
        echo "✅ GitHub: 文件已同步 ($GITHUB_SIZE 字节)"
    else
        echo "❌ GitHub: 文件大小不匹配 (本地: $LOCAL_SIZE, GitHub: $GITHUB_SIZE)"
        exit 1
    fi
else
    echo "❌ GitHub: 文件未找到"
    exit 1
fi

# 验证 Gitee
if git ls-tree -r origin/master | grep -q "$TARGET_REL_PATH"; then
    GITEE_SIZE=$(git show origin/master:"$TARGET_REL_PATH" 2>/dev/null | wc -c)
    
    if [ "$GITEE_SIZE" -eq "$LOCAL_SIZE" ]; then
        echo "✅ Gitee: 文件已同步 ($GITEE_SIZE 字节)"
    else
        echo "❌ Gitee: 文件大小不匹配"
        exit 1
    fi
else
    echo "❌ Gitee: 文件未找到"
    exit 1
fi

# 6. 最终报告
echo ""
echo "================================"
echo "✅ 自动推送完成"
echo "================================"
echo ""
echo "📍 在线地址："
echo "GitHub: https://github.com/LEOLEOLEO-AI/i-nest/blob/main/$TARGET_REL_PATH"
echo "Gitee: https://gitee.com/iBrainNest/i-nest/blob/master/$TARGET_REL_PATH"
```

### 使用方法

```bash
# 使脚本可执行
chmod +x ~/genspark_auto_push.sh

# 示例 1：推送诊断报告
~/genspark_auto_push.sh diagnosis ~/experiment_results/diagnosis_2026-06-23.md

# 示例 2：推送仿真代码
~/genspark_auto_push.sh code ~/sdi_sim/experiment_v31.py

# 示例 3：推送论文
~/genspark_auto_push.sh paper ~/my_research/paper_draft.md
```

---

## 【集成到 GenSpark 工作流】

### 在 GenSpark 中的使用方式

**方式 1：手动触发**
```bash
# 生成报告后
python generate_report.py → output/report.md

# 手动推送
genspark_auto_push.sh report output/report.md
# ✅ 自动验证 + 推送到 GitHub
```

**方式 2：程序自动触发**
```python
# GenSpark 程序中
import subprocess

# 生成报告
report_file = generate_diagnosis()

# 自动推送
subprocess.run([
    'genspark_auto_push.sh',
    'diagnosis',
    report_file
])
# ✅ 自动完成整个流程
```

**方式 3：Cron 定时推送**
```bash
# 定时脚本
0 * * * * ~/genspark_auto_push.sh diagnosis $(ls -t ~/output/diagnosis_*.md | head -1)
# 每小时自动推送最新的诊断报告
```

---

## 【质量保证】

### 推送前检查清单

```bash
# 自动检查列表
☑️ 文件大小 > 0
☑️ 文件内容不为空
☑️ 文件格式正确（.md, .py 等）
☑️ 无二进制或加密内容
☑️ 无敏感信息（API key, 密码等）
☑️ 与现有文件无重名冲突
```

### 验证失败处理

```bash
如果验证失败：
  1. 保存文件到 ~/failed_pushes/
  2. 生成错误报告
  3. 发送告警到管理员
  4. 不隐瞒错误，清晰报告问题
```

---

## 【文件命名规范】

为了便于追踪和组织，所有推送的文件应遵循：

```
诊断报告：    YYYY-MM-DD_<topic>.md
论文：       <author>_<title>_vX.md
仿真代码：    exp_<number>_<description>.py
研究报告：    report_<year>_<quarter>_<topic>.md
理论文档：    theory_<concept>_<version>.md
```

### 示例

```
✅ 2026-06-23_SOC_analysis.md
✅ liu_neural_complexity_v3.md
✅ exp_31_hemibrain_simulation.py
✅ report_2026_Q2_iNEST_progress.md
✅ theory_TCC_topology_v2.0.md
```

---

## 【监控与告警】

### 定期检查

```bash
# 每周检查同步状态
cron: 0 0 * * 0 ~/check_github_sync.sh

# 检查内容：
  ✅ GitHub 和 Gitee 的同步延迟
  ✅ 推送失败的文件
  ✅ 未同步的变更
```

### 告警机制

```
推送失败 → 生成 ERROR.log
3 次失败 → 管理员通知
持续失败 → 暂停自动推送，转为手动审核
```

---

## 【版本和迭代】

| 版本 | 日期 | 内容 |
|------|------|------|
| v1.0 | 2026-06-23 | 初版规范 + 自动推送脚本 |
| v1.1 | TBD | 支持增量推送优化 |
| v1.2 | TBD | 集成 CI/CD 流程 |
| v2.0 | TBD | 完整自动化工作流 |

---

**规范版本**：v1.0
**生效时间**：2026-06-23 09:23 EDT
**所有 GenSpark 输出必须支持本规范的推送流程**

