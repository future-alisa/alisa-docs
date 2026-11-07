# 镜像与 Argo CD

## 文档项目本身

本仓库是静态文档站，不需要 Java 后端、数据库或生产凭据。

```bash
npm ci
npm run build
```

构建输出是 `docs/.vitepress/dist`。当前服务器发布配置位于 `deploy/production`，Argo CD Application 定义位于 `deploy/argocd/application.yaml`；通用占位示例仍保留在 `deploy/examples`。

目标入口为 `https://alisa.vip.cpolar.cn/docs/`。应用 `alisa-docs` 使用独立 Deployment、Service 和 `/docs` HTTPRoute，使用当前命名空间中的专用 Registry Secret `alisa-docs-registry-auth`，其真实认证值由 Argo CD API 注入并受差异忽略策略保护。它是静态公开文档，不使用业务 JWT_SECRET。实际可用性以 Argo CD 状态和入口验证为准。

### 更新线上文档

先编辑 Markdown，执行测试和构建，然后提交正文。再生成固定源码版本的发布清单：

```bash
git add docs README.md
git commit -m "Update documentation"
npm run release:prepare
git add deploy/production deploy/argocd
git commit -m "Prepare documentation release"
git push origin main
```

在 Argo CD 对 `alisa-docs` 执行完整 Sync：前置 Job 下载固定提交，Node 构建静态文件，Kaniko 使用固定摘要的 NGINX 运行时推送镜像，随后更新站点资源。构建缓存卷保留 npm 下载缓存，默认不启用自动同步。完整步骤见仓库的 [发布说明](https://github.com/future-alisa/alisa-docs/blob/main/deploy/README.md)。

站点部署在子路径时，构建设置 `DOCS_BASE=/docs/`，入口代理去掉 `/docs` 后送入容器，页面生成的资源 URL 保留 `/docs/`；根路径部署使用 `/`。

新文档镜像的上传与节点拉取均使用 `registry.kind.internal:5000` 内网 Registry，构建任务使用节点 DNS 解析内网名称；官方 NGINX 基础镜像仍按固定摘要从官方源读取。内网仓库现有自签 TLS 的 Kaniko 例外仅限该仓库，其他镜像源保持证书校验。

本次实际上线的应用、外网 URL 和管理后台见 [已部署服务与公网入口](/services/deployed)。

## Argo CD 仓库代理与直连范围

当前四个已部署应用对应的 GitHub 仓库均在 Argo CD 的 Settings → Repositories 中登记了服务器现有 HTTP 代理，并配置 `noProxy`；强制刷新仓库连接可核验实际连通性，不需要在应用代码中写 Git 代理。

直连范围包含 `localhost`、`127.0.0.1`、`::1`、Kubernetes Service 域名（`.svc`、`.cluster.local`）、`.kind.internal`、`.alisa.local`、`registry.kind.internal`、宿主机内部别名以及 `10.0.0.0/8`、`172.16.0.0/12`、`192.168.0.0/16` 等私网地址。实际代理地址在 Argo CD 中维护，不把代理认证信息写入公开文档。

这是仓库访问配置，影响 Git 拉取及相关 Helm/Kustomize 操作；构建 Job 和节点 kubelet 不会自动继承这些设置。文档镜像上传与节点拉取仍使用内网 Registry。若构建器需要下载外部依赖，应在构建 Job 中单独配置并保留内网直连范围。

更新代理后先强制刷新仓库连接，再确认 Application 解析到预期 Git 提交，最后执行 Sync。参见 [Argo CD 官方仓库代理说明](https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/#configure-repositories-with-proxy)。

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
