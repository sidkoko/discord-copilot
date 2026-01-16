from config import get_settings
from openai import AsyncOpenAI
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


class LLMClient:
    """Unified LLM client using OpenRouter"""
    
    def __init__(self):
        # OpenRouter uses OpenAI-compatible API
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.openrouter_api_key,
        )
        self.model = settings.llm_provider
    
    async def generate_response(self, system_prompt: str, user_message: str) -> str:
        """
        Generate a response using OpenRouter
        """
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ]
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"LLM generation failed: {str(e)}")
            return "I apologize, but I'm having trouble processing your request right now. Please try again later."
    
    async def generate_memory_summary(self, conversation_history: str, new_exchange: str) -> str:
        """
        Generate a concise rolling summary of the conversation for context
        """
        prompt = f"""You are a conversation context manager. Create a BRIEF summary that captures the essence of conversations.

RULES:
1. Summarize topics discussed, NOT exact words spoken
2. Focus on: key topics, user interests, important facts mentioned
3. Use short phrases, not full sentences
4. Maximum 200 words - be concise!
5. Format: Topic-based summary, not chronological

EXISTING CONTEXT:
{conversation_history}

NEW EXCHANGE:
{new_exchange}

Write a brief, updated context summary. Example format:
"Topics covered: [topics]. User asked about: [interests]. Key info shared: [facts]."

Keep under 200 words."""

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300
            )
            return response.choices[0].message.content
        
        except Exception as e:
            logger.error(f"Memory summary generation failed: {str(e)}")
            # Return simple concatenation as fallback
            return f"{conversation_history}\n\n{new_exchange}"


# Global LLM client instance
llm_client = LLMClient()
