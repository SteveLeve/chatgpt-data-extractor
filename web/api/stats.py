from fastapi import APIRouter
from web.services import manager

router = APIRouter()

@router.get("/stats")
async def get_stats():
    return {
        "ingestion_status": manager.ingestion_status,
        "ingestion_progress": manager.ingestion_progress,
        "ingestion_message": manager.ingestion_message,
        "agent_initialized": manager.agent is not None
    }
