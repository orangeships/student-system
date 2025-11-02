<template>
  <el-container class="layout-container">
    <el-aside width="240px" class="layout-aside">
      <div class="logo">
        <h2>学生管理系统</h2>
      </div>
      <el-menu
        :default-active="$route.path"
        class="layout-menu"
        router
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
        :collapse="false"
        :unique-opened="true"
      >
        <el-menu-item index="/" class="menu-item">
          <el-icon><HomeFilled /></el-icon>
          <span>首页</span>
        </el-menu-item>
        <el-menu-item index="/students" class="menu-item">
          <el-icon><UserFilled /></el-icon>
          <span>学生管理</span>
        </el-menu-item>
        <el-menu-item index="/finance" class="menu-item">
          <el-icon><Money /></el-icon>
          <span>费用管理</span>
        </el-menu-item>
        <el-menu-item index="/statistics" class="menu-item">
          <el-icon><TrendCharts /></el-icon>
          <span>统计报表</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    
    <el-container>
      <el-header class="layout-header">
        <div class="header-content">
          <h1>{{ pageTitle }}</h1>
          <div class="header-actions">
            <el-button type="primary" @click="refreshData">
              <el-icon><Refresh /></el-icon>
              刷新
            </el-button>
          </div>
        </div>
      </el-header>
      
      <el-main class="layout-main">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  HomeFilled,
  UserFilled,
  Money,
  TrendCharts,
  Refresh
} from '@element-plus/icons-vue'

const route = useRoute()

const pageTitle = computed(() => {
  const titles: Record<string, string> = {
    '/': '首页',
    '/students': '学生管理',
    '/finance': '费用管理',
    '/statistics': '统计报表'
  }
  return titles[route.path] || '学生管理系统'
})

const refreshData = () => {
  // 触发数据刷新事件
  window.dispatchEvent(new CustomEvent('refresh-data'))
  ElMessage.success('数据已刷新')
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
  min-width: 1200px;
}

.layout-aside {
  background-color: #304156;
  box-shadow: 2px 0 6px rgba(0, 21, 41, 0.35);
}

.logo {
  padding: 24px 20px;
  text-align: center;
  background-color: #2b3a4b;
  border-bottom: 1px solid #434a50;
}

.logo h2 {
  color: #ffffff;
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  letter-spacing: 0.5px;
}

.layout-menu {
  border-right: none;
  background-color: #304156;
}

.menu-item {
  height: 50px;
  line-height: 50px;
  padding-left: 24px !important;
  border-left: 3px solid transparent;
  transition: all 0.3s ease;
}

.menu-item:hover {
  background-color: #263445 !important;
  border-left-color: #409EFF;
}

.menu-item.is-active {
  background-color: #1890ff !important;
  border-left-color: #1890ff;
}

.layout-header {
  background-color: #ffffff;
  border-bottom: 1px solid #e4e7ed;
  padding: 0 24px;
  height: 64px !important;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
}

.header-content h1 {
  margin: 0;
  font-size: 24px;
  color: #303133;
  font-weight: 600;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.layout-main {
  background-color: #f5f7fa;
  padding: 24px;
  min-height: calc(100vh - 64px);
  overflow-y: auto;
}

/* 响应式布局 */
@media screen and (max-width: 1200px) {
  .layout-container {
    min-width: 992px;
  }
}

@media screen and (max-width: 992px) {
  .layout-container {
    min-width: 768px;
  }
  
  .layout-aside {
    width: 200px !important;
  }
}
</style>