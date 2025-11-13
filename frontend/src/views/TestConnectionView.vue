<template>
  <div class="test-container">
    <h1>API连接测试</h1>
    
    <div class="test-section">
      <h3>1. 基础连接测试</h3>
      <el-button @click="testBasicConnection" type="primary">测试基础连接</el-button>
      <div v-if="basicTestResult" class="result" :class="{ success: basicTestResult.success, error: !basicTestResult.success }">
        {{ basicTestResult.message }}
      </div>
    </div>

    <div class="test-section">
      <h3>2. 用户登录测试</h3>
      <el-button @click="testLogin" type="success">测试用户登录</el-button>
      <div v-if="loginTestResult" class="result" :class="{ success: loginTestResult.success, error: !loginTestResult.success }">
        {{ loginTestResult.message }}
      </div>
    </div>

    <div class="test-section">
      <h3>3. 测试结果汇总</h3>
      <div class="summary">
        <p>后端服务: {{ backendStatus }}</p>
        <p>前端服务: {{ frontendStatus }}</p>
        <p>CORS配置: {{ corsStatus }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { authAPI } from '@/api'

const basicTestResult = ref<{success: boolean, message: string} | null>(null)
const loginTestResult = ref<{success: boolean, message: string} | null>(null)

const backendStatus = ref('检测中...')
const frontendStatus = ref('运行中')
const corsStatus = ref('检测中...')

const testBasicConnection = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/auth/login/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: 'testuser',
        password: 'test123456'
      })
    })
    
    if (response.ok) {
      basicTestResult.value = {
        success: true,
        message: '✅ 基础连接成功！后端服务响应正常'
      }
      backendStatus.value = '运行中'
      corsStatus.value = '配置正确'
    } else {
      basicTestResult.value = {
        success: false,
        message: `❌ 基础连接失败！状态码: ${response.status}`
      }
      backendStatus.value = '可能未运行'
    }
  } catch (error: any) {
    basicTestResult.value = {
      success: false,
      message: `❌ 连接错误: ${error?.message || '网络错误'}`
    }
    backendStatus.value = '未运行或不可访问'
    corsStatus.value = '可能配置错误'
  }
}

const testLogin = async () => {
  try {
    const result = await authAPI.login({
      username: 'testuser',
      password: 'test123456'
    })
    
    console.log('登录测试结果:', result)
    
    // 检查登录结果 - authAPI.login 返回的是 axios 响应
    if (result.data?.data?.token) {
      loginTestResult.value = {
        success: true,
        message: '✅ 登录测试成功！用户认证正常'
      }
    } else {
      loginTestResult.value = {
        success: false,
        message: `❌ 登录测试失败！未获取到token。响应数据: ${JSON.stringify(result.data)}`
      }
    }
  } catch (error: any) {
    console.error('登录测试错误:', error)
    loginTestResult.value = {
      success: false,
      message: `❌ 登录错误: ${error.response?.data?.message || error?.message || '未知错误'}`
    }
  }
}

// 页面加载时自动测试
setTimeout(() => {
  testBasicConnection()
}, 1000)
</script>

<style scoped>
.test-container {
  max-width: 800px;
  margin: 50px auto;
  padding: 30px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.test-section {
  margin-bottom: 30px;
  padding: 20px;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
}

.test-section h3 {
  margin-top: 0;
  color: #303133;
}

.result {
  margin-top: 15px;
  padding: 10px;
  border-radius: 4px;
  font-weight: bold;
}

.result.success {
  background-color: #f0f9ff;
  color: #67c23a;
  border: 1px solid #b3e19d;
}

.result.error {
  background-color: #fef0f0;
  color: #f56c6c;
  border: 1px solid #fab6b6;
}

.summary {
  background-color: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
}

.summary p {
  margin: 8px 0;
  font-weight: bold;
}
</style>