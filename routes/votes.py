from fastapi import APIRouter, Depends, HTTPException
from utils.auth import get_current_user
from services.supabase import supabase
from models.vote import VoteCreate
from services.notifications import create_notification

router = APIRouter()

def normalize_vote(vote: VoteCreate) -> str | None:
    if vote.vote_type in {"upvote", "downvote"}:
        return vote.vote_type

    if vote.value in {1, "1", "upvote", "up", "UP"}:
        return "upvote"
    if vote.value in {-1, "-1", "downvote", "down", "DOWN"}:
        return "downvote"
    if vote.value in {0, "0", None}:
        return None

    raise HTTPException(status_code=400, detail="Invalid vote value")

def sync_vote_counts(idea_id: str):
    votes_res = supabase.table("votes").select("vote_type").eq("idea_id", idea_id).execute()
    upvotes = sum(1 for row in votes_res.data if row["vote_type"] == "upvote")
    downvotes = sum(1 for row in votes_res.data if row["vote_type"] == "downvote")
    supabase.table("ideas").update({
        "upvotes_count": upvotes,
        "downvotes_count": downvotes
    }).eq("id", idea_id).execute()

@router.post("/{idea_id}/vote")
def cast_vote(idea_id: str, vote: VoteCreate, current_user: dict = Depends(get_current_user)):
    vote_type = normalize_vote(vote)
    if vote_type is None:
        supabase.table("votes").delete().match({
            "idea_id": idea_id,
            "user_id": current_user["id"]
        }).execute()
        sync_vote_counts(idea_id)
        return {"message": "Vote removed"}

    # Check existing vote
    existing = supabase.table("votes").select("*").match({
        "idea_id": idea_id, 
        "user_id": current_user["id"]
    }).execute()
    
    if existing.data:
        # Update existing vote
        if existing.data[0]["vote_type"] == vote_type:
            return {"message": "Already voted with same type"}
        
        res = supabase.table("votes").update({"vote_type": vote_type}).eq("id", existing.data[0]["id"]).execute()
        sync_vote_counts(idea_id)
        return res.data[0]
    
    # New vote
    idea = supabase.table("ideas").select("id, title, user_id").eq("id", idea_id).execute()
    if not idea.data:
        raise HTTPException(status_code=404, detail="Idea not found")

    data = {
        "idea_id": idea_id,
        "user_id": current_user["id"],
        "vote_type": vote_type
    }
    res = supabase.table("votes").insert(data).execute()
    sync_vote_counts(idea_id)

    idea_owner = idea.data[0]["user_id"]
    if idea_owner != current_user["id"] and vote_type == "upvote":
        create_notification(
            idea_owner,
            "vote",
            f"{current_user.get('name', 'Someone')} upvoted your idea '{idea.data[0]['title']}'.",
            idea_id,
        )
    return res.data[0]

@router.delete("/{idea_id}/vote")
def remove_vote(idea_id: str, current_user: dict = Depends(get_current_user)):
    res = supabase.table("votes").delete().match({
        "idea_id": idea_id, 
        "user_id": current_user["id"]
    }).execute()
    sync_vote_counts(idea_id)
    return {"message": "Vote removed"}
