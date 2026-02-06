"""
AI Partner Churn Predictor - Database Configuration
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DATABASE_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 5432)),
    'user': os.getenv('DB_USER', 'churn_user'),
    'password': os.getenv('DB_PASSWORD', 'churn_secure_2024'),
    'database': os.getenv('DB_NAME', 'churn_predictor'),
}

# Build connection string
DATABASE_URL = (
    f"postgresql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}"
    f"@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}"
    f"/{DATABASE_CONFIG['database']}"
)

# Model configuration
MODEL_CONFIG = {
    'churn_threshold': 0.65,
    'uplift_threshold': 0.10,
    'min_roi_for_call': 500,  # Minimum ROI to justify call intervention
}

# Feature configuration
REQUIRED_FEATURES = [
    'login_count_30d',
    'login_trend_30d',
    'days_since_last_interaction',
    'dashboard_usage_score',
    'asset_download_count_30d',
    'revenue_velocity',
    'conversion_rate_wow',
    'traffic_quality_score',
    'commission_trend_90d',
    'payment_delay_flag',
    'unresolved_ticket_count',
    'negative_sentiment_score',
    'subnetwork_avg_health_score',
    'subnetwork_recent_churn_count',
    'tier_proximity_score',
    'tenure_months',
    'avg_commission_3m',
    'commission_volatility',
]

# Churn scenarios
CHURN_SCENARIOS = [
    'Healthy',
    'Trust_Erosion',
    'Network_Contagion',
    'Tier_Cliff_Anxiety',
    'Active_Churn',
    'Passive_Disengagement',
]

# Intervention types
INTERVENTION_TYPES = ['call', 'email', 'none']

# Tier thresholds (for tier_proximity_score calculation)
TIER_THRESHOLDS = {
    'Bronze': 0,
    'Silver': 1000,
    'Gold': 5000,
    'Platinum': 25000,
}
