from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional, List
from utils.auth import get_current_user
from services.supabase import supabase
from models.idea import IdeaCreate, IdeaUpdate, IdeaProgressCreate
from utils.helpers import paginate

router = APIRouter()

@router.get("/")
def get_ideas(
    domain: Optional[str] = None,
    city: Optional[str] = None,
    college: Optional[str] = None,
    user_id: Optional[str] = None,
    sort: Optional[str] = "recent", # recent, trending, popular
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100)
):
    try:
        query = supabase.table("ideas").select("*, users(name, avatar_url)", count="exact")
        
        if domain:
            query = query.eq("domain", domain)
        if city:
            query = query.eq("city", city)
        if college:
            query = query.eq("college", college)
        if user_id:
            query = query.eq("user_id", user_id)
            
        if sort == "recent":
            query = query.order("created_at", desc=True)
        elif sort == "trending":
            query = query.order("views_count", desc=True).order("upvotes_count", desc=True)
        elif sort == "popular":
            query = query.order("upvotes_count", desc=True)
        else:
            query = query.order("created_at", desc=True)
        
        # Paginate query
        query = paginate(query, page, limit)
        res = query.execute()
        
        return {
            "items": res.data,
            "total": res.count if hasattr(res, 'count') else len(res.data),
            "page": page,
            "limit": limit
        }
    except Exception as e:
        return {"error": str(e), "type": str(type(e))}

@router.post("/")
def create_idea(idea: IdeaCreate, current_user: dict = Depends(get_current_user)):
    data = idea.model_dump()
    data["user_id"] = current_user["id"]
    
    res = supabase.table("ideas").insert(data).execute()
    if not res.data:
        raise HTTPException(status_code=500, detail="Failed to create idea")

    created = supabase.table("ideas").select("*, users(name, avatar_url)").eq("id", res.data[0]["id"]).execute()
    return created.data[0] if created.data else res.data[0]

@router.get("/trending")
def get_trending_ideas():
    # Very simple trending algorithm logic for now (order by views/votes)
    res = supabase.table("ideas").select("*, users(name, avatar_url)").order("views_count", desc=True).limit(10).execute()
    return res.data

@router.get("/{idea_id}")
def get_idea(idea_id: str):
    res = supabase.table("ideas").select("*, users(name, avatar_url, bio)").eq("id", idea_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="Idea not found")
        
    # Increment view count
    val = res.data[0].get("views_count", 0) + 1
    supabase.table("ideas").update({"views_count": val}).eq("id", idea_id).execute()
        
    return res.data[0]

@router.put("/{idea_id}")
def update_idea(idea_id: str, idea_update: IdeaUpdate, current_user: dict = Depends(get_current_user)):
    # Check ownership
    existing = supabase.table("ideas").select("user_id").eq("id", idea_id).execute()
    if not existing.data or existing.data[0]["user_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this idea")
        
    update_data = {k: v for k, v in idea_update.model_dump().items() if v is not None}
    res = supabase.table("ideas").update(update_data).eq("id", idea_id).execute()
    return res.data[0]

@router.delete("/{idea_id}")
def delete_idea(idea_id: str, current_user: dict = Depends(get_current_user)):
    existing = supabase.table("ideas").select("user_id").eq("id", idea_id).execute()
    if not existing.data or existing.data[0]["user_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this idea")
        
    supabase.table("ideas").delete().eq("id", idea_id).execute()
    return {"message": "Idea deleted successfully"}

@router.post("/{idea_id}/progress")
def add_idea_progress(idea_id: str, progress: IdeaProgressCreate, current_user: dict = Depends(get_current_user)):
    existing = supabase.table("ideas").select("user_id").eq("id", idea_id).execute()
    if not existing.data or existing.data[0]["user_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    data = progress.model_dump()
    data["idea_id"] = idea_id
    
    res = supabase.table("idea_progress").insert(data).execute()
    return res.data[0]
