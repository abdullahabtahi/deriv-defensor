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
