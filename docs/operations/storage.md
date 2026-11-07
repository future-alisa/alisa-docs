# 存储：文件、对象与持久化卷

本页使用 2026-11-08 管理员提供的真实 Kubernetes Service 清单。集群内部优先使用 Service DNS；公网地址用于浏览器、开发机及协议客户端。以下地址不包含密码、S3 密钥或预签名凭据。

## 实际服务地址

| 接口 | 集群内地址 | 外网地址 / 用途 |
| --- | --- | --- |
| SeaweedFS S3 | `http://seaweedfs-s3.seaweedfs.svc.cluster.local:8333` | `https://alisa.vip.cpolar.cn/s3/`，S3 API，不是网页管理界面 |
| Filer | `http://seaweedfs-filer.seaweedfs.svc.cluster.local:8888` | [文件浏览](https://alisa.vip.cpolar.cn/fs/)，需入口认证 |
| WebDAV | `http://seaweedfs-filer-webdav.seaweedfs.svc.cluster.local:7333` | `https://alisa.vip.cpolar.cn/webdav/`，由 WebDAV 客户端使用 |
| Admin | `http://seaweedfs-admin.seaweedfs.svc.cluster.local:23646` | [存储管理](https://alisa.vip.cpolar.cn/fs-admin/)，服务自身登录 |
| Master | `http://seaweedfs-master.seaweedfs.svc.cluster.local:9333` | [Master 页面](https://alisa.vip.cpolar.cn/fs-master/) |
| Volume | `http://seaweedfs-volume.seaweedfs.svc.cluster.local:8080` | 实际文件块服务，不作为业务浏览器的统一入口 |

S3 Service 当前 ClusterIP 为 `10.96.89.125`；WebDAV 为 `10.96.203.200`；Admin 为 `10.96.231.90`。这些 IP 是核验快照，应用配置使用上面的 DNS。Filer、Master、Volume 是 Headless Service（ClusterIP 为 None），DNS 返回后端地址，并不是缺少服务。

## 业务文件怎样存

1. 浏览器请求社区上传 API，由业务服务校验用户、社区成员关系、文件用途与大小。
2. community-service 的 ObjectStorageService 使用 S3 兼容 SDK 上传到 SeaweedFS；依赖 MinIO SDK 不代表运行的是 MinIO 服务。
3. 数据库存资料元数据、归属和文件引用；SeaweedFS 存文件内容。数据库记录与对象上传不是跨系统原子事务，需要处理失败重试与孤儿文件。
4. 下载通过业务读取接口取得短期签名 URL；浏览器不持有 Access Key 或 Secret Key。

实际社区 API：

| 操作 | 完整 URL | 说明 |
| --- | --- | --- |
| 上传 | `POST https://alisa.vip.cpolar.cn/science/community-api/storage` | multipart 字段 `file`，可带 `communityId`、`purpose`；服务端执行访问检查 |
| 获取读取链接 | `GET https://alisa.vip.cpolar.cn/science/community-api/storage/read-url?url=文件引用` | 对 `url` 正确编码；不可把此处的签名响应记录进公开日志 |
| 批量读取链接 | `POST https://alisa.vip.cpolar.cn/science/community-api/storage/read-urls` | 请求字段以 [社区接口](/api/generated/community) 和 DTO 为准 |

源码限制为普通附件最多 20 MiB、封面最多 5 MiB，读取签名通常有效 600 秒。过期后重新向业务 API 取链接，不通过增加签名有效期代替权限校验。

## 服务端 S3 对接

集群内服务可使用真实 S3 Service 作为上传连接：

```properties
S3_ENDPOINT=http://seaweedfs-s3.seaweedfs.svc.cluster.local:8333
S3_BUCKET=app-storage
S3_REGION=us-east-1
S3_PUBLIC_URL=https://alisa.vip.cpolar.cn/s3/app-storage/
```

`app-storage` 来自当前社区本地环境配置；线上 Secret 的实际 bucket 值未通过此次只读检查取得，部署前需确认与已分配 bucket 一致。`S3_ACCESS_KEY_ID`、`S3_SECRET_ACCESS_KEY` 通过 Secret 注入，此页不填实际值。

上面是集群直连方式，不是一组可不加区分替换现有配置的开关：上传 endpoint、下载地址与代理还原 Host 必须配套。浏览器不能解析 `.svc.cluster.local`，下载需要业务代理或已验证的外网签名转发。

当前社区本地配置另有一套隧道方式：`S3_ENDPOINT=https://s3.alisa.local`，`S3_TUNNEL_URL=https://alisa.vip.cpolar.cn/s3`。SDK 按前一个地址生成签名，再通过隧道转发；这时代理必须去掉 `/s3`，还原签名时使用的 Host，并保留原始路径和查询参数。若改用集群 DNS 签名，代理还原的 Host 也要相应调整，不能沿用旧值。

通用 S3 客户端不要直接把含 `/s3/` 的网页路径当成根 endpoint；当前代理的 Host、路径与签名约定不一定被所有 SDK 支持。优先在集群内部使用根 S3 地址，外部访问按经过验证的业务流程接入。

## WebDAV 对接

在 Zotero 或 WebDAV 客户端中填写 `https://alisa.vip.cpolar.cn/webdav/` 以及实际分配的用户目录和账号。使用独立的 WebDAV 认证，不使用业务 JWT 或门户 API_TOKEN。

浏览器 GET 返回 405 不能单独判定 WebDAV 不可用；应使用客户端执行 PROPFIND 等协议操作，再验证目录列出、上传、下载和同步冲突。此次只记录已知协议入口，没有执行文件写入或删除测试。

## Kubernetes PVC 与文件存储的边界

当前默认 StorageClass：`standard`，provisioner 为 `rancher.io/local-path`，回收策略 `Delete`，绑定模式 `WaitForFirstConsumer`，不允许在线扩容。

- Portal 的 `portal-data` PVC 保存其 JSON 目录数据；文档构建缓存 PVC 保存 npm 缓存和工作区，二者不等于 SeaweedFS bucket。
- PVC 等待消费者调度后绑定。Argo CD 中不要先等 PVC Healthy、再在后一个 wave 创建它的首个消费者；文档构建的 PVC 与 Job 当前在同一个 wave。
- local-path 数据依赖当前节点，不是跨节点复制。迁移或扩容需要新卷和明确的数据迁移流程；备份应覆盖业务数据而非只备份清单。
- S3 文件、Filer 元数据、卷内容、业务数据库和 PVC 各有自己的恢复范围。详见 [数据接入](/operations/data) 与 [Kubernetes 组件](/guide/kubernetes)。
