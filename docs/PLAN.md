# Day 1 Execution Plan: Data + Core Features

> **Goal:** Build database foundation, synthetic data generator, and 18-feature engineering pipeline  
> **Timeline:** Day 1 of 5  
> **Agents:** database-architect, backend-specialist, test-engineer

---

## 📋 Overview

Day 1 establishes the data foundation for the AI Partner Churn Predictor. We will:
1. Create PostgreSQL schema (local Docker setup)
2. Build synthetic data generator with realistic distributions
3. Implement 18-feature engineering pipeline
4. Create golden demo records for reliable scenarios

---

## 🎯 Deliverables

| Component | Output | Verification |
|-----------|--------|--------------|
| 1. Database Schema | `schema/predictions.sql` | psql connection test |
| 2. Synthetic Generator | `data/synthetic_generator.py` | Generate 10,000 records |
| 3. Feature Engineering | `data/feature_engineering.py` | Validate 18 features |
| 4. Golden Records | `data/golden_demo_records.py` | Hardcoded scenarios |
| 5. Docker Setup | `docker-compose.yml` | `docker-compose up` |

---

## 📊 Component Breakdown

### 1. Database Schema Setup

**Agent:** `database-architect`

**Files to Create:**
- `schema/predictions.sql` — Predictions table for learning loop
- `schema/partners.sql` — Core partner data
- `schema/interventions.sql` — Historical intervention outcomes
- `docker-compose.yml` — Local PostgreSQL container

**Schema Requirements:**

```sql
-- partners table (10,000 synthetic records)
CREATE TABLE partners (
    partner_id VARCHAR(50) PRIMARY KEY,
    region VARCHAR(50),
    payment_rail_type VARCHAR(50),
    is_master_affiliate BOOLEAN,
    tier VARCHAR(20),
    tenure_months INTEGER,
    avg_commission_3m DECIMAL(10,2),
    
    -- Engagement metrics (last 30 days)
    login_count_30d INTEGER,
    login_trend_30d DECIMAL(5,2),  -- slope
    days_since_last_interaction INTEGER,
    
    -- Performance metrics
    revenue_velocity DECIMAL(10,2),  -- 2nd derivative
    conversion_rate_wow DECIMAL(5,4),  -- WoW change
    
    -- Trust/Friction
    payment_delay_flag BOOLEAN,
    unresolved_ticket_count INTEGER,
    negative_sentiment_score DECIMAL(3,2),
    
    -- Network (for Master Affiliates)
    subnetwork_avg_health_score DECIMAL(5,2),
    subnetwork_recent_churn_count INTEGER,
    
    -- Tier Risk
    tier_proximity_score DECIMAL(5,4),  -- 0-1, distance to tier cliff
    
    -- Ground truth
    churn_label BOOLEAN,  -- Actual outcome for training
    churn_scenario VARCHAR(50),  -- Active/Passive/Involuntary/Contagion
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- interventions table (historical outcomes)
CREATE TABLE interventions (
    intervention_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    partner_id VARCHAR(50) REFERENCES partners(partner_id),
    intervention_type VARCHAR(50),  -- Call, Email, None
    outcome VARCHAR(20),  -- Retained, Churned
    uplift_signal DECIMAL(5,3),  -- Hidden ground truth (-1 to 1)
    intervention_date TIMESTAMP,
    outcome_recorded_at TIMESTAMP
);

-- predictions table (learning loop)
CREATE TABLE predictions (
    prediction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    partner_id VARCHAR(50) REFERENCES partners(partner_id),
    churn_probability DECIMAL(5,4),
    top_churn_factors JSONB,
    recommended_intervention VARCHAR(50),
    uplift_score DECIMAL(5,3),
    predicted_at TIMESTAMP DEFAULT NOW(),
    
    -- Outcome fields (populated T+30)
    actual_intervention VARCHAR(50),
    actual_outcome VARCHAR(20),
    outcome_recorded_at TIMESTAMP,
    
    model_version VARCHAR(20)
);

-- Indexes for performance
CREATE INDEX idx_partners_churn ON partners(churn_label);
CREATE INDEX idx_partners_region ON partners(region);
CREATE INDEX idx_predictions_partner ON predictions(partner_id);

-- network_relationships table (for graph analysis)
CREATE TABLE network_relationships (
    relationship_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    master_affiliate_id VARCHAR(50) REFERENCES partners(partner_id),
    sub_affiliate_id VARCHAR(50) REFERENCES partners(partner_id),
    recruited_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    
    CONSTRAINT fk_master FOREIGN KEY (master_affiliate_id) 
        REFERENCES partners(partner_id),
    CONSTRAINT fk_sub FOREIGN KEY (sub_affiliate_id) 
        REFERENCES partners(partner_id)
);

CREATE INDEX idx_network_master ON network_relationships(master_affiliate_id);
CREATE INDEX idx_network_sub ON network_relationships(sub_affiliate_id);
```

