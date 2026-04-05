"""
Main entry point for the Host Pricing Assistant backend API.

This file creates the FastAPI application object and defines:
1. API metadata
2. CORS configuration so the React frontend can call the backend
3. A root route so we can confirm the API is running
4. A health route so we can quickly test backend health
5. Pricing routes so recommendation requests can be handled
6. Startup tasks so database tables can be created automatically
7. Database model imports so table metadata is registered before startup
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes_pricing import router as pricing_router
from app.core.database import create_db_and_tables
from app.models.recommendation import Recommendation


# Create the FastAPI application instance.
# This 'app' object is what the server will run.
app = FastAPI(
    title="Host Pricing Assistant API",
    description="Backend API for the Host Pricing Assistant project.",
    version="0.1.0",
)


# Add CORS middleware so the frontend running on a different origin
# can make requests to this backend during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include pricing routes so pricing-related endpoints become part
# of the main FastAPI application.
app.include_router(pricing_router)


@app.on_event("startup")
def on_startup():
    """
    Run startup tasks before the application begins handling requests.

    This startup function creates the database tables if they do not
    already exist.
    """
    create_db_and_tables()


@app.get("/")
def read_root():
    """
    Root route for the API.

    Returns:
        dict: A simple message confirming the API is running.
    """
    return {"message": "Host Pricing Assistant API is running"}


@app.get("/health")
def health_check():
    """
    Health check route.

    Returns:
        dict: A simple status response that can be used to verify
        the backend is up and responding correctly.
    """
    return {"status": "ok"}