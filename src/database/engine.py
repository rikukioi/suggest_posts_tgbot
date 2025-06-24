from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


engine = create_engine("sqlite:///./bot.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def get_db() -> AsyncSession[Any, Any, Any]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
