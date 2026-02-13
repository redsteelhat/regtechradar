"""FastAPI application — RegTech Radar API."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import init_db
from app.routers import auth, regulations, alerts, admin
from app.scheduler import start_scheduler, stop_scheduler

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(name)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting RegTech Radar API...")
    await init_db()
    start_scheduler()
    yield
    stop_scheduler()
    logger.info("RegTech Radar API shut down.")


app = FastAPI(
    title="RegTech Radar API",
    description="Regulatory change tracking for FinTech compliance teams",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS — allow Next.js dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        settings.APP_URL,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router)
app.include_router(regulations.router)
app.include_router(alerts.router)
app.include_router(admin.router)


@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "RegTech Radar API"}
