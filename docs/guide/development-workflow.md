# 标准开发流程

适用于 alisa-cloud、SmallOKR、Science Community、Portal 和文档站。标准链路是：**明确需求 → 短期分支开发 → 本地验证 → 提交与评审 → 合入 main → 构建固定版本镜像 → Argo CD 发布 → 业务验证 → 更新记录**。

本文定义日常协作约定，不表示所有仓库都已配置强制评审、分支保护或全自动流水线。各项目的实际构建入口和功能状态仍以源码、CI 与 Argo CD 配置为准。

## 1. 先明确改什么、怎样验收

动手前在任务或 Issue 中记录具体触发场景、期望结果和影响范围，并在 PR 中关联；没有单独任务系统时，至少在 PR 描述中保留验收条件。确认以下信息：

| 信息 | 要明确的内容 |
| --- | --- |
| 项目与服务 | 属于 SmallOKR、Science Community 还是公共身份/网关；修改哪些前后端模块 |
| 接口契约 | HTTP 方法、完整 URL、请求/响应字段、兼容性；不要只写“加个接口” |
| 身份与数据 | 调用者、应用 scope、租户/资源权限、数据归属与迁移 |
| 配置与依赖 | 是否涉及 Nacos、路由、数据库、Redis、S3、Secret 或前端构建变量 |
| 验收 | 正常结果、权限拒绝、错误场景和恢复方式；谁负责确认 |

接口和权限设计可从 [SmallOKR API](/services/smallokr)、[Science Community API](/services/science-community) 与 [开发接入指南](/guide/development-integration) 开始。

## 2. 使用一个长期主线和短期开发分支

`main` 是长期主线；功能或修复使用短期分支，合入后删除。部署跟踪 main 的项目，不再保留一份长期独立的部署分支。某个应用仍跟踪其他分支时，先核对实际配置，再单独安排迁移，不能只改文档就假定部署已切换。

在工作区干净、已确认当前改动归属后：

```bash
git status --short
git switch main
git pull --ff-only
git switch -c codex/todo-filter
```

如果有未提交改动，先提交到合适分支或明确保存，再切换；不要用 reset、clean 或覆盖文件来“清理”别人的工作。多个任务同时进行时可使用独立 worktree，不在同一工作区混合不同任务。

一个分支解决一个可评审的问题。需求扩大时重新确认范围，避免同时混入接口改名、依赖升级、UI 重构和数据库迁移。

## 3. 配置环境，再实现与测试

- 使用当前项目支持的 Java、Node、Go 与锁文件版本；Java 公共库、业务服务和客户端应使用相互兼容的版本。
- 本地 `.env`、线上 Secret 和公开配置分开维护；已有 JWT_SECRET、密码和资源客户端凭据不能为方便联调随意替换。
- 浏览器使用完整公网 URL 或已配置的同源代理；集群内使用 Service DNS / Nacos 注册名，不写死临时 Pod IP。
- 修改 API 时同步考虑 DTO、权限、错误响应和旧客户端；新增路由必须确认前缀与 context-path。
- 修改租户相关代码时验证列表、详情、修改、删除、批量和内部调用的数据范围；只检查按钮显示不算授权测试。
- 数据库迁移先设计兼容顺序和备份，不让每次 Argo Sync 重复执行非幂等 DDL。

实际地址与示例见 [数据接入](/operations/data)、[存储接入](/operations/storage)、[认证与授权](/operations/authentication)、[租户管理](/operations/tenancy)。

## 4. 提交前执行与改动对应的验证

优先运行能覆盖实际风险的测试，再构建。下面是现有项目可用的常见入口，命令在表中指定目录执行；没有修改某个项目时，不要求把所有仓库全部重建。

| 项目 / 执行目录 | 常见检查 | 应额外验证什么 |
| --- | --- | --- |
| alisa-cloud 根目录 | `mvn -pl alisa-gateway -am test`；修改其他模块时替换模块名，或执行 `mvn test` | 路由、账号、凭据和授权相关测试；使用 Java 17 与实际环境依赖 |
| SmallOKR 的 smallokr_server | `mvn test`，公共库需先按匹配源码版本安装 | 目标/待办权限、租户过滤、trace → target 的上下文传递 |
| ScienceCommunity/App | `npm ci`、`npm run build`，并运行本次功能对应的现有测试脚本 | basePath、社区权限、资料/封面、聊天连接；不要假定项目一定有 npm test |
| alisa-cloud/alisa-admin-web | `pnpm install --frozen-lockfile`、`pnpm test`、`pnpm build` | 401/403、租户切换、一次性凭据和权限界面 |
| alisa-portal 根目录 | `make test`、`make build` | 后端持久化与令牌、前端类型检查；目录记录不等于真实资源 |
| alisa-docs 根目录 | `npm ci`、`npm test`、`npm run build` | 链接、服务分组、API 索引、实际地址及状态说明 |

前端页面改动要打开页面验证主要交互和布局；后端接口改动要验证正常与拒绝路径。HTTP 200、Pod Running、构建成功是不同层次的证据，不能互相代替。

## 5. 提交、推送与评审

```bash
git diff --check
git diff
git add path/to/changed-file
git diff --cached
git commit -m "fix(todo): restrict filtering to selected tenant"
git push -u origin codex/todo-filter
```

提交信息建议采用 `type(scope): 摘要`，常用类型为 feat、fix、docs、refactor、test、chore，scope 填业务或模块名。

按文件暂存并检查 staged diff，不盲目提交整个目录的 `.env`、日志或数据文件。提交信息描述具体行为；PR 描述让未看过聊天记录的人也能理解问题、改动、验证和发布影响。

