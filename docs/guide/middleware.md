# 中间件与基础设施清单

本页区分“环境中有组件”“源码已使用”和“配置后才启用”。当前没有重新探测全部服务器端口或核验每个组件的运行健康，不能把下面的清单当成实时监控。

## 接入与运行基础设施

| 组件 | 证据/状态 | 职责 | 开发时怎么对接 |
| --- | --- | --- | --- |
| cpolar | 基础设施清单记录 | 把公网 HTTPS 请求引入现有服务器接入链路 | 应用只使用环境约定的外部 base URL，不在业务代码中调用隧道管理接口 |
| Caddy | 基础设施记录有路径代理、Host 转发与内部 TLS 信任配置 | 在公网统一入口按路径分流，处理需要的路径/Host/响应重写 | 新入口由运维配置；先说明外部前缀、转发目标和签名协议需求 |
| Traefik + Gateway API | Git 中有 HTTPRoute 等清单，既有服务已按该方式发布 | 将集群入口流量转给对应 Service | 提供 Service 名、端口、域名和路径，确认跨命名空间引用策略 |
| Kubernetes / kind | 既有 Argo CD 应用运行平台；基础设施记录为 Windows/Podman 环境内的 Kubernetes | 调度容器、Service、ConfigMap/Secret、探针与存储卷 | 交付镜像和声明式清单，业务服务不向浏览器暴露 kubeconfig |
| Podman | 既有服务器容器运行/构建环境记录 | 运行服务器侧容器和相关构建工作 | 开发可用对应容器工具；Podman、Kubernetes 与 Registry 不是同一组件 |
| Nginx | 文档站镜像使用的静态运行时，运行状态以发布结果为准 | 提供静态页面、资源和健康检查 | 构建 `DOCS_BASE` 与入口重写配套，不能据示例推断已经上线 |

## 服务发现、配置和数据

| 组件 | 证据/状态 | 当前作用 | 不要误认为 |
| --- | --- | --- | --- |
| Nacos Discovery | Java 服务有 discovery 配置，Feign/网关按注册名访问后端 | 服务实例注册、发现及实例地址变化 | 注册一个服务就自动生成自定义 API 网关路径 |
| Nacos Config | alisa-gateway 有配置监听与路由编译代码 | 分发 `ALISA_GATEWAY / alisa-gateway-routes.yaml` 中的业务路由 | 所有微服务配置都已经迁入 Nacos，或 Nacos 替代 GitOps/Secret |
| MySQL | Java datasource/MyBatis 配置、账号及业务 Mapper/SQL | 账号和业务关系型数据；可选授权/OAuth/租户持久化按模块配置 | 所有服务必须共用同一个库或相互直接访问表 |
| Redis | `VerificationCodeService` 通过 StringRedisTemplate 和 Lua 使用 | 邮箱重置验证码、发送间隔限制、尝试次数与原子消费 | 全平台 JWT session、即时注销、通用分布式锁和缓存都已实现 |
| SeaweedFS / S3 兼容存储 | 基础设施有 SeaweedFS 的 S3、Filer、Master、WebDAV 等入口；社区源码有 S3 兼容适配 | 文件对象、附件和封面的存储与访问 | Java 依赖 MinIO SDK 就证明环境部署了 MinIO 服务端 |
| SMTP / 邮件提供方 | alisa-notification 和账号服务已有邮件调用 | 找回密码等邮件投递 | 邮件接口模块本身是独立微服务，或仅有域名就代表投递已经验证 |
| PostgreSQL | 基础设施清单记录有；Portal 文档列为演进方向 | 可作为后续关系型持久化方案，实际使用者须单独确认 | Portal 当前数据已经保存在 PostgreSQL |

### Nacos 有两个不同的分组概念

- **服务发现**使用 discovery namespace 和发现 group；同名服务在不同 namespace/group 不一定能互相发现。
- **动态路由配置**使用 config namespace、Group `ALISA_GATEWAY` 和 Data ID `alisa-gateway-routes.yaml`。

Group `ALISA_GATEWAY` 是网关配置所在的组，不自动成为后端服务的发现分组。当前网关配置客户端复用 discovery 中的服务器地址、namespace 与凭据。

## 构建、镜像和部署

| 组件 | 证据/状态 | 主要职责 | 开发接入点 |
| --- | --- | --- | --- |
| GitHub | 当前源码和 Argo CD 应用引用该来源 | 版本、评审、CI 和 GitOps 清单 | 提交代码与部署期望状态，记录对应源码提交 |
| Gitea | 基础设施清单记录有入口 | 可承载内部 Git 仓库或镜像源代码 | 仓库/凭据需显式接入，不能假定已自动镜像所有 GitHub 仓库 |
| OCI Registry | 当前网关和 Portal 发布记录使用私有 Registry | 保存、分发容器镜像标签和摘要 | 构建后推送；集群用 imagePullSecret 拉取；凭据不进 Git |
| Argo CD | 当前应用有 Git 来源、同步及健康记录 | 将 Git 声明的资源应用到集群并持续比较 | 配置 repo、revision、path、destination；同步后核对实际 Pod |
| Maven / npm / Go 工具链 | 各项目已有构建脚本 | 依赖解析、测试、编译与打包 | 以项目锁文件和受支持版本构建；不是线上请求链路中的中间件 |

