# M8A WordPress Draft 验证报告 V1

日期：2026-07-07
Mission：WordPress 凭证重建与 Draft 验证 V1
状态：完成

## 一、执行边界

本次只执行凭证重建和 Draft Only 验证。

已遵守：

- 未修改 WordPress 用户角色。
- 未修改 WordPress 权限。
- 未删除旧 Application Password。
- 未安装、停用或修改插件。
- 未修改主题或代码。
- 未发布文章。
- 未更新已有文章。
- 未删除任何文章。
- 未记录或输出真实 Application Password。

## 二、Credential 是否更新成功

结果：成功。

执行内容：

- WordPress 后台创建新的 Application Password：M8A n8n WordPress V2。
- n8n Credential：M8A WordPress Reserved。
- n8n Username：admin。
- n8n WordPress URL：https://woodmachinerynetwork.com。
- n8n Credential Test：Connection tested successfully。

## 三、Application Password 最后使用记录

结果：已更新。

WordPress 后台 Application Passwords 列表显示：

- M8A n8n WordPress V2 已存在。
- 创建日期：2026年7月7日。
- 最后使用：2026年7月7日。
- 最后登录 IP 地址：172.69.9.40。

旧密码未删除。

## 四、Draft 是否创建成功

结果：成功。

n8n 最新执行记录：

- Workflow：CWbGujhdNKFpa5JZ。
- Execution ID：7。
- Status：success。
- 执行时间：2026-07-07 08:07:11 UTC 至 2026-07-07 08:07:13 UTC。

WordPress REST 返回结果包含：

- status：draft。
- class_list：status-draft。
- title：M8A Draft Test - 请勿发布。

WordPress 后台文章列表确认：

- 搜索结果：M8A Draft Test。
- 标题：【M8A Draft Test - 请勿发布】。
- 作者：admin。
- 分类：未分类。
- 日期：最后修改 2026-07-07 下午 4:07。
- 位于草稿列表，未发布。

## 五、是否发生异常

本次验证未发生异常。

对比前次失败：

- 前次失败：HTTP 401 / rest_cannot_create。
- 本次结果：n8n execution success，WordPress 返回 draft。

根因验证结论：

前次失败最可能由 n8n 保存的 Application Password 与 WordPress 后台有效密码不一致，或旧密码未被 WordPress 接受导致。新建并替换为 M8A n8n WordPress V2 后，Draft 创建成功。

## 六、Website Agent 是否具备正式上岗条件

结论：具备 Draft Only 上岗条件。

允许范围：

- Website Agent 可以通过 n8n 创建 WordPress 草稿。
- 仅允许 status=draft。
- 所有正式发布仍需 CEO 审批。

不允许范围：

- 不允许自动 publish。
- 不允许更新已有文章。
- 不允许删除文章。
- 不允许修改 WordPress 用户、插件、主题或设置。

正式上岗建议：

Website Agent 可以进入“WordPress Draft 生产准备阶段”，但不能进入“自动发布阶段”。

## 七、最终结论

M8A 与 WordPress 的 n8n 认证关系已重建成功。

Credential Test 已成功。

Application Password 最后使用记录已更新。

Draft Only 验证已成功。

WordPress 后台已确认测试文章为草稿，未发布。

下一步等待 CEO 审批是否允许 Website Agent 开始 WordPress 草稿任务队列。
