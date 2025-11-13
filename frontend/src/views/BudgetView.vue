<template>
  <div class="budget-view">
    <el-card class="budget-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon style="color: #1890ff; margin-right: 8px;"><Wallet /></el-icon>
            <span class="card-title">预算管理</span>
            <el-tag type="info" size="small" style="margin-left: 12px;">
              共 {{ budgetStore.totalCount }} 个预算
            </el-tag>
          </div>
          <el-button type="primary" @click="showAddDialog = true" :icon="Plus">
            新增预算
          </el-button>
        </div>
      </template>

      <!-- 搜索 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="搜索">
          <el-input
            v-model="searchForm.search"
            placeholder="预算名称/分类"
            clearable
            @clear="handleSearch"
            @keyup.enter="handleSearch"
            @input="handleSearchInput"
            style="width: 200px"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
        </el-form-item>
        <el-form-item label="状态">
          <el-select 
            v-model="searchForm.status" 
            placeholder="全部" 
            clearable 
            @change="handleSearch"
            style="width: 120px"
          >
            <el-option label="进行中" value="active" />
            <el-option label="已结束" value="completed" />
            <el-option label="已暂停" value="paused" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch" :loading="budgetStore.loading">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="handleReset">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </el-form-item>
      </el-form>

      <!-- 预算列表 -->
      <div class="table-section">
        <div class="table-toolbar">
          <div class="toolbar-left">
            <el-tag type="info" size="small">
              已选择 {{ selectedBudgets.length }} 项
            </el-tag>
            <el-button 
              v-if="selectedBudgets.length > 0"
              type="danger" 
              size="small" 
              @click="handleBatchDelete"
              :icon="Delete"
            >
              批量删除
            </el-button>
          </div>
          <div class="toolbar-right">
            <el-button 
              size="small" 
              @click="handleRefresh"
              :loading="budgetStore.loading"
              :icon="Refresh"
            >
              刷新
            </el-button>
          </div>
        </div>
        <el-table
          v-loading="budgetStore.loading"
          :data="budgetStore.budgets"
          style="width: 100%"
          stripe
          :header-cell-style="{ background: '#fafafa', fontWeight: '600', color: '#262626' }"
          @selection-change="handleSelectionChange"
          :size="density === 'compact' ? 'small' : 'default'"
          row-key="id"
        >
          <el-table-column type="selection" width="55" fixed="left" />
          <el-table-column prop="id" label="ID" width="80" align="center" />
          <el-table-column prop="name" label="预算名称" min-width="150" sortable="custom">
            <template #default="{ row }">
              <div class="budget-info">
                <span class="budget-name">{{ row.name }}</span>
                <el-tag size="small" :type="getStatusType(row.status)">
                  {{ getStatusName(row.status) }}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="category_name" label="关联分类" width="120">
            <template #default="{ row }">
              <el-tag type="info" size="small" effect="plain">
                {{ row.category_name }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="amount" label="预算金额" width="120" align="right" sortable="custom">
            <template #default="{ row }">
              <span class="amount-text">{{ formatCurrency(row.amount) }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="spent_amount" label="已用金额" width="120" align="right" sortable="custom">
            <template #default="{ row }">
              <span class="spent-text">{{ formatCurrency(row.spent_amount) }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="remaining_amount" label="剩余金额" width="120" align="right" sortable="custom">
            <template #default="{ row }">
              <span :class="['remaining-text', row.remaining_amount < 0 ? 'over-budget' : '']">
                {{ formatCurrency(row.remaining_amount) }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="progress_percentage" label="使用进度" width="150" align="center">
            <template #default="{ row }">
              <div class="progress-container">
                <el-progress 
                  :percentage="row.progress_percentage" 
                  :status="getProgressStatus(row.progress_percentage)"
                  :stroke-width="8"
                />
                <span class="progress-text">{{ row.progress_percentage }}%</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="start_date" label="开始日期" width="120" sortable="custom">
            <template #default="{ row }">
              <span class="date-text">{{ formatDate(row.start_date) }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="end_date" label="结束日期" width="120" sortable="custom">
            <template #default="{ row }">
              <span class="date-text">{{ formatDate(row.end_date) }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="120" align="center" fixed="right">
            <template #default="{ row }">
              <el-button type="primary" link size="small" @click="handleEdit(row)">
                编辑
              </el-button>
              <el-button type="danger" link size="small" @click="handleDelete(row)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <el-pagination
          v-model:current-page="pagination.currentPage"
          v-model:page-size="pagination.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="budgetStore.totalCount"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          style="margin-top: 20px; text-align: right"
        />
      </div>
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog
      v-model="showAddDialog"
      :title="editingBudget ? '编辑预算' : '新增预算'"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form :model="budgetForm" :rules="rules" ref="budgetFormRef" label-width="100px">
        <el-form-item label="预算名称" prop="name">
          <el-input
            v-model="budgetForm.name"
            placeholder="请输入预算名称"
            maxlength="20"
            show-word-limit
          />
        </el-form-item>
        <el-form-item label="关联分类" prop="category">
          <el-select v-model="budgetForm.category" placeholder="选择分类" style="width: 100%">
            <el-option 
              v-for="category in expenseCategories" 
              :key="category.id" 
              :label="category.name" 
              :value="category.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="预算金额" prop="amount">
          <el-input-number
            v-model="budgetForm.amount"
            :min="0.01"
            :precision="2"
            :step="100"
            placeholder="请输入预算金额"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="日期范围" prop="dateRange">
          <el-date-picker
            v-model="budgetForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-radio-group v-model="budgetForm.status">
            <el-radio label="active">进行中</el-radio>
            <el-radio label="paused">已暂停</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="备注" prop="description">
          <el-input
            v-model="budgetForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入备注信息"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddDialog = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="submitting">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useBudgetStore } from '@/stores/budget'
import { useCategoryStore } from '@/stores/category'
import type { Budget, BudgetForm } from '@/types/budget'
import type { Category } from '@/types/category'
import {
  Wallet,
  Plus,
  Search,
  Refresh,
  Delete
} from '@element-plus/icons-vue'

const budgetStore = useBudgetStore()
const categoryStore = useCategoryStore()

const searchForm = reactive({
  search: '',
  status: ''
})

const pagination = reactive({
  currentPage: 1,
  pageSize: 20
})

const selectedBudgets = ref<Budget[]>([])
const showAddDialog = ref(false)
const editingBudget = ref<Budget | null>(null)
const submitting = ref(false)
const density = ref<'default' | 'compact'>('default')

const budgetFormRef = ref()

interface ExtendedBudgetForm extends BudgetForm {
  name: string
  status: 'active' | 'completed' | 'paused'
  description: string
  dateRange: string[]
}

const budgetForm = reactive<ExtendedBudgetForm>({
  name: '',
  category: 0,
  amount: 0,
  dateRange: [],
  status: 'active' as 'active' | 'completed' | 'paused',
  description: '',
  period: 'monthly' as 'monthly' | 'yearly',
  start_date: '',
  end_date: ''
})

const rules = {
  name: [{ required: true, message: '请输入预算名称', trigger: 'blur' }],
  category: [{ required: true, message: '请选择关联分类', trigger: 'change' }],
  amount: [{ required: true, message: '请输入预算金额', trigger: 'blur' }],
  dateRange: [{ required: true, message: '请选择日期范围', trigger: 'change' }],
  status: [{ required: true, message: '请选择状态', trigger: 'change' }]
}

// 只显示支出分类
const expenseCategories = computed(() => 
  categoryStore.categories.filter((category: Category) => category.category_type === 'expense')
)

onMounted(async () => {
  await Promise.all([
    budgetStore.fetchBudgets(),
    categoryStore.fetchCategories()
  ])
})

const handleSearch = () => {
  budgetStore.searchBudgets({
    ...searchForm,
    page: pagination.currentPage,
    page_size: pagination.pageSize
  })
}

const handleReset = () => {
  searchForm.search = ''
  searchForm.status = ''
  handleSearch()
}

const handleSearchInput = () => {
  // 防抖搜索
  clearTimeout((window as any).searchTimeout)
  ;(window as any).searchTimeout = setTimeout(handleSearch, 500)
}

const handleSelectionChange = (selection: Budget[]) => {
  selectedBudgets.value = selection
}

const handleSizeChange = (size: number) => {
  pagination.pageSize = size
  handleSearch()
}

const handleCurrentChange = (page: number) => {
  pagination.currentPage = page
  handleSearch()
}

const handleRefresh = () => {
  budgetStore.fetchBudgets()
  showSuccess('数据已刷新')
}

const handleBatchDelete = async () => {
  if (selectedBudgets.value.length === 0) return
  
  await ElMessageBox.confirm(
    `确定要删除选中的 ${selectedBudgets.value.length} 个预算吗？`,
    '批量删除确认',
    { type: 'warning' }
  )
  
  try {
    const ids = selectedBudgets.value.map(b => b.id)
    await budgetStore.batchDeleteBudgets(ids)
    showSuccess('批量删除成功')
    selectedBudgets.value = []
  } catch (error) {
    showError('批量删除失败')
  }
}

const handleEdit = (budget: Budget) => {
  editingBudget.value = budget
  Object.assign(budgetForm, {
    name: (budget as any).name,
    category: budget.category,
    amount: budget.amount,
    dateRange: [budget.start_date, budget.end_date],
    status: (budget as any).status,
    description: (budget as any).description || '',
    period: (budget as any).period || 'monthly'
  } as any)
  showAddDialog.value = true
}

const handleDelete = async (budget: Budget) => {
  await ElMessageBox.confirm(
    `确定要删除预算 "${(budget as any).name}" 吗？`,
    '删除确认',
    { type: 'warning' }
  )
  
  try {
    await budgetStore.deleteBudget(budget.id)
    showSuccess('删除成功')
  } catch (error) {
    showError('删除失败')
  }
}

const handleSubmit = async () => {
  await budgetFormRef.value.validate()
  
  submitting.value = true
  try {
    const formData = {
      category: budgetForm.category,
      amount: budgetForm.amount,
      period: budgetForm.period,
      start_date: budgetForm.dateRange[0],
      end_date: budgetForm.dateRange[1],
      is_active: budgetForm.status === 'active'
    } as BudgetForm
    
    if (editingBudget.value) {
      await budgetStore.updateBudget(editingBudget.value.id, formData)
      showSuccess('更新成功')
    } else {
      await budgetStore.createBudget(formData)
      showSuccess('新增成功')
    }
    
    showAddDialog.value = false
    resetForm()
  } catch (error) {
    showError('操作失败')
  } finally {
    submitting.value = false
  }
}

const resetForm = () => {
  editingBudget.value = null
  Object.assign(budgetForm, {
    name: '',
    category: 0,
    amount: 0,
    dateRange: [],
    status: 'active',
    description: '',
    period: 'monthly' as 'monthly' | 'yearly',
    start_date: '',
    end_date: ''
  })
}

const formatCurrency = (amount: number | string) => {
  const numAmount = typeof amount === 'string' ? parseFloat(amount) : amount
  if (isNaN(numAmount)) {
    return '¥0.00'
  }
  return `¥${numAmount.toFixed(2)}`
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('zh-CN')
}

const getStatusType = (status: string) => {
  const types: Record<string, string> = {
    active: 'success',
    completed: 'info',
    paused: 'warning'
  }
  return types[status] || 'info'
}

const getStatusName = (status: string) => {
  const names: Record<string, string> = {
    active: '进行中',
    completed: '已结束',
    paused: '已暂停'
  }
  return names[status] || status
}

const getProgressStatus = (percentage: number) => {
  if (percentage >= 90) return 'exception'
  if (percentage >= 70) return 'warning'
  return 'success'
}

const showSuccess = (message: string) => {
  ElMessage.success(message)
}

const showError = (message: string) => {
  ElMessage.error(message)
}

// 监听数据刷新事件
window.addEventListener('refresh-data', handleRefresh)

// 组件卸载时移除事件监听器
onUnmounted(() => {
  window.removeEventListener('refresh-data', handleRefresh)
})
</script>

<style scoped>
.budget-view {
  padding: 0;
}

.budget-card {
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
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

.search-form {
  margin-bottom: 20px;
  padding: 16px;
  background-color: #fafafa;
  border-radius: 4px;
}

.table-section {
  padding: 0 16px;
}

.table-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.toolbar-left, .toolbar-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.budget-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.budget-name {
  font-weight: 500;
  color: #262626;
}

.amount-text {
  font-weight: 600;
  color: #262626;
}

.spent-text {
  font-weight: 600;
  color: #1890ff;
}

.remaining-text {
  font-weight: 600;
  color: #52c41a;
}

.remaining-text.over-budget {
  color: #ff4d4f;
}

.progress-container {
  display: flex;
  align-items: center;
  gap: 8px;
}

.progress-text {
  font-size: 12px;
  color: #595959;
  min-width: 35px;
}

.date-text {
  color: #595959;
  font-size: 14px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>