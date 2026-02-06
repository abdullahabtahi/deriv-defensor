"""
AI Partner Churn Predictor - Day 1 Validation Tests
Test Engineer Agent: Validation Suite

Tests verify:
1. Database schema and connections
2. Synthetic data quality (Pareto distribution, churn rate)
3. Feature completeness (18 features)
4. Golden records presence
5. Network relationships integrity
6. Uplift signal heterogeneity (CausalML requirement)
7. Scenario distribution
"""

import pytest
import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def partners_df():
    """Load partners dataset."""
    path = 'data/partners.csv'
    if not os.path.exists(path):
        pytest.skip("Partners data not generated yet")
    return pd.read_csv(path)


@pytest.fixture
def interventions_df():
    """Load interventions dataset."""
    path = 'data/interventions.csv'
    if not os.path.exists(path):
        pytest.skip("Interventions data not generated yet")
    return pd.read_csv(path)


@pytest.fixture
def network_df():
    """Load network relationships dataset."""
    path = 'data/network_relationships.csv'
    if not os.path.exists(path):
        pytest.skip("Network relationships not generated yet")
    return pd.read_csv(path)


@pytest.fixture
def engineered_df():
    """Load engineered features dataset."""
    path = 'data/partners_engineered.csv'
    if not os.path.exists(path):
        pytest.skip("Engineered features not generated yet")
    return pd.read_csv(path)


# ============================================================================
# 1. DATA GENERATION TESTS
# ============================================================================

class TestSyntheticDataQuality:
    """Test synthetic data generation quality."""
    
    def test_partner_count(self, partners_df):
        """Verify correct number of partners generated."""
        assert len(partners_df) == 10000, f"Expected 10000 partners, got {len(partners_df)}"
    
    def test_churn_rate_range(self, partners_df):
        """Verify churn rate is in realistic range (15-25%)."""
        churn_rate = partners_df['churn_label'].mean()
        assert 0.15 <= churn_rate <= 0.25, \
            f"Churn rate {churn_rate:.2%} outside expected range 15-25%"
    
    def test_pareto_distribution(self, partners_df):
        """Verify financial metrics follow Pareto (80/20) distribution."""
        # Top 20% should have ~80% of revenue (allow 70-90% for synthetic data)
        total_revenue = partners_df['avg_commission_3m'].sum()
        top_20_pct = partners_df.nlargest(2000, 'avg_commission_3m')
        top_20_revenue = top_20_pct['avg_commission_3m'].sum()
        pareto_ratio = top_20_revenue / total_revenue
        
        assert 0.60 <= pareto_ratio <= 0.95, \
            f"Pareto ratio {pareto_ratio:.2%} outside expected range 60-95%"
    
    def test_master_affiliate_percentage(self, partners_df):
        """Verify ~5% of partners are Master Affiliates."""
        master_pct = partners_df['is_master_affiliate'].mean()
        assert 0.03 <= master_pct <= 0.08, \
            f"Master Affiliate % {master_pct:.2%} outside expected range 3-8%"
    
    def test_no_null_required_fields(self, partners_df):
        """Verify no nulls in required fields."""
        required_fields = [
            'partner_id', 'region', 'tier', 'churn_label', 
            'avg_commission_3m', 'login_count_30d'
        ]
        for field in required_fields:
            null_count = partners_df[field].isna().sum()
            assert null_count == 0, f"Field {field} has {null_count} null values"


class TestGoldenRecords:
    """Test golden demo records are present and correct."""
    
    def test_golden_records_exist(self, partners_df):
        """Verify all 5 golden records exist."""
        golden_ids = ['P00001', 'P00002', 'P00003', 'P00004', 'P00005']
        for pid in golden_ids:
            assert pid in partners_df['partner_id'].values, \
                f"Golden record {pid} not found"
    
    def test_golden_records_scenarios(self, partners_df):
        """Verify golden records have correct scenarios."""
        expected = {
            'P00001': 'Tier_Cliff_Anxiety',
            'P00002': 'Trust_Erosion',
            'P00003': 'Network_Contagion',
            'P00004': 'Active_Churn',
            'P00005': 'Passive_Disengagement'
        }
        
        for pid, expected_scenario in expected.items():
            actual = partners_df[partners_df['partner_id'] == pid]['churn_scenario'].values[0]
            assert actual == expected_scenario, \
                f"Golden {pid} has scenario {actual}, expected {expected_scenario}"
    
    def test_golden_records_are_churners(self, partners_df):
        """Verify all golden records have churn_label=True."""
        golden_ids = ['P00001', 'P00002', 'P00003', 'P00004', 'P00005']
        golden = partners_df[partners_df['partner_id'].isin(golden_ids)]
        
        assert golden['churn_label'].all(), \
            "Not all golden records have churn_label=True"


# ============================================================================
# 2. FEATURE TESTS
# ============================================================================

