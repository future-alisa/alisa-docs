# Alisa Portal：平台门户与管理后台

项目：[alisa-portal](https://github.com/future-alisa/alisa-portal)。外网入口是 [平台门户](https://alisa.vip.cpolar.cn/)，Argo CD 应用与命名空间均为 `alisa-portal`，GitOps 路径为 `deploy/overlays/production`。

## 前后端职责

| Deployment | Service | 职责 |
| --- | --- | --- |
| web | web:3000 | Next.js 工作台、服务资源、租户、部署中心、监控页面；代理同源 `/api/**` |
| api | api:8080 | Go API，目录与操作记录持久化、租户及配额校验、生成部署清单 |

2026-11-07 两个 Deployment 均 1/1 就绪。门户后端数据放在 `portal-data` PVC；当前是 JSON 文件单实例存储，不要因为环境有 PostgreSQL 就声称已迁移数据库。

## 后台怎么进入

打开根地址，在「连接设置」填写当前门户管理员令牌，再查看服务资源和管理页面。令牌只保存在页面内存；这里使用独立 `API_TOKEN`，不是 Science Community 的业务 JWT，不应替换 `.env` 中的 JWT_SECRET 来接入门户。

| 地址 | 用途 |
| --- | --- |
| `https://alisa.vip.cpolar.cn/` | 平台门户与管理界面 |
| `https://alisa.vip.cpolar.cn/api/health` | 无需管理员令牌的健康探测 |
| `https://alisa.vip.cpolar.cn/api/state` | 服务目录、租户、部署申请、操作记录，需门户令牌 |

门户管理界面与 [Science Community 社区管理](/services/science-community) 是两套不同用途的后台。门户的 Argo CD、Nacos、Traefik 等目录链接只是入口导航，目标服务仍执行自己的登录与访问控制。

统一账号、OAuth2 应用审批和资源授权由 [Alisa Admin](https://alisa.vip.cpolar.cn/admin/) 管理，接入流程见 [OAuth2 接入与联调](/operations/oauth2)。

## 服务目录与真实基础设施的边界

目录保存名称、分类、HTTP(S) 地址和说明，登记或移除记录不会部署、删除 Kubernetes 服务。当前 API 只有登记和移除操作，没有目录条目更新接口；更改已有条目时先登记新值、确认保存成功，再移除旧记录，避免先删后加丢失入口。

服务条目的 `unverified` 状态表示门户没有接入实时探测。即使说明中记录某天入口检查通过，也不能把它解释成持续监控健康。指标是否可用取决于 Prometheus 配置；部署中心生成 YAML，不会直接执行集群发布。

## 更新与恢复

目录变更写入 PVC，会立即反映在已连接的门户中，不需要重建前端镜像。文档与门户的公共入口快照见 [已部署服务](/services/deployed)，实际目录仍以受保护的 `/api/state` 为准。

修改门户程序才需要构建镜像并同步 Argo CD。应保留现有 `portal-auth`、`portal-registry-auth` 与 PVC，遵循 Application 的 Secret 差异忽略配置，不能将实际认证内容写入 Git。
