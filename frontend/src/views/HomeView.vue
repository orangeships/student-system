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
          <el-card class="stat-card" shadow="hover" @click="navigateToStudents">
            <div class="stat-content">
              <div class="stat-icon-wrapper" style="background-color: #e6f7ff;">
                <el-icon class="stat-icon" style="color: #1890ff; font-size: 24px;"><UserFilled /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-number" :class="{ 'skeleton': loading }">{{ statistics?.total_students || 0 }}</div>
                <div class="stat-label">总学生数</div>
              </div>
            </div>
            <div class="stat-footer">
              <span class="stat-trend" v-if="studentTrend !== 0">
                <el-icon :class="{ 'trend-up': studentTrend > 0, 'trend-down': studentTrend < 0 }">
                  <CaretTop v-if="studentTrend > 0" />
                  <CaretBottom v-else />
                </el-icon>
                {{ Math.abs(studentTrend) }}% 较上月
              </span>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6" :xs="24" :sm="12" :md="6">
          <el-card class="stat-card" shadow="hover" @click="filterActiveStudents">
            <div class="stat-content">
              <div class="stat-icon-wrapper" style="background-color: #f6ffed;">
                <el-icon class="stat-icon" style="color: #52c41a; font-size: 24px;"><User /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-number" :class="{ 'skeleton': loading }">{{ statistics?.active_students || 0 }}</div>
                <div class="stat-label">在读学生</div>
              </div>
            </div>
            <div class="stat-footer">
              <span class="stat-trend" v-if="activeStudentTrend !== 0">
                <el-icon :class="{ 'trend-up': activeStudentTrend > 0, 'trend-down': activeStudentTrend < 0 }">
                  <CaretTop v-if="activeStudentTrend > 0" />
                  <CaretBottom v-else />
                </el-icon>
                {{ Math.abs(activeStudentTrend) }}% 较上月
              </span>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6" :xs="24" :sm="12" :md="6">
          <el-card class="stat-card" shadow="hover" @click="navigateToFinance">
            <div class="stat-content">
              <div class="stat-icon-wrapper" style="background-color: #fff7e6;">
                <el-icon class="stat-icon" style="color: #fa8c16; font-size: 24px;"><Money /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-number" :class="{ 'skeleton': loading }">¥{{ formatMoney(paymentStats?.total_amount || 0) }}</div>
                <div class="stat-label">总缴费金额</div>
              </div>
            </div>
            <div class="stat-footer">
              <span class="stat-trend" v-if="paymentTrend !== 0">
                <el-icon :class="{ 'trend-up': paymentTrend > 0, 'trend-down': paymentTrend < 0 }">
                  <CaretTop v-if="paymentTrend > 0" />
                  <CaretBottom v-else />
                </el-icon>
                {{ Math.abs(paymentTrend) }}% 较上月
              </span>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6" :xs="24" :sm="12" :md="6">
          <el-card class="stat-card" shadow="hover" @click="navigateToFinance">
            <div class="stat-content">
              <div class="stat-icon-wrapper" style="background-color: #fff1f0;">
                <el-icon class="stat-icon" style="color: #f5222d; font-size: 24px;"><Document /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-number" :class="{ 'skeleton': loading }">{{ paymentStats?.total_payments || 0 }}</div>
                <div class="stat-label">缴费记录</div>
              </div>
            </div>
            <div class="stat-footer">
              <span class="stat-trend" v-if="recordTrend !== 0">
                <el-icon :class="{ 'trend-up': recordTrend > 0, 'trend-down': recordTrend < 0 }">
                  <CaretTop v-if="recordTrend > 0" />
                  <CaretBottom v-else />
                </el-icon>
                {{ Math.abs(recordTrend) }}% 较上月
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
                <span>学生性别分布</span>
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
              <div v-if="chartLoading.gender" class="chart-loading">
                <el-icon class="loading-icon" size="32"><Loading /></el-icon>
              </div>
              <div v-else-if="chartError.gender" class="chart-error">
                <el-icon size="32" color="#f5222d"><Warning /></el-icon>
                <p>图表加载失败</p>
                <el-button type="primary" link @click="reloadGenderChart">重试</el-button>
              </div>
              <div v-else ref="genderChart" class="chart-container"></div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="12" :xs="24" :sm="24" :md="12">
          <el-card class="chart-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <el-icon style="color: #52c41a; margin-right: 8px;"><TrendCharts /></el-icon>
                <span>每月缴费趋势</span>
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
              <div v-if="chartLoading.payment" class="chart-loading">
                <el-icon class="loading-icon" size="32"><Loading /></el-icon>
              </div>
              <div v-else-if="chartError.payment" class="chart-error">
                <el-icon size="32" color="#f5222d"><Warning /></el-icon>
                <p>图表加载失败</p>
                <el-button type="primary" link @click="reloadPaymentChart">重试</el-button>
              </div>
              <div v-else ref="paymentChart" class="chart-container"></div>
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
                    <p class="empty-hint">当您添加或编辑学生信息时，操作记录将显示在这里</p>
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
                    <div class="activity-subtitle">学生：{{ activity.student_name }}</div>
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
import { useStudentStore } from '@/stores/student'
import { useFinanceStore } from '@/stores/finance'
import * as echarts from 'echarts'
import { showSuccess, showError, showInfo } from '@/utils/message'
import { 
  UserFilled, 
  User, 
  Money, 
  Document, 
  PieChart, 
  TrendCharts, 
  Clock,
  Plus,
  Edit,
  Delete,
  Refresh,
  ArrowRight,
  Loading,
  Warning,
  CaretTop,
  CaretBottom
} from '@element-plus/icons-vue'

