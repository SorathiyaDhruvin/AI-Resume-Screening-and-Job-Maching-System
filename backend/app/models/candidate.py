from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.connection import Base

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    location = Column(String)
    linkedin = Column(String)
    github = Column(String)
    portfolio = Column(String)

    user = relationship("User")
    skills = relationship("CandidateSkill", back_populates="candidate")
    education = relationship("Education", back_populates="candidate")
    experience = relationship("Experience", back_populates="candidate")
    projects = relationship("Project", back_populates="candidate")

class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    category = Column(String)

class CandidateSkill(Base):
    __tablename__ = "candidate_skills"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    skill_id = Column(Integer, ForeignKey("skills.id"))
    confidence = Column(Float, default=1.0)

    candidate = relationship("Candidate", back_populates="skills")
    skill = relationship("Skill")

class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    degree = Column(String)
    institution = Column(String)
    graduation_year = Column(Integer)
    score = Column(String)

    candidate = relationship("Candidate", back_populates="education")

class Experience(Base):
    __tablename__ = "experience"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    company = Column(String)
    role = Column(String)
    start_date = Column(String)
    end_date = Column(String)
    description = Column(String)

    candidate = relationship("Candidate", back_populates="experience")

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    candidate_id = Column(Integer, ForeignKey("candidates.id"))
    name = Column(String)
    description = Column(String)
    technologies = Column(String)

    candidate = relationship("Candidate", back_populates="projects")
