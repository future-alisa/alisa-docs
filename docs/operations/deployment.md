# 镜像与 Argo CD

## 文档项目本身

本仓库是静态文档站，不需要 Java 后端、数据库或生产凭据。

```bash
npm ci
npm run build
```

构建输出是 `docs/.vitepress/dist`。根目录提供 `Dockerfile` 与 Nginx 配置，可用于后续接入 Registry 和 Argo CD。`deploy/examples` 只保存待替换环境参数的示例，初始化文档仓库不会自动部署这些资源。

站点部署在子路径时，构建前设置 `DOCS_BASE`，例如 `/docs/`；根路径部署使用默认 `/`。入口代理需要保留浏览器侧的前缀，并按部署示例将其重写到容器根目录；不能仅修改外部代理前缀而保持构建 base 不变。

## 公共网关的现有发布流程

`alisa-cloud` 的 `codex/alisa-infra-argocd` 分支包含 `deploy/kubernetes/alisa-infra*.yaml`。应用 `alisa-infra` 通过以下阶段发布网关：

1. PreSync 构建任务下载固定提交的官方源码归档，运行 Maven 测试与打包。
2. 使用集群已有 Registry Secret 构建并推送固定源码版本标签的镜像。
3. Nacos 初始化任务检查配置：已有非空内容时保留，首次配置缺失时写入示例并读回校验。
4. 前置阶段成功后才更新 Deployment，观察新 Pod 就绪和应用健康状态。

当前示例保留 2 GiB 构建缓存卷；默认 StorageClass 需支持 ReadWriteOnce。运行时基础层使用已有私有 Registry 镜像，构建任务使用外部 DNS 解析源码和依赖站点。镜像源、网络和存储设置应按环境维护。

## 正常同步与选择性同步

只修改已有 Deployment、Service、ConfigMap、Namespace 或 HTTPRoute 时，可选择相应资源同步并跳过 PreSync Hook。完整同步会执行构建及初始化流程，不能把一次文档修改误当成必须重建网关的理由。

以 Argo CD 当前从 Git 解析的提交、同步结果和实际 Pod 为准。本项目不是实时发布仪表盘，历史成功记录不等于当前环境状态。

## 发布后验证

- Registry 中目标镜像标签及摘要已返回成功。
- Argo CD 应用达到 Synced / Healthy，目标 Deployment 更新完成。
- 新 Pod 的 imageID 与目标摘要一致，重启计数没有持续增加。
- 网关日志确认预期业务路由数量。
- 账号健康接口与真实授权业务请求正常。401 只验证匿名鉴权，不代表业务端到端联调完成。

## 凭据引用

镜像推送和拉取使用环境中已有的 Registry Secret；Nacos 和数据库连接通过 ConfigMap/Secret 等环境方式注入。文档只记录资源引用方式，不复制 Secret 内容、登录口令或真实用户数据。