**Verification:**
```bash
docker-compose up -d
psql -h localhost -U admin -d deriv_churn -c "\dt"
# Should show: partners, interventions, predictions
```

---

### 2. Synthetic Data Generator

**Agent:** `backend-specialist`

**File:** `data/synthetic_generator.py`

**Requirements:**

1. **Pareto Distribution for Financial Metrics** (NOT Gaussian)
   - Partners follow 80/20 rule (few whales, many minnows)
   - Use: `np.random.pareto(alpha=1.16)` for revenue/commissions

2. **10,000 Partners with Realistic Distributions**
   ```python
   REGIONS = ['Brazil', 'EU', 'UK', 'Nigeria', 'SE_Asia', 'APAC']
   PAYMENT_RAILS = ['P2P', 'Crypto', 'Bank', 'Agent']
   TIERS = ['Bronze', 'Silver', 'Gold', 'Platinum']
   SCENARIOS = ['Active', 'Passive', 'Involuntary', 'Contagion']
   ```

3. **Feature Correlations**
   - `tier_proximity_score < 0.05` → higher churn
   - `payment_delay_flag == 1` AND `days_since_last_interaction > 14` → "Trust Erosion"
   - `is_master_affiliate == 1` AND `subnetwork_recent_churn_count > 2` → "Contagion"

