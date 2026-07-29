# M8A YouTube Upload Reliability V1 报告

日期：2026-07-10

## 结论

状态：BLOCKED。

原因不是 OAuth、不是 M8A Storage、不是 n8n 读取文件，而是当前 n8n 原生 YouTube Upload 节点在 189MB 视频上传过程中遇到网络 `ECONNRESET` 后，不能从已上传 offset 恢复同一个 upload session。

本 Sprint 未继续上传 189MB HK680 视频，未公开发布新视频，未修改生产凭证，未调用 WordPress/Gmail/Google API。

## 1. 当前上传工作流审计

Workflow：`M8A_YOUTUBE_HK680_PUBLIC_UPLOAD_V1`

Workflow ID：`yt_hk680_public_v1`

状态：inactive

当前序列：

```text
Manual Trigger
→ Set HK680 Public Metadata
→ Read HK680 Video File
→ YouTube HK680 Public Upload
→ Normalize Execution Response
```

关键节点：

- `Read HK680 Video File`
  - node：`n8n-nodes-base.readBinaryFile`
  - version：1
  - path：`/home/node/.n8n-files/videos/hk680-promo-video.mp4`
  - 读取成功：`video/mp4`, `189 MB`

- `YouTube HK680 Public Upload`
  - node：`n8n-nodes-base.youTube`
  - version：1
  - resource：`video`
  - operation：`upload`
  - privacyStatus：`public`
  - notifySubscribers：`false`
  - categoryId：`28`

n8n 版本：`2.28.6`

Timeout 证据：执行数据中 `timeout: 300000`。

## 2. n8n YouTube 节点能力判断

源码证据显示当前节点使用 YouTube resumable upload：

```text
POST /upload/youtube/v3/videos?uploadType=resumable
```

并逐块 PUT：

```text
Content-Range: bytes offset-nextOffset/total
```

源码注释：

```text
Stream data in 256KB chunks, and upload via the resumable upload api
```

实际执行记录中看到每次 PUT 的 `Content-Length` 为 `1048576`，即 1MB 分块。

当前节点支持：

- Resumable Upload：部分支持，内部使用 YouTube resumable upload session。
- Chunk Upload：支持，逐块 PUT。

当前节点不支持或未暴露：

- 可配置 chunk size：未暴露。
- 可配置 retry count：未暴露。
- 可配置 retry interval：未暴露。
- 断线后恢复同一个 upload URL：未暴露。
- offset 状态持久化：未实现。
- partial upload recovery：未实现。

结论：n8n 原生节点“使用了 resumable upload 技术”，但没有形成 M8A 所需的可靠上传层。

## 3. 根因证据

执行记录：

- Execution `84`：error
- Execution `85`：error

失败节点：

```text
YouTube HK680 Public Upload
```

错误：

```text
ECONNRESET
Client network socket disconnected before secure TLS connection was established
```

HTTP host：

```text
www.googleapis.com:443
```

Upload URL 类型：

```text
https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&...
```

断点证据：

- Execution 84：`Content-Range: bytes 58720256-59768831/189110192`
- Execution 85：`Content-Range: bytes 11534336-12582911/189110192`

含义：

- 第一次约在 58.7MB 到 59.8MB 分块处断开。
- 第二次约在 11.5MB 到 12.6MB 分块处断开。
- 文件总大小：`189110192 bytes`，约 189MB。

执行耗时：

- Execution 84：约 213 秒后失败。
- Execution 85：约 47 秒后失败。

HTTP status：无可用最终 HTTP status；错误发生在 TLS/socket 层。

Video ID：未返回。

Video URL：未返回。

## 4. Upload Reliability Layer V1 设计

目标：为 YouTube / Vimeo / Google Drive / Dropbox / OSS / S3 等所有大文件上传提供统一状态层。

统一状态对象：

