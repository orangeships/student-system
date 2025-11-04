import { defineStore } from 'pinia'
import { ref } from 'vue'
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

  // 获取预算列表
  const fetchBudgets = async (params: BudgetSearchParams = {}) => {
    loading.value = true
    try {
      const response = await api.get('/api/budgets/', { params })
      budgets.value = response.data.results || response.data
      totalCount.value = response.data.count || budgets.value.length
    } catch (error) {
      console.error('获取预算失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 搜索预算
  const searchBudgets = async (params: BudgetSearchParams = {}) => {
    loading.value = true
    try {
      const response = await api.get('/api/budgets/', { params })
      budgets.value = response.data.results || response.data
      totalCount.value = response.data.count || budgets.value.length
    } catch (error) {
      console.error('搜索预算失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 获取单个预算
  const fetchBudget = async (id: number) => {
    loading.value = true
    try {
      const response = await api.get(`/api/budgets/${id}/`)
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
      const response = await api.post('/api/budgets/', data)
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
      const response = await api.put(`/api/budgets/${id}/`, data)
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
      await api.delete(`/api/budgets/${id}/`)
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
      await api.post('/api/budgets/batch_delete/', { ids })
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