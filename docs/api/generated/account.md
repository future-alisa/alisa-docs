---
editLink: false
---

# 统一账号与授权

> 本页由 `npm run api:sync` 生成，请勿手动修改。

- 服务注册名：`user-service`
- 源码：[alisa-cloud · 03f0644](https://github.com/future-alisa/alisa-cloud/tree/03f0644ea91b6df262425b62000398e40a7d4fbc)
- servlet context-path：`/`
- 路径组合数：69

路径已包含服务 context-path，不包含环境域名及入口代理前缀。它是源码索引，不代表功能已启用或已部署，详见 [覆盖范围](/api/)。

## AuthorizationController

启用条件：`alisa.authorization.enabled=true`。

| HTTP | 服务 HTTP 路径 | 控制器方法 |
| --- | --- | --- |
| `GET` | `/api/v1/authorization/applications/{app}/roles` | [roles](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/controller/AuthorizationController.java#L69) |
| `DELETE` | `/api/v1/authorization/applications/{app}/roles/{role}` | [deleteRole](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/controller/AuthorizationController.java#L82) |
| `PUT` | `/api/v1/authorization/applications/{app}/roles/{role}` | [saveRole](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/controller/AuthorizationController.java#L75) |
| `DELETE` | `/api/v1/authorization/applications/{app}/roles/{role}/bindings` | [unbind](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/controller/AuthorizationController.java#L122) |
| `GET` | `/api/v1/authorization/applications/{app}/roles/{role}/bindings` | [bindings](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/controller/AuthorizationController.java#L109) |
| `PUT` | `/api/v1/authorization/applications/{app}/roles/{role}/bindings` | [bind](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/controller/AuthorizationController.java#L115) |
| `DELETE` | `/api/v1/authorization/applications/{app}/roles/{role}/grants` | [revoke](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/controller/AuthorizationController.java#L102) |
| `GET` | `/api/v1/authorization/applications/{app}/roles/{role}/grants` | [grants](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/controller/AuthorizationController.java#L89) |
| `PUT` | `/api/v1/authorization/applications/{app}/roles/{role}/grants` | [grant](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/controller/AuthorizationController.java#L95) |
| `POST` | `/api/v1/authorization/check` | [check](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/controller/AuthorizationController.java#L37) |

## IdentityProviderController

| HTTP | 服务 HTTP 路径 | 控制器方法 |
| --- | --- | --- |
| `GET` | `/api/v1/user/identities` | [bindings](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/controller/IdentityProviderController.java#L28) |
| `DELETE` | `/api/v1/user/identities/{providerId}` | [unbind](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/controller/IdentityProviderController.java#L40) |
| `POST` | `/api/v1/user/identities/{providerId}` | [bind](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/controller/IdentityProviderController.java#L33) |
| `GET` | `/api/v1/user/providers` | [providers](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/controller/IdentityProviderController.java#L20) |
| `POST` | `/api/v1/user/signin/{providerId}` | [signin](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/controller/IdentityProviderController.java#L23) |

## OAuthPages

启用条件：`alisa.oauth.enabled=true`。

| HTTP | 服务 HTTP 路径 | 控制器方法 |
| --- | --- | --- |
| `GET` | `/oauth/apps` | [applications](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/oauth/OAuthPages.java#L35) |
| `POST` | `/oauth/apps` | [create](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/oauth/OAuthPages.java#L52) |
| `POST` | `/oauth/apps/disable` | [disable](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/oauth/OAuthPages.java#L59) |
| `GET` | `/oauth/connections` | [connections](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/oauth/OAuthPages.java#L63) |
| `POST` | `/oauth/connections/revoke` | [revoke](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/oauth/OAuthPages.java#L69) |
| `GET` | `/oauth/consent` | [consent](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/oauth/OAuthPages.java#L73) |

## OAuthResourceClients

启用条件：`alisa.oauth.enabled=true`。

| HTTP | 服务 HTTP 路径 | 控制器方法 |
| --- | --- | --- |
| `POST` | `/api/v1/user/oauth/resource-clients` | [create](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/oauth/OAuthResourceClients.java#L20) |

## TenantCapabilityController

| HTTP | 服务 HTTP 路径 | 控制器方法 |
| --- | --- | --- |
| `GET` | `/api/v1/user/tenancy` | [capability](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantCapabilityController.java#L9) |

## TenantController

启用条件：`alisa.tenancy.enabled=true`。

| HTTP | 服务 HTTP 路径 | 控制器方法 |
| --- | --- | --- |
| `GET` | `/api/v1/user/tenants` | [list](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantController.java#L24) |
| `POST` | `/api/v1/user/tenants` | [create](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantController.java#L25) |
| `PUT` | `/api/v1/user/tenants/{tenant}` | [update](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantController.java#L26) |
| `GET` | `/api/v1/user/tenants/{tenant}/applications` | [applications](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantController.java#L41) |
| `POST` | `/api/v1/user/tenants/{tenant}/applications` | [application](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantController.java#L46) |
| `DELETE` | `/api/v1/user/tenants/{tenant}/applications/{client}` | [disable](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantController.java#L48) |
| `PUT` | `/api/v1/user/tenants/{tenant}/applications/{client}/approval` | [approve](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantController.java#L47) |
| `POST` | `/api/v1/user/tenants/{tenant}/applications/{client}/secret` | [rotate](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantController.java#L49) |
| `GET` | `/api/v1/user/tenants/{tenant}/audit` | [audit](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantController.java#L54) |
| `GET` | `/api/v1/user/tenants/{tenant}/catalog` | [catalog](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantController.java#L42) |
| `GET` | `/api/v1/user/tenants/{tenant}/invitations` | [invitations](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantController.java#L35) |
| `POST` | `/api/v1/user/tenants/{tenant}/invitations` | [invite](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantController.java#L34) |
| `POST` | `/api/v1/user/tenants/{tenant}/invitations/accept` | [accept](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantController.java#L37) |
| `DELETE` | `/api/v1/user/tenants/{tenant}/invitations/{invitation}` | [cancelInvitation](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantController.java#L36) |
| `GET` | `/api/v1/user/tenants/{tenant}/members` | [members](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantController.java#L33) |
| `DELETE` | `/api/v1/user/tenants/{tenant}/members/{member}` | [remove](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantController.java#L39) |
| `PUT` | `/api/v1/user/tenants/{tenant}/members/{member}` | [role](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantController.java#L38) |
| `POST` | `/api/v1/user/tenants/{tenant}/owner` | [transfer](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantController.java#L40) |
| `DELETE` | `/api/v1/user/tenants/{tenant}/permissions` | [revoke](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantController.java#L53) |
| `GET` | `/api/v1/user/tenants/{tenant}/permissions` | [permissions](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantController.java#L51) |
| `PUT` | `/api/v1/user/tenants/{tenant}/permissions` | [grant](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantController.java#L52) |
| `POST` | `/api/v1/user/tenants/{tenant}/resource-clients` | [resource](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantController.java#L50) |
| `POST` | `/api/v1/user/tenants/{tenant}/token` | [tenantToken](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantController.java#L27) |

## TenantPages

启用条件：`alisa.tenancy.enabled=true`。

| HTTP | 服务 HTTP 路径 | 控制器方法 |
| --- | --- | --- |
| `GET` | `/oauth/tenants` | [list](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantPages.java#L27) |
| `POST` | `/oauth/tenants` | [create](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantPages.java#L34) |
| `POST` | `/oauth/tenants/accept` | [accept](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantPages.java#L35) |
| `GET` | `/oauth/tenants/{tenant}` | [view](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantPages.java#L36) |
| `POST` | `/oauth/tenants/{tenant}/applications` | [app](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantPages.java#L82) |
| `POST` | `/oauth/tenants/{tenant}/applications/{client}/approval` | [approval](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantPages.java#L84) |
| `POST` | `/oauth/tenants/{tenant}/applications/{client}/disable` | [disable](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantPages.java#L85) |
| `POST` | `/oauth/tenants/{tenant}/applications/{client}/secret` | [rotate](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantPages.java#L86) |
| `GET` | `/oauth/tenants/{tenant}/audit` | [audit](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantPages.java#L88) |
| `POST` | `/oauth/tenants/{tenant}/invitations/{invitation}/cancel` | [cancel](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantPages.java#L78) |
| `POST` | `/oauth/tenants/{tenant}/invite` | [invite](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantPages.java#L76) |
| `POST` | `/oauth/tenants/{tenant}/member-role` | [role](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantPages.java#L77) |
| `POST` | `/oauth/tenants/{tenant}/owner` | [owner](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantPages.java#L80) |
| `POST` | `/oauth/tenants/{tenant}/permissions` | [permission](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantPages.java#L87) |
| `POST` | `/oauth/tenants/{tenant}/remove` | [remove](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantPages.java#L79) |
| `POST` | `/oauth/tenants/{tenant}/settings` | [settings](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/tenant/TenantPages.java#L81) |

## UserController

| HTTP | 服务 HTTP 路径 | 控制器方法 |
| --- | --- | --- |
| `POST` | `/api/v1/user/change-password` | [changePassword](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/controller/UserController.java#L30) |
| `POST` | `/api/v1/user/change-password-email` | [changePasswordByEmail](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/controller/UserController.java#L35) |
| `GET` | `/api/v1/user/health` | [health](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/controller/UserController.java#L46) |
| `GET` | `/api/v1/user/profile` | [profile](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/controller/UserController.java#L40) |
| `POST` | `/api/v1/user/send` | [sendResetCode](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/controller/UserController.java#L24) |
| `POST` | `/api/v1/user/signin` | [signin](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/controller/UserController.java#L18) |
| `POST` | `/api/v1/user/signup` | [signup](https://github.com/future-alisa/alisa-cloud/blob/03f0644ea91b6df262425b62000398e40a7d4fbc/alisa-user/src/main/java/com/alisa/user/controller/UserController.java#L21) |
