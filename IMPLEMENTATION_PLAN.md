# AI Partner Churn Predictor — Implementation Plan (Enhanced "Mind-Blowing" Edition)

> **Goal:** Build an AI system that doesn't just predict *who* will churn, but discovers *why*, prescribes *what to do*, *when* to do it, and **learns from outcomes** to maximize profit.
> 
> **Review Status:** ✅ Approved by Demis Hassabis (DeepMind) + QuantumBlack Senior Partner

---

## 🎯 Strategic Approach: The "6-Criteria" Architecture

We are optimizing specifically for these judging criteria:

| Criterion | Solution | Status |
|-----------|----------|--------|
| 1. **Accurate Early Prediction** | LightGBM + SHAP + Reason Codes | ✅ |
| 2. **Cohort Risk Detection** | Statistical Anomaly Detection + Network Graph | ✅ Enhanced |
| 3. **Intervention Timing** | Uplift Modeling (CausalML T-Learner) | ✅ |
| 4. **Pattern Discovery** | K-Means Clustering + Apriori Association Rules | ✅ Enhanced |
| 5. **Learning from Outcomes** | Feedback Loop Architecture + Model Retraining | ✅ Enhanced |
| 6. **Proactive Recommendations** | ROI-based Prescriptions + "Sleeping Dogs" Filter | ✅ Enhanced |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DATA LAYER                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  Partners + Interventions + Outcomes → Feature Engineering (18 Features)     │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PREDICTION LAYER                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────────┐  │
│  │   LightGBM       │    │   CausalML       │    │   Pattern Discovery  │  │
│  │   (Base Risk)    │    │   (Uplift Score) │    │   (K-Means + Apriori)│  │
│  │                  │    │                  │    │                      │  │
│  │  → P(Churn)      │    │  → TE per Action │    │  → Emergent Clusters │  │
│  │  → SHAP Reasons  │    │  → Persuadables  │    │  → Association Rules │  │
│  └──────────────────┘    └──────────────────┘    └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                         DETECTION LAYER                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────┐    ┌──────────────────────────────────────┐  │
│  │   Cohort Anomaly Engine  │    │   Network Topology Analyzer          │  │
│  │                          │    │                                      │  │
│  │  → Region + Rail Z-Score │    │  → Master Affiliate Graph            │  │
│  │  → Systemic Alerts       │    │  → Subnetwork Health Scores          │  │
│  └──────────────────────────┘    └──────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                       RECOMMENDATION LAYER                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │   Recommendation Engine                                               │  │
│  │                                                                       │  │
│  │   → "Partner X Risk: 85%"                                            │  │
│  │   → "Recommended: Manager Call (ROI: $12k, Success: 65%)"            │  │
│  │   → "Alternative: Email (ROI: $3k, Success: 25%)"                    │  │
│  │   → "⚠️ Sleeping Dog Filter: Do Not Contact Partner Y"               │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
┌─────────────────────────────────────────────────────────────────────────────┐
│                         LEARNING LAYER (NEW)                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────────┐ │
│  │  Predictions DB │ →  │  Outcome Logger │ →  │  Accuracy Monitor       │ │
│  │                 │    │  (T+30 days)    │    │  (Drift Detection)      │ │
│  │  prediction_id  │    │                 │    │                         │ │
│  │  partner_id     │    │  actual_outcome │    │  → Trigger Retraining   │ │
│  │  intervention   │    │  recorded_at    │    │  → Dashboard Metrics    │ │
│  └─────────────────┘    └─────────────────┘    └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                    ↓
                              Dashboard
