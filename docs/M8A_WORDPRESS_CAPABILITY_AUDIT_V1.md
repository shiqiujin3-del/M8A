# M8A WordPress Capability 审计报告 V1

日期：2026-07-07
Mission：WordPress REST 权限能力审计 V1
状态：已完成只读审计，等待 CEO 审批下一步

## 一、审计边界

本次只读取和诊断。

已遵守以下限制：

- 未修改 WordPress 配置。
- 未修改任何用户权限。
- 未安装、停用或修改插件。
- 未修改主题。
- 未修改代码。
- 未创建 Draft。
- 未发布文章。
- 未读取、记录或复述真实密码、密钥、令牌。

## 二、审计过程

本次使用以下只读来源：

1. n8n 最近失败执行日志。
2. WordPress 公共 REST API 根端点。
3. WordPress 公共 REST users view context。
4. WordPress 公共 REST post type view context。

本次没有使用任何写入型 WordPress API。

## 三、当前 REST API 实际登录身份

### 1. n8n 凭证填写的用户名

用户名字段：admin

说明：这是 n8n WordPress 凭证中填写的用户名字段。

### 2. WordPress 公共 REST 中的 admin 用户

公开 REST 端点可确认：

- 用户名 / slug：admin
- 用户 ID：1
- 用户公开链接：https://woodmachinerynetwork.com/author/admin/

### 3. 创建文章请求中的实际认证状态

n8n 执行 WordPress Create Post 时，WordPress 返回：

- HTTP 状态码：401
- WordPress 错误代码：rest_cannot_create
- WordPress 错误信息：抱歉，您不能为此用户创建文章。

判断：本次 POST /wp/v2/posts 请求没有被 WordPress 识别为一个具备创建文章权限的已认证用户。

注意：

n8n 凭证中填写 admin，不等于 WordPress REST 在这次 POST 请求里已经实际登录为 admin。HTTP 401 更接近“未认证或认证未被接受”，而不是一个已登录管理员的普通权限不足。

## 四、Capability 清单

本表分两层表达：

- “失败 POST 请求实际有效身份”：以 WordPress 返回 401 为准，视为未成功认证。
- “admin 用户本身”：当前只读公共 REST 不暴露 role/capabilities，未能直接确认。

| Capability | 失败 POST 请求实际有效身份 | admin 用户本身 | 说明 |
|---|---:|---:|---|
| edit_posts | FALSE | 未确认 | 失败请求未被识别为具备创建文章权限的已认证用户。 |
| edit_others_posts | FALSE | 未确认 | 公共 REST 不暴露该能力。 |
| publish_posts | FALSE | 未确认 | 未执行发布测试。 |
| delete_posts | FALSE | 未确认 | 未执行删除测试。 |
| upload_files | FALSE | 未确认 | 未执行上传测试。 |
| edit_pages | FALSE | 未确认 | 公共 REST 不暴露该能力。 |
| manage_options | FALSE | 未确认 | 公共 REST 不暴露该能力。 |
| create_posts | FALSE | 未确认 | WordPress post type 的 create_posts 通常映射到 edit_posts；本次 POST 返回 rest_cannot_create。 |

结论：

可以明确确认的是，这次 n8n 创建草稿请求的实际有效身份不具备 create_posts/edit_posts。

不能在当前只读边界内明确确认的是，WordPress 后台里 admin 用户本身是否拥有完整 Administrator capabilities。

## 五、角色来源审计

### 1. Administrator 角色是否被修改

结果：未确认。

原因：公共 REST API 不暴露角色定义、role capabilities、remove_cap/add_cap 历史。当前没有服务器文件系统、数据库 wp_options/wp_usermeta 或 WP-CLI 只读访问权限。

### 2. 是否存在自定义角色

结果：未确认。

原因：公共 REST API 不列出所有角色。

### 3. 是否存在 Capability 覆盖

结果：未确认。

需要只读检查：wp_user_roles、wp_usermeta 中该用户 capabilities、以及相关插件配置。

### 4. 是否存在 remove_cap() / add_cap()

结果：未确认。

需要只读检查主题 functions.php、mu-plugins、active plugins 或数据库权限配置。

### 5. 是否存在 User Role Editor、Members、PublishPress、Capability Manager 等插件修改权限

结果：未确认。

原因：本次没有取得可稳定读取的插件列表。未发现 n8n 错误日志中出现这些插件名。

## 六、REST API 权限链

n8n WordPress 节点执行的是：

- resource：post
- operation：create
- title：M8A WordPress Draft Connection Test - Do Not Publish
- additionalFields.status：draft

WordPress 返回的原始错误：

```json
{
  "code": "rest_cannot_create",
  "message": "抱歉，您不能为此用户创建文章。",
  "data": { "status": 401 }
}
```

