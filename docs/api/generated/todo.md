---
editLink: false
---

# 待办

> 本页由 `npm run api:sync` 生成，请勿手动修改。

- 服务注册名：`todo-service`
- 源码：[SmallOKR · bf29dd6](https://github.com/sunyuboalisa/SmallOKR/tree/bf29dd6ddc868c8d94b2bba5d32c179065efce44)
- servlet context-path：`/`
- 路径组合数：10

路径已包含服务 context-path，不包含环境域名及入口代理前缀。它是源码索引，不代表功能已启用或已部署，详见 [覆盖范围](/api/)。

## DicController

| HTTP | 服务 HTTP 路径 | 控制器方法 |
| --- | --- | --- |
| `GET` | `/api/v1/todo/dic/get` | [getDicEntry](https://github.com/sunyuboalisa/SmallOKR/blob/bf29dd6ddc868c8d94b2bba5d32c179065efce44/smallokr_server/todoservice/src/main/java/alisa/smallokr/controller/DicController.java#L22) |

## TodoController

| HTTP | 服务 HTTP 路径 | 控制器方法 |
| --- | --- | --- |
| `POST` | `/api/v1/todo/add` | [addTodo](https://github.com/sunyuboalisa/SmallOKR/blob/bf29dd6ddc868c8d94b2bba5d32c179065efce44/smallokr_server/todoservice/src/main/java/alisa/smallokr/controller/TodoController.java#L37) |
| `POST` | `/api/v1/todo/addRepeat` | [addRepeat](https://github.com/sunyuboalisa/SmallOKR/blob/bf29dd6ddc868c8d94b2bba5d32c179065efce44/smallokr_server/todoservice/src/main/java/alisa/smallokr/controller/TodoController.java#L113) |
| `GET` | `/api/v1/todo/analysis` | [getAnalysis](https://github.com/sunyuboalisa/SmallOKR/blob/bf29dd6ddc868c8d94b2bba5d32c179065efce44/smallokr_server/todoservice/src/main/java/alisa/smallokr/controller/TodoController.java#L138) |
| `DELETE` | `/api/v1/todo/delete` | [deleteTodo](https://github.com/sunyuboalisa/SmallOKR/blob/bf29dd6ddc868c8d94b2bba5d32c179065efce44/smallokr_server/todoservice/src/main/java/alisa/smallokr/controller/TodoController.java#L53) |
| `DELETE` | `/api/v1/todo/deleteRepeat` | [deleteRepeat](https://github.com/sunyuboalisa/SmallOKR/blob/bf29dd6ddc868c8d94b2bba5d32c179065efce44/smallokr_server/todoservice/src/main/java/alisa/smallokr/controller/TodoController.java#L131) |
| `GET` | `/api/v1/todo/get` | [get](https://github.com/sunyuboalisa/SmallOKR/blob/bf29dd6ddc868c8d94b2bba5d32c179065efce44/smallokr_server/todoservice/src/main/java/alisa/smallokr/controller/TodoController.java#L68) |
| `GET` | `/api/v1/todo/getRepeat` | [getRepeat](https://github.com/sunyuboalisa/SmallOKR/blob/bf29dd6ddc868c8d94b2bba5d32c179065efce44/smallokr_server/todoservice/src/main/java/alisa/smallokr/controller/TodoController.java#L105) |
| `GET` | `/api/v1/todo/getTodoByWeekDay` | [getTodoByWeekDay](https://github.com/sunyuboalisa/SmallOKR/blob/bf29dd6ddc868c8d94b2bba5d32c179065efce44/smallokr_server/todoservice/src/main/java/alisa/smallokr/controller/TodoController.java#L79) |
| `PUT` | `/api/v1/todo/update` | [updateTodo](https://github.com/sunyuboalisa/SmallOKR/blob/bf29dd6ddc868c8d94b2bba5d32c179065efce44/smallokr_server/todoservice/src/main/java/alisa/smallokr/controller/TodoController.java#L60) |