```

---

## 📊 Key Components

### 1. Data Generation (`data/synthetic_generator.py`)

- **Partners:** 10,000 records, 90 days history
- **Scenarios:** Active, Passive, Involuntary, Network (Contagion)
- **Intervention History:**
  - `intervention_type`: Call, Email, None
  - `outcome`: Retained/Churned
  - `uplift_signal`: Hidden ground truth for validation

### 2. Feature Engineering (18 Features)

*Depth over Breadth to avoid overfitting*

| Category | Key Features |
|----------|--------------|
| **Engagement** | `login_trend_30d` (slope), `days_since_last_interaction` |
| **Performance** | `revenue_velocity` (2nd derivative), `conversion_rate_wow` |
| **Trust** | `payment_delay_flag`, `unresolved_ticket_count` |
| **Network** | `is_master_affiliate`, `subnetwork_avg_health_score`, `subnetwork_recent_churn_count` |
| **Sentiment** | `negative_sentiment_score` |
| **Cohort** | `region`, `payment_rail_type` |
| **Tier Risk** | `tier_proximity_score` (distance to tier cliff) |

### 3. ML Models (`models/`)

#### A. Base Churn Model (LightGBM)

- **Role:** Predict base probability of churn `P(Y=1|X)`
- **Why:** Faster and handles categories better than XGBoost
- **Explainability:** SHAP feature importance → **Reason Codes**

**Reason Code Mapping (NEW):**
```python
REASON_CODES = {
    'login_trend_30d < -0.5': 'DECLINING_ENGAGEMENT',
    'payment_delay_flag == 1': 'PAYMENT_FRICTION',
    'tier_proximity_score < 0.05': 'TIER_CLIFF_ANXIETY',
    'subnetwork_recent_churn_count > 2': 'NETWORK_CONTAGION',
    'negative_sentiment_score > 0.7': 'TRUST_EROSION'
}
```

#### B. Uplift Model (CausalML T-Learner)

- **Role:** Estimate Treatment Effect (TE)
- **Logic:** `TE = E[Y|X, T=1] - E[Y|X, T=0]`
- **Output:**
  - "Uplift from Call: +25% retention prob"
  - "Uplift from Email: +5% retention prob"
- **"Sleeping Dogs" Filter (NEW):** Partners where `Uplift Score < 0` are tagged "Do Not Disturb"

### 4. Pattern Discovery Engine (NEW)

**Purpose:** Automatically discover churn patterns the model finds, not pre-defined rules.

#### A. Behavioral Clustering

```python
# Cluster high-risk partners (>70% churn prob) using K-Means
from sklearn.cluster import KMeans

def discover_churn_clusters(df_high_risk, n_clusters=5):
    """
    Unsupervised clustering of churners to discover emergent patterns.
    Returns cluster centroids with human-readable descriptions.
    """
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df_high_risk['cluster'] = kmeans.fit_predict(df_high_risk[FEATURE_COLS])
    
    # Analyze centroids to generate insights
    for i, centroid in enumerate(kmeans.cluster_centers_):
        insight = generate_cluster_insight(centroid, FEATURE_COLS)
        # e.g., "CLUSTER 2: High tenure + Tier Cliff + Low Support → 'Betrayal' pattern"
```

#### B. Association Rule Mining

```python
# Discover co-occurring signals using Apriori
from mlxtend.frequent_patterns import apriori, association_rules

def discover_churn_rules(df_churned):
    """
    Find frequently co-occurring signals among churned partners.
    Example output: {Payment Delay + Silence > 14d} → Churn (Confidence: 85%)
    """
    # Binarize features
    df_binary = binarize_features(df_churned)
    
    # Run Apriori
    frequent_itemsets = apriori(df_binary, min_support=0.1, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric='confidence', min_threshold=0.7)
    
    return rules.sort_values('lift', ascending=False)
