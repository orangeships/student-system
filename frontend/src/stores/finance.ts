import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { FeeCategory, FeeRecord, Payment, PaymentStatistics, FeeRecordQuery } from '@/api/finance'
import { financeApi } from '@/api/finance'
import { handleRequest } from '@/utils/message'

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
    return handleRequest(
      async () => {
        loading.value = true
        error.value = null
        const response = await financeApi.getCategories()
        categories.value = response.results
        return response.results
      },
      {
        error: '获取费用类别失败',
        finally: () => {
          loading.value = false
        }
      }
    )
  }

  // 获取缴费记录
  const fetchFeeRecords = async (params?: FeeRecordQuery) => {
    return handleRequest(
      async () => {
        loading.value = true
        error.value = null
        const response = await financeApi.getFeeRecords({
          page: currentPage.value,
          page_size: pageSize.value,
          ...params
        })
        feeRecords.value = response.results
        totalRecords.value = response.count
        return response
      },
      {
        error: '获取缴费记录失败',
        finally: () => {
          loading.value = false
        }
      }
    )
  }

  // 创建缴费记录
  const createFeeRecord = async (recordData: Omit<FeeRecord, 'id'>) => {
    return handleRequest(
      async () => {
        loading.value = true
        error.value = null
        const newRecord = await financeApi.createFeeRecord(recordData)
        await fetchFeeRecords()
        return newRecord
      },
      {
        success: '缴费记录创建成功',
        error: '创建缴费记录失败',
        finally: () => {
          loading.value = false
        }
      }
    )
  }

  // 创建支付记录
  const createPayment = async (paymentData: Omit<Payment, 'id'>) => {
    return handleRequest(
      async () => {
        loading.value = true
        error.value = null
        const newPayment = await financeApi.createPayment(paymentData)
        return newPayment
      },
      {
        success: '支付记录创建成功',
        error: '创建支付记录失败',
        finally: () => {
          loading.value = false
        }
      }
    )
  }

  // 获取支付统计
  const fetchPaymentStatistics = async (params?: any) => {
    return handleRequest(
      async () => {
        loading.value = true
        error.value = null
        const response = await financeApi.getPaymentStatistics(params)
        statistics.value = response.data
        return response
      },
      {
        error: '获取支付统计失败',
        finally: () => {
          loading.value = false
        }
      }
    )
  }

  // 更新缴费记录
  const updateFeeRecord = async (id: number, recordData: Partial<FeeRecord>) => {
    return handleRequest(
      async () => {
        loading.value = true
        error.value = null
        const response = await financeApi.updateFeeRecord(id, recordData)
        const updatedRecord = response.data
        const index = feeRecords.value.findIndex(r => r.id === id)
        if (index !== -1) {
          feeRecords.value[index] = updatedRecord
        }
        return response
      },
      {
        success: '缴费记录更新成功',
        error: '更新缴费记录失败',
        finally: () => {
          loading.value = false
        }
      }
    )
  }

  // 删除缴费记录
  const deleteFeeRecord = async (id: number) => {
    return handleRequest(
      async () => {
        loading.value = true
        error.value = null
        await financeApi.deleteFeeRecord(id)
        await fetchFeeRecords()
      },
      {
        success: '缴费记录删除成功',
        error: '删除缴费记录失败',
        finally: () => {
          loading.value = false
        }
      }
    )
  }



  // 获取支付记录
  const fetchPayments = async () => {
    return handleRequest(
      async () => {
        loading.value = true
        error.value = null
        const response = await financeApi.getPayments()
        payments.value = response.results || response
        return response
      },
      {
        error: '获取支付记录失败',
        finally: () => {
          loading.value = false
        }
      }
    )
  }

  // 获取统计信息
  const fetchStatistics = async () => {
    return handleRequest(
      async () => {
        loading.value = true
        error.value = null
        const stats = await financeApi.getPaymentStatistics() as unknown as PaymentStatistics
        statistics.value = stats
        return stats
      },
      {
        error: '获取统计信息失败',
        finally: () => {
          loading.value = false
        }
      }
    )
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
    createPayment,
    updateFeeRecord,
    deleteFeeRecord,
    fetchPaymentStatistics,
    fetchPayments,
    fetchStatistics,
    setPage,
    setPageSize
  }
})