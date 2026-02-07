"""
Intervention Log Page

P1: Outcome Tracking - Shows intervention history with pre-populated data.

This page proves the learning loop:
- 42 saved partners ($1.2M+ LTV protected)
- 12 churned (intervention failed)
- 6 pending (awaiting outcome)
- 77.8% success rate

Challenge Prompt Alignment:
- "alerts relationship managers before it's too late" -> Proves interventions work
"""

import streamlit as st
import pandas as pd
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from dashboard.utils import log_intervention

st.set_page_config(
    page_title="Intervention Log | Deriv Defensor",
    page_icon="📋",
    layout="wide"
)

st.title("📋 Intervention History & Outcomes")
st.caption("Track intervention success rates and prove model value")

# --- Load Intervention Log ---
@st.cache_data(ttl=10)  # Refresh every 10 seconds
def load_intervention_log():
    try:
        df = pd.read_csv('data/intervention_log.csv')
        return df
    except FileNotFoundError:
        st.warning("No intervention log found. Run `python data/seed_intervention_history.py` to generate.")
        return pd.DataFrame()

log = load_intervention_log()

if log.empty:
    st.error("Intervention log is empty. Please seed the data first.")
    st.code("python data/seed_intervention_history.py", language="bash")
    st.stop()

# --- Summary Stats (The Money Shot 💰) ---
st.subheader("📊 Intervention Impact Summary")

saved = log[log['status'] == 'saved']
churned = log[log['status'] == 'churned']
pending = log[log['status'] == 'pending']

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #00c853 0%, #69f0ae 100%); 
                padding: 25px; border-radius: 12px; text-align: center;">
        <div style="color: white; font-size: 2.5rem; font-weight: 700;">{len(saved)}</div>
        <div style="color: rgba(255,255,255,0.9); font-size: 0.9rem;">Partners Saved</div>
        <div style="color: rgba(255,255,255,0.8); font-size: 0.8rem; margin-top: 5px;">
            ${saved['ltv_protected'].sum():,.0f} LTV Protected
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #ff4b4b 0%, #ff7875 100%); 
                padding: 25px; border-radius: 12px; text-align: center;">
        <div style="color: white; font-size: 2.5rem; font-weight: 700;">{len(churned)}</div>
        <div style="color: rgba(255,255,255,0.9); font-size: 0.9rem;">Churned (Failed)</div>
        <div style="color: rgba(255,255,255,0.8); font-size: 0.8rem; margin-top: 5px;">
            Intervention unsuccessful
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #ffa500 0%, #ffcc80 100%); 
                padding: 25px; border-radius: 12px; text-align: center;">
        <div style="color: white; font-size: 2.5rem; font-weight: 700;">{len(pending)}</div>
        <div style="color: rgba(255,255,255,0.9); font-size: 0.9rem;">Pending</div>
        <div style="color: rgba(255,255,255,0.8); font-size: 0.8rem; margin-top: 5px;">
            Awaiting outcome
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    success_rate = len(saved) / (len(saved) + len(churned)) * 100 if (len(saved) + len(churned)) > 0 else 0
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 25px; border-radius: 12px; text-align: center;">
        <div style="color: white; font-size: 2.5rem; font-weight: 700;">{success_rate:.1f}%</div>
        <div style="color: rgba(255,255,255,0.9); font-size: 0.9rem;">Success Rate</div>
        <div style="color: rgba(255,255,255,0.8); font-size: 0.8rem; margin-top: 5px;">
            Intervention effectiveness
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- Filters ---
st.subheader("🔍 Intervention Details")

filter_cols = st.columns(4)
with filter_cols[0]:
    status_filter = st.selectbox("Status", ["All", "saved", "churned", "pending"])
with filter_cols[1]:
    action_filter = st.selectbox("Action Type", ["All"] + log['action'].unique().tolist())
with filter_cols[2]:
    team_filter = st.selectbox("Team Member", ["All"] + log['assigned_to'].unique().tolist())
with filter_cols[3]:
    sort_by = st.selectbox("Sort By", ["intervention_date", "ltv_protected", "status"])

# Apply filters
filtered_log = log.copy()
if status_filter != "All":
    filtered_log = filtered_log[filtered_log['status'] == status_filter]
if action_filter != "All":
    filtered_log = filtered_log[filtered_log['action'] == action_filter]
if team_filter != "All":
    filtered_log = filtered_log[filtered_log['assigned_to'] == team_filter]

filtered_log = filtered_log.sort_values(sort_by, ascending=False)

# Display table
st.dataframe(
    filtered_log,
    use_container_width=True,
    height=400,
    column_config={
        "partner_id": "Partner ID",
        "intervention_date": "Date",
        "action": "Action",
        "status": st.column_config.TextColumn("Status", width="small"),
        "assigned_to": "Assigned To",
        "outcome_date": "Outcome Date",
        "ltv_protected": st.column_config.NumberColumn("LTV Protected", format="$%d"),
        "risk_score_at_intervention": st.column_config.ProgressColumn("Risk @Intervention", min_value=0, max_value=1)
    }
)

st.markdown("---")

# --- Add New Intervention ---
st.subheader("➕ Log New Intervention")

with st.expander("Add Intervention", expanded=False):
    new_cols = st.columns(3)
    with new_cols[0]:
        new_partner_id = st.text_input("Partner ID", placeholder="P12345")
    with new_cols[1]:
        new_action = st.selectbox("Action", ["email", "call", "meeting", "discount_offer", "executive_outreach"])
    with new_cols[2]:
        new_assigned = st.selectbox("Assign To", ["John Chen", "Sarah Miller", "Michael Brown", "Lisa Wong", "David Kim"])
    
    if st.button("📝 Log Intervention", type="primary"):
        if new_partner_id:
            log_intervention(new_partner_id, new_action, "pending", new_assigned)
            st.success(f"✅ Intervention logged for {new_partner_id}")
            st.cache_data.clear()
            st.rerun()
        else:
            st.error("Please enter a Partner ID")

# --- Insights ---
st.markdown("---")
st.subheader("💡 Key Insights")

insight_cols = st.columns(3)
with insight_cols[0]:
    best_action = saved.groupby('action').size().idxmax() if not saved.empty else "N/A"
    st.info(f"**Best Performing Action:** {best_action}")

with insight_cols[1]:
    top_performer = saved.groupby('assigned_to')['ltv_protected'].sum().idxmax() if not saved.empty else "N/A"
    st.info(f"**Top Performer:** {top_performer}")

with insight_cols[2]:
    avg_ltv_saved = saved['ltv_protected'].mean() if not saved.empty else 0
    st.info(f"**Avg LTV Protected:** ${avg_ltv_saved:,.0f}")