```

**Dashboard Output:**
> 🔍 **New Pattern Discovered:** Partners with `unresolved_ticket_count > 3` AND `days_since_last_interaction > 14` have **4.2x higher churn rate** (Confidence: 87%).

### 5. Cohort Anomaly Detection Engine (NEW)

**Purpose:** Detect systemic issues affecting partner groups.

```python
def detect_cohort_anomalies(df, group_cols=['region', 'payment_rail_type']):
    """
    Aggregate churn signals by cohort and flag systemic issues.
    Alert if >3 partners in cohort exceed 2σ on churn_probability.
    """
    cohort_stats = df.groupby(group_cols).agg({
        'churn_probability': ['mean', 'std', 'count'],
        'partner_id': 'count'
    })
    
    # Calculate baseline from global population
    global_mean = df['churn_probability'].mean()
    global_std = df['churn_probability'].std()
    
    # Flag anomalous cohorts
    anomalies = cohort_stats[
        (cohort_stats['churn_probability']['mean'] > global_mean + 2 * global_std) &
        (cohort_stats['partner_id']['count'] >= 3)
    ]
    
    return generate_systemic_alerts(anomalies)
```

**Dashboard Output:**
> ⚠️ **Systemic Alert:** 12 partners in `Brazil` with `P2P` payment rail showing correlated churn signals. Investigate payment infrastructure issue.

### 6. Network Topology Analyzer (NEW)

**Purpose:** Detect contagion risk in Master Affiliate networks.

```python
def analyze_network_topology(df_partners, df_affiliations):
    """
    Model Master → Sub-Affiliate relationships as directed graph.
    Calculate subnetwork health scores and contagion risk.
    """
    import networkx as nx
    
    G = nx.DiGraph()
    
    # Add edges: Master → Sub
    for _, row in df_affiliations.iterrows():
        G.add_edge(row['master_id'], row['sub_id'])
    
    # Calculate centrality (influence)
    centrality = nx.degree_centrality(G)
    
    # For each Master, calculate subnetwork health
    for master_id in df_partners[df_partners['is_master_affiliate'] == 1]['partner_id']:
        subs = list(G.successors(master_id))
        sub_churn_probs = df_partners[df_partners['partner_id'].isin(subs)]['churn_probability']
        
        subnetwork_health = 100 - (sub_churn_probs.mean() * 100)  # 0-100 score
        df_partners.loc[df_partners['partner_id'] == master_id, 'subnetwork_health_score'] = subnetwork_health
    
    return df_partners, G
```

### 7. Learning Loop Architecture (NEW)

**Purpose:** System improves predictions based on actual outcomes.

#### A. Database Schema

```sql
-- Predictions Table (Supabase)
CREATE TABLE predictions (
    prediction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    partner_id VARCHAR(50) NOT NULL,
    churn_probability FLOAT NOT NULL,
    top_churn_factors JSONB,  -- SHAP-derived reasons
    recommended_intervention VARCHAR(50),
    uplift_score FLOAT,
    predicted_at TIMESTAMP DEFAULT NOW(),
    
    -- Outcome fields (populated later)
    actual_intervention VARCHAR(50),
    actual_outcome VARCHAR(20),  -- 'RETAINED', 'CHURNED', 'PENDING'
    outcome_recorded_at TIMESTAMP,
    
    -- Metadata
    model_version VARCHAR(20)
);

-- Aggregated Metrics View
CREATE VIEW model_performance AS
SELECT 
    DATE_TRUNC('week', predicted_at) AS week,
    model_version,
    COUNT(*) AS total_predictions,
    AVG(CASE WHEN actual_outcome = 'CHURNED' AND churn_probability > 0.5 THEN 1 
             WHEN actual_outcome = 'RETAINED' AND churn_probability <= 0.5 THEN 1 
             ELSE 0 END) AS accuracy,
    AVG(CASE WHEN recommended_intervention = actual_intervention 
             AND actual_outcome = 'RETAINED' THEN 1 ELSE 0 END) AS intervention_success_rate
FROM predictions
WHERE actual_outcome IS NOT NULL
GROUP BY 1, 2;
```

#### B. Feedback Loop Pipeline

```yaml
# Learning Loop Workflow
1. Prediction Service:
   - Scores partner → logs to `predictions` table
   - Includes `prediction_id`, `churn_probability`, `recommended_intervention`

2. Outcome Logger (Daily Scheduler):
   - For predictions at T+30 days: check partner status
   - Update `actual_outcome` (RETAINED/CHURNED)
   - Update `actual_intervention` (from CRM/intervention logs)

