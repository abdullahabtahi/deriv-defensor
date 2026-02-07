"""
Seed Intervention History Generator

P1: Outcome Tracking - Creates realistic synthetic intervention history.

This shows 42 saved (~70%), 12 churned (~20%), 6 pending (~10%)
instead of "0 saved, 0 churned" during demo.

Challenge Prompt Alignment:
- "alerts relationship managers before it's too late" -> Proves intervention success
"""

import pandas as pd
import random
from datetime import datetime, timedelta
import os


def generate_intervention_history(n_interventions: int = 60):
    """
    Creates realistic intervention history for demo.
    
    Distribution:
    - 42 saved (~70%) - intervention worked
    - 12 churned (~20%) - intervention failed
    - 6 pending (~10%) - awaiting outcome
    """
    outcomes = (
        ['saved'] * 42 +
        ['churned'] * 12 +
        ['pending'] * 6
    )
    
    # Shuffle for realism
    random.shuffle(outcomes)
    
    team_members = ['John Chen', 'Sarah Miller', 'Michael Brown', 'Lisa Wong', 'David Kim']
    actions = ['email', 'call', 'meeting', 'discount_offer', 'executive_outreach']
    regions = ['MENA', 'EU', 'APAC', 'LATAM', 'NA']
    tiers = ['Platinum', 'Gold', 'Silver', 'Bronze']
    
    history = []
    for i, outcome in enumerate(outcomes):
        days_ago = random.randint(1, 30)
        intervention_date = datetime.now() - timedelta(days=days_ago)
        
        if outcome == 'pending':
            outcome_date = None
            ltv_protected = 0
        elif outcome == 'saved':
            outcome_date = intervention_date + timedelta(days=random.randint(3, 14))
            ltv_protected = random.randint(15000, 80000)  # Revenue protected
        else:  # churned
            outcome_date = intervention_date + timedelta(days=random.randint(7, 21))
            ltv_protected = 0
        
        history.append({
            'partner_id': f'P{18000 + i}',
            'intervention_date': intervention_date.strftime('%Y-%m-%d'),
            'action': random.choice(actions),
            'status': outcome,
            'assigned_to': random.choice(team_members),
            'outcome_date': outcome_date.strftime('%Y-%m-%d') if outcome_date else None,
            'ltv_protected': ltv_protected,
            'region': random.choice(regions),
            'tier': random.choice(tiers),
            'risk_score_at_intervention': round(random.uniform(0.75, 0.98), 2)
        })
    
    df = pd.DataFrame(history)
    
    # Ensure data directory exists
    os.makedirs('data', exist_ok=True)
    
    df.to_csv('data/intervention_log.csv', index=False)
    
    # Summary stats
    saved = df[df['status'] == 'saved']
    churned = df[df['status'] == 'churned']
    pending = df[df['status'] == 'pending']
    
    print("✅ Intervention History Generated")
    print(f"   📊 Total: {len(df)} records")
    print(f"   ✅ Saved: {len(saved)} partners (${saved['ltv_protected'].sum():,.0f} LTV protected)")
    print(f"   ❌ Churned: {len(churned)} partners")
    print(f"   ⏳ Pending: {len(pending)} partners")
    print(f"   📈 Success Rate: {len(saved) / (len(saved) + len(churned)) * 100:.1f}%")
    
    return df


if __name__ == '__main__':
    generate_intervention_history()
