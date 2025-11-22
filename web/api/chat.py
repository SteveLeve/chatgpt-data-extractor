from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from web.services import manager
import asyncio

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

@router.post("/chat")
async def chat(request: ChatRequest):
    try:
        agent = manager.get_agent()
        
        # Create a generator for streaming response
        async def event_generator():
            response = await agent.astream_chat(request.message)
            async for token in response.async_response_gen():
                yield token
                
        return StreamingResponse(event_generator(), media_type="text/plain")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
