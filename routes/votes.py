from fastapi import APIRouter, Depends, HTTPException
from utils.auth import get_current_user
from services.supabase import supabase
from models.vote import VoteCreate

router = APIRouter()

@router.post("/{idea_id}/vote")
def cast_vote(idea_id: str, vote: VoteCreate, current_user: dict = Depends(get_current_user)):
    # Check existing vote
    existing = supabase.table("votes").select("*").match({
        "idea_id": idea_id, 
        "user_id": current_user["id"]
    }).execute()
    
    if existing.data:
        # Update existing vote
        if existing.data[0]["vote_type"] == vote.vote_type:
            return {"message": "Already voted with same type"}
        
        res = supabase.table("votes").update({"vote_type": vote.vote_type}).eq("id", existing.data[0]["id"]).execute()
        
        # We should update idea aggregates cleanly (ideally via DB trigger or function). Here we leave a placeholder.
        return res.data[0]
    
    # New vote
    data = {
        "idea_id": idea_id,
        "user_id": current_user["id"],
        "vote_type": vote.vote_type
    }
    res = supabase.table("votes").insert(data).execute()
    return res.data[0]

@router.delete("/{idea_id}/vote")
def remove_vote(idea_id: str, current_user: dict = Depends(get_current_user)):
    res = supabase.table("votes").delete().match({
        "idea_id": idea_id, 
        "user_id": current_user["id"]
    }).execute()
    return {"message": "Vote removed"}
