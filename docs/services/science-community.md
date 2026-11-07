# Science Community API 与应用

项目：[ScienceCommunity](https://github.com/future-alisa/ScienceCommunity)。当前 Argo CD 应用 `science-community` 读取 `codex/k8s-deploy` 分支的 `deploy/kubernetes`，运行在同名命名空间。2026-11-07 核验 web、community、transfer 三个 Deployment 均 1/1 就绪。

## 统一服务概览

社区、资料、频道讨论、聊天与在线状态在本项目下统一介绍；后台仍由 community-service、transfer-service 与 Next.js Web 协作，不是合并进一个进程。

| 入口类型 | 完整地址 | 说明 |
| --- | --- | --- |
| 用户站根地址 | `https://alisa.vip.cpolar.cn/science` | 页面导航与用户交互 |
| 社区 HTTP API 根地址 | `https://alisa.vip.cpolar.cn/science/community-api` | Next.js 同源代理到 community-service |
| 聊天 / 在线状态 HTTP 根地址 | `https://alisa.vip.cpolar.cn/science-chat` | 独立 HTTPRoute 到 transfer-service |
| SockJS / STOMP 连接 | `https://alisa.vip.cpolar.cn/science-chat/ws` | 由 SockJS/STOMP 客户端按此基址协商传输；不假定原生 WebSocket 路径与 SockJS 根路径相同，仍需会话身份验证 |
| 统一账号 API 根地址 | `https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/user` | 社区应用复用公共账号身份 |

## 按资源调用

| 资源 | HTTP 请求（完整 URL） | 访问说明 |
| --- | --- | --- |
| 社区 | `GET https://alisa.vip.cpolar.cn/science/community-api/community/getAll` | 本次验证公开列表可达 |
| 我的社区 | `GET https://alisa.vip.cpolar.cn/science/community-api/community/getAllByUser` | 用户身份与业务权限 |
| 当前社区访问能力 | `GET https://alisa.vip.cpolar.cn/science/community-api/communityuser/access?communityId={communityId}` | 用于取得当前用户的社区角色/能力，不能由前端自填角色 |
| 资料文档 | `GET https://alisa.vip.cpolar.cn/science/community-api/document/getAllByCommunityId?communityId={communityId}` | 成员/可见性与实际资源权限 |
| 频道 | `GET https://alisa.vip.cpolar.cn/science/community-api/channel/getAllByCommunityId?communityId={communityId}` | 社区成员与频道能力 |
| 频道讨论记录 | `GET https://alisa.vip.cpolar.cn/science/community-api/channel/{channelId}/messages` | 持久化讨论与频道访问检查 |
| 文件上传 | `POST https://alisa.vip.cpolar.cn/science/community-api/storage` | multipart file、用途与大小检查，服务端连接对象存储 |
| 在线用户 | `GET https://alisa.vip.cpolar.cn/science-chat/api/users/online` | 旧 transfer HTTP 接口；身份与访问策略需独立核查 |
| 用户群组 | `GET https://alisa.vip.cpolar.cn/science-chat/api/users/groups/{username}` | 旧 transfer HTTP 接口，不因与社区同一项目就自动具有同样的成员授权 |
| 聊天连接探测 | `GET https://alisa.vip.cpolar.cn/science-chat/ws/info` | 只验证 SockJS 元信息，不验证登录或消息投递 |

社区的持久化频道讨论 API 与 transfer 的旧 STOMP 通道是不同实现。`/science-chat` 当前直达 transfer，不自动经过 Spring Gateway 的 JWT 校验；上线客户端需单独验证会话身份、授权和订阅范围。完整控制器索引见 [社区资源](/api/generated/community) 与 [聊天/在线状态](/api/generated/transfer)。

## 权限与请求示例

受保护社区 API 使用业务 Bearer 凭据，并由服务端检查成员、管理员或作者权限；不能用一个前端 role 字段代替授权。社区角色不是统一业务租户角色，也不是 Portal 管理令牌。详情见 [认证与授权](/operations/authentication)。

已验证的公开读取请求：

```http
GET https://alisa.vip.cpolar.cn/science/community-api/community/getAll
Accept: application/json
```

需要登录的读取请求示例（communityId 用自己的合法资源 ID 替换）：

```bash
curl -H "Authorization: Bearer $ACCESS_TOKEN"   'https://alisa.vip.cpolar.cn/science/community-api/document/getAllByCommunityId?communityId=YOUR_COMMUNITY_ID'
```

资源字段、创建/更新请求体与返回模型以 DTO 为准，不自动宣称支持 Microsoft Graph 的 scope 名称、OData 查询或统一分页。文件读写对接见 [存储模块](/operations/storage)，关系数据见 [数据模块](/operations/data)。

## 直接访问

| 用途 | 地址 | 访问要求 |
| --- | --- | --- |
| 用户站 | [Science Community](https://alisa.vip.cpolar.cn/science) | 可打开用户站，部分业务需登录 |
| 社区列表 | [浏览社区](https://alisa.vip.cpolar.cn/science/community) | 页面和公开列表可达 |
| 社区管理 | [我的社区 / 社区管理](https://alisa.vip.cpolar.cn/science/community/settings) | 需登录，管理能力取决于选中社区的角色 |
| 登录 | [登录页面](https://alisa.vip.cpolar.cn/science/signin) | 使用统一账号能力 |
| 社区 API 探测 | [公开社区列表](https://alisa.vip.cpolar.cn/science/community-api/community/getAll) | JSON 接口，不是后台网页 |
| 聊天连接探测 | [SockJS info](https://alisa.vip.cpolar.cn/science-chat/ws/info) | JSON 探测，不代表已验证消息收发 |

“后台管理”不是另一个 `/admin` 应用，而是用户站里的 `/science/community/settings` 页面。进入后可选择自己加入的社区，也支持 `?communityId=社区ID` 定位。拥有者和管理员可按权限管理成员、角色、频道成员、资料及封面；普通成员不会因此获得管理权限。

## 三个工作负载

| Deployment | 服务注册名 / 模块 | Service 端口 | 职责 |
| --- | --- | --- | --- |
| web | App，Next.js | web:3000 | 用户界面、社区管理、同源社区 API 代理 |
| community | community-service | community:9091 | 社区、成员、资料、频道与持久化讨论；共享账号与授权能力按配置接入 |
| transfer | transfer-service | transfer:9092 | 在线状态、用户群组、旧 STOMP / SockJS 通道 |

## 前端开发与发布对接

生产前端构建使用这些非敏感入口设置：

```properties
NEXT_PUBLIC_BASE_PATH=/science
NEXT_PUBLIC_API_BASE_URL=/science/community-api
NEXT_PUBLIC_USER_API_BASE_URL=https://alisa.vip.cpolar.cn/alisa-gateway
NEXT_PUBLIC_CHAT_URL=https://alisa.vip.cpolar.cn/science-chat/ws
COMMUNITY_API_PROXY_TARGET=http://community:9091/community
```

`NEXT_PUBLIC_*` 和 basePath 在构建时写入前端，修改后需要重新构建镜像；`COMMUNITY_API_PROXY_TARGET` 是 Next.js 服务端 rewrite 目标，不要把集群内部 DNS 地址作为浏览器 API 地址。上面的 `community` 是同一命名空间的 Kubernetes Service 名。

社区请求例如 `/science/community-api/community/getAll`，会代理到 `http://community:9091/community/community/getAll`。账号请求仍走 `/alisa-gateway/api/v1/user/**`。聊天请求由独立 `/science-chat` HTTPRoute 去前缀后送到 transfer，不经过社区页面的 API rewrite。

外部浏览器入口与 Nacos 发现服务是两层能力，Nacos 不会自动给前端增加网页路径。详情见 [组件如何交互](/guide/interactions)、[社区接口](/api/generated/community)、[聊天接口](/api/generated/transfer)。

## 本次验证边界

已验证用户站、社区管理页面、公开社区列表接口与 SockJS info 可达。未使用真实用户执行登录、社区成员变更、文件上传或消息发送，不能把匿名探测当成这些操作已经联调通过。S3 凭据、JWT_SECRET、数据库配置只通过服务端配置维护。
