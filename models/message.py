from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MessageCreate(BaseModel):
    content: str
    receiver_id: Optional[str] = None

class MessageResponse(BaseModel):
    id: str
    sender_id: str
    receiver_id: str
    idea_id: str
    content: str
    is_read: bool = False
    created_at: datetime
