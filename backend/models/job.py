from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from db.databases import base

## StoryJob represents status of a story being made (LLM will take time to acctually make the story)
class StoryJob(base):
    __tablename__ = "story_job"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, index= True, unique= True)
    session_id = Column(String, index=True)
    theme = Column(String)
    status = Column(String)
    story_id = Column(Integer, nullable=True)
    error = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)             ## Job could fail to complete
