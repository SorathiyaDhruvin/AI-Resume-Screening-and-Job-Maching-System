from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ResumeBase(BaseModel):
    filename: str
    processing_status: str

class ResumeResponse(ResumeBase):
    id: int
    candidate_id: int
    uploaded_at: datetime
    
    class Config:
        from_attributes = True
