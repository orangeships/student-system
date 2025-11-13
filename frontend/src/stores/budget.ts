import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { 
  Budget, 
  BudgetForm, 
  BudgetSearchParams 
} from '@/types/budget'
import { api } from '@/utils/api'

export const useBudgetStore = defineStore('budget', () => {
  const budgets = ref<Budget[]>([])
  const loading = ref(false)
  const totalCount = ref(0)
  const currentBudget = ref<Budget | null>(null)
  
  // 计算总预算金额
  const totalBudget = computed(() => {
    return budgets.value.reduce((sum, budget) => sum + budget.amount, 0)
  })

  // 获取预算列表
  const fetchBudgets = async (params: BudgetSearchParams = {}) => {
    loading.value = true
    try {
      const response = await api.get('/api/transactions/budgets/', { params })
      const data = response.data.results || response.data
      
      // 数据格式验证
      if (!Array.isArray(data)) {
        console.warn('预算数据格式错误，期望数组，实际:', typeof data)
        budgets.value = []
        totalCount.value = 0
      } else {
        budgets.value = data
        totalCount.value = response.data.count || data.length
      }
    } catch (error) {
      console.error('获取预算失败:', error)
      budgets.value = []
      totalCount.value = 0
      throw error
    } finally {
      loading.value = false
    }
  }

  // 搜索预算
  const searchBudgets = async (params: BudgetSearchParams = {}) => {
    loading.value = true
    try {
      const response = await api.get('/api/transactions/budgets/', { params })
      const data = response.data.results || response.data
      
      // 数据格式验证
      if (!Array.isArray(data)) {
        console.warn('搜索预算数据格式错误，期望数组，实际:', typeof data)
        budgets.value = []
        totalCount.value = 0
      } else {
        budgets.value = data
        totalCount.value = response.data.count || data.length
      }
    } catch (error) {
      console.error('搜索预算失败:', error)
      budgets.value = []
      totalCount.value = 0
      throw error
    } finally {
      loading.value = false
    }
  }

  // 获取单个预算
  const fetchBudget = async (id: number) => {
    loading.value = true
    try {
      const response = await api.get(`/api/transactions/budgets/${id}/`)
      currentBudget.value = response.data
      return response.data
    } catch (error) {
      console.error('获取预算失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 创建预算
  const createBudget = async (data: BudgetForm) => {
    loading.value = true
    try {
      const response = await api.post('/api/transactions/budgets/', data)
      await fetchBudgets() // 重新获取列表
      return response.data
    } catch (error) {
      console.error('创建预算失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 更新预算
  const updateBudget = async (id: number, data: BudgetForm) => {
    loading.value = true
    try {
      const response = await api.put(`/api/transactions/budgets/${id}/`, data)
      await fetchBudgets() // 重新获取列表
      return response.data
    } catch (error) {
      console.error('更新预算失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 删除预算
  const deleteBudget = async (id: number) => {
    loading.value = true
    try {
      await api.delete(`/api/transactions/budgets/${id}/`)
      await fetchBudgets() // 重新获取列表
    } catch (error) {
      console.error('删除预算失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 批量删除预算
  const batchDeleteBudgets = async (ids: number[]) => {
    loading.value = true
    try {
      await api.post('/api/transactions/budgets/batch_delete/', { ids })
      await fetchBudgets() // 重新获取列表
    } catch (error) {
      console.error('批量删除预算失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  return {
    // 状态
    budgets,
    loading,
    totalCount,
    currentBudget,
    totalBudget,
    
    // 方法
    fetchBudgets,
    searchBudgets,
    fetchBudget,
    createBudget,
    updateBudget,
    deleteBudget,
    batchDeleteBudgets
  }
})