import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend!"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from the backend API!"}

@app.get("/api/showcase/projects")
def get_showcase_projects():
    """Return a curated list of showcase projects and demos."""
    projects = [
        {
            "id": "ai-todo",
            "title": "AI-Powered Todo",
            "subtitle": "Natural language to tasks",
            "description": "Turn plain English into structured tasks, prioritize automatically, and track progress with a clean UI.",
            "tags": ["AI", "Tasks", "NLP"],
            "status": "featured",
            "metrics": {"stars": 4.9, "users": 1200},
        },
        {
            "id": "chat-realtime",
            "title": "Realtime Chat",
            "subtitle": "Typing indicators, presence, reactions",
            "description": "A delightful chat experience with message threading, reactions, and presence — optimized for low latency.",
            "tags": ["WebSockets", "UX", "Messaging"],
            "status": "production",
            "metrics": {"stars": 4.8, "users": 980},
        },
        {
            "id": "ecommerce-api",
            "title": "E‑commerce API",
            "subtitle": "Catalog, carts, checkout",
            "description": "Well-structured endpoints with validation and analytics hooks. Ready for storefronts and marketplaces.",
            "tags": ["API", "FastAPI", "Payments"],
            "status": "stable",
            "metrics": {"stars": 4.7, "users": 1520},
        },
    ]
    return {"projects": projects}

@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        # Try to import database module
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            
            # Try to list collections to verify connectivity
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]  # Show first 10 collections
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    # Check environment variables
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
