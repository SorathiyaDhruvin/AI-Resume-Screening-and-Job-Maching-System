from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    recruiter_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    company = Column(String)
    location = Column(String)
    experience_min = Column(Integer, default=0)
    experience_max = Column(Integer, default=0)
    salary = Column(String)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    recruiter = relationship("User")
    skills = relationship("JobSkill", back_populates="job")


class JobSkill(Base):
    __tablename__ = "job_skills"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))
    required = Column(Boolean, default=True)
    importance = Column(Integer, default=1) # e.g. 1-5 scale

    job = relationship("Job", back_populates="skills")
    skill = relationship("Skill")
