import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import init_db

shared_resources = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Application starting up...")
    print("Initializing database...")
    await init_db()
    yield
    print("Application shutting down...")
    shared_resources.clear() 

app = FastAPI(lifespan=lifespan)

@app.get("/up")
def read_root():
    return "online"

if __name__ == "__main__":
    uvicorn.run(app)