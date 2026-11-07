# 开发时如何接入平台

先选定服务的职责和环境，再接入它实际需要的能力。下面的配置是文档样例，不会读取、生成或修改现有 `.env`，也不包含可用于线上认证的真实值。

## 1. 定义边界和标识

新增服务先写清楚：

| 信息 | 示例/说明 |
| --- | --- |
| 业务归属 | 属于 SmallOKR、ScienceCommunity，或新的独立业务项目 |
| 模块/镜像/Deployment 名 | 例如 `example-service`，实际可以与注册名不同 |
| Nacos 注册名 | `spring.application.name`，例如 `example-service` |
| 对外 API 前缀 | 如 `/api/v1/example/**`，避免抢占已有账号或业务路径 |
| servlet context-path | 是否有额外前缀；网关 URI 不自动消除这个前缀 |
| 应用/资源标识 | 独立于服务注册名，用于令牌 audience/授权范围等接入配置 |
| 数据归属 | 自有业务表和迁移方案，不直接写别的服务的数据库 |

## 2. Java 公共能力与配置

当前 Java 项目使用 Java 17、Spring Boot/Spring Cloud。跟随项目父 POM 管理版本，不单独混入不兼容版本的 starter。

```xml
<dependency>
  <groupId>com.alisa.cloud</groupId>
  <artifactId>alisa-common</artifactId>
  <version>0.0.1-SNAPSHOT</version>
</dependency>
```

本地先在相同源码版本的 alisa-cloud 中执行 `mvn install`。自动构建环境还需要可访问的 Maven 依赖来源或按既有流程安装公共库；OCI Registry 不是 Maven 仓库。

下面仅演示注册、数据源与普通资源服务接入项。用户名和密码由各服务环境注入。

```yaml
server:
  port: ${SERVER_PORT:9093}
spring:
  application:
    name: example-service
  cloud:
    nacos:
      discovery:
        server-addr: ${NACOS_SERVER_ADDR}
        namespace: ${NACOS_NAMESPACE}
        username: ${NACOS_USERNAME:}
        password: ${NACOS_PASSWORD:}
  datasource:
    url: ${MYSQL_URL}
    username: ${MYSQL_USERNAME}
    password: ${MYSQL_PASSWORD}
jwt:
  secret: ${JWT_SECRET}
alisa:
  security:
    enabled: true
    application-id: example
    require-tenant: false
```

此示例不是完整服务脚手架：仍需对应依赖、驱动、Mapper、业务权限实现和环境文件加载方式。启动后核对注册 namespace、发现 group、服务名及健康实例。

### 认证和业务权限

`alisa.security.enabled=true` 才会启用当前公共资源服务自动配置。`application-id` 必须是与该资源服务认证/授权模型一致的标识。

- 当前资源服务组件可验证适用的 JWT 或委托凭据，并建立请求身份。
- 需要委托令牌时，为该 application 配置 issuer、introspection URI、authorization URI、resource client ID/secret，URI 和凭据放在服务端环境中。
- 需要租户模式时，按现有模块实现补齐租户校验、表结构和作用域，不能只改 `require-tenant` 开关。
- 业务层对具体资源 ID 和动作执行适用的访问检查。以 `ResourceAccess` 为入口时仍要理解当前实现对普通与委托/租户身份的不同分支，并保留业务自身的成员、所有者或管理员规则。
- 避免从客户端提交的 `userId`、角色或未经保护的身份头直接建立可信身份。

当前 `JwtUtil` 的签名密钥按 Base64 处理。已经存在的环境需要和签发端对齐配置及编码，不在接入新服务时随意轮换共享密钥。客户端只持有访问令牌，不配置 `JWT_SECRET`。

## 3. 接入网关

在对应 namespace 的 Group `ALISA_GATEWAY`、Data ID `alisa-gateway-routes.yaml` 中维护业务路由。下面只展示要新增的一项，**发布时必须保留原有其他业务项，提交完整列表**。

```yaml
- id: example-service
  uri: lb://example-service
  predicates:
    - Path=/api/v1/example/**
```

`lb://` 后面是注册名。新项默认不要增加 `delegated-ready`，也不要扩大匿名白名单；确认后端具备独立 Bearer 校验并有实际需要后，才按现有接入约定启用委托路由标记。

