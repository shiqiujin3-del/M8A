# External Executor V1 Architecture

生成时间：2026-07-10T01:40:29Z

## 定位
External Executor V1 是 M8A 从本地 A 类 Build 进入 B 类 External Action 前的统一执行器规格。它不绕过 Production Safety Gate，只接受安全闸门批准后的 action。

## 当前模式
- 当前模式：Dry-run only
- 允许动作：create_wordpress_draft_only
- 禁止动作：publish、update_published_post、delete_post、send_gmail、upload_youtube
- 禁止旧 workflow：CWbGujhdNKFpa5JZ
- 本 Sprint 没有真实调用 n8n / WordPress

## 链路
1. Website Agent 生成本地 Draft JSON。
2. QA Agent 输出 QA Score，必须 >= 90。
3. Production Safety Gate 输出安全批准状态。
4. External Executor V1 读取 payload contract。
5. Dry-run Validator 校验字段和禁止动作。
6. 通过后进入 ready_for_real_execution。
7. 下一步必须 CEO 单独授权后，才能真实调用 n8n Draft-only。
