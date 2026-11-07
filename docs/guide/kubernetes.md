# Kubernetes 内部组件与平台拓扑

依据 2026-11-08 管理员提供的 `kubectl get pods,svc,storageclass -A -o wide` 整理。当前清单中的 Pod 都运行在 `kind-control-plane`，节点地址为 `10.89.0.2`；这是单节点 kind 集群，宿主环境是 Windows / Podman。节点内运行 kubelet 与 containerd，不能把外层 Podman 当成 Kubernetes 直接调用的 CRI。

![当前集群的控制面、节点运行环境、入口和平台组件](/diagrams/kubernetes-overview.svg)

## 控制面怎样把声明变成容器

| 组件 | 当前所在位置 | 职责与交互 |
| --- | --- | --- |
| kube-apiserver | kube-system，kind-control-plane 静态 Pod | Kubernetes API 入口；kubectl、Argo CD 和控制器经 API 读取/写入对象 |
| etcd | kube-system，同节点静态 Pod | 保存集群对象和状态，包括 Secret；不是 MySQL、对象文件或 Portal 数据备份 |
| kube-controller-manager | kube-system，同节点静态 Pod | 协调 Deployment / ReplicaSet / Job 等对象，使实际状态接近期望状态 |
| kube-scheduler | kube-system，同节点静态 Pod | 为未绑定的 Pod 选择节点；不直接拉镜像、运行容器 |
| kubelet | kind-control-plane 内的系统服务 | 监听本节点 Pod、准备卷、调用 CRI、执行探针并上报状态 |
| containerd | kind-control-plane 内的系统服务 | 拉取镜像、准备容器与运行时；由 kubelet 通过 CRI 调用 |

一次发布的顺序：Argo CD 将期望对象写入 API Server → 控制器创建 ReplicaSet / Pod → scheduler 绑定节点 → kubelet 准备卷和调用 containerd → readiness 通过 → 服务后端具备接流条件。Argo CD repo-server 不负责替节点拉运行时镜像。

## 网络、DNS 与两套入口

| 组件 | 当前部署 / 地址 | 负责什么 |
| --- | --- | --- |
| kindnet | kube-system，DaemonSet Pod | 当前 CNI 网络组件，配置 Pod 网络与连通性；不代替业务权限校验 |
| kube-proxy | kube-system | 为 Kubernetes Service 实现服务转发所需网络规则；不是公网 HTTP 反向代理 |
| CoreDNS | kube-system，两个 Pod | 集群 DNS；kube-dns Service 为 `10.96.0.10`，端口 53 UDP/TCP |
| MetalLB controller / speaker | metallb-system | 为裸机/本地环境的 LoadBalancer Service 分配并宣告地址；不处理 API 认证与 HTTP 路由 |
| Traefik | traefik | 当前平台主入口。LoadBalancer IP `10.89.0.201`，HTTP 80、HTTPS 443；实际路由由 HTTPRoute / Gateway 等资源承载 |
| Contour + Envoy | projectcontour，Contour 两 Pod、Envoy 一 Pod | 另一套现存入口组件。Envoy LoadBalancer IP 为 `10.89.0.212`，80/443。存在组件不代表当前文档/社区路由由它接管 |
| nginx-cloudflared | infrastructure，一个双容器 Pod | 清单中另有隧道相关工作负载；当前已验证的公网业务链路仍为 cpolar → Caddy → Traefik，不推断所有请求经过它 |

`10.89.0.201` 和 `10.89.0.212` 是私网 LoadBalancer 地址，“EXTERNAL-IP”在这里表示相对集群 Service 的外部地址，不表示可从互联网直接访问。公网由 cpolar/Caddy 对接。

当前业务 HTTPRoute 的父资源是 `traefik/traefik-gateway`。新增路由时明确选择父 Gateway，不能把 Traefik 与 Contour 的配置混用。完整前缀处理见 [Caddy、网关与动态路由](/operations/gateway)。

## Service DNS 与 Nacos 的分工

| 寻址方式 | 例子 | 谁解析 / 使用 |
| --- | --- | --- |
| 同命名空间 Service 短名 | Portal 的 `api:8080`；社区 Web 的 `community:9091` | Pod 经集群 DNS 解析 |
| 跨命名空间 Service DNS | `alisa-user.alisa-infra.svc.cluster.local:8084` | 集群内其他服务，不能直接给互联网浏览器使用 |
| Nacos 注册名 | `user-service`、`community-service`，路由中写 `lb://community-service` | Spring Cloud 服务发现与负载均衡客户端 |
| 公网完整 URL | `https://alisa.vip.cpolar.cn/alisa-gateway/api/v1/user/health` | 浏览器、App、外部调用方 |

Nacos 自身的集群地址为 `nacos-service.traefik.svc.cluster.local:8848`，gRPC 端口为 9848，Console Service 端口另有 8080。`https://alisa.vip.cpolar.cn/nacos/` 是控制台入口，不等于 SDK 的 8848/9848 TCP 地址。

Service / EndpointSlice 描述服务及就绪后端，Pod IP 可能随重建变化。不要把当前 `10.244.0.*` Pod IP 写死在业务配置中。当前快照地址见下表，日常使用 DNS。

