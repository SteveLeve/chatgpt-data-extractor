import asyncio
from typing import Optional
from llama_index.core.chat_engine.types import BaseChatEngine
from chat_rag.query import setup_agent

class ServiceManager:
    _instance = None
    
    def __init__(self):
        self.agent: Optional[BaseChatEngine] = None
        self.ingestion_status: str = "idle"
        self.ingestion_progress: float = 0.0
        self.ingestion_message: str = ""
        
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
        
    def get_agent(self) -> BaseChatEngine:
        if self.agent is None:
            # Initialize agent lazily
            self.agent = setup_agent()
        return self.agent
        
    def set_ingestion_status(self, status: str, progress: float = 0.0, message: str = ""):
        self.ingestion_status = status
        self.ingestion_progress = progress
        self.ingestion_message = message

manager = ServiceManager()
