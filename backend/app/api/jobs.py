from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.api.dependencies import get_current_user, get_current_recruiter
from app.models.user import User
from app.models.job import Job, JobSkill
from app.models.candidate import Skill
from app.schemas.job import JobCreate, JobResponse

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.post("", response_model=JobResponse)
def create_job(
    job_in: JobCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_recruiter)
):
    job = Job(
        recruiter_id=current_user.id,
        title=job_in.title,
        company=job_in.company,
        location=job_in.location,
        experience_min=job_in.experience_min,
        experience_max=job_in.experience_max,
        salary=job_in.salary,
        description=job_in.description
    )
    db.add(job)
    db.commit()
    db.refresh(job)

    # Add required skills
    for skill_name in job_in.required_skills:
        skill_name_lower = skill_name.lower()
        skill = db.query(Skill).filter(Skill.name == skill_name_lower).first()
        if not skill:
            skill = Skill(name=skill_name_lower, category="Required")
            db.add(skill)
            db.commit()
            db.refresh(skill)
        db.add(JobSkill(job_id=job.id, skill_id=skill.id, required=True))

    db.commit()
    return job

@router.get("", response_model=list[JobResponse])
def list_jobs(db: Session = Depends(get_db)):
    return db.query(Job).all()

@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
