from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from services.supabase import supabase

router = APIRouter()

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    phone_number: str
    college: Optional[str] = None
    city: Optional[str] = None
    bio: Optional[str] = None
    language: Optional[str] = "en"
    domain_interests: Optional[list[str]] = []

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RecoveryRequest(BaseModel):
    email: EmailStr

class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

@router.post("/register", response_model=AuthResponse)
def register(request: RegisterRequest):
    try:
        res = supabase.auth.sign_up({
            "email": request.email,
            "password": request.password,
            "options": {
                "data": {
                    "full_name": request.full_name,
                    "phone_number": request.phone_number,
                    "college": request.college,
                    "city": request.city,
                    "bio": request.bio,
                    "language": request.language,
                    "domain_interests": request.domain_interests,
                }
            }
        })
        if not res.user:
            raise HTTPException(status_code=400, detail="Registration failed. Check if user already exists.")
            
        # Supabase auth.sign_up creates a user in auth.users
        # We manually insert the user into the public.users table as well
        user_data = {
            "id": res.user.id,
            "name": request.full_name,
            "email": request.email,
            "phone": request.phone_number,
            "college": request.college,
            "city": request.city,
            "bio": request.bio,
            "language": request.language,
            "preferences": {
                "domain_interests": request.domain_interests or []
            },
        }
        user_row = supabase.table("users").upsert(user_data).execute()
        created_user = user_row.data[0] if user_row.data else {
            "id": res.user.id,
            "email": request.email,
            "name": request.full_name,
        }

        return AuthResponse(
            access_token=res.session.access_token if res.session else "registration-successful-login-required",
            token_type="bearer",
            user=created_user
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=AuthResponse)
def login(request: LoginRequest):
    try:
        res = supabase.auth.sign_in_with_password({
            "email": request.email,
            "password": request.password
        })
        if not res.session:
            raise HTTPException(status_code=401, detail="Invalid email or password")

        user_row = supabase.table("users").select("*").eq("id", res.user.id).execute()
        user = user_row.data[0] if user_row.data else {"id": res.user.id, "email": res.user.email}
            
        return AuthResponse(
            access_token=res.session.access_token,
            token_type="bearer",
            user=user
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/logout")
def logout():
    try:
        supabase.auth.sign_out()
        return {"message": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recovery")
def recovery(request: RecoveryRequest):
    try:
        supabase.auth.reset_password_email(request.email)
        return {"message": "Recovery instructions sent to email"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
