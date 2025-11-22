from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from web.api import chat, stats, ingest

app = FastAPI(title="ChatGPT Data Extractor")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routers
app.include_router(chat.router, prefix="/api")
app.include_router(stats.router, prefix="/api")
app.include_router(ingest.router, prefix="/api")

# Mount static files (Frontend)
# We will build the frontend to 'web/static' later
static_path = Path(__file__).parent / "static"
if static_path.exists():
    app.mount("/", StaticFiles(directory=str(static_path), html=True), name="static")
