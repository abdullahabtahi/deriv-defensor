#!/bin/bash
# Run FastAPI Backend
# Usage: ./run.sh

cd "$(dirname "$0")"
cd ..

if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup_env.sh first."
    exit 1
fi

# Credentials should be set in environment or .env file
# Exporting them here is only for local dev convenience if not using .env
if [ -z "$SUPABASE_URL" ]; then
    export $(grep SUPABASE_URL .env | xargs)
fi
if [ -z "$SUPABASE_KEY" ]; then
    export $(grep SUPABASE_KEY .env | xargs)
fi


echo "🚀 Starting FastAPI Backend on port 8001..."
source venv/bin/activate
uvicorn backend.main:app --reload --port 8001

