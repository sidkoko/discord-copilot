from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from api.middleware.auth import get_current_user
from db.supabase_client import get_supabase
from datetime import datetime

router = APIRouter(prefix="/api/channels", tags=["channels"])


class ChannelCreate(BaseModel):
    channel_id: str
    channel_name: str | None = None


class ChannelResponse(BaseModel):
    id: str
    channel_id: str
    channel_name: str | None
    added_at: datetime
    added_by: str | None


@router.get("", response_model=list[ChannelResponse])
async def list_channels():
    """
    List all allowed Discord channels (public for bot access)
    """
    supabase = get_supabase()
    
    try:
        response = supabase.table("allowed_channels").select("*").order("added_at", desc=True).execute()
        return response.data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch channels: {str(e)}")


@router.post("", response_model=ChannelResponse)
async def add_channel(
    channel: ChannelCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Add a Discord channel to the allow-list (requires authentication)
    """
    supabase = get_supabase()
    
    try:
        response = supabase.table("allowed_channels").insert({
            "channel_id": channel.channel_id,
            "channel_name": channel.channel_name,
            "added_by": current_user["user_id"]
        }).execute()
        
        if not response.data:
            raise HTTPException(status_code=500, detail="Failed to add channel")
        
        return response.data[0]
    
    except Exception as e:
        # Handle unique constraint violation
        if "duplicate key" in str(e).lower():
            raise HTTPException(status_code=400, detail="Channel already exists in allow-list")
        raise HTTPException(status_code=500, detail=f"Failed to add channel: {str(e)}")


@router.delete("/{channel_id}")
async def remove_channel(
    channel_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Remove a Discord channel from the allow-list (requires authentication)
    """
    supabase = get_supabase()
    
    try:
        response = supabase.table("allowed_channels").delete().eq("channel_id", channel_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Channel not found")
        
        return {"message": "Channel removed successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to remove channel: {str(e)}")
