import api from '@/api'

export interface FeeCategory {
  id?: number
  name: string
  description: string
  amount: number
  is_active: boolean
  created_at?: string
  updated_at?: string
}

export interface FeeRecord {
  id?: number
  student: number
  student_name?: string
  student_id?: string
  fee_category: number
  category_name?: string
  amount: number
  paid_amount?: number
  due_date: string
  paid_date?: string
  status: 'pending' | 'paid' | 'overdue' | 'cancelled'
  payment_method?: string
  notes?: string
  created_at?: string
  updated_at?: string
}

export interface Payment {
  id?: number
  fee_record: number
  amount: number
  payment_date: string
  payment_method: 'cash' | 'bank_transfer' | 'alipay' | 'wechat' | 'other'
  transaction_id?: string
  notes?: string
  created_at?: string
  updated_at?: string
}

export interface FeeRecordQuery {
  student?: number
  fee_category?: number
  status?: string
  due_date_after?: string
  due_date_before?: string
  ordering?: string
  page?: number
  page_size?: number
}

export interface PaymentStatistics {
  total_payments: number
  total_amount: number
  by_payment_method: Array<{ payment_method: string; total_amount: number; count: number }>
  monthly_stats: Array<{ month: string; total_amount: number; count: number }>
}

export interface PaginatedResponse<T> {
  count: number
  results: T[]
}

export const financeApi = {
  // 费用类别管理
  getCategories(): Promise<PaginatedResponse<FeeCategory>> {
    return api.get('/finance/categories/')
  },

  createCategory(data: FeeCategory) {
    return api.post('/finance/categories/', data)
  },

  updateCategory(id: number, data: FeeCategory) {
    return api.put(`/finance/categories/${id}/`, data)
  },

  deleteCategory(id: number) {
    return api.delete(`/finance/categories/${id}/`)
  },

  // 缴费记录管理
  getFeeRecords(params?: FeeRecordQuery): Promise<PaginatedResponse<FeeRecord>> {
    return api.get('/finance/records/', { params })
  },

  createFeeRecord(data: FeeRecord) {
    return api.post('/finance/records/', data)
  },

  updateFeeRecord(id: number, data: Partial<FeeRecord>) {
    return api.put(`/finance/records/${id}/`, data)
  },

  deleteFeeRecord(id: number) {
    return api.delete(`/finance/records/${id}/`)
  },

  // 支付记录管理
  getPayments(): Promise<PaginatedResponse<Payment>> {
    return api.get('/finance/payments/')
  },

  createPayment(data: Payment) {
    return api.post('/finance/payments/', data)
  },

  updatePayment(id: number, data: Payment) {
    return api.put(`/finance/payments/${id}/`, data)
  },

  deletePayment(id: number) {
    return api.delete(`/finance/payments/${id}/`)
  },

  // 统计信息
  getPaymentStatistics(params?: any) {
    return api.get('/finance/records/statistics/', { params })
  },
}