import uuid
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Cookie, Response, BackgroundTasks, status
from sqlalchemy.orm import Session

from backend.db.databases import get_db, SessionLocal
from backend.models.story import Story, StoryNode
from backend.models.job import StoryJob
from backend.schemas.story import CompleteStoryNodeResponse, CompleteStoryResponse, CreateStoryRequest
from backend.schemas.jobs import StoryJobResponse, StoryJobCreate

router = APIRouter(
    prefix="/stories"
    tags=["stories"]
)

def get_session_id(session_id: Optional[str] = Cookie(None)):
    if session_id is None:
        session_id = str(uuid.uuid4())
    return session_id

@router.post("/create", response_model=StoryJobResponse)
def create_story(
    request: CreateStoryRequest, 
    background_tasks: BackgroundTasks, 
    response: Response, 
    session_id: str = Depends(get_session_id), 
    db: Session = Depends(get_db)
    ):
    response.set_cookie(key="session_id", value=session_id, httponly=True)

    job_id = str(uuid.uuid4())

    job = StoryJob(
        job_id= job_id,
        session_id= session_id,
        theme= request.theme,
        status= "pending"
    )
    db.add(job)
    db.commit()

    ## Runs on seperate thread
    background_tasks.add_task(
        generate_story_task,
        job_id= job_id,
        theme= request.theme,
        session_id= session_id
    )

    return job

def generate_story_task(job_id: str, theme: str, session_id: str):

    ## need new db instance to allow for asynchronous jobs
    db = SessionLocal()

    try:
        job = db.query(StoryJob).filter(StoryJob.job_id == job_id).first()

        if not job:
            return 
        
        try:
            job.status = "processing"
            db.commit()

            story = {}
            job.story_id = 1 ## TODO: update story id
            job.status = "completed"
            job.completed_at = datetime.now()
            db.commit()
        except Exception as e:
            job.status = "failed"
            job.completed_at = datetime.now()
            job.error = str(e)
            db.commit()
    finally:
        db.close()

@router.get("/{story_id}/complete", response_model=CompleteStoryResponse)
def get_complete_story(story_id: int, db: Session = Depends(get_db)):
    story = db.query(Story).filter(Story.id == story_id).first()

    if not story:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found")
    
    ## TODO: parse story
    return story

def build_complete_story_tree(db: Session, story: Story):
    pass