4. **Balanced Churn Labels**
   - Use ADASYN/SMOTE logic to ensure ~20% churn rate
   - But respect natural class imbalance (don't force 50/50)

**Pseudocode:**
```python
def generate_partners(n=10000):
    partners = []
    
    for i in range(n):
        # Base attributes
        partner = {
            'partner_id': f'P{10000+i}',
            'region': random.choice(REGIONS),
            'payment_rail_type': random.choice(PAYMENT_RAILS),
            'is_master_affiliate': random.random() < 0.05,  # 5% are Masters
            'tier': weighted_choice(TIERS),
            'tenure_months': int(np.random.exponential(scale=12)),
            
            # Financial (Pareto distributed)
            'avg_commission_3m': pareto_sample(alpha=1.16, scale=1000, max=50000),
            
            # Engagement (raw counts)
            'login_count_30d': max(0, int(np.random.normal(15, 8))),
            'days_since_last_interaction': max(0, int(np.random.exponential(5))),
            
            # ... other raw features
        }
        
        # Derive churn label based on feature logic
        churn_score = calculate_churn_score(partner)
        partner['churn_label'] = churn_score > 0.65  # threshold
        
        # Pre-compute velocity features (see section below)
        velocity_features = generate_velocity_features(partner, partner['churn_label'])
        partner.update(velocity_features)
        
        # Assign scenario based on feature patterns (see section below)
        partner['churn_scenario'] = assign_churn_scenario(partner)
        
        partners.append(partner)
    
    return pd.DataFrame(partners)
```

#### 2.4 Velocity Feature Pre-Computation (EFFICIENCY)

**Design Decision:** Pre-compute slopes/velocities instead of generating full time-series.

**Why:**
- Generating 30 days × 10,000 partners = 300,000 time-series data points adds 2+ hours
- LightGBM only uses the final slope value, not the raw time-series
- Hackathon timeline prioritizes working model over data generation realism

**Implementation:**

```python
def generate_velocity_features(partner, churn_label):
    """
    Pre-compute slope/velocity features with realistic distributions.
    Churners show declining trends, healthy partners show stable/growth.
    
    Args:
        partner: Partner dict with base features
        churn_label: Whether this partner will churn
        
    Returns:
        dict with velocity features
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
        'login_trend_30d': round(login_trend, 3),
        'revenue_velocity': round(revenue_velocity, 2),
        'commission_trend_90d': round(commission_trend_90d, 3),
        'conversion_rate_wow': round(conversion_rate_wow, 4)
    }
```

**Alternative (if time permits):** Generate full time-series and compute slopes:
```python
# Only if Day 1 finishes early and you want more realism
login_history = generate_time_series(mean=15, trend=-0.15, days=30)
login_trend_30d = linregress(range(30), login_history).slope
```

#### 2.5 Churn Scenario Assignment (CRITICAL for Pattern Discovery)

**Purpose:** Assign ground truth scenarios based on feature patterns for validation.

**Why This Matters:**
- Day 3 Pattern Discovery uses K-Means to *discover* behavioral clusters
- This function creates ground truth labels to validate: "Did the model discover Trust Erosion?"
- Without this, you can't prove the clustering found meaningful patterns

**Implementation:**

```python
def assign_churn_scenario(partner):
    """
    Assign churn scenario based on feature patterns.
    These become ground truth labels for Pattern Discovery validation.
    
    Scenarios:
    - Trust_Erosion: Payment issues + silence
    - Network_Contagion: Master with failing subnetwork
    - Tier_Cliff_Anxiety: Close to tier demotion
    - Active_Churn: Competitor signals (negative sentiment)
    - Passive_Disengagement: Declining engagement without clear cause
    - Healthy: Not churning
    
    Returns:
        str: Scenario name
    """
    if not partner['churn_label']:
        return 'Healthy'
    
    # Trust Erosion: payment issues + silence (highest priority)
    if (partner.get('payment_delay_flag', False) and 
        partner.get('days_since_last_interaction', 0) > 14):
        return 'Trust_Erosion'
    
    # Network Contagion: master affiliate with failing network
    if (partner.get('is_master_affiliate', False) and 
        partner.get('subnetwork_recent_churn_count', 0) > 2):
        return 'Network_Contagion'
    
    # Tier Cliff: close to demotion threshold
    if partner.get('tier_proximity_score', 1.0) < 0.05:
        return 'Tier_Cliff_Anxiety'
    
    # Active Churn: high negative sentiment (competitor interest)
    if partner.get('negative_sentiment_score', 0) > 0.7:
        return 'Active_Churn'
    
    # Default: Passive disengagement
    return 'Passive_Disengagement'
```

**Validation:**

```python
def test_scenario_distribution():
    """Verify scenario labels are realistic"""
    df = pd.read_csv('data/partners.csv')
    
    scenario_counts = df['churn_scenario'].value_counts()
    
    # Most partners should be healthy
    assert scenario_counts['Healthy'] > len(df) * 0.75
    
    # Churn scenarios should all be represented
    churn_scenarios = ['Trust_Erosion', 'Network_Contagion', 
                       'Tier_Cliff_Anxiety', 'Active_Churn', 
                       'Passive_Disengagement']
    
    for scenario in churn_scenarios:
        assert scenario in scenario_counts.index, f"Missing {scenario}"
    
    print("✅ Churn scenarios validated")
```

**Integration with Pattern Discovery (Day 3):**

```python
# Day 3: Compare discovered clusters to ground truth scenarios
clusters = KMeans(n_clusters=5).fit(partner_features)

for i in range(5):
    cluster_partners = df[clusters.labels_ == i]
    dominant_scenario = cluster_partners['churn_scenario'].mode()[0]
    overlap = (cluster_partners['churn_scenario'] == dominant_scenario).mean()
    
    if overlap > 0.70:
        print(f"🔍 Cluster {i} discovered '{dominant_scenario}' pattern (overlap: {overlap:.0%})")
```

**Verification:**
```bash
python data/synthetic_generator.py
# Output: data/partners.csv (10,000 rows)
# Check: mean(avg_commission_3m) follows Pareto (few large, many small)
# Check: churn_label distribution ~15-25%
```

#### 2.5 Intervention Outcome Generation (CRITICAL for CausalML)

**Purpose:** Generate realistic uplift signals for CausalML T-Learner training on Day 3.

**Ground Truth Causal Model:**

```python
def generate_intervention_outcome(partner, intervention_type, random_seed=None):
    """
    Ground truth uplift model (hidden from ML training).
    Models how different interventions work for different partner types.
    
    Returns:
        dict with 'outcome', 'uplift_signal', 'final_churn_prob'
    """
    if random_seed:
        np.random.seed(random_seed)
    
    # Calculate base churn probability (no intervention)
    base_churn_prob = calculate_base_churn_probability(partner)
    
    # Treatment effects vary by partner characteristics
    if intervention_type == "call":
        # Calls work better for:
        # - High LTV partners (relationship value justifies effort)
        # - Trust issues (human touch rebuilds confidence)
        # - Master Affiliates (strategic importance)
        if partner['avg_commission_3m'] > 10000:
            treatment_effect = -0.30  # Strong retention effect
        elif partner['payment_delay_flag']:
            treatment_effect = -0.25  # Rebuilds trust
        elif partner['is_master_affiliate']:
            treatment_effect = -0.28  # VIP treatment
        else:
            treatment_effect = -0.10  # Modest effect
            
    elif intervention_type == "email":
        # Emails work better for:
        # - Medium engagement partners (still checking inbox)
        # - Technical issues (can send documentation)
        # - Tier proximity (can explain grace period)
        if -0.5 < partner['login_trend_30d'] < 0:
            treatment_effect = -0.15  # Catches mild disengagement
        elif partner['unresolved_ticket_count'] > 0:
            treatment_effect = -0.12  # Can address specific issues
        elif partner['tier_proximity_score'] < 0.1:
            treatment_effect = -0.18  # Tier anxiety response
        else:
            treatment_effect = -0.05  # Weak signal
            
    else:  # No intervention
        treatment_effect = 0
    
    # Add realistic noise (interventions aren't deterministic)
    treatment_effect += np.random.normal(0, 0.08)
    
    # Clip treatment effect to realistic bounds
    treatment_effect = np.clip(treatment_effect, -0.5, 0.2)
    
    # Final churn probability after intervention
    final_churn_prob = np.clip(base_churn_prob + treatment_effect, 0, 1)
    
    # Simulate outcome (stochastic)
    did_churn = np.random.binomial(1, final_churn_prob)
    
    return {
        'outcome': 'Churned' if did_churn else 'Retained',
        'uplift_signal': treatment_effect,  # Hidden ground truth
        'final_churn_prob': final_churn_prob
    }


def generate_historical_interventions(partners_df, interventions_per_partner=2):
    """
    Generate 1-3 historical interventions per partner.
    Mix of calls, emails, and no-intervention controls.
    
    Args:
        partners_df: DataFrame of partners
        interventions_per_partner: Average number of interventions
        
    Returns:
        DataFrame with columns: partner_id, intervention_type, outcome, uplift_signal
    """
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
                partner, intervention_type
            )
            
            # Random past date (30-90 days ago)
            intervention_date = datetime.now() - timedelta(
                days=np.random.randint(30, 91)
            )
            
            interventions.append({
                'partner_id': partner['partner_id'],
                'intervention_type': intervention_type,
                'outcome': outcome_data['outcome'],
                'uplift_signal': outcome_data['uplift_signal'],
                'intervention_date': intervention_date,
                'outcome_recorded_at': intervention_date + timedelta(days=30)
            })
    
    return pd.DataFrame(interventions)
```

**Why This is Critical:**

1. **CausalML T-Learner requires** historical `(X, T, Y)` data:
   - `X` = partner features
   - `T` = intervention type
   - `Y` = outcome (Retained/Churned)

2. **Without realistic uplift signals**, the T-Learner learns noise instead of heterogeneous treatment effects

3. **This enables "Persuadables" detection** (partners who respond to intervention)

**Validation Test:**

```python
def test_uplift_signals():
    """Verify uplift signals have realistic heterogeneity"""
    df_interventions = pd.read_csv('data/interventions.csv')
    
    # Check treatment effect distribution
    assert -0.5 <= df_interventions['uplift_signal'].min() <= 0.0
    assert 0.0 <= df_interventions['uplift_signal'].max() <= 0.2
    
    # Verify heterogeneity: calls should have stronger effects than emails
    call_effects = df_interventions[
        df_interventions['intervention_type'] == 'call'
    ]['uplift_signal']
    
    email_effects = df_interventions[
        df_interventions['intervention_type'] == 'email'
    ]['uplift_signal']
    
    # Calls should be more negative (stronger retention effect)
    assert call_effects.mean() < email_effects.mean()
    
    print("✅ Uplift signals validated")


def test_intervention_distribution():
    """Verify realistic intervention mix"""
    df = pd.read_csv('data/interventions.csv')
    
    # Email should be most common (cheapest)
    intervention_counts = df['intervention_type'].value_counts(normalize=True)
    
    assert intervention_counts['email'] > intervention_counts['call']
    assert intervention_counts['none'] > intervention_counts['call']
    
    print("✅ Intervention distribution realistic")
```

#### 2.6 Network Relationships Generation (CRITICAL for Graph Analysis)

**Purpose:** Create Master → Sub-Affiliate relationships for network features and contagion detection.

**Network Generation Logic:**

```python
def generate_network_relationships(partners_df):
    """
    Create master -> sub-affiliate relationships.
    Each master has 10-50 unique sub-affiliates (tree structure).
    
    Args:
        partners_df: DataFrame with all partners
        
    Returns:
        DataFrame with columns: master_affiliate_id, sub_affiliate_id, recruited_at
    """
    masters = partners_df[partners_df['is_master_affiliate'] == True].copy()
    non_masters = partners_df[partners_df['is_master_affiliate'] == False].copy()
    
    relationships = []
    available_subs = non_masters.copy()  # Track unassigned sub-affiliates
    
    for _, master in masters.iterrows():
        # Each master gets 10-50 subs (or remaining if fewer)
        n_subs = min(np.random.randint(10, 51), len(available_subs))
        
        if n_subs == 0:
            # No more subs available
            continue
        
        # Assign UNIQUE subs to this master (tree, not graph)
        assigned_subs = available_subs.sample(n=n_subs)
        
        for _, sub in assigned_subs.iterrows():
            # Random recruitment date (30-365 days ago)
            recruited_date = datetime.now() - timedelta(
                days=np.random.randint(30, 366)
            )
            
            relationships.append({
                'master_affiliate_id': master['partner_id'],
                'sub_affiliate_id': sub['partner_id'],
                'recruited_at': recruited_date,
                'is_active': True
            })
        
        # Remove assigned subs from pool (enforce uniqueness)
        available_subs = available_subs.drop(assigned_subs.index)
    
    return pd.DataFrame(relationships)
```

**Why This is Critical:**

1. **Network Features Depend on This:**
   - `subnetwork_avg_health_score` = mean churn prob of sub-affiliates
   - `subnetwork_recent_churn_count` = count of churned subs in last 30 days

2. **Network Topology Analyzer (Day 4) Requires Edges:**
   - Graph construction: `G.add_edge(master_id, sub_id)`
   - Centrality calculations: `nx.degree_centrality(G)`
   - Contagion detection: traverse graph from churning nodes

3. **Pattern Discovery - "Contagion" Scenario:**
   - Golden record P00003 needs 4+ churning sub-affiliates
   - This is impossible to verify without relationship table

**Integration with Feature Engineering:**

```python
def calculate_network_features(partner, network_df, partners_df):
    """
    Calculate network-based features for a partner.
    Only applicable if partner is a Master Affiliate.
    """
    if not partner['is_master_affiliate']:
        return {
            'subnetwork_avg_health_score': None,
            'subnetwork_recent_churn_count': None
        }
    
    # Get sub-affiliates for this master
    subs = network_df[
        network_df['master_affiliate_id'] == partner['partner_id']
    ]['sub_affiliate_id'].tolist()
    
    if len(subs) == 0:
        return {
            'subnetwork_avg_health_score': 100.0,  # No subs = perfect health
            'subnetwork_recent_churn_count': 0
        }
    
    # Get churned subs in last 30 days
    recent_churns = partners_df[
        (partners_df['partner_id'].isin(subs)) &
        (partners_df['churn_label'] == True) &
        (partners_df['created_at'] > datetime.now() - timedelta(days=30))
    ]
    
    # Calculate average health (0-100 scale)
    sub_churn_probs = partners_df[
        partners_df['partner_id'].isin(subs)
    ]['churn_label'].mean()  # proportion of churned subs
    
    avg_health = (1 - sub_churn_probs) * 100
    
    return {
        'subnetwork_avg_health_score': round(avg_health, 2),
        'subnetwork_recent_churn_count': len(recent_churns)
    }
```

**Validation Tests:**

```python
def test_network_relationships():
    """Verify network structure is valid"""
    df_network = pd.read_csv('data/network_relationships.csv')
    df_partners = pd.read_csv('data/partners.csv')
    
    masters = df_partners[df_partners['is_master_affiliate'] == True]
    
    # Each master should have 10-50 subs
    for _, master in masters.iterrows():
        subs = df_network[
            df_network['master_affiliate_id'] == master['partner_id']
        ]
        assert 0 <= len(subs) <= 50, f"Master {master['partner_id']} has {len(subs)} subs"
    
    # No duplicate sub-affiliates (tree structure)
    sub_counts = df_network['sub_affiliate_id'].value_counts()
    assert sub_counts.max() == 1, "Sub-affiliates should have only ONE parent"
    
    print("✅ Network relationships validated")


def test_network_features():
    """Verify network features calculated correctly"""
    df_partners = pd.read_csv('data/partners_engineered.csv')
    
    # Only masters should have network features
    masters = df_partners[df_partners['is_master_affiliate'] == True]
    non_masters = df_partners[df_partners['is_master_affiliate'] == False]
    
    assert masters['subnetwork_avg_health_score'].notna().all()
    assert non_masters['subnetwork_avg_health_score'].isna().all()
    
    print("✅ Network features validated")
```

---

### 3. Feature Engineering Pipeline

**Agent:** `backend-specialist`

**File:** `data/feature_engineering.py`

**Requirements:**

**Complete 18-Feature List:**

```python
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
    'subnetwork_avg_health_score',       # Mean health of sub-affiliates (0-100)
    'subnetwork_recent_churn_count',     # Churned subs in last 30 days
    
    # Tier Risk (2 features)
    'tier_proximity_score',         # 0-1, distance to tier demotion threshold
    'tenure_months',                # Months since partnership started
    
    # Financial (2 features)
    'avg_commission_3m',            # Average commission last 3 months
    'commission_volatility',        # Standard deviation of monthly commissions
]
# Total: 18 features
```

**Feature Calculation Details:**

| Feature | Type | Calculation | Example Value |
|---------|------|-------------|---------------|
| `login_trend_30d` | Velocity | `linregress(days, login_counts).slope` | `-0.5` (declining) |
| `revenue_velocity` | Acceleration | `2nd_derivative(commissions)` | `-50` (decelerating) |
| `tier_proximity_score` | Risk | `(current - threshold) / threshold` | `0.02` (2% above cliff) |
| `subnetwork_avg_health_score` | Network | `mean(100 - sub_churn_prob * 100)` | `72.0` (72% healthy) |
| `dashboard_usage_score` | Composite | `normalize(clicks * 0.4 + time * 0.3 + features * 0.3)` | `0.65` |
| `traffic_quality_score` | Composite | `(1 - bounce_rate) * avg_session_time` | `0.78` |
| `negative_sentiment_score` | NLP | `sentiment_analyzer(ticket_text)` | `0.85` (very negative) |
| `commission_volatility` | Stats | `std(monthly_commissions)` | `1200.5` |

**Function Signature:**
```python
def engineer_features(df_raw: pd.DataFrame, network_df: pd.DataFrame = None) -> pd.DataFrame:
    """
    Takes raw partner data, computes all 18 engineered features.
    Returns DataFrame with all features ready for LightGBM.
    
    Args:
        df_raw: Raw partner data
        network_df: Network relationships (for network features)
        
    Returns:
        DataFrame with 18 features + partner_id
    """
    df = df_raw.copy()
    
    # Engagement features (5)
    df['login_count_30d'] = df['login_history'].apply(lambda x: len(x))
    df['login_trend_30d'] = df['login_history'].apply(compute_slope)
    df['days_since_last_interaction'] = (datetime.now() - df['last_interaction_date']).dt.days
    df['dashboard_usage_score'] = compute_composite_usage(df)
    df['asset_download_count_30d'] = df['download_history'].apply(lambda x: len(x))
    
    # Performance features (4)
    df['revenue_velocity'] = df['commission_history'].apply(compute_second_derivative)
    df['conversion_rate_wow'] = compute_week_over_week(df['conversion_rates'])
    df['traffic_quality_score'] = compute_traffic_quality(df)
    df['commission_trend_90d'] = df['commission_history'].apply(
        lambda x: compute_slope(x[-90:])
    )
    
    # Trust/Friction features (3)
    df['payment_delay_flag'] = df['payment_delay_days'] > 7
    df['unresolved_ticket_count'] = df['tickets'].apply(
        lambda x: len([t for t in x if t['status'] == 'open'])
    )
    df['negative_sentiment_score'] = df['ticket_texts'].apply(analyze_sentiment)
    
    # Network features (2) - only for Masters
    if network_df is not None:
        network_features = df.apply(
            lambda row: calculate_network_features(row, network_df, df),
            axis=1,
            result_type='expand'
        )
        df['subnetwork_avg_health_score'] = network_features['subnetwork_avg_health_score']
        df['subnetwork_recent_churn_count'] = network_features['subnetwork_recent_churn_count']
    else:
        df['subnetwork_avg_health_score'] = None
        df['subnetwork_recent_churn_count'] = None
    
    # Tier Risk features (2)
    df['tier_proximity_score'] = compute_tier_proximity(df['tier'], df['avg_commission_3m'])
    df['tenure_months'] = (datetime.now() - df['partnership_start_date']).dt.days / 30
    
    # Financial features (2)
    df['avg_commission_3m'] = df['commission_history'].apply(
        lambda x: np.mean(x[-90:]) if len(x) >= 90 else np.mean(x)
    )
    df['commission_volatility'] = df['commission_history'].apply(np.std)
    
    return df
```

**Verification:**
```python
# In data/feature_engineering.py
def validate_features(df):
    required_features = [
        'login_trend_30d', 'days_since_last_interaction',
        'revenue_velocity', 'conversion_rate_wow',
        # ... all 18
    ]
    
    for feat in required_features:
        assert feat in df.columns, f"Missing feature: {feat}"
        assert df[feat].isna().sum() == 0, f"NaNs in {feat}"
    
    print(f"✅ All {len(required_features)} features validated")
```

---

### 4. Golden Demo Records

**Agent:** `backend-specialist`

**File:** `data/golden_demo_records.py`

**Requirements:**

Hardcode 5 specific partners to guarantee demo scenario reliability:

```python
GOLDEN_RECORDS = [
    {
        'partner_id': 'P00001',
        'scenario': 'Tier Cliff Anxiety',
        'tier': 'Platinum',
        'avg_commission_3m': 5100,  # Just above $5k threshold
        'tier_proximity_score': 0.02,  # Close to drop
        'login_trend_30d': -0.4,  # Declining engagement
        'churn_label': True
    },
    {
        'partner_id': 'P00002',
        'scenario': 'Trust Erosion',
        'payment_delay_flag': True,
        'days_since_last_interaction': 18,
        'unresolved_ticket_count': 3,
        'negative_sentiment_score': 0.85,
        'churn_label': True
    },
    {
        'partner_id': 'P00003',
        'scenario': 'Network Contagion',
        'is_master_affiliate': True,
        'subnetwork_recent_churn_count': 4,
        'subnetwork_avg_health_score': 0.35,
        'churn_label': True
    },
    {
        'partner_id': 'P00004',
        'scenario': 'Brazil P2P Systemic',
        'region': 'Brazil',
        'payment_rail_type': 'P2P',
        'payment_delay_flag': True,
        'churn_label': True
    },
    {
        'partner_id': 'P00005',
        'scenario': 'Healthy (Control)',
        'tier': 'Gold',
        'login_trend_30d': 0.2,  # Growing
        'payment_delay_flag': False,
        'churn_label': False
    }
]
```

These are injected into the dataset to ensure predictable demo outcomes.

---

## 🔄 Integration Flow

```
1. Run docker-compose up → PostgreSQL ready
2. Run schema/*.sql → Tables created
3. Run synthetic_generator.py → 10,000 partners + interventions
4. Run feature_engineering.py → Add 18 computed features
5. Load to database → INSERT INTO partners
6. Verify → Query partners table, check feature distributions
```

---

## ✅ Verification Plan

### Automated Tests

**Test File:** `tests/test_day1_data.py`

```python
def test_database_connection():
    """Verify PostgreSQL is running and accessible"""
    conn = psycopg2.connect(DATABASE_URL)
    assert conn is not None

def test_schema_exists():
    """Verify all tables created"""
    tables = ['partners', 'interventions', 'predictions']
    for table in tables:
        result = query(f"SELECT COUNT(*) FROM {table}")
        assert result is not None

def test_synthetic_data_quality():
    """Verify data follows expected distributions"""
    df = pd.read_csv('data/partners.csv')
    assert len(df) == 10000
    assert 0.15 <= df['churn_label'].mean() <= 0.25  # 15-25% churn
    
    # Pareto check: top 20% should have 80% of revenue
    top_20_pct = df.nlargest(2000, 'avg_commission_3m')
    assert top_20_pct['avg_commission_3m'].sum() / df['avg_commission_3m'].sum() > 0.75

def test_feature_engineering():
    """Verify all 18 features computed"""
    df = pd.read_csv('data/partners_engineered.csv')
    required = 18
    assert len([c for c in df.columns if c not in ['partner_id', 'created_at']]) >= required

def test_golden_records():
    """Verify hardcoded demo partners exist"""
    df = pd.read_csv('data/partners.csv')
    golden_ids = ['P00001', 'P00002', 'P00003', 'P00004', 'P00005']
    for pid in golden_ids:
        assert pid in df['partner_id'].values
```

**Run:**
```bash
pytest tests/test_day1_data.py -v
```

### Manual Verification

**Checklist:**
- [ ] `docker-compose up` shows PostgreSQL running on port 5432
- [ ] `psql -h localhost -U admin -d deriv_churn -c "\dt"` lists 3 tables
- [ ] `python data/synthetic_generator.py` creates `partners.csv` with 10,000 rows
- [ ] Open `partners.csv` in Excel/Numbers: check distributions make sense
- [ ] `python data/feature_engineering.py` creates `partners_engineered.csv` with 18 features
- [ ] Query: `SELECT * FROM partners WHERE partner_id = 'P00001'` returns Tier Cliff demo record

---

## 📦 File Structure After Day 1

```
deriv-defensor/
├── docker-compose.yml          ← PostgreSQL container
├── schema/
│   ├── partners.sql            ← Partner table schema
│   ├── interventions.sql       ← Intervention history
│   └── predictions.sql         ← Learning loop table
├── data/
│   ├── synthetic_generator.py  ← 10k partner generator
│   ├── feature_engineering.py  ← 18-feature pipeline
│   ├── golden_demo_records.py  ← Hardcoded scenarios
│   ├── partners.csv            ← Raw output
│   └── partners_engineered.csv ← With features
├── tests/
│   └── test_day1_data.py       ← Validation tests
└── IMPLEMENTATION_PLAN.md
```

---

## 🚀 Agent Assignments

| Agent | Focus | Files |
|-------|-------|-------|
| **database-architect** | Schema design, docker-compose | `schema/*.sql`, `docker-compose.yml` |
| **backend-specialist** | Data generation, feature eng | `data/synthetic_generator.py`, `data/feature_engineering.py` |
| **test-engineer** | Validation, pytest setup | `tests/test_day1_data.py` |

---

## 🎯 Success Criteria

By end of Day 1:
- ✅ Local PostgreSQL running in Docker
- ✅ 10,000 synthetic partners with realistic Pareto distributions
- ✅ All 18 features engineered and validated
- ✅ 5 golden demo records hardcoded
- ✅ All tests passing: `pytest tests/test_day1_data.py`

**This establishes the foundation for Day 2: Base Model + SHAP**
