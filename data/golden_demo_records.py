"""
AI Partner Churn Predictor - Golden Demo Records
Day 1: Data Foundation

5 hardcoded partners with specific feature patterns for reliable demo scenarios.
These showcase all churn types identified in the expert review.
"""

from datetime import datetime
from typing import Dict, List

# ============================================================================
# GOLDEN DEMO RECORDS
# ============================================================================
# These partners have fixed, predictable values for demos
# They cover the 5 churn scenarios:
# 1. Tier Cliff Anxiety
# 2. Trust Erosion
# 3. Network Contagion
# 4. Active Churn
# 5. Passive Disengagement

GOLDEN_RECORDS: List[Dict] = [
    
    # =========================================================================
    # P00001: TIER CLIFF ANXIETY
    # =========================================================================
    # Story: Gold-tier partner generating $5,200/month, just 4% above the 
    #        $5,000 threshold. One bad month = demotion to Silver. 
    #        Recommended action: Call to discuss retention bonus.
    {
        'partner_id': 'P00001',
        'region': 'LATAM',
        'payment_rail_type': 'Bank',
        'is_master_affiliate': False,
        'tier': 'Gold',
        'tenure_months': 24,
        
        # Engagement - Slightly declining but still active
        'login_count_30d': 12,
        'login_trend_30d': -0.12,  # Mild decline
        'days_since_last_interaction': 7,
        'dashboard_usage_score': 0.55,
        'asset_download_count_30d': 1,
        
        # Performance - Stable but close to threshold
        'revenue_velocity': -15.0,  # Slight deceleration
        'conversion_rate_wow': -0.015,
        'traffic_quality_score': 0.68,
        'commission_trend_90d': -0.03,
        
        # Trust - No major issues
        'payment_delay_flag': False,
        'unresolved_ticket_count': 1,
        'negative_sentiment_score': 0.25,
        
        # Network - N/A (not master)
        'subnetwork_avg_health_score': None,
        'subnetwork_recent_churn_count': None,
        
        # CRITICAL: Tier proximity
        'tier_proximity_score': 0.04,  # 4% above Gold threshold ($5000)
        
        # Financial
        'avg_commission_3m': 5200.00,  # Just above $5000 threshold
        'commission_volatility': 800.0,
        
        # Labels
        'churn_label': True,
        'churn_scenario': 'Tier_Cliff_Anxiety',
        
        # Demo notes
        '_demo_story': 'High-value Gold partner at risk of demotion. '
                       'Call recommended to discuss retention bonus.',
        '_expected_intervention': 'call',
        '_why_model_flags': 'tier_proximity_score = 0.04 (extremely close to cliff)'
    },
    
    # =========================================================================
    # P00002: TRUST EROSION
    # =========================================================================
    # Story: Payment was delayed by 12 days. Partner went silent (21 days 
    #        no interaction). Has 3 open support tickets. Classic trust breakdown.
    #        Recommended action: Urgent call from senior account manager.
    {
        'partner_id': 'P00002',
        'region': 'MENA',
        'payment_rail_type': 'P2P',
        'is_master_affiliate': False,
        'tier': 'Silver',
        'tenure_months': 18,
        
        # Engagement - Severely disengaged
        'login_count_30d': 2,
        'login_trend_30d': -0.35,  # Sharp decline
        'days_since_last_interaction': 21,  # 3 weeks silent
        'dashboard_usage_score': 0.12,
        'asset_download_count_30d': 0,
        
        # Performance - Declining
        'revenue_velocity': -45.0,
        'conversion_rate_wow': -0.04,
        'traffic_quality_score': 0.35,
        'commission_trend_90d': -0.08,
        
        # CRITICAL: Trust issues
        'payment_delay_flag': True,  # Payment delayed >7 days
        'unresolved_ticket_count': 3,  # Multiple open tickets
        'negative_sentiment_score': 0.45,  # Frustrated but not angry
        
        # Network - N/A
        'subnetwork_avg_health_score': None,
        'subnetwork_recent_churn_count': None,
        
        # Tier - Stable
        'tier_proximity_score': 0.45,
        
        # Financial
        'avg_commission_3m': 1800.00,
        'commission_volatility': 450.0,
        
        # Labels
        'churn_label': True,
        'churn_scenario': 'Trust_Erosion',
        
        # Demo notes
        '_demo_story': 'Payment delay + silence = trust erosion. '
                       'Urgent escalation to senior account manager.',
        '_expected_intervention': 'call',
        '_why_model_flags': 'payment_delay_flag + days_since_last_interaction > 14'
    },
    
    # =========================================================================
    # P00003: NETWORK CONTAGION
    # =========================================================================
    # Story: Master Affiliate with 35 sub-affiliates. 4 have churned recently.
    #        Network health score dropped to 45%. Contagion risk is real.
    #        Recommended action: VIP call + retention package for entire network.
    {
        'partner_id': 'P00003',
        'region': 'APAC',
        'payment_rail_type': 'Crypto',
        'is_master_affiliate': True,  # MASTER
        'tier': 'Platinum',
        'tenure_months': 36,
        
        # Engagement - Moderate but concerning
        'login_count_30d': 8,
        'login_trend_30d': -0.08,
        'days_since_last_interaction': 5,
        'dashboard_usage_score': 0.62,
        'asset_download_count_30d': 2,
        
        # Performance - Still strong
        'revenue_velocity': -25.0,
        'conversion_rate_wow': -0.01,
        'traffic_quality_score': 0.75,
        'commission_trend_90d': -0.02,
        
        # Trust - Generally OK
        'payment_delay_flag': False,
        'unresolved_ticket_count': 1,
        'negative_sentiment_score': 0.30,
        
        # CRITICAL: Network issues
        'subnetwork_avg_health_score': 45.0,  # Very unhealthy network
        'subnetwork_recent_churn_count': 4,   # 4 churned subs!
        
        # Tier - Stable
        'tier_proximity_score': 0.85,
        
        # Financial - High value
        'avg_commission_3m': 15000.00,  # High-value master
        'commission_volatility': 2500.0,
        
        # Labels
        'churn_label': True,
        'churn_scenario': 'Network_Contagion',
        
        # Demo notes
        '_demo_story': 'Master Affiliate with failing network. 4 subs churned. '
                       'VIP retention package for entire sub-affiliate network.',
        '_expected_intervention': 'call',
        '_why_model_flags': 'is_master + subnetwork_recent_churn_count > 2'
    },
    
    # =========================================================================
    # P00004: ACTIVE CHURN (Competitor Poaching)
    # =========================================================================
    # Story: Recent support tickets contain competitor mentions. Sentiment 
    #        analysis shows high frustration (0.82). Actively evaluating alternatives.
    #        Recommended action: Immediate competitive counter-offer.
    {
        'partner_id': 'P00004',
        'region': 'CIS',
        'payment_rail_type': 'Bank',
        'is_master_affiliate': False,
        'tier': 'Silver',
        'tenure_months': 12,
        
        # Engagement - Dropping sharply
        'login_count_30d': 2,
        'login_trend_30d': -0.42,  # Sharp decline
        'days_since_last_interaction': 10,
        'dashboard_usage_score': 0.15,
        'asset_download_count_30d': 0,
        
        # Performance - Declining
        'revenue_velocity': -65.0,
        'conversion_rate_wow': -0.05,
        'traffic_quality_score': 0.28,
        'commission_trend_90d': -0.12,
        
        # CRITICAL: Active dissatisfaction
        'payment_delay_flag': False,
        'unresolved_ticket_count': 2,
        'negative_sentiment_score': 0.82,  # Very negative!
        
        # Network - N/A
        'subnetwork_avg_health_score': None,
        'subnetwork_recent_churn_count': None,
        
        # Tier - At risk
        'tier_proximity_score': 0.18,
        
        # Financial
        'avg_commission_3m': 1400.00,
        'commission_volatility': 380.0,
        
        # Labels
        'churn_label': True,
        'churn_scenario': 'Active_Churn',
        
        # Demo notes
        '_demo_story': 'Competitor signals detected. High negative sentiment. '
                       'Immediate competitive counter-offer required.',
        '_expected_intervention': 'call',
        '_why_model_flags': 'negative_sentiment_score > 0.7 (competitor frustration)'
    },
    
    # =========================================================================
    # P00005: PASSIVE DISENGAGEMENT
    # =========================================================================
    # Story: Gradual decline in all metrics. No specific trigger, just 
    #        fading away. Classic passive churn pattern.
    #        Recommended action: Re-engagement email campaign first.
    {
        'partner_id': 'P00005',
        'region': 'Africa',
        'payment_rail_type': 'Mobile_Money',
        'is_master_affiliate': False,
        'tier': 'Bronze',
        'tenure_months': 8,
        
        # CRITICAL: Passive decline
        'login_count_30d': 3,
        'login_trend_30d': -0.25,  # Steady decline
        'days_since_last_interaction': 12,
        'dashboard_usage_score': 0.22,
        'asset_download_count_30d': 0,
        
        # Performance - Steadily declining
        'revenue_velocity': -120.0,  # Significant deceleration
        'conversion_rate_wow': -0.03,
        'traffic_quality_score': 0.35,
        'commission_trend_90d': -0.15,  # Long-term decline
        
        # Trust - No major issues (passive, not angry)
        'payment_delay_flag': False,
        'unresolved_ticket_count': 0,
        'negative_sentiment_score': 0.18,  # Not vocal
        
        # Network - N/A
        'subnetwork_avg_health_score': None,
        'subnetwork_recent_churn_count': None,
        
        # Tier - Not at risk (Bronze)
        'tier_proximity_score': 0.95,  # Far from any threshold
        
        # Financial
        'avg_commission_3m': 650.00,
        'commission_volatility': 180.0,
        
        # Labels
        'churn_label': True,
        'churn_scenario': 'Passive_Disengagement',
        
        # Demo notes
        '_demo_story': 'Classic passive churn - gradual fade. Lower LTV, '
                       'so email campaign is cost-effective first step.',
        '_expected_intervention': 'email',
        '_why_model_flags': 'login_trend + revenue_velocity declining, no acute trigger'
    }
]


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_golden_records() -> List[Dict]:
    """Return list of golden demo records."""
    # Remove internal demo notes before returning
    records = []
    for r in GOLDEN_RECORDS:
        clean = {k: v for k, v in r.items() if not k.startswith('_')}
        records.append(clean)
    return records