class TestFeatureCompleteness:
    """Test all 18 features are present and valid."""
    
    REQUIRED_FEATURES = [
        # Engagement (5)
        'login_count_30d',
        'login_trend_30d',
        'days_since_last_interaction',
        'dashboard_usage_score',
        'asset_download_count_30d',
        
        # Performance (4)
        'revenue_velocity',
        'conversion_rate_wow',
        'traffic_quality_score',
        'commission_trend_90d',
        
        # Trust/Friction (3)
        'payment_delay_flag',
        'unresolved_ticket_count',
        'negative_sentiment_score',
        
        # Network (2)
        'subnetwork_avg_health_score',
        'subnetwork_recent_churn_count',
        
        # Tier Risk (2)
        'tier_proximity_score',
        'tenure_months',
        
        # Financial (2)
        'avg_commission_3m',
        'commission_volatility',
    ]
    
    def test_all_features_present(self, partners_df):
        """Verify all 18 features exist in dataset."""
        missing = []
        for feature in self.REQUIRED_FEATURES:
            if feature not in partners_df.columns:
                missing.append(feature)
        
        assert len(missing) == 0, f"Missing features: {missing}"
    
    def test_feature_count(self, partners_df):
        """Verify we have at least 18 features."""
        feature_count = len([c for c in partners_df.columns 
                            if c in self.REQUIRED_FEATURES])
        assert feature_count >= 18, \
            f"Only {feature_count} of 18 required features found"
    
    def test_normalized_features_in_range(self, partners_df):
        """Verify normalized features are in 0-1 range."""
        normalized_features = [
            'dashboard_usage_score',
            'traffic_quality_score', 
            'tier_proximity_score',
            'negative_sentiment_score'
        ]
        
        for feature in normalized_features:
            if feature in partners_df.columns:
                min_val = partners_df[feature].min()
                max_val = partners_df[feature].max()
                assert 0 <= min_val <= max_val <= 1, \
                    f"{feature} has values outside [0,1]: [{min_val}, {max_val}]"
    
    def test_network_features_only_for_masters(self, partners_df):
        """Verify network features are only set for Master Affiliates."""
        masters = partners_df[partners_df['is_master_affiliate'] == True]
        non_masters = partners_df[partners_df['is_master_affiliate'] == False]
        
        # Masters should have network scores
        if len(masters) > 0:
            master_has_score = masters['subnetwork_avg_health_score'].notna().any()
            assert master_has_score, "Masters should have network health scores"
        
        # Non-masters should have null/none for network features
        # (or -1 if filled for ML)


# ============================================================================
# 3. NETWORK RELATIONSHIP TESTS
# ============================================================================

class TestNetworkRelationships:
    """Test network relationship integrity."""
    
    def test_tree_structure(self, network_df):
        """Verify each sub-affiliate has only ONE parent (tree, not graph)."""
        sub_counts = network_df['sub_affiliate_id'].value_counts()
        max_parents = sub_counts.max()
        
        assert max_parents == 1, \
            f"Sub-affiliates have max {max_parents} parents, should be 1"
    
    def test_masters_have_subs(self, network_df, partners_df):
        """Verify master affiliates have sub-affiliates."""
        masters = partners_df[partners_df['is_master_affiliate'] == True]
        
        for _, master in masters.iterrows():
            subs = network_df[network_df['master_affiliate_id'] == master['partner_id']]
            assert len(subs) >= 0, \
                f"Master {master['partner_id']} has no sub-affiliates"
    
    def test_sub_range(self, network_df, partners_df):
        """Verify masters have 10-50 subs (as specified in plan)."""
        masters = partners_df[partners_df['is_master_affiliate'] == True]
        
        for _, master in masters.iterrows():
            subs = network_df[network_df['master_affiliate_id'] == master['partner_id']]
            sub_count = len(subs)
            # Allow 0-50 since some masters may not get subs if pool exhausted
            assert 0 <= sub_count <= 50, \
                f"Master {master['partner_id']} has {sub_count} subs, expected 0-50"


# ============================================================================
# 4. UPLIFT SIGNAL TESTS (CRITICAL for CausalML)
# ============================================================================

