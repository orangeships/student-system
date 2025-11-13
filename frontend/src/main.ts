import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(ElementPlus)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.mount('#app')

// 自动登录测试用户（仅用于开发测试）
if (import.meta.env.DEV) {
  const authStore = useAuthStore()
  
  // 如果还没有登录，自动登录测试用户
  if (!authStore.isAuthenticated) {
    console.log('🚀 [DEV] 自动登录测试用户...')
    authStore.login('testuser', 'testpass123').then(result => {
      if (result.success) {
        console.log('✅ [DEV] 自动登录成功！')
      } else {
        console.log('❌ [DEV] 自动登录失败:', result.error)
      }
    })
  } else {
    console.log('✅ [DEV] 用户已登录，跳过自动登录')
  }
}
