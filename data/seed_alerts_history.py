"""
Seed Alerts History Data

Generates realistic alert history for demo purposes.
- 15 alerts over past 7 days
- Mix of acknowledged (10) and pending (5)
- Various severity levels and alert types
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import uuid
import random

np.random.seed(42)
random.seed(42)

def generate_alerts_history(n_alerts=15):
    """
    Generate synthetic alert history for demo.
    """
    alerts = []
    
    # Generate alert distribution
    # 5 pending (recent), 10 acknowledged (older)
    for i in range(n_alerts):
        # Spread over 7 days
        days_ago = random.randint(0, 7)
        hours_ago = random.randint(0, 23)
        timestamp = datetime.now() - timedelta(days=days_ago, hours=hours_ago)
        
        # More recent alerts are pending
        acknowledged = days_ago > 2 or random.random() > 0.6
        
        # Severity distribution: 60% high, 30% medium, 10% low
        severity = np.random.choice(
            ['high', 'medium', 'low'],
            p=[0.6, 0.3, 0.1]
        )
        
        # Alert types
        alert_type = random.choice(['churn_risk', 'urgency_escalation', 'cohort_warning'])
        
        alerts.append({
            'alert_id': str(uuid.uuid4())[:8],
            'partner_id': f'P{10000 + random.randint(1, 9000):05d}',
            'alert_type': alert_type,
            'severity': severity,
            'sent_to': random.choice(['dashboard', 'john@example.com', 'sarah@example.com']),
            'timestamp': timestamp.isoformat(),
            'acknowledged': acknowledged
        })
    
    df = pd.DataFrame(alerts)
    df = df.sort_values('timestamp', ascending=False)
    return df

if __name__ == '__main__':
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, 'alerts_history.csv')
    
    alerts_df = generate_alerts_history(15)
    alerts_df.to_csv(output_path, index=False)
    
    print("✅ Generated alerts_history.csv")
    print(f"   Path: {output_path}")
    print(f"   Total: {len(alerts_df)}")
    print(f"   Pending: {len(alerts_df[alerts_df['acknowledged'] == False])}")
    print(f"   Acknowledged: {len(alerts_df[alerts_df['acknowledged'] == True])}")
    print(f"\nSeverity Distribution:")
    print(alerts_df['severity'].value_counts())