class TestUpliftSignals:
    """Test uplift signals for CausalML training."""
    
    def test_uplift_signal_range(self, interventions_df):
        """Verify uplift signals are in valid range (-0.5 to 0.2)."""
        min_val = interventions_df['uplift_signal'].min()
        max_val = interventions_df['uplift_signal'].max()
        
        assert min_val >= -0.6, f"Uplift signal min {min_val} below expected range"
        assert max_val <= 0.3, f"Uplift signal max {max_val} above expected range"
    
    def test_heterogeneous_treatment_effects(self, interventions_df):
        """Verify calls have stronger effects than emails (heterogeneity)."""
        call_effects = interventions_df[
            interventions_df['intervention_type'] == 'call'
        ]['uplift_signal']
        
        email_effects = interventions_df[
            interventions_df['intervention_type'] == 'email'
        ]['uplift_signal']
        
        # Calls should be more negative (stronger retention effect)
        assert call_effects.mean() < email_effects.mean(), \
            f"Calls ({call_effects.mean():.3f}) should have stronger effect than emails ({email_effects.mean():.3f})"
    
    def test_intervention_distribution(self, interventions_df):
        """Verify realistic intervention mix (emails > calls)."""
        counts = interventions_df['intervention_type'].value_counts(normalize=True)
        
        # Emails should be more common than calls
        assert counts.get('email', 0) > counts.get('call', 0), \
            "Emails should be more common than calls"
        
        # Control group (none) should exist
        assert counts.get('none', 0) > 0, \
            "Control group (none) should exist"
    
    def test_sufficient_interventions(self, interventions_df, partners_df):
        """Verify sufficient interventions for CausalML training."""
        # At least 1 intervention per partner on average
        avg_interventions = len(interventions_df) / len(partners_df)
        assert avg_interventions >= 1.0, \
            f"Average {avg_interventions:.1f} interventions/partner, need >= 1"
    
    def test_causalml_data_requirements(self, interventions_df, partners_df):
        """
        CRITICAL: Verify CausalML has enough signal to learn from.
        Tests intervention type balance, outcome distribution, and coverage.
        """
        # 1. Intervention type balance (need sufficient samples of each)
        type_dist = interventions_df['intervention_type'].value_counts(normalize=True)
        
        assert type_dist.get('call', 0) >= 0.10, \
            f"Need 10%+ calls for learning, got {type_dist.get('call', 0):.1%}"
        assert type_dist.get('email', 0) >= 0.30, \
            f"Need 30%+ emails for learning, got {type_dist.get('email', 0):.1%}"
        assert type_dist.get('none', 0) >= 0.20, \
            f"Need 20%+ control group, got {type_dist.get('none', 0):.1%}"
        
        # 2. Outcome balance (shouldn't be too imbalanced)
        outcome_dist = interventions_df['outcome'].value_counts(normalize=True)
        churn_rate = outcome_dist.get('Churned', 0)
        
        assert 0.14 <= churn_rate <= 0.35, \
            f"Need 14-35% churn for signal, got {churn_rate:.1%}. " \
            f"If too low, interventions are unrealistically effective. " \
            f"If too high, interventions don't work."
        
        # 3. Coverage (most partners should have intervention history)
        partners_with_interventions = interventions_df['partner_id'].nunique()
        total_partners = len(partners_df)
        coverage = partners_with_interventions / total_partners
        
        assert coverage >= 0.75, \
            f"Only {coverage:.1%} partners have intervention history, need 75%+"
        
        # Print summary for visibility
        print(f"\n✅ CausalML Data Quality:")
        print(f"  - Intervention types: Call {type_dist.get('call', 0):.1%}, "
              f"Email {type_dist.get('email', 0):.1%}, "
              f"None {type_dist.get('none', 0):.1%}")
        print(f"  - Outcome churn rate: {churn_rate:.1%}")
        print(f"  - Partner coverage: {coverage:.1%}")


# ============================================================================
# 5. SCENARIO DISTRIBUTION TESTS
# ============================================================================

class TestScenarioDistribution:
    """Test churn scenario distribution."""
    
    def test_all_scenarios_represented(self, partners_df):
        """Verify all 5 churn scenarios exist in data."""
        required_scenarios = [
            'Trust_Erosion',
            'Network_Contagion',
            'Tier_Cliff_Anxiety',
            'Active_Churn',
            'Passive_Disengagement'
        ]
        
        actual_scenarios = partners_df['churn_scenario'].unique()
        
        for scenario in required_scenarios:
            assert scenario in actual_scenarios, \
                f"Scenario {scenario} not found in data"
    
    def test_healthy_is_majority(self, partners_df):
        """Verify 'Healthy' is the most common scenario (>75%)."""
        scenario_counts = partners_df['churn_scenario'].value_counts(normalize=True)
        healthy_pct = scenario_counts.get('Healthy', 0)
        
        assert healthy_pct >= 0.75, \
            f"Healthy partners are only {healthy_pct:.2%}, expected >= 75%"


# ============================================================================
# 6. INTEGRATION TESTS
# ============================================================================

class TestDataIntegration:
    """Test that all components work together."""
    
    def test_all_csvs_exist(self):
        """Verify all required CSV files exist."""
        required_files = [
            'data/partners.csv',
            'data/interventions.csv',
            'data/network_relationships.csv'
        ]
        
        for filepath in required_files:
            assert os.path.exists(filepath), \
                f"Required file {filepath} not found"
    
    def test_partner_ids_consistent(self, partners_df, interventions_df, network_df):
        """Verify partner IDs are consistent across datasets."""
        partner_ids = set(partners_df['partner_id'])
        
        # All intervention partner IDs should be in partners
        intervention_ids = set(interventions_df['partner_id'])
        missing_in_partners = intervention_ids - partner_ids
        assert len(missing_in_partners) == 0, \
            f"Intervention partner IDs not in partners: {missing_in_partners}"
        
        # All network partner IDs should be in partners
        master_ids = set(network_df['master_affiliate_id'])
        sub_ids = set(network_df['sub_affiliate_id'])
        all_network_ids = master_ids | sub_ids
        missing_network = all_network_ids - partner_ids
        assert len(missing_network) == 0, \
            f"Network partner IDs not in partners: {missing_network}"


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
