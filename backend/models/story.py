from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func 
from sqlalchemy.orm import relationship
from db.databases import base

## Contains metadata about the overall story
class Story(base):
    __tablename__ = "stories"
    id = Column(Integer, primary_key=True, index= True)
    title = Column(String, index=True)
    session_id = Column(String, index= True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    nodes = relationship("StoryNode", back_populates="story")  ## one to many relationship (one story connected to many nodes)


## Nodes contains all the different options and paths for story
class StoryNode(base):
    __tablename__ = "story_nodes"

    id = Column(Integer, primary_key=True, index=True)
    story_id = Column(Integer, ForeignKey("stories.id"), index=True)
    content = Column(String)
    is_root = Column(Boolean, default=False)
    is_ending = Column(Boolean, default=False)
    is_winning_ending = Column(Boolean, default=False)
    options = Column(JSON, default=list)

    story = relationship("Story", back_populates= "nodes")

