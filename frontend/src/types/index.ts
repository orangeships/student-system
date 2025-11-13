// 用户类型定义
export interface User {
  id: number
  username: string
  email: string
  first_name?: string
  last_name?: string
  date_joined?: string
  is_active?: boolean
}

// 交易类型定义
export interface Transaction {
  id: number
  user: number
  category: Category
  amount: number
  transaction_type: 'income' | 'expense'
  description: string
  transaction_date: string
  created_at: string
  updated_at: string
}

// 分类类型定义
export interface Category {
  id: number
  name: string
  type: 'income' | 'expense'
  color: string
  icon: string
  description: string
  is_active: boolean
}

// 预算类型定义
export interface Budget {
  id: number
  user: number
  category: Category
  amount: number
  period: 'monthly' | 'weekly' | 'yearly'
  start_date: string
  end_date: string
  is_active: boolean
  created_at: string
  updated_at: string
}

// 预警类型定义
export interface Alert {
  id: number
  user: number
  type: 'budget' | 'transaction' | 'system'
  title: string
  message: string
  level: 'info' | 'warning' | 'error'
  related_data?: any
  is_read: boolean
  created_at: string
}

// 统计类型定义
export interface Statistics {
  total_income: number
  total_expense: number
  net_income: number
  transaction_count: number
  category_breakdown: Array<{
    category: string
    amount: number
    percentage: number
  }>
  monthly_trend: Array<{
    month: string
    income: number
    expense: number
  }>
}

// API响应类型定义
export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
  errors?: Record<string, string[]>
}

// 分页响应类型定义
export interface PaginatedResponse<T = any> {
  code: number
  message: string
  data: {
    count: number
    next: string | null
    previous: string | null
    results: T[]
  }
}

// 登录响应类型定义
export interface LoginResponse {
  token: string
  user: User
}

// 注册响应类型定义
export interface RegisterResponse {
  token: string
  user: User
}