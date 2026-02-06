# Sentinel System - AI Partner Churn Predictor
## Project Context & Architecture

> **Status:** FINAL (Ready for Execution)
> **Architecture:** Sentinel System (Binary ML + Rule Engine + Agentic Reflection)
> **Stack:** Python, XGBoost, AWS Bedrock (Claude 3.5 Sonnet), Supabase

---

## 1. Executive Summary
**Project:** The Sentinel System
**Goal:** Prevent partner churn through "Correctness from Context" (DeepMind Principle)
**Core Innovation:** Combining **Binary ML** (for robust risk scoring) with a **Rule Engine** (for deterministic classification) and **Network Topology** (to stop contagion).

**Key Differentiators:**
- **Network Contagion Detection:** Treating Master Affiliates as graph nodes to predict downstream churn.
- **Explainable AI:** SHAP values mapped to human-readable "Reason Codes".
- **Agentic Intervention:** AWS Bedrock agents identifying "Emotional Drivers" vs. just numbers.

---

## 2. Deriv AI Team Alignment
This project embodies core Deriv AI principles:
1.  **Correctness from Context:** Features engineered from deep domain knowledge (e.g., Tier Cliff, Negative Carry-Forward).
2.  **Production-Ready:** XGBoost for reliability, Supabase for state management, strict "Target Leakage" firewalls.
3.  **Partner Enablement:** Moving from "Prediction" to "Intervention".

---

## 3. Churn & Risk Taxonomy (Refined)

The system identifies 4 distinct categories using a Hybrid approach:

| Category | Definition | Detection Method |
|----------|------------|------------------|
| **1. Contagion Churn** | Master Affiliate decays, infecting sub-network | **Rule Engine** (Network Graph) |
| **2. Involuntary Churn** | Compliance blocks, fraud, regulatory bans | **Rule Engine** (Status Flags) |
| **3. Passive Disengagement** | "Silent Killer" (stops promoting, keeps account) | **ML Model** (Velocity Features) |
| **4. Active Churn** | Rage-quit triggered by specific friction | **ML Model** (Friction Features) |

---

## 4. Feature Specification (QuantumBlack Approved)

**Total Features:** 18 (Optimized for Hackathon Viability)

### Tier 1: Financial Metrics (P0)
- **`tier_proximity_score`**: Distance to "Tier Cliff" (e.g., Platinum -> Gold drop).
- **`whale_concentration_risk`**: % of partner revenue from single client (Fintech unique).
- **`cpa_sensitivity_score`**: Exposure to competitor arbitrage (Exness vs Deriv).
- **`avg_commission_3m`**: Rolling average (Power Law distributed).

### Tier 2: Network Topology (Blue Ocean)
- **`is_master_affiliate`**: Graph node flag.
- **`subnetwork_avg_health_score`**: Health of downstream partners.
- **`subnetwork_recent_churn_count`**: Leading indicator of Master disengagement.

### Tier 3: Operational Friction (P0)
- **`withdrawal_failure_rate`**: "Entrapment" signal (P2P/Payment friction).
- **`avg_kyc_time_referrals`**: "Operational Gap" signal (Conversion friction).
- **`support_tickets_pending`**: "Powerlessness" signal.

### Tier 4: Infrastructure & Context (Scenario Enablers)
- **`payment_rail_type`**: [P2P, Crypto, Bank, Agent] - Enables **Brazil P2P** scenario.
- **`region`**: [Brazil, EU, UK, Nigeria, SE_Asia] - Enables **EU Regulatory** scenario.

