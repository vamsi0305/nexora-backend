from fastapi import APIRouter, Depends, HTTPException
from utils.auth import get_current_user
from services.supabase import admin_supabase

router = APIRouter()

def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

@router.get("/reports")
def get_reports(admin_user: dict = Depends(require_admin)):
    res = admin_supabase.table("reports").select("*").order("created_at", desc=True).execute()
    return res.data

@router.put("/users/{user_id}/ban")
def ban_user(user_id: str, admin_user: dict = Depends(require_admin)):
    # Simple hard ban logic or changing role/status
    res = admin_supabase.table("users").update({"role": "banned"}).eq("id", user_id).execute()
    return {"message": f"User {user_id} banned"}

@router.delete("/ideas/{idea_id}")
def delete_idea_admin(idea_id: str, admin_user: dict = Depends(require_admin)):
    admin_supabase.table("ideas").delete().eq("id", idea_id).execute()
    return {"message": f"Idea {idea_id} deleted"}

@router.get("/stats")
def get_stats(admin_user: dict = Depends(require_admin)):
    users = admin_supabase.table("users").select("id", count="exact").execute()
    ideas = admin_supabase.table("ideas").select("id", count="exact").execute()
    reports = admin_supabase.table("reports").select("id, status", count="exact").execute()
    pending_reports = sum(1 for report in reports.data if report.get("status") == "pending")
    return {
        "total_users": users.count if hasattr(users, 'count') else len(users.data),
        "total_ideas": ideas.count if hasattr(ideas, 'count') else len(ideas.data),
        "total_reports": reports.count if hasattr(reports, 'count') else len(reports.data),
        "pending_reports": pending_reports,
    }
