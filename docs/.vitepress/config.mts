import { defineConfig } from 'vitepress'

export default defineConfig({
  lang: 'zh-CN',
  title: 'Alisa Docs',
  description: 'Alisa 服务目录、接口索引与部署文档',
  base: process.env.DOCS_BASE || '/',
  cleanUrls: true,
  lastUpdated: process.env.DOCS_ARCHIVE_BUILD !== 'true',
  head: [['link', { rel: 'icon', type: 'image/svg+xml', href: `${process.env.DOCS_BASE || '/'}logo.svg` }]],
  themeConfig: {
    logo: '/logo.svg',
    siteTitle: 'Alisa Docs',
    nav: [
      { text: '开始使用', link: '/guide/getting-started' },
      { text: '平台架构', link: '/guide/architecture' },
      { text: '服务目录', link: '/services/' },
      { text: '线上入口', link: '/services/deployed' },
      { text: '接口索引', link: '/api/' },
      { text: '部署运维', link: '/operations/deployment' }
    ],
    sidebar: [
      { text: '了解系统', items: [
        { text: '开始使用', link: '/guide/getting-started' },
        { text: '平台架构与服务职责', link: '/guide/architecture' },
        { text: 'Kubernetes 内部组件与拓扑', link: '/guide/kubernetes' },
        { text: '中间件与基础设施', link: '/guide/middleware' },
        { text: '组件交互流程', link: '/guide/interactions' },
        { text: '标准开发流程', link: '/guide/development-workflow' },
        { text: '开发接入指南', link: '/guide/development-integration' },
        { text: '本地开发', link: '/guide/local-development' }
      ] },
      { text: '服务与接口', items: [
        { text: '服务目录', link: '/services/' },
        { text: '已部署服务与公网入口', link: '/services/deployed' },
        { text: 'SmallOKR API', link: '/services/smallokr' },
        { text: 'Science Community API 与应用', link: '/services/science-community' },
        { text: '平台门户与管理后台', link: '/services/portal' },
        { text: 'API 入口与覆盖范围', link: '/api/' },
        { text: '统一账号与授权', link: '/api/generated/account' }
      ] },
      { text: '接入与运维', items: [
        { text: '网关、Caddy 与动态路由', link: '/operations/gateway' },
        { text: '存储接入', link: '/operations/storage' },
        { text: '数据接入', link: '/operations/data' },
        { text: '认证与授权及服务地址', link: '/operations/authentication' },
        { text: 'OAuth2 接入与联调', link: '/operations/oauth2' },
        { text: '租户管理办法', link: '/operations/tenancy' },
        { text: '配置归属与对照', link: '/operations/configuration' },
        { text: '镜像与 Argo CD', link: '/operations/deployment' },
        { text: '排障与回滚', link: '/operations/troubleshooting' },
        { text: '维护这份文档', link: '/guide/contributing' }
      ] }
    ],
    search: {
      provider: 'local',
      options: {
        locales: { root: { translations: {
          button: { buttonText: '搜索文档', buttonAriaLabel: '搜索文档' },
          modal: { noResultsText: '没有找到相关内容', resetButtonTitle: '清除搜索',
            footer: { selectText: '选择', navigateText: '切换', closeText: '关闭' } }
        } } }
      }
    },
    socialLinks: [{ icon: 'github', link: 'https://github.com/future-alisa/alisa-docs' }],
    editLink: { pattern: 'https://github.com/future-alisa/alisa-docs/edit/main/docs/:path', text: '在 GitHub 上编辑' },
    outline: { level: [2, 3], label: '本页目录' },
    docFooter: { prev: '上一篇', next: '下一篇' },
    lastUpdated: { text: '最后更新', formatOptions: { dateStyle: 'medium' } },
    footer: { message: '接口以服务源码和运行时契约为准 · 运维配置由环境维护', copyright: 'Alisa Engineering' }
  }
})
