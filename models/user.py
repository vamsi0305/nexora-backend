from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    city: Optional[str] = None
    college: Optional[str] = None
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    language: Optional[str] = "en"
    preferences: Optional[dict] = {}

class UserCreate(UserBase):
    firebase_uid: str
    phone: str
    pass

class UserUpdate(UserBase):
    pass

class UserResponse(UserBase):
    id: str
    created_at: datetime
    role: str = "user"
    followers_count: int = 0
    following_count: int = 0
    trust_score: float = 0.0

class UserLanguageUpdate(BaseModel):
    language: str

class UserPreferencesUpdate(BaseModel):
    preferences: dict

class BlockUserRequest(BaseModel):
    reason: Optional[str] = None
