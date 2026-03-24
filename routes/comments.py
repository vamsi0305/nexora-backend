from fastapi import APIRouter, Depends, HTTPException
from utils.auth import get_current_user
from services.supabase import supabase
from models.comment import CommentCreate

router = APIRouter()

@router.get("/ideas/{idea_id}/comments")
def get_comments(idea_id: str, current_user: dict = Depends(get_current_user)):
    res = supabase.table("comments").select("*, users(name, avatar_url)").eq("idea_id", idea_id).order("created_at", desc=False).execute()
    return res.data

@router.post("/ideas/{idea_id}/comments")
def create_comment(idea_id: str, comment: CommentCreate, current_user: dict = Depends(get_current_user)):
    data = comment.model_dump()
    data["idea_id"] = idea_id
    data["user_id"] = current_user["id"]
    
    res = supabase.table("comments").insert(data).execute()
    return res.data[0]

@router.delete("/comments/{comment_id}")
def delete_comment(comment_id: str, current_user: dict = Depends(get_current_user)):
    existing = supabase.table("comments").select("user_id").eq("id", comment_id).execute()
    if not existing.data or existing.data[0]["user_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    supabase.table("comments").delete().eq("id", comment_id).execute()
    return {"message": "Comment deleted"}
