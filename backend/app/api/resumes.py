from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.api.dependencies import get_current_user
from app.models.user import User
from app.models.candidate import Candidate, CandidateSkill, Skill
from app.models.resume import Resume
from app.services.resume_parser import ResumeParser
from app.services.skill_extractor import SkillExtractor
import os
import uuid

router = APIRouter(prefix="/resumes", tags=["resumes"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "candidate":
        raise HTTPException(status_code=403, detail="Only candidates can upload resumes")

    if not file.filename.endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Only PDF or DOCX files are allowed")

    file_bytes = await file.read()
    
    # Save file
    unique_filename = f"{uuid.uuid4()}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, unique_filename)
    with open(file_path, "wb") as f:
        f.write(file_bytes)

    # Parse text
    if file.filename.endswith('.pdf'):
        text = ResumeParser.extract_text_from_pdf(file_bytes)
    else:
        text = ResumeParser.extract_text_from_docx(file_bytes)
    
    clean_text = ResumeParser.clean_text(text)
    
    if not clean_text:
        raise HTTPException(status_code=400, detail="Unable to extract text from the uploaded resume.")

    # Get or create Candidate
    candidate = db.query(Candidate).filter(Candidate.user_id == current_user.id).first()
    if not candidate:
        candidate = Candidate(
            user_id=current_user.id,
            name=current_user.name,
            email=ResumeParser.extract_email(clean_text) or current_user.email,
            phone=ResumeParser.extract_phone(clean_text)
        )
        db.add(candidate)
        db.commit()
        db.refresh(candidate)

    # Save Resume
    resume = Resume(
        candidate_id=candidate.id,
        filename=file.filename,
        file_path=file_path,
        extracted_text=clean_text,
        processing_status="completed"
    )
    db.add(resume)
    
    # Extract Skills
    extracted_skills = SkillExtractor.extract_skills(clean_text)
    
    # Add skills to candidate
    for skill_name in extracted_skills:
        skill = db.query(Skill).filter(Skill.name == skill_name).first()
        if not skill:
            skill = Skill(name=skill_name, category="General")
            db.add(skill)
            db.commit()
            db.refresh(skill)
            
        existing_candidate_skill = db.query(CandidateSkill).filter(
            CandidateSkill.candidate_id == candidate.id,
            CandidateSkill.skill_id == skill.id
        ).first()
        
        if not existing_candidate_skill:
            db.add(CandidateSkill(candidate_id=candidate.id, skill_id=skill.id))
            
    db.commit()

    return {"success": True, "message": "Resume uploaded and processed successfully", "resume_id": resume.id}
