from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from utils.auth import get_current_user
from services.supabase import admin_supabase

router = APIRouter()

class ReportCreate(BaseModel):
    item_type: str # idea, comment, user
    item_id: str
    reason: str
    details: Optional[str] = None

@router.post("/")
def create_report(report: ReportCreate, current_user: dict = Depends(get_current_user)):
    data = report.model_dump()
    data["reporter_id"] = current_user["id"]
    data["status"] = "pending"
    
    # Normal user insert
    res = admin_supabase.table("reports").insert(data).execute()
    return res.data[0]
