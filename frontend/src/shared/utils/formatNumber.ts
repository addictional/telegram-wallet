import type {CurrencyType} from '@/shared/types'
export function formatNumber(value: number,currency: CurrencyType) {
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: currency,
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(value)
}