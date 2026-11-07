# 服务目录

此页按业务项目组织入口。SmallOKR 统一覆盖目标/阶段成果、待办与跟踪；Science Community 统一覆盖社区、资料、聊天与在线状态，页面列出完整外网域名。归并文档不改变底层微服务部署，条目存在不代表已部署。当前环境的部署清单、用户站和管理后台地址见 [已部署服务与公网入口](/services/deployed)。

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

[alisa-portal](https://github.com/future-alisa/alisa-portal) 提供已上线的 [平台门户与管理后台](/services/portal)。[Science Community](/services/science-community) 的用户站和社区管理也在当前服务目录中；具体部署状态以 [环境核验记录](/services/deployed) 为准。

源码、协议定义和环境配置各有归属，参见[架构与项目边界](/guide/architecture)。
