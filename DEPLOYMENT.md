# Discord Copilot - Deployment Guide

## 📋 Pre-Deployment Checklist

Before deploying, ensure you have:

- [x] Completed local development and testing
- [ ] Supabase project created and configured
- [ ] Discord bot created in Developer Portal
- [ ] All API keys ready (OpenAI, Gemini/Claude)
- [ ] GitHub repository for code
- [ ] Vercel account (free tier works)
- [ ] Render or Railway account

---

## 🗄️ Step 1: Supabase Setup

### 1.1 Create Supabase Project

1. Go to [supabase.com](https://supabase.com) and sign up/login
2. Click "New Project"
3. Choose organization and set:
   - **Project name**: discord-copilot
   - **Database password**: (save this!)
   - **Region**: Choose closest to your users
4. Wait for project to finish setting up (~2 minutes)

### 1.2 Run SQL Schema

1. Go to SQL Editor in Supabase dashboard
2. Click "New Query"
3. Copy contents of `discord-copilot-backend/schema.sql`
4. Paste and click "Run"
5. Verify all tables created (check Tables tab)

### 1.3 Create Storage Bucket

1. Go to Storage in Supabase dashboard
2. Click "Create Bucket"
3. Name: `documents`
4. Public: **No** (keep private)
5. Click "Create"

### 1.4 Get Credentials

Go to Settings → API and copy:
- Project URL
- `anon` public key
- `service_role` secret key

Also get database URL:
- Settings → Database → Connection String → URI
- Replace `[YOUR-PASSWORD]` with your database password

---

## 🤖 Step 2: Discord Bot Setup

### 2.1 Create Application

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application"
3. Name: "Discord Copilot" (or your choice)
4. Accept terms and create

### 2.2 Create Bot

1. Go to "Bot" tab
2. Click "Add Bot" → "Yes, do it!"
3. Under "Privileged Gateway Intents", enable:
   - ✅ Message Content Intent
   - ✅ Server Members Intent
4. Click "Reset Token" and copy your bot token (save it!)

### 2.3 Invite Bot to Server

1. Go to OAuth2 → URL Generator
2. Select scopes:
   - ✅ bot
3. Select bot permissions:
   - ✅ Send Messages
   - ✅ Read Messages/View Channels
   - ✅ Read Message History
4. Copy generated URL
5. Open in browser and add bot to your server

---

## 🚀 Step 3: Deploy Backend (Render)

### 3.1 Prepare Code

1. Ensure all code is committed to GitHub:
```bash
cd discord-copilot-backend
git init
git add .
git commit -m "Initial backend setup"
git remote add origin https://github.com/yourusername/discord-copilot-backend.git
git push -u origin main
```

### 3.2 Create Render Service

1. Go to [render.com](https://render.com) and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: discord-copilot-api
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free (or starter for better performance)

### 3.3 Add Environment Variables

Add these in Render's Environment tab:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
SUPABASE_ANON_KEY=your_anon_key
DATABASE_URL=your_postgres_connection_string

DISCORD_BOT_TOKEN=your_discord_bot_token

OPENAI_API_KEY=your_openai_key
GEMINI_API_KEY=your_gemini_key
LLM_PROVIDER=gemini

EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIMENSIONS=1536
CHUNK_SIZE=600
CHUNK_OVERLAP=100
TOP_K_RETRIEVAL=5
MAX_MEMORY_LENGTH=500
```

### 3.4 Deploy

1. Click "Create Web Service"
2. Wait for deployment (~5-10 minutes)
3. Once live, copy your service URL (e.g., `https://discord-copilot-api.onrender.com`)
4. Test health endpoint: `https://your-url.onrender.com/health`

**Note**: Free tier spins down after 15 minutes of inactivity. First request after spin-down takes ~30 seconds.

---

## 🎨 Step 4: Deploy Frontend (Vercel)

### 4.1 Prepare Code

```bash
cd discord-copilot-admin
# Ensure .env.local is NOT committed (it's in .gitignore)
git init
git add .
git commit -m "Initial frontend setup"
git remote add origin https://github.com/yourusername/discord-copilot-admin.git
git push -u origin main
```

### 4.2 Create Vercel Project

1. Go to [vercel.com](https://vercel.com) and sign up/login
2. Click "Add New..." → "Project"
3. Import your GitHub repository
4. Configure:
   - **Framework Preset**: Next.js (auto-detected)
   - **Root Directory**: `./` (or `discord-copilot-admin` if monorepo)
   - **Build Command**: `npm run build` (default)
   - **Output Directory**: `.next` (default)

### 4.3 Add Environment Variables

In Vercel's project settings, add:

```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
NEXT_PUBLIC_API_URL=https://your-render-backend-url.onrender.com
```

**Important**: Replace the API URL with your actual Render service URL!

### 4.4 Deploy

1. Click "Deploy"
2. Wait for build and deployment (~2-3 minutes)
3. Once live, you'll get a URL like `https://discord-copilot-admin.vercel.app`

### 4.5 Optional: Add Custom Domain

1. Go to Project Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions

---

## ✅ Step 5: Verify Deployment

### 5.1 Test Backend

1. Visit your Render URL + `/health`
2. Should see: `{"status": "healthy", "service": "discord-copilot-api"}`
3. Check logs in Render dashboard for Discord bot connection message

### 5.2 Test Frontend

1. Visit your Vercel URL
2. Sign up for a new account
3. Verify email confirmation (check Supabase Auth users)
4. Login to dashboard

### 5.3 End-to-End Test

1. **Update System Instructions**:
   - Go to System Instructions page
   - Enter bot personality
   - Save

2. **Upload PDF**:
   - Go to Knowledge Base
   - Upload a sample PDF
   - Wait for status to change to "completed"

3. **Add Discord Channel**:
   - Go to Channels page
   - Copy a Discord channel ID from your server
   - Add it to allow-list

4. **Test Bot**:
   - In Discord, in the allowed channel, mention your bot:
     ```
     @YourBot Hello! What can you do?
     ```
   - Bot should respond according to your instructions

5. **Test RAG**:
   - Ask a question about your uploaded PDF:
     ```
     @YourBot What does the document say about [topic]?
     ```
   - Bot should use knowledge from the PDF

6. **Check Memory**:
   - Have a multi-turn conversation
   - Go to Memory page in dashboard
   - Verify conversation is being tracked

---

## 🔧 Post-Deployment Configuration

### Enable Supabase Email Confirmations (Optional)

1. Supabase Dashboard → Authentication → Settings
2. Disable "Enable email confirmations" for easier testing
3. Or configure SMTP for production email delivery

### Set Up Monitoring

**Backend (Render)**:
- Check logs regularly in Render dashboard
- Set up health check alerts

**Frontend (Vercel)**:
- Vercel automatically monitors deployments
- Check Analytics tab for usage stats

### Configure CORS (if needed)

If you have custom domain issues, update CORS in `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Replace with your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🐛 Troubleshooting

### Bot Not Coming Online

- Check Render logs for errors
- Verify `DISCORD_BOT_TOKEN` is correct
- Ensure "Message Content Intent" is enabled in Discord Dev Portal

### PDF Upload Fails

- Check Supabase storage bucket "documents" exists
- Verify `SUPABASE_SERVICE_ROLE_KEY` (not anon key) is set in backend
- Check Render logs for detailed error

### Authentication Errors

- Verify Supabase URL and keys match in both frontend and backend
- Check that `SUPABASE_ANON_KEY` in frontend is correct
- Ensure `NEXT_PUBLIC_API_URL` points to your Render backend

### RAG Not Working

- Verify OpenAI API key is valid and has credits
- Check if PDF processing completed (status = "completed")
- Look at backend logs during query

---

## 💰 Cost Estimates

### Free Tier (Good for testing)

- **Supabase**: Free (500MB database, 1GB storage)
- **Render**: Free (spins down after 15 min inactivity)
- **Vercel**: Free (100GB bandwidth/month)
- **OpenAI**: ~$0.0001 per 1K tokens (embeddings)
- **Gemini**: Free tier available

**Total**: $0-5/month depending on API usage

### Production (Recommended)

- **Supabase**: $25/month (Pro plan)
- **Render**: $7/month (Starter instance, no spin-down)
- **Vercel**: Free (sufficient for most use cases)
- **OpenAI**: ~$5-20/month (depending on usage)
- **Gemini/Claude**: ~$10-30/month

**Total**: ~$50-100/month for stable production

---

## 🎉 You're Done!

Your Discord Copilot is now live! Here's what to do next:

1. ✅ Test all features thoroughly
2. 📝 Customize system instructions for your use case
3. 📚 Upload domain-specific PDFs
4. 💬 Invite users to your Discord server
5. 📊 Monitor usage and costs
6. 🚀 Scale as needed

Need help? Check logs in Render and Vercel dashboards!
