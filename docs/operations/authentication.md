# 认证与授权约定

## 调用方式

普通受保护请求使用 Bearer token。

```bash
curl -H "Authorization: Bearer $ACCESS_TOKEN"   "$GATEWAY_BASE/api/v1/user/profile"
```

`GATEWAY_BASE` 是对应环境完整的网关入口，可以包含入口代理前缀。`ACCESS_TOKEN` 由服务的登录/授权流程取得，不写入文档、构建产物或 Git。

网关与账号服务需要使用一致的 `JWT_SECRET`。网关清除客户端伪造的 `X-User-Header`、`X-Authenticated`，经过校验后再生成下游身份头。

## 公开路径不等于无需业务校验

网关通过 `alisa.gateway.auth.public-paths` 配置登录、健康检查及邮箱重置等公开入口。公开路径是否仍要求请求体、验证码或服务端 token 校验，由实际接口决定；不能把整个 `/api/v1/user/**` 或 `/api/v1/authorization/**` 设为匿名。

`/api/v1/authorization/check` 可以由下游承担 token 校验。相关授权端点可能依赖 `alisa.authorization.enabled=true`；源码里有控制器不代表功能已经启用。

## delegated-ready 标记

SmallOKR 的现有路由示例使用 `metadata.delegated-ready: true`。它允许指定后端接收需自行校验的不透明 Bearer 凭据，不能把它理解为允许匿名访问。

只有后端已部署独立 Bearer 校验时才能启用这一标记。新增服务默认不增加该标记，也不自动扩大公开路径。

## 401、403 与身份传递

- **401**：通常表示缺少、无效或不适用的凭据，先检查 token 和当前路径的认证流程。
- **403**：通常表示身份已识别但资源操作不被允许，还应查看服务端实际错误响应。
- 业务权限留在业务服务执行；通过网关验证 JWT 不代表对任意社区、目标或成员操作都有权限。

WebSocket 的 HTTP 握手、SockJS 请求和 STOMP 会话身份是不同环节。路由存在不代表会话级身份绑定已正确实现，仍需按 transfer-service 的实际实现验证。
