# Science Community：用户站与社区管理

项目：[ScienceCommunity](https://github.com/future-alisa/ScienceCommunity)。当前 Argo CD 应用 `science-community` 读取 `codex/k8s-deploy` 分支的 `deploy/kubernetes`，运行在同名命名空间。2026-11-07 核验 web、community、transfer 三个 Deployment 均 1/1 就绪。

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
