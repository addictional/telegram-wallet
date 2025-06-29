// src/pages/Wallet.tsx
import {useState} from 'react'
import { useParams, useNavigate } from 'react-router';
import { useWalletQuery } from '@/hooks/useWalletQuery';
import {CardIcon} from  '@/shared/ui'

export default function Wallet() {
  const navigate = useNavigate();
  const { id } = useParams();             // id берём из URL /wallet/:id
  const cardId = Number(id);

  const [showSensitive, setShowSensitive] = useState(true);

  const toggleSensitive = () => setShowSensitive(v => !v);

  const { data, isLoading, error } = useWalletQuery(cardId);

  const sendData = () => {
    window.Telegram?.WebApp?.sendData?.('👋 Привет из React!');
  };


  if (isLoading) return <div className="p-4 text-center">Загрузка…</div>;
  if (error || !data) return <div className="p-4 text-center text-red-500">Ошибка загрузки</div>;

  return (
    <div className="max-w-sm mx-auto bg-white min-h-screen p-4 rounded-3xl shadow-lg flex flex-col">
      {/* Header */}
      <div className="flex justify-between items-center mb-6">
        <button onClick={() => navigate(-1)} className="text-blue-500 text-xl hover:text-blue-600">&larr;</button>
        <h1 className="text-xl font-semibold">Wallet</h1>
        <button className="text-blue-600 hover:text-blue-700 font-medium">SEND</button>
      </div>

     {/* 💳 Card Block */}
      <div className="bg-white border border-slate-200 rounded-2xl p-4 mb-6 relative">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <CardIcon cardType={data.card.brand} className="w-10 h-10" />
            <div>
              <div className="font-semibold text-lg">{data.card.brand}</div>
              <div className="text-sm opacity-80">
                {showSensitive ? data.card.number : `**** **** **** ${data.card.last4}`}
              </div>
            </div>
          </div>
          <button onClick={toggleSensitive} className="text-white text-sm opacity-70 hover:opacity-100 transition">
            {showSensitive ? '🙈' : '👁️'}
          </button>
        </div>

        <div className="mt-4 text-2xl font-bold text-right">
          {showSensitive ? data.formattedBalance : '****'}
        </div>
      </div>

      {/* Transactions */}
      <h2 className="text-lg font-semibold mb-2">Transactions</h2>
      <div className="space-y-4 grow">
        {data.transactions.map(tx => (
          <div key={tx.id} className="flex items-center justify-between border-b pb-3">
            <div className="flex items-center gap-3">
              <div className="text-2xl">{tx.icon}</div>
              <div>
                <div className="font-medium">{tx.title}</div>
                <div className="text-sm text-gray-500">{tx.subtitle}</div>
              </div>
            </div>
            <div className={`text-lg font-semibold ${tx.color}`}>{tx.formattedAmount}</div>
          </div>
        ))}
      </div>

      {/* Balance Button */}
      <div className="mt-6 mb-6">
        <button
          className="w-full bg-blue-600 text-white py-2 rounded-xl font-semibold hover:bg-blue-700"
          onClick={sendData}
        >
          Balance
        </button>
      </div>
    </div>
  );
}
