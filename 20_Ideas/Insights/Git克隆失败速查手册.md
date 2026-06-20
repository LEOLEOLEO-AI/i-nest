---
title: Git 克隆失败速查手册
tags:
- brain
- tools
- tutorial
---
刘老师，如果您在电脑上执行 `git clone https://gitee.com/iBrainNest/i-nest.git` 时遇到了红色的报错，千万别急，通常只有以下 3 种最常见的小问题：

### ❌ 错误 1：`fatal: Authentication failed` (认证失败 / 密码错了)
*   **原因**：这是最常见的，您输入的 Gitee 账号或密码不匹配，或者弹出的凭据管理器（Credential Manager）记住了别人的账号。
*   **解决**：
    *   确保账号（手机号或邮箱）和密码输入准确无误。
    *   如果您用的 Windows，去电脑的“控制面板 -> 用户账户 -> 凭据管理器 -> Windows 凭据”，把里面保存的 `gitee.com` 的普通密码删掉重新输一遍。

### ❌ 错误 2：`fatal: repository not found` (找不到仓库)
*   **原因**：仓库名字拼错了，或者您的 Gitee 账号还没有新建这个 `i-nest` 私有仓库。
*   **解决**：
    *   请登录您的 Gitee 网页端（[gitee.com](https://gitee.com/)），点击右上角 `+` 号新建仓库。
    *   仓库名称填 `i-nest`，记得勾选为 **“私有 (Private)”**！然后创建它。

### ❌ 错误 3：`fatal: could not read Username` (弹不出输密码的框)
*   **原因**：您的 Git 版本较旧，或者没有安装图形化的凭证助手。
*   **解决**：在终端里换个更直接的带账号密码的克隆方式（临时用一下，注意保护隐私）：
    `git clone https://您的Gitee用户名:您的Gitee密码@gitee.com/iBrainNest/i-nest.git`

---
### 🎉 如果出现绿色的 `Resolving deltas: 100% (xx/xx), done.`
**恭喜您，克隆成功！** 您本地现在有了一个带有 `.git` 灵魂的 `i-nest` 文件夹。
赶快用 Obsidian 打开它，享受双联星空图谱的震撼吧！

## Related Notes

- [[事件相机 (DVS)、类脑计算 (SNN) 与 FPGA 部署]]
- [[Get笔记×Obsidian 配置与工作流]]
- [[AI-ML — 全景导航 (Map of Content)]]
