// 分类相关类型定义

export interface Category {
  id: number
  name: string
  category_type: 'income' | 'expense'
  icon?: string
  color?: string
  description?: string
  user: number
  created_at: string
  updated_at: string
}

export interface CategoryForm {
  name: string
  category_type: 'income' | 'expense'
  icon?: string
  color?: string
  description?: string
}

export interface CategorySearchParams {
  search?: string
  category_type?: string
  page?: number
  page_size?: number
  ordering?: string
}