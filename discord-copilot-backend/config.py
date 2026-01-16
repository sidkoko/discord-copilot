from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Supabase
    supabase_url: str
    supabase_service_role_key: str
    supabase_anon_key: str
    database_url: str
    
    # Discord
    discord_bot_token: str
    
    # AI APIs (using OpenRouter)
    openrouter_api_key: str
    
    # LLM Choice (use OpenRouter model names like: openai/gpt-4, anthropic/claude-3-opus, google/gemini-pro)
    llm_provider: str 
    
    # Embedding model
    embedding_model: str = "text-embedding-3-small"
    embedding_dimensions: int = 1536
    
    # RAG settings
    chunk_size: int = 600
    chunk_overlap: int = 100
    top_k_retrieval: int = 5
    
    # Conversation settings
    max_memory_length: int = 500
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
