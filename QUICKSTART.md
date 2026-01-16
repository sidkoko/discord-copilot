# Discord Copilot - Quick Start Guide 🚀

Get your Discord Copilot running in **15 minutes**!

## Prerequisites Checklist

Before starting, create accounts and get keys for:

- [ ] [Supabase](https://supabase.com) - Database (free tier)
- [ ] [Discord Developer Portal](https://discord.com/developers) - Bot token
- [ ] [OpenAI](https://platform.openai.com) - Embeddings API key
- [ ] [Google AI Studio](https://makersuite.google.com/app/apikey) - Gemini API key (free tier available)

---

## 🏃 Quick Setup (Local Development)

### Step 1: Clone & Setup (2 minutes)

```bash
cd /Users/siddhantkokate/Desktop/figmenta-brief-1

# Backend setup
cd discord-copilot-backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env

# Frontend setup (in new terminal)
cd discord-copilot-admin
npm install
cp env.example.txt .env.local
```

### Step 2: Configure Supabase (3 minutes)

1. Create project at [supabase.com](https://supabase.com)
2. Go to SQL Editor → New Query
3. Copy & run `discord-copilot-backend/schema.sql`
4. Create Storage bucket named `documents` (Storage → New Bucket)
5. Get credentials from Settings → API:
   - Project URL
   - `anon` public key  
   - `service_role` key
   - Database URL (Settings → Database → URI)

### Step 3: Create Discord Bot (2 minutes)

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. New Application → "Discord Copilot"
3. Bot tab → Add Bot
4. Enable "Message Content Intent" under Privileged Gateway Intents
5. Reset Token → Copy bot token
6. OAuth2 → URL Generator:
   - Scopes: `bot`
   - Permissions: Send Messages, Read Messages, Read Message History
7. Copy URL and invite bot to your server

### Step 4: Get API Keys (2 minutes)

1. **OpenAI**: [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - Create new secret key
   - Add $5 credit to account

2. **Gemini**: [makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
   - Create API key (free tier available)

### Step 5: Configure Environment (3 minutes)

**Backend** (`discord-copilot-backend/.env`):
```env
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=eyJxxx...
SUPABASE_ANON_KEY=eyJxxx...
DATABASE_URL=postgresql://postgres:[password]@[host]:5432/postgres

DISCORD_BOT_TOKEN=MTxxx...

OPENAI_API_KEY=sk-xxx...
GEMINI_API_KEY=AIxxx...
LLM_PROVIDER=gemini
```

**Frontend** (`discord-copilot-admin/.env.local`):
```env
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJxxx...
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Step 6: Run Everything (1 minute)

**Terminal 1 - Backend:**
```bash
cd discord-copilot-backend
source venv/bin/activate
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd discord-copilot-admin
npm run dev
```

You should see:
- ✅ Backend: http://localhost:8000 (API docs at /docs)
- ✅ Frontend: http://localhost:3000
- ✅ Discord bot online in your server

### Step 7: First Test (2 minutes)

1. **Create Account**:
   - Open http://localhost:3000
   - Click "Sign up"
   - Create account with email

2. **Configure Bot**:
   - Login to dashboard
   - Go to "System Instructions"
   - Add: "You are a friendly Discord assistant. Be helpful and concise."
   - Save

3. **Add Channel**:
   - Go to "Channels"
   - In Discord: Enable Developer Mode (Settings → Advanced)
   - Right-click your channel → Copy Channel ID
   - Paste in dashboard and add

4. **Test Bot**:
   - In Discord channel, type: `@YourBot Hello!`
   - Bot should respond!

---

## 🧪 Test RAG Feature (3 minutes)

1. **Upload PDF**:
   - Dashboard → Knowledge Base
   - Upload any PDF (max 10MB)
   - Wait for status: "completed"

2. **Ask Question**:
   - In Discord: `@YourBot What does the document say about [topic]?`
   - Bot uses PDF content to answer!

3. **Check Memory**:
   - Have a conversation (3-4 exchanges)
   - Dashboard → Memory
   - See conversation summary!

---

## 🎯 Common Issues & Fixes

### Bot Not Responding

**Issue**: Bot online but doesn't reply
- ❌ Channel not in allow-list → Add it in dashboard
- ❌ Message Content Intent not enabled → Enable in Discord Dev Portal
- ❌ Didn't mention bot → Must use `@YourBot` to trigger

### PDF Upload Fails

**Issue**: Upload button doesn't work
- ❌ Storage bucket missing → Create "documents" bucket in Supabase
- ❌ Wrong key → Use `service_role` key (not anon) in backend .env
- ❌ File too large → Max 10MB

### Authentication Error

**Issue**: Can't login to dashboard
- ❌ Email confirmation required → Disable in Supabase: Auth → Settings → Email Confirmations
- ❌ Wrong Supabase credentials → Verify URL and anon key match
- ❌ CORS error → Backend must be running on :8000

---

## 📚 Next Steps

Once everything works locally:

1. ✅ **Customize** system instructions for your use case
2. ✅ **Upload** domain-specific PDFs
3. ✅ **Test** thoroughly with various questions
4. 🚀 **Deploy** following [DEPLOYMENT.md](./DEPLOYMENT.md) guide

---

## 💡 Pro Tips

- **Switch LLM**: Change `LLM_PROVIDER` in backend .env (gemini/claude/gpt)
- **Better RAG**: Upload focused, well-structured PDFs
- **Save costs**: Use Gemini free tier for testing
- **Debug**: Check backend terminal for detailed logs
- **Memory**: Reset when changing topics for better context

---

## 🆘 Need Help?

1. Check logs in backend terminal
2. Review [README.md](./README.md) for full documentation
3. See [DEPLOYMENT.md](./DEPLOYMENT.md) for production setup

**Common Log Locations**:
- Backend: Terminal running `python main.py`
- Frontend: Browser console (F12)
- Supabase: Dashboard → Logs

---

**Enjoy your Discord Copilot! 🤖✨**
