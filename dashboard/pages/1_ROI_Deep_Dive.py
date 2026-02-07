import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data, load_model

st.set_page_config(page_title="ROI Analysis", page_icon="💰", layout="wide")

st.title("💰 Business Impact & ROI Analysis")
st.markdown("Quantify the financial value of AI-guided interventions vs. random targeting.")

# Load Data
df = load_data()
model = load_model()

if df.empty or model is None:
    st.warning("Model not trained.")
    st.stop()

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Scenario Parameters")
intervention_cost = st.sidebar.slider(
    "Intervention Cost ($)", 
    min_value=50, max_value=500, value=100, step=10,
    help="Cost per partner contacted (e.g., call center time, incentives)"
)

success_rate = st.sidebar.slider(
    "Exp. Success Rate (%)", 
    min_value=10, max_value=90, value=40, step=5,
    help="Predicted conversion rate of interventions"
)

top_k_pct = st.sidebar.slider(
    "Target Capacity (%)",
    min_value=5, max_value=50, value=20, step=5,
    help="Percentage of partner base we have budget to contact"
)

# --- CALCULATIONS ---
# Pre-calculate predictions
feature_cols = [
    'login_count_30d', 'login_trend_30d', 'days_since_last_interaction',
    'revenue_velocity', 'conversion_rate_wow', 'commission_trend_90d',
    'payment_delay_flag', 'unresolved_ticket_count', 'negative_sentiment_score',
    'subnetwork_avg_health_score', 'subnetwork_recent_churn_count',
    'tier_proximity_score', 'tenure_months', 'avg_commission_3m'
]
X = df[feature_cols].copy().fillna(0)
# Cache predictions in session state for speed? For now recalculate is fast
y_pred_proba = model.predict_proba(X)[:, 1]
ltv = df['avg_commission_3m'] * 12
y_true = df['churn_label']

# 1. AI Model ROI
sorted_indices = np.argsort(y_pred_proba)[::-1]
cutoff = int(len(df) * (top_k_pct / 100.0))
target_indices = sorted_indices[:cutoff]

ai_invested = len(target_indices) * intervention_cost
ai_saved_revenue = 0
for i in target_indices:
    if y_true.iloc[i]:
        ai_saved_revenue += (ltv.iloc[i] * (success_rate / 100.0))
ai_net_profit = ai_saved_revenue - ai_invested

# 2. Random Baseline ROI
rng = np.random.default_rng(42)
random_indices = rng.choice(len(df), size=cutoff, replace=False)

rnd_invested = len(random_indices) * intervention_cost
rnd_saved_revenue = 0
for i in random_indices:
    if y_true.iloc[i]:
        rnd_saved_revenue += (ltv.iloc[i] * (success_rate / 100.0))
rnd_net_profit = rnd_saved_revenue - rnd_invested

# Calculate ROI lift for use in visualizations
roi_lift = ai_net_profit / rnd_net_profit if rnd_net_profit > 0 else 0

# --- VISUALIZATIONS ---

