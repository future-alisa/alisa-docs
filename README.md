# Alisa Docs

Alisa 的统一开发文档：服务目录、源码接口索引、网关认证、Nacos 路由、Registry 与 Argo CD 运维说明。

## 本地启动

需要 Node.js 22+、npm；更新接口索引或运行生成器测试另需 Python 3.10+。

```bash
npm ci
npm run dev
```

```bash
npm test          # 接口索引生成器测试
npm run build    # 文档结构检查、死链检查、静态构建
npm run preview  # 预览构建产物
```

站点输出为 `docs/.vitepress/dist`。本仓库可独立构建，不要求业务仓库存在。

## 同步接口索引

默认从同级 `alisa-cloud`、`SmallOKR`、`ScienceCommunity` 读取注解控制器：

```bash
npm run api:sync
# 自定义源码父目录
python3 scripts/sync-api.py --repos-root /path/to/Repos
```

索引包含服务 HTTP 路径与源码链接，不是完整 OpenAPI 或线上可用性声明。正文见 [接口入口](docs/api/index.md) 和 [维护指南](docs/guide/contributing.md)。

## 平台架构专题

- [平台分层与服务职责](docs/guide/architecture.md)
- [中间件、状态与使用方](docs/guide/middleware.md)
- [请求、认证、文件与部署交互](docs/guide/interactions.md)
- [新服务和客户端开发接入](docs/guide/development-integration.md)
- [配置项与凭据归属](docs/operations/configuration.md)

## 项目结构

```text
docs/                  Markdown 文档、主题和服务目录
  api/generated/       可重复生成的控制器路径索引
  public/api-index.json 机器可读索引
scripts/               文档检查与索引生成
tests/                 生成器测试
.github/workflows/     构建验证（不自动发布站点）
deploy/examples/       待环境配置的部署示例
Dockerfile             静态站容器构建
```

子路径部署构建前设置 `DOCS_BASE=/docs/`。凭据不写入本仓库，运行环境与站点公开范围由部署方确定。服务器发布使用独立的 `alisa-docs` Argo CD 应用，详见 [发布说明](deploy/README.md)。

## 服务器发布

目标入口：`https://alisa.vip.cpolar.cn/docs/`。修改并提交 Markdown 后，运行 `npm run release:prepare`，提交生成的清单并 push，再在 Argo CD 同步 `alisa-docs`。本地保存只热更新本地预览，不直接改线上页面。
