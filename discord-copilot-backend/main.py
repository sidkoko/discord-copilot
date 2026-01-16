from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import logging

from api.routes import instructions, memory, channels, knowledge, bot_query
from bot.discord_bot import start_bot

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown"""
    # Startup: Start Discord bot in background
    logger.info("Starting Discord bot...")
    bot_task = asyncio.create_task(start_bot())
    
    yield
    
    # Shutdown: Cancel bot task
    logger.info("Shutting down Discord bot...")
    bot_task.cancel()
    try:
        await bot_task
    except asyncio.CancelledError:
        pass


# Create FastAPI app
app = FastAPI(
    title="Discord Copilot API",
    description="Backend API for Discord Copilot admin dashboard and bot",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(instructions.router)
app.include_router(memory.router)
app.include_router(channels.router)
app.include_router(knowledge.router)
app.include_router(bot_query.router)


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "discord-copilot-api"
    }


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Discord Copilot API",
        "docs": "/docs",
        "health": "/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
