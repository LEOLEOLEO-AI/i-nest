# 2026-06-23 08:04 EDT - GitHub SSH 公钥设置失败诊断 & 修复

## 【错误信息】

**用户报告**：
```
Key is invalid. You must supply a key in OpenSSH public key format
```

**时间**：2026-06-23 08:04 EDT
**位置**：GitHub SSH and GPG keys 页面

---

## 【原因诊断】

### ✅ 公钥本身格式正确
```bash
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINOF0fsWWK6BbWSiI369OcDio9amh4L80tE1RDkhaXgZ qinrangliu@gmail.com
```

**验证**：`ssh-ed25519` 开头 + Base64 编码 + 注释 = 标准 OpenSSH 格式 ✅

### ❌ 粘贴过程可能引入的错误
1. 包含 Markdown 代码块 (```) 
2. 前后有空格或制表符
3. 中间被换行符分割
4. 包含隐形字符

---

## 【正确的公钥（纯格式，一行）】

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINOF0fsWWK6BbWSiI369OcDio9amh4L80tE1RDkhaXgZ qinrangliu@gmail.com
```

**复制规则**：
- ✅ 从 `ssh-ed25519` 开始，到 `qinrangliu@gmail.com` 结束
- ✅ 不要包含三引号或代码块标记
- ✅ 不要有换行符
- ✅ 不要有多余空格

---

## 【GitHub SSH 密钥设置（详细步骤）】

### 步骤 1：登录 GitHub
```
URL：https://github.com/login
账户：LEOLEOLEO-AI
```

### 步骤 2：进入 SSH 设置
```
顶部右角 → 用户头像
  → Settings
    → SSH and GPG keys（左侧菜单）
```

### 步骤 3：创建新密钥
```
点击绿色按钮 "New SSH key"
```

### 步骤 4：填写密钥信息

**Title 字段**：
```
i-nest-deploy
```

**Key type 字段**（下拉选择）：
```
Authentication Key (默认)
```

**Key 字段**（粘贴公钥）：
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINOF0fsWWK6BbWSiI369OcDio9amh4L80tE1RDkhaXgZ qinrangliu@gmail.com
```

### 步骤 5：保存
```
点击绿色按钮 "Add SSH key"
```

---

## 【常见粘贴错误及修复】

### ❌ 错误 1：包含代码块标记
```
❌ ```ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINOF0fsWWK6BbWSiI369OcDio9amh4L80tE1RDkhaXgZ qinrangliu@gmail.com```
```

**修复**：删除前后的三引号

### ❌ 错误 2：分成两行
```
❌ ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINOF0fsWWK6BbWSiI369OcDio9amh4L80tE1RDkhaXgZ
qinrangliu@gmail.com
```

**修复**：确保在一行内，无换行

### ❌ 错误 3：前后有空格
```
❌   ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINOF0fsWWK6BbWSiI369OcDio9amh4L80tE1RDkhaXgZ qinrangliu@gmail.com   
```

**修复**：删除前后空格

### ✅ 正确做法
```
✅ 复制整行（从 ssh-ed25519 到 .com）
✅ 直接粘贴，不编辑
✅ 点击 Add SSH key
```

---

## 【验证命令】

密钥添加完成后，在本地执行验证：
```bash
ssh -T git@github.com
```

**预期输出**：
```
Hi LEOLEOLEO-AI! You've successfully authenticated, but GitHub does not provide shell access.
```

如果看到这条消息，说明 SSH 密钥已正确配置 ✅

---

## 【重试推送】

SSH 密钥添加完成后，Genspark 可进行重试推送。

**触发方式**：
```
触发词："推送"
```

**预期结果**：
```
Enumerating objects: ...
Counting objects: ...
master -> main [新建或更新]

✅ 推送成功
```

---

## 【诊断记录】

| 时间 | 事件 | 状态 |
|------|------|------|
| 07:47 | 首次推送尝试 | Gitee ✅，GitHub ❌ |
| 07:55 | 诊断 GitHub 认证问题 | SSH 公钥未授权 |
| 08:04 | 用户报告粘贴错误 | 格式无效 |
| 08:04 | 提供修复方案 | 等待用户重新粘贴 |

---

**状态**：等待用户按正确步骤重新添加 SSH 公钥

