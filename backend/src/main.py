"""
FastAPI application for AI-Native Textbook Generation System.

This is the main entry point for the backend API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import generation, rag, textbooks
from .core.config import settings
from .core.security import initialize_firebase

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Backend API for AI-Native Textbook Generation with RAG Chatbot",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize services on application startup."""
    # Initialize Firebase
    try:
        initialize_firebase()
    except Exception as e:
        print(f"Warning: Firebase initialization failed: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    pass


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "docs": "/docs",
    }


@app.get("/health", tags=["Health"])
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


# Include routers
app.include_router(textbooks.router, prefix="/api/textbooks")
app.include_router(generation.router, prefix="/api/generation")
app.include_router(rag.router, prefix="/api")
