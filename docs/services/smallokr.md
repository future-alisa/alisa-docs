# SmallOKR API

SmallOKR 将目标、阶段成果、待办与跟踪作为一个业务项目介绍，调用方按资源查找 API；底层仍由 target-service、todo-service、trace-service 分别运行。本文参考 [Microsoft Graph 的请求与资源组织方式](https://learn.microsoft.com/en-us/graph/call-api)，但保持本项目实际路径、字段和权限模型。

## 服务根地址与可用性

公共网关基址：`https://alisa.vip.cpolar.cn/alisa-gateway`。

当前网关已有 SmallOKR 路由，但最近的实际 Deployment 清单未发现这三个后端。下面给出的是已配置路由对应的完整调用地址，不宣称它们目前可返回真实业务数据；首次联调先确认后端部署与 Nacos 注册。

| 资源组 | 完整服务根地址 | 后端 |
| --- | --- | --- |
| 目标与阶段成果 | `https://alisa.vip.cpolar.cn/alisa-gateway/target-service/api/v1` | target-service，默认 9081 |
| 待办 | `https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/todo` | todo-service，默认 9082 |
| 跟踪 | `https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/trace` | trace-service，默认 8083 |

`/target-service` 是目标服务实际 context-path，不能省略；todo 和 trace 不需要此段。这里的“跟踪”是业务模块，不是分布式调用链监控。

## 资源与常用方法

| 资源 / 操作 | HTTP 请求（完整 URL） | 输入 / 权限边界 |
| --- | --- | --- |
| 读取目标 | `GET https://alisa.vip.cpolar.cn/alisa-gateway/target-service/api/v1/target/get` | 身份与 target/read 检查；用户身份由后端决定 |
| 创建目标 | `POST https://alisa.vip.cpolar.cn/alisa-gateway/target-service/api/v1/target/save` | Target 请求体与 create 权限，以源码 DTO 为准 |
| 读取目标的阶段成果 | `GET https://alisa.vip.cpolar.cn/alisa-gateway/target-service/api/v1/result/getAll?targetId={targetId}` | 目标归属与 result/read 检查 |
| 读取待办 | `GET https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/todo/get` | todo/read 检查，不能通过改 userId 参数冒充另一用户 |
| 新建或保存待办 | `POST https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/todo/add` | Todo JSON；新记录执行 create，已有 ID 执行 update 检查 |
| 删除待办 | `DELETE https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/todo/delete?todoId={todoId}` | 具体记录的 delete 权限 |
| 读取跟踪入口 | `GET https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/trace/get` | target/read 检查，内部 Feign 调用目标服务 |

这些是当前控制器的真实方法名，不为了模仿 Graph 改写成不存在的 `/tasks` 或 `/goals`。完整控制器路径索引： [目标与成果](/api/generated/target)、[待办](/api/generated/todo)、[跟踪](/api/generated/trace)。

## 身份与权限

所有受保护请求传 `Authorization: Bearer ...`。SmallOKR 的资源 applicationId 为 `smallokr`，和微服务注册名不同；委托场景的 scope 按服务器目录采用 `smallokr:资源:动作`，例如已在目录配置时的 `smallokr:todo:read`，不能仅凭字符串自行获得授权。

第一方用户、用户委托应用和后台 machine 应用是不同身份。除了 scope，还执行具体资源权限与数据归属检查。租户模式需要相应表结构、资源服务配置及租户 token 一起启用，见 [认证与授权](/operations/authentication)、[租户管理办法](/operations/tenancy)。

## 请求示例

在后端已部署且取得所需权限后，读取当前身份的待办：

```http
GET https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/todo/get
Authorization: Bearer <access-token>
Accept: application/json
```

```bash
curl --fail-with-body   -H "Authorization: Bearer $ACCESS_TOKEN"   'https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/todo/get'
```

该方法的源码返回 `Result<List<TodoVo>>`。完整字段以 DTO 和具体接口为准，不把某个列表响应推导成所有资源具有相同 schema。不要向这些现有 API 自动添加 Graph 的 `$filter`、`$select` 或分页参数；当前没有声明实现 OData。

## 开发对接顺序

1. 明确调用者是第一方用户、委托应用还是后台应用，申请对应资源范围。
2. 配置完整网关 URL；不要将 Kubernetes DNS、Nacos 注册名或 Pod IP 给外部客户端。
3. 确认三个后端各自的部署、Nacos namespace/group 与依赖，再验证业务接口。
4. 对读取、创建、更新、删除分别验证权限；租户场景增加跨租户拒绝和 SQL 范围检查。
5. 最后验证 trace → target 的身份上下文与错误传播，不以网关一次 401 代替端到端结果。
