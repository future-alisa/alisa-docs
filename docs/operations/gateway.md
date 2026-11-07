# 网关、Caddy 与动态路由

## 实际入口与分层

| 层 | 当前地址 / 配置 | 职责 |
| --- | --- | --- |
| 公网 | `https://alisa.vip.cpolar.cn` | 外部浏览器、App 和客户端访问 |
| cpolar → Caddy | Windows Podman 中的 caddy-gateway，现有入口 `localhost:8088` | 按路径/Host 转发，接入已有内网 TLS 信任 |
| Traefik | `https://10.89.0.201:443`，HTTPRoute Host 为 `alisa.vip.cpolar.cn` | 根据完整外部路径选 Kubernetes Service，按各路由规则改写前缀 |
| Spring Gateway | `http://alisa-gateway.alisa-infra.svc.cluster.local:8100` | 业务 JWT/身份处理、账号静态路由与 Nacos 动态业务路由 |
| Nacos | `nacos-service.traefik.svc.cluster.local:8848`，控制台 [https://alisa.vip.cpolar.cn/nacos/](https://alisa.vip.cpolar.cn/nacos/) | 服务发现和动态业务路由配置；不是公网路径代理 |

公共 API 完整基址是 `https://alisa.vip.cpolar.cn/alisa-gateway`。例如账号健康：`https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/user/health`。

## Caddy 当前网关片段

下面沿用管理员提供的实际网关配置，放在已有站点块内；不是一份可覆盖整个站点的 Caddyfile：

```text
redir /alisa-gateway /alisa-gateway/ 302

handle /alisa-gateway/* {
    reverse_proxy https://10.89.0.201:443 {
        header_up Host alisa.vip.cpolar.cn
        transport http {
            tls_server_name dashboard.alisa.local
        }
    }
}
```

`handle` 保留 `/alisa-gateway` 前缀，Traefik 的 HTTPRoute 再去掉它。因此请求依次为：

```text
https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/user/health
→ Caddy 保留 /alisa-gateway/api/v1/user/health，HTTP Host 为 alisa.vip.cpolar.cn
→ Traefik 匹配 /alisa-gateway 并改写为 /api/v1/user/health
→ Spring Gateway 发现 user-service
→ alisa-user /api/v1/user/health
```

不要将此片段直接改成 `handle_path`：它会提前剥离前缀，使当前 Traefik HTTPRoute 匹配不到网关。HTTP Host 用于 HTTPRoute 选择，TLS SNI `dashboard.alisa.local` 用于上游证书验证，两者用途不同。沿用已有 mkcert CA 信任，不以关闭 TLS 验证解决 Host 配置问题。

## 各子路径不能套同一个重写规则

| 外网完整入口 | Caddy / Traefik 处理 | 去向 |
| --- | --- | --- |
| `https://alisa.vip.cpolar.cn/alisa-gateway/` | Caddy 保留；Traefik 去 `/alisa-gateway` | Spring Gateway |
| `https://alisa.vip.cpolar.cn/docs/` | 转入 Traefik；HTTPRoute 去 `/docs`，产物资源地址保留 `/docs/` | 文档站 |
| `https://alisa.vip.cpolar.cn/science` | 保留 `/science`，匹配前端构建 basePath | Science Web |
| `https://alisa.vip.cpolar.cn/science-chat/ws` | Traefik 去 `/science-chat` | transfer-service 的 `/ws` |
| `https://alisa.vip.cpolar.cn/` | 现有根路径兜底规则 | Portal Web；同源 `/api/**` 再代理 Portal API |

已有 Caddy 兜底代理覆盖的路径，无需再新建同用途文件。本次文档发布没有修改服务器 Caddy 配置。SeaweedFS 的 S3/WebDAV 是另外的协议和签名规则，见 [存储接入](/operations/storage)。

若确实需要更新服务器 Caddy，在 PowerShell 验证再重载：

```powershell
podman exec caddy-gateway caddy validate --config /etc/caddy/Caddyfile
podman exec caddy-gateway caddy reload --config /etc/caddy/Caddyfile
```

## 新服务应该改哪里

- 复用网关已有前缀新增业务 API：发布后端、确认 Nacos 注册和网络可达，再发布 Nacos 业务路由；通常不用新增 Caddy 路径。
- 新增独立用户站或管理页面：配置前端 basePath、Kubernetes Service / HTTPRoute；现有 Caddy 未覆盖时才增加相应转发。
- 只改后端实例地址：服务发现或 Kubernetes Service 管理，不把临时 Pod IP 写入 Caddy。
- OAuth 绝对路径、回调与 issuer 要整体核验，不能只加一个 `/oauth` 通配匿名规则。当前可用状态见 [认证与授权](/operations/authentication)。

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
