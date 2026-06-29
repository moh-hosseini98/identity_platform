from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.db import engine



@asynccontextmanager
async def lifespan(app: FastAPI):
    
    yield
    await engine.dispose()


app = FastAPI(
    title="Identity Platform API",
    version="1.0.0",
    lifespan=lifespan,
)



@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok"}