import pandas as pd
import numpy as np
import pickle
import streamlit as st
import os
import sys

# Add project root to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import ExplainabilityEngine so pickle can deserialize it
try:
    from models.explain_model import ExplainabilityEngine
except ImportError:
    pass  # Graceful degradation if module not found

@st.cache_resource
def load_data():
    """Load partner data and engineer features if needed."""
    try:
        df = pd.read_csv('dataset/partners.csv')
        # Ensure numeric types for critical columns
        cols_to_numeric = ['avg_commission_3m', 'login_trend_30d', 'days_since_last_interaction']
        for col in cols_to_numeric:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        return df
    except FileNotFoundError:
        st.error("Data file not found in dataset/partners.csv")
        return pd.DataFrame()

@st.cache_resource
def load_model():
    """Load trained churn model."""
    try:
        with open('models/lgb_churn_model.pkl', 'rb') as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        st.error("Model file not found in models/lgb_churn_model.pkl")
        return None

@st.cache_resource
def load_explainer():
    """Load explainability engine."""
    try:
        with open('models/explainer.pkl', 'rb') as f:
            explainer = pickle.load(f)
        return explainer
    except (FileNotFoundError, AttributeError) as e:
        # AttributeError occurs when class definition is not available
        # This is non-critical for dashboard functionality
        return None

def calculate_empc(y_true, y_pred_proba, ltv, intervention_cost, save_probability, top_k_percent=0.2):
    """
    Dynamic EMPC Calculation for Dashboard Sliders.
    Returns: (net_profit, roi, total_interventions)
    """
    # Sort indices by risk
    sorted_indices = np.argsort(y_pred_proba)[::-1]
    
    # Select Top K%
    n_partners = len(y_true)
    cutoff = int(n_partners * top_k_percent)
    target_indices = sorted_indices[:cutoff]
    
    invested_budget = 0
    saved_revenue = 0
    
    for i in target_indices:
        is_churn = y_true.iloc[i]
        partner_ltv = ltv.iloc[i]
        
        invested_budget += intervention_cost
        
        if is_churn:
            saved_revenue += (partner_ltv * (save_probability / 100.0))
            
    net_profit = saved_revenue - invested_budget
    roi = (net_profit / invested_budget) if invested_budget > 0 else 0
    return net_profit, roi, len(target_indices)

def get_high_risk_stream(df, model, threshold=0.85, limit=5):
    """
    Get a stream of high-risk partners for the live feed.
    """
    feature_cols = [
        'login_count_30d', 'login_trend_30d', 'days_since_last_interaction',
        'revenue_velocity', 'conversion_rate_wow', 'commission_trend_90d',
        'payment_delay_flag', 'unresolved_ticket_count', 'negative_sentiment_score',
        'subnetwork_avg_health_score', 'subnetwork_recent_churn_count',
        'tier_proximity_score', 'tenure_months', 'avg_commission_3m'
    ]
    
    if 'churn_prob' not in df.columns:
        X = df[feature_cols].copy().fillna(0)
        df['churn_prob'] = model.predict_proba(X)[:, 1]
    
    high_risk = df[df['churn_prob'] > threshold].sort_values('churn_prob', ascending=False)
    return high_risk.head(limit).to_dict('records')


def estimate_churn_urgency(partner: dict) -> dict:
    """
    Heuristic urgency estimator (no model rebuild required).
    
    P2: Time-to-Churn - De-risked approach using existing features.
    
    Logic:
    - Steep login decline + payment delays = 🔴 ~7 days
    - Moderate decline + unresolved tickets = 🟡 ~30 days  
    - Slow drift = 🟢 ~90 days
    
    Returns:
        dict with 'label', 'color', 'days' keys
    """
    urgency_score = 0
    
    # Login trend (stronger signal)
    login_trend = partner.get('login_trend_30d', 0)
    if login_trend < -50:
        urgency_score += 14
    elif login_trend < -20:
        urgency_score += 7
    
    # Payment delays (strong signal)
    if partner.get('payment_delay_flag', False):
        urgency_score += 7
    
    # Support backlog
    urgency_score += partner.get('unresolved_ticket_count', 0) * 2
    
    # Days since interaction
    urgency_score += partner.get('days_since_last_interaction', 0) * 0.3
    
    # Map score to buckets
    if urgency_score > 14:
        return {"label": "🔴 ~7 days", "color": "red", "days": 7}
    elif urgency_score > 7:
        return {"label": "🟡 ~30 days", "color": "orange", "days": 30}
    else:
        return {"label": "🟢 ~90 days", "color": "green", "days": 90}


def log_intervention(partner_id: str, action: str, status: str = "pending", assigned_to: str = None):
    """
    Append intervention to CSV log.
    
    P1: Outcome Tracking - Creates audit trail of all interventions.
    """
    from datetime import datetime
    
    new_entry = {
        'partner_id': partner_id,
        'intervention_date': datetime.now().strftime('%Y-%m-%d'),
        'action': action,
        'status': status,
        'assigned_to': assigned_to or 'System',
        'outcome_date': None,
        'ltv_protected': 0
    }
    
    log_path = 'data/intervention_log.csv'
    
    try:
        log = pd.read_csv(log_path)
        log = pd.concat([log, pd.DataFrame([new_entry])], ignore_index=True)
    except FileNotFoundError:
        log = pd.DataFrame([new_entry])
    
    log.to_csv(log_path, index=False)
    return True

