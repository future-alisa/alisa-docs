---
editLink: false
---

# 聊天与在线状态

> 本页由 `npm run api:sync` 生成，请勿手动修改。

- 服务注册名：`transfer-service`
- 源码：[ScienceCommunity · d10e11a](https://github.com/future-alisa/ScienceCommunity/tree/d10e11afb91e40a99457b91958a382b4015ef1e9)
- servlet context-path：`/`
- 路径组合数：2

路径已包含服务 context-path，不包含环境域名及入口代理前缀。它是源码索引，不代表功能已启用或已部署，详见 [覆盖范围](/api/)。

## UserController

| HTTP | 服务 HTTP 路径 | 控制器方法 |
| --- | --- | --- |
| `GET` | `/api/users/groups/{username}` | [getUserGroups](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/transfer_service/src/main/java/com/alisa/controller/UserController.java#L23) |
| `GET` | `/api/users/online` | [getOnlineUsers](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/transfer_service/src/main/java/com/alisa/controller/UserController.java#L18) |
