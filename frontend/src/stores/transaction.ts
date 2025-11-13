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
      const response = await api.get('/api/transactions/transactions/', { params })
      console.log('交易列表API响应:', response.data)
      
      // 处理不同的响应格式
      if (response.data.code === 200 && response.data.data) {
        // 格式: {code: 200, data: {transactions: [...], pagination: {...}}}
        const data = response.data.data
        transactions.value = data.transactions || []
        totalCount.value = data.pagination?.total || data.transactions?.length || 0
      } else if (response.data.results) {
        // 标准分页格式: {results: [...], count: ...}
        transactions.value = response.data.results
        totalCount.value = response.data.count
      } else if (Array.isArray(response.data)) {
        // 简单数组格式
        transactions.value = response.data
        totalCount.value = response.data.length
      } else {
        console.warn('交易数据格式错误，期望数组但收到:', response.data)
        transactions.value = []
        totalCount.value = 0
      }
    } catch (error) {
      console.error('获取交易记录失败:', error)
      transactions.value = []
      totalCount.value = 0
      throw error
    } finally {
      loading.value = false
    }
  }

  // 搜索交易记录
  const searchTransactions = async (params: TransactionSearchParams = {}) => {
    loading.value = true
    try {
      const response = await api.get('/api/transactions/transactions/', { params })
      console.log('searchTransactions response:', response.data)
      
      // 处理多种可能的响应格式
      let data = response.data
      if (data.code === 200 && data.data) {
        // 格式: {code: 200, data: {transactions: [...], pagination: {...}}}
        transactions.value = data.data.transactions || []
        totalCount.value = data.data.pagination?.total || data.data.transactions?.length || 0
      } else if (data.results) {
        // 标准分页格式: {results: [...], count: ...}
        transactions.value = data.results
        totalCount.value = data.count || 0
      } else if (Array.isArray(data)) {
        // 简单数组格式
        transactions.value = data
        totalCount.value = data.length
      } else {
        // 未知格式，尝试直接赋值
        transactions.value = data.transactions || data.data || []
        totalCount.value = data.pagination?.total || 0
      }
    } catch (error) {
      console.error('搜索交易失败:', error)
      transactions.value = []
      totalCount.value = 0
      throw error
    } finally {
      loading.value = false
    }
  }

  // 获取单个交易
  const fetchTransaction = async (id: number) => {
    try {
      loading.value = true
      const response = await api.get(`/api/transactions/transactions/${id}/`)
      console.log('fetchTransaction response:', response.data)
      
      // 处理多种响应格式
      if (response.data.code === 200 && response.data.data) {
        currentTransaction.value = response.data.data
        return response.data.data
      } else {
        currentTransaction.value = response.data
        return response.data
      }
    } catch (error) {
      console.error('获取交易详情失败:', error)
      ElMessage.error('获取交易详情失败')
      throw error
    } finally {
      loading.value = false
    }
  }

  // 创建交易
  const createTransaction = async (data: CreateTransactionData) => {
    try {
      loading.value = true
      const response = await api.post('/api/transactions/transactions/', data)
      console.log('createTransaction response:', response.data)
      
      // 处理多种响应格式
      if (response.data.code === 201 && response.data.data) {
        return response.data.data
      } else {
        return response.data
      }
    } catch (error) {
      console.error('创建交易失败:', error)
      ElMessage.error('创建交易失败')
      throw error
    } finally {
      loading.value = false
    }
  }

  // 更新交易
  const updateTransaction = async (id: number, data: TransactionForm) => {
    try {
      loading.value = true
      const response = await api.put(`/api/transactions/transactions/${id}/`, data)
      console.log('updateTransaction response:', response.data)
      
      // 处理多种响应格式
      if (response.data.code === 200 && response.data.data) {
        return response.data.data
      } else {
        return response.data
      }
    } catch (error) {
      console.error('更新交易失败:', error)
      ElMessage.error('更新交易失败')
      throw error
    } finally {
      loading.value = false
    }
  }

  // 删除交易记录
  const deleteTransaction = async (id: number) => {
    try {
      loading.value = true
      const response = await api.delete(`/api/transactions/transactions/${id}/`)
      console.log('删除交易API响应:', response.data)
      await fetchTransactions() // 重新获取列表
      return response.data
    } catch (error) {
      console.error('删除交易记录失败:', error)
      ElMessage.error('删除交易失败')
      throw error
    } finally {
      loading.value = false
    }
  }

  // 批量删除交易记录
  const batchDeleteTransactions = async (ids: number[]) => {
    loading.value = true
    try {
      const response = await api.post('/api/transactions/transactions/batch_delete/', { ids })
      console.log('批量删除交易API响应:', response.data)
      await fetchTransactions() // 重新获取列表
      return response.data
    } catch (error) {
      console.error('批量删除交易记录失败:', error)
      ElMessage.error('批量删除交易失败')
      throw error
    } finally {
      loading.value = false
    }
  }

  // 获取交易统计摘要
  const fetchTransactionSummary = async (params: { start_date?: string; end_date?: string } = {}) => {
    try {
      const response = await api.get('/api/transactions/transactions/summary/', { params })
      console.log('fetchTransactionSummary response:', response.data)
      summary.value = response.data.data
      return response.data
    } catch (error) {
      console.error('获取交易统计失败:', error)
      ElMessage.error('获取交易统计失败')
      throw error
    }
  }

  // 获取分类趋势
  const fetchCategoryTrends = async (params: { start_date?: string; end_date?: string; transaction_type?: string } = {}) => {
    try {
      const response = await api.get('/api/transactions/transactions/category_trends/', { params })
      console.log('fetchCategoryTrends response:', response.data)
      categoryTrends.value = response.data.data
      return response.data
    } catch (error) {
      console.error('获取分类趋势失败:', error)
      ElMessage.error('获取分类趋势失败')
      throw error
    }
  }

  // 获取月度趋势
  const fetchMonthlyTrends = async (params: { start_date?: string; end_date?: string } = {}) => {
    try {
      const response = await api.get('/api/transactions/transactions/monthly_trends/', { params })
      console.log('fetchMonthlyTrends response:', response.data)
      monthlyTrends.value = response.data.data
      return response.data
    } catch (error) {
      console.error('获取月度趋势失败:', error)
      ElMessage.error('获取月度趋势失败')
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