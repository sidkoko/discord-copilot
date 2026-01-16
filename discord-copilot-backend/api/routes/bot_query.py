from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db.supabase_client import get_supabase
from services.rag_service import search_knowledge
from config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(prefix="/api/bot", tags=["bot"])


class BotQueryRequest(BaseModel):
    query: str
    channel_id: str


class KnowledgeChunk(BaseModel):
    text: str
    source: str
    similarity: float


class BotQueryResponse(BaseModel):
    system_instructions: str
    conversation_memory: str
    relevant_knowledge: list[KnowledgeChunk]
    is_allowed_channel: bool


@router.post("/query", response_model=BotQueryResponse)
async def bot_query(request: BotQueryRequest):
    """
    Internal endpoint for Discord bot to get complete context
    No authentication required (internal use only)
    """
    supabase = get_supabase()
    
    try:
        # 1. Check if channel is allowed
        channel_response = supabase.table("allowed_channels").select("channel_id").eq(
            "channel_id", request.channel_id
        ).execute()
        
        is_allowed = len(channel_response.data) > 0
        
        if not is_allowed:
            return BotQueryResponse(
                system_instructions="",
                conversation_memory="",
                relevant_knowledge=[],
                is_allowed_channel=False
            )
        
        # 2. Get system instructions
        instructions_response = supabase.table("system_instructions").select(
            "instructions"
        ).order("updated_at", desc=True).limit(1).execute()
        
        system_instructions = "You are a helpful Discord assistant."
        if instructions_response.data:
            system_instructions = instructions_response.data[0]["instructions"]
        
        # 3. Get conversation memory
        memory_response = supabase.table("conversation_memory").select(
            "summary"
        ).limit(1).execute()
        
        conversation_memory = "No conversation history yet."
        if memory_response.data:
            conversation_memory = memory_response.data[0]["summary"]
        
        # 4. Search knowledge base
        knowledge_chunks = await search_knowledge(request.query, settings.top_k_retrieval)
        
        return BotQueryResponse(
            system_instructions=system_instructions,
            conversation_memory=conversation_memory,
            relevant_knowledge=[
                KnowledgeChunk(
                    text=chunk["text"],
                    source=chunk["source"],
                    similarity=chunk["similarity"]
                )
                for chunk in knowledge_chunks
            ],
            is_allowed_channel=True
        )
    
    except Exception as e:
        logger.error(f"Bot query failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to process bot query: {str(e)}")
