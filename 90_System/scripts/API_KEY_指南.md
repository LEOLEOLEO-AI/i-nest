---
provenance: external
---

﻿# API Key 申请指南

## 1. Web of Science API (Clarivate)

### 申请步骤
1. 打开 https://developer.clarivate.com/
2. 点右上角 "Sign Up" → 用 @tju.edu.cn 邮箱注册
3. 登录后 → "My Apps" → "Create Application"
4. 选择 "Web of Science API" → Starter 或 Expanded
5. 勾选同意条款 → 提交
6. 邮箱会收到 API Key

### 天大优势
- 天大已订阅 WoS → 可直接用 Expanded API（比免费版数据多）
- API Key 形如: `abc123def456...`
- 日限额: ~50,000 次调用（学术订阅）

---

## 2. IEEE Xplore API

### 申请步骤
1. 打开 https://developer.ieee.org/
2. 点 "Register" → 填 @tju.edu.cn 邮箱
3. 验证邮箱 → 登录
4. "My Apps" → "Create New App"
5. 获取 API Key

### 天大优势
- 通过天大 VPN/IP 访问可自动获得全文权限
- API Key 形如: `xyz789...`
- 日限额: ~200 次（免费层）

---

## 拿到 Key 后的操作

把两个 Key 填入环境变量即可，集成代码已写好：

```powershell
[System.Environment]::SetEnvironmentVariable("WOS_API_KEY", "your-wos-key", "User")
[System.Environment]::SetEnvironmentVariable("IEEE_API_KEY", "your-ieee-key", "User")
```

然后运行:
```powershell
python openalex_crawler.py --with-wos --with-ieee
```
