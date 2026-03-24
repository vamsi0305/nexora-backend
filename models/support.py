from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class SupportPledgeCreate(BaseModel):
    support_type: Optional[str] = Field(default=None, alias="pledge_type") # 'financial', 'skill', 'mentorship'
    amount: Optional[float] = None
    message: Optional[str] = None
    skills_offered: Optional[list[str]] = []

    model_config = {
        "populate_by_name": True
    }

class SupportPledgeUpdate(BaseModel):
    status: str # 'pending', 'accepted', 'rejected'

class SupportPledgeResponse(BaseModel):
    id: str
    idea_id: str
    user_id: str
    support_type: str
    amount: Optional[float] = None
    message: Optional[str] = None
    skills_offered: Optional[list[str]] = []
    status: str
    created_at: datetime
