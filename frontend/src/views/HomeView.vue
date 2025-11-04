<template>
  <div class="dashboard">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-container">
      <el-icon class="loading-icon" size="48"><Loading /></el-icon>
      <p class="loading-text">正在加载数据...</p>
    </div>

    <!-- 错误状态 -->
    <div v-else-if="error" class="error-container">
      <el-icon class="error-icon" size="48"><Warning /></el-icon>
      <p class="error-text">{{ error }}</p>
      <el-button type="primary" @click="loadData" :icon="Refresh">重新加载</el-button>
    </div>

    <!-- 数据展示区域 -->
    <div v-else>
      <!-- 统计卡片区域 -->
      <el-row :gutter="24" class="stats-row">
        <el-col :span="6" :xs="24" :sm="12" :md="6">
          <el-card class="stat-card" shadow="hover" @click="navigateToTransactions">
            <div class="stat-content">
              <div class="stat-icon-wrapper" style="background-color: #e6f7ff;">
                <el-icon class="stat-icon" style="color: #1890ff; font-size: 24px;"><Money /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-number" :class="{ 'skeleton': loading }">{{ (statistics as any)?.total_transactions || 0 }}</div>
                <div class="stat-label">总交易数</div>
              </div>
            </div>
            <div class="stat-footer">
              <span class="stat-trend" v-if="transactionTrend !== 0">
                <el-icon :class="{ 'trend-up': transactionTrend > 0, 'trend-down': transactionTrend < 0 }">
                  <CaretTop v-if="transactionTrend > 0" />
                  <CaretBottom v-else />
                </el-icon>
                {{ Math.abs(transactionTrend) }}% 较上月
              </span>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6" :xs="24" :sm="12" :md="6">
          <el-card class="stat-card" shadow="hover" @click="navigateToBudget">
            <div class="stat-content">
              <div class="stat-icon-wrapper" style="background-color: #f6ffed;">
                <el-icon class="stat-icon" style="color: #52c41a; font-size: 24px;"><Wallet /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-number" :class="{ 'skeleton': loading }">¥{{ formatMoney((statistics as any)?.total_budget || 0) }}</div>
                <div class="stat-label">总预算</div>
              </div>
            </div>
            <div class="stat-footer">
              <span class="stat-trend" v-if="budgetTrend !== 0">
                <el-icon :class="{ 'trend-up': budgetTrend > 0, 'trend-down': budgetTrend < 0 }">
                  <CaretTop v-if="budgetTrend > 0" />
                  <CaretBottom v-else />
                </el-icon>
                {{ Math.abs(budgetTrend) }}% 较上月
              </span>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6" :xs="24" :sm="12" :md="6">
          <el-card class="stat-card" shadow="hover" @click="navigateToFinance">
            <div class="stat-content">
              <div class="stat-icon-wrapper" style="background-color: #fff7e6;">
                <el-icon class="stat-icon" style="color: #fa8c16; font-size: 24px;"><TrendCharts /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-number" :class="{ 'skeleton': loading }">¥{{ formatMoney((statistics as any)?.total_expense || 0) }}</div>
                <div class="stat-label">总支出</div>
              </div>
            </div>
            <div class="stat-footer">
              <span class="stat-trend" v-if="expenseTrend !== 0">
                <el-icon :class="{ 'trend-up': expenseTrend > 0, 'trend-down': expenseTrend < 0 }">
                  <CaretTop v-if="expenseTrend > 0" />
                  <CaretBottom v-else />
                </el-icon>
                {{ Math.abs(expenseTrend) }}% 较上月
              </span>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6" :xs="24" :sm="12" :md="6">
          <el-card class="stat-card" shadow="hover" @click="navigateToGoals">
            <div class="stat-content">
              <div class="stat-icon-wrapper" style="background-color: #f0f5ff;">
                <el-icon class="stat-icon" style="color: #2f54eb; font-size: 24px;"><Flag /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-number" :class="{ 'skeleton': loading }">{{ (statistics as any)?.active_goals || 0 }}</div>
                <div class="stat-label">活跃目标</div>
              </div>
            </div>
            <div class="stat-footer">
              <span class="stat-trend" v-if="goalsTrend !== 0">
                <el-icon :class="{ 'trend-up': goalsTrend > 0, 'trend-down': goalsTrend < 0 }">
                  <CaretTop v-if="goalsTrend > 0" />
                  <CaretBottom v-else />
                </el-icon>
                {{ Math.abs(goalsTrend) }}% 较上月
              </span>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <el-row :gutter="24" class="charts-row">
        <el-col :span="12" :xs="24" :sm="24" :md="12">
          <el-card class="chart-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <el-icon style="color: #1890ff; margin-right: 8px;"><PieChart /></el-icon>
                <span>支出分类分布</span>
                <el-tooltip content="点击查看详细分析" placement="top">
                  <el-button 
                    type="primary" 
                    link 
                    @click="navigateToStatistics"
                    style="margin-left: auto;"
                  >
                    详情
                  </el-button>
                </el-tooltip>
              </div>
            </template>
            <div class="chart-wrapper">
              <div v-if="chartLoading.expense" class="chart-loading">
                <el-icon class="loading-icon" size="32"><Loading /></el-icon>
              </div>
              <div v-else-if="chartError.expense" class="chart-error">
                <el-icon size="32" color="#f5222d"><Warning /></el-icon>
                <p>图表加载失败</p>
                <el-button type="primary" link @click="reloadExpenseChart">重试</el-button>
              </div>
              <div v-else ref="expenseChart" class="chart-container"></div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="12" :xs="24" :sm="24" :md="12">
          <el-card class="chart-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <el-icon style="color: #52c41a; margin-right: 8px;"><TrendCharts /></el-icon>
                <span>月度收支趋势</span>
                <el-tooltip content="点击查看详细分析" placement="top">
                  <el-button 
                    type="primary" 
                    link 
                    @click="navigateToStatistics"
                    style="margin-left: auto;"
                  >
                    详情
                  </el-button>
                </el-tooltip>
              </div>
            </template>
            <div class="chart-wrapper">
              <div v-if="chartLoading.trend" class="chart-loading">
                <el-icon class="loading-icon" size="32"><Loading /></el-icon>
              </div>
              <div v-else-if="chartError.trend" class="chart-error">
                <el-icon size="32" color="#f5222d"><Warning /></el-icon>
                <p>图表加载失败</p>
                <el-button type="primary" link @click="reloadTrendChart">重试</el-button>
              </div>
              <div v-else ref="trendChart" class="chart-container"></div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <!-- 最近操作 -->
      <el-row class="recent-activities-row">
        <el-col :span="24">
          <el-card class="recent-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <el-icon style="color: #722ed1; margin-right: 8px;"><Clock /></el-icon>
                <span>最近操作</span>
                <div class="header-actions">
                  <el-tag size="small" type="info" style="margin-right: 8px;">最近5条</el-tag>
                  <el-button 
                    type="primary" 
                    link 
                    @click="refreshActivities"
                    :loading="activitiesLoading"
                    :icon="Refresh"
                  >
                    刷新
                  </el-button>
                </div>
              </div>
            </template>
            <div class="recent-activities">
              <div v-if="activitiesLoading" class="activities-loading">
                <el-icon class="loading-icon" size="32"><Loading /></el-icon>
                <p>正在加载操作记录...</p>
              </div>
              <div v-else-if="recentActivities.length === 0" class="empty-state">
                <el-empty description="暂无操作记录" :image-size="64">
                  <template #description>
                    <p>暂无操作记录</p>
                    <p class="empty-hint">当您添加交易或管理预算时，操作记录将显示在这里</p>
                  </template>
                </el-empty>
              </div>
              <div v-else class="activity-list">
                <div 
                  v-for="activity in recentActivities" 
                  :key="activity.id"
                  class="activity-item"
                  @click="handleActivityClick(activity)"
                >
                  <div class="activity-icon" :class="getActivityIconClass(activity.action)">
                    <el-icon :size="16">
                      <component :is="getActivityIcon(activity.action)" />
                    </el-icon>
                  </div>
                  <div class="activity-content">
                    <div class="activity-title">{{ activity.action }}</div>
                    <div class="activity-subtitle">{{ activity.description }} <span v-if="activity.amount > 0">¥{{ formatMoney(activity.amount) }}</span></div>
                    <div class="activity-time">{{ formatDateTime(activity.created_at) }}</div>
                  </div>
                  <div class="activity-action">
                    <el-icon><ArrowRight /></el-icon>
                  </div>
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useFinanceStore } from '@/stores/finance'
import * as echarts from 'echarts'
import { showSuccess, showError, showInfo } from '@/utils/message'
import { 
  Money, 
  Wallet, 
  TrendCharts, 
  Flag,
  PieChart, 
  Clock,
  Plus,
  Edit,
  Delete,
  Refresh,
  ArrowRight,
  Loading,
  Warning,
  CaretTop,
  CaretBottom,
  Document
} from '@element-plus/icons-vue'

