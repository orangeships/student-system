import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Category, CategoryForm, CategorySearchParams } from '@/types/category'
import { api } from '@/utils/api'

export const useCategoryStore = defineStore('category', () => {
  const categories = ref<Category[]>([])
  const loading = ref(false)
  const totalCount = ref(0)
  const currentCategory = ref<Category | null>(null)

  // 获取分类列表
  const fetchCategories = async (params: CategorySearchParams = {}) => {
    loading.value = true
    try {
      const response = await api.get('/api/transactions/categories/', { params })
      // 确保返回的是数组
      const data = response.data.results || response.data
      if (Array.isArray(data)) {
        categories.value = data
        totalCount.value = response.data.count || data.length
      } else {
        console.warn('分类数据格式错误，期望数组但收到:', data)
        categories.value = []
        totalCount.value = 0
      }
    } catch (error) {
      console.error('获取分类列表失败:', error)
      categories.value = []
      totalCount.value = 0
      throw error
    } finally {
      loading.value = false
    }
  }

  // 搜索分类
  const searchCategories = async (params: CategorySearchParams = {}) => {
    loading.value = true
    try {
      const response = await api.get('/api/transactions/categories/', { params })
      // 确保返回的是数组
      const data = response.data.results || response.data
      if (Array.isArray(data)) {
        categories.value = data
        totalCount.value = response.data.count || data.length
      } else {
        console.warn('搜索分类数据格式错误，期望数组但收到:', data)
        categories.value = []
        totalCount.value = 0
      }
    } catch (error) {
      console.error('搜索分类失败:', error)
      categories.value = []
      totalCount.value = 0
      throw error
    } finally {
      loading.value = false
    }
  }

  // 获取单个分类
  const fetchCategory = async (id: number) => {
    loading.value = true
    try {
      const response = await api.get(`/api/transactions/categories/${id}/`)
      currentCategory.value = response.data
      return response.data
    } catch (error) {
      console.error('获取分类失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 创建分类
  const createCategory = async (data: CategoryForm) => {
    loading.value = true
    try {
      const response = await api.post('/api/transactions/categories/', data)
      await fetchCategories() // 重新获取列表
      return response.data
    } catch (error) {
      console.error('创建分类失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 更新分类
  const updateCategory = async (id: number, data: CategoryForm) => {
    loading.value = true
    try {
      const response = await api.put(`/api/transactions/categories/${id}/`, data)
      await fetchCategories() // 重新获取列表
      return response.data
    } catch (error) {
      console.error('更新分类失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 删除分类
  const deleteCategory = async (id: number) => {
    loading.value = true
    try {
      await api.delete(`/api/transactions/categories/${id}/`)
      await fetchCategories() // 重新获取列表
    } catch (error) {
      console.error('删除分类失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 批量删除分类
  const batchDeleteCategories = async (ids: number[]) => {
    loading.value = true
    try {
      await api.post('/api/transactions/categories/batch_delete/', { ids })
      await fetchCategories() // 重新获取列表
    } catch (error) {
      console.error('批量删除分类失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  return {
    // 状态
    categories,
    loading,
    totalCount,
    currentCategory,
    
    // 方法
    fetchCategories,
    searchCategories,
    fetchCategory,
    createCategory,
    updateCategory,
    deleteCategory,
    batchDeleteCategories
  }
})