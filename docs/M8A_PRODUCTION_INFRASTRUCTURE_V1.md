# M8A Production Infrastructure V1

## 目标

把当前依赖本机手工启动的 M8A 运行链路升级为 Docker Compose 统一托管。
本次不新增业务 Workflow、不新增 Executor、不新增 Dashboard、不改 Commander 业务逻辑。

## Production Architecture

```mermaid
flowchart LR
  Visitor[访客 Contact Form] --> WP[WordPress / Fluent Forms]
  WP --> RemoteTunnel[服务器本地 127.0.0.1:15678]
  RemoteTunnel --> Tunnel[contact-bridge-tunnel 容器]
  Tunnel --> N8N[n8n 容器]
  N8N --> CommanderAPI[Commander Mission API 容器]
  CommanderAPI --> Runtime[(Runtime SQLite / Mission Queue)]
  CommanderAPI --> Audit[Audit Log]
  CommanderAPI --> Logs[统一生产日志目录]
  CommanderAPI --> Health[/health]
  Health --> PG[(Postgres)]
  Health --> Redis[(Redis)]
  Health --> Qdrant[(Qdrant)]
```

## 服务清单

- n8n：继续使用现有容器，`restart: unless-stopped`。
- Postgres：继续作为 n8n 数据库，`restart: unless-stopped`。
- Redis：继续作为运行缓存基础设施，`restart: unless-stopped`。
- Qdrant：继续作为向量库基础设施，`restart: unless-stopped`。
- Commander Mission API：新增 compose 服务 `commander-api`，托管现有 `local_mission_api.py`。
- Contact Bridge Tunnel：新增 compose 服务 `contact-bridge-tunnel`，把服务器 Webhook 入口稳定转发到本地 n8n。

## 启动方式

```bash
docker compose -f docker-compose.yml -f compose.prod.yml up -d --build
```

## 健康检查

统一健康检查入口：

```bash
curl http://127.0.0.1:8787/health
```

检查项：

- Commander
- Mission API
- n8n
- Database / Postgres
- Redis
- Qdrant
- Runtime DB
- 统一日志目录

## 统一日志

生产日志目录：

```text
/Users/shiqiujing/Documents/M8A/logs/production/
```

当前 Contact Webhook Bridge 写入：

```text
contact_webhook_bridge.jsonl
```

## 配置管理

示例配置已写入 `.env.example`。真实密钥只允许放到私有 `.env`，不得提交到仓库。

## 安全边界

本 Sprint 不调用 n8n 业务 Workflow、不调用 WordPress、不发布、不删除、不修改线上内容。
Contact Form 到 Mission 的生产桥接只创建 Mission，不自动回复、不生成报价、不创建 Gmail Draft。