const financeStore = useFinanceStore()

const statistics = computed(() => financeStore.statistics)
const paymentStats = computed(() => financeStore.statistics)

// 图表引用
const expenseChart = ref<HTMLElement>()
const trendChart = ref<HTMLElement>()

// 状态定义
const financeLoading = ref(false)
const financeError = ref('')
const expenseChartLoading = ref(false)
const expenseChartError = ref('')
const trendChartLoading = ref(false)
const trendChartError = ref('')
const activitiesLoading = ref(false)
const loading = ref(false)
const error = ref('')
const router = useRouter()

// 计算属性
const transactionTrend = ref(0)
const budgetTrend = ref(0)
const expenseTrend = ref(0)
const goalsTrend = ref(0)

// 图表加载状态
const chartLoading = ref({
  expense: false,
  trend: false
})

const chartError = ref({
  expense: '',
  trend: ''
})

// 模拟最近活动数据
const recentActivities = ref([
  {
    id: 1,
    action: '添加交易',
    description: '餐饮支出',
    category: 'food',
    amount: 128.50,
    created_at: new Date(Date.now() - 1000 * 60 * 30).toISOString()
  },
  {
    id: 2,
    action: '预算更新',
    description: '月度预算调整',
    category: 'budget',
    amount: 0,
    created_at: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString()
  },
  {
    id: 3,
    action: '添加交易',
    description: '交通费用',
    category: 'transport',
    amount: 45.00,
    created_at: new Date(Date.now() - 1000 * 60 * 60 * 5).toISOString()
  },
  {
    id: 4,
    action: '目标达成',
    description: '储蓄目标完成',
    category: 'savings',
    amount: 1000.00,
    created_at: new Date(Date.now() - 1000 * 60 * 60 * 8).toISOString()
  },
  {
    id: 5,
    action: '添加交易',
    description: '购物支出',
    category: 'shopping',
    amount: 299.90,
    created_at: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString()
  }
])

