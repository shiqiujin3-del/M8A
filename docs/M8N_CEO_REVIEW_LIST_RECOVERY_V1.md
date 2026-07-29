# M8N CEO Review List Recovery V1

日期：2026-07-08
状态：代理总经理生成

## 一、当前需要 CEO 处理的事项

### P0：Google OAuth 安全加固

原因：GA4、Google Search Console、Gmail、YouTube 均已完成只读验收，但此前 OAuth Client Secret 曾被复制到对话中。为符合安全规范，需要轮换密钥。

CEO 需要决定：是否今天执行 Google OAuth Client Secret 轮换。

建议：批准执行。

### P0：PR #3 审核

PR：https://github.com/shiqiujin3-del/M8A/pull/3

内容：AI Employee Registry、Access Manager Agent、Automation Agent、Commander Reporting Agent、Department Registry、Employee Dashboard 数据。

CEO 需要决定：是否批准合并 PR #3 到 main。

建议：审核后批准合并。

### P1：总经理通道恢复

问题：CEO 当前无法给总经理线程发送消息，总经理日报未同步最新事实。

CEO 需要决定：是否启用代理总经理机制；是否要求以后所有关键日报写入统一报告索引，而不是只依赖单一线程。

建议：批准代理总经理机制。

### P1：总控 Dashboard 数据更新

问题：Dashboard 数据仍显示旧平台状态，新 WordPress / GA4 / GSC / Gmail / YouTube 验收未完全反映到 Dashboard。

CEO 需要决定：是否批准更新 Dashboard 数据文件，不改首页架构。

建议：批准数据更新，但不重构 UI。

### P2：Gmail Draft Only 工作流

当前状态：Gmail 已只读验收成功，尚未允许发送邮件。

CEO 需要决定：是否进入 Gmail Draft Only 阶段。

建议：等 Google OAuth 密钥轮换完成后再做。

### P2：YouTube Private / Draft Only 工作流

当前状态：YouTube 已只读验收成功，尚未允许上传、发布或修改频道。

CEO 需要决定：是否进入 YouTube Private/Draft Only 阶段。

建议：等 Google OAuth 密钥轮换完成后再做。

## 二、当前禁止动作

在 CEO 再次明确批准前，继续禁止：Gmail 发送邮件、Gmail 读取正文、Gmail 删除邮件、YouTube 上传公开视频、YouTube 发布视频、YouTube 删除视频、修改外部平台权限、保存任何明文密钥到报告或 Git。

## 三、推荐今天唯一优先动作

先恢复治理链路：批准代理总经理接管，审核 PR #3，完成 Google OAuth 密钥轮换计划。

不要同时开启 Gmail 发送、YouTube 上传或新的外部平台写入动作。
