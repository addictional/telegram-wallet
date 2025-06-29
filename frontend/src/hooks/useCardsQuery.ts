import { useQuery } from '@tanstack/react-query';
import { formatNumber } from '@/shared';
import type {CurrencyType} from '@/shared'



export type Card = {
  id: number;
  brand: 'Visa' | 'MasterCard' | 'Mir';
  last4: string;
  balance: number;
  currency: CurrencyType;
  formattedBalance?: string; // добавлено
};

export function useCardsQuery() {
  return useQuery<Card[]>({
    queryKey: ['cards'],
    queryFn: async () => {
      const res = await fetch('/api/cards');
      if (!res.ok) throw new Error('Failed to fetch cards');
      const data = await res.json();
      return data.cards.map((card: Card) => ({
        ...card,
        formattedBalance: formatNumber(card.balance, card.currency),
      }));
    },
  });
}