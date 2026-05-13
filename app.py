from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from database import create_tables
from routes import include_routes
from seed_data import seed_demo_data

# Initialize app
app = FastAPI(
    title="AI Smart Business Assistant",
    description="AI-powered business management system for small business owners",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    create_tables()
    print("Database tables created successfully")

# Include all routers
include_routes(app)

# Health check endpoint
@app.get("/")
def home():
    """Health check endpoint"""
    return {
        "message": "AI Smart Business Assistant API",
        "status": "running",
        "version": "1.0.0"
    }

# Seed demo data endpoint (for development)
@app.post("/api/seed-demo-data")
def seed_data(user_id: int = None):
    """Seed demo data for testing (development only)"""
    try:
        seed_demo_data(user_id)
        if user_id is not None:
            return {"message": f"Demo data seeded successfully for user_id={user_id}"}
        return {"message": "Demo data seeded successfully for all demo users"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
