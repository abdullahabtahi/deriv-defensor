"""
AI Partner Churn Predictor - Synthetic Data Generator
Day 1: Data Foundation

Generates 10,000 synthetic partners with realistic distributions:
- Pareto distribution for financial metrics (80/20 rule)
- Feature correlations matching real-world patterns
- Ground truth uplift signals for CausalML training
- Network relationships for graph analysis
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import random
import uuid
from scipy import stats
import json

# Reproducibility
np.random.seed(42)
random.seed(42)

# ============================================================================
# CONFIGURATION
# ============================================================================

# Domain constants matching Deriv's partner ecosystem
REGIONS = ['LATAM', 'APAC', 'EMEA', 'MENA', 'CIS', 'Africa']
REGION_WEIGHTS = [0.25, 0.20, 0.20, 0.15, 0.10, 0.10]

PAYMENT_RAILS = ['Bank', 'Crypto', 'P2P', 'Agent', 'Mobile_Money']
PAYMENT_WEIGHTS = [0.30, 0.25, 0.20, 0.15, 0.10]

TIERS = ['Bronze', 'Silver', 'Gold', 'Platinum']
TIER_WEIGHTS = [0.60, 0.25, 0.10, 0.05]

TIER_THRESHOLDS = {
    'Bronze': 0,
    'Silver': 1000,
    'Gold': 5000,
    'Platinum': 25000
}

CHURN_SCENARIOS = [
    'Trust_Erosion',       # Payment issues + silence
    'Network_Contagion',   # Master with failing subs
    'Tier_Cliff_Anxiety',  # Close to demotion
    'Active_Churn',        # Competitor signals
    'Passive_Disengagement' # Declining engagement
]

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def pareto_sample(alpha: float = 1.0, scale: float = 500, 
                  min_val: float = 100, max_val: float = 100000) -> float:
    """
    Generate Pareto-distributed values for financial metrics.
    Alpha=1.0 creates strong 80/20 distribution (heavier tail).
    """
    sample = (np.random.pareto(alpha) + 1) * scale
    return np.clip(sample, min_val, max_val)


def weighted_choice(choices: List[str], weights: List[float]) -> str:
    """Weighted random choice."""
    return np.random.choice(choices, p=weights)


def compute_slope(values: List[float]) -> float:
    """Compute linear regression slope for trend."""
    if len(values) < 2:
        return 0.0
    x = np.arange(len(values))
    slope, _, _, _, _ = stats.linregress(x, values)
    return round(slope, 4)


# ============================================================================
# VELOCITY FEATURE GENERATION (Pre-computed for efficiency)
# ============================================================================

def generate_velocity_features(churn_label: bool) -> Dict[str, float]:
    """
    Pre-compute slope/velocity features with realistic distributions.
    Churners show declining trends, healthy partners show stable/growth.
    
    This is more efficient than generating full 30-day time series.
    """
    if churn_label:
        # Churners: declining engagement and revenue
        login_trend = np.random.normal(loc=-0.15, scale=0.25)
        revenue_velocity = np.random.normal(loc=-80, scale=40)
        commission_trend_90d = np.random.normal(loc=-0.08, scale=0.12)
        conversion_rate_wow = np.random.normal(loc=-0.03, scale=0.02)
    else:
        # Healthy partners: stable or growing
        login_trend = np.random.normal(loc=0.05, scale=0.2)
        revenue_velocity = np.random.normal(loc=10, scale=30)
        commission_trend_90d = np.random.normal(loc=0.02, scale=0.08)
        conversion_rate_wow = np.random.normal(loc=0.01, scale=0.015)
    
    return {
        'login_trend_30d': round(np.clip(login_trend, -1, 1), 3),
        'revenue_velocity': round(revenue_velocity, 2),
        'commission_trend_90d': round(np.clip(commission_trend_90d, -0.5, 0.5), 3),
        'conversion_rate_wow': round(np.clip(conversion_rate_wow, -0.2, 0.2), 4)
    }


# ============================================================================
# CHURN SCORE CALCULATION
# ============================================================================

def calculate_churn_score(partner: Dict) -> float:
    """
    Calculate churn probability based on feature patterns.
    Returns 0-1 score; threshold at 0.65 for churn label.
    """
    score = 0.0
    
    # Engagement signals (weight: 0.3)
    if partner.get('login_count_30d', 15) < 5:
        score += 0.15
    if partner.get('days_since_last_interaction', 0) > 14:
        score += 0.10
    if partner.get('dashboard_usage_score', 0.5) < 0.2:
        score += 0.05
    
    # Trust/Friction signals (weight: 0.25)
    if partner.get('payment_delay_flag', False):
        score += 0.12
    if partner.get('unresolved_ticket_count', 0) > 2:
        score += 0.08
    if partner.get('negative_sentiment_score', 0) > 0.6:
        score += 0.05
    
    # Tier risk (weight: 0.20)
    if partner.get('tier_proximity_score', 1.0) < 0.1:
        score += 0.15
    if partner.get('tenure_months', 12) < 3:
        score += 0.05
    
    # Financial decline (weight: 0.15)
    if partner.get('avg_commission_3m', 1000) < 500:
        score += 0.10
    if partner.get('commission_volatility', 0) > 2000:
        score += 0.05
    
    # Network contagion (weight: 0.10) - only for Masters
    if partner.get('is_master_affiliate', False):
        if partner.get('subnetwork_recent_churn_count', 0) > 2:
            score += 0.10
    
    # Add some noise
    score += np.random.normal(0, 0.05)
    
    return np.clip(score, 0, 1)


# ============================================================================
# SCENARIO ASSIGNMENT
# ============================================================================

def assign_churn_scenario(partner: Dict) -> str:
    """
    Assign churn scenario based on feature patterns.
    Ground truth labels for Pattern Discovery validation.
    """
    if not partner.get('churn_label', False):
        return 'Healthy'
    
    # Trust Erosion: payment issues + silence
    if (partner.get('payment_delay_flag', False) and 
        partner.get('days_since_last_interaction', 0) > 14):
        return 'Trust_Erosion'
    
    # Network Contagion: master with failing network
    if (partner.get('is_master_affiliate', False) and 
        partner.get('subnetwork_recent_churn_count', 0) > 2):
        return 'Network_Contagion'
    
    # Tier Cliff: close to demotion
    if partner.get('tier_proximity_score', 1.0) < 0.05:
        return 'Tier_Cliff_Anxiety'
    
    # Active Churn: high negative sentiment
    if partner.get('negative_sentiment_score', 0) > 0.7:
        return 'Active_Churn'
    
    # Default: Passive disengagement
    return 'Passive_Disengagement'


# ============================================================================
# PARTNER GENERATION
# ============================================================================

def generate_single_partner(partner_id: str, force_scenario: Optional[str] = None) -> Dict:
    """
    Generate a single synthetic partner with all 18 features.
    """
    # Base attributes
    partner = {
        'partner_id': partner_id,
        'region': weighted_choice(REGIONS, REGION_WEIGHTS),
        'payment_rail_type': weighted_choice(PAYMENT_RAILS, PAYMENT_WEIGHTS),
        'is_master_affiliate': random.random() < 0.05,  # 5% are Masters
        'tier': weighted_choice(TIERS, TIER_WEIGHTS),
        'tenure_months': max(1, int(np.random.exponential(scale=18))),
    }
    
    # Financial metrics (Pareto distributed)
    partner['avg_commission_3m'] = round(pareto_sample(alpha=1.16, scale=1000), 2)
    partner['commission_volatility'] = round(
        abs(np.random.normal(loc=partner['avg_commission_3m'] * 0.3, scale=200)), 2
    )
    
    # Engagement metrics
    partner['login_count_30d'] = max(0, int(np.random.normal(15, 8)))
    partner['days_since_last_interaction'] = max(0, int(np.random.exponential(5)))
    partner['dashboard_usage_score'] = round(np.clip(np.random.beta(5, 3), 0, 1), 4)
    partner['asset_download_count_30d'] = max(0, int(np.random.poisson(3)))
    
    # Trust/Friction metrics
    partner['payment_delay_flag'] = random.random() < 0.08  # 8% have delays
    partner['unresolved_ticket_count'] = max(0, int(np.random.poisson(0.5)))
    partner['negative_sentiment_score'] = round(np.clip(np.random.beta(2, 8), 0, 1), 2)
    
    # Tier proximity (distance to demotion threshold)
    tier_threshold = TIER_THRESHOLDS.get(partner['tier'], 0)
    if tier_threshold > 0:
        distance = (partner['avg_commission_3m'] - tier_threshold) / tier_threshold
        partner['tier_proximity_score'] = round(np.clip(distance, 0, 1), 4)
    else:
        partner['tier_proximity_score'] = 1.0  # Bronze can't be demoted
    
    # Performance metrics (will be updated with velocity features)
    partner['traffic_quality_score'] = round(np.clip(np.random.beta(6, 4), 0, 1), 4)
    
    # Network features (placeholder - updated after network generation)
    partner['subnetwork_avg_health_score'] = None if not partner['is_master_affiliate'] else 85.0
    partner['subnetwork_recent_churn_count'] = 0
    
    # Calculate churn probability and assign label
    # Use direct probability (20% base) + feature-based adjustments
    # This ensures realistic ~20% churn rate
    if force_scenario:
        partner['churn_label'] = force_scenario != 'Healthy'
    else:
        # Base churn probability: 18% + feature adjustments
        churn_prob = 0.18
        
        # Increase churn probability based on risk factors
        if partner.get('login_count_30d', 15) < 5:
            churn_prob += 0.15
        if partner.get('days_since_last_interaction', 0) > 14:
            churn_prob += 0.12
        if partner.get('payment_delay_flag', False):
            churn_prob += 0.20
        if partner.get('tier_proximity_score', 1.0) < 0.1:
            churn_prob += 0.15
        if partner.get('negative_sentiment_score', 0) > 0.5:
            churn_prob += 0.10
        
        # Decrease churn probability based on protective factors  
        if partner.get('tenure_months', 0) > 24:
            churn_prob -= 0.08
        if partner.get('avg_commission_3m', 0) > 5000:
            churn_prob -= 0.05
        if partner.get('dashboard_usage_score', 0) > 0.7:
            churn_prob -= 0.05
            
        # Stochastic churn assignment
        partner['churn_label'] = np.random.binomial(1, np.clip(churn_prob, 0, 0.9)) == 1
    
    # Add velocity features based on churn status
    velocity = generate_velocity_features(partner['churn_label'])
    partner.update(velocity)
    
    # Assign scenario
    if force_scenario:
        partner['churn_scenario'] = force_scenario
    else:
        partner['churn_scenario'] = assign_churn_scenario(partner)
    
    # Timestamps
    partner['created_at'] = datetime.now().isoformat()
    partner['updated_at'] = datetime.now().isoformat()
    
    return partner


def generate_golden_records() -> List[Dict]:
    """
    Generate 5 hardcoded golden demo records for reliable demo scenarios.
    """
    golden_records = []
    
    # P00001: Tier Cliff Anxiety - High LTV partner close to demotion
    p1 = generate_single_partner('P00001', force_scenario='Tier_Cliff_Anxiety')
    p1.update({
        'tier': 'Gold',
        'avg_commission_3m': 5200.00,  # Just above $5000 threshold
        'tier_proximity_score': 0.04,   # 4% above cliff
        'churn_label': True,
        'login_trend_30d': -0.12,
        'days_since_last_interaction': 7
    })
    golden_records.append(p1)
    
    # P00002: Trust Erosion - Payment issues + silence
    p2 = generate_single_partner('P00002', force_scenario='Trust_Erosion')
    p2.update({
        'payment_delay_flag': True,
        'days_since_last_interaction': 21,
        'negative_sentiment_score': 0.45,
        'unresolved_ticket_count': 3,
        'churn_label': True
    })
    golden_records.append(p2)
    
    # P00003: Network Contagion - Master with churning subs
    p3 = generate_single_partner('P00003', force_scenario='Network_Contagion')
    p3.update({
        'is_master_affiliate': True,
        'subnetwork_recent_churn_count': 4,
        'subnetwork_avg_health_score': 45.0,
        'churn_label': True,
        'avg_commission_3m': 15000.00  # High LTV master
    })
    golden_records.append(p3)
    
    # P00004: Active Churn - Competitor signals
    p4 = generate_single_partner('P00004', force_scenario='Active_Churn')
    p4.update({
        'negative_sentiment_score': 0.82,  # High negative sentiment
        'login_count_30d': 2,
        'dashboard_usage_score': 0.15,
        'churn_label': True
    })
    golden_records.append(p4)
    
    # P00005: Passive Disengagement - Declining engagement
    p5 = generate_single_partner('P00005', force_scenario='Passive_Disengagement')
    p5.update({
        'login_trend_30d': -0.25,
        'login_count_30d': 3,
        'days_since_last_interaction': 12,
        'revenue_velocity': -120.0,
        'churn_label': True
    })
    golden_records.append(p5)
    
    return golden_records


def generate_partners(n: int = 10000) -> pd.DataFrame:
    """
    Generate n synthetic partners including golden records.
    """
    print(f"Generating {n} synthetic partners...")
    
    # Start with golden records
    partners = generate_golden_records()
    
    # Generate remaining partners
    for i in range(5, n):
        partner_id = f'P{10000 + i:05d}'
        partners.append(generate_single_partner(partner_id))
    
    df = pd.DataFrame(partners)
    
    # Validate churn rate
    churn_rate = df['churn_label'].mean()
    print(f"Generated churn rate: {churn_rate:.2%}")
    
    # Validate Pareto distribution
    top_20_pct = df.nlargest(int(n * 0.2), 'avg_commission_3m')
    pareto_ratio = top_20_pct['avg_commission_3m'].sum() / df['avg_commission_3m'].sum()
    print(f"Top 20% revenue share: {pareto_ratio:.2%} (target: ~80%)")
    
    return df


# ============================================================================
# NETWORK RELATIONSHIPS GENERATION
# ============================================================================

def generate_network_relationships(partners_df: pd.DataFrame) -> pd.DataFrame:
    """
    Create master -> sub-affiliate relationships.
    Each master has 10-50 unique sub-affiliates (tree structure).
    """
    print("Generating network relationships...")
    
    masters = partners_df[partners_df['is_master_affiliate'] == True].copy()
    non_masters = partners_df[partners_df['is_master_affiliate'] == False].copy()
    
    relationships = []
    available_subs = non_masters.copy()
    
    for _, master in masters.iterrows():
        # Each master gets 10-50 subs (or remaining if fewer)
        n_subs = min(np.random.randint(10, 51), len(available_subs))
        
        if n_subs == 0:
            continue
        
        # Assign UNIQUE subs to this master (tree, not graph)
        assigned_subs = available_subs.sample(n=n_subs)
        
        for _, sub in assigned_subs.iterrows():
            # Random recruitment date (30-365 days ago)
            recruited_date = datetime.now() - timedelta(
                days=np.random.randint(30, 366)
            )
            
            relationships.append({
                'relationship_id': str(uuid.uuid4()),
                'master_affiliate_id': master['partner_id'],
                'sub_affiliate_id': sub['partner_id'],
                'recruited_at': recruited_date.isoformat(),
                'is_active': True,
                'created_at': datetime.now().isoformat()
            })
        
        # Remove assigned subs from pool (enforce uniqueness)
        available_subs = available_subs.drop(assigned_subs.index)
    
    print(f"Generated {len(relationships)} network relationships")
    return pd.DataFrame(relationships)


def update_network_features(partners_df: pd.DataFrame, 
                           network_df: pd.DataFrame) -> pd.DataFrame:
    """
    Update network features for master affiliates based on sub-affiliate health.
    """
    print("Updating network features for masters...")
    
    partners = partners_df.copy()
    
    for idx, partner in partners.iterrows():
        if not partner['is_master_affiliate']:
            continue
        
        # Get sub-affiliates for this master
        subs = network_df[
            network_df['master_affiliate_id'] == partner['partner_id']
        ]['sub_affiliate_id'].tolist()
        
        if len(subs) == 0:
            continue
        
        # Calculate network health from sub-affiliate churn status
        sub_data = partners[partners['partner_id'].isin(subs)]
        churn_count = sub_data['churn_label'].sum()
        avg_health = (1 - sub_data['churn_label'].mean()) * 100
        
        partners.at[idx, 'subnetwork_recent_churn_count'] = int(churn_count)
        partners.at[idx, 'subnetwork_avg_health_score'] = round(avg_health, 2)
    
    return partners


# ============================================================================
# INTERVENTION OUTCOME GENERATION (CRITICAL for CausalML)
# ============================================================================

def calculate_base_churn_probability(partner: Dict) -> float:
    """
    Calculate baseline churn probability without intervention.
    Uses simplified fixed baseline for clearer intervention signal.
    """
    # Use fixed baseline (18%) + partner risk adjustment
    if partner.get('churn_label', False):
        # At-risk partners: 18-35% baseline
        return np.clip(np.random.uniform(0.18, 0.35), 0, 1)
    else:
        # Healthy partners: 5-15% baseline
        return np.clip(np.random.uniform(0.05, 0.15), 0, 1)


def generate_intervention_outcome(partner: Dict, intervention_type: str) -> Dict:
    """
    Ground truth uplift model (hidden from ML training).
    Models how different interventions work for different partner types.
    
    REBALANCED: Interventions now have 30% failure rate to ensure
    outcome distribution is 15-25% churn (was 6% - too low for CausalML).
    """
    base_churn_prob = calculate_base_churn_probability(partner)
    
    # 40% of interventions fail (some may backfire)
    intervention_failed = np.random.random() < 0.40
    
    if intervention_failed:
        # Failed intervention: minimal effect or slight backfire
        treatment_effect = np.random.uniform(-0.03, 0.08)  # Can backfire!
    else:
        # Successful intervention: heterogeneous effects
        if intervention_type == 'call':
            # Calls work better for:
            # - High LTV partners (relationship value justifies effort)
            # - Trust issues (human touch rebuilds confidence)
            # - Master Affiliates (strategic importance)
            if partner.get('avg_commission_3m', 0) > 10000:
                treatment_effect = -0.14  # Strong retention (further reduced)
            elif partner.get('payment_delay_flag', False):
                treatment_effect = -0.12  # Rebuilds trust (further reduced)
            elif partner.get('is_master_affiliate', False):
                treatment_effect = -0.13  # VIP treatment (further reduced)
            else:
                treatment_effect = -0.05  # Modest effect (further reduced)
                
        elif intervention_type == 'email':
            # Emails work better for:
            # - Medium engagement partners (still checking inbox)
            # - Technical issues (can send documentation)
            # - Tier proximity (can explain grace period)
            if -0.5 < partner.get('login_trend_30d', 0) < 0:
                treatment_effect = -0.08  # Catches mild disengagement (further reduced)
            elif partner.get('unresolved_ticket_count', 0) > 0:
                treatment_effect = -0.06  # Can address specific issues (further reduced)
            elif partner.get('tier_proximity_score', 1.0) < 0.1:
                treatment_effect = -0.10  # Tier anxiety response (further reduced)
            else:
                treatment_effect = -0.03  # Weak signal (further reduced)
                
        else:  # 'none' - control group
            treatment_effect = 0
    
    # Add realistic noise (increased variance for learning signal)
    treatment_effect += np.random.normal(0, 0.15)  # Increased for more variance
    treatment_effect = np.clip(treatment_effect, -0.50, 0.20)
    
    # Final churn probability after intervention
    final_churn_prob = np.clip(base_churn_prob + treatment_effect, 0, 1)
    
    # Simulate outcome (stochastic)
    did_churn = np.random.binomial(1, final_churn_prob)
    
    return {
        'outcome': 'Churned' if did_churn else 'Retained',
        'uplift_signal': round(treatment_effect, 3),
        'final_churn_prob': round(final_churn_prob, 4)
    }


def generate_historical_interventions(partners_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate 1-3 historical interventions per partner for CausalML training.
    """
    print("Generating historical interventions with uplift signals...")
    
    interventions = []
    
    for _, partner in partners_df.iterrows():
        # Randomize number of interventions per partner (1-3)
        n_interventions = np.random.randint(1, 4)
        
        for _ in range(n_interventions):
            # Realistic distribution:
            # - Emails are cheap → most common (45%)
            # - No intervention → control group (40%)
            # - Calls are expensive → rare (15%)
            intervention_type = np.random.choice(
                ['call', 'email', 'none'],
                p=[0.15, 0.45, 0.40]
            )
            
            # Generate outcome based on ground truth causal model
            outcome_data = generate_intervention_outcome(
                partner.to_dict(), intervention_type
            )
            
            # Random past date (30-90 days ago)
            intervention_date = datetime.now() - timedelta(
                days=np.random.randint(30, 91)
            )
            
            interventions.append({
                'intervention_id': str(uuid.uuid4()),
                'partner_id': partner['partner_id'],
                'intervention_type': intervention_type,
                'intervention_date': intervention_date.isoformat(),
                'outcome': outcome_data['outcome'],
                'uplift_signal': outcome_data['uplift_signal'],
                'outcome_recorded_at': (intervention_date + timedelta(days=30)).isoformat(),
                'created_at': datetime.now().isoformat()
            })
    
    df = pd.DataFrame(interventions)
    
    # Validate uplift heterogeneity
    call_effects = df[df['intervention_type'] == 'call']['uplift_signal']
    email_effects = df[df['intervention_type'] == 'email']['uplift_signal']
    
    print(f"Generated {len(df)} interventions")
    print(f"Call avg uplift: {call_effects.mean():.3f}")
    print(f"Email avg uplift: {email_effects.mean():.3f}")
    
    return df


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main execution: generate all synthetic data and save to CSV.
    """
    print("="*60)
    print("AI Partner Churn Predictor - Synthetic Data Generation")
    print("="*60)
    
    # 1. Generate partners
    partners_df = generate_partners(n=10000)
    
    # 2. Generate network relationships
    network_df = generate_network_relationships(partners_df)
    
    # 3. Update network features based on actual relationships
    partners_df = update_network_features(partners_df, network_df)
    
    # 4. Re-assign scenarios after network features updated
    for idx, partner in partners_df.iterrows():
        if partner['partner_id'] not in ['P00001', 'P00002', 'P00003', 'P00004', 'P00005']:
            partners_df.at[idx, 'churn_scenario'] = assign_churn_scenario(partner.to_dict())
    
    # 5. Generate historical interventions
    interventions_df = generate_historical_interventions(partners_df)
    
    # 6. Save to CSV
    print("\nSaving data to CSV...")
    partners_df.to_csv('data/partners.csv', index=False)
    network_df.to_csv('data/network_relationships.csv', index=False)
    interventions_df.to_csv('data/interventions.csv', index=False)
    
    # 7. Print summary
    print("\n" + "="*60)
    print("GENERATION COMPLETE")
    print("="*60)
    print(f"Partners: {len(partners_df):,} records → data/partners.csv")
    print(f"Networks: {len(network_df):,} relationships → data/network_relationships.csv")
    print(f"Interventions: {len(interventions_df):,} records → data/interventions.csv")
    
    # Scenario distribution
    print("\nChurn Scenario Distribution:")
    print(partners_df['churn_scenario'].value_counts())
    
    # Intervention type distribution
    print("\nIntervention Type Distribution:")
    print(interventions_df['intervention_type'].value_counts(normalize=True))
    
    return partners_df, network_df, interventions_df


if __name__ == '__main__':
    partners_df, network_df, interventions_df = main()