const studentStore = useStudentStore()
const financeStore = useFinanceStore()

const statistics = computed(() => studentStore.statistics)
const paymentStats = computed(() => financeStore.statistics)

// 图表引用
const genderChart = ref<HTMLElement>()
const paymentChart = ref<HTMLElement>()

// 状态定义
const studentLoading = ref(false)
const studentError = ref('')
const financeLoading = ref(false)
const financeError = ref('')
const genderChartLoading = ref(false)
const genderChartError = ref('')
const paymentChartLoading = ref(false)
const paymentChartError = ref('')
const activitiesLoading = ref(false)
const loading = ref(false)
const error = ref('')
const router = useRouter()

// 计算属性
const studentTrend = ref(0)
const activeStudentTrend = ref(0)
const paymentTrend = ref(0)
const recordTrend = ref(0)

// 图表加载状态
const chartLoading = ref({
  gender: false,
  payment: false
})

const chartError = ref({
  gender: '',
  payment: ''
})

// 模拟最近活动数据
const recentActivities = ref([
  {
    id: 1,
    action: '添加学生',
    student_name: '张三',
    student_id: '2024001',
    created_at: new Date(Date.now() - 1000 * 60 * 30).toISOString()
  },
  {
    id: 2,
    action: '缴费登记',
    student_name: '李四',
    student_id: '2024002',
    created_at: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString()
  },
  {
    id: 3,
    action: '编辑学生信息',
    student_name: '王五',
    student_id: '2024003',
    created_at: new Date(Date.now() - 1000 * 60 * 60 * 5).toISOString()
  },
  {
    id: 4,
    action: '退费处理',
    student_name: '赵六',
    student_id: '2024004',
    created_at: new Date(Date.now() - 1000 * 60 * 60 * 8).toISOString()
  },
  {
    id: 5,
    action: '添加学生',
    student_name: '钱七',
    student_id: '2024005',
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
  if (activity.action.includes('学生')) {
    router.push({
      name: 'students',
      query: { search: activity.student_name }
    })
  } else if (activity.action.includes('缴费') || activity.action.includes('退费')) {
    router.push({
      name: 'finance',
      query: { student_name: activity.student_name }
    })
  }
  
  showInfo(`正在查看 ${activity.student_name} 的详细信息`)
}

const maxMajorCount = computed(() => {
  if (!statistics.value?.by_major?.length) return 0
  return Math.max(...statistics.value.by_major.map(item => item.count))
})

const maxGradeCount = computed(() => {
  if (!statistics.value?.by_grade?.length) return 0
  return Math.max(...statistics.value.by_grade.map(item => item.count))
})

const getBarWidth = (value: number, max: number) => {
  return max > 0 ? (value / max) * 100 : 0
}

// 更新性别分布图表
const updateGenderChart = () => {
  if (!genderChart.value) return
  
  const chart = echarts.init(genderChart.value)
  
  // 计算性别统计
  let maleCount = 0
  let femaleCount = 0
  
  if (statistics.value?.total_students) {
    // 如果有实际统计数据，使用实际数据
    if (statistics.value.by_gender) {
      const genderStats = statistics.value.by_gender
      maleCount = genderStats.find(item => item.gender === 'M')?.count || 0
      femaleCount = genderStats.find(item => item.gender === 'F')?.count || 0
    } else {
      // 否则使用模拟数据
      maleCount = Math.floor((statistics.value.total_students || 0) * 0.6)
      femaleCount = Math.floor((statistics.value.total_students || 0) * 0.4)
    }
  }
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'horizontal',
      bottom: '5%',
      textStyle: {
        fontSize: 12
      }
    },
    color: ['#1890ff', '#52c41a'],
    series: [
      {
        name: '性别分布',
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
        data: [
          { value: maleCount, name: '男' },
          { value: femaleCount, name: '女' }
        ]
      }
    ]
  }
  
  chart.setOption(option)
  
  // 响应式处理
  window.addEventListener('resize', () => {
    chart.resize()
  })
}