// 刷新操作记录
const refreshActivities = async () => {
  activitiesLoading.value = true
  try {
    // 模拟API调用延迟
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 模拟刷新数据 - 随机添加或更新时间
    const now = new Date()
    recentActivities.value = recentActivities.value.map(activity => ({
      ...activity,
      created_at: new Date(now.getTime() - Math.random() * 24 * 60 * 60 * 1000).toISOString()
    }))
    
    showSuccess('操作记录已刷新')
  } catch (error) {
    showError('刷新操作记录失败')
  } finally {
    activitiesLoading.value = false
  }
}

// 处理活动点击
const handleActivityClick = (activity: any) => {
  // 根据活动类型导航到对应页面
  if (activity.action.includes('交易') || activity.action.includes('支出')) {
    router.push({
      name: 'transactions',
      query: { search: activity.description }
    })
  } else if (activity.action.includes('预算') || activity.action.includes('目标')) {
    router.push({
      name: 'budget',
      query: { category: activity.category }
    })
  }
  
  showInfo(`正在查看 ${activity.description || activity.action} 的详细信息`)
}

const maxCategoryCount = computed(() => {
  if (!(statistics.value as any)?.by_category?.length) return 0
  return Math.max(...(statistics.value as any).by_category.map((item: any) => item.amount))
})

const maxMonthlyCount = computed(() => {
  if (!statistics.value?.monthly_stats?.length) return 0
  return Math.max(...statistics.value.monthly_stats.map(item => item.total_amount))
})

const getBarWidth = (value: number, max: number) => {
  return max > 0 ? (value / max) * 100 : 0
}

const getCategoryBarWidth = (amount: number) => {
  return getBarWidth(amount, maxCategoryCount.value)
}

const getMonthlyBarWidth = (amount: number) => {
  return getBarWidth(amount, maxMonthlyCount.value)
}

// 更新支出分类图表
const updateExpenseChart = () => {
  if (!expenseChart.value) return
  
  const chart = echarts.init(expenseChart.value)
  
  // 模拟支出分类数据
  const expenseData = [
    { value: 1200, name: '餐饮' },
    { value: 800, name: '交通' },
    { value: 600, name: '购物' },
    { value: 400, name: '娱乐' },
    { value: 300, name: '其他' }
  ]
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: ¥{c} ({d}%)'
    },
    legend: {
      orient: 'horizontal',
      bottom: '5%',
      textStyle: {
        fontSize: 12
      }
    },
    color: ['#1890ff', '#52c41a', '#fa8c16', '#f5222d', '#722ed1'],
    series: [
      {
        name: '支出分类',
        type: 'pie',
        radius: ['40%', '70%'],
        center: ['50%', '40%'],
        avoidLabelOverlap: false,
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: expenseData
      }
    ]
  }
  
  chart.setOption(option)
  
  // 响应式处理
  window.addEventListener('resize', () => {
    chart.resize()
  })
}

