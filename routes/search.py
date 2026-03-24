from fastapi import APIRouter, Depends, Query
from utils.auth import get_current_user
from services.supabase import supabase

router = APIRouter()

@router.get("/")
def search(q: str = Query(..., min_length=2), type: str = Query("all")):
    results = {}
    
    # Search ideas
    if type in ["all", "ideas"]:
        ideas_res = supabase.table("ideas").select("*").ilike("title", f"%{q}%").execute()
        results["ideas"] = ideas_res.data
        
    # Search users
    if type in ["all", "users"]:
        users_res = supabase.table("users").select("id, name, avatar_url, college").ilike("name", f"%{q}%").execute()
        results["users"] = users_res.data
        
    return results
