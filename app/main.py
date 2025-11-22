from fastapi import FastAPI
from app.routers import questions, answers
from app.logging_config import setup_logging
import logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="Q&A API", version="1.0.0")

app.include_router(questions.router, prefix="/api/v1")
app.include_router(answers.router, prefix="/api/v1")

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "Q&A API Service"}

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "healthy"}