// 更新收支趋势图表
const updateTrendChart = () => {
  if (!trendChart.value) return
  
  const chart = echarts.init(trendChart.value)
  
  // 模拟月度收支数据
  const months = ['1月', '2月', '3月', '4月', '5月', '6月']
  const incomeData = [8000, 8500, 7800, 9200, 8800, 9500]
  const expenseData = [6500, 7200, 6800, 7500, 7100, 7800]
  
  const option = {
    tooltip: {
      trigger: 'axis',
      formatter: function(params: any) {
        let result = params[0].name + '<br/>'
        params.forEach((param: any) => {
          result += param.seriesName + ': ¥' + param.value.toLocaleString() + '<br/>'
        })
        return result
      }
    },
    legend: {
      data: ['收入', '支出'],
      bottom: '5%'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: months,
      axisLabel: {
        fontSize: 11
      }
    },
    yAxis: {
      type: 'value',
      name: '金额(元)',
      nameTextStyle: {
        fontSize: 11
      },
      axisLabel: {
        fontSize: 11,
        formatter: function(value: number) {
          if (value >= 10000) {
            return (value / 10000) + '万'
          }
          return value
        }
      }
    },
    series: [
      {
        name: '收入',
        type: 'line',
        data: incomeData,
        smooth: true,
        symbol: 'circle',
        symbolSize: 6,
        lineStyle: {
          width: 3,
          color: '#52c41a'
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(82, 196, 26, 0.3)' },
              { offset: 1, color: 'rgba(82, 196, 26, 0.1)' }
            ]
          }
        },
        itemStyle: {
          color: '#52c41a'
        }
      },
      {
        name: '支出',
        type: 'line',
        data: expenseData,
        smooth: true,
        symbol: 'circle',
        symbolSize: 6,
        lineStyle: {
          width: 3,
          color: '#f5222d'
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(245, 34, 45, 0.3)' },
              { offset: 1, color: 'rgba(245, 34, 45, 0.1)' }
            ]
          }
        },
        itemStyle: {
          color: '#f5222d'
        }
      }
    ]
  }
  
  chart.setOption(option)
  
  // 响应式处理
  window.addEventListener('resize', () => {
    chart.resize()
  })
}

// 格式化金额
const formatMoney = (amount: number) => {
  return amount.toLocaleString()
}

// 获取活动图标
const getActivityIcon = (action: string) => {
  if (action.includes('新增')) return Plus
  if (action.includes('编辑')) return Edit
  if (action.includes('删除')) return Delete
  if (action.includes('缴费')) return Money
  return Document
}

// 获取活动图标样式类
const getActivityIconClass = (action: string) => {
  if (action.includes('新增')) return 'icon-add'
  if (action.includes('编辑')) return 'icon-edit'
  if (action.includes('删除')) return 'icon-delete'
  if (action.includes('缴费')) return 'icon-payment'
  return 'icon-default'
}

// 格式化日期时间
const formatDateTime = (dateTime: string) => {
  if (!dateTime) return ''
  const date = new Date(dateTime)
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  const hours = Math.floor(diff / (1000 * 60 * 60))
  const minutes = Math.floor(diff / (1000 * 60))
  
  if (days > 0) return `${days}天前`
  if (hours > 0) return `${hours}小时前`
  if (minutes > 0) return `${minutes}分钟前`
  return '刚刚'
}

// 导航方法
const navigateToTransactions = () => {
  router.push({ name: 'transactions' })
}

const navigateToBudget = () => {
  router.push({ name: 'budget' })
}

const navigateToFinance = () => {
  router.push({ name: 'finance' })
}

const navigateToGoals = () => {
  router.push({ name: 'goals' })
}

const navigateToStatistics = () => {
  router.push({ name: 'statistics' })
}

// 重新加载图表
const reloadExpenseChart = () => {
  chartError.value.expense = ''
  chartLoading.value.expense = true
  setTimeout(() => {
    chartLoading.value.expense = false
    updateExpenseChart()
  }, 500)
}

const reloadTrendChart = () => {
  chartError.value.trend = ''
  chartLoading.value.trend = true
  setTimeout(() => {
    chartLoading.value.trend = false
    updateTrendChart()
  }, 500)
}

// 加载数据
const loadData = async () => {
  loading.value = true
  error.value = ''
  try {
    // Only load finance statistics since this is now a personal finance system
    await financeStore.fetchStatistics()
    loading.value = false
  } catch (err) {
    error.value = '加载数据失败，请重试'
    loading.value = false
  }
}

