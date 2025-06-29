import { useNavigate } from 'react-router';
import { useCardsQuery } from '@/hooks/useCardsQuery';
import {CardIcon} from '@/shared/ui'

export default function Cards() {
  const navigate = useNavigate();
  const { data: cards, isLoading, error } = useCardsQuery();

  if (isLoading) return <div className="text-center p-4">Загрузка...</div>;
  if (error) return <div className="text-center text-red-500">Ошибка при загрузке карт</div>;

  return (
    <div className="max-w-sm mx-auto bg-white min-h-screen p-4 rounded-3xl shadow-lg">
      {/* header */}
      <div className="flex items-center justify-between mb-6">
        <button onClick={() => navigate(-1)} className="text-blue-600 text-xl">&larr;</button>
        <h1 className="text-xl font-semibold">Card&nbsp;Selection</h1>
        <button className="text-blue-600 font-semibold">SEND</button>
      </div>

      {/* cards list */}
      <div className="space-y-4">
        {cards?.map(card => (
          <button
            key={card.id}
            onClick={() => {
              navigate(`/wallet/${card.id}`);
            }}
            className="w-full flex justify-between items-center p-4 rounded-2xl border border-slate-200 hover:shadow transition"
          >
            <div className="flex items-center gap-4">
              <CardIcon cardType={card.brand} className='w-14 h-10 shrink-0'/>
              <div className="text-left">
                <div className="font-medium">{card.brand}</div>
                <div className="text-sm text-slate-500">**** **** {card.last4}</div>
              </div>
            </div>

            <span className="text-lg font-semibold">
              {card.formattedBalance}
            </span>
          </button>
        ))}
      </div>
    </div>
  );
}