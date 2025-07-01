import { useQuery } from "@tanstack/react-query";
import { formatNumber, authFetch } from "@/shared";
import type { CurrencyType } from "@/shared";

export type Card = {
  id: number;
  brand: "Visa" | "MasterCard" | "Mir"; // или string, если не ограничено
  last4: string;
  number: string; // полный номер карты
  ccv: string; // код безопасности
  balance: number;
  currency: CurrencyType;
};

export type Transaction = {
  id: number;
  card_id: number;
  icon: string;
  title: string;
  subtitle: string;
  color: string; // например: text-green-600 / text-red-500
  amount: number;
  currency: CurrencyType;
};

export type WalletResponse = {
  card: Card;
  transactions: Transaction[];
};

export function useWalletQuery(cardId: number) {
  return useQuery({
    queryKey: ["wallet", cardId],
    queryFn: async () => {
      const data = await authFetch<WalletResponse>(`/api/wallet/${cardId}`);

      return {
        ...data,
        formattedBalance: formatNumber(data.card.balance, data.card.currency),
        transactions: data.transactions.map((tx) => ({
          ...tx,
          formattedAmount: formatNumber(tx.amount, tx.currency),
        })),
      };
    },
    enabled: !!cardId,
  });
}
