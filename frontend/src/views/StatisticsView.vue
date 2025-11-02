<template>
  <div class="statistics-view">
    <!-- 页面标题 -->
    <el-card>
      <template #header>
        <div class="card-header">
          <span>统计分析</span>
          <el-date-picker
            v-model="dateRange"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            @change="handleDateChange"
          />
        </div>
      </template>

      <!-- 统计卡片 -->
      <el-row :gutter="20" class="stats-row">
        <el-col :span="6">
          <el-card shadow="hover">
            <div class="stat-item">
              <div class="stat-icon student-icon">
                <el-icon><User /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-label">学生总数</div>
                <div class="stat-value">{{ statistics.total_students }}</div>
                <div class="stat-trend" :class="{ positive: calculateStudentsGrowth() > 0 }">
                  {{ calculateStudentsGrowth() > 0 ? '+' : '' }}{{ calculateStudentsGrowth() }}%
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover">
            <div class="stat-item">
              <div class="stat-icon finance-icon">
                <el-icon><Money /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-label">总收入</div>
                <div class="stat-value">¥{{ formatMoney(calculateTotalIncome()) }}</div>
                <div class="stat-trend" :class="{ positive: calculateIncomeGrowth() > 0 }">
                  {{ calculateIncomeGrowth() > 0 ? '+' : '' }}{{ calculateIncomeGrowth() }}%
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover">
            <div class="stat-item">
              <div class="stat-icon unpaid-icon">
                <el-icon><Warning /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-label">未缴费用</div>
                <div class="stat-value">¥{{ formatMoney(calculateUnpaidAmount()) }}</div>
                <div class="stat-trend negative">
                  {{ calculateUnpaidStudents() }} 人
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card shadow="hover">
            <div class="stat-item">
              <div class="stat-icon refund-icon">
                <el-icon><RefreshLeft /></el-icon>
              </div>
              <div class="stat-content">
                <div class="stat-label">退款金额</div>
                <div class="stat-value">¥{{ formatMoney(calculateTotalRefunds()) }}</div>
                <div class="stat-trend">
                  {{ calculateRefundRecords() }} 笔
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 图表区域 -->
      <el-row :gutter="20" class="charts-row">
        <el-col :span="12">
          <el-card>
            <template #header>
              <span>学生专业分布</span>
            </template>
            <div ref="majorChartRef" class="chart-container"></div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card>
            <template #header>
              <span>月度收入趋势</span>
            </template>
            <div ref="incomeChartRef" class="chart-container"></div>
          </el-card>
        </el-col>
      </el-row>

      <el-row :gutter="20" class="charts-row">
        <el-col :span="12">
          <el-card>
            <template #header>
              <span>缴费状态分布</span>
            </template>
            <div ref="paymentStatusChartRef" class="chart-container"></div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card>
            <template #header>
              <span>年级分布</span>
            </template>
            <div ref="gradeChartRef" class="chart-container"></div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 数据表格 -->
      <el-card class="data-table-card">
        <template #header>
          <span>详细数据统计</span>
          <el-button type="primary" @click="exportData">
            <el-icon><Download /></el-icon>
            导出数据
          </el-button>
        </template>
        
        <el-table
          :data="tableData"
          style="width: 100%"
          stripe
        >
          <el-table-column prop="major" label="专业" width="120" />
          <el-table-column prop="grade" label="年级" width="80" />
          <el-table-column prop="total_students" label="学生数" width="80" />
          <el-table-column prop="total_income" label="总收入" width="100">
            <template #default="{ row }">
              ¥{{ formatMoney(row.total_income) }}
            </template>
          </el-table-column>
          <el-table-column prop="unpaid_amount" label="未缴金额" width="100">
            <template #default="{ row }">
              ¥{{ formatMoney(row.unpaid_amount) }}
            </template>
          </el-table-column>
          <el-table-column prop="paid_rate" label="缴费率" width="80">
            <template #default="{ row }">
              {{ (row.paid_rate * 100).toFixed(1) }}%
            </template>
          </el-table-column>
          <el-table-column prop="avg_income" label="人均缴费" width="100">
            <template #default="{ row }">
              ¥{{ formatMoney(row.avg_income) }}
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import echarts from 'echarts'
import { useStudentStore } from '@/stores/student'
import { useFinanceStore } from '@/stores/finance'
import type { StudentStatistics } from '@/api/student'
import type { FeeRecord } from '@/api/finance'

const studentStore = useStudentStore()
const financeStore = useFinanceStore()

const dateRange = ref<string[]>([])
const statistics = ref<StudentStatistics>({
  total_students: 0,
  active_students: 0,
  inactive_students: 0,
  graduated_students: 0,
  by_major: [],
  by_grade: [],
})

const tableData = ref<any[]>([])

