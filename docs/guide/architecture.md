# 架构与项目边界

## 请求链路

```text
客户端
  └─ 环境入口代理（可带 /alisa-gateway 前缀）
       └─ alisa-gateway / gateway-service
            ├─ 本地公共账号路由 ────── user-service
            └─ Nacos 动态业务路由
                 ├─ target-service / todo-service / trace-service
                 └─ community-service / transfer-service
```

服务地址由 Nacos Discovery 提供，业务路径匹配规则由网关路由配置提供。服务注册成功不会自动产生目前这些自定义业务路径。

## 项目职责

| 仓库 | 负责什么 | 文档归属 |
| --- | --- | --- |
| [alisa-cloud](https://github.com/future-alisa/alisa-cloud) | 网关、统一账号、公共库和授权/通知扩展 | 接入约定与平台配置 |
| [SmallOKR](https://github.com/sunyuboalisa/SmallOKR) | 目标、阶段成果、待办、跟踪与客户端 | OKR 业务接口与规则 |
| [ScienceCommunity](https://github.com/future-alisa/ScienceCommunity) | 社区、成员、资料、频道讨论与聊天服务 | 社区业务接口与权限规则 |
| [alisa-docs](https://github.com/future-alisa/alisa-docs) | 文档导航、接口索引和运维指南 | 跨项目说明与维护入口 |

## 谁维护哪份事实

| 事实 | 唯一维护位置 | 本项目做什么 |
| --- | --- | --- |
| 控制器路径、DTO、业务行为 | 对应服务源码 | 生成路径索引、链接到源码 |
| 运行中的业务路由 | 对应环境 Nacos 配置 | 说明结构、发布及验证方式 |
| 部署期望状态 | Argo CD 跟踪的 Git 分支 | 说明镜像、同步和回滚流程 |
| 账号、密钥、环境连接凭据 | Secret 或凭据管理系统 | 只记录变量名与引用方式 |

业务表与业务权限留在各项目，共享用户标识连接公共账号体系；不要为了统一入口把所有业务代码和数据集中到账号服务。
