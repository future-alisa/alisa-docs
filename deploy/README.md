# 文档站 Argo CD 发布

目标入口：`https://alisa.vip.cpolar.cn/docs/`。应用名 `alisa-docs`，部署命名空间 `alisa-infra`，复用已有 `alisa-registry` Secret。该静态站内容与公开文档源码一致，不使用业务 JWT 或数据库凭据。

## 日常更新

```bash
# 编辑 docs 下的 Markdown 后先验证和提交正文
npm test
npm run build
git add docs README.md
git commit -m "Update documentation"

# 再将已提交正文固定为发布源，生成镜像标签和清单
npm run release:prepare
git add deploy/production deploy/argocd
git commit -m "Prepare documentation release"
git push origin main
```

随后在 Argo CD 对 `alisa-docs` 执行完整 Sync。应用默认手动同步，不会因为本地保存 Markdown 就自动发布线上。生成器要求工作区干净，避免已提交的镜像源遗漏本地修改；清单固定到正文提交，不使用浮动 latest。

## 发布链路

1. 普通 PVC 保留 npm 下载缓存与构建工作区，与 Sync 构建 Job 位于同一同步批次（wave -10），支持延迟绑定存储。
2. 构建 Job 从 GitHub 官方 codeload 下载固定提交归档。
3. Node 22 执行 npm ci 和带 `DOCS_BASE=/docs/` 的静态构建。CI 中另行执行 Python 索引生成器测试。
4. Kaniko 将预构建静态文件打入固定摘要的 NGINX 非 root 运行时，并推送到私有 Registry。
5. 前置任务成功后更新 Deployment、Service 和 HTTPRoute；入口去掉 `/docs` 后转发给静态服务器。

`deploy/release-config.json` 只保存可公开的发布参数；运行时基础镜像来自 [NGINX 官方公开渠道](https://github.com/nginx/docker-nginx-unprivileged)，以摘要固定。Registry 凭据由环境中已有 Secret 提供，不写入本仓库。

初次安装：向现有 Argo CD 注册 `deploy/argocd/application.yaml`，确认当前 namespace、StorageClass、Registry Secret、Traefik Gateway 和 allowedRoutes 均适用，然后 Sync。`deploy/examples` 仍为通用占位示例，不是当前生产目录。

## 变更与回滚

- 环境参数改变后，修改 release-config 并提交，再运行 release:prepare。HTTPRoute 模板目前专用于 `/docs/`，若改路径也要同步修改模板中的 Exact/PathPrefix。
- 内容更新需要新镜像，浏览器线上不会读取本机 Markdown。
- 回滚时在部署 Git 恢复已验证镜像及相关路径配置，再同步；不要以清理 PVC/Secret 的方式回滚。
- 仅同步已有静态资源可以跳过构建 Hook；切换到尚未构建的标签时必须先执行完整发布。

源码归档没有 Git 历史，构建 Job 和容器构建设置 `DOCS_ARCHIVE_BUILD=true`，关闭基于 Git 的页面最后更新时间。开发模式仍可显示本地 Git 提交时间；线上版本以部署源码提交和镜像摘要追溯。CI 同时构建普通模式和归档子路径模式。

生产镜像推送到公网 Registry；节点使用同一仓库的 `registry.kind.internal:5000` 内网入口拉取，避免公网绕行。文档专用 Secret `alisa-docs-registry-auth` 的实际认证数据仅通过 Argo CD API 注入，Application 忽略其 `/data` 差异并启用 `RespectIgnoreDifferences`，后续同步保留凭据。Git 中仅存合法空占位；首次部署需先同步 Secret 再注入凭据。
