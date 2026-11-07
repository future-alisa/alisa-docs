---
layout: home
hero:
  name: Alisa Docs
  text: 服务、接口与部署，
    一处查阅。
  tagline: 连接 alisa-cloud、SmallOKR 与 ScienceCommunity 的开发文档。
  image:
    src: /logo.svg
    alt: Alisa
  actions:
    - theme: brand
      text: 从这里开始
      link: /guide/getting-started
    - theme: alt
      text: 查找接口
      link: /api/
features:
  - title: 理解平台
    details: 区分入口、业务服务、中间件和交付控制面，按步骤接入现有能力。
    link: /guide/architecture
  - title: 找到服务
    details: 按项目查看职责、源码默认端口与网关路径，明确公共能力和业务边界。
    link: /services/
  - title: 阅读接口
    details: 从控制器源码生成接口索引，保留条件启用说明与可追溯的源码链接。
    link: /api/
  - title: 完成部署
    details: 了解 Registry、Argo CD 与 Nacos 路由更新流程，按步骤验证和回滚。
    link: /operations/deployment
---

<section class="service-section" aria-labelledby="service-heading">
  <h2 id="service-heading">从一个服务开始</h2>
  <p class="intro">先找到服务，再查看接口与接入方式。这里是源码目录，不是实时监控面板。</p>
  <ServiceDirectory />
</section>
