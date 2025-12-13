import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import init_db
from utils import logger

from api.v1.router import router

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger.info("Application starting up...")

    logger.info("Initializing database...")
    await init_db()

    yield

    logger.info("Application shutting down...")

app = FastAPI(lifespan=lifespan)

app.include_router(router)

@app.get("/status")
def read_root():
    return "online"

if __name__ == "__main__":
    uvicorn.run(app)