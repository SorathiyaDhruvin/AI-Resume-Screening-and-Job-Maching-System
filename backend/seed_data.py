import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database.connection import SessionLocal, engine, Base
from app.models.user import User
from app.models.candidate import Candidate, Skill
from app.models.job import Job, JobSkill
from app.core.security import get_password_hash

def seed_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Check if we already seeded
    if db.query(User).first():
        print("Database already seeded.")
        return
        
    print("Seeding database...")
    
    # Users
    recruiter = User(name="Admin Recruiter", email="recruiter@example.com", password_hash=get_password_hash("password"), role="recruiter")
    candidate_user = User(name="John Doe", email="candidate@example.com", password_hash=get_password_hash("password"), role="candidate")
    db.add(recruiter)
    db.add(candidate_user)
    db.commit()
    
    # Skills
    skills = [
        "java", "python", "c++", "javascript", "typescript", "react", "spring boot",
        "fastapi", "node.js", "express", "sql", "postgresql", "mongodb", "docker",
        "aws", "machine learning", "nlp", "dsa", "git"
    ]
    db_skills = {}
    for s in skills:
        skill = Skill(name=s, category="General")
        db.add(skill)
        db_skills[s] = skill
    db.commit()
    
    # Jobs
    job1 = Job(
        recruiter_id=recruiter.id,
        title="Software Engineer",
        company="ABC Technologies",
        location="Bangalore",
        experience_min=0,
        experience_max=2,
        description="We are looking for a Software Engineer with strong programming skills in Java and Spring Boot. Good knowledge of SQL and DSA is required. Familiarity with Git is a plus."
    )
    db.add(job1)
    db.commit()
    db.refresh(job1)
    
    job_skills_data = ["java", "spring boot", "sql", "dsa", "git"]
    for s in job_skills_data:
        db.add(JobSkill(job_id=job1.id, skill_id=db_skills[s].id, required=True))
        
    db.commit()
    
    print("Seeding completed.")

if __name__ == "__main__":
    seed_db()
