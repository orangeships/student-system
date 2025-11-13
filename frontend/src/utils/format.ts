/**
 * 格式化工具函数
 */

/**
 * 格式化日期
 */
export const formatDate = (date: string | Date): string => {
  if (!date) return ''
  const d = new Date(date)
  return d.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

/**
 * 格式化日期时间
 */
export const formatDateTime = (date: string | Date): string => {
  if (!date) return ''
  const d = new Date(date)
  return d.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

/**
 * 格式化货币
 */
export const formatMoney = (amount: number | string): string => {
  const num = typeof amount === 'string' ? parseFloat(amount) : amount
  if (isNaN(num)) return '¥0.00'
  return num.toLocaleString('zh-CN', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  })
}

/**
 * 格式化货币（带符号）
 */
export const formatCurrency = (amount: number | string, type: 'income' | 'expense'): string => {
  const num = typeof amount === 'string' ? parseFloat(amount) : amount
  const sign = type === 'income' ? '+' : '-'
  return `${sign}¥${formatMoney(Math.abs(num))}`
}

/**
 * 格式化百分比
 */
export const formatPercentage = (value: number | string): string => {
  const num = typeof value === 'string' ? parseFloat(value) : value
  if (isNaN(num)) return '0.0%'
  return `${num.toFixed(1)}%`
}

/**
 * 格式化月份
 */
export const formatMonth = (dateString: string): string => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long' })
}

/**
 * 获取支付方式类型
 */
export const getPaymentMethodType = (method: string): string => {
  const types: Record<string, string> = {
    'cash': 'info',
    'card': 'primary',
    'alipay': 'success',
    'wechat': 'warning',
    'bank': 'primary'
  }
  return types[method] || 'info'
}

/**
 * 获取支付方式名称
 */
export const getPaymentMethodName = (method: string): string => {
  const names: Record<string, string> = {
    'cash': '现金',
    'card': '银行卡',
    'alipay': '支付宝',
    'wechat': '微信支付',
    'bank': '银行转账'
  }
  return names[method] || method
}