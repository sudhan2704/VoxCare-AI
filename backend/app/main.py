
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.database import Base, engine
from app.models.call import Call
from app.models.analysis import CallAnalysis
from app.routers.calls import router as calls_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description="AI-powered Voice Process Quality and Productivity Assistant",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
def home():
    return {
        "project": "VoxCare AI",
        "message": "Backend is running successfully!",
        "status": "success"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


app.include_router(calls_router)
