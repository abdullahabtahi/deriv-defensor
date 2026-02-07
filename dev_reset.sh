#!/bin/bash

# Setup colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🔄 Stopping existing processes...${NC}"
pkill -f uvicorn || true
pkill -f "next-server" || true
pkill -f "next" || true
pkill -f streamlit || true

echo -e "${GREEN}🧹 Cleaning Next.js build cache...${NC}"
cd web
rm -rf .next
cd ..

echo -e "${GREEN}🚀 Starting Backend (Port 8001)...${NC}"
# Use nohup to keep running in background, but log to a file
nohup bash -c "source /tmp/deriv_dashboard_venv/bin/activate && cd backend && uvicorn main:app --reload --port 8001" > backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend started with PID $BACKEND_PID. Logs in backend.log"

echo -e "${GREEN}⏳ Waiting 3s for Backend...${NC}"
sleep 3

echo -e "${GREEN}🚀 Starting Frontend (Port 3000)...${NC}"
cd web
# Use nohup to keep running in background
nohup npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend started with PID $FRONTEND_PID. Logs in web/frontend.log"

echo -e "${GREEN}✅ Local Environment Reset Complete!${NC}"
echo -e "Backend: http://localhost:8001"
echo -e "Frontend: http://localhost:3000"
