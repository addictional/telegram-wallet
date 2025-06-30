from sqlalchemy import Column, Integer, BigInteger, String
from .database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    username = Column(String(100))
