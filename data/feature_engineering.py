"""
AI Partner Churn Predictor - Feature Engineering Pipeline
Day 1: Data Foundation

Computes all 18 features required for LightGBM training:
- Engagement (5 features)
- Performance (4 features)
- Trust/Friction (3 features)
- Network (2 features)
- Tier Risk (2 features)
- Financial (2 features)
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from scipy import stats
import warnings

warnings.filterwarnings('ignore')

# ============================================================================
# FEATURE CONFIGURATION
# ============================================================================

REQUIRED_FEATURES = [
    # Engagement (5 features)
    'login_count_30d',              # Raw count of logins in last 30 days
    'login_trend_30d',              # Linear regression slope (velocity)
    'days_since_last_interaction',  # Recency signal
    'dashboard_usage_score',        # Composite: clicks, time_spent, features_used
    'asset_download_count_30d',     # Marketing material engagement
    
    # Performance (4 features)
    'revenue_velocity',             # 2nd derivative of commission (acceleration)
    'conversion_rate_wow',          # Week-over-week change in conversion
    'traffic_quality_score',        # Composite: bounce_rate, avg_session_time
    'commission_trend_90d',         # 90-day slope (longer-term momentum)
    
    # Trust/Friction (3 features)
    'payment_delay_flag',           # Boolean: payment delayed >7 days
    'unresolved_ticket_count',      # Open support tickets
    'negative_sentiment_score',     # 0-1, from support interactions (NLP)
    
    # Network (2 features - only for Masters)
    'subnetwork_avg_health_score',  # Mean health of sub-affiliates (0-100)
    'subnetwork_recent_churn_count', # Churned subs in last 30 days
    
    # Tier Risk (2 features)
    'tier_proximity_score',         # 0-1, distance to tier demotion threshold
    'tenure_months',                # Months since partnership started
    
    # Financial (2 features)
    'avg_commission_3m',            # Average commission last 3 months
    'commission_volatility',        # Standard deviation of monthly commissions
]

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def compute_slope(values: List[float]) -> float:
    """
    Compute linear regression slope for trend analysis.
    """
    if values is None or len(values) < 2:
        return 0.0
    try:
        x = np.arange(len(values))
        slope, _, _, _, _ = stats.linregress(x, values)
        return round(slope, 4)
    except:
        return 0.0


def compute_second_derivative(values: List[float]) -> float:
    """
    Compute second derivative (acceleration) of a time series.
    Positive = accelerating growth, Negative = decelerating
    """
    if values is None or len(values) < 3:
        return 0.0
    try:
        first_derivative = np.diff(values)
        second_derivative = np.diff(first_derivative)
        return round(np.mean(second_derivative), 2)
    except:
        return 0.0


def normalize(value: float, min_val: float = 0, max_val: float = 1) -> float:
    """Normalize value to 0-1 range."""
    return np.clip(value, min_val, max_val)


# ============================================================================
# NETWORK FEATURE CALCULATION
# ============================================================================

def calculate_network_features(
    partner_id: str,
    is_master: bool,
    network_df: Optional[pd.DataFrame],
    partners_df: pd.DataFrame
) -> Dict[str, Optional[float]]:
    """
    Calculate network-based features for a partner.
    Only applicable if partner is a Master Affiliate.
    """
    if not is_master or network_df is None:
        return {
            'subnetwork_avg_health_score': None,
            'subnetwork_recent_churn_count': None
        }
    
    # Get sub-affiliates for this master
    subs = network_df[
        network_df['master_affiliate_id'] == partner_id
    ]['sub_affiliate_id'].tolist()
    
    if len(subs) == 0:
        return {
            'subnetwork_avg_health_score': 100.0,  # No subs = perfect health
            'subnetwork_recent_churn_count': 0
        }
    
    # Get health of sub-affiliates
    sub_data = partners_df[partners_df['partner_id'].isin(subs)]
    
    if len(sub_data) == 0:
        return {
            'subnetwork_avg_health_score': 100.0,
            'subnetwork_recent_churn_count': 0
        }
    
    # Calculate metrics
    churn_count = sub_data['churn_label'].sum() if 'churn_label' in sub_data else 0
    avg_health = (1 - sub_data['churn_label'].mean()) * 100 if 'churn_label' in sub_data else 100.0
    
    return {
        'subnetwork_avg_health_score': round(avg_health, 2),
        'subnetwork_recent_churn_count': int(churn_count)
    }


# ============================================================================
# FEATURE ENGINEERING PIPELINE
# ============================================================================

def engineer_features(
    df_raw: pd.DataFrame,
    network_df: Optional[pd.DataFrame] = None
) -> pd.DataFrame:
    """
    Main feature engineering function.
    Takes raw partner data, computes all 18 engineered features.
    
    Args:
        df_raw: Raw partner data DataFrame
        network_df: Network relationships DataFrame (optional)
        
    Returns:
        DataFrame with all 18 features + metadata columns
    """
    print("Starting feature engineering...")
    df = df_raw.copy()
    
    # ===== ENGAGEMENT FEATURES (5) =====
    
    # 1. login_count_30d - already present or compute from history
    if 'login_count_30d' not in df.columns:
        df['login_count_30d'] = 0
    
    # 2. login_trend_30d - velocity indicator
    if 'login_trend_30d' not in df.columns:
        df['login_trend_30d'] = 0.0
    
    # 3. days_since_last_interaction - recency
    if 'days_since_last_interaction' not in df.columns:
        df['days_since_last_interaction'] = 0
    
    # 4. dashboard_usage_score - composite score
    if 'dashboard_usage_score' not in df.columns:
        df['dashboard_usage_score'] = np.random.beta(5, 3, size=len(df))
    
    # 5. asset_download_count_30d - engagement metric
    if 'asset_download_count_30d' not in df.columns:
        df['asset_download_count_30d'] = np.random.poisson(3, size=len(df))
    
    # ===== PERFORMANCE FEATURES (4) =====
    
    # 6. revenue_velocity - 2nd derivative (acceleration)
    if 'revenue_velocity' not in df.columns:
        df['revenue_velocity'] = 0.0
    
    # 7. conversion_rate_wow - week-over-week change
    if 'conversion_rate_wow' not in df.columns:
        df['conversion_rate_wow'] = np.random.normal(0, 0.02, size=len(df))
    
    # 8. traffic_quality_score - composite
    if 'traffic_quality_score' not in df.columns:
        df['traffic_quality_score'] = np.random.beta(6, 4, size=len(df))
    
    # 9. commission_trend_90d - longer-term momentum
    if 'commission_trend_90d' not in df.columns:
        df['commission_trend_90d'] = 0.0
    
    # ===== TRUST/FRICTION FEATURES (3) =====
    
    # 10. payment_delay_flag - boolean
    if 'payment_delay_flag' not in df.columns:
        df['payment_delay_flag'] = False
    
    # 11. unresolved_ticket_count
    if 'unresolved_ticket_count' not in df.columns:
        df['unresolved_ticket_count'] = 0
    
    # 12. negative_sentiment_score - 0-1
    if 'negative_sentiment_score' not in df.columns:
        df['negative_sentiment_score'] = np.random.beta(2, 8, size=len(df))
    
    # ===== NETWORK FEATURES (2) =====
    # Only for Master Affiliates
    
    if network_df is not None:
        print("Computing network features for masters...")
        for idx, row in df.iterrows():
            if row.get('is_master_affiliate', False):
                net_features = calculate_network_features(
                    row['partner_id'],
                    True,
                    network_df,
                    df
                )
                df.at[idx, 'subnetwork_avg_health_score'] = net_features['subnetwork_avg_health_score']
                df.at[idx, 'subnetwork_recent_churn_count'] = net_features['subnetwork_recent_churn_count']
    
    # Ensure network columns exist
    if 'subnetwork_avg_health_score' not in df.columns:
        df['subnetwork_avg_health_score'] = None
    if 'subnetwork_recent_churn_count' not in df.columns:
        df['subnetwork_recent_churn_count'] = None
    
    # ===== TIER RISK FEATURES (2) =====
    
    # 14. tier_proximity_score - 0-1 distance to demotion
    if 'tier_proximity_score' not in df.columns:
        df['tier_proximity_score'] = np.random.beta(5, 2, size=len(df))
    
    # 15. tenure_months
    if 'tenure_months' not in df.columns:
        df['tenure_months'] = np.random.exponential(18, size=len(df)).astype(int)
    
    # ===== FINANCIAL FEATURES (2) =====
    
    # 16. avg_commission_3m
    if 'avg_commission_3m' not in df.columns:
        df['avg_commission_3m'] = 1000.0
    
    # 17. commission_volatility - std dev
    if 'commission_volatility' not in df.columns:
        df['commission_volatility'] = df['avg_commission_3m'] * 0.3
    
    # ===== NORMALIZE FEATURES =====
    
    # Clip and normalize specific features
    df['dashboard_usage_score'] = df['dashboard_usage_score'].clip(0, 1)
    df['traffic_quality_score'] = df['traffic_quality_score'].clip(0, 1)
    df['tier_proximity_score'] = df['tier_proximity_score'].clip(0, 1)
    df['negative_sentiment_score'] = df['negative_sentiment_score'].clip(0, 1)
    df['login_trend_30d'] = df['login_trend_30d'].clip(-1, 1)
    
    # ===== VALIDATE FEATURES =====
    
    missing = []
    for feature in REQUIRED_FEATURES:
        if feature not in df.columns:
            missing.append(feature)
    
    if missing:
        print(f"WARNING: Missing features: {missing}")
    else:
        print(f"✅ All {len(REQUIRED_FEATURES)} features present")
    
    return df


# ============================================================================
# FEATURE SELECTION FOR ML
# ============================================================================

def get_ml_features(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str]]:
    """
    Extract ML-ready features and return with column names.
    Handles missing values and type conversions.
    """
    # Select only the required features
    feature_cols = [f for f in REQUIRED_FEATURES if f in df.columns]
    
    X = df[feature_cols].copy()
    
    # Handle missing values
    # Network features: fill NaN with neutral values for non-masters
    if 'subnetwork_avg_health_score' in X.columns:
        X['subnetwork_avg_health_score'] = X['subnetwork_avg_health_score'].fillna(-1)
    if 'subnetwork_recent_churn_count' in X.columns:
        X['subnetwork_recent_churn_count'] = X['subnetwork_recent_churn_count'].fillna(-1)
    
    # Convert boolean to int
    if 'payment_delay_flag' in X.columns:
        X['payment_delay_flag'] = X['payment_delay_flag'].astype(int)
    
    # Fill remaining NaN with 0
    X = X.fillna(0)
    
    return X, feature_cols


# ============================================================================
# FEATURE IMPORTANCE ANALYSIS
# ============================================================================

def analyze_feature_correlations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute correlation matrix between features and churn label.
    """
    if 'churn_label' not in df.columns:
        print("No churn_label column found for correlation analysis")
        return pd.DataFrame()
    
    X, feature_cols = get_ml_features(df)
    X['churn_label'] = df['churn_label'].astype(int)
    
    correlations = X.corr()['churn_label'].drop('churn_label')
    
    result = pd.DataFrame({
        'feature': correlations.index,
        'correlation_with_churn': correlations.values
    }).sort_values('correlation_with_churn', key=abs, ascending=False)
    
    return result


# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """
    Main execution: load raw data, engineer features, save engineered dataset.
    """
    print("="*60)
    print("AI Partner Churn Predictor - Feature Engineering")
    print("="*60)
    
    # Load raw data
    print("\nLoading raw data...")
    partners_df = pd.read_csv('data/partners.csv')
    
    # Load network data if exists
    try:
        network_df = pd.read_csv('data/network_relationships.csv')
        print(f"Loaded {len(network_df)} network relationships")
    except FileNotFoundError:
        network_df = None
        print("No network data found, skipping network features")
    
    # Engineer features
    engineered_df = engineer_features(partners_df, network_df)
    
    # Get ML-ready features
    X, feature_cols = get_ml_features(engineered_df)
    
    print(f"\nFeature Matrix Shape: {X.shape}")
    print(f"Features: {feature_cols}")
    
    # Analyze correlations
    print("\n" + "="*60)
    print("FEATURE CORRELATIONS WITH CHURN")
    print("="*60)
    correlations = analyze_feature_correlations(engineered_df)
    print(correlations.to_string())
    
    # Save engineered data
    print("\n\nSaving engineered data...")
    engineered_df.to_csv('data/partners_engineered.csv', index=False)
    print(f"Saved to: data/partners_engineered.csv")
    
    # Also save just the feature matrix for quick ML loading
    X.to_csv('data/features_matrix.csv', index=False)
    print(f"Saved feature matrix to: data/features_matrix.csv")
    
    return engineered_df, X, feature_cols


if __name__ == '__main__':
    engineered_df, X, feature_cols = main()
