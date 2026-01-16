import discord
from discord.ext import commands
import httpx
from config import get_settings
from bot.llm_client import llm_client
from db.supabase_client import get_supabase
import logging
import asyncio

logger = logging.getLogger(__name__)
settings = get_settings()


class DiscordBot(commands.Bot):
    """Discord bot with RAG-powered responses"""
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        
        super().__init__(command_prefix="!", intents=intents)
        
        self.api_base_url = "http://localhost:8000"  # FastAPI running locally
    
    async def on_ready(self):
        """Called when bot is ready"""
        logger.info(f'Discord bot logged in as {self.user}')
        print(f'✅ Discord bot is online as {self.user}')
    
    async def on_message(self, message: discord.Message):
        """Handle incoming messages"""
        # Debug logging
        logger.info(f"📩 Message received from {message.author}: {message.content[:50]}...")
        logger.info(f"   Channel ID: {message.channel.id}, Bot mentioned: {self.user in message.mentions}")
        
        # Ignore own messages
        if message.author == self.user:
            logger.info("   ↪ Ignoring own message")
            return
        
        # Only respond when mentioned
        if self.user not in message.mentions:
            logger.info("   ↪ Bot not mentioned, ignoring")
            return
        
        # Get channel ID
        channel_id = str(message.channel.id)
        
        # Remove bot mention from message
        query = message.content.replace(f'<@{self.user.id}>', '').strip()
        
        if not query:
            await message.reply("Hello! How can I help you?")
            return
        
        try:
            # Show typing indicator
            async with message.channel.typing():
                # Get context from API
                context = await self._get_bot_context(query, channel_id)
                
                # Check if channel is allowed
                if not context["is_allowed_channel"]:
                    await message.reply("❌ This channel is not configured for bot responses. Please ask an admin to add it to the allow-list.")
                    return
                
                # Assemble prompt
                prompt = self._assemble_prompt(
                    context["system_instructions"],
                    context["conversation_memory"],
                    context["relevant_knowledge"],
                    query
                )
                
                # Generate response using LLM
                response = await llm_client.generate_response(prompt, query)
                
                # Send response (split if too long)
                await self._send_response(message, response)
                
                # Update conversation memory
                await self._update_memory(query, response, context["conversation_memory"])
        
        except Exception as e:
            logger.error(f"Error handling message: {str(e)}")
            await message.reply("❌ Sorry, I encountered an error processing your request.")
    
    async def _get_bot_context(self, query: str, channel_id: str) -> dict:
        """Get context from FastAPI bot query endpoint"""
        from services.rag_service import search_knowledge
        from db.supabase_client import get_supabase
        
        # Call directly without HTTP overhead
        supabase = get_supabase()
        
        # Check if channel is allowed
        channel_response = supabase.table("allowed_channels").select("channel_id").eq(
            "channel_id", channel_id
        ).execute()
        
        is_allowed = len(channel_response.data) > 0
        
        if not is_allowed:
            return {
                "system_instructions": "",
                "conversation_memory": "",
                "relevant_knowledge": [],
                "is_allowed_channel": False
            }
        
        # Get system instructions
        instructions_response = supabase.table("system_instructions").select(
            "instructions"
        ).order("updated_at", desc=True).limit(1).execute()
        
        system_instructions = "You are a helpful Discord assistant."
        if instructions_response.data:
            system_instructions = instructions_response.data[0]["instructions"]
        
        # Get conversation memory
        memory_response = supabase.table("conversation_memory").select(
            "summary"
        ).limit(1).execute()
        
        conversation_memory = "No conversation history yet."
        if memory_response.data:
            conversation_memory = memory_response.data[0]["summary"]
        
        # Search knowledge base
        knowledge_chunks = await search_knowledge(query, settings.top_k_retrieval)
        
        return {
            "system_instructions": system_instructions,
            "conversation_memory": conversation_memory,
            "relevant_knowledge": knowledge_chunks,
            "is_allowed_channel": True
        }
    
    def _assemble_prompt(
        self,
        system_instructions: str,
        conversation_memory: str,
        knowledge_chunks: list,
        query: str
    ) -> str:
        """Assemble complete prompt for LLM"""
        prompt_parts = [system_instructions]
        
        # Add conversation context
        if conversation_memory and conversation_memory != "No conversation history yet.":
            prompt_parts.append(f"\n**Previous Conversation Summary:**\n{conversation_memory}")
        
        # Add relevant knowledge
        if knowledge_chunks:
            knowledge_text = "\n**Relevant Knowledge:**\n"
            for chunk in knowledge_chunks:
                if chunk["similarity"] > 0.5:  # Only include relevant chunks
                    knowledge_text += f"\n[From {chunk['source']}]\n{chunk['text']}\n"
            
            if len(knowledge_text) > len("\n**Relevant Knowledge:**\n"):
                prompt_parts.append(knowledge_text)
        
        return "\n\n".join(prompt_parts)
    
    async def _send_response(self, message: discord.Message, response: str):
        """Send response, splitting if necessary (Discord 2000 char limit)"""
        if len(response) <= 2000:
            await message.reply(response)
        else:
            # Split into chunks
            chunks = [response[i:i+2000] for i in range(0, len(response), 2000)]
            for chunk in chunks:
                await message.channel.send(chunk)
    
    async def _update_memory(self, user_query: str, bot_response: str, current_memory: str):
        """Update conversation memory"""
        try:
            supabase = get_supabase()
            
            # Get current memory record (include 'id' for update)
            memory_data = supabase.table("conversation_memory").select("id, message_count").limit(1).execute()
            
            # Generate new summary
            new_exchange = f"User: {user_query}\nAssistant: {bot_response}"
            new_summary = await llm_client.generate_memory_summary(current_memory, new_exchange)
            
            if memory_data.data:
                # Update existing record
                message_count = (memory_data.data[0].get("message_count") or 0) + 1
                supabase.table("conversation_memory").update({
                    "summary": new_summary,
                    "message_count": message_count,
                    "last_updated": "now()"
                }).eq("id", memory_data.data[0]["id"]).execute()
                logger.info(f"✅ Memory updated. Message count: {message_count}")
            else:
                # Create new memory record if none exists
                supabase.table("conversation_memory").insert({
                    "summary": new_summary,
                    "message_count": 1
                }).execute()
                logger.info("✅ Created new memory record")
        
        except Exception as e:
            logger.error(f"Failed to update memory: {str(e)}")


# Global bot instance
bot = DiscordBot()


async def start_bot():
    """Start the Discord bot"""
    try:
        await bot.start(settings.discord_bot_token)
    except Exception as e:
        logger.error(f"Failed to start Discord bot: {str(e)}")
        raise
