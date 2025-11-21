import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Literal, Dict, Any
from database import db, create_document, get_documents
from schemas import Contactsubmission, Analyticsevent

app = FastAPI(title="Viren Mirpuri Portfolio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Viren Mirpuri Portfolio API"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
                response["connection_status"] = "Connected"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    return response

# Contact submission endpoint
@app.post("/api/contact")
def submit_contact(payload: Contactsubmission):
    try:
        inserted_id = create_document("contactsubmission", payload)
        return {"status": "ok", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Simple analytics ingestion
@app.post("/api/analytics")
def track_event(event: Analyticsevent):
    try:
        inserted_id = create_document("analyticsevent", event)
        return {"status": "ok", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Fetch analytics (basic list with optional limit)
@app.get("/api/analytics")
def list_analytics(limit: int = 100):
    try:
        docs = get_documents("analyticsevent", {}, limit=limit)
        # Convert ObjectId to string if present
        for d in docs:
            if "_id" in d:
                d["_id"] = str(d["_id"])
            if "created_at" in d:
                d["created_at"] = str(d["created_at"])  # simple serialization
        return {"count": len(docs), "events": docs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Optional: fetch articles (static list to start; could be extended later)
class Article(BaseModel):
    id: str
    category: Literal["Formula 1", "NASCAR", "Gaming"]
    title: str
    publication: str
    date: str
    excerpt: str
    thumbnail: str
    url: str

ARTICLES: List[Article] = [
    Article(
        id="1",
        category="Formula 1",
        title="Inside the Paddock: Strategy Shifts in the Hybrid Era",
        publication="EssentiallySports",
        date="2024-07-12",
        excerpt="How teams are rethinking tire windows and energy deployment.",
        thumbnail="https://images.unsplash.com/photo-1517331156700-3c241d2b4d83?w=1200&q=60&auto=format&fit=crop",
        url="https://www.essentiallysports.com/author/viren-mirpuri/"
    ),
    Article(
        id="2",
        category="NASCAR",
        title="Short Tracks, Big Drama: Decoding the Next Gen Battles",
        publication="EssentiallySports",
        date="2024-06-03",
        excerpt="A lap-by-lap dive into the season's most heated clashes.",
        thumbnail="https://images.unsplash.com/photo-1502877338535-766e1452684a?w=1200&q=60&auto=format&fit=crop",
        url="https://www.essentiallysports.com/author/viren-mirpuri/"
    ),
    Article(
        id="3",
        category="Gaming",
        title="Sim Racing to Esports Stardom: The iRacing Pipeline",
        publication="EssentiallySports",
        date="2024-05-18",
        excerpt="From rigs to trophies—how sim racers are making the leap.",
        thumbnail="https://images.unsplash.com/photo-1542751371-adc38448a05e?w=1200&q=60&auto=format&fit=crop",
        url="https://www.essentiallysports.com/author/viren-mirpuri/"
    ),
]

@app.get("/api/articles")
def list_articles(category: Optional[str] = None):
    data = ARTICLES
    if category and category in {"Formula 1", "NASCAR", "Gaming"}:
        data = [a for a in ARTICLES if a.category == category]
    return [a.model_dump() for a in data]

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
