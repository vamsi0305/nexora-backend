from pydantic import BaseModel
from typing import Optional, Union
from datetime import datetime

class VoteCreate(BaseModel):
    vote_type: Optional[str] = None # 'upvote' or 'downvote'
    value: Optional[Union[int, str]] = None

class VoteResponse(BaseModel):
    id: str
    idea_id: str
    user_id: str
    vote_type: str
    created_at: datetime
