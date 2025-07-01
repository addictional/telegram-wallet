from typing import Optional
from sqlalchemy.orm import Session
from app.core.models import User, Card, Transaction


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_tg(db: Session, telegram_id: int) -> Optional[User]:
    return db.query(User).filter(User.telegram_id == telegram_id).first()


def create_card(
    db: Session,
    user: User,
    brand: str,
    number: str,
    ccv: str,
    balance: int = 0,
    currency: str = "USD",
) -> Card:
    card = Card(
        user_id=user.id,
        brand=brand,
        number=number,
        ccv=ccv,
        balance=balance,
        currency=currency,
    )
    db.add(card)
    db.commit()
    db.refresh(card)
    return card

