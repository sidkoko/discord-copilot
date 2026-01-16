import PyPDF2
import pdfplumber
import io
from typing import List, Tuple
from db.supabase_client import get_supabase
from services.rag_service import generate_embeddings, chunk_text
from config import get_settings
import logging

logger = logging.getLogger(__name__)
settings = get_settings()


def extract_text_from_pdf(pdf_content: bytes) -> List[Tuple[int, str]]:
    """
    Extract text from PDF and return list of (page_number, text) tuples.
    Tries PyPDF2 first, then falls back to pdfplumber for better extraction.
    """
    pages = []
    
    try:
        # Try PyPDF2 first (faster)
        pdf_file = io.BytesIO(pdf_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            
            if text.strip():
                pages.append((page_num + 1, text))
        
        # If PyPDF2 extracted text, return it
        if pages:
            logger.info(f"Extracted text using PyPDF2: {len(pages)} pages")
            return pages
        
        # Fallback to pdfplumber for better extraction
        logger.info("PyPDF2 extracted no text, trying pdfplumber...")
        pdf_file = io.BytesIO(pdf_content)
        
        with pdfplumber.open(pdf_file) as pdf:
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                
                if text and text.strip():
                    pages.append((page_num + 1, text))
        
        if pages:
            logger.info(f"Extracted text using pdfplumber: {len(pages)} pages")
        
        return pages
    
    except Exception as e:
        logger.error(f"Failed to extract text from PDF: {str(e)}")
        raise


async def process_pdf_document(document_id: str, storage_path: str, pdf_content: bytes):
    """
    Background task to process PDF: extract text, chunk, embed, and store
    """
    supabase = get_supabase()
    
    try:
        logger.info(f"Processing document {document_id}")
        
        # 1. Extract text from PDF
        pages = extract_text_from_pdf(pdf_content)
        
        if not pages:
            # Update status to failed
            supabase.table("pdf_documents").update({
                "status": "failed"
            }).eq("id", document_id).execute()
            logger.error(f"No text extracted from document {document_id}")
            return
        
        logger.info(f"Extracted {len(pages)} pages from document {document_id}")
        
        # 2. Chunk text
        all_chunks = []
        chunk_index = 0
        
        for page_num, page_text in pages:
            chunks = chunk_text(page_text, settings.chunk_size, settings.chunk_overlap)
            
            for chunk in chunks:
                all_chunks.append({
                    "text": chunk,
                    "page_number": page_num,
                    "chunk_index": chunk_index
                })
                chunk_index += 1
        
        logger.info(f"Created {len(all_chunks)} chunks from document {document_id}")
        
        # 3. Generate embeddings for all chunks
        chunk_texts = [c["text"] for c in all_chunks]
        embeddings = await generate_embeddings(chunk_texts)
        
        logger.info(f"Generated {len(embeddings)} embeddings for document {document_id}")
        
        # 4. Store chunks with embeddings in database using Supabase REST API
        # Prepare data for batch insert
        chunks_to_insert = []
        for i, chunk_data in enumerate(all_chunks):
            chunks_to_insert.append({
                "document_id": document_id,
                "chunk_text": chunk_data["text"],
                "chunk_index": chunk_data["chunk_index"],
                "page_number": chunk_data["page_number"],
                "embedding": embeddings[i]  # List of floats
            })
        
        # Insert chunks in batches (Supabase has limits)
        batch_size = 50
        for i in range(0, len(chunks_to_insert), batch_size):
            batch = chunks_to_insert[i:i + batch_size]
            supabase.table("document_chunks").insert(batch).execute()
        
        logger.info(f"Stored {len(all_chunks)} chunks for document {document_id}")
        
        # 5. Update document status to completed
        supabase.table("pdf_documents").update({
            "status": "completed"
        }).eq("id", document_id).execute()
        
        logger.info(f"Successfully processed document {document_id}")
    
    except Exception as e:
        logger.error(f"Failed to process document {document_id}: {str(e)}")
        
        # Update status to failed
        try:
            supabase.table("pdf_documents").update({
                "status": "failed"
            }).eq("id", document_id).execute()
        except:
            pass
