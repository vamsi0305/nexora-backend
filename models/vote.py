from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class VoteCreate(BaseModel):
    vote_type: str # 'upvote' or 'downvote'

class VoteResponse(BaseModel):
    id: str
    idea_id: str
    user_id: str
    vote_type: str
    created_at: datetime
