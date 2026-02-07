"""
Supabase Seeder Script
---------------------
Migrates synthetic data from CSV/Generators to Supabase.
Handles:
1. Partners
2. Interventions
3. Agent Summaries (Mock)

NOTE: Uses PostgREST client directly to avoid heavy dependencies.
"""

import os
import random
import uuid
from datetime import datetime, timedelta
# import pandas as pd # Removed to avoid compilation issues
from dotenv import load_dotenv
from postgrest import SyncPostgrestClient

# Load env variables (assumes .env in project root)
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Error: Missing SUPABASE_URL or SUPABASE_KEY in .env file.")
    print("   Please create a .env file with your Supabase credentials.")
    exit(1)

# Initialize PostgREST Client
try:
    rest_url = f"{SUPABASE_URL}/rest/v1"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates"
    }
    supabase = SyncPostgrestClient(rest_url, headers=headers)
except Exception as e:
    print(f"❌ Error initializing client: {e}")
    exit(1)

def seed_partners():
    """Seeds the Partners table from generated data or on-the-fly generation."""
    print("🌱 Seeding Partners...")
    
    # Generate mock partners if CSV doesn't exist (simplified version of synthetic_generator)
    partners = []
    regions = ['MENA', 'EU', 'APAC', 'LATAM', 'NA']
    tiers = ['Platinum', 'Gold', 'Silver', 'Bronze']
    
    for i in range(50):
        pid = f'P{18000 + i}'
        partners.append({
            "partner_id": pid,
            "region": random.choice(regions),
            "tier": random.choice(tiers),
            "join_date": (datetime.now() - timedelta(days=random.randint(100, 1000))).isoformat(),
            "status": "Active",
            "churn_prob": round(random.uniform(0.1, 0.95), 2),
            "risk_category": random.choice(['High', 'Medium', 'Low']),
            "urgency_score": random.randint(10, 100),
            "ltv": round(random.uniform(5000, 50000), 2),
            "avg_commission_3m": round(random.uniform(500, 5000), 2),
            "login_trend_30d": round(random.uniform(-0.5, 0.5), 2),
            "payment_delay_flag": random.choice([True, False]),
            "unresolved_ticket_count": random.randint(0, 5)
        })

    # Bulk Insert
    try:
        # Note: postgrest-py use .execute()
        response = supabase.from_("partners").upsert(partners).execute()
        print(f"✅ Inserted {len(partners)} partners.")
    except Exception as e:
        print(f"❌ Failed to insert partners: {e}")

def seed_interventions():
    """Seeds the Interventions table."""
    print("🌱 Seeding Interventions...")
    
    interventions = []
    actions = ['Email', 'Call', 'Bonus', 'Meeting']
    statuses = ['Pending', 'Completed', 'Failed']
    
    for i in range(20):
        interventions.append({
            "partner_id": f'P{18000 + random.randint(0, 49)}',
            "action_type": random.choice(actions),
            "status": random.choice(statuses),
            "explanation_text": "AI detected significant drop in login frequency.",
            "email_draft": "Dear Partner, we noticed...",
            "performed_by": "System",
            "timestamp": (datetime.now() - timedelta(days=random.randint(0, 10))).isoformat(),
            "outcome_label": random.choice(['Saved', 'Churned', None])
        })

    try:
        response = supabase.from_("interventions").insert(interventions).execute()
        print(f"✅ Inserted {len(interventions)} interventions.")
    except Exception as e:
        print(f"❌ Failed to insert interventions: {e}")

def seed_agent_summaries():
    """Seeds the Agent Summaries table."""
    print("🌱 Seeding Agent Summaries...")
    
    summaries = []
    for i in range(10):
        summaries.append({
            "partner_id": f'P{18000 + random.randint(0, 49)}',
            "churn_tendency": round(random.uniform(0.5, 0.99), 2),
            "summary": "Agent reports high dissatisfaction with new commission structure.",
            "metrics": {
                "sentiment_score": round(random.uniform(-1.0, 0.0), 2),
                "competitor_mention": True
            },
            "created_at": datetime.now().isoformat()
        })
        
    try:
        response = supabase.from_("agent_summaries").insert(summaries).execute()
        print(f"✅ Inserted {len(summaries)} agent summaries.")
    except Exception as e:
        print(f"❌ Failed to insert agent summaries: {e}")

if __name__ == "__main__":
    print("🚀 Starting Supabase Seed (Lightweight)...")
    seed_partners()
    seed_interventions()
    seed_agent_summaries()
    print("✨ Seeding Complete!")
