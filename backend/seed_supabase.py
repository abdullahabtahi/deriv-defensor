import os
import pandas as pd
from supabase import create_client, Client
from typing import List, Dict
import time

# --- Configuration ---
# You need to set these env vars or hardcode them temporarily
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("❌ Error: SUPABASE_URL and SUPABASE_KEY environment variables must be set.")
    exit(1)

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
DATA_DIR = "../data"

def batch_upsert(table: str, data: List[Dict], batch_size: int = 1000):
    """Upserts data in batches to avoid timeouts."""
    total = len(data)
    print(f"🚀 Upserting {total} records to '{table}'...")
    
    for i in range(0, total, batch_size):
        batch = data[i:i+batch_size]
        try:
            response = supabase.table(table).upsert(batch).execute()
            print(f"   ✅ Batch {i//batch_size + 1}: {len(batch)} records")
        except Exception as e:
            print(f"   ❌ Error in batch {i//batch_size + 1}: {e}")
            time.sleep(1) # Simple backoff

def seed_partners():
    df = pd.read_csv(f"{DATA_DIR}/partners.csv")
    
    # Map CSV columns to Supabase schema
    records = []
    for _, row in df.iterrows():
        record = {
            "partner_id": row['partner_id'],
            "region": row['region'],
            "tier": row['tier'],
            "join_date": row['join_date'],
            "status": "Active", # Default
            "churn_prob": row.get('churn_prob', 0.0),
            "ltv": row.get('ltv', 0.0),
            "avg_commission_3m": row.get('avg_commission_3m', 0.0),
            # Add other fields as needed
            "login_trend_30d": row.get('login_trend_30d', 0),
            "payment_delay_flag": bool(row.get('payment_delay_flag', False)),
            "unresolved_ticket_count": int(row.get('unresolved_ticket_count', 0))
        }
        records.append(record)
    
    batch_upsert("partners", records)

def seed_relationships():
    try:
        df = pd.read_csv(f"{DATA_DIR}/network_relationships.csv")
        records = df.to_dict(orient='records')
        batch_upsert("network_relationships", records)
    except FileNotFoundError:
        print("⚠️ network_relationships.csv not found, skipping.")

def seed_interventions():
    try:
        df = pd.read_csv(f"{DATA_DIR}/interventions.csv")
        # Ensure column mapping matches
        records = df.to_dict(orient='records')
        batch_upsert("interventions", records)
    except FileNotFoundError:
        print("⚠️ interventions.csv not found, skipping.")

if __name__ == "__main__":
    print("🌱 Starting Supabase Seed Process...")
    seed_partners()
    seed_relationships()
    seed_interventions()
    print("✅ Seeding Complete!")
