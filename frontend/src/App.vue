<script setup lang="ts">
import { RouterView } from 'vue-router'
</script>

<template>
  <div id="app">
    <RouterView />
  </div>
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>

<style>
/* 全局样式优化 */
html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}

#app {
  height: 100%;
}

/* Element Plus 样式优化 */
.el-card {
  margin-bottom: 20px;
}

.el-table {
  font-size: 14px;
}

.el-form-item {
  margin-bottom: 18px;
}

/* 表格样式优化 */
.el-table .cell {
  padding: 8px 12px;
  line-height: 1.5;
}

/* 对话框样式优化 */
.el-dialog__body {
  padding: 20px 24px;
}

/* 响应式布局 */
@media screen and (max-width: 768px) {
  .el-col {
    width: 100% !important;
  }
  
  .el-form-item {
    display: block;
    margin-bottom: 15px;
  }
  
  .el-form-item__label {
    display: block;
    text-align: left;
    padding: 0 0 8px 0;
  }
  
  .el-form-item__content {
    display: block;
  }
}

/* 统计卡片样式 */
.stat-card .el-card__body {
  padding: 24px;
}

/* 图表容器样式 */
.chart-container {
  padding: 16px;
  min-height: 300px;
}

/* 搜索表单样式优化 */
.search-form {
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 4px;
  margin-bottom: 20px;
}

.search-form .el-form-item {
  margin-right: 16px;
  margin-bottom: 12px;
}

/* 分页样式优化 */
.pagination-container {
  margin-top: 20px;
  text-align: right;
  padding: 16px 0;
}

/* 按钮间距优化 */
.el-button {
  margin-right: 8px;
  margin-bottom: 8px;
}

.el-button:last-child {
  margin-right: 0;
}

/* 卡片头部样式 */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
}

/* 布局主内容区域样式优化 */
.layout-main {
  padding: 24px;
  background-color: #f5f7fa;
  min-height: calc(100vh - 60px);
}
</style>