当前网关的 PreSync Job 把构建、推镜像、初始化 Nacos 与 Deployment 更新串在一次 Argo CD 同步中。实际编译发生在 Job 中；这不表示 Argo CD 本身替代 CI 或镜像构建工具。

## 监控和“尚不能认定已落地”的能力

| 能力 | 当前能确认的内容 | 接入前还要确认 |
| --- | --- | --- |
| Prometheus | Portal Go API 有可选即时指标查询连接器 | `PROMETHEUS_URL`、可选令牌、可达性及实际指标；部分查询需要 node-exporter/kube-state-metrics |
| Sentinel | SmallOKR 部分模块声明了依赖，部分服务有注释配置 | 控制台、运行时规则来源和限流/熔断验证；仅有 starter 不能证明防护有效 |
| Seata | 检查到注释中的历史配置 | 服务端、事务模式、业务接入和回滚验证；不据此承诺跨库原子事务 |
| 统一日志、告警、分布式追踪 | SDK 有控制台日志封装，Portal 文档说明当前指标能力有限 | 未在本次范围证明已建立日志采集/检索、告警和 Trace 全链路 |
| 消息队列与搜索引擎 | 当前检查的几个服务未找到足够接入证据 | 不将 Kafka、RabbitMQ、Elasticsearch 等列为平台已部署的既定依赖 |

## 业务服务实际依赖哪些组件

| 使用者 | 源码可确认的直接依赖 | 可选或需环境确认 |
| --- | --- | --- |
| alisa-gateway | Nacos Discovery；开启动态路由时使用 Nacos Config | 入口代理、JWT 环境配置及后端服务实例 |
| alisa-user | MySQL、Redis、邮件发送接口/SMTP | 外部身份提供者、OAuth、授权与租户能力的开关及表结构 |
| target-service / todo-service | MySQL、Nacos、alisa-common | 已配置的资源授权/令牌内省接口；租户模式需表结构配合 |
| trace-service | Nacos、OpenFeign 调用 target-service、资源访问检查 | 是否另接数据存储以服务真实实现为准，不从名称推断它是链路追踪系统 |
| community-service | MySQL、Nacos、社区业务权限检查 | S3 环境配置与对象存储；使用 MinIO Java SDK 调 S3 兼容协议 |
| transfer-service | Nacos、MyBatis/数据库配置、STOMP/SockJS 相关实现 | 不能把旧内存会话机制认定为跨副本可靠消息系统 |
| Portal Go API | 当前 JSON 文件存储、管理员 API_TOKEN 认证 | 可选 Prometheus；PostgreSQL、多用户 OIDC/RBAC 属于需单独核验的演进 |
| alisa-docs | 构建期 Node/npm，运行期静态服务器 | 不需要 Nacos、数据库、业务 JWT_SECRET 或 SMTP |

## 对象存储的几个入口不要混用

SeaweedFS 的 Master、Volume、Filer、S3 和 WebDAV 面向不同协议与职责。业务附件服务当前通过 **S3 协议**读写，不把 Filer 管理页面地址直接当作 `S3_ENDPOINT`，也不把 WebDAV 认证当作 S3 Access Key。

运行时是否确实访问 SeaweedFS 由 `S3_ENDPOINT` 决定。新环境先验证 bucket、读写策略、预签名 URL 和反向代理行为，再交付业务功能。具体链路见[文件交互流程](/guide/interactions#附件与封面上传和读取)。

## 证据入口

- [账号验证码与 Redis](https://github.com/future-alisa/alisa-cloud/blob/main/alisa-user/src/main/java/com/alisa/user/service/VerificationCodeService.java)
- [SMTP 自动配置](https://github.com/future-alisa/alisa-cloud/blob/main/alisa-notification/src/main/java/com/alisa/notification/mail/MailNotificationAutoConfiguration.java)
- [网关动态路由代码](https://github.com/future-alisa/alisa-cloud/tree/codex/alisa-infra-argocd/alisa-gateway/src/main/java/com/alisa/routes)
- [社区对象存储适配](https://github.com/future-alisa/ScienceCommunity/blob/main/science_community/community_service/src/main/java/com/alisa/service/ObjectStorageService.java)
- [Portal 当前存储、认证和可选监控说明](https://github.com/future-alisa/alisa-portal/blob/main/README.md)
