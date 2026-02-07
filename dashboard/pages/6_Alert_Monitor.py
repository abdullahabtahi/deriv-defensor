"""
Alert Monitor Dashboard Page

Gap 4: Intelligent Alerting System
- Real-time alert history
- Acknowledgment workflow
- Alert configuration
- Alert frequency analytics
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import get_pending_alerts, acknowledge_alert

st.set_page_config(page_title="Alert Monitor", page_icon="🔔", layout="wide")

st.title("🔔 Alert Monitor")
st.markdown("*Real-time monitoring of high-risk partner alerts*")

# Summary Metrics
col1, col2, col3, col4 = st.columns(4)

try:
    alerts_df = pd.read_csv('data/alerts_history.csv')
    
    pending = alerts_df[alerts_df['acknowledged'] == False]
    acknowledged = alerts_df[alerts_df['acknowledged'] == True]
    high_severity = alerts_df[alerts_df['severity'] == 'high']
    
    col1.metric("📥 Pending Alerts", len(pending), delta=f"+{len(pending[pending['timestamp'] > (datetime.now() - timedelta(hours=24)).isoformat()]) if len(pending) > 0 else 0} today")
    col2.metric("✅ Acknowledged", len(acknowledged))
    col3.metric("🔴 High Severity", len(high_severity))
    col4.metric("📊 Total Alerts", len(alerts_df))
    
except FileNotFoundError:
    col1.metric("📥 Pending Alerts", 0)
    col2.metric("✅ Acknowledged", 0)
    col3.metric("🔴 High Severity", 0)
    col4.metric("📊 Total Alerts", 0)
    st.info("No alerts yet. Alerts are generated when high-risk partners cross the threshold.")
    alerts_df = pd.DataFrame()

st.divider()

# Alert Configuration
with st.expander("⚙️ Alert Configuration", expanded=False):
    st.markdown("**Threshold Settings**")
    col1, col2 = st.columns(2)
    
    with col1:
        risk_threshold = st.slider(
            "Risk Score Threshold",
            min_value=0.5, max_value=1.0, value=0.85, step=0.05,
            help="Alert when partner risk exceeds this threshold"
        )
        
    with col2:
        urgency_filter = st.multiselect(
            "Alert on Urgency Levels",
            options=["🔴 Critical (7 days)", "🟡 Warning (30 days)", "🟢 Watch (90 days)"],
            default=["🔴 Critical (7 days)"]
        )
    
    st.markdown("**Notification Channels (Demo Mode)**")
    col3, col4 = st.columns(2)
    with col3:
        st.checkbox("📧 Email Alerts", value=True, disabled=True, help="In demo mode, emails are logged but not sent")
    with col4:
        st.checkbox("💬 Slack Alerts", value=False, disabled=True, help="Configure Slack webhook in production")

st.divider()

# Pending Alerts Section
st.subheader("📥 Pending Alerts")

if len(alerts_df) > 0 and len(pending) > 0:
    # Display pending alerts as cards
    for idx, alert in pending.head(10).iterrows():
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            
            severity_color = "🔴" if alert.get('severity') == 'high' else "🟡"
            
            with col1:
                st.markdown(f"**{severity_color} {alert.get('partner_id', 'N/A')}**")
                st.caption(f"Alert Type: {alert.get('alert_type', 'N/A')}")
            
            with col2:
                try:
                    ts = datetime.fromisoformat(str(alert.get('timestamp', '')))
                    st.markdown(f"⏰ {ts.strftime('%Y-%m-%d %H:%M')}")
                except:
                    st.markdown(f"⏰ {alert.get('timestamp', 'N/A')}")
            
            with col3:
                st.markdown(f"📫 Sent to: `{alert.get('sent_to', 'dashboard')}`")
            
            with col4:
                if st.button("✅ Ack", key=f"ack_{alert.get('alert_id', idx)}"):
                    if acknowledge_alert(str(alert.get('alert_id', ''))):
                        st.toast(f"✅ Alert {alert.get('alert_id')} acknowledged!")
                        st.rerun()
            
            st.divider()
else:
    st.info("🎉 No pending alerts. All alerts have been acknowledged.")

# Alert History
st.subheader("📋 Alert History")

if len(alerts_df) > 0:
    # Alert Type Distribution
    col1, col2 = st.columns(2)
    
    with col1:
        if 'alert_type' in alerts_df.columns:
            fig_type = px.pie(
                alerts_df, 
                names='alert_type', 
                title='Alert Type Distribution',
                color_discrete_sequence=['#00d4ff', '#ff6b6b', '#ffd93d']
            )
            st.plotly_chart(fig_type, use_container_width=True)
    
    with col2:
        if 'severity' in alerts_df.columns:
            fig_severity = px.pie(
                alerts_df, 
                names='severity', 
                title='Severity Distribution',
                color_discrete_sequence=['#ff4b4b', '#ffa500', '#4caf50']
            )
            st.plotly_chart(fig_severity, use_container_width=True)
    
    # Full Table
    st.dataframe(
        alerts_df.sort_values('timestamp', ascending=False),
        use_container_width=True,
        hide_index=True
    )
    
    # Export Button
    csv = alerts_df.to_csv(index=False)
    st.download_button(
        "📥 Export Alert History",
        csv,
        "alerts_history.csv",
        "text/csv",
        key='download_alerts'
    )
else:
    st.info("No alert history available.")

# Footer
st.divider()
st.caption("""
💡 **How Alerts Work:** 
The system monitors partner risk scores in real-time. When a partner crosses the configured threshold 
AND shows critical urgency signals (🔴 ~7 days), an alert is generated and logged. 
In production, these alerts would trigger email/Slack notifications to Relationship Managers.
""")
