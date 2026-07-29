# AI Employee Auto Runner V1 架构

本 Runner 只执行 A 类 Build 本地任务。它从 Global Mission Queue / Runtime Store 读取任务，通过 Global AI Event Center 的事件模型驱动员工领取任务，并写回 Runtime Persistence V1。

安全边界：不调用 n8n，不调用 WordPress，不发布，不删除，不发送 Gmail，不上传 YouTube，不修改生产环境。

流程：Mission Ready → Event → Employee Subscription → Work Queue → Local Execution → Runtime Log → Local Output。
