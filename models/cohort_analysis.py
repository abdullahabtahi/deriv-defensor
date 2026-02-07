import pandas as pd
import numpy as np

class CohortAnalyzer:
    def __init__(self, data_path='dataset/partners.csv'):
        try:
            self.df = pd.read_csv(data_path)
        except FileNotFoundError:
            self.df = pd.DataFrame()
            print(f"Warning: {data_path} not found.")

    def analyze_regional_risk(self, threshold_multiplier=1.2):
        """
        Identify regions with churn rates significantly higher than global average.
        """
        if self.df.empty: return {}
        
        global_churn = self.df['churn_label'].mean()
        region_stats = self.df.groupby('region')['churn_label'].agg(['mean', 'count']).reset_index()
        region_stats.columns = ['region', 'churn_rate', 'partner_count']
        
        high_risk_regions = region_stats[
            region_stats['churn_rate'] > (global_churn * threshold_multiplier)
        ].copy()
        
        high_risk_regions['risk_factor'] = high_risk_regions['churn_rate'] / global_churn
        
        return {
            'global_churn_rate': global_churn,
            'high_risk_regions': high_risk_regions.to_dict('records')
        }

    def analyze_tier_risk(self):
        """
        Analyze churn risk by tier, specifically focusing on 'Tier Cliff' (partners near demotion).
        """
        if self.df.empty: return {}
        
        tier_stats = self.df.groupby('tier')['churn_label'].agg(['mean', 'count']).reset_index()
        
        # Analyze Tier Cliff (High proximity score + High churn risk)
        # Assuming 'tier_proximity_score' < 0.1 is "At Risk" of demotion
        if 'tier_proximity_score' in self.df.columns:
            cliff_partners = self.df[self.df['tier_proximity_score'] < 0.1]
            cliff_churn_rate = cliff_partners['churn_label'].mean()
        else:
            cliff_churn_rate = 0.0
            
        return {
            'tier_stats': tier_stats.to_dict('records'),
            'tier_cliff_churn_rate': cliff_churn_rate
        }

    def analyze_network_contagion(self):
        """
        Identify Master Affiliates with high sub-affiliate churn (Contagion).
        """
        if self.df.empty: return []
        
        if 'is_master_affiliate' not in self.df.columns:
            return []
            
        masters = self.df[self.df['is_master_affiliate'] == True].copy()
        
        # High risk masters: >50% subs churning or > 2 recent churns
        risky_masters = masters[
            (masters['subnetwork_recent_churn_count'] > 2) |
            (masters['subnetwork_avg_health_score'] < 50) # Assuming <50 means >50% churn roughly
        ]
        
        return risky_masters[['partner_id', 'region', 'tier', 'subnetwork_recent_churn_count']].head(10).to_dict('records')

if __name__ == "__main__":
    analyzer = CohortAnalyzer()
    
    print("--- Regional Risk ---")
    print(analyzer.analyze_regional_risk())
    
    print("\n--- Tier Risk ---")
    print(analyzer.analyze_tier_risk())
    
    print("\n--- Network Contagion ---")
    print(analyzer.analyze_network_contagion())
