import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Student, StudentStatistics } from '@/api/student'
import { studentApi } from '@/api/student'
import { handleRequest } from '@/utils/message'

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
      throw err
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
  const createStudent = async (studentData: Omit<Student, 'id'>) => {
    return handleRequest(
      async () => {
        loading.value = true
        error.value = null
        const newStudent = await studentApi.createStudent(studentData)
        await fetchStudents()
        return newStudent
      },
      {
        success: '学生创建成功',
        error: '创建学生失败',
        finally: () => {
          loading.value = false
        }
      }
    )
  }

  // 更新学生
  const updateStudent = async (id: number, studentData: Partial<Student>) => {
    return handleRequest(
      async () => {
        loading.value = true
        error.value = null
        const response = await studentApi.updateStudent(id, studentData)
        const updatedStudent = response
        const index = students.value.findIndex(s => s.id === id)
        if (index !== -1) {
          students.value[index] = updatedStudent
        }
        return updatedStudent
      },
      {
        success: '学生更新成功',
        error: '更新学生失败',
        finally: () => {
          loading.value = false
        }
      }
    )
  }

  // 删除学生
  const deleteStudent = async (id: number) => {
    return handleRequest(
      async () => {
        loading.value = true
        error.value = null
        await studentApi.deleteStudent(id)
        await fetchStudents()
      },
      {
        success: '学生删除成功',
        error: '删除学生失败',
        finally: () => {
          loading.value = false
        }
      }
    )
  }

  // 批量删除学生
  const batchDeleteStudents = async (ids: number[]) => {
    return handleRequest(
      async () => {
        loading.value = true
        error.value = null
        await Promise.all(ids.map(id => studentApi.deleteStudent(id)))
        await fetchStudents()
      },
      {
        success: '批量删除学生成功',
        error: '批量删除学生失败',
        finally: () => {
          loading.value = false
        }
      }
    )
  }

  // 获取统计信息
  const fetchStatistics = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await studentApi.getStatistics()
      statistics.value = response
      return response
    } catch (err: any) {
      error.value = err.message || '获取统计信息失败'
      console.error('获取统计信息失败:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // 更新学生状态
  const updateStudentStatus = async (id: number, status: 'active' | 'inactive' | 'graduated') => {
    return handleRequest(
      async () => {
        loading.value = true
        error.value = null
        const response = await studentApi.updateStudent(id, { status })
        const updatedStudent = response
        const index = students.value.findIndex(s => s.id === id)
        if (index !== -1) {
          students.value[index] = updatedStudent
        }
        return updatedStudent
      },
      {
        success: '学生状态更新成功',
        error: '更新学生状态失败',
        finally: () => {
          loading.value = false
        }
      }
    )
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
    batchDeleteStudents,
    fetchStatistics,
    updateStudentStatus,
    setPage,
    setPageSize,
  }
})