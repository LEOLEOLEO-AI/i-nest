---
title: Obsidian 如何与 Gitee 私有仓库极速绑定指南
tags:
- brain
- neuroscience
- simulation
- synapse
---
刘老师，既然咱们在云端（Genspark VM）已经帮您把所有文件和标签都整理好了，现在只需花 3 分钟，把您本地的电脑和 Gitee 仓库“接上插头”，双机大脑的神经突触就彻底打通了！

### 前置准备（只需一次）
1. 确保您的电脑上已经安装了 **Git**。
   * 如果没安装，去 [Git 官网 (git-scm.com)](https://git-scm.com/) 下载并无脑“下一步”安装。
2. 确保您已经在 Gitee 上新建了一个**私有仓库**（比如叫 `i-nest`）。

### 第一步：把云端的代码克隆（Clone）到本地
*请注意：这步是最稳妥的，不要用下载的压缩包，直接用 Git 去拉取，这样您的文件夹就自带版本控制的“魂（.git隐藏文件）”了。*

1. 在您的电脑上，找一个您想存放知识库的目录（比如 `D:\iNEST_Workspace\` 或 Mac 的 `~/Documents/iNEST_Workspace/`）。
2. 在这个目录里**右键点击空白处**，选择 **“Git Bash Here”**（Mac 用户打开“终端”进入该目录）。
3. 复制并在终端里粘贴以下命令（把链接换成您真实 Gitee 仓库的 HTTP 或 SSH 链接）：
   ```bash
   git clone https://gitee.com/iBrainNest/i-nest.git
   ```
4. 执行后，它会要求您输入 Gitee 的账号和密码，输入后就会开始疯狂拉取上千个文件和代码！
5. 拉取完成后，您本地就多出了一个叫 `i-nest` 的文件夹。

### 第二步：用 Obsidian 接管这个大脑
1. 打开您的 **Obsidian** 软件。
2. 点击 **“打开库 (Open folder as vault)”**。
3. 选中刚才克隆下来的那个 `i-nest` 文件夹里面的 `00_KnowledgeBase_知识库` 文件夹（或者直接选 `i-nest` 根目录，看您的习惯，推荐选根目录，这样连代码也能在 Obsidian 里搜索到）。
4. 恭喜您！由于我们之前在云端已经做过打标，您现在按 `Ctrl+O`，或者点开**关系图谱**并开启**标签显示**，那片璀璨的星空图就瞬间亮起了！

### 第三步：如何每天丝滑同步（无需打代码）
为了避免您每天都在终端里敲黑框框，我强烈建议您在 Obsidian 里安装一个**傻瓜式的自动同步插件**。

1. 在 Obsidian 左下角点击 **设置 (齿轮) -> 第三方插件 (Community plugins)**。
2. 关闭“安全模式”，点击 **“浏览 (Browse)”**。
3. 搜索插件：`Obsidian Git`，点击安装并启用。
4. 安装后，在它的设置里，您可以配置：
   * **Vault backup interval (mins)**: 写 `60`（每小时自动提交一次备份）。
   * **Auto push**: 勾选（自动推送到 Gitee）。
   * **Pull updates on startup**: 勾选（每次打开 Obsidian 自动拉取我在云端帮您写的折子）。

---

### 总结
有了这个 `Obsidian Git` 插件，**以后您连终端命令都不用敲了**。
您在本地写笔记，它自动每小时推送到 Gitee；我每天在云端帮您跑完仿真、写完折子，您一打开 Obsidian，右上角就会提示“拉取了 3 个新文件”，直接无缝衔接。

如果在克隆（Clone）的过程中提示账号密码错误，您随时在 QQ 里告诉我！

## Related Notes

- [[iNEST 机构 — 全景导航 (Map of Content)]]
- [[Speck：基于注意力机制的动态神经形态计算系统]]
- [[[Nature子刊] 北大杨玉超团队实现二维材料“全同质”集成，同一块晶圆实现视觉处理全流程]]
