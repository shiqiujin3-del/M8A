# M8N 代理总经理下一步执行清单

日期：2026-07-08
状态：active

## 当前判断

M8N 总经理线程不可达，但 M8A 项目没有停止。

当前由 Codex 临时代理总经理，负责：

- 汇总日报
- 维护 CEO Review List
- 识别 P0/P1 优先级
- 推动 PR 与安全治理

## 下一步 5 件事

### 1. 同步总经理恢复包

目标：把恢复日报、CEO 待办、通道恢复报告写回 M8A docs。

状态：ready_to_sync

阻塞：当前执行环境无 M8A 写权限。

### 2. 审核并合并 PR #3

PR：https://github.com/shiqiujin3-del/M8A/pull/3

目标：让 AI Employee + Access Manager 进入 main。

状态：waiting_ceo_review

### 3. 建立 Google OAuth 安全加固任务

目标：轮换 Google OAuth Client Secret，并重新验证 GA4、GSC、Gmail、YouTube。

状态：P0 waiting_ceo_approval

注意：不应在未轮换前扩大 Gmail / YouTube 写入能力。

### 4. 更新总控 Dashboard 数据

目标：让总控台显示最新状态：WordPress 已发布、GA4/GSC/Gmail/YouTube 已只读验收、PR #3 待审。

状态：waiting_sync

限制：不重构 UI，只更新数据。

### 5. 准备 PR #4

目标：整理 WordPress / n8n / HK620 Draft & Publish 证据链。

状态：waiting_after_PR3

建议：PR #3 合并后再做，避免治理线和业务执行线混在一起。

## 今日唯一建议

先恢复治理链路，再继续扩平台能力。

顺序：

1. 总经理恢复包写回 M8A。
2. PR #3 CEO Review。
3. Google OAuth 安全加固。
4. Dashboard 数据刷新。
5. PR #4 业务证据链。

## 禁止事项

当前禁止：

- Gmail 自动发送。
- YouTube 公开视频上传。
- 自动发布社媒。
- 未审批修改平台权限。
- 保存或输出密钥。
- 把所有未整理文件一次性合并。
