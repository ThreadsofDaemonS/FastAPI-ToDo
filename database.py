from decouple import config
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from models import Base  # ✅ Используем Base из models.py

DATABASE_URL = config('DATABASE_URL')

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_local = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

async def get_db():
    async with async_session_local() as session:
        yield session