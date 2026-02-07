import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
import pickle
import os
import numpy as np

# ensure directory exists
os.makedirs('models', exist_ok=True)

# Load data
print("Loading data...")
try:
    df = pd.read_csv('dataset/partners.csv')
    if os.path.exists('data/partners_engineered.csv'):
        print("Found engineered features, loading partners_engineered.csv...")
        df = pd.read_csv('data/partners_engineered.csv')
except FileNotFoundError:
    print("Error: Data file not found in data/ directory.")
    exit(1)

print(f"Data shape: {df.shape}")

# Features (18 core features from Day 1)
feature_cols = [
    'login_count_30d', 'login_trend_30d', 'days_since_last_interaction',
    'revenue_velocity', 'conversion_rate_wow', 'commission_trend_90d',
    'payment_delay_flag', 'unresolved_ticket_count', 'negative_sentiment_score',
    'subnetwork_avg_health_score', 'subnetwork_recent_churn_count',
    'tier_proximity_score', 'tenure_months', 'avg_commission_3m'
]

# Select features and target
X = df[feature_cols].copy()
X.fillna(0, inplace=True)
y = df['churn_label']

# Split
print("Splitting data...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# Train
print("Training HistGradientBoostingClassifier (LightGBM-alternative)...")
model = HistGradientBoostingClassifier(
    learning_rate=0.05,
    max_iter=100,
    max_leaf_nodes=31,
    early_stopping=True,
    validation_fraction=0.1,
    n_iter_no_change=10,
    random_state=42,
    verbose=0
)

model.fit(X_train, y_train)

# Evaluation
train_auc = roc_auc_score(y_train, model.predict_proba(X_train)[:, 1])
test_auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])

print(f"Training AUC: {train_auc:.4f}")
print(f"Test AUC:     {test_auc:.4f}")

# Save
print("Saving model artifacts...")
with open('models/lgb_churn_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✅ Model training complete.")
