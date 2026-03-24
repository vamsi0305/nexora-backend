from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from utils.auth import get_current_user
from services.groq_ai import generate_completion

router = APIRouter()

class AICheckRequest(BaseModel):
    content: str
    
class SchemeMatchRequest(BaseModel):
    idea_description: str
    user_profile_context: str

@router.post("/check-quality")
def check_quality(req: AICheckRequest, current_user: dict = Depends(get_current_user)):
    prompt = f"Analyze the following idea description and rate its quality, clarity, and viability on a scale of 1-10. Provide constructive feedback.\nIdea: {req.content}"
    response = generate_completion(prompt, system_message="You are an expert startup advisor and pitch analyst.")
    return {"feedback": response}
    
@router.post("/check-similarity")
def check_similarity(req: AICheckRequest, current_user: dict = Depends(get_current_user)):
    # In a real app, we'd query our DB for existing ideas and ask AI to compare, 
    # or use vector search with embeddings. For now, we simulate this.
    prompt = f"I have a new idea: '{req.content}'. Without querying a real DB, what are some potential similar existing platforms or concepts, and how can this stand out?"
    response = generate_completion(prompt)
    return {"analysis": response}

@router.post("/scheme-matcher")
def scheme_matcher(req: SchemeMatchRequest, current_user: dict = Depends(get_current_user)):
    prompt = f"Given the user context: {req.user_profile_context} and their idea: {req.idea_description}, suggest actionable government schemes, grants, or incubators in India (specifically relevant to Kakinada/Andhra Pradesh if possible) they can apply for."
    response = generate_completion(prompt, system_message="You are an expert on Indian startup ecosystems and government schemes.")
    return {"schemes_suggestions": response}
