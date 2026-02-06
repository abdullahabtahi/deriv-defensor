-- ============================================================================
-- AI Partner Churn Predictor - Database Schema
-- Day 1: Data Foundation
-- ============================================================================
-- 
-- This schema supports the 6 criteria:
-- 1. Accurate Prediction → partners table with 18 features
-- 2. Cohort Risk Detection → regional/tier grouping via indexes
-- 3. Intervention Timing → predictions table with outcome tracking
-- 4. Pattern Discovery → churn_scenario labels for validation
-- 5. Learning from Outcomes → predictions + interventions feedback loop
-- 6. Proactive Recommendations → uplift_signal for CausalML training
--
-- ============================================================================

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================================================
-- 1. PARTNERS TABLE - Core partner data with 18 features
-- ============================================================================
CREATE TABLE partners (
    partner_id VARCHAR(50) PRIMARY KEY,
    
    -- Demographic
    region VARCHAR(50) NOT NULL,
    payment_rail_type VARCHAR(50) NOT NULL,
    is_master_affiliate BOOLEAN DEFAULT FALSE,
    tier VARCHAR(20) NOT NULL,
    
    -- Engagement (5 features)
    login_count_30d INTEGER DEFAULT 0,
    login_trend_30d DECIMAL(5,3),              -- slope: negative = declining
    days_since_last_interaction INTEGER DEFAULT 0,
    dashboard_usage_score DECIMAL(5,4),        -- 0-1 composite
    asset_download_count_30d INTEGER DEFAULT 0,
    
    -- Performance (4 features)
    revenue_velocity DECIMAL(10,2),            -- 2nd derivative: negative = decelerating
    conversion_rate_wow DECIMAL(6,4),          -- week-over-week change
    traffic_quality_score DECIMAL(5,4),        -- 0-1 composite
    commission_trend_90d DECIMAL(5,3),         -- 90-day slope
    
    -- Trust/Friction (3 features)
    payment_delay_flag BOOLEAN DEFAULT FALSE,
    unresolved_ticket_count INTEGER DEFAULT 0,
    negative_sentiment_score DECIMAL(3,2),     -- 0-1, from support NLP
    
    -- Network (2 features - only for Masters)
    subnetwork_avg_health_score DECIMAL(5,2), -- 0-100 scale
    subnetwork_recent_churn_count INTEGER DEFAULT 0,
    
    -- Tier Risk (2 features)
    tier_proximity_score DECIMAL(5,4),         -- 0-1, distance to demotion
    tenure_months INTEGER DEFAULT 0,
    
    -- Financial (2 features)
    avg_commission_3m DECIMAL(12,2),
    commission_volatility DECIMAL(12,2),       -- std deviation
    
    -- Ground truth labels
    churn_label BOOLEAN DEFAULT FALSE,
    churn_scenario VARCHAR(50),                -- Trust_Erosion, Tier_Cliff, etc.
    
    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Performance indexes
CREATE INDEX idx_partners_churn ON partners(churn_label);
CREATE INDEX idx_partners_region ON partners(region);
CREATE INDEX idx_partners_tier ON partners(tier);
CREATE INDEX idx_partners_master ON partners(is_master_affiliate);
CREATE INDEX idx_partners_scenario ON partners(churn_scenario);

-- ============================================================================
-- 2. INTERVENTIONS TABLE - Historical intervention outcomes for CausalML
-- ============================================================================
CREATE TABLE interventions (
    intervention_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    partner_id VARCHAR(50) NOT NULL REFERENCES partners(partner_id) ON DELETE CASCADE,
    
    -- Intervention details
    intervention_type VARCHAR(50) NOT NULL,    -- 'call', 'email', 'none'
    intervention_date TIMESTAMP NOT NULL,
    
    -- Outcomes (for CausalML training)
    outcome VARCHAR(20),                       -- 'Retained', 'Churned'
    uplift_signal DECIMAL(5,3),                -- Hidden ground truth: -0.5 to 0.2
    outcome_recorded_at TIMESTAMP,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT NOW()
);

-- Performance indexes
CREATE INDEX idx_interventions_partner ON interventions(partner_id);
CREATE INDEX idx_interventions_type ON interventions(intervention_type);
CREATE INDEX idx_interventions_date ON interventions(intervention_date);

-- ============================================================================
-- 3. PREDICTIONS TABLE - Learning loop with outcome tracking
-- ============================================================================
CREATE TABLE predictions (
    prediction_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    partner_id VARCHAR(50) NOT NULL REFERENCES partners(partner_id) ON DELETE CASCADE,
    
    -- Model predictions
    churn_probability DECIMAL(5,4) NOT NULL,   -- 0.0000 to 1.0000
    top_churn_factors JSONB,                   -- SHAP-derived: {"login_trend": -0.15, ...}
    recommended_intervention VARCHAR(50),      -- 'call', 'email', 'none'
    uplift_score DECIMAL(5,3),                 -- Expected lift from intervention
    
    -- Model metadata
    model_version VARCHAR(20) NOT NULL,
    predicted_at TIMESTAMP DEFAULT NOW(),
    
    -- Outcome tracking (populated T+30 days)
    actual_intervention VARCHAR(50),
    actual_outcome VARCHAR(20),                -- 'Retained', 'Churned'
    outcome_recorded_at TIMESTAMP,
    
    -- Learning loop flags
    feedback_incorporated BOOLEAN DEFAULT FALSE
);

-- Performance indexes
CREATE INDEX idx_predictions_partner ON predictions(partner_id);
CREATE INDEX idx_predictions_date ON predictions(predicted_at);
CREATE INDEX idx_predictions_version ON predictions(model_version);
CREATE INDEX idx_predictions_feedback ON predictions(feedback_incorporated);

-- ============================================================================
-- 4. NETWORK_RELATIONSHIPS TABLE - Master → Sub-Affiliate graph
-- ============================================================================
CREATE TABLE network_relationships (
    relationship_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    master_affiliate_id VARCHAR(50) NOT NULL REFERENCES partners(partner_id) ON DELETE CASCADE,
    sub_affiliate_id VARCHAR(50) NOT NULL REFERENCES partners(partner_id) ON DELETE CASCADE,
    
    -- Relationship metadata
    recruited_at TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Constraint: sub-affiliate can only have one parent (tree structure)
    CONSTRAINT unique_sub_affiliate UNIQUE (sub_affiliate_id),
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- Performance indexes for graph traversal
CREATE INDEX idx_network_master ON network_relationships(master_affiliate_id);
CREATE INDEX idx_network_sub ON network_relationships(sub_affiliate_id);
CREATE INDEX idx_network_active ON network_relationships(is_active);

-- ============================================================================
-- 5. COHORT_ANOMALIES TABLE - For cohort risk detection
-- ============================================================================
CREATE TABLE cohort_anomalies (
    anomaly_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Cohort definition
    cohort_type VARCHAR(50) NOT NULL,          -- 'region', 'tier', 'payment_rail'
    cohort_value VARCHAR(100) NOT NULL,        -- 'LATAM', 'Silver', 'Crypto'
    
    -- Anomaly metrics
    baseline_churn_rate DECIMAL(5,4),          -- Historical average
    current_churn_rate DECIMAL(5,4),           -- Current period
    z_score DECIMAL(6,3),                      -- Standard deviations from mean
    partner_count INTEGER,                     -- Cohort size
    
    -- Alert metadata
    detected_at TIMESTAMP DEFAULT NOW(),
    severity VARCHAR(20),                      -- 'warning', 'critical'
    acknowledged BOOLEAN DEFAULT FALSE,
    
    CONSTRAINT unique_cohort_detection UNIQUE (cohort_type, cohort_value, detected_at)
);

CREATE INDEX idx_cohort_type ON cohort_anomalies(cohort_type);
CREATE INDEX idx_cohort_severity ON cohort_anomalies(severity);

-- ============================================================================
-- 6. MODEL_VERSIONS TABLE - Model registry for A/B testing
-- ============================================================================
CREATE TABLE model_versions (
    version_id VARCHAR(20) PRIMARY KEY,
    
    -- Model metadata
    model_type VARCHAR(50) NOT NULL,           -- 'lightgbm_churn', 'causal_tlearner'
    trained_at TIMESTAMP NOT NULL,
    training_samples INTEGER,
    
    -- Performance metrics
    auc_roc DECIMAL(5,4),
    precision_score DECIMAL(5,4),
    recall_score DECIMAL(5,4),
    
    -- Status
    is_active BOOLEAN DEFAULT FALSE,
    promoted_at TIMESTAMP,
    retired_at TIMESTAMP,
    
    -- Artifact path
    model_path VARCHAR(500)
);

CREATE INDEX idx_model_active ON model_versions(is_active);

-- ============================================================================
-- VIEWS - Convenience views for dashboard
-- ============================================================================

-- High-risk partners requiring intervention
CREATE VIEW v_high_risk_partners AS
SELECT 
    p.partner_id,
    p.region,
    p.tier,
    p.avg_commission_3m,
    pred.churn_probability,
    pred.top_churn_factors,
    pred.recommended_intervention,
    pred.uplift_score
FROM partners p
JOIN (
    SELECT DISTINCT ON (partner_id) *
    FROM predictions
    ORDER BY partner_id, predicted_at DESC
) pred ON p.partner_id = pred.partner_id
WHERE pred.churn_probability > 0.65
AND p.churn_label = FALSE;

-- Learning loop accuracy tracking
CREATE VIEW v_model_accuracy AS
SELECT 
    model_version,
    COUNT(*) as total_predictions,
    SUM(CASE WHEN 
        (churn_probability > 0.5 AND actual_outcome = 'Churned') OR
        (churn_probability <= 0.5 AND actual_outcome = 'Retained')
        THEN 1 ELSE 0 END) as correct_predictions,
    ROUND(
        SUM(CASE WHEN 
            (churn_probability > 0.5 AND actual_outcome = 'Churned') OR
            (churn_probability <= 0.5 AND actual_outcome = 'Retained')
            THEN 1 ELSE 0 END)::DECIMAL / NULLIF(COUNT(*), 0), 
        4
    ) as accuracy
FROM predictions
WHERE actual_outcome IS NOT NULL
GROUP BY model_version;

-- Network health summary for masters
CREATE VIEW v_network_health AS
SELECT 
    m.partner_id as master_id,
    m.region,
    m.tier,
    COUNT(nr.sub_affiliate_id) as total_subs,
    SUM(CASE WHEN s.churn_label THEN 1 ELSE 0 END) as churned_subs,
    ROUND(AVG(CASE WHEN s.churn_label THEN 0 ELSE 100 END), 2) as avg_health_score
FROM partners m
JOIN network_relationships nr ON m.partner_id = nr.master_affiliate_id
JOIN partners s ON nr.sub_affiliate_id = s.partner_id
WHERE m.is_master_affiliate = TRUE
AND nr.is_active = TRUE
GROUP BY m.partner_id, m.region, m.tier;

-- ============================================================================
-- FUNCTIONS - Utility functions
-- ============================================================================

-- Function to recalculate network features for a master affiliate
CREATE OR REPLACE FUNCTION update_network_features(p_master_id VARCHAR(50))
RETURNS VOID AS $$
DECLARE
    v_avg_health DECIMAL(5,2);
    v_churn_count INTEGER;
BEGIN
    SELECT 
        ROUND(AVG(CASE WHEN s.churn_label THEN 0 ELSE 100 END), 2),
        SUM(CASE WHEN s.churn_label THEN 1 ELSE 0 END)
    INTO v_avg_health, v_churn_count
    FROM network_relationships nr
    JOIN partners s ON nr.sub_affiliate_id = s.partner_id
    WHERE nr.master_affiliate_id = p_master_id
    AND nr.is_active = TRUE;
    
    UPDATE partners 
    SET 
        subnetwork_avg_health_score = COALESCE(v_avg_health, 100.0),
        subnetwork_recent_churn_count = COALESCE(v_churn_count, 0),
        updated_at = NOW()
    WHERE partner_id = p_master_id;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- SEED DATA - Golden demo records (5 hardcoded scenarios)
-- ============================================================================
-- These will be inserted by the synthetic data generator
-- But documented here for reference:
--
-- P00001: Tier Cliff Anxiety (high LTV, close to demotion)
-- P00002: Trust Erosion (payment delay + silence)  
-- P00003: Network Contagion (master with churning subs)
-- P00004: Active Churn (competitor signals)
-- P00005: Passive Disengagement (declining engagement)
-- ============================================================================
