from datetime import datetime, timedelta
from pathlib import Path
import json
import os
from typing import Optional

from fastapi import (
    FastAPI,
    HTTPException,
    status,
    Depends,
    Body,
)
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
import uvicorn

from urllib.parse import parse_qsl
import hashlib
import hmac

from .database import SessionLocal, engine
from .models import Base, User

app = FastAPI()

SECRET_KEY = "CHANGE_ME"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

revoked_tokens: set[str] = set()

Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_init_data(init_data: str) -> Optional[dict]:
    if not BOT_TOKEN:
        return None
    parsed = dict(parse_qsl(init_data, strict_parsing=True))
    hash_value = parsed.pop("hash", None)
    data_check_string = "\n".join(f"{k}={v}" for k, v in sorted(parsed.items()))

    secret_key = hmac.new("WebAppData".encode(), BOT_TOKEN.encode(), hashlib.sha256).digest()
    h = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256)
    if(h.hexdigest() != hash_value):
        print(f"not equal", flush=True)
        print(f"not equal!! - Computed hash: {h.hexdigest()}, Expected hash: {hash_value}", flush=True)
        return None
    return parsed


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_tg(db: Session, telegram_id: int) -> Optional[User]:
    return db.query(User).filter(User.telegram_id == telegram_id).first()


def create_access_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if token in revoked_tokens:
        raise credentials_exception
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_id(db, int(user_id))
    if user is None:
        raise credentials_exception
    return user




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


# Serve index.html for root
# @app.get("/")
# async def index():
#     return FileResponse(STATIC_DIR / "index.html")


@app.post("/api/login")
async def login(
    init_data: str = Body(..., embed=True),
    db: Session = Depends(get_db),
):
    data_raw = init_data
    print(f"Received init_data: {data_raw}", flush=True)
    if not data_raw:
        raise HTTPException(status_code=400, detail="init_data required")
    parsed = verify_init_data(data_raw)
    print(f"Parsed init_data 1: {parsed}", flush=True)
    if not parsed or "user" not in parsed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid init data")
    user_info = json.loads(parsed["user"])
    tg_id = int(user_info["id"])
    username = user_info.get("username")
    user = get_user_by_tg(db, tg_id)
    if not user:
        user = User(telegram_id=tg_id, username=username)
        db.add(user)
        db.commit()
        db.refresh(user)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/api/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    revoked_tokens.add(token)
    return {"detail": "Logged out"}


@app.get("/api/cards")
async def get_cards(current_user: User = Depends(get_current_user)):
    return {"cards": cards}

@app.get("/api/wallet/{card_id}")
async def get_wallet(card_id: int, current_user: User = Depends(get_current_user)):
    card = next((c for c in cards if c["id"] == card_id), None)
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    card_transactions = [t for t in transactions if t["card_id"] == card_id]
    return {"card": card, "transactions": card_transactions}


# Serve static files with correct MIME types
# app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

# === Main entrypoint ===
if __name__ == "__main__":

    # Запускаем FastAPI
    uvicorn.run(app, port=8000)
