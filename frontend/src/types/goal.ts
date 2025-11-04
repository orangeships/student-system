// 财务目标相关类型定义

export interface FinancialGoal {
  id: number
  name: string
  goal_type: 'savings' | 'expense_limit'
  target_amount: number
  current_amount: number
  deadline?: string
  description?: string
  is_active: boolean
  user: number
  created_at: string
  updated_at: string
}

export interface FinancialGoalForm {
  name: string
  goal_type: 'savings' | 'expense_limit'
  target_amount: number
  current_amount?: number
  deadline?: string
  description?: string
  is_active?: boolean
}

export interface FinancialGoalSearchParams {
  search?: string
  goal_type?: string
  is_active?: boolean
  page?: number
  page_size?: number
  ordering?: string
}