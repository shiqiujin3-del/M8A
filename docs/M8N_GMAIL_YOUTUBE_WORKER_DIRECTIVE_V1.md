# M8N Gmail / YouTube 工作指令 V1

状态：已下达

负责人：流程 Codex / Access Manager Agent / Automation Agent

## 任务

负责 Gmail 与 YouTube 接入授权。

## 执行路线

CEO / Commander -> AI 员工 -> n8n -> Google OAuth / YouTube API / Gmail API。

## Gmail

允许：

1. 准备 n8n Gmail Credential。
2. 打开 Google 授权入口让 CEO 授权。
3. 验证 Credential Test。
4. 记录授权状态。

禁止：

1. 群发邮件。
2. 读取无关私人邮件正文。
3. 发送外部邮件。
4. 删除邮件。
5. 保存明文 token、client secret 或密码。

## YouTube

允许：

1. 准备 n8n YouTube Credential。
2. 打开 YouTube 授权入口让 CEO 授权。
3. 验证 Credential Test。
4. 读取频道基本信息用于连接验收。
5. 记录授权状态。

禁止：

1. 上传视频。
2. 发布视频。
3. 删除视频。
4. 修改频道设置。
5. 保存明文 token、client secret 或密码。

## 输出

1. `docs/M8N_GMAIL_AUTHORIZATION_V1_REPORT.md`
2. `docs/M8N_YOUTUBE_AUTHORIZATION_V1_REPORT.md`
3. 更新 `apps/commander/employees/registry/credential_registry.json`

## 停止条件

完成连接验收或遇到 OAuth Client / 权限配置阻塞后立即停止并报告。


## 追加发现

当前 n8n 已存在 Gmail 凭证：

```text
Name: Gmail account
Type: gmailOAuth2
ID: phhmEVWx1Jh5Gssf
```

流程 Codex 不要重复创建 Gmail 凭证。先验收现有凭证是否可用；只有现有凭证失效时，才打开重新授权入口。

当前未发现 YouTube 凭证，需要按 YouTube 授权流程处理。
