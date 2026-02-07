"""
Agent Control Panel Page

P3: Agentic AI - Dashboard for controlling the Intervention Agent.

Features:
- Configure risk threshold and batch size
- Manual "Run Agent" button
- Real-time progress display
- Activity log viewer

Challenge Prompt Alignment:
- "alerts relationship managers before it's too late" -> Autonomous batch intervention
"""

import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
import pickle
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from agents.intervention_agent import InterventionAgent
from agents.genai_explainer import GenAIExplainer

st.set_page_config(
    page_title="Agent Control | Deriv Defensor",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Intervention Agent Control Panel")
st.caption("Autonomous AI-powered partner intervention system")

# --- Load Resources ---
@st.cache_data
def load_data():
    df = pd.read_csv('dataset/partners.csv')
    return df

@st.cache_resource
def load_model():
    try:
        with open('models/lgb_churn_model.pkl', 'rb') as f:
            return pickle.load(f)
    except:
        return None

@st.cache_resource
def load_explainer():
    try:
        with open('models/explainer.pkl', 'rb') as f:
            return pickle.load(f)
    except:
        return None

df = load_data()
model = load_model()
explainer = load_explainer()
genai = GenAIExplainer()

# Generate predictions if model exists
if model is not None:
    try:
        feature_cols = [c for c in df.columns if c not in ['partner_id', 'churn_label', 'ltv']]
        X = df[feature_cols].select_dtypes(include=[np.number])
        df['risk_score'] = model.predict_proba(X)[:, 1]
    except Exception as e:
        df['risk_score'] = np.random.uniform(0.3, 0.95, len(df))
else:
    df['risk_score'] = np.random.uniform(0.3, 0.95, len(df))

# Initialize agent
agent = InterventionAgent(model=model, explainer=explainer, genai=genai)

# --- Agent Status ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("⚙️ Agent Configuration")

with col2:
    api_status = "🟢 Claude API Active" if genai.client else "🟡 Template Mode"
    st.info(api_status)

# --- Configuration ---
config_cols = st.columns(3)

with config_cols[0]:
    threshold = st.slider(
        "Risk Threshold",
        min_value=0.70,
        max_value=0.95,
        value=0.85,
        step=0.05,
        help="Only intervene on partners above this risk score"
    )

with config_cols[1]:
    batch_limit = st.slider(
        "Batch Size",
        min_value=5,
        max_value=50,
        value=15,
        step=5,
        help="Maximum partners to process in one batch"
    )

with config_cols[2]:
    # Preview count
    high_risk_count = len(df[df['risk_score'] > threshold])
    st.metric(
        "Partners Above Threshold",
        high_risk_count,
        delta=f"Top {batch_limit} will be processed"
    )

st.markdown("---")

# --- Agent Actions ---
st.subheader("🚀 Agent Actions")

action_cols = st.columns([2, 1, 1])

with action_cols[0]:
    if st.button("🔍 Scan for High-Risk Partners", use_container_width=True):
        with st.spinner("Scanning partner database..."):
            targets = agent.scan_for_interventions(df, threshold, batch_limit)
            st.session_state['scan_results'] = targets
            st.success(f"Found {len(targets)} partners above {threshold:.0%} risk threshold")

with action_cols[1]:
    if st.button("✉️ Execute Interventions", type="primary", use_container_width=True):
        if 'scan_results' not in st.session_state or not st.session_state['scan_results']:
            st.warning("Please scan for partners first")
        else:
            targets = st.session_state['scan_results']
            
            st.subheader("📊 Processing Interventions...")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            results = []
            for i, partner in enumerate(targets):
                status_text.text(f"Processing {partner.get('partner_id', 'Unknown')}...")
                result = agent.execute_intervention(partner)
                results.append(result)
                progress_bar.progress((i + 1) / len(targets))
                time.sleep(0.2)  # Brief delay for visual effect
            
            st.session_state['batch_results'] = results
            st.balloons()
            st.success(f"✅ Completed {len(results)} interventions!")
            st.cache_data.clear()

with action_cols[2]:
    if st.button("🔄 Clear Queue", use_container_width=True):
        st.session_state.pop('scan_results', None)
        st.session_state.pop('batch_results', None)
        st.info("Queue cleared")

# --- Scan Results Preview ---
if 'scan_results' in st.session_state and st.session_state['scan_results']:
    st.markdown("---")
    st.subheader("📋 Scan Results (Ready for Intervention)")
    
    scan_df = pd.DataFrame(st.session_state['scan_results'])
    display_cols = ['partner_id', 'risk_score', 'tier', 'region']
    available_cols = [c for c in display_cols if c in scan_df.columns]
    
    st.dataframe(
        scan_df[available_cols] if available_cols else scan_df.head(),
        use_container_width=True,
        column_config={
            "risk_score": st.column_config.ProgressColumn("Risk Score", min_value=0, max_value=1)
        }
    )

# --- Batch Results ---
if 'batch_results' in st.session_state and st.session_state['batch_results']:
    st.markdown("---")
    st.subheader("📧 Generated Interventions")
    
    for result in st.session_state['batch_results'][:3]:  # Show first 3
        with st.expander(f"🎯 {result['partner_id']} ({result['risk_score']:.0%} risk)", expanded=False):
            st.markdown("**AI Explanation:**")
            st.markdown(result['explanation'])
            
            st.markdown("**Draft Email:**")
            st.text_area(
                "Email",
                result['email'],
                height=150,
                key=f"email_{result['partner_id']}",
                disabled=True
            )

# --- Activity Log ---
st.markdown("---")
st.subheader("📜 Recent Agent Activity")

try:
    log = pd.read_csv('data/intervention_log.csv')
    agent_log = log[log['assigned_to'] == 'AI Agent'].tail(10)
    
    if not agent_log.empty:
        st.dataframe(
            agent_log[['partner_id', 'intervention_date', 'action', 'status']],
            use_container_width=True
        )
    else:
        st.info("No AI Agent activity yet. Run interventions to see results here.")
except FileNotFoundError:
    st.info("Intervention log not found. Run `python data/seed_intervention_history.py` to initialize.")

# --- Agent Architecture Info ---
with st.expander("ℹ️ How the Agent Works", expanded=False):
    st.markdown("""
    ### Intervention Agent Workflow
    
    ```
    1. SCAN → Identify partners above risk threshold
    2. ANALYZE → Generate SHAP-based reason codes
    3. EXPLAIN → GenAI synthesizes human-readable insight
    4. DRAFT → Create personalized retention email
    5. LOG → Record intervention in audit trail
    ```
    
    ### Guardrails
    - **Rate Limiting:** Max 50 interventions per batch
    - **Audit Trail:** All actions logged to `data/intervention_log.csv`
    - **Human Review:** Platinum partners flagged for manager approval
    - **Fallback Mode:** Template-based generation if Claude API unavailable
    """)
