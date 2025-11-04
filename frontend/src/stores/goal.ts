import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { 
  FinancialGoal, 
  FinancialGoalForm, 
  FinancialGoalSearchParams 
} from '@/types/goal'
import { api } from '@/utils/api'

export const useGoalStore = defineStore('goal', () => {
  const goals = ref<FinancialGoal[]>([])
  const loading = ref(false)
  const totalCount = ref(0)
  const currentGoal = ref<FinancialGoal | null>(null)

  // 获取财务目标列表
  const fetchGoals = async (params: FinancialGoalSearchParams = {}) => {
    loading.value = true
    try {
      const response = await api.get('/api/goals/', { params })
      goals.value = response.data.results || response.data
      totalCount.value = response.data.count || goals.value.length
    } catch (error) {
      console.error('获取财务目标失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 搜索财务目标
  const searchGoals = async (params: FinancialGoalSearchParams = {}) => {
    loading.value = true
    try {
      const response = await api.get('/api/goals/', { params })
      goals.value = response.data.results || response.data
      totalCount.value = response.data.count || goals.value.length
    } catch (error) {
      console.error('搜索财务目标失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 获取单个财务目标
  const fetchGoal = async (id: number) => {
    loading.value = true
    try {
      const response = await api.get(`/api/goals/${id}/`)
      currentGoal.value = response.data
      return response.data
    } catch (error) {
      console.error('获取财务目标失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 创建财务目标
  const createGoal = async (data: FinancialGoalForm) => {
    loading.value = true
    try {
      const response = await api.post('/api/goals/', data)
      await fetchGoals() // 重新获取列表
      return response.data
    } catch (error) {
      console.error('创建财务目标失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 更新财务目标
  const updateGoal = async (id: number, data: FinancialGoalForm) => {
    loading.value = true
    try {
      const response = await api.put(`/api/goals/${id}/`, data)
      await fetchGoals() // 重新获取列表
      return response.data
    } catch (error) {
      console.error('更新财务目标失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 删除财务目标
  const deleteGoal = async (id: number) => {
    loading.value = true
    try {
      await api.delete(`/api/goals/${id}/`)
      await fetchGoals() // 重新获取列表
    } catch (error) {
      console.error('删除财务目标失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 批量删除财务目标
  const batchDeleteGoals = async (ids: number[]) => {
    loading.value = true
    try {
      await api.post('/api/goals/batch_delete/', { ids })
      await fetchGoals() // 重新获取列表
    } catch (error) {
      console.error('批量删除财务目标失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  return {
    // 状态
    goals,
    loading,
    totalCount,
    currentGoal,
    
    // 方法
    fetchGoals,
    searchGoals,
    fetchGoal,
    createGoal,
    updateGoal,
    deleteGoal,
    batchDeleteGoals
  }
})