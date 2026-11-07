# 开始使用

Alisa Docs 是多个项目的统一文档入口，源码放在 [alisa-docs](https://github.com/future-alisa/alisa-docs)。

## 按任务找到入口

| 你要做什么 | 从哪里开始 |
| --- | --- |
| 了解平台分层和各项职责 | [平台架构](/guide/architecture) |
| 查中间件用途与真实使用方 | [中间件清单](/guide/middleware) |
| 了解一次请求、文件上传和发布链路 | [组件交互](/guide/interactions) |
| 开发新服务并接入认证、路由和存储 | [开发接入指南](/guide/development-integration) |
| 查一个服务由哪个项目维护 | [服务目录](/services/) |
| 找 HTTP 接口和控制器 | [API 索引](/api/) |
| 把新业务路径接到公共网关 | [网关与动态路由](/operations/gateway) |
| 排查 401、403、404 或 503 | [排障与回滚](/operations/troubleshooting) |
| 构建镜像并通过 Argo CD 部署 | [镜像与 Argo CD](/operations/deployment) |
| 启动后端联调 | [本地开发](/guide/local-development) |

## 三个需要区分的地址

- **控制器路径**：Java 注解声明的路径，例如 `/api/v1/target/get`。
- **服务 HTTP 路径**：包括 servlet context-path。目标服务带 `/target-service`，所以为 `/target-service/api/v1/target/get`。
- **网关外部路径**：还可能包括入口代理的 `/alisa-gateway`。具体域名和代理前缀由环境决定。

本文档的生成 API 索引使用“服务 HTTP 路径”，不自动拼接生产域名或外部入口前缀。

## 如何判断文档是否适用于线上

生成的 API 页面是控制器源码快照，并记录各源码仓库提交。源码存在不代表功能开关已启用，也不代表该源码已经部署。接口权限、DTO 和响应字段以服务源码及运行时契约为准。

本期已纳入账号、目标、待办、跟踪、社区和聊天服务的注解控制器索引。由框架、安全过滤器或函数式路由提供的协议端点不在自动索引中。
