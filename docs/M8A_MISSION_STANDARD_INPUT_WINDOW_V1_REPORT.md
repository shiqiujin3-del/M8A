# M8A Mission 标准输入窗口 V1 开发验收报告

日期：2026-07-28
状态：completed

## 一、完成内容

已将 Mission 标准输入窗口 V1 接入 M8A 总控台。

总控台入口：

- 页面：http://127.0.0.1:8099/index.html
- 顶部导航：创建 Mission
- 页面区域：老板今日视图下方的“创建 Mission / Mission 标准输入窗口 V1”

## 二、页面字段

已支持：

- CEO 指令输入框
- 任务类型选择
- 目标员工选择
- 优先级
- 输入资料
- 输出要求
- 安全边界
- 是否需要 CEO 审批
- 创建 Mission 按钮

## 三、本地队列写入

提交后通过本地 Commander API 写入：

- apps/commander/missions/local_queue/commander_mission_queue.json
- apps/commander/missions/local_queue/mission_standard_input_1785243447870.json

测试 Mission ID：mission_standard_input_1785243447870

测试状态：ready

## 四、安全确认

本次只写入本地任务队列。

未执行：

- n8n workflow
- WordPress publish
- 已发布文章修改
- 删除内容
- Gmail 发送
- YouTube 上传
- merge / push

Mission 对象已包含安全字段：

- n8n_execution_allowed=false
- wordpress_publish_allowed=false
- wordpress_published_article_edit_allowed=false
- gmail_send_allowed=false
- youtube_upload_allowed=false

## 五、验证结果

- Dashboard HTML 解析通过。
- local_mission_api.py AST 解析通过。
- commander_mission_queue.json JSON 校验通过。
- POST /api/missions 成功返回 Mission ID。
- Mission 已进入本地任务队列。

## 六、下一步

建议下一步开发 AI 员工详情页 V1，让 Website Agent、QA Agent、Commander Reporting Agent、Automation Agent 的任务队列、权限、workflow 风险和 KPI 能在员工页直接查看。
