"""Main application module for smart-qa-portal."""

import logging
from typing import Optional, Dict, Any
from fastapi import FastAPI, HTTPException, Request, status
from pydantic import BaseModel, Field
import uvicorn
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Smart Qa Portal",
    description="An AI-powered Q&A portal that helps users find accurate answers to technical questions by leveraging a curated knowledge base and machine learning models. The system can automatically categorize questions, provide relevant documentation links, and offer step-by-step troubleshooting guidance.",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Request/Response Models
class HealthResponse(BaseModel):
    """Health check response model."""
    status: str = Field(..., description="Application status (healthy/unhealthy)")
    version: str = Field(..., description="Application version")
    healthy: bool = Field(..., description="Health status boolean")
    timestamp: str = Field(..., description="Check timestamp")

class RequestData(BaseModel):
    """Request model for processing endpoint."""
    input_text: str = Field(..., min_length=1, max_length=10000, description="Input text to process")
    options: Optional[Dict[str, Any]] = Field(default=None, description="Processing options")

class ResponseData(BaseModel):
    """Response model for processing endpoint."""
    output: str = Field(..., description="Processed output")
    status: str = Field(..., description="Operation status")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Response metadata")

# Health check endpoint
@app.get("/health", response_model=HealthResponse, status_code=status.HTTP_200_OK)
async def health_check():
    """Check application health and readiness."""
    logger.info("Health check endpoint called")
    return HealthResponse(
        status="healthy",
        version="0.1.0",
        healthy=True,
        timestamp=datetime.now().isoformat()
    )

# Main processing endpoint
@app.post("/process", response_model=ResponseData, status_code=status.HTTP_200_OK)
async def process_data(request: RequestData):
    """
    Process input data using application logic.
    
    Args:
        request: Request with input_text and optional processing options
        
    Returns:
        ResponseData: Processed output and status information
        
    Raises:
        HTTPException: If validation or processing fails
    """
    try:
        # Validate input
        if not request.input_text or not request.input_text.strip():
            logger.warning("Empty input received")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Input text cannot be empty"
            )
        
        # Log processing request
        input_length = len(request.input_text)
        logger.info(f"Processing input of length: {input_length}")
        
        # Process the input text
        processed = request.input_text.upper()
        output = f"Processed {input_length} characters: {processed[:50]}..."
        
        logger.info("Processing completed successfully")
        
        return ResponseData(
            output=output,
            status="success",
            metadata={
                "input_length": input_length,
                "output_length": len(output),
                "processed_at": datetime.now().isoformat(),
                "options": request.options
            }
        )
        
    except HTTPException as e:
        logger.error(f"HTTP error: {e.detail}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during processing: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during processing"
        )

# Middleware for request/response logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming HTTP requests and responses."""
    logger.info(f"Incoming: {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        logger.info(f"Response: {response.status_code} for {request.url.path}")
        return response
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise

# Root endpoint
@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    """Root endpoint with API information and links."""
    return {
        "name": "smart-qa-portal",
        "description": "An AI-powered Q&A portal that helps users find accurate answers to technical questions by leveraging a curated knowledge base and machine learning models. The system can automatically categorize questions, provide relevant documentation links, and offer step-by-step troubleshooting guidance.",
        "version": "0.1.0",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "process": "/process"
        },
        "status": "running"
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    logger.info("Application startup initiated")
    logger.info(f"Service: smart-qa-portal v0.1.0")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    logger.info("Application shutdown initiated")

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting smart-qa-portal FastAPI application")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

# Update 1: Development iteration 1
