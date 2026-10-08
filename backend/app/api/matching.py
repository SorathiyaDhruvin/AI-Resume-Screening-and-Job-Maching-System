from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.api.dependencies import get_current_user, get_current_recruiter
from app.models.user import User
from app.models.job import Job
from app.models.candidate import Candidate
from app.models.resume import Resume
from app.models.match import MatchResult
from app.schemas.match import MatchResultResponse, MatchExplanation
from app.services.embedding_service import EmbeddingService
from app.services.matching_service import MatchingService
import json

router = APIRouter(prefix="/matching", tags=["matching"])

@router.post("/candidate/{candidate_id}/job/{job_id}", response_model=MatchResultResponse)
def run_matching(
    candidate_id: int, 
    job_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_recruiter)
):
    candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
    job = db.query(Job).filter(Job.id == job_id).first()
    
    if not candidate or not job:
        raise HTTPException(status_code=404, detail="Candidate or Job not found")
        
    resume = db.query(Resume).filter(Resume.candidate_id == candidate.id).order_by(Resume.uploaded_at.desc()).first()
    if not resume:
        raise HTTPException(status_code=400, detail="Candidate has no uploaded resume")

    # Semantic similarity
    semantic_score = EmbeddingService.calculate_similarity(resume.extracted_text, job.description)
    
    # Skills
    required_skills = [js.skill.name for js in job.skills if js.required]
    candidate_skills = [cs.skill.name for cs in candidate.skills]
    
    skill_match_result = MatchingService.calculate_skill_match(required_skills, candidate_skills)
    skill_score = skill_match_result["score"]
    
    # Calculate final score (simplified for now)
    final_score = MatchingService.calculate_final_score(
        semantic_score=semantic_score,
        skill_score=skill_score,
        exp_score=1.0, # Placeholder
        edu_score=1.0  # Placeholder
    )
    
    # Save or update result
    match = db.query(MatchResult).filter(MatchResult.candidate_id == candidate_id, MatchResult.job_id == job_id).first()
    if not match:
        match = MatchResult(candidate_id=candidate_id, job_id=job_id)
        db.add(match)
        
    match.semantic_score = float(semantic_score)
    match.skill_score = float(skill_score)
    match.final_score = float(final_score)
    match.matched_skills = json.dumps(skill_match_result["matched"])
    match.missing_skills = json.dumps(skill_match_result["missing"])
    
    db.commit()
    db.refresh(match)
    
    return match

@router.get("/job/{job_id}", response_model=list[MatchResultResponse])
def get_job_matches(
    job_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_recruiter)
):
    matches = db.query(MatchResult).filter(MatchResult.job_id == job_id).order_by(MatchResult.final_score.desc()).all()
    # Decode json strings to lists before returning
    for match in matches:
        match.matched_skills = json.loads(match.matched_skills) if match.matched_skills else []
        match.missing_skills = json.loads(match.missing_skills) if match.missing_skills else []
    return matches

@router.get("/candidate/{candidate_id}", response_model=list[MatchResultResponse])
def get_candidate_matches(
    candidate_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "candidate" and current_user.id != candidate_id:
        # candidates can only view their own matches
        candidate = db.query(Candidate).filter(Candidate.id == candidate_id).first()
        if candidate.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Forbidden")

    matches = db.query(MatchResult).filter(MatchResult.candidate_id == candidate_id).order_by(MatchResult.final_score.desc()).all()
    for match in matches:
        match.matched_skills = json.loads(match.matched_skills) if match.matched_skills else []
        match.missing_skills = json.loads(match.missing_skills) if match.missing_skills else []
    return matches
