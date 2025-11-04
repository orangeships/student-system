// 预算管理相关类型定义

export interface Budget {
  id: number
  category: number
  category_name: string
  amount: number
  period: 'monthly' | 'yearly'
  start_date: string
  end_date: string
  is_active: boolean
  user: number
  created_at: string
  updated_at: string
}

export interface BudgetForm {
  category: number
  amount: number
  period: 'monthly' | 'yearly'
  start_date: string
  end_date: string
  is_active?: boolean
}

export interface BudgetSearchParams {
  search?: string
  category?: string
  period?: string
  is_active?: boolean
  page?: number
  page_size?: number
  ordering?: string
}