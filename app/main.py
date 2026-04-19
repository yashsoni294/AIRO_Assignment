import logging
from fastapi import FastAPI
from app.api.routes import router as api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

logger.info("Starting Text-to-SQL API application")

app = FastAPI(
    title="Text-to-SQL API",
    description="LangGraph + LangChain SQL Toolkit Text to SQL system",
    version="1.0.0"
)

# Include API routes
logger.info("Including API routes with prefix /api")
app.include_router(api_router, prefix="/api")

@app.get("/")
def root():
    logger.info("Root endpoint accessed")
    return {"message": "Text-to-SQL API is running."}
