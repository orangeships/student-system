// 交易记录相关类型定义

export interface Transaction {
  id: number
  transaction_date: string
  transaction_type: 'income' | 'expense'
  category: number
  category_name: string
  amount: number
  payment_method: string
  description?: string
  user: number
  created_at: string
  updated_at: string
}

export interface TransactionForm {
  transaction_date: string
  transaction_type: 'income' | 'expense'
  category: number | string
  amount: number
  payment_method: string
  description?: string
}

export interface TransactionSearchParams {
  search?: string
  transaction_type?: string
  category?: string
  dateRange?: string[]
  page?: number
  page_size?: number
  ordering?: string
}

export interface TransactionSummary {
  total_income: number
  total_expense: number
  net_amount: number
  transaction_count: number
  income_count: number
  expense_count: number
}

export interface CategoryTrend {
  category_name: string
  category_type: string
  total_amount: number
  percentage: number
}

export interface MonthlyTrend {
  month: string
  income: number
  expense: number
  net: number
}