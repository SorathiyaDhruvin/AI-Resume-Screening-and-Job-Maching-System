from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.candidate import SkillBase

class JobSkillBase(BaseModel):
    skill: SkillBase
    required: bool
    importance: int

class JobBase(BaseModel):
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    experience_min: int = 0
    experience_max: int = 0
    salary: Optional[str] = None
    description: str

class JobCreate(JobBase):
    required_skills: List[str] = []
    preferred_skills: List[str] = []

class JobResponse(JobBase):
    id: int
    recruiter_id: int
    created_at: datetime
    skills: List[JobSkillBase] = []

    class Config:
        from_attributes = True
