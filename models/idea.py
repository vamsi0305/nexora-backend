from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class IdeaBase(BaseModel):
    title: str
    description: str
    domain: str
    city: Optional[str] = None
    college: Optional[str] = None
    tags: Optional[List[str]] = []
    required_skills: Optional[List[str]] = []
    goal_amount: Optional[float] = 0.0
    status: Optional[str] = "open" # open, in_progress, completed, archived

class IdeaCreate(IdeaBase):
    pass

class IdeaUpdate(IdeaBase):
    title: Optional[str] = None
    description: Optional[str] = None
    domain: Optional[str] = None

class IdeaResponse(IdeaBase):
    id: str
    user_id: str
    created_at: datetime
    views_count: int = 0
    upvotes_count: int = 0
    downvotes_count: int = 0
    pledged_amount: float = 0.0

class IdeaProgressCreate(BaseModel):
    title: str
    description: str
    update_type: str = "general" # general, milestone, pivot
    images: Optional[List[str]] = []
