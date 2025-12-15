from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError('DATABASE_URL environment variable is not set:\n   Set it up in .env file.\n DATABASE_URL="sqlite+aiosqlite:///./test.db"')

engine = create_async_engine(DATABASE_URL, echo=False)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def enable_foreign_keys():
    async with engine.connect() as conn:
        await conn.execute(text("PRAGMA foreign_keys = ON"))
        await conn.commit()

# async def get_session():
#     session = AsyncSessionLocal()
#     try:
#         await enable_foreign_keys()  
#         yield session
#     finally:
#         await session.close()

async def get_session() -> AsyncSession:
    await enable_foreign_keys()
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
