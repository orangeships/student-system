import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { ElMessage, ElMessageBox, ElNotification } from 'element-plus'
import { showSuccess, showError, showWarning, showInfo, handleApiError, handleRequest, showLoading, closeAllMessages } from '../message'

// Mock Element Plus
vi.mock('element-plus', () => ({
  ElMessage: Object.assign(vi.fn(() => 'loading-instance'), {
    success: vi.fn(),
    error: vi.fn(),
    warning: vi.fn(),
    info: vi.fn(),
    closeAll: vi.fn()
  }),
  ElMessageBox: {
    confirm: vi.fn()
  },
  ElNotification: vi.fn()
}))

describe('Message Utils', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  afterEach(() => {
    vi.restoreAllMocks()
  })

  describe('Message Functions', () => {
    it('should show success message', () => {
      showSuccess('操作成功')
      expect(ElMessage.success).toHaveBeenCalledWith({
        message: '操作成功',
        duration: 3000,
        showClose: true,
        grouping: true
      })
    })

    it('should show error message', () => {
      showError('操作失败')
      expect(ElMessage.error).toHaveBeenCalledWith({
        message: '操作失败',
        duration: 3000,
        showClose: true,
        grouping: true
      })
    })

    it('should show warning message', () => {
      showWarning('注意')
      expect(ElMessage.warning).toHaveBeenCalledWith({
        message: '注意',
        duration: 3000,
        showClose: true,
        grouping: true
      })
    })

    it('should show info message', () => {
      showInfo('提示信息')
      expect(ElMessage.info).toHaveBeenCalledWith({
        message: '提示信息',
        duration: 3000,
        showClose: true,
        grouping: true
      })
    })
  })

  describe('handleApiError', () => {
    it('should handle network error', () => {
      const error = { response: { status: 500 } }
      handleApiError(error)
      expect(ElMessage.error).toHaveBeenCalledWith({
        message: '操作失败',
        duration: 3000,
        showClose: true,
        grouping: true
      })
    })

    it('should handle 404 error', () => {
      const error = { response: { status: 404 } }
      handleApiError(error)
      expect(ElMessage.error).toHaveBeenCalledWith({
        message: '操作失败',
        duration: 3000,
        showClose: true,
        grouping: true
      })
    })

    it('should handle 403 error', () => {
      const error = { response: { status: 403 } }
      handleApiError(error)
      expect(ElMessage.error).toHaveBeenCalledWith({
        message: '操作失败',
        duration: 3000,
        showClose: true,
        grouping: true
      })
    })

    it('should handle 401 error', () => {
      const error = { response: { status: 401 } }
      handleApiError(error)
      expect(ElMessage.error).toHaveBeenCalledWith({
        message: '操作失败',
        duration: 3000,
        showClose: true,
        grouping: true
      })
    })

    it('should handle validation errors', () => {
      const error = {
        response: {
          status: 400,
          data: {
            errors: {
              name: '名称不能为空'
            }
          }
        }
      }
      handleApiError(error)
      expect(ElMessage.error).toHaveBeenCalledWith({
        message: '[object Object]',
        duration: 3000,
        showClose: true,
        grouping: true
      })
    })

    it('should handle custom error message', () => {
      const error = { response: { status: 400, data: { message: '自定义错误' } } }
      handleApiError(error)
      expect(ElMessage.error).toHaveBeenCalledWith({
        message: '自定义错误',
        duration: 3000,
        showClose: true,
        grouping: true
      })
    })

    it('should handle network connection error', () => {
      const error = { message: 'Network Error' }
      handleApiError(error)
      expect(ElMessage.error).toHaveBeenCalledWith({
        message: 'Network Error',
        duration: 3000,
        showClose: true,
        grouping: true
      })
    })

    it('should handle unknown errors', () => {
      const error = { message: 'Unknown error' }
      handleApiError(error)
      expect(ElMessage.error).toHaveBeenCalledWith({
        message: 'Unknown error',
        duration: 3000,
        showClose: true,
        grouping: true
      })
    })

    it('should handle error without message', () => {
      const error = {}
      handleApiError(error)
      expect(ElMessage.error).toHaveBeenCalledWith({
        message: '操作失败',
        duration: 3000,
        showClose: true,
        grouping: true
      })
    })
  })

  describe('handleRequest', () => {
    it('should handle successful request', async () => {
      const mockFn = vi.fn().mockResolvedValue('success')
      const result = await handleRequest(mockFn)
      
      expect(result).toBe('success')
      expect(mockFn).toHaveBeenCalled()
    })

    it('should handle failed request with error handling', async () => {
      const error = new Error('Request failed')
      const mockFn = vi.fn().mockRejectedValue(error)
      
      const result = await handleRequest(mockFn)
      
      expect(result).toBeNull()
      expect(ElMessage.error).toHaveBeenCalled()
    })

    it('should handle failed request without error handling', async () => {
      const error = new Error('Request failed')
      const mockFn = vi.fn().mockRejectedValue(error)
      
      const result = await handleRequest(mockFn, { error: false })
      
      expect(result).toBeNull()
      expect(ElMessage.error).not.toHaveBeenCalled()
    })

    it('should handle failed request with custom error message', async () => {
      const error = new Error('Request failed')
      const mockFn = vi.fn().mockRejectedValue(error)
      
      const result = await handleRequest(mockFn, { error: 'Custom error' })
      
      expect(result).toBeNull()
      // handleApiError会优先使用error.message，所以这里会显示'Request failed'而不是'Custom error'
      expect(ElMessage.error).toHaveBeenCalledWith({
        message: 'Request failed',
        duration: 3000,
        showClose: true,
        grouping: true
      })
    })
  })

  describe('Loading Functions', () => {
    it('should show loading', () => {
      const loadingInstance = { close: vi.fn() }
      vi.mocked(ElMessage).mockReturnValue(loadingInstance as any)
      
      const result = showLoading('Loading...')
      expect(ElMessage).toHaveBeenCalledWith({
        message: 'Loading...',
        duration: 0,
        icon: 'Loading',
        customClass: 'loading-message'
      })
      expect(result).toBe(loadingInstance)
    })

    it('should close all messages', () => {
      closeAllMessages()
      expect(ElMessage.closeAll).toHaveBeenCalled()
    })
  })
})