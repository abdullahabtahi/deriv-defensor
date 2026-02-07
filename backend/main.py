import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv
from postgrest import SyncPostgrestClient

# Load environment variables
load_dotenv()

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Deriv Defensor API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Supabase Client (Using PostgREST directly)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Warning: SUPABASE_URL and SUPABASE_KEY must be set in .env")
    supabase = None
else:
    try:
        # Construct the REST URL
        rest_url = f"{SUPABASE_URL}/rest/v1"
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}"
        }
        supabase = SyncPostgrestClient(rest_url, headers=headers)
    except Exception as e:
        print(f"Error initializing Supabase client: {e}")
        supabase = None

# --- Pydantic Models ---
class AgentSummaryRequest(BaseModel):
    partner_id: str
    churn_tendency: float
    summary: str
    metrics: Dict[str, Any] = {}

class Partner(BaseModel):
    partner_id: str
    region: str
    tier: str

# --- Endpoints ---

@app.get("/")
def read_root():
    return {"status": "ok", "service": "Deriv Defensor Backend"}

@app.get("/partners")
def get_partners(limit: int = 50, region: Optional[str] = None):
    """
    Fetch partners with optional filtering.
    """
    if not supabase:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        query = supabase.from_("partners").select("*")
        if region:
            query = query.eq("region", region)
        
        response = query.limit(limit).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/partners/{partner_id}")
def get_partner(partner_id: str):
    """
    Fetch a single partner by ID.
    """
    if not supabase:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        response = supabase.from_("partners").select("*").eq("partner_id", partner_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Partner not found")
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/partners/{partner_id}/summary")
def get_partner_summary(partner_id: str):
    """
    Fetch the latest agent summary for a partner.
    """
    if not supabase:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        response = supabase.from_("agent_summaries").select("*").eq("partner_id", partner_id).order("created_at", desc=True).limit(1).execute()
        return response.data[0] if response.data else {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
def get_stats():

    """
    Fetch the latest daily ROI stats.
    """
    if not supabase:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        # Get the most recent entry
        response = supabase.from_("daily_stats").select("*").order("date", desc=True).limit(1).execute()
        return response.data[0] if response.data else {}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/agent-summary")
def create_agent_summary(request: AgentSummaryRequest):
    """
    Receive summary/analysis from an external Agentic Worker.
    """
    if not supabase:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        data = {
            "partner_id": request.partner_id,
            "churn_tendency": request.churn_tendency,
            "summary": request.summary,
            "metrics": request.metrics
        }
        
        # Insert into Supabase
        response = supabase.from_("agent_summaries").insert(data).execute()
        
        return {"status": "success", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/interventions")
def get_interventions(limit: int = 20):
    if not supabase:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        response = supabase.from_("interventions").select("*").order("timestamp", desc=True).limit(limit).execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Allow running this file directly for dev
    uvicorn.run(app, host="0.0.0.0", port=8000)
