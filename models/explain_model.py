import pandas as pd
import numpy as np
import pickle
import json

class ExplainabilityEngine:
    def __init__(self):
        self.stats = {}
        self.feature_importance = {}
        
    def fit(self, df_train, feature_cols):
        """
        Learn baseline statistics from training data (ideally healthy partners).
        """
        print("Fitting explainability engine...")
        for col in feature_cols:
            # Ensure numeric type for stats calculation
            series = pd.to_numeric(df_train[col], errors='coerce').fillna(0).astype(float)
            
            self.stats[col] = {
                'mean': series.mean(),
                'std': series.std() or 1.0,  # Avoid div/0
                'p75': series.quantile(0.75),
                'p25': series.quantile(0.25)
            }
            
        print("✅ Explainability engine fit complete.")
        
    def explain(self, partner_row, top_k=3):
        """
        Generate reason codes based on deviation from 'normal'.
        returns: List of dicts [{'feature': 'login_trend', 'score': 2.5, 'desc': 'Declining rapidly'}]
        """
        reasons = []
        
        for feat, stat in self.stats.items():
            val = partner_row.get(feat, 0)
            try:
                val = float(val)
            except (ValueError, TypeError):
                continue
            
            # 1. Z-score deviation
            z_score = (val - stat['mean']) / stat['std']
            
            # 2. Risk direction logic (Business Rules)
            # define which direction is 'bad' for each feature
            impact_score = 0
            description = ""
            
            if feat == 'login_trend_30d' and val < 0:
                impact_score = abs(z_score) * 2.0  # High weight
                description = f"Engagement dropping (Trend: {val})"
            elif feat == 'days_since_last_interaction' and val > stat['p75']:
                impact_score = abs(z_score) * 1.5
                description = f"Silent for {val} days"
            elif feat == 'payment_delay_flag' and val == 1:
                impact_score = 10.0  # Immediate flag
                description = "Payment delayed"
            elif feat == 'tier_proximity_score' and val < 0.1:
                impact_score = (1.0 - val) * 5.0
                description = "Close to tier demotion"
            elif feat == 'subnetwork_recent_churn_count' and val > 0:
                 impact_score = val * 3.0
                 description = f"{int(val)} sub-affiliate churns"
            # Add more rules as needed...
            
            if impact_score > 0.5:
                reasons.append({
                    'feature': feat,
                    'impact_score': impact_score,
                    'description': description,
                    'value': val
                })
        
        # Sort by impact
        reasons = sorted(reasons, key=lambda x: x['impact_score'], reverse=True)
        return reasons[:top_k]

if __name__ == "__main__":
    # Test run
    try:
        df = pd.read_csv('dataset/partners.csv')
        # Load features list from training script logic (hardcoded here for now)
        feature_cols = [
            'login_count_30d', 'login_trend_30d', 'days_since_last_interaction',
            'revenue_velocity', 'conversion_rate_wow', 'commission_trend_90d',
            'payment_delay_flag', 'unresolved_ticket_count', 'negative_sentiment_score',
            'subnetwork_avg_health_score', 'subnetwork_recent_churn_count',
            'tier_proximity_score', 'tenure_months', 'avg_commission_3m'
        ]
        
        explainer = ExplainabilityEngine()
        explainer.fit(df, feature_cols)
        
        # Test on a known high-risk partner (e.g., P00001 Tier Cliff)
        p1 = df[df['partner_id'] == 'P00001'].iloc[0]
        print(f"\\nExplaining P00001 (Tier Cliff):")
        print(json.dumps(explainer.explain(p1), indent=2))

        # Test on Trust Erosion (P00002)
        p2 = df[df['partner_id'] == 'P00002'].iloc[0]
        print(f"\\nExplaining P00002 (Trust Erosion):")
        print(json.dumps(explainer.explain(p2), indent=2))
        
        # Save explainer
        with open('models/explainer.pkl', 'wb') as f:
            pickle.dump(explainer, f)
            
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error: {e}")
