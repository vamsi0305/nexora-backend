from fastapi import APIRouter, Query
from services.supabase import supabase

router = APIRouter()

@router.get("/")
def search(
    q: str = Query(..., min_length=2),
    type: str = Query("all"),
):
    results = {}
    
    # Search ideas
    if type in ["all", "ideas"]:
        ideas_res = supabase.table("ideas").select("*, users(name, avatar_url)").or_(
            f"title.ilike.%{q}%,description.ilike.%{q}%,domain.ilike.%{q}%"
        ).order("created_at", desc=True).limit(10).execute()
        results["ideas"] = ideas_res.data
        
    # Search users
    if type in ["all", "users"]:
        users_res = supabase.table("users").select(
            "id, name, avatar_url, college, city, trust_score"
        ).or_(f"name.ilike.%{q}%,college.ilike.%{q}%,city.ilike.%{q}%").limit(10).execute()
        results["users"] = users_res.data
        
    return results
