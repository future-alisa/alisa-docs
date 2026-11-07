# 服务目录

下面是当前文档覆盖的三个后端项目。端口来自源码默认值，运行环境可以通过配置覆盖；条目存在不代表该服务已在当前环境部署。

<ServiceDirectory />

## 公共库与独立服务的边界

| 模块 | 归属 | 运行方式 | 职责 |
| --- | --- | --- | --- |
| alisa-common | alisa-cloud | 普通 JAR | 公共响应、令牌和身份上下文等共享能力 |
| alisa-authorization | alisa-cloud | 普通 JAR，由账号服务按配置承载接口 | 授权与策略扩展 |
| alisa-notification | alisa-cloud | 普通 JAR | 通知与邮件能力 |
| gateway-service | alisa-cloud | 独立进程 | 路由、网关鉴权与身份传递 |
| user-service | alisa-cloud | 独立进程 | 统一账号与身份能力 |

`alisa-user` 是模块、镜像和 Deployment 名，`user-service` 是 Nacos 注册名。`alisa-gateway` 对应注册名 `gateway-service`，不要混用这两组名称。

## 其他相关项目

[alisa-portal](https://github.com/future-alisa/alisa-portal) 提供平台入口与管理界面。本期先链接该项目，不把它的 API/web 部署状态并入上面的业务服务清单。

源码、协议定义和环境配置各有归属，参见[架构与项目边界](/guide/architecture)。
