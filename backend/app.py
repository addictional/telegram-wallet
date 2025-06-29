from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import uvicorn

app = FastAPI()

# Transaction data linked to cards by card_id
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

# Example cards list
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


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR  / "frontend" / "dist"

# Serve index.html for root
@app.get("/")
async def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/cards")
async def get_cards():
    return {"cards": cards}

@app.get("/api/wallet/{card_id}")
async def get_wallet(card_id: int):
    card = next((c for c in cards if c["id"] == card_id), None)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    card_transactions = [t for t in transactions if t["card_id"] == card_id]
    return {"card": card, "transactions": card_transactions}

# Serve static files with correct MIME types
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
