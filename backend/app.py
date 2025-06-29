from flask import Flask, send_from_directory,jsonify
import os

app = Flask(__name__,static_folder='../frontend/dist',static_url_path='/')

# 🔗 Транзакции связаны с картами по полю card_id
transactions = [
    {"id": 1, "card_id": 1, "icon": "⬇️", "title": "Funding", "color": "text-green-600",
     "subtitle": "Bank Transfer", "amount": 90000, "currency": 'RUB'},

    {"id": 2, "card_id": 1, "icon": "🎮", "title": "Steam", "color": "text-red-500",
     "subtitle": "Payment", "amount": -50, "currency": 'USD'},

    {"id": 3, "card_id": 1, "icon": "🎁", "title": "Gift received", "color": "text-green-600",
     "subtitle": "From Dad", "amount": 30000, "currency": "RUB"},

    {"id": 4, "card_id": 2, "icon": "📦", "title": "AliExpress", "color": "text-red-500",
     "subtitle": "Order #456", "amount": -130, "currency": "USD"},
]

# Пример: список карт
cards = [
    {
        "id": 1,
        "brand": "Visa",
        "last4": "1234",
        "balance": 1200,
        "currency": "USD",
        "number": "4111 1111 1111 1234",
        "ccv": "123"
    },
    {
        "id": 2,
        "brand": "MasterCard",
        "last4": "5678",
        "balance": 1500,
        "currency": "USD",
        "number": "5500 0000 0000 5678",
        "ccv": "456"
    },
    {
        "id": 3,
        "brand": "Visa",
        "last4": "9012",
        "balance": 900,
        "currency": "USD",
        "number": "4111 1111 1111 9012",
        "ccv": "789"
    }
]

@app.route('/') # type: ignore
def serve():
  if(app.static_folder != None):
    return send_from_directory(app.static_folder,'index.html')
  
@app.route("/api/cards", methods=["GET"])
def get_cards():
    return jsonify({"cards": cards})

# ✅ GET /api/wallet/<card_id>
@app.route("/api/wallet/<int:card_id>", methods=["GET"])
def get_wallet(card_id):
    card = next((c for c in cards if c["id"] == card_id), None)
    if not card:
        return jsonify({"error": "Card not found"}), 404

    card_transactions = [t for t in transactions if t["card_id"] == card_id]

    return jsonify({
        "card": card,  # теперь возвращаем всю карту
        "transactions": card_transactions
    })

  
@app.route('/<path:path>')   # type: ignore
def static_proxy(path):
  if(app.static_folder != None):
    return send_from_directory(app.static_folder,path)
  
if __name__ == '__main__':
    app.run(port=8000)  