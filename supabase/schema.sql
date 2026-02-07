-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 1. Partners Table (Core Profile + Risk Metrics)
CREATE TABLE partners (
    partner_id TEXT PRIMARY KEY,
    region TEXT NOT NULL,
    tier TEXT NOT NULL CHECK (tier IN ('Bronze', 'Silver', 'Gold', 'Platinum')),
    join_date DATE,
    status TEXT DEFAULT 'Active',
    
    -- Risk Metrics (Updated Daily)
    churn_prob FLOAT DEFAULT 0.0,
    risk_category TEXT, -- 'High', 'Medium', 'Low'
    urgency_score INT,
    
    -- Business Metrics
    ltv FLOAT DEFAULT 0.0,
    avg_commission_3m FLOAT DEFAULT 0.0,
    
    -- Behavioral Features
    login_trend_30d FLOAT,
    payment_delay_flag BOOLEAN DEFAULT FALSE,
    unresolved_ticket_count INT DEFAULT 0,
    
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Network Relationships (Contagion Analysis)
CREATE TABLE network_relationships (
    master_id TEXT REFERENCES partners(partner_id),
    sub_affiliate_id TEXT REFERENCES partners(partner_id),
    relationship_strength FLOAT, -- 0.0 to 1.0
    PRIMARY KEY (master_id, sub_affiliate_id)
);

-- 3. Interventions (Audit Log)
CREATE TABLE interventions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    partner_id TEXT REFERENCES partners(partner_id),
    action_type TEXT NOT NULL, -- 'Email', 'Call', 'Bonus', 'Meeting'
    status TEXT DEFAULT 'Pending', -- 'Pending', 'Completed', 'Failed'
    
    -- GenAI Content
    explanation_text TEXT,
    email_draft TEXT,
    
    -- Metadata
    performed_by TEXT DEFAULT 'System',
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    outcome_label TEXT -- 'Saved', 'Churned' (updated later)
);

-- 4. Daily ROI Stats (For Dashboard Header)
CREATE TABLE daily_stats (
    date DATE PRIMARY KEY DEFAULT CURRENT_DATE,
    total_partners_at_risk INT,
    total_revenue_exposed FLOAT,
    total_recovered_revenue FLOAT,
    intervention_success_rate FLOAT
);

-- 5. Agent Summaries (External Agent Input)
CREATE TABLE agent_summaries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    partner_id TEXT REFERENCES partners(partner_id),
    churn_tendency FLOAT, -- 0.0 to 1.0
    summary TEXT,
    metrics JSONB, -- Flexible JSON for sentiment, competitor info, etc.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Row Level Security (RLS) - Enable Read Access for Public/Anon (For Demo)
ALTER TABLE partners ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public Read Partners" ON partners FOR SELECT USING (true);
CREATE POLICY "Public Insert Partners" ON partners FOR INSERT WITH CHECK (true);

ALTER TABLE interventions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public Read Interventions" ON interventions FOR SELECT USING (true);
CREATE POLICY "Public Insert Interventions" ON interventions FOR INSERT WITH CHECK (true);

ALTER TABLE network_relationships ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public Read Networks" ON network_relationships FOR SELECT USING (true);
CREATE POLICY "Public Insert Networks" ON network_relationships FOR INSERT WITH CHECK (true);

ALTER TABLE daily_stats ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public Read Stats" ON daily_stats FOR SELECT USING (true);
CREATE POLICY "Public Insert Stats" ON daily_stats FOR INSERT WITH CHECK (true);

ALTER TABLE agent_summaries ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Public Read Agent Summaries" ON agent_summaries FOR SELECT USING (true);
CREATE POLICY "Public Insert Agent Summaries" ON agent_summaries FOR INSERT WITH CHECK (true);
