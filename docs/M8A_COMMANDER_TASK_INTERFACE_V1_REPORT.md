# M8A Commander 任务接口打通报告 V1

日期：2026-07-08

## 一、执行结论

状态：PASS

总控台“任务指挥 / 创建任务”入口已打通。

当前链路：

```text
总控台输入任务
↓
POST http://127.0.0.1:8787/api/missions
↓
Commander Local Mission API 接收任务
↓
写入本地任务队列
↓
总控台可读取 Mission / Task / Approval / Artifact
```

## 二、问题原因

原页面 `createMissionFromConsole()` 调用：

```text
POST /api/missions
```

前端 API Base 原为：

```text
http://localhost:8787
```

但本机 8787 没有任务接口服务监听，因此点击创建任务时返回：

```text
创建失败：Failed to fetch
```

## 三、修复内容

### 1. 新增本地 Commander 任务接口

新增文件：

```text
apps/commander/mission-control/local_mission_api.py
```

职责：

- 监听 `127.0.0.1:8787`
- 支持 `POST /api/missions`
- 支持 Dashboard 所需读取接口
- 不依赖 PostgreSQL
- 不依赖 Docker
- 不连接外部平台
- 只写本地 JSON 队列

### 2. 修复 Dashboard API 地址

修改文件：

```text
apps/dashboard/index.html
```

修改：

```text
http://localhost:8787
```

改为：

```text
http://127.0.0.1:8787
```

原因：避免浏览器将 localhost 解析到 IPv6 或异常地址导致 Failed to fetch。

## 四、接口地址

```text
GET  http://127.0.0.1:8787/health
POST http://127.0.0.1:8787/api/missions
GET  http://127.0.0.1:8787/api/missions
GET  http://127.0.0.1:8787/api/missions/:mission_id
GET  http://127.0.0.1:8787/api/tasks
GET  http://127.0.0.1:8787/api/approvals
GET  http://127.0.0.1:8787/api/artifacts
GET  http://127.0.0.1:8787/api/dashboard/commander
GET  http://127.0.0.1:8787/api/runner/status
```

## 五、测试任务

测试任务内容：

```text
打通第一条链路：Website Agent 生成客户可看的文章 → n8n 创建 WordPress Draft → QA Agent 检查 → Commander 返回验收结果。禁止自动发布。
```

测试 Mission ID：

```text
mission_commander_entry_1783486573930
```

任务状态：

```text
queued
```

任务数量：

```text
4
```

审批数量：

```text
1
```

## 六、任务写入位置

本地总队列：

```text
apps/commander/missions/local_queue/commander_mission_queue.json
```

单任务文件：

```text
apps/commander/missions/local_queue/mission_commander_entry_1783486573930.json
```

## 七、任务队列内容

已进入队列：YES

自动拆分为：

1. Website Agent：生成客户可看的文章
2. n8n Execution Layer：创建 WordPress Draft，不发布
3. QA Agent：检查 Draft
4. Commander：返回验收结果

其中 n8n 创建 WordPress Draft 任务需要 CEO Approval。

## 八、安全确认

本次没有执行以下动作：

- 未发布 WordPress 文章
- 未发送 Gmail
- 未上传 YouTube
- 未修改 OAuth 密钥
- 未删除文件
- 未 merge
- 未 push
- 未连接外部平台

本次只完成：

```text
本地 Commander 任务入口打通
本地 JSON Mission Queue 写入
Dashboard API 可读取
```

## 九、验证结果

### API 创建任务

```text
POST /api/missions
HTTP 201
Mission queued
```

### Dashboard 所需读取接口

全部通过：

```text
GET /health                      200
GET /api/missions                200
GET /api/tasks                   200
GET /api/approvals               200
GET /api/artifacts               200
GET /api/dashboard/commander     200
```

### CORS 预检

```text
OPTIONS /api/missions
HTTP 200
Access-Control-Allow-Origin: *
Access-Control-Allow-Headers: Content-Type, Authorization
```

### JSON 校验

```text
commander_mission_queue.json PASS
```

### Python 校验

```text
local_mission_api.py py_compile PASS
```

## 十、下一步如何交给 Website Agent

下一步建议：

1. Website Agent 读取 `commander_mission_queue.json` 中状态为 `queued` 的 mission。
2. 领取任务 `generate_customer_article`。
3. 基于 HK620 已审核知识生成客户可看的文章草稿。
4. 将文章草稿保存为 Artifact。
5. n8n Execution Layer 只允许创建 WordPress Draft。
6. QA Agent 检查 Draft。
7. Commander 汇总验收结果返回总控台。

继续禁止自动发布。
