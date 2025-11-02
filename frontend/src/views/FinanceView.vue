<template>
  <Layout>
    <div class="finance-view">
      <el-card class="finance-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <div class="header-left">
              <el-icon style="color: #52c41a; margin-right: 8px;"><Money /></el-icon>
              <span class="card-title">费用管理</span>
              <el-tag type="info" size="small" style="margin-left: 12px;">
                共 {{ financeStore.totalCount }} 条记录
              </el-tag>
            </div>
            <el-button type="primary" @click="showAddDialog = true" :icon="Plus">
              新增缴费记录
            </el-button>
          </div>
        </template>

      <!-- 搜索和筛选 -->
      <div class="search-section">
        <el-form :inline="true" :model="searchForm" class="search-form">
          <el-form-item label="学生姓名">
            <el-input
              v-model="searchForm.student_name"
              placeholder="请输入学生姓名"
              clearable
              @clear="handleSearch"
              @keyup.enter="handleSearch"
              :prefix-icon="Search"
            />
          </el-form-item>
          <el-form-item label="费用类别">
            <el-select v-model="searchForm.category_id" placeholder="全部" clearable @change="handleSearch">
              <el-option
                v-for="category in financeStore.categories"
                :key="category.id"
                :label="category.name"
                :value="category.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="缴费状态">
            <el-select v-model="searchForm.status" placeholder="全部" clearable @change="handleSearch">
              <el-option label="已缴费" value="paid" />
              <el-option label="未缴费" value="unpaid" />
              <el-option label="部分缴费" value="partial" />
            </el-select>
          </el-form-item>
          <el-form-item label="缴费日期">
            <el-date-picker
              v-model="searchForm.date_range"
              type="daterange"
              range-separator="至"
              start-placeholder="开始日期"
              end-placeholder="结束日期"
              format="YYYY-MM-DD"
              value-format="YYYY-MM-DD"
              @change="handleSearch"
              style="width: 240px;"
            />
          </el-form-item>
          <el-form-item>
            <div class="search-buttons">
              <el-button type="primary" @click="handleSearch" :icon="Search">
                搜索
              </el-button>
              <el-button @click="handleReset" :icon="Refresh">
                重置
              </el-button>
            </div>
          </el-form-item>
        </el-form>
      </div>

      <!-- 统计信息 -->
      <div class="statistics-section">
        <el-row :gutter="20" class="statistics-row">
          <el-col :xs="12" :sm="6" :md="6" :lg="6">
            <div class="statistic-card">
              <div class="statistic-icon" style="background: #e6f7ff;">
                <el-icon style="color: #1890ff; font-size: 24px;"><Money /></el-icon>
              </div>
              <div class="statistic-content">
                <div class="statistic-label">总缴费金额</div>
                <div class="statistic-value">¥{{ formatMoney(financeStore.totalPaidAmount) }}</div>
              </div>
            </div>
          </el-col>
          <el-col :xs="12" :sm="6" :md="6" :lg="6">
            <div class="statistic-card">
              <div class="statistic-icon" style="background: #fff7e6;">
                <el-icon style="color: #faad14; font-size: 24px;"><Warning /></el-icon>
              </div>
              <div class="statistic-content">
                <div class="statistic-label">待缴费金额</div>
                <div class="statistic-value">¥{{ formatMoney(financeStore.totalUnpaidAmount) }}</div>
              </div>
            </div>
          </el-col>
          <el-col :xs="12" :sm="6" :md="6" :lg="6">
            <div class="statistic-card">
              <div class="statistic-icon" style="background: #f6ffed;">
                <el-icon style="color: #52c41a; font-size: 24px;"><TrendCharts /></el-icon>
              </div>
              <div class="statistic-content">
                <div class="statistic-label">本月缴费</div>
                <div class="statistic-value">¥{{ formatMoney(financeStore.monthlyPaidAmount) }}</div>
              </div>
            </div>
          </el-col>
          <el-col :xs="12" :sm="6" :md="6" :lg="6">
            <div class="statistic-card">
              <div class="statistic-icon" style="background: #f9f0ff;">
                <el-icon style="color: #722ed1; font-size: 24px;"><Document /></el-icon>
              </div>
              <div class="statistic-content">
                <div class="statistic-label">缴费记录数</div>
                <div class="statistic-value">{{ financeStore.totalCount }}</div>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>

      <!-- 缴费记录列表 -->
      <div class="table-section">
        <el-table
          v-loading="financeStore.loading"
          :data="financeStore.feeRecords"
          style="width: 100%"
          stripe
          border
          :header-cell-style="{ background: '#f8f9fa', fontWeight: 'bold' }"
        >
          <el-table-column prop="student_name" label="学生姓名" width="120" fixed="left">
            <template #default="{ row }">
              <div class="student-info">
                <el-avatar :size="24" :style="{ backgroundColor: getAvatarColor(row.student_name) }">
                  {{ row.student_name.charAt(0) }}
                </el-avatar>
                <span class="student-name">{{ row.student_name }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="student_id" label="学号" width="120" />
          <el-table-column prop="category_name" label="费用类别" width="120">
            <template #default="{ row }">
              <el-tag type="info" size="small">{{ row.category_name }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="amount" label="应缴金额" width="100" align="right">
            <template #default="{ row }">
              <span class="amount-due">¥{{ formatMoney(row.amount) }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="paid_amount" label="实缴金额" width="100" align="right">
            <template #default="{ row }">
              <span class="amount-paid">¥{{ formatMoney(row.paid_amount) }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="status" label="缴费状态" width="100" align="center">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)" size="small">
                <el-icon style="margin-right: 4px;">
                  <CircleCheck v-if="row.status === 'paid'" />
                  <CircleClose v-else-if="row.status === 'unpaid'" />
                  <Warning v-else />
                </el-icon>
                {{ getStatusLabel(row.status) }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="due_date" label="应缴日期" width="120" align="center">
            <template #default="{ row }">
              <span class="date-text">{{ row.due_date }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="payment_date" label="缴费日期" width="120" align="center">
            <template #default="{ row }">
              <span class="date-text">{{ row.payment_date || '-' }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="description" label="描述" min-width="150" show-overflow-tooltip />
          <el-table-column label="操作" width="180" fixed="right" align="center">
            <template #default="{ row }">
              <div class="action-buttons">
                <el-button
                  v-if="row.status !== 'paid'"
                  type="primary"
                  size="small"
                  @click="handlePayment(row)"
                  :icon="Money"
                >
                  缴费
                </el-button>
                <el-button
                  v-if="row.status === 'paid'"
                  type="warning"
                  size="small"
                  @click="handleRefund(row)"
                  :icon="RefreshLeft"
                >
                  退款
                </el-button>
                <el-button type="danger" size="small" @click="handleDelete(row)" :icon="Delete">
                  删除
                </el-button>
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 分页 -->
      <div class="pagination-section">
        <el-pagination
          v-model:current-page="financeStore.currentPage"
          v-model:page-size="financeStore.pageSize"
          :total="financeStore.totalRecords"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          background
          :hide-on-single-page="false"
        />
      </div>
    </el-card>

    <!-- 新增缴费记录对话框 -->
    <el-dialog
      v-model="showAddDialog"
      title="新增缴费记录"
      width="600px"
    >
      <el-form
        ref="feeRecordFormRef"
        :model="feeRecordForm"
        :rules="feeRecordRules"
        label-width="100px"
      >
        <el-form-item label="学生" prop="student">
          <el-select
            v-model="feeRecordForm.student"
            placeholder="请选择学生"
            filterable
            style="width: 100%"
          >
            <el-option
              v-for="student in studentStore.students"
              :key="student.id"
              :label="`${student.name} (${student.student_id})`"
              :value="student.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="费用类别" prop="fee_category">
          <el-select
            v-model="feeRecordForm.fee_category"
            placeholder="请选择费用类别"
            style="width: 100%"
          >
            <el-option
              v-for="category in financeStore.categories"
              :key="category.id"
              :label="category.name"
              :value="category.id"
            />
          </el-select>
        </el-form-item>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="应缴金额" prop="amount">
              <el-input-number
                v-model="feeRecordForm.amount"
                :min="0"
                :precision="2"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="应缴日期" prop="due_date">
              <el-date-picker
                v-model="feeRecordForm.due_date"
                type="date"
                placeholder="选择日期"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="feeRecordForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入描述信息"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showAddDialog = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="financeStore.loading">
            确定
          </el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 缴费对话框 -->
    <el-dialog
      v-model="showPaymentDialog"
      title="缴费"
      width="400px"
    >
      <el-form
        ref="paymentFormRef"
        :model="paymentForm"
        :rules="paymentRules"
        label-width="80px"
      >
        <el-form-item label="应缴金额">
          <el-input :value="`¥${formatMoney(currentRecord?.amount || 0)}`" readonly />
        </el-form-item>
        <el-form-item label="实缴金额" prop="amount">
          <el-input-number
            v-model="paymentForm.amount"
            :min="0"
            :max="currentRecord?.amount || 0"
            :precision="2"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="缴费日期" prop="payment_date">
          <el-date-picker
            v-model="paymentForm.payment_date"
            type="date"
            placeholder="选择日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="备注" prop="notes">
          <el-input
            v-model="paymentForm.notes"
            type="textarea"
            :rows="2"
            placeholder="请输入备注信息"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showPaymentDialog = false">取消</el-button>
          <el-button type="primary" @click="handlePaymentSubmit" :loading="financeStore.loading">
            确认缴费
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
  </Layout>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import type { FormInstance, FormRules } from 'element-plus'
import { useFinanceStore } from '@/stores/finance'
import { useStudentStore } from '@/stores/student'
import type { FeeRecord } from '@/api/finance'
import Layout from '@/components/Layout.vue'
import {
  Money,
  Search,
  Refresh,
  Plus,
  Edit,
  Delete,
  CircleCheck,
  CircleClose,
  Warning,
  TrendCharts,
  Document,
  RefreshLeft
} from '@element-plus/icons-vue'

const financeStore = useFinanceStore()
const studentStore = useStudentStore()

const showAddDialog = ref(false)
const showPaymentDialog = ref(false)
const feeRecordFormRef = ref<FormInstance>()
const paymentFormRef = ref<FormInstance>()
const currentRecord = ref<FeeRecord | null>(null)

const searchForm = reactive({
  student_name: '',
  category_id: '',
  status: '',
  date_range: [],
})

const feeRecordForm = reactive({
  student: '',
  fee_category: '',
  amount: 0,
  due_date: '',
  status: 'pending',
  description: '',
})

const paymentForm = reactive({
  amount: 0,
  payment_date: '',
  notes: '',
})

const feeRecordRules: FormRules = {
  student: [{ required: true, message: '请选择学生', trigger: 'change' }],
  fee_category: [{ required: true, message: '请选择费用类别', trigger: 'change' }],
  amount: [{ required: true, message: '请输入应缴金额', trigger: 'blur' }],
  due_date: [{ required: true, message: '请选择应缴日期', trigger: 'change' }],
}

const paymentRules: FormRules = {
  amount: [{ required: true, message: '请输入实缴金额', trigger: 'blur' }],
  payment_date: [{ required: true, message: '请选择缴费日期', trigger: 'change' }],
}

const monthlyIncome = computed(() => {
  const now = new Date()
  const currentMonth = now.getMonth()
  const currentYear = now.getFullYear()
  
  return financeStore.feeRecords
    .filter((record: FeeRecord) => {
      const paymentDate = record.paid_date ? new Date(record.paid_date) : null
      return paymentDate && 
             paymentDate.getMonth() === currentMonth && 
             paymentDate.getFullYear() === currentYear &&
             record.status === 'paid'
    })
    .reduce((sum: number, record: FeeRecord) => sum + (record.paid_amount || 0), 0)
})

const unpaidAmount = computed(() => {
  return financeStore.feeRecords
    .filter((record: FeeRecord) => record.status === 'pending' || record.status === 'overdue')
    .reduce((sum: number, record: FeeRecord) => sum + (record.amount - (record.paid_amount || 0)), 0)
})

const formatMoney = (amount: number) => {
  return amount.toFixed(2)
}

const getAvatarColor = (name: string) => {
  const colors = ['#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#909399']
  const index = name.charCodeAt(0) % colors.length
  return colors[index]
}

const getStatusType = (status: string) => {
  const types: Record<string, string> = {
    paid: 'success',
    unpaid: 'danger',
    partial: 'warning',
  }
  return types[status] || 'info'
}

const getStatusLabel = (status: string) => {
  const labels: Record<string, string> = {
    paid: '已缴费',
    unpaid: '未缴费',
    partial: '部分缴费',
  }
  return labels[status] || status
}

const handleSearch = () => {
  financeStore.fetchFeeRecords(searchForm)
}

const handleReset = () => {
  searchForm.student_name = ''
  searchForm.category_id = ''
  searchForm.status = ''
  searchForm.date_range = []
  financeStore.fetchFeeRecords()
}

const handleSizeChange = (size: number) => {
  financeStore.setPageSize(size)
}

const handleCurrentChange = (page: number) => {
  financeStore.setPage(page)
}

const handlePayment = (row: FeeRecord) => {
  currentRecord.value = row
  paymentForm.amount = row.amount - (row.paid_amount || 0)
  paymentForm.payment_date = new Date().toISOString().split('T')[0] as string
  paymentForm.notes = ''
  showPaymentDialog.value = true
}

const handleRefund = async (row: FeeRecord) => {
  try {
    await ElMessageBox.confirm(
      `确定要为学生 "${row.student_name || '未知学生'}" 办理退款吗？`,
      '退款确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await financeStore.createPayment({
      fee_record: row.id!,
      amount: row.paid_amount || 0,
      payment_date: new Date().toISOString().split('T')[0] as string,
      payment_method: 'cash',
      notes: '管理员操作退款',
    })
    
    ElMessage.success('退款成功')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('退款失败')
    }
  }
}

const handleDelete = async (row: FeeRecord) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除缴费记录吗？`,
      '删除确认',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    await financeStore.deleteFeeRecord(row.id!)
    ElMessage.success('删除成功')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleSubmit = async () => {
  if (!feeRecordFormRef.value) return
  
  try {
    await feeRecordFormRef.value.validate()
    await financeStore.createFeeRecord({
      student: Number(feeRecordForm.student),
      fee_category: Number(feeRecordForm.fee_category),
      amount: feeRecordForm.amount,
      due_date: feeRecordForm.due_date,
      status: feeRecordForm.status as 'pending' | 'paid' | 'overdue' | 'cancelled',
      notes: feeRecordForm.description,
    })
    ElMessage.success('创建成功')
    showAddDialog.value = false
    resetFeeRecordForm()
  } catch (error) {
    ElMessage.error('创建失败')
  }
}

const handlePaymentSubmit = async () => {
  if (!paymentFormRef.value || !currentRecord.value) return
  
  try {
    await paymentFormRef.value.validate()
    
    await financeStore.updateFeeRecord(currentRecord.value.id!, {
      student: currentRecord.value.student,
      fee_category: currentRecord.value.fee_category,
      amount: currentRecord.value.amount,
      due_date: currentRecord.value.due_date,
      paid_date: paymentForm.payment_date,
      status: 'paid',
      notes: paymentForm.notes,
    })
    
    ElMessage.success('缴费成功')
    showPaymentDialog.value = false
  } catch (error) {
    ElMessage.error('缴费失败')
  }
}

function resetFeeRecordForm() {
  Object.assign(feeRecordForm, {
    student: '',
    fee_category: '',
    amount: 0,
    due_date: '',
    status: 'pending',
    description: '',
  })
  feeRecordFormRef.value?.clearValidate()
}

onMounted(async () => {
  await studentStore.fetchStudents()
  await financeStore.fetchCategories()
  await financeStore.fetchFeeRecords()
})
</script>

<style scoped>
.finance-view {
  padding: 24px;
  background: #f5f7fa;
  min-height: calc(100vh - 60px);
}

.finance-card {
  border: none;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.finance-card:hover {
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12) !important;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0;
}

.header-left {
  display: flex;
  align-items: center;
}

.card-title {
  font-size: 20px;
  font-weight: 600;
  color: #303133;
}

.search-section {
  margin-bottom: 24px;
  padding: 20px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.search-form {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  align-items: flex-start;
}

.search-buttons {
  display: flex;
  gap: 12px;
}

.statistics-section {
  margin-bottom: 24px;
}

.statistics-row {
  margin: 0 !important;
}

.statistic-card {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: transform 0.2s ease;
  height: 100%;
}

.statistic-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.statistic-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.statistic-content {
  flex: 1;
}

.statistic-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
  font-weight: 500;
}

.statistic-value {
  font-size: 24px;
  font-weight: 700;
  color: #303133;
  line-height: 1.2;
}

.table-section {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.student-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.student-name {
  font-weight: 500;
  color: #303133;
}

.amount-due {
  color: #f5222d;
  font-weight: 600;
}

.amount-paid {
  color: #52c41a;
  font-weight: 600;
}

.date-text {
  color: #666;
  font-size: 14px;
}

.action-buttons {
  display: flex;
  gap: 8px;
  justify-content: center;
}

.pagination-section {
  margin-top: 24px;
  display: flex;
  justify-content: flex-end;
}

.dialog-footer {
  text-align: right;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .finance-view {
    padding: 16px;
  }
  
  .search-form {
    flex-direction: column;
    align-items: stretch;
  }
  
  .search-buttons {
    justify-content: center;
    margin-top: 8px;
  }
  
  .statistic-card {
    padding: 16px;
    gap: 12px;
  }
  
  .statistic-icon {
    width: 40px;
    height: 40px;
  }
  
  .statistic-value {
    font-size: 20px;
  }
  
  .action-buttons {
    flex-direction: column;
    gap: 4px;
  }
  
  .pagination-section {
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .card-title {
    font-size: 18px;
  }
  
  .header-left {
    flex-wrap: wrap;
    gap: 8px;
  }
  
  .statistic-card {
    flex-direction: column;
    text-align: center;
  }
  
  .action-buttons {
    flex-direction: row;
    flex-wrap: wrap;
  }
}
</style>