# M8A WordPress 后台只读验收报告 V1

日期：2026-07-07
Mission：WordPress 后台只读验收 V1
状态：已完成，只读停止

## 一、验收边界

本次只读验收未执行任何修改动作。

- 未修改任何设置。
- 未修改任何用户权限。
- 未修改任何角色。
- 未修改任何插件。
- 未停用或安装插件。
- 未修改主题或代码。
- 未创建 Draft。
- 未发布文章。
- 未记录任何真实密码、密钥或令牌。

## 二、后台用户验收

进入 WordPress 后台 Users 页面后确认：

| 项目 | 结果 |
|---|---|
| 用户名 | admin |
| 用户 ID | 1 |
| 邮箱 | admin@example.com |
| 用户角色 | 管理员 |
| 文章数量 | 49 |
| 是否为 Administrator | 是，后台用户列表显示角色为“管理员” |

结论：后台层面 admin 是管理员角色。

## 三、Application Passwords 验收

进入 admin 的个人资料页 Application Passwords 区域后确认：

当前存在多个 Application Password。可见记录包括：

| 名称 | 创建日期 | 最后使用 | 状态判断 |
|---|---|---|---|
| M8A n8n WordPress | 2026年7月7日 | — | 存在，未显示最后使用 |
| M8A WMN Draft Writer | 2026年7月6日 | — | 存在，未显示最后使用 |
| M8A WMN Draft Writer | 2026年7月6日 | — | 存在，未显示最后使用 |
| Codex REST Category Setup | 2026年6月23日 | 2026年6月23日 | 存在，曾使用 |
| Home Article Upload | 2026年6月19日 | 2026年6月21日 | 存在，曾使用 |
| Codex Upload | 2026年6月18日 | 2026年6月18日 | 存在，曾使用 |

判断：

- 用于 n8n 的 M8A n8n WordPress 确实存在。
- 页面没有显示该记录已撤销；可见撤销按钮表示它仍在列表中。
- “最后使用”为 —，说明 WordPress 后台没有记录到该 Application Password 被成功使用过。
- 不能在不读取密码值的前提下确认 n8n 当前保存的密码值是否就是这条 M8A n8n WordPress。

## 四、插件验收

进入 Plugins 页面后确认已启用插件共 3 个：

| 插件 | 状态 | 可能影响 REST 创建文章 |
|---|---|---|
| Rank Math SEO | 已启用 | 低。SEO 插件通常不限制 REST 创建文章，但可能注入 REST/SEO 元字段逻辑。当前无证据显示它导致 rest_cannot_create。 |
| Site Kit by Google | 已启用 | 低。Google 数据插件，通常不限制 WordPress REST 创建文章。 |
| WMN Rank Math Static Sitemap Provider | 已启用 | 低到中。自定义站点插件，主要描述为向 Rank Math sitemap index 加入静态 HTML 页面；当前无证据显示它限制 REST 创建文章，但自定义插件仍建议只读复核代码。 |

未看到典型权限管理/安全插件：

- 未看到 User Role Editor。
- 未看到 Members。
- 未看到 PublishPress。
- 未看到 Capability Manager。
- 未看到 Wordfence、iThemes Security、All In One WP Security 等典型安全插件。

结论：后台插件列表未显示明显的权限管理插件或 REST API 封锁插件。

## 五、站点健康验收

进入 Tools → Site Health 后确认：

| 项目 | 结果 |
|---|---|
| 站点健康状态 | 待改进 |
| 关键问题 | 1 个：有插件等待更新 |
| 推荐改进 | 3 个：移除未启用主题、缺少一个或多个推荐模块、陈旧的 SQL 服务器 |
| REST API 异常 | 当前可见区域未显示 REST API 异常 |

补充确认：公共 REST 根端点 https://woodmachinerynetwork.com/wp-json/ 返回 HTTP 200。

结论：未发现站点健康页面显示 REST API 不可用。

## 六、固定链接验收

进入 Settings → Permalinks 后确认：

当前固定链接结构选择为：文章名。

结构：/%postname%/

结论：固定链接配置正常，不是导致 REST 创建草稿失败的直接原因。

## 七、Credential 一致性检查

### 1. WordPress

- WordPress 站点：https://woodmachinerynetwork.com
- admin 用户存在。
- admin 用户 ID 为 1。
- admin 角色显示为管理员。
- Application Password 名称 M8A n8n WordPress 存在。

### 2. n8n

- 凭证名：M8A WordPress Reserved
- 类型：Wordpress API
- Username：admin
- Wordpress URL：https://woodmachinerynetwork.com
- Connection tested successfully

### 3. Website Agent

根据已生效的 M8A 外部执行路线政策：

- Website Agent 以后不再走旧 Python/REST 直连生产路线。
- WordPress 正式执行路线统一为 n8n。

### 4. 一致性结论

