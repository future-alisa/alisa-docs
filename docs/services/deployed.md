# 已部署服务与公网入口

核验日期：2026-11-07。以 Argo CD 的实时 Deployment、HTTPRoute 和公网请求交叉核对；下面是本次核验快照，不是持续健康监控。HTTP 200 表示相应页面或探测可达，401 表示需要入口认证；两者都不等同于完整业务测试通过。

## 这次部署了什么

4 个 Argo CD 应用、8 个 Deployment 均达到 1/1 就绪，应用为 Synced / Healthy。

| Argo CD 应用 | 命名空间 | Deployment | 职责与外网入口 |
| --- | --- | --- | --- |
| alisa-infra | alisa-infra | alisa-gateway | 公共 API 网关，基址 `/alisa-gateway`，通过 Nacos 发现业务服务 |
| alisa-infra | alisa-infra | alisa-user | 统一账号，经网关 `/alisa-gateway/api/v1/user/**` 对外 |
| alisa-docs | alisa-infra | alisa-docs | [开发文档](https://alisa.vip.cpolar.cn/docs/) |
| alisa-portal | alisa-portal | web | [平台门户与管理界面](https://alisa.vip.cpolar.cn/) |
| alisa-portal | alisa-portal | api | 门户目录、租户、部署申请 API；同源 `/api/**`，管理请求需门户令牌 |
| science-community | science-community | web | [Science Community](https://alisa.vip.cpolar.cn/science)，含社区管理界面 |
| science-community | science-community | community | 社区、资料、成员、频道讨论，浏览器经 `/science/community-api/**` 访问 |
| science-community | science-community | transfer | 聊天与在线状态，客户端连接 `/science-chat/ws` |

SmallOKR 的 `target-service`、`todo-service`、`trace-service` 在源码和网关路由目录中，但本次 Argo CD 核验未发现对应 Deployment。不要把 Nacos 中存在一条路由等同于后端已部署。

## 用户站、管理后台和 API

用户站与社区管理的详细路径、权限和调用关系见 [Science Community 部署说明](/services/science-community)；门户前后端和管理员令牌边界见 [平台门户说明](/services/portal)。

| 入口 | 外网地址 | 本次检查 |
| --- | --- | --- |
| Alisa Portal · 平台管理 | [https://alisa.vip.cpolar.cn/](https://alisa.vip.cpolar.cn/) | 入口可达（200） |
| Alisa Docs | [https://alisa.vip.cpolar.cn/docs/](https://alisa.vip.cpolar.cn/docs/) | 入口可达（200） |
| Science Community | [https://alisa.vip.cpolar.cn/science](https://alisa.vip.cpolar.cn/science) | 入口可达（200） |
| Science Community · 社区管理 | [https://alisa.vip.cpolar.cn/science/community/settings](https://alisa.vip.cpolar.cn/science/community/settings) | 入口可达（200） |
| Science Community API | [https://alisa.vip.cpolar.cn/science/community-api/community/getAll](https://alisa.vip.cpolar.cn/science/community-api/community/getAll) | 入口可达（200） |
| Science Chat · 连接探测 | [https://alisa.vip.cpolar.cn/science-chat/ws/info](https://alisa.vip.cpolar.cn/science-chat/ws/info) | 入口可达（200） |
| Alisa Gateway / 统一账号 | [https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/user/health](https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/user/health) | 入口可达（200） |
| Alisa Portal API | [https://alisa.vip.cpolar.cn/api/health](https://alisa.vip.cpolar.cn/api/health) | 未登记 HTTP 入口 |
| Traefik | [https://alisa.vip.cpolar.cn/dashboard/](https://alisa.vip.cpolar.cn/dashboard/) | 需要访问认证（401） |
| Argo CD | [https://alisa.vip.cpolar.cn/argocd/](https://alisa.vip.cpolar.cn/argocd/) | 入口可达（200） |
| Nacos | [https://alisa.vip.cpolar.cn/nacos/](https://alisa.vip.cpolar.cn/nacos/) | 入口可达（200） |
| Registry | [https://alisa-registry.cpolar.top/v2/](https://alisa-registry.cpolar.top/v2/) | 需要访问认证（401） |
| SeaweedFS | [https://alisa.vip.cpolar.cn/fs/](https://alisa.vip.cpolar.cn/fs/) | 需要访问认证（401） |
| SeaweedFS Admin | [https://alisa.vip.cpolar.cn/fs-admin/](https://alisa.vip.cpolar.cn/fs-admin/) | 入口可达（200） |
| Gitea | [https://gitea-alisa.cpolar.top/](https://gitea-alisa.cpolar.top/) | 本次检查超时，待确认 |

PostgreSQL、MySQL 未登记 HTTP 管理页面。数据库的 TCP 连接信息、账号和密码通过环境配置维护，不放入公开文档或门户链接。

## 请求经过哪些组件

| 访问路径 | 转发方式 | 最终服务 |
| --- | --- | --- |
| `/`、门户页面 | Caddy → Traefik，保留路径 | alisa-portal/web:3000 |
| `/api/**` | 门户 Next.js 同源代理 | alisa-portal/api:8080 |
| `/docs/**` | Traefik 去掉 `/docs`，构建产物资源地址保留 `/docs/` | alisa-infra/alisa-docs:8080 |
| `/alisa-gateway/**` | Traefik 去掉 `/alisa-gateway` | alisa-gateway:8100 → Nacos 发现目标服务 |
| `/science/**` | Traefik 保留 `/science`，Next.js 的构建 basePath 同为 `/science` | science-community/web:3000 |
| `/science/community-api/**` | Next.js rewrite 到 `http://community:9091/community/**` | science-community/community:9091 |
| `/science-chat/**` | Traefik 去掉 `/science-chat` | science-community/transfer:9092 |

不同子路径的前缀处理不同，不能统一改成 Caddy `handle_path`。目前已有的 Caddy 转发可覆盖这些入口，无需为了登记链接改动服务器 Caddy 文件。

## 如何维护这份记录

公开入口快照保存在 [service-access.json](/service-access.json)，门户使用相同条目登记。新增服务时同时核对 Deployment、HTTPRoute、前端 basePath 与匿名/登录行为，再更新此页和门户目录；修改文档不会自动改写门户数据。

文档发布流程见 [镜像与 Argo CD](/operations/deployment)。源码服务目录仍见 [服务目录](/services/)，不能用它替代当前环境核验。
