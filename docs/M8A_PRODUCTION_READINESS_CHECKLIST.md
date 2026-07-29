# M8A Production Readiness Checklist

## 已完成

- [x] Docker Compose 已覆盖 n8n、Postgres、Redis、Qdrant。
- [x] Commander Mission API 已可作为 Docker Compose 长期服务启动。
- [x] Commander Mission API 支持自动恢复：`restart: unless-stopped`。
- [x] Contact Webhook Bridge Tunnel 已纳入 Docker Compose，不再依赖临时手工 SSH 命令。
- [x] `/health` 已统一检查 Commander、Mission API、n8n、Database、Redis、Qdrant、Runtime DB、日志目录。
- [x] Contact Webhook Bridge 写入统一生产日志目录。
- [x] `.env.example` 已补充生产基础设施配置项，真实密钥仍不入库。

## CEO 人工验收步骤

1. 启动生产编排：

```bash
docker compose -f docker-compose.yml -f compose.prod.yml up -d --build
```

2. 检查容器：

```bash
docker ps
```

应看到：

- m8a-n8n
- m8a-postgres
- m8a-redis
- m8a-qdrant
- m8a-commander-api
- m8a-contact-bridge-tunnel

3. 检查统一健康入口：

```bash
curl http://127.0.0.1:8787/health
```

4. 检查 Webhook 仍可从服务器进入 n8n。

5. 访问 Contact 页面并提交一次真实表单：

```text
https://woodmachinerynetwork.com/contact/
```

6. 验证 Mission 自动创建：

```bash
ls apps/commander/missions/local_queue/mission_website_contact_*.json
```

7. 验证 Runtime：

```bash
sqlite3 apps/commander/runtime_persistence_v1/db/m8a_runtime_v1.sqlite "select mission_id,status,updated_at from missions order by updated_at desc limit 3;"
```

8. 验证 Audit：

```bash
tail -n 20 apps/commander/external_executor_v1/audit/external_executor_real_execution_audit_log.v1.json
```

9. 验证统一日志：

```bash
tail -n 20 logs/production/contact_webhook_bridge.jsonl
```

10. 电脑重启验收：

- CEO 手动重启电脑。
- 登录后打开 Docker Desktop。
- 执行 `docker ps`，确认所有 M8A 容器恢复。
- 再次提交 Contact Form，确认 Mission / Runtime / Audit 正常写入。

## 当前风险

- Docker Desktop 自身是否随 macOS 登录启动，需要 CEO 在 Docker Desktop 设置里确认。
- `contact-bridge-tunnel` 依赖部署密钥路径，生产 `.env` 中必须写真实路径。
- 电脑完全关机期间，本地 n8n 与 Commander 不可用；若要真正 7×24，需要后续迁移到云服务器或常开主机。
- 当前 Runtime 主数据仍以本地文件与 SQLite 为主，适合当前阶段；高并发生产建议后续迁移到独立数据库服务。
