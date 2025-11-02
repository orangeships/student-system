<template>
  <div class="students-view">
    <el-card class="students-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon style="color: #1890ff; margin-right: 8px;"><User /></el-icon>
            <span class="card-title">学生管理</span>
            <el-tag type="info" size="small" style="margin-left: 12px;">
              共 {{ studentStore.totalCount }} 名学生
            </el-tag>
          </div>
          <el-button type="primary" @click="showAddDialog = true" :icon="Plus">
            新增学生
          </el-button>
        </div>
      </template>

      <!-- 搜索和筛选 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="搜索">
          <el-input
            v-model="searchForm.search"
            placeholder="姓名/学号/手机号"
            clearable
            @clear="handleSearch"
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.status" placeholder="全部" clearable @change="handleSearch">
            <el-option label="在读" value="active" />
            <el-option label="休学" value="inactive" />
            <el-option label="毕业" value="graduated" />
          </el-select>
        </el-form-item>
        <el-form-item label="专业">
          <el-select v-model="searchForm.major" placeholder="全部" clearable @change="handleSearch">
            <el-option label="计算机科学" value="计算机科学" />
            <el-option label="软件工程" value="软件工程" />
            <el-option label="信息管理" value="信息管理" />
            <el-option label="电子商务" value="电子商务" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="handleReset">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </el-form-item>
      </el-form>

      <!-- 学生列表 -->
      <div class="table-section">
        <el-table
          v-loading="studentStore.loading"
          :data="studentStore.students"
          style="width: 100%"
          stripe
          :header-cell-style="{ background: '#fafafa', fontWeight: '600', color: '#262626' }"
        >
          <el-table-column prop="student_id" label="学号" width="120" fixed="left">
            <template #default="{ row }">
              <span class="student-id">{{ row.student_id }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="name" label="姓名" width="100" fixed="left">
            <template #default="{ row }">
              <div class="student-name">
                <el-avatar :size="24" :style="{ backgroundColor: getAvatarColor(row.name) }">
                  {{ row.name.charAt(0) }}
                </el-avatar>
                <span class="name-text">{{ row.name }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="gender" label="性别" width="60" align="center">
            <template #default="{ row }">
              <el-tag :type="row.gender === 'M' ? 'primary' : 'danger'" size="small">
                {{ row.gender === 'M' ? '男' : '女' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="major" label="专业" width="120" show-overflow-tooltip>
            <template #default="{ row }">
              <el-tag type="info" size="small" effect="plain">{{ row.major }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="grade" label="年级" width="80" align="center">
            <template #default="{ row }">
              <span class="grade-text">{{ row.grade }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="class_name" label="班级" width="100" align="center">
            <template #default="{ row }">
              <span class="class-text">{{ row.class_name }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="phone" label="手机号" width="120">
            <template #default="{ row }">
              <span class="phone-text">{{ row.phone }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="email" label="邮箱" width="180" show-overflow-tooltip>
            <template #default="{ row }">
              <span class="email-text">{{ row.email }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="状态" width="80" align="center" fixed="right">
            <template #default="{ row }">
              <el-tag 
                :type="getStatusType(row.status)"
                size="small"
                effect="dark"
              >
                <el-icon style="margin-right: 2px;">
                  <CircleCheck v-if="row.status === 'active'" />
                  <CircleClose v-else />
                </el-icon>
                {{ getStatusLabel(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="enrollment_date" label="入学日期" width="120">
            <template #default="{ row }">
              <span class="enrollment-date">{{ row.enrollment_date }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="180" fixed="right" align="center">
            <template #default="{ row }">
              <div class="action-buttons">
                <el-button 
                  type="primary" 
                  link 
                  @click="handleEdit(row)"
                  :icon="Edit"
                  size="small"
                >
                  编辑
                </el-button>
                <el-button 
                  type="danger" 
                  link 
                  @click="handleDelete(row)"
                  :icon="Delete"
                  size="small"
                >
                  删除
                </el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="studentStore.currentPage"
          v-model:page-size="studentStore.pageSize"
          :total="studentStore.totalCount"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          background
          :hide-on-single-page="false"
        />
      </div>
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="showAddDialog"
      :title="editingStudent ? '编辑学生' : '新增学生'"
      width="600px"
    >
      <el-form
        ref="studentFormRef"
        :model="studentForm"
        :rules="studentRules"
        label-width="100px"
      >
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="学号" prop="student_id">
              <el-input v-model="studentForm.student_id" placeholder="请输入学号" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="姓名" prop="name">
              <el-input v-model="studentForm.name" placeholder="请输入姓名" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="性别" prop="gender">
              <el-radio-group v-model="studentForm.gender">
                <el-radio label="M">男</el-radio>
                <el-radio label="F">女</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="出生日期" prop="date_of_birth">
              <el-date-picker
                v-model="studentForm.date_of_birth"
                type="date"
                placeholder="选择日期"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="专业" prop="major">
              <el-select v-model="studentForm.major" placeholder="请选择专业" style="width: 100%">
                <el-option label="计算机科学" value="计算机科学" />
                <el-option label="软件工程" value="软件工程" />
                <el-option label="信息管理" value="信息管理" />
                <el-option label="电子商务" value="电子商务" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="年级" prop="grade">
              <el-select v-model="studentForm.grade" placeholder="请选择年级" style="width: 100%">
                <el-option label="大一" value="大一" />
                <el-option label="大二" value="大二" />
                <el-option label="大三" value="大三" />
                <el-option label="大四" value="大四" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="班级" prop="class_name">
              <el-input v-model="studentForm.class_name" placeholder="请输入班级" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态" prop="status">
              <el-select v-model="studentForm.status" placeholder="请选择状态" style="width: 100%">
                <el-option label="在读" value="active" />
                <el-option label="休学" value="inactive" />
                <el-option label="毕业" value="graduated" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="手机号" prop="phone">
              <el-input v-model="studentForm.phone" placeholder="请输入手机号" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="邮箱" prop="email">
              <el-input v-model="studentForm.email" placeholder="请输入邮箱" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="地址" prop="address">
          <el-input
            v-model="studentForm.address"
            type="textarea"
            :rows="2"
            placeholder="请输入地址"
          />
        </el-form-item>
        
        <el-form-item label="入学日期" prop="enrollment_date">
          <el-date-picker
            v-model="studentForm.enrollment_date"
            type="date"
            placeholder="选择日期"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddDialog = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="studentStore.loading">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { useStudentStore } from '@/stores/student'
import type { Student } from '@/api/student'
import { Plus, Edit, Delete, Search, Refresh, CircleCheck, CircleClose, User } from '@element-plus/icons-vue'

const studentStore = useStudentStore()

const showAddDialog = ref(false)
const studentFormRef = ref<FormInstance>()
const editingStudent = ref<Student | null>(null)

const searchForm = reactive({
  search: '',
  status: '',
  major: '',
})

const studentForm = reactive<Student>({
  student_id: '',
  name: '',
  gender: 'M',
  date_of_birth: '',
  major: '',
  grade: '',
  class_name: '',
  phone: '',
  email: '',
  address: '',
  enrollment_date: '',
  status: 'active',
})

const studentRules: FormRules = {
  student_id: [{ required: true, message: '请输入学号', trigger: 'blur' }],
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
  date_of_birth: [{ required: true, message: '请选择出生日期', trigger: 'change' }],
  major: [{ required: true, message: '请选择专业', trigger: 'change' }],
  grade: [{ required: true, message: '请选择年级', trigger: 'change' }],
  class_name: [{ required: true, message: '请输入班级', trigger: 'blur' }],
  phone: [
    { required: true, message: '请输入手机号', trigger: 'blur' },
    { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' },
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '邮箱格式不正确', trigger: 'blur' },
  ],
  address: [{ required: true, message: '请输入地址', trigger: 'blur' }],
  enrollment_date: [{ required: true, message: '请选择入学日期', trigger: 'change' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }],
}

const getStatusType = (status: string) => {
  const types: Record<string, string> = {
    active: 'success',
    inactive: 'warning',
    graduated: 'info',
  }
  return types[status] || 'info'
}

const getStatusLabel = (status: string) => {
  const labels: Record<string, string> = {
    active: '在读',
    inactive: '休学',
    graduated: '毕业',
  }
  return labels[status] || status
}

const handleSearch = () => {
  studentStore.fetchStudents(searchForm)
}

const handleReset = () => {
  searchForm.search = ''
  searchForm.status = ''
  searchForm.major = ''
  studentStore.fetchStudents()
}

const handleSizeChange = (size: number) => {
  studentStore.setPageSize(size)
}

const handleCurrentChange = (page: number) => {
  studentStore.setPage(page)
}

const handleEdit = (row: Student) => {
  editingStudent.value = row
  Object.assign(studentForm, row)
  showAddDialog.value = true
}

const handleDelete = async (row: Student) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除学生 "${row.name}" 吗？`,
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await studentStore.deleteStudent(row.id!)
    ElMessage.success('删除成功')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleSubmit = async () => {
  if (!studentFormRef.value) return
  
  try {
    await studentFormRef.value.validate()
    
    if (editingStudent.value) {
      await studentStore.updateStudent(editingStudent.value.id!, studentForm)
      ElMessage.success('更新成功')
    } else {
      await studentStore.createStudent(studentForm)
      ElMessage.success('创建成功')
    }
    
    showAddDialog.value = false
    resetForm()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const resetForm = () => {
  editingStudent.value = null
  Object.assign(studentForm, {
    student_id: '',
    name: '',
    gender: 'M',
    date_of_birth: '',
    major: '',
    grade: '',
    class_name: '',
    phone: '',
    email: '',
    address: '',
    enrollment_date: '',
    status: 'active',
  })
  studentFormRef.value?.clearValidate()
}

const getAvatarColor = (name: string) => {
  const colors = ['#1890ff', '#52c41a', '#faad14', '#f5222d', '#722ed1', '#13c2c2']
  const index = name.charCodeAt(0) % colors.length
  return colors[index]
}

onMounted(() => {
  studentStore.fetchStudents()
})
</script>

<style scoped>
.students-view {
  padding: 24px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 120px);
}

.students-card {
  border: none;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.students-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1) !important;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
}

.card-title {
  font-size: 18px;
  font-weight: 600;
  color: #262626;
}

.search-section {
  background-color: #fafafa;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 24px;
}

.search-form {
  margin-bottom: 0;
}

.search-buttons {
  display: flex;
  gap: 8px;
}

.table-section {
  background-color: #fff;
  border-radius: 8px;
  overflow: hidden;
}

.students-table {
  border-radius: 8px;
}

.student-id {
  font-weight: 500;
  color: #1890ff;
}

.student-name {
  display: flex;
  align-items: center;
  gap: 8px;
}

.name-text {
  font-weight: 500;
  color: #262626;
}

.birth-date {
  color: #595959;
  font-size: 13px;
}

.grade-text {
  color: #262626;
  font-weight: 500;
}

.class-text {
  color: #595959;
  font-size: 13px;
}

.phone-text {
  color: #1890ff;
  font-size: 13px;
}

.email-text {
  color: #595959;
  font-size: 13px;
}

.enrollment-date {
  color: #8c8c8c;
  font-size: 12px;
}

.action-buttons {
  display: flex;
  gap: 8px;
  justify-content: center;
}

.pagination-container {
  margin-top: 24px;
  text-align: center;
  padding: 16px 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .students-view {
    padding: 16px;
  }
  
  .search-section {
    padding: 16px;
  }
  
  .search-buttons {
    justify-content: flex-end;
  }
  
  .card-header {
    flex-direction: column;
    gap: 12px;
    align-items: flex-start;
  }
  
  .header-left {
    width: 100%;
  }
}

@media (max-width: 480px) {
  .students-view {
    padding: 12px;
  }
  
  .search-section {
    padding: 12px;
  }
  
  .search-buttons {
    flex-direction: column;
  }
  
  .action-buttons {
    flex-direction: column;
    gap: 4px;
  }
}
</style>