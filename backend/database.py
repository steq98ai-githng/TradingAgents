from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, Float, String, DateTime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:password@localhost:5432/postgres")

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

class MNQCandle(Base):
    __tablename__ = "mnq_candles"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    timestamp = Column(DateTime, index=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    interval = Column(String)

async def init_db():
    async with engine.begin() as conn:
        # Create TimescaleDB extension if needed
        # await conn.execute("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;")
        await conn.run_sync(Base.metadata.create_all)
        # Note: For actual TimescaleDB hypertable, we would run:
        # SELECT create_hypertable('mnq_candles', 'timestamp');