```json
{
  "upload_id": "...",
  "mission_id": "...",
  "execution_id": "...",
  "platform": "youtube",
  "object_type": "video",
  "source_path": "/home/node/.n8n-files/videos/hk680-promo-video.mp4",
  "file_size_bytes": 189110192,
  "status": "queued | uploading | retrying | completed | failed",
  "progress_percent": 0,
  "bytes_uploaded": 0,
  "retry_count": 0,
  "max_retry": 3,
  "failure_reason": null,
  "session_url_ref": null,
  "external_id": null,
  "external_url": null,
  "started_at": null,
  "updated_at": null,
  "finished_at": null
}
```

状态流：

```text
Queued
→ Uploading
→ Retrying
→ Completed
或
→ Failed
```

最小字段：

- Upload State
- Progress %
- Retry count
- Max retry
- Failure reason
- Execution ID mapping
- Mission ID mapping
- Draft/Video ID mapping
- Unified status object

存储建议：

- V1 可先存本地 JSON 或 Runtime DB 现有日志表。
- 不新增 Runtime DB schema 的情况下，可写入现有 audit/runtime log JSON。
- 后续如果进入正式长期运行，再把 upload_state 纳入 Runtime Persistence。

## 5. 最小实现建议

不建议继续依赖 n8n 原生 YouTube Upload 节点来上传 100MB+ 文件。

原因：

- 原生节点虽然用了 resumable upload，但 upload session URL 没有暴露。
- 失败后无法查询当前 offset 并继续同一个 session。
- 无法持久化 `uploadUrl`、`bytes_uploaded`、`retry_count`。

推荐最小自定义实现：

1. `Initiate Upload Session`
   - POST YouTube resumable endpoint。
   - 保存 `upload_url`。

2. `Upload Chunk`
   - 按固定 chunk size PUT。
   - 每块成功后更新 `bytes_uploaded` 和 `progress_percent`。

3. `Recover Offset`
   - 失败后向 `upload_url` 发 `Content-Range: bytes */total`。
   - 根据 Google 返回的 Range 继续上传。

4. `Retry Policy`
   - ECONNRESET / ETIMEDOUT / 5xx 可重试。
   - 4xx 权限/配额错误不重试。
   - 默认 max_retry=3。

5. `Finalize Response`
   - 成功后统一返回 Execution Response Contract。

## 6. 标准执行响应

成功后必须返回：

```json
{
  "success": true,
  "execution_id": "...",
  "status": "completed",
  "platform": "youtube",
  "executor": "youtube",
  "action_type": "upload_video",
  "result": {
    "type": "youtube_upload",
    "video_id": "...",
    "video_url": "...",
    "privacy_status": "private | unlisted | public",
    "platform_status": "processed"
  },
  "retry_count": 0,
  "upload_duration": "...",
  "finished_at": "...",
  "error": null
}
```

该结构兼容现有 Execution Response Contract。

## 7. 测试策略

禁止继续 brute-force 上传 189MB HK680。

下一步测试顺序：

1. 生成或选择小视频（小于 5MB）。
2. 使用 private 或 unlisted 上传验证可靠性层。
3. 故意模拟断点，验证 retry / progress / failure reason。
4. 只有可靠性层通过后，才允许再次测试 189MB HK680。
5. 189MB HK680 首次重测建议使用 private，不直接 public。

## 8. 最终建议

READY FOR PRODUCTION：否。

BLOCKED：是。

阻塞原因：现有 n8n YouTube Upload 节点没有 M8A 所需的断点恢复状态层。大文件上传遇到 ECONNRESET 后会失败，且不会返回 video_id/video_url。

下一步建议：建立最小 YouTube resumable upload custom workflow 或轻量 External Executor adapter，先用小视频验证，再回到 HK680 大文件。

## 安全确认

本 Sprint 未继续上传 HK680，未公开视频，未删除 YouTube 视频，未修改频道/播放列表，未修改 WordPress，未调用 Gmail/Google API，未修改生产凭证。
