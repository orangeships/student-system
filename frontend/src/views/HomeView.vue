<template>
  <Layout>
    <div class="dashboard">
      <!-- 统计卡片区域 -->
      <el-row :gutter="24" class="stats-row">
        <el-col :span="6" :xs="24" :sm="12" :md="6">
          <el-card class="stat-card" shadow="hover">
            <div class="stat-content">
              <div class="stat-icon-wrapper" style="background-color: #e6f7ff;">
                <el-icon class="stat-icon" style="color: #1890ff; font-size: 24px;"><UserFilled /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-number">{{ statistics?.total_students || 0 }}</div>
                <div class="stat-label">总学生数</div>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6" :xs="24" :sm="12" :md="6">
          <el-card class="stat-card" shadow="hover">
            <div class="stat-content">
              <div class="stat-icon-wrapper" style="background-color: #f6ffed;">
                <el-icon class="stat-icon" style="color: #52c41a; font-size: 24px;"><User /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-number">{{ statistics?.active_students || 0 }}</div>
                <div class="stat-label">在读学生</div>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6" :xs="24" :sm="12" :md="6">
          <el-card class="stat-card" shadow="hover">
            <div class="stat-content">
              <div class="stat-icon-wrapper" style="background-color: #fff7e6;">
                <el-icon class="stat-icon" style="color: #fa8c16; font-size: 24px;"><Money /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-number">¥{{ formatMoney(paymentStats?.total_amount || 0) }}</div>
                <div class="stat-label">总缴费金额</div>
              </div>
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6" :xs="24" :sm="12" :md="6">
          <el-card class="stat-card" shadow="hover">
            <div class="stat-content">
              <div class="stat-icon-wrapper" style="background-color: #fff1f0;">
                <el-icon class="stat-icon" style="color: #f5222d; font-size: 24px;"><Document /></el-icon>
              </div>
              <div class="stat-info">
                <div class="stat-number">{{ paymentStats?.total_payments || 0 }}</div>
                <div class="stat-label">缴费记录</div>
              </div>
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
              </div>
            </template>
            <div ref="genderChart" class="chart-container"></div>
          </el-card>
        </el-col>
        
        <el-col :span="12" :xs="24" :sm="24" :md="12">
          <el-card class="chart-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <el-icon style="color: #52c41a; margin-right: 8px;"><TrendCharts /></el-icon>
                <span>每月缴费趋势</span>
              </div>
            </template>
            <div ref="paymentChart" class="chart-container"></div>
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
                <el-tag size="small" type="info" style="margin-left: auto;">最近5条</el-tag>
              </div>
            </template>
            <div class="recent-activities">
              <div v-if="recentActivities.length === 0" class="empty-state">
                <el-empty description="暂无操作记录" :image-size="64" />
              </div>
              <div v-else class="activity-list">
                <div 
                  v-for="activity in recentActivities" 
                  :key="activity.id"
                  class="activity-item"
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
                </div>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </Layout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import Layout from '@/components/Layout.vue'
import { useStudentStore } from '@/stores/student'
import { useFinanceStore } from '@/stores/finance'
import * as echarts from 'echarts'
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
  Delete
} from '@element-plus/icons-vue'

const studentStore = useStudentStore()
const financeStore = useFinanceStore()

const statistics = computed(() => studentStore.statistics)
const paymentStats = computed(() => financeStore.statistics)

// 图表引用
const genderChart = ref<HTMLElement>()
const paymentChart = ref<HTMLElement>()

// 模拟最近活动数据
const recentActivities = ref([
  {
    id: 1,
    action: '新增学生',
    student_name: '张三',
    created_at: new Date(Date.now() - 1000 * 60 * 30).toISOString()
  },
  {
    id: 2,
    action: '缴费登记',
    student_name: '李四',
    created_at: new Date(Date.now() - 1000 * 60 * 60).toISOString()
  },
  {
    id: 3,
    action: '编辑学生信息',
    student_name: '王五',
    created_at: new Date(Date.now() - 1000 * 60 * 90).toISOString()
  }
])

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
  // 由于没有性别统计数据，使用模拟数据
  const data = [
    { gender: '男', count: Math.floor((statistics.value?.total_students || 0) * 0.6) },
    { gender: '女', count: Math.floor((statistics.value?.total_students || 0) * 0.4) }
  ]
  
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
        data: data.map(item => ({
          value: item.count,
          name: item.gender === 'M' ? '男' : '女'
        }))
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

onMounted(async () => {
  await studentStore.fetchStatistics()
  await financeStore.fetchStatistics()
})
</script>

<style scoped>
.dashboard {
  padding: 24px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 120px);
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

.empty-state {
  text-align: center;
  padding: 40px 0;
}

.activity-list {
  max-height: 400px;
  overflow-y: auto;
}

.activity-item {
  display: flex;
  align-items: flex-start;
  padding: 16px;
  border-radius: 8px;
  transition: background-color 0.2s ease;
  margin-bottom: 8px;
}

.activity-item:hover {
  background-color: #fafafa;
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