评审至少覆盖：

| 项目 | 看什么 |
| --- | --- |
| 行为 | 是否满足验收、是否兼容现有调用者、错误是否可理解 |
| 权限与数据 | 身份、scope、租户、资源归属；迁移是否可控 |
| 配置与凭据 | 没有真实密钥；地址属于正确环境；配置归属清楚 |
| 验证 | 实际执行的命令、结果和未覆盖的边界，而非只写“已测试” |
| 发布与回滚 | 哪些镜像/配置/路由需要更新；回滚能否兼容数据 |

简短 PR 模板：

```markdown
问题与结果：说明具体触发场景，以及修改后的行为。
验证：列出实际执行的测试、构建或接口验证。
发布：列出配置、迁移、镜像、路由及必要顺序；没有特殊步骤则说明。
限制：只列影响验收或回滚的实际限制。
```

## 6. 合入 main 后整理分支

按仓库评审规则完成合并，再更新本地 main。若远端已发生变化，先解决差异并重新验证，不强推覆盖主线。

```bash
git switch main
git pull --ff-only
git branch -d codex/todo-filter
```

确认已合入、没有其他工作区或部署继续依赖该分支后，再从 GitHub 或 Git 删除远端短期分支。Squash 合并时 `git branch -d` 可能因提交图不同而拒绝；先核对改动已完整进入 main，不直接将拒绝当成需要强制删除。

合入 main 不等于已经上线。继续确认 CI、构建产物、目标 Argo CD 应用及其跟踪的仓库/分支/路径。

## 7. 构建与发布

| 改动类型 | 正确发布位置 |
| --- | --- |
| 后端/前端代码、依赖、构建期变量 | 构建新的不可变镜像，更新 Git 部署清单，再由 Argo CD 同步 |
| Nacos 动态业务路由 | 在正确 namespace、Group、Data ID 发布完整配置并验证；不必因此重建所有服务 |
| Kubernetes 配置或入口 | 修改 Git 中对应 ConfigMap/Service/HTTPRoute 等清单，确认程序是否需要重启 |
| Secret | 通过现有受控凭据流程注入，保留差异忽略/同步保护，不把真实值提交 Git |
| Portal 服务目录 | 通过门户 API 更新持久化目录；不需要仅为改导航重建 Web 镜像 |
| 数据库结构 | 经验证的迁移与备份流程，配合新旧应用兼容顺序，不能靠镜像回滚还原数据 |

当前文档镜像使用 `registry.kind.internal:5000` 进行集群内上传和节点拉取。业务项目使用各自已验证的构建入口，不假定统一的 release:prepare 脚本适用于所有仓库。

Argo CD 的仓库代理用于 Git 拉取及清单生成；构建 Job 和 kubelet 不自动继承。全量 Sync 可能执行构建/初始化 Hook；选择性同步会跳过 Hook，只有在不依赖这些步骤时才使用。详见 [镜像与 Argo CD](/operations/deployment)、[Caddy 和路由](/operations/gateway)。

## 8. 发布后验证

按顺序记录证据：

1. Argo CD 解析到预期 Git 提交，目标镜像标签/摘要正确，应用 Synced / Healthy。
2. Deployment 就绪、Pod 重启数没有持续增加，Service / HTTPRoute 状态及后端正确。
3. 从真实外网完整 URL 请求，确认前缀、静态资源、页面跳转与接口响应。
4. 使用允许的测试身份验证关键业务、401/403 拒绝、租户边界；聊天或存储需验证其协议操作，不能只访问页面。
5. 记录提交、镜像、环境、时间、验证范围和遗留问题，更新 docs 及必要的门户入口信息。

不能为了完成验证任意修改真实用户数据；优先使用明确的测试资源。只做了匿名探测时，应如实注明没有验证登录后的业务操作。

## 9. 回滚与紧急修复

先识别问题属于代码、路由、配置、凭据还是数据，再选择对应恢复动作：

- 代码/镜像问题：在 Git 中恢复上一已验证镜像与配置，提交后由 Argo CD 同步；不要只在集群手改后留下 Git 漂移。
- Nacos 路由问题：恢复有效历史配置并发布，检查每个网关实例加载结果。
- 数据迁移问题：按事先评估的兼容与恢复方案处理；回退镜像不会自动恢复数据库、对象文件或 PVC。
- 紧急修复：从主线创建短期 hotfix 分支，完成最小必要验证并正常合回 main；临时运维改动需及时补回 Git 和文档。

不通过强推 main、删除数据、重置整个集群或随意更换 JWT_SECRET 来代替回滚。涉及凭据轮换时另行安排兼容窗口和调用方迁移。

## 日常示例：更新这份文档

只改 Markdown 时，开发分支完成评审并合入后，可在干净的 main 生成发布清单：

```bash
npm test
npm run build
git status --short
npm run release:prepare
git add deploy/production deploy/argocd
git commit -m "Prepare documentation release"
git push origin main
```

`release:prepare` 固定当前已提交的源码 SHA，要求工作区干净；正文必须先提交，再生成清单。发布清单作为发布元数据按仓库规则提交/评审；若生成前 main 已推进，先更新到最终源码版本再重新生成，不能让镜像指向未包含需求的旧提交。随后对 alisa-docs 执行完整 Sync，核验 `https://alisa.vip.cpolar.cn/docs/` 和本次变更页面。

## 完成标准

需求已实现，相关验证通过，评审/提交可追溯；需要上线的改动已进入正确环境并完成业务验证，文档与入口记录一致；短期分支和临时运维状态已按实际情况整理。仅“代码已推送”或“Sync 成功”不能代替整个完成标准。
