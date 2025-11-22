import shutil
import zipfile
from pathlib import Path
from fastapi import APIRouter, UploadFile, BackgroundTasks, HTTPException
from web.services import manager
from chat_rag.ingest import ingest_data

router = APIRouter()

def run_ingestion_task(input_dir: Path):
    try:
        manager.set_ingestion_status("running", 0.0, "Starting ingestion...")
        # Note: ingest_data is currently synchronous and prints to stdout.
        # In a real app, we'd want to capture progress callbacks.
        # For now, we just mark it as running/done.
        ingest_data(input_dir)
        manager.set_ingestion_status("idle", 1.0, "Ingestion complete")
    except Exception as e:
        manager.set_ingestion_status("error", 0.0, str(e))

@router.post("/upload")
async def upload_file(file: UploadFile):
    if not file.filename.endswith('.zip'):
        raise HTTPException(status_code=400, detail="Only .zip files are allowed")
    
    upload_path = Path("source-data.zip")
    with upload_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {"message": "File uploaded successfully"}

@router.post("/ingest")
async def trigger_ingest(background_tasks: BackgroundTasks):
    if manager.ingestion_status == "running":
        raise HTTPException(status_code=400, detail="Ingestion already in progress")
        
    # Extract zip
    zip_path = Path("source-data.zip")
    extract_dir = Path("source-data")
    
    if not zip_path.exists():
         raise HTTPException(status_code=400, detail="No source data found. Please upload first.")

    if extract_dir.exists():
        shutil.rmtree(extract_dir)
    extract_dir.mkdir()
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
        
    background_tasks.add_task(run_ingestion_task, extract_dir)
    
    return {"message": "Ingestion started"}
