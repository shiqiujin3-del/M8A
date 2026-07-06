# M8A Bootstrap Report

时间：2026-07-06

目标：仅启动 M8A Bootstrap Stack，使 `http://localhost:5678` 能在浏览器打开 n8n 首页。

## 1. Docker 是否正常

PASS

- Docker Desktop 已安装：`/Applications/Docker.app`
- Docker CLI：`Docker version 29.6.1, build 8900f1d330`
- Docker Compose：`Docker Compose version v5.3.0`
- Docker daemon 最终可用：Server version `29.6.1`

排查过程：

- 初始失败原因 1：Docker daemon socket 不存在。
- 证据：`dial unix /Users/shiqiujing/.docker/run/docker.sock: connect: no such file or directory`
- 初始失败原因 2：Docker Desktop 首次安装/授权未完成，状态为 `starting`。
- 证据：Docker Desktop 日志显示打开 `install` 页面；官方安装命令返回需要写入 `/Library/Application Support/com.docker.docker/install-settings.json`，当前命令行没有系统级写权限。
- 处理结果：重新打开 Docker Desktop 并完成首次授权后，daemon 可用。

## 2. Compose 是否正常

PASS

- `docker compose config` 已通过。
- `docker compose config --quiet` 已通过。
- `docker compose up -d` 已成功执行。

修复内容：

- `docker-compose.yml` 已改为最小 Bootstrap Stack。
- `compose.override.yml`、`compose.dev.yml`、`compose.prod.yml` 的空占位 `services` 已修正为有效 YAML 空映射，避免 `services must be a mapping`。

Bootstrap Stack 仅包含：

- Postgres
- Redis
- n8n

未加入：

- Qdrant
- MCP
- Dashboard
- Workflow
- AI Agent

## 3. 哪些容器成功启动

| 容器 | 镜像 | 状态 | 端口 | Volume | Network | Restart Policy | Health |
|---|---|---|---|---|---|---|---|
| `m8a-postgres` | `postgres:16-alpine` | running | `5432/tcp` container internal | `m8a-bootstrap_m8a_postgres_data:/var/lib/postgresql/data` | `m8a-bootstrap_m8a_bootstrap` | `unless-stopped` | `healthy` |
| `m8a-redis` | `redis:7-alpine` | running | `6379/tcp` container internal | `m8a-bootstrap_m8a_redis_data:/data` | `m8a-bootstrap_m8a_bootstrap` | `unless-stopped` | `healthy` |
| `m8a-n8n` | `n8nio/n8n:latest` | running | `0.0.0.0:5678->5678/tcp`, `[::]:5678->5678/tcp` | `m8a-bootstrap_m8a_n8n_data:/home/node/.n8n` | `m8a-bootstrap_m8a_bootstrap` | `unless-stopped` | `none` |

说明：

- n8n 镜像当前没有 Docker healthcheck，因此 Docker Health 显示 `none`。
- n8n 已通过 HTTP 与浏览器访问验证。

## 4. 哪些失败

最终失败项：无。

启动过程中的已解决问题：

1. Docker daemon 初始不可用。
   - 原因：Docker Desktop 未完成首次启动/授权。
   - 结果：完成授权后 Docker daemon 正常。

2. `docker compose config` 初始失败。
   - 原因：compose 占位文件中 `services:` 只有注释，YAML 解析结果不是 mapping。
   - 错误：`services must be a mapping`
   - 结果：已修复，Compose 校验通过。

3. 首次拉取镜像时找不到 credential helper。
   - 错误：`error getting credentials - err: exec: "docker-credential-desktop": executable file not found in $PATH`
   - 处理：使用 Docker.app 自带 bin 路径完成首次镜像拉取。
   - 结果：镜像已拉取，随后普通 `docker compose up -d` 成功。

## 5. n8n 是否成功打开

PASS

- HTTP 验证：`http://localhost:5678` 返回 `HTTP/1.1 200 OK`
- 浏览器验证：
  - URL：`http://localhost:5678/setup`
  - 页面标题：`n8n.io - Workflow Automation`
  - 页面内容：`Set up owner account`

## 6. 目前 M8A 是否进入 Bootstrap Running 状态

YES

依据：

- Docker daemon 正常。
- Compose 校验正常。
- `docker compose up -d` 正常。
- Postgres running + healthy。
- Redis running + healthy。
- n8n running。
- 浏览器可打开 n8n 初始化页面。

## 7. 下一步建议

1. 创建 n8n owner account，完成首次登录。
2. 保持当前 Bootstrap Stack，不加入 Qdrant/MCP/Agent，先确认 n8n 数据能持久化。
3. 下一步再单独做 P1：第一个测试 Workflow。
