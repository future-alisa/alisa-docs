# 数据：数据库、Redis 与数据归属

## 当前地址

| 数据服务 | 实际连接地址 | 接入方式 |
| --- | --- | --- |
| MySQL 公网 TCP | `27.tcp.vip.cpolar.cn:14681` | 本次由管理员指定；JDBC、MySQL CLI 或数据库客户端直接使用 TCP，不经过 HTTP 网关 |
| 账号库 | `jdbc:mysql://27.tcp.vip.cpolar.cn:14681/db_user` | `db_user` 来自当前账号服务本地配置；账号权限与线上库名以已分配配置为准 |
| 社区库 | `jdbc:mysql://27.tcp.vip.cpolar.cn:14681/db_community` | 社区与 transfer 的本地配置使用此库名；不是让其他服务直接读写其业务表 |
| 业务 Redis | `redis.redis.svc.cluster.local:6379` | Service ClusterIP 当前为 `10.96.53.54`，数据库索引由 `REDIS_DB` 配置 |
| Redis 内网接入入口 | `10.89.0.201:6379` | 当前 Traefik Service 暴露此 TCP 端口；入口资源和认证仍需按环境核验，集群内优先直连 Redis Service |
| Argo CD Redis | `argocd-redis.argocd.svc.cluster.local:6379` | Argo CD 内部缓存，不给业务服务共用 |
| PostgreSQL | 未确认实际服务地址 | 基础设施目录有记录，当前提供的 K8s Service 清单没有对应服务；不编造域名或管理网页 |

当前 Service 清单也未列出 MySQL Service，不能填写虚构的 `mysql.default.svc.cluster.local`。旧本地配置中出现的 MySQL 内网/组网 IP 不代表本次指定的公网入口发生变化；本页以 `27.tcp.vip.cpolar.cn:14681` 为开发接入地址。本次只更新文档，不改线上数据源或密码。

## Java / Spring Boot 接 MySQL

账号服务示例：

```properties
MYSQL_URL=jdbc:mysql://27.tcp.vip.cpolar.cn:14681/db_user?useUnicode=true&characterEncoding=UTF-8&serverTimezone=Asia/Shanghai
```

`MYSQL_USERNAME` 与 `MYSQL_PASSWORD` 由现有环境或 Secret 注入，不在上面的非敏感地址配置中重复定义。社区服务使用 `db_community`；新业务先分配自己的库与账号，不能直接复用账号库的管理员连接。TLS 与 `sslMode` 应匹配数据库实际支持的配置，不为了连接成功统一关闭证书验证。

CLI 可使用交互式密码提示：

```bash
mysql --host=27.tcp.vip.cpolar.cn --port=14681   --user="$MYSQL_USERNAME" --password --database=db_user
```

TCP 连通只验证入口，接入完成还需核对数据库名、表结构、账号授权、字符集、时区及连接池。此文档整理没有执行建库、迁移或生产数据读写。

## 数据由谁管理

| 数据 | 归属 | 跨服务访问 |
| --- | --- | --- |
| 用户、身份绑定、OAuth 和租户授权 | alisa-user | 调用统一账号、租户和授权 API |
| 社区、成员、资料、频道及讨论 | community-service / 对应模块 | 通过社区 API 访问，先做成员与角色检查 |
| 目标、阶段成果、待办 | SmallOKR 对应服务 | 使用 SmallOKR API，不直接操作另一服务的表 |
| 邮箱验证码与发送间隔 | 账号服务使用业务 Redis | 用 key 前缀与 TTL 管理，不作为永久业务数据库 |
| 门户目录、租户规划与部署申请 | Portal Go API | 当前写入 portal-data PVC 的 JSON 文件，不是已经接 PostgreSQL |
| 文件内容 | SeaweedFS S3 / Filer / Volume | 业务库保留引用与归属，详见 [存储接入](/operations/storage) |
| Kubernetes 对象与 Secret 等集群状态 | etcd | 仅由 Kubernetes 控制面管理，不是业务 MySQL 的替代品 |

## Redis 接入

集群中的账号服务可按实际 Service 配置：

```properties
REDIS_HOST=redis.redis.svc.cluster.local
REDIS_PORT=6379
REDIS_DB=0
```

`REDIS_PASSWORD` 由现有 Secret 注入。Redis DB 编号不是安全隔离边界，仍需账号权限、网络访问控制和业务 key 前缀。当前账号验证码有有效期、发送间隔和尝试次数控制，不在日志中打印验证码；不要把 Argo CD 的 Redis 配进业务应用。

## 表结构、迁移和租户数据

账号项目中 OAuth 表结构在 `alisa-user/src/main/resources/sql/oauth.sql`，租户增量在 `sql/tenant.sql`，后者要求先具备 OAuth 表结构。已有生产库先核对迁移记录与数据兼容性，不能把非幂等 SQL 在每次 Argo Sync 中重新执行。

SmallOKR 的租户模式还需要业务表 `tenant_id`、查询过滤与 `SMALLOKR_TENANCY_ENABLED` 一起切换。只给 token 加一个租户 ID 不会自动隔离 SQL；旧数据归属和跨租户越权验证必须先明确。详见 [租户管理办法](/operations/tenancy)。

## 备份与恢复顺序

- 分别备份 MySQL 数据、SeaweedFS 元数据与文件卷、Portal 数据 PVC，以及恢复所需的 Kubernetes 清单和凭据来源。
- 先确认数据和表结构对应的版本，再恢复应用、外部依赖及路由；Argo CD 回滚镜像不会自动回滚数据库。
- 恢复后验证登录、授权、资料引用和文件内容一致；不能只看 Pod Running 或数据库 TCP 可达。
