# 租户管理办法

租户能力由 alisa-user 承载。此页根据当前源码说明流程；本次匿名探测得到租户能力 API 401、OAuth 租户页面 403，尚未用真实用户验证线上租户操作。不要把以下能力写成已对所有线上客户端启用。

## 三种“租户”不要混用

| 概念 | 负责什么 | 不自动带来什么 |
| --- | --- | --- |
| 业务租户 | 用户成员、角色、应用范围和资源权限；关联业务数据的 tenant_id | 不自动创建 Kubernetes namespace 或独立数据库 |
| Portal 中的租户 | 平台资源规划、命名空间唯一性和配额、生成部署申请 | 不等于 alisa-user 的业务租户，不自动创建真实集群资源 |
| Kubernetes Namespace | 集群对象的作用范围，可配合 RBAC、Quota、网络策略 | 单独创建 namespace 不等于业务身份或强网络隔离 |

## 管理入口与启用条件

| 入口 | 当前地址 / 状态 |
| --- | --- |
| 业务租户 API 根地址 | `https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/user/tenants` |
| 租户能力探测 | `GET https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/user/tenancy`；需要第一方登录 token，成功后查看 `enabled` |
| 源码中的 OAuth 租户页面 | `https://alisa.vip.cpolar.cn/alisa-gateway/oauth/tenants`；本次为 403，不作为已可用后台推荐 |
| 独立身份管理控制台 | alisa-cloud 的 `alisa-admin-web`；尚未在本次部署清单中发现对应生产服务和域名 |
| 平台资源规划 | [Alisa Portal](https://alisa.vip.cpolar.cn/)；仍使用独立管理员令牌 |

启用业务租户前，需要发布包含租户接口的账号服务版本、完成 `oauth.sql` / `tenant.sql` 表结构迁移，并配套配置 `TENANCY_ENABLED`、`OAUTH_ENABLED`、`AUTHORIZATION_ENABLED`、应用 scope 目录和授权提供者。源码默认关闭这些可选能力；本次不会修改开关、执行迁移或轮换密钥。

## 角色规则

| 角色 | 当前实现中的职责 |
| --- | --- |
| OWNER | 创建者成为所有者；管理租户名称和启停、管理管理员、转移所有权。不能直接退出或被普通角色调整操作降级 |
| ADMIN | 管理普通成员/只读成员的邀请与角色、应用审批、资源授权和审计；涉及 ADMIN 的成员提升或调整需 OWNER |
| MEMBER | 租户成员，具体业务资源操作依赖授权记录与业务检查，不能把“已加入”当成可修改全部数据 |
| READER | 租户授权提供者只允许 read 动作继续判定；仍需相应资源授权记录，不等于自动可读全部资源 |

OWNER/ADMIN 在租户授权提供者中可通过租户内资源判定，但仍要满足凭据类型、应用 scope、token 版本和业务资源服务的校验。社区自身的 owner/admin/member 角色与这里的大写租户角色是不同的业务关系。

## 标准管理流程

1. 用户先完成统一账号登录，取得第一方 Bearer token；租户管理接口不接受拿后台应用身份冒充用户。
2. 读取 `.../api/v1/user/tenancy`，确认当前实例启用了租户能力；再读取或创建自己的租户。
3. OWNER/ADMIN 给已存在的用户 ID 发定向邀请；当前邀请有效期为 2 天，服务端保存凭据哈希，原始邀请凭据只向接收者安全交付。
4. 受邀用户用自己的登录身份提交 `invitationId` 与邀请凭据加入。可以查询、撤销未接受邀请，不要在文档或截图里保存实际邀请 token。
5. 用户选择租户，调用租户 token 接口；后端校验成员关系并签发包含 `tenantId`、`tenantVersion` 的访问凭据。切换租户后刷新页面业务状态，不复用上个租户的数据。
6. 在该租户下登记应用并请求明确范围；管理员审批范围，再为用户或 machine 应用分配具体资源权限。
7. 定期查看审计。成员移除会清理其相关授权；所有者转移必须由现有 OWNER 指定已加入的成员，原所有者成为 ADMIN。
8. 停用租户会更新 token 版本、撤销相关 OAuth 授权并清理邀请；恢复不应被理解为旧授权自动恢复。具体 token 是否有效以服务端验证为准。

## 常用 API

下面 URL 的完整公共前缀均为 `https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/user/tenants`，表中给出完整地址，示例租户 ID 只用占位符。

| 方法 | 完整 URL | 用途 |
| --- | --- | --- |
| GET / POST | `https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/user/tenants` | 列出自己的租户 / 创建租户 |
| POST | `https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/user/tenants/{tenant}/token` | 选择租户并取得业务访问凭据 |
| GET | `https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/user/tenants/{tenant}/members` | 查看成员 |
| POST / GET | `https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/user/tenants/{tenant}/invitations` | 生成邀请 / 查询未接受邀请 |
| POST | `https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/user/tenants/{tenant}/invitations/accept` | 接受定向邀请 |
| PUT / DELETE | `https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/user/tenants/{tenant}/members/{member}` | 改角色 / 移除成员或退出 |
| POST | `https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/user/tenants/{tenant}/owner` | 转移所有者 |
| GET / POST | `https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/user/tenants/{tenant}/applications` | 应用列表 / 登记应用 |
| GET | `https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/user/tenants/{tenant}/catalog` | 当前租户成员可见的应用功能目录 |
| PUT / DELETE | `https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/user/tenants/{tenant}/permissions` | 授予 / 撤销资源权限 |
| GET | `https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/user/tenants/{tenant}/audit` | 审计查询，limit 1–200，按游标分页 |

读取能力与租户列表的例子（需要有效用户 token）：

```bash
curl -H "Authorization: Bearer $ACCESS_TOKEN"   'https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/user/tenancy'
curl -H "Authorization: Bearer $ACCESS_TOKEN"   'https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/user/tenants'
```

## 业务服务怎样完成隔离

SmallOKR 三个服务使用相同业务 applicationId `smallokr`，租户模式由 `SMALLOKR_TENANCY_ENABLED` 控制。目标表为 `tb_target`、待办表为 `tb_todo`；资源服务的 tenant-table / require-tenant 与表结构必须匹配，源码校验发现不匹配时会拒绝启动。

每个查询、详情、修改、删除都要从已验证身份取得 tenantId，并作用到 SQL 或持久层条件；不能信任浏览器随意传来的 tenantId/userId。分页、分析、批量操作和 Feign 内部调用也要传递正确上下文。当前模式未启用时，资源服务会拒绝不匹配的租户 token，不能只换 token 就切换数据模式。

OAuth 委托 scope 采用 `application:resource:action` 格式，例如目录中明确配置的 `smallokr:todo:read`，还需对应的租户资源授权。不要使用 Microsoft Graph 的权限名称来替代本平台目录，也不要假设仅批准 scope 就获得全部对象权限。
