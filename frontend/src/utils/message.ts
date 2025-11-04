import { ElMessage, ElMessageBox, ElNotification } from 'element-plus'
import type { MessageOptions } from 'element-plus'

export interface MessageConfig {
  duration?: number
  showClose?: boolean
  center?: boolean
  offset?: number
  icon?: string | any
  customClass?: string
  grouping?: boolean
}

const defaultConfig: MessageConfig = {
  duration: 3000,
  showClose: true,
  grouping: true
}

/**
 * 成功消息
 */
export const showSuccess = (message: string, config?: MessageConfig) => {
  ElMessage.success({
    message,
    ...defaultConfig,
    ...config
  })
}

/**
 * 错误消息
 */
export const showError = (message: string, config?: MessageConfig) => {
  ElMessage.error({
    message,
    ...defaultConfig,
    ...config
  })
}

/**
 * 警告消息
 */
export const showWarning = (message: string, config?: MessageConfig) => {
  ElMessage.warning({
    message,
    ...defaultConfig,
    ...config
  })
}

/**
 * 信息消息
 */
export const showInfo = (message: string, config?: MessageConfig) => {
  ElMessage.info({
    message,
    ...defaultConfig,
    ...config
  })
}

/**
 * 确认对话框
 */
export const showConfirm = async (
  message: string,
  title = '确认',
  options?: {
    confirmButtonText?: string
    cancelButtonText?: string
    type?: 'info' | 'success' | 'warning' | 'error'
  }
) => {
  try {
    await ElMessageBox.confirm(message, title, {
      confirmButtonText: options?.confirmButtonText || '确定',
      cancelButtonText: options?.cancelButtonText || '取消',
      type: options?.type || 'warning',
      lockScroll: false
    })
    return true
  } catch {
    return false
  }
}

/**
 * 通知消息
 */
export const showNotification = (options: {
  title: string
  message: string
  type?: 'success' | 'error' | 'warning' | 'info'
  duration?: number
  position?: 'top-right' | 'top-left' | 'bottom-right' | 'bottom-left'
}) => {
  ElNotification({
    ...options,
    duration: options.duration || 4500,
    position: options.position || 'top-right'
  })
}

/**
 * 处理API错误
 */
export const handleApiError = (error: any, defaultMessage = '操作失败') => {
  let message = defaultMessage
  
  if (error?.response?.data) {
    const { data } = error.response
    if (typeof data === 'object' && data !== null) {
      if (data.detail) {
        message = data.detail
      } else if (data.message) {
        message = data.message
      } else if (Array.isArray(data.errors)) {
        message = data.errors.map((err: any) => 
          typeof err === 'string' ? err : err.message || err.field
        ).join('\n')
      } else {
        message = Object.values(data).flat().join('\n')
      }
    } else if (typeof data === 'string') {
      message = data
    }
  } else if (error?.message) {
    message = error.message
  } else if (typeof error === 'string') {
    message = error
  }
  
  showError(message)
  return message
}

/**
 * 处理请求结果
 */
export const handleRequest = async <T>(
  request: () => Promise<T>,
  options?: {
    loading?: boolean
    success?: boolean | string
    error?: boolean | string
    finally?: () => void
  }
): Promise<T | null> => {
  try {
    const result = await request()
    
    if (options?.success !== false) {
      const message = typeof options?.success === 'string' ? options.success : '操作成功'
      showSuccess(message)
    }
    
    return result
  } catch (error) {
    if (options?.error !== false) {
      const message = typeof options?.error === 'string' ? options.error : undefined
      handleApiError(error, message)
    }
    return null
  } finally {
    if (options?.finally) {
      options.finally()
    }
  }
}

/**
 * 显示加载状态
 */
export const showLoading = (message = '加载中...') => {
  return ElMessage({
    message,
    duration: 0,
    icon: 'Loading',
    customClass: 'loading-message'
  })
}

/**
 * 关闭所有消息
 */
export const closeAllMessages = () => {
  ElMessage.closeAll()
}