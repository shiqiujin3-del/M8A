# M8A YouTube 小视频上传验证

日期：2026-07-10

## 结论

YouTube 小视频 Private Upload 验证成功。

## 执行结果

- n8n Workflow：M8A_YOUTUBE_PRIVATE_UPLOAD_EXECUTOR_V1
- Workflow ID：yt_private_upload_v1
- n8n Execution ID：87
- Video ID：I2m1MealZBA
- Video URL：https://www.youtube.com/watch?v=I2m1MealZBA
- Privacy：private
- 上传视频大小：86680 bytes
- 状态：completed
- requires_execution_lookup：false

## 安全确认

- 未公开发布。
- 未设为 unlisted。
- 未删除视频。
- 未修改频道。
- 未修改播放列表。
- 未通知订阅者。
- 未触碰网站和 WordPress。

## 仍未解决

HK680 189MB 大视频公开上传此前在约 58-59MB 处出现 ECONNRESET。此次小视频成功只能证明小文件上传链路正常，不能证明大文件 public upload 已生产可用。

## 当前判断

- YouTube 小视频 Private Upload：PASS
- YouTube 大视频 Public Upload：Known Issue，仍需 Upload Reliability / resumable recovery