const majorChartRef = ref<HTMLElement>()
const incomeChartRef = ref<HTMLElement>()
const paymentStatusChartRef = ref<HTMLElement>()
const gradeChartRef = ref<HTMLElement>()

let majorChart: echarts.ECharts | null = null
let incomeChart: echarts.ECharts | null = null
let paymentStatusChart: echarts.ECharts | null = null
let gradeChart: echarts.ECharts | null = null

const formatMoney = (amount: number) => {
  return amount.toFixed(2)
}

const calculateUnpaidAmount = () => {
  return financeStore.feeRecords
    .filter((record: FeeRecord) => record.status !== 'paid')
    .reduce((total: number, record: FeeRecord) => total + record.amount, 0)
}

const calculateUnpaidStudents = () => {
  const unpaidStudentIds = new Set(
    financeStore.feeRecords
      .filter((record: FeeRecord) => record.status !== 'paid')
      .map((record: FeeRecord) => record.student)
  )
  return unpaidStudentIds.size
}

const calculateTotalRefunds = () => {
  // 由于没有退款数据，返回0
  return 0
}

const calculateRefundRecords = () => {
  // 由于没有退款数据，返回0
  return 0
}

const calculateTotalIncome = () => {
  return financeStore.feeRecords
    .filter((record: FeeRecord) => record.status === 'paid')
    .reduce((total: number, record: FeeRecord) => total + record.amount, 0)
}

const calculateIncomeGrowth = () => {
  // 简化计算，返回0（可以根据实际需求实现更复杂的计算逻辑）
  return 0
}

const calculateStudentsGrowth = () => {
  // 简化计算，返回0（可以根据实际需求实现更复杂的计算逻辑）
  return 0
}

const handleDateChange = () => {
  loadStatistics()
}

const loadStatistics = async () => {
  try {
    await studentStore.fetchStatistics()
    if (studentStore.statistics) {
      statistics.value = studentStore.statistics
    }
    
    await loadCharts()
    loadTableData()
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

const loadCharts = async () => {
  // 专业分布图表
  if (majorChartRef.value) {
    majorChart = echarts.init(majorChartRef.value)
    const majorData = studentStore.students.reduce((acc, student) => {
      acc[student.major] = (acc[student.major] || 0) + 1
      return acc
    }, {} as Record<string, number>)
    
    majorChart.setOption({
      tooltip: {
        trigger: 'item',
      },
      legend: {
        orient: 'vertical',
        left: 'left',
      },
      series: [
        {
          name: '学生数',
          type: 'pie',
          radius: '50%',
          data: Object.entries(majorData).map(([name, value]) => ({ name, value })),
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: 'rgba(0, 0, 0, 0.5)',
            },
          },
        },
      ],
    })
  }
  
  // 月度收入趋势图表
  if (incomeChartRef.value) {
    incomeChart = echarts.init(incomeChartRef.value)
    const monthlyData = financeStore.feeRecords.reduce((acc: Record<string, number>, record: FeeRecord) => {
      if (record.status === 'paid' && record.paid_date) {
        const month = record.paid_date.substring(0, 7)
        acc[month] = (acc[month] || 0) + record.amount
      }
      return acc
    }, {} as Record<string, number>)
    
    const sortedMonths = Object.keys(monthlyData).sort()
    
    incomeChart.setOption({
      tooltip: {
        trigger: 'axis',
      },
      xAxis: {
        type: 'category',
        data: sortedMonths,
      },
      yAxis: {
        type: 'value',
        name: '收入 (元)',
      },
      series: [
        {
          name: '月度收入',
          type: 'line',
          data: sortedMonths.map(month => monthlyData[month]),
          smooth: true,
          itemStyle: {
            color: '#409EFF',
          },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(64, 158, 255, 0.3)' },
              { offset: 1, color: 'rgba(64, 158, 255, 0.1)' },
            ]),
          },
        },
      ],
    })
  }
  
  // 缴费状态分布图表
  if (paymentStatusChartRef.value) {
    paymentStatusChart = echarts.init(paymentStatusChartRef.value)
    const statusData = financeStore.feeRecords.reduce((acc: Record<string, number>, record: FeeRecord) => {
      acc[record.status] = (acc[record.status] || 0) + 1
      return acc
    }, {} as Record<string, number>)
    
    const statusLabels: Record<string, string> = {
      paid: '已缴费',
      unpaid: '未缴费',
      partial: '部分缴费',
    }
    
    paymentStatusChart.setOption({
      tooltip: {
        trigger: 'item',
      },
      series: [
        {
          name: '缴费状态',
          type: 'pie',
          radius: ['40%', '70%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderColor: '#fff',
            borderWidth: 2,
          },
          label: {
            show: false,
            position: 'center',
          },
          emphasis: {
            label: {
              show: true,
              fontSize: '20',
              fontWeight: 'bold',
            },
          },
          labelLine: {
            show: false,
          },
          data: Object.entries(statusData).map(([status, count]) => ({
            name: statusLabels[status] || status,
            value: count,
          })),
        },
      ],
    })
  }
  
  // 年级分布图表
  if (gradeChartRef.value) {
    gradeChart = echarts.init(gradeChartRef.value)
    const gradeData = studentStore.students.reduce((acc, student) => {
      acc[student.grade] = (acc[student.grade] || 0) + 1
      return acc
    }, {} as Record<string, number>)
    
    gradeChart.setOption({
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow',
        },
      },
      xAxis: {
        type: 'category',
        data: Object.keys(gradeData),
      },
      yAxis: {
        type: 'value',
        name: '学生数',
      },
      series: [
        {
          name: '学生数',
          type: 'bar',
          data: Object.values(gradeData),
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#83bff6' },
              { offset: 0.5, color: '#188df0' },
              { offset: 1, color: '#188df0' },
            ]),
          },
        },
      ],
    })
  }
}

