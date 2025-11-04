<template>
  <div class="categories-view">
    <el-card class="categories-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <div class="header-left">
            <el-icon style="color: #1890ff; margin-right: 8px;"><Collection /></el-icon>
            <span class="card-title">分类管理</span>
            <el-tag type="info" size="small" style="margin-left: 12px;">
              共 {{ categoryStore.totalCount }} 个分类
            </el-tag>
          </div>
          <el-button type="primary" @click="showAddDialog = true" :icon="Plus">
            新增分类
          </el-button>
        </div>
      </template>

      <!-- 搜索 -->
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="搜索">
          <el-input
            v-model="searchForm.search"
            placeholder="分类名称"
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
            v-model="searchForm.category_type" 
            placeholder="全部" 
            clearable 
            @change="handleSearch"
            style="width: 120px"
          >
            <el-option label="收入" value="income" />
            <el-option label="支出" value="expense" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleSearch" :loading="categoryStore.loading">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="handleReset">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </el-form-item>
      </el-form>

      <!-- 分类列表 -->
      <div class="table-section">
        <div class="table-toolbar">
          <div class="toolbar-left">
            <el-tag type="info" size="small">
              已选择 {{ selectedCategories.length }} 项
            </el-tag>
            <el-button 
              v-if="selectedCategories.length > 0"
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
              :loading="categoryStore.loading"
              :icon="Refresh"
            >
              刷新
            </el-button>
          </div>
        </div>
        <el-table
          v-loading="categoryStore.loading"
          :data="categoryStore.categories"
          style="width: 100%"
          stripe
          :header-cell-style="{ background: '#fafafa', fontWeight: '600', color: '#262626' }"
          @selection-change="handleSelectionChange"
          :size="density === 'compact' ? 'small' : 'default'"
          row-key="id"
        >
          <el-table-column type="selection" width="55" fixed="left" />
          <el-table-column prop="id" label="ID" width="80" align="center" />
          <el-table-column prop="name" label="分类名称" min-width="150" sortable="custom">
            <template #default="{ row }">
              <div class="category-info">
                <div 
                  class="category-icon" 
                  :style="{ backgroundColor: row.color || '#1890ff' }"
                >
                  <el-icon><component :is="row.icon || 'Collection'" /></el-icon>
                </div>
                <span class="category-name">{{ row.name }}</span>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="category_type" label="类型" width="80" align="center" sortable="custom">
            <template #default="{ row }">
              <el-tag :type="row.category_type === 'income' ? 'success' : 'danger'" size="small">
                {{ row.category_type === 'income' ? '收入' : '支出' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="description" label="描述" min-width="200" show-overflow-tooltip>
            <template #default="{ row }">
              <span class="description-text">{{ row.description || '-' }}</span>
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
          :total="categoryStore.totalCount"
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
      :title="editingCategory ? '编辑分类' : '新增分类'"
      width="500px"
      :close-on-click-modal="false"
    >
      <el-form :model="categoryForm" :rules="rules" ref="categoryFormRef" label-width="80px">
        <el-form-item label="分类名称" prop="name">
          <el-input
            v-model="categoryForm.name"
            placeholder="请输入分类名称"
            maxlength="20"
            show-word-limit
          />
        </el-form-item>
        <el-form-item label="分类类型" prop="category_type">
          <el-radio-group v-model="categoryForm.category_type">
            <el-radio label="income">收入</el-radio>
            <el-radio label="expense">支出</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="图标" prop="icon">
          <el-select v-model="categoryForm.icon" placeholder="选择图标" style="width: 100%">
            <el-option label="默认" value="Collection" />
            <el-option label="食物" value="Food" />
            <el-option label="交通" value="Van" />
            <el-option label="购物" value="ShoppingBag" />
            <el-option label="娱乐" value="VideoPlay" />
            <el-option label="医疗" value="FirstAidKit" />
            <el-option label="教育" value="School" />
            <el-option label="工资" value="Money" />
            <el-option label="投资" value="TrendCharts" />
            <el-option label="其他" value="More" />
          </el-select>
        </el-form-item>
        <el-form-item label="颜色" prop="color">
          <el-color-picker v-model="categoryForm.color" show-alpha />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="categoryForm.description"
            type="textarea"
            :rows="3"
            placeholder="请输入分类描述"
            maxlength="100"
            show-word-limit
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
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useCategoryStore } from '@/stores/category'
import type { Category, CategoryForm } from '@/types/category'
import {
  Collection,
  Plus,
  Search,
  Refresh,
  Delete
} from '@element-plus/icons-vue'

const categoryStore = useCategoryStore()

const searchForm = reactive({
  search: '',
  category_type: ''
})

const pagination = reactive({
  currentPage: 1,
  pageSize: 20
})

const selectedCategories = ref<Category[]>([])
const showAddDialog = ref(false)
const editingCategory = ref<Category | null>(null)
const submitting = ref(false)
const density = ref<'default' | 'compact'>('default')

const categoryFormRef = ref()

const categoryForm = reactive<CategoryForm>({
  name: '',
  category_type: 'expense',
  icon: 'Collection',
  color: '#1890ff',
  description: ''
})

const rules = {
  name: [{ required: true, message: '请输入分类名称', trigger: 'blur' }],
  category_type: [{ required: true, message: '请选择分类类型', trigger: 'change' }]
}

onMounted(async () => {
  await categoryStore.fetchCategories()
})

const handleSearch = () => {
  categoryStore.searchCategories({
    ...searchForm,
    page: pagination.currentPage,
    page_size: pagination.pageSize
  })
}

const handleReset = () => {
  searchForm.search = ''
  searchForm.category_type = ''
  handleSearch()
}

const handleSearchInput = () => {
  // 防抖搜索
  clearTimeout((window as any).searchTimeout)
  ;(window as any).searchTimeout = setTimeout(handleSearch, 500)
}

const handleSelectionChange = (selection: Category[]) => {
  selectedCategories.value = selection
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
  categoryStore.fetchCategories()
  showSuccess('数据已刷新')
}

const handleBatchDelete = async () => {
  if (selectedCategories.value.length === 0) return
  
  await ElMessageBox.confirm(
    `确定要删除选中的 ${selectedCategories.value.length} 个分类吗？`,
    '批量删除确认',
    { type: 'warning' }
  )
  
  try {
    const ids = selectedCategories.value.map(c => c.id)
    await categoryStore.batchDeleteCategories(ids)
    showSuccess('批量删除成功')
    selectedCategories.value = []
  } catch (error) {
    showError('批量删除失败')
  }
}

const handleEdit = (category: Category) => {
  editingCategory.value = category
  Object.assign(categoryForm, {
    name: category.name,
    category_type: category.category_type,
    icon: category.icon || 'Collection',
    color: category.color || '#1890ff',
    description: category.description || ''
  })
  showAddDialog.value = true
}

const handleDelete = async (category: Category) => {
  await ElMessageBox.confirm(
    `确定要删除分类 "${category.name}" 吗？`,
    '删除确认',
    { type: 'warning' }
  )
  
  try {
    await categoryStore.deleteCategory(category.id)
    showSuccess('删除成功')
  } catch (error) {
    showError('删除失败')
  }
}

const handleSubmit = async () => {
  await categoryFormRef.value.validate()
  
  submitting.value = true
  try {
    if (editingCategory.value) {
      await categoryStore.updateCategory(editingCategory.value.id, categoryForm)
      showSuccess('更新成功')
    } else {
      await categoryStore.createCategory(categoryForm)
      showSuccess('新增成功')
    }
    
    showAddDialog.value = false
    resetForm()
  } catch (error) {
    showError('操作失败')
  } finally {
    submitting.value = false
  }
}

const resetForm = () => {
  editingCategory.value = null
  Object.assign(categoryForm, {
    name: '',
    category_type: 'expense',
    icon: 'Collection',
    color: '#1890ff',
    description: ''
  })
}

const formatDateTime = (date: string) => {
  return new Date(date).toLocaleString('zh-CN')
}

const showSuccess = (message: string) => {
  ElMessage.success(message)
}

const showError = (message: string) => {
  ElMessage.error(message)
}

// 监听数据刷新事件
window.addEventListener('refresh-data', handleRefresh)
</script>

<style scoped>
.categories-view {
  padding: 0;
}

.categories-card {
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

.category-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.category-icon {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 16px;
}

.category-name {
  font-weight: 500;
  color: #262626;
}

.description-text {
  color: #595959;
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