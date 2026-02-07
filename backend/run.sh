#!/bin/bash
# Run FastAPI Backend
# Usage: ./run.sh

cd "$(dirname "$0")"
cd ..

if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup_env.sh first."
    exit 1
fi

# Explicitly export Supabase credentials for the backend
export SUPABASE_URL=https://gmacvzranexqivmqovba.supabase.co
export SUPABASE_KEY=sb_publishable_QXtnAWiracWF4pPaPimejQ_upZRD-6T

echo "🚀 Starting FastAPI Backend on port 8001..."
source venv/bin/activate
uvicorn backend.main:app --reload --port 8001

