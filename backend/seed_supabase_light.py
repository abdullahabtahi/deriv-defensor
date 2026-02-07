import csv
import json
import os
import time
import requests

# Credentials should be set in environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    # Try loading from .env if available
    from dotenv import load_dotenv
    load_dotenv()
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

DATA_DIR = "../data"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates" # Upsert behavior
}

def batch_upsert(table: str, data: list, batch_size: int = 1000):
    total = len(data)
    print(f"🚀 Upserting {total} records to '{table}'...")
    url = f"{SUPABASE_URL}/rest/v1/{table}"
    
    for i in range(0, total, batch_size):
        batch = data[i:i+batch_size]
        try:
            response = requests.post(url, headers=HEADERS, json=batch)
            if response.status_code in [200, 201]:
                print(f"   ✅ Batch {i//batch_size + 1}: Success")
            else:
                print(f"   ❌ Error in batch {i//batch_size + 1}: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"   ❌ Network Error: {e}")
            time.sleep(1)

def seed_partners():
    try:
        with open(f"{DATA_DIR}/partners.csv", mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            records = []
            for row in reader:
                # Type conversion (CSV makes everything strings)
                record = {
                    "partner_id": row['partner_id'],
                    "region": row['region'],
                    "tier": row['tier'],
                    "join_date": row['join_date'],
                    "status": "Active",
                    "churn_prob": float(row.get('churn_prob', 0.0)),
                    "ltv": float(row.get('ltv', 0.0)),
                    "avg_commission_3m": float(row.get('avg_commission_3m', 0.0)),
                    "login_trend_30d": float(row.get('login_trend_30d', 0)),
                    "payment_delay_flag": row.get('payment_delay_flag', 'False').lower() == 'true',
                    "unresolved_ticket_count": int(row.get('unresolved_ticket_count', 0))
                }
                records.append(record)
            batch_upsert("partners", records)
    except FileNotFoundError:
        print("⚠️ partners.csv not found.")

def seed_relationships():
    try:
        with open(f"{DATA_DIR}/network_relationships.csv", 'r') as f:
            reader = csv.DictReader(f)
            records = [{k: v for k, v in row.items()} for row in reader]
            batch_upsert("network_relationships", records)
    except FileNotFoundError:
        print("⚠️ network_relationships.csv not found.")

def seed_interventions():
    try:
        with open(f"{DATA_DIR}/interventions.csv", 'r') as f:
            reader = csv.DictReader(f)
            records = [{k: v for k, v in row.items()} for row in reader]
            batch_upsert("interventions", records)
    except FileNotFoundError:
        print("⚠️ interventions.csv not found.")

if __name__ == "__main__":
    print("🌱 Starting Lightweight Supabase Seed...")
    seed_partners()
    seed_relationships()
    seed_interventions()
    print("✅ Seeding Complete!")
