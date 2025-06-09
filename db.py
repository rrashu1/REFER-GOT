from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()
engine = create_engine(os.getenv("DATABASE_URL", "sqlite:///data.db"))
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    ref_code = Column(String)
    referred_by = Column(Integer, nullable=True)
    balance_usdt = Column(Float, default=0.0)
    withdrawn = Column(Float, default=0.0)

def init_db():
    Base.metadata.create_all(engine)

def get_or_create_user(tg_id):
    user = session.query(User).filter_by(telegram_id=tg_id).first()
    if not user:
        user = User(telegram_id=tg_id, ref_code=f"ref{tg_id}")
        session.add(user)
        session.commit()
    return user

def get_user(tg_id):
    return session.query(User).filter_by(telegram_id=tg_id).first()

def get_user_by_ref_code(ref_code):
    return session.query(User).filter_by(ref_code=ref_code).first()

def update_balances(user, referrer):
    user.referred_by = referrer.telegram_id
    user.balance_usdt += 0.01
    referrer.balance_usdt += 0.01
    session.commit()
