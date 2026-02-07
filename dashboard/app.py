import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.express as px
from utils import load_data, load_model, calculate_empc, get_high_risk_stream, load_explainer, estimate_churn_urgency
# We'll import CohortAnalyzer dynamically or assume logic is embedded/simple for now
# To keep it robust, let's implement simple contagion logic here or import if module exists

# Page Config
st.set_page_config(
    page_title="Deriv Command Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Corporate Clean CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    load_css("dashboard/style.css")
except FileNotFoundError:
    st.warning("CSS file not found. Please ensure dashboard/style.css exists.")

def main():
    st.title("🛡️ Churn Intervention Command Center")
    st.markdown("### 🔴 Real-Time Threat Monitoring & AI Response")
    
    # Load Resources
    df = load_data()
    model = load_model()
    explainer = load_explainer() # Ensure this handles None safely
    
    if df.empty or model is None:
        st.error("System Offline: Run training pipeline first.")
        return

    # Predictions
    feature_cols = [
        'login_count_30d', 'login_trend_30d', 'days_since_last_interaction',
        'revenue_velocity', 'conversion_rate_wow', 'commission_trend_90d',
        'payment_delay_flag', 'unresolved_ticket_count', 'negative_sentiment_score',
        'subnetwork_avg_health_score', 'subnetwork_recent_churn_count',
        'tier_proximity_score', 'tenure_months', 'avg_commission_3m'
    ]
    X = df[feature_cols].copy().fillna(0)
    # Simple check to avoid re-running predict too often if cached
    if 'churn_prob' not in df.columns:
        df['churn_prob'] = model.predict_proba(X)[:, 1]
    
    # --- COMMAND CENTER LAYOUT ---
    
    # Top Row: The "Money Shot"
    c1, c2, c3, c4 = st.columns(4)
    
    # Calc Metrics
    at_risk = df[df['churn_prob'] > 0.65]
    annual_exposure = at_risk['avg_commission_3m'].sum() * 12
    # ROI
    ltv = df['avg_commission_3m'] * 12
    model_profit, _, _ = calculate_empc(df['churn_label'], df['churn_prob'], ltv, 100, 40)
    rng = np.random.default_rng(42)
    base_profit, _, _ = calculate_empc(df['churn_label'], rng.random(len(df)), ltv, 100, 40)
    roi_x = model_profit / base_profit if base_profit > 0 else 0
    
    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="sub-stat">Risk Exposure (Yearly)</div>
            <div class="big-stat">${annual_exposure/1e6:.1f}M</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
         st.markdown(f"""
        <div class="metric-card">
            <div class="sub-stat">Partners At Risk</div>
            <div class="big-stat">{len(at_risk):,}</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card-green">
            <div class="sub-stat">Est. Recoverable</div>
            <div class="big-stat">${model_profit/1e6:.1f}M</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown(f"""
        <div class="metric-card-green">
            <div class="sub-stat">Transformation ROI</div>
            <div class="big-stat">{roi_x:.2f}x</div>
        </div>
        """, unsafe_allow_html=True)

    # Main Split: Strategy (Left) vs Tactics (Right)
    col_strat, col_tactics = st.columns([2, 1])
    
    with col_strat:
        st.subheader("📡 Regional & Network Intelligence")
        
        # 1. Map / Region chart
        # Aggregation by Region
        region_risk = df.groupby('region')[['churn_prob', 'avg_commission_3m']].mean().reset_index()
        fig_map = px.bar(
            region_risk, x='region', y='churn_prob', color='churn_prob',
            title="Avg Churn Risk by Region",
            color_continuous_scale='RdYlGn_r'
        )
        st.plotly_chart(fig_map, use_container_width=True)
        
        # 2. Contagion Alert
        st.subheader("🦠 Contagion Alerts")
        masters = df[df['is_master_affiliate'] == True].sort_values('subnetwork_recent_churn_count', ascending=False).head(3)
        
        for _, master in masters.iterrows():
            if master['subnetwork_recent_churn_count'] > 0:
                st.error(f"⚠️ **Network Contagion:** Master Partner {master['partner_id']} ({master['region']}) has {master['subnetwork_recent_churn_count']} sub-affiliates churning. Immediate intervention required.")

    with col_tactics:
        st.subheader("⚡ Live GenAI Intervention Feed")
        
        # Simulate a live feed of the system "working"
        placeholder = st.empty()
        
        # Get high risk stream
        stream = get_high_risk_stream(df, model, limit=5)
        
        # Display them statically for now (Streamlit loop would block interaction without advanced async)
        # We'll just show the "Latest Actions"
        
        for partner in stream:
            urgency = estimate_churn_urgency(partner)
            urgency_label = urgency['label']
            
            # Mock GenAI processing viz
            with st.container():
                st.markdown(f"""
                <div class="live-feed-item">
                    <div class="feed-timestamp">Just now • {partner['partner_id']} • {partner['tier']}</div>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="font-weight:bold; color:#FF444F;">Risk: {partner['churn_prob']:.1%}</div>
                        <div style="font-size: 0.9rem;">{urgency_label}</div>
                    </div>
                    <div>🤖 <i>Analyzing drivers...</i></div>
                    <div>Login Trend: {partner['login_trend_30d']:.2f} | Tickets: {partner['unresolved_ticket_count']}</div>
                    <div style="margin-top:5px; padding:5px; background:#333; border-radius:3px; font-size:0.8rem;">
                        "Drafted email: Noticed drop in logins. Lets discuss tier upgrade..."
                    </div>
                </div>
                """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
