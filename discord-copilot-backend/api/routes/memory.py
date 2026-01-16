from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from api.middleware.auth import get_current_user
from db.supabase_client import get_supabase
from datetime import datetime

router = APIRouter(prefix="/api/memory", tags=["memory"])


class MemoryResponse(BaseModel):
    id: str
    summary: str
    last_updated: datetime
    message_count: int


class MemoryUpdate(BaseModel):
    summary: str
    message_count: int


@router.get("", response_model=MemoryResponse)
async def get_memory():
    """
    Get current conversation memory (public endpoint for bot access)
    """
    supabase = get_supabase()
    
    try:
        response = supabase.table("conversation_memory").select("*").limit(1).execute()
        
        if not response.data:
            # Create default memory if none exists
            default = supabase.table("conversation_memory").insert({
                "summary": "No conversation history yet.",
                "message_count": 0
            }).execute()
            return default.data[0]
        
        return response.data[0]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch memory: {str(e)}")


@router.post("", response_model=MemoryResponse)
async def update_memory(update: MemoryUpdate):
    """
    Update conversation memory (used by bot, no auth required)
    """
    supabase = get_supabase()
    
    try:
        # Get existing memory
        existing = supabase.table("conversation_memory").select("id").limit(1).execute()
        
        if existing.data:
            # Update existing
            response = supabase.table("conversation_memory").update({
                "summary": update.summary,
                "message_count": update.message_count,
                "last_updated": datetime.utcnow().isoformat()
            }).eq("id", existing.data[0]["id"]).execute()
        else:
            # Insert new
            response = supabase.table("conversation_memory").insert({
                "summary": update.summary,
                "message_count": update.message_count
            }).execute()
        
        if not response.data:
            raise HTTPException(status_code=500, detail="Failed to update memory")
        
        return response.data[0]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update memory: {str(e)}")


@router.delete("")
async def reset_memory(current_user: dict = Depends(get_current_user)):
    """
    Reset conversation memory (requires authentication)
    """
    supabase = get_supabase()
    
    try:
        # Get existing memory
        existing = supabase.table("conversation_memory").select("id").limit(1).execute()
        
        if existing.data:
            # Reset to default
            response = supabase.table("conversation_memory").update({
                "summary": "No conversation history yet.",
                "message_count": 0,
                "last_updated": datetime.utcnow().isoformat()
            }).eq("id", existing.data[0]["id"]).execute()
            
            return {"message": "Memory reset successfully"}
        else:
            raise HTTPException(status_code=404, detail="No memory found to reset")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reset memory: {str(e)}")
