# M8N General Manager Recovery Sync Instructions

状态：ready_to_sync

## 目标

把代理总经理生成的恢复文件写回 M8A 正式总控目录。

## 当前恢复文件

```text
/private/tmp/m8n_general_manager_recovery_v1/M8N_GENERAL_MANAGER_RECOVERY_DAILY_REPORT.md
/private/tmp/m8n_general_manager_recovery_v1/M8N_CEO_REVIEW_LIST_RECOVERY_V1.md
/private/tmp/m8n_general_manager_recovery_v1/M8N_GENERAL_MANAGER_CHANNEL_RECOVERY_REPORT.md
```

## 建议写回位置

```text
/Users/shiqiujing/Documents/M8A/docs/M8N_GENERAL_MANAGER_RECOVERY_DAILY_REPORT.md
/Users/shiqiujing/Documents/M8A/docs/M8N_CEO_REVIEW_LIST_RECOVERY_V1.md
/Users/shiqiujing/Documents/M8A/docs/M8N_GENERAL_MANAGER_CHANNEL_RECOVERY_REPORT.md
```

## 建议同步动作

1. 复制三份恢复报告到 M8A docs。
2. 用恢复日报内容更新或补充：

```text
/Users/shiqiujing/Documents/M8A/docs/M8N_TODAY_GENERAL_MANAGER_REPORT.md
```

3. 用恢复版 CEO Review List 更新或补充：

```text
/Users/shiqiujing/Documents/M8A/docs/M8N_CEO_REVIEW_LIST_V1.md
```

4. 在报告索引中新增记录：

```json
{
  "mission_id": "m8n_general_manager_recovery_v1",
  "mission_name": "M8N General Manager Channel Recovery V1",
  "module": "Governance / Commander Reporting",
  "branch": "local_recovery_pending_sync",
  "commit": "not_committed",
  "report_path": "docs/M8N_GENERAL_MANAGER_CHANNEL_RECOVERY_REPORT.md",
  "status": "completed_as_temp_recovery_package",
  "tests": "Recovery package generated from existing closing and validation reports. No external API, publish, send, upload, merge, or push performed.",
  "ceo_review_status": "waiting",
  "next_action": "Sync recovery package into M8A docs and update dashboard/report index."
}
```

## 安全边界

本恢复包不包含：

- OAuth Client Secret
- Access Token
- Refresh Token
- WordPress Application Password
- API Key
- .env 内容

本恢复包没有执行：

- 外部 API 调用
- 邮件发送
- YouTube 上传
- WordPress 发布
- Git merge
- Git push

## 当前阻塞

当前 Codex 执行环境只能写入：

```text
/Users/shiqiujing/Documents/n8n
/private/tmp
```

不能直接写入：

```text
/Users/shiqiujing/Documents/M8A
```

因此当前状态为：

```text
ready_to_sync_when_M8A_write_access_available
```
