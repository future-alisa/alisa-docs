import { readFile, writeFile, mkdir } from 'node:fs/promises'
import { execFileSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'
import path from 'node:path'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const git = (...args) => execFileSync('git', args, { cwd: root, encoding: 'utf8' }).trim()
if (git('status', '--porcelain')) throw new Error('请先提交文档与源码变更，再生成发布清单；构建只读取已提交的源码。')
const revision = git('rev-parse', 'HEAD')
const config = JSON.parse(await readFile(path.join(root, 'deploy/release-config.json'), 'utf8'))
const image = `${config.registry}/alisa-docs:src-${revision.slice(0, 12)}`
const values = { ...config, revision, image, shortRevision: revision.slice(0, 12) }
for (const [key, value] of Object.entries(values)) {
  if (typeof value !== 'string' || /[\r\n"']/.test(value)) throw new Error(`Invalid release configuration: ${key}`)
}
if (!/^\/[a-z0-9/_-]*\/$/i.test(config.docsBase)) throw new Error('docsBase must include a leading and trailing slash')
await mkdir(path.join(root, 'deploy/production'), { recursive: true })
await mkdir(path.join(root, 'deploy/argocd'), { recursive: true })
for (const [template, output] of [
  ['build.yaml.tmpl', 'production/build.yaml'],
  ['site.yaml.tmpl', 'production/site.yaml'],
  ['application.yaml.tmpl', 'argocd/application.yaml']
]) {
  let text = await readFile(path.join(root, 'deploy/templates', template), 'utf8')
  text = text.replace(/@@(\w+)@@/g, (_, key) => {
    if (!(key in values)) throw new Error(`Missing template value: ${key}`)
    return values[key]
  })
  await writeFile(path.join(root, 'deploy', output), text)
}
console.log(`Prepared source ${revision}\nImage: ${image}\nURL: https://${config.publicHost}${config.docsBase}`)
console.log('提交 deploy/production 和 deploy/argocd 的生成清单，push 后在 Argo CD 同步 alisa-docs。')
