# 认证与授权：服务地址与接入

## 当前服务地址

| 用途 | 实际地址 | 本次核验 / 要求 |
| --- | --- | --- |
| 公共 API 基址 | `https://alisa.vip.cpolar.cn/alisa-gateway` | 完整外网前缀，不能省略 /alisa-gateway |
| 登录 | `POST https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/user/signin` | JSON 字段 username、password；本次未使用真实账号执行登录 |
| 注册 | `POST https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/user/signup` | 字段以 UserDto 和服务实际校验为准 |
| 当前用户 | `GET https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/user/profile` | Bearer 用户凭据 |
| 身份提供者 | `GET https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/user/providers` | 本次匿名请求 200 |
| 健康 | `GET https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/user/health` | 本次 200，返回 UP，不等于登录和全部授权已联调 |
| 授权判定 | `POST https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/authorization/check` | 功能需启用；凭据、应用、资源、动作与对应 scope 都要匹配 |
| 业务租户 API | `https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/user/tenants` | 第一方用户 token；见 [租户管理](/operations/tenancy) |
| 集群内账号 Service | `http://alisa-user.alisa-infra.svc.cluster.local:8084` | 服务间寻址，不给外部浏览器直接使用 |
| 集群内网关 Service | `http://alisa-gateway.alisa-infra.svc.cluster.local:8100` | 不带外部 /alisa-gateway 前缀 |

服务注册名是 `user-service`，Kubernetes Service 名是 `alisa-user`。Nacos 负责发现，不替代客户端所需的完整外网 URL。

## Bearer 请求

```bash
curl -H "Authorization: Bearer $ACCESS_TOKEN"   'https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/user/profile'
```

第一方登录返回的业务凭据和 OAuth 委托/后台应用凭据不是相同格式的承诺。不要假定所有 Bearer 都能在客户端按 JWT 解码；服务器资源验证与 scope 检查才决定有效性。不得将实际 token、JWT_SECRET、Client Secret 写入文档或前端构建。

网关与第一方 JWT 签发/校验方使用一致的现有 `JWT_SECRET`，按当前 JwtUtil 的 Base64/HMAC 实现配置。网关清除客户端伪造的 `X-User-Header`、`X-Authenticated` 再产生可信身份上下文。本次文档更新不改任何现有签名密钥。

## 身份、权限和业务数据分别校验

| 层次 | 检查内容 |
| --- | --- |
| 身份认证 | 用户或应用是谁，凭据是否有效、过期或被撤销 |
| 应用 scope | 委托/后台应用可调用的 application:resource:action 目录，不能用任意 scope 字符串越权 |
| 租户权限 | 活跃租户、成员关系、token 版本、用户/应用对资源的授权 |
| 业务权限 | 当前社区成员、文档作者、目标所有者等资源规则及 SQL 数据范围 |

授权判定请求包含 `applicationId`、`resourceType`、`resourceId`、`action`。例如 SmallOKR 的 applicationId 是 `smallokr`，不能误写成 target-service。权限目录以服务当前配置为准，不套用 Microsoft Graph 的权限名称。

## OAuth2 与管理入口

生产环境的 OAuth2 issuer 为 `https://alisa.vip.cpolar.cn/admin/auth`。管理员在 [Alisa 管理控制台](https://alisa.vip.cpolar.cn/admin/) 管理成员、应用审批和资源授权。浏览器登录、授权码交换、令牌验证和应用测试见 [OAuth2 接入与联调](/operations/oauth2)。

平台资源门户使用独立管理凭据。社区管理入口位于 [Science Community](/services/science-community)，权限由社区角色决定。

## 公开路径和 delegated-ready

网关公开路径只放必要的登录、健康和密码找回等入口；不能将整个 `/api/v1/user/**` 或 `/api/v1/authorization/**` 设为匿名。`authorization/check` 可由下游校验凭据，但仍要按实际功能与策略执行。

SmallOKR 路由中的 `metadata.delegated-ready: true` 允许指定后端接收需自行校验的不透明 Bearer，前提是后端已完成相应验证。它不表示匿名，也不表示服务已部署或任意 OAuth 应用均可访问。

401 通常先检查凭据；403 检查认证链、功能开关、应用范围、租户与业务权限，不能只根据状态码猜一个唯一原因。WebSocket 握手、SockJS 与 STOMP 会话身份另需完整联调，不能把一次 `/ws/info` 200 当成会话鉴权已验证。
