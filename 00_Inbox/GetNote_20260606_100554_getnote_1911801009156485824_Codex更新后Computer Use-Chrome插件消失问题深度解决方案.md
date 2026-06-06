---
title: getnote_1911801009156485824_Codex更新后Computer Use-Chrome插件消失问题深度解决方案
tags:
  - inest
  - research
  - tech-clip
date: 2026-06-06 10:05
source: GetNotes
score: 6
---

## Original Note

---
note_id: 1911801009156485824
title: "Codex更新后Computer Use/Chrome插件消失问题深度解决方案"
type: link
created: 2026-06-04 00:17:18
source: 得到大脑
---

# Codex更新后Computer Use/Chrome插件消失问题深度解决方案

### **🔍 问题概述**

**适用人群**：微软商店安装 Codex 的用户  
**核心问题**：更新后 **Computer Use**（电脑操控）和 **Chrome**（谷歌浏览器操控）插件消失  

### **💻 核心解决方案（结论先行）**

**推荐命令修复**：  
复制以下命令，在**管理员模式PowerShell**中粘贴执行：  
```powershell
powershell -ExecutionPolicy Bypass -Command "$p=Get-AppxPackage 'OpenAI.Codex';$m=Join-Path $p.InstallLocation 'app\\resources\\plugins\\openai-bundled';codex plugin marketplace remove openai-bundled -ErrorAction SilentlyContinue;codex plugin marketplace add $m;Write-Host '✅ 修复完成，请重启 Codex' -ForegroundColor Green"
```
**操作后续**：运行完成后**重启Codex**，通过「设置→电脑操控」即可确认插件恢复。

### **🔌 消失插件功能解析**

#### **🖥️ Computer Use（电脑操控）**
- **核心作用**：赋予Codex直接操控电脑应用程序的能力  
- **具体功能**：  
  - 自动打开微信并发送消息、操作界面  
  - 管理文件资源管理器  
  - 控制任意桌面软件  
  - 执行重复性鼠标键盘操作  
- **通俗理解**：Codex的"手"，使其从代码生成工具升级为电脑操作助手  

#### **🌐 Chrome（谷歌浏览器操控）**
- **核心作用**：授权Codex控制Chrome浏览器  
- **具体功能**：  
  - 自动打开网页、截图及读取页面内容  
  - 填充表单与执行搜索  
  - 实现网页自动化操作  
- **通俗理解**：Codex的"眼睛"，扩展其在浏览器环境中的交互能力  

#### **插件组合价值**

| 配置类型 | 能力范围 |
| :------- | :------- |
| **仅Codex** | 代码生成（无执行能力） |
| **Codex+双插件** | 代码生成+电脑操控+浏览器操控（完整智能助手） |

### **🔎 问题根源分析**

**本质**：Codex更新机制的**缓存同步bug**，非用户操作或设备问题  

**技术原理**：  
1. 微软商店更新后，Codex新版本文件被安装至新路径  
2. 插件市场缓存文件（**marketplace.json**）未同步刷新  
3. Codex无法读取正确插件索引，导致设置界面不显示插件  

**类比说明**：如同搬家后快递员仍使用旧地址，导致无法送达  

**常见误解澄清**：  
"移到D盘再移回C盘"的解决方案仅对C盘安装用户有效，其原理是触发系统重新注册应用以刷新缓存，非普适性方法。

### **🛠️ 三种修复方法详解**

#### **方法一：一行命令修复（推荐 ⭐）**

**操作步骤**：  
1. 打开管理员PowerShell（Win+X → Windows PowerShell (管理员)）  
2. 粘贴并执行前文提供的核心修复命令  
3. 重启Codex完成修复  

#### **方法二：手动操作修复**

| 步骤 | 操作详情 |
| :--- | :--- |
| **Step 1** | 获取安装路径：在PowerShell运行<br>`Get-AppxPackage -Name "OpenAI.Codex" | Select-Object InstallLocation` |
| **Step 2** | 确认插件目录：检查路径下是否存在<br>`app\resources\plugins\openai-bundled\.agents\plugins\marketplace.json` |
| **Step 3** | 移除旧配置：执行<br>`codex plugin marketplace remove openai-bundled` |
| **Step 4** | 添加新路径：执行（替换为实际路径）<br>`codex plugin marketplace add "C:\Program Files\WindowsApps\OpenAI.Codex_版本号_x64__xxxxx\app\resources\plugins\openai-bundled"` |
| **Step 5** | 重启Codex |

#### **方法三：脚本文件修复**
1. 下载 `fix-codex-plugins.ps1` 脚本  
2. 右键选择「使用PowerShell运行」  
3. 按提示完成操作  

**补充操作**：若重启后插件仍未显示，可手动安装：  
```powershell
codex plugin add computer-use@openai-bundled  
codex plugin add chrome@openai-bundled
```
### **❓ 常见问题解答**

| 问题 | 解决方案 |
| :--- | :--- |
| **Q：非微软商店版（npm/GitHub安装）适用吗？** | 仅适用于微软商店版，其他版本建议重新安装 |
| **Q：提示"codex不是可识别的命令"** | 需使用完整路径运行，默认路径：<br>`%LOCALAPPDATA%\OpenAI\Codex\bin\xxx\codex.exe` |
| **Q：插件恢复但无法使用** | 检查配置文件：<br>`notepad $env:USERPROFILE\.codex\config.toml`<br>确保 `[features]` 下 `js_repl = true` |

### **📝 补充细节**
- **bug本质**：更新后安装路径变化与缓存不同步的矛盾  
- **配置文件关键项**：`js_repl = true` 是插件功能启用的必要条件  
- **脚本版本**：当前方案基于修复脚本 **v1.0**（最后更新：2026-06-03）

---
*得到大脑 | 2026-06-06 09:52*


---

## Related Notes

[[iNEST-MOC]]
