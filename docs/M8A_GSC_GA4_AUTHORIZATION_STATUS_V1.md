# M8A GSC / GA4 接入状态报告 V1

日期：2026-07-07

## 分工状态

当前 Codex 负责：Google Search Console 与 GA4。

流程 Codex 负责：Gmail 与 YouTube。

## 已下达给流程 Codex 的指令

指令文件：`apps/commander/missions/M8N_GMAIL_YOUTUBE_AUTHORIZATION_V1.json`

报告文件：`docs/M8N_GMAIL_YOUTUBE_WORKER_DIRECTIVE_V1.md`

追加发现：n8n 已存在 Gmail 凭证 `Gmail account`，类型 `gmailOAuth2`，ID `phhmEVWx1Jh5Gssf`。流程 Codex 不应重复创建 Gmail 凭证，应先验收现有凭证。

YouTube 当前未发现凭证，需要单独授权。

## GSC / GA4 当前状态

已确认 n8n 中没有现成的 GSC / GA4 凭证。

已打开 n8n 创建 Google Analytics OAuth2 API 凭证页面。

当前页面要求填写：

1. Client ID
2. Client Secret

这不是填写邮箱。

## OAuth Redirect URL

```text
http://localhost:5678/rest/oauth2-credential/callback
```

Google Cloud OAuth Client 必须把上面这个地址加入 Authorized redirect URIs。

## 当前阻塞

GSC / GA4 授权需要 Google Cloud OAuth Client ID 与 Client Secret。

如果继续使用占位符 `Client ID`，会再次出现：

```text
invalid_client
The OAuth client was not found
```

## 允许动作

1. CEO 在 n8n 页面直接填写 Client ID / Client Secret。
2. CEO 授权 Google OAuth。
3. Codex 验证 GA4 只读连接。
4. Codex 为 GSC 建立 HTTP Request + Google OAuth2 只读流程。

## 禁止动作

1. 不保存 Client Secret 到报告。
2. 不读取无关 Google 账号数据。
3. 不修改 GA4 / GSC 设置。
4. 不删除、发布、上传任何内容。

## 下一步

等待 CEO 在 n8n 当前页面填写 Google OAuth Client ID / Client Secret，并完成 Google 授权。