const loadTableData = () => {
  const majorGradeData: Record<string, any> = {}
  
  studentStore.students.forEach(student => {
    const key = `${student.major}-${student.grade}`
    if (!majorGradeData[key]) {
      majorGradeData[key] = {
        major: student.major,
        grade: student.grade,
        total_students: 0,
        total_income: 0,
        unpaid_amount: 0,
        paid_rate: 0,
        avg_income: 0,
      }
    }
    majorGradeData[key].total_students++
  })
  
  financeStore.feeRecords.forEach((record: FeeRecord) => {
    const student = studentStore.students.find(s => s.id === record.student)
    if (student) {
      const key = `${student.major}-${student.grade}`
      if (majorGradeData[key]) {
        if (record.status === 'paid') {
        majorGradeData[key].total_income += record.amount
      } else {
        majorGradeData[key].unpaid_amount += record.amount
        }
      }
    }
  })
  
  Object.values(majorGradeData).forEach((item: any) => {
    const totalRecords = financeStore.feeRecords.filter((record: FeeRecord) => {
      const student = studentStore.students.find(s => s.id === record.student)
      return student && student.major === item.major && student.grade === item.grade
    }).length
    
    const paidRecords = financeStore.feeRecords.filter((record: FeeRecord) => {
      const student = studentStore.students.find(s => s.id === record.student)
      return student && student.major === item.major && student.grade === item.grade && record.status === 'paid'
    }).length
    
    item.paid_rate = totalRecords > 0 ? paidRecords / totalRecords : 0
    item.avg_income = item.total_students > 0 ? item.total_income / item.total_students : 0
  })
  
  tableData.value = Object.values(majorGradeData)
}

const exportData = () => {
  const data = tableData.value.map(item => ({
    专业: item.major,
    年级: item.grade,
    学生数: item.total_students,
    总收入: item.total_income,
    未缴金额: item.unpaid_amount,
    缴费率: (item.paid_rate * 100).toFixed(1) + '%',
    人均缴费: item.avg_income.toFixed(2),
  }))
  
  if (data.length === 0) {
    return
  }
  
  const headers = ['专业', '年级', '学生数', '总收入', '未缴金额', '缴费率', '人均缴费']
  const csvContent = [
    headers.join(','),
    ...data.map(item => Object.values(item).join(','))
  ].join('\n')
  
  const blob = new Blob(['\ufeff' + csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = `学生缴费统计_${new Date().toISOString().split('T')[0]}.csv`
  link.click()
}

onMounted(async () => {
  await studentStore.fetchStudents()
  await financeStore.fetchFeeRecords()
  await loadStatistics()
  
  window.addEventListener('resize', () => {
    majorChart?.resize()
    incomeChart?.resize()
    paymentStatusChart?.resize()
    gradeChart?.resize()
  })
})

onUnmounted(() => {
  majorChart?.dispose()
  incomeChart?.dispose()
  paymentStatusChart?.dispose()
  gradeChart?.dispose()
  
  window.removeEventListener('resize', () => {
    majorChart?.resize()
    incomeChart?.resize()
    paymentStatusChart?.resize()
    gradeChart?.resize()
  })
})
</script>

<style scoped>
.statistics-view {
  padding: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-item {
  display: flex;
  align-items: center;
  padding: 20px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 20px;
  font-size: 24px;
  color: white;
}

.student-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.finance-icon {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.unpaid-icon {
  background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
  color: #e6a23c;
}

.refund-icon {
  background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
  color: #f56c6c;
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 8px;
}

.stat-trend {
  font-size: 12px;
  color: #909399;
}

.stat-trend.positive {
  color: #67c23a;
}

.stat-trend.negative {
  color: #f56c6c;
}

.charts-row {
  margin-bottom: 20px;
}

.chart-container {
  height: 300px;
}

.data-table-card {
  margin-top: 20px;
}
</style>