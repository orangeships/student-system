import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { 
  Transaction, 
  TransactionForm, 
  TransactionSearchParams, 
  TransactionSummary,
  CategoryTrend,
  MonthlyTrend
} from '@/types/transaction'
import { api } from '@/utils/api'

export const useTransactionStore = defineStore('transaction', () => {
  const transactions = ref<Transaction[]>([])
  const loading = ref(false)
  const totalCount = ref(0)
  const currentTransaction = ref<Transaction | null>(null)
  const summary = ref<TransactionSummary | null>(null)
  const categoryTrends = ref<CategoryTrend[]>([])
  const monthlyTrends = ref<MonthlyTrend[]>([])

  // 获取交易记录列表
  const fetchTransactions = async (params: TransactionSearchParams = {}) => {
    loading.value = true
    try {
      const response = await api.get('/api/transactions/', { params })
      transactions.value = response.data.results || response.data
      totalCount.value = response.data.count || transactions.value.length
    } catch (error) {
      console.error('获取交易记录失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 搜索交易记录
  const searchTransactions = async (params: TransactionSearchParams = {}) => {
    loading.value = true
    try {
      const response = await api.get('/api/transactions/', { params })
      transactions.value = response.data.results || response.data
      totalCount.value = response.data.count || transactions.value.length
    } catch (error) {
      console.error('搜索交易记录失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 获取单个交易记录
  const fetchTransaction = async (id: number) => {
    loading.value = true
    try {
      const response = await api.get(`/api/transactions/${id}/`)
      currentTransaction.value = response.data
      return response.data
    } catch (error) {
      console.error('获取交易记录失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 创建交易记录
  const createTransaction = async (data: TransactionForm) => {
    loading.value = true
    try {
      const response = await api.post('/api/transactions/', data)
      await fetchTransactions() // 重新获取列表
      return response.data
    } catch (error) {
      console.error('创建交易记录失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 更新交易记录
  const updateTransaction = async (id: number, data: TransactionForm) => {
    loading.value = true
    try {
      const response = await api.put(`/api/transactions/${id}/`, data)
      await fetchTransactions() // 重新获取列表
      return response.data
    } catch (error) {
      console.error('更新交易记录失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 删除交易记录
  const deleteTransaction = async (id: number) => {
    loading.value = true
    try {
      await api.delete(`/api/transactions/${id}/`)
      await fetchTransactions() // 重新获取列表
    } catch (error) {
      console.error('删除交易记录失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 批量删除交易记录
  const batchDeleteTransactions = async (ids: number[]) => {
    loading.value = true
    try {
      await api.post('/api/transactions/batch_delete/', { ids })
      await fetchTransactions() // 重新获取列表
    } catch (error) {
      console.error('批量删除交易记录失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 获取交易统计摘要
  const fetchTransactionSummary = async (params: { start_date?: string; end_date?: string } = {}) => {
    try {
      const response = await api.get('/api/transactions/summary/', { params })
      summary.value = response.data
      return response.data
    } catch (error) {
      console.error('获取交易统计失败:', error)
      throw error
    }
  }

  // 获取分类趋势
  const fetchCategoryTrends = async (params: { start_date?: string; end_date?: string; transaction_type?: string } = {}) => {
    try {
      const response = await api.get('/api/transactions/category_trends/', { params })
      categoryTrends.value = response.data
      return response.data
    } catch (error) {
      console.error('获取分类趋势失败:', error)
      throw error
    }
  }

  // 获取月度趋势
  const fetchMonthlyTrends = async (params: { start_date?: string; end_date?: string } = {}) => {
    try {
      const response = await api.get('/api/transactions/monthly_trends/', { params })
      monthlyTrends.value = response.data
      return response.data
    } catch (error) {
      console.error('获取月度趋势失败:', error)
      throw error
    }
  }

  return {
    // 状态
    transactions,
    loading,
    totalCount,
    currentTransaction,
    summary,
    categoryTrends,
    monthlyTrends,
    
    // 方法
    fetchTransactions,
    searchTransactions,
    fetchTransaction,
    createTransaction,
    updateTransaction,
    deleteTransaction,
    batchDeleteTransactions,
    fetchTransactionSummary,
    fetchCategoryTrends,
    fetchMonthlyTrends
  }
})