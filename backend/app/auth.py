import os
import json
import hmac
import hashlib
from urllib.parse import parse_qsl
from sqlalchemy.orm import Session
from .db.models import User
from .db.database import SessionLocal


def authenticate_webapp_user(init_data: str, db: Session | None = None) -> User:
    """Verify Telegram WebApp init data and upsert the user."""
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise EnvironmentError("BOT_TOKEN is required")

    data = dict(parse_qsl(init_data, keep_blank_values=True))
    received_hash = data.pop("hash", None)
    check_string = "\n".join(f"{k}={v}" for k, v in sorted(data.items()))
    secret_key = hashlib.sha256(token.encode()).digest()
    calculated_hash = hmac.new(secret_key, check_string.encode(), hashlib.sha256).hexdigest()
    if calculated_hash != received_hash:
        raise ValueError("Invalid init data")

    user_json = data.get("user")
    if not user_json:
        raise ValueError("User data missing")
    user_data = json.loads(user_json)
    telegram_id = user_data.get("id")

    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True
    try:
        user = db.query(User).filter_by(telegram_id=telegram_id).first()
        if user is None:
            user = User(
                telegram_id=telegram_id,
                first_name=user_data.get("first_name"),
                last_name=user_data.get("last_name"),
                username=user_data.get("username"),
            )
            db.add(user)
        else:
            user.first_name = user_data.get("first_name")
            user.last_name = user_data.get("last_name")
            user.username = user_data.get("username")
        db.commit()
        db.refresh(user)
    finally:
        if close_db:
            db.close()
    return user
