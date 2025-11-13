import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import axios from 'axios'

// 创建带调试功能的axios实例
const debugAxios = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
  }
})

// 详细的请求拦截器
debugAxios.interceptors.request.use(
  (config) => {
    console.log('🚀 [DEBUG] 请求配置:', {
      url: config.url,
      method: config.method,
      headers: config.headers,
      data: config.data,
      baseURL: config.baseURL
    })
    
    // 确保有正确的Content-Type
    if (!config.headers['Content-Type']) {
      config.headers['Content-Type'] = 'application/json'
      console.log('📝 [DEBUG] 设置Content-Type为application/json')
    }
    
    return config
  },
  (error) => {
    console.error('❌ [DEBUG] 请求拦截器错误:', error)
    return Promise.reject(error)
  }
)

// 详细的响应拦截器
debugAxios.interceptors.response.use(
  (response) => {
    console.log('✅ [DEBUG] 响应成功:', {
      url: response.config.url,
      status: response.status,
      statusText: response.statusText,
      headers: response.headers,
      data: response.data
    })
    return response
  },
  (error) => {
    console.error('❌ [DEBUG] 响应错误:', {
      url: error.config?.url,
      method: error.config?.method,
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      headers: error.response?.headers,
      message: error.message
    })
    
    return Promise.reject(error)
  }
)

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || '')
  const user = ref(JSON.parse(localStorage.getItem('user') || 'null'))
  const loading = ref(false)
  const error = ref('')

  const isAuthenticated = computed(() => {
    const hasToken = !!token.value
    console.log('🔐 [DEBUG] isAuthenticated检查:', { token: token.value, hasToken })
    return hasToken
  })

  const login = async (username: string, password: string) => {
    console.log('🎯 [DEBUG] 开始登录流程:', { username, password: '***' })
    loading.value = true
    error.value = ''
    
    try {
      // 确保使用正确的Content-Type
      const loginData = { username, password }
      console.log('📤 [DEBUG] 发送登录数据:', loginData)
      
      const response = await debugAxios.post('/auth/login/', loginData)
      
      console.log('📥 [DEBUG] 登录响应:', response.data)
      
      if (response.data && response.data.data && response.data.data.token) {
        const newToken = response.data.data.token
        const newUser = response.data.data.user || { username }
        
        console.log('💾 [DEBUG] 保存认证数据:', { token: newToken, user: newUser })
        
        token.value = newToken
        user.value = newUser
        localStorage.setItem('token', newToken)
        localStorage.setItem('user', JSON.stringify(newUser))
        
        console.log('✨ [DEBUG] 登录成功，更新后的状态:', { token: token.value, user: user.value })
        
        return { success: true, data: response.data }
      } else {
        console.error('❌ [DEBUG] 登录响应格式错误:', response.data)
        error.value = '登录响应格式错误'
        return { success: false, error: error.value }
      }
    } catch (err: any) {
      console.error('💥 [DEBUG] 登录失败:', err)
      
      if (err.response?.status === 400) {
        error.value = err.response.data.message || '用户名或密码错误'
      } else if (err.response?.status === 401) {
        error.value = '未授权'
      } else if (!err.response) {
        error.value = '网络连接失败，请检查服务器是否运行'
      } else {
        error.value = err.response?.data?.message || '登录失败'
      }
      
      console.error('🚫 [DEBUG] 设置错误信息:', error.value)
      return { success: false, error: error.value }
    } finally {
      loading.value = false
      console.log('🏁 [DEBUG] 登录流程结束，最终状态:', { loading: loading.value, error: error.value })
    }
  }

  const register = async (username: string, password: string, email?: string) => {
    loading.value = true
    error.value = ''
    
    try {
      const response = await debugAxios.post('/auth/register/', {
        username,
        password,
        email
      })
      
      if (response.data && response.data.data && response.data.data.token) {
        token.value = response.data.data.token
        user.value = response.data.data.user || { username }
        localStorage.setItem('token', token.value)
        localStorage.setItem('user', JSON.stringify(user.value))
        
        return { success: true, data: response.data }
      }
      
      return { success: true, data: response.data }
    } catch (err: any) {
      if (err.response?.status === 400) {
        error.value = err.response.data.message || '注册失败'
      } else {
        error.value = err.response?.data?.message || '注册失败'
      }
      
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    console.log('🚪 [DEBUG] 登出')
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('user')
  }

  const updateUser = (userData: any) => {
    console.log('🔄 [DEBUG] 更新用户信息:', userData)
    user.value = { ...user.value, ...userData }
    localStorage.setItem('user', JSON.stringify(user.value))
  }

  return {
    token,
    user,
    loading,
    error,
    isAuthenticated,
    login,
    register,
    logout,
    updateUser
  }
})