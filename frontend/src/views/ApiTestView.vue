<template>
  <div class="api-test">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>API 集成测试</span>
          <el-button type="primary" @click="runAllTests">运行所有测试</el-button>
        </div>
      </template>

      <div class="test-results">
        <el-table :data="testResults" style="width: 100%">
          <el-table-column prop="name" label="测试项目" width="200" />
          <el-table-column prop="status" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="getStatusType(row.status)">
                {{ row.status }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="message" label="消息" />
          <el-table-column prop="response" label="响应" width="100">
            <template #default="{ row }">
              <el-button 
                v-if="row.response" 
                type="text" 
                @click="showResponse(row)"
              >
                查看
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>

    <!-- 响应详情对话框 -->
    <el-dialog v-model="dialogVisible" title="API 响应详情" width="60%">
      <pre class="response-content">{{ currentResponse }}</pre>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'
import { formatDateTime } from '@/utils/format'

interface TestResult {
  name: string
  status: 'pending' | 'success' | 'failed'
  message: string
  response?: any
}

const authStore = useAuthStore()
const testResults = ref<TestResult[]>([])
const dialogVisible = ref(false)
const currentResponse = ref('')

const getStatusType = (status: string) => {
  switch (status) {
    case 'success': return 'success'
    case 'failed': return 'danger'
    default: return 'info'
  }
}

const showResponse = (row: TestResult) => {
  currentResponse.value = JSON.stringify(row.response, null, 2)
  dialogVisible.value = true
}

const addTestResult = (name: string, status: TestResult['status'], message: string, response?: any) => {
  testResults.value.push({
    name,
    status,
    message,
    response
  })
}

const testAuth = async () => {
  addTestResult('用户认证', 'pending', '正在测试用户认证...')
  
  try {
    if (!authStore.token) {
      addTestResult('用户认证', 'failed', '用户未登录')
      return false
    }
    
    const response = await fetch('http://localhost:8000/api/auth/user/', {
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
        'Content-Type': 'application/json'
      }
    })
    
    if (response.ok) {
      const data = await response.json()
      addTestResult('用户认证', 'success', '用户认证成功', data)
      return true
    } else {
      addTestResult('用户认证', 'failed', `认证失败: ${response.status}`)
      return false
    }
  } catch (error) {
    addTestResult('用户认证', 'failed', `认证错误: ${error}`)
    return false
  }
}

const testTransactions = async () => {
  addTestResult('交易数据', 'pending', '正在测试交易数据API...')
  
  try {
    const response = await fetch('http://localhost:8000/api/transactions/transactions/', {
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
        'Content-Type': 'application/json'
      }
    })
    
    if (response.ok) {
      const data = await response.json()
      addTestResult('交易数据', 'success', `获取到 ${data.results?.length || 0} 条交易记录`, data)
      return true
    } else {
      addTestResult('交易数据', 'failed', `获取交易数据失败: ${response.status}`)
      return false
    }
  } catch (error) {
    addTestResult('交易数据', 'failed', `获取交易数据错误: ${error}`)
    return false
  }
}

const testCategories = async () => {
  addTestResult('分类数据', 'pending', '正在测试分类数据API...')
  
  try {
    const response = await fetch('http://localhost:8000/api/transactions/categories/', {
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
        'Content-Type': 'application/json'
      }
    })
    
    if (response.ok) {
      const data = await response.json()
      addTestResult('分类数据', 'success', `获取到 ${data.results?.length || 0} 个分类`, data)
      return true
    } else {
      addTestResult('分类数据', 'failed', `获取分类数据失败: ${response.status}`)
      return false
    }
  } catch (error) {
    addTestResult('分类数据', 'failed', `获取分类数据错误: ${error}`)
    return false
  }
}

const testBudgets = async () => {
  addTestResult('预算数据', 'pending', '正在测试预算数据API...')
  
  try {
    const response = await fetch('http://localhost:8000/api/transactions/budgets/', {
      headers: {
        'Authorization': `Bearer ${authStore.token}`,
        'Content-Type': 'application/json'
      }
    })
    
    if (response.ok) {
      const data = await response.json()
      addTestResult('预算数据', 'success', `获取到 ${data.results?.length || 0} 个预算`, data)
      return true
    } else {
      addTestResult('预算数据', 'failed', `获取预算数据失败: ${response.status}`)
      return false
    }
  } catch (error) {
    addTestResult('预算数据', 'failed', `获取预算数据错误: ${error}`)
    return false
  }
}

const runAllTests = async () => {
  testResults.value = []
  
  // 按顺序运行测试
  const authSuccess = await testAuth()
  if (authSuccess) {
    await testTransactions()
    await testCategories()
    await testBudgets()
  }
  
  // 统计结果
  const successCount = testResults.value.filter(r => r.status === 'success').length
  const failedCount = testResults.value.filter(r => r.status === 'failed').length
  
  ElMessage({
    message: `测试完成: 成功 ${successCount} 个, 失败 ${failedCount} 个`,
    type: failedCount === 0 ? 'success' : 'warning'
  })
}

onMounted(() => {
  runAllTests()
})
</script>

<style scoped>
.api-test {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.test-results {
  margin-top: 20px;
}

.response-content {
  background-color: #f5f7fa;
  padding: 15px;
  border-radius: 4px;
  font-family: 'Courier New', monospace;
  font-size: 12px;
  max-height: 400px;
  overflow-y: auto;
  white-space: pre-wrap;
  word-break: break-all;
}
</style>