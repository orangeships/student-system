<template>
  <div class="goals-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>财务目标管理</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增目标
          </el-button>
        </div>
      </template>

      <!-- 搜索表单 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="目标名称">
          <el-input v-model="searchForm.search" placeholder="请输入目标名称" clearable />
        </el-form-item>
        <el-form-item label="目标类型">
          <el-select v-model="searchForm.goal_type" placeholder="请选择类型" clearable>
            <el-option label="储蓄目标" value="savings" />
            <el-option label="支出限制" value="expense_limit" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="searchForm.is_active" placeholder="请选择状态" clearable>
            <el-option label="启用" :value="true" />
            <el-option label="禁用" :value="false" />
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

      <!-- 数据表格 -->
      <el-table
        :data="goals"
        v-loading="loading"
        stripe
        border
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="name" label="目标名称" min-width="120" />
        <el-table-column prop="goal_type" label="目标类型" width="100">
          <template #default="scope">
            <el-tag :type="scope.row.goal_type === 'savings' ? 'success' : 'warning'">
              {{ scope.row.goal_type === 'savings' ? '储蓄目标' : '支出限制' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="target_amount" label="目标金额" width="100">
          <template #default="scope">
            ¥{{ scope.row.target_amount.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="current_amount" label="当前金额" width="100">
          <template #default="scope">
            ¥{{ scope.row.current_amount.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column label="完成进度" width="150">
          <template #default="scope">
            <el-progress 
              :percentage="getProgressPercentage(scope.row)" 
              :status="getProgressStatus(scope.row)"
            />
          </template>
        </el-table-column>
        <el-table-column prop="deadline" label="截止日期" width="120">
          <template #default="scope">
            {{ scope.row.deadline ? formatDate(scope.row.deadline) : '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="is_active" label="状态" width="80">
          <template #default="scope">
            <el-tag :type="scope.row.is_active ? 'success' : 'info'">
              {{ scope.row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="160">
          <template #default="scope">
            {{ formatDateTime(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="scope">
            <el-button type="primary" link @click="handleEdit(scope.row)">
              编辑
            </el-button>
            <el-button type="danger" link @click="handleDelete(scope.row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="totalCount"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>

      <!-- 批量操作 -->
      <div class="batch-operation" v-if="selectedGoals.length > 0">
        <el-button type="danger" @click="handleBatchDelete">
          <el-icon><Delete /></el-icon>
          批量删除
        </el-button>
        <span class="selected-count">已选择 {{ selectedGoals.length }} 项</span>
      </div>
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="500px"
      @close="handleDialogClose"
    >
      <el-form
        ref="goalFormRef"
        :model="goalForm"
        :rules="formRules"
        label-width="100px"
      >
        <el-form-item label="目标名称" prop="name">
          <el-input v-model="goalForm.name" placeholder="请输入目标名称" />
        </el-form-item>
        <el-form-item label="目标类型" prop="goal_type">
          <el-select v-model="goalForm.goal_type" placeholder="请选择目标类型">
            <el-option label="储蓄目标" value="savings" />
            <el-option label="支出限制" value="expense_limit" />
          </el-select>
        </el-form-item>
        <el-form-item label="目标金额" prop="target_amount">
          <el-input-number
            v-model="goalForm.target_amount"
            :min="0"
            :precision="2"
            :step="100"
            controls-position="right"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="当前金额" prop="current_amount">
          <el-input-number
            v-model="goalForm.current_amount"
            :min="0"
            :precision="2"
            :step="100"
            controls-position="right"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="截止日期" prop="deadline">
          <el-date-picker
            v-model="goalForm.deadline"
            type="date"
            placeholder="选择日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="goalForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入描述"
          />
        </el-form-item>
        <el-form-item label="状态" prop="is_active">
          <el-switch v-model="goalForm.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="loading">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { useGoalStore } from '@/stores/goal'
import type { FinancialGoal, FinancialGoalForm } from '@/types/goal'
import { formatDate, formatDateTime } from '@/utils/format'

const goalStore = useGoalStore()

// 状态
const loading = computed(() => goalStore.loading)
const goals = computed(() => goalStore.goals)
const totalCount = computed(() => goalStore.totalCount)

// 搜索表单
const searchForm = reactive({
  search: '',
  goal_type: '',
  is_active: undefined as boolean | undefined
})

// 分页
const currentPage = ref(1)
const pageSize = ref(10)

// 选择
const selectedGoals = ref<FinancialGoal[]>([])

// 对话框
const dialogVisible = ref(false)
const dialogTitle = ref('')
const isEdit = ref(false)
const currentGoalId = ref<number | null>(null)

// 表单
const goalFormRef = ref<FormInstance>()
const goalForm = reactive<FinancialGoalForm>({
  name: '',
  goal_type: 'savings',
  target_amount: 0,
  current_amount: 0,
  deadline: '',
  description: '',
  is_active: true
})

// 表单规则
const formRules: FormRules = {
  name: [
    { required: true, message: '请输入目标名称', trigger: 'blur' },
    { min: 2, max: 100, message: '长度在 2 到 100 个字符', trigger: 'blur' }
  ],
  goal_type: [
    { required: true, message: '请选择目标类型', trigger: 'change' }
  ],
  target_amount: [
    { required: true, message: '请输入目标金额', trigger: 'blur' },
    { type: 'number', min: 0, message: '目标金额必须大于等于0', trigger: 'blur' }
  ],
  current_amount: [
    { type: 'number', min: 0, message: '当前金额必须大于等于0', trigger: 'blur' }
  ]
}

// 方法
const fetchData = async () => {
  const params = {
    page: currentPage.value,
    page_size: pageSize.value,
    ...searchForm
  }
  await goalStore.fetchGoals(params)
}

const handleSearch = () => {
  currentPage.value = 1
  fetchData()
}

const handleReset = () => {
  searchForm.search = ''
  searchForm.goal_type = ''
  searchForm.is_active = undefined
  handleSearch()
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  fetchData()
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
  fetchData()
}

const handleSelectionChange = (val: FinancialGoal[]) => {
  selectedGoals.value = val
}

const handleAdd = () => {
  dialogTitle.value = '新增财务目标'
  isEdit.value = false
  currentGoalId.value = null
  resetForm()
  dialogVisible.value = true
}

const handleEdit = (row: FinancialGoal) => {
  dialogTitle.value = '编辑财务目标'
  isEdit.value = true
  currentGoalId.value = row.id
  Object.assign(goalForm, {
    name: row.name,
    goal_type: row.goal_type,
    target_amount: row.target_amount,
    current_amount: row.current_amount,
    deadline: row.deadline,
    description: row.description,
    is_active: row.is_active
  })
  dialogVisible.value = true
}

const handleDelete = async (row: FinancialGoal) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除财务目标 "${row.name}" 吗？`,
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    await goalStore.deleteGoal(row.id)
    ElMessage.success('删除成功')
    fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleBatchDelete = async () => {
  if (selectedGoals.value.length === 0) {
    ElMessage.warning('请选择要删除的目标')
    return
  }
  
  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedGoals.value.length} 个财务目标吗？`,
      '批量删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )
    const ids = selectedGoals.value.map(item => item.id)
    await goalStore.batchDeleteGoals(ids)
    ElMessage.success('批量删除成功')
    selectedGoals.value = []
    fetchData()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('批量删除失败')
    }
  }
}

const handleSubmit = async () => {
  if (!goalFormRef.value) return
  
  try {
    await goalFormRef.value.validate()
    
    if (isEdit.value && currentGoalId.value) {
      await goalStore.updateGoal(currentGoalId.value, goalForm)
      ElMessage.success('更新成功')
    } else {
      await goalStore.createGoal(goalForm)
      ElMessage.success('创建成功')
    }
    
    dialogVisible.value = false
    fetchData()
  } catch (error) {
    ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
  }
}

const handleDialogClose = () => {
  goalFormRef.value?.resetFields()
  resetForm()
}

const resetForm = () => {
  Object.assign(goalForm, {
    name: '',
    goal_type: 'savings',
    target_amount: 0,
    current_amount: 0,
    deadline: '',
    description: '',
    is_active: true
  })
}

const getProgressPercentage = (goal: FinancialGoal) => {
  if (goal.target_amount === 0) return 0
  return Math.min(100, (goal.current_amount / goal.target_amount) * 100)
}

const getProgressStatus = (goal: FinancialGoal) => {
  const percentage = getProgressPercentage(goal)
  if (percentage >= 100) return 'success'
  if (percentage >= 80) return 'warning'
  return 'exception'
}

// 初始化
onMounted(() => {
  fetchData()
})
</script>

<style scoped>
.goals-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-form {
  margin-bottom: 20px;
}

.pagination-container {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

.batch-operation {
  margin-top: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.selected-count {
  color: #606266;
  font-size: 14px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>