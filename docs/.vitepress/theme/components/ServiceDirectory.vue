<script setup>
import { computed, ref } from 'vue'
import { withBase } from 'vitepress'
import services from '../../../services/groups.json'
const selected = ref('全部')
const query = ref('')
const groups = ['全部', ...new Set(services.map(service => service.project))]
const filtered = computed(() => services.filter(service =>
  (selected.value === '全部' || service.project === selected.value) &&
  `${service.project} ${service.project.replaceAll(' ', '')} ${service.name} ${service.title} ${service.description} ${service.services.join(' ')} ${service.paths.join(' ')}`
    .toLowerCase().includes(query.value.trim().toLowerCase())
))
</script>

<template>
  <div class="service-directory">
    <div class="directory-tools">
      <div class="filters" role="group" aria-label="按项目筛选服务">
        <button v-for="group in groups" :key="group" :aria-pressed="selected === group"
          :class="{ active: selected === group }" @click="selected = group">{{ group }}</button>
      </div>
      <label class="service-search"><span class="sr-only">查找服务或路由</span>
        <input v-model="query" type="search" placeholder="查找服务或路由…" />
      </label>
    </div>
    <p class="result-count" role="status" aria-live="polite">{{ filtered.length }} 个服务入口 · 按业务项目组织</p>
    <div class="service-grid">
      <a v-for="service in filtered" :key="service.name" class="service-card" :href="withBase(service.doc)">
        <div class="card-top"><span class="project">{{ service.project }}</span><span class="port">{{ service.status }}</span></div>
        <h3>{{ service.title }}</h3><code>{{ service.name }}</code>
        <p>{{ service.description }}</p>
        <div class="paths"><span v-for="path in service.paths" :key="path">{{ path }}</span></div>
        <span class="card-action">查看文档 <span aria-hidden="true">↗</span></span>
      </a>
    </div>
    <p v-if="!filtered.length" class="empty">没有匹配的服务。可以尝试服务名、项目名或路径前缀。</p>
  </div>
</template>

<style scoped>
.directory-tools { display: flex; justify-content: space-between; align-items: center; gap: 16px; flex-wrap: wrap; }
.filters { display: flex; flex-wrap: wrap; gap: 6px; }
.filters button { border: 1px solid var(--vp-c-divider); border-radius: 7px; padding: 7px 12px; font-size: 13px; transition: background .15s; }
.filters button.active { background: var(--vp-c-brand-soft); color: var(--vp-c-brand-1); border-color: var(--vp-c-brand-1); }
.filters button:focus-visible, input:focus-visible, .service-card:focus-visible { outline: 2px solid var(--vp-c-brand-1); outline-offset: 3px; }
.service-search input { padding: 9px 13px; border: 1px solid var(--vp-c-divider); border-radius: 7px; min-width: 220px; font-size: 14px; background: var(--vp-c-bg-soft); }
.result-count { color: var(--vp-c-text-3); font-size: 12px; margin: 15px 0; }
.service-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr)); gap: 16px; }
.service-card { padding: 24px; border: 1px solid var(--vp-c-divider); border-radius: 12px; background: var(--vp-c-bg); display: flex; flex-direction: column; transition: border-color .15s; }
.service-card:hover { border-color: var(--vp-c-brand-1); }
.card-top { display: flex; justify-content: space-between; align-items: center; gap: 8px; flex-wrap: wrap; margin-bottom: 20px; }
.project { font-size: 11px; color: var(--vp-c-brand-1); padding: 2px 7px; background: var(--vp-c-brand-soft); border-radius: 4px; }
.port { font-size: 12px; font-family: var(--vp-font-family-mono); color: var(--vp-c-text-3); }
h3 { margin: 0 0 5px; font-size: 19px; font-weight: 650; }
.service-card code { font-size: 12px; color: var(--vp-c-text-2); }
.service-card p { color: var(--vp-c-text-2); font-size: 14px; line-height: 1.7; margin: 14px 0; }
.paths { display: flex; gap: 5px; flex-wrap: wrap; margin-top: auto; }
.paths span { background: var(--vp-c-bg-soft); color: var(--vp-c-text-2); font-size: 11px; border-radius: 4px; padding: 3px 6px; overflow-wrap: anywhere; }
.card-action { color: var(--vp-c-brand-1); font-size: 12px; margin-top: 18px; }
.empty { padding: 40px 0; color: var(--vp-c-text-2); }
.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0; }
@media (max-width: 600px) { .service-grid { grid-template-columns: 1fr; } .service-search, .service-search input { width: 100%; } }
</style>
