from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, resumes, jobs, matching
from app.database.connection import engine, Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Resume Screening API")

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

@app.get("/")
def root():
    return {"message": "AI Resume Screening API is running"}
