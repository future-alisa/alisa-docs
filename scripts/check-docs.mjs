import { readFile, access } from 'node:fs/promises'
import { fileURLToPath } from 'node:url'
import path from 'node:path'

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const readJson = async file => JSON.parse(await readFile(path.join(root, file), 'utf8'))
const services = await readJson('docs/services/catalog.json')
const sources = await readJson('scripts/api-sources.json')
const index = await readJson('docs/public/api-index.json')
const names = new Set()
for (const service of services) {
  if (names.has(service.name)) throw new Error(`Duplicate service: ${service.name}`)
  names.add(service.name)
  if (!Number.isInteger(service.port) || !service.paths.length) throw new Error(`Incomplete service: ${service.name}`)
  const doc = service.doc.endsWith('/') ? `${service.doc}index.md` : `${service.doc}.md`
  await access(path.join(root, 'docs', doc))
}
const directory = await readJson('docs/services/groups.json')
const groupedNames = new Set()
const groupIds = new Set()
for (const group of directory) {
  if (groupIds.has(group.name)) throw new Error(`Duplicate directory group: ${group.name}`)
  groupIds.add(group.name)
  for (const member of group.services) {
    if (!names.has(member) || groupedNames.has(member)) throw new Error(`Invalid directory membership: ${member}`)
    groupedNames.add(member)
  }
  for (const endpoint of group.paths) {
    const url = new URL(endpoint)
    if (url.protocol !== 'https:' || url.hostname !== 'alisa.vip.cpolar.cn' || url.username || url.password) throw new Error(`Invalid public service URL: ${group.name}`)
  }
  await access(path.join(root, 'docs', `${group.doc}.md`))
}
if (groupedNames.size !== names.size) throw new Error('Directory groups must cover every catalog service')
if (index.schemaVersion !== 1 || !index.endpoints?.length) throw new Error('Missing generated API index')
const methods = new Set(['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD', 'TRACE', 'ANY'])
for (const source of sources) {
  if (!names.has(source.service)) throw new Error(`Unknown API service: ${source.service}`)
  await access(path.join(root, 'docs/api/generated', `${source.id}.md`))
  if (!index.endpoints.some(row => row.service === source.service)) throw new Error(`Empty API service: ${source.service}`)
}
for (const row of index.endpoints) {
  if (!names.has(row.service) || !methods.has(row.httpMethod) || !row.path.startsWith('/') || !row.source.startsWith('https://github.com/')) {
    throw new Error(`Invalid API row: ${row.service} ${row.path}`)
  }
}
console.log(`Validated ${services.length} services and ${index.endpoints.length} controller path combinations`)
