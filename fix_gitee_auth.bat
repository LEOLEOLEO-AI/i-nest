@echo off 
chcp 65001 >nul 2>&1
title Gitee 凭据修复（Obsidian） 
 
:: ---------- 请在这里填你的信息 ---------- 
set "GIT_USER=iBrainNest" 
set "GIT_EMAIL=leo@csivo.com" 
set "GIT_REPO=i-nest" 
:: 【注意】密码中的 @ 需要进行 URL 编码写为 %%40，否则在拼接到 URL 时会导致解析错误！
set "NEW_PASS_OR_PAT=Liusansan%%406363" 
:: ----------------------------------------- 
 
echo [1/5] 配置全局用户名/邮箱... 
git config --global user.name "%GIT_USER%" 
git config --global user.email "%GIT_EMAIL%" 
 
echo [2/5] 查看当前远程... 
git remote -v 
 
echo [3/5] 更新远程地址（写入密码/PAT）... 
:: 【注意】移除了原代码中包裹 URL 的反引号 `，因为批处理脚本不支持将其作为字符串定界符
git remote set-url origin https://%GIT_USER%:%NEW_PASS_OR_PAT%@gitee.com/%GIT_USER%/%GIT_REPO%.git
 
echo [4/5] 清除系统旧凭据（避免缓存）... 
git config --global --unset credential.helper 
git config --global credential.helper manager 
 
echo [5/5] 测试连接... 
git ls-remote origin 
if %errorlevel% equ 0 ( 
    echo ✅ 成功！现在去 Obsidian 里 Git: Push 即可。 
) else ( 
    echo ❌ 失败！请检查密码/PAT是否正确、网络是否通。 
) 
