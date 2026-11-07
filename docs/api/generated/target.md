---
editLink: false
---

# 目标与阶段成果

> 本页由 `npm run api:sync` 生成，请勿手动修改。

- 服务注册名：`target-service`
- 源码：[SmallOKR · bf29dd6](https://github.com/sunyuboalisa/SmallOKR/tree/bf29dd6ddc868c8d94b2bba5d32c179065efce44)
- servlet context-path：`/target-service`
- 路径组合数：9

路径已包含服务 context-path，不包含环境域名及入口代理前缀。它是源码索引，不代表功能已启用或已部署，详见 [覆盖范围](/api/)。

## ResultController

| HTTP | 服务 HTTP 路径 | 控制器方法 |
| --- | --- | --- |
| `DELETE` | `/target-service/api/v1/result/delete` | [deleteResult](https://github.com/sunyuboalisa/SmallOKR/blob/bf29dd6ddc868c8d94b2bba5d32c179065efce44/smallokr_server/targetservice/src/main/java/alisa/smallokr/controller/ResultController.java#L48) |
| `GET` | `/target-service/api/v1/result/get` | [get](https://github.com/sunyuboalisa/SmallOKR/blob/bf29dd6ddc868c8d94b2bba5d32c179065efce44/smallokr_server/targetservice/src/main/java/alisa/smallokr/controller/ResultController.java#L55) |
| `GET` | `/target-service/api/v1/result/getAll` | [getAll](https://github.com/sunyuboalisa/SmallOKR/blob/bf29dd6ddc868c8d94b2bba5d32c179065efce44/smallokr_server/targetservice/src/main/java/alisa/smallokr/controller/ResultController.java#L62) |
| `POST` | `/target-service/api/v1/result/save` | [addResult](https://github.com/sunyuboalisa/SmallOKR/blob/bf29dd6ddc868c8d94b2bba5d32c179065efce44/smallokr_server/targetservice/src/main/java/alisa/smallokr/controller/ResultController.java#L27) |

## TargetController

| HTTP | 服务 HTTP 路径 | 控制器方法 |
| --- | --- | --- |
| `GET` | `/target-service/api/v1/target/analysis` | [getAnalysis](https://github.com/sunyuboalisa/SmallOKR/blob/bf29dd6ddc868c8d94b2bba5d32c179065efce44/smallokr_server/targetservice/src/main/java/alisa/smallokr/controller/TargetController.java#L80) |
| `DELETE` | `/target-service/api/v1/target/delete` | [deleteTarget](https://github.com/sunyuboalisa/SmallOKR/blob/bf29dd6ddc868c8d94b2bba5d32c179065efce44/smallokr_server/targetservice/src/main/java/alisa/smallokr/controller/TargetController.java#L52) |
| `GET` | `/target-service/api/v1/target/get` | [get](https://github.com/sunyuboalisa/SmallOKR/blob/bf29dd6ddc868c8d94b2bba5d32c179065efce44/smallokr_server/targetservice/src/main/java/alisa/smallokr/controller/TargetController.java#L67) |
| `POST` | `/target-service/api/v1/target/save` | [addTarget](https://github.com/sunyuboalisa/SmallOKR/blob/bf29dd6ddc868c8d94b2bba5d32c179065efce44/smallokr_server/targetservice/src/main/java/alisa/smallokr/controller/TargetController.java#L31) |
| `PUT` | `/target-service/api/v1/target/update` | [updateTarget](https://github.com/sunyuboalisa/SmallOKR/blob/bf29dd6ddc868c8d94b2bba5d32c179065efce44/smallokr_server/targetservice/src/main/java/alisa/smallokr/controller/TargetController.java#L59) |
