from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CommentCreate(BaseModel):
    content: str
    parent_id: Optional[str] = None

class CommentResponse(BaseModel):
    id: str
    idea_id: str
    user_id: str
    content: str
    parent_id: Optional[str] = None
    created_at: datetime
