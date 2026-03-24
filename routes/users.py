from fastapi import APIRouter, Depends, HTTPException
from utils.auth import get_current_user
from services.supabase import supabase
from models.user import UserUpdate, UserLanguageUpdate, UserPreferencesUpdate, BlockUserRequest

router = APIRouter()

@router.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    return current_user

@router.put("/me")
def update_me(user_update: UserUpdate, current_user: dict = Depends(get_current_user)):
    update_data = {k: v for k, v in user_update.model_dump().items() if v is not None}
    if not update_data:
        return current_user
        
    res = supabase.table("users").update(update_data).eq("id", current_user["id"]).execute()
    if not res.data:
        raise HTTPException(status_code=400, detail="Failed to update user")
    return res.data[0]

@router.get("/{user_id}")
def get_user(user_id: str, current_user: dict = Depends(get_current_user)):
    res = supabase.table("users").select("id, name, bio, city, college, avatar_url, followers_count, following_count, trust_score, created_at").eq("id", user_id).execute()
    if not res.data:
        raise HTTPException(status_code=404, detail="User not found")
    return res.data[0]

@router.put("/me/preferences")
def update_preferences(prefs: UserPreferencesUpdate, current_user: dict = Depends(get_current_user)):
    res = supabase.table("users").update({"preferences": prefs.preferences}).eq("id", current_user["id"]).execute()
    return res.data[0]

@router.put("/me/language")
def update_language(lang: UserLanguageUpdate, current_user: dict = Depends(get_current_user)):
    res = supabase.table("users").update({"language": lang.language}).eq("id", current_user["id"]).execute()
    return res.data[0]

@router.post("/{user_id}/block")
def block_user(user_id: str, req: BlockUserRequest, current_user: dict = Depends(get_current_user)):
    if user_id == current_user["id"]:
        raise HTTPException(status_code=400, detail="Cannot block yourself")
        
    data = {
        "blocker_id": current_user["id"],
        "blocked_id": user_id,
        "reason": req.reason
    }
    
    res = supabase.table("blocks").insert(data).execute()
    return {"message": "User blocked successfully"}

@router.delete("/{user_id}/block")
def unblock_user(user_id: str, current_user: dict = Depends(get_current_user)):
    res = supabase.table("blocks").delete().match({"blocker_id": current_user["id"], "blocked_id": user_id}).execute()
    return {"message": "User unblocked successfully"}
