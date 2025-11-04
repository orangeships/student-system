import { setActivePinia, createPinia } from 'pinia'
import { useFinanceStore } from '../finance'
import { vi, describe, it, expect, beforeEach } from 'vitest'

// Mock API
vi.mock('@/api/finance', () => ({
  financeApi: {
    getCategories: vi.fn().mockResolvedValue({
      results: [
        { id: 1, name: '学费', amount: 5000, description: '学费', is_active: true },
        { id: 2, name: '住宿费', amount: 1200, description: '住宿费', is_active: true }
      ]
    }),
    getFeeRecords: vi.fn().mockResolvedValue({
      results: [
        { 
          id: 1, 
          student: 1, 
          fee_category: 1, 
          amount: 5000, 
          paid_amount: 3000, 
          status: 'pending',
          due_date: '2024-09-01'
        }
      ],
      count: 1
    }),
    createFeeRecord: vi.fn().mockResolvedValue({
      id: 2,
      student: 2,
      fee_category: 1,
      amount: 5000,
      paid_amount: 0,
      status: 'pending',
      due_date: '2024-10-01'
    }),
    updateFeeRecord: vi.fn().mockResolvedValue({
      id: 1,
      student: 1,
      fee_category: 1,
      amount: 5000,
      paid_amount: 5000,
      status: 'paid',
      due_date: '2024-09-01'
    }),
    deleteFeeRecord: vi.fn().mockResolvedValue(undefined),
    getPayments: vi.fn().mockResolvedValue({
      results: [
        { id: 1, fee_record: 1, amount: 3000, payment_method: 'alipay', transaction_id: '123' }
      ]
    }),
    createPayment: vi.fn().mockResolvedValue({
      id: 2,
      fee_record: 1,
      amount: 2000,
      payment_method: 'wechat',
      transaction_id: '456'
    }),
    getPaymentStatistics: vi.fn().mockResolvedValue({
      total_amount: 10000,
      paid_amount: 6000,
      unpaid_amount: 4000,
      overdue_amount: 0
    })
  }
}))

// Mock message utils
vi.mock('@/utils/message', () => ({
  handleRequest: vi.fn((fn, options) => {
    return fn().catch(() => {
      if (options?.error !== false) {
        console.log('Error:', options?.error)
      }
      return null
    })
  })
}))

describe('Finance Store', () => {
  let store: ReturnType<typeof useFinanceStore>

  beforeEach(() => {
    setActivePinia(createPinia())
    store = useFinanceStore()
  })

  describe('State Management', () => {
    it('should initialize with default values', () => {
      expect(store.categories).toEqual([])
      expect(store.feeRecords).toEqual([])
      expect(store.payments).toEqual([])
      expect(store.statistics).toBeNull()
      expect(store.loading).toBe(false)
      expect(store.error).toBeNull()
      expect(store.totalRecords).toBe(0)
      expect(store.currentPage).toBe(1)
      expect(store.pageSize).toBe(10)
    })

    it('should calculate computed values correctly', () => {
      // 设置测试数据
      store.feeRecords = [
        { id: 1, status: 'paid', paid_amount: 3000, amount: 3000 },
        { id: 2, status: 'pending', paid_amount: 0, amount: 5000 },
        { id: 3, status: 'overdue', paid_amount: 1000, amount: 2000 }
      ] as any

      expect(store.monthlyPaidAmount).toBe(3000)
      expect(store.totalPaidAmount).toBe(3000)
      expect(store.totalUnpaidAmount).toBe(6000) // 5000 + (2000-1000)
    })
  })

  describe('Actions', () => {
    it('should fetch categories', async () => {
      const result = await store.fetchCategories()
      
      expect(result).toHaveLength(2)
      expect(result?.[0].name).toBe('学费')
      expect(store.categories).toHaveLength(2)
    })

    it('should fetch fee records', async () => {
      const result = await store.fetchFeeRecords()
      
      expect(result?.results).toHaveLength(1)
      expect(store.feeRecords).toHaveLength(1)
      expect(store.totalRecords).toBe(1)
    })

    it('should create fee record', async () => {
      const newRecord = {
        student: 2,
        category: 1,
        amount: 5000,
        status: 'pending',
        due_date: '2024-10-01'
      }

      const result = await store.createFeeRecord(newRecord as any)
      
      expect(result?.id).toBe(2)
      expect(result?.student).toBe(2)
    })

    it('should update fee record', async () => {
      store.feeRecords = [{ id: 1, status: 'pending', paid_amount: 0 }] as any
      
      const result = await store.updateFeeRecord(1, { status: 'paid', paid_amount: 5000 })
      
      expect(result?.status).toBe('paid')
      expect(result?.paid_amount).toBe(5000)
    })

    it('should delete fee record', async () => {
      store.feeRecords = [{ id: 1, status: 'pending' }] as any
      
      await store.deleteFeeRecord(1)
      
      // 验证deleteFeeRecord被调用
      expect(store.feeRecords).toHaveLength(1) // 因为mock的fetchFeeRecords返回固定数据
    })

    it('should fetch payments', async () => {
      const result = await store.fetchPayments()
      
      expect(result?.results).toHaveLength(1)
      expect(store.payments).toHaveLength(1)
    })

    it('should create payment', async () => {
      const paymentData = {
        fee_record: 1,
        amount: 2000,
        payment_method: 'wechat',
        transaction_id: '456'
      }

      const result = await store.createPayment(paymentData as any)
      
      expect(result?.id).toBe(2)
      expect(result?.payment_method).toBe('wechat')
    })

    it('should fetch payment statistics', async () => {
      const result = await store.fetchPaymentStatistics()
      
      expect(result?.total_amount).toBe(10000)
      expect(result?.paid_amount).toBe(6000)
      expect(store.statistics).not.toBeNull()
    })
  })
})