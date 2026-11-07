# 网关与动态路由

## 两种配置同时生效

公共 `user-service` 路由保留在网关本地 `application.yml`，业务路由由 Nacos 动态提供。当前配置分工如下：

| 来源 | 内容 |
| --- | --- |
| 网关本地配置 | 账号、授权及 OAuth 登录/协议路径 |
| Nacos：`ALISA_GATEWAY / alisa-gateway-routes.yaml` | SmallOKR 和 ScienceCommunity 的业务路径 |

本地账号路径包括 `/api/v1/user/**`、`/api/v1/authorization/**`、`/oauth2/**`、`/oauth/**`、`/login`、`/logout`、`/.well-known/**`。

**Nacos 文件不要重复添加 `user-service`。** 自定义加载器会检查本地与动态路由 ID，重复配置会被拒绝。

## 业务路由清单

| 路由 ID | 转发目标 | 匹配 |
| --- | --- | --- |
| target-service | `lb://target-service` | `/target-service/api/v1/**` |
| todo-service | `lb://todo-service` | `/api/v1/todo/**` |
| trace-service | `lb://trace-service` | `/api/v1/trace/**` |
| community-service | `lb://community-service` | `/community/**` |
| transfer-api | `lb://transfer-service` | `/api/users/**` |
| chat-websocket | `lb:ws://transfer-service` | `/ws/**` 且 Upgrade 为 websocket，order 为 -1 |
| chat-sockjs | `lb://transfer-service` | `/ws/**` 的 HTTP/SockJS 请求 |

对应结构示例：[gateway-routes.yaml](/examples/gateway-routes.yaml)。它是文档快照；运行环境以 Nacos 中当前发布的配置为准。

## 发布路由

1. 在正确 Nacos namespace 中找到 Group `ALISA_GATEWAY`、Data ID `alisa-gateway-routes.yaml`。
2. 修改完整的业务路由列表，确认 ID、URI 和路径没有重复或意外扩大。
3. 发布后检查每个网关实例日志中的 `Loaded N business routes from Nacos ...`。
4. 用实际业务请求验证鉴权及后端响应。单纯得到 401 只能证明请求进入了鉴权阶段。

网关会先编译候选路由，成功后替换当前快照并刷新缓存；错误更新保留当前进程上一版有效路由。每个实例独立接收更新，不提供跨实例同时生效的事务。

初始配置无法加载时网关启动失败。显式 `routes: []` 用于清空业务路由，删除整个配置会被视为无效更新。需要回滚时，在 Nacos 历史中恢复有效版本后发布。

## 配置项

| 环境变量 | 用途 |
| --- | --- |
| `GATEWAY_NACOS_ROUTES_ENABLED` | 开启动态业务路由，设置为 `true` |
| `GATEWAY_NACOS_ROUTES_DATA_ID` | 默认 `alisa-gateway-routes.yaml` |
| `GATEWAY_NACOS_ROUTES_GROUP` | 默认 `ALISA_GATEWAY` |
| `NACOS_SERVER_ADDR`、`NACOS_NAMESPACE` | 现有 Nacos 地址与 namespace ID |
| `NACOS_USERNAME`、`NACOS_PASSWORD` | 由环境注入读取配置所需的凭据 |

不要同时挂载一份包含相同业务 ID 的静态路由文件。SDK 的本地缓存行为仍适用，进程内有效快照不等同于独立持久化备份。
