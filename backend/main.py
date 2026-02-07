import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv
from postgrest import SyncPostgrestClient

# Load environment variables from backend directory
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Deriv Defensor API")

# Enable CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001,http://localhost:3002,http://localhost:3003").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
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
    Calculate real-time statistics from partners and interventions data.
    Calculates dynamically instead of querying daily_stats table.
    """
    if not supabase:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        # Get all partners for risk calculation
        partners_response = supabase.from_("partners").select("ltv, churn_prob").execute()
        partners = partners_response.data
        
        # Calculate total risk exposure (sum of LTV for partners with churn_prob >= 0.5)
        total_exposure = sum(float(p['ltv']) for p in partners if float(p.get('churn_prob', 0)) >= 0.5)
        
        # Calculate recoverable revenue (assume 30% of at-risk LTV is recoverable through intervention)
        recoverable_revenue = total_exposure * 0.3
        
        # Get active interventions count (interventions with status "Pending")
        interventions_response = supabase.from_("interventions").select("id", count="exact").eq("status", "Pending").execute()
        active_interventions = interventions_response.count if interventions_response.count else 0
        
        return {
            "total_revenue_exposed": round(total_exposure, 2),
            "total_recovered_revenue": round(recoverable_revenue, 2),
            "total_partners_at_risk": active_interventions
        }
    except Exception as e:
        print(f"Error calculating stats: {e}")
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
