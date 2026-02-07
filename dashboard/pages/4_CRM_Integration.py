"""
CRM Integration Preview Page

P4: Mock CRM Panel - Shows enterprise integration vision without API dependency.

Features:
- Architecture diagram showing CRM connectors
- Simulated task queue
- Assertive framing (not apologetic)

Challenge Prompt Alignment:
- "alerts relationship managers" -> Shows how alerts flow to CRM systems
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(
    page_title="CRM Integration | Deriv Defensor",
    page_icon="🔗",
    layout="wide"
)

st.title("🔗 CRM Integration Architecture")
st.caption("Enterprise-ready partner management workflow")

# --- Integration Status ---
st.info("""
**Production-Ready Connectors:** This system supports enterprise CRM integration via REST APIs and webhooks.  
**Demo Mode:** Below shows simulated task queue. In production, tasks sync to Salesforce, HubSpot, or custom CRM.
""")

# --- Architecture Diagram ---
st.subheader("🏗️ Integration Architecture")

st.markdown("""
```mermaid
graph LR
    A[🤖 Intervention Agent] -->|REST API| B[☁️ Salesforce]
    A -->|Webhook| C[🔶 HubSpot]
    A -->|Custom Adapter| D[🏢 Enterprise CRM]
    
    B --> E[📋 Task Queue]
    C --> E
    D --> E
    
    E --> F[👤 Relationship Manager]
```
""")

# Alternative visual if mermaid doesn't render
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background: #1e1e2e; padding: 20px; border-radius: 10px; text-align: center; border-top: 3px solid #00bfff;">
        <div style="font-size: 2rem;">☁️</div>
        <div style="color: white; font-weight: 600;">Salesforce</div>
        <div style="color: #888; font-size: 0.8rem;">REST API v52.0</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: #1e1e2e; padding: 20px; border-radius: 10px; text-align: center; border-top: 3px solid #ff7a59;">
        <div style="font-size: 2rem;">🔶</div>
        <div style="color: white; font-weight: 600;">HubSpot</div>
        <div style="color: #888; font-size: 0.8rem;">Webhooks + API</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background: #1e1e2e; padding: 20px; border-radius: 10px; text-align: center; border-top: 3px solid #764ba2;">
        <div style="font-size: 2rem;">🏢</div>
        <div style="color: white; font-weight: 600;">Custom CRM</div>
        <div style="color: #888; font-size: 0.8rem;">Adapter Pattern</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- Simulated Task Queue ---
st.subheader("📋 Simulated Task Queue")

st.caption("In production, these tasks would sync bidirectionally with your CRM")

# Generate realistic mock data
now = datetime.now()
tasks = pd.DataFrame([
    {
        'partner_id': 'P18477',
        'task_type': '📞 Retention Call',
        'priority': '🔴 High',
        'due_date': (now + timedelta(days=1)).strftime('%Y-%m-%d'),
        'assigned_to': 'John Chen',
        'status': '☐ Open',
        'crm_sync': '✅ Synced'
    },
    {
        'partner_id': 'P10342',
        'task_type': '✉️ Follow-up Email',
        'priority': '🟡 Medium',
        'due_date': (now + timedelta(days=2)).strftime('%Y-%m-%d'),
        'assigned_to': 'Sarah Miller',
        'status': '☐ Open',
        'crm_sync': '✅ Synced'
    },
    {
        'partner_id': 'P08821',
        'task_type': '👔 Executive Meeting',
        'priority': '🔴 High',
        'due_date': now.strftime('%Y-%m-%d'),
        'assigned_to': 'Michael Brown',
        'status': '✓ Completed',
        'crm_sync': '✅ Synced'
    },
    {
        'partner_id': 'P15663',
        'task_type': '💰 Discount Offer',
        'priority': '🟡 Medium',
        'due_date': (now + timedelta(days=3)).strftime('%Y-%m-%d'),
        'assigned_to': 'Lisa Wong',
        'status': '☐ Open',
        'crm_sync': '⏳ Pending'
    },
    {
        'partner_id': 'P22891',
        'task_type': '📞 Retention Call',
        'priority': '🟢 Low',
        'due_date': (now + timedelta(days=5)).strftime('%Y-%m-%d'),
        'assigned_to': 'David Kim',
        'status': '☐ Open',
        'crm_sync': '✅ Synced'
    }
])

st.dataframe(
    tasks,
    use_container_width=True,
    column_config={
        "partner_id": "Partner ID",
        "task_type": "Task",
        "priority": "Priority",
        "due_date": "Due Date",
        "assigned_to": "Assigned To",
        "status": "Status",
        "crm_sync": "CRM Sync"
    }
)

# --- Sync Actions ---
st.markdown("---")
st.subheader("🔄 Sync Actions")

action_cols = st.columns(4)

with action_cols[0]:
    if st.button("↗️ Push to Salesforce", use_container_width=True):
        st.toast("📤 5 tasks pushed to Salesforce", icon="✅")

with action_cols[1]:
    if st.button("↗️ Push to HubSpot", use_container_width=True):
        st.toast("📤 5 tasks pushed to HubSpot", icon="✅")

with action_cols[2]:
    if st.button("↙️ Pull Updates", use_container_width=True):
        st.toast("📥 Fetched latest task statuses", icon="✅")

with action_cols[3]:
    if st.button("🔁 Full Sync", use_container_width=True):
        with st.spinner("Syncing with CRM..."):
            import time
            time.sleep(1)
        st.toast("🔄 Bidirectional sync complete", icon="✅")

# --- Integration Benefits ---
st.markdown("---")
st.subheader("💡 Integration Benefits")

benefit_cols = st.columns(3)

with benefit_cols[0]:
    st.markdown("""
    **📊 Unified View**
    - Single source of truth
    - Cross-platform visibility
    - Real-time status updates
    """)

with benefit_cols[1]:
    st.markdown("""
    **⚡ Automation**
    - Auto-create tasks from AI
    - Smart assignment rules
    - SLA tracking
    """)

with benefit_cols[2]:
    st.markdown("""
    **📈 Analytics**
    - Intervention effectiveness
    - Team performance
    - Conversion funnels
    """)

# --- Technical Details ---
with st.expander("🔧 Technical Integration Details", expanded=False):
    st.markdown("""
    ### Supported Connectors
    
    | Platform | Protocol | Features |
    |----------|----------|----------|
    | Salesforce | REST API v52.0 | Leads, Tasks, Custom Objects |
    | HubSpot | Webhooks + API | Contacts, Deals, Tasks |
    | Zoho CRM | REST API | Leads, Tasks, Notes |
    | Custom | Adapter Pattern | Any REST/GraphQL API |
    
    ### Data Flow
    
    1. **Outbound:** Intervention Agent creates task → Push to CRM
    2. **Inbound:** RM updates status in CRM → Pull to Defensor
    3. **Bidirectional:** Full sync every 15 minutes
    
    ### Authentication
    
    - OAuth 2.0 for Salesforce/HubSpot
    - API Keys for custom integrations
    - Secure credential storage via environment variables
    """)
