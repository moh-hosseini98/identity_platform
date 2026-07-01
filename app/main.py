from contextlib import asynccontextmanager
from fastapi import APIRouter, FastAPI
from app.routes.todo import router as todo_router
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

v1_router = APIRouter(prefix="/api/v1")

v1_router.include_router(todo_router, prefix="/todo")

app.include_router(v1_router)



@app.get("/health", tags=["Health"])
async def health():
    return {"status": "ok (test for ci cd in production)"}