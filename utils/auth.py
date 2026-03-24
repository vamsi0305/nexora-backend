import os
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from services.supabase import supabase

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        # Use Supabase client to get the user from the JWT
        res = supabase.auth.get_user(token)
        if not res.user:
            raise credentials_exception
            
        user_id = res.user.id
    except Exception:
        raise credentials_exception
        
    # Check if user exists in database
    user_response = supabase.table("users").select("*").eq("id", user_id).execute()
    if not user_response.data or len(user_response.data) == 0:
        raise credentials_exception
        
    return user_response.data[0]
