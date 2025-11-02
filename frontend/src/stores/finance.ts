import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { FeeCategory, FeeRecord, Payment, PaymentStatistics, FeeRecordQuery } from '@/api/finance'
import { financeApi } from '@/api/finance'

export const useFinanceStore = defineStore('finance', () => {
  const categories = ref<FeeCategory[]>([])
  const feeRecords = ref<FeeRecord[]>([])
  const payments = ref<Payment[]>([])
  const statistics = ref<PaymentStatistics | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  const totalRecords = ref(0)
  const currentPage = ref(1)
  const pageSize = ref(10)
  const monthlyPaidAmount = computed(() => {
    return feeRecords.value
      .filter((record: FeeRecord) => record.status === 'paid')
      .reduce((sum: number, record: FeeRecord) => sum + (record.paid_amount || 0), 0)
  })

  const totalUnpaidAmount = computed(() => {
    return feeRecords.value
      .filter((record: FeeRecord) => record.status === 'pending' || record.status === 'overdue')
      .reduce((sum: number, record: FeeRecord) => sum + (record.amount - (record.paid_amount || 0)), 0)
  })

  const totalPaidAmount = computed(() => {
    return feeRecords.value
      .filter((record: FeeRecord) => record.status === 'paid')
      .reduce((sum: number, record: FeeRecord) => sum + (record.paid_amount || 0), 0)
  })

  // 获取费用类别
  const fetchCategories = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await financeApi.getCategories()
      categories.value = response.results || response
    } catch (err: any) {
      error.value = err.message || '获取费用类别失败'
      console.error('获取费用类别失败:', err)
    } finally {
      loading.value = false
    }
  }

  // 获取缴费记录
  const fetchFeeRecords = async (params?: FeeRecordQuery) => {
    loading.value = true
    error.value = null
    try {
      const response = await financeApi.getFeeRecords({
        page: currentPage.value,
        page_size: pageSize.value,
        ...params
      })
      feeRecords.value = response.results
      totalRecords.value = response.count
    } catch (err: any) {
      error.value = err.message || '获取缴费记录失败'
      console.error('获取缴费记录失败:', err)
    } finally {
      loading.value = false
    }
  }

  // 创建缴费记录
  const createFeeRecord = async (data: FeeRecord) => {
    loading.value = true
    error.value = null
    try {
      const record = await financeApi.createFeeRecord(data)
      await fetchFeeRecords()
      return record
    } catch (err: any) {
      error.value = err.message || '创建缴费记录失败'
      console.error('创建缴费记录失败:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // 更新缴费记录
  const updateFeeRecord = async (id: number, data: FeeRecord) => {
    loading.value = true
    error.value = null
    try {
      const record = await financeApi.updateFeeRecord(id, data)
      await fetchFeeRecords()
      return record
    } catch (err: any) {
      error.value = err.message || '更新缴费记录失败'
      console.error('更新缴费记录失败:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // 删除缴费记录
  const deleteFeeRecord = async (id: number) => {
    loading.value = true
    error.value = null
    try {
      await financeApi.deleteFeeRecord(id)
      await fetchFeeRecords()
    } catch (err: any) {
      error.value = err.message || '删除缴费记录失败'
      console.error('删除缴费记录失败:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // 创建支付记录
  const createPayment = async (data: Payment) => {
    loading.value = true
    error.value = null
    try {
      const payment = await financeApi.createPayment(data)
      await fetchFeeRecords() // 刷新缴费记录状态
      return payment
    } catch (err: any) {
      error.value = err.message || '创建支付记录失败'
      console.error('创建支付记录失败:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // 获取支付记录
  const fetchPayments = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await financeApi.getPayments()
      payments.value = response.results || response
    } catch (err: any) {
      error.value = err.message || '获取支付记录失败'
      console.error('获取支付记录失败:', err)
    } finally {
      loading.value = false
    }
  }

  // 获取统计信息
  const fetchStatistics = async () => {
    loading.value = true
    error.value = null
    try {
      const stats = await financeApi.getPaymentStatistics() as unknown as PaymentStatistics
      statistics.value = stats
      return stats
    } catch (err: any) {
      error.value = err.message || '获取统计信息失败'
      console.error('获取统计信息失败:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  // 分页相关
  const setPage = (page: number) => {
    currentPage.value = page
    fetchFeeRecords()
  }

  const setPageSize = (size: number) => {
    pageSize.value = size
    currentPage.value = 1
    fetchFeeRecords()
  }

  return {
    categories,
    feeRecords,
    payments,
    statistics,
    loading,
    error,
    totalRecords,
    totalCount: totalRecords, // 兼容旧代码
    currentPage,
    pageSize,
    monthlyPaidAmount,
    totalUnpaidAmount,
    totalPaidAmount,
    fetchCategories,
    fetchFeeRecords,
    createFeeRecord,
    updateFeeRecord,
    deleteFeeRecord,
    createPayment,
    fetchPayments,
    fetchStatistics,
    setPage,
    setPageSize,
  }
})