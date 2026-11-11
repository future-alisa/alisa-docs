# Alisa OAuth2 接入与联调

Alisa Admin 管理 OAuth2 应用审批、租户成员和资源授权。接入方先确定业务、租户和实际需要的功能，再登记应用。管理入口为 [Alisa 管理控制台](https://alisa.vip.cpolar.cn/admin/)。

| 用途 | 生产地址 |
| --- | --- |
| Issuer | `https://alisa.vip.cpolar.cn/admin/auth` |
| 发现文档 | [OAuth2 元数据](https://alisa.vip.cpolar.cn/admin/auth/.well-known/oauth-authorization-server) |
| 浏览器授权 | `GET https://alisa.vip.cpolar.cn/admin/auth/oauth2/authorize` |
| 换取令牌 | `POST https://alisa.vip.cpolar.cn/admin/auth/oauth2/token` |
| 验证令牌 | `POST https://alisa.vip.cpolar.cn/admin/auth/oauth2/introspect` |
| 撤销令牌 | `POST https://alisa.vip.cpolar.cn/admin/auth/oauth2/revoke` |
| 服务端资源判定 | `POST https://alisa.vip.cpolar.cn/admin/api/v1/authorization/check` |

## 登记应用与授权

1. 在 Admin 切换到目标业务租户。网站或移动端登记为公开客户端，填写实际回调地址并逐项申请 scope。能在服务端保管凭据的应用按实际用途登记。
2. 在「应用与审批」检查批准的 scope。应用只可请求其批准范围内的功能；用户也可在授权页选择同意的功能。
3. 在「成员管理」确认登录账号已加入该租户。在「资源权限」选对应业务、成员或角色、允许的功能及资源范围。填写具体资源 ID 可缩小授权范围。使用 `*` 代表当前租户内该资源类型的全部资源。
4. 资源服务使用专门登记的验证凭据调用 introspection，并校验 issuer、受众、有效期、租户和 scope。服务端再调用资源判定并检查业务角色和数据归属。验证凭据与业务客户端分开维护，密钥仅保存在服务端 Secret。

## 授权码与 PKCE

公开客户端为每次登录生成随机 `state` 和 `code_verifier`，使用 SHA-256 和无填充 Base64URL 生成 `code_challenge`。浏览器打开授权端点时传 `response_type=code`、`client_id`、`redirect_uri`、以空格分隔的 `scope`、`state`、`code_challenge` 和 `code_challenge_method=S256`。回调地址必须和登记值完全一致。

回调先验证 `state` 并处理用户拒绝等 OAuth 错误。用原始 verifier 和回调地址向 token 端点提交表单。下面使用公开客户端；机密客户端按登记的方式认证。

```bash
curl --fail-with-body 'https://alisa.vip.cpolar.cn/admin/auth/oauth2/token' \
  --data-urlencode 'grant_type=authorization_code' \
  --data-urlencode "client_id=$CLIENT_ID" \
  --data-urlencode "redirect_uri=$REDIRECT_URI" \
  --data-urlencode "code=$CODE" \
  --data-urlencode "code_verifier=$CODE_VERIFIER"
```

使用返回的 `access_token` 设置 `Authorization: Bearer …`，按返回的 `scope` 判断实际获批功能。令牌可能是不透明字符串，资源服务应按其验证配置处理。只有客户端配置与响应允许时才使用 refresh token；`client_credentials` 用于应用身份，不能代表登录用户。用户可通过授权页上的「已授权应用」撤销委托。

## 应用联调

| 应用 | 回调 | 最小读取 scope | 建议验证 |
| --- | --- | --- | --- |
| SmallOKR 移动端 | `com.sunyubo.smallokr:/oauth2/callback` | `smallokr:target:read` | 请求 `GET /alisa-gateway/target-service/api/v1/target/get` |
| Science Community 网站 | `https://alisa.vip.cpolar.cn/science/auth/oauth/callback` | `science-community:community:read` | 请求 `GET /science/community-api/auth/profile`，再读取自己的社区 |

第三方应用登记自己的 Client ID 和回调地址。Science Community 的写入 scope 为 `science-community:community:write`，实际操作还受租户资源授权和社区角色限制。各业务的接口与部署配置见 [SmallOKR](/services/smallokr) 和 [Science Community](/services/science-community)。

联调时用新令牌分别验证受保护读取、缺少 scope、错误租户和撤销后的请求。在 Bruno 切换账号后先清除旧令牌缓存，再走一遍授权码流程。公开列表即使返回 200，也只验证接口可达。

| 现象 | 优先检查 |
| --- | --- |
| 回调失败或 `invalid_grant` | 回调地址是否完全一致，授权码是否已使用或过期，PKCE verifier 是否对应当前请求 |
| 401 | Bearer 是否已发送，令牌是否有效，issuer 和受众是否匹配 |
| 403 | 确认令牌所属账号、租户、实际 scope、资源授权及业务角色 |
| 503 | 查看网关路由、Nacos 注册和后端就绪状态。验证服务依赖故障也应结合日志定位 |

记录复现步骤时仅保留状态码、请求路径和脱敏后的日志。授权码、访问令牌、刷新令牌及 Client Secret 通过安全配置管理。
