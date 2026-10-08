from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SkillBase(BaseModel):
    name: str
    category: Optional[str] = None

class CandidateSkillBase(BaseModel):
    skill: SkillBase
    confidence: float

class EducationBase(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    graduation_year: Optional[int] = None
    score: Optional[str] = None

class ExperienceBase(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    description: Optional[str] = None

class ProjectBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    technologies: Optional[str] = None

class CandidateBase(BaseModel):
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None

class CandidateResponse(CandidateBase):
    id: int
    user_id: int
    skills: List[CandidateSkillBase] = []
    education: List[EducationBase] = []
    experience: List[ExperienceBase] = []
    projects: List[ProjectBase] = []

    class Config:
        from_attributes = True
