# M8N Access Manager Agent V1 报告

## 状态

```text
completed
```

## 目标

建立专门管理账号、凭证位置和权限状态的 AI 员工。

该员工只记录账号和授权状态，不记录明文密码、token、Application Password 或 OAuth Secret。

## 新增员工

```text
Access Manager Agent
```

所属部门：

```text
运营部门
```

## 新增文件

```text
apps/commander/employees/profiles/access_manager_agent.json
docs/M8N_ACCESS_MANAGER_AGENT_V1_REPORT.md
```

本地存在 `apps/commander/employees/registry/credential_registry.json` 用于记录凭证位置与授权状态。

安全说明：

```text
credential_registry.json 被 .gitignore 的 *credential* 规则拦截。
本次 PR 不使用 git add -f 强制加入。
该文件保持本地治理状态，不进入 GitHub。
如未来需要提交，应改为 credential registry template，并确保不包含任何真实凭证。
```

## 已登记平台

```text
GitHub
WordPress
n8n
Gmail
YouTube
Google Search Console
GA4
Coze
```

## 安全原则

```text
不保存明文密码。
不保存 API Token。
不保存 Application Password。
不保存 OAuth Client Secret。
只保存凭证所在位置、账号名、权限范围、授权状态、允许动作和禁止动作。
```

## 当前最重要账号状态

GitHub：

```text
账号：shiqiujin3-del
状态：已完成只读身份验证
凭证位置：GitHub CLI local keyring
禁止：push / remote add / repo create / PR create，除非 CEO 单独批准
```

WordPress：

```text
账号：admin
状态：Draft Only 已验证
凭证位置：n8n Credential: M8A WordPress Reserved
禁止：publish / delete / update existing published post
```

n8n：

```text
状态：本地执行层已接入
用途：外部平台唯一正式执行路线
禁止：启用未批准 workflow / 发送 / 发布 / 删除
```

## 验收

需要校验：

```text
python3 -m json.tool apps/commander/employees/profiles/access_manager_agent.json
本地校验 credential_registry.json，但不提交该文件。
```

## 下一步建议

把 Access Manager Agent 接入 Commander Console，让 CEO 能看到：

```text
哪些账号已授权
哪些账号未授权
哪些平台只读
哪些平台只能草稿
哪些动作被禁止
```
