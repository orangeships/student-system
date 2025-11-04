import api from '@/api'
import type { PaginatedResponse } from '@/api/finance'

export interface Student {
  id?: number
  student_id: string
  name: string
  gender: 'M' | 'F'
  date_of_birth: string
  major: string
  grade: string
  class_name: string
  phone: string
  email: string
  address: string
  enrollment_date: string
  status: 'active' | 'inactive' | 'graduated'
  created_at?: string
  updated_at?: string
}

export interface StudentQuery {
  search?: string
  status?: string
  major?: string
  grade?: string
  ordering?: string
  page?: number
  page_size?: number
}

export interface StudentStatistics {
  total_students: number
  active_students: number
  inactive_students: number
  graduated_students: number
  by_major: Array<{ major: string; count: number }>
  by_grade: Array<{ grade: string; count: number }>
  by_gender?: Array<{ gender: 'M' | 'F'; count: number }>
}

export const studentApi = {
  // 获取学生列表
  getStudents(params?: StudentQuery): Promise<PaginatedResponse<Student>> {
    return api.get('/students/', { params })
  },

  // 获取学生详情
  getStudent(id: number) {
    return api.get(`/students/${id}/`)
  },

  // 创建学生
  createStudent(data: Student) {
    return api.post('/students/', data)
  },

  // 更新学生
  updateStudent(id: number, data: Student) {
    return api.put(`/students/${id}/`, data)
  },

  // 删除学生
  deleteStudent(id: number) {
    return api.delete(`/students/${id}/`)
  },

  // 获取学生统计
  getStatistics() {
    return api.get('/students/statistics/')
  },
}