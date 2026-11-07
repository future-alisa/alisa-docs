---
editLink: false
---

# 社区

> 本页由 `npm run api:sync` 生成，请勿手动修改。

- 服务注册名：`community-service`
- 源码：[ScienceCommunity · d10e11a](https://github.com/future-alisa/ScienceCommunity/tree/d10e11afb91e40a99457b91958a382b4015ef1e9)
- servlet context-path：`/community`
- 路径组合数：87

路径已包含服务 context-path，不包含环境域名及入口代理前缀。它是源码索引，不代表功能已启用或已部署，详见 [覆盖范围](/api/)。

::: warning 本地源码快照
源码包含未提交变更；索引反映本地文件，链接指向上述 HEAD，可能存在差异。
:::

## CategoryController

| HTTP | 服务 HTTP 路径 | 控制器方法 |
| --- | --- | --- |
| `DELETE` | `/community/category/batch-delete` | [batchDelete](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/CategoryController.java#L42) |
| `POST` | `/community/category/batch-upsert` | [batchUpsert](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/CategoryController.java#L36) |
| `GET` | `/community/category/getAll` | [getAll](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/CategoryController.java#L18) |
| `POST` | `/community/category/upsert` | [upsert](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/CategoryController.java#L30) |
| `GET` | `/community/category/{id}` | [getById](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/CategoryController.java#L24) |

## ChannelController

| HTTP | 服务 HTTP 路径 | 控制器方法 |
| --- | --- | --- |
| `DELETE` | `/community/channel/batch-delete` | [batchDelete](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/ChannelController.java#L59) |
| `POST` | `/community/channel/batch-upsert` | [batchUpsert](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/ChannelController.java#L53) |
| `GET` | `/community/channel/getAll` | [getAll](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/ChannelController.java#L29) |
| `GET` | `/community/channel/getAllByCommunityId` | [getAllByCommunityId](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/ChannelController.java#L35) |
| `POST` | `/community/channel/save` | [save](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/ChannelController.java#L18) |
| `POST` | `/community/channel/upsert` | [upsert](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/ChannelController.java#L47) |
| `DELETE` | `/community/channel/{id}` | [delete](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/ChannelController.java#L24) |
| `GET` | `/community/channel/{id}` | [getById](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/ChannelController.java#L41) |

## ChannelDiscussionController

| HTTP | 服务 HTTP 路径 | 控制器方法 |
| --- | --- | --- |
| `GET` | `/community/channel/{channelId}/access` | [access](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/ChannelDiscussionController.java#L15) |
| `POST` | `/community/channel/{channelId}/join` | [join](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/ChannelDiscussionController.java#L19) |
| `POST` | `/community/channel/{channelId}/leave` | [leave](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/ChannelDiscussionController.java#L21) |
| `GET` | `/community/channel/{channelId}/messages` | [history](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/ChannelDiscussionController.java#L23) |
| `POST` | `/community/channel/{channelId}/messages` | [send](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/ChannelDiscussionController.java#L28) |

## ChannelUserController

| HTTP | 服务 HTTP 路径 | 控制器方法 |
| --- | --- | --- |
| `DELETE` | `/community/channeluser/batch-delete` | [batchDelete](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/ChannelUserController.java#L55) |
| `POST` | `/community/channeluser/batch-upsert` | [batchUpsert](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/ChannelUserController.java#L49) |
| `GET` | `/community/channeluser/getAll` | [getAll](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/ChannelUserController.java#L25) |
| `GET` | `/community/channeluser/getAllByChannelId` | [getAllByChannelId](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/ChannelUserController.java#L31) |
| `POST` | `/community/channeluser/upsert` | [upsert](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/ChannelUserController.java#L43) |
| `DELETE` | `/community/channeluser/{id}` | [remove](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/ChannelUserController.java#L20) |
| `GET` | `/community/channeluser/{id}` | [getById](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/ChannelUserController.java#L37) |

## CommentController

| HTTP | 服务 HTTP 路径 | 控制器方法 |
| --- | --- | --- |
| `DELETE` | `/community/comment/batch-delete` | [batchDelete](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/CommentController.java#L42) |
| `POST` | `/community/comment/batch-upsert` | [batchUpsert](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/CommentController.java#L36) |
| `GET` | `/community/comment/getAll` | [getAll](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/CommentController.java#L18) |
| `POST` | `/community/comment/upsert` | [upsert](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/CommentController.java#L30) |
| `GET` | `/community/comment/{id}` | [getById](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/CommentController.java#L24) |

## CommunityController

| HTTP | 服务 HTTP 路径 | 控制器方法 |
| --- | --- | --- |
| `DELETE` | `/community/community/batch-delete` | [batchDelete](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/CommunityController.java#L63) |
| `POST` | `/community/community/batch-upsert` | [batchUpsert](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/CommunityController.java#L57) |
| `GET` | `/community/community/getAll` | [getAll](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/CommunityController.java#L21) |
| `GET` | `/community/community/getAllByTag/{tagName}` | [getAllWithTag](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/CommunityController.java#L34) |
| `GET` | `/community/community/getAllByUser` | [getAllByUser](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/CommunityController.java#L27) |
| `POST` | `/community/community/upsert` | [upsert](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/CommunityController.java#L46) |
| `GET` | `/community/community/{id}` | [getById](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/CommunityController.java#L40) |
| `POST` | `/community/community/{id}/cover` | [updateCover](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/CommunityController.java#L52) |

## CommunityUserController

| HTTP | 服务 HTTP 路径 | 控制器方法 |
| --- | --- | --- |
| `GET` | `/community/communityuser/access` | [access](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/CommunityUserController.java#L23) |
| `POST` | `/community/communityuser/add` | [add](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/CommunityUserController.java#L45) |
| `DELETE` | `/community/communityuser/batch-delete` | [batchDelete](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/CommunityUserController.java#L94) |
| `POST` | `/community/communityuser/batch-upsert` | [batchUpsert](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/CommunityUserController.java#L88) |
| `GET` | `/community/communityuser/getAll` | [getAll](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/CommunityUserController.java#L64) |
| `GET` | `/community/communityuser/getAllByCommunityId` | [getAllByCommunityId](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/CommunityUserController.java#L70) |
| `POST` | `/community/communityuser/join` | [join](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/CommunityUserController.java#L40) |
| `GET` | `/community/communityuser/roles` | [roles](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/CommunityUserController.java#L30) |
| `POST` | `/community/communityuser/upsert` | [upsert](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/CommunityUserController.java#L82) |
| `DELETE` | `/community/communityuser/{id}` | [remove](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/CommunityUserController.java#L59) |
| `GET` | `/community/communityuser/{id}` | [getById](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/CommunityUserController.java#L76) |

## DocumentController

| HTTP | 服务 HTTP 路径 | 控制器方法 |
| --- | --- | --- |
| `DELETE` | `/community/document/batch-delete` | [batchDelete](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/DocumentController.java#L60) |
| `POST` | `/community/document/batch-upsert` | [batchUpsert](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/DocumentController.java#L54) |
| `GET` | `/community/document/getAll` | [getAll](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/DocumentController.java#L19) |
| `GET` | `/community/document/getAllByCommunityId` | [getAllByComunityId](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/DocumentController.java#L25) |
| `POST` | `/community/document/save` | [save](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/DocumentController.java#L43) |
| `POST` | `/community/document/upsert` | [upsert](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/DocumentController.java#L37) |
| `DELETE` | `/community/document/{id}` | [delete](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/DocumentController.java#L49) |
| `GET` | `/community/document/{id}` | [getById](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/DocumentController.java#L31) |

## InvitationController

| HTTP | 服务 HTTP 路径 | 控制器方法 |
| --- | --- | --- |
| `POST` | `/community/invitation/community` | [inviteJoinCommunity](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/InvitationController.java#L20) |

## LegacyDocumentController

兼容入口返回 **410 Gone**，请迁移到文档接口。

| HTTP | 服务 HTTP 路径 | 控制器方法 |
| --- | --- | --- |
| `ANY` | `/community/basis` | [retired](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/LegacyDocumentController.java#L11) |
| `ANY` | `/community/basis/**` | [retired](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/LegacyDocumentController.java#L11) |
| `ANY` | `/community/case` | [retired](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/LegacyDocumentController.java#L11) |
| `ANY` | `/community/case/**` | [retired](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/LegacyDocumentController.java#L11) |
| `ANY` | `/community/post` | [retired](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/LegacyDocumentController.java#L11) |
| `ANY` | `/community/post/**` | [retired](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/LegacyDocumentController.java#L11) |

## MessageController

| HTTP | 服务 HTTP 路径 | 控制器方法 |
| --- | --- | --- |
| `DELETE` | `/community/message/batch-delete` | [batchDelete](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/MessageController.java#L42) |
| `POST` | `/community/message/batch-upsert` | [batchUpsert](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/MessageController.java#L36) |
| `GET` | `/community/message/getAll` | [getAll](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/MessageController.java#L18) |
| `POST` | `/community/message/upsert` | [upsert](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/MessageController.java#L30) |
| `GET` | `/community/message/{id}` | [getById](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/MessageController.java#L24) |

## StorageController

| HTTP | 服务 HTTP 路径 | 控制器方法 |
| --- | --- | --- |
| `POST` | `/community/storage` | [upload](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/StorageController.java#L22) |
| `GET` | `/community/storage/read-url` | [readUrl](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/StorageController.java#L18) |
| `POST` | `/community/storage/read-urls` | [readUrls](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/StorageController.java#L14) |

## TagCommunityController

| HTTP | 服务 HTTP 路径 | 控制器方法 |
| --- | --- | --- |
| `DELETE` | `/community/tagcommunity/batch-delete` | [batchDelete](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/TagCommunityController.java#L42) |
| `POST` | `/community/tagcommunity/batch-upsert` | [batchUpsert](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/TagCommunityController.java#L36) |
| `GET` | `/community/tagcommunity/getAll` | [getAll](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/TagCommunityController.java#L18) |
| `POST` | `/community/tagcommunity/upsert` | [upsert](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/TagCommunityController.java#L30) |
| `GET` | `/community/tagcommunity/{id}` | [getById](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/TagCommunityController.java#L24) |

## TagController

| HTTP | 服务 HTTP 路径 | 控制器方法 |
| --- | --- | --- |
| `DELETE` | `/community/tag/batch-delete` | [batchDelete](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/TagController.java#L42) |
| `POST` | `/community/tag/batch-upsert` | [batchUpsert](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/TagController.java#L36) |
| `GET` | `/community/tag/getAll` | [getAll](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/TagController.java#L18) |
| `POST` | `/community/tag/upsert` | [upsert](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/TagController.java#L30) |
| `GET` | `/community/tag/{id}` | [getById](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/TagController.java#L24) |

## TagDocumentController

| HTTP | 服务 HTTP 路径 | 控制器方法 |
| --- | --- | --- |
| `DELETE` | `/community/tagdocument/batch-delete` | [batchDelete](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/TagDocumentController.java#L42) |
| `POST` | `/community/tagdocument/batch-upsert` | [batchUpsert](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/TagDocumentController.java#L36) |
| `GET` | `/community/tagdocument/getAll` | [getAll](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/TagDocumentController.java#L18) |
| `POST` | `/community/tagdocument/upsert` | [upsert](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/TagDocumentController.java#L30) |
| `GET` | `/community/tagdocument/{id}` | [getById](https://github.com/future-alisa/ScienceCommunity/blob/d10e11afb91e40a99457b91958a382b4015ef1e9/science_community/community_service/src/main/java/com/alisa/controller/TagDocumentController.java#L24) |
