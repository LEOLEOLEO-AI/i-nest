@echo off 
chcp 65001 >nul 2>&1 
setlocal enabledelayedexpansion 

:: ========== 配置区（直接用你的仓库） ========== 
set "GITEE_REPO=git@gitee.com:iBrainNest/i-nest.git" 
set "VAULT_DIR=%cd%" 
set "REMOTE_NAME=origin" 
set "BRANCH=main" 
:: =============================================== 

echo [1/6] 克隆/初始化仓库... 
if not exist .git ( 
    git clone %GITEE_REPO% . 
) else ( 
    git remote add %REMOTE_NAME% %GITEE_REPO% 2>nul 
) 

echo [2/6] 创建目录结构... 
mkdir "00-索引" "01-专利" "02-指南" "03-设计" "04-测试" "assets" 2>nul 

echo [3/6] 安装依赖（markitdown）... 
pip install markitdown 

echo [4/6] 批量转换 Word/PDF → Markdown... 
markitdown "01-专利\*.docx" -o "01-专利\" --format markdown 
markitdown "02-指南\*.pdf" -o "02-指南\" --extract-images --image-dir ./assets 

echo [5/6] 生成索引文档... 
:: 指标基线表 
echo # 指标基线表 > "00-索引\指标基线表.md" 
echo. >> "00-索引\指标基线表.md" 
echo ## 1. 文档质量基线 >> "00-索引\指标基线表.md" 
echo ^| 指标 ^| 基线值 ^| 说明 ^| >> "00-索引\指标基线表.md" 
echo ^|------^|--------^|------^| >> "00-索引\指标基线表.md" 
echo ^| 双向链接覆盖率 ^| ≥90% ^| 核心文档间互链比例 ^| >> "00-索引\指标基线表.md" 

:: 文档依赖图 
echo # 文档依赖图（核心文档） > "00-索引\文档依赖图.md" 
echo. >> "00-索引\文档依赖图.md" 
echo ```mermaid >> "00-索引\文档依赖图.md" 
echo graph TD >> "00-索引\文档依赖图.md" 
echo     A[核心技术指南.md] --^> B[专利-正交原语集与拓扑融合变换.md] >> "00-索引\文档依赖图.md" 
echo ``` >> "00-索引\文档依赖图.md" 

:: 术语对照表 
echo # 术语对照表 > "00-索引\术语对照表.md" 
echo. >> "00-索引\术语对照表.md" 
echo ## 正交原语 >> "00-索引\术语对照表.md" 
echo - 定义：[[专利-正交原语集与拓扑融合变换]] 提出的基础计算单元 >> "00-索引\术语对照表.md" 

echo [6/6] Git 提交并推送到 Gitee... 
git add . 
git commit -m "feat: 知识迁移完成 - 转换+索引+双向链接" 
git push -u %REMOTE_NAME% %BRANCH% 

echo ✅ 全部完成！ 
pause