WordPress REST 创建文章通常经过以下权限链：

1. n8n WordPress 节点向 /wp-json/wp/v2/posts 发起 POST。
2. WordPress REST Server 路由到 posts controller。
3. WordPress Core 的 posts controller 执行 create_item_permissions_check。
4. 对 post type=post 检查 create_posts capability。
5. post 的 create_posts capability 通常映射到 edit_posts。
6. 检查失败时返回 rest_cannot_create。

可定位到的 WordPress Core 位置：

- 文件：wp-includes/rest-api/endpoints/class-wp-rest-posts-controller.php
- 函数：WP_REST_Posts_Controller::create_item_permissions_check()
- Capability：post type object 的 cap->create_posts；对普通 post 通常对应 edit_posts。

本次返回 401 的含义：

WordPress 没有把这次 POST 请求识别为已登录且有 create_posts/edit_posts 的用户。

## 七、插件与主题影响

本次未发现 Cloudflare/WAF 痕迹。

n8n 执行日志中：

- rest_cannot_create：存在。
- Cloudflare：未发现。
- n8n WordPress 节点来源：存在。

可能影响项：

1. Application Password 没有被 WordPress 接受。
2. n8n 凭证测试只验证了连接，不代表 POST /wp/v2/posts 写入权限通过。
3. WordPress 用户 admin 的 role/capability 被限制。
4. 安全插件限制 Application Password 写入 REST API。
5. 权限管理插件修改了 admin 或 post capabilities。
6. 主题或 mu-plugin 通过 map_meta_cap/user_has_cap/rest_authentication_errors 等过滤器影响 REST 权限。

上述第 3 到第 6 项需要 WordPress 后台或服务器侧只读权限进一步确认。

## 八、必须回答的问题

### 1. admin 是否真正拥有 Administrator 权限？

未确认。

公共 REST 只能确认 admin 用户存在，ID 为 1；不能确认其后台角色是否仍为 Administrator。

### 2. 是否拥有 edit_posts？

对本次失败 POST 请求的实际有效身份：FALSE。

对 admin 用户本身：未确认。

### 3. 是否拥有 publish_posts？

对本次失败 POST 请求的实际有效身份：FALSE。

对 admin 用户本身：未确认。

### 4. REST API 为什么返回 rest_cannot_create？

因为 POST /wp/v2/posts 创建文章时，WordPress REST 权限检查没有确认该请求拥有 create_posts/edit_posts 能力。

HTTP 401 表明请求未被识别为已认证有权用户，或认证未被接受。

### 5. 根因是什么？

当前最小确定根因：

n8n 的 WordPress Create Post 请求没有以具备 create_posts/edit_posts 能力的有效 WordPress 身份通过 REST 权限检查。

更具体根因仍需只读确认：

- Application Password 是否属于 admin。
- Application Password 是否实际被 WordPress 接受用于 POST。
- admin 角色/capability 是否被修改。
- 是否有插件/主题限制 REST 写入。

### 6. 最小修复方案是什么？

建议不要直接提升现有 admin 权限。

最小修复方案：

1. 只读确认 admin 的角色和 capabilities。
2. 如果 admin 不是必要的执行账号，则创建专用低权限账号，例如 M8A Draft Bot。
3. 该账号只授予创建草稿所需的最小权限，优先 Author 或经过明确约束的 Editor。
4. 为该专用账号生成新的 Application Password。
5. 更新 n8n WordPress 凭证。
6. 再执行一次只创建 draft 的验证。

### 7. 修复风险是什么？

- 如果直接提升 admin 权限，可能扩大账号风险。
- 如果使用 Administrator 账号接入 n8n，n8n 凭证泄露后的影响面过大。
- 如果安全插件限制 REST 写入，绕过限制可能影响站点安全策略。
- 如果未建立最小权限账号，后续 Gmail、YouTube、GA4 等平台接入也会重复出现权限边界不清的问题。

## 九、建议的下一步审批项

建议 CEO 批准下一步只读检查：

1. 只读查看 WordPress 用户列表，确认 admin 角色。
2. 只读查看 active plugins，确认是否存在权限/REST/API 安全插件。
3. 如有服务器侧权限，只读检查 wp_user_roles 和 admin 用户 capabilities。
4. 仍然不修改权限、不创建文章、不发布文章。

## 十、最终结论

本次 Mission 完成了 WordPress REST 权限能力审计的第一阶段。

已确认：问题在 WordPress REST 权限/认证层，不是 n8n 工作流未启动，也不是 Cloudflare/WAF 拦截。

已确认：本次 n8n Create Post 请求的实际有效身份不具备 create_posts/edit_posts。

未确认：admin 用户本身是否仍具备完整 Administrator 权限。

下一步必须继续只读确认角色与插件来源，然后再由 CEO 审批最小修复方案。
