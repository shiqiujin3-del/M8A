# M8A WordPress n8n 授权失败诊断报告 V1

日期：2026-07-07
执行层：n8n
平台：WordPress / woodmachinerynetwork.com
状态：诊断完成，暂不修改权限

## 一、CEO 指令边界

本次只做诊断。

不修改 WordPress 用户权限。

不提升账号权限。

不发布正式文章。

不删除任何内容。

不读取、记录或复述真实密码、密钥、令牌。

## 二、已确认事实

1. n8n 凭证页显示：Connection tested successfully。
2. n8n 当前 WordPress 凭证名：M8A WordPress Reserved。
3. n8n 当前 WordPress 用户名字段：admin。
4. n8n 执行 WordPress Create Post，目标状态为 draft。
5. 执行结果失败，没有创建草稿，没有发布内容。

## 三、HTTP 状态码

HTTP 状态码：401。

## 四、WordPress 原始错误

WordPress REST API 返回：


dan code: rest_cannot_create
message: 抱歉，您不能为此用户创建文章。
data.status: 401

## 五、根因判断

本次失败不是 Cloudflare/WAF 拦截。

理由：n8n 执行日志中没有 Cloudflare 错误痕迹，返回的是 WordPress REST API 的 JSON 错误。

本次失败也不是普通网络连接失败。

理由：n8n 凭证连接测试已经成功。

当前最可能根因：

WordPress 用户 admin 当前在 REST API 创建文章场景下不具备 create/edit posts 权限，或被 WordPress 站内安全/权限插件限制了 REST API 创建文章能力。

## 六、仍未完全确认的事项

1. WordPress 后台中 admin 的实际角色是否为 Administrator、Editor、Author 或其他。
2. 是否存在安全插件限制 REST API 写入。
3. 是否存在服务器或 WordPress 规则限制 Application Password 创建文章。

## 七、修复建议

建议下一步仍然不要直接修改权限。

先在 WordPress 后台确认：

1. admin 的角色。
2. admin 是否具备编辑/创建文章权限。
3. 是否有安全插件限制 REST API 或 Application Password 写入。
4. 是否需要为 M8A 单独创建一个最小权限账号，例如 Author 或 Editor，只允许创建草稿。

推荐修复方案：

创建一个专用 WordPress 用户，例如 M8A Draft Bot。

该用户只授予创建草稿所需的最小权限。

为该用户生成专用 Application Password。

把 n8n WordPress 凭证改为该专用用户。

再执行一次只创建 draft 的验证。

## 八、安全结论

当前不建议批准修改权限。

建议批准下一步：只读检查 WordPress 用户角色和安全插件配置。

在 CEO 批准前，不进行权限提升，不发布文章。
