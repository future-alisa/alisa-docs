# 本地开发

## 目录布局

推荐将相关仓库放在同一个父目录，接口索引同步脚本默认按这个布局查找源码。

```text
Repos/
├─ alisa-docs/
├─ alisa-cloud/
├─ SmallOKR/
└─ ScienceCommunity/
```

## 启动文档站

使用 Node.js 22+ 和 npm。

```bash
cd alisa-docs
npm ci
npm run dev
```

文档不依赖后端服务在线。`npm run build` 生成 `docs/.vitepress/dist`；`npm run preview` 预览构建产物。

## 后端准备顺序

1. 准备 Java 17、Maven 以及对应环境的 Nacos、数据库、Redis 等依赖。
2. 在 `alisa-cloud` 执行 `mvn clean install`，先安装业务服务需要的公共 JAR。
3. 按各服务的 `example.env` 配置自己的本地环境，确认网关和用户服务使用一致的 `JWT_SECRET`。
4. 构建并启动账号服务和所需业务服务，核对 Nacos 注册名、namespace 和发现分组。
5. 启动网关，加载本地公共路由及选定环境的 Nacos 业务路由。

文档只提供启动顺序，实际数据库结构、功能开关和客户端配置以各仓库说明为准。已有数据库不要直接执行包含 DROP 或示例账号的历史导出脚本。

## 更新接口索引

```bash
# 仓库为同级目录时
npm run api:sync

# 使用其他源码父目录时
python3 scripts/sync-api.py --repos-root /path/to/Repos

npm test
npm run build
```

索引同步只读取 `src/main/java` 下的注解控制器，不会读取 `.env`、基础设施账号文档或数据库导出。构建文档本身不要求这些源码仓库存在，已生成索引会随 Git 一同提交。
