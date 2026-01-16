from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, BackgroundTasks
from pydantic import BaseModel
from api.middleware.auth import get_current_user
from db.supabase_client import get_supabase
from services.pdf_processor import process_pdf_document
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])


class DocumentResponse(BaseModel):
    id: str
    filename: str
    file_path: str
    file_size: int | None
    upload_date: datetime
    uploaded_by: str | None
    status: str


@router.get("/list", response_model=list[DocumentResponse])
async def list_documents(current_user: dict = Depends(get_current_user)):
    """
    List all uploaded PDF documents
    """
    supabase = get_supabase()
    
    try:
        response = supabase.table("pdf_documents").select("*").order("upload_date", desc=True).execute()
        return response.data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch documents: {str(e)}")


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Upload a PDF document for processing
    """
    # Validate file type
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Validate file size (10MB max)
    content = await file.read()
    file_size = len(content)
    max_size = 10 * 1024 * 1024  # 10MB
    
    if file_size > max_size:
        raise HTTPException(status_code=400, detail="File size exceeds 10MB limit")
    
    supabase = get_supabase()
    
    try:
        # Generate unique filename
        doc_id = str(uuid.uuid4())
        storage_path = f"pdfs/{doc_id}_{file.filename}"
        
        # Upload to Supabase Storage
        storage_response = supabase.storage.from_("documents").upload(
            storage_path,
            content,
            {"content-type": "application/pdf"}
        )
        
        # Create database record
        db_response = supabase.table("pdf_documents").insert({
            "id": doc_id,
            "filename": file.filename,
            "file_path": storage_path,
            "file_size": file_size,
            "uploaded_by": current_user["user_id"],
            "status": "processing"
        }).execute()
        
        if not db_response.data:
            raise HTTPException(status_code=500, detail="Failed to create document record")
        
        # Process PDF in background
        background_tasks.add_task(process_pdf_document, doc_id, storage_path, content)
        
        return db_response.data[0]
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload document: {str(e)}")


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a PDF document and its chunks (CASCADE)
    """
    supabase = get_supabase()
    
    try:
        # Get document info
        doc_response = supabase.table("pdf_documents").select("file_path").eq("id", document_id).execute()
        
        if not doc_response.data:
            raise HTTPException(status_code=404, detail="Document not found")
        
        file_path = doc_response.data[0]["file_path"]
        
        # Delete from storage
        try:
            supabase.storage.from_("documents").remove([file_path])
        except:
            pass  # Continue even if storage deletion fails
        
        # Delete from database (chunks will be deleted via CASCADE)
        delete_response = supabase.table("pdf_documents").delete().eq("id", document_id).execute()
        
        if not delete_response.data:
            raise HTTPException(status_code=404, detail="Document not found")
        
        return {"message": "Document deleted successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete document: {str(e)}")