onMounted(async () => {
  await loadData()
  
  // 初始化图表
  setTimeout(() => {
    updateExpenseChart()
    updateTrendChart()
  }, 100)
})
</script>

<style scoped>
.dashboard {
  padding: 24px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 88px);
  height: calc(100vh - 88px);
  overflow-y: auto;
  margin: 0;
}

/* 统计卡片区域 */
.stats-row {
  margin-bottom: 24px;
}

.stat-card {
  border: none;
  border-radius: 12px;
  transition: all 0.3s ease;
  height: 120px;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12) !important;
}

.stat-content {
  display: flex;
  align-items: center;
  height: 100%;
  padding: 0 8px;
}

.stat-icon-wrapper {
  width: 64px;
  height: 64px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  flex-shrink: 0;
}

.stat-icon {
  font-size: 28px;
}

.stat-info {
  flex: 1;
}

.stat-number {
  font-size: 28px;
  font-weight: 700;
  color: #262626;
  margin-bottom: 4px;
  line-height: 1.2;
}

.stat-label {
  font-size: 14px;
  color: #8c8c8c;
  font-weight: 500;
}

/* 图表区域 */
.charts-row {
  margin-bottom: 24px;
}

.chart-card {
  border: none;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.chart-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1) !important;
}

.card-header {
  display: flex;
  align-items: center;
  font-weight: 600;
  font-size: 16px;
  color: #262626;
}

.header-actions {
  display: flex;
  align-items: center;
  margin-left: auto;
}

.chart-container {
  height: 320px;
  padding: 16px 0;
}

/* 最近操作区域 */
.recent-activities-row {
  margin-bottom: 24px;
}

.recent-card {
  border: none;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.recent-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1) !important;
}

.recent-activities {
  padding: 8px 0;
}

.activities-loading {
  text-align: center;
  padding: 60px 0;
  color: #909399;
}

.loading-icon {
  animation: rotate 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.empty-state {
  text-align: center;
  padding: 40px 0;
}

.empty-hint {
  font-size: 12px;
  color: #c0c4cc;
  margin-top: 8px;
}

.activity-action {
  color: #c0c4cc;
  margin-left: 12px;
  transition: all 0.3s ease;
}

.activity-item:hover .activity-action {
  color: #409eff;
  transform: translateX(4px);
}

.activity-list {
  max-height: 400px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  align-items: center;
  padding: 16px;
  border-radius: 8px;
  transition: all 0.3s ease;
  margin-bottom: 8px;
  cursor: pointer;
  position: relative;
}

.activity-item:hover {
  background-color: #fafafa;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.activity-item:active {
  transform: translateY(0);
}

.activity-item:last-child {
  margin-bottom: 0;
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  flex-shrink: 0;
  color: white;
  font-weight: 600;
}

.icon-add {
  background-color: #52c41a;
}

.icon-edit {
  background-color: #1890ff;
}

.icon-delete {
  background-color: #f5222d;
}

.icon-payment {
  background-color: #fa8c16;
}

.icon-default {
  background-color: #722ed1;
}

.activity-content {
  flex: 1;
  min-width: 0;
}

.activity-title {
  font-size: 15px;
  font-weight: 500;
  color: #262626;
  margin-bottom: 4px;
}

.activity-subtitle {
  font-size: 13px;
  color: #595959;
  margin-bottom: 4px;
}

.activity-time {
  font-size: 12px;
  color: #8c8c8c;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .dashboard {
    padding: 16px;
  }
  
  .stat-card {
    height: 100px;
    margin-bottom: 16px;
  }
  
  .stat-icon-wrapper {
    width: 48px;
    height: 48px;
    margin-right: 12px;
  }
  
  .stat-icon {
    font-size: 20px;
  }
  
  .stat-number {
    font-size: 20px;
  }
  
  .stat-label {
    font-size: 12px;
  }
  
  .chart-container {
    height: 280px;
  }
  
  .activity-item {
    padding: 12px;
  }
  
  .activity-icon {
    width: 32px;
    height: 32px;
    margin-right: 12px;
  }
}

@media (max-width: 480px) {
  .dashboard {
    padding: 12px;
  }
  
  .stat-content {
    padding: 0 4px;
  }
  
  .stat-icon-wrapper {
    width: 40px;
    height: 40px;
    margin-right: 8px;
  }
  
  .stat-number {
    font-size: 18px;
  }
  
  .chart-container {
    height: 240px;
  }
}
</style>