## 当前应用 Service 地址

| Service | 集群 DNS 与端口 | 当前 ClusterIP |
| --- | --- | --- |
| alisa-gateway | `alisa-gateway.alisa-infra.svc.cluster.local:8100` | 10.96.9.216 |
| alisa-user | `alisa-user.alisa-infra.svc.cluster.local:8084` | 10.96.175.226 |
| alisa-docs | `alisa-docs.alisa-infra.svc.cluster.local:8080` | 10.96.175.31 |
| Portal Web | `web.alisa-portal.svc.cluster.local:3000` | 10.96.83.126 |
| Portal API | `api.alisa-portal.svc.cluster.local:8080` | 10.96.2.12 |
| Science Web | `web.science-community.svc.cluster.local:3000` | 10.96.237.113 |
| Community API | `community.science-community.svc.cluster.local:9091` | 10.96.204.10 |
| Transfer | `transfer.science-community.svc.cluster.local:9092` | 10.96.21.153 |
| Nacos | `nacos-service.traefik.svc.cluster.local:8848` | 10.96.155.165 |
| 业务 Redis | `redis.redis.svc.cluster.local:6379` | 10.96.53.54 |
| SeaweedFS S3 | `seaweedfs-s3.seaweedfs.svc.cluster.local:8333` | 10.96.89.125 |

存储各协议地址见 [存储接入](/operations/storage)，MySQL 公网 TCP 和 Redis 数据边界见 [数据接入](/operations/data)。

## Argo CD 内部不是只有一个 server

| 工作负载 | 职责 | 与业务系统的边界 |
| --- | --- | --- |
| argocd-server | Web / API，登录与 Argo CD RBAC | 外网 [Argo CD](https://alisa.vip.cpolar.cn/argocd/)；不是业务 API Gateway |
| argocd-repo-server | 拉 Git、解析 Helm/Kustomize/目录并生成清单 | 仓库 proxy/noProxy 在此链路生效，不自动传给 kubelet 或构建 Job |
| argocd-application-controller | 比较集群实际状态与 Git 期望，执行同步、上报健康 | 不代表所有业务事务验证成功 |
| argocd-applicationset-controller | 根据 ApplicationSet 模板/生成器管理 Application | 组件在运行不表示当前四个应用都由 ApplicationSet 生成 |
| argocd-redis | Argo CD 缓存 | 不给账号验证码等业务共用 |
| argocd-dex-server | Argo CD 身份联邦 / SSO 适配组件 | 不等于 alisa-user，也不据此认定已配置外部 SSO |
| argocd-notifications-controller | 处理配置好的通知触发与发送 | 组件在运行不等于已经接入告警渠道 |

内部服务包括 `argocd-server.argocd.svc.cluster.local:80/443`、`argocd-repo-server.argocd.svc.cluster.local:8081`、`argocd-redis.argocd.svc.cluster.local:6379`，只用于相应控制面组件。

## 存储、配置与安全对象

- `local-path-provisioner` 运行在 local-path-storage；默认 `standard` 使用 `rancher.io/local-path`，`Delete` 回收、`WaitForFirstConsumer` 绑定且不支持在线扩容。PVC 不是对象存储 bucket。
- Deployment 管无状态副本；当前 Redis、SeaweedFS 的 Pod 名反映有 StatefulSet 风格工作负载，但具体持久化策略仍要看 PVC / PV 配置，不能仅凭 Pod 名认定高可用。
- ConfigMap 放非敏感配置，Secret 放凭据；Secret 的 base64 不是加密。ServiceAccount/RBAC 控制访问 Kubernetes API，不代替用户的业务角色。
- 本次应用运行 Pod 和构建 Job 通常不挂载 ServiceAccount token；自动发布由有相应权限的 Argo CD 执行。
- namespace、资源 requests/limits、探针、配额和 NetworkPolicy 各有作用。此次清单未核验全套网络策略或集群配额，不宣称已实现完整多租户基础设施隔离。

## 排障与容量边界

当前所有组件落在同一个 Node。CoreDNS 或 Contour 的两个副本都在该节点，不构成跨节点容灾；节点本地存储也不能凭增加 Pod 副本变成分布式备份。

| 现象 | 优先核对 |
| --- | --- |
| Argo 无法解析 GitHub / 拉取仓库失败 | repo-server、仓库代理、noProxy 与连接刷新；不重启业务 Pod 代替排查 |
| Pod Pending，PVC 未绑定 | StorageClass、消费者调度、资源与同批次创建，查看事件 |
| 新 Pod 停在 Pulling，已有缓存镜像仍能启动 | kubelet/containerd 拉取日志与串行队列；不要仅看镜像仓库网页是否打开 |
| 页面能打开但 API 失败 | Caddy Host/路径、HTTPRoute、前端 basePath/rewrite、Service 后端和业务认证 |
| 历史构建 Pod Error，但服务 Running | 区分 Job 历史与当前 Deployment，不把所有历史失败都当成实时服务故障 |

组件职责参考 [Kubernetes 官方架构](https://kubernetes.io/docs/concepts/architecture/) 和 [持久化卷说明](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)。实际组件名称和地址以上述管理员提供的当前清单为准。
