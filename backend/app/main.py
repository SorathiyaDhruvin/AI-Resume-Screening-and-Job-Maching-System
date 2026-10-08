from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, resumes, jobs, matching
from app.database.connection import engine, Base
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Resume Screening API")

@app.on_event("startup")
def startup_event():
    logger.info("Starting FastAPI application...")
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database configuration loaded.")
    except Exception as e:
        logger.error(f"Failed to connect to the database: {e}")
    logger.info("FastAPI application ready.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(resumes.router, prefix="/api")
app.include_router(jobs.router, prefix="/api")
app.include_router(matching.router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def root():
    return {"message": "AI Resume Screening API is running"}
