import numpy as np
import pandas as pd
import pickle
from sklearn.metrics import roc_auc_score, precision_recall_curve

def calculate_empc(y_true, y_pred_proba, ltv, intervention_cost=100, acceptance_rate=0.3, top_k_percent=0.2):
    """
    Calculate Expected Maximum Profit from Churn (EMPC) with Capacity Constraint.
    
    We simulate a realistic scenario where we can only intervene on top K% of partners.
    """
    save_probability = 0.4 
    
    # Indices sorted by model score (descending)
    sorted_indices = np.argsort(y_pred_proba)[::-1]
    
    # Select Top K% indices
    n_partners = len(y_true)
    cutoff = int(n_partners * top_k_percent)
    target_indices = sorted_indices[:cutoff]
    
    invested_budget = 0
    saved_revenue = 0
    
    for i in target_indices:
        is_churn = y_true.iloc[i]
        partner_ltv = ltv.iloc[i]
        
        # We intervene on these selected partners
        invested_budget += intervention_cost
        
        if is_churn:
            # If they were going to churn, we save them with prob 'save_probability'
            saved_revenue += (partner_ltv * save_probability)
                
    net_profit = saved_revenue - invested_budget
    return net_profit

def evaluate_business_impact():
    print("Loading data and model...")
    df = pd.read_csv('dataset/partners.csv')
    
    with open('models/lgb_churn_model.pkl', 'rb') as f:
        model = pickle.load(f)
        
    feature_cols = [
        'login_count_30d', 'login_trend_30d', 'days_since_last_interaction',
        'revenue_velocity', 'conversion_rate_wow', 'commission_trend_90d',
        'payment_delay_flag', 'unresolved_ticket_count', 'negative_sentiment_score',
        'subnetwork_avg_health_score', 'subnetwork_recent_churn_count',
        'tier_proximity_score', 'tenure_months', 'avg_commission_3m'
    ]
    
    X = df[feature_cols].copy().fillna(0)
    y_true = df['churn_label']
    y_pred_proba = model.predict_proba(X)[:, 1]
    
    # LTV Proxy: avg_commission_3m * 12 (1 year LTV)
    ltv = df['avg_commission_3m'] * 12
    
    print("Calculating Business Impact (EMPC) @ 20% Capacity...")
    
    # 1. Random Policy (Baseline)
    # Random scores result in random ordering
    rng = np.random.default_rng(42)
    random_scores = rng.random(len(y_true))
    baseline_profit = calculate_empc(y_true, random_scores, ltv, top_k_percent=0.2)
    
    # 2. Model Policy
    model_profit = calculate_empc(y_true, y_pred_proba, ltv, top_k_percent=0.2)
    
    print(f"Baseline Profit (Random 20%): ${baseline_profit:,.2f}")
    print(f"Model Profit (AI Top 20%):    ${model_profit:,.2f}")
    
    if baseline_profit > 0:
        improvement = model_profit / baseline_profit
        print(f"📈 Improvement: {improvement:.2f}x")
    else:
        print(f"📈 Improvement: Infinite (Baseline Loss)")

if __name__ == "__main__":
    evaluate_business_impact()
