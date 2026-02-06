#!/bin/bash
# AI Partner Churn Predictor - Environment Setup Script
# Usage: source setup_env.sh

echo "🛠️  Setting up development environment..."

# 1. Check if python3 exists
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3."
    return 1
fi

# 2. VPC Setup
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "✅ Virtual environment exists."
fi

# 3. Activate
echo "🔌 Activating venv..."
source venv/bin/activate

# 4. Install dependencies
echo "⬇️  Installing dependencies from requirements.txt..."
pip install -r requirements.txt --quiet

# 5. Verify
echo "✅ Environment ready!"
python3 -c "import pandas; print(f'Pandas version: {pandas.__version__}')"
python3 -c "import causalml; print(f'CausalML version: {causalml.__version__}')" 2>/dev/null || echo "⚠️ CausalML not installed (Day 3 requirement)"

echo "🚀 You can now run: python data/synthetic_generator.py"