部署前后验证：后端路径和 context-path → Nacos 实例 → 网关路径 → 外部代理路径。四者不是同一层配置。

## 4. 前端和客户端调用

前端应使用环境定义的完整 API base URL。只有需要的公开配置进入前端构建，服务端密钥、数据库连接和 S3 Secret Key 不进入客户端。

```javascript
async function loadProfile(gatewayBase, accessToken) {
  const base = gatewayBase.replace(/\/$/, '')
  const response = await fetch(`${base}/api/v1/user/profile`, {
    headers: { Authorization: `Bearer ${accessToken}` }
  })
  if (!response.ok) throw new Error(`Profile request failed: ${response.status}`)
  return response.json()
}
```

示例只说明 Bearer 和路径的拼接；实际调用还需按目标接口处理成功结构、空令牌、401/403、超时与业务错误。不要将前端显示的“JWT 已解码”当作身份已经被服务端接受。

`@alisa-sdk/request` 当前提供 AxiosClient 和请求/响应/错误插件钩子，可用于统一 baseURL、超时和令牌附加。它不会替调用者签发 token 或自动完成业务授权。是否已发布到可用 npm 源，要按包实际发布方式确认，不能仅凭包名执行线上依赖安装。

## 5. 服务间调用

同环境服务优先通过约定的注册名或集群 Service 访问，不硬编码某个 Pod IP。OpenFeign 的服务名、HTTP 路径及 namespace/group 要一起核对。

alisa-common 现有 Feign 拦截器会在适用的请求上下文中传递 Authorization，并可带身份上下文头。异步任务没有当前 Servlet 请求时不会自动获得用户身份，需设计适用的服务身份流程。

重试要基于操作是否可重复执行来设计。创建、扣减、发消息等写操作不能因为网络超时就无条件重试，也不能因为引入 Feign 就认为跨服务事务已原子化。

## 6. 按需接入数据和外部能力

| 需要的能力 | 对接方式 | 开发验证 |
| --- | --- | --- |
| 关系型业务数据 | 本服务 datasource/MyBatis、明确表结构与迁移 | CRUD、唯一约束、事务回滚、资源/租户访问边界 |
| 验证码或其他临时状态 | 经服务端 Redis 客户端和约定的独立 key 前缀 | TTL、并发、原子操作、错误处理；不要破坏其他模块的 key |
| 邮件 | alisa-notification + MailSender/SMTP，或自定义发送 Bean | 发送成功/失败、超时及业务补偿，不只看连接端口可达 |
| 文件附件/封面 | 服务端调用 S3 兼容 API，客户端经授权接口取得文件引用和短期 URL | 权限、大小、格式、预签名过期、代理 Host/路径、失败处理 |
| 监控指标 | 当前 Portal 可按环境配置 Prometheus 查询 | 未配置/无数据明确区分，先确认 exporter 和查询指标存在 |

详细变量见[配置归属](/operations/configuration)。不要为了新增一个服务默认接入所有中间件，也不要把 JSON 文件存储的单实例组件直接扩成多副本共写。

## 7. 交付与联调

1. 单元/集成测试和明确的数据库迁移验证通过。
2. 镜像推入环境 Registry，记录标签与摘要。
3. Git 中声明 Deployment、Service、所需 ConfigMap/Secret 引用和探针。
4. 经 Argo CD 同步，确认新 Pod 就绪、实际摘要和重启情况。
5. 确认 Nacos 健康实例和网关已加载的路由。
6. 分别验证匿名、合法用户、无权限用户和直连后端的行为；再用真实参数完成业务联调。
7. 对文件、邮件、服务间写操作等涉及外部依赖的路径验证失败场景与回滚/补偿。

401 只说明请求在认证阶段被拒绝；200 健康接口只说明该探针通过；一条 Git 同步成功也不能替代上述业务验证。

## 接入后更新文档

将新服务加入 `docs/services/catalog.json`，将符合生成器范围的控制器源码加入 `scripts/api-sources.json`，运行 `npm run api:sync`、`npm test` 和 `npm run build`。新增中间件要说明真实使用者、凭据归属和降级/故障影响，而不是只增加一个服务名称。
