from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from api.middleware.auth import get_current_user
from db.supabase_client import get_supabase
from datetime import datetime

router = APIRouter(prefix="/api/instructions", tags=["instructions"])


class InstructionsUpdate(BaseModel):
    instructions: str


class InstructionsResponse(BaseModel):
    id: str
    instructions: str
    updated_at: datetime
    updated_by: str | None


@router.get("", response_model=InstructionsResponse)
async def get_instructions():
    """
    Get current system instructions (public endpoint for bot access)
    """
    supabase = get_supabase()
    
    try:
        response = supabase.table("system_instructions").select("*").order("updated_at", desc=True).limit(1).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="No system instructions found")
        
        return response.data[0]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch instructions: {str(e)}")


@router.post("", response_model=InstructionsResponse)
async def update_instructions(
    update: InstructionsUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update system instructions (requires authentication)
    """
    supabase = get_supabase()
    
    try:
        # Check if any instructions exist
        existing = supabase.table("system_instructions").select("id").limit(1).execute()
        
        if existing.data:
            # Update existing
            response = supabase.table("system_instructions").update({
                "instructions": update.instructions,
                "updated_at": datetime.utcnow().isoformat(),
                "updated_by": current_user["user_id"]
            }).eq("id", existing.data[0]["id"]).execute()
        else:
            # Insert new
            response = supabase.table("system_instructions").insert({
                "instructions": update.instructions,
                "updated_by": current_user["user_id"]
            }).execute()
        
        if not response.data:
            raise HTTPException(status_code=500, detail="Failed to update instructions")
        
        return response.data[0]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update instructions: {str(e)}")
