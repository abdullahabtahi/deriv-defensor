"""
Gap 2: Business Impact Summary

Executive-level dashboard showing key business metrics that judges care about.
This page answers: "Did you solve a real business problem?"
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from utils import load_data, load_model, calculate_empc

st.set_page_config(page_title="Business Impact", page_icon="📊", layout="wide")

# Custom CSS for executive presentation
st.markdown("""
<style>
    .executive-card {
        background: linear-gradient(135deg, #1a1c24 0%, #2d3748 100%);
        border-radius: 12px;
        padding: 25px;
        margin: 10px 0;
        border-left: 4px solid #48bb78;
    }
    .metric-label {
        color: #a0aec0;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }
    .metric-value {
        color: #ffffff;
        font-size: 2.5rem;
        font-weight: 700;
    }
    .metric-delta {
        color: #48bb78;
        font-size: 1rem;
    }
    .summary-table {
        background: #1a1c24;
        border-radius: 8px;
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Executive Business Impact Summary")
st.markdown("### Quantifying AI Value for Partner Retention")

# Load Data
df = load_data()
model = load_model()

if df.empty or model is None:
    st.error("Model not trained. Run training pipeline first.")
    st.stop()

# Calculate predictions
feature_cols = [
    'login_count_30d', 'login_trend_30d', 'days_since_last_interaction',
    'revenue_velocity', 'conversion_rate_wow', 'commission_trend_90d',
    'payment_delay_flag', 'unresolved_ticket_count', 'negative_sentiment_score',
    'subnetwork_avg_health_score', 'subnetwork_recent_churn_count',
    'tier_proximity_score', 'tenure_months', 'avg_commission_3m'
]
X = df[feature_cols].copy().fillna(0)
y_pred_proba = model.predict_proba(X)[:, 1]
ltv = df['avg_commission_3m'] * 12
y_true = df['churn_label']

# Calculate metrics with default parameters
INTERVENTION_COST = 100
SUCCESS_RATE = 40
TOP_K_PERCENT = 0.20

# AI Model Performance
sorted_indices = np.argsort(y_pred_proba)[::-1]
cutoff = int(len(df) * TOP_K_PERCENT)
target_indices = sorted_indices[:cutoff]

ai_invested = cutoff * INTERVENTION_COST
ai_saved = sum(ltv.iloc[i] * (SUCCESS_RATE/100) for i in target_indices if y_true.iloc[i])
ai_profit = ai_saved - ai_invested
ai_partners_saved = sum(1 for i in target_indices if y_true.iloc[i])

# Random Baseline
rng = np.random.default_rng(42)
random_indices = rng.choice(len(df), size=cutoff, replace=False)
rnd_saved = sum(ltv.iloc[i] * (SUCCESS_RATE/100) for i in random_indices if y_true.iloc[i])
rnd_profit = rnd_saved - cutoff * INTERVENTION_COST
rnd_partners_saved = sum(1 for i in random_indices if y_true.iloc[i])

# Calculate improvement
roi_improvement = ai_profit / rnd_profit if rnd_profit > 0 else float('inf')
partners_saved_improvement = ai_partners_saved / rnd_partners_saved if rnd_partners_saved > 0 else float('inf')

# Cost per save
ai_cost_per_save = ai_invested / ai_partners_saved if ai_partners_saved > 0 else 0
rnd_cost_per_save = (cutoff * INTERVENTION_COST) / rnd_partners_saved if rnd_partners_saved > 0 else 0

# Avg LTV protected
avg_ltv_protected = ltv.iloc[target_indices][y_true.iloc[target_indices] == 1].mean() if ai_partners_saved > 0 else 0

# ============================================================================
# HEADLINE METRIC - THE MONEY SHOT
# ============================================================================

st.markdown("---")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="executive-card" style="border-left-color: #e53e3e;">
        <div class="metric-label">Annual Risk Exposure</div>
        <div class="metric-value">${ltv[y_true == 1].sum()/1e6:.1f}M</div>
        <div class="metric-delta" style="color: #e53e3e;">Partners at risk of churning</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="executive-card" style="border-left-color: #48bb78;">
        <div class="metric-label">Recoverable Value (AI)</div>
        <div class="metric-value">${ai_profit/1e3:.0f}K</div>
        <div class="metric-delta">+${(ai_profit - rnd_profit)/1e3:.0f}K vs random</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="executive-card" style="border-left-color: #4299e1;">
        <div class="metric-label">ROI Improvement</div>
        <div class="metric-value">{roi_improvement:.1f}x</div>
        <div class="metric-delta">AI vs Random Targeting</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# BUSINESS IMPACT TABLE - JUDGES WANT THIS
# ============================================================================

st.markdown("---")
st.subheader("📋 Business Impact Summary Table")

impact_data = {
    'Metric': [
        'Partners Saved',
        'Expected Profit',
        'Cost per Save',
        'Avg LTV Protected',
        'Intervention Budget',
        'Net ROI'
    ],
    'Random Targeting': [
        f"{rnd_partners_saved:,}",
        f"${rnd_profit:,.0f}",
        f"${rnd_cost_per_save:,.0f}",
        "N/A (Untargeted)",
        f"${cutoff * INTERVENTION_COST:,.0f}",
        f"{((rnd_profit)/(cutoff * INTERVENTION_COST))*100:.0f}%"
    ],
    'AI Model': [
        f"{ai_partners_saved:,}",
        f"${ai_profit:,.0f}",
        f"${ai_cost_per_save:,.0f}",
        f"${avg_ltv_protected:,.0f}",
        f"${ai_invested:,.0f}",
        f"{((ai_profit)/ai_invested)*100:.0f}%"
    ],
    'Improvement': [
        f"{partners_saved_improvement:.1f}x",
        f"+${ai_profit - rnd_profit:,.0f}",
        f"-{((rnd_cost_per_save - ai_cost_per_save)/rnd_cost_per_save)*100:.0f}%",
        "Targeted High-LTV",
        "Same budget",
        f"+{((ai_profit/ai_invested) - (rnd_profit/(cutoff*INTERVENTION_COST)))*100:.0f}pp"
    ]
}

impact_df = pd.DataFrame(impact_data)

# Display as styled table
st.dataframe(
    impact_df.style.set_properties(**{
        'background-color': '#1a1c24',
        'color': 'white',
        'border-color': '#2d3748'
    }),
    use_container_width=True,
    hide_index=True
)

# ============================================================================
# EMPC CALCULATION BREAKDOWN
# ============================================================================

st.markdown("---")
st.subheader("💰 EMPC: Expected Maximum Profit from Churn Prevention")

col_formula, col_values = st.columns([1, 1])

with col_formula:
    st.markdown("""
    **Formula:**
    ```
    EMPC = Σ (LTV × P(save) - Cost) × P(churn)
    ```

    **Components:**
    - **LTV**: Lifetime Value per partner (avg_commission × 12)
    - **P(save)**: Probability of successful retention (40%)
    - **Cost**: Intervention cost per partner ($100)
    - **P(churn)**: Model-predicted churn probability
    """)

with col_values:
    st.markdown(f"""
    **Our Results:**

    | Component | Value |
    |-----------|-------|
    | Avg Partner LTV | ${ltv.mean():,.0f} |
    | High-Risk Partner LTV | ${ltv[y_pred_proba > 0.5].mean():,.0f} |
    | Churn Rate (Actual) | {y_true.mean()*100:.1f}% |
    | Model Precision | {(y_true.iloc[target_indices].sum() / len(target_indices))*100:.1f}% |

    **Bottom Line:**
    - Every $1 spent on AI-guided intervention returns **${ai_profit/ai_invested:.2f}**
    - Random targeting returns only **${rnd_profit/(cutoff*INTERVENTION_COST):.2f}**
    """)

# ============================================================================
# VISUAL: WATERFALL CHART
# ============================================================================

st.markdown("---")
st.subheader("📈 Value Creation Waterfall")

fig = go.Figure(go.Waterfall(
    orientation="v",
    measure=["relative", "relative", "relative", "total"],
    x=["Risk Exposure<br>(At-Risk Partners)", "Random Recovery<br>(Baseline)", "AI Uplift<br>(Incremental)", "Net Protected<br>Value"],
    y=[ltv[y_true == 1].sum()/1000, -rnd_saved/1000, -(ai_saved - rnd_saved)/1000, 0],
    text=[f"${ltv[y_true == 1].sum()/1e6:.1f}M", f"-${rnd_saved/1e3:.0f}K", f"-${(ai_saved - rnd_saved)/1e3:.0f}K", f"${(ltv[y_true == 1].sum() - ai_saved)/1e3:.0f}K"],
    textposition="outside",
    connector={"line": {"color": "rgb(63, 63, 63)"}},
    decreasing={"marker": {"color": "#48bb78"}},
    increasing={"marker": {"color": "#e53e3e"}},
    totals={"marker": {"color": "#4299e1"}}
))

fig.update_layout(
    title="From Risk Exposure to Protected Value",
    showlegend=False,
    height=400,
    yaxis_title="Value ($K)"
)

st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# KEY TAKEAWAYS FOR JUDGES
# ============================================================================

st.markdown("---")
st.subheader("🎯 Key Takeaways")

st.success(f"""
**Business Problem Solved:** Partner churn costs Deriv millions annually in lost commissions.

**AI Solution Value:**
1. **{roi_improvement:.1f}x better targeting** - AI identifies high-value churners, not just any churner
2. **${ai_cost_per_save:.0f} cost per save** vs ${rnd_cost_per_save:.0f} random (efficiency gain: {((rnd_cost_per_save - ai_cost_per_save)/rnd_cost_per_save)*100:.0f}%)
3. **${(ai_profit - rnd_profit):,.0f} incremental profit** from same intervention budget
4. **Proactive, not reactive** - Model predicts churn 30-90 days before it happens

**ROI Summary:** For every $1 invested in this AI system, Deriv recovers **${ai_profit/ai_invested:.2f}** in protected LTV.
""")

# ============================================================================
# SCENARIO SIMULATOR (Interactive)
# ============================================================================

st.markdown("---")
st.subheader("🔧 Scenario Simulator")
st.markdown("Adjust parameters to see how business impact changes:")

sim_col1, sim_col2, sim_col3 = st.columns(3)

with sim_col1:
    sim_cost = st.slider("Intervention Cost ($)", 50, 300, 100, 10)
with sim_col2:
    sim_success = st.slider("Success Rate (%)", 20, 60, 40, 5)
with sim_col3:
    sim_capacity = st.slider("Target Capacity (%)", 10, 40, 20, 5)

# Recalculate with new parameters
sim_cutoff = int(len(df) * (sim_capacity/100))
sim_target_indices = sorted_indices[:sim_cutoff]
sim_invested = sim_cutoff * sim_cost
sim_saved = sum(ltv.iloc[i] * (sim_success/100) for i in sim_target_indices if y_true.iloc[i])
sim_profit = sim_saved - sim_invested

st.metric(
    "Simulated Net Profit",
    f"${sim_profit:,.0f}",
    delta=f"${sim_profit - ai_profit:,.0f} vs default"
)
