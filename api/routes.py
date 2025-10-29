"""
API routes for Anthropomorphic AI
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    version: str

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(status="healthy", version="1.0.0")

@router.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Anthropomorphic AI API", "status": "running"}