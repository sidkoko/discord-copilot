from openai import AsyncOpenAI
from config import get_settings
from typing import List
import logging

logger = logging.getLogger(__name__)
settings = get_settings()

# Initialize OpenAI client for embeddings (OpenRouter also supports OpenAI embeddings API)
openai_client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.openrouter_api_key
)


def chunk_text(text: str, chunk_size: int = 600, overlap: int = 100) -> List[str]:
    """
    Split text into overlapping chunks based on token count (approximately)
    Using simple word-based chunking (4 chars ≈ 1 token heuristic)
    """
    # Approximate tokens by characters (rough estimate: 4 chars = 1 token)
    chars_per_chunk = chunk_size * 4
    overlap_chars = overlap * 4
    
    # Split by sentences first (better semantic boundaries)
    sentences = text.replace('\n', ' ').split('. ')
    
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        
        sentence_length = len(sentence)
        
        if current_length + sentence_length > chars_per_chunk and current_chunk:
            # Create chunk
            chunk_text = '. '.join(current_chunk) + '.'
            chunks.append(chunk_text)
            
            # Start new chunk with overlap
            # Keep last few sentences for context
            overlap_sentences = []
            overlap_length = 0
            for sent in reversed(current_chunk):
                if overlap_length + len(sent) <= overlap_chars:
                    overlap_sentences.insert(0, sent)
                    overlap_length += len(sent)
                else:
                    break
            
            current_chunk = overlap_sentences
            current_length = overlap_length
        
        current_chunk.append(sentence)
        current_length += sentence_length
    
    # Add final chunk
    if current_chunk:
        chunk_text = '. '.join(current_chunk) + '.'
        chunks.append(chunk_text)
    
    return chunks


async def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a list of texts using OpenAI
    """
    try:
        # OpenAI supports batch embedding (max 2048 texts)
        response = await openai_client.embeddings.create(
            model=settings.embedding_model,
            input=texts
        )
        
        embeddings = [item.embedding for item in response.data]
        return embeddings
    
    except Exception as e:
        logger.error(f"Failed to generate embeddings: {str(e)}")
        raise


async def search_knowledge(query: str, top_k: int = 5) -> List[dict]:
    """
    Search knowledge base using vector similarity via Supabase RPC
    Returns list of relevant chunks with metadata
    """
    try:
        from db.supabase_client import get_supabase
        
        # 1. Generate query embedding
        query_embeddings = await generate_embeddings([query])
        query_embedding = query_embeddings[0]
        
        # 2. Search using Supabase RPC function
        supabase = get_supabase()
        
        # Call the search_documents RPC function
        response = supabase.rpc(
            "search_documents",
            {
                "query_embedding": query_embedding,
                "match_count": top_k
            }
        ).execute()
        
        knowledge_chunks = []
        for row in response.data:
            knowledge_chunks.append({
                "text": row["chunk_text"],
                "page_number": row["page_number"],
                "source": f"{row['filename']} (page {row['page_number']})",
                "similarity": float(row["similarity"])
            })
        
        return knowledge_chunks
    
    except Exception as e:
        logger.error(f"Failed to search knowledge: {str(e)}")
        return []  # Return empty list on error, don't fail the bot
