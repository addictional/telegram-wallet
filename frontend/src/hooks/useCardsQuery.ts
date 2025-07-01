import { useQuery } from "@tanstack/react-query";
import { formatNumber } from "@/shared";
import type { CurrencyType } from "@/shared";
import { authFetch } from "@/shared/utils/authFetch";

export type Card = {
  id: number;
  brand: "Visa" | "MasterCard" | "Mir";
  last4: string;
  balance: number;
  currency: CurrencyType;
  formattedBalance?: string; // добавлено
};

export function useCardsQuery() {
  return useQuery<Card[]>({
    queryKey: ["cards"],
    queryFn: async () => {
      const res = await authFetch<{ cards: Card[] }>("/api/cards");
      return res.cards.map((card: Card) => ({
        ...card,
        formattedBalance: formatNumber(card.balance, card.currency),
      }));
    },
  });
}
