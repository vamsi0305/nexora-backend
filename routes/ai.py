from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from utils.auth import get_current_user
from services.groq_ai import generate_completion

router = APIRouter()

class AICheckRequest(BaseModel):
    content: str | None = None
    text: str | None = None
    
class SchemeMatchRequest(BaseModel):
    idea_description: str
    user_profile_context: str

@router.post("/check-quality")
def check_quality(req: AICheckRequest, current_user: dict = Depends(get_current_user)):
    content = req.content or req.text
    if not content:
        raise HTTPException(status_code=400, detail="Idea content is required")

    prompt = f"Analyze the following idea description and rate its quality, clarity, and viability on a scale of 1-10. Provide constructive feedback.\nIdea: {content}"
    response = generate_completion(prompt, system_message="You are an expert startup advisor and pitch analyst.")
    lowered = response.lower()
    score = 65
    for token in ["10", "9", "8", "7", "6", "5", "4", "3", "2", "1"]:
        if f"{token}/10" in lowered or f" {token} " in lowered:
            score = int(token) * 10
            break
    return {"score": score, "feedback": response}
    
@router.post("/check-similarity")
def check_similarity(req: AICheckRequest, current_user: dict = Depends(get_current_user)):
    content = req.content or req.text
    if not content:
        raise HTTPException(status_code=400, detail="Idea content is required")

    # In a real app, we'd query our DB for existing ideas and ask AI to compare, 
    # or use vector search with embeddings. For now, we simulate this.
    prompt = f"I have a new idea: '{content}'. Without querying a real DB, what are some potential similar existing platforms or concepts, and how can this stand out?"
    response = generate_completion(prompt)
    return {"analysis": response}

@router.post("/scheme-matcher")
def scheme_matcher(req: SchemeMatchRequest, current_user: dict = Depends(get_current_user)):
    prompt = f"Given the user context: {req.user_profile_context} and their idea: {req.idea_description}, suggest actionable government schemes, grants, or incubators in India (specifically relevant to Kakinada/Andhra Pradesh if possible) they can apply for."
    response = generate_completion(prompt, system_message="You are an expert on Indian startup ecosystems and government schemes.")
    return {"schemes_suggestions": response}
