import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from postgrest import SyncPostgrestClient
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from backend directory and root
env_path = Path(__file__).resolve().parent / ".env"
root_env = Path(__file__).resolve().parent.parent / ".env"
cwd_env = Path.cwd() / ".env"
print(f"__file__: {__file__}")
print(f"Resolved main.py: {Path(__file__).resolve()}")
print(f"Loading env from: {env_path}, exists: {env_path.exists()}")
print(f"Loading env from: {root_env}, exists: {root_env.exists()}")
print(f"Loading env from: {cwd_env}, exists: {cwd_env.exists()}")
load_dotenv(dotenv_path=env_path)
load_dotenv(dotenv_path=root_env, override=True)
load_dotenv(dotenv_path=cwd_env, override=True)

app = FastAPI(title="Deriv Defensor API")

# Enable CORS
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:3001,http://localhost:3002,http://localhost:3003,http://localhost:3004,http://localhost:3005")
allowed_origins = allowed_origins_env.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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

from agents.genai_explainer import GenAIExplainer
explainer = GenAIExplainer()

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

@app.post("/partners/{partner_id}/trigger")
def trigger_partner_analysis(partner_id: str):
    """
    Trigger AI analysis for a partner and save it.
    """
    if not supabase:
        raise HTTPException(status_code=500, detail="Database connection failed")

    try:
        # 1. Fetch partner data
        response = supabase.from_("partners").select("*").eq("partner_id", partner_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Partner not found")
        
        partner = response.data[0]
        
        # 2. Generate summary using Explainer
        # Mock some reason codes based on partner data
        reasons = [
            {'feature': 'login_trend_30d', 'description': f'Login frequency dropped {abs(partner.get("login_trend_30d", 0))}%', 'impact_score': 8.0},
            {'feature': 'tier_proximity_score', 'description': f'Usage patterns inconsistent with {partner.get("tier")} tier expectations', 'impact_score': 5.0}
        ]
        
        narrative = explainer.generate_narrative(partner, partner.get('churn_prob', 0.5), reasons)
        
        # 3. Save to agent_summaries
        data = {
            "partner_id": partner_id,
            "churn_tendency": partner.get('churn_prob', 0.5),
            "summary": narrative,
            "metrics": {
                "login_velocity": partner.get("login_trend_30d", 0) / 100,
                "urgency": partner.get("urgency_score", 50)
            }
        }
        
        supabase.from_("agent_summaries").insert(data).execute()
        
        # 4. Log an intervention
        intervention = {
            "partner_id": partner_id,
            "action_type": "AI Investigation",
            "status": "Completed",
            "explanation_text": narrative[:200], # Add snippet of summary
            "outcome_label": "Saved" if partner.get('churn_prob', 0.5) < 0.6 else None
        }
        supabase.from_("interventions").insert(intervention).execute()

        return {"status": "success", "summary": narrative}
    except Exception as e:
        print(f"Error triggering analysis: {e}")
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
