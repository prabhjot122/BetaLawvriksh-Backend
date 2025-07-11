import os
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from database import verify_database_connection
from schemas import HealthResponse, HomeResponse, ErrorResponse
from routers import users, feedback, admin

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up FastAPI application...")
    verify_database_connection()
    yield
    # Shutdown
    logger.info("Shutting down FastAPI application...")


# Create FastAPI app
app = FastAPI(
    title="LawVriksh Feedback API",
    description="API for user registration and feedback collection",
    version="2.0.0",
    lifespan=lifespan
)

# CORS configuration
cors_origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:5175",
    "https://lawvrikshbetapage.onrender.com",
    "https://preorder.lawvriksh.com/",
    "https://lawvriksh.com"

]

# Add production origins from environment variable
if os.environ.get('CORS_ORIGINS'):
    production_origins = os.environ.get('CORS_ORIGINS').split(',')
    cors_origins.extend([origin.strip() for origin in production_origins])

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for templates
app.mount("/static", StaticFiles(directory="templates"), name="static")

# Include routers
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(feedback.router, prefix="/api", tags=["feedback"])
app.include_router(admin.router, prefix="/api", tags=["admin"])


@app.get("/", response_model=HomeResponse)
async def home():
    """Root endpoint"""
    return HomeResponse(
        message="LawVriksh Feedback API",
        version="2.0.0",
        endpoints={
            'health': '/api/health',
            'register': '/api/register',
            'feedback': '/api/feedback',
            'admin': '/admin'
        }
    )


@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard():
    """Admin dashboard for managing data and downloading Excel files"""
    try:
        with open("templates/admin.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Admin dashboard not found")


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow()
    )


@app.get("/favicon.ico")
async def favicon():
    """Handle favicon requests to prevent 404 errors"""
    return JSONResponse(status_code=204, content=None)


@app.exception_handler(404)
async def not_found_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=404,
        content={"error": "Endpoint not found"}
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": "An unexpected error occurred"}
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=debug,
        log_level="info"
    )
