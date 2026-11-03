from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.utils.config import settings
from typing import Generator

engine = create_engine(
    settings.DATABASE_URL,
    pool_size = 10,
    max_overflow = 20,
    pool_pre_ping = True
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()

def get_db() -> Generator:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()