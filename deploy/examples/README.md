# 部署示例

这里不是可直接同步的生产目录。构建并推送文档镜像后，替换 `resources.yaml` 中的 Registry 地址与镜像标签，再将清单放入目标环境的 GitOps 目录。

镜像监听 8080，健康检查路径 `/healthz`。访问域名、入口代理、TLS、Registry Secret 与公开范围由对应环境配置；本项目初始化不创建公开站点、不自动创建 Argo CD Application。

子路径部署时需同时配置构建 `DOCS_BASE` 和入口代理重写：浏览器请求 `/docs/guide/...` 应由代理去掉 `/docs` 后送入容器，页面生成的资源 URL 仍保留 `/docs/`。
