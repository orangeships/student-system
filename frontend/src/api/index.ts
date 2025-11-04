import axios from 'axios'
import { showError } from '@/utils/message'

const API_BASE_URL = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    console.error('API Error:', error)
    
    // 统一错误处理
    let errorMessage = '请求失败，请稍后重试'
    
    if (error.response) {
      // 服务器响应错误
      const status = error.response.status
      const data = error.response.data
      
      switch (status) {
        case 400:
          errorMessage = data.detail || '请求参数错误'
          break
        case 401:
          errorMessage = '未授权，请重新登录'
          break
        case 403:
          errorMessage = '权限不足'
          break
        case 404:
          errorMessage = '请求的资源不存在'
          break
        case 422:
          errorMessage = data.detail || '数据验证失败'
          break
        case 500:
          errorMessage = '服务器内部错误'
          break
        default:
          errorMessage = data.detail || `请求失败 (${status})`
      }
    } else if (error.request) {
      // 请求发送失败
      errorMessage = '网络连接失败，请检查网络设置'
    } else {
      // 请求配置错误
      errorMessage = error.message || '请求配置错误'
    }
    
    // 显示错误消息
    showError(errorMessage)
    
    return Promise.reject(error)
  }
)

export default api