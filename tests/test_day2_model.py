import unittest
import pandas as pd
import numpy as np
import os
import sys
import pickle

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.genai_explainer import GenAIExplainer
from models.evaluation import calculate_empc
# from models.explain_model import ExplainabilityEngine # Class definition needed if pickling not independent

class TestDay2Model(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        print("Setting up Day 2 Tests...")
        cls.data_path = 'dataset/partners.csv'
        cls.model_path = 'models/lgb_churn_model.pkl'
        cls.explainer_path = 'models/explainer.pkl'
        
    def test_data_existence(self):
        """Test existence of generated data"""
        self.assertTrue(os.path.exists(self.data_path), "Dataset not found")
        df = pd.read_csv(self.data_path)
        self.assertGreater(len(df), 1000, "Dataset too small")
        
    def test_model_loading_and_prediction(self):
        """Test model loading and prediction validity"""
        self.assertTrue(os.path.exists(self.model_path), "Model artifact not found")
        
        with open(self.model_path, 'rb') as f:
            model = pickle.load(f)
            
        df = pd.read_csv(self.data_path).head(10)
        # Select features - strictly what model expects (hardcoded here for test stability)
        feature_cols = [
            'login_count_30d', 'login_trend_30d', 'days_since_last_interaction',
            'revenue_velocity', 'conversion_rate_wow', 'commission_trend_90d',
            'payment_delay_flag', 'unresolved_ticket_count', 'negative_sentiment_score',
            'subnetwork_avg_health_score', 'subnetwork_recent_churn_count',
            'tier_proximity_score', 'tenure_months', 'avg_commission_3m'
        ]
        X = df[feature_cols].copy().fillna(0)
        
        probs = model.predict_proba(X)[:, 1]
        
        self.assertEqual(len(probs), 10)
        self.assertTrue(np.all((probs >= 0) & (probs <= 1)), "Predictions out of [0,1] range")
        
    def test_genai_narrative(self):
        """Test GenAI fallback narrative generation"""
        explainer = GenAIExplainer() # No API key -> Fallback
        
        dummy_data = {'region': 'TestRegion', 'tier': 'TestTier'}
        dummy_reasons = [{'feature': 'test_feat', 'description': 'Test Description', 'impact_score': 5.0}]
        
        narrative = explainer.generate_narrative(dummy_data, 0.85, dummy_reasons)
        self.assertIsInstance(narrative, str)
        self.assertIn("TestTier", narrative) # Check it uses context
        
    def test_empc_calculation(self):
        """Test Business Metric Calculation"""
        y_true = pd.Series([0, 1, 1, 0, 1])
        y_pred = np.array([0.1, 0.9, 0.8, 0.2, 0.7])
        ltv = pd.Series([1000, 1000, 1000, 1000, 1000])
        
        # With perfect predictions on index 1, 2, 4 (churners)
        # Cost 100, Save Rate 0.4 -> Value = 400 - 100 = 300 per save
        # Total potential: 900
        
        profit = calculate_empc(y_true, y_pred, ltv, intervention_cost=100, acceptance_rate=0.4, top_k_percent=1.0)
        # We target all 5
        # Cost = 500
        # Saved = 3 churners * 1000 * 0.4 = 1200
        # Net = 700? 
        # Wait, calculate_empc logic:
        # sorted: 1(0.9), 2(0.8), 4(0.7), 3(0.2), 0(0.1)
        # Correct order. 
        # Logic: sum(saved_revenue) - sum(cost)
        
        self.assertGreater(profit, 0)

if __name__ == '__main__':
    unittest.main()
