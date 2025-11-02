import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Student, StudentStatistics } from '@/api/student'
import { studentApi } from '@/api/student'

export const useStudentStore = defineStore('student', () => {
  const students = ref<Student[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  const statistics = ref<StudentStatistics | null>(null)

  const totalCount = ref(0)
  const currentPage = ref(1)
  const pageSize = ref(10)

  // 获取学生列表
  const fetchStudents = async (params?: any) => {
    loading.value = true
    error.value = null
    try {
      const response = await studentApi.getStudents({
        page: currentPage.value,
        page_size: pageSize.value,
        ...params
      })
      students.value = response.results
      totalCount.value = response.count
    } catch (err: any) {
      error.value = err.message || '获取学生列表失败'
      console.error('获取学生列表失败:', err)
    } finally {
      loading.value = false
    }
  }

  // 获取学生详情
  const fetchStudent = async (id: number) => {
    loading.value = true
    error.value = null
    try {
      const student = await studentApi.getStudent(id)
      return student
    } catch (err: any) {
      error.value = err.message || '获取学生详情失败'
      console.error('获取学生详情失败:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // 创建学生
  const createStudent = async (data: Student) => {
    loading.value = true
    error.value = null
    try {
      const student = await studentApi.createStudent(data)
      await fetchStudents()
      return student
    } catch (err: any) {
      error.value = err.message || '创建学生失败'
      console.error('创建学生失败:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // 更新学生
  const updateStudent = async (id: number, data: Student) => {
    loading.value = true
    error.value = null
    try {
      const student = await studentApi.updateStudent(id, data)
      await fetchStudents()
      return student
    } catch (err: any) {
      error.value = err.message || '更新学生失败'
      console.error('更新学生失败:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // 删除学生
  const deleteStudent = async (id: number) => {
    loading.value = true
    error.value = null
    try {
      await studentApi.deleteStudent(id)
      await fetchStudents()
    } catch (err: any) {
      error.value = err.message || '删除学生失败'
      console.error('删除学生失败:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // 获取统计信息
  const fetchStatistics = async () => {
    loading.value = true
    error.value = null
    try {
      const stats = await studentApi.getStatistics() as unknown as StudentStatistics
      statistics.value = stats
      return stats
    } catch (err: any) {
      error.value = err.message || '获取统计信息失败'
      console.error('获取统计信息失败:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // 分页相关
  const setPage = (page: number) => {
    currentPage.value = page
    fetchStudents()
  }

  const setPageSize = (size: number) => {
    pageSize.value = size
    currentPage.value = 1
    fetchStudents()
  }

  return {
    students,
    loading,
    error,
    statistics,
    totalCount,
    currentPage,
    pageSize,
    fetchStudents,
    fetchStudent,
    createStudent,
    updateStudent,
    deleteStudent,
    fetchStatistics,
    setPage,
    setPageSize,
  }
})