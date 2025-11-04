import '@testing-library/jest-dom'
import { vi } from 'vitest'

// Mock Element Plus组件
vi.mock('element-plus', () => ({
  ElMessage: {
    success: vi.fn(),
    error: vi.fn(),
    warning: vi.fn(),
    info: vi.fn(),
    closeAll: vi.fn()
  },
  ElMessageBox: {
    confirm: vi.fn()
  },
  ElNotification: vi.fn()
}))

// Mock Element Plus图标
vi.mock('@element-plus/icons-vue', () => ({
  HomeFilled: {},
  UserFilled: {},
  Money: {},
  TrendCharts: {},
  Refresh: {},
  Search: {},
  Plus: {},
  Edit: {},
  Delete: {},
  View: {}
}))

// 全局测试配置
global.ResizeObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}))