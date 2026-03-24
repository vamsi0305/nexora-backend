from fastapi import HTTPException
import httpx

def handle_db_error(response, default_message="Database operation failed"):
    """
    Supabase (postgrest-py) now raises exceptions on errors instead of 
    returning them in the response tuple for normal queries,
    but it's good to have a uniform wrapper.
    """
    if hasattr(response, "error") and response.error is not None:
         raise HTTPException(status_code=400, detail=f"{default_message}: {response.error.message}")
    if hasattr(response, "data") and isinstance(response.data, list) and not response.data:
         # Depending on the operation, this could just mean not found
         pass
    return response

def paginate(query, page: int, limit: int):
    """
    Apply pagination offset to a Supabase query.
    """
    # Fix 0-indexing page or 1-indexing page. Assuming page 1 is the first page.
    start = (page - 1) * limit
    end = start + limit - 1
    return query.range(start, end)