| 项目 | 是否一致 | 说明 |
|---|---|---|
| WordPress 地址 | 是 | n8n 使用 https://woodmachinerynetwork.com，与后台站点一致。 |
| 用户名 | 是 | n8n 使用 admin，后台存在 admin 用户。 |
| Application Password 名称 | 部分一致 | WordPress 后台存在 M8A n8n WordPress；n8n 凭证名是 M8A WordPress Reserved。名称不同不一定是错误。 |
| Application Password 值 | 未确认 | 出于安全原则，不读取、不记录密码值。 |
| 是否真正被 WordPress 接受 | 否 / 未通过 | n8n 创建草稿 POST 返回 401，且 M8A n8n WordPress 的最后使用仍为 —。 |

关键发现：n8n 的 Connection tested successfully 不能证明 POST /wp/v2/posts 写入权限成功。后台 Application Password 最后使用为 —，说明 WordPress 没有记录该 n8n 用途的成功认证调用。

## 八、REST 错误复核

n8n 最近一次 Create Post 测试返回：

code: rest_cannot_create
message: 抱歉，您不能为此用户创建文章。
data.status: 401

确认：

- 没有创建 Draft。
- 没有发布文章。
- 没有 Cloudflare/WAF 痕迹。
- REST 根端点可访问。
- 后台 admin 是管理员。

## 九、必须回答的问题

### 1. admin 是否为 Administrator？

是。后台 Users 页面显示 admin 角色为“管理员”。

### 2. Application Password 是否有效？

不能判定为完全有效。

它在后台存在，未显示撤销；但用于 n8n 的 M8A n8n WordPress 最后使用为 —，且 n8n 创建草稿 POST 返回 401。

结论：这条 Application Password 存在，但没有证明它已被 n8n 的写入请求成功使用。

### 3. 是否存在影响 REST API 的插件？

未发现明显插件。

已启用插件为 Rank Math SEO、Site Kit by Google、WMN Rank Math Static Sitemap Provider。未看到典型权限管理插件、安全插件或 REST API 封锁插件。

自定义插件 WMN Rank Math Static Sitemap Provider 建议后续只读复核代码，但当前无证据显示它导致 rest_cannot_create。

### 4. 是否发现 Credential 不一致？

发现一个关键不一致风险：

- n8n 使用 admin 和正确 URL。
- WordPress 后台存在 M8A n8n WordPress。
- 但后台显示该 Application Password 最后使用为 —。
- n8n POST 创建草稿返回 401。

这说明 n8n 当前保存的密码值可能不是这条 Application Password，或者 WordPress 没有把 n8n 的 POST 请求认证为该 Application Password。

### 5. 当前导致 rest_cannot_create 最可能的原因是什么？

最可能原因：n8n 当前保存的 Application Password 与 WordPress 后台的有效 Application Password 不一致，或该凭证没有被 WordPress 在 POST /wp/v2/posts 请求中成功认证。

由于 admin 后台角色为管理员，且没有看到明显权限插件，单纯“admin 没有管理员权限”的可能性降低。

### 6. 下一步最小修复方案是什么？

最小修复方案应继续保持低风险：

1. 不提升 admin 权限。
2. 不修改现有角色。
3. 在 WordPress 后台重新生成一个新的 Application Password，名称建议：M8A n8n WordPress V2。
4. 由 CEO 亲自复制该新密码，不发给 AI。
5. 在 n8n 的 M8A WordPress Reserved 凭证中只替换 Password 字段，Username 保持 admin，URL 保持 https://woodmachinerynetwork.com。
6. 保存后先查看 WordPress Application Password 的最后使用是否变化。
7. 再执行一次只创建 draft 的验证。

更安全的长期方案：创建 M8A Draft Bot 专用低权限账号，只授予创建草稿所需权限，再为该账号生成 Application Password。

## 十、风险评估

| 风险 | 等级 | 说明 |
|---|---|---|
| 继续使用 admin 接 n8n | 中到高 | admin 权限过大，不符合最小权限原则。 |
| 直接修改管理员权限 | 高 | 可能影响整站安全和后台可用性。 |
| 直接停用插件排查 | 中 | 可能影响 SEO、Search Console、站点地图。 |
| 继续用不明 Application Password 测试 | 中 | 会重复失败，且无法建立清晰验收链。 |
| 创建专用 Draft Bot 账号 | 低到中 | 需要 CEO 审批，但最符合长期安全。 |

## 十一、最终结论

后台只读验收完成。

本次最重要的新发现：

1. admin 在后台 Users 页面确认为管理员，用户 ID 为 1。
2. WordPress 后台存在 M8A n8n WordPress Application Password。
3. 该 Application Password 最后使用为 —。
4. n8n 凭证使用 admin 和正确 URL，但创建草稿仍返回 401/rest_cannot_create。
5. 已启用插件中未发现明显权限管理或 REST 封锁插件。
6. 站点健康未显示 REST API 异常，固定链接为 /%postname%/。

当前最可能根因：n8n 当前保存的 Application Password 没有被 WordPress 的创建文章 POST 请求成功认证，或者 n8n 保存的密码值与后台新生成的 Application Password 不一致。

建议等待 CEO 审批下一步：重新生成新的 Application Password 并只替换 n8n Password 字段，或创建专用低权限 Draft Bot 账号后再验证。
