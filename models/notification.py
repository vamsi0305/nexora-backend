from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class NotificationResponse(BaseModel):
    id: str
    user_id: str
    type: str
    message: str
    reference_id: Optional[str] = None
    meta_data: Optional[Dict[str, Any]] = None
    is_read: bool
    created_at: datetime
