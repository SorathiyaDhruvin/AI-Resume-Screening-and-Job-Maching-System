from pydantic import BaseModel
from typing import List, Optional, Any
from datetime import datetime
from app.schemas.candidate import CandidateResponse
from app.schemas.job import JobResponse

class MatchResultResponse(BaseModel):
    id: int
    candidate_id: int
    job_id: int
    semantic_score: float
    skill_score: float
    experience_score: float
    education_score: float
    preferred_skill_score: float
    final_score: float
    matched_skills: Any # Can be list of strings
    missing_skills: Any # Can be list of strings
    created_at: datetime

    candidate: Optional[CandidateResponse] = None
    job: Optional[JobResponse] = None

    class Config:
        from_attributes = True

class MatchExplanation(BaseModel):
    final_score: float
    semantic_score: float
    skill_score: float
    experience_score: float
    education_score: float
    matched_skills: List[str]
    missing_skills: List[str]
