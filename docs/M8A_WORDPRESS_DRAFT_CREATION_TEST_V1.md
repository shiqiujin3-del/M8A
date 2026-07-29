# M8A WordPress 草稿创建实测报告 V1

日期：2026-07-07
执行层：n8n 本地实例（http://localhost:5678）
目标平台：WordPress（woodmachinerynetwork.com）

## 一、测试目的

验证 M8A 是否可以通过 n8n 调用 WordPress 节点，创建一篇“草稿”文章。

本次测试只允许创建草稿，不允许发布到前台。

## 二、执行结果

结果：未通过。

n8n 已进入 WordPress 节点并使用凭证 M8A WordPress Reserved 执行 Create Post 动作。

WordPress 返回错误：Authorization failed - please check your credentials。

页面同时显示中文提示：您不能为此用户创建文章。

## 三、判断

这说明 n8n 工作流可以被启动，WordPress 节点也能发起动作，但当前 WordPress 凭证或账号权限不足，无法完成“创建文章”这一步。

当前不应把 WordPress 标记为已完全接入生产。

## 四、安全边界

本次没有发布任何内容。

本次没有读取、记录、复制或写入任何真实密码、应用密码、密钥或令牌。

## 五、下一步建议

1. CEO 在 WordPress 后台重新生成 Application Password。
2. 确认该 WordPress 用户拥有创建文章/草稿的权限。
3. 在 n8n 中更新 M8A WordPress Reserved 凭证。
4. 再次运行草稿创建验证。
5. 只有草稿验证通过后，才允许 Website Agent 进入 WordPress 草稿工作流。

## 六、第二次 n8n 实测

时间：2026-07-07

前提：n8n WordPress 凭证页面显示 Connection tested successfully。

执行：通过 n8n WordPress 节点创建 WordPress 草稿。

结果：未通过。

错误：Authorization failed - please check your credentials。

判断：凭证可以完成连接测试，但该 WordPress 用户仍没有创建文章/草稿权限，或 Application Password 不属于具备发文权限的用户。

安全确认：没有发布内容，没有删除内容，没有记录任何密码或密钥。
