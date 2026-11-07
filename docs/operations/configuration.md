# 配置归属与开发对照

此页列配置项、消费者和约定。管理员明确提供的实际地址见 [存储](/operations/storage)、[数据](/operations/data) 和 [认证](/operations/authentication)；不保存密码、访问令牌或密钥。服务的 `example.env` 和当前配置类决定实际变量名；第三方组件自己的容器配置不一定使用同一组名称。

## 应用读取的环境配置

| 配置项/前缀 | 谁读取 | 用途与接入注意 |
| --- | --- | --- |
| `NACOS_SERVER_ADDR`、`NACOS_NAMESPACE` | 相关 Java 服务，网关动态配置客户端 | Nacos 地址和 namespace ID；同环境内按发现范围配置 |
| `NACOS_USERNAME`、`NACOS_PASSWORD` | 对应 Nacos 客户端 | 读取/注册所需权限；空值是否可用由环境认证策略决定 |
| `spring.cloud.nacos.discovery.group` | 使用发现机制的服务 | 发现分组，不能和网关配置 Group 混为一谈；显式配置时需客户端和服务端一致 |
| `GATEWAY_NACOS_ROUTES_*` | alisa-gateway | 动态路由开关、Data ID、配置 Group；不代表后端服务功能开关 |
| `JWT_SECRET` → `jwt.secret` | 相关 Java 签发/校验端 | 按当前 JwtUtil 的 Base64/HMAC 实现对齐；绝不进入前端构建 |
| `MYSQL_URL`、`MYSQL_USERNAME`、`MYSQL_PASSWORD` | 各服务自己的 datasource | 每个服务环境决定其数据库，不把同名变量当作所有服务共享同一实例/库的证明 |
| `REDIS_HOST`、`REDIS_PORT`、`REDIS_PASSWORD`、`REDIS_DB` | 当前账号服务等实际 Redis 使用方 | 验证码等临时状态；配合业务 key 前缀隔离 |
| `MAIL_HOST`、`MAIL_PORT`、`MAIL_USERNAME`、`MAIL_PASSWORD`、TLS/SSL 配置 | JavaMailSender 与通知模块 | 使用邮件提供方的协议参数；与外部 Web 邮件页面入口不是同一个概念 |
| `AUTHORIZATION_ENABLED`、`OAUTH_ENABLED`、`TENANCY_ENABLED` | 当前账号服务 | 可选能力开关，还需要相应的协议参数、策略或表结构 |
| `alisa.security.enabled`、`application-id`、`resources.*` | 业务资源服务公共安全组件 | 配置身份校验与资源访问能力；并不代替业务自身权限规则 |
| `S3_ENDPOINT`、`S3_BUCKET`、`S3_REGION` | community-service 的对象存储适配 | 服务端连接/签名目标和对象存储范围 |
| `S3_ACCESS_KEY_ID`、`S3_SECRET_ACCESS_KEY` | 对象存储适配 | 服务端凭据，不放到浏览器或 API 响应中 |
| `S3_PUBLIC_URL`、`S3_TUNNEL_URL`、`S3_DOWNLOAD_PROXY_URL` | 当前社区文件引用与预签名流程 | 各自用途不同，代理需满足签名的 Host/路径/查询规则 |
| `API_TOKEN`、`DATA_FILE`、`LISTEN_ADDR` | Portal Go API | 管理员访问令牌、JSON 存储路径、监听地址；与 JWT_SECRET 独立 |
| `PROMETHEUS_URL`、`PROMETHEUS_TOKEN` | Portal Go API 的可选连接器 | 后端查询指标，未配置时不能把空结果伪装成健康数据 |
| `DOCS_BASE` | alisa-docs 构建 | 静态站资源和文档路径的前缀，不是业务 API base URL |

## 放在哪里

| 场景 | 建议归属 |
| --- | --- |
| 本地个人开发 | 服务实际支持的本地环境加载方式；敏感文件由 Git 忽略 |
| Kubernetes 非敏感配置 | ConfigMap 或清单中适合公开的环境项 |
| Kubernetes 凭据 | 已有 Secret 或对应凭据系统，由权限允许的维护流程注入 |
| 路由热更新 | 指定 namespace 中的 Nacos 配置；完整列表与历史回滚 |
| 镜像和副本等部署期望 | Argo CD 跟踪的 Git 来源 |
| 前端公开环境 | 仅客户端确实需要且可公开的 base URL、功能展示设置等 |

## 变更与生效

- VitePress 的 Markdown 在开发服务器中通常热更新；构建期 `DOCS_BASE` 变化需要重新构建站点。
- 当前网关的 Nacos 业务路由有专门监听器；不能据此推断所有 `.env`、ConfigMap 或 Secret 变化都会自动刷新应用 Bean。
- 环境变量注入的值通常在进程启动时读取。更换 ConfigMap/Secret 内容后是否需要滚动更新，按服务真实加载机制判断。
- JWT、资源客户端、SMTP、S3、Portal 管理员令牌是不同用途的凭据，不能为了“统一配置”互相复用。
- 本次文档整理不轮换任何已有密钥；需要轮换时应另行设计签发端、验证端与仍有效令牌的迁移流程。

## 如何确认配置已接对

先确认服务实际加载了哪个 profile、Secret/ConfigMap 引用和配置项，再检查下游可达性及业务操作。排查时可以比较配置来源和一致性，不在日志、截图或公开文档中输出完整密钥、访问令牌、验证码或预签名链接。
