from fastapi import APIRouter, Depends
from utils.auth import get_current_user
from services.supabase import supabase

router = APIRouter()

@router.get("/")
def get_notifications(current_user: dict = Depends(get_current_user)):
    res = supabase.table("notifications").select("*").eq("user_id", current_user["id"]).order("created_at", desc=True).execute()
    return res.data

@router.put("/read")
def mark_all_read(current_user: dict = Depends(get_current_user)):
    res = supabase.table("notifications").update({"is_read": True}).eq("user_id", current_user["id"]).execute()
    return {"message": "All marked as read"}

@router.put("/{notif_id}/read")
def mark_read(notif_id: str, current_user: dict = Depends(get_current_user)):
    res = supabase.table("notifications").update({"is_read": True}).eq("id", notif_id).eq("user_id", current_user["id"]).execute()
    return res.data[0] if res.data else {"message": "Not found"}