# Headline ROI Card (Maximum Impact)
st.markdown(f"""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 30px; border-radius: 15px; text-align: center; margin-bottom: 30px;">
    <h2 style="color: white; margin: 0; font-size: 1.2rem; font-weight: 400;">🎯 MODEL PERFORMANCE</h2>
    <div style="display: flex; justify-content: space-around; margin-top: 20px;">
        <div>
            <div style="color: #e0e0e0; font-size: 0.9rem;">Random Targeting</div>
            <div style="color: white; font-size: 2rem; font-weight: 700;">${rnd_net_profit:,.0f}</div>
        </div>
        <div>
            <div style="color: #e0e0e0; font-size: 0.9rem;">AI-Guided</div>
            <div style="color: white; font-size: 2rem; font-weight: 700;">${ai_net_profit:,.0f}</div>
        </div>
    </div>
    <div style="margin-top: 25px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.2);">
        <div style="color: #ffd700; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">ROI Improvement</div>
        <div style="color: white; font-size: 3rem; font-weight: 900;">{roi_lift:.2f}x ✨</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Row 1: The Big Picture (KPIs)
col1, col2, col3 = st.columns(3)
col1.metric("Net Profit (AI Model)", f"${ai_net_profit:,.0f}", delta=f"${ai_net_profit - rnd_net_profit:,.0f} vs Random")
col2.metric("Net Profit (Random)", f"${rnd_net_profit:,.0f}")
roi_lift = ai_net_profit / rnd_net_profit if rnd_net_profit > 0 else 0
col3.metric("ROI Multiplier", f"{roi_lift:.2f}x")

st.markdown("---")

# Row 2: Charts
c1, c2 = st.columns([1, 1])

with c1:
    st.subheader("Profit Comparison")
    chart_data = pd.DataFrame({
        'Strategy': ['Random Baseline', 'AI Model'],
        'Net Profit': [rnd_net_profit, ai_net_profit],
        'Color': ['#bdc3c7', '#2ecc71']
    })
    
    fig_bar = px.bar(
        chart_data, x='Strategy', y='Net Profit', 
        color='Strategy', 
        color_discrete_map={'Random Baseline': '#95a5a6', 'AI Model': '#27ae60'},
        text_auto='.2s',
        title=f"Net Profit @ {top_k_pct}% Capacity"
    )
    fig_bar.update_layout(showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

with c2:
    st.subheader("Cumulative Profit Curve (Lift Chart)")
    
    # Calculate cumulative curves
    # Sort data by model score
    sorted_df = pd.DataFrame({'y_true': y_true, 'ltv': ltv, 'score': y_pred_proba}).sort_values('score', ascending=False)
    
    # Cumulative stats
    sorted_df['potential_save'] = sorted_df['y_true'].astype(int) * sorted_df['ltv'] * (success_rate / 100.0)
    sorted_df['cost'] = intervention_cost
    sorted_df['net_value'] = sorted_df['potential_save'] - sorted_df['cost']
    
    # AI Curve
    sorted_df['cum_profit_ai'] = sorted_df['net_value'].cumsum()
    
    # Random Curve (Theoretical Average)
    avg_value_per_user = (df['churn_label'].astype(int) * df['avg_commission_3m'] * 12 * (success_rate/100.0)).mean() - intervention_cost
    x_axis = np.arange(len(df))
    y_random = x_axis * avg_value_per_user
    
    fig_lift = go.Figure()
    
    # AI Line
    fig_lift.add_trace(go.Scatter(
        x=np.arange(len(sorted_df)), 
        y=sorted_df['cum_profit_ai'], 
        mode='lines', name='AI Model',
        line=dict(color='#27ae60', width=3)
    ))
    
    # Random Line
    fig_lift.add_trace(go.Scatter(
        x=x_axis, y=y_random, 
        mode='lines', name='Random Targeting',
        line=dict(color='#95a5a6', width=2, dash='dash')
    ))
    
    # Current Cutoff Line
    fig_lift.add_vline(x=cutoff, line_width=1, line_dash="dash", line_color="red", annotation_text=f"Selected Capacity ({top_k_pct}%)")
    
    fig_lift.update_layout(
        title="Profit Accumulation by Targeting Depth",
        xaxis_title="Number of Partners Contacted",
        yaxis_title="Cumulative Net Profit ($)",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    
    st.plotly_chart(fig_lift, use_container_width=True)

# Detailed Breakdown
with st.expander("See Calculation Breakdown"):
    st.write(f"""
    **Formula:**
    `Profit = (Partners Contacted × Churn Rate × Success Rate × LTV) - (Partners Contacted × Cost)`
    
    **Scenario Inputs:**
    - Total Partners: {len(df):,}
    - Target Capacity: Top {top_k_pct}% ({cutoff:,} partners)
    - Intervention Cost: ${intervention_cost}
    - Success Rate: {success_rate}%
    
    **AI Performance:**
    - Partners Contacted: {cutoff}
    - Revenue Saved: ${ai_saved_revenue:,.0f}
    - Total Cost: ${ai_invested:,.0f}
    - **Net Profit: ${ai_net_profit:,.0f}**
    """)
