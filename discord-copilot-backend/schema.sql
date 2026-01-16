-- Discord Copilot Database Schema
-- Execute this in your Supabase SQL Editor

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- System Instructions Table
CREATE TABLE IF NOT EXISTS system_instructions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  instructions TEXT NOT NULL,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_by UUID REFERENCES auth.users(id)
);

-- PDF Documents Table
CREATE TABLE IF NOT EXISTS pdf_documents (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  filename TEXT NOT NULL,
  file_path TEXT NOT NULL,
  file_size INTEGER,
  upload_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  uploaded_by UUID REFERENCES auth.users(id),
  status TEXT DEFAULT 'processing' -- processing, completed, failed
);

-- Document Chunks Table (for RAG)
CREATE TABLE IF NOT EXISTS document_chunks (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  document_id UUID REFERENCES pdf_documents(id) ON DELETE CASCADE,
  chunk_text TEXT NOT NULL,
  chunk_index INTEGER,
  page_number INTEGER,
  embedding vector(1536), -- Dimension for OpenAI text-embedding-3-small
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index for vector similarity search
CREATE INDEX IF NOT EXISTS document_chunks_embedding_idx 
ON document_chunks USING ivfflat (embedding vector_cosine_ops);

-- Conversation Memory Table
CREATE TABLE IF NOT EXISTS conversation_memory (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  summary TEXT,
  last_updated TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  message_count INTEGER DEFAULT 0
);

-- Allowed Channels Table
CREATE TABLE IF NOT EXISTS allowed_channels (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  channel_id TEXT UNIQUE NOT NULL,
  channel_name TEXT,
  added_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  added_by UUID REFERENCES auth.users(id)
);

-- Insert default system instruction
INSERT INTO system_instructions (instructions, updated_at)
VALUES ('You are a helpful Discord assistant. Answer questions clearly and concisely.', NOW())
ON CONFLICT DO NOTHING;

-- Insert default conversation memory
INSERT INTO conversation_memory (summary, message_count)
VALUES ('No conversation history yet.', 0)
ON CONFLICT DO NOTHING;

-- RPC function for vector similarity search (callable via REST API)
CREATE OR REPLACE FUNCTION search_documents(
  query_embedding vector(1536),
  match_count int DEFAULT 5
)
RETURNS TABLE (
  chunk_text text,
  page_number int,
  filename text,
  similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT 
    c.chunk_text,
    c.page_number,
    d.filename,
    1 - (c.embedding <=> query_embedding) as similarity
  FROM document_chunks c
  JOIN pdf_documents d ON c.document_id = d.id
  WHERE d.status = 'completed'
  ORDER BY c.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
