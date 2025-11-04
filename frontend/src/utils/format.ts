// 日期时间格式化工具

export function formatDate(dateString: string): string {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

export function formatDateTime(dateString: string): string {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

export function formatCurrency(amount: number): string {
  return `¥${amount.toFixed(2)}`
}

export function formatPercentage(value: number): string {
  return `${value.toFixed(1)}%`
}

export function formatMonth(dateString: string): string {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', { year: 'numeric', month: 'long' })
}