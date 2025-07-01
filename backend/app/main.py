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

from .core.database import SessionLocal, engine
from .core.models import Base, User, Card, Transaction
from .crud import get_user_by_id, get_user_by_tg, create_card

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
async def get_cards(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user_cards = db.query(Card).filter(Card.user_id == current_user.id).all()
    cards_response = [
        {
            "id": c.id,
            "brand": c.brand,
            "last4": c.number.replace(" ", "")[-4:],
            "balance": c.balance,
            "currency": c.currency,
        }
        for c in user_cards
    ]
    return {"cards": cards_response}

@app.get("/api/wallet/{card_id}")
async def get_wallet(
    card_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    card = (
        db.query(Card)
        .filter(Card.id == card_id, Card.user_id == current_user.id)
        .first()
    )
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    card_data = {
        "id": card.id,
        "brand": card.brand,
        "last4": card.number.replace(" ", "")[-4:],
        "balance": card.balance,
        "currency": card.currency,
        "number": card.number,
        "ccv": card.ccv,
    }
    card_transactions = (
        db.query(Transaction).filter(Transaction.card_id == card.id).all()
    )
    tx_data = [
        {
            "id": tx.id,
            "card_id": tx.card_id,
            "icon": tx.icon,
            "title": tx.title,
            "subtitle": tx.subtitle,
            "color": tx.color,
            "amount": tx.amount,
            "currency": tx.currency,
        }
        for tx in card_transactions
    ]
    return {"card": card_data, "transactions": tx_data}


# Serve static files with correct MIME types
# app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")

# === Main entrypoint ===
if __name__ == "__main__":

    # Запускаем FastAPI
    uvicorn.run(app, port=8000)
