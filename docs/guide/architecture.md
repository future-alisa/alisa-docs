# 平台架构与服务职责

本页回答“平台由什么组成、每层做什么”。[中间件清单](/guide/middleware)、[交互流程](/guide/interactions)和[开发接入指南](/guide/development-integration)分别展开组件、请求链路和实际接入步骤。

## 阅读范围与状态

本文依据当前 `alisa-cloud`、`SmallOKR`、`ScienceCommunity`、`alisa-portal`、`alisa-sdk` 源码和管理员提供的基础设施清单整理。基础设施账号原文不进入文档仓库。

- **源码已接入**：找到了实际调用或配置，不表示当前线上实例一定已发布这份代码。
- **按配置启用**：代码存在，但仍需要功能开关、连接参数、表结构及运行环境配合。
- **基础设施记录有**：环境清单列出了组件，当前检查范围未必有业务调用。
- **计划或待确认**：不将设计设想、注释配置或仅有依赖声明当作已经落地的能力。

![Alisa 平台分层总览：公网入口分流到业务网关、门户与管理界面，业务服务按需使用注册配置、数据库、Redis、对象存储及邮件。](/diagrams/platform-overview.svg)

图是逻辑职责图，不是集群实时拓扑；底层组件的具体使用者见[依赖表](/guide/middleware#业务服务实际依赖哪些组件)。

## 平台分成五层

| 层次 | 当前组件 | 负责什么 | 不负责什么 |
| --- | --- | --- | --- |
| 客户端与开发入口 | SmallOKR 客户端、ScienceCommunity Web、Portal Web、文档站、可选 alisa-sdk | 展示、交互、调用 API、开发指引 | 保存服务端签名密钥、直接访问数据库或承担可信授权 |
| 外部接入与集群入口 | cpolar、Caddy、Traefik、Gateway API HTTPRoute | 公网接入、路径/Host 转发、TLS 与集群 Service 分流 | 代替业务服务判断某个用户是否能修改某条数据 |
| 应用入口与业务服务 | alisa-gateway、alisa-user、SmallOKR 三服务、社区与聊天服务、Portal Go API | API 路由、身份处理、账号与业务规则 | 承担所有基础设施的运行与持久化 |
| 中间件与外部依赖 | Nacos、MySQL、Redis、S3 兼容对象存储、SMTP；其他组件见清单 | 实例发现、配置分发、数据和文件存储、邮件投递 | 自动生成业务路由或替业务系统完成成员权限校验 |
| 构建与交付 | GitHub/环境中的 Gitea、Maven/npm/Go 构建工具、Registry、Argo CD、Kubernetes、Podman | 源码版本、构建镜像、分发、声明式部署、运行与探针 | 将一次镜像构建成功等同于用户业务请求全部成功 |

## 应用服务职责

| 服务/模块 | 归属 | 主要职责 | 接入方式 |
| --- | --- | --- | --- |
| `gateway-service` / alisa-gateway | alisa-cloud | 公共 API 入口、网关鉴权、身份头清理与生成、动态路由 | 入口 HTTPRoute 转发；Nacos 发现后端实例并读取业务路由配置 |
| `user-service` / alisa-user | alisa-cloud | 登录注册、身份提供者、资料和密码找回；按配置启用 OAuth、资源授权与租户能力 | `/api/v1/user/**`、`/api/v1/authorization/**` 及框架协议路径 |
| `target-service` | SmallOKR | 目标、阶段成果与对应业务访问检查 | `/target-service/api/v1/**`；服务 context-path 为 `/target-service` |
| `todo-service` | SmallOKR | 待办、重复任务、字典和分析 | `/api/v1/todo/**` |
| `trace-service` | SmallOKR | 当前源码的跟踪入口，并通过 OpenFeign 调用目标服务 | `/api/v1/trace/**`，内部按 `target-service` 注册名发现实例 |
| `community-service` | ScienceCommunity | 社区、成员、资料、频道讨论及按配置启用的附件存储 | `/community/**`；业务层执行成员/管理员/作者等权限判断 |
| `transfer-service` | ScienceCommunity | 在线用户、群组与旧 STOMP/SockJS 聊天入口 | `/api/users/**`、`/ws/**`；会话级身份需单独验证 |
| Portal Web + Go API | alisa-portal | 基础设施目录、部署清单生成和可选指标查询 | Web 同源代理 `/api/*`；当前管理员 API_TOKEN 体系独立于公共 user-service JWT |
| 文档站 | alisa-docs | 架构、接口索引、接入与发布说明 | 静态文件站；浏览地址由文档站实际部署决定 |

`alisa-gateway`、`alisa-user` 是模块/镜像/Deployment 名；`gateway-service`、`user-service` 是服务发现注册名。`lb://` 和 Feign 使用注册名，Kubernetes Service 则有自己的名称与命名空间。

## 公共库不是额外的微服务

| 公共能力 | 形态 | 使用方要做什么 |
| --- | --- | --- |
| alisa-common | Java JAR | 引入依赖，按需启用资源服务安全配置，使用身份上下文与公共类型 |
| alisa-authorization | Java JAR，由账号服务等承载接口 | 配置授权实现、应用/资源标识及相关表结构；调用侧仍要传递正确资源上下文 |
| alisa-notification | Java JAR，包含可替换邮件接口和 SMTP 实现 | 提供 MailSender/SMTP 配置，或以自定义 Bean 替换发送实现 |
| `@alisa-sdk/request` | TypeScript 请求库 | 配置 baseURL、超时及请求插件；调用方提供令牌获取方式 |
| `@alisa-sdk/log` | TypeScript 日志小模块 | 当前源码是控制台日志封装，不代表平台已具备日志采集、检索和告警系统 |

Maven/npm 包的构建与发布，和 OCI Registry 中的容器镜像分发是不同流程。当前 Java 公共库可先在 alisa-cloud 执行 `mvn install` 供同机开发使用；不能直接拿容器 Registry 地址作为 Maven 仓库地址。

## 两种网关、两种控制面

1. **Traefik / Gateway API** 将 Host 和路径转给集群 Service，服务于业务入口、Portal 及各管理界面。
2. **Spring Cloud Gateway** 处理其入口内的业务 API 路由与认证。

因此，不能假定 Argo CD、Nacos 控制台、Registry、WebDAV 和对象存储的所有流量都经过 alisa-gateway。管理界面及存储协议各自有认证边界。

- **请求数据面**：客户端请求经代理、网关、业务服务，访问数据库或存储。
- **服务配置控制面**：服务向 Nacos 注册，网关监听 Nacos 业务路由配置。
- **部署控制面**：Argo CD 读取 Git 中的期望状态，Kubernetes 运行对应镜像。

Nacos 的路由发布不会构建镜像；Argo CD 的 Deployment 同步也不会自动把运行中的 Nacos 业务配置替换成 Git 里的示例。

## 数据与权限归属

- 统一账号维护公共身份，业务项目通过公共用户标识建立自己的成员关系和业务权限。
- 社区、目标、待办等业务表留在所属业务系统；跨服务操作通过接口完成，不直接修改另一个服务的数据库。
- Redis 验证码、S3 文件、数据库元数据各有不同生命周期，不能互相当作备份或权威身份来源。
- 网关 token 校验、业务资源授权、租户隔离和管理平台登录是不同层次，须分别配置和验证。

## 项目与事实来源

| 事实 | 维护位置 | 文档如何引用 |
| --- | --- | --- |
| Java 控制器、DTO、权限判断与功能开关 | [alisa-cloud](https://github.com/future-alisa/alisa-cloud)、[SmallOKR](https://github.com/sunyuboalisa/SmallOKR)、[ScienceCommunity](https://github.com/future-alisa/ScienceCommunity) | 自动接口索引和源码链接 |
| Portal 目录数据、管理员认证、监控连接器 | [alisa-portal](https://github.com/future-alisa/alisa-portal) | 区分 Go API 当前实现与后续规划 |
| 客户端请求和日志库 | [alisa-sdk](https://github.com/future-alisa/alisa-sdk) | 以实际包 API 和安装来源为准 |
| 业务路由的运行值 | 对应环境的 Nacos namespace、Group、Data ID | 记录发布流程，不复制凭据 |
| 部署期望状态 | Argo CD 跟踪的 Git 仓库、分支及目录 | 记录镜像摘要、同步与回滚方式 |
| 密钥、账号与环境连接信息 | Secret/凭据管理与环境配置 | 只记录变量名和引用方式 |