3. Accuracy Monitor (Weekly):
   - Query `model_performance` view
   - If accuracy drift > 5% from baseline: trigger alert
   - Log to dashboard metrics

4. Retraining Pipeline (Monthly or on drift):
   - Pull new training data with outcomes
   - Retrain LightGBM + CausalML models
   - Version new model, deploy to production
```

### 8. Dashboard (`dashboard/app.py`)

**Page 1: Risk Overview**
- Top at-risk partners with Reason Codes
- Cohort Alerts ("Systemic Issue Predicted")
- Network Contagion Risk visualization

**Page 2: Uplift & Intervention View (The "Money Shot")**
- "Partner X Risk: 85%"
- "Recommended: **Manager Call** (ROI: $12k, Success: 65%)"
- "Alternative: Email (ROI: $3k, Success: 25%)"
- "⚠️ Sleeping Dog: Do Not Contact Partner Y"

**Page 3: Pattern Discovery**
- Discovered clusters with descriptions
- Association rules with confidence scores
- "NEW: Trust Erosion pattern detected in Cluster 3"

**Page 4: Learning Tracker (NEW)**
- "Model Accuracy: Last 30 Days — 82%"
- "Intervention Success Rate: Calls — 65%, Emails — 22%"
- "Model Version: v2.1 (retrained 2026-02-01)"
- Accuracy trend charts

---

## 📅 5-Day Implementation Timeline (Updated)

| Day | Focus | Output |
|-----|-------|--------|
| **Day 1** | **Data + Core Features** | Synthetic data with intervention outcomes, 18 features, `predictions` DB schema |
| **Day 2** | **Base Model + SHAP** | LightGBM operational, Reason Code mapping, SHAP visualizations |
| **Day 3** | **CausalML Uplift + Pattern Discovery** | T-Learner implementation, "Sleeping Dogs" filter, K-Means clustering, Apriori rules |
| **Day 4** | **Dashboard + Detection Engines** | Cohort Anomaly Alerts, Network Topology view, Learning Tracker, Recommendation UI |
| **Day 5** | **Polish & Story** | Demo the *discovery* of "Trust Erosion" pattern (not pre-defined), narrative refinement |

---

## ✅ Success Criteria aligned with "Mind-Blowing" Goals

| Criterion | Implementation | Metric |
|-----------|----------------|--------|
| 1. **Accurate Early Prediction** | LightGBM + SHAP + Reason Codes | >80% precision, human-readable explanations |
| 2. **Cohort Risk Detection** | Cohort Anomaly Engine | Dashboard shows regional/payment rail alerts |
| 3. **Intervention Timing** | Uplift Model + Sleeping Dogs filter | "Persuadables" identified, "Do Not Disturb" protected |
| 4. **Pattern Discovery** | K-Means + Apriori | System *discovers* Trust Erosion pattern autonomously |
| 5. **Learning from Outcomes** | Feedback Loop + Retraining | Dashboard shows accuracy trends, proves improvement |
| 6. **Proactive Recommendations** | ROI-based engine | "Call vs Email" with success probability and ROI |

---

## 🔑 Key Differentiators (vs. "Competent Data Science")

1. **Emergent Pattern Discovery:** The AI discovers behavioral clusters and association rules, not pre-baked domain knowledge.

2. **Causal Reasoning:** Uplift modeling distinguishes "Persuadables" from "Lost Causes" and "Sleeping Dogs."

3. **Systemic Risk Detection:** Cohort-level anomaly detection catches infrastructure issues before they cascade.

4. **Closed Learning Loop:** Every prediction is tracked, outcomes are logged, and the model improves over time.

5. **Network Topology Awareness:** Master Affiliate graph analysis detects contagion risk in hierarchical partner structures.

---

**Team Alignment:** This plan trades "complex deep learning" for "advanced business intelligence + causal reasoning." This directly targets the Innovation judging criteria while remaining implementable in 5 days.