### Tier 5: Engagement (Early Warning)
- **`login_velocity_7d`**: Velocity of engagement change.
- **`link_generation_30d`**: Purest intent signal (New Links = Marketing).
- **`days_since_asset_download`**: Marketing dormancy.
- **`referral_first_loss_rate_7d`**: Reputation risk (Partner's clients losing money).

### Tier 6: Behavioral
- **`support_ticket_sentiment_score`**: Trust erosion signal.
- **`tenure_months`**: "Betrayal" sensitivity factor.

> **Implementation Note:** All "Composite Metrics" (LPI, TFS, CDR) were removed as they are redundant for XGBoost.

---

## 5. System Architecture

### A. The "Sentinel" Pipeline
```
[Data Ingestion] -> [Feature Engineering] -> [Dual-Layer Inference]
                                                  |
                          +-----------------------+-----------------------+
                          |                       |                       |
                  [ML Layer (XGBoost)]    [Rule Engine (Hard Logic)]      |
                          |                       |                       |
                          v                       v                       |
                  [Churn Probability]     [Class: Contagion/InVol]        |
                          |                       |                       |
                          +-----------+-----------+                       |
                                      |                                   |
                                      v                                   |
                            [Supabase State Store]                        |
                                      |                                   |
                            [Agentic Reflection]                          |
                            (AWS Bedrock / Claude)                        |
                                      |                                   |
                            [Emotional Driver & Action]                   |
```

### B. Technical Stack
- **ML Engine:** XGBoost (Binary classification)
- **Reasoning Engine:** AWS Bedrock (Claude 3.5 Sonnet) via `boto3`
- **Database:** Supabase (PostgreSQL) - Tables: `partners`, `partner_health`, `agent_decisions`
- **Dashboard:** Streamlit (Network Graph, Geo Heatmap, Intervention Queue)

---

## 6. MVP Scope & Components

### 1. Synthetic Data Generator (Power Law Edition)
*   **Crucial:** Must use `numpy.random.pareto()` for financial metrics. Gaussian distributions will fail to capture "Whale" dynamics.
*   **Golden Records:** Hard-coded specific partners (#10001-10003) to guarantee demo scenario reliability.

### 2. Dual-Layer Prediction System
*   **Layer 1:** XGBoost for `churn_probability` (focus on Passive Disengagement).
*   **Layer 2:** Python Rule Engine for `churn_reason` (focus on Contagion/Systemic).

### 3. Agentic Reflection (The "Brain")
*   Analyzes ML output + Feature context.
*   Determines **Emotional Driver** (Financial Friction, Trust Erosion, Operational Gap).
*   Selects **Intervention** (e.g., "Tier Grace Period", "Fast-Track Withdrawal").
*   **Compliance Firewall:** Blocks interventions for "Involuntary" churn (Fraud/Compliance).

### 4. Interactive Dashboard (3 Views)
*   **Network Topology:** Visualizing Master Affiliate contagion risks.
*   **Geographic Heatmap:** Detecting systemic regional issues (e.g., Brazil P2P).
*   **Intervention Queue:** Prioritized list for retention agents.

---

## 7. Cohort Scenarios (Demo Narratives)

### Scenario 1: Brazil P2P Outage
*   **Feature Signature:** `Region=Brazil` + `Rail=P2P` + `Withdrawal_Fail > 0.2`.
*   **Outcome:** Systemic Alert -> "Switch to Crypto" intervention.

### Scenario 2: Master Affiliate Contagion
*   **Feature Signature:** `Is_Master=1` + `Sub_Health < 40`.
*   **Outcome:** Network Risk Alert -> "VIP Account Manager" intervention.

### Scenario 3: The "Tier Cliff"
*   **Feature Signature:** `Tier_Proximity < 0.05` + `Velocity < -0.5`.
*   **Outcome:** "Performance Anxiety" -> "15-Day Grace Period" intervention.

---

## 8. Development Timeline (Pre-Hackathon)

1.  **Golden Record Generation:** Define the 3 demo heroes.
2.  **Synthetic Data Engine:** Build 10,000 partner dataset (Pareto distributed).
3.  **Model Training:** Train XGBoost, save as artifact.
4.  **Supabase Setup:** Schema migration.

**Ready for Day 1 Implementation.**