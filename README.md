# Discord Copilot 🤖

A production-ready Discord bot with an admin dashboard, RAG-powered knowledge base, and intelligent conversation memory.

## 🚀 Features

- **Admin Dashboard**: Beautiful Next.js dashboard for managing bot configuration
- **RAG Knowledge Base**: Upload PDFs to give your bot domain-specific knowledge
- **Conversation Memory**: Bot maintains context across conversations
- **Channel Management**: Control which Discord channels the bot responds in
- **Customizable Instructions**: Define your bot's personality and behavior
- **Multi-LLM Support**: Choose between Gemini, Claude, or GPT

## 🏗️ Architecture

```
discord-copilot/
├── discord-copilot-admin/      # Next.js admin dashboard
│   ├── app/                    # App router pages
│   │   ├── auth/              # Login/signup pages
│   │   └── dashboard/         # Protected dashboard pages
│   └── lib/                   # Utility functions
│
└── discord-copilot-backend/    # FastAPI + Discord bot
    ├── api/                   # API routes
    │   ├── routes/           # Endpoint handlers
    │   └── middleware/       # Auth middleware
    ├── bot/                  # Discord bot
    ├── services/             # Business logic
    │   ├── rag_service.py   # RAG pipeline
    │   └── pdf_processor.py # PDF processing
    └── db/                  # Database clients
```

## 📋 Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (Supabase)
- Discord Bot Token
- API Keys:
  - OpenAI (for embeddings)
  - Gemini/Claude/GPT (for LLM)

## 🔧 Setup Instructions

### 1. Database Setup (Supabase)

1. Create a Supabase project at [supabase.com](https://supabase.com)
2. Run the SQL schema in `discord-copilot-backend/schema.sql` in the Supabase SQL Editor
3. Enable pgvector extension (should be done automatically)
4. Create a storage bucket named "documents" for PDF uploads

### 2. Discord Bot Setup

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to "Bot" tab and create a bot
4. Copy the bot token
5. Enable these Privileged Gateway Intents:
   - Message Content Intent
   - Server Members Intent
6. Go to OAuth2 → URL Generator:
   - Select scopes: `bot`
   - Select permissions: `Send Messages`, `Read Message History`, `Read Messages/View Channels`
7. Use the generated URL to add the bot to your server

### 3. Backend Setup

```bash
cd discord-copilot-backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Edit .env with your credentials
```

**Required environment variables:**

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
SUPABASE_ANON_KEY=your_anon_key
DATABASE_URL=postgresql://postgres:[password]@[host]:5432/postgres

DISCORD_BOT_TOKEN=your_discord_bot_token

OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
LLM_PROVIDER=gemini
```

### 4. Frontend Setup

```bash
cd discord-copilot-admin

# Install dependencies
npm install

# Create .env.local file
cp env.example.txt .env.local

# Edit .env.local
```

**Required environment variables:**

```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🎮 Running Locally

### Start Backend (Terminal 1)

```bash
cd discord-copilot-backend
source venv/bin/activate
python main.py
```

The backend will start on `http://localhost:8000`
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

### Start Frontend (Terminal 2)

```bash
cd discord-copilot-admin
npm run dev
```

The dashboard will start on `http://localhost:3000`

## 📚 Usage Guide

### 1. Create Admin Account

1. Go to http://localhost:3000
2. Click "Sign up"
3. Create an account with your email

### 2. Configure Bot Instructions

1. Login to the dashboard
2. Go to "System Instructions"
3. Define how your bot should behave
4. Click "Save Instructions"

### 3. Upload Knowledge Base

1. Go to "Knowledge Base"
2. Upload PDF documents
3. Wait for processing to complete (status will change to "completed")
4. The bot will use this knowledge to answer questions

### 4. Add Allowed Channels

1. Go to "Channels"
2. Get your Discord channel ID:
   - Enable Developer Mode in Discord
   - Right-click channel → Copy Channel ID
3. Add the channel ID to allow-list

### 5. Test the Bot

1. Go to your Discord server
2. In an allowed channel, mention the bot:
   ```
   @YourBot What is this document about?
   ```
3. The bot will respond using its instructions and knowledge base

## 🚀 Deployment

### Backend Deployment (Render)

1. Push code to GitHub
2. Create new Web Service on [render.com](https://render.com)
3. Connect your repository
4. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`
   - Environment: Python 3
5. Add all environment variables from `.env`
6. Deploy!

### Frontend Deployment (Vercel)

1. Push code to GitHub
2. Import project on [vercel.com](https://vercel.com)
3. Configure:
   - Framework: Next.js
   - Root Directory: `discord-copilot-admin`
4. Add environment variables:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - `NEXT_PUBLIC_API_URL` (your Render backend URL)
5. Deploy!

## 🔧 API Endpoints

### Public Endpoints
- `GET /health` - Health check
- `GET /api/instructions` - Get system instructions
- `GET /api/memory` - Get conversation memory
- `GET /api/channels` - List allowed channels

### Protected Endpoints (require JWT)
- `POST /api/instructions` - Update instructions
- `POST /api/knowledge/upload` - Upload PDF
- `GET /api/knowledge/list` - List documents
- `DELETE /api/knowledge/{id}` - Delete document
- `POST /api/memory` - Update memory
- `DELETE /api/memory` - Reset memory
- `POST /api/channels` - Add channel
- `DELETE /api/channels/{id}` - Remove channel

## 🎨 Tech Stack

### Frontend
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Supabase Auth

### Backend
- FastAPI
- discord.py
- PostgreSQL + pgvector
- OpenAI (embeddings)
- Google Gemini / Anthropic Claude (LLM)

## 📝 Development Tips

- **Test RAG**: Upload a PDF and ask specific questions about its content
- **Memory**: The bot remembers conversation context automatically
- **LLM Switch**: Change `LLM_PROVIDER` in `.env` to switch between Gemini/Claude/GPT
- **Logs**: Check terminal output for bot activity and errors

## 🐛 Troubleshooting

**Bot not responding:**
- Check if channel is in allow-list
- Verify bot has Message Content Intent enabled
- Check bot online status in Discord

**PDF upload fails:**
- Ensure file is under 10MB
- Check if Supabase storage bucket "documents" exists
- Verify API backend is running

**Authentication errors:**
- Verify Supabase credentials in `.env` files
- Check if JWT token is being sent correctly

## 📄 License

MIT

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

---

Built with ❤️ using Next.js, FastAPI, and Discord.py
