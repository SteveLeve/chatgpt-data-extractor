from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from web.services import manager
from llama_index.core.agent.workflow import AgentStream
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
            # Use workflow run method which returns a handler
            handler = agent.run(user_msg=request.message)
            
            # Iterate over events
            async for event in handler.stream_events():
                if isinstance(event, AgentStream):
                    yield event.delta
                
        return StreamingResponse(event_generator(), media_type="text/plain")
        
    except Exception as e:
        # Log the error for debugging
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))
