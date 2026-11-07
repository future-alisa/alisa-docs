# API 入口与覆盖范围

## 目前提供的内容

这里提供从 Java 注解控制器生成的路径索引：HTTP 方法、服务 HTTP 路径、控制器方法、条件装配提示和对应提交的源码链接。

**它不是完整 OpenAPI 契约，也不是运行时可用性清单。** 请求字段、响应结构、字段约束和权限逻辑仍需查看 DTO、控制器及服务实现；本项目不根据方法名猜测 schema。

| 服务 | 索引 |
| --- | --- |
| user-service | [账号、身份与授权](/api/generated/account) |
| target-service | [目标与阶段成果](/api/generated/target) |
| todo-service | [待办](/api/generated/todo) |
| trace-service | [跟踪](/api/generated/trace) |
| community-service | [社区](/api/generated/community) |
| transfer-service | [聊天和在线状态](/api/generated/transfer) |

完整机器可读路径索引：[api-index.json](/api-index.json)。

## OpenAPI 接入状态

源码依赖检查发现，`community-service` 已声明 `springdoc-openapi-starter-webmvc-ui`。在对应功能启用、路径未覆盖且鉴权允许的环境中，其服务地址通常提供 `/community/v3/api-docs` 与 `/community/swagger-ui.html`。经过公共网关时还需添加环境入口代理前缀，并满足网关鉴权。

其他服务目前不在本项目中宣称已经提供 Swagger/OpenAPI。后续应在服务内维护契约，再把经过验证的规范加入统一入口；文档站不在浏览器中保存运维账号或自动发送生产凭据。

## 生成器的范围

- 支持 `@GetMapping`、`@PostMapping`、`@PutMapping`、`@DeleteMapping`、`@PatchMapping` 与 `@RequestMapping`。
- 合并 controller 前缀、方法路径以及源码配置的 servlet context-path；支持字面量路径数组。
- 未指定 HTTP 方法的 `@RequestMapping` 标为 `ANY`，不擅自当作 GET。
- 忽略注释和嵌套类的方法映射，非字面量路径会明确报错，需要人工补充规则。
- 不展开组合注解、继承控制器、框架安全链、函数式路由或运行时动态路径。

`/oauth2/**` 等协议路由可能由安全框架提供，不会因为自动索引中缺少某个路径就判定该路径不存在。

## 重要兼容说明

ScienceCommunity 的旧 `/basis`、`/case`、`/post` 关系接口在 `LegacyDocumentController` 中返回 410，内容统一到 `/document`，不要将旧索引条目当作仍可写入的业务入口。
