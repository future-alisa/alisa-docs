# 组件如何交互

这里按一次具体操作说明各组件的先后关系。地址使用逻辑名称，真实域名、端口映射和凭据由环境提供。

## 普通业务请求

```text
客户端携带 Bearer token
  → 外部入口：cpolar / Caddy
  → Traefik：按 Host 和 HTTPRoute 分流
  → alisa-gateway：匹配路由、清理伪造身份头、执行适用的认证流程
  → Nacos Discovery 对应的业务实例
  → 服务自身的身份/资源访问检查与业务逻辑
  → MyBatis / 数据库或所需外部依赖
  → HTTP 响应返回客户端
```

1. 客户端选择环境的网关 base URL，不把 Nacos 注册名当成浏览器域名。
2. 外部 `/alisa-gateway` 等代理前缀由入口层按配置处理，服务自己的 context-path 仍需保留。
3. 网关中的 `lb://todo-service` 表示通过发现机制解析实例，不是调用一个叫 `lb` 的独立服务。
4. 后端应执行适用的 token 和业务权限校验；能经过网关不代表能访问任意一条业务数据。
5. 业务服务返回的 403、参数错误或数据库错误不能靠增加网关公开路径修复。

管理平台、Registry、Nacos 控制台、WebDAV 等入口可被接入层直接分流，不自动使用 alisa-gateway 的业务 JWT 规则。

## 登录、身份与资源权限

### 公共账号登录

```text
客户端 → 网关公开登录路径 → user-service
                              ├─ 本地账号 / 配置的 IdentityProvider
                              ├─ 账号和绑定数据
                              └─ 由相应流程签发访问凭据
客户端保存访问凭据 → 后续请求 Authorization: Bearer ...
```

当前公共 JWT 的 `JwtUtil` 使用 HS256，读取 `jwt.secret`，配置来源为 `JWT_SECRET`，源码会先按 Base64 解码再取得 HMAC 密钥。接入端应按现有实现对齐，而不是自行更换密钥编码或算法。

客户端通常不应掌握签名密钥；本地解码 token 只能得到未经信任的展示信息，不代表验签。OAuth 流程可能使用不透明 token，不能假定所有访问凭据都能用 JWT 解码器解析。

### 业务服务校验

- 启用 `alisa.security.enabled=true` 后，公共资源服务组件可从 Bearer token 建立请求身份，并提供 `ResourceAccess`。
- 业务操作仍需检查资源 ID、动作、成员关系等条件。OAuth/委托凭据还可能调用内省与授权接口。
- 只有后端确实部署独立 Bearer 校验时，网关对应路由才可以使用 `delegated-ready: true`。
- 旧的 Header 上下文路径与启用独立校验的路径有不同信任边界，不能只引入 JAR 就认为所有直连请求都已安全。
- `UserContext` 是请求线程上下文，需在请求结束清理；异步任务、定时任务和线程池不能假定自动继承它。

租户模式还要求相应成员关系、令牌上下文与业务表结构，不是单独增加一个 `tenantId` 字段就完成隔离。

### Portal 管理员登录是另一个边界

当前 Portal Go API 使用管理员 `API_TOKEN`。它不是公共 `JWT_SECRET`，也不是 user-service 颁发的业务访问令牌。Portal 的目录租户/配额记录不能直接当作业务用户租户隔离已经生效的证据。

## 邮箱重置验证码

```text
客户端请求发送验证码
  → user-service 校验请求与账号条件
  → Redis：发送间隔限制、验证码 TTL、尝试次数
  → alisa-notification 邮件接口
  → JavaMailSender / SMTP → 收件邮箱

客户端提交验证码
  → Redis Lua：比较、累计尝试、原子消费
  → user-service 更新相应凭据
```

源码默认验证码有效期为 5 分钟、发送间隔为 60 秒，允许最多 5 次尝试；实际值以环境和代码为准。邮件发送失败会清理本次相关状态。Redis 在这条链路中提供临时状态，不取代 MySQL 中的账号记录。

这里说明组件协作，不进行任何真实账号密码或环境密钥变更。

## 服务间调用

当前 traceservice 的 `MyFeginClient` 声明 `@FeignClient("target-service")`，按服务注册名发现目标服务。

```text
trace-service 的当前请求
  → OpenFeign 请求拦截器：按现有配置转发 Authorization / 身份上下文
  → Nacos 实例发现 + 客户端负载均衡
  → target-service 的 context-path 与控制器路径
  → 目标接口再次执行适用的校验
```

开发时需同时核对 namespace、发现 group、服务注册名、路径、请求参数与 token 上下文。源码中存在 Feign 方法不等于该调用已完成参数与权限的端到端联调；当前链路也不能被当成系统级分布式追踪平台。

非用户触发的服务任务应采用明确设计的服务身份流程，不能从浏览器拿一个管理员令牌硬编码在后端。

## 附件与封面上传和读取

社区源码的 `StorageController` 与 `ObjectStorageService` 已有 S3 兼容适配。

```text
浏览器上传 file / communityId / purpose
  → community-service 检查登录、成员/管理员条件、用途、类型和大小
  → 使用服务端 S3 凭据上传对象
  → S3 兼容存储中的 bucket/object
  → 返回文件引用信息

浏览器请求读取地址
  → community-service 检查引用和访问范围
  → 服务端签发短时预签名 GET URL
  → 浏览器访问该 URL（可能经过配置的公网代理）
```

当前源代码中附件上限为 20 MiB、封面上限为 5 MiB；读取地址预签名有效期为 600 秒。还有 Spring multipart、入口代理和对象存储自身的限制，应一起核验，不能只改变前端限制。

`S3_ENDPOINT` 是服务端实际连接/签名使用的地址；`S3_PUBLIC_URL` 用于文件引用；可选隧道/下载代理将签名 URL 暴露到客户端可达的地址。**S3 的 Host、路径和查询参数参与签名，代理必须按实现恢复签名时的 Host 并正确去掉代理前缀**，不能当成普通无签名静态路径随意改写。

S3 Access Key/Secret Key 只在服务端配置，不进入前端 `NEXT_PUBLIC_*` 变量。返回一个 URL 字符串不自动等于任何人都可以匿名下载，业务侧仍要验证文件访问策略和链接过期行为。

## 路由热更新

```text
维护者在 Nacos 发布完整业务路由列表
  → 每个网关配置客户端收到变化
  → 解析 YAML、检查 ID、编译全部候选路由
  → 成功后替换快照并刷新路由缓存
  → 新请求按新路由匹配
```

这条流程不需要构建镜像或重启网关。错误候选配置被拒绝，运行中的实例保留上一份有效快照；首次启动拿不到有效配置时则启动失败。多实例各自接收更新，不能据一次控制台“发布成功”就保证所有实例已同时生效。

新增业务路径仍需有真实已注册的后端实例；路由正确但没有可用实例时可能得到 503。

## 应用发布

```text
源码 Git 提交
  → 构建工具 / CI 或集群内构建 Job：测试、打包
  → Registry：保存镜像标签与摘要
  → 部署 Git：记录要运行的镜像和资源配置
  → Argo CD：读取 Git、比较差异、同步资源
  → Kubernetes：拉取镜像、启动 Pod、执行探针
  → 发布验证：实际镜像、就绪状态、路由与授权业务请求
```

当前公共网关通过 PreSync Job 把部分步骤串联；Portal 有自己的发布配置；文档站需单独接入。Argo CD 的 Synced 表示声明与集群状态的比较结果，Healthy 表示其健康评估，二者都不代替带真实权限和参数的业务联调。
