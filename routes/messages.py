from fastapi import APIRouter, Depends, HTTPException
from utils.auth import get_current_user
from services.supabase import supabase
from models.message import MessageCreate
from services.notifications import create_notification

router = APIRouter()

@router.get("/{idea_id}")
def get_messages(idea_id: str, current_user: dict = Depends(get_current_user)):
    # Check if a support pledge exists/accepted first to allow DMs matching user specification
    # Spec: DM endpoints check support_pledge exists before allowing message
    
    idea_resp = supabase.table("ideas").select("user_id").eq("id", idea_id).execute()
    if not idea_resp.data:
        raise HTTPException(status_code=404, detail="Idea not found")
        
    idea_owner_id = idea_resp.data[0]["user_id"]
    
    if current_user["id"] != idea_owner_id:
        pledge_resp = supabase.table("support_pledges").select("id").match({
            "idea_id": idea_id,
            "user_id": current_user["id"]
        }).execute()
        
        if not pledge_resp.data:
            raise HTTPException(status_code=403, detail="Must pledge support before messaging")
            
    res = supabase.table("messages").select("*").eq("idea_id", idea_id).or_(
        f"sender_id.eq.{current_user['id']},receiver_id.eq.{current_user['id']}"
    ).order("created_at").execute()
    
    return res.data

@router.post("/{idea_id}")
def send_message(idea_id: str, message: MessageCreate, current_user: dict = Depends(get_current_user)):
    idea_resp = supabase.table("ideas").select("user_id").eq("id", idea_id).execute()
    if not idea_resp.data:
        raise HTTPException(status_code=404, detail="Idea not found")
        
    idea_owner_id = idea_resp.data[0]["user_id"]
    receiver_id = idea_owner_id if current_user["id"] != idea_owner_id else message.receiver_id
    
    # Needs support pledge if not owner sending
    if current_user["id"] != idea_owner_id:
        pledge_resp = supabase.table("support_pledges").select("id").match({
            "idea_id": idea_id,
            "user_id": current_user["id"]
        }).execute()
        
        if not pledge_resp.data:
            raise HTTPException(status_code=403, detail="Must pledge support before messaging")
    else:
        if not receiver_id:
            raise HTTPException(status_code=400, detail="receiver_id is required when the idea owner sends a message")
    
    data = {
        "idea_id": idea_id,
        "sender_id": current_user["id"],
        "receiver_id": receiver_id,
        "content": message.content
    }
    
    res = supabase.table("messages").insert(data).execute()
    if receiver_id and receiver_id != current_user["id"]:
        create_notification(
            receiver_id,
            "message",
            f"{current_user.get('name', 'Someone')} sent you a message about an idea.",
            idea_id,
        )
    return res.data[0]
