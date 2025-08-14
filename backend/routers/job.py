from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.db.databases import get_db
from backend.models.job import StoryJob
from backend.schemas.jobs import StoryJobResponse

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"]
)

@router.get("/{jobs_id}", response_model=StoryJobResponse)
def get_job_status(jobs_id: str, db: Session = Depends(get_db)):
    job = db.query(StoryJob).filter(StoryJob.id == jobs_id).first()

    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    
    return job