// 更新缴费趋势图表
const updatePaymentChart = () => {
  if (!paymentChart.value || !paymentStats.value?.monthly_stats) return
  
  const chart = echarts.init(paymentChart.value)
  const data = paymentStats.value.monthly_stats
  
  const option = {
    tooltip: {
      trigger: 'axis',
      formatter: function(params: any) {
        const param = params[0]
        return `${param.name}<br/>缴费金额: ¥${param.value.toLocaleString()}`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: data.map((item: any) => item.month.substring(5)), // 只显示月份
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
        name: '缴费金额',
        type: 'line',
        data: data.map((item: any) => item.total_amount),
        smooth: true,
        symbol: 'circle',
        symbolSize: 6,
        lineStyle: {
          width: 3,
          color: '#52c41a'
        },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(82, 196, 26, 0.3)' },
            { offset: 1, color: 'rgba(82, 196, 26, 0.1)' }
          ])
        },
        itemStyle: {
          color: '#52c41a'
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
const navigateToStudents = () => {
  router.push({ name: 'students' })
}

const navigateToFinance = () => {
  router.push({ name: 'finance' })
}

const navigateToStatistics = () => {
  router.push({ name: 'statistics' })
}

const filterActiveStudents = () => {
  router.push({ 
    name: 'students',
    query: { status: 'active' }
  })
}

// 重新加载图表
const reloadGenderChart = () => {
  chartError.gender = ''
  chartLoading.gender = true
  setTimeout(() => {
    chartLoading.gender = false
    updateGenderChart()
  }, 500)
}

const reloadPaymentChart = () => {
  chartError.payment = ''
  chartLoading.payment = true
  setTimeout(() => {
    chartLoading.payment = false
    updatePaymentChart()
  }, 500)
}

// 加载数据
const loadData = async () => {
  loading.value = true
  error.value = ''
  try {
    await studentStore.fetchStatistics()
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
    updateGenderChart()
    updatePaymentChart()
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
