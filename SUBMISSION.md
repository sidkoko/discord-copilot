# Discord Copilot - Project Submission

**Submitted by:** Siddhant Kokate  
**Date:** January 18, 2026  
**Project:** Discord Copilot – AI-Powered Discord Bot with Admin Dashboard

---

## 🔗 Deployment Links

| Component | URL |
|-----------|-----|
| 🌐 **Admin Dashboard** | [https://discord-copilot-admin.vercel.app](https://discord-copilot-admin.vercel.app) |
| 🔧 **Backend API** | [https://discord-copilot-api.onrender.com](https://discord-copilot-api.onrender.com) |
| 📦 **Source Code** | [https://github.com/sidkoko/discord-copilot](https://github.com/sidkoko/discord-copilot) |
| 🤖 **Discord Bot Invite** | [Add Bot to Server](https://discord.com/oauth2/authorize?client_id=1461262484726874142&permissions=274878024704&integration_type=0&scope=bot+applications.commands) |
| 🎬 **Demo Video** | [Watch Demo](https://drive.google.com/file/d/1gHnjVXFqX33B7Wh9LNqD6mRV8izETLVb/view?usp=drive_link) |

> **Note:** The Discord bot is integrated into the backend and runs continuously once the backend is deployed. You can test the bot by inviting it to your Discord server using the provided invite link.

### 🤖 How to Invite the Bot to Your Server

1. Click the **"Add Bot to Server"** link above
2. Select the Discord server you want to add the bot to (you must have "Manage Server" permission // you must be owner of the server)
3. Click **"Authorize"** and complete the captcha
4. Go back to the **Admin Dashboard** and add your channel ID:
   - In Discord, right-click on the channel where you want the bot → **Copy Channel ID**
   - Go to Dashboard → **Channel Management** → Paste and add the channel
5. Start chatting! Mention the bot: `@DiscordCopilot Hello!`

> 💡 **Tip:** If you don't see "Copy Channel ID", enable Developer Mode in Discord: User Settings → App Settings → Advanced → Developer Mode

---

## 📋 Project Overview

**Discord Copilot** is a full-stack, production-ready AI assistant for Discord servers. It combines a modern admin dashboard with a powerful backend that includes conversational AI, RAG (Retrieval-Augmented Generation) for domain-specific knowledge, and intelligent conversation memory.

### ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🎛️ **Admin Dashboard** | Beautiful Next.js dashboard with user authentication for managing the entire system |
| 📚 **RAG Knowledge Base** | Upload PDFs to give the bot domain-specific knowledge using vector embeddings |
| 🧠 **Conversation Memory** | Bot remembers context across conversations with rolling summaries |
| 📢 **Channel Management** | Control which Discord channels the bot responds in via an allow-list |
| ⚙️ **System Instructions** | Define the bot's personality, behavior, and response style |
| 🔄 **Multi-LLM Support** | Works with OpenRouter (GPT-4, Claude, Gemini, Llama, and more) |

---

## 🏗️ Tech Stack

### Frontend (Admin Dashboard)
- **Framework:** Next.js 14 with App Router
- **Language:** TypeScript
- **Styling:** Tailwind CSS with custom dark theme
- **Authentication:** Supabase Auth (email/password)
- **Deployment:** Vercel

### Backend (API + Discord Bot)
- **Framework:** FastAPI (Python)
- **Discord Integration:** discord.py
- **AI/LLM:** OpenRouter API
- **Embeddings:** OpenAI text-embedding-3-small
- **Vector Search:** pgvector (PostgreSQL extension)
- **Deployment:** Render (Docker container)

### Database & Storage
- **Database:** PostgreSQL with pgvector (Supabase)
- **File Storage:** Supabase Storage (for PDF documents)
- **Vector Dimensions:** 1536-dimensional embeddings

---

## 🖼️ Screenshots

### Dashboard Overview
> The admin dashboard provides a central hub for managing all aspects of the Discord bot.

### System Instructions
> Define how your bot should behave, its personality, and response patterns.

### Knowledge Base (RAG)
> Upload PDF documents that the bot can reference when answering user questions.

### Conversation Memory
> View and manage the bot's memory of ongoing conversations.

### Channel Management
> Control which Discord channels the bot is allowed to respond in.

---

## 🔑 Key Technical Achievements

1. **Full RAG Pipeline Implementation**
   - PDF text extraction with OCR fallback
   - Semantic chunking with configurable overlap
   - Vector embeddings using OpenAI's text-embedding-3-small
   - Similarity search using pgvector's cosine distance

2. **Conversation Memory System**
   - Rolling memory with automatic summarization
   - Context-aware responses based on conversation history
   - Memory persistence in database

3. **Multi-LLM Architecture**
   - Unified OpenRouter integration
   - Support for GPT-4, Claude, Gemini, Llama models
   - Easy model switching via environment variable

4. **Production-Ready Deployment**
   - Dockerized backend for consistent deployments
   - Separate frontend/backend architecture
   - Secure environment variable management

---

## 🎯 How to Test

### Testing the Admin Dashboard
1. Visit the Vercel deployment link
2. Sign up for a new account 
3. Explore the dashboard pages:
   - System Instructions
   - Knowledge Base
   - Conversation Memory (clear this before/after you save new instructions, the bot uses this for context!) 
   - Channel Management

### Testing the Discord Bot
1. Join the demo Discord server (link available upon request)
2. Go to an allowed channel
3. Mention the bot: `@DiscordCopilot Hello!`
4. Ask questions about uploaded knowledge: `@DiscordCopilot What does the documentation say about...?`

### API Health Check
```bash
curl https://discord-copilot-api.onrender.com/health
```
Expected response:
```json
{"status": "healthy", "service": "discord-copilot-api"}
```

---

## 📂 Project Structure

```
discord-copilot/
├── discord-copilot-admin/      # Next.js 14 Admin Dashboard
│   ├── app/                    
│   │   ├── auth/               # Login & Signup pages
│   │   └── dashboard/          # Protected admin pages
│   │       ├── instructions/   # Bot personality config
│   │       ├── knowledge/      # PDF upload & management
│   │       ├── memory/         # Conversation context viewer
│   │       └── channels/       # Discord channel allow-list
│   ├── components/             # Reusable React components
│   └── lib/                    # Utilities & Supabase client
│
├── discord-copilot-backend/    # FastAPI + Discord.py Backend
│   ├── api/routes/             # REST API endpoints
│   ├── bot/                    # Discord bot logic
│   │   └── discord_bot.py      # Main bot implementation
│   ├── services/               
│   │   ├── rag_service.py      # Vector search & embeddings
│   │   └── pdf_processor.py    # PDF text extraction
│   └── db/                     # Database client
│
├── README.md                   # Project documentation
├── DEPLOYMENT.md               # Detailed deployment guide
└── QUICKSTART.md               # Quick start guide
```

---

## 💡 Future Improvements (Roadmap)

- [ ] Add support for more document types (Word, TXT, Markdown)
- [ ] Implement webhook notifications for document processing
- [ ] Add analytics dashboard for bot usage statistics
- [ ] Multi-tenant support for managing multiple Discord servers
- [ ] Rate limiting and usage quotas

---

## 📞 Contact

**Siddhant Kokate**  
Email: sidkokate25@gmail.com  
GitHub: [@sidkoko](https://github.com/sidkoko)

---

*Thank you for reviewing this project! I'm happy to provide a demo or answer any questions.*