def get_golden_record_by_id(partner_id: str) -> Dict:
    """Get a specific golden record by ID."""
    for r in GOLDEN_RECORDS:
        if r['partner_id'] == partner_id:
            return r
    return {}


def get_demo_stories() -> Dict[str, str]:
    """Get demo stories for each golden record."""
    return {r['partner_id']: r.get('_demo_story', '') for r in GOLDEN_RECORDS}


def get_expected_interventions() -> Dict[str, str]:
    """Get expected interventions for validation."""
    return {r['partner_id']: r.get('_expected_intervention', '') for r in GOLDEN_RECORDS}


# ============================================================================
# VALIDATION
# ============================================================================

def validate_golden_records() -> bool:
    """
    Validate that golden records cover all required scenarios.
    """
    scenarios = set()
    for r in GOLDEN_RECORDS:
        scenarios.add(r['churn_scenario'])
    
    required = {
        'Tier_Cliff_Anxiety',
        'Trust_Erosion', 
        'Network_Contagion',
        'Active_Churn',
        'Passive_Disengagement'
    }
    
    missing = required - scenarios
    
    if missing:
        print(f"❌ Missing scenarios: {missing}")
        return False
    
    print(f"✅ All {len(required)} churn scenarios covered by golden records")
    return True


if __name__ == '__main__':
    validate_golden_records()
    
    print("\nGolden Record Summary:")
    print("-" * 60)
    for r in GOLDEN_RECORDS:
        print(f"{r['partner_id']}: {r['churn_scenario']}")
        print(f"  Story: {r.get('_demo_story', 'N/A')[:60]}...")
        print(f"  Intervention: {r.get('_expected_intervention', 'N/A')}")
        print()
