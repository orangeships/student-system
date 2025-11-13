<template>
  <div class="transactions-view">
    <el-card class="transactions-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon style="color: #1890ff; margin-right: 8px;"><Money /></el-icon>
            <span class="card-title">记账管理</span>
            <el-tag type="info" size="small" style="margin-left: 12px;">
              共 {{ transactionStore.totalCount }} 笔交易
            </el-tag>
          </div>
          <el-button type="primary" @click="handleAddNew" :icon="Plus">
          新增记账
        </el-button>
        </div>
      </template>

      <!-- 搜索和筛选 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="搜索">
          <el-input
            v-model="searchForm.search"
            placeholder="交易描述/备注"
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
        <el-form-item label="类型">
          <el-select 
            v-model="searchForm.transaction_type" 
            placeholder="全部" 
            clearable 
            @change="handleSearch"
            style="width: 120px"
          >
            <el-option label="收入" value="income" />
            <el-option label="支出" value="expense" />
          </el-select>
        </el-form-item>
        <el-form-item label="分类">
          <el-select 
            v-model="searchForm.category" 
            placeholder="全部" 
            clearable 
            @change="handleSearch"
            style="width: 140px"
          >
            <el-option 
              v-for="category in categories" 
              :key="category.id" 
              :label="category.name" 
              :value="category.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="日期范围">
          <el-date-picker
            v-model="searchForm.dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            @change="handleSearch"
            style="width: 240px"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch" :loading="transactionStore.loading">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="handleReset">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
          <el-button @click="handleExport" :icon="Download">
            导出
          </el-button>
        </el-form-item>
      </el-form>

      <!-- 交易列表 -->
      <div class="table-section">
        <div class="table-toolbar">
          <div class="toolbar-left">
            <el-tag type="info" size="small">
              已选择 {{ selectedTransactions.length }} 项
            </el-tag>
            <el-button 
              v-if="selectedTransactions.length > 0"
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
              :loading="transactionStore.loading"
              :icon="Refresh"
            >
              刷新
            </el-button>
            <el-button 
                size="small" 
                @click="toggleDensity"
                :icon="density === 'default' ? Expand : Remove"
              >
                {{ density === 'default' ? '紧凑' : '默认' }}
              </el-button>
          </div>
        </div>
        <el-table
          v-loading="transactionStore.loading"
          :data="transactionStore.transactions || []"
          style="width: 100%"
          stripe
          :header-cell-style="{ background: '#fafafa', fontWeight: '600', color: '#262626' }"
          @selection-change="handleSelectionChange"
          :size="density === 'compact' ? 'small' : 'default'"
          row-key="id"
          v-if="transactionStore.transactions"
        >
          <el-table-column type="selection" width="55" fixed="left" />
          <el-table-column prop="id" label="ID" width="80" align="center" />
          <el-table-column prop="transaction_date" label="交易日期" width="120" sortable="custom">
            <template #default="{ row }">
              <span class="date-text">{{ formatDate(row.transaction_date) }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="transaction_type" label="类型" width="80" align="center" sortable="custom">
            <template #default="{ row }">
              <el-tag :type="row.transaction_type === 'income' ? 'success' : 'danger'" size="small">
                {{ row.transaction_type === 'income' ? '收入' : '支出' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="category_name" label="分类" width="120" show-overflow-tooltip>
            <template #default="{ row }">
              <el-tag type="info" size="small" effect="plain">
                {{ row.category_name }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="amount" label="金额" width="120" align="right" sortable="custom">
            <template #default="{ row }">
              <span :class="['amount-text', row.transaction_type === 'income' ? 'income' : 'expense']">
                {{ formatCurrency(row.amount) }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip>
            <template #default="{ row }">
              <span class="description-text">{{ row.description || '-' }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="payment_method" label="支付方式" width="100" align="center">
            <template #default="{ row }">
              <el-tag size="small" :type="getPaymentMethodType(row.payment_method)">
                {{ getPaymentMethodName(row.payment_method) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" width="160" sortable="custom">
            <template #default="{ row }">
              <span class="created-text">{{ formatDateTime(row.created_at) }}</span>
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
          :total="transactionStore.totalCount"
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
      :title="editingTransaction ? '编辑记账' : '新增记账'"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form :model="transactionForm" :rules="rules" ref="transactionFormRef" label-width="80px">
        <el-form-item label="交易日期" prop="transaction_date">
          <el-date-picker
            v-model="transactionForm.transaction_date"
            type="date"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            placeholder="选择日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="交易类型" prop="transaction_type">
          <el-radio-group v-model="transactionForm.transaction_type">
            <el-radio label="income">收入</el-radio>
            <el-radio label="expense">支出</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-select 
            v-model="transactionForm.category" 
            placeholder="选择分类" 
            style="width: 100%"
            clearable
            filterable
            :disabled="categories.length === 0"
          >
            <el-option 
              v-for="category in categories || []" 
              :key="category.id" 
              :label="category.name" 
              :value="category.id"
            />
          </el-select>
          <div v-if="categories.length === 0" style="color: #909399; font-size: 12px; margin-top: 5px;">
            暂无分类，请先前往分类管理页面添加分类
          </div>
        </el-form-item>
        <el-form-item label="金额" prop="amount">
          <el-input-number
            v-model="transactionForm.amount"
            :min="0.01"
            :precision="2"
            :step="0.1"
            placeholder="请输入金额"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="支付方式" prop="payment_method">
          <el-select v-model="transactionForm.payment_method" placeholder="选择支付方式" style="width: 100%">
            <el-option label="现金" value="cash" />
            <el-option label="银行卡" value="card" />
            <el-option label="支付宝" value="alipay" />
            <el-option label="微信" value="wechat" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="transactionForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入交易描述"
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
import { ref, reactive, onMounted, onUnmounted, computed, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useTransactionStore } from '@/stores/transaction'
import { useCategoryStore } from '@/stores/category'
import type { Transaction, TransactionForm } from '@/types/transaction'
import {
  Plus,
  Search,
  Refresh,
  Download,
  Delete,
  Expand,
  Remove
} from '@element-plus/icons-vue'

const transactionStore = useTransactionStore()
const categoryStore = useCategoryStore()

const searchForm = reactive({
  search: '',
  transaction_type: '',
  category: '',
  dateRange: []
})

const pagination = reactive({
  currentPage: 1,
  pageSize: 20
})

const selectedTransactions = ref<Transaction[]>([])
const showAddDialog = ref(false)
const editingTransaction = ref<Transaction | null>(null)
const submitting = ref(false)
const density = ref<'default' | 'compact'>('default')

const transactionFormRef = ref()

const transactionForm = reactive<TransactionForm>({
  transaction_date: new Date().toISOString().split('T')[0] || '',
  transaction_type: 'expense',
  category: '',
  amount: 0,
  payment_method: 'cash',
  description: ''
})

const rules = {
  transaction_date: [{ required: true, message: '请选择交易日期', trigger: 'change' }],
  transaction_type: [{ required: true, message: '请选择交易类型', trigger: 'change' }],
  category: [{ required: true, message: '请选择分类', trigger: 'change' }],
  amount: [{ required: true, message: '请输入金额', trigger: 'blur' }],
  payment_method: [{ required: true, message: '请选择支付方式', trigger: 'change' }]
}

const categories = computed(() => {
  const allCategories = categoryStore.categories || []
  if (!transactionForm.transaction_type) {
    return allCategories
  }
  return allCategories.filter(category => 
    category.category_type === transactionForm.transaction_type
  )
})

onMounted(async () => {
  try {
    await Promise.all([
      transactionStore.fetchTransactions(),
      categoryStore.fetchCategories()
    ])
    console.log('分类数据加载完成:', categories.value)
    if (categories.value.length === 0) {
      console.warn('分类数据为空，请确保已添加分类')
    }
  } catch (error) {
    console.error('数据加载失败:', error)
  }
})

// 监听交易类型变化，清空不匹配的已选择分类
watch(() => transactionForm.transaction_type, (newType) => {
  if (newType && transactionForm.category) {
    const selectedCategory = categories.value.find(cat => cat.id === transactionForm.category)
    if (selectedCategory && selectedCategory.category_type !== newType) {
      transactionForm.category = ''
      console.log('交易类型变化，清空不匹配的已选择分类')
    }
  }
})

const handleSearch = () => {
  transactionStore.searchTransactions({
    ...searchForm,
    page: pagination.currentPage,
    page_size: pagination.pageSize
  })
}

const handleReset = () => {
  searchForm.search = ''
  searchForm.transaction_type = ''
  searchForm.category = ''
  searchForm.dateRange = []
  handleSearch()
}

interface WindowWithSearchTimeout extends Window {
  searchTimeout?: ReturnType<typeof setTimeout>
}

const handleSearchInput = () => {
  // 防抖搜索
  const win = window as WindowWithSearchTimeout
  if (win.searchTimeout) clearTimeout(win.searchTimeout)
  win.searchTimeout = setTimeout(handleSearch, 500)
}

const handleSelectionChange = (selection: Transaction[]) => {
  selectedTransactions.value = selection
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
  transactionStore.fetchTransactions()
  showSuccess('数据已刷新')
}

const handleExport = () => {
  // 导出功能
  showSuccess('导出功能开发中')
}

const handleBatchDelete = async () => {
  if (selectedTransactions.value.length === 0) return
  
  await ElMessageBox.confirm(
    `确定要删除选中的 ${selectedTransactions.value.length} 笔交易吗？`,
    '批量删除确认',
    { type: 'warning' }
  )
  
  try {
    const ids = selectedTransactions.value.map(t => t.id)
    await transactionStore.batchDeleteTransactions(ids)
    showSuccess('批量删除成功')
    selectedTransactions.value = []
  } catch {
    showError('批量删除失败')
  }
}

const handleEdit = (transaction: Transaction) => {
  editingTransaction.value = transaction
  Object.assign(transactionForm, {
    transaction_date: transaction.transaction_date || '',
    transaction_type: transaction.transaction_type,
    category: transaction.category,
    amount: transaction.amount,
    payment_method: transaction.payment_method,
    description: transaction.description
  })
  
  // 检查分类数据
  if (categories.value.length === 0) {
    ElMessage.warning('暂无分类，请先添加分类后再编辑')
  }
  
  showAddDialog.value = true
}

const handleDelete = async (transaction: Transaction) => {
  await ElMessageBox.confirm(
    `确定要删除这笔${transaction.transaction_type === 'income' ? '收入' : '支出'}吗？`,
    '删除确认',
    { type: 'warning' }
  )
  
  try {
    await transactionStore.deleteTransaction(transaction.id)
    showSuccess('删除成功')
  } catch {
    showError('删除失败')
  }
}

const handleAddNew = () => {
  // 重置表单
  Object.assign(transactionForm, {
    transaction_date: new Date().toISOString().split('T')[0] || '',
    transaction_type: 'expense',
    category: '',
    amount: 0,
    payment_method: 'cash',
    description: ''
  })
  editingTransaction.value = null
  
  // 检查分类数据
  if (categories.value.length === 0) {
    ElMessage.warning('暂无分类，请先添加分类后再记账')
  }
  
  showAddDialog.value = true
}

const handleSubmit = async () => {
  await transactionFormRef.value.validate()
  
  submitting.value = true
  try {
    // 转换字段名以匹配后端API
    const submitData: any = {
      ...transactionForm,
      date: transactionForm.transaction_date  // 将transaction_date转换为date
    }
    delete submitData.transaction_date  // 删除原字段
    
    if (editingTransaction.value) {
      await transactionStore.updateTransaction(editingTransaction.value.id, submitData)
      showSuccess('更新成功')
    } else {
      await transactionStore.createTransaction(submitData)
      showSuccess('新增成功')
    }
    
    showAddDialog.value = false
    resetForm()
  } catch (error) {
    console.error('提交失败:', error)
    showError('操作失败')
  } finally {
    submitting.value = false
  }
}

const resetForm = () => {
  editingTransaction.value = null
  Object.assign(transactionForm, {
    transaction_date: new Date().toISOString().split('T')[0] || '',
    transaction_type: 'expense',
    category: '',
    amount: 0,
    payment_method: 'cash',
    description: ''
  })
}

const toggleDensity = () => {
  density.value = density.value === 'default' ? 'compact' : 'default'
}

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('zh-CN')
}

const formatDateTime = (date: string) => {
  return new Date(date).toLocaleString('zh-CN')
}

const formatCurrency = (amount: number | string) => {
  const numAmount = typeof amount === 'string' ? parseFloat(amount) : amount
  if (isNaN(numAmount)) {
    return '¥0.00'
  }
  return `¥${numAmount.toFixed(2)}`
}

const getPaymentMethodType = (method: string) => {
  const types: Record<string, string> = {
    cash: 'info',
    card: 'primary',
    alipay: 'success',
    wechat: 'success',
    other: 'warning'
  }
  return types[method] || 'info'
}

const getPaymentMethodName = (method: string) => {
  const names: Record<string, string> = {
    cash: '现金',
    card: '银行卡',
    alipay: '支付宝',
    wechat: '微信',
    other: '其他'
  }
  return names[method] || method
}

const showSuccess = (message: string) => {
  ElMessage.success(message)
}

const showError = (message: string) => {
  ElMessage.error(message)
}

// 监听数据刷新事件
window.addEventListener('refresh-data', handleRefresh)

// 组件卸载时清理事件监听器
onUnmounted(() => {
  window.removeEventListener('refresh-data', handleRefresh)
})
</script>

<style scoped>
.transactions-view {
  padding: 0;
}

.transactions-card {
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

.amount-text.income {
  color: #52c41a;
  font-weight: 600;
}

.amount-text.expense {
  color: #ff4d4f;
  font-weight: 600;
}

.date-text {
  color: #595959;
  font-size: 14px;
}

.description-text {
  color: #262626;
  font-size: 14px;
}

.created-text {
  color: #8c8c8c;
  font-size: 12px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>