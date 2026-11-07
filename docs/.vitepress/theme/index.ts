import DefaultTheme from 'vitepress/theme'
import ServiceDirectory from './components/ServiceDirectory.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) { app.component('ServiceDirectory', ServiceDirectory) }
}
