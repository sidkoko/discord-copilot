# Discord Copilot 🤖✨

> A production-ready Discord bot with an AI-powered knowledge base, intelligent conversation memory, and a sleek admin dashboard.

![Discord](https://img.shields.io/badge/Discord-Bot-5865F2?style=for-the-badge&logo=discord&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge&logo=next.js&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🎛️ **Admin Dashboard** | Beautiful Next.js dashboard with authentication for managing everything |
| 📚 **RAG Knowledge Base** | Upload PDFs and give your bot domain-specific knowledge using vector embeddings |
| 🧠 **Conversation Memory** | Bot remembers context across conversations with rolling summaries |
| 📢 **Channel Management** | Control which Discord channels the bot responds in |
| ⚙️ **Custom Instructions** | Define your bot's personality, behavior, and response style |
| 🔄 **Multi-LLM Support** | Works with OpenRouter (Gemini, Claude, GPT, Llama, etc.) |

---

## 🏗️ Architecture

```
discord-copilot/
├── discord-copilot-admin/      # Next.js 14 Admin Dashboard
│   ├── app/                    
│   │   ├── auth/              # Login & Signup
│   │   └── dashboard/         # Protected admin pages
│   │       ├── instructions/  # Bot personality config
│   │       ├── knowledge/     # PDF upload & management
│   │       ├── memory/        # Conversation context
│   │       └── channels/      # Discord channel allow-list
│   └── lib/                   
│
└── discord-copilot-backend/    # FastAPI + Discord.py Backend
    ├── api/routes/            # REST API endpoints
    ├── bot/                   # Discord bot logic
    ├── services/              
    │   ├── rag_service.py     # Vector search & embeddings
    │   └── pdf_processor.py   # PDF text extraction
    └── db/                    # Supabase client
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- [Supabase](https://supabase.com) account (free tier works!)
- [Discord Developer](https://discord.com/developers) bot token
- [OpenRouter](https://openrouter.ai) API key

### 1️⃣ Clone & Setup Database

```bash
git clone https://github.com/sidkoko/discord-copilot.git
cd discord-copilot
```

Run the SQL from `discord-copilot-backend/schema.sql` in your Supabase SQL Editor.

### 2️⃣ Backend Setup

```bash
cd discord-copilot-backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env  # Edit with your credentials
python main.py
```

### 3️⃣ Frontend Setup

```bash
cd discord-copilot-admin
npm install

# Configure environment
# Create .env.local with Supabase credentials
npm run dev
```

### 4️⃣ Use the Bot!

1. Open dashboard at `http://localhost:3000`
2. Sign up and configure your bot
3. Upload PDFs to the knowledge base
4. Add your Discord channel ID to allow-list
5. Mention the bot in Discord: `@YourBot What does the document say about...?`

---

## 🔧 Environment Variables

### Backend (`.env`)
```env
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_service_key
SUPABASE_ANON_KEY=your_anon_key
DISCORD_BOT_TOKEN=your_bot_token
OPENROUTER_API_KEY=your_openrouter_key
LLM_PROVIDER=openai/gpt-4o-mini
```

### Frontend (`.env.local`)
```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 📸 Screenshots

| Dashboard | Knowledge Base | Memory |
|-----------|----------------|--------|
| System instructions config | PDF upload & management | Conversation context viewer |

---

## 🛠️ Tech Stack

**Frontend:** Next.js 14, TypeScript, Tailwind CSS, Supabase Auth

**Backend:** FastAPI, discord.py, OpenRouter, pgvector

**Database:** PostgreSQL (Supabase) with vector embeddings

**AI:** OpenRouter API (GPT-4, Claude, Gemini, Llama, etc.)

---

## 📄 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/api/instructions` | Get system instructions |
| POST | `/api/instructions` | Update instructions (auth required) |
| POST | `/api/knowledge/upload` | Upload PDF (auth required) |
| GET | `/api/knowledge/list` | List documents |
| GET | `/api/memory` | Get conversation memory |
| DELETE | `/api/memory` | Reset memory (auth required) |
| GET | `/api/channels` | List allowed channels |
| POST | `/api/channels` | Add channel (auth required) |

---

## 🚀 Deployment

**Recommended Stack:**
- **Backend:** [Render](https://render.com) (free tier available)
- **Frontend:** [Vercel](https://vercel.com) (free tier available)
- **Database:** [Supabase](https://supabase.com) (free tier available)

See `DEPLOYMENT.md` for detailed deployment instructions.

---

## 📝 License

MIT License - feel free to use this for your own projects!

---

<p align="center">
  Built with ❤️ using Next.js, FastAPI, and Discord.py
